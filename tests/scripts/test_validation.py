# Copyright (c) 2026
# ruff: noqa: COM812 -- compatible with repository formatter
"""Deterministic impact and recovery controls using tiny authored inputs."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

from scripts.validation import __main__ as entry
from scripts.validation import evidence
from scripts.validation.__main__ import recovery
from scripts.validation.observation import Observations, failure_kind
from scripts.validation.selection import imports, select


def fixture_tree(root: Path) -> None:
    """Create isolated dependency and public facade consumers."""
    files = {
        "src/devtools/alpha/local.py": "x = 1\n",
        "src/devtools/beta/shared.py": "from devtools.alpha.local import x\n",
        "src/devtools/alpha/__init__.py": "from .local import x\n",
        "tests/alpha/test_local.py": "from devtools.alpha.local import x\n",
        "tests/beta/test_shared.py": "from devtools.beta.shared import x\n",
        "tests/integration/test_public.py": "from devtools.alpha import x\n",
        "tests/other/test_other.py": "x = 0\n",
    }
    for name, text in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "paths",
    [
        ["src/devtools/alpha/local.py"],
        ["src/devtools/alpha/local.py", "src/devtools/beta/shared.py"],
    ],
)
def test_transitive_and_public_consumers(tmp_path: Path, paths: list[str]) -> None:
    """Local, shared and multiple changes include indirect public consumers."""
    fixture_tree(tmp_path)
    plan = select(tmp_path, paths)
    groups = plan["groups"]
    assert isinstance(groups, dict)
    assert "tests/alpha" in groups
    assert "tests/beta/test_shared.py" in groups or "tests/beta" in groups
    assert "tests/integration/test_public.py" in groups
    assert "tests/other/test_other.py" not in groups


@pytest.mark.parametrize(
    "path",
    [
        "conftest.py",
        "tests/alpha/conftest.py",
        "pyproject.toml",
        "uv.lock",
        "src/devtools/alpha/__init__.py",
        "src/devtools/alpha/deleted.py",
        "src/devtools/alpha/renamed.py",
    ],
)
def test_uncertain_inputs_require_review(tmp_path: Path, path: str) -> None:
    """Fixture, dependency, facade, deleted and new layout cannot claim closure."""
    fixture_tree(tmp_path)
    plan = select(tmp_path, [path])
    assert plan["uncertainty"]
    assert plan["comprehensive_required_for_publication"]


def test_test_only_selection(tmp_path: Path) -> None:
    """Test-only edits select their exact owning file."""
    fixture_tree(tmp_path)
    plan = select(tmp_path, ["tests/other/test_other.py"])
    assert list(plan["groups"]) == ["tests/other/test_other.py"]


def test_dynamic_import_and_parse_uncertainty() -> None:
    """Dynamic import and invalid syntax are explicitly uncertain."""
    assert imports("src/devtools/a.py", "importlib.import_module(name)")[1]
    assert imports("src/devtools/a.py", "!")[1]
    assert imports("src/devtools/a/b.py", "from ..c import value")[0] == {
        "devtools.c",
        "devtools.c.value",
    }


@pytest.mark.parametrize("mode", ["targeted", "comprehensive"])
def test_failed_run_recovery_keeps_original(mode: str) -> None:
    """A repair selects original failed IDs without rewriting prior outcomes."""
    previous: dict[str, Any] = {
        "mode": mode,
        "status": "failed",
        "phases": [{"nodeid": "tests/test_a.py::test_fix", "outcome": "failed"}],
    }
    assert recovery(previous, "one-line boundary repair") == [
        "tests/test_a.py::test_fix",
    ]
    assert previous["status"] == "failed"
    with pytest.raises(ValueError, match="Recovery requires"):
        recovery(previous, "")
    with pytest.raises(ValueError, match="No failed"):
        recovery({"phases": []}, "diagnose configuration")


def test_failure_classification() -> None:
    """Collection, interruption and configuration are not assertions."""
    observations = Observations()
    assert failure_kind(2, observations) == "interrupted"
    assert failure_kind(4, observations) == "configuration"
    observations.collection_errors.append("syntax")
    assert failure_kind(2, observations) == "collection"


def test_input_changes_are_not_reusable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reject stale dependency and environment correspondence."""
    fixture_tree(tmp_path)
    lock = tmp_path / "uv.lock"
    lock.write_text("first", encoding="utf-8")
    monkeypatch.setattr(
        evidence, "git", lambda *_: "src/devtools/alpha/local.py\0uv.lock"
    )
    before = evidence.inputs(tmp_path)
    source = tmp_path / "src/devtools/alpha/local.py"
    source.write_text("x = 2\n", encoding="utf-8")
    assert evidence.inputs(tmp_path) != before
    source.write_text("x = 1\n", encoding="utf-8")
    lock.write_text("second", encoding="utf-8")
    assert evidence.inputs(tmp_path) != before
    lock.write_text("first", encoding="utf-8")
    monkeypatch.setenv("VALIDATION_TEST_ENVIRONMENT", "changed")
    assert evidence.inputs(tmp_path) != before


