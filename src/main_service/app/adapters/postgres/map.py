from sqlalchemy.orm import registry, relationship

from main_service.app.adapters.postgres.table.bond import (
    bonds_table,
    metadata,
    operations_table,
    portfolio_table,
)
from main_service.app.domain.portfolio import (
    BondEntity,
    BondOperationVO,
    PortfolioAggregate,
)

mapper_registry = registry(metadata=metadata)


def run_mapper():
    mapper_registry.map_imperatively(
        BondOperationVO,
        operations_table,
    )

    mapper_registry.map_imperatively(
        BondEntity,
        bonds_table,
        properties={
            "operations": relationship(BondOperationVO, lazy="subquery")
        },
    )

    mapper_registry.map_imperatively(
        PortfolioAggregate,
        portfolio_table,
        properties={"bonds": relationship(BondEntity, lazy="subquery")},
    )
