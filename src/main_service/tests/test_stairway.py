import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config as AlembicConfig
from alembic.script import Script, ScriptDirectory

from main_service.app.config import get_config


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


def get_revisions(alembic_config: AlembicConfig) -> list[Script]:
    # Get directory object with Alembic migrations
    revisions_dir = ScriptDirectory(alembic_config.get_main_option("script_location"))

    # Get & sort migrations, from first to last
    revisions: list[Script] = list(revisions_dir.walk_revisions("base", "heads"))
    revisions.reverse()
    return revisions


@pytest.mark.order("first")
def test_migrations_stairway(alembic_config: AlembicConfig) -> None:
    for revision in get_revisions(alembic_config):
        upgrade(alembic_config, revision.revision)

        # We need -1 for downgrading first migration (its down_revision is None)
        downgrade(alembic_config, revision.down_revision or "-1")
        upgrade(alembic_config, revision.revision)
