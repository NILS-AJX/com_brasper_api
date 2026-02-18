"""create_commission_trial_table

Revision ID: 023
Revises: 022
Create Date: 2026-02-18

Crea tabla coin.commission_trial para pruebas de calculadora.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "023"
down_revision: Union[str, None] = "022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "coin"


def upgrade() -> None:
    op.execute(sa.text(f'CREATE schema IF NOT EXISTS "{schema}"'))

    op.execute(sa.text("""
        CREATE TABLE coin.commission_trial (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            coin_a coin.currency NOT NULL,
            coin_b coin.currency NOT NULL,
            percentage NUMERIC(20, 8) NOT NULL DEFAULT 0,
            reverse NUMERIC(20, 8) NOT NULL DEFAULT 0,
            min_amount NUMERIC(20, 8) NULL,
            max_amount NUMERIC(20, 8) NULL
        )
    """))

    op.create_index(
        op.f("ix_coin_commission_trial_coin_a"),
        "commission_trial",
        ["coin_a"],
        schema=schema,
    )
    op.create_index(
        op.f("ix_coin_commission_trial_coin_b"),
        "commission_trial",
        ["coin_b"],
        schema=schema,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_coin_commission_trial_coin_b"),
        table_name="commission_trial",
        schema=schema,
    )
    op.drop_index(
        op.f("ix_coin_commission_trial_coin_a"),
        table_name="commission_trial",
        schema=schema,
    )
    op.drop_table("commission_trial", schema=schema)
