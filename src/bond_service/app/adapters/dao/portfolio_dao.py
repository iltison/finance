from typing import Optional

import aiohttp
import structlog
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domains.const import UUID
from app.domains.portfolio import BondEntity, PortfolioAggregate

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

            portfolio.calc()

        return portfolio

    async def add(self, entity: PortfolioAggregate):
        if len(entity.bonds) == 0:
            return
        statement: str = """
                INSERT INTO bonds (id, portfolio_id, bond_isin)
                VALUES (:id, :portfolio_id, :bond_isin)
                """
        values = [
            {
                "id": bond.id,
                "portfolio_id": entity.id,
                "bond_isin": bond.bond_isin,
            }
            for bond in entity.bonds
        ]

        await self.__session.execute(text(statement), values)

    async def update(self, entity: PortfolioAggregate):
        if len(entity.bonds) == 0:
            return
        statement: str = """
        INSERT INTO bonds (id, portfolio_id, bond_isin)
        VALUES (:id, :portfolio_id, :bond_isin)
        ON CONFLICT (id) DO NOTHING"""

        values = [
            {
                "id": bond.id,
                "portfolio_id": entity.id,
                "bond_isin": bond.bond_isin,
            }
            for bond in entity.bonds
        ]

        await self.__session.execute(text(statement), values)

    async def __get_by_id_from_database(
        self, id: UUID
    ) -> PortfolioAggregate | None:
        portfolio = PortfolioAggregate(id=id)
        statement: str = """
                SELECT id, portfolio_id, bond_isin
                FROM bonds
                WHERE portfolio_id = :id
                """

        result = await self.__session.execute(text(statement), {"id": id})
        for bond in result:
            portfolio.bonds.append(
                BondEntity(
                    id=bond[0],
                    portfolio_id=bond[1],
                    bond_isin=bond[2],
                )
            )

        return portfolio

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
