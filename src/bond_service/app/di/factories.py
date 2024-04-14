from app.adapters.interface.unit_of_work import UOWInterface
from app.adapters.postgres.dao.portfolio_dao import PortfolioDAO
from app.adapters.postgres.dao.unit_of_work import PostgresUOW
from app.application.commands.create_bond import CreateBondService
from app.application.commands.create_operation import (
    CreateOperationService,
)
from app.application.commands.create_portfolio import (
    CreatePortfolioService,
)
from app.application.queries.get_portfolio import (
    GetPortfolioService,
)
from app.application.queries.get_portfolios import (
    GetPortfoliosService,
)
from app.config import Config
from rodi import ActivationScope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)


def build_sa_engine(context: ActivationScope) -> AsyncEngine:
    config: Config = context.provider.get(Config)
    return create_async_engine(
        f"postgresql+asyncpg://{config.database.login}:{config.database.password}@{config.database.host}:{config.database.port}/{config.database.database}",
        echo=False,
    )


def build_sa_sessionmaker(context: ActivationScope) -> async_sessionmaker:
    engine = context.provider.get(AsyncEngine)
    return async_sessionmaker(engine, expire_on_commit=False)


def build_uow(context: ActivationScope) -> UOWInterface:
    session_factory = context.provider.get(async_sessionmaker)
    return PostgresUOW(session=session_factory())


def build_create_bound_service(context: ActivationScope) -> CreateBondService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = PortfolioDAO(session)
    uow = PostgresUOW(session=session)
    return CreateBondService(repo=repo, uow=uow)


def build_get_portfolios_service(
    context: ActivationScope,
) -> GetPortfoliosService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = PortfolioDAO(session)
    uow = PostgresUOW(session=session)
    return GetPortfoliosService(repo=repo, uow=uow)


def build_get_portfolio_service(
    context: ActivationScope,
) -> GetPortfolioService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = PortfolioDAO(session)
    uow = PostgresUOW(session=session)
    return GetPortfolioService(repo=repo, uow=uow)


def build_create_portfolio_service(
    context: ActivationScope,
) -> CreatePortfolioService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = PortfolioDAO(session)
    uow = PostgresUOW(session=session)
    return CreatePortfolioService(repo=repo, uow=uow)


def build_create_operation_service(
    context: ActivationScope,
) -> CreateOperationService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = PortfolioDAO(session)
    uow = PostgresUOW(session=session)
    return CreateOperationService(repo=repo, uow=uow)
