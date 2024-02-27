"""test

Revision ID: 9044381187bb
Revises:
Create Date: 2024-02-26 15:33:00.072068

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "9044381187bb"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        sa.DDL(
            """
        create type operation_type as enum ('purchase', 'sell');

        CREATE TABLE bonds (
        id serial PRIMARY KEY,
        name varchar(255)
        );

        CREATE TABLE bond_operations (
        id serial PRIMARY KEY,
        bond_id int REFERENCES bonds (id) ON DELETE CASCADE,
        price FLOAT,
        date DATE,
        operation operation_type
        );

        CREATE TABLE bond_profit (
        id serial PRIMARY KEY,
        bond_id int REFERENCES bonds (id) ON DELETE CASCADE,
        price FLOAT,
        date DATE
        );
        """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.DDL(
            """
        DROP TABLE bond_operations;

        DROP TABLE bond_profit;

        DROP TABLE bonds;

        DROP TYPE operation_type;
        """
        )
    )
