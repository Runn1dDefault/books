from fastapi import FastAPI

from routers import genres, books


app = FastAPI()
app.include_router(genres.router)
app.include_router(books.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}

