# Copyright (c) 2026
# ruff: noqa: ANN401, S101, PLR2004, PT018, E501 -- explicit synthetic admission fixtures
"""No-launch usage admission, reservations and original adoption attribution."""

from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Barrier
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction.usage import ModelUsage
from devtools.observability.usage import Attribution, Purpose
from devtools.observability.usage.ingestion import from_capture
from devtools.observability.usage.storage import load, writer
from devtools.observability.usage.storage import save as save_observations
from experiments.codex_dogfood.case_0009.artifacts import ROOT
from experiments.orchestration import usage_budget
from experiments.orchestration.controller import Controller
from experiments.orchestration.pipeline import usage
from experiments.orchestration.storage import load as read
from experiments.orchestration.storage import save
from experiments.orchestration.workers import accounting, measurement


def plan() -> Any:
    """Build an explicit synthetic two-call authority-independent inventory."""
    return {
        "usage_budget": {
            "fresh_call_limit": 2,
            "model_call_limits": {"fake": 2},
            "calls": {
                case + "/C": {"model": "fake", "input_upper": 100, "output_upper": 20}
                for case in ("one", "two")
            },
        },
    }


def capture() -> Any:
    """Build a native completed synthetic turn without a model/process."""
    raw = b'{"type":"thread.started","thread_id":"synthetic"}\n{"type":"turn.completed","usage":{"input_tokens":10,"cached_input_tokens":2,"cache_write_input_tokens":0,"output_tokens":4,"reasoning_output_tokens":1}}\n'
    return measurement.capture(
        {"model_id": "fake", "reasoning": "High"},
        "one",
        "original",
        b"synthetic",
        SimpleNamespace(stdout=raw, duration=Duration.seconds(1)),
        b"{}",
        validated=True,
        failure=None,
    )


def test_pipeline_fresh_and_adopted_accounting(tmp_path: Path) -> None:
    """Project original and reused evidence without charging the reuse twice."""
    started = str(Timestamp.now())
    original = from_capture(
        capture(),
        timestamp=Timestamp.now(),
        source="SYNTHETIC",
        source_digest="original",
        attribution=Attribution("devtools", Purpose.SCIENCE, "previous", "one", "B"),
    )
    fresh = replace(
        original,
        invocation_id="fresh",
        thread_id="fresh-thread",
        attribution=Attribution("project", Purpose.SCIENCE, "current"),
    )
    save_observations(tmp_path / ".local/usage/ledger.json", (original, fresh))
    usage_budget.adoption(
        tmp_path,
        "current",
        "one",
        accounting.accept(capture(), "SYNTHETIC"),
        "previous",
    )
    result = usage({"target": str(tmp_path), "run_id": "current", "started": started})
    assert result["experiment"]["fresh_invocations"] == 1
    assert result["experiment"]["adopted_dependencies"] == 1
    assert result["experiment"]["tokens"]["input_tokens"] == 10
    assert result["experiment"]["tokens"]["cached_input_tokens"] == 2
    assert result["experiment"]["tokens"]["output_tokens"] == 4
    assert result["experiment"]["tokens"]["reasoning_tokens"] == 1
    assert result["local"]["fresh_invocations"] == 2


def test_reservation_authority_and_no_retry(tmp_path: Path) -> None:
    """Budget permission alone cannot enter science, repeat or expand a plan."""
    assert (
        usage_budget.reserve(tmp_path, {}, "run", "one", "C", authorized=False) is None
    )
    with pytest.raises(ValueError, match="authority"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=False)
    assert (
        usage_budget.reserve(tmp_path, plan(), "run", "one", "prepare", authorized=True)
        is None
    )
    result = usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)
    assert result["weekly_limits"] == "UNSET"
    assert usage_budget.verify(tmp_path, "run", "one", "C") == result
    with pytest.raises(ValueError, match="already reserved"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)
    usage_budget.capture(tmp_path, "run", "one", "C", tmp_path / "absent.json")
    with pytest.raises(ValueError, match="cannot be repeated"):
        usage_budget.verify(tmp_path, "run", "one", "C")
    unknown = load(tmp_path / ".local/usage/ledger.json")[0]
    assert unknown.usage.input_tokens is None
    usage_budget.reserve(tmp_path, plan(), "run", "two", "C", authorized=True)
    larger = plan()
    larger["usage_budget"]["calls"]["three/C"] = {
        "model": "fake",
        "input_upper": 0,
        "output_upper": 0,
    }
    with pytest.raises(ValueError, match="fresh-call"):
        usage_budget.reserve(tmp_path, larger, "run", "three", "C", authorized=True)


