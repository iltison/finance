from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.domain.const import UUID
from main_service.app.domain.portfolio import PortfolioAggregate


class PortfolioDAO:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_id(self, id: UUID) -> PortfolioAggregate | None:
        query = select(PortfolioAggregate).where(PortfolioAggregate.id == id)
        result = await self.__session.execute(query)
        result = result.scalars().first()
        return result

    async def add(self, entity: PortfolioAggregate):
        self.__session.add(entity)

    async def get_all(self) -> list[PortfolioAggregate]:
        query = select(PortfolioAggregate)
        result = await self.__session.execute(query)
        return cast(list[PortfolioAggregate], result.scalars().all())

    async def update(self, entity: PortfolioAggregate):
        await self.__session.merge(entity)
