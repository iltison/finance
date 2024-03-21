import uuid

import structlog
from blacksheep import JSONContent, Response, Router
from blacksheep.server.controllers import Controller

from main_service.app.application.commands.create_portfolio import (
    CreatePortfolioCommand,
    CreatePortfolioService,
)
from main_service.app.application.queries.get_portfolio import (
    GetPortfolioQuery,
    GetPortfolioService,
)
from main_service.app.application.queries.get_portfolios import (
    GetPortfoliosService,
)
from main_service.app.controllers.web_api.schemas.additional import (
    ExceptionResponse,
)
from main_service.app.controllers.web_api.schemas.portfolio import (
    PortfolioCreateRequest,
    PortfolioCreateResponse,
    PortfolioGetBondResponse,
    PortfolioGetResponse,
)

portfolio_router = Router()
logger = structlog.get_logger(__name__)


class PortfolioController(Controller):
    @portfolio_router.get("/portfolios")
    async def get_portfolios(
        self, service: GetPortfoliosService
    ) -> list[PortfolioGetResponse] | Response:
        """
        Получение портфелей
        :param service:
        :return:
        """
        result = await service.execute()
        if len(result.errors) != 0:
            return Response(
                status=409,
                content=JSONContent(
                    ExceptionResponse(message=str(result.errors))
                ),
            )

        return [
            PortfolioGetResponse(id=i.id, name=i.name) for i in result.payload
        ]

    @portfolio_router.get("/portfolios/{portfolio_id}")
    async def get_portfolio(
        self, portfolio_id: uuid.UUID, service: GetPortfolioService
    ) -> PortfolioGetResponse | Response:
        """
        Получение конкретного портфеля
        :param portfolio_id:
        :param service:
        :return:
        """
        query = GetPortfolioQuery(id=portfolio_id)
        result = await service.execute(query)

        if len(result.errors) != 0:
            return Response(
                status=409,
                content=JSONContent(
                    ExceptionResponse(message=str(result.errors))
                ),
            )
        return PortfolioGetResponse(
            id=result.payload.id,
            name=result.payload.name,
            bonds=[
                PortfolioGetBondResponse(name=bond.name)
                for bond in result.payload.bonds
            ],
        )

    @portfolio_router.post("/portfolios")
    async def create_portfolio(
        self, model: PortfolioCreateRequest, service: CreatePortfolioService
    ) -> PortfolioCreateResponse | Response:
        """
        Создание портфеля
        :return:
        """

        command = CreatePortfolioCommand(name=model.name)
        result = await service.execute(command)

        if len(result.errors) != 0:
            return Response(
                status=409,
                content=JSONContent(
                    ExceptionResponse(message=str(result.errors))
                ),
            )
        return PortfolioCreateResponse(id=result.result)
