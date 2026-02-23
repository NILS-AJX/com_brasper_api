from __future__ import annotations

from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.transactions.domain.models import Bank
from app.modules.transactions.interfaces.bank_repository import BankRepositoryInterface
from app.shared.repositorie_base import BaseAsyncRepository


class SQLAlchemyBankRepository(
    BaseAsyncRepository[Bank], BankRepositoryInterface
):
    def __init__(self, db: AsyncSession):
        super().__init__(Bank, db)

    async def list_distinct_names(self) -> List[str]:
        """Lista nombres únicos de bancos (ordenados alfabéticamente)."""
        stmt = (
            select(Bank.bank)
            .where(Bank.deleted.is_(False))
            .distinct()
            .order_by(Bank.bank)
        )
        result = await self.session.execute(stmt)
        return [row[0] for row in result.all()]
