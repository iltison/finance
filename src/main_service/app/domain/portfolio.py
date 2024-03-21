from dataclasses import dataclass, field

from main_service.app.domain.bond import Bond
from main_service.app.domain.const import UUID
from main_service.app.domain.operation import BondOperation


@dataclass
class Portfolio:
    name: str
    id: UUID = field(default_factory=UUID)
    bonds: list[Bond] = field(default_factory=list)

    def add_bond(self, bond: Bond):
        """
        Добавление облигации
        :param bond:
        :return:
        """
        self.bonds.append(bond)

    def add_bond_operation(self, bond_id: UUID, operation: BondOperation):
        """
        Добавление операции
        :param bond_id:
        :param operation:
        :return:
        """
        if len(self.bonds) == 0:
            raise

        for bond in self.bonds:
            if bond.id == bond_id:
                bond.operations.append(operation)
                break
        else:
            raise
