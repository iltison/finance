import uuid
from dataclasses import dataclass, field
from datetime import date

from app.domain.portfolio import BondType


@dataclass
class PortfolioGetRequest:
    id: uuid.UUID


@dataclass
class PortfolioGetBondResponse:
    isin: str


@dataclass
class PortfolioGetResponse:
    id: uuid.UUID
    name: str
    bonds: list[PortfolioGetBondResponse] = field(default_factory=list)


@dataclass
class PortfolioCreateRequest:
    name: str


@dataclass
class PortfolioCreateResponse:
    id: uuid.UUID


@dataclass
class OperationCreateRequest:
    price_per_piece: float
    count: int
    date: date
    type: BondType


@dataclass
class BondCreateRequest:
    isin: str
