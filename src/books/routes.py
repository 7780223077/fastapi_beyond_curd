
import uuid
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import RoleEnum
from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateSchema
from src.auth.dependencies import verify_token, TokenType
from src.db.main import get_session
from .service import BookService

book_router = APIRouter()


@book_router.get("/")
async def read_books(
    session: AsyncSession = Depends(get_session),
    access_token: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN]))
):
    """Read all books"""
    books = await BookService(session).get_all_books()
    return books


@book_router.get("/{book_id}")
async def read_book(
    book_uid: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    access_token: dict = Depends(verify_token(TokenType.ACCESS))
):
    """Read a book"""
    book = await BookService(session).get_book(book_uid)
    return book


@book_router.post("/", status_code=201)
async def create_book(
    book: BookSchema, 
    session: AsyncSession = Depends(get_session),
    access_token: dict = Depends(verify_token(TokenType.ACCESS))
):
    """Create a new book"""
    new_book = await BookService(session).create_book(book)
    return new_book


@book_router.patch("/{book_id}")
async def update_book(
    book_uid: uuid.UUID,
    update_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_session),
    access_token: dict = Depends(verify_token(TokenType.ACCESS))
):
    """ "update book"""
    updated_book = await BookService(session).update_book(book_uid, update_data)
    return updated_book


@book_router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_uid: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    access_token: dict = Depends(verify_token(TokenType.ACCESS))
):
    """delete a book"""
    await BookService(session).delete_book(book_uid)
    return {}
