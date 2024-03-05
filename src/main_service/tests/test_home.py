import pytest

from main_service.tests.conftest import AsyncClient


@pytest.mark.asyncio
async def test_get_home(test_client: AsyncClient):
    response = await test_client.get("/")

    data = response.json()

    assert response is not None
    assert response.status_code == 200

    assert data["ok"] is True
