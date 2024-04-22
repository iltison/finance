import os
from dataclasses import dataclass


@dataclass
class WebConfig:
    host: str = "localhost"
    port: int = 8000
    log_level: str = "debug"


@dataclass
class DBConfig:
    host: str = "localhost"
    port: int = 5432
    database: str = "portfolio"
    login: str = "postgres"
    password: str = "postgres"


def get_web_config() -> WebConfig:
    return WebConfig()


def get_db_config() -> DBConfig:
    config = DBConfig()
    database = os.getenv("DB_DATABASE", config.database)
    config.database = database
    return config
