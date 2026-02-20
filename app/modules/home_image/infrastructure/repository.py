from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.home_image.domain.models import HomeBanner, HomePopup
from app.modules.home_image.interfaces.home_banner_repository import HomeBannerRepositoryInterface
from app.modules.home_image.interfaces.home_popup_repository import HomePopupRepositoryInterface
from app.shared.repositorie_base import BaseAsyncRepository


class SQLAlchemyHomeBannerRepository(BaseAsyncRepository[HomeBanner], HomeBannerRepositoryInterface):
    def __init__(self, db: AsyncSession):
        super().__init__(HomeBanner, db)


class SQLAlchemyHomePopupRepository(BaseAsyncRepository[HomePopup], HomePopupRepositoryInterface):
    def __init__(self, db: AsyncSession):
        super().__init__(HomePopup, db)
