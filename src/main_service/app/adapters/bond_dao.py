from typing import Protocol

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.domain.bond import Bond


class BondDAOInterface(Protocol):
    async def get_by_id(self, name: str) -> Bond | None: ...

    async def get_all(self) -> list[Bond]: ...

    async def add(self, entity: Bond): ...


class BondDAODatabase:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_id(self, name: str) -> Bond | None:
        query = select(Bond).where(Bond.name == name)
        print(query)
        result = await self.__session.execute(query)
        result = result.first()
        return result

    async def add(self, entity: Bond):
        query = insert(Bond).values(name=entity.name)
        await self.__session.execute(query)

    async def get_all(self) -> list[Bond]:
        query = select(Bond)
        result = await self.__session.execute(query)
        return result.scalars().all()