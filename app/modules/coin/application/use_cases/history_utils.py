from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any
from uuid import UUID


def _serialize_value(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, UUID):
        return str(value)
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def build_snapshot(entity: Any, fields: list[str]) -> dict[str, Any]:
    snapshot: dict[str, Any] = {}
    for field in fields:
        snapshot[field] = _serialize_value(getattr(entity, field, None))
    return snapshot


def diff_fields(before_data: dict[str, Any], after_data: dict[str, Any]) -> list[str]:
    changed: list[str] = []
    keys = set(before_data.keys()) | set(after_data.keys())
    for key in keys:
        if before_data.get(key) != after_data.get(key):
            changed.append(key)
    return sorted(changed)
