from typing import Annotated
from sqlmodel import create_engine, Session, SQLModel
from fastapi import Depends
from .settings import get_settings
settings = get_settings()

print(settings.database_url)
engine = create_engine(settings.database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
