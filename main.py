from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import initdb


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server is starting")
    yield
    print("server is stopping")


app = FastAPI(
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI Beyond CRUD!"}

app.include_router(book_router, prefix="/books", tags=['books'])
app.include_router(auth_router, prefix="/auth", tags=['auth'])