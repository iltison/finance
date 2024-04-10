from typing import Protocol

from main_service.app.domain.bond import BondAggregate
from main_service.app.domain.const import UUID


class BondDAOInterface(Protocol):
    async def get_by_id(self, id: UUID) -> BondAggregate | None: ...

    async def get_all(self) -> list[BondAggregate]: ...

    async def add(self, entity: BondAggregate): ...

    async def update(self, entity: BondAggregate): ...
