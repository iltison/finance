import psycopg2
import structlog
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.configs.config import get_db_config

logger = structlog.get_logger(__name__)


def create_database(name):
    config = get_db_config()
    conn = psycopg2.connect(
        user=config.login,
        password=config.password,
        host=config.host,
        port=config.port,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    try:
        sql = f"""CREATE DATABASE {name} with template reference"""
        cur.execute(sql)
        logger.debug("Database created successfully", name=name)
    finally:
        cur.close()
        conn.close()
