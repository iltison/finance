import pytest
from alembic.command import downgrade
from alembic.config import Config as AlembicConfig


@pytest.fixture(scope="function")
def alembic_config() -> AlembicConfig:
    alembic_cfg = AlembicConfig("alembic.ini")
    return alembic_cfg


@pytest.fixture(scope="function", autouse=True)
def drop_db(alembic_config: AlembicConfig) -> None:
    downgrade(alembic_config, "base")
