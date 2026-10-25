# Copyright (c) 2026
# ruff: noqa: ANN401, PLR2004, PT018, TRY003, EM101 -- explicit synthetic assertions
"""Usage identity, windows, conflicts, adoption and missing-count contracts."""

import json
from dataclasses import replace
from itertools import permutations
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


@pytest.mark.parametrize("dimension", ["backend", "provider"])
@pytest.mark.parametrize("alias", ["thread", "invocation", "invocation-only"])
def test_provider_local_aliases_do_not_exclude_other_providers(
    tmp_path: Path,
    dimension: str,
    alias: str,
) -> None:
    """Public reports and persisted rows keep names local to both discriminators."""
    original = observation()
    rows: tuple[UsageObservation, ...]
    other = (
        replace(original, backend="other")
        if dimension == "backend"
        else replace(original, provider="other")
    )
    if alias == "thread":
        rows = (original, replace(original, turn_id=None, source_digest="alias"))
        other = replace(
            other,
            turn_id="other-turn",
            invocation_id="other-invocation",
        )
    else:
        rows = (
            (original,)
            if alias == "invocation"
            else (
                original,
                replace(original, thread_id=None, turn_id=None, source_digest="alias"),
            )
        )
        other = replace(other, thread_id="other-thread")
    alone = report(rows, UsageWindow.rolling(AT))
    assert alone["fresh_invocations"] == 1
    assert alone["tokens"]["input_tokens"] == 10
    for sequence in permutations((*rows, other)):
        path = tmp_path / "provider-ledger.json"
        with writer(path):
            save(path, sequence)
        result = report(load(path), UsageWindow.rolling(AT))
        assert result["conflicting_invocations_excluded"] == 0
        assert result["fresh_invocations"] == 2
        assert result["tokens"]["input_tokens"] == 20
        assert result["tokens"]["output_tokens"] == 8


@pytest.mark.parametrize("granularity", ["TURN", "RESPONSE"])
def test_partial_copies_preserve_all_known_fields_in_any_order(
    tmp_path: Path,
    granularity: str,
) -> None:
    """Independent literal expected counts survive duplicate copies and save/load."""
    first = observation(
        granularity=granularity,
        response_id="response" if granularity == "RESPONSE" else None,
        usage=ModelUsage(input_tokens=10),
    )
    second = replace(
        first,
        usage=ModelUsage(output_tokens=4, reasoning_tokens=2, total_tokens=14),
        source_digest="complement",
    )
    empty = replace(first, usage=ModelUsage(), source_digest="unknown-copy")
    for sequence in permutations((first, second, empty)):
        result = report(sequence, UsageWindow.rolling(AT))
        assert result["tokens"]["input_tokens"] == 10
        assert result["tokens"]["output_tokens"] == 4
        assert result["tokens"]["reasoning_tokens"] == 2
        assert result["unknown_category_observations"]["cached_input_tokens"] == 1
        assert result["conflicting_invocations_excluded"] == 0
        component = reconcile(sequence)[0]
        assert component.consumption[0].usage.total_tokens == 14
        assert component.consumption[0].source == "RECONCILED_USAGE"
        assert set(component.observations) == set(sequence)
        # Derived usage must not claim one original source supplied all fields.
        assert component.consumption[0].source_digest not in {
            r.source_digest for r in sequence
        }
        path = tmp_path / "partial-ledger.json"
        with writer(path):
            save(path, (*sequence, first))
        restored = report(load(path), UsageWindow.rolling(AT))
        assert restored == result


@pytest.mark.parametrize("granularity", ["TURN", "RESPONSE"])
def test_partial_conflicts_cannot_hide_behind_more_complete_row(
    granularity: str,
) -> None:
    """The most complete row is not authority to ignore two other known facts."""
    first = observation(
        granularity=granularity,
        response_id="response" if granularity == "RESPONSE" else None,
        usage=ModelUsage(input_tokens=10, output_tokens=4),
    )
    second = replace(
        first,
        usage=ModelUsage(reasoning_tokens=1),
        source_digest="partial1",
    )
    third = replace(
        first,
        usage=ModelUsage(reasoning_tokens=2),
        source_digest="partial2",
    )
    for sequence in permutations((first, second, third)):
        result = report(sequence, UsageWindow.rolling(AT))
        assert result["conflicting_invocations_excluded"] == 1
        assert result["fresh_invocations"] == 0
        assert (
            result["tokens"]["input_tokens"] == 0
        )  # explicitly excluded, not consumption
        assert reconcile(sequence)[0].conflict


