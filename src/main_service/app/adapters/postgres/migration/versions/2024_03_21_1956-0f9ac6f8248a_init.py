"""init

Revision ID: 0f9ac6f8248a
Revises:
Create Date: 2024-03-21 19:56:46.926731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f9ac6f8248a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bonds',
    sa.Column('name', sa.String(), nullable=True, comment='Наименование облигации'),
    sa.Column('isin', sa.String(), nullable=False, comment='Международный идентификационный код ценной бумаги'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.PrimaryKeyConstraint('isin')
    )
    op.create_index(op.f('ix_bonds_isin'), 'bonds', ['isin'], unique=True)
    op.create_table('portfolios',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор'),
    sa.Column('name', sa.String(), nullable=True, comment='Наименование облигации'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_id'), 'portfolios', ['id'], unique=True)
    op.create_table('portfolio_bonds',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор'),
    sa.Column('portfolio_id', sa.UUID(), nullable=True, comment='Идентификатор портфеля'),
    sa.Column('bond_isin', sa.String(), nullable=True, comment='Идентификатор облигации'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.ForeignKeyConstraint(['bond_isin'], ['bonds.isin'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['portfolio_id'], ['portfolios.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolio_bonds_id'), 'portfolio_bonds', ['id'], unique=True)
    op.create_table('operations',
    sa.Column('id', sa.UUID(), nullable=False, comment='Идентификатор'),
    sa.Column('portfolio_bond_id', sa.UUID(), nullable=True, comment='Идентификатор отношения портфеля и облигации'),
    sa.Column('price_per_piece', sa.Float(), nullable=True, comment='Цена за штуку'),
    sa.Column('count', sa.Integer(), nullable=True, comment='Количество'),
    sa.Column('date', sa.DateTime(), nullable=True, comment='Дата покупки'),
    sa.Column('type', sa.Enum('purchase', 'sell', name='bondtype'), nullable=True, comment='Тип операции'),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True, comment='Дата создания записи'),
    sa.ForeignKeyConstraint(['portfolio_bond_id'], ['portfolio_bonds.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_operations_id'), 'operations', ['id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_operations_id'), table_name='operations')
    op.drop_table('operations')
    op.drop_index(op.f('ix_portfolio_bonds_id'), table_name='portfolio_bonds')
    op.drop_table('portfolio_bonds')
    op.drop_index(op.f('ix_portfolios_id'), table_name='portfolios')
    op.drop_table('portfolios')
    op.drop_index(op.f('ix_bonds_isin'), table_name='bonds')
    op.drop_table('bonds')
    # ### end Alembic commands ###
