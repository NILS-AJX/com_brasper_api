"""add_social_actor_to_banks

Revision ID: 030
Revises: 029
Create Date: 2026-02-22

Añade columna social_actor a transaction.banks (usa enum account_holder_type).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "030"
down_revision: Union[str, None] = "029"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"


def upgrade() -> None:
    # Usa el enum account_holder_type existente (naturalPerson, legalEntity, generalAspect)
    op.execute(sa.text(
        f"ALTER TABLE {schema}.banks ADD COLUMN social_actor {schema}.account_holder_type"
    ))
    op.create_index(
        op.f("ix_transaction_banks_social_actor"),
        "banks",
        ["social_actor"],
        schema=schema,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_transaction_banks_social_actor"),
        table_name="banks",
        schema=schema,
    )
    op.execute(sa.text(f"ALTER TABLE {schema}.banks DROP COLUMN social_actor"))
