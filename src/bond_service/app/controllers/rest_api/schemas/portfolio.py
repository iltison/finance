from dataclasses import dataclass, field

from app.domains.const import UUID


@dataclass
class PortfolioInfoBondResponse:
    isin: str
    name: str
    current_price: float
    current_amount: float


@dataclass
class PortfolioInfoResponse:
    portfolio_id: UUID
    bonds: list[PortfolioInfoBondResponse] = field(default_factory=list)
