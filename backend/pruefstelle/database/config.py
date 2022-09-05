from fastapi import Depends
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, registry

from ..config import settings


engine = create_engine(
    url=settings.db.uri,  # type: ignore
    echo=False,  # settings.db.echo # type: ignore
    connect_args=settings.db.connect_args,  # type: ignore
    future=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

mapper_registry = registry()


def create_all():
    mapper_registry.metadata.create_all(bind=engine)


def get_session():
    with SessionLocal() as session:
        yield session


ActiveSession = Depends(get_session)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in settings.db.uri:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
