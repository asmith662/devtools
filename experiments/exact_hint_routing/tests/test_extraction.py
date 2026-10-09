# Copyright (c) 2026
# ruff: noqa: S101, D103, PT011 -- literal protocol prose or fixture assertions; formatter owns commas
"""Task-only rule boundaries, immutable spans, associations and identity."""

from dataclasses import FrozenInstanceError, replace

import pytest

from devtools.context.localization.identity import (
    LocalizationObligationIdentity,
    LocalizationTaskIdentity,
    TaskProvenance,
)
from experiments.exact_hint_routing.extraction import caller_observation, extract
from experiments.exact_hint_routing.models import HintAssociation, HintCategory
from experiments.exact_hint_routing.routing import admit
from experiments.exact_hint_routing.serialization import encode

TASK = LocalizationTaskIdentity("fixture-hint-syntax")


@pytest.mark.parametrize(
    ("text", "category"),
    [
        ("Read `src/pkg/native.py`.", "RESOURCE_ADDRESS"),
        ("Read file src/pkg/native.py", "RESOURCE_ADDRESS"),
        ("Update file `pyproject.toml`.", "RESOURCE_ADDRESS"),
        ("module `pkg.native`", "PYTHON_MODULE"),
        ("package `pkg.native`", "PYTHON_MODULE"),
        ("class `pkg.native.Target`", "PYTHON_DIRECT_CLASS"),
        ("type `Target`", "PYTHON_DIRECT_CLASS"),
        ("function `pkg.native.build`", "PYTHON_DIRECT_FUNCTION"),
        ("method `pkg.native.Target.run`", "PYTHON_DIRECT_METHOD"),
    ],
)
def test_supported_syntax(text: str, category: str) -> None:
    decisions = extract(TASK, text)
    hint = next(d.observation for d in decisions if d.observation)
    assert hint.category.value == category
    assert text[hint.span.start : hint.span.end] == hint.text
    assert extract(TASK, text) == decisions
    assert encode(hint) == encode(hint)
    assert replace(hint, rule="caller-other-rule").identity == hint.identity
    with pytest.raises(FrozenInstanceError):
        hint.text = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    "text",
    [
        "CamelCase prose and Capitalized Words",
        "`CamelCase`",
        "`version.one`",
        "`reasonable English phrase`",
        "`file.py`",
        "class `List[Target]`",
        "`../escape.py`",
        "`/absolute.py`",
        "`C:/drive.py`",
        "`src\\file.py`",
        "`src//file.py`",
        "``class Target``",
        "```module pkg.native```",
        "```python\nclass `pkg.native.Target`\n```",
        "Operational: `.local/codex-result.md` is never a scientific hint.",
        "function `pkg.native.fn()`",
        "class `None`",
        "`x/y`",
        "```python\nclass `pkg.native.Target`\n",
        "function `pkg.native.for`",
    ],
)
def test_false_positive_boundaries(text: str) -> None:
    assert all(d.observation is None for d in extract(TASK, text))


def test_unicode_spans_task_review_association() -> None:
    text = "é\nclass `pkg.native.Target` and class `Target`"
    hints = [d.observation for d in extract(TASK, text) if d.observation]
    full, bare = hints
    reviewed = caller_observation(
        TASK,
        text,
        start=full.span.start,
        end=full.span.end,
        category=HintCategory.PYTHON_DIRECT_CLASS,
        rationale="Task syntax only",
    )
    assert reviewed.identity == full.identity
    association = HintAssociation(
        full.identity,
        LocalizationObligationIdentity(TASK, "owner"),
        "Explicit task clause",
        full.provenance,
    )
    assert admit(full, association).locator is not None
    assert (
        admit(
            bare,
            HintAssociation(
                bare.identity,
                LocalizationObligationIdentity(TASK, "owner"),
                "Bare explicit class",
                bare.provenance,
            ),
        ).locator
        is None
    )
    with pytest.raises(ValueError):
        admit(full, replace(association, hint=bare.identity))
    with pytest.raises(ValueError):
        replace(full, provenance=TaskProvenance("foreign"))
    with pytest.raises(ValueError):
        caller_observation(
            TASK,
            text,
            start=0,
            end=len(text) + 1,
            category=HintCategory.PYTHON_MODULE,
            rationale="invalid",
        )
