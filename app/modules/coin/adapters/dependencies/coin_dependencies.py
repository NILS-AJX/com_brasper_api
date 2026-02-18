# app/modules/coin/adapters/dependencies/coin_dependencies.py
"""Inyección de dependencias del módulo coin para las rutas (adapters)."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.modules.coin.interfaces.tax_rate_repository import TaxRateRepositoryInterface
from app.modules.coin.interfaces.tax_rate_trial_repository import TaxRateTrialRepositoryInterface
from app.modules.coin.interfaces.commission_repository import CommissionRepositoryInterface
from app.modules.coin.interfaces.tax_rate_history_repository import TaxRateHistoryRepositoryInterface
from app.modules.coin.interfaces.commission_history_repository import CommissionHistoryRepositoryInterface
from app.modules.coin.infrastructure.repository import (
    SQLAlchemyTaxRateRepository,
    SQLAlchemyTaxRateTrialRepository,
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
    GetTaxRateTrialByIdUseCase,
    ListTaxRateTrialsUseCase,
    CreateTaxRateTrialUseCase,
    UpdateTaxRateTrialUseCase,
    DeleteTaxRateTrialUseCase,
    GetCommissionByIdUseCase,
    ListCommissionsUseCase,
    ListCommissionHistoryUseCase,
    CreateCommissionUseCase,
    UpdateCommissionUseCase,
    DeleteCommissionUseCase,
)


# --- Repositorios ---

def get_tax_rate_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaxRateRepositoryInterface:
    return SQLAlchemyTaxRateRepository(db)


def get_commission_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CommissionRepositoryInterface:
    return SQLAlchemyCommissionRepository(db)


def get_tax_rate_history_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaxRateHistoryRepositoryInterface:
    return SQLAlchemyTaxRateHistoryRepository(db)


def get_commission_history_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CommissionHistoryRepositoryInterface:
    return SQLAlchemyCommissionHistoryRepository(db)


# --- TaxRate: factories de casos de uso ---

def get_tax_rate_by_id_uc(
    repo: Annotated[TaxRateRepositoryInterface, Depends(get_tax_rate_repository)],
) -> GetTaxRateByIdUseCase:
    return GetTaxRateByIdUseCase(repo)


def list_tax_rates_uc(
    repo: Annotated[TaxRateRepositoryInterface, Depends(get_tax_rate_repository)],
) -> ListTaxRatesUseCase:
    return ListTaxRatesUseCase(repo)


def create_tax_rate_uc(
    repo: Annotated[TaxRateRepositoryInterface, Depends(get_tax_rate_repository)],
    history_repo: Annotated[TaxRateHistoryRepositoryInterface, Depends(get_tax_rate_history_repository)],
) -> CreateTaxRateUseCase:
    return CreateTaxRateUseCase(repo, history_repo)


def update_tax_rate_uc(
    repo: Annotated[TaxRateRepositoryInterface, Depends(get_tax_rate_repository)],
    history_repo: Annotated[TaxRateHistoryRepositoryInterface, Depends(get_tax_rate_history_repository)],
) -> UpdateTaxRateUseCase:
    return UpdateTaxRateUseCase(repo, history_repo)


def delete_tax_rate_uc(
    repo: Annotated[TaxRateRepositoryInterface, Depends(get_tax_rate_repository)],
    history_repo: Annotated[TaxRateHistoryRepositoryInterface, Depends(get_tax_rate_history_repository)],
) -> DeleteTaxRateUseCase:
    return DeleteTaxRateUseCase(repo, history_repo)


def list_tax_rate_history_uc(
    history_repo: Annotated[TaxRateHistoryRepositoryInterface, Depends(get_tax_rate_history_repository)],
) -> ListTaxRateHistoryUseCase:
    return ListTaxRateHistoryUseCase(history_repo)


# --- TaxRateTrial (tasa prueba): repositorio y factories ---

def get_tax_rate_trial_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TaxRateTrialRepositoryInterface:
    return SQLAlchemyTaxRateTrialRepository(db)


def get_tax_rate_trial_by_id_uc(
    repo: Annotated[TaxRateTrialRepositoryInterface, Depends(get_tax_rate_trial_repository)],
) -> GetTaxRateTrialByIdUseCase:
    return GetTaxRateTrialByIdUseCase(repo)


def list_tax_rate_trials_uc(
    repo: Annotated[TaxRateTrialRepositoryInterface, Depends(get_tax_rate_trial_repository)],
) -> ListTaxRateTrialsUseCase:
    return ListTaxRateTrialsUseCase(repo)


def create_tax_rate_trial_uc(
    repo: Annotated[TaxRateTrialRepositoryInterface, Depends(get_tax_rate_trial_repository)],
) -> CreateTaxRateTrialUseCase:
    return CreateTaxRateTrialUseCase(repo)


def update_tax_rate_trial_uc(
    repo: Annotated[TaxRateTrialRepositoryInterface, Depends(get_tax_rate_trial_repository)],
) -> UpdateTaxRateTrialUseCase:
    return UpdateTaxRateTrialUseCase(repo)


def delete_tax_rate_trial_uc(
    repo: Annotated[TaxRateTrialRepositoryInterface, Depends(get_tax_rate_trial_repository)],
) -> DeleteTaxRateTrialUseCase:
    return DeleteTaxRateTrialUseCase(repo)


# --- Commission: factories de casos de uso ---

def get_commission_by_id_uc(
    repo: Annotated[CommissionRepositoryInterface, Depends(get_commission_repository)],
) -> GetCommissionByIdUseCase:
    return GetCommissionByIdUseCase(repo)


def list_commissions_uc(
    repo: Annotated[CommissionRepositoryInterface, Depends(get_commission_repository)],
) -> ListCommissionsUseCase:
    return ListCommissionsUseCase(repo)


def create_commission_uc(
    repo: Annotated[CommissionRepositoryInterface, Depends(get_commission_repository)],
    history_repo: Annotated[CommissionHistoryRepositoryInterface, Depends(get_commission_history_repository)],
) -> CreateCommissionUseCase:
    return CreateCommissionUseCase(repo, history_repo)


def update_commission_uc(
    repo: Annotated[CommissionRepositoryInterface, Depends(get_commission_repository)],
    history_repo: Annotated[CommissionHistoryRepositoryInterface, Depends(get_commission_history_repository)],
) -> UpdateCommissionUseCase:
    return UpdateCommissionUseCase(repo, history_repo)


def delete_commission_uc(
    repo: Annotated[CommissionRepositoryInterface, Depends(get_commission_repository)],
    history_repo: Annotated[CommissionHistoryRepositoryInterface, Depends(get_commission_history_repository)],
) -> DeleteCommissionUseCase:
    return DeleteCommissionUseCase(repo, history_repo)


def list_commission_history_uc(
    history_repo: Annotated[CommissionHistoryRepositoryInterface, Depends(get_commission_history_repository)],
) -> ListCommissionHistoryUseCase:
    return ListCommissionHistoryUseCase(history_repo)


# --- Tipos anotados para inyección en rutas (sin Depends explícito en el handler) ---

GetTaxRateByIdUseCaseDep = Annotated[GetTaxRateByIdUseCase, Depends(get_tax_rate_by_id_uc)]
ListTaxRatesUseCaseDep = Annotated[ListTaxRatesUseCase, Depends(list_tax_rates_uc)]
ListTaxRateHistoryUseCaseDep = Annotated[ListTaxRateHistoryUseCase, Depends(list_tax_rate_history_uc)]
CreateTaxRateUseCaseDep = Annotated[CreateTaxRateUseCase, Depends(create_tax_rate_uc)]
UpdateTaxRateUseCaseDep = Annotated[UpdateTaxRateUseCase, Depends(update_tax_rate_uc)]
DeleteTaxRateUseCaseDep = Annotated[DeleteTaxRateUseCase, Depends(delete_tax_rate_uc)]

GetTaxRateTrialByIdUseCaseDep = Annotated[GetTaxRateTrialByIdUseCase, Depends(get_tax_rate_trial_by_id_uc)]
ListTaxRateTrialsUseCaseDep = Annotated[ListTaxRateTrialsUseCase, Depends(list_tax_rate_trials_uc)]
CreateTaxRateTrialUseCaseDep = Annotated[CreateTaxRateTrialUseCase, Depends(create_tax_rate_trial_uc)]
UpdateTaxRateTrialUseCaseDep = Annotated[UpdateTaxRateTrialUseCase, Depends(update_tax_rate_trial_uc)]
DeleteTaxRateTrialUseCaseDep = Annotated[DeleteTaxRateTrialUseCase, Depends(delete_tax_rate_trial_uc)]

GetCommissionByIdUseCaseDep = Annotated[GetCommissionByIdUseCase, Depends(get_commission_by_id_uc)]
ListCommissionsUseCaseDep = Annotated[ListCommissionsUseCase, Depends(list_commissions_uc)]
ListCommissionHistoryUseCaseDep = Annotated[ListCommissionHistoryUseCase, Depends(list_commission_history_uc)]
CreateCommissionUseCaseDep = Annotated[CreateCommissionUseCase, Depends(create_commission_uc)]
UpdateCommissionUseCaseDep = Annotated[UpdateCommissionUseCase, Depends(update_commission_uc)]
DeleteCommissionUseCaseDep = Annotated[DeleteCommissionUseCase, Depends(delete_commission_uc)]
