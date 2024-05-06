import uuid

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter

from app.applications.queries.get_portfolio_info import (
    GetPortfolioInformationQuery,
    GetPortfolioInformationService,
)
from app.controllers.rest_api.schemas.additional import ExceptionResponse
from app.controllers.rest_api.schemas.portfolio import (
    PortfolioInfoBondResponse,
    PortfolioInfoResponse,
)

portfolio_router = APIRouter()


@portfolio_router.get(
    "/portfolios/{portfolio_id}",
    responses={409: {"model": ExceptionResponse}},
)
@inject
async def get_portfolio_information(
    portfolio_id: uuid.UUID,
    service: FromDishka[GetPortfolioInformationService],
) -> PortfolioInfoResponse | ExceptionResponse:
    query = GetPortfolioInformationQuery(portfolio_id=portfolio_id)
    result = await service.execute(query)
    if len(result.errors) != 0:
        return ExceptionResponse(message=str(result.errors))

    portfolio = PortfolioInfoResponse(portfolio_id=result.payload.id)
    for bond in result.payload.bonds:
        portfolio.bonds.append(
            PortfolioInfoBondResponse(
                bond_id=bond.id,
                isin=bond.bond_isin,
                name=bond.name,
                current_price=bond.current_price,
                current_amount=bond.current_amount,
                count=bond.count,
                profit=round(bond.profit, 4),
                coupon_profit=round(bond.coupon_profit, 4),
                diff_amount_price=round(bond.diff_amount_price, 4),
            )
        )
    return portfolio
