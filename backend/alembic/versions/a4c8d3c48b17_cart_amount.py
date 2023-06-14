"""cart_amount

Revision ID: a4c8d3c48b17
Revises: ad9a49c0c1c2
Create Date: 2023-06-07 16:06:57.730398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a4c8d3c48b17'
down_revision = 'ad9a49c0c1c2'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('amount', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'amount')
    # ### end Alembic commands ###
