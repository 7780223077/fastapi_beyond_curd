from datetime import timedelta

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException, status

from src.auth.models import User
from src.auth.schemas import UserCreateModel
from src.auth.utils import hash_password, verify_password, create_access_token

REFRESH_TOKEN_EXPIRY_SECONDS = 60 * 60 * 24 * 2  # 2 days

async def get_user_email_id(email: str, session: AsyncSession) -> User | None:
    """Get user by email."""
    statement = select(User).where(User.email == email)
    return await session.scalar(statement)


async def is_user_exists(email: str, session: AsyncSession) -> bool:
    """Check if user exists by email."""
    return await get_user_email_id(email, session) is not None


async def create_user(user_data: UserCreateModel, session: AsyncSession) -> User:
    """Create a new user."""
    if await is_user_exists(user_data.email, session):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    user_data_dict = user_data.model_dump()
    user_data_dict["password"] = hash_password(user_data_dict["password"])
    user = User(**user_data_dict)

    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def login_user(email: str, password: str, session: AsyncSession) -> dict:
    """Login user by email and password."""
    user = await get_user_email_id(email, session)
    if not user or not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )
    access_token = create_access_token(
        claims={"user_id": str(user.uid), "email": user.email, "role": user.role},
    )
    refresh_token = create_access_token(
        claims={"user_id": str(user.uid), "email": user.email, "role": user.role},
        expiry=timedelta(seconds=REFRESH_TOKEN_EXPIRY_SECONDS),
        refresh_token=True
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "message": "Login successful",
    }
