"""empty message

Revision ID: 1e51381e9cd1
Revises: cf5877edc3f1
Create Date: 2022-07-08 22:36:46.434672

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e51381e9cd1'
down_revision = 'cf5877edc3f1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('accounts', sa.Column('password', sa.Text(), nullable=False))
    op.add_column('accounts', sa.Column('user', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_accounts_users_id_user', 'accounts', 'users', ['user'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_accounts_users_id_user', 'accounts', type_='foreignkey')
    op.drop_column('accounts', 'user')
    op.drop_column('accounts', 'password')
    # ### end Alembic commands ###