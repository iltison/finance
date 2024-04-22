import pytest
import structlog
from httpx import AsyncClient

from tests.plugins.domain_factory.interface import (
    PortfolioBuilderInterface,
    PortfolioFactoryInterface,
)

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_get_existing_portfolio(
    test_client: AsyncClient,
    portfolio_builder: PortfolioBuilderInterface,
):
    portfolio = await portfolio_builder()
    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    assert response is not None
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_non_existing_portfolio(
    test_client: AsyncClient, portfolio_factory: PortfolioFactoryInterface
):
    portfolio = portfolio_factory()
    response = await test_client.get(f"/portfolios/{str(portfolio.id)}")

    assert response is not None
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_portfolio(
    test_client: AsyncClient, portfolio_factory: PortfolioFactoryInterface
):
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
    portfolio_builder: PortfolioBuilderInterface,
):
    await portfolio_builder()
    await portfolio_builder()

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
