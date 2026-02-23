"""Casos de uso CRUD y listado agrupado para Bank."""
from uuid import UUID
from typing import List, Optional

from app.modules.transactions.domain.models import Bank
from app.modules.transactions.interfaces.bank_repository import BankRepositoryInterface
from app.modules.transactions.application.schemas.bank_schema import (
    BankCreateCmd,
    BankUpdateCmd,
    BankReadDTO,
    BankItemDTO,
    BankOptionDTO,
    BanksByCountryCurrencyDTO,
    CURRENCY_DISPLAY_BANK,
    DISPLAY_TO_CURRENCY,
)
from app.modules.transactions.domain.enums import BankCountry, SocialActor
from app.modules.coin.domain.enums import Currency
from app.shared.query_filter import FilterSchema, OperatorEnum, QueryFilter


def _to_item_dto(entity: Bank) -> BankItemDTO:
    return BankItemDTO(
        bank=entity.bank,
        account=entity.account,
        pix=entity.pix,
        company=entity.company,
        currency=CURRENCY_DISPLAY_BANK.get(entity.currency.value, entity.currency.value.upper()),
        image=entity.image,
        social_actor=entity.social_actor,
    )


class GetBankByIdUseCase:
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self, bank_id: UUID) -> Optional[BankReadDTO]:
        entity = await self.repo.get(bank_id)
        if not entity:
            return None
        return BankReadDTO.from_bank(entity)


class ListBanksUseCase:
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(
        self,
        bank: Optional[str] = None,
        company: Optional[str] = None,
        currency: Optional[str] = None,
        currency_display: Optional[str] = None,
        social_actor: Optional[str] = None,
    ) -> List[BankReadDTO]:
        filters: List[FilterSchema] = []

        if bank and bank.strip():
            filters.append(FilterSchema(field="bank", value=f"%{bank.strip()}%", operator=OperatorEnum.ILIKE))
        if company and company.strip():
            filters.append(FilterSchema(field="company", value=f"%{company.strip()}%", operator=OperatorEnum.ILIKE))

        # currency: acepta pen, PEN, usd, USD, etc.
        if currency and currency.strip():
            curr_str = currency.strip().upper()
            try:
                curr_enum = Currency(curr_str)  # Currency("PEN") -> pen
                filters.append(FilterSchema(field="currency", value=curr_enum, operator=OperatorEnum.EQ))
            except (ValueError, KeyError):
                pass  # valor inválido, ignorar

        # currency_display: "Soles (PEN)", "Dólares (USD)", "Reales (BRL)"
        if currency_display and currency_display.strip():
            curr_key = DISPLAY_TO_CURRENCY.get(currency_display.strip())
            if curr_key:
                curr_enum = Currency[curr_key]
                filters.append(FilterSchema(field="currency", value=curr_enum, operator=OperatorEnum.EQ))

        # social_actor: naturalPerson, legalEntity, generalAspect
        if social_actor and social_actor.strip():
            try:
                actor_enum = SocialActor(social_actor.strip())
                filters.append(FilterSchema(field="social_actor", value=actor_enum, operator=OperatorEnum.EQ))
            except (ValueError, KeyError):
                pass

        query_filter = QueryFilter(filters=filters) if filters else None
        items = await self.repo.list(query_filter=query_filter)
        return [BankReadDTO.from_bank(x) for x in items]


class ListBankNamesUseCase:
    """Devuelve lista de bancos con id, bank, currency, country (para dropdowns, filtros, etc.)."""
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self) -> List[BankOptionDTO]:
        items = await self.repo.list()
        return [
            BankOptionDTO(id=x.id, bank=x.bank, currency=x.currency, country=x.country)
            for x in sorted(items, key=lambda b: (b.bank, b.currency.value))
        ]


class ListBanksByCountryCurrencyUseCase:
    """Devuelve bancos agrupados por país (PE, BR) y luego por moneda (PEN, USD, BRL)."""
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self) -> BanksByCountryCurrencyDTO:
        items = await self.repo.list()
        pe: dict[str, list[BankItemDTO]] = {}
        br: dict[str, list[BankItemDTO]] = {}
        for entity in items:
            item = _to_item_dto(entity)
            key = entity.currency.value.upper()
            if entity.country == BankCountry.pe:
                pe.setdefault(key, []).append(item)
            else:
                br.setdefault(key, []).append(item)
        return BanksByCountryCurrencyDTO(pe=pe if pe else None, br=br if br else None)


class CreateBankUseCase:
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: BankCreateCmd) -> BankReadDTO:
        entity = Bank(
            bank=cmd.bank,
            account=cmd.account,
            pix=cmd.pix,
            company=cmd.company,
            currency=cmd.currency,
            image=cmd.image,
            country=cmd.country,
            social_actor=cmd.social_actor,
        )
        saved = await self.repo.add(entity)
        await self.repo.commit()
        await self.repo.refresh(saved)
        return BankReadDTO.from_bank(saved)


class UpdateBankUseCase:
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self, cmd: BankUpdateCmd) -> Optional[BankReadDTO]:
        entity = await self.repo.get(cmd.id)
        if not entity:
            return None
        if cmd.bank is not None:
            entity.bank = cmd.bank
        if cmd.account is not None:
            entity.account = cmd.account
        if cmd.pix is not None:
            entity.pix = cmd.pix
        if cmd.company is not None:
            entity.company = cmd.company
        if cmd.currency is not None:
            entity.currency = cmd.currency
        if cmd.image is not None:
            entity.image = cmd.image
        if cmd.country is not None:
            entity.country = cmd.country
        if cmd.social_actor is not None:
            entity.social_actor = cmd.social_actor
        await self.repo.update(entity)
        await self.repo.commit()
        await self.repo.refresh(entity)
        return BankReadDTO.from_bank(entity)


class DeleteBankUseCase:
    def __init__(self, repo: BankRepositoryInterface):
        self.repo = repo

    async def execute(self, bank_id: UUID) -> None:
        await self.repo.delete(bank_id)
        await self.repo.commit()
