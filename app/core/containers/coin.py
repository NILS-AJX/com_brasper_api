# app/core/containers/coin.py
"""Inyección de dependencias del módulo coin: TaxRate y Commission."""
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.modules.coin.interfaces.tax_rate_repository import TaxRateRepositoryInterface
from app.modules.coin.interfaces.commission_repository import CommissionRepositoryInterface
from app.modules.coin.interfaces.tax_rate_history_repository import TaxRateHistoryRepositoryInterface
from app.modules.coin.interfaces.commission_history_repository import CommissionHistoryRepositoryInterface
from app.modules.coin.infrastructure.repository import (
    SQLAlchemyTaxRateRepository,
    SQLAlchemyCommissionRepository,
    SQLAlchemyTaxRateHistoryRepository,
    SQLAlchemyCommissionHistoryRepository,
)
from app.modules.coin.application.use_cases import (
    GetTaxRateByIdUseCase,
    ListTaxRatesUseCase,
    ListTaxRateHistoryUseCase,
    CreateTaxRateUseCase,
    UpdateTaxRateUseCase,
    DeleteTaxRateUseCase,
    GetCommissionByIdUseCase,
    ListCommissionsUseCase,
    ListCommissionHistoryUseCase,
    CreateCommissionUseCase,
    UpdateCommissionUseCase,
    DeleteCommissionUseCase,
)


def get_tax_rate_repository(
    db: AsyncSession = Depends(get_db),
) -> TaxRateRepositoryInterface:
    return SQLAlchemyTaxRateRepository(db)


def get_commission_repository(
    db: AsyncSession = Depends(get_db),
) -> CommissionRepositoryInterface:
    return SQLAlchemyCommissionRepository(db)


def get_tax_rate_history_repository(
    db: AsyncSession = Depends(get_db),
) -> TaxRateHistoryRepositoryInterface:
    return SQLAlchemyTaxRateHistoryRepository(db)


def get_commission_history_repository(
    db: AsyncSession = Depends(get_db),
) -> CommissionHistoryRepositoryInterface:
    return SQLAlchemyCommissionHistoryRepository(db)


# --- TaxRate use cases ---

def get_tax_rate_by_id_uc(db: AsyncSession = Depends(get_db)) -> GetTaxRateByIdUseCase:
    return GetTaxRateByIdUseCase(get_tax_rate_repository(db))


def list_tax_rates_uc(db: AsyncSession = Depends(get_db)) -> ListTaxRatesUseCase:
    return ListTaxRatesUseCase(get_tax_rate_repository(db))


def create_tax_rate_uc(db: AsyncSession = Depends(get_db)) -> CreateTaxRateUseCase:
    return CreateTaxRateUseCase(
        get_tax_rate_repository(db),
        get_tax_rate_history_repository(db),
    )


def update_tax_rate_uc(db: AsyncSession = Depends(get_db)) -> UpdateTaxRateUseCase:
    return UpdateTaxRateUseCase(
        get_tax_rate_repository(db),
        get_tax_rate_history_repository(db),
    )


def delete_tax_rate_uc(db: AsyncSession = Depends(get_db)) -> DeleteTaxRateUseCase:
    return DeleteTaxRateUseCase(
        get_tax_rate_repository(db),
        get_tax_rate_history_repository(db),
    )


def list_tax_rate_history_uc(db: AsyncSession = Depends(get_db)) -> ListTaxRateHistoryUseCase:
    return ListTaxRateHistoryUseCase(get_tax_rate_history_repository(db))


# --- Commission use cases ---

def get_commission_by_id_uc(db: AsyncSession = Depends(get_db)) -> GetCommissionByIdUseCase:
    return GetCommissionByIdUseCase(get_commission_repository(db))


def list_commissions_uc(db: AsyncSession = Depends(get_db)) -> ListCommissionsUseCase:
    return ListCommissionsUseCase(get_commission_repository(db))


def create_commission_uc(db: AsyncSession = Depends(get_db)) -> CreateCommissionUseCase:
    return CreateCommissionUseCase(
        get_commission_repository(db),
        get_commission_history_repository(db),
    )


def update_commission_uc(db: AsyncSession = Depends(get_db)) -> UpdateCommissionUseCase:
    return UpdateCommissionUseCase(
        get_commission_repository(db),
        get_commission_history_repository(db),
    )


def delete_commission_uc(db: AsyncSession = Depends(get_db)) -> DeleteCommissionUseCase:
    return DeleteCommissionUseCase(
        get_commission_repository(db),
        get_commission_history_repository(db),
    )


def list_commission_history_uc(db: AsyncSession = Depends(get_db)) -> ListCommissionHistoryUseCase:
    return ListCommissionHistoryUseCase(get_commission_history_repository(db))
