from fastapi import FastAPI

from app.routers import api_router
from app.configs import settings


def init_routers(app: FastAPI):
    app.include_router(api_router, prefix=settings.API_V1_STR)
