import pytest
from alembic.command import downgrade
from alembic.config import Config as AlembicConfig

from app.config import get_config


@pytest.fixture(scope="function")
def alembic_config() -> AlembicConfig:
    config = get_config()
    postgres_url = f"postgresql://{config.database.login}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}"
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", postgres_url)
    return alembic_cfg


@pytest.fixture(scope="function", autouse=True)
def drop_db(alembic_config: AlembicConfig) -> None:
    downgrade(alembic_config, "base")
