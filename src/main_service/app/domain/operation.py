import enum
from dataclasses import dataclass, field
from datetime import date

from main_service.app.domain.const import UUID


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"


@dataclass
class BondOperation:
    price_per_piece: float
    count: int
    date: date
    type: BondType
    id: UUID = field(default_factory=UUID)
