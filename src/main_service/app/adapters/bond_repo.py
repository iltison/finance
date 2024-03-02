from typing import Protocol

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.domain.bond import Bond


class BondRepoInterface(Protocol):
    async def get(self, name: str) -> Bond | None: ...

    async def add(self, entity: Bond): ...


class BondRepoDatabase:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def get(self, name: str) -> Bond | None:
        result = list(
            await self.__session.execute(
                text("""SELECT * FROM bonds where name = :name"""),
                {"name": name},
            ),
        )
        if len(result) == 0:
            return None

        return Bond(name=result[0][1])

    async def add(self, entity: Bond):
        await self.__session.execute(
            text(
                """
            INSERT INTO bonds (name)
            VALUES (:name);
            """,
            ),
            {"name": entity.name},
        )
