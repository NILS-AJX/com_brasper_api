from app.shared.interface_base import BaseRepositoryInterface
from app.modules.coin.domain.models import TaxRateHistory


class TaxRateHistoryRepositoryInterface(BaseRepositoryInterface[TaxRateHistory]):
    """Puerto de persistencia para TaxRateHistory."""
