from fastapi import APIRouter

from .profile import router as profile_router


api_router = APIRouter(prefix="/api/v1")
api_router.include_router(profile_router)