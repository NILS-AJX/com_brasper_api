# app/modules/transactions/adapters/router/transaction_routes.py
import json
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, Request, UploadFile, status
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.modules.transactions.domain.enums import TransactionStatus
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
async def list_transactions(
    use_case: ListTransactionsUseCaseDep,
    status: Optional[TransactionStatus] = Query(None, description="Filtro por estado (pending, completed, failed)"),
    user_id: Optional[UUID] = Query(None, description="Filtro por ID de usuario"),
    bank_account_origin_id: Optional[UUID] = Query(None, description="Filtro por cuenta origen"),
    bank_account_destination_id: Optional[UUID] = Query(None, description="Filtro por cuenta destino"),
    created_at_from: Optional[datetime] = Query(None, description="Filtro: transacciones desde esta fecha (ISO)"),
    created_at_to: Optional[datetime] = Query(None, description="Filtro: transacciones hasta esta fecha (ISO)"),
):
    """Lista transacciones. Filtros: status, user_id, bank_account_origin_id, bank_account_destination_id, created_at_from, created_at_to."""
    return await use_case.execute(
        status=status,
        user_id=user_id,
        bank_account_origin_id=bank_account_origin_id,
        bank_account_destination_id=bank_account_destination_id,
        created_at_from=created_at_from,
        created_at_to=created_at_to,
    )


@router.get("/{transaction_id}", response_model=TransactionReadDTO)
async def get_transaction_by_id(transaction_id: UUID, use_case: GetTransactionByIdUseCaseDep):
    entity = await use_case.execute(transaction_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return entity


def _is_form_request(content_type: str) -> bool:
    return "multipart/form-data" in content_type or "application/x-www-form-urlencoded" in content_type


async def _parse_create_request(
    request: Request,
) -> tuple[TransactionCreateCmd, Optional[UploadFile], Optional[UploadFile]]:
    content_type = request.headers.get("content-type", "")
    if _is_form_request(content_type):
        form = await request.form()
        from app.modules.transactions.application.schemas.transaction_schema import (
            _parse_optional_datetime,
            _parse_optional_float,
            _parse_optional_uuid,
        )
        from app.modules.transactions.domain.enums import TransactionStatus
        cmd = TransactionCreateCmd(
            bank_account_origin=UUID(form.get("bank_account_origin", "")),
            bank_account_destination=UUID(form.get("bank_account_destination", "")),
            user_id=UUID(form.get("user_id", "")),
            tax_rate_id=UUID(form.get("tax_rate_id", "")),
            commission_id=UUID(form.get("commission_id", "")),
            status=TransactionStatus(form.get("status", "pending") or "pending"),
            origin_amount=float(form.get("origin_amount", 0)),
            destination_amount=float(form.get("destination_amount", 0)),
            code=form.get("code", ""),
            commission_result=_parse_optional_float(
                form.get("commission_result") or form.get("resultado_comision")
            ),
            total_to_send=_parse_optional_float(
                form.get("total_to_send") or form.get("total_a_enviar")
            ),
            coupon_id=_parse_optional_uuid(form.get("coupon_id")),
            send_date=_parse_optional_datetime(form.get("send_date")),
            payment_date=_parse_optional_datetime(form.get("payment_date")),
            send_voucher=None,
            payment_voucher=None,
        )
        send_f = form.get("send_voucher") if "send_voucher" in form else None
        pay_f = form.get("payment_voucher") if "payment_voucher" in form else None
        if send_f and hasattr(send_f, "filename") and not send_f.filename:
            send_f = None
        if pay_f and hasattr(pay_f, "filename") and not pay_f.filename:
            pay_f = None
        return cmd, send_f, pay_f
    body = await request.json()
    cmd = TransactionCreateCmd.model_validate(body)
    return cmd, None, None


@router.post(
    "/",
    response_model=TransactionReadDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Create Transaction",
    responses={201: {"description": "Transacción creada"}, 400: {"description": "Datos inválidos"}},
    openapi_extra={
        "requestBody": {
            "required": True,
            "content": {
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/TransactionCreateCmd"},
                    "example": {
                        "bank_account_origin": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "bank_account_destination": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "tax_rate_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "commission_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "status": "pending",
                        "origin_amount": 100.0,
                        "destination_amount": 95.0,
                        "code": "TXN-001",
                        "commission_result": 5.0,
                        "total_to_send": 100.0,
                    },
                },
                "multipart/form-data": {
                    "schema": {"$ref": "#/components/schemas/TransactionCreateCmd"},
                },
            },
        },
    },
)
async def create_transaction(request: Request, use_case: CreateTransactionUseCaseDep):
    """Crea transacción. Acepta JSON o form-data (multipart)."""
    try:
        cmd, send_voucher_file, payment_voucher_file = await _parse_create_request(request)
        if send_voucher_file and send_voucher_file.filename:
            cmd.send_voucher = await save_transaction_voucher(send_voucher_file, "send")
        if payment_voucher_file and payment_voucher_file.filename:
            cmd.payment_voucher = await save_transaction_voucher(payment_voucher_file, "payment")
        return await use_case.execute(cmd)
    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"JSON inválido: {e}",
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors(),
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Referencia inválida: bank_account_origin, bank_account_destination, user, tax_rate, commission o coupon no existe",
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


