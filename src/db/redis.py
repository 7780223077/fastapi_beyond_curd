import aioredis

from src.config import settings

JTI_EXPIRY_SECONDS = 60 * 60

token_blocklist = aioredis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)


async def is_token_blocked(token_jti: str) -> bool:
    jti = await token_blocklist.get(token_jti)
    print("jti", jti)
    return jti is not None


async def block_token(token_jti: str) -> None:
    await token_blocklist.set(name=token_jti, value="blocked", ex=JTI_EXPIRY_SECONDS)