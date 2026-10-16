# Copyright (c) 2026
# ruff: noqa: S101, D103, PT018, COM812 -- exact production script startup regression
"""Real direct-script imports from external CWD, never a scientific operation."""

import asyncio
import copy
import sys
from pathlib import Path

import pytest

from experiments.codex_dogfood.case_0009.artifacts import ROOT, digest
from experiments.orchestration import entrypoints
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load


def test_real_entry_script_from_external_cwd() -> None:
    """The exact --help subprocess fails under the old statistics.py layout."""
    script = "experiments/source_grounding/discrimination/entry.py"
    argv = ["{python}", "-B", "{repository}/" + script]
    value = {
        "commands": {"prepare": argv},
        "semantic": {"kind": "process", "argv": argv},
        "implementation": {script: digest((ROOT / script).read_bytes())},
        "worker_entrypoints": {
            "schema": entrypoints.SCHEMA,
            "mode": "DIRECT_SCRIPT_HELP",
            "timeout_seconds": 30,
            "scripts": {script: digest((ROOT / script).read_bytes())},
        },
    }
    receipt = asyncio.run(entrypoints.check(ROOT, value))
    assert receipt["status"] == "PASS"
    process = receipt["scripts"][0]
    assert process["argv"] == [sys.executable, "-B", str(ROOT / script), "--help"]
    assert not Path(process["cwd"]).is_relative_to(ROOT)
    assert process["cwd_unchanged"] and process["exit_code"] == 0


def test_no_stdlib_shadowing_siblings() -> None:
    names = {p.stem for p in Path(__file__).parent.glob("*.py")} - {"__init__"}
    assert not names.intersection(sys.stdlib_module_names)


def test_exact_four_call_inventory_rejects_fifth() -> None:
    plan = load(
        ROOT
        / "experiments/source_grounding/plans/candidate-discrimination-run-plan.json"
    )
    assert set(plan["usage_budget"]["calls"]) == {
        "0022/C",
        "0023/C",
        "0024/C",
        "0024/B",
    }
    assert plan["usage_budget"]["model_call_limits"] == {
        "gpt-6-astra": 3,
        "gpt-6-sol": 1,
    }
    assert set(plan["adopted_branches"]) == {"0022", "0023"}
    assert plan["semantic"]["model_id"] == "gpt-6-astra"
    assert plan["semantic"]["reasoning"] == "High"
    changed = copy.deepcopy(plan)
    changed["usage_budget"]["calls"]["0022/B"] = copy.deepcopy(
        changed["usage_budget"]["calls"]["0024/B"]
    )
    changed["usage_budget"]["fresh_call_limit"] = 5
    changed["usage_budget"]["model_call_limits"]["gpt-6-sol"] = 2
    changed["economics"]["fresh_calls"] = 5
    with pytest.raises(ValueError, match="budgeted exactly once"):
        RunPlan.parse(changed)
