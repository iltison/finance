from typing import Awaitable, Callable, Unpack

import pytest
import pytest_asyncio
import structlog
from mimesis import Field, Schema

from app.domains.portfolio import BondOperationEntity, BondType

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="function")
def operation_factory() -> Callable[[], BondOperationEntity]:
    def factory(**fields: Unpack[BondOperationEntity]) -> BondOperationEntity:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        def _random_type(random, **kwargs):
            return random.choice([BondType.purchase, BondType.sell], **kwargs)

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

        return BondOperationEntity(
            **{
                **schema_operation.create()[0],
                **fields,
            }
        )

    return factory


@pytest_asyncio.fixture
async def operation_builder(
    operation_factory,
) -> Callable[[], Awaitable[BondOperationEntity]]:
    async def builder(
        **fields: Unpack[BondOperationEntity],
    ) -> BondOperationEntity:
        operation_vo = operation_factory(**fields)

        logger.debug("Added test operation", uuid=operation_vo.id)
        return operation_vo

    return builder
