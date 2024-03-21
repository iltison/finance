from dataclasses import dataclass, field

import structlog

from main_service.app.adapters.interface.bond_dao import BondDAOInterface
from main_service.app.adapters.interface.unit_of_work import UOWInterface
from main_service.app.application.queries.query import QueryResult
from main_service.app.domain.bond import Bond

logger = structlog.get_logger(__name__)


@dataclass
class GetBondQueryResult(QueryResult):
    payload: list[Bond] = field(default_factory=list)
    errors: list[Bond] = field(default_factory=list)


class GetBondsService:
    def __init__(self, uow: UOWInterface, repo: BondDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(self) -> GetBondQueryResult:
        structlog.contextvars.bind_contextvars()
        async with self.__uow:
            bonds = await self.__repo.get_all()
            logger.info("Bonds got")
            return GetBondQueryResult().success(bonds)
