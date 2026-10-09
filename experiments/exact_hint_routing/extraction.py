# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003 -- formatter owns commas; bounded experiment validation
"""Frozen bounded syntactic extraction; inputs contain no repository state."""

from __future__ import annotations

import keyword
import re

from devtools.context.localization.identity import (
    LocalizationTaskIdentity,
    TaskProvenance,
    TaskTextSpan,
)
from devtools.context.repository.resource import RepositoryResourceAddress
from experiments.exact_hint_routing.models import (
    ExactHintObservation,
    ExtractionDecision,
    HintCategory,
)

POLICY = "u2-task-syntax-v1"
_CODE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")
_FENCES = re.compile(
    r"^[ \t]*(`{3,}|~{3,})[^\n]*\n.*?(?:^[ \t]*\1[ \t]*(?:\n|$)|\Z)",
    re.MULTILINE | re.DOTALL,
)
_INTRO = re.compile(
    r"\b(class|type|function|method|module|package|path|file|resource)\s*$",
    re.IGNORECASE,
)
_UNQUOTED_PATH = re.compile(
    r"\b(?:path|file|resource)\s+([A-Za-z0-9_./-]+/[A-Za-z0-9_./-]+)"
)
_FILENAME = re.compile(r"[A-Za-z0-9_-]+\.(?:py|md|toml|yaml|yml|json|txt)")


def _category(text: str, intro: str) -> tuple[HintCategory | None, str]:  # noqa: PLR0911 -- explicit accept/reject syntax boundaries
    """Classify syntax only; never test native existence or infer module roots."""
    if "/" in text or (
        intro in {"path", "file", "resource"} and _FILENAME.fullmatch(text)
    ):
        if intro not in {"path", "file", "resource"} and not _FILENAME.fullmatch(
            text.rsplit("/", 1)[-1]
        ):
            return None, "slash-expression-without-path-cue-or-recognized-file-suffix"
        try:
            RepositoryResourceAddress(text)
        except ValueError:
            return None, "noncanonical-resource-address"
        if any(c.isspace() for c in text) or not re.fullmatch(
            r"[A-Za-z0-9_./-]+", text
        ):
            return None, "non-path-code-prose"
        return HintCategory.RESOURCE_ADDRESS, "code-address-v1"
    parts = text.split(".")
    if not all(p.isidentifier() and not keyword.iskeyword(p) for p in parts):
        return None, "not-a-supported-syntactic-reference"
    kinds = {
        "class": HintCategory.PYTHON_DIRECT_CLASS,
        "type": HintCategory.PYTHON_DIRECT_CLASS,
        "function": HintCategory.PYTHON_DIRECT_FUNCTION,
        "method": HintCategory.PYTHON_DIRECT_METHOD,
        "module": HintCategory.PYTHON_MODULE,
        "package": HintCategory.PYTHON_MODULE,
    }
    if intro in kinds:
        return kinds[intro], "explicit-api-introduction-v1"
    return (
        None,
        "no-explicit-api-introduction; dotted prose and bare CamelCase excluded",
    )


def extract(
    task: LocalizationTaskIdentity, text: str
) -> tuple[ExtractionDecision, ...]:
    """Retain every inline code decision and introduced unquoted path boundary."""
    spans: list[tuple[int, int, str, str]] = []
    fences = tuple((m.start(), m.end()) for m in _FENCES.finditer(text))
    for match in _CODE.finditer(text):
        start, end = match.span(1)
        prefix = text[max(0, start - 48) : start - 1]
        introduction = _INTRO.search(prefix)
        spans.append(
            (
                start,
                end,
                introduction.group(1).casefold() if introduction else "",
                "inline-code",
            )
        )
    for match in _UNQUOTED_PATH.finditer(text):
        start, end = match.span(1)
        if not any(a <= start < b for a, b, _, _ in spans):
            spans.append((start, end, "path", "introduced-path"))
    decisions = []
    for start, end, intro, form in sorted(spans):
        source = text[start:end]
        line_start = text.rfind("\n", 0, start) + 1
        if any(a <= start < b for a, b in fences):
            category, rule = None, "fenced-code-not-task-reference"
        elif text[line_start:start].startswith("Operational:"):
            category, rule = None, "operational-instruction-excluded"
        else:
            category, rule = _category(source, intro)
        span = TaskTextSpan(start, end)
        observation = (
            None
            if category is None
            else ExactHintObservation(
                task,
                source,
                span,
                f"{POLICY}/{rule}",
                form,
                category,
                TaskProvenance(
                    task.value, span, "Task text only; no repository lookup"
                ),
            )
        )
        decisions.append(ExtractionDecision(span, source, rule, observation))
    return tuple(decisions)


def caller_observation(  # noqa: PLR0913 -- explicit task-only review inputs
    task: LocalizationTaskIdentity,
    text: str,
    *,
    start: int,
    end: int,
    category: HintCategory,
    rationale: str,
) -> ExactHintObservation:
    """Admit caller review through an interface with task-only inputs."""
    span = TaskTextSpan(start, end)
    if end > len(text) or not rationale.strip():
        raise ValueError("Caller reference span/rationale invalid")
    return ExactHintObservation(
        task,
        text[start:end],
        span,
        "caller-task-review-v1",
        "caller-reviewed-task-syntax",
        category,
        TaskProvenance(task.value, span, rationale),
    )
