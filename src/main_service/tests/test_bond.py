import pytest
import sqlalchemy
from sqlalchemy.ext.asyncio import async_sessionmaker

from main_service.tests.conftest import AsyncClient


@pytest.mark.asyncio
async def test_create_bond(test_client: type[AsyncClient]):
    # async with test_client() as client:
    response = await test_client.post("/bonds", json={"name": "HARDCODE"})

    assert response is not None
    assert response.status == 201


@pytest.mark.asyncio
async def test_create_bond_duplicate(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"

    async with session_factory() as session:
        await session.execute(sqlalchemy.text("""INSERT INTO bonds (name) VALUES (:name)"""), {"name": name})
        await session.commit()

    response = await test_client.post("/bonds", json={"name": name})
    assert response is not None
    assert response.status == 409
