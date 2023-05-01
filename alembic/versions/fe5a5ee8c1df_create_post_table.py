"""create post table

Revision ID: fe5a5ee8c1df
Revises: 
Create Date: 2023-05-01 11:41:54.781239

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe5a5ee8c1df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id',sa.Integer(),nullable= False,primary_key= True),
                    sa.Column('title', sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
