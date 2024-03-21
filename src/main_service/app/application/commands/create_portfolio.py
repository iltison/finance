from dataclasses import dataclass, field
from typing import Optional

import structlog

from main_service.app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from main_service.app.adapters.interface.unit_of_work import UOWInterface
from main_service.app.application.commands.command import CommandResult
from main_service.app.domain.const import UUID
from main_service.app.domain.exeption import ServiceError
from main_service.app.domain.portfolio import Portfolio

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
            portfolio = Portfolio(name=command.name)
            await self.__repo.add(portfolio)
        logger.info("Portfolio created")
        return CommandCreatePortfolioResult().ok(portfolio.id)
