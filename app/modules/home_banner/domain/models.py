from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.model_base import ORMBaseModel


class HomeBanner(ORMBaseModel):
    """Banner de la sección home con imágenes por idioma (es, pr, en)."""
    __tablename__ = "home_banner"
    __table_args__ = {"schema": "home_banner"}

    banner_es: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    banner_pr: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    banner_en: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
