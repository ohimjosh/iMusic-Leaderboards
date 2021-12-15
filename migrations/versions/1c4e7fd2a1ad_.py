"""empty message

Revision ID: 1c4e7fd2a1ad
Revises: aad9aa4d3da8
Create Date: 2021-12-15 18:05:26.740840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c4e7fd2a1ad'
down_revision = 'aad9aa4d3da8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('song', 'popularity')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('song', sa.Column('popularity', sa.INTEGER(), nullable=True))
    # ### end Alembic commands ###
