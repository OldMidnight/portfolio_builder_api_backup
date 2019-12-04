"""empty message

Revision ID: df02a04cba10
Revises: 862336113a69
Create Date: 2019-10-09 11:28:01.494840

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df02a04cba10'
down_revision = '862336113a69'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('u_id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), nullable=True),
    sa.Column('f_name', sa.String(), nullable=False),
    sa.Column('s_name', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('u_id'),
    sa.UniqueConstraint('domain'),
    sa.UniqueConstraint('email')
    )
    op.create_table('website',
    sa.Column('w_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('domain', sa.String(), nullable=False),
    sa.Column('activation_date', sa.DateTime(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('site_props', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['domain'], ['user.domain'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.u_id'], ),
    sa.PrimaryKeyConstraint('w_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('website')
    op.drop_table('user')
    # ### end Alembic commands ###