"""add content to post

Revision ID: 0228947a0419
Revises: 41d23efcc0b5
Create Date: 2023-05-01 22:39:14.118580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0228947a0419'
down_revision = '41d23efcc0b5'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
