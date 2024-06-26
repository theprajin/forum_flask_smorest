"""votes table created

Revision ID: e5ad3b3ae180
Revises: 0c6662236bb2
Create Date: 2024-04-08 10:00:03.851646

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5ad3b3ae180'
down_revision = '0c6662236bb2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('content_type_id', sa.Integer(), nullable=False),
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('vote_type', sa.Enum('UP', 'DOWN', name='votetype'), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['content_type_id'], ['content_types.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
