"""Alterando modelo de dados do cadastro de pedidos

Revision ID: 360560900ab4
Revises: 102cae994de6
Create Date: 2024-10-17 09:22:22.703956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '360560900ab4'
down_revision = '102cae994de6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.alter_column('tamanho',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('tela',
               existing_type=sa.VARCHAR(length=100),
               nullable=True)
        batch_op.alter_column('medida_alca',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.alter_column('medida_alca',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               nullable=False)
        batch_op.alter_column('tela',
               existing_type=sa.VARCHAR(length=100),
               nullable=False)
        batch_op.alter_column('tamanho',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)

    # ### end Alembic commands ###
