from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.home_banner.domain.models import HomeBanner
from app.modules.home_banner.interfaces.home_banner_repository import HomeBannerRepositoryInterface
from app.shared.repositorie_base import BaseAsyncRepository


class SQLAlchemyHomeBannerRepository(BaseAsyncRepository[HomeBanner], HomeBannerRepositoryInterface):
    def __init__(self, db: AsyncSession):
        super().__init__(HomeBanner, db)
