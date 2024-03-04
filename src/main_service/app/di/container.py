from rodi import Container
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from main_service.app.adapters.bond_repo import BondRepoInterface
from main_service.app.adapters.unit_of_work import UOWInterface
from main_service.app.application.commands.create_bond import CreateBondService
from main_service.app.config import Config, get_config
from main_service.app.di.factories import (
    build_bond_repository_factory,
    build_create_bound_service,
    build_sa_engine,
    build_sa_sessionmaker,
    build_uow,
)


def get_container() -> Container:
    container: Container = Container()

    container.add_singleton_by_factory(get_config, Config)
    container.add_singleton_by_factory(build_sa_engine, AsyncEngine)
    container.add_scoped_by_factory(build_sa_sessionmaker, sessionmaker)
    container.add_scoped_by_factory(build_uow, UOWInterface)

    container.add_scoped_by_factory(build_bond_repository_factory, BondRepoInterface)
    container.add_scoped_by_factory(build_create_bound_service, CreateBondService)

    return container
