# Copyright (c) 2026
# ruff: noqa: COM812 -- existing formatter convention for bounded fixtures
"""Real bounded acquisition, Localization and edit/check consumer contracts."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.obligations import ObligationFrame
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from tests.apps.qwen.test_coding_loop import (
    _TINY_OLD,
    _TINY_SOURCE,
    _TINY_TEST,
    _TINY_TEST_TEXT,
    _TINY_TYPED_GOOD,
    _refuse_terminal_closeout,
    _terminal_cli_exit,
    _tiny_task,
)

if TYPE_CHECKING:
    from pathlib import Path

    from apps.qwen.tasks import CodingTask


def member(
    path: str = _TINY_SOURCE,
    text: str = _TINY_OLD,
    decision: str = "supported",
) -> dict[str, Any]:
    """Declare required coordinates and judgment explicitly as the trusted host."""
    return {
        "path": path,
        "version": str(ContentIdentity.from_text(text)),
        "start": 0,
        "end": len(text),
        "decision": decision,
        "claim": "This exact block supplies the stated implementation contract",
        "reason": "Independent host-selected criterion witness",
    }


def obligation(
    key: str,
    members: list[dict[str, Any]],
    requirement: str = "mandatory",
) -> dict[str, Any]:
    """No criterion, requirement or query is authored by the model double."""
    return {
        "key": key,
        "predicate": "Inspect the exact " + key + " contract",
        "query": "value integer Frozen",
        "requirement": requirement,
        "criterion": {
            "name": "host-exact-block",
            "statement": (
                "Inspect every declared exact current source block before editing"
            ),
        },
        "alternatives": [{"key": "host-selected", "members": members}]
        if members
        else [],
    }


def frame(task: CodingTask, obligations: list[dict[str, Any]]) -> ObligationFrame:
    """Bind the independently specified frame to the actual frozen task."""
    return ObligationFrame.from_dict(
        {
            "schema": "qwen-obligation-frame-v1",
            "task_definition_sha256": task.definition_sha256,
            "caller": "independent trusted fixture host",
            "obligations": obligations,
        },
    )


def read(path: str = _TINY_SOURCE, start: int = 0) -> tuple[str, dict[str, Any]]:
    """Use the actual native read interface, not a supplied readiness Boolean."""
    return "inspect_source", {"path": path, "start": start}


EDIT = (
    "replace_source",
    {"path": _TINY_SOURCE, "old_text": _TINY_OLD, "new_text": _TINY_TYPED_GOOD},
)


class Scripted:
    """Literal bounded actions and captured actual model requests; no inference."""

    source = InteractionSource("obligation-independent")

    def __init__(self, actions: list[tuple[str, dict[str, Any]]]) -> None:
        """Retain only independently selected literal actions."""
        self.actions = actions
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return one explicitly scheduled action per real invocation."""
        index = len(self.requests)
        self.requests.append(request)
        name, values = self.actions[index]
        return ModelResponse(
            "Literal independent action",
            self.source,
            termination=ModelTermination.TOOL_CALL,
            tool_calls=(
                ModelToolCall(name, json.dumps(values), f"independent-{index}"),
            ),
        )


def run(
    root: Path,
    task: CodingTask,
    model: Scripted,
    selected: ObligationFrame | None,
) -> dict[str, Any]:
    """Exercise the real public worker and unchanged fixed validation commands."""
    options: dict[str, Any] = {} if selected is None else {"obligation_frame": selected}
    return asyncio.run(
        worker.run_coding_task(
            root,
            root / ".local/run",
            model,
            task=task,
            coordinated_edits=True,
            observed_edits=True,
            **options,
        ),
    )


def test_unframed_native_contract_remains_unchanged(tmp_path: Path) -> None:
    """The preintegration worker supports this narrow task without a frame."""
    root = resolve_path(tmp_path / "task").value
    task = asyncio.run(_tiny_task(root, native=True))
    model = Scripted([read(), EDIT])
    original_digest = task.definition_sha256
    result = run(root, task, model, None)
    assert result["accepted"]
    assert result["task_definition_sha256"] == original_digest
    assert "obligation_context" not in result
    assert "obligation_frame_sha256" not in result
    assert "HOST OBLIGATION CONTEXT" not in str(model.requests)
    assert (root / _TINY_SOURCE).read_text() == _TINY_OLD


