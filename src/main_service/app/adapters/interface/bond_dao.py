from typing import Protocol

from main_service.app.domain.bond import Bond


class BondDAOInterface(Protocol):
    async def get_by_id(self, name: str) -> Bond | None: ...

    async def get_all(self) -> list[Bond]: ...

    async def add(self, entity: Bond): ...
