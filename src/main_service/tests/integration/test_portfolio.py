import pytest
import structlog
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from main_service.app.domain.bond import Bond
from main_service.app.domain.portfolio import Portfolio

logger = structlog.get_logger(__name__)


# @pytest.mark.asyncio
# async def test_create_bond(test_client: AsyncClient):
#     response = await test_client.post("/bonds", json={"name": "HARDCODE"})
#     assert response is not None
#     assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_portfolio_by_id(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"
    portfolio_entity = Portfolio(name=name)
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
    portfolio_entity = Portfolio(name=name)

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

    name = "HARDCODE"
    bond_entity = Bond(name=name)
    portfolio_entity = Portfolio(name=name, bonds=[bond_entity])
    async with session_factory() as session:
        session.add(portfolio_entity)
        await session.commit()

    response = await test_client.get(f"/portfolios/{str(portfolio_entity.id)}")
    data = response.json()
    assert response is not None
    assert response.status_code == 200
    assert data == {
        "name": name,
        "id": str(portfolio_entity.id),
        "bonds": [{"name": name}],
    }
