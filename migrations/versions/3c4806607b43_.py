"""empty message

Revision ID: 3c4806607b43
Revises: afe010c26a14
Create Date: 2020-03-07 20:40:15.742175

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c4806607b43'
down_revision = 'afe010c26a14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'game_data',
               existing_type=sa.VARCHAR(length=1024),
               type_=sa.String(length=500000),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'game_data',
               existing_type=sa.String(length=500000),
               type_=sa.VARCHAR(length=1024),
               existing_nullable=True)
    # ### end Alembic commands ###
