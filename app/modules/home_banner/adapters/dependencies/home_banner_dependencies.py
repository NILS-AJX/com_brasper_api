"""Inyección de dependencias del módulo home_banner."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.modules.home_banner.interfaces.home_banner_repository import HomeBannerRepositoryInterface
from app.modules.home_banner.infrastructure.repository import SQLAlchemyHomeBannerRepository
from app.modules.home_banner.application.use_cases import (
    GetHomeBannerByIdUseCase,
    ListHomeBannersUseCase,
    CreateHomeBannerUseCase,
    UpdateHomeBannerUseCase,
)


def get_home_banner_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HomeBannerRepositoryInterface:
    return SQLAlchemyHomeBannerRepository(db)


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
