from uuid import UUID
from fastapi import APIRouter

import schemas
from db import crud
from dependencies import PageDepends, DBDepends


router = APIRouter(
    prefix="/genres",
    tags=["genres"],
    responses={404: {"description": "Not found"}},
)


@router.get("/base", response_model=list[schemas.GenreSchema])
async def base_genres(params: PageDepends, db: DBDepends):
    limit, skip = params['limit'], params['skip']
    return await crud.get_base_genres_list(db, limit=limit, skip=skip)


@router.get("/children/{genre_id}", response_model=list[schemas.GenreSchema])
async def genre_children(genre_id: UUID, params: PageDepends, db: DBDepends):
    limit, skip = params['limit'], params['skip']
    return await crud.get_genre_children(db, genre_id=genre_id, limit=limit, skip=skip)


@router.get("/parents/{genre_id}", response_model=list[schemas.GenreSchema])
async def genre_parents(genre_id: UUID, db: DBDepends):
    return await crud.get_genre_parents(db, genre_id=genre_id)


@router.get("/{genre_id}/books", response_model=list[schemas.GenreSchema])
async def genre_books(genre_id: UUID, params: PageDepends, db: DBDepends):
    limit, skip, search = params['limit'], params['skip'], params["search"]
    return await crud.get_book_list(db, genre_id=genre_id, limit=limit, skip=skip, search_term=search)
