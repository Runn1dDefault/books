from typing import Any
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.orm.util import AliasedClass
from sqlalchemy.sql.selectable import Select

from db.models import Book, BookImage, Author, Genre


def get_books_list_stmt() -> tuple[AliasedClass[Book], Select[Any]]:
    """
    ex sql for filtering by genre_id with limit 10 and offset 0:
        SELECT
            b.id,
            b.title,
            b.publisher,
            b.released_date,
            (
                SELECT
                    img.image
                FROM
                    book_image img
                WHERE
                    img.book_id = b.id
                LIMIT 1
            ) as image,
            ARRAY_AGG(
                JSON_BUILD_OBJECT(
                    'id'::text, a.id,
                    'fullname'::text, a.first_name || ' ' || a.last_name
                )
            ) as authors,
            ARRAY_AGG(
                JSON_BUILD_OBJECT(
                    'id'::text, g.id,
                    'title'::text, g.title
                )
            ) as genres
        FROM
            book b
        INNER JOIN book_author ba ON b.id = ba.book_id
        INNER JOIN author a ON ba.author_id = a.id
        INNER JOIN book_genre bg ON b.id = bg.book_id
        INNER JOIN genre g ON bg.genre_id = g.id
        WHERE
            g.id = genre_id
        GROUP BY
            b.id
        ORDER BY
            b.released_date
        LIMIT 10 OFFSET 0;
    """

    book_alias = aliased(Book, name='b')
    return book_alias, (
        select(
            book_alias.id,
            book_alias.title,
            book_alias.publisher,
            book_alias.released_date,
            func.coalesce(
                (
                    select(BookImage.image)
                    .where(BookImage.book_id == book_alias.id)
                    .limit(1)
                ), ''
            ).label('image'),
            func.coalesce(
                func.array_agg(
                    func.json_build_object(
                        'id', Author.id,
                        'fullname', func.concat(Author.first_name, ' ', Author.last_name),
                    )
                ), []
            ).label('authors'),
            func.coalesce(
                func.array_agg(
                    func.json_build_object(
                        'id', Genre.id,
                        'title', Genre.title
                    )
                ), []
            ).label('genres'),
        )
        .select_from(book_alias)
        .join(book_alias.authors)
        .join(book_alias.genres)
        .group_by(book_alias.id)
    )


async def get_book_list(
    async_db: AsyncSession,
    limit: int,
    skip: int = 0,
    genre_id: UUID | str = None,
    search_term: str = None
):
    book_alias, stmt = get_books_list_stmt()

    if genre_id:
        stmt = stmt.where(Genre.id == genre_id)

    if search_term:
        stmt = stmt.where(book_alias.title.ilike(f"%{search_term}%"))

    stmt = stmt.limit(limit).offset(skip)
    return await async_db.execute(stmt)
