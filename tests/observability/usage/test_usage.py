# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, PT018, TRY003, EM101 -- explicit synthetic assertions
"""Usage identity, windows, conflicts, adoption and missing-count contracts."""

import json
from dataclasses import replace
from pathlib import Path
from typing import Any

import pytest

from devtools.core.time import Timestamp
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.evidence.invocation import ExecutionOrigin
from devtools.observability.usage import (
    Attribution,
    Purpose,
    UsageObservation,
    UsageWindow,
    report,
)
from devtools.observability.usage.collection import incompatible, reconcile, sum_usage
from devtools.observability.usage.storage import load, save, writer

AT = Timestamp.from_isoformat("2026-10-15T18:00:00Z")


def observation(**changes: Any) -> UsageObservation:
    """Build one explicitly synthetic completed invocation observation."""
    base = UsageObservation(
        timestamp=Timestamp.from_isoformat("2026-10-14T12:00:00Z"),
        backend="Codex",
        provider="OpenAI",
        model="fake",
        reasoning_effort="High",
        execution_profile="SEMANTIC_WORKER",
        invocation_id="one",
        thread_id="thread",
        turn_id="turn",
        response_id=None,
        usage=ModelUsage(
            input_tokens=10,
            cached_input_tokens=2,
            cache_write_tokens=0,
            output_tokens=4,
            reasoning_tokens=1,
        ),
        source="DEVTOOLS",
        source_digest="digest",
        completed=True,
        validated=True,
        accepted=True,
        attribution=Attribution("project", Purpose.SCIENCE, "experiment", "case", "C"),
    )
    return replace(base, **changes)


def test_adopted_only_and_mixed_turn() -> None:
    """A retained dependency uses original time; mixed agent turns remain one."""
    row = observation(
        execution_origin=ExecutionOrigin.ADOPTED,
        original_timestamp=Timestamp.from_isoformat("2026-09-01T00:00:00Z"),
        original_attribution=Attribution("project", Purpose.SCIENCE, "original"),
    )
    assert UsageObservation.from_dict(json.loads(json.dumps(row.to_dict()))) == row
    value = report((row,), UsageWindow.rolling(AT), experiment="experiment")
    assert value["fresh_invocations"] == 0 and value["adopted_dependencies"] == 1
    first = observation(response_id="response1", granularity="RESPONSE")
    second = replace(
        first,
        response_id="response2",
        model="other",
        reasoning_effort="Low",
    )
    value = report((first, second), UsageWindow.rolling(AT))
    assert value["fresh_invocations"] == 1
    assert any(
        g["dimension"] == "model" and g["value"] == "MIXED" for g in value["groups"]
    )


def test_rollup_dedup_and_dimensions() -> None:
    """Duplicate receipts are one invocation, with separate token categories."""
    row = observation()
    value = report((row, replace(row, source_digest="copy")), UsageWindow.rolling(AT))
    assert value["fresh_invocations"] == 1
    assert value["tokens"] == {
        "input_tokens": 10,
        "cached_input_tokens": 2,
        "cache_write_tokens": 0,
        "output_tokens": 4,
        "reasoning_tokens": 1,
    }
    assert value["accepted"] == 1
    assert "PARTIAL" in value["coverage"]
    assert {r["dimension"] for r in value["groups"]} == {
        "model",
        "reasoning",
        "purpose",
        "project",
        "experiment",
    }
    assert (
        report((row,), UsageWindow.rolling(AT), experiment="other")["fresh_invocations"]
        == 0
    )


def test_missing_failure_unallocated_and_zero_denominator() -> None:
    """Missing categories and timestamps never become authoritative zero counts."""
    row = observation(
        usage=ModelUsage(),
        accepted=False,
        validated=False,
        failure_class="FAILED",
    )
    value = report(
        (
            row,
            observation(
                invocation_id="unknown",
                thread_id=None,
                turn_id=None,
                timestamp=None,
            ),
        ),
        UsageWindow.rolling(AT),
    )
    assert value["missing_usage_invocations"] == 1
    assert value["unknown_category_observations"]["input_tokens"] == 1
    assert value["failed"] == 1 and value["rejected"] == 0
    assert value["unallocated_timestamp_observations"] == 1
    assert (
        next(g for g in value["groups"] if g["dimension"] == "experiment")[
            "observed_input_percent"
        ]
        is None
    )


def test_conflicting_categories_and_scopes_are_excluded() -> None:
    """No convenient source wins a conflict."""
    row = observation()
    bad = replace(row, usage=ModelUsage(input_tokens=11), source_digest="bad")
    assert (
        report((row, bad), UsageWindow.rolling(AT))["conflicting_invocations_excluded"]
        == 1
    )
    other = replace(row, attribution=Attribution("other"), source_digest="scope")
    assert reconcile((row, other))[0].conflict
    assert not incompatible(ModelUsage(), row.usage)


