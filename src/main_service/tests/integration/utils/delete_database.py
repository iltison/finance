import psycopg2
import structlog
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from main_service.app.config import get_config

logger = structlog.get_logger(__name__)


def delete_database(name):
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
