from typing import Unpack

import pytest
import pytest_asyncio
import structlog
from app.adapters.interface.portfolio_dao import PortfolioDAOInterface
from app.adapters.interface.unit_of_work import UOWInterface
from app.domain.bond import BondAggregate
from app.domain.portfolio import PortfolioAggregate
from dishka import AsyncContainer
from mimesis import Field, Locale, Schema

logger = structlog.get_logger(__name__)


@pytest.fixture(params=[Locale.RU, Locale.EN], scope="function")
def portfolio_factory(request):
    def factory(**fields: Unpack[PortfolioAggregate]) -> PortfolioAggregate:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        mf = Field(locale=request.param)
        schema_portfolio = Schema(
            schema=lambda: {
                "name": mf("word"),
            }
        )

        return PortfolioAggregate(
            **{
                **schema_portfolio.create()[0],
                **fields,
            }
        )

    return factory


@pytest_asyncio.fixture
async def portfolio_builder(container: AsyncContainer, portfolio_factory):
    async def builder(**fields: Unpack[BondAggregate]):
        uow = await container.get(UOWInterface)
        repo = await container.get(PortfolioDAOInterface)

        portfolio_entity = portfolio_factory(**fields)
        async with uow:
            await repo.add(portfolio_entity)

            logger.debug(
                "Added test portfolio",
                uuid=portfolio_entity.id,
                name=portfolio_entity.name,
            )
        return portfolio_entity

    return builder
