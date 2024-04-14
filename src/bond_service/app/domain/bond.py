from dataclasses import dataclass, field

from app.domain.const import UUID


@dataclass
class BondAggregate:
    name: str
    isin: str
    id: UUID = field(default_factory=UUID)
