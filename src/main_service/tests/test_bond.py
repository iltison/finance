import pytest
from blacksheep import Application, JSONContent
from blacksheep.testing import TestClient


@pytest.mark.asyncio
async def test_create_bond(test_client: TestClient):
    response = await test_client.post("/bonds", content=JSONContent({"name": "HARDCODE"}))
    assert response is not None
    assert response.status == 201


@pytest.mark.asyncio
async def test_create_bond_duplicate(test_client: TestClient, application: Application):
    response = await test_client.post("/bonds", content=JSONContent({"name": "HARDCODE"}))
    assert response is not None
    assert response.status == 409
