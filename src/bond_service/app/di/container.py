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
from app.config import Config, get_config
from app.di.factories import (
    build_create_bound_service,
    build_create_operation_service,
    build_create_portfolio_service,
    build_get_portfolio_service,
    build_get_portfolios_service,
    build_sa_engine,
    build_sa_sessionmaker,
)
from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker


def get_container() -> Container:
    container: Container = Container()

    container.add_scoped_by_factory(get_config, Config)
    container.add_singleton_by_factory(build_sa_engine, AsyncEngine)
    container.add_scoped_by_factory(build_sa_sessionmaker, async_sessionmaker)
    container.add_scoped_by_factory(
        build_create_bound_service, CreateBondService
    )

    container.add_scoped_by_factory(
        build_get_portfolios_service, GetPortfoliosService
    )
    container.add_scoped_by_factory(
        build_get_portfolio_service, GetPortfolioService
    )

    container.add_scoped_by_factory(
        build_create_portfolio_service, CreatePortfolioService
    )
    container.add_scoped_by_factory(
        build_create_operation_service, CreateOperationService
    )

    return container