def test_capture_and_adoption_once(tmp_path: Path) -> None:
    """Original usage survives failure/adoption without a new model invocation."""
    usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)
    path = tmp_path / "measurement.json"
    save(path, capture())
    usage_budget.capture(
        tmp_path,
        "run",
        "one",
        "C",
        path,
        accepted=False,
        failure_class="SYNTHETIC_REJECTION",
    )
    rows = load(tmp_path / ".local/usage/ledger.json")
    assert (
        rows[0].usage.input_tokens == 10
        and rows[0].failure_class == "SYNTHETIC_REJECTION"
    )
    with pytest.raises(ValueError, match="cannot be repeated"):
        usage_budget.verify(tmp_path, "run", "one", "C")
    original = accounting.accept(capture(), "SYNTHETIC")
    usage_budget.adoption(tmp_path, "next", "one", original, "run")
    adopted = next(
        r
        for r in load(tmp_path / ".local/usage/ledger.json")
        if r.execution_origin == "ADOPTED"
    )
    assert adopted.original_timestamp == rows[0].timestamp
    assert adopted.usage == rows[0].usage and adopted.invocation_id == "original"


def test_configured_weekly_block_prelaunch(tmp_path: Path) -> None:
    """Configured observed limits require fresh metadata and block before entry."""
    local = tmp_path / ".local/usage"
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 0,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    save_observations(local / "ledger.json", ())
    with pytest.raises(ValueError, match="BUDGET_BLOCKED"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)
    assert not (local / "reservations.json").exists()
    save(local / "backfill.json", {"observed_at": "2000-01-01T00:00:00Z"})
    with pytest.raises(ValueError, match="refresh"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)


def test_unrelated_model_budget_is_not_charged(tmp_path: Path) -> None:
    """An unrelated rule adds no constraint when another rule covers the call."""
    local = tmp_path / ".local/usage"
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "PROJECT",
                    "identity": "devtools",
                    "limits": {
                        "fresh_calls": 2,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "model": "different-model",
                    "limits": {"fresh_calls": 0, "input_tokens": 0, "output_tokens": 0},
                },
            ],
        },
    )
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    save_observations(local / "ledger.json", ())
    assert (
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)[
            "status"
        ]
        == "BUDGET_RESERVED"
    )


def test_unknown_observation_time_blocks_configured_window(tmp_path: Path) -> None:
    """Unknown allocation cannot silently become zero consumed this week."""
    local = tmp_path / ".local/usage"
    observed = from_capture(
        capture(),
        timestamp=None,
        source="SYNTHETIC",
        source_digest="unknown-time",
    )
    save_observations(local / "ledger.json", (observed,))
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 100,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    with pytest.raises(ValueError, match="UNKNOWN"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)


def test_frozen_profile_and_economics_cannot_be_retuned_in_plan() -> None:
    """Plan admission authenticates the whole launcher and numeric contract."""
    frozen = {
        "model_id": "fake",
        "reasoning": "High",
        "argv": ["frozen-entry", "{stage_a_checkpoint}"],
    }
    value: dict[str, Any] = {
        "usage_budget": {"fresh_call_limit": 4},
        "economics": {"fresh_calls": 4},
        "semantic": {**frozen, "argv": ["frozen-entry", "checkpoint"]},
        "stage_a": {"checkpoint": "checkpoint"},
    }
    protocol = {
        "usage_budget": value["usage_budget"],
        "economics": value["economics"],
        "semantic_execution": frozen,
    }
    controller: Any = SimpleNamespace(value=value)
    Controller.authenticate_usage_protocol(controller, protocol)
    value["semantic"]["argv"] = ["hidden-extra-model-stages", "checkpoint"]
    with pytest.raises(ValueError, match="launcher"):
        Controller.authenticate_usage_protocol(controller, protocol)
    with pytest.raises(ValueError, match="economics"):
        Controller.authenticate_usage_protocol(
            controller,
            {**protocol, "economics": {}},
        )
    legacy: Any = SimpleNamespace(value={})
    Controller.authenticate_usage_protocol(legacy, {})


def test_preview_is_read_only_and_assesses_whole_inventory(tmp_path: Path) -> None:
    """Combined forecast, existing consumption and reservations share admission."""
    local = tmp_path / ".local/usage"
    value = {**plan(), "economics": {"fresh_calls": 2}}
    assert usage_budget.preview(tmp_path, {}, "run")["status"] == "UNAVAILABLE"
    assert usage_budget.preview(tmp_path, value, "run")["status"] == "UNSET"
    assert not local.exists()
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 2,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    assert usage_budget.preview(tmp_path, value, "run")["status"] == "UNAVAILABLE"
    save_observations(local / "ledger.json", ())
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    before = {p.name: p.read_bytes() for p in local.iterdir()}
    result = usage_budget.preview(tmp_path, value, "run")
    assert result["status"] == "BUDGET_CHECK_PASS" and not result["reservation_created"]
    assert before == {p.name: p.read_bytes() for p in local.iterdir()}
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 1,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    with pytest.raises(ValueError, match="EXCEEDED"):
        usage_budget.preview(tmp_path, value, "run")
    assert not (local / "reservations.json").exists()
    usage_budget.reserve(tmp_path, value, "run", "one", "C", authorized=True)
    with pytest.raises(ValueError, match="reconciliation"):
        usage_budget.preview(tmp_path, value, "run")


def test_strict_reservation_and_terminal_consumption(tmp_path: Path) -> None:
    """Execution cannot lose configured admission; closeout shares the same rules."""
    local = tmp_path / ".local/usage"
    assert usage_budget.consumption(tmp_path, plan(), "run")["status"] == "UNAVAILABLE"
    with pytest.raises(ValueError, match="ledger required"):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    save_observations(local / "ledger.json", ())
    with pytest.raises(ValueError, match="configured policy"):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    assert (
        usage_budget.consumption(tmp_path, plan(), "run")["status"]
        == "UNAVAILABLE_OR_BLOCKED"
    )
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 0,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    row = from_capture(
        capture(),
        timestamp=Timestamp.now(),
        source="SYNTHETIC",
        source_digest="synthetic",
    )
    save_observations(local / "ledger.json", (row,))
    blocked = usage_budget.consumption(tmp_path, plan(), "run")
    assert blocked["status"] == "UNAVAILABLE_OR_BLOCKED"
    assert "EXCEEDED" in blocked["decisions"]["one/C"]["reason"]
    save(
        local / "policy.json",
        {
            "limits": [
                {
                    "scope": "OBSERVED_WINDOW",
                    "identity": "local",
                    "limits": {
                        "fresh_calls": 10,
                        "input_tokens": None,
                        "output_tokens": None,
                    },
                },
            ],
        },
    )
    assert (
        usage_budget.consumption(tmp_path, plan(), "run")["status"]
        == "BUDGET_CHECK_PASS"
    )


def configured(root: Path, rules: list[Any]) -> None:
    """Install an isolated numeric policy with a fresh empty observation set."""
    local = root / ".local/usage"
    save(local / "policy.json", {"limits": rules})
    save(local / "backfill.json", {"observed_at": str(Timestamp.now())})
    save_observations(local / "ledger.json", ())


def rule(scope: str = "EXPERIMENT", identity: str = "run", **selectors: Any) -> Any:
    """Name real canonical scopes; no alternative policy assessment."""
    limits = selectors.pop(
        "limits",
        {"fresh_calls": 2, "input_tokens": 200, "output_tokens": 40},
    )
    return {
        "scope": scope,
        "identity": identity,
        "limits": {
            "fresh_calls": None,
            "input_tokens": None,
            "output_tokens": None,
            **limits,
        },
        **selectors,
    }


@pytest.mark.parametrize(
    "rules",
    [
        [rule(identity="unrelated")],
        [rule(model="another-model")],
        [rule(scope="STAGE", identity="B")],
        [rule(scope="PROJECT", identity="another-project")],
        [
            rule(
                limits={
                    "fresh_calls": None,
                    "input_tokens": None,
                    "output_tokens": None,
                },
            ),
        ],
    ],
)
def test_inapplicable_policy_blocks_all_assessments(tmp_path: Path, rules: Any) -> None:
    """Policy presence cannot admit an uncovered invocation through any seam."""
    configured(tmp_path, rules)
    value = {**plan(), "economics": {}}
    with pytest.raises(ValueError, match="no applicable numeric policy"):
        usage_budget.preview(tmp_path, value, "run")
    with pytest.raises(ValueError, match="no applicable numeric policy"):
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    result = usage_budget.consumption(tmp_path, value, "run")
    assert result["status"] == "UNAVAILABLE_OR_BLOCKED"
    assert all("no applicable" in v["reason"] for v in result["decisions"].values())
    assert not (tmp_path / ".local/usage/reservations.json").exists()


