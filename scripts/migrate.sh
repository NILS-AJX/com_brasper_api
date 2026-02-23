#!/bin/sh
# Aplica migraciones de Alembic antes de arrancar la API.
# Ejecutar: ./scripts/migrate.sh  o  sh scripts/migrate.sh

set -e
cd "$(dirname "$0")/.."

echo ">>> Aplicando migraciones..."
if command -v poetry >/dev/null 2>&1; then
  poetry run alembic upgrade head
elif command -v alembic >/dev/null 2>&1; then
  alembic upgrade head
else
  python -m alembic upgrade head
fi

echo ">>> Migraciones aplicadas. Versión actual:"
if command -v poetry >/dev/null 2>&1; then
  poetry run alembic current
elif command -v alembic >/dev/null 2>&1; then
  alembic current
else
  python -m alembic current
fi
