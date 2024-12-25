from fastapi import APIRouter
import logging


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def read_users():
    logging.info("Hello World")
    return {"users": "Hello World"}

