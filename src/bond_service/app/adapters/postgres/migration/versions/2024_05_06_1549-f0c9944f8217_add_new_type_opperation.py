"""add new type opperation

Revision ID: f0c9944f8217
Revises: dc141178a84f
Create Date: 2024-05-06 15:49:29.119489

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0c9944f8217'
down_revision: Union[str, None] = 'dc141178a84f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Replace 'enumtype' with your enum type name and add your values
old_options = ['sell', 'purchase']
new_options = ['sell', 'purchase', 'coupon']
name = 'bondtype'
column = "type"
table = "operations"
def upgrade():
    # Create a temporary enum type with the new values
    tmp_type = sa.Enum(*new_options, name="_" + name)
    tmp_type.create(op.get_bind(), checkfirst=False)

    # Update column to use the new enum type
    op.execute('ALTER TABLE %s ALTER COLUMN %s TYPE _%s USING %s ::text::_%s' % (table,column, name,column, name))

    # Drop the old enum type
    op.execute('DROP TYPE %s' % name)

    # Rename the new enum type
    op.execute('ALTER TYPE _%s RENAME TO %s' % (name, name))

def downgrade():
    # Reverse the process for downgrade
    tmp_type = sa.Enum(*old_options, name="_" + name)
    tmp_type.create(op.get_bind(), checkfirst=False)

    op.execute('ALTER TABLE %s ALTER COLUMN %s TYPE _%s USING %s::text::_%s' % (table,column, name,column, name))
    op.execute('DROP TYPE %s' % name)
    op.execute('ALTER TYPE _%s RENAME TO %s' % (name, name))
