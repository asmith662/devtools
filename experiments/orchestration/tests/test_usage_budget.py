# Copyright (c) 2026
# ruff: noqa: ANN401, S101, PLR2004, PT018, E501 -- explicit synthetic admission fixtures
"""No-launch usage admission, reservations and original adoption attribution."""

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.observability.usage.ingestion import from_capture
from devtools.observability.usage.storage import load
from devtools.observability.usage.storage import save as save_observations
from experiments.orchestration import usage_budget
from experiments.orchestration.controller import Controller
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
    with pytest.raises(ValueError, match="BUDGET_BLOCKED"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)
    assert not (local / "reservations.json").exists()
    save(local / "backfill.json", {"observed_at": "2000-01-01T00:00:00Z"})
    with pytest.raises(ValueError, match="refresh"):
        usage_budget.reserve(tmp_path, plan(), "run", "one", "C", authorized=True)


def test_unrelated_model_budget_is_not_charged(tmp_path: Path) -> None:
    """A model-specific zero limit cannot accidentally block another model."""
    local = tmp_path / ".local/usage"
    save(
        local / "policy.json",
        {
            "limits": [
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
