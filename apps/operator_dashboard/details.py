# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812 -- bounded read-only evidence projection
"""Allowlisted detail projections; archived text is never an executable command."""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from apps.operator_dashboard.project import _reference, _text
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import (
    FileFormat,
    FilesystemError,
    MarkdownFile,
    read,
)
from scripts.backlog.intake import Intake, load_json

DISPLAY_LIMIT = 16000
MAX_TURNS = 10

if TYPE_CHECKING:
    from pathlib import Path


def confined(root: Path, path: Path) -> Path:
    """Resolve every file, including symlinks, under its configured trust root."""
    result = resolve_path(path).value
    if not result.is_relative_to(resolve_path(root).value):
        raise ValueError("Evidence path escapes configured root")
    return result


def display(value: object, *, disclosed: bool = True) -> dict[str, Any]:
    """Bound exact archived text with explicit missing/disclosure/truncation states."""
    if not disclosed:
        return {
            "availability": "NOT_DISCLOSED",
            "text": "Start with --raw-details to inspect allowlisted raw evidence.",
        }
    if value is None:
        return {"availability": "NOT_CAPTURED", "text": "NOT_CAPTURED"}
    text = value if isinstance(value, str) else json.dumps(value, indent=2)
    return {
        "availability": "CAPTURED",
        "text": text[:DISPLAY_LIMIT],
        "truncated": len(text) > DISPLAY_LIMIT,
        "total_characters": len(text),
    }


def _captured(folder: Path, name: str, *, raw: bool) -> dict[str, Any]:
    path = confined(folder, folder / name)
    if not path.is_file():
        return display(None)
    if not raw:
        return display(None, disclosed=False)
    try:
        return {**display(_text(path)), "reference": _reference(path)}
    except (OSError, ValueError, FilesystemError) as error:
        return {"availability": "UNAVAILABLE", "text": str(error)}


def _feedback(request: dict[str, Any]) -> str | None:
    for message in reversed(request.get("prompt", {}).get("messages", [])):
        if message.get("role") == "tool":
            content = message.get("content")
            if not isinstance(content, str):
                continue
            try:
                result = json.loads(content)
            except ValueError:
                continue
            if isinstance(result, dict) and "validation" in result:
                return content  # exact native result, no invented summary
    prompt = request.get("prompt", {}).get("content", "")
    if not isinstance(prompt, str):
        return None
    marker = "HOST FEEDBACK:\n"
    if marker not in prompt:
        return None
    tail = prompt.split(marker, 1)[1]
    try:
        _, end = json.JSONDecoder().raw_decode(tail)
    except ValueError:
        return None
    return tail[:end]  # exact archived substring, not a reconstructed conversation


def _validation(value: dict[str, Any], *, raw: bool) -> dict[str, Any]:
    return {
        name: {
            "argv": command.get("argv"),
            "exit_code": command.get("exit_code"),
            "started_at": command.get("started_at"),
            "elapsed_seconds": command.get("elapsed_seconds"),
            "stdout": display(command.get("stdout"), disclosed=raw),
            "stderr": display(command.get("stderr"), disclosed=raw),
        }
        for name, command in value.items()
        if name in {"tests", "oracle", "ruff", "format", "typing"}
        and isinstance(command, dict)
    }


def turn_detail(folder: Path, stage: dict[str, Any], *, raw: bool) -> dict[str, Any]:
    """Associate an archived model request, proposal and host validation by turn."""
    number = stage["number"]
    if type(number) is not int or not 1 <= number <= MAX_TURNS:
        raise ValueError("Invalid recorded turn number")
    turn = confined(folder, folder / f"turn-{number:02d}")
    request_path = confined(turn, turn / "request.json")
    response_path = confined(turn, turn / "response.json")
    request = load_json(request_path) if request_path.is_file() else {}
    response = load_json(response_path) if response_path.is_file() else {}
    calls = response.get("tool_calls", [])
    proposal_id = stage.get("proposal_id")
    tools = [
        {
            "name": call.get("name"),
            "provider_call_id": call.get("provider_call_id"),
            "arguments": display(call.get("arguments_json"), disclosed=raw),
        }
        for call in calls
    ]
    return {
        "number": number,
        "stage": {
            key: stage.get(key)
            for key in (
                "phase",
                "disposition",
                "started_at",
                "finished_at",
                "elapsed_seconds",
                "model_seconds",
                "termination",
                "proposal_id",
                "proposal_valid",
                "source_before",
                "source_after",
                "usage",
                "context",
                "context_bytes",
                "context_utilization",
                "prompt_bytes",
                "input_tokens_measured",
                "sources_before",
                "sources_after",
                "edits",
                "mechanical_format",
            )
        },
        "request_reference": _reference(request_path) if request else None,
        "response_reference": _reference(response_path) if response else None,
        "request_text": display(
            request.get("prompt", {}).get("messages")
            or request.get("prompt", {}).get("content"),
            disclosed=raw,
        ),
        "response_text": display(response.get("content"), disclosed=raw),
        "reasoning_text": display(response.get("reasoning_content"), disclosed=raw),
        "conversation": display(response.get("conversation"), disclosed=raw),
        "settings": request.get("settings"),
        "provider_settings": request.get("provider_settings"),
        "request_role": request.get("prompt", {}).get("role", "NOT_CAPTURED"),
        "response_source": response.get("source", "NOT_CAPTURED"),
        "tools": tools,
        "proposal_correlation": "MATCH"
        if isinstance(proposal_id, str)
        and bool(proposal_id.strip())
        and any(c.get("provider_call_id") == proposal_id for c in calls)
        else "NOT_ESTABLISHED",
        "feedback": display(_feedback(request), disclosed=raw),
        "patch": _captured(turn, "proposal.patch", raw=raw),
        "tool_results": _captured(turn, "tools.json", raw=raw),
        "capacity": _captured(turn, "capacity.json", raw=raw),
        "validation": _validation(stage.get("validation", {}), raw=raw),
    }


