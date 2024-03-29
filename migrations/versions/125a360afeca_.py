"""empty message

Revision ID: 125a360afeca
Revises: 3e3c88bfaa08
Create Date: 2020-01-12 15:55:32.022588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '125a360afeca'
down_revision = '3e3c88bfaa08'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('cards', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('collections', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('collections', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('cards', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
