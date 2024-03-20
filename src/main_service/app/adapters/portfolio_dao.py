from typing import Protocol

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.domain.const import UUID
from main_service.app.domain.portfolio import Portfolio
from typing import cast


class PortfolioDAOInterface(Protocol):
    async def get_by_id(self, id: UUID) -> Portfolio | None: ...

    async def get_all(self) -> list[Portfolio]: ...

    async def add(self, entity: Portfolio): ...


class PortfolioDAO:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_id(self, id: UUID) -> Portfolio | None:
        query = select(Portfolio).where(Portfolio.id == id)
        result = await self.__session.execute(query)
        result = result.scalars().first()
        return result

    async def add(self, entity: Portfolio):
        query = insert(Portfolio).values(name=entity.name)
        await self.__session.execute(query)

    async def get_all(self) -> list[Portfolio]:
        query = select(Portfolio)
        result = await self.__session.execute(query)
        return cast(list[Portfolio], result.scalars().all())
