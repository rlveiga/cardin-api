"""empty message

Revision ID: 3ec3e80e8174
Revises: aba6568e3244
Create Date: 2019-12-17 13:38:57.072045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ec3e80e8174'
down_revision = 'aba6568e3244'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rooms', sa.Column('status', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rooms', 'status')
    # ### end Alembic commands ###
