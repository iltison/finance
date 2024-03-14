import sqlalchemy as sa
from sqlalchemy.sql import func

from main_service.app.domain.operation import BondType
from uuid6 import uuid7

metadata = sa.MetaData()

portfolio_table = sa.Table(
    "portfolios",
    metadata,
    sa.Column("id", sa.UUID, primary_key=True, index=True, default=uuid7, unique=True, comment="Идентификатор"),
    sa.Column("name", sa.String, comment="Наименование облигации"),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), comment="Дата создания записи"),
)

bonds_table = sa.Table(
    "bonds",
    metadata,
    sa.Column("id", sa.UUID, primary_key=True, index=True, default=uuid7, unique=True, comment="Идентификатор"),
    sa.Column(
        "portfolio_id", sa.UUID, sa.ForeignKey("portfolios.id", ondelete="CASCADE"), comment="Идентификатор портфеля"
    ),
    sa.Column("name", sa.String, comment="Наименование облигации"),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), comment="Дата создания записи"),
)

operations_table = sa.Table(
    "operations",
    metadata,
    sa.Column("id", sa.UUID, primary_key=True, index=True, default=uuid7, unique=True, comment="Идентификатор"),
    sa.Column(
        "portfolio_bond_id",
        sa.UUID,
        sa.ForeignKey("bonds.id", ondelete="CASCADE"),
        comment="Идентификатор отношения портфеля и облигации",
    ),
    sa.Column("price_per_piece", sa.Float, default=0.0, comment="Цена за штуку"),
    sa.Column("count", sa.Integer, default=0, comment="Количество"),
    sa.Column("date", sa.DateTime, comment="Дата покупки"),
    sa.Column("type", sa.Enum(BondType), comment="Тип операции"),
    sa.Column("created_at", sa.DateTime, server_default=func.now(), comment="Дата создания записи"),
)
