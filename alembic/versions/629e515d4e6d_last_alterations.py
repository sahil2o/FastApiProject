"""last alterations

Revision ID: 629e515d4e6d
Revises: 899af5b0f8e2
Create Date: 2023-05-01 22:49:28.160755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '629e515d4e6d'
down_revision = '899af5b0f8e2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa. Boolean(), nullable=False, server_default='TRUE'), )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')), )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
