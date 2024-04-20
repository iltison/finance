from dataclasses import dataclass, field

import structlog

from app.adapters.interface.portfolio_dao import PortfolioDAOInterface
from app.adapters.interface.unit_of_work import UOWInterface
from app.applications.commands.command import CommandResult
from app.domains.const import UUID
from app.domains.exeption import ServiceError
from app.domains.portfolio import BondEntity

logger = structlog.get_logger(__name__)


@dataclass
class CreateBondCommand:
    isin: str
    portfolio_id: UUID


@dataclass
class CommandCreateBondResult(CommandResult):
    result: None = None
    errors: list[ServiceError] = field(default_factory=list)


class CreateBondService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(
        self, command: CreateBondCommand
    ) -> CommandCreateBondResult:
        structlog.contextvars.bind_contextvars(bond_isin=command.isin)
        async with self.__uow:
            portfolio = await self.__repo.get_by_id(command.portfolio_id)
            bond = BondEntity(bond_isin=command.isin)
            portfolio.add_bond(bond)
            await self.__repo.update(portfolio)
        logger.info("Bond created")
        return CommandCreateBondResult().ok()