def test_response_slices_reconcile_turn_and_copies() -> None:
    """Use atomic timestamps for windows; a turn sum is never another charge."""
    aggregate = observation()
    first = replace(
        aggregate,
        granularity="RESPONSE",
        response_id="r1",
        usage=ModelUsage(input_tokens=4, output_tokens=1),
        source_digest="r1",
    )
    second = replace(
        first,
        response_id="r2",
        usage=ModelUsage(input_tokens=6, output_tokens=3),
        source_digest="r2",
    )
    result = reconcile((aggregate, first, second, first))[0]
    assert not result.conflict
    assert len(result.consumption) == 2
    assert sum_usage(tuple(r.usage for r in result.consumption)).input_tokens == 10
    assert (
        report((aggregate, first, second), UsageWindow.rolling(AT))["tokens"][
            "input_tokens"
        ]
        == 10
    )
    assert reconcile(
        (aggregate, replace(first, usage=ModelUsage(input_tokens=11)), second),
    )[0].conflict


def test_turn_aliases_snapshots_and_adoption() -> None:
    """Original usage remains queryable; new-window adopted use has no consumption."""
    old = Timestamp.from_isoformat("2026-09-01T12:00:00Z")
    adopted = observation(
        execution_origin=ExecutionOrigin.ADOPTED,
        original_timestamp=old,
    )
    current = report((adopted,), UsageWindow.rolling(AT))
    assert current["adopted_dependencies"] == 1
    assert current["fresh_invocations"] == 0
    assert (
        report(
            (adopted,),
            UsageWindow.rolling(Timestamp.from_isoformat("2026-09-02T00:00:00Z")),
        )["tokens"]["input_tokens"]
        == 10
    )
    unknown_turn = observation(turn_id=None)
    no_thread = observation(thread_id=None, turn_id=None)
    assert len(reconcile((unknown_turn, no_thread, observation()))) == 1
    assert any(
        c.conflict
        for c in reconcile(
            (
                unknown_turn,
                observation(),
                observation(turn_id="other", invocation_id="other"),
            ),
        )
    )
    assert any(
        c.conflict for c in reconcile((observation(), observation(thread_id="other")))
    )
    snap1 = observation(
        source="LOCAL_CODEX_TURN_SUMMARY",
        usage=ModelUsage(input_tokens=1),
    )
    snap2 = replace(
        snap1,
        timestamp=AT,
        usage=ModelUsage(input_tokens=10),
        source_digest="new",
    )
    assert not reconcile((snap1, snap2, observation()))[0].conflict
    # Unknown invocation identity can still use a provider response identity.
    assert reconcile(
        (
            observation(
                invocation_id=None,
                thread_id=None,
                turn_id=None,
                response_id="response",
            ),
        ),
    )[0].identity.endswith("response:response")


def test_metadata_storage_and_exclusive_writer(tmp_path: Path) -> None:
    """Use canonical filesystem storage and fail closed on writer contention."""
    path = tmp_path / "usage.json"
    assert load(path) == ()
    row = observation()
    with writer(path):
        with pytest.raises(FileExistsError), writer(path):
            pytest.fail("second writer")
        save(path, (row, row))
    assert load(path) == (row,)
    with pytest.raises(RuntimeError), writer(path):
        raise RuntimeError("synthetic writer failure")
    with writer(path):
        pass
    path.write_text('{"schema":"wrong"}')
    with pytest.raises(ValueError, match="schema"):
        load(path)
    path.write_text("[]")
    with pytest.raises(ValueError, match="schema"):
        load(path)


def test_wire_and_identity_validation() -> None:
    """Unknown is explicit; malformed metadata is not silently accepted."""
    row = observation()
    assert UsageObservation.from_dict(json.loads(json.dumps(row.to_dict()))) == row
    unknown = observation(timestamp=None, original_timestamp=None)
    assert (
        UsageObservation.from_dict(json.loads(json.dumps(unknown.to_dict()))) == unknown
    )
    with pytest.raises(ValueError, match="fields"):
        UsageObservation.from_dict({})
    bad = row.to_dict()
    bad["usage"] = []
    with pytest.raises(TypeError, match="Typed"):
        UsageObservation.from_dict(bad)
    with pytest.raises(ValueError, match="identity"):
        observation(invocation_id=None, thread_id=None, response_id=None)
    with pytest.raises(ValueError, match="granularity"):
        observation(granularity="REQUEST_GUESS")


def test_week_boundaries_and_dst() -> None:
    """Calendar week uses local midnight; rolling days always use 24 hours."""
    rolling = UsageWindow.rolling(AT)
    assert (rolling.end.value - rolling.start.value).total_seconds() == 7 * 86400
    assert rolling.contains(rolling.start) and not rolling.contains(rolling.end)
    assert not rolling.contains(None)
    week = UsageWindow.calendar_week(AT, "America/New_York")
    assert str(week.start) == "2026-10-12T04:00:00+00:00"
    previous = UsageWindow.calendar_week(AT, "America/New_York", previous=True)
    assert previous.end == week.start
    dst = UsageWindow.calendar_week(
        Timestamp.from_isoformat("2026-11-01T12:00:00Z"),
        "America/New_York",
    )
    assert (dst.end.value - dst.start.value).total_seconds() == 169 * 3600
    assert (
        UsageWindow.calendar_week(AT, "America/New_York", week_start=6).start
        != week.start
    )
    for bad in (0, -1):
        with pytest.raises(ValueError, match="positive"):
            UsageWindow.rolling(AT, bad)
    with pytest.raises(ValueError, match="Week start"):
        UsageWindow.calendar_week(AT, "UTC", week_start=7)
    with pytest.raises(ValueError, match="exceeds"):
        UsageWindow(AT, rolling.start)
