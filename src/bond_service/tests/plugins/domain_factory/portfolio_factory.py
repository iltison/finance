from typing import Awaitable, Callable, Unpack

import pytest
import pytest_asyncio
import structlog
from dishka import AsyncContainer
from mimesis import Schema

from app.adapters.interface.portfolio_dao import PortfolioDAOInterface
from app.adapters.interface.unit_of_work import UOWInterface
from app.domains.portfolio import PortfolioAggregate
from tests.plugins.domain_factory.interface import PortfolioFactoryInterface

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="function")
def portfolio_factory() -> Callable[[], PortfolioAggregate]:
    def factory(**fields: Unpack[PortfolioAggregate]) -> PortfolioAggregate:
        schema_portfolio = Schema(schema=lambda: {})

        return PortfolioAggregate(
            **{
                **schema_portfolio.create()[0],
                **fields,
            }
        )

    return factory


@pytest_asyncio.fixture
async def portfolio_builder(
    container: AsyncContainer, portfolio_factory: PortfolioFactoryInterface
) -> Callable[[], Awaitable[PortfolioAggregate]]:
    async def builder(
        **fields: Unpack[PortfolioAggregate],
    ) -> PortfolioAggregate:
        uow = await container.get(UOWInterface)
        repo = await container.get(PortfolioDAOInterface)

        portfolio_entity = portfolio_factory(**fields)
        async with uow:
            await repo.add(portfolio_entity)

            logger.debug(
                "Added test portfolio",
                uuid=portfolio_entity.id,
            )
        return portfolio_entity

    return builder
