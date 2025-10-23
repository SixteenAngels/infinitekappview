from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0003_partition_measurements'
down_revision = '0002_indexes'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Partitioning requires table rebuild; provide placeholder notice.
    op.execute("""
    DO $$ BEGIN RAISE NOTICE 'Partitioning requires manual migration or fresh schema.'; END $$;
    """)


def downgrade() -> None:
    pass
