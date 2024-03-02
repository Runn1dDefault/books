from fastapi import APIRouter

import schemas
from db import crud
from dependencies import PageDepends, DBDepends


router = APIRouter(
    prefix="/books",
    tags=["books"],
    responses={404: {"description": "Not found"}},
)


@router.get("/books", response_model=list[schemas.ShortBookSchema])
async def book_list(params: PageDepends, db: DBDepends):
    limit, skip, search = params['limit'], params['skip'], params["search"]
    return await crud.get_book_list(db, limit=limit, skip=skip, search_term=search)

