from contextlib import asynccontextmanager

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from app.adapters.postgres.map import run_mapper
from app.configs.logging import configure_logger
from app.controllers.rest_api.handlers.bond import bond_router
from app.controllers.rest_api.handlers.home import home_router
from app.controllers.rest_api.handlers.portfolio import portfolio_router
from app.di.ioc import AdaptersProvider


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await app.state.dishka_container.close()


def application_factory():
    clear_mappers()
    run_mapper()
    app = FastAPI(lifespan=lifespan)
    app.include_router(home_router)
    app.include_router(bond_router)
    app.include_router(portfolio_router)
    return app


def production_application_factory():
    """
    1. Создание контейнера для di
    :return:
    """
    configure_logger()
    app = application_factory()
    container = make_async_container(AdaptersProvider())
    setup_dishka(container, app)
    return app
