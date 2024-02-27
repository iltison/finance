from blacksheep import Router
from blacksheep.server.controllers import Controller

from main_service.app.controllers.web_api.schemas.home import HomeResponse

home_router = Router()


class Home(Controller):
    @home_router.get("/")
    async def index(self) -> HomeResponse:
        return HomeResponse(ok=True)
