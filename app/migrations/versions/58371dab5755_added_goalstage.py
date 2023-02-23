"""added goalstage

Revision ID: 58371dab5755
Revises: 7d23687734c4
Create Date: 2023-02-23 21:02:45.617687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '58371dab5755'
down_revision = '7d23687734c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('goal_stage',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=40), nullable=False),
    sa.Column('number', sa.Integer(), nullable=False),
    sa.Column('target_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('goal_stage')
    # ### end Alembic commands ###
