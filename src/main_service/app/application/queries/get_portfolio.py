from dataclasses import dataclass, field

import structlog

from main_service.app.adapters.portfolio_dao import PortfolioDAOInterface
from main_service.app.adapters.unit_of_work import UOWInterface
from main_service.app.application.queries.query import QueryResult
from main_service.app.domain.const import UUID
from main_service.app.domain.portfolio import Portfolio

logger = structlog.get_logger(__name__)


@dataclass
class GetPortfolioQueryResult(QueryResult):
    payload: Portfolio = field(default_factory=list)
    errors: list[Portfolio] = field(default_factory=list)


@dataclass
class GetPortfolioQuery:
    id: UUID


class GetPortfolioService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(self, query: GetPortfolioQuery) -> GetPortfolioQueryResult:
        structlog.contextvars.bind_contextvars()
        async with self.__uow:
            portfolio = await self.__repo.get_by_id(id=query.id)
            logger.info("Portfolio got")
            return GetPortfolioQueryResult().success(portfolio)
