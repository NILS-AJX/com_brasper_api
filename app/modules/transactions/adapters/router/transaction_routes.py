# app/modules/transactions/adapters/router/transaction_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from typing import Annotated, List, Optional

from fastapi import UploadFile

from app.shared.services.file_service import save_transaction_voucher
from app.modules.transactions.application.schemas import (
    TransactionCreateCmd,
    TransactionUpdateCmd,
    TransactionReadDTO,
)
from app.modules.transactions.adapters.dependencies import (
    GetTransactionByIdUseCaseDep,
    ListTransactionsUseCaseDep,
    CreateTransactionUseCaseDep,
    UpdateTransactionUseCaseDep,
    DeleteTransactionUseCaseDep,
)

router = APIRouter(tags=["transactions"])


@router.get("/", response_model=List[TransactionReadDTO])
async def list_transactions(use_case: ListTransactionsUseCaseDep):
    return await use_case.execute()


@router.get("/{transaction_id}", response_model=TransactionReadDTO)
async def get_transaction_by_id(transaction_id: UUID, use_case: GetTransactionByIdUseCaseDep):
    entity = await use_case.execute(transaction_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return entity


@router.post("/", response_model=TransactionReadDTO, status_code=status.HTTP_201_CREATED)
async def create_transaction(cmd: TransactionCreateCmd, use_case: CreateTransactionUseCaseDep):
    """Crea transacción (JSON)."""
    try:
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/form/",
    response_model=TransactionReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction (form-data)",
)
async def create_transaction_form(
    form_data: Annotated[
        tuple[TransactionCreateCmd, Optional[UploadFile], Optional[UploadFile]],
        Depends(TransactionCreateCmd.from_form),
    ],
    use_case: CreateTransactionUseCaseDep,
):
    """Crea transacción con form-data (incluye upload de vouchers)."""
    cmd, send_voucher_file, payment_voucher_file = form_data
    try:
        if send_voucher_file and send_voucher_file.filename:
            cmd.send_voucher = await save_transaction_voucher(send_voucher_file, "send")
        if payment_voucher_file and payment_voucher_file.filename:
            cmd.payment_voucher = await save_transaction_voucher(payment_voucher_file, "payment")
        return await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/", response_model=TransactionReadDTO)
async def update_transaction(cmd: TransactionUpdateCmd, use_case: UpdateTransactionUseCaseDep):
    """Actualiza transacción (JSON)."""
    try:
        entity = await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not entity:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return entity


@router.put(
    "/form/",
    response_model=TransactionReadDTO,
    summary="Update transaction (form-data)",
)
async def update_transaction_form(
    form_data: Annotated[
        tuple[TransactionUpdateCmd, Optional[UploadFile], Optional[UploadFile]],
        Depends(TransactionUpdateCmd.from_form),
    ],
    use_case: UpdateTransactionUseCaseDep,
):
    """Actualiza transacción con form-data (incluye upload de vouchers)."""
    cmd, send_voucher_file, payment_voucher_file = form_data
    try:
        if send_voucher_file and send_voucher_file.filename:
            cmd.send_voucher = await save_transaction_voucher(send_voucher_file, "send")
        if payment_voucher_file and payment_voucher_file.filename:
            cmd.payment_voucher = await save_transaction_voucher(payment_voucher_file, "payment")
        entity = await use_case.execute(cmd)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    if not entity:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return entity


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(transaction_id: UUID, use_case: DeleteTransactionUseCaseDep):
    await use_case.execute(transaction_id)
