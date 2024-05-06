from typing import AsyncIterable

import structlog
from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.adapters.dao.portfolio_dao import PortfolioGateway
from app.adapters.interface.portfolio_gateway import PortfolioGatewayInterface
from app.applications.commands.create_bond import CreateBondService
from app.applications.commands.create_operation import CreateOperationService
from app.applications.queries.get_portfolio_info import (
    GetPortfolioInformationService,
)
from app.configs.config import get_db_config

logger = structlog.get_logger(__name__)


# app dependency logic
class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    portfolio_gateway = provide(
        PortfolioGateway, provides=PortfolioGatewayInterface
    )
    create_bond_service = provide(CreateBondService)
    create_operation_service = provide(CreateOperationService)
    get_portfolio_information_service = provide(GetPortfolioInformationService)

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
