# Copyright (c) 2026
# ruff: noqa: S101, D103 -- publication byte-equivalence fixtures
"""Memoized statistics fragments preserve every frozen serialization byte."""

from __future__ import annotations

from typing import TYPE_CHECKING

from experiments.codex_dogfood.case_0012.stage_b import canonical, replay

pytest_plugins = ["experiments.exact_hint_routing.tests.test_behavior"]
if TYPE_CHECKING:
    from experiments.exact_hint_routing.models import ExactHintRoutingView
    from experiments.exact_hint_routing.routing import ExactFrame


def test_exact_frozen_hashes(
    equivalent: tuple[ExactFrame, ExactHintRoutingView, ExactHintRoutingView],
) -> None:
    frame, b, c = equivalent
    stats = b.original_lexical_acquisition.matches[0].document_statistics
    values: tuple[object, ...] = (
        frame,
        b,
        c,
        b.original_lexical_acquisition.index,
        {"a": [stats, stats], "b": {"nested": stats}},
        [None, True, 1, 1.0, -0.0, "é\r\n", {}, []],
    )
    for value in values:
        assert replay.fast_hash(value) == canonical.native_hash(value)
