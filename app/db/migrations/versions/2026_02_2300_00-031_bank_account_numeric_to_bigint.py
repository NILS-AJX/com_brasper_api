"""bank_account_numeric_to_bigint

Revision ID: 031
Revises: 030
Create Date: 2026-02-23

Convierte columnas numéricas de bank_accounts de VARCHAR a BIGINT:
document_number, ruc_number, legal_representative_document,
account_number, cci_number, cpf.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "031"
down_revision: Union[str, None] = "030"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"
table = "bank_accounts"


def _cast_to_bigint(col: str) -> str:
    """Expresión SQL para convertir VARCHAR a BIGINT (NULL y vacío -> NULL)."""
    return (
        f"CASE WHEN {col} IS NULL OR TRIM({col}) = '' "
        f"THEN NULL ELSE ({col})::BIGINT END"
    )


def upgrade() -> None:
    numeric_cols = [
        "document_number",
        "ruc_number",
        "legal_representative_document",
        "account_number",
        "cci_number",
        "cpf",
    ]
    for col in numeric_cols:
        op.execute(sa.text(
            f"ALTER TABLE {schema}.{table} "
            f"ALTER COLUMN {col} TYPE BIGINT "
            f"USING {_cast_to_bigint(col)}"
        ))


def downgrade() -> None:
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN document_number TYPE VARCHAR(20) "
        "USING document_number::TEXT"
    ))
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN ruc_number TYPE VARCHAR(20) "
        "USING ruc_number::TEXT"
    ))
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN legal_representative_document TYPE VARCHAR(20) "
        "USING legal_representative_document::TEXT"
    ))
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN account_number TYPE VARCHAR(255) "
        "USING account_number::TEXT"
    ))
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN cci_number TYPE VARCHAR(255) "
        "USING cci_number::TEXT"
    ))
    op.execute(sa.text(
        f"ALTER TABLE {schema}.{table} "
        "ALTER COLUMN cpf TYPE VARCHAR(14) "
        "USING cpf::TEXT"
    ))
