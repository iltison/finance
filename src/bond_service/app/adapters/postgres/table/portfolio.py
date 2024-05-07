import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.sql import func
from uuid6 import uuid7

from app.adapters.postgres.base import Base
from app.domains.portfolio import (
    BondType,
)


class Bonds(Base):
    __tablename__ = "bonds"

    id = Column(
        "id",
        sa.UUID,
        primary_key=True,
        index=True,
        default=uuid7,
        unique=True,
        comment="Идентификатор",
    )
    portfolio_id = Column(
        sa.UUID,
        comment="Идентификатор портфеля",
    )
    bond_isin = Column(
        sa.String,
        comment="Идентификатор облигации",
    )
    created_at = Column(
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    )


class Operations(Base):
    __tablename__ = "operations"

    id = Column(
        "id",
        sa.UUID,
        primary_key=True,
        index=True,
        default=uuid7,
        unique=True,
        comment="Идентификатор",
    )
    bond_id = Column(
        sa.UUID,
        sa.ForeignKey("bonds.id", ondelete="CASCADE"),
        comment="Идентификатор отношения портфеля и облигации",
    )
    price_per_piece = Column(sa.Float, default=0.0, comment="Цена за штуку")
    count = Column(sa.Integer, default=0, comment="Количество")
    date = Column(sa.DateTime, comment="Дата покупки")
    type = Column(sa.Enum(BondType), comment="Тип операции")
    created_at = Column(
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    )
