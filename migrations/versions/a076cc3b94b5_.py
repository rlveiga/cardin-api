"""empty message

Revision ID: a076cc3b94b5
Revises: 3c4806607b43
Create Date: 2020-04-12 13:36:19.156389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a076cc3b94b5'
down_revision = '3c4806607b43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('slots', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cards', 'slots')
    # ### end Alembic commands ###
