"""Alterando Quantidade de alça de INT pra FLoat

Revision ID: 9525374451b3
Revises: f0ba3c3b732c
Create Date: 2024-10-17 12:03:03.372073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9525374451b3'
down_revision = 'f0ba3c3b732c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tamanho_altura', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('tamanho_largura', sa.String(length=50), nullable=True))
        batch_op.drop_column('tamanho')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tamanho', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
        batch_op.drop_column('tamanho_largura')
        batch_op.drop_column('tamanho_altura')

    # ### end Alembic commands ###
