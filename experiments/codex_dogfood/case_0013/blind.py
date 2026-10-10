# Copyright (c) 2026
# ruff: noqa: COM812 -- formatter owns commas
"""Future blind packet allowlist; this stage creates no packet or gold."""

from __future__ import annotations

from typing import Any

from experiments.codex_dogfood.case_0012.blind import (
    packet_projection as native_projection,
)


def packet_projection(
    treatment: dict[str, Any], resources: list[dict[str, Any]]
) -> dict[str, Any]:
    """Reuse the task/obligation/content-only boundary, with a new case owner."""
    packet = native_projection(treatment, resources)
    packet["case"] = "case-0013"
    return packet
