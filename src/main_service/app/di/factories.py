from rodi import ActivationScope
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from main_service.app.adapters.bond_repo import BondDAODatabase, BondDAOInterface
from main_service.app.adapters.unit_of_work import PostgresUOW, UOWInterface
from main_service.app.application.commands.create_bond import CreateBondService
from main_service.app.application.queries.get_bonds import GetBondsService
from main_service.app.config import Config


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


def build_bond_repository_factory(context: ActivationScope) -> BondDAOInterface:
    session_factory = context.provider.get(async_sessionmaker)
    return BondDAODatabase(session_factory())


def build_create_bound_service(context: ActivationScope) -> CreateBondService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = BondDAODatabase(session)
    uow = PostgresUOW(session=session)
    return CreateBondService(repo=repo, uow=uow)


def build_get_bounds_service(context: ActivationScope) -> GetBondsService:
    session_factory = context.provider.get(async_sessionmaker)
    session = session_factory()

    repo = BondDAODatabase(session)
    uow = PostgresUOW(session=session)
    return GetBondsService(repo=repo, uow=uow)
