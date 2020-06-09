"""empty message

Revision ID: 91919e08908f
Revises: b6fd6795a402
Create Date: 2020-06-08 21:47:49.844010

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91919e08908f'
down_revision = 'b6fd6795a402'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('games', sa.Column('round_number', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('games', 'round_number')
    # ### end Alembic commands ###
