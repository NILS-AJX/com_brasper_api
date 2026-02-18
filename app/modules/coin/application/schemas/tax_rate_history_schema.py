from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaxRateHistoryReadDTO(BaseModel):
    id: UUID
    tax_rate_id: Optional[UUID] = None
    action: str
    before_data: Optional[dict[str, Any]] = None
    after_data: Optional[dict[str, Any]] = None
    changed_fields: list[str] = Field(default_factory=list)
    changed_by: Optional[str] = None
    changed_at: datetime
    created_at: datetime
    created_by: Optional[str] = None
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
