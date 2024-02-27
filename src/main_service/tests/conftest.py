import pytest_asyncio
from blacksheep.testing import TestClient

from main_service.app.controllers.web_api.app import app as app_server

# @pytest.fixture(scope="session")
# def event_loop(request):
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest_asyncio.fixture(scope="session")
async def api():
    await app_server.start()
    yield app_server
    await app_server.stop()


@pytest_asyncio.fixture(scope="session")
async def test_client(api):
    return TestClient(api)
