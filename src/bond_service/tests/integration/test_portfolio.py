import pytest
import structlog
from httpx import AsyncClient

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_get_existing_portfolio(
    test_client: AsyncClient,
    bond_builder,
    portfolio_builder,
    operation_builder,
):
    operation = await operation_builder()
    bond = await bond_builder(operations=[operation])
    portfolio = await portfolio_builder(bonds=[bond])

    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    assert response is not None
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_non_existing_portfolio(
    test_client: AsyncClient, portfolio_factory
):
    portfolio = portfolio_factory()
    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    assert response is not None
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_portfolio(test_client: AsyncClient, portfolio_factory):
    portfolio = portfolio_factory()

    response = await test_client.post(
        "/portfolios", json={"name": portfolio.name}
    )
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_get_existing_portfolios(
    test_client: AsyncClient,
    bond_builder,
    portfolio_builder,
    operation_builder,
):
    operation = await operation_builder()
    bond = await bond_builder(operations=[operation])
    await portfolio_builder(bonds=[bond])

    operation = await operation_builder()
    bond = await bond_builder(operations=[operation])
    await portfolio_builder(bonds=[bond])

    response = await test_client.get("/portfolios")

    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data != []


@pytest.mark.asyncio
async def test_get_non_existing_portfolios(test_client: AsyncClient):
    response = await test_client.get("/portfolios")

    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == []


@pytest.mark.asyncio
async def test_create_portfolio_bond(
    test_client: AsyncClient,
    bond_builder,
    portfolio_builder,
):
    bond = await bond_builder()
    portfolio = await portfolio_builder()

    response = await test_client.post(
        f"/portfolios/{str(portfolio.id)}/bonds",
        json={"isin": bond.bond_isin},
    )
    assert response is not None
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_portfolio_operation(
    test_client: AsyncClient,
    bond_builder,
    portfolio_builder,
    operation_factory,
):
    operation = operation_factory()
    bond = await bond_builder()
    portfolio = await portfolio_builder(bonds=[bond])

    response = await test_client.post(
        f"/portfolios/{str(portfolio.id)}/bonds/{str(bond.id)}/operations",
        json={
            "price_per_piece": operation.price_per_piece,
            "count": operation.count,
            "date": operation.date.isoformat(),
            "type": operation.type.value,
        },
    )

    assert response is not None
    assert response.status_code == 200
