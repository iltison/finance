import dataclasses
import uuid

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Response
from starlette.responses import JSONResponse

from app.applications.commands.create_bond import (
    CreateBondCommand,
    CreateBondService,
)
from app.applications.commands.create_operation import (
    CreateOperationCommand,
    CreateOperationService,
)
from app.controllers.rest_api.schemas.additional import ExceptionResponse
from app.controllers.rest_api.schemas.bond import (
    BondCreateRequest,
    OperationCreateRequest,
)

bond_router = APIRouter()


@bond_router.post(
    "/portfolios/{portfolio_id}/bonds",
    response_model=None,
    responses={409: {"model": ExceptionResponse}},
)
@inject
async def create_bond(
    portfolio_id: uuid.UUID,
    model: BondCreateRequest,
    service: FromDishka[CreateBondService],
) -> str | Response:
    command = CreateBondCommand(isin=model.isin, portfolio_id=portfolio_id)
    result = await service.execute(command)
    if len(result.errors) != 0:
        return JSONResponse(
            status_code=409,
            content=dataclasses.asdict(
                ExceptionResponse(message=str(result.errors))
            ),
        )

    return "good"


@bond_router.post(
    "/portfolios/{portfolio_id}/bonds/{bond_id}/operations",
    response_model=None,
    responses={409: {"model": ExceptionResponse}},
)
@inject
async def create_bond_operation(
    portfolio_id: uuid.UUID,
    bond_id: uuid.UUID,
    model: OperationCreateRequest,
    service: FromDishka[CreateOperationService],
) -> str | Response:
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
        return JSONResponse(
            status_code=409,
            content=dataclasses.asdict(
                ExceptionResponse(message=str(result.errors))
            ),
        )

    return "good"
