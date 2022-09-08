import json
from uuid import UUID


from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from pydantic import parse_obj_as
import typer
import uvicorn
from pydantic import EmailStr

from .config import settings
from .database.config import SessionLocal, create_all
from .database import crud
from . import database
from . import schemas


cli = typer.Typer(name="pruefstelle API")


@cli.command()
def run(
    port: int = settings.server.port,  # type: ignore
    host: str = settings.server.host,  # type: ignore
    log_level: str = settings.server.log_level,  # type: ignore
    reload: bool = settings.server.reload,  # type: ignore
    populate_if_empty=True,
):  # pragma: no cover

    if populate_if_empty:
        try:
            session = SessionLocal()
            case_categories = crud.category.get_categories(
                session, schemas.CategoryType.CaseCategory
            )
            has_been_populated = len(case_categories) > 0
            if not has_been_populated:
                # database exists, but hasn't been populated
                populate()
        except OperationalError:
            # database doesn't exist
            populate()

    """Start server"""
    uvicorn.run(
        "pruefstelle.app:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command()
def create_user(
    email: str, password: str, password_confirm: str, superuser: bool = False
):
    """Create user"""

    # make sure the db exists
    create_all()

    try:
        if password != password_confirm:
            raise ValueError("password mismatch")
        user = schemas.UserCreate(email=EmailStr(email), password=password)  # type: ignore
        with SessionLocal() as session:
            db_user = crud.create_user(session, user, superuser)
    except database.NotUniqueError:
        return typer.echo(f"Error: User '{email} exists")
    except ValueError as v:
        if "password" in str(v):
            typer.echo("Error: Passwords don't match")
            return None
        typer.echo(f"Error: '{email}' is not an email")
        return None

    typer.echo(f"Created: {db_user.email}")
    return db_user


def create_category(
    session: Session,
    name: str,
    discriminator: schemas.CategoryType,
    ndb_norm_id: Optional[int] = None,
    source_id: Optional[UUID] = None,
    verbose=False,
    exist_ok=False,
):
    category = parse_obj_as(
        schemas.CategoryCreate,
        dict(name=name, discriminator=discriminator, ndb_norm_id=ndb_norm_id),
    )
    if discriminator == schemas.CategoryType.ExternalIDCategory:
        category.source_id = source_id

    category = crud.create_category(session, category)
    if category is None and not exist_ok:
        typer.echo(f"Error: Couldn't create: {name} ({discriminator})")
        return None
    if verbose:
        typer.echo(f"Created:  {name} ({discriminator})")
    return category


@cli.command()
def populate(verbose=False, exist_ok=True):
    """Populate database"""
    typer.echo("Populating...")

    gone_wrong = 0

    # make sure the db exists
    create_all()

    created_categories_by_name = dict()

    with open("settings/fixed_categories.json") as f:
        categories = json.load(f)

    if verbose:
        typer.echo("-" * 36)
        typer.echo("Creating categories\n")
    with SessionLocal() as session:
        for discriminator in categories:
            discriminator = schemas.CategoryType(discriminator)
            for category in categories[discriminator]:
                name = category["name"]
                db_category = crud.get_category_by_name(session, name, discriminator)
                if db_category is not None and not exist_ok:
                    typer.echo(f"Warning: Didn't create category '{name}'")
                    typer.echo("  It seems to exist")
                    typer.echo(f"  -> {db_category.id}")
                    gone_wrong += 1
                    continue
                ndb_norm_id = category.get("ndb_norm_id", None)
                source = category.get("source", None)
                source_id = None
                if source is not None:
                    source_id = created_categories_by_name[source["name"]].id
                created_category = create_category(
                    session,
                    name=name,
                    discriminator=discriminator,
                    ndb_norm_id=ndb_norm_id,
                    source_id=source_id,
                    verbose=verbose,
                    exist_ok=exist_ok,
                )
                if created_category is not None:
                    created_categories_by_name[created_category.name] = created_category
                    if not exist_ok:
                        gone_wrong += 1

    if verbose:
        typer.echo("-" * 36)
        typer.echo("\n")

        if gone_wrong > 0:
            typer.echo(f"There were warning(s) and/or errors ({gone_wrong})")
            typer.echo(" -> See above for more information")

        typer.echo("\nDone!\n")
