"""drop_tax_rate_history_table

Revision ID: 027
Revises: 026
Create Date: 2026-02-20

Elimina la tabla coin.tax_rate_history (ya no se usa en el código).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "027"
down_revision: Union[str, None] = "026"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "coin"


def upgrade() -> None:
    op.execute(sa.text(f'DROP TABLE IF EXISTS "{schema}".tax_rate_history CASCADE'))


def downgrade() -> None:
    op.execute(sa.text("""
        CREATE TABLE IF NOT EXISTS coin.tax_rate_history (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            tax_rate_id UUID NULL,
            action VARCHAR(20) NOT NULL,
            before_data JSONB NULL,
            after_data JSONB NULL,
            changed_fields JSONB NOT NULL DEFAULT '[]'::jsonb,
            changed_by VARCHAR(250) NULL,
            changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            CONSTRAINT fk_tax_rate_history_tax_rate
                FOREIGN KEY (tax_rate_id) REFERENCES coin.tax_rate(id)
        )
    """))
    op.execute(sa.text('CREATE INDEX IF NOT EXISTS ix_coin_tax_rate_history_tax_rate_id ON coin.tax_rate_history (tax_rate_id)'))
    op.execute(sa.text('CREATE INDEX IF NOT EXISTS ix_coin_tax_rate_history_changed_at ON coin.tax_rate_history (changed_at)'))
