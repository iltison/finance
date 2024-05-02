from typing import AsyncIterable

import structlog
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.adapters.interface.bond_dao import BondDAOInterface
from app.adapters.interface.portfolio_dao import PortfolioDAOInterface
from app.adapters.interface.unit_of_work import UOWInterface
from app.adapters.postgres.dao.bond_dao import BondDAO
from app.adapters.postgres.dao.portfolio_dao import PortfolioDAO
from app.adapters.postgres.dao.unit_of_work import PostgresUOW
from app.applications.commands.create_bond import CreateBondService
from app.applications.commands.create_operation import CreateOperationService
from app.configs.config import get_db_config

logger = structlog.get_logger(__name__)


# app dependency logic
class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    uow = provide(PostgresUOW, provides=UOWInterface)

    portfolio_dao = provide(PortfolioDAO, provides=PortfolioDAOInterface)
    bond_dao = provide(BondDAO, provides=BondDAOInterface)
    create_bond_service = provide(CreateBondService)
    create_operation_service = provide(CreateOperationService)

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
