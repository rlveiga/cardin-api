"""empty message

Revision ID: 3176fce5c48d
Revises: 6688f98a5ab1
Create Date: 2020-04-26 12:01:36.132752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3176fce5c48d'
down_revision = '6688f98a5ab1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('games',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_data', sa.String(length=500000), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('discarded_at', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('games')
    # ### end Alembic commands ###
