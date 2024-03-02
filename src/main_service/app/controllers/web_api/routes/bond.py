import structlog
from blacksheep import JSONContent, Response, Router, created
from blacksheep.server.controllers import Controller

from main_service.app.application.commands.create_bond import CreateBondCommand, CreateBondService
from main_service.app.controllers.web_api.schemas.additional import ExceptionResponse
from main_service.app.controllers.web_api.schemas.bond import BondCreateRequest

bond_router = Router()
logger = structlog.get_logger("controller")


class BondController(Controller):
    @bond_router.post("/bonds")
    async def create_bond(self, model: BondCreateRequest, service: CreateBondService) -> Response:
        command = CreateBondCommand(name=model.name)
        result = await service.execute(command)
        if len(result.errors) != 0:
            return Response(status=409, content=JSONContent(ExceptionResponse(message=str(result.errors))))

        return created()
