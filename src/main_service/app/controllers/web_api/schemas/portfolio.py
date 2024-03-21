import uuid
from dataclasses import dataclass, field


@dataclass
class PortfolioGetRequest:
    id: uuid.UUID


@dataclass
class PortfolioGetBondResponse:
    name: str


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
