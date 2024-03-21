from dataclasses import dataclass, field

import structlog

from main_service.app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from main_service.app.adapters.interface.unit_of_work import UOWInterface
from main_service.app.application.commands.command import CommandResult
from main_service.app.domain.const import UUID
from main_service.app.domain.exeption import ServiceError
from main_service.app.domain.portfolio import BondEntity

logger = structlog.get_logger(__name__)


@dataclass
class CreateBondCommand:
    name: str
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
        structlog.contextvars.bind_contextvars(bond_name=command.name)
        async with self.__uow:
            portfolio = await self.__repo.get_by_id(command.portfolio_id)
            bond = BondEntity(name=command.name)
            portfolio.add_bond(bond)
            await self.__repo.update(portfolio)
        logger.info("Bond created")
        return CommandCreateBondResult().ok()
