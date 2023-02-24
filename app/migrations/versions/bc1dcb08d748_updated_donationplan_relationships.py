"""updated DonationPlan relationships

Revision ID: bc1dcb08d748
Revises: 086275917325
Create Date: 2023-02-24 04:30:21.072594

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc1dcb08d748'
down_revision = '086275917325'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plan_amount',
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('amount_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['amount_id'], ['donation_amount.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['donation_plan.id'], ),
    sa.PrimaryKeyConstraint('plan_id', 'amount_id')
    )
    op.create_table('plan_period',
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('period_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['period_id'], ['donation_period.id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['donation_plan.id'], ),
    sa.PrimaryKeyConstraint('plan_id', 'period_id')
    )
    op.create_table('record_amount',
    sa.Column('record_id', sa.Integer(), nullable=False),
    sa.Column('amount_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['amount_id'], ['donation_amount.id'], ),
    sa.ForeignKeyConstraint(['record_id'], ['donation_record.id'], ),
    sa.PrimaryKeyConstraint('record_id', 'amount_id')
    )
    with op.batch_alter_table('donation_record', schema=None) as batch_op:
        batch_op.drop_column('amount')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('donation_record', schema=None) as batch_op:
        batch_op.add_column(sa.Column('amount', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False))

    op.drop_table('record_amount')
    op.drop_table('plan_period')
    op.drop_table('plan_amount')
    # ### end Alembic commands ###