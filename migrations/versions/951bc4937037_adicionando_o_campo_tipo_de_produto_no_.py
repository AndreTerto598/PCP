"""Adicionando o campo Tipo de Produto no cadastro de pedidos

Revision ID: 951bc4937037
Revises: 1b0e67ae1607
Create Date: 2024-10-18 14:17:25.224296

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '951bc4937037'
down_revision = '1b0e67ae1607'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('tipo_produto', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pedido_cliente', schema=None) as batch_op:
        batch_op.drop_column('tipo_produto')

    # ### end Alembic commands ###
