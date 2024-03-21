from sqlalchemy.ext.asyncio import AsyncSession

from main_service.app.adapters.interface.unit_of_work import logger


class PostgresUOW:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def __aenter__(self) -> "PostgresUOW":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            logger.error(
                "Handled exception", type=exc_type.__name__, exc_info=True
            )
            await self.rollback()
        else:
            await self._session.commit()
        await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
