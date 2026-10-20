# Copyright (c) 2026
# ruff: noqa: D103, F811 -- actual bounded edit admission fixtures
"""Flat calls reuse exact atomic admission; no inference or fuzzy repair."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from apps.qwen.context_tools import ContextRequestError, ContextTools
from apps.qwen.edits import admit_observed, observed_definition
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.models.interaction import ModelToolCall
from tests.apps.qwen.test_context_tools import dispatch, tools  # noqa: F401

if TYPE_CHECKING:
    from typing import Any


def native(ref: str, old: str, new: str, identity: str = "edit") -> ModelToolCall:
    return ModelToolCall(
        "replace_source",
        json.dumps({"reference": ref, "old_text": old, "new_text": new}),
        identity,
    )


def test_path_read_reuses_versioned_materialization_and_absence(
    tools: ContextTools,
) -> None:
    task = replace(tools.task, new_paths=("src/devtools/new.py",))
    direct = ContextTools(tools.root, task, direct_reads=True)
    first = dispatch(direct, "inspect_source", path=task.source, start=0)
    assert first["version"] == str(direct.snapshot.resources[0].content_identity)
    assert first["text"] == direct.snapshot.resources[0].content
    assert first["edit_ref"]
    bad = dispatch(
        direct,
        "inspect_source",
        path=task.source,
        start=len(first["text"]) + 1,
    )
    assert bad["error"] == "SOURCE_RANGE_OUT_OF_BOUNDS"
    absent = dispatch(direct, "inspect_source", path=task.new_paths[0], start=0)
    assert absent["status"] == "ABSENT"
    assert absent["edit_ref"]
    with pytest.raises(ValueError, match="Unauthorized"):
        dispatch(direct, "inspect_source", path="src/devtools/private.py", start=0)


def test_direct_continuation_and_empty_source(tools: ContextTools) -> None:
    path = tools.root / tools.task.source
    content = "# " + "雪" * 2500 + "\n"
    path.write_bytes(content.encode())
    direct = ContextTools(tools.root, tools.task, direct_reads=True)
    names = {d.name for d in direct.definitions}
    assert "inspect_source" in names
    assert "read_source" not in names
    first = dispatch(direct, "inspect_source", path=tools.task.source, start=0)
    maximum_bytes = 4096
    assert first["truncated"]
    assert first["bytes"] <= maximum_bytes
    second = dispatch(
        direct,
        "inspect_source",
        path=tools.task.source,
        start=first["continuation_start"],
    )
    assert first["text"] + second["text"] == content
    assert not second["truncated"]
    assert first["edit_ref"] != second["edit_ref"]
    path.write_bytes(b"")
    empty = ContextTools(tools.root, tools.task, direct_reads=True)
    observation = dispatch(empty, "inspect_source", path=tools.task.source, start=0)
    assert observation["text"] == ""
    assert observation["span"] == [0, 0]
    assert not observation["truncated"]


def test_safe_feedback_keeps_integrity_failures_terminal(tools: ContextTools) -> None:
    operation = ModelToolCall("expand_source", "{}", "bad")
    with pytest.raises(ContextRequestError) as captured:
        dispatch(tools, "expand_source", unit=tools.task.source, to="file")
    result = tools.refusal(operation, captured.value)
    assert result["operation"] == "expand_source"
    assert result["error"] == "SOURCE_UNIT_MISMATCH"
    assert result["arguments_schema"]["required"] == ["unit", "to"]
    assert not tools.observations
    source = tools.root / tools.task.source
    source.write_bytes(b"# drift\n")
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        tools.refusal(operation, captured.value)


def test_missing_symbol_and_parent_have_recovery_guidance(tools: ContextTools) -> None:
    missing = dispatch(tools, "lookup_symbol", name="Missing.symbol")
    assert missing["status"] == "NOT_FOUND"
    assert not missing["matches"]
    assert "search_source" in missing["instruction"]
    found = dispatch(tools, "lookup_symbol", name="helper")["matches"][0]
    for target in ("class", "symbol"):
        with pytest.raises(ContextRequestError, match="no"):
            dispatch(tools, "expand_source", unit=found["unit"], to=target)


def read(tools: ContextTools) -> dict[str, Any]:
    source = tools.snapshot.resources[0]
    return dispatch(
        tools,
        "read_source",
        path=source.address.value,
        version=str(source.content_identity),
        start=0,
        end=len(source.content),
    )


def test_flat_shape_and_exact_anchor_resolution(tools: ContextTools) -> None:
    assert set(json.loads(observed_definition().input_schema_json)["properties"]) == {
        "reference",
        "old_text",
        "new_text",
    }
    o = read(tools)
    before = (tools.root / tools.task.source).read_text()
    patches, updated, evidence, _ = admit_observed(
        tools.root,
        {tools.task.source: before},
        (native(o["edit_ref"], "return 1", "return 2"),),
        tools,
    )
    assert updated[tools.task.source] == before.replace("return 1", "return 2")
    assert evidence[0]["observation"]["observation_call_id"] == "fixture-call"
    assert evidence[0]["observation_reference"] == o["edit_ref"]
    assert patches
    assert (tools.root / tools.task.source).read_text() == before
    assert read(tools)["edit_ref"] == o["edit_ref"]


@pytest.mark.parametrize(
    "failure",
    ["unknown", "overlap", "outside", "malformed", "suffix", "empty-batch", "schema"],
)
def test_entire_batch_refused_without_mutation(
    tools: ContextTools,
    failure: str,
) -> None:
    o = read(tools)
    before = (tools.root / tools.task.source).read_text()
    good = native(o["edit_ref"], "return 1", "return 2")
    bad = native("R999", "", "x", "bad")
    if failure == "overlap":
        bad = replace(good, provider_call_id="bad")
    if failure == "outside":
        bad = native(o["edit_ref"], "never seen", "x", "bad")
    if failure == "suffix":
        bad = native(o["edit_ref"], 'return 1"}]}', "x", "bad")
    if failure == "malformed":
        bad = replace(bad, arguments_json='{"reference":"R1","reference":"R2"}')
    if failure == "schema":
        bad = replace(
            bad,
            arguments_json='{"reference":false,"old_text":"","new_text":"x"}',
        )
    with pytest.raises(PatchProposalError):
        admit_observed(
            tools.root,
            {tools.task.source: before},
            () if failure == "empty-batch" else (good, bad),
            tools,
        )
    assert (tools.root / tools.task.source).read_text() == before


def test_version_drift_and_refreshed_evidence(tools: ContextTools) -> None:
    o = read(tools)
    path = tools.task.source
    before = (tools.root / path).read_text()
    _, updates, edits, _ = admit_observed(
        tools.root,
        {path: before},
        (native(o["edit_ref"], "return 1", "return 2"),),
        tools,
    )
    (tools.root / path).write_bytes(updates[path].encode())
    tools.accept_transaction(updates, edits, call_id="edit")
    with pytest.raises(PatchProposalError, match="Stale"):
        admit_observed(
            tools.root,
            updates,
            (native(o["edit_ref"], "return 1", "return 3"),),
            tools,
        )
    fresh = read(tools)
    assert fresh["edit_ref"] != o["edit_ref"]
    assert tools.edit_references[o["edit_ref"]]["version"] == o["version"]


def test_wrong_observation_region_reports_exact_handle_without_mutation(
    tools: ContextTools,
) -> None:
    before = (tools.root / tools.task.source).read_bytes()
    observation = dispatch(
        tools,
        "read_source",
        path=tools.task.source,
        version=str(tools.snapshot.resources[0].content_identity),
        start=0,
        end=10,
    )
    with pytest.raises(PatchProposalError, match=r"R1 .*span \[0, 10\)"):
        admit_observed(
            tools.root,
            {tools.task.source: before.decode()},
            (native(observation["edit_ref"], "return 1", "return 2"),),
            tools,
        )
    assert (tools.root / tools.task.source).read_bytes() == before


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_unicode_whole_region_and_new_file(tools: ContextTools, newline: str) -> None:
    path = tools.task.source
    before = 'value = "café🦊"' + newline
    (tools.root / path).write_bytes(before.encode())
    new = "src/devtools/created.py"
    task = replace(tools.task, new_paths=(new,))
    tools = ContextTools(tools.root, task)
    o = read(tools)
    absent = dispatch(tools, "inspect_new_source", path=new)
    _, updates, metadata, _ = admit_observed(
        tools.root,
        {path: before, new: ""},
        (
            native(o["edit_ref"], "", 'value = "雪"\n'),
            native(absent["edit_ref"], "", '"""Created source."""\n', "create"),
        ),
        tools,
    )
    assert updates[path] == 'value = "雪"' + newline
    assert metadata[1]["created"]
    assert not (tools.root / new).exists()
