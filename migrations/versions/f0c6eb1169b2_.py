"""empty message

Revision ID: f0c6eb1169b2
Revises: e57e0f40e072
Create Date: 2020-01-18 18:01:20.871845

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f0c6eb1169b2'
down_revision = 'e57e0f40e072'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('cards_collection_id_fkey', 'cards', type_='foreignkey')
    op.drop_column('cards', 'collection_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('collection_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('cards_collection_id_fkey', 'cards', 'collections', ['collection_id'], ['id'])
    # ### end Alembic commands ###
