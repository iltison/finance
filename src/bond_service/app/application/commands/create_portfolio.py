from dataclasses import dataclass, field
from typing import Optional

import structlog
from app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from app.adapters.interface.unit_of_work import UOWInterface
from app.application.commands.command import CommandResult
from app.domain.const import UUID
from app.domain.exeption import ServiceError
from app.domain.portfolio import PortfolioAggregate

logger = structlog.get_logger(__name__)


@dataclass
class CreatePortfolioCommand:
    name: str


@dataclass
class CommandCreatePortfolioResult(CommandResult):
    result: Optional[UUID] = None
    errors: list[ServiceError] = field(default_factory=list)


class CreatePortfolioService:
    def __init__(self, uow: UOWInterface, repo: PortfolioDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(
        self, command: CreatePortfolioCommand
    ) -> CommandCreatePortfolioResult:
        structlog.contextvars.bind_contextvars(portfolio_name=command.name)

        async with self.__uow:
            portfolio = PortfolioAggregate(name=command.name)
            await self.__repo.add(portfolio)
        logger.info("Portfolio created")
        return CommandCreatePortfolioResult().ok(portfolio.id)
