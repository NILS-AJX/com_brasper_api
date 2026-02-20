"""Casos de uso CRUD para HomePopup (GET, POST, PUT)."""
from uuid import UUID
from typing import List, Optional

from app.modules.home_image.domain.models import HomePopup
from app.modules.home_image.interfaces.home_popup_repository import HomePopupRepositoryInterface
from app.modules.home_image.application.schemas.home_popup_schema import (
    HomePopupCreateCmd,
    HomePopupUpdateCmd,
    HomePopupReadDTO,
)


class GetHomePopupByIdUseCase:
    def __init__(self, repo: HomePopupRepositoryInterface):
        self.repo = repo

    async def execute(self, home_popup_id: UUID) -> Optional[HomePopupReadDTO]:
        entity = await self.repo.get(home_popup_id)
        if not entity:
            return None
        return HomePopupReadDTO.model_validate(entity)


class ListHomePopupsUseCase:
    def __init__(self, repo: HomePopupRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[HomePopupReadDTO]:
        items = await self.repo.list()
        return [HomePopupReadDTO.model_validate(x) for x in items]


class CreateHomePopupUseCase:
    def __init__(self, repo: HomePopupRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: HomePopupCreateCmd) -> HomePopupReadDTO:
        entity = HomePopup(
            popup_es=cmd.popup_es,
            popup_pr=cmd.popup_pr,
            popup_en=cmd.popup_en,
            enable=cmd.enable,
        )
        saved = await self.repo.add(entity)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return HomePopupReadDTO.model_validate(saved)


class UpdateHomePopupUseCase:
    def __init__(self, repo: HomePopupRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: HomePopupUpdateCmd) -> Optional[HomePopupReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
        if cmd.popup_es is not None:
            entity.popup_es = cmd.popup_es
        if cmd.popup_pr is not None:
            entity.popup_pr = cmd.popup_pr
        if cmd.popup_en is not None:
            entity.popup_en = cmd.popup_en
        if cmd.enable is not None:
            entity.enable = cmd.enable
        await self.repo.update(entity)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return HomePopupReadDTO.model_validate(entity)