@pytest.mark.parametrize(
    ("scope", "identity"),
    [
        ("PROJECT", "devtools"),
        ("STAGE", "C"),
        ("OBSERVED_WINDOW", "local"),
        ("EXPERIMENT", "run"),
    ],
)
def test_applicable_broader_scopes_and_preview_agree(
    tmp_path: Path,
    scope: str,
    identity: str,
) -> None:
    """Existing broader scopes remain usable, with identical real admission."""
    configured(tmp_path, [rule(scope, identity)])
    value = {**plan(), "economics": {}}
    before = {p.name: p.read_bytes() for p in (tmp_path / ".local/usage").iterdir()}
    assert usage_budget.preview(tmp_path, value, "run")["status"] == "BUDGET_CHECK_PASS"
    assert before == {
        p.name: p.read_bytes() for p in (tmp_path / ".local/usage").iterdir()
    }
    for case in ("one", "two"):
        assert (
            usage_budget.reserve(
                tmp_path,
                value,
                "run",
                case,
                "C",
                authorized=True,
                require_configured=True,
            )["status"]
            == "BUDGET_RESERVED"
        )
    with pytest.raises(ValueError, match="already reserved"):
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    assert (
        usage_budget.consumption(tmp_path, value, "run")["status"]
        == "BUDGET_CHECK_PASS"
    )


def test_frozen_four_call_population_and_partial_coverage(tmp_path: Path) -> None:
    """Real frozen inventory covers B/Sol and C/Astra without reserving live calls."""
    value = read(
        ROOT
        / "experiments/source_grounding/plans/candidate-discrimination-pipeline-run-plan.json",
    )
    calls = value["usage_budget"]["calls"]
    assert set(calls) == {"0024/B", "0022/C", "0023/C", "0024/C"}
    assert calls["0024/B"]["model"] == "gpt-6-sol"
    assert {calls[key]["model"] for key in calls if key.endswith("/C")} == {
        "gpt-6-astra",
    }
    exact = rule(
        limits={"fresh_calls": 4, "input_tokens": 1756679, "output_tokens": 191923},
    )
    configured(tmp_path, [exact])
    assert usage_budget.preview(tmp_path, value, "run")["status"] == "BUDGET_CHECK_PASS"
    with pytest.raises(ValueError, match="no applicable"):
        usage_budget.preview(tmp_path, value, "unrelated")
    for selector in (
        {"model": "gpt-6-sol"},
        {"model": "gpt-6-astra"},
        {"scope": "STAGE", "identity": "B"},
    ):
        configured(tmp_path, [{**exact, **selector}])
        with pytest.raises(ValueError, match="no applicable"):
            usage_budget.preview(tmp_path, value, "run")
    configured(tmp_path, [exact])
    for key in calls:
        case, stage = key.split("/")
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            case,
            stage,
            authorized=True,
            require_configured=True,
        )
    assert len(read(tmp_path / ".local/usage/reservations.json")["calls"]) == 4
    assert (
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            "0022",
            "B",
            authorized=True,
            require_configured=True,
        )
        is None
    )
    assert (
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            "0023",
            "B",
            authorized=True,
            require_configured=True,
        )
        is None
    )
    expanded = read(
        ROOT
        / "experiments/source_grounding/plans/candidate-discrimination-pipeline-run-plan.json",
    )
    expanded["usage_budget"]["calls"]["extra/C"] = calls["0022/C"]
    with pytest.raises(ValueError, match="fresh-call limit"):
        usage_budget.reserve(
            tmp_path,
            expanded,
            "run",
            "extra",
            "C",
            authorized=True,
            require_configured=True,
        )


def test_every_matching_rule_and_pending_reservation_count(tmp_path: Path) -> None:
    """A permissive exact rule cannot override a stricter matching rule."""
    configured(
        tmp_path,
        [rule(), rule("PROJECT", "devtools", limits={"fresh_calls": 1})],
    )
    value = {**plan(), "economics": {}}
    with pytest.raises(ValueError, match="EXCEEDED"):
        usage_budget.preview(tmp_path, value, "run")
    usage_budget.reserve(
        tmp_path,
        value,
        "run",
        "one",
        "C",
        authorized=True,
        require_configured=True,
    )
    with pytest.raises(ValueError, match="EXCEEDED"):
        usage_budget.reserve(
            tmp_path,
            value,
            "run",
            "two",
            "C",
            authorized=True,
            require_configured=True,
        )


