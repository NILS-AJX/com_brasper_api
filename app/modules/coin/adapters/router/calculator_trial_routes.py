from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException

from app.modules.coin.adapters.dependencies import (
    GetCommissionTrialByIdUseCaseDep,
    GetTaxRateTrialByIdUseCaseDep,
    ListCommissionTrialsUseCaseDep,
    ListTaxRateTrialsUseCaseDep,
)
from app.modules.coin.application.schemas import (
    CommissionTrialReadDTO,
    CurrencyReadDTO,
    TaxRateTrialReadDTO,
)
from app.modules.coin.domain.enums import Currency

router = APIRouter(prefix="/calculator-trial", tags=["calculator-trial"])


@router.get("/currencies", response_model=List[CurrencyReadDTO])
async def list_trial_currencies() -> List[CurrencyReadDTO]:
    """Monedas disponibles para la calculadora de pruebas."""
    return [CurrencyReadDTO(**c.to_dto()) for c in Currency]


@router.get("/tax-rate", response_model=List[TaxRateTrialReadDTO])
async def list_trial_tax_rates(use_case: ListTaxRateTrialsUseCaseDep):
    """Lista tasas de prueba (tax_rate_trial)."""
    return await use_case.execute()


@router.get("/tax-rate/{tax_rate_trial_id}", response_model=TaxRateTrialReadDTO)
async def get_trial_tax_rate_by_id(
    tax_rate_trial_id: UUID,
    use_case: GetTaxRateTrialByIdUseCaseDep,
):
    entity = await use_case.execute(tax_rate_trial_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Tasa prueba no encontrada")
    return entity


@router.get("/commission", response_model=List[CommissionTrialReadDTO])
async def list_trial_commissions(use_case: ListCommissionTrialsUseCaseDep):
    """Lista comisiones de prueba (commission_trial)."""
    return await use_case.execute()


@router.get("/commission/{commission_id}", response_model=CommissionTrialReadDTO)
async def get_trial_commission_by_id(
    commission_id: UUID,
    use_case: GetCommissionTrialByIdUseCaseDep,
):
    entity = await use_case.execute(commission_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Comisión no encontrada")
    return entity
