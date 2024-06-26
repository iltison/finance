from typing import Protocol

from app.domains.const import UUID
from app.domains.portfolio import PortfolioAggregate


class PortfolioDAOInterface(Protocol):
    async def get_by_id(self, id: UUID) -> PortfolioAggregate | None: ...

    async def get_all(self) -> list[PortfolioAggregate]: ...

    async def add(self, entity: PortfolioAggregate): ...

    async def update(self, entity: PortfolioAggregate): ...
