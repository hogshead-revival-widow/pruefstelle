from threading import Thread
from time import sleep
import io
import os

from fastapi import FastAPI, Request
from fastapi_pagination import add_pagination

# needed for clean client geneartion
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from .routes import main_router
from .database.config import create_all
from .database import errors
from .config import settings
from .tasks import update_status


def read(*paths, **kwargs):
    """Read the contents of a text file safely."""
    content = ""
    with io.open(
        os.path.join(os.path.dirname(__file__), *paths),
        encoding=kwargs.get("encoding", "utf8"),
    ) as open_file:
        content = open_file.read().strip()
    return content


app = FastAPI(
    title=settings.about.title,
    version=read("VERSION"),
    contact=settings.about.contact,
    redoc_url=None,
    swagger_ui_parameters=settings.about.swagger_ui_parameters,
)


app.include_router(main_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.server.cors_origins,  # type: ignore # must be set, otherwise newer chrome versions error out
    allow_credentials=settings.get("server.cors_allow_credentials", True),  # type: ignore
    allow_methods=settings.get("server.cors_allow_methods", ["*"]),  # type: ignore
    allow_headers=settings.get("server.cors_allow_headers", ["*"]),  # type: ignore
)


@app.on_event("startup")
def create_tables():
    create_all()


@app.on_event("startup")
def start_update_status():
    def background_task(seconds: int):
        while True:
            sleep(seconds)
            update_status()

    repeat_every_seconds = 60
    daemon = Thread(
        target=background_task,
        args=(repeat_every_seconds,),
        daemon=True,
        name="Update status",
    )
    daemon.start()


@app.exception_handler(errors.CRUDError)
async def crud_exception_handler(request: Request, e: errors.CRUDError):

    content = {"detail": f"{e.user_message} ({e.name})"}
    if isinstance(e, errors.IDError):
        return JSONResponse(status_code=400, content=content)
    if isinstance(e, errors.NotUniqueError):
        return JSONResponse(status_code=400, content=content)
    return JSONResponse(status_code=500, content=content)


add_pagination(app)


# uncomment for clean  client code generation
def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.

    Should be called only after all routes have been added.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name


use_route_names_as_operation_ids(app)
