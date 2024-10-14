"""Adicionando campo status ao PedidoCliente

Revision ID: a336a21172a8
Revises: 3c4308871ea1
Create Date: 2024-10-14 13:16:47.986013

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a336a21172a8'
down_revision = '3c4308871ea1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(length=50), nullable=False, server_default='andamento'))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###