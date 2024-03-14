import pytest
from main_service.app.config import get_config
from alembic.config import Config as AlembicConfig
from alembic.command import downgrade


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