def run_detail(path: Path, *, raw: bool) -> dict[str, Any]:
    """Project a trusted indexed run; never follow paths recorded in its payload."""
    folder = path.parent
    result = load_json(path)
    freeze_path = confined(folder, folder / "freeze.json")
    freeze = load_json(freeze_path) if freeze_path.is_file() else {}
    task = result.get("task_definition", {})
    provenance = result.get("provenance") or {}
    return {
        "id": folder.name,
        "reference": _reference(path),
        "objective": display(task.get("objective") or freeze.get("task")),
        "task_identity": result.get(
            "task_name", "NOT_RECORDED (legacy source-bound task)"
        ),
        "model": provenance.get("model", "NOT_RECORDED"),
        "profile": provenance.get("profile", "NOT_RECORDED"),
        "limits": result.get("limits"),
        "baseline": result.get("baseline"),
        "closeout": _captured(folder, "closeout.json", raw=raw),
        "command_checks": [
            _captured(folder, f"coding-command-{n:02d}.json", raw=raw)
            for n in range(1, 33)
            if confined(folder, folder / f"coding-command-{n:02d}.json").is_file()
        ],
        "validation_seconds": result.get("validation_seconds"),
        "raw_disclosure": raw,
        "recorded_turn_count": len(result.get("turns", [])),
        "turns_truncated": len(result.get("turns", [])) > MAX_TURNS,
        "turns": [
            turn_detail(folder, stage, raw=raw)
            for stage in result.get("turns", [])[:MAX_TURNS]
        ],
        "limitations": [
            "Archived receipt presence is not current liveness or authority.",
            (
                "No cross-run session is inferred. File digests identify bytes, "
                "not signed attestations."
            ),
            (
                "Request and response JSON are normalized worker captures, "
                "not an invented chat transcript."
            ),
        ],
    }


def proposal_detail(root: Path, identity: str) -> dict[str, Any]:
    """Reuse proposal/review authentication and canonical duplicate hints."""
    intake = Intake(root)
    folder = confined(root, root / "docs/backlog/proposals" / identity)
    confined(root, folder / "proposal.json")
    record = intake.get(identity)
    return {
        **record,
        "duplicates": intake.duplicates(identity),
        "implementation_authority": (
            "NOT_ASSESSED; proposal/review never grants execution authority"
        ),
        "reference": _reference(folder / "proposal.json"),
    }


def _backlog_reviews(root: Path, identity: str) -> list[dict[str, Any]]:
    intake = Intake(root)
    reviews = []
    for entry in intake.queue()["proposals"]:
        record = intake.get(entry["id"])
        linked = [
            r
            for r in record["history"]
            if (r.get("publication") or {}).get("id") == identity
        ]
        if linked:
            reviews.append({"proposal": entry["id"], "history": linked})
    return reviews


def backlog_detail(root: Path, identity: str) -> dict[str, Any]:
    """Use the existing Markdown model for recorded sections, not inferred meaning."""
    if not re.fullmatch(r"B-\d{4}", identity):
        raise ValueError("Invalid backlog identity")
    paths = list((root / "docs/backlog/items").glob(identity + "-*.md"))
    paths += list((root / "docs/backlog/epics").glob(identity + "-*.md"))
    if len(paths) != 1:
        raise ValueError("Backlog item missing or ambiguous")
    path = confined(root, paths[0])
    file = read(resolve_path(path), file_format=FileFormat.MARKDOWN, max_bytes=1 << 20)
    if not isinstance(file, MarkdownFile):
        raise TypeError("Expected Markdown")
    metadata = {
        key: value.strip()
        for key, value in re.findall(r"^- ([a-z_]+): (.+)$", file.content, re.MULTILINE)
    }
    rationale = [
        s.content
        for s in file.sections
        if s.title.lower()
        in {
            "split record",
            "disposition",
            "decision",
            "reason for deferral",
            "supersession",
            "resolution",
        }
    ]
    return {
        "id": identity,
        "metadata": metadata,
        "body": display(file.content),
        "rationale": rationale
        or ["NOT_RECORDED as a dedicated rationale section; inspect source body."],
        "sections": [s.title for s in file.sections],
        "reference": _reference(path),
        "review_history": _backlog_reviews(root, identity) or "NOT_RECORDED",
    }
