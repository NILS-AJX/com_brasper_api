"""Inyección de dependencias del módulo home_image."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.modules.home_image.interfaces.home_banner_repository import HomeBannerRepositoryInterface
from app.modules.home_image.interfaces.home_popup_repository import HomePopupRepositoryInterface
from app.modules.home_image.infrastructure.repository import (
    SQLAlchemyHomeBannerRepository,
    SQLAlchemyHomePopupRepository,
)
from app.modules.home_image.application.use_cases import (
    GetHomeBannerByIdUseCase,
    ListHomeBannersUseCase,
    CreateHomeBannerUseCase,
    UpdateHomeBannerUseCase,
    GetHomePopupByIdUseCase,
    ListHomePopupsUseCase,
    CreateHomePopupUseCase,
    UpdateHomePopupUseCase,
)


def get_home_banner_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HomeBannerRepositoryInterface:
    return SQLAlchemyHomeBannerRepository(db)


def get_home_popup_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HomePopupRepositoryInterface:
    return SQLAlchemyHomePopupRepository(db)


def get_home_banner_by_id_uc(
    repo: Annotated[HomeBannerRepositoryInterface, Depends(get_home_banner_repository)],
) -> GetHomeBannerByIdUseCase:
    return GetHomeBannerByIdUseCase(repo)


def list_home_banners_uc(
    repo: Annotated[HomeBannerRepositoryInterface, Depends(get_home_banner_repository)],
) -> ListHomeBannersUseCase:
    return ListHomeBannersUseCase(repo)


def create_home_banner_uc(
    repo: Annotated[HomeBannerRepositoryInterface, Depends(get_home_banner_repository)],
) -> CreateHomeBannerUseCase:
    return CreateHomeBannerUseCase(repo)


def update_home_banner_uc(
    repo: Annotated[HomeBannerRepositoryInterface, Depends(get_home_banner_repository)],
) -> UpdateHomeBannerUseCase:
    return UpdateHomeBannerUseCase(repo)


GetHomeBannerByIdUseCaseDep = Annotated[GetHomeBannerByIdUseCase, Depends(get_home_banner_by_id_uc)]
ListHomeBannersUseCaseDep = Annotated[ListHomeBannersUseCase, Depends(list_home_banners_uc)]
CreateHomeBannerUseCaseDep = Annotated[CreateHomeBannerUseCase, Depends(create_home_banner_uc)]
UpdateHomeBannerUseCaseDep = Annotated[UpdateHomeBannerUseCase, Depends(update_home_banner_uc)]


def get_home_popup_by_id_uc(
    repo: Annotated[HomePopupRepositoryInterface, Depends(get_home_popup_repository)],
) -> GetHomePopupByIdUseCase:
    return GetHomePopupByIdUseCase(repo)


def list_home_popups_uc(
    repo: Annotated[HomePopupRepositoryInterface, Depends(get_home_popup_repository)],
) -> ListHomePopupsUseCase:
    return ListHomePopupsUseCase(repo)


def create_home_popup_uc(
    repo: Annotated[HomePopupRepositoryInterface, Depends(get_home_popup_repository)],
) -> CreateHomePopupUseCase:
    return CreateHomePopupUseCase(repo)


def update_home_popup_uc(
    repo: Annotated[HomePopupRepositoryInterface, Depends(get_home_popup_repository)],
) -> UpdateHomePopupUseCase:
    return UpdateHomePopupUseCase(repo)


GetHomePopupByIdUseCaseDep = Annotated[GetHomePopupByIdUseCase, Depends(get_home_popup_by_id_uc)]
ListHomePopupsUseCaseDep = Annotated[ListHomePopupsUseCase, Depends(list_home_popups_uc)]
CreateHomePopupUseCaseDep = Annotated[CreateHomePopupUseCase, Depends(create_home_popup_uc)]
UpdateHomePopupUseCaseDep = Annotated[UpdateHomePopupUseCase, Depends(update_home_popup_uc)]
