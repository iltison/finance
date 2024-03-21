import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from main_service.app.domain.bond import Bond
from main_service.app.domain.portfolio import Portfolio


@pytest.mark.asyncio
async def test_create_operation(test_client: AsyncClient, server):
    session_factory = server.services.provider.get(async_sessionmaker)

    name = "HARDCODE"
    bond_entity = Bond(name=name)
    portfolio_entity = Portfolio(name=name, bonds=[bond_entity])
    async with session_factory() as session:
        session.add(portfolio_entity)
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
