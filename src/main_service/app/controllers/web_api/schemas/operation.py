from dataclasses import dataclass
from datetime import date, datetime

from main_service.app.domain.operation import BondType


@dataclass
class OperationCreateRequest:
    price_per_piece: float
    count: int
    date: date
    type: BondType

    def __post_init__(self):
        self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