def test_comprehensive_failure_then_targeted_repair(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Keep the failed full result when recovering after a correction."""
    fixture_tree(tmp_path)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(entry, "git", lambda *_: "")
    state = {"source": "before"}
    monkeypatch.setattr(entry, "inputs", lambda _: dict(state))
    observed: list[list[str]] = []

    def run(arguments: list[str], *, plugins: list[Any]) -> int:
        observed.append(arguments)
        plugins[0].phases.append(
            {
                "nodeid": "tests/alpha/test_local.py::test_x",
                "outcome": "failed" if len(observed) == 1 else "passed",
            }
        )
        return 1 if len(observed) == 1 else 0

    monkeypatch.setattr(pytest, "main", run)
    monkeypatch.setattr(
        entry,
        "run_protected",
        lambda _root, _output, args, observations: run(args, plugins=[observations]),
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["validation", "comprehensive", "--execute", "--output", ".local/full.json"],
    )
    assert entry.main() == 1
    original = (tmp_path / ".local/full.json").read_bytes()
    state["source"] = "one-line repair"
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "validation",
            "recover",
            "--previous",
            ".local/full.json",
            "--correction",
            "repair boundary",
            "--test",
            "tests/beta",
            "--execute",
            "--output",
            ".local/repair.json",
        ],
    )
    assert entry.main() == 0
    assert "--no-cov" in observed[-1]
    assert "tests/alpha/test_local.py::test_x" in observed[-1]
    assert (tmp_path / ".local/full.json").read_bytes() == original
    assert json.loads(original)["exit_code"] == 1


def test_coding_protocol_contract_groups(tmp_path: Path) -> None:
    """Include cross-component contracts beyond static import witnesses."""
    for group in ("agents", "tools", "apps/qwen", "scripts/backlog"):
        (tmp_path / "tests" / group).mkdir(parents=True)
    plan = select(tmp_path, ["src/devtools/tools/checks.py"])
    assert set(plan["groups"]) == {
        "tests/agents",
        "tests/tools",
        "tests/apps/qwen",
        "tests/scripts/backlog",
    }


def test_protected_starts_coverage_before_imports(tmp_path: Path) -> None:
    """Cover import-time statements through the actual fresh child boundary."""
    from scripts.validation.protected import run_protected  # noqa: PLC0415

    package = tmp_path / "tiny_validation_fixture.py"
    package.write_text("VALUE = 1\n", encoding="utf-8")
    test = tmp_path / "test_tiny.py"
    test.write_text(
        f"import sys\nsys.path.insert(0, {str(tmp_path)!r})\n"
        "from tiny_validation_fixture import VALUE\n"
        "def test_value():\n    assert VALUE == 1\n",
        encoding="utf-8",
    )
    config = tmp_path / "pytest.ini"
    config.write_text("[pytest]\n", encoding="utf-8")
    observations = Observations()
    result = run_protected(
        Path.cwd(),
        tmp_path / "result.json",
        [
            str(test),
            "-c",
            str(config),
            "--cov=tiny_validation_fixture",
            "--cov-fail-under=100",
            "--cov-report=term",
        ],
        observations,
    )
    assert result == 0
    assert observations.phases[1]["outcome"] == "passed"
