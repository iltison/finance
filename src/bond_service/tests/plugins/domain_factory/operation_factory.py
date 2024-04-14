from typing import Unpack

import pytest
import pytest_asyncio
import structlog
from app.domain.portfolio import BondOperationVO, BondType
from dishka import AsyncContainer
from mimesis import Field, Schema

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="function")
def operation_factory():
    def factory(**fields: Unpack[BondOperationVO]) -> BondOperationVO:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        def _random_type(random, **kwargs):
            return random.choice([BondType.purchase, BondType.sell])

        mf = Field()
        mf.register_handler("random_type", _random_type)

        schema_operation = Schema(
            schema=lambda: {
                "price_per_piece": mf("price"),
                "count": mf("integers")[0],
                "date": mf("date"),
                "type": mf("random_type"),
            }
        )

        return BondOperationVO(
            **{
                **schema_operation.create()[0],
                **fields,
            }
        )

    return factory


@pytest_asyncio.fixture
async def operation_builder(container: AsyncContainer, operation_factory):
    async def builder(**fields: Unpack[BondOperationVO]):
        operation_vo = operation_factory(**fields)

        logger.debug("Added test operation", uuid=operation_vo.id)
        return operation_vo

    return builder
