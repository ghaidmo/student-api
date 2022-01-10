"""add students table

Revision ID: 07b2088a3a72
Revises: c53f7654c0ba
Create Date: 2022-01-09 15:13:09.708329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07b2088a3a72'
down_revision = 'c53f7654c0ba'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'students', ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'students', type_='unique')
    # ### end Alembic commands ###
