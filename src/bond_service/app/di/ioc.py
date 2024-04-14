from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
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
from app.application.commands.create_bond import CreateBondService
from app.application.commands.create_operation import CreateOperationService
from app.application.commands.create_portfolio import CreatePortfolioService
from app.application.queries.get_portfolio import GetPortfolioService
from app.application.queries.get_portfolios import GetPortfoliosService
from app.config import get_config


# app dependency logic
class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    uow = provide(PostgresUOW, provides=UOWInterface)

    portfolio_dao = provide(PortfolioDAO, provides=PortfolioDAOInterface)
    bond_dao = provide(BondDAO, provides=BondDAOInterface)
    get_portfolios_service = provide(GetPortfoliosService)
    create_bond_service = provide(CreateBondService)
    get_portfolio_service = provide(GetPortfolioService)
    create_portfolio_service = provide(CreatePortfolioService)
    create_operation_service = provide(CreateOperationService)

    @provide
    async def build_sa_sessionmaker(self) -> AsyncIterable[AsyncSession]:
        config = get_config()
        engine = create_async_engine(
            f"postgresql+asyncpg://{config.database.login}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}",
            echo=False,
        )
        session = async_sessionmaker(engine, expire_on_commit=False)()
        yield session
        await session.close()
        await engine.dispose()