def case_spec(
    case: str,
) -> tuple[list[dict[str, Any]], list[tuple[str, dict[str, Any]]]]:
    """Specify independent expected acquisitions and host judgments."""
    source = member()
    test = member(_TINY_TEST, _TINY_TEST_TEXT)
    specs = [obligation("implementation", [source])]
    actions = [read(), EDIT]
    if case in {"missing", "partial", "helpful", "complementary", "acquire-all"}:
        specs = [obligation("behavior", [test])]
        if case == "missing":
            actions = [
                ("search_source", {"query": "test_integer", "mode": "file"}),
                read(),
                EDIT,
            ]
        elif case == "complementary":
            specs = [obligation("complete", [source, test])]
        else:
            specs.insert(0, obligation("implementation", [source]))
            if case == "helpful":
                specs[1]["requirement"] = "helpful"
            elif case == "acquire-all":
                actions = [read(), read(_TINY_TEST), EDIT]
    if case == "contradicted":
        source["decision"] = "contradicted"
    if case == "unjudged":
        source["decision"] = "unresolved"
    if case == "stale":
        source["version"] = "0" * 64
    return specs, actions


def assert_bound_context(
    status: dict[str, Any], selected: ObligationFrame, task: CodingTask
) -> None:
    """Check identity and native lexical provenance independently of admission."""
    assert status["identity_coverage_exact"]
    assert status["frame_sha256"] == selected.sha256
    assert status["task_definition_sha256"] == task.definition_sha256
    assert status["repository"]
    assert status["snapshot"]
    assert status["full_task_query"] == task.objective


@pytest.mark.parametrize(
    "case",
    [
        "supported",
        "missing",
        "helpful",
        "partial",
        "complementary",
        "contradicted",
        "unjudged",
        "stale",
        "acquire-all",
    ],
)
def test_native_readiness_controls_actual_edit_admission(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
) -> None:
    """Exercise literal criteria through native Localization owners."""
    root = resolve_path(tmp_path / "task").value
    task = replace(
        asyncio.run(_tiny_task(root, native=True)),
        maximum_calls=4,
        maximum_proposals=1,
    )
    specs, actions = case_spec(case)
    selected = frame(task, specs)
    model = Scripted(actions)
    result = run(root, task, model, selected)
    accepted = case in {"supported", "helpful", "acquire-all"}
    assert result["accepted"] is accepted, result
    assert result["proposals_attempted"] == 1
    assert result["proposals_admitted"] == int(accepted)
    assert result["model_calls_attempted"] == len(actions)
    assert result["source_restored"]
    assert result["original_unchanged"]
    status = result["obligation_context"]
    assert status["readiness"] == ("ready" if accepted else "blocked")
    assert_bound_context(status, selected, task)
    assert status["full_task_paths"]
    assert all(lane["paths"] for lane in status["lexical_lanes"])
    assert "HOST OBLIGATION CONTEXT" in model.requests[-1].prompt.messages[0].content
    assert status["assessment_sha256"] in model.requests[-1].prompt.messages[0].content
    assert all(
        r["decision"] != "supported" or r["used_disclosures"]
        for c in status["candidates"]
        for r in c["members"]
    )
    if case == "missing":
        observed = json.loads((root / ".local/run/turn-01/tools.json").read_text())
        assert observed[0]["result"]["matches"]
        assert any(m["path"] == _TINY_TEST for m in observed[0]["result"]["matches"])
        assert status["unresolved_mandatory"] == ["behavior"]
    if case == "partial":
        assert status["unresolved_mandatory"] == ["behavior"]
        assert status["candidates"][0]["members"][0]["decision"] == "supported"
    if case == "helpful":
        assert status["unresolved_helpful"] == ["behavior"]
        assert not status["unresolved_mandatory"]
    if case == "stale":
        assert (
            status["candidates"][0]["members"][0]["reason"]
            == "STALE_OR_FOREIGN_WITNESS_SOURCE"
        )
    if accepted:
        stage = result["turns"][-1]
        assert stage["edit_context_assessment"] == status["assessment_sha256"]
        assert stage["validation"]["accepted"]
        assert (root / ".local/run/final-source.py").read_text() == _TINY_TYPED_GOOD
    else:
        assert result["disposition"] == "PROPOSAL_ADMISSION_FAILED"
        assert (root / ".local/run/final-source.py").read_text() == _TINY_OLD
        feedback = json.loads(
            (root / f".local/run/turn-{len(actions):02d}/tools.json").read_text(),
        )
        assert feedback[0]["result"]["error"] == "CONTEXT_NOT_READY"
        _refuse_terminal_closeout(root, task, root / ".local/run")
    assert _terminal_cli_exit(root, task, result, monkeypatch) == int(not accepted)
