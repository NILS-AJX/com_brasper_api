#!/usr/bin/env python
"""
Script para probar el POST /transactions/import/

Ejecutar: poetry run python -m scripts.test_import_transaction

Requisitos: Servidor corriendo (uvicorn), y que existan en DB:
- Al menos un bank (PE y uno BR)
- Al menos un tax_rate
- Al menos un commission

Para crear tax_rate y commission si no existen, ejecutar primero:
  poetry run python -m scripts.seed_coin  # si existe
O crearlos manualmente vía API/DB.
"""
import asyncio
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import httpx


async def main():
    # Obtener IDs existentes
    async with httpx.AsyncClient(timeout=30.0) as client:
        banks = (await client.get("http://localhost:8000/transactions/banks/")).json()
        bank_pe = next((b for b in banks if b.get("country") == "pe"), None)
        bank_br = next((b for b in banks if b.get("country") == "br"), None)
        if not bank_pe or not bank_br:
            print("Error: Se necesitan bancos PE y BR. Ejecuta: python -m scripts.seed_banks")
            sys.exit(1)

        tax_rates = (await client.get("http://localhost:8000/coin/tax-rate/")).json()
        commissions = (await client.get("http://localhost:8000/coin/commission/")).json()
        tax_id = tax_rates[0]["id"] if tax_rates else None
        comm_id = commissions[0]["id"] if commissions else None
        if not tax_id or not comm_id:
            print("Error: Se necesitan tax_rate y commission. Créalos vía POST /coin/tax-rate/ y /coin/commission/")
            sys.exit(1)

        payload = {
            "items": [
                {
                    "user_origin": {
                        "user": {
                            "names": "Juan",
                            "lastnames": "Pérez",
                            "email": "juan.perez.import@example.com",
                            "password": "MiClave123!",
                        },
                        "bank_account": {
                            "bank_id": bank_pe["id"],
                            "account_flow": "origin",
                            "account_holder_type": "naturalPerson",
                            "bank_country": "pe",
                        },
                    },
                    "user_destination": {
                        "user": {
                            "names": "María",
                            "lastnames": "García",
                            "email": "maria.garcia.import@example.com",
                            "password": "OtraClave456!",
                        },
                        "bank_account": {
                            "bank_id": bank_br["id"],
                            "account_flow": "destination",
                            "account_holder_type": "naturalPerson",
                            "bank_country": "br",
                        },
                    },
                    "transaction": {
                        "tax_rate_id": tax_id,
                        "commission_id": comm_id,
                        "origin_amount": 1000.0,
                        "destination_amount": 950.0,
                    },
                }
            ]
        }

        resp = await client.post(
            "http://localhost:8000/transactions/import/",
            json=payload,
        )
        print(f"Status: {resp.status_code}")
        print(resp.json())


if __name__ == "__main__":
    asyncio.run(main())
