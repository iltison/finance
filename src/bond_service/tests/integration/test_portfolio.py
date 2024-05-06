import pytest
import structlog
from httpx import AsyncClient

from tests.plugins.domain_factory.interface import (
    BondBuilderInterface,
    PortfolioBuilderInterface,
)

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_get_portfolio_without_bond(
    test_client: AsyncClient,
    portfolio_builder: PortfolioBuilderInterface,
):
    portfolio = await portfolio_builder()
    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    result = response.json()

    assert response is not None
    assert response.status_code == 200
    assert result["portfolio_id"] == str(portfolio.id)
    assert len(result["bonds"]) == 0


@pytest.mark.asyncio
async def test_get_portfolio_with_bonds(
    test_client: AsyncClient,
    portfolio_builder: PortfolioBuilderInterface,
    bond_builder: BondBuilderInterface,
):
    bond1 = await bond_builder()
    bond2 = await bond_builder()
    portfolio = await portfolio_builder(bonds=[bond1, bond2])

    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    result = response.json()

    assert response is not None
    assert response.status_code == 200
    assert result["portfolio_id"] == str(portfolio.id)
    assert len(result["bonds"]) == 2
