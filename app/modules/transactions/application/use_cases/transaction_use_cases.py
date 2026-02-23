# app/modules/transactions/application/use_cases/transaction_use_cases.py
"""Casos de uso CRUD para Transaction."""
from datetime import datetime
from uuid import UUID
from typing import List, Optional

from app.shared.query_filter import FilterSchema, OperatorEnum, QueryFilter
from app.modules.transactions.domain.models import Transaction
from app.modules.transactions.domain.enums import TransactionStatus
from app.modules.transactions.interfaces.transaction_repository import TransactionRepositoryInterface
from app.modules.transactions.application.schemas.transaction_schema import (
    TransactionCreateCmd,
    TransactionUpdateCmd,
    TransactionReadDTO,
)


class GetTransactionByIdUseCase:
    def __init__(self, repo: TransactionRepositoryInterface):
        self.repo = repo

    async def execute(self, transaction_id: UUID) -> Optional[TransactionReadDTO]:
        entity = await self.repo.get(transaction_id)
        if not entity:
            return None
        return TransactionReadDTO.model_validate(entity)


def _build_transaction_query_filter(
    status: Optional[TransactionStatus] = None,
    user_id: Optional[UUID] = None,
    bank_account_origin_id: Optional[UUID] = None,
    bank_account_destination_id: Optional[UUID] = None,
    created_at_from: Optional[datetime] = None,
    created_at_to: Optional[datetime] = None,
) -> Optional[QueryFilter]:
    """Construye QueryFilter para transacciones."""
    filters = []
    if status is not None:
        filters.append(FilterSchema(field="status", value=status, operator=OperatorEnum.EQ))
    if user_id is not None:
        filters.append(FilterSchema(field="user_id", value=user_id, operator=OperatorEnum.EQ))
    if bank_account_origin_id is not None:
        filters.append(FilterSchema(field="bank_account_origin_id", value=bank_account_origin_id, operator=OperatorEnum.EQ))
    if bank_account_destination_id is not None:
        filters.append(FilterSchema(field="bank_account_destination_id", value=bank_account_destination_id, operator=OperatorEnum.EQ))
    if created_at_from is not None:
        filters.append(FilterSchema(field="created_at", value=created_at_from, operator=OperatorEnum.GTE))
    if created_at_to is not None:
        filters.append(FilterSchema(field="created_at", value=created_at_to, operator=OperatorEnum.LTE))
    return QueryFilter(filters=filters) if filters else None


class ListTransactionsUseCase:
    def __init__(self, repo: TransactionRepositoryInterface):
        self.repo = repo

    async def execute(
        self,
        status: Optional[TransactionStatus] = None,
        user_id: Optional[UUID] = None,
        bank_account_origin_id: Optional[UUID] = None,
        bank_account_destination_id: Optional[UUID] = None,
        created_at_from: Optional[datetime] = None,
        created_at_to: Optional[datetime] = None,
    ) -> List[TransactionReadDTO]:
        query_filter = _build_transaction_query_filter(
            status=status,
            user_id=user_id,
            bank_account_origin_id=bank_account_origin_id,
            bank_account_destination_id=bank_account_destination_id,
            created_at_from=created_at_from,
            created_at_to=created_at_to,
        )
        items = await self.repo.list(query_filter=query_filter)
        return [TransactionReadDTO.model_validate(x) for x in items]


class CreateTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: TransactionCreateCmd) -> TransactionReadDTO:
        entity = Transaction(
            bank_account_origin_id=cmd.bank_account_origin,
            bank_account_destination_id=cmd.bank_account_destination,
            user_id=cmd.user_id,
            tax_rate_id=cmd.tax_rate_id,
            commission_id=cmd.commission_id,
            status=cmd.status,
            origin_amount=cmd.origin_amount,
            destination_amount=cmd.destination_amount,
            code=cmd.code,
            commission_result=cmd.commission_result,
            total_to_send=cmd.total_to_send,
            coupon_id=cmd.coupon_id,
            send_date=cmd.send_date,
            payment_date=cmd.payment_date,
            send_voucher=cmd.send_voucher,
            payment_voucher=cmd.payment_voucher,
        )
        saved = await self.repo.add(entity)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return TransactionReadDTO.model_validate(saved)


class UpdateTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: TransactionUpdateCmd) -> Optional[TransactionReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
        if cmd.bank_account_origin is not None:
            entity.bank_account_origin_id = cmd.bank_account_origin
        if cmd.bank_account_destination is not None:
            entity.bank_account_destination_id = cmd.bank_account_destination
        if cmd.user_id is not None:
            entity.user_id = cmd.user_id
        if cmd.tax_rate_id is not None:
            entity.tax_rate_id = cmd.tax_rate_id
        if cmd.commission_id is not None:
            entity.commission_id = cmd.commission_id
        if cmd.status is not None:
            entity.status = cmd.status
        if cmd.origin_amount is not None:
            entity.origin_amount = cmd.origin_amount
        if cmd.destination_amount is not None:
            entity.destination_amount = cmd.destination_amount
        if cmd.code is not None:
            entity.code = cmd.code
        if cmd.commission_result is not None:
            entity.commission_result = cmd.commission_result
        if cmd.total_to_send is not None:
            entity.total_to_send = cmd.total_to_send
        if cmd.coupon_id is not None:
            entity.coupon_id = cmd.coupon_id
        if cmd.send_date is not None:
            entity.send_date = cmd.send_date
        if cmd.payment_date is not None:
            entity.payment_date = cmd.payment_date
        if cmd.send_voucher is not None:
            entity.send_voucher = cmd.send_voucher
        if cmd.payment_voucher is not None:
            entity.payment_voucher = cmd.payment_voucher
        await self.repo.update(entity)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return TransactionReadDTO.model_validate(entity)


class DeleteTransactionUseCase:
    def __init__(self, repo: TransactionRepositoryInterface):
        self.repo = repo

    async def execute(self, transaction_id: UUID) -> None:
        await self.repo.delete(transaction_id)
        await self.repo.commit()
