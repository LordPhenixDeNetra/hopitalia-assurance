from fastapi import APIRouter
from app.api.routes.health import router as health_router
from app.api.routes.hello import router as hello_router
from app.api.routes.config import router as config_router
from app.api.routes.prestations import router as prestations_router


router = APIRouter()
router.include_router(health_router, tags=["health"])
router.include_router(hello_router, prefix="/hello", tags=["hello"])
router.include_router(config_router, tags=["config"])
router.include_router(prestations_router)