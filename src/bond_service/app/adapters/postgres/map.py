from app.adapters.postgres.table.bond import mapper_bond
from app.adapters.postgres.table.portfolio import (
    mapper_portfolio,
)


def run_mapper():
    mapper_portfolio()
    mapper_bond()
