# app/modules/coin/application/use_cases/commission_use_cases.py
"""Casos de uso CRUD para Commission."""
from uuid import UUID
from typing import List, Optional

from app.modules.coin.domain.models import Commission, CommissionHistory
from app.modules.coin.interfaces.commission_history_repository import CommissionHistoryRepositoryInterface
from app.modules.coin.interfaces.commission_repository import CommissionRepositoryInterface
from app.modules.coin.application.schemas.commission_schema import (
    CommissionCreateCmd,
    CommissionUpdateCmd,
    CommissionReadDTO,
)
from app.modules.coin.application.schemas.commission_history_schema import CommissionHistoryReadDTO
from app.modules.coin.application.use_cases.history_utils import build_snapshot, diff_fields
from app.middlewares.auth import get_current_user
from app.shared.query_filter import FilterSchema, QueryFilter


COMMISSION_AUDIT_FIELDS = [
    "id",
    "coin_a",
    "coin_b",
    "percentage",
    "reverse",
    "min_amount",
    "max_amount",
    "deleted",
    "enable",
]


def _resolve_actor() -> str:
    current_user = get_current_user() or {}
    return (
        current_user.get("username")
        or current_user.get("user_id")
        or "system"
    )


class GetCommissionByIdUseCase:
    def __init__(self, repo: CommissionRepositoryInterface):
        self.repo = repo

    async def execute(self, commission_id: UUID) -> Optional[CommissionReadDTO]:
        entity = await self.repo.get(commission_id)
        if not entity:
            return None
        return CommissionReadDTO.model_validate(entity)


class ListCommissionsUseCase:
    def __init__(self, repo: CommissionRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[CommissionReadDTO]:
        items = await self.repo.list()
        return [CommissionReadDTO.model_validate(x) for x in items]


class CreateCommissionUseCase:
    def __init__(
        self,
        repo: CommissionRepositoryInterface,
        history_repo: CommissionHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, cmd: CommissionCreateCmd) -> CommissionReadDTO:
        entity = Commission(
            coin_a=cmd.coin_a,
            coin_b=cmd.coin_b,
            percentage=cmd.percentage,
            reverse=cmd.reverse,
            min_amount=cmd.min_amount,
            max_amount=cmd.max_amount,
        )
        saved = await self.repo.add(entity)
        after_data = build_snapshot(saved, COMMISSION_AUDIT_FIELDS)
        history = CommissionHistory(
            commission_id=saved.id,
            action="create",
            before_data=None,
            after_data=after_data,
            changed_fields=sorted(after_data.keys()),
            changed_by=_resolve_actor(),
        )
        await self.history_repo.add(history)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return CommissionReadDTO.model_validate(saved)


class UpdateCommissionUseCase:
    def __init__(
        self,
        repo: CommissionRepositoryInterface,
        history_repo: CommissionHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, cmd: CommissionUpdateCmd) -> Optional[CommissionReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
        before_data = build_snapshot(entity, COMMISSION_AUDIT_FIELDS)
        if cmd.coin_a is not None:
            entity.coin_a = cmd.coin_a
        if cmd.coin_b is not None:
            entity.coin_b = cmd.coin_b
        if cmd.percentage is not None:
            entity.percentage = cmd.percentage
        if cmd.reverse is not None:
            entity.reverse = cmd.reverse
        if cmd.min_amount is not None:
            entity.min_amount = cmd.min_amount
        if cmd.max_amount is not None:
            entity.max_amount = cmd.max_amount
        after_data = build_snapshot(entity, COMMISSION_AUDIT_FIELDS)
        changed_fields = diff_fields(before_data, after_data)
        await self.repo.update(entity)
        if changed_fields:
            history = CommissionHistory(
                commission_id=entity.id,
                action="update",
                before_data=before_data,
                after_data=after_data,
                changed_fields=changed_fields,
                changed_by=_resolve_actor(),
            )
            await self.history_repo.add(history)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return CommissionReadDTO.model_validate(entity)


class DeleteCommissionUseCase:
    def __init__(
        self,
        repo: CommissionRepositoryInterface,
        history_repo: CommissionHistoryRepositoryInterface,
    ):
        self.repo = repo
        self.history_repo = history_repo

    async def execute(self, commission_id: UUID) -> None:
        entity = await self.repo.get(commission_id)
        before_data = build_snapshot(entity, COMMISSION_AUDIT_FIELDS) if entity else None
        await self.repo.delete(commission_id)
        if entity:
            history = CommissionHistory(
                commission_id=commission_id,
                action="delete",
                before_data=before_data,
                after_data={"deleted": True},
                changed_fields=["deleted"],
                changed_by=_resolve_actor(),
            )
            await self.history_repo.add(history)
        await self.repo.commit()


class ListCommissionHistoryUseCase:
    def __init__(self, history_repo: CommissionHistoryRepositoryInterface):
        self.history_repo = history_repo

    async def execute(self, commission_id: UUID) -> List[CommissionHistoryReadDTO]:
        query_filter = QueryFilter(filters=[FilterSchema(field="commission_id", value=commission_id)])
        items = await self.history_repo.list(query_filter=query_filter)
        return [CommissionHistoryReadDTO.model_validate(x) for x in items]
