import os
from dataclasses import dataclass


@dataclass
class WebConfig:
    host: str = "localhost"
    port: int = 8000
    log_level: str = "debug"


@dataclass
class DBConfig:
    host: str
    port: int
    database: str
    login: str
    password: str


def get_web_config() -> WebConfig:
    return WebConfig()


def get_db_config() -> DBConfig:
    config = DBConfig(
        host = os.getenv("DB_HOST", "localhost"),
        port = os.getenv("DB_PORT", 5432),
        database = os.getenv("DB_DATABASE", "postgres"),
        login = os.getenv("DB_LOGIN", "postgres"),
        password = os.getenv("DB_PASSWORD", "postgres"),
    )
    return config

