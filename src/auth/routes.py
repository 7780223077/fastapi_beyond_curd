from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.utils import create_access_token
from src.auth.schemas import UserCreateModel, UserOut, UserLoginModel
from src.auth.dependencies import verify_token, TokenType
from src.db.redis import block_token
import src.auth.service as user_service
from src.db.main import get_session

auth_router = APIRouter()

@auth_router.post(
    "/signup", 
    response_model=UserOut, 
    status_code=status.HTTP_201_CREATED
)
async def create_account(
    user_data: UserCreateModel, 
    session: AsyncSession = Depends(get_session)
) -> UserOut:
        return await user_service.create_user(user_data, session)


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK
)
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    return await user_service.login_user(
        email=login_data.email, 
        password=login_data.password, 
        session=session
    )


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
async def logout_user(
    user_details: dict = Depends(verify_token(TokenType.ACCESS)),
):
    token_jti = user_details["jti"]
    await block_token(token_jti)
    return JSONResponse(
        content={
        "message": "You have been logged out successfully.",
        "status": "success"
        },
        status_code=status.HTTP_200_OK
    )


@auth_router.get("/refresh-token", status_code=status.HTTP_200_OK)
async def get_new_access_token(
    user_details: dict = Depends(verify_token(TokenType.REFRESH)),
):
    new_access_token = create_access_token(claims=user_details["user"])
    return JSONResponse(content={"access_token": new_access_token})