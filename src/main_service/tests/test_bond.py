import pytest
import sqlalchemy
from blacksheep import Application, JSONContent
from blacksheep.testing import TestClient
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker

from main_service.app.adapters.unit_of_work import UOWInterface
from main_service.app.application.commands.create_bond import CreateBondCommand, CreateBondService
from main_service.tests.conftest import ClientSession


@pytest.mark.asyncio
async def test_create_bond(test_client: type[ClientSession]):
    async with test_client() as client:
        response = await client.post("/bonds", json={"name": "HARDCODE"})

    assert response is not None
    assert response.status == 201


@pytest.mark.asyncio
async def test_create_bond_duplicate(test_client: type[ClientSession], server):
    session_factory = server.services.provider.get(sessionmaker)

    name = "HARDCODE"

    async with session_factory() as session:
        await session.execute(sqlalchemy.text("""INSERT INTO bonds (name) VALUES (:name)"""), {"name": name})
        await session.commit()

    async with test_client() as client:
        response = await client.post("/bonds", json={"name": name})
    assert response is not None
    assert response.status == 409
