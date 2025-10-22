from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_indexes'
down_revision = '0001_initial'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index('ix_measurements_owner_device_time', 'measurements', ['owner_id','device_id','created_at'])
    op.create_index('ix_measurements_sensor_time', 'measurements', ['sensor','created_at'])


def downgrade() -> None:
    op.drop_index('ix_measurements_sensor_time', table_name='measurements')
    op.drop_index('ix_measurements_owner_device_time', table_name='measurements')
