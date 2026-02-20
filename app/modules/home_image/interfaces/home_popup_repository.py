from app.shared.interface_base import BaseRepositoryInterface
from app.modules.home_image.domain.models import HomePopup


class HomePopupRepositoryInterface(BaseRepositoryInterface[HomePopup]):
    """Puerto de persistencia para HomePopup."""
    ...
