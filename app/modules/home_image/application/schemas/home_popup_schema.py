from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class HomePopupCreateCmd(BaseModel):
    popup_es: Optional[str] = Field(default=None, max_length=500)
    popup_pr: Optional[str] = Field(default=None, max_length=500)
    popup_en: Optional[str] = Field(default=None, max_length=500)
    enable: bool = Field(default=True)


class HomePopupUpdateCmd(BaseModel):
    id: UUID
    popup_es: Optional[str] = Field(default=None, max_length=500)
    popup_pr: Optional[str] = Field(default=None, max_length=500)
    popup_en: Optional[str] = Field(default=None, max_length=500)
    enable: Optional[bool] = None


class HomePopupReadDTO(BaseModel):
    id: UUID
    popup_es: Optional[str] = None
    popup_pr: Optional[str] = None
    popup_en: Optional[str] = None
    enable: bool
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
