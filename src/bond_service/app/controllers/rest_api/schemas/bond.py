from dataclasses import dataclass
from datetime import date

from app.domains.portfolio import BondType


@dataclass
class OperationCreateRequest:
    price_per_piece: float
    count: int
    date: date
    type: BondType


@dataclass
class BondCreateRequest:
    isin: str
