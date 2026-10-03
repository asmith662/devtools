# Copyright (c) 2026
# ruff: noqa: ANN001, ANN201, D103, INP001, S101, PLR2004
"""Focused independent checks for the frozen Case 0005 Stage D join."""

import json
import subprocess
import sys
from pathlib import Path

import analyze
import pytest


@pytest.fixture(scope="module")
def joined():
    """Read the pinned frozen artifacts once without any production operation."""
    return analyze.load(), analyze.analyze(analyze.load())


def test_checkpoint_and_join_invariants(joined):
    items, report = joined
    assert report["join_integrity"]["frame"]["observed"] == 515
    assert report["join_integrity"]["obligations"]["observed"] == 9
    assert report["join_integrity"]["queries_and_preferences"]["observed"] == 9
    assert report["join_integrity"]["judgments"]["observed"] == 4635
    assert report["join_integrity"]["routed_candidate_loss"] == 0
    assert report["join_integrity"]["global_lane_unchanged"]
    assert report["required"]["unit_occurrences"] == 27
    assert report["required"]["distinct_units"] == 25
    assert report["required"]["witness_universe_unique_resources"] == 24
    assert set(items["hashes"]) == set(analyze.PINNED)


def test_alternative_completion_is_conjunctive_and_surface_specific(joined):
    items, report = joined
    units = {
        u["identity"]: u["resource_identity"]["address"]
        for u in items["adjudication/judgments.json"]["information_units"]
    }
    global_positions = {
        m["resource_address"]: m["native_rank"]
        for m in items["retrieval.json"]["lanes"][0]["matches"]
    }
    for obligation in report["own_lanes"]["obligations"]:
        oid = obligation["identity"]
        native_lane = next(
            x
            for x in items["retrieval.json"]["lanes"]
            if x["obligation_identity"] == oid
        )
        routed_lane = next(
            x for x in items["routing.json"]["lanes"] if x["obligation_identity"] == oid
        )
        native = {
            m["resource_address"]: m["native_rank"] for m in native_lane["matches"]
        }
        routed = {
            m["resource_address"]: m["routed_position"]
            for m in routed_lane["candidates"]
        }
        for alt in obligation["alternatives"]:
            targets = {units[unit] for unit in alt["units"]}
            assert targets == set(alt["resources"])
            for surface, positions in (
                ("global", global_positions),
                ("native", native),
                ("routed", routed),
            ):
                expected = max(positions.get(a) or float("inf") for a in targets)
                actual = alt["completion"][surface]
                assert actual == (None if expected == float("inf") else expected)
        for surface in ("global", "native", "routed"):
            finite = [
                a["completion"][surface]
                for a in obligation["alternatives"]
                if a["completion"][surface] is not None
            ]
            assert obligation["best_completion"][surface] == min(finite)


def test_prefix_union_and_labels_are_recomputed_from_actual_candidates(joined):
    items, report = joined
    labels = {
        (c["obligation_identity"], c["resource_identity"]["address"]): c["judgment"]
        for c in items["adjudication/judgments.json"]["resource_obligation_judgments"]
    }
    for surface in ("native", "routed"):
        union = set()
        occurrences = 0
        counts = dict.fromkeys(analyze.LABELS, 0)
        source = (
            items["retrieval.json"]["lanes"][1:]
            if surface == "native"
            else items["routing.json"]["lanes"]
        )
        for lane, obligation in zip(
            source, report["own_lanes"]["obligations"], strict=True
        ):
            candidates = lane["matches"] if surface == "native" else lane["candidates"]
            field = "native_rank" if surface == "native" else "routed_position"
            depth = obligation["best_completion"][surface]
            selected = [c for c in candidates if c[field] <= depth]
            addresses = {c["resource_address"] for c in selected}
            union |= addresses
            occurrences += len(selected)
            assert addresses == set(obligation[f"{surface}_prefix"]["resources"])
            for candidate in selected:
                counts[
                    labels[obligation["identity"], candidate["resource_address"]]
                ] += 1
        assert len(union) == report["review_surface"][f"{surface}_unique_resources"]
        assert occurrences == report["review_surface"][f"{surface}_summed_occurrences"]
        assert counts == report["review_surface"]["prefix_label_totals"][surface]


def test_empty_preference_preserves_every_rank(joined):
    items, report = joined
    validation = next(
        x for x in report["own_lanes"]["obligations"] if x["identity"] == "validation"
    )
    native = next(
        x
        for x in items["retrieval.json"]["lanes"]
        if x["obligation_identity"] == "validation"
    )
    routed = next(
        x
        for x in items["routing.json"]["lanes"]
        if x["obligation_identity"] == "validation"
    )
    assert routed["preferred_roles"] == []
    assert [x["resource_address"] for x in native["matches"]] == [
        x["resource_address"] for x in routed["candidates"]
    ]
    assert all(x["native_rank"] == x["routed_position"] for x in routed["candidates"])
    assert (
        validation["best_completion"]["native"]
        == validation["best_completion"]["routed"]
    )


def test_rendered_artifacts_replay_and_correspond(joined):
    _items, report = joined
    json_bytes = analyze.output_json(report)
    md_bytes = analyze.markdown(report)
    assert analyze.output_json(json.loads(json_bytes)) == json_bytes
    assert (analyze.CASE / "analysis.json").read_bytes() == json_bytes
    assert (analyze.CASE / "analysis.md").read_bytes() == md_bytes
    markdown = md_bytes.decode()
    for item in report["own_lanes"]["obligations"]:
        b = item["best_completion"]
        assert (
            f"| {item['identity']} | {b['global']} | {b['native']} | {b['routed']} |"
        ) in markdown
    surface = report["review_surface"]
    assert (
        f"{surface['native_summed_occurrences']} occurrences / "
        f"{surface['native_unique_resources']} unique resources"
    ) in markdown
    assert (
        f"{surface['routed_summed_occurrences']} occurrences / "
        f"{surface['routed_unique_resources']} unique resources"
    ) in markdown


def test_frozen_hash_failure_and_overwrite_refusal(monkeypatch):
    altered = {**analyze.PINNED, "routing.json": "0" * 64}
    monkeypatch.setattr(analyze, "PINNED", altered)
    with pytest.raises(AssertionError, match=r"routing\.json"):
        analyze.verify_frozen()
    monkeypatch.undo()
    before = {
        name: analyze.sha((analyze.CASE / name).read_bytes()) for name in analyze.PINNED
    }
    completed = subprocess.run(  # noqa: S603 -- fixed local analyzer invocation
        [sys.executable, str(Path(analyze.__file__)), "--write"],
        cwd=analyze.ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode != 0
    assert "FileExistsError" in completed.stderr
    assert before == {
        name: analyze.sha((analyze.CASE / name).read_bytes()) for name in analyze.PINNED
    }
