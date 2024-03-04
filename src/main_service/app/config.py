import os
from dataclasses import dataclass, field


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
    login: str = "postgres"
    password: str = "postgres"


@dataclass
class Config:
    database: DBConfig = field(default_factory=DBConfig)


def get_web_config() -> WebConfig:
    return WebConfig()


def get_db_config() -> DBConfig:
    return DBConfig()


def get_config() -> Config:
    config = Config()
    database = os.getenv("DB_DATABASE", config.database.database)
    config.database.database = database
    return config
