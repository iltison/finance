from typing import Protocol

from sqlalchemy import text
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

    async def get_all(self) -> list[Bond]:
        result_query = list(
            await self.__session.execute(
                text("""SELECT * FROM bonds"""),
            ),
        )
        if len(result_query) == 0:
            return []

        return [Bond(name=i[1]) for i in result_query]
