from datetime import datetime, date
from decimal import Decimal
from uuid import UUID, uuid4

from sqlalchemy import MetaData, String, Table, Column, ForeignKey, DECIMAL, UniqueConstraint, Uuid, \
    PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata_obj = MetaData(naming_convention=convention)
DeclarativeBase = declarative_base(metadata=metadata_obj)


class BaseModel(DeclarativeBase):
    __abstract__ = True

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)


genre_book_association = Table(
    "book_genre",
    BaseModel.metadata,
    Column("genre_id", ForeignKey("genre.id", ondelete="CASCADE")),
    Column("book_id", ForeignKey("book.id", ondelete="CASCADE"))
)


class Genre(BaseModel):
    __tablename__ = "genre"

    id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(nullable=True)

    # Relations
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("genre.id", ondelete="SET NULL"), nullable=True)
    parent: Mapped['Genre'] = relationship(remote_side=[id], back_populates='children')
    children: Mapped[list['Genre']] = relationship()
    
    books: Mapped[list['Book']] = relationship(secondary=genre_book_association, back_populates='genres')


book_author_association = Table(
    "book_author",
    BaseModel.metadata,
    Column("book_id", ForeignKey("book.id", ondelete="CASCADE"), primary_key=True),
    Column("author_id", ForeignKey("author.id", ondelete="CASCADE"), primary_key=True)
)


class Author(BaseModel):
    __tablename__ = "author"

    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    # Relations
    books: Mapped[list['Book']] = relationship(secondary=book_author_association, back_populates='authors')


class Book(BaseModel):
    __tablename__ = "book"

    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    released_date: Mapped[date] = mapped_column()
    publisher: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    modified_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    images: Mapped[list['BookImage']] = relationship(back_populates="book")
    authors: Mapped[list['Author']] = relationship(secondary=book_author_association, back_populates="books")
    genres: Mapped[list['Genre']] = relationship(secondary=genre_book_association, back_populates="books")


class BookImage(BaseModel):
    __tablename__ = "book_image"

    image: Mapped[str] = mapped_column(String(100), unique=True)

    # Relations
    book_id: Mapped[UUID] = mapped_column(ForeignKey("book.id", ondelete="CASCADE"))
    book: Mapped['Book'] = relationship(back_populates="images")
