from enum import Enum

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.models import RoleEnum
from src.auth.service import get_user_email_id
from src.auth.utils import decode_access_token
from src.db.redis import is_token_blocked
from src.db.main import get_session


security = HTTPBearer()



class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"


def verify_token(expected_type: TokenType = TokenType.ACCESS, allowed_roles: list[RoleEnum] = None):
    """
    Reusable dependency to verify either access or refresh token.

    Args:
        expected_type (str): "access" or "refresh"

    Returns:
        dict: decoded user details from the token
    """
    async def _verify(
            credentials: HTTPAuthorizationCredentials = Depends(security),
            session: AsyncSession = Depends(get_session)
        ):
        user_details = decode_access_token(credentials.credentials)

        is_refresh = user_details.get("refresh_token", False)
        if expected_type == TokenType.ACCESS and is_refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide the access token, not the refresh token",
            )
        if expected_type == TokenType.REFRESH and not is_refresh:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Please provide the refresh token, not the access token",
            )

        # Optional: Check if token is blocked (for access tokens)
        # if expected_type == "access":
        #     if await is_token_blocked(user_details.get("jti")):
        #         raise HTTPException(
        #             status_code=status.HTTP_401_UNAUTHORIZED,
        #             detail="Token has been blocked",
        #         )
        user_email = user_details["user"]["email"]
        current_user = await get_user_email_id(user_email, session)
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not allowed to perform this action",
            )

        return user_details 

    return _verify