@pytest.mark.parametrize(
    "scenario",
    [
        "decrease-through-unknown",
        "same-time-conflict",
        "missing-time",
        "missing-time-total",
        "same-time-partials",
        "unknown-later-total",
    ],
)
def test_cumulative_snapshot_order_is_explicit(scenario: str) -> None:
    """Only the existing timestamped cumulative contract may supersede counts."""
    first = observation(
        source="LOCAL_CODEX_TURN_SUMMARY",
        usage=ModelUsage(input_tokens=10),
    )
    later = replace(
        first,
        timestamp=AT,
        source_digest="later",
        usage=ModelUsage(input_tokens=20),
    )
    expected_conflict = scenario in {
        "decrease-through-unknown",
        "same-time-conflict",
        "missing-time",
        "missing-time-total",
    }
    rows: tuple[UsageObservation, ...]
    if scenario == "decrease-through-unknown":
        later = replace(later, usage=ModelUsage(input_tokens=5))
        middle = replace(
            first,
            timestamp=Timestamp.from_isoformat("2026-10-14T13:00:00Z"),
            usage=ModelUsage(),
            source_digest="unknown",
        )
        rows = (first, middle, later)
    elif scenario == "same-time-conflict":
        rows = (first, replace(later, timestamp=first.timestamp))
    elif scenario == "missing-time":
        rows = (first, replace(later, timestamp=None))
    elif scenario == "missing-time-total":
        rows = (
            replace(first, usage=ModelUsage(total_tokens=14)),
            replace(later, timestamp=None, usage=ModelUsage(total_tokens=15)),
        )
    elif scenario == "same-time-partials":
        rows = (
            first,
            replace(
                later,
                timestamp=first.timestamp,
                usage=ModelUsage(output_tokens=4),
            ),
        )
    else:
        rows = (first, replace(later, usage=ModelUsage()))
    for sequence in permutations(rows):
        component = reconcile(sequence)[0]
        assert component.conflict is expected_conflict
        result = report(
            sequence,
            UsageWindow.rolling(Timestamp.from_isoformat("2026-10-15T19:00:00Z")),
        )
        assert result["conflicting_invocations_excluded"] == int(
            expected_conflict
            and scenario not in {"missing-time", "missing-time-total"},
        )
        if scenario in {"missing-time", "missing-time-total"}:
            assert result["unallocated_timestamp_observations"] == 1
        if scenario == "same-time-partials":
            assert result["tokens"]["input_tokens"] == 10
            assert result["tokens"]["output_tokens"] == 4
        if scenario == "unknown-later-total":
            # The old historical count is retained, but is not guessed as the
            # current value of a later cumulative measurement at another time.
            assert component.observations[0].usage.input_tokens in {10, None}
            assert component.consumption[0].usage.input_tokens is None
            assert result["unknown_category_observations"]["input_tokens"] == 1


@pytest.mark.parametrize(
    "kind",
    ["known-conflict", "unknown-model", "reported-total", "source-fallback"],
)
def test_response_identity_and_conflicts_remain_supported(kind: str) -> None:
    """Distinct source support and model/total conflicts are not summable copies."""
    first = observation(
        granularity="RESPONSE",
        response_id="same",
        usage=ModelUsage(input_tokens=10, output_tokens=4, total_tokens=14),
    )
    second = replace(first, source_digest="other-copy")
    if kind == "known-conflict":
        second = replace(second, model="other-model")
    elif kind == "unknown-model":
        second = replace(second, model="UNKNOWN")
    elif kind == "reported-total":
        second = replace(
            second,
            usage=ModelUsage(input_tokens=10, output_tokens=4, total_tokens=15),
        )
    else:
        first = replace(first, response_id=None, source_digest="same-capture")
        second = replace(first)
    for sequence in permutations((first, second)):
        result = report(sequence, UsageWindow.rolling(AT))
        assert result["conflicting_invocations_excluded"] == int(
            kind in {"known-conflict", "reported-total"},
        )
        if kind in {"source-fallback", "unknown-model"}:
            assert result["fresh_invocations"] == 1
            assert result["tokens"]["input_tokens"] == 10


def test_incomplete_response_slices_do_not_gain_unallocated_turn_counts() -> None:
    """A complete aggregate cannot assign missing counts to individual responses."""
    total = observation(usage=ModelUsage(input_tokens=10))
    first = replace(
        total,
        granularity="RESPONSE",
        response_id="one",
        usage=ModelUsage(input_tokens=5),
    )
    second = replace(first, response_id="two", usage=ModelUsage())
    result = report((first, second, total), UsageWindow.rolling(AT))
    assert result["tokens"]["input_tokens"] == 5
    assert result["unknown_category_observations"]["input_tokens"] == 1
    assert result["fresh_invocations"] == 1
    assert result["conflicting_invocations_excluded"] == 0
