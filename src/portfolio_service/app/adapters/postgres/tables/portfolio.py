import sqlalchemy as sa
from sqlalchemy.sql import func
from uuid6 import uuid7

from app.adapters.postgres.base import mapper_registry, metadata
from app.domains.portfolio import (
    PortfolioAggregate,
)

portfolio_table = sa.Table(
    "portfolios",
    metadata,
    sa.Column(
        "id",
        sa.UUID,
        primary_key=True,
        index=True,
        default=uuid7,
        unique=True,
        comment="Идентификатор",
    ),
    sa.Column("name", sa.String, comment="Наименование облигации"),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    ),
)


def mapper_portfolio():
    mapper_registry.map_imperatively(
        PortfolioAggregate,
        portfolio_table,
    )
