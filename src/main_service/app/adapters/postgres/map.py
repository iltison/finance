from sqlalchemy.orm import registry, relationship

from main_service.app.adapters.postgres.table.bond import (
    bonds_table,
    metadata,
    operations_table,
    portfolio_table,
)
from main_service.app.domain.bond import Bond, BondOperation
from main_service.app.domain.portfolio import Portfolio

mapper_registry = registry(metadata=metadata)


def run_mapper():
    mapper_registry.map_imperatively(
        BondOperation,
        operations_table,
    )

    mapper_registry.map_imperatively(
        Bond,
        bonds_table,
        properties={
            "operations": relationship(BondOperation, lazy="subquery")
        },
    )

    mapper_registry.map_imperatively(
        Portfolio,
        portfolio_table,
        properties={"bonds": relationship(Bond, lazy="subquery")},
    )
