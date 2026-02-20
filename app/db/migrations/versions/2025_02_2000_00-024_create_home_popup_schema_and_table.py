"""create_home_popup_schema_and_table

Revision ID: 024
Revises: 023
Create Date: 2025-02-20

Crea esquema home_popup y tabla home_popup (popup_es, popup_pr, popup_en, enable).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "026"
down_revision: Union[str, None] = "025"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "home_popup"


def upgrade() -> None:
    op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    op.execute(sa.text("""
        CREATE TABLE home_popup.home_popup (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            popup_es VARCHAR(500),
            popup_pr VARCHAR(500),
            popup_en VARCHAR(500)
        )
    """))


def downgrade() -> None:
    op.drop_table("home_popup", schema=schema)
    op.execute(sa.text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
