from dataclasses import dataclass

from structlog import get_logger

from main_service.app.adapters.bond_repo import BondRepoInterface
from main_service.app.adapters.UOW import UOWInterface
from main_service.app.domain.bond import Bond
from main_service.app.domain.exeption import ValueExist

logger = get_logger()


@dataclass
class CreateBondCommand:
    name: str


def create_bond(repo: BondRepoInterface, uow: UOWInterface, command: CreateBondCommand):
    with uow:
        bond = repo.get(command.name)

        if bond is None:
            raise ValueExist(f"Облигация с именем {command.name} существует")

        repo.add(Bond(name=command.name))
