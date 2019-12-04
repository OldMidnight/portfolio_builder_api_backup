"""empty message

Revision ID: 56b1eaf2cd6e
Revises: 8d4cd2e7d781
Create Date: 2019-11-13 11:20:16.242569

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56b1eaf2cd6e'
down_revision = '8d4cd2e7d781'
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
    sa.Column('account_type', sa.String(), nullable=False),
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
