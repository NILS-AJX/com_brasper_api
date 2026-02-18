"""Casos de uso CRUD para CommissionTrial (comisión de prueba)."""
from uuid import UUID
from typing import List, Optional

from app.modules.coin.domain.models import CommissionTrial
from app.modules.coin.interfaces.commission_trial_repository import CommissionTrialRepositoryInterface
from app.modules.coin.application.schemas.commission_trial_schema import (
    CommissionTrialCreateCmd,
    CommissionTrialUpdateCmd,
    CommissionTrialReadDTO,
)


class GetCommissionTrialByIdUseCase:
    def __init__(self, repo: CommissionTrialRepositoryInterface):
        self.repo = repo

    async def execute(self, commission_trial_id: UUID) -> Optional[CommissionTrialReadDTO]:
        entity = await self.repo.get(commission_trial_id)
        if not entity:
            return None
        return CommissionTrialReadDTO.model_validate(entity)


class ListCommissionTrialsUseCase:
    def __init__(self, repo: CommissionTrialRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[CommissionTrialReadDTO]:
        items = await self.repo.list()
        return [CommissionTrialReadDTO.model_validate(x) for x in items]


class CreateCommissionTrialUseCase:
    def __init__(self, repo: CommissionTrialRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: CommissionTrialCreateCmd) -> CommissionTrialReadDTO:
        entity = CommissionTrial(
            coin_a=cmd.coin_a,
            coin_b=cmd.coin_b,
            percentage=cmd.percentage,
            reverse=cmd.reverse,
            min_amount=cmd.min_amount,
            max_amount=cmd.max_amount,
        )
        saved = await self.repo.add(entity)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return CommissionTrialReadDTO.model_validate(saved)


class UpdateCommissionTrialUseCase:
    def __init__(self, repo: CommissionTrialRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: CommissionTrialUpdateCmd) -> Optional[CommissionTrialReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
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
        await self.repo.update(entity)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return CommissionTrialReadDTO.model_validate(entity)


class DeleteCommissionTrialUseCase:
    def __init__(self, repo: CommissionTrialRepositoryInterface):
        self.repo = repo

    async def execute(self, commission_trial_id: UUID) -> None:
        await self.repo.delete(commission_trial_id)
        await self.repo.commit()
