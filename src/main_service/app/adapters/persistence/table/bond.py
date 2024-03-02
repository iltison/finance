import sqlalchemy as sa
from sqlalchemy.sql import func

from main_service.app.domain.bond import BondType

metadata = sa.MetaData()

bonds_table = sa.Table(
    "bonds",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True, index=True),
    sa.Column("name", sa.String),
    sa.Column("created_at", sa.DateTime, server_default=func.now()),
)

bond_profits_table = sa.Table(
    "bond_profits",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("bond_id", sa.BigInteger, sa.ForeignKey("bonds.id", ondelete="CASCADE")),
    sa.Column("price", sa.Float, default=0.0),
    sa.Column("date", sa.DateTime),
    sa.Column("created_at", sa.DateTime, server_default=func.now()),
)

bond_operations_table = sa.Table(
    "bond_operations",
    metadata,
    sa.Column("id", sa.BigInteger, primary_key=True, autoincrement=True),
    sa.Column("bond_id", sa.BigInteger, sa.ForeignKey("bonds.id", ondelete="CASCADE")),
    sa.Column("price", sa.Float, default=0.0),
    sa.Column("date", sa.DateTime),
    sa.Column("type", sa.Enum(BondType)),
    sa.Column("created_at", sa.DateTime, server_default=func.now()),
)
