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

from main_service.app.config import get_config
from main_service.app.controllers.web_api.app import application_factory
from main_service.tests.integration.utils.provider import TestAdaptersProvider

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="module", autouse=True)
def migration():
    """
    Накатывание последней версии миграции на теестовую таблицу
    :return:
    """
    config = get_config()
    postgres_url = f"postgresql://{config.database.login}:{config.database.password}@{config.database.host}:{config.database.port}/reference"
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
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
