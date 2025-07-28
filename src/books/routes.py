
import uuid
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.models import RoleEnum
from src.books.book_data import books
from src.books.schemas import BookSchema, BookUpdateSchema, BookOutModel
from src.auth.dependencies import verify_token, TokenType
from src.db.main import get_session
from .service import BookService

book_router = APIRouter()


@book_router.get("/")
async def read_books(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    """Read all books"""
    books = await BookService(session).get_all_books()
    return books


@book_router.get("/me", response_model=list[BookOutModel])
async def read_all_books_for_current_user(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    return await BookService(session).get_all_books_for_current_user(token_details["user"]["user_id"])


@book_router.get("/{book_id}")
async def read_book(
    book_uid: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    """Read a book"""
    book = await BookService(session).get_book(book_uid)
    return book


@book_router.post("/", status_code=201)
async def create_book(
    book: BookSchema, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    """Create a new book"""
    new_book = await BookService(session).create_book(book, token_details["user"]["user_id"])
    return new_book


@book_router.patch("/{book_id}")
async def update_book(
    book_uid: uuid.UUID,
    update_data: BookUpdateSchema,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    """ "update book"""
    updated_book = await BookService(session).update_book(book_uid, update_data)
    return updated_book


@book_router.delete("/{book_id}", status_code=204)
async def delete_book(
    book_uid: uuid.UUID, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(verify_token(TokenType.ACCESS, allowed_roles=[RoleEnum.ADMIN, RoleEnum.USER]))
):
    """delete a book"""
    await BookService(session).delete_book(book_uid)
    return {}
