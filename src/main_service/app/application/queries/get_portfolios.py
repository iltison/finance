from dataclasses import dataclass, field

import structlog

from main_service.app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from main_service.app.adapters.interface.unit_of_work import UOWInterface
from main_service.app.application.queries.query import QueryResult
from main_service.app.domain.portfolio import PortfolioAggregate

logger = structlog.get_logger(__name__)


@dataclass
class GetPortfoliosQueryResult(QueryResult):
    payload: list[PortfolioAggregate] = field(default_factory=list)
    errors: list[PortfolioAggregate] = field(default_factory=list)


class GetPortfoliosService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(self) -> GetPortfoliosQueryResult:
        structlog.contextvars.bind_contextvars()
        async with self.__uow:
            portfolios = await self.__repo.get_all()
            logger.info("Portfolios got")
            return GetPortfoliosQueryResult().success(portfolios)
