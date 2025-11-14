import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/")
        assert r.status_code == 200
        assert r.json() == {"message": "Hello World"}


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/health")
        assert r.status_code == 200
        assert r.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_hello():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        r = await client.get("/hello/Tester")
        assert r.status_code == 200
        assert r.json() == {"message": "Hello Tester"}