import logging

from fastapi import APIRouter

from app.models.data import User
from app.extensions.ext_db import SessionDep
from app.extensions.ext_redis import RedisDep


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users():
    logging.info("Hello World")
    return {"users": "Hello World"}

@router.post("/add")
async def add_user(user: User, session: SessionDep):  # 尽量不要用数据表作为验证参数
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"user": user}

# 示例路由：Redis 读写
@router.post("/set")
async def set_key(key: str, value: str, redis: RedisDep):
    """设置键值对到 Redis"""
    await redis.set(key, value)
    return {"message": f"Key '{key}' set with value '{value}'"}

@router.get("/get")
async def get_key(key: str, redis: RedisDep):
    """从 Redis 获取键值"""
    value = await redis.get(key)
    if value is None:
        return {"message": f"Key '{key}' not found"}
    return {"key": key, "value": value}
