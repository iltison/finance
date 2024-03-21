from typing import Protocol

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

logger = structlog.get_logger(__name__)


class UOWInterface(Protocol):
    async def __aenter__(self) -> "UOWInterface": ...

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...


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
