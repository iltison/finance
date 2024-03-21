import uuid

import structlog
from blacksheep import JSONContent, Response, Router, created
from blacksheep.server.controllers import Controller

from main_service.app.application.commands.create_operation import (
    CreateOperationCommand,
    CreateOperationService,
)
from main_service.app.controllers.web_api.schemas.additional import (
    ExceptionResponse,
)
from main_service.app.controllers.web_api.schemas.operation import (
    OperationCreateRequest,
)

operation_router = Router()
logger = structlog.get_logger(__name__)


class OperationController(Controller):
    @operation_router.post(
        "/portfolios/{portfolio_id}/bonds/{bond_id}/operations"
    )
    async def create_portfolio(
        self,
        portfolio_id: uuid.UUID,
        bond_id: uuid.UUID,
        model: OperationCreateRequest,
        service: CreateOperationService,
    ) -> Response:
        """
        Добавление операции
        :return:
        """

        command = CreateOperationCommand(
            portfolio_id=portfolio_id,
            bond_id=bond_id,
            price_per_piece=model.price_per_piece,
            count=model.count,
            date=model.date,
            type=model.type,
        )
        result = await service.execute(command)

        if len(result.errors) != 0:
            return Response(
                status=409,
                content=JSONContent(
                    ExceptionResponse(message=str(result.errors))
                ),
            )
        return created()
