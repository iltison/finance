from blacksheep import Application, Router

from main_service.app.controllers.web_api.routes.home import home_router

router = Router(sub_routers=[home_router])


app = Application(router=router)
