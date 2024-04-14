from dataclasses import dataclass, field
from datetime import date

import structlog
from app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from app.adapters.interface.unit_of_work import UOWInterface
from app.application.commands.command import CommandResult
from app.domain.const import UUID
from app.domain.exeption import ServiceError
from app.domain.portfolio import (
    BondOperationVO,
    BondType,
)

logger = structlog.get_logger(__name__)


@dataclass
class CreateOperationCommand:
    portfolio_id: UUID
    bond_id: UUID
    price_per_piece: float
    count: int
    date: date
    type: BondType


@dataclass
class CommandCreateOperationResult(CommandResult):
    result: None = None
    errors: list[ServiceError] = field(default_factory=list)


class CreateOperationService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(
        self, command: CreateOperationCommand
    ) -> CommandCreateOperationResult:
        structlog.contextvars.bind_contextvars(
            portfolio_id=command.portfolio_id, bond_id=command.bond_id
        )

        async with self.__uow:
            portfolio = await self.__repo.get_by_id(command.portfolio_id)
            operation = BondOperationVO(
                price_per_piece=command.price_per_piece,
                count=command.count,
                date=command.date,
                type=command.type,
            )
            portfolio.add_bond_operation(command.bond_id, operation=operation)
            await self.__repo.update(portfolio)

        logger.info("Operation created", operation_id=operation.id)
        return CommandCreateOperationResult().ok()
