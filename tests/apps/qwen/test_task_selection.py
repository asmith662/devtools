# Copyright (c) 2026
# ruff: noqa: COM812 -- experiment host regression boundaries
"""Two tasks through one worker, with no inference or maintained target edits."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen import coding_loop as worker
from apps.qwen.development_task import _hash
from apps.qwen.tasks import MARKDOWN, SOURCE_SEGMENTS, select_task
from devtools.models.interaction import InteractionSource, ModelResponse, ModelToolCall
from tests.apps.qwen.test_coding_loop import GOOD, OLD, Scripted, proposal

ROOT = Path(__file__).resolve().parents[3]
if TYPE_CHECKING:
    from collections.abc import Callable

    from apps.qwen.tasks import CodingTask


@pytest.fixture(autouse=True)
def captured_task_root(
    captured_inputs: Callable[[CodingTask], Path], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Bind only the historical task inputs; never mutate maintained source."""
    monkeypatch.setattr(__name__ + ".ROOT", captured_inputs(SOURCE_SEGMENTS))


OLD_SPLIT = "content.splitlines(keepends=True)"
# Reference-only stand-in: the stdlib's own segment splitter. This is not a
# proposed maintained implementation and is never part of model Context.
REFERENCE_SPLIT = 'filter(None, __import__("ast")._splitlines_no_ff(content))'


def segment_proposal(old: str, new: str) -> ModelResponse:
    """Deliver an explicitly scripted native proposal for host verification."""
    return ModelResponse(
        "scripted reference only",
        InteractionSource("scripted"),
        tool_calls=(
            ModelToolCall(
                "propose_edit",
                json.dumps(
                    {
                        "path": SOURCE_SEGMENTS.source,
                        "old_text": old,
                        "new_text": new,
                    }
                ),
                "reference-call",
            ),
        ),
    )


def test_second_task_baseline_fails_and_reference_is_accepted(tmp_path: Path) -> None:
    """The independent 48-check oracle distinguishes baseline and valid reference."""
    original = _hash(ROOT / SOURCE_SEGMENTS.source)
    model = Scripted([segment_proposal(OLD_SPLIT, REFERENCE_SPLIT)])
    result = asyncio.run(
        worker.run_coding_task(
            ROOT, tmp_path / "second", model, task=select_task("python-source-segments")
        )
    )
    assert result["accepted"], result
    assert result["baseline_validation"]["oracle"]["failed"]
    assert not result["baseline_validation"]["tests"]["failed"]
    validation = result["turns"][0]["validation"]
    assert "48 exact AST segment checks" in validation["oracle"]["stdout"]
    assert result["original_unchanged"]
    assert result["workspace_removed"]
    # The pinned baseline lives only in isolation after the maintained fix lands.
    assert _hash(ROOT / SOURCE_SEGMENTS.source) == original
    request = model.requests[0]
    assert json.loads(request.tools[0].input_schema_json)["properties"]["path"][
        "enum"
    ] == [SOURCE_SEGMENTS.source]
    assert "MarkdownFile" not in request.prompt.content
    assert "_extract_source_segment" in request.prompt.content
    assert "Reference-only" not in request.prompt.content
    assert result["turns"][0]["context"][0]["selected_kind"] == "symbol"


def test_invalid_first_edit_gets_feedback_then_reference_repair(tmp_path: Path) -> None:
    """A second task needs no alternate worker loop for repair."""
    bad = "content.splitlines(keepends=False)"
    model = Scripted(
        [segment_proposal(OLD_SPLIT, bad), segment_proposal(bad, REFERENCE_SPLIT)]
    )
    result = asyncio.run(
        worker.run_coding_task(ROOT, tmp_path / "repair", model, task=SOURCE_SEGMENTS)
    )
    assert result["accepted"], result
    assert result["repair_cycles"] == 1
    assert "AssertionError" in model.requests[1].prompt.content
    assert "reference-call" in model.requests[1].prompt.content
    assert result["original_unchanged"]


