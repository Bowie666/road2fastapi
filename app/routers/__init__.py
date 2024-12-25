from fastapi import APIRouter

from app.routers import basicUse


api_router = APIRouter()
api_router.include_router(basicUse.router)

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)
