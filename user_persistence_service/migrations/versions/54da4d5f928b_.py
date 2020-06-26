"""empty message

Revision ID: 54da4d5f928b
Revises: df9f11a7efd4
Create Date: 2020-05-01 04:12:34.036177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54da4d5f928b'
down_revision = 'df9f11a7efd4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
