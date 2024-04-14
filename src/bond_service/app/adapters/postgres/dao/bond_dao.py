from typing import cast

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.domain.bond import BondAggregate
from main_service.app.domain.const import UUID


class BondDAO:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get_by_id(self, id: UUID) -> BondAggregate | None: ...

    async def add(self, entity: BondAggregate):
        self.__session.add(entity)

    async def get_all(self) -> list[BondAggregate]:
        query = select(BondAggregate)
        result = await self.__session.execute(query)
        return cast(list[BondAggregate], result.scalars().all())

    async def update(self, entity: BondAggregate):
        await self.__session.merge(entity)
