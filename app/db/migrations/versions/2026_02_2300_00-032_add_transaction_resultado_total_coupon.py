"""add_transaction_resultado_total_coupon

Revision ID: 032
Revises: 031
Create Date: 2026-02-23

Añade a transaction.transactions: resultado_comision, total_a_enviar, coupon_id.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "032"
down_revision: Union[str, None] = "031"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"


def upgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("resultado_comision", sa.Numeric(20, 8), nullable=True),
        schema=schema,
    )
    op.add_column(
        "transactions",
        sa.Column("total_a_enviar", sa.Numeric(20, 8), nullable=True),
        schema=schema,
    )
    op.add_column(
        "transactions",
        sa.Column("coupon_id", sa.UUID(), nullable=True),
        schema=schema,
    )
    op.create_foreign_key(
        "fk_transactions_coupon_id_coupons",
        "transactions",
        "coupons",
        ["coupon_id"],
        ["id"],
        source_schema=schema,
        referent_schema=schema,
    )
    op.create_index(
        op.f("ix_transaction_transactions_coupon_id"),
        "transactions",
        ["coupon_id"],
        schema=schema,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_transaction_transactions_coupon_id"),
        table_name="transactions",
        schema=schema,
    )
    op.drop_constraint(
        "fk_transactions_coupon_id_coupons",
        "transactions",
        schema=schema,
        type_="foreignkey",
    )
    op.drop_column("transactions", "coupon_id", schema=schema)
    op.drop_column("transactions", "total_a_enviar", schema=schema)
    op.drop_column("transactions", "resultado_comision", schema=schema)
