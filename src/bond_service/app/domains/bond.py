from dataclasses import dataclass


@dataclass
class BondAggregate:
    name: str
    isin: str
    # sometime zero sales, dont have price
    price: float | None
    coupon_amount: float
