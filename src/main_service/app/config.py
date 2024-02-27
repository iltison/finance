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
    database: str = "postgres"
    login: str = "admin"
    password: str = "admin"


def get_web_config() -> WebConfig:
    return WebConfig()


def get_db_config() -> DBConfig:
    return DBConfig()
