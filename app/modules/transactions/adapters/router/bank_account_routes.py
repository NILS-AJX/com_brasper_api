# app/modules/transactions/adapters/router/bank_account_routes.py
from uuid import UUID
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status

from app.modules.transactions.application.schemas import (
    BankAccountCreateCmd,
    BankAccountUpdateCmd,
    BankAccountReadDTO,
)
from app.modules.transactions.adapters.dependencies import (
    GetBankAccountByIdUseCaseDep,
    ListBankAccountsUseCaseDep,
    CreateBankAccountUseCaseDep,
    UpdateBankAccountUseCaseDep,
    DeleteBankAccountUseCaseDep,
)

router = APIRouter(prefix="/bank-accounts", tags=["bank-accounts"])


@router.get("/", response_model=List[BankAccountReadDTO])
async def list_bank_accounts(
    use_case: ListBankAccountsUseCaseDep,
    user_id: Optional[UUID] = Query(None, description="Filtro por ID de usuario"),
):
    """Lista cuentas bancarias. Opcionalmente filtra por user_id."""
    return await use_case.execute(user_id=user_id)


@router.get("/{bank_account_id}", response_model=BankAccountReadDTO)
async def get_bank_account_by_id(bank_account_id: UUID, use_case: GetBankAccountByIdUseCaseDep):
    entity = await use_case.execute(bank_account_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    return entity


@router.post("/", response_model=BankAccountReadDTO, status_code=status.HTTP_201_CREATED)
async def create_bank_account(cmd: BankAccountCreateCmd, use_case: CreateBankAccountUseCaseDep):
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/", response_model=BankAccountReadDTO)
async def update_bank_account(cmd: BankAccountUpdateCmd, use_case: UpdateBankAccountUseCaseDep):
    try:
        entity = await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not entity:
        raise HTTPException(status_code=404, detail="Cuenta bancaria no encontrada")
    return entity


@router.delete("/{bank_account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bank_account(bank_account_id: UUID, use_case: DeleteBankAccountUseCaseDep):
    await use_case.execute(bank_account_id)
