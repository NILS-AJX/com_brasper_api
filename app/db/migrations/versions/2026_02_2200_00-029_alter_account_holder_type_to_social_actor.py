"""alter_account_holder_type_to_social_actor

Revision ID: 029
Revises: 028
Create Date: 2026-02-22

Cambia enum account_holder_type de (personal, legal) a SocialActor:
(naturalPerson, legalEntity, generalAspect).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "029"
down_revision: Union[str, None] = "028"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

schema = "transaction"


def upgrade() -> None:
    # Crear nuevo tipo con valores SocialActor
    op.execute(sa.text(
        "CREATE TYPE transaction.account_holder_type_new AS ENUM "
        "('naturalPerson', 'legalEntity', 'generalAspect')"
    ))
    # Alterar columna: migrar personal->naturalPerson, legal->legalEntity
    op.execute(sa.text("""
        ALTER TABLE transaction.bank_accounts
        ALTER COLUMN account_holder_type TYPE transaction.account_holder_type_new
        USING (
            CASE account_holder_type::text
                WHEN 'personal' THEN 'naturalPerson'::transaction.account_holder_type_new
                WHEN 'legal' THEN 'legalEntity'::transaction.account_holder_type_new
                ELSE 'naturalPerson'::transaction.account_holder_type_new
            END
        )
    """))
    # Eliminar tipo viejo y renombrar el nuevo
    op.execute(sa.text("DROP TYPE transaction.account_holder_type"))
    op.execute(sa.text(
        "ALTER TYPE transaction.account_holder_type_new RENAME TO account_holder_type"
    ))


def downgrade() -> None:
    # Crear tipo original
    op.execute(sa.text(
        "CREATE TYPE transaction.account_holder_type_old AS ENUM ('personal', 'legal')"
    ))
    # Revertir columna
    op.execute(sa.text("""
        ALTER TABLE transaction.bank_accounts
        ALTER COLUMN account_holder_type TYPE transaction.account_holder_type_old
        USING (
            CASE account_holder_type::text
                WHEN 'naturalPerson' THEN 'personal'::transaction.account_holder_type_old
                WHEN 'legalEntity' THEN 'legal'::transaction.account_holder_type_old
                WHEN 'generalAspect' THEN 'personal'::transaction.account_holder_type_old
                ELSE 'personal'::transaction.account_holder_type_old
            END
        )
    """))
    op.execute(sa.text("DROP TYPE transaction.account_holder_type"))
    op.execute(sa.text(
        "ALTER TYPE transaction.account_holder_type_old RENAME TO account_holder_type"
    ))
