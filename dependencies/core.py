from config import MAX_PAGE_SIZE
from db.connections import db_session_manager


async def list_parameters(skip: int = 0, limit: int = 10, search: str = None):
    if limit > MAX_PAGE_SIZE:
        limit = MAX_PAGE_SIZE
    return {"skip": skip, "limit": limit, "search": search}


async def get_db():
    async with db_session_manager.session() as session:
        yield session
