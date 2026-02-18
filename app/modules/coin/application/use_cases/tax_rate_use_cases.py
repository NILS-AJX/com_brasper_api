# app/modules/coin/application/use_cases/tax_rate_use_cases.py
"""Casos de uso CRUD para TaxRate."""
from uuid import UUID
from typing import List, Optional

from app.modules.coin.domain.models import TaxRate, TaxRateHistory
from app.modules.coin.interfaces.tax_rate_history_repository import TaxRateHistoryRepositoryInterface
from app.modules.coin.interfaces.tax_rate_repository import TaxRateRepositoryInterface
from app.modules.coin.application.schemas.tax_rate_schema import (
    TaxRateCreateCmd,
    TaxRateUpdateCmd,
    TaxRateReadDTO,
)
from app.modules.coin.application.schemas.tax_rate_history_schema import TaxRateHistoryReadDTO
from app.modules.coin.application.use_cases.history_utils import build_snapshot, diff_fields
from app.middlewares.auth import get_current_user
from app.shared.query_filter import FilterSchema, QueryFilter


TAX_RATE_AUDIT_FIELDS = ["id", "coin_a", "coin_b", "tax", "deleted", "enable"]


def _resolve_actor() -> str:
    current_user = get_current_user() or {}
    return (
        current_user.get("username")
        or current_user.get("user_id")
        or "system"
    )


class GetTaxRateByIdUseCase:
    def __init__(self, repo: TaxRateRepositoryInterface):
        self.repo = repo

    async def execute(self, tax_rate_id: UUID) -> Optional[TaxRateReadDTO]:
        entity = await self.repo.get(tax_rate_id)
        if not entity:
            return None
        return TaxRateReadDTO.model_validate(entity)


class ListTaxRatesUseCase:
    def __init__(self, repo: TaxRateRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[TaxRateReadDTO]:
        items = await self.repo.list()
        return [TaxRateReadDTO.model_validate(x) for x in items]


class CreateTaxRateUseCase:
    def __init__(
        self,
        repo: TaxRateRepositoryInterface,
        history_repo: TaxRateHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, cmd: TaxRateCreateCmd) -> TaxRateReadDTO:
        entity = TaxRate(
            coin_a=cmd.coin_a,
            coin_b=cmd.coin_b,
            tax=cmd.tax,
        )
        saved = await self.repo.add(entity)
        after_data = build_snapshot(saved, TAX_RATE_AUDIT_FIELDS)
        history = TaxRateHistory(
            tax_rate_id=saved.id,
            action="create",
            before_data=None,
            after_data=after_data,
            changed_fields=sorted(after_data.keys()),
            changed_by=_resolve_actor(),
        )
        await self.history_repo.add(history)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return TaxRateReadDTO.model_validate(saved)


class UpdateTaxRateUseCase:
    def __init__(
        self,
        repo: TaxRateRepositoryInterface,
        history_repo: TaxRateHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, cmd: TaxRateUpdateCmd) -> Optional[TaxRateReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
        before_data = build_snapshot(entity, TAX_RATE_AUDIT_FIELDS)
        if cmd.coin_a is not None:
            entity.coin_a = cmd.coin_a
        if cmd.coin_b is not None:
            entity.coin_b = cmd.coin_b
        if cmd.tax is not None:
            entity.tax = cmd.tax
        after_data = build_snapshot(entity, TAX_RATE_AUDIT_FIELDS)
        changed_fields = diff_fields(before_data, after_data)
        await self.repo.update(entity)
        if changed_fields:
            history = TaxRateHistory(
                tax_rate_id=entity.id,
                action="update",
                before_data=before_data,
                after_data=after_data,
                changed_fields=changed_fields,
                changed_by=_resolve_actor(),
            )
            await self.history_repo.add(history)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return TaxRateReadDTO.model_validate(entity)


class DeleteTaxRateUseCase:
    def __init__(
        self,
        repo: TaxRateRepositoryInterface,
        history_repo: TaxRateHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, tax_rate_id: UUID) -> None:
        entity = await self.repo.get(tax_rate_id)
        before_data = build_snapshot(entity, TAX_RATE_AUDIT_FIELDS) if entity else None
        await self.repo.delete(tax_rate_id)
        if entity:
            history = TaxRateHistory(
                tax_rate_id=tax_rate_id,
                action="delete",
                before_data=before_data,
                after_data={"deleted": True},
                changed_fields=["deleted"],
                changed_by=_resolve_actor(),
            )
            await self.history_repo.add(history)
        await self.repo.commit()


class ListTaxRateHistoryUseCase:
    def __init__(self, history_repo: TaxRateHistoryRepositoryInterface):
        self.history_repo = history_repo

    async def execute(self, tax_rate_id: UUID) -> List[TaxRateHistoryReadDTO]:
        query_filter = QueryFilter(filters=[FilterSchema(field="tax_rate_id", value=tax_rate_id)])
        items = await self.history_repo.list(query_filter=query_filter)
        return [TaxRateHistoryReadDTO.model_validate(x) for x in items]
