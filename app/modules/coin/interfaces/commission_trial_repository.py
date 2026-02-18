from app.shared.interface_base import BaseRepositoryInterface
from app.modules.coin.domain.models import CommissionTrial


class CommissionTrialRepositoryInterface(BaseRepositoryInterface[CommissionTrial]):
    """Puerto de persistencia para CommissionTrial (comisión de prueba)."""