@pytest.mark.parametrize(
    "defect",
    ["ledger", "baseline", "stale", "unknown", "conflict", "attribution_conflict"],
)
def test_required_accounting_fails_closed(tmp_path: Path, defect: str) -> None:
    """Real reservation admission refuses absent, unknown or conflicting evidence."""
    configured(tmp_path, [rule()])
    local = tmp_path / ".local/usage"
    row = from_capture(
        capture(),
        timestamp=Timestamp.now(),
        source="SYNTHETIC",
        source_digest="one",
        attribution=Attribution("devtools", Purpose.SCIENCE, "run", "one", "C"),
    )
    if defect == "ledger":
        (local / "ledger.json").unlink()
    elif defect == "baseline":
        (local / "backfill.json").unlink()
    elif defect == "stale":
        save(local / "backfill.json", {"observed_at": "2000-01-01T00:00:00Z"})
    elif defect == "unknown":
        save_observations(local / "ledger.json", (replace(row, usage=ModelUsage()),))
    elif defect == "attribution_conflict":
        save_observations(
            local / "ledger.json",
            (
                row,
                replace(
                    row,
                    source_digest="conflict",
                    attribution=Attribution(
                        "devtools",
                        Purpose.SCIENCE,
                        "another-run",
                        "one",
                        "C",
                    ),
                ),
            ),
        )
    else:
        save_observations(
            local / "ledger.json",
            (
                row,
                replace(
                    row,
                    source_digest="conflict",
                    usage=ModelUsage(input_tokens=11, output_tokens=4),
                ),
            ),
        )
    with pytest.raises((ValueError, OSError)):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    assert not (local / "reservations.json").exists()


def test_adoption_and_overlapping_categories_are_not_charged_twice(
    tmp_path: Path,
) -> None:
    """Input/output limits include their cached/reasoning subsets exactly once."""
    configured(
        tmp_path,
        [rule(limits={"fresh_calls": 2, "input_tokens": 110, "output_tokens": 24})],
    )
    local = tmp_path / ".local/usage"
    row = from_capture(
        capture(),
        timestamp=Timestamp.now(),
        source="SYNTHETIC",
        source_digest="one",
        attribution=Attribution("devtools", Purpose.SCIENCE, "prior", "one", "B"),
    )
    fresh = replace(
        row,
        invocation_id="fresh",
        thread_id="fresh-thread",
        attribution=Attribution("devtools", Purpose.SCIENCE, "run", "one", "B"),
    )
    save_observations(local / "ledger.json", (row, fresh))
    usage_budget.adoption(
        tmp_path,
        "run",
        "one",
        accounting.accept(capture(), "SYNTHETIC"),
        "prior",
    )
    usage_budget.reserve(
        tmp_path,
        plan(),
        "run",
        "one",
        "C",
        authorized=True,
        require_configured=True,
    )
    assert (
        usage_budget.consumption(tmp_path, plan(), "run")["status"]
        == "BUDGET_CHECK_PASS"
    )


def test_uncertain_outcome_blocks_consumption_and_retry(tmp_path: Path) -> None:
    """Unknown usage is not zero; the existing invocation stays non-repeatable."""
    configured(tmp_path, [rule()])
    usage_budget.reserve(
        tmp_path,
        plan(),
        "run",
        "one",
        "C",
        authorized=True,
        require_configured=True,
    )
    usage_budget.capture(tmp_path, "run", "one", "C", tmp_path / "absent.json")
    with pytest.raises(ValueError, match="already reserved"):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
    with pytest.raises(ValueError, match="UNKNOWN"):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "two",
            "C",
            authorized=True,
            require_configured=True,
        )
    assert (
        usage_budget.consumption(tmp_path, plan(), "run")["status"]
        == "UNAVAILABLE_OR_BLOCKED"
    )


def test_competing_admissions_use_existing_writer_lease(tmp_path: Path) -> None:
    """Concurrent attempts cannot oversubscribe or bypass an active writer lease."""
    configured(tmp_path, [rule(limits={"fresh_calls": 1})])
    ledger = tmp_path / ".local/usage/ledger.json"
    start = Barrier(2)

    def attempt(case: str) -> str:
        start.wait(timeout=5)
        try:
            usage_budget.reserve(
                tmp_path,
                plan(),
                "run",
                case,
                "C",
                authorized=True,
                require_configured=True,
            )
        except FileExistsError:
            return "CONTENDED"
        except ValueError as error:
            return str(error)
        return "RESERVED"

    with ThreadPoolExecutor(max_workers=2) as executor:
        outcomes = list(executor.map(attempt, ("one", "two")))
    assert outcomes.count("RESERVED") == 1
    assert any(value == "CONTENDED" or "EXCEEDED" in value for value in outcomes)
    assert len(read(ledger.parent / "reservations.json")["calls"]) == 1
    assert not ledger.with_suffix(".writer").exists()
    with writer(ledger), pytest.raises(FileExistsError):
        usage_budget.reserve(
            tmp_path,
            plan(),
            "run",
            "one",
            "C",
            authorized=True,
            require_configured=True,
        )