async def _parse_update_request(
    request: Request,
) -> tuple[TransactionUpdateCmd, Optional[UploadFile], Optional[UploadFile]]:
    content_type = request.headers.get("content-type", "")
    if _is_form_request(content_type):
        form = await request.form()
        from app.modules.transactions.application.schemas.transaction_schema import (
            _parse_optional_datetime,
            _parse_optional_float,
            _parse_optional_uuid,
        )
        from app.modules.transactions.domain.enums import TransactionStatus

        cmd = TransactionUpdateCmd(
            id=UUID(form.get("id", "")),
            bank_account_origin=_parse_optional_uuid(form.get("bank_account_origin")),
            bank_account_destination=_parse_optional_uuid(form.get("bank_account_destination")),
            user_id=_parse_optional_uuid(form.get("user_id")),
            tax_rate_id=_parse_optional_uuid(form.get("tax_rate_id")),
            commission_id=_parse_optional_uuid(form.get("commission_id")),
            status=TransactionStatus(form["status"]) if form.get("status") else None,
            origin_amount=_parse_optional_float(form.get("origin_amount")),
            destination_amount=_parse_optional_float(form.get("destination_amount")),
            code=form.get("code"),
            commission_result=_parse_optional_float(
                form.get("commission_result") or form.get("resultado_comision")
            ),
            total_to_send=_parse_optional_float(
                form.get("total_to_send") or form.get("total_a_enviar")
            ),
            coupon_id=_parse_optional_uuid(form.get("coupon_id")),
            send_date=_parse_optional_datetime(form.get("send_date")),
            payment_date=_parse_optional_datetime(form.get("payment_date")),
            send_voucher=None,
            payment_voucher=None,
        )
        send_f = form.get("send_voucher") if "send_voucher" in form else None
        pay_f = form.get("payment_voucher") if "payment_voucher" in form else None
        if send_f and hasattr(send_f, "filename") and not send_f.filename:
            send_f = None
        if pay_f and hasattr(pay_f, "filename") and not pay_f.filename:
            pay_f = None
        return cmd, send_f, pay_f
    body = await request.json()
    cmd = TransactionUpdateCmd.model_validate(body)
    return cmd, None, None


@router.put("/", response_model=TransactionReadDTO)
async def update_transaction(request: Request, use_case: UpdateTransactionUseCaseDep):
    """Actualiza transacción. Acepta JSON o form-data (multipart)."""
    try:
        cmd, send_voucher_file, payment_voucher_file = await _parse_update_request(request)
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
