# Copyright (c) 2026
"""Original canonical JSON source fingerprints; not occurrence identities."""

import hashlib
import json
from enum import Enum


def fingerprint(value: object) -> str:
    """Canonical numerical/input binding; not an authentication claim."""
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode(),
    ).hexdigest()


def source_fingerprint(value: object) -> str:
    """Bind typed original source specifications, including declared enums."""

    def enum_value(item: object) -> object:

        if isinstance(item, Enum):
            return item.value

        msg = "unsupported ranking source identity value"
        raise TypeError(msg)

    return fingerprint(
        json.loads(json.dumps(value, default=enum_value, allow_nan=False)),
    )
