import uuid

import structlog
from blacksheep import JSONContent, Response, Router, created
from blacksheep.server.controllers import Controller

from main_service.app.application.commands.create_bond import (
    CreateBondCommand,
    CreateBondService,
)
from main_service.app.application.commands.create_operation import (
    CreateOperationCommand,
    CreateOperationService,
)
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
    BondCreateRequest,
    OperationCreateRequest,
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
                PortfolioGetBondResponse(isin=bond.bond_isin)
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

    @portfolio_router.post("/portfolios/{portfolio_id}/bonds")
    async def create_bond(
        self,
        portfolio_id: uuid.UUID,
        model: BondCreateRequest,
        service: CreateBondService,
    ) -> Response:
        command = CreateBondCommand(isin=model.isin, portfolio_id=portfolio_id)
        result = await service.execute(command)
        if len(result.errors) != 0:
            return Response(
                status=409,
                content=JSONContent(
                    ExceptionResponse(message=str(result.errors))
                ),
            )

        return created()

    @portfolio_router.post(
        "/portfolios/{portfolio_id}/bonds/{bond_id}/operations"
    )
    async def create_bond_operation(
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
