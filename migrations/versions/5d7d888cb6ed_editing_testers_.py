"""Editing tester events

Revision ID: 5d7d888cb6ed
Revises: 4c8e999dc7fe
Create Date: 2019-09-13 18:58:33.553697

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d7d888cb6ed'
down_revision = '4c8e999dc7fe'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    metadata = sa.MetaData(bind=bind, reflect=True)
    events_table = metadata.tables['event']
    op.execute(
        events_table.update().
        where(events_table.c.id == op.inline_literal("74")).
        values(
            {
                'country_of_authentication1': op.inline_literal("For this event"),
                'country_of_authentication2': op.inline_literal("please just"),
                'number_successful_logins1': op.inline_literal("select 'Escalate'"),
                'number_successful_logins2': op.inline_literal("for your"),
                'number_failed_logins1': op.inline_literal("decision"),
                'number_failed_logins2': op.inline_literal("and '2'"),
                'source_provider1': op.inline_literal("for"),
                'source_provider2': op.inline_literal("confidence"),
            }
        )
    )

    op.execute(
        events_table.update().
        where(events_table.c.number_successful_logins1 == op.inline_literal('75')).
        values(
            {
                'country_of_authentication1': op.inline_literal("For this event"),
                'country_of_authentication2': op.inline_literal("please just"),
                'number_successful_logins1': op.inline_literal('select "Don\'t Escalate"'),
                'number_successful_logins2': op.inline_literal("for your"),
                'number_failed_logins1': op.inline_literal("decision"),
                'number_failed_logins2': op.inline_literal("and '4'"),
                'source_provider1': op.inline_literal("for"),
                'source_provider2': op.inline_literal("confidence"),
            }
        )
    )


def downgrade():
    pass
