from typing import Protocol

from app.domains.const import UUID
from app.domains.portfolio import PortfolioAggregate


class PortfolioGatewayInterface(Protocol):
    async def __aenter__(self) -> "PortfolioGatewayInterface": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...

    async def get_portfolio_by_id(
        self, id: UUID
    ) -> PortfolioAggregate | None: ...

    async def get_all(self) -> list[PortfolioAggregate]: ...

    async def add(self, entity: PortfolioAggregate): ...

    async def update(self, entity: PortfolioAggregate): ...
