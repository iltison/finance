import pytest
from blacksheep.testing import TestClient

from main_service.tests.conftest import ClientSession


@pytest.mark.asyncio
async def test_get_home(test_client: type[ClientSession]):
    async with test_client() as client:
        response = await client.get("/")

        data = await response.json()

    assert response is not None
    assert response.status == 200

    assert data["ok"] is True
