from typing import Awaitable, Callable, Unpack

import pytest
import pytest_asyncio
import structlog
from mimesis import Finance

from app.domains.portfolio import BondEntity

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="function")
def bond_factory() -> Callable[[], BondEntity]:
    """
    Генерация Сущности облигации
    :return:
    """

    def factory(**fields: Unpack[BondEntity]) -> BondEntity:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        return BondEntity(
            bond_isin=fields.get("bond_isin") or Finance().stock_ticker(),
            operations=fields.get("operations") or [],
        )

    return factory


@pytest_asyncio.fixture
async def bond_builder(
    bond_factory,
) -> Callable[[], Awaitable[BondEntity]]:
    async def builder(**fields: Unpack[BondEntity]) -> BondEntity:
        bond_entity = bond_factory(**fields)
        logger.debug(
            "Added test bond",
            uuid=bond_entity.id,
            name=bond_entity.name,
            isin=bond_entity.bond_isin,
        )
        return bond_entity

    return builder
