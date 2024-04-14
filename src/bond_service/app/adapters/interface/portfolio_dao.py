from typing import Protocol

from main_service.app.domain.const import UUID
from main_service.app.domain.portfolio import PortfolioAggregate


class PortfolioDAOInterface(Protocol):
    async def get_by_id(self, id: UUID) -> PortfolioAggregate | None: ...

    async def get_all(self) -> list[PortfolioAggregate]: ...

    async def add(self, entity: PortfolioAggregate): ...

    async def update(self, entity: PortfolioAggregate): ...
