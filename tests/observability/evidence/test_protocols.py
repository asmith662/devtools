# Copyright (c) 2026
"""Tests for the narrow Evidence delivery protocol."""

from __future__ import annotations

from devtools.observability.evidence import EvidenceSink


class _Sink:
    """Structural Evidence sink used only to prove protocol ownership."""

    def accept(self, evidence: object) -> None:
        """Accept a value in this deliberately untyped negative fixture."""
        del evidence


def test_evidence_sink_is_an_observability_protocol() -> None:
    """Evidence delivery belongs to observability rather than execution."""
    assert EvidenceSink.__module__ == "devtools.observability.evidence.protocols"
