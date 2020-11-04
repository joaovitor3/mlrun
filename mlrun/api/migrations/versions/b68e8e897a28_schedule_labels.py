"""schedule labels

Revision ID: b68e8e897a28
Revises: cf21882f938e
Create Date: 2020-10-07 11:30:41.810844

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b68e8e897a28'
down_revision = 'cf21882f938e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'schedules_v2_labels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('value', sa.String(), nullable=True),
        sa.Column('parent', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['parent'], ['schedules_v2.id'],),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name', 'parent', name='_schedules_v2_labels_uc'),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('schedules_v2_labels')
    # ### end Alembic commands ###
