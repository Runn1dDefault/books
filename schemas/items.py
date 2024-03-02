from decimal import Decimal
from datetime import datetime
from uuid import UUID
from typing import Any

from pydantic import BaseModel


class OrmSchema(BaseModel):
    id: UUID

    class Config:
        orm_mode = True


class GenreSchema(OrmSchema):
    title: str
    description: str | None = None


class BookAuthorSchema(OrmSchema):
    role: str
    # person: PersonSchema
    is_main: bool = False


class AuthorSchema(OrmSchema):
    fullname: str


class ShortBookSchema(OrmSchema):
    title: str 
    released_date: datetime
    image: str | None = None
    authors: list[AuthorSchema] = []
    publisher: str | None = None
    genres: list[GenreSchema] = []
