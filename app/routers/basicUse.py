import logging

from fastapi import APIRouter

from app.models.data import User
from app.extensions.ext_db import SessionDep


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
