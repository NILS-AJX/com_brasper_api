from typing import List

from app.shared.interface_base import BaseRepositoryInterface
from app.modules.transactions.domain.models import Bank


class BankRepositoryInterface(BaseRepositoryInterface[Bank]):
    """Puerto de persistencia para Bank."""

    async def list_distinct_names(self) -> List[str]:
        """Lista nombres únicos de bancos (ordenados alfabéticamente)."""
        ...
