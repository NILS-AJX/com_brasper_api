"""create_coin_history_tables

Revision ID: 022
Revises: 021
Create Date: 2026-02-18

Crea tablas de auditoría para tasas y comisiones:
- coin.tax_rate_history
- coin.commission_history
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "022"
down_revision: Union[str, None] = "021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "coin"


def upgrade() -> None:
    op.execute(sa.text(f'CREATE schema IF NOT EXISTS "{schema}"'))

    op.execute(sa.text("""
        CREATE TABLE coin.tax_rate_history (
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
    op.create_index(
        op.f("ix_coin_tax_rate_history_tax_rate_id"),
        "tax_rate_history",
        ["tax_rate_id"],
        schema=schema,
    )
    op.create_index(
        op.f("ix_coin_tax_rate_history_changed_at"),
        "tax_rate_history",
        ["changed_at"],
        schema=schema,
    )

    op.execute(sa.text("""
        CREATE TABLE coin.commission_history (
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
    op.create_index(
        op.f("ix_coin_commission_history_commission_id"),
        "commission_history",
        ["commission_id"],
        schema=schema,
    )
    op.create_index(
        op.f("ix_coin_commission_history_changed_at"),
        "commission_history",
        ["changed_at"],
        schema=schema,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_coin_commission_history_changed_at"),
        table_name="commission_history",
        schema=schema,
    )
    op.drop_index(
        op.f("ix_coin_commission_history_commission_id"),
        table_name="commission_history",
        schema=schema,
    )
    op.drop_table("commission_history", schema=schema)

    op.drop_index(
        op.f("ix_coin_tax_rate_history_changed_at"),
        table_name="tax_rate_history",
        schema=schema,
    )
    op.drop_index(
        op.f("ix_coin_tax_rate_history_tax_rate_id"),
        table_name="tax_rate_history",
        schema=schema,
    )
    op.drop_table("tax_rate_history", schema=schema)
