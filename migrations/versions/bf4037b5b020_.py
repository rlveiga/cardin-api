"""empty message

Revision ID: bf4037b5b020
Revises: e4eb0090cc62
Create Date: 2020-05-02 14:10:41.821095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bf4037b5b020'
down_revision = 'e4eb0090cc62'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('rooms', 'collection_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.create_foreign_key(None, 'rooms', 'collections', ['collection_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.alter_column('rooms', 'collection_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
