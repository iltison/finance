from dataclasses import dataclass, field
from datetime import date


@dataclass
class BondOperation:
    type: str
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
