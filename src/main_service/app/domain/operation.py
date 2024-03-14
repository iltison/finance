import datetime
import enum
from dataclasses import dataclass, field
from datetime import date

from main_service.app.domain.const import UUID


class BondType(enum.Enum):
    purchase = "purchase"
    sell = "sell"


@dataclass
class BondOperation:
    price: float
    date: date
    type: BondType
    created_at: datetime
    id: UUID = field(default_factory=UUID)
