import os
from typing import AsyncIterable

import structlog
from dishka import Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
)

from app.di.ioc import AdaptersProvider
from tests.integration.utils.create_database import create_database
from tests.integration.utils.delete_database import delete_database
from tests.integration.utils.generate_name import generate_random_name

logger = structlog.get_logger(__name__)


class TestAdaptersProvider(AdaptersProvider):
    """
    Контейнер di для тестов
    """

    scope = Scope.APP

    @provide(scope=Scope.APP)
    async def build_engine(self) -> AsyncIterable[AsyncEngine]:
        db_name = generate_random_name()
        create_database(db_name)

        os.environ["DB_DATABASE"] = db_name
        async for v in super().build_engine():
            yield v

        delete_database(db_name)
