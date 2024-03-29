"""empty message

Revision ID: 13db3bbe7e3f
Revises: 786586988b1a
Create Date: 2020-03-07 16:54:46.398261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13db3bbe7e3f'
down_revision = '786586988b1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cards', 'name',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=256),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cards', 'name',
               existing_type=sa.String(length=256),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)
    # ### end Alembic commands ###
