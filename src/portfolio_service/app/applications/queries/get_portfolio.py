from dataclasses import dataclass, field

import structlog

from app.adapters.interfaces.portfolio_dao import PortfolioDAOInterface
from app.adapters.interfaces.unit_of_work import UOWInterface
from app.applications.queries.query import QueryResult
from app.domains.const import UUID
from app.domains.portfolio import PortfolioAggregate

logger = structlog.get_logger(__name__)


@dataclass
class GetPortfolioQueryResult(QueryResult):
    payload: PortfolioAggregate = field(default_factory=list)
    errors: list[PortfolioAggregate] = field(default_factory=list)


@dataclass
class GetPortfolioQuery:
    id: UUID


class GetPortfolioService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(
        self, query: GetPortfolioQuery
    ) -> GetPortfolioQueryResult:
        structlog.contextvars.bind_contextvars()
        async with self.__uow:
            portfolio = await self.__repo.get_by_id(id=query.id)
            logger.info("Portfolio got")
            return GetPortfolioQueryResult().success(portfolio)
