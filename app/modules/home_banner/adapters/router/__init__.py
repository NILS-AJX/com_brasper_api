# app/modules/home_banner/adapters/router
from fastapi import APIRouter

from app.modules.home_banner.adapters.router.home_banner_routes import router as home_banner_routes

router = APIRouter(prefix="/home-banner")
router.include_router(home_banner_routes)

__all__ = ["router"]
