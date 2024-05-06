from dataclasses import dataclass, field
from datetime import date

import structlog

from app.adapters.interface.portfolio_gateway import PortfolioGatewayInterface
from app.applications.commands.command import CommandResult
from app.domains.const import UUID
from app.domains.exeption import ServiceError
from app.domains.portfolio import BondOperationEntity, BondType

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
    def __init__(self, gateway: PortfolioGatewayInterface):
        self.__gateway = gateway

    async def execute(
        self, command: CreateOperationCommand
    ) -> CommandCreateOperationResult:
        structlog.contextvars.bind_contextvars(
            portfolio_id=command.portfolio_id, bond_id=command.bond_id
        )

        async with self.__gateway as gateway:
            portfolio = await gateway.get_portfolio_by_id(command.portfolio_id)
            operation = BondOperationEntity(
                price_per_piece=command.price_per_piece,
                count=command.count,
                date=command.date,
                type=command.type,
            )
            portfolio.add_bond_operation(command.bond_id, operation=operation)
            await gateway.update(portfolio)

        logger.info("Operation created", operation_id=operation.id)
        return CommandCreateOperationResult().ok()
