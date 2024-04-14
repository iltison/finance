from dataclasses import dataclass, field

from main_service.app.domain.const import UUID


@dataclass
class BondAggregate:
    name: str
    isin: str
    id: UUID = field(default_factory=UUID)
