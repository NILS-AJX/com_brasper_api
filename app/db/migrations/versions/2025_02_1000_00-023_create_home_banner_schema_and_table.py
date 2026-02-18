"""create_home_banner_schema_and_table

Revision ID: 023
Revises: 022
Create Date: 2025-02-10

Crea esquema home_banner y tabla home_banner (banner_es, banner_pr, banner_en, enable).
Reemplaza home_images por home_banner.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "023"
down_revision: Union[str, None] = "022"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "home_banner"


def upgrade() -> None:
    # Eliminar home_images si existe (de migración anterior)
    op.execute(sa.text('DROP SCHEMA IF EXISTS "home_images" CASCADE'))

    op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    op.execute(sa.text("""
        CREATE TABLE home_banner.home_banner (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            banner_es VARCHAR(500),
            banner_pr VARCHAR(500),
            banner_en VARCHAR(500)
        )
    """))


def downgrade() -> None:
    op.drop_table("home_banner", schema=schema)
    op.execute(sa.text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
