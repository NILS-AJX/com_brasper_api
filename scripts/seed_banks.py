#!/usr/bin/env python
"""
Script para cargar datos de bancos (PE y BR) en la base de datos.

Ejecutar desde la raíz del proyecto (con venv/poetry activo):

    python -m scripts.seed_banks

O con Poetry:
    poetry run python -m scripts.seed_banks

Requisitos: .env configurado con DATABASE_URL
"""
import asyncio
import sys
from pathlib import Path

# Añadir raíz del proyecto al path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Registrar modelos SQLAlchemy
import app.models_registry  # noqa: F401

from app.db.base import AsyncSessionLocal
from app.modules.transactions.infrastructure.bank_repository import SQLAlchemyBankRepository
from app.modules.transactions.application.use_cases.bank_use_cases import CreateBankUseCase
from app.modules.transactions.application.schemas.bank_schema import BankCreateCmd
from app.modules.coin.domain.enums import Currency
from app.modules.transactions.domain.enums import BankCountry


# Datos a cargar
BANKS_DATA = {
    "PE": {
        "PEN": [
            {"bank": "Interbank", "account": "8983003838875", "company": "BRASPER 21", "currency": "Soles (PEN)", "image": "/bancos/interbank.png"},
            {"bank": "BBVA", "account": "001101280200817822", "company": "BRASPER 21 S.A.C", "currency": "Soles (PEN)", "image": "/bancos/bbva.png"},
            {"bank": "BCP", "account": "1912077975044", "company": "INGENITECH S.A.C", "currency": "Soles (PEN)", "image": "/bancos/bcp.png"},
            {"bank": "Yape", "account": "966991933", "company": "INGENITECH S.A.C", "currency": "Soles (PEN)", "image": "/bancos/yape.png"},
            {"bank": "Izipay", "account": "No disponible", "company": "No disponible", "currency": "Soles (PEN)", "image": "/bancos/izipay.png"},
        ],
        "USD": [
            {"bank": "Interbank", "account": "8983003838882", "company": "BRASPER 21", "currency": "Dólares (USD)", "image": "/bancos/interbank.png"},
            {"bank": "BBVA", "account": "001101280200817830", "company": "BRASPER 21 S.A.C", "currency": "Dólares (USD)", "image": "/bancos/bbva.png"},
            {"bank": "Scotiabank", "account": "0560603578", "company": "BRASPER 21 S.A.C", "currency": "Dólares (USD)", "image": "/bancos/scotiabank.png"},
            {"bank": "BCP", "account": "1912077982125", "company": "INGENITECH S.A.C", "currency": "Dólares (USD)", "image": "/bancos/bcp.png"},
        ],
    },
    "BR": {
        "BRL": [
            {"bank": "Banco FITBANK - 450", "pix": "50.754.016/0001-68", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/fitbank.png"},
            {"bank": "Banco do Brasil - 001", "pix": "826a6382-fb0b-4998-9c30-772596098a48", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/banco_do_brasil.png"},
            {"bank": "C6 Bank", "pix": "No disponible", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/c6.png"},
            {"bank": "Nubank", "pix": "No disponible", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/nubank.png"},
            {"bank": "Banco Inter", "pix": "No disponible", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/inter.png"},
            {"bank": "Bradesco", "pix": "No disponible", "company": "Brasper 21 Corretora De Cambio Ltda", "currency": "Reales (BRL)", "image": "/bancos/bradesco.png"},
        ],
    },
}


def build_bank_commands():
    """Construye la lista de BankCreateCmd a partir de BANKS_DATA."""
    commands = []
    for country_key, currencies in BANKS_DATA.items():
        country = BankCountry.pe if country_key == "PE" else BankCountry.br
        for currency_key, items in currencies.items():
            currency = Currency.pen if currency_key == "PEN" else (Currency.usd if currency_key == "USD" else Currency.brl)
            for item in items:
                cmd = BankCreateCmd(
                    bank=item["bank"],
                    account=item.get("account"),
                    pix=item.get("pix"),
                    company=item["company"],
                    currency=currency,
                    image=item["image"],
                    country=country,
                )
                commands.append(cmd)
    return commands


async def seed_banks():
    """Inserta los bancos en la base de datos."""
    commands = build_bank_commands()
    print(f"Se insertarán {len(commands)} bancos...")

    async with AsyncSessionLocal() as session:
        repo = SQLAlchemyBankRepository(session)
        use_case = CreateBankUseCase(repo)

        created = 0
        for cmd in commands:
            try:
                result = await use_case.execute(cmd)
                created += 1
                print(f"  ✓ {result.bank} ({result.currency.value}) - {result.country.value}")
            except Exception as e:
                print(f"  ✗ Error en {cmd.bank}: {e}")
                await session.rollback()
                raise

    print(f"\nListo. Se insertaron {created} bancos.")


if __name__ == "__main__":
    asyncio.run(seed_banks())
