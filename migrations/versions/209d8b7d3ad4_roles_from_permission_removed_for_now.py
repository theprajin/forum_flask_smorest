"""roles from permission removed for now

Revision ID: 209d8b7d3ad4
Revises: 34d4fd1e6447
Create Date: 2024-04-04 18:46:41.580086

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '209d8b7d3ad4'
down_revision = '34d4fd1e6447'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.drop_constraint('permissions_role_id_fkey', type_='foreignkey')
        batch_op.drop_column('role_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('permissions', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=False))
        batch_op.create_foreign_key('permissions_role_id_fkey', 'roles', ['role_id'], ['id'])

    # ### end Alembic commands ###
