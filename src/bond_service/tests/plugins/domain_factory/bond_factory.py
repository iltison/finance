from typing import Awaitable, Callable, Unpack

import pytest
import pytest_asyncio
import structlog
from dishka import AsyncContainer
from mimesis import Field, Locale

from app.adapters.interface.bond_dao import BondDAOInterface
from app.adapters.interface.unit_of_work import UOWInterface
from app.domain.bond import BondAggregate
from app.domain.portfolio import BondEntity

logger = structlog.get_logger(__name__)


@pytest.fixture(scope="function")
def _bond_factory() -> Callable[[], BondAggregate]:
    """
    Генерация Агрегата облигации, тк в системе должна находиться облигация
    при добавлении
    :return:
    """

    def factory(**fields: Unpack[BondAggregate]) -> BondAggregate:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        mf = Field(locale=Locale.EN)
        return BondAggregate(
            isin=fields.get("isin") or mf("word"),
            name=fields.get("name") or mf("word"),
        )

    return factory


@pytest.fixture(scope="function")
def bond_factory() -> Callable[[], BondEntity]:
    """
    Генерация Сущности облигации
    :return:
    """

    def factory(**fields: Unpack[BondEntity]) -> BondEntity:
        # TODO: придумать как чтобы параметры передавались в датакласс явно
        mf = Field(locale=Locale.EN)
        return BondEntity(
            bond_isin=fields.get("bond_isin") or mf("word"),
            operations=fields.get("operations") or [],
        )

    return factory


@pytest_asyncio.fixture
async def _bond_builder(
    container: AsyncContainer, _bond_factory
) -> Callable[[], Awaitable[BondAggregate]]:
    """
    Создание Агрегата облигации, тк в системе должна находиться облигация
    при добавлении
    :return:
    """

    async def builder(**fields: Unpack[BondAggregate]) -> BondAggregate:
        uow = await container.get(UOWInterface)
        repo = await container.get(BondDAOInterface)

        bond_aggregate = _bond_factory(**fields)

        async with uow:
            await repo.add(bond_aggregate)

            logger.debug(
                "Added test bond aggregate",
                uuid=bond_aggregate.id,
                name=bond_aggregate.name,
            )

        return bond_aggregate

    return builder


@pytest_asyncio.fixture
async def bond_builder(
    bond_factory, _bond_builder
) -> Callable[[], Awaitable[BondEntity]]:
    async def builder(**fields: Unpack[BondEntity]) -> BondEntity:
        bond_entity = bond_factory(**fields)
        bond_aggregate = await _bond_builder(isin=bond_entity.bond_isin)

        logger.debug(
            "Added test bond entity",
            uuid=bond_aggregate.id,
            name=bond_aggregate.name,
        )
        return bond_entity

    return builder
