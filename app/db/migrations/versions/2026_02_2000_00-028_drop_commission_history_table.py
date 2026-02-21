"""drop_commission_history_table

Revision ID: 028
Revises: 027
Create Date: 2026-02-20

Elimina la tabla coin.commission_history (ya no se usa en el código).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "028"
down_revision: Union[str, None] = "027"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "coin"


def upgrade() -> None:
    op.execute(sa.text(f'DROP TABLE IF EXISTS "{schema}".commission_history CASCADE'))


def downgrade() -> None:
    op.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS coin.commission_history (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            commission_id UUID NULL,
            action VARCHAR(20) NOT NULL,
            before_data JSONB NULL,
            after_data JSONB NULL,
            changed_fields JSONB NOT NULL DEFAULT '[]'::jsonb,
            changed_by VARCHAR(250) NULL,
            changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            CONSTRAINT fk_commission_history_commission
                FOREIGN KEY (commission_id) REFERENCES coin.commission(id)
        )
    """))
    op.execute(sa.text('CREATE INDEX IF NOT EXISTS ix_coin_commission_history_commission_id ON coin.commission_history (commission_id)'))
    op.execute(sa.text('CREATE INDEX IF NOT EXISTS ix_coin_commission_history_changed_at ON coin.commission_history (changed_at)'))
