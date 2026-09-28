# Copyright (c) 2026
# ruff: noqa: D103, PLR2004
"""Probability sample integrity before outcome joins."""

from __future__ import annotations

from experiments.increment_27.depth_diagnostic import sha256_file
from experiments.increment_30.mechanics import _verified_json
from experiments.increment_32.mechanics import ROOT
from experiments.increment_32.sampling import (
    FREEZE_NAME,
    SAMPLED_INPUT_NAME,
    SOURCE_IDENTITY,
    SOURCE_SHA256,
    build_sample,
)


def test_frozen_simple_random_sample_is_exact_and_neutral() -> None:
    freeze = _verified_json(ROOT / FREEZE_NAME)
    blind = _verified_json(ROOT / SAMPLED_INPUT_NAME)
    assert (freeze, blind) == build_sample(ROOT)
    payload = freeze["payload"]
    assert payload["source_neutral_input_content_identity"] == SOURCE_IDENTITY
    assert payload["source_neutral_input_sha256"] == SOURCE_SHA256
    assert payload["population_size"] == 702
    assert payload["sample_size"] == 128
    assert payload["seed"] == 320128
    assert payload["sampling_method"] == "simple-random-sampling-without-replacement"
    assert payload["outcomes_accessed_before_freeze"] is False
    selected = {tuple(row) for row in payload["sampled_neutral_identities"]}
    unsampled = {tuple(row) for row in payload["unsampled_neutral_identities"]}
    assert len(selected) == 128
    assert len(unsampled) == 574
    assert not selected & unsampled
    actual = {
        (case["neutral_case_id"], row["neutral_resource_id"])
        for case in blind["payload"]["cases"]
        for row in case["resources"]
    }
    assert actual == selected
    assert payload["sampled_input_content_identity"] == blind["content_identity"]
    assert (
        sha256_file(ROOT / FREEZE_NAME)
        == "1b1b113a17939a5cadfbe731c4282d756b5835422de99845207e06789e03d00d"
    )
    assert (
        sha256_file(ROOT / SAMPLED_INPUT_NAME)
        == "dc922555365307e8146c00ae5bda2c646372badbc45574dbbd30c707d4190949"
    )
    for case in blind["payload"]["cases"]:
        assert set(case) == {
            "neutral_case_id",
            "information_need",
            "parent_snapshot_sha",
            "resources",
        }
        for row in case["resources"]:
            assert set(row) == {"neutral_resource_id", "address", "content"}
