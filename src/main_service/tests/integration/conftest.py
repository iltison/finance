import asyncio
import os
import random
import string
from multiprocessing import Process

import httpx
import psycopg2
import pytest
import pytest_asyncio
import structlog
from alembic.command import upgrade
from alembic.config import Config as AlembicConfig
from httpx import AsyncClient
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from sqlalchemy.orm import clear_mappers

from main_service.app.adapters.persistence.map import run_mapper
from main_service.app.config import get_config
from main_service.app.controllers.web_api.app import application_factory
from main_service.app.main import run

logger = structlog.get_logger(__name__)


def generate_random_name():
    length = 10
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def create_database(name):
    config = get_config()
    conn = psycopg2.connect(
        database="reference",
        user=config.database.login,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    try:
        sql = f"""CREATE DATABASE {name} with template reference"""
        cur.execute(sql)
        logger.debug("Database created successfully........", name=name)
    finally:
        cur.close()
        conn.close()


def drop_database(name):
    config = get_config()
    conn = psycopg2.connect(
        database="reference",
        user=config.database.login,
        password=config.database.password,
        host=config.database.host,
        port=config.database.port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    try:
        sql = f"""DROP DATABASE {name}"""
        cur.execute(sql)
        logger.debug("Database dropped successfully........", name=name)
    finally:
        cur.close()
        conn.close()


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


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def mappers():
    """
    Маппинг таблиц на доменные модели
    :return:
    """
    clear_mappers()
    run_mapper()


@pytest_asyncio.fixture(scope="function", autouse=True)
async def server():
    app = application_factory()

    name = generate_random_name()
    create_database(name)
    os.environ["DB_DATABASE"] = name

    server_process = Process(target=run)
    server_process.start()

    if not server_process.is_alive():
        raise TypeError("The server process did not start!")
    await app.start()
    yield app
    await app.stop()
    server_process.terminate()  # Cleanup after test
    drop_database(name)


@pytest_asyncio.fixture(scope="session")
async def test_client() -> AsyncClient:
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        yield client
