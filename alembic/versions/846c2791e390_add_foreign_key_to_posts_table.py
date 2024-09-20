"""add foreign-key to posts table

Revision ID: 846c2791e390
Revises: e845f9f2e22d
Create Date: 2024-08-27 22:13:45.032094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '846c2791e390'
down_revision: Union[str, None] = 'e845f9f2e22d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable= False))
    op.create_foreign_key('post_user_fk', source_table='posts', referent_table='users', 
                          local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts','owner_id')
    pass
