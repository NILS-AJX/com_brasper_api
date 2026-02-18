from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import List

from app.modules.coin.application.schemas import (
    CommissionTrialCreateCmd,
    CommissionTrialUpdateCmd,
    CommissionTrialReadDTO,
)
from app.modules.coin.adapters.dependencies import (
    GetCommissionTrialByIdUseCaseDep,
    ListCommissionTrialsUseCaseDep,
    CreateCommissionTrialUseCaseDep,
    UpdateCommissionTrialUseCaseDep,
    DeleteCommissionTrialUseCaseDep,
)

router = APIRouter(prefix="/commission-trial", tags=["commission-trial"])


@router.get("", response_model=List[CommissionTrialReadDTO])
async def list_commission_trials(use_case: ListCommissionTrialsUseCaseDep):
    return await use_case.execute()


@router.get("/{commission_trial_id}", response_model=CommissionTrialReadDTO)
async def get_commission_trial_by_id(commission_trial_id: UUID, use_case: GetCommissionTrialByIdUseCaseDep):
    entity = await use_case.execute(commission_trial_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Comisión prueba no encontrada")
    return entity


@router.post("", response_model=CommissionTrialReadDTO, status_code=status.HTTP_201_CREATED)
async def create_commission_trial(cmd: CommissionTrialCreateCmd, use_case: CreateCommissionTrialUseCaseDep):
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("", response_model=CommissionTrialReadDTO)
async def update_commission_trial(cmd: CommissionTrialUpdateCmd, use_case: UpdateCommissionTrialUseCaseDep):
    entity = await use_case.execute(cmd)
    if not entity:
        raise HTTPException(status_code=404, detail="Comisión prueba no encontrada")
    return entity


@router.delete("/{commission_trial_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_commission_trial(commission_trial_id: UUID, use_case: DeleteCommissionTrialUseCaseDep):
    await use_case.execute(commission_trial_id)
