from dataclasses import dataclass, field

from main_service.app.domain.const import UUID
from main_service.app.domain.operation import BondOperation


@dataclass
class Bond:
    name: str
    id: UUID = field(default_factory=UUID)
    operations: list[BondOperation] = field(default_factory=list)
