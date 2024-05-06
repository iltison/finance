from dataclasses import dataclass, field

import structlog

from app.adapters.interface.portfolio_gateway import PortfolioGatewayInterface
from app.applications.queries.query import QueryResult
from app.domains.const import UUID
from app.domains.exeption import ServiceError
from app.domains.portfolio import (
    PortfolioAggregate,
)

logger = structlog.get_logger(__name__)


@dataclass
class GetPortfolioInformationQuery:
    portfolio_id: UUID


@dataclass
class GetPortfolioInformationResult(QueryResult):
    payload: PortfolioAggregate = None
    errors: list[ServiceError] = field(default_factory=list)


class GetPortfolioInformationService:
    def __init__(self, portfolio_gateway: PortfolioGatewayInterface):
        self.__gateway = portfolio_gateway

    async def execute(
        self, query: GetPortfolioInformationQuery
    ) -> GetPortfolioInformationResult:
        structlog.contextvars.bind_contextvars(
            portfolio_id=query.portfolio_id,
        )

        async with self.__gateway as gateway:
            portfolio = await gateway.get_portfolio_by_id(query.portfolio_id)

        logger.info("Got portfolio")
        return GetPortfolioInformationResult().success(portfolio)
