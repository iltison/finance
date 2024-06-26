from dataclasses import dataclass, field

import structlog

from app.adapters.interface.portfolio_gateway import PortfolioGatewayInterface
from app.applications.commands.command import CommandResult
from app.domains.const import UUID
from app.domains.exeption import ServiceError
from app.domains.portfolio import BondEntity, PortfolioAggregate

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
    def __init__(self, gateway: PortfolioGatewayInterface):
        self.__gateway = gateway

    async def execute(
        self, command: CreateBondCommand
    ) -> CommandCreateBondResult:
        structlog.contextvars.bind_contextvars(bond_isin=command.isin)
        async with self.__gateway as gateway:
            portfolio = await gateway.get_portfolio_by_id(command.portfolio_id)
            # create portfolio if not exist
            if portfolio is None:
                portfolio = PortfolioAggregate(id=command.portfolio_id)

            # check if bond exist
            if portfolio.find_bond_by_isin(command.isin):
                logger.info("Bond exist")
                error = ServiceError("Bond exist")
                return CommandCreateBondResult().failed(exception=error)

            bond = BondEntity(bond_isin=command.isin)
            portfolio.add_bond(bond)
            await gateway.update(portfolio)
        logger.info("Bond created")
        return CommandCreateBondResult().ok()
