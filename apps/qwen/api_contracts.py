# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, PLR2004 -- bounded local consumer
"""Fixed installed Python API observations, never arbitrary imports/execution."""

from __future__ import annotations

import hashlib
import inspect
import json
import math
import re
import sys
from pathlib import PurePath
from typing import Any

# Host-owned concrete objects only. No importlib, eval, getattr traversal or
# callable execution from model strings. These are observations, not edit scope.
_APIS: dict[str, Any] = {
    "bytes.decode": bytes.decode,
    "str.encode": str.encode,
    "math.isfinite": math.isfinite,
    "pathlib.PurePath.with_suffix": PurePath.with_suffix,
    "json.loads": json.loads,
    "json.JSONDecoder": json.JSONDecoder,
    "re.Pattern.finditer": re.Pattern.finditer,
    "re.Pattern.search": re.Pattern.search,
    "re.Pattern.fullmatch": re.Pattern.fullmatch,
}
API_TARGETS = tuple(_APIS)


def inspect_contract(target: str, allowed: tuple[str, ...]) -> dict[str, Any]:
    """Read a fixed object's installed signature/docstring without calling it."""
    if target not in allowed or target not in _APIS:
        raise ValueError("API target is not host-authorized")
    obj = _APIS[target]
    doc = inspect.getdoc(obj) or "NOT_DOCUMENTED"
    value: dict[str, Any] = {
        "target": target,
        "signature": str(inspect.signature(obj)),
        "docstring": doc[:3500],
        "truncated": len(doc) > 3500,
        "package": "Python standard library",
        "package_version": sys.version.split()[0],
        "implementation": sys.implementation.name,
        "authority": "installed allowlisted API observation; not model inference",
        "limitations": (
            "Signature **kwargs alone does not validate a keyword; no usage executed."
        ),
    }
    if target == "json.loads":
        value["delegated_decoder_signature"] = str(inspect.signature(json.JSONDecoder))
    value["observation_id"] = hashlib.sha256(
        json.dumps(value, sort_keys=True).encode()
    ).hexdigest()
    return value
