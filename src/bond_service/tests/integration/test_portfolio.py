from typing import Callable

import pytest
import pytest_asyncio
import structlog
from app.adapters.interface.bond_dao import BondDAOInterface
from app.adapters.interface.portfolio_dao import (
    PortfolioDAOInterface,
)
from app.adapters.interface.unit_of_work import UOWInterface
from app.domain.bond import BondAggregate
from app.domain.portfolio import (
    BondEntity,
    PortfolioAggregate,
)
from dishka import AsyncContainer
from httpx import AsyncClient
from mimesis.schema import Field, Locale

logger = structlog.get_logger(__name__)


@pytest_asyncio.fixture
async def uow(container: AsyncContainer) -> UOWInterface:
    yield await container.get(UOWInterface)


@pytest_asyncio.fixture
async def repo_portfolio(container: AsyncContainer) -> PortfolioDAOInterface:
    yield await container.get(PortfolioDAOInterface)


@pytest_asyncio.fixture
async def repo_bond(container: AsyncContainer) -> BondDAOInterface:
    yield await container.get(BondDAOInterface)


@pytest.fixture
def random_name() -> Callable[[], str]:
    field = Field(locale=Locale.RU)
    return lambda: field("word")


@pytest.fixture
def random_isin() -> Callable[[], str]:
    field = Field(locale=Locale.RU)
    return lambda: field("word")


@pytest_asyncio.fixture(scope="function")
async def bond_builder(
    uow: UOWInterface, repo_bond: BondDAOInterface, random_name, random_isin
) -> BondAggregate:
    bond_entity = BondAggregate(name=random_name(), isin=random_isin())

    async with uow:
        await repo_bond.add(bond_entity)

        logger.info(
            "Added test bond", uuid=bond_entity.id, name=bond_entity.name
        )
    return bond_entity


@pytest_asyncio.fixture(scope="function")
async def portfolio_builder(
    uow: UOWInterface,
    repo_portfolio: PortfolioDAOInterface,
    random_name,
    bond_builder,
) -> PortfolioAggregate:
    """
    Создание портфеля
    :return:
    """
    bond_entity = BondEntity(bond_isin=bond_builder.isin)
    portfolio_entity = PortfolioAggregate(
        name=random_name(), bonds=[bond_entity]
    )

    async with uow:
        await repo_portfolio.add(portfolio_entity)

        logger.info(
            "Added test portfolio",
            uuid=portfolio_entity.id,
            name=portfolio_entity.name,
        )
    return portfolio_entity


@pytest.mark.asyncio
async def test_get_portfolio_by_id(
    test_client: AsyncClient, portfolio_builder: PortfolioAggregate
):
    portfolio_entity = portfolio_builder
    response = await test_client.get(f"/portfolios/{str(portfolio_entity.id)}")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {
        "name": portfolio_entity.name,
        "id": str(portfolio_entity.id),
        "bonds": [],
    }


@pytest.mark.asyncio
async def test_get_portfolios(
    test_client: AsyncClient, portfolio_builder: PortfolioAggregate
):
    portfolio_entity = portfolio_builder

    response = await test_client.get("/portfolios")

    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == [
        {
            "name": portfolio_entity.name,
            "id": str(portfolio_entity.id),
            "bonds": [],
        }
    ]


@pytest.mark.asyncio
async def test_get_empty_portfolios(test_client: AsyncClient):
    response = await test_client.get("/portfolios")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == []


@pytest.mark.asyncio
async def test_get_portfolio_with_bonds(
    test_client: AsyncClient, portfolio_builder: PortfolioAggregate
):
    response = await test_client.get(
        f"/portfolios/{str(portfolio_builder.id)}"
    )
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {
        "name": portfolio_builder.name,
        "id": str(portfolio_builder.id),
        "bonds": [{"isin": str(portfolio_builder.bonds[0].id)}],
    }


@pytest.mark.asyncio
async def test_create_portfolio(test_client: AsyncClient, random_name):
    response = await test_client.post(
        "/portfolios", json={"name": random_name()}
    )
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_create_portfolio_bond(
    test_client: AsyncClient, portfolio_builder: PortfolioAggregate
):
    response = await test_client.post(
        f"/portfolios/{str(portfolio_builder.id)}/bonds",
        json={"isin": portfolio_builder.bonds[0].bond_isin},
    )
    assert response is not None
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_portfolio_bond_operation(
    test_client: AsyncClient, portfolio_builder: PortfolioAggregate
):
    response = await test_client.post(
        f"/portfolios/{str(portfolio_builder.id)}/bonds/{str(portfolio_builder.bonds[0].id)}/operations",
        json={
            "price_per_piece": 1000,
            "count": 4,
            "date": "2023-01-01",
            "type": "purchase",
        },
    )

    assert response is not None
    assert response.status_code == 200
