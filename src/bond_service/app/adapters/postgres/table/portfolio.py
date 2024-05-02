import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid6 import uuid7

from app.adapters.postgres.base import mapper_registry, metadata
from app.domains.portfolio import (
    BondEntity,
    BondOperationEntity,
    BondType,
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
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    ),
)

portfolio_bonds_table = sa.Table(
    "portfolio_bonds",
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
    sa.Column(
        "portfolio_id",
        sa.UUID,
        sa.ForeignKey("portfolios.id", ondelete="CASCADE"),
        comment="Идентификатор портфеля",
    ),
    sa.Column(
        "bond_isin",
        sa.String,
        sa.ForeignKey("bonds.isin", ondelete="CASCADE"),
        comment="Идентификатор облигации",
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    ),
)

operations_table = sa.Table(
    "operations",
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
    sa.Column(
        "portfolio_bond_id",
        sa.UUID,
        sa.ForeignKey("portfolio_bonds.id", ondelete="CASCADE"),
        comment="Идентификатор отношения портфеля и облигации",
    ),
    sa.Column(
        "price_per_piece", sa.Float, default=0.0, comment="Цена за штуку"
    ),
    sa.Column("count", sa.Integer, default=0, comment="Количество"),
    sa.Column("date", sa.DateTime, comment="Дата покупки"),
    sa.Column("type", sa.Enum(BondType), comment="Тип операции"),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    ),
)


def mapper_portfolio():
    mapper_registry.map_imperatively(
        BondOperationEntity,
        operations_table,
    )

    mapper_registry.map_imperatively(
        BondEntity,
        portfolio_bonds_table,
        properties={
            "operations": relationship(BondOperationEntity, lazy="subquery")
        },
    )

    mapper_registry.map_imperatively(
        PortfolioAggregate,
        portfolio_table,
        properties={"bonds": relationship(BondEntity, lazy="subquery")},
    )
