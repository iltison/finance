from typing import Optional

import aiohttp
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.const import UUID
from app.domains.portfolio import PortfolioAggregate

logger = structlog.get_logger(__name__)


class PortfolioGateway:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def __aenter__(self) -> "PortfolioGateway":
        return self

    async def get_portfolio_by_id(
        self, id: UUID
    ) -> Optional[PortfolioAggregate]:
        portfolio = await self.__get_by_id_from_database(id)
        if portfolio:
            await self.__get_moex_info(portfolio)
        return portfolio

    async def add(self, entity: PortfolioAggregate):
        self.__session.add(entity)

    async def update(self, entity: PortfolioAggregate):
        await self.__session.merge(entity)

    async def __get_by_id_from_database(
        self, id: UUID
    ) -> PortfolioAggregate | None:
        query = select(PortfolioAggregate).where(PortfolioAggregate.id == id)
        result = await self.__session.execute(query)
        result = result.scalars().first()
        return result

    async def __get_moex_info(self, portfolio: PortfolioAggregate):
        url = "http://iss.moex.com/iss/engines/stock/markets/bonds/securities.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    for row in data["securities"]["data"]:
                        if bond := portfolio.find_bond_by_isin(row[28]):
                            bond.current_price = (
                                row[3] * row[10] / 100 if row[3] else None
                            )
                            bond.name = row[2]
                    logger.info("Fetch moex data")
                else:
                    logger.warning("Failed to fetch moex data")
                    return None

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            logger.error(
                "Handled exception", type=exc_type.__name__, exc_info=True
            )
            await self.__session.rollback()
        else:
            await self.__session.commit()
        await self.__session.close()
