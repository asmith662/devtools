# Copyright (c) 2026
# ruff: noqa: S101, PLR2004 -- synthetic complete-frame partition fixtures
"""Input and response maxima constrain deterministic address-ordered packing."""

from copy import deepcopy

import pytest

from experiments.source_grounding.chunked.packing import partition
from experiments.source_grounding.chunked.test_archive import coverage, fixture


def test_partition_is_output_aware_and_independent_of_resource_input_order() -> None:
    """Two obligation cells fit; four exceed the unchanged per-cell capacities."""
    packet, _ = fixture()
    other = {
        **packet["resources"][0],
        "address": "another.txt",
        "document_identity": "another-doc",
    }
    packet["resources"].append(other)
    result = partition(packet, coverage(packet))
    assert len(result["batches"]) == 2
    assert all(batch["response_maximum_bytes"] <= 65536 for batch in result["batches"])
    packet["resources"].reverse()
    assert partition(packet, coverage(packet))["batches"] == result["batches"]
    # No treatment/rank structure exists in the accepted full blind packet.
    changed = deepcopy(packet)
    changed["task"] += " additional frozen purpose"
    assert (
        partition(changed, coverage(changed))["partition_sha256"]
        != result["partition_sha256"]
    )


def test_oversized_single_resource_fails_before_any_invocation() -> None:
    """No model or journal is needed to detect an impossible resource batch."""
    packet, _ = fixture()
    packet["resources"][0]["content"] = "x" * 700000
    with pytest.raises(ValueError, match="Single resource"):
        partition(packet)
