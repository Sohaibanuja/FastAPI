"""add column to post table

Revision ID: 56abadd1c417
Revises: 01855c2f5ea1
Create Date: 2022-03-23 17:16:36.280977

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56abadd1c417'
down_revision = '01855c2f5ea1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',
        sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
