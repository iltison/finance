import pytest
import structlog
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from main_service.app.domain.bond import BondAggregate
from main_service.app.domain.portfolio import (
    BondEntity,
    PortfolioAggregate,
)

logger = structlog.get_logger(__name__)


@pytest.mark.asyncio
async def test_get_portfolio_by_id(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"
    portfolio_entity = PortfolioAggregate(name=name)
    async with session_factory() as session:
        session.add(portfolio_entity)
        await session.commit()

    response = await test_client.get(f"/portfolios/{str(portfolio_entity.id)}")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {
        "name": "HARDCODE",
        "id": str(portfolio_entity.id),
        "bonds": [],
    }


@pytest.mark.asyncio
async def test_get_portfolios(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"
    portfolio_entity = PortfolioAggregate(name=name)

    async with session_factory() as session:
        session.add(portfolio_entity)
        await session.commit()

    response = await test_client.get("/portfolios")

    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == [
        {"name": "HARDCODE", "id": str(portfolio_entity.id), "bonds": []}
    ]


@pytest.mark.asyncio
async def test_get_empty_portfolios(test_client: AsyncClient):
    response = await test_client.get("/portfolios")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == []


@pytest.mark.asyncio
async def test_get_portfolio_with_bonds(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    isin = "HARDCODE"
    name = "HARDCODE"
    bond_entity = BondEntity(bond_isin=isin)
    bond_aggregate = BondAggregate(isin=isin, name=name)
    portfolio_entity = PortfolioAggregate(name=name, bonds=[bond_entity])
    async with session_factory() as session:
        session.add(portfolio_entity)
        session.add(bond_aggregate)
        await session.commit()

    response = await test_client.get(f"/portfolios/{str(portfolio_entity.id)}")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {
        "name": name,
        "id": str(portfolio_entity.id),
        "bonds": [{"isin": isin}],
    }


@pytest.mark.asyncio
async def test_create_portfolio(test_client: AsyncClient):
    name = "HARDCODE"

    response = await test_client.post("/portfolios", json={"name": name})
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_create_portfolio_bond(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)
    name = "HARDCODE"
    isin = "HARDCODE"

    portfolio = PortfolioAggregate(name=name)
    bond_aggregate = BondAggregate(isin=isin, name=name)
    async with session_factory() as session:
        session.add(portfolio)
        session.add(bond_aggregate)
        await session.commit()

    response = await test_client.post(
        f"/portfolios/{str(portfolio.id)}/bonds", json={"isin": isin}
    )
    assert response is not None
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_create_portfolio_bond_operation(
    test_client: AsyncClient, server
):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"
    isin = "HARDCODE"
    bond_entity = BondEntity(bond_isin=isin)
    bond_aggregate = BondAggregate(isin=isin, name=name)
    portfolio_entity = PortfolioAggregate(name=name, bonds=[bond_entity])
    async with session_factory() as session:
        session.add(portfolio_entity)
        session.add(bond_aggregate)
        await session.commit()

    response = await test_client.post(
        f"/portfolios/{str(portfolio_entity.id)}/bonds/{str(bond_entity.id)}/operations",
        json={
            "price_per_piece": 1000,
            "count": 4,
            "date": "2023-01-01",
            "type": "purchase",
        },
    )

    assert response is not None
    assert response.status_code == 201
