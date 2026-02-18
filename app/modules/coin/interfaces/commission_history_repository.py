from app.shared.interface_base import BaseRepositoryInterface
from app.modules.coin.domain.models import CommissionHistory


class CommissionHistoryRepositoryInterface(BaseRepositoryInterface[CommissionHistory]):
    """Puerto de persistencia para CommissionHistory."""
