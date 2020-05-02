"""empty message

Revision ID: 4754c7b10a56
Revises: a84936959220
Create Date: 2020-05-02 16:11:20.053182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4754c7b10a56'
down_revision = 'a84936959220'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('source', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'source')
    # ### end Alembic commands ###
