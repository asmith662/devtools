# Copyright (c) 2026
# ruff: noqa: D103 -- independent published-wire equivalence assertions
"""The real host preserves all three accepted native Tool surfaces."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import asdict
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.navigation import NavigationPolicy
from devtools.agents.coding.projection import request_bytes
from tests.agents.coding.test_inventory import inventory
from tests.agents.coding.test_repository import LIMITS, host_at

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("mode", "fingerprint"),
    [
        ("base", "3656e5d73660e744c484cb90e686fd8e7436084eaccabf176f1642f1e47ee5f4"),
        (
            "navigation",
            "c5b387dcf51398b3168218a13fbe72293b6c5eb866e46292e95aff2fcc5434f2",
        ),
        ("task", "7adcfe7d9c940827a75760645b319d5beadd1174be12198f160f6a695377516c"),
    ],
)
def test_real_preparation_preserves_baseline_native_contract(
    tmp_path: Path,
    mode: str,
    fingerprint: str,
) -> None:
    # These hashes capture the published 0006e913 surface before extraction.
    host = host_at(tmp_path)
    host.navigation = mode != "base"
    host.navigation_policy = NavigationPolicy() if mode == "task" else None
    progress = CodingProgress(LIMITS)
    request = asyncio.run(host.prepare(progress))
    raw = json.dumps(
        [asdict(tool) for tool in request.tools],
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    assert hashlib.sha256(raw).hexdigest() == fingerprint
    assert request.prompt.messages[0].content == host.objective.text
    assert inventory(request)["complete_inventory"] is True
    assert request_bytes(request) <= host.objective.prompt_bytes
    assert not progress.effects
    assert not host.disclosures
    assert not host.active_disclosures
    assert asyncio.run(host.prepare(progress)) == request
