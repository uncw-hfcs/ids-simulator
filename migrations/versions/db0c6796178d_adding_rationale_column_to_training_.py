"""adding rationale column to training events

Revision ID: db0c6796178d
Revises: 5d7d888cb6ed
Create Date: 2019-09-14 06:12:27.430882

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db0c6796178d'
down_revision = '5d7d888cb6ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('training_event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('rationale', sa.Text(), nullable=True))

    bind = op.get_bind()
    metadata = sa.MetaData(bind=bind, reflect=True)
    events_table = metadata.tables['training_event']
    op.execute(
        events_table.update().
        where(events_table.c.id == op.inline_literal("3")).
        values(
            {
                'rationale': op.inline_literal("There are a few failed logins, but the ratio of failed to successful logins is low. The travel times are impossible, but the Miami source provider is `mobile/cellular'. As mentioned in the Security Playbook, it is common for a mobile device to route through its home country. This user could, for example, using their laptop on hotel internet in Miami while their mobile phone continues to route through France. This should be rated \"Don't Escalate\" with a Confidence of say 3-5.")
            }
        )
    )
    op.execute(
        events_table.update().
        where(events_table.c.id == op.inline_literal("4")).
        values(
            {
                'rationale': op.inline_literal("The failed/passed login ratio is not a concern. The travel times are realistic. The locations are not concerning. This should be \"Don't Escalate\" with a confidence of 5.")
            }
        )
    )
    op.execute(
        events_table.update().
        where(events_table.c.id == op.inline_literal("5")).
        values(
            {
                'rationale': op.inline_literal("The failed/passing login ration is not a concern, but the travel time is impossible. The source provider is telecom for both locations, meaning the actor(s) are likely physically located at the locations. This seems like a good candidate for someone whose credentials have been stolen. Choose \"Escalate\" for this event with high confidence.")
            }
        )
    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('training_event', schema=None) as batch_op:
        batch_op.drop_column('rationale')

    # ### end Alembic commands ###
