import os
from typing import AsyncIterable

import httpx
import pytest
import pytest_asyncio
import structlog
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from httpx import AsyncClient

from app.controllers.rest_api.app import application_factory
from tests.integrations.configs.config import get_reference_name_database
from tests.integrations.utils.provider import TestAdaptersProvider

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="module", autouse=True)
def migration():
    """
    Накатывание последней версии миграции на тестовую базу
    :return:
    """
    os.environ["DB_DATABASE"] = get_reference_name_database()

    alembic_cfg = AlembicConfig("alembic.ini")
    upgrade(alembic_cfg, "head")


@pytest_asyncio.fixture(scope="function")
async def container() -> AsyncIterable[AsyncContainer]:
    container = make_async_container(TestAdaptersProvider())
    yield container
    await container.close()


@pytest_asyncio.fixture(scope="function")
async def test_client(container) -> AsyncIterable[AsyncClient]:
    app = application_factory()

    setup_dishka(container, app)

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://localhost:8000"
    ) as client:
        yield client
