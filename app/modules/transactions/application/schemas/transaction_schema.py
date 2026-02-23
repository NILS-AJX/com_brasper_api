# app/modules/transactions/application/schemas/transaction_schema.py
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import File, Form, UploadFile
from pydantic import BaseModel, ConfigDict

from app.modules.transactions.domain.enums import TransactionStatus


def _parse_optional_datetime(v: Optional[str]) -> Optional[datetime]:
    """Convierte string ISO a datetime o None."""
    if not v or (isinstance(v, str) and v.strip() == ""):
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def _parse_optional_float(v: Optional[str]) -> Optional[float]:
    if v is None or (isinstance(v, str) and v.strip() == ""):
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def _parse_optional_uuid(v: Optional[str]) -> Optional[UUID]:
    if v is None or (isinstance(v, str) and v.strip() == ""):
        return None
    try:
        return UUID(v)
    except (ValueError, TypeError):
        return None


class TransactionCreateCmd(BaseModel):
    bank_account_id: UUID
    user_id: UUID
    tax_rate_id: UUID
    commission_id: UUID
    status: TransactionStatus = TransactionStatus.pending
    origin_amount: float
    destination_amount: float
    code: str
    send_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    send_voucher: Optional[str] = None
    payment_voucher: Optional[str] = None

    @classmethod
    def from_form(
        cls,
        bank_account_id: str = Form(..., description="UUID de cuenta bancaria"),
        user_id: str = Form(..., description="UUID de usuario"),
        tax_rate_id: str = Form(..., description="UUID de tasa"),
        commission_id: str = Form(..., description="UUID de comisión"),
        status: str = Form("pending", description="Estado: pending, completed, failed"),
        origin_amount: str = Form(..., description="Monto origen"),
        destination_amount: str = Form(..., description="Monto destino"),
        code: str = Form(..., description="Código de transacción"),
        send_date: Optional[str] = Form(None),
        payment_date: Optional[str] = Form(None),
        send_voucher: Optional[UploadFile] = File(None),
        payment_voucher: Optional[UploadFile] = File(None),
    ) -> tuple["TransactionCreateCmd", Optional[UploadFile], Optional[UploadFile]]:
        cmd = cls(
            bank_account_id=UUID(bank_account_id),
            user_id=UUID(user_id),
            tax_rate_id=UUID(tax_rate_id),
            commission_id=UUID(commission_id),
            status=TransactionStatus(status) if status else TransactionStatus.pending,
            origin_amount=float(origin_amount),
            destination_amount=float(destination_amount),
            code=code,
            send_date=_parse_optional_datetime(send_date),
            payment_date=_parse_optional_datetime(payment_date),
            send_voucher=None,  # se llenará en la ruta tras guardar
            payment_voucher=None,
        )
        return cmd, send_voucher, payment_voucher


class TransactionUpdateCmd(BaseModel):
    id: UUID
    bank_account_id: Optional[UUID] = None
    user_id: Optional[UUID] = None
    tax_rate_id: Optional[UUID] = None
    commission_id: Optional[UUID] = None
    status: Optional[TransactionStatus] = None
    origin_amount: Optional[float] = None
    destination_amount: Optional[float] = None
    code: Optional[str] = None
    send_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    send_voucher: Optional[str] = None
    payment_voucher: Optional[str] = None

    @classmethod
    def from_form(
        cls,
        id: str = Form(..., description="UUID de la transacción"),
        bank_account_id: Optional[str] = Form(None),
        user_id: Optional[str] = Form(None),
        tax_rate_id: Optional[str] = Form(None),
        commission_id: Optional[str] = Form(None),
        status: Optional[str] = Form(None),
        origin_amount: Optional[str] = Form(None),
        destination_amount: Optional[str] = Form(None),
        code: Optional[str] = Form(None),
        send_date: Optional[str] = Form(None),
        payment_date: Optional[str] = Form(None),
        send_voucher: Optional[UploadFile] = File(None),
        payment_voucher: Optional[UploadFile] = File(None),
    ) -> tuple["TransactionUpdateCmd", Optional[UploadFile], Optional[UploadFile]]:
        cmd = cls(
            id=UUID(id),
            bank_account_id=_parse_optional_uuid(bank_account_id),
            user_id=_parse_optional_uuid(user_id),
            tax_rate_id=_parse_optional_uuid(tax_rate_id),
            commission_id=_parse_optional_uuid(commission_id),
            status=TransactionStatus(status) if status else None,
            origin_amount=_parse_optional_float(origin_amount),
            destination_amount=_parse_optional_float(destination_amount),
            code=code,
            send_date=_parse_optional_datetime(send_date),
            payment_date=_parse_optional_datetime(payment_date),
            send_voucher=None,
            payment_voucher=None,
        )
        return cmd, send_voucher, payment_voucher


class TransactionReadDTO(BaseModel):
    id: UUID
    bank_account_id: UUID
    user_id: UUID
    tax_rate_id: UUID
    commission_id: UUID
    status: TransactionStatus
    origin_amount: float
    destination_amount: float
    code: str
    send_date: Optional[datetime] = None
    payment_date: Optional[datetime] = None
    send_voucher: Optional[str] = None
    payment_voucher: Optional[str] = None
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
