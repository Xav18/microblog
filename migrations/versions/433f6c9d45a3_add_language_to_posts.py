"""add language to posts

Revision ID: 433f6c9d45a3
Revises: e3de871aba0c
Create Date: 2023-04-04 15:34:27.661262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '433f6c9d45a3'
down_revision = 'e3de871aba0c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('language', sa.String(length=5), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('language')

    # ### end Alembic commands ###
