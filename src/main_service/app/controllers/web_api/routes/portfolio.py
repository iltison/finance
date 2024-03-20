import uuid

import structlog
from blacksheep import Router, Response, JSONContent
from blacksheep.server.controllers import Controller


from main_service.app.application.queries.get_portfolio import GetPortfolioService, GetPortfolioQuery
from main_service.app.application.queries.get_portfolios import GetPortfoliosService
from main_service.app.controllers.web_api.schemas.additional import ExceptionResponse
from main_service.app.controllers.web_api.schemas.portfolio import PortfolioGetResponse


portfolio_router = Router()
logger = structlog.get_logger(__name__)


class PortfolioController(Controller):
    @portfolio_router.get("/portfolios")
    async def get_portfolios(self, service: GetPortfoliosService) -> list[PortfolioGetResponse] | Response:
        result = await service.execute()
        if len(result.errors) != 0:
            return Response(status=409, content=JSONContent(ExceptionResponse(message=str(result.errors))))

        return [PortfolioGetResponse(id=i.id, name=i.name) for i in result.payload]

    @portfolio_router.get("/portfolios/{portfolio_id}")
    async def get_portfolio(
        self, portfolio_id: uuid.UUID, service: GetPortfolioService
    ) -> PortfolioGetResponse | Response:
        query = GetPortfolioQuery(id=portfolio_id)
        result = await service.execute(query)

        if len(result.errors) != 0:
            return Response(status=409, content=JSONContent(ExceptionResponse(message=str(result.errors))))
        print(result.payload, type(result.payload))
        return PortfolioGetResponse(id=result.payload.id, name=result.payload.name)
