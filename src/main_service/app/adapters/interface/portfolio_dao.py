from typing import Protocol

from main_service.app.domain.const import UUID
from main_service.app.domain.portfolio import Portfolio


class PortfolioDAOInterface(Protocol):
    async def get_by_id(self, id: UUID) -> Portfolio | None: ...

    async def get_all(self) -> list[Portfolio]: ...

    async def add(self, entity: Portfolio): ...

    async def update(self, entity: Portfolio): ...
