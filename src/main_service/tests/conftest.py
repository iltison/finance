import asyncio
from collections.abc import AsyncIterator

import pytest
import pytest_asyncio
from blacksheep import Application
from blacksheep.testing import TestClient

from main_service.app.controllers.web_api.app import application_factory


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def application() -> AsyncIterator[Application]:
    app = application_factory()
    await app.start()
    yield app
    await app.stop()


@pytest_asyncio.fixture(scope="session")
async def test_client(application) -> TestClient:
    return TestClient(application)
