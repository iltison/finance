import pytest
from blacksheep.testing import TestClient


@pytest.mark.asyncio
async def test_get_home(test_client: TestClient):
    response = await test_client.get("/")
    data = await response.json()

    assert response is not None
    assert response.status == 200

    assert data["ok"] is True
