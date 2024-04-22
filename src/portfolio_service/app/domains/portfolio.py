import enum
from dataclasses import dataclass, field

from app.domains.const import UUID


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"


@dataclass
class PortfolioAggregate:
    name: str
    id: UUID = field(default_factory=UUID)
