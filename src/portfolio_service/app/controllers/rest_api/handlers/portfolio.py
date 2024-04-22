import uuid

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.applications.commands.create_portfolio import (
    CreatePortfolioCommand,
    CreatePortfolioService,
)
from app.applications.queries.get_portfolio import (
    GetPortfolioQuery,
    GetPortfolioService,
)
from app.applications.queries.get_portfolios import GetPortfoliosService
from app.controllers.rest_api.schemas.additional import ExceptionResponse
from app.controllers.rest_api.schemas.portfolio import (
    PortfolioCreateRequest,
    PortfolioCreateResponse,
    PortfolioGetResponse,
)

portfolio_router = APIRouter()


@portfolio_router.get(
    "/portfolios", responses={409: {"model": ExceptionResponse}}
)
@inject
async def get_portfolios(
    service: FromDishka[GetPortfoliosService],
) -> list[PortfolioGetResponse] | ExceptionResponse:
    result = await service.execute()
    if len(result.errors) != 0:
        return ExceptionResponse(message=str(result.errors))

    return [PortfolioGetResponse(id=i.id, name=i.name) for i in result.payload]


@portfolio_router.get(
    "/portfolios/{portfolio_id}",
    responses={
        409: {"model": ExceptionResponse},
        404: {"model": ExceptionResponse},
        200: {"model": PortfolioGetResponse},
    },
    response_model=None,
)
@inject
async def get_portfolio(
    portfolio_id: uuid.UUID, service: FromDishka[GetPortfolioService]
) -> PortfolioGetResponse | Response:
    query = GetPortfolioQuery(id=portfolio_id)
    result = await service.execute(query)

    if len(result.errors) != 0:
        return JSONResponse(
            status_code=409, content={"message": str(result.errors)}
        )
    elif result.payload is None:
        return JSONResponse(
            status_code=404, content={"message": "Item not found"}
        )

    return PortfolioGetResponse(
        id=result.payload.id,
        name=result.payload.name,
    )


@portfolio_router.post(
    "/portfolios", responses={409: {"model": ExceptionResponse}}
)
@inject
async def create_portfolio(
    model: PortfolioCreateRequest, service: FromDishka[CreatePortfolioService]
) -> PortfolioCreateResponse | ExceptionResponse:
    command = CreatePortfolioCommand(name=model.name)
    result = await service.execute(command)

    if len(result.errors) != 0:
        return ExceptionResponse(message=str(result.errors))
    return PortfolioCreateResponse(id=result.result)
