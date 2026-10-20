# Copyright (c) 2026
# ruff: noqa: D103, F811 -- actual bounded edit admission fixtures
"""Flat calls reuse exact atomic admission; no inference or fuzzy repair."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from apps.qwen.context_tools import ContextTools
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
