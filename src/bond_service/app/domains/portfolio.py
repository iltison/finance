import enum
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domains.const import UUID


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"


@dataclass
class BondOperationEntity:
    price_per_piece: float
    count: int
    date: date
    type: BondType
    id: UUID = field(default_factory=UUID)


@dataclass
class BondEntity:
    id: UUID = field(default_factory=UUID)
    name: Optional[str] = None
    bond_isin: Optional[str] = None
    # текущая цена облигации
    current_price: Optional[float] = None
    profit: float = 0

    operations: list[BondOperationEntity] = field(default_factory=list)


@dataclass
class PortfolioAggregate:
    id: UUID = field(default_factory=UUID)
    bonds: list[BondEntity] = field(default_factory=list)

    def add_bond(self, bond: BondEntity):
        """
        Добавление облигации
        :param bond:
        :return:
        """
        self.bonds.append(bond)

    def find_bond_by_isin(self, isin: str):
        for bond in self.bonds:
            if bond.bond_isin == isin:
                return bond
        return None

    def add_bond_operation(
        self, bond_id: UUID, operation: BondOperationEntity
    ):
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
