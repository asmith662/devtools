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
from importlib.metadata import version
from pathlib import PurePath
from typing import Any

import pytest
from huggingface_hub import hf_hub_download

# Host-owned concrete objects only. No importlib, eval, getattr traversal or
# callable execution from model strings. These are observations, not edit scope.
_APIS: dict[str, Any] = {
    "bytes.decode": bytes.decode,
    "str.encode": str.encode,
    "math.isfinite": math.isfinite,
    "pathlib.PurePath.with_suffix": PurePath.with_suffix,
    "pytest.main": pytest.main,
    "huggingface_hub.hf_hub_download": hf_hub_download,
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
    package = {
        "pytest.main": "pytest",
        "huggingface_hub.hf_hub_download": "huggingface-hub",
    }.get(target)
    value: dict[str, Any] = {
        "target": target,
        "signature": str(inspect.signature(obj)),
        "docstring": doc[:3500],
        "truncated": len(doc) > 3500,
        "package": package or "Python standard library",
        "package_version": version(package) if package else sys.version.split()[0],
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