def test_second_task_refuses_markdown_edit(tmp_path: Path) -> None:
    """Configuration does not broaden the one-file admission boundary."""
    model = Scripted([proposal(OLD, GOOD)])
    result = asyncio.run(
        worker.run_coding_task(
            ROOT, tmp_path / "cross-task", model, task=SOURCE_SEGMENTS
        )
    )
    assert not result["accepted"]
    assert result["disposition"] == "PROPOSAL_ADMISSION_FAILED"
    assert len(model.requests) == 1
    assert result["workspace_removed"]
    assert result["original_unchanged"]


def test_markdown_restores_original_inputs_only_in_workspace(tmp_path: Path) -> None:
    """The accepted original task remains reproducible after its maintained fix."""
    original = _hash(ROOT / MARKDOWN.source)
    model = Scripted([proposal(OLD, GOOD)])
    result = asyncio.run(
        worker.run_coding_task(
            ROOT, tmp_path / "first", model, task=select_task("markdown-fences")
        )
    )
    assert result["accepted"], result
    assert result["baseline_validation"]["oracle"]["failed"]
    assert _hash(ROOT / MARKDOWN.source) == original
    assert result["original_unchanged"]


def test_second_task_repair_exhaustion(tmp_path: Path) -> None:
    """A valid but incorrect replacement cannot obtain unbounded repairs."""
    model = Scripted(
        [segment_proposal(OLD_SPLIT, "content.splitlines(keepends=False)")]
    )
    result = asyncio.run(
        worker.run_coding_task(
            ROOT, tmp_path / "exhausted", model, task=SOURCE_SEGMENTS, maximum_calls=1
        )
    )
    assert result["disposition"] == "REPAIR_BUDGET_EXHAUSTED"
    assert result["original_unchanged"]


@pytest.mark.parametrize(
    "response",
    [
        RuntimeError("provider failure"),
        ModelResponse("", Scripted.source, tool_calls=(ModelToolCall("shell", "{}"),)),
    ],
)
def test_second_task_provider_or_tool_failure_stops(
    tmp_path: Path,
    response: ModelResponse | Exception,
) -> None:
    """No different-model fallback or repair follows an ambiguous provider failure."""
    model = Scripted([response])
    result = asyncio.run(
        worker.run_coding_task(ROOT, tmp_path / "stopped", model, task=SOURCE_SEGMENTS)
    )
    assert not result["accepted"]
    assert len(model.requests) == 1
    assert result["original_unchanged"]
    assert result["workspace_removed"]


@pytest.mark.parametrize(
    "changes",
    [
        {"source": "../outside.py"},
        {"maximum_calls": 4},
        {"wall_seconds": 901},
        {"output_tokens": 4097},
        {"call_seconds": 301},
        {"baseline_revision": "main"},
    ],
)
def test_configuration_cannot_broaden_scope_or_bounds(
    changes: dict[str, Any],
) -> None:
    """Malformed host definitions are rejected before the worker can run."""
    with pytest.raises(ValueError, match=r"Task|resource address"):
        replace(SOURCE_SEGMENTS, **changes)


def test_unknown_task_is_not_model_selected() -> None:
    """Only maintained task names are CLI choices."""
    with pytest.raises(ValueError, match="Unknown coding task"):
        select_task("arbitrary-task")


def test_nonexistent_baseline_revision_stops_before_model(tmp_path: Path) -> None:
    """Matching current bytes cannot substitute for the configured Git identity."""
    model = Scripted([])
    result = asyncio.run(
        worker.run_coding_task(
            ROOT,
            tmp_path / "wrong-revision",
            model,
            task=replace(SOURCE_SEGMENTS, baseline_revision="0" * 40),
        )
    )
    assert result["disposition"] == "PREPARATION_FAILED"
    assert model.requests == []
    assert result["original_unchanged"]
