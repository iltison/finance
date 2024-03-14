import pytest
import structlog
from httpx import AsyncClient
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import async_sessionmaker

from main_service.app.domain.bond import Bond

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_create_bond(test_client: AsyncClient):
    response = await test_client.post("/bonds", json={"name": "HARDCODE"})
    assert response is not None
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_bond_duplicate(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"

    async with session_factory() as session:
        query = insert(Bond).values(name=name)
        await session.execute(query)
        await session.commit()

    response = await test_client.post("/bonds", json={"name": name})
    assert response is not None
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_bonds(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"

    async with session_factory() as session:
        query = insert(Bond).values(name=name)
        await session.execute(query)
        await session.commit()

    response = await test_client.get("/bonds")

    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {"names": ["HARDCODE"]}


@pytest.mark.asyncio
async def test_get_empty_bonds(test_client: AsyncClient):
    response = await test_client.get("/bonds")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {"names": []}