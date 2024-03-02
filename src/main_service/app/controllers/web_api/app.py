from blacksheep import Application, Router

from main_service.app.controllers.web_api.routes.bond import bond_router
from main_service.app.controllers.web_api.routes.home import home_router
from main_service.app.di.container import get_container


def application_factory():
    containers = get_container()
    router = Router(sub_routers=[home_router, bond_router])
    return Application(services=containers, router=router, show_error_details=True)
