from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router as api_router
from app.core.logging import setup_logging
import logging


setup_logging()
logger = logging.getLogger("app")
app = FastAPI(title=settings.PROJECT_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router, prefix=settings.API_PREFIX)


@app.on_event("startup")
async def on_startup():
    logger.info("Application startup complete")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Application shutdown")