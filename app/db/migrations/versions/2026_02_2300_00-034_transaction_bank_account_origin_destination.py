"""transaction_bank_account_origin_destination

Revision ID: 034
Revises: 033
Create Date: 2026-02-23

Reemplaza bank_account_id por bank_account_origin_id y bank_account_destination_id.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "034"
down_revision: Union[str, None] = "033"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"


def upgrade() -> None:
    # Añadir nuevas columnas (nullable primero para migrar datos)
    op.add_column(
        "transactions",
        sa.Column("bank_account_origin_id", sa.UUID(), nullable=True),
        schema=schema,
    )
    op.add_column(
        "transactions",
        sa.Column("bank_account_destination_id", sa.UUID(), nullable=True),
        schema=schema,
    )
    # Copiar bank_account_id a ambas columnas
    op.execute(
        sa.text(
            f"""
            UPDATE {schema}.transactions
            SET bank_account_origin_id = bank_account_id,
                bank_account_destination_id = bank_account_id
            WHERE bank_account_id IS NOT NULL
            """
        )
    )
    # Hacer NOT NULL
    op.alter_column(
        "transactions",
        "bank_account_origin_id",
        nullable=False,
        schema=schema,
    )
    op.alter_column(
        "transactions",
        "bank_account_destination_id",
        nullable=False,
        schema=schema,
    )
    # Crear FKs e índices
    op.create_foreign_key(
        "fk_transactions_bank_account_origin_id_bank_accounts",
        "transactions",
        "bank_accounts",
        ["bank_account_origin_id"],
        ["id"],
        source_schema=schema,
        referent_schema=schema,
    )
    op.create_foreign_key(
        "fk_transactions_bank_account_destination_id_bank_accounts",
        "transactions",
        "bank_accounts",
        ["bank_account_destination_id"],
        ["id"],
        source_schema=schema,
        referent_schema=schema,
    )
    op.create_index(
        op.f("ix_transaction_transactions_bank_account_origin_id"),
        "transactions",
        ["bank_account_origin_id"],
        schema=schema,
    )
    op.create_index(
        op.f("ix_transaction_transactions_bank_account_destination_id"),
        "transactions",
        ["bank_account_destination_id"],
        schema=schema,
    )
    # Eliminar FK, índice y columna antigua
    op.drop_constraint(
        "fk_transactions_bank_account_id_bank_accounts",
        "transactions",
        schema=schema,
        type_="foreignkey",
    )
    op.drop_index(
        op.f("ix_transaction_transactions_bank_account_id"),
        table_name="transactions",
        schema=schema,
    )
    op.drop_column("transactions", "bank_account_id", schema=schema)


def downgrade() -> None:
    op.add_column(
        "transactions",
        sa.Column("bank_account_id", sa.UUID(), nullable=True),
        schema=schema,
    )
    op.execute(
        sa.text(
            f"""
            UPDATE {schema}.transactions
            SET bank_account_id = bank_account_origin_id
            WHERE bank_account_origin_id IS NOT NULL
            """
        )
    )
    op.alter_column(
        "transactions",
        "bank_account_id",
        nullable=False,
        schema=schema,
    )
    op.create_foreign_key(
        "fk_transactions_bank_account_id_bank_accounts",
        "transactions",
        "bank_accounts",
        ["bank_account_id"],
        ["id"],
        source_schema=schema,
        referent_schema=schema,
    )
    op.create_index(
        op.f("ix_transaction_transactions_bank_account_id"),
        "transactions",
        ["bank_account_id"],
        schema=schema,
    )
    op.drop_constraint(
        "fk_transactions_bank_account_origin_id_bank_accounts",
        "transactions",
        schema=schema,
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_transactions_bank_account_destination_id_bank_accounts",
        "transactions",
        schema=schema,
        type_="foreignkey",
    )
    op.drop_index(
        op.f("ix_transaction_transactions_bank_account_origin_id"),
        table_name="transactions",
        schema=schema,
    )
    op.drop_index(
        op.f("ix_transaction_transactions_bank_account_destination_id"),
        table_name="transactions",
        schema=schema,
    )
    op.drop_column("transactions", "bank_account_origin_id", schema=schema)
    op.drop_column("transactions", "bank_account_destination_id", schema=schema)
