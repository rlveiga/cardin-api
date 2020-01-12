"""empty message

Revision ID: 523e281a75ba
Revises: 14373d5aefd8
Create Date: 2020-01-12 15:51:56.355004

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '523e281a75ba'
down_revision = '14373d5aefd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cards', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('cards', sa.Column('created_by', sa.Integer(), nullable=False))
    op.add_column('cards', sa.Column('name', sa.String(length=64), nullable=False))
    op.drop_column('cards', 'card_text')
    op.add_column('collections', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('collections', sa.Column('created_by', sa.Integer(), nullable=False))
    op.drop_column('collections', 'value')
    op.add_column('rooms', sa.Column('data', sa.String(length=1024), nullable=True))
    op.alter_column('rooms', 'code',
               existing_type=sa.VARCHAR(length=5),
               nullable=False)
    op.alter_column('rooms', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('rooms', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('rooms', 'status',
               existing_type=sa.VARCHAR(length=64),
               nullable=False)
    op.drop_column('rooms', 'state')
    op.add_column('users', sa.Column('username', sa.String(length=20), nullable=False))
    op.drop_constraint('users_email_key', 'users', type_='unique')
    op.drop_column('users', 'email')
    op.drop_column('users', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.VARCHAR(length=32), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('email', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.create_unique_constraint('users_email_key', 'users', ['email'])
    op.drop_column('users', 'username')
    op.add_column('rooms', sa.Column('state', sa.VARCHAR(length=1024), autoincrement=False, nullable=True))
    op.alter_column('rooms', 'status',
               existing_type=sa.VARCHAR(length=64),
               nullable=True)
    op.alter_column('rooms', 'created_by',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('rooms', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('rooms', 'code',
               existing_type=sa.VARCHAR(length=5),
               nullable=True)
    op.drop_column('rooms', 'data')
    op.add_column('collections', sa.Column('value', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('collections', 'created_by')
    op.drop_column('collections', 'created_at')
    op.add_column('cards', sa.Column('card_text', sa.VARCHAR(length=64), autoincrement=False, nullable=False))
    op.drop_column('cards', 'name')
    op.drop_column('cards', 'created_by')
    op.drop_column('cards', 'created_at')
    # ### end Alembic commands ###
