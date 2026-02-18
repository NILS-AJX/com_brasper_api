# app/modules/coin/domain/models.py
from datetime import datetime
from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import DateTime, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID as PgUUID
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.coin.domain.enums import Currency, CurrencyEnumType
from app.shared.model_base import ORMBaseModel


class TaxRate(ORMBaseModel):
    """Tasa impositiva entre dos monedas (coin_a → coin_b) con valor tax."""
    __tablename__ = "tax_rate"
    __table_args__ = {"schema": "coin"}

    tax: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False, default=0)
    coin_a: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)
    coin_b: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)


class TaxRateTrial(ORMBaseModel):
    """Tasa prueba entre dos monedas (coin_a → coin_b) con valor tax. Misma estructura que TaxRate."""
    __tablename__ = "tax_rate_trial"
    __table_args__ = {"schema": "coin"}

    tax: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False, default=0)
    coin_a: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)
    coin_b: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)


class Commission(ORMBaseModel):
    """Comisión entre dos monedas (coin_a → coin_b): porcentaje, reversa y montos min/max."""
    __tablename__ = "commission"
    __table_args__ = {"schema": "coin"}

    coin_a: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)
    coin_b: Mapped[Currency] = mapped_column(CurrencyEnumType, nullable=False, index=True)
    percentage: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False, default=0)
    reverse: Mapped[float] = mapped_column(Numeric(20, 8), nullable=False, default=0)
    min_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 8), nullable=True)
    max_amount: Mapped[Optional[float]] = mapped_column(Numeric(20, 8), nullable=True)


class TaxRateHistory(ORMBaseModel):
    """Auditoría de cambios sobre coin.tax_rate."""
    __tablename__ = "tax_rate_history"
    __table_args__ = {"schema": "coin"}

    tax_rate_id: Mapped[Optional[PyUUID]] = mapped_column(
        PgUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    before_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    after_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    changed_fields: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    changed_by: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class CommissionHistory(ORMBaseModel):
    """Auditoría de cambios sobre coin.commission."""
    __tablename__ = "commission_history"
    __table_args__ = {"schema": "coin"}

    commission_id: Mapped[Optional[PyUUID]] = mapped_column(
        PgUUID(as_uuid=True),
        nullable=True,
        index=True,
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    before_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    after_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    changed_fields: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    changed_by: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
