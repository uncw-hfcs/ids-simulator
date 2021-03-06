"""empty message

Revision ID: 4fefd667833a
Revises: db0c6796178d
Create Date: 2019-09-17 05:48:15.180561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fefd667833a'
down_revision = 'db0c6796178d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event_decision', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=5),
               existing_nullable=True)

    with op.batch_alter_table('training_event_decision', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.VARCHAR(length=1),
               type_=sa.String(length=5),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('training_event_decision', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.String(length=5),
               type_=sa.VARCHAR(length=1),
               existing_nullable=True)

    with op.batch_alter_table('event_decision', schema=None) as batch_op:
        batch_op.alter_column('confidence',
               existing_type=sa.String(length=5),
               type_=sa.VARCHAR(length=1),
               existing_nullable=True)

    # ### end Alembic commands ###
