"""rename_transaction_columns_to_english

Revision ID: 033
Revises: 032
Create Date: 2026-02-23

Rename transaction columns: resultado_comision -> commission_result, total_a_enviar -> total_to_send.
"""
from typing import Sequence, Union

from alembic import op

revision: str = "033"
down_revision: Union[str, None] = "032"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"


def upgrade() -> None:
    op.alter_column(
        "transactions",
        "resultado_comision",
        new_column_name="commission_result",
        schema=schema,
    )
    op.alter_column(
        "transactions",
        "total_a_enviar",
        new_column_name="total_to_send",
        schema=schema,
    )


def downgrade() -> None:
    op.alter_column(
        "transactions",
        "commission_result",
        new_column_name="resultado_comision",
        schema=schema,
    )
    op.alter_column(
        "transactions",
        "total_to_send",
        new_column_name="total_a_enviar",
        schema=schema,
    )
