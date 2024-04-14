import sqlalchemy as sa
from sqlalchemy.sql import func

from main_service.app.adapters.postgres.base import mapper_registry, metadata
from main_service.app.domain.bond import BondAggregate

bonds_table = sa.Table(
    "bonds",
    metadata,
    sa.Column("name", sa.String, comment="Наименование облигации"),
    sa.Column(
        "isin",
        sa.String,
        comment="Международный идентификационный код ценной бумаги",
        primary_key=True,
        index=True,
        unique=True,
    ),
    sa.Column(
        "created_at",
        sa.DateTime,
        server_default=func.now(),
        comment="Дата создания записи",
    ),
)


def mapper_bond():
    mapper_registry.map_imperatively(
        BondAggregate,
        bonds_table,
    )
