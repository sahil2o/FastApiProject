"""add content column to posts table

Revision ID: 97c919239a18
Revises: fe5a5ee8c1df
Create Date: 2023-05-01 11:56:44.650695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97c919239a18'
down_revision = 'fe5a5ee8c1df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String,nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
