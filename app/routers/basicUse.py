import logging

from fastapi import APIRouter
from celery.result import AsyncResult

from app.models.data import User
from app.extensions.ext_db import SessionDep
from app.extensions.ext_redis import RedisDep
from app.tasks.tasks import long_task, shot_task


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

@router.put("/task")
async def put_task_time():
    task = long_task.apply_async()  # 启动异步任务
    # task = long_task.delay()  # 启动异步任务
    return { 'task_id': task.id }

@router.post("/task")
async def short_task_time():
    task = shot_task.apply_async()  # 启动异步任务
    return { 'task_id': task.id }

@router.get("/task")
async def get_task_time(task_id: str):
    task = AsyncResult(task_id)  # 获取任务状态
    return {
        'task_id': task.id,
        'status': task.status,
        'result': task.result,
        "ready": task.ready(),
        "successful": task.successful(),
        "value": task.result if task.ready() else None,
    }
