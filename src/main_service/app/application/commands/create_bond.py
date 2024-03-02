from dataclasses import dataclass

import structlog

from main_service.app.adapters.bond_repo import BondRepoInterface
from main_service.app.adapters.unit_of_work import UOWInterface
from main_service.app.application.commands.command import CommandResult
from main_service.app.domain.bond import Bond
from main_service.app.domain.exeption import ValueExistError

logger = structlog.get_logger("service")


@dataclass
class CreateBondCommand:
    name: str


class CreateBondService:
    def __init__(self, uow: UOWInterface, repo: BondRepoInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(self, command: CreateBondCommand) -> CommandResult:
        structlog.contextvars.bind_contextvars(bond_name=command.name)
        async with self.__uow:
            bond = await self.__repo.get(command.name)
            if bond is not None:
                logger.debug("Bond exist")
                return CommandResult().failed(exception=ValueExistError(f"Bond {command.name} exist "))
            await self.__repo.add(Bond(name=command.name))
        logger.info("Bond created")
        return CommandResult().ok()
