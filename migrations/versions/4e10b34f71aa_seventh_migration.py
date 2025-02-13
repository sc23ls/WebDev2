"""seventh migration

Revision ID: 4e10b34f71aa
Revises: de608e3aee91
Create Date: 2024-12-08 17:14:47.659752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e10b34f71aa'
down_revision = 'de608e3aee91'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('order_email')
        batch_op.drop_column('fulfilled')
        batch_op.drop_column('shipping_address')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('shipping_address', sa.VARCHAR(length=200), nullable=True))
        batch_op.add_column(sa.Column('fulfilled', sa.BOOLEAN(), nullable=False))
        batch_op.add_column(sa.Column('order_email', sa.VARCHAR(length=80), nullable=True))

    # ### end Alembic commands ###
