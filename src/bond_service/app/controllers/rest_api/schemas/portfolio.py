from dataclasses import dataclass, field

from app.domains.const import UUID


@dataclass
class PortfolioInfoBondResponse:
    bond_id: UUID
    isin: str
    name: str
    current_price: float
    current_amount: float
    profit: float
    coupon_profit: float
    diff_amount_price: float
    count: int


@dataclass
class PortfolioInfoResponse:
    portfolio_id: UUID
    bonds: list[PortfolioInfoBondResponse] = field(default_factory=list)
