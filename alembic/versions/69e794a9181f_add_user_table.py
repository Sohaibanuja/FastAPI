"""add user table

Revision ID: 69e794a9181f
Revises: 56abadd1c417
Create Date: 2022-03-23 17:26:45.467379

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69e794a9181f'
down_revision = '56abadd1c417'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
