from fastapi import APIRouter
from app.schemas.hello import HelloResponse


router = APIRouter()


# @router.get("/{name}", response_model=HelloResponse)
async def say_hello(name: str):
    return HelloResponse(message=f"Hello {name}")