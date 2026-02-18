"""create_home_images_schema_and_home_image_table

Revision ID: 022
Revises: 021
Create Date: 2025-02-10

Crea esquema home_images y tabla home_image (url, title, description, order).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "022"
down_revision: Union[str, None] = "021"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "home_images"


def upgrade() -> None:
    op.execute(sa.text(f'CREATE SCHEMA IF NOT EXISTS "{schema}"'))
    op.execute(sa.text("""
        CREATE TABLE home_images.home_image (
            id UUID NOT NULL PRIMARY KEY,
            deleted BOOLEAN NOT NULL DEFAULT false,
            enable BOOLEAN NOT NULL DEFAULT true,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            created_by VARCHAR(250),
            updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now(),
            url VARCHAR(500) NOT NULL,
            title VARCHAR(250),
            description TEXT,
            "order" INTEGER NOT NULL DEFAULT 0
        )
    """))
    op.create_index(
        op.f("ix_home_images_home_image_url"), "home_image", ["url"], schema=schema
    )
    op.create_index(
        op.f("ix_home_images_home_image_order"), "home_image", ["order"], schema=schema
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_home_images_home_image_order"),
        table_name="home_image",
        schema=schema,
    )
    op.drop_index(
        op.f("ix_home_images_home_image_url"),
        table_name="home_image",
        schema=schema,
    )
    op.drop_table("home_image", schema=schema)
    op.execute(sa.text(f'DROP SCHEMA IF EXISTS "{schema}" CASCADE'))
