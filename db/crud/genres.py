from uuid import UUID

from sqlalchemy import select, literal
from sqlalchemy.orm import selectinload, joinedload, aliased
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Genre
from db.utils import get_objects_from_rows


async def get_base_genres_list(async_db: AsyncSession, limit: int, skip: int = 0):
    query = (
        select(Genre)
        .where(Genre.parent_id.is_(None))
        .order_by(Genre.title)
        .limit(limit).offset(skip)
    )
    return get_objects_from_rows(await async_db.execute(query))


async def get_genre_children(async_db: AsyncSession, genre_id: UUID, limit: int, skip: int = 0):
    query = (
        select(Genre)
        .where(Genre.parent_id == genre_id)
        .order_by(Genre.title)
        .limit(limit).offset(skip)
    )
    return get_objects_from_rows(await async_db.execute(query))


async def get_genre_parents(async_db: AsyncSession, genre_id: UUID):
    async with async_db.begin():
        parent_alias = aliased(Genre)

        cte = select(Genre).where(Genre.id == genre_id).cte(name="genre_hierarchy", recursive=True)
        cte = cte.union_all(select(parent_alias).join(parent_alias.children))
        query = select(cte).where(cte.c.id != genre_id)
        return await async_db.execute(query)
