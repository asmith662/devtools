# Copyright (c) 2026
# ruff: noqa: D103 -- independently specified public host behavior
"""Protect native refusal order and whole-batch behavior across owner extraction."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding import edits, repository, run_coding_agent
from devtools.context import RepositoryResourceAddress
from tests.agents.coding.fixtures import SOURCE
from tests.agents.coding.test_repository import (
    EDIT,
    LIMITS,
    READ,
    Script,
    call,
    host_at,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping
    from pathlib import Path


@pytest.mark.parametrize("operation_limit", [1, 2])
def test_earlier_admission_refusal_precedes_later_bad_arguments(
    tmp_path: Path,
    operation_limit: int,
) -> None:
    host = host_at(tmp_path)
    host.objective = replace(
        host.objective,
        edits=replace(host.objective.edits, operations=operation_limit),
    )
    foreign = call(
        "replace_source",
        {"path": "outside.py", "old_text": "return 6", "new_text": "return 7"},
        "foreign",
    )
    malformed = call("replace_source", {}, "bad-members")
    result = asyncio.run(
        run_coding_agent(
            Script([(READ,), (foreign, malformed)]),
            limits=LIMITS,
            host=host,
        ),
    )
    assert result.disposition == "proposal_limit"
    assert not result.accepted
    assert result.custody.restored
    reason = (
        "Edit operation limit exceeded."
        if operation_limit == 1
        else "Edit path is outside the admitted editing surface."
    )
    assert [m.tool_call_id for m in host.messages[-2:]] == ["foreign", "bad-members"]
    assert all(
        json.loads(m.content) == {"status": "REFUSED", "reason": reason}
        for m in host.messages[-2:]
    )
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
    assert len(result.progress.effects) == 1  # the source read, no edit dispatch


@pytest.mark.parametrize("refuse", [False, True])
def test_actual_host_delegates_admission_before_effects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    *,
    refuse: bool,
) -> None:
    host = host_at(tmp_path)
    entered = []

    def boundary(
        arguments: Iterable[Mapping[str, object]],
        **values: Any,  # noqa: ANN401 -- transparent real admission boundary
    ) -> tuple[edits.SourceChange, ...]:
        assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
        entered.append(values["snapshot"].id)
        if refuse:
            message = "Independent admission boundary refused."
            raise edits.CodingEditError(message)
        return edits.admit_source_batch(arguments, **values)

    monkeypatch.setattr(repository, "admit_source_batch", boundary)
    result = asyncio.run(
        run_coding_agent(Script([(READ,), (EDIT,)]), limits=LIMITS, host=host),
    )
    assert entered == [host.objective.scope.snapshot.id]
    assert result.accepted is not refuse
    assert result.custody.restored
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
    if refuse:
        assert json.loads(host.messages[-1].content) == {
            "status": "REFUSED",
            "reason": "Independent admission boundary refused.",
        }
        assert len(result.progress.effects) == 1


def test_maintained_imports_and_change_projection() -> None:
    assert repository.EditLimits is edits.EditLimits
    assert repository.SourceChange is edits.SourceChange
    change = repository.SourceChange(RepositoryResourceAddress("a.py"), "a", "b", 0, 1)
    assert asdict(change) == {
        "address": {"value": "a.py"},
        "before": "a",
        "after": "b",
        "start": 0,
        "end": 1,
    }


def test_small_edit_still_obeys_independent_complete_file_bound() -> None:
    source = "#" * 32768 + "\nreturn 6\n"
    with pytest.raises(edits.CodingEditError, match="bounded source size") as error:
        edits.replace_exact_text(
            source,
            "return 6",
            "return 7",
            region_bytes=16,
            source_bytes=32768,
        )
    assert error.value.details == {
        "code": "SOURCE_BYTE_LIMIT",
        "source_bytes": 32778,
        "source_limit_bytes": 32768,
    }
    # The shared primitive has caller bounds, not a hardcoded 32 KiB default.
    updated, start, end = edits.replace_exact_text(
        source,
        "return 6",
        "return 7",
        region_bytes=16,
        source_bytes=40000,
    )
    assert updated == "#" * 32768 + "\nreturn 7\n"
    assert (start, end) == (32769, 32777)
