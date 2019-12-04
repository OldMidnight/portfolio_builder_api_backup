"""empty message

Revision ID: edfa22331a4d
Revises: 723b1f06124f
Create Date: 2019-08-02 15:42:25.793539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edfa22331a4d'
down_revision = '723b1f06124f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('password', sa.VARCHAR(length=25), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
