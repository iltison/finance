import pytest
import structlog
from httpx import AsyncClient

from tests.plugins.domain_factory.interface import (
    BondBuilderInterface,
    OperationFactoryInterface,
    PortfolioBuilderInterface,
)

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_create_portfolio_bond(
    test_client: AsyncClient,
    bond_builder: BondBuilderInterface,
    portfolio_builder: PortfolioBuilderInterface,
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
    bond_builder: BondBuilderInterface,
    portfolio_builder: PortfolioBuilderInterface,
    operation_factory: OperationFactoryInterface,
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


@pytest.mark.asyncio
async def test_create_bond_without_portfolio(
    test_client: AsyncClient,
    bond_builder: BondBuilderInterface,
    portfolio_factory,
):
    bond = await bond_builder()
    portfolio = portfolio_factory()

    response = await test_client.post(
        f"/portfolios/{str(portfolio.id)}/bonds",
        json={"isin": bond.bond_isin},
    )
    assert response is not None
    assert response.status_code == 200
