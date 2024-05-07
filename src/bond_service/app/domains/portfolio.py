import enum
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domains.const import UUID


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"
    coupon = "coupon"


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
    portfolio_id: Optional[UUID] = None
    name: Optional[str] = None
    bond_isin: Optional[str] = None
    # текущая цена облигации. Цены может не быть
    current_price: Optional[float] = None
    # накопленная стоимость
    current_amount: float = 0
    # текущая цена - накопленная стоимость
    diff_amount_price: float = 0
    coupon_profit: float = 0
    # текущая цена - накопленная стоимость + купонный доход
    profit: float = 0
    count: int = 0

    operations: list[BondOperationEntity] = field(default_factory=list)

    def calc(self):
        for operation in self.operations:
            if operation.type == BondType.purchase:
                self.current_amount += (
                    operation.price_per_piece * operation.count
                )
                self.count += 1
            elif operation.type == BondType.sell:
                self.count -= 1
            elif operation.type == BondType.coupon:
                self.coupon_profit += (
                    operation.price_per_piece * operation.count
                )

        self.diff_amount_price = (
            self.current_price - self.current_amount
            if self.current_price
            else self.current_amount
        )
        self.profit = self.diff_amount_price + self.coupon_profit


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

    def calc(self):
        for bond in self.bonds:
            bond.calc()
