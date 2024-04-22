from typing import AsyncIterable

import structlog
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


from app.configs.config import get_db_config

logger = structlog.get_logger(__name__)


# app dependency logic
class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def build_sa_sessionmaker(
        self, engine: AsyncEngine
    ) -> AsyncIterable[AsyncSession]:
        session = async_sessionmaker(engine, expire_on_commit=False)()
        yield session
        await session.close()
        await engine.dispose()

    @provide(scope=Scope.APP)
    async def build_engine(self) -> AsyncIterable[AsyncEngine]:
        config = get_db_config()
        engine = create_async_engine(
            f"postgresql+asyncpg://{config.login}:{config.password}@{config.host}:{config.port}/{config.database}",
            future=True,
            query_cache_size=1200,
            pool_size=100,
            max_overflow=200,
            echo=False,
            echo_pool=True,
        )
        yield engine

        await engine.dispose()
