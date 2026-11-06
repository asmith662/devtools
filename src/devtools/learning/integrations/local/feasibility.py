# Copyright (c) 2026
import json
from datetime import datetime
from enum import Enum
from uuid import UUID


def json_document(value: object) -> object:
    """Safe deterministic JSON primitives; no arbitrary object reconstruction."""

    def default(item: object) -> str:
        if isinstance(item, Enum):
            return str(item.value)
        if isinstance(item, UUID):
            return str(item)
        if isinstance(item, datetime):
            return item.isoformat()
        msg = "unsupported feasibility wire object"
        raise TypeError(msg)

    return json.loads(
        json.dumps(value, default=default, sort_keys=True, allow_nan=False),
    )
