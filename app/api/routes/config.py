from fastapi import APIRouter
from app.core.config import settings


router = APIRouter()


@router.get("/config")
async def get_config():
    return {
        "project_name": settings.PROJECT_NAME,
        "cors_origins": settings.CORS_ORIGINS,
        "api_prefix": settings.API_PREFIX,
    }