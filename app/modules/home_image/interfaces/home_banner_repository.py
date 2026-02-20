from app.shared.interface_base import BaseRepositoryInterface
from app.modules.home_image.domain.models import HomeBanner


class HomeBannerRepositoryInterface(BaseRepositoryInterface[HomeBanner]):
    """Puerto de persistencia para HomeBanner."""
    ...
