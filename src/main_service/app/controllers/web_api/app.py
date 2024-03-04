import logging

import structlog
from blacksheep import Application, Router
from sqlalchemy.ext.asyncio import AsyncEngine

from main_service.app.controllers.web_api.routes.bond import bond_router
from main_service.app.controllers.web_api.routes.home import home_router
from main_service.app.di.container import get_container

logger = structlog.get_logger("main")


async def on_shutdown(applications: Application):
    logger.info("Closed engine")
    engine = applications.services.provider.get(AsyncEngine, default=None)
    if engine is None:
        return None

    await engine.dispose()


def application_factory():
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG),
    )

    containers = get_container()
    router = Router(sub_routers=[home_router, bond_router])
    app = Application(services=containers, router=router, show_error_details=True)

    app.on_stop += on_shutdown

    return app
