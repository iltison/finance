from dataclasses import dataclass, field

from main_service.app.domain.bond import Bond
from main_service.app.domain.const import UUID


@dataclass
class Portfolio:
    name: str
    id: UUID = field(default_factory=UUID)
    bonds: list[Bond] = field(default_factory=list)
