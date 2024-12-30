from typing import Annotated, AsyncGenerator

from fastapi import Depends
from aioredis import Redis, from_url

from app.configs import settings


redis_client = from_url(settings.REDIS_URL, decode_responses=True,  # 是否以字符串返回 
                        max_connections=settings.REDIS_POOL_MAX)
# redis = await aioredis.create_redis_pool("redis://localhost")  # 更精细的控制

async def get_redis() -> AsyncGenerator[Redis, None]:
    try:
        yield redis_client
    finally:
        redis_client.close()


RedisDep = Annotated[Redis, Depends(get_redis)]

