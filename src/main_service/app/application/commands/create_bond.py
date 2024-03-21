from dataclasses import dataclass, field

import structlog

from main_service.app.adapters.interface.bond_dao import BondDAOInterface
from main_service.app.adapters.interface.unit_of_work import UOWInterface
from main_service.app.application.commands.command import CommandResult
from main_service.app.domain.bond import Bond
from main_service.app.domain.exeption import ServiceError, ValueExistError

logger = structlog.get_logger(__name__)


@dataclass
class CreateBondCommand:
    name: str


@dataclass
class CommandCreateBondResult(CommandResult):
    result: None = None
    errors: list[ServiceError] = field(default_factory=list)


class CreateBondService:
    def __init__(self, uow: UOWInterface, repo: BondDAOInterface):
        self.__uow = uow
        self.__repo = repo

    async def execute(
        self, command: CreateBondCommand
    ) -> CommandCreateBondResult:
        structlog.contextvars.bind_contextvars(bond_name=command.name)
        async with self.__uow:
            bond = await self.__repo.get_by_id(command.name)
            if bond is not None:
                logger.debug("Bond exist")
                return CommandCreateBondResult().failed(
                    exception=ValueExistError(f"Bond {command.name} exist ")
                )
            await self.__repo.add(Bond(name=command.name))
        logger.info("Bond created")
        return CommandCreateBondResult().ok()
