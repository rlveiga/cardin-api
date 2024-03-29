"""empty message

Revision ID: e76825681e19
Revises: 3ec3e80e8174
Create Date: 2019-12-17 19:07:11.242996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e76825681e19'
down_revision = '3ec3e80e8174'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_type', sa.String(length=16), nullable=False),
    sa.Column('card_text', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('black_game_cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('white_game_cards',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_id', sa.Integer(), nullable=False),
    sa.Column('room_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['card_id'], ['cards.id'], ),
    sa.ForeignKeyConstraint(['room_id'], ['rooms.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('white_game_cards')
    op.drop_table('black_game_cards')
    op.drop_table('cards')
    # ### end Alembic commands ###
