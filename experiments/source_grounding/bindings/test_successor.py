# Copyright (c) 2026
# ruff: noqa: INP001, S101, COM812 -- immutable deployment equivalence contracts
"""Test the prospective successor without scientific evidence or model dispatch."""

import asyncio
import copy
import json

import pytest

from experiments.codex_dogfood.case_0009.artifacts import ROOT, digest
from experiments.orchestration.model import RunPlan
from experiments.orchestration.storage import load
from experiments.source_grounding.bindings import successor


def test_scientific_contract_is_unchanged() -> None:
    """Every semantic plan field and disclosed input retains its predecessor."""
    original = load(ROOT / successor.ORIGINAL)
    current = load(ROOT / successor.PLAN)
    binding_keys = {
        "name",
        "attempt",
        "stage_a",
        "implementation",
        "controller_implementation",
        "cases",
        "commands",
        "semantic",
    }
    assert {k: v for k, v in current.items() if k not in binding_keys} == {
        k: v for k, v in original.items() if k not in binding_keys
    }
    assert current["stage_a"]["protocol"] == original["stage_a"]["protocol"]
    assert current["stage_a"]["checkpoint"] != original["stage_a"]["checkpoint"]
    for before, after in zip(original["cases"], current["cases"], strict=True):
        assert {k: v for k, v in before.items() if k != "inputs"} == {
            k: v for k, v in after.items() if k != "inputs"
        }
        for old_input, new_input in zip(before["inputs"], after["inputs"], strict=True):
            if old_input["name"] == "implementation.json":
                assert new_input["name"] == old_input["name"]
                assert new_input["path"] == successor.INTEGRITY
            else:
                assert old_input == new_input
    for argv in [*current["commands"].values(), current["semantic"]["argv"]]:
        assert argv[argv.index("--stage-a") + 1] == current["stage_a"]["checkpoint"]
    normalized = copy.deepcopy(current)
    for argv in [*normalized["commands"].values(), normalized["semantic"]["argv"]]:
        argv[argv.index("--stage-a") + 1] = original["stage_a"]["checkpoint"]
    assert normalized["commands"] == original["commands"]
    assert normalized["semantic"] == original["semantic"]


def test_preserved_bytes_and_adoption() -> None:
    """Hash opaque adopted closures without opening their scientific judgments."""
    binding = load(ROOT / successor.BINDING)
    for address, sha in binding["scientific_artifacts_preserved"].items():
        assert digest((ROOT / address).read_bytes()) == sha
    value = load(ROOT / successor.PLAN)
    assert set(value["adopted_branches"]) == {"0022", "0023"}
    assert value["economics"]["adopted_new_consumption"] == 0
    assert value["economics"]["input_range"] == [28539, 1756679]
    assert value["economics"]["output_range"] == [0, 191923]


def test_fifth_fresh_call_is_rejected() -> None:
    """Changing every numeric allowance still cannot re-invoke adopted science."""
    value = load(ROOT / successor.PLAN)
    assert set(value["usage_budget"]["calls"]) == {
        "0022/C",
        "0023/C",
        "0024/C",
        "0024/B",
    }
    value["usage_budget"]["calls"]["0022/B"] = copy.deepcopy(
        value["usage_budget"]["calls"]["0024/B"]
    )
    value["usage_budget"]["fresh_call_limit"] = 5
    value["usage_budget"]["model_call_limits"]["gpt-6-sol"] = 2
    value["economics"]["fresh_calls"] = 5
    with pytest.raises(ValueError, match="budgeted exactly once"):
        RunPlan.parse(value)


def test_canonical_plan_replays_with_distinct_identity() -> None:
    """Canonical construction plus actual startup remains exactly reproducible."""
    value = load(ROOT / successor.PLAN)
    rebuilt = asyncio.run(successor.plan(value["stage_a"]["checkpoint"]))
    assert rebuilt == value
    original = load(ROOT / successor.ORIGINAL)
    old = RunPlan.parse(original)
    new = RunPlan.parse(value)
    assert new.identity(value["controller_implementation"]) != old.identity(
        original["controller_implementation"]
    )
    assert json.loads(new.canonical) == value
