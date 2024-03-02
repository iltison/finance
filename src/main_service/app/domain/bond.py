import enum
from dataclasses import dataclass, field
from datetime import date


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"


@dataclass
class BondOperation:
    type: BondType
    date: date
    price: float


@dataclass
class BondProfit:
    price: float
    date: date


@dataclass
class Bond:
    name: str
    operations: list[BondOperation] = field(default_factory=list)
    profits: list[BondProfit] = field(default_factory=list)
