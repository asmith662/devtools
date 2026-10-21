# Copyright (c) 2026
# ruff: noqa: D103, F811 -- actual bounded edit admission fixtures
"""Flat calls reuse exact atomic admission; no inference or fuzzy repair."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from apps.qwen import coding_loop
from apps.qwen.context_tools import ContextRequestError, ContextTools
from apps.qwen.continuation import present_sources
from apps.qwen.edits import admit_observed, observed_definition, transaction_definition
from apps.qwen.patch_proposal_worker import PatchProposalError
from apps.qwen.tasks import MARKDOWN
from devtools.models.interaction import (
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from tests.apps.qwen.test_coding_loop import GOOD, OLD, Scripted
from tests.apps.qwen.test_context_tools import dispatch, tools  # noqa: F401

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path
    from typing import Any

    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelRequest


def native(ref: str, old: str, new: str, identity: str = "edit") -> ModelToolCall:
    return ModelToolCall(
        "replace_source",
        json.dumps({"reference": ref, "old_text": old, "new_text": new}),
        identity,
    )


def by_path(path: str, old: str, new: str, identity: str = "edit") -> ModelToolCall:
    return ModelToolCall(
        "replace_source",
        json.dumps({"path": path, "old_text": old, "new_text": new}),
        identity,
    )


@pytest.mark.parametrize("succeed", [True, False])
def test_native_six_proposals_are_bounded_and_correlated(
    *,
    succeed: bool,
    captured_inputs: Callable[[CodingTask], Path],
    tmp_path: Path,
) -> None:
    """Five refusals can be repaired at six, while a seventh never dispatches."""
    task = replace(
        MARKDOWN,
        context_mode="on-demand",
        maximum_calls=8,
        maximum_proposals=6,
        path_edits=True,
    )
    root = captured_inputs(task)
    source = (root / task.source).read_text()
    first_edit = 2
    final_request = task.maximum_proposals + 1

    class Sixth(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            number = len(self.requests)
            if number == 1:
                schema = json.loads(request.tools[0].input_schema_json)
                assert "path" in schema["required"]
                native_call = ModelToolCall(
                    "inspect_source",
                    json.dumps(
                        {"path": task.source, "start": max(0, source.index(OLD) - 50)},
                    ),
                    "read",
                )
            else:
                if number == first_edit:
                    assert "EXACT SOURCE BLOCK" in request.prompt.messages[-1].content
                    assert OLD in request.prompt.messages[-1].content
                if number == final_request:
                    feedback = json.loads(request.prompt.messages[-1].content)
                    assert feedback["host_limits"]["proposals_remaining"] == 1
                    assert "path" in feedback["instruction"]
                native_call = by_path(
                    task.source,
                    OLD if number == final_request and succeed else "NOT_SOURCE",
                    GOOD,
                )
            return ModelResponse("scripted", self.source, tool_calls=(native_call,))

    model = Sixth([])
    result = asyncio.run(
        coding_loop.run_coding_task(
            root,
            tmp_path / "six",
            model,
            task=task,
            coordinated_edits=True,
            observed_edits=True,
        ),
    )
    assert result["accepted"] is succeed
    assert result["limits"]["proposals"] == task.maximum_proposals
    assert result["proposals_attempted"] == task.maximum_proposals
    expected_requests = 7
    assert len(model.requests) == expected_requests
    assert result["original_unchanged"]


@pytest.mark.parametrize("value", [0, 7, True, 1.5])
def test_native_proposal_limits_refuse_invalid_configuration(value: object) -> None:
    """Model-facing budgets are authenticated host integers, never soft hints."""
    with pytest.raises(ValueError, match="bounded native"):
        replace(
            MARKDOWN,
            context_mode="on-demand",
            maximum_proposals=cast("int", value),
        )
    with pytest.raises(ValueError, match="bounded native"):
        replace(MARKDOWN, maximum_proposals=6)
    assert MARKDOWN.maximum_proposals == 3  # noqa: PLR2004 -- durable legacy default


def test_path_anchor_resolves_observed_union_without_redirecting_legacy(
    tools: ContextTools,
) -> None:
    path = tools.task.source
    tools = ContextTools(tools.root, replace(tools.task, path_edits=True))
    source = tools.snapshot.resources[0].content
    version = str(tools.snapshot.resources[0].content_identity)
    split = source.index("return 1") + 3
    first = dispatch(
        tools,
        "read_source",
        path=path,
        version=version,
        start=0,
        end=split,
    )
    dispatch(
        tools,
        "read_source",
        path=path,
        version=version,
        start=split,
        end=len(source),
    )
    with pytest.raises(PatchProposalError, match="outside referenced"):
        admit_observed(
            tools.root,
            {path: source},
            (native(first["edit_ref"], "return 1", "return 2"),),
            tools,
        )
    _, updates, edits, plan = admit_observed(
        tools.root,
        {path: source},
        (by_path(path, "return 1", "return 2"),),
        tools,
    )
    assert "return 2" in updates[path]
    assert edits[0]["anchor_mode"] == "path-observed-union"
    expected_regions = 2
    assert len(edits[0]["observation_references"]) == expected_regions
    assert (
        len(plan["resolved_observations"][0]["supporting_observations"])
        == expected_regions
    )
    assert (tools.root / path).read_text() == source


@pytest.mark.parametrize(
    "failure",
    ["unobserved", "contaminated", "empty", "ambiguous", "unauthorized", "oversize"],
)
def test_path_anchor_refusals_are_atomic(tools: ContextTools, failure: str) -> None:
    path = tools.task.source
    before = (tools.root / path).read_text()
    if failure == "ambiguous":
        before += "\ndef another():\n    return 1\n"
        (tools.root / path).write_bytes(before.encode())
    tools = ContextTools(tools.root, replace(tools.task, path_edits=True))
    if failure != "unobserved":
        read(tools)
    target = tools.task.tests[0] if failure == "unauthorized" else path
    old = {"contaminated": 'return 1\\",\\"host_projection\\":{}', "empty": ""}.get(
        failure,
        "return 1",
    )
    replacement = "x" * 4097 if failure == "oversize" else "return 2"
    with pytest.raises(PatchProposalError):
        admit_observed(
            tools.root,
            {path: before},
            (
                by_path(path, "class Demo:", "class DemoNew:", "valid-component"),
                by_path(target, old, replacement),
            ),
            tools,
        )
    assert (tools.root / path).read_text() == before


def test_path_anchor_drift_and_current_observation_attestation(
    tools: ContextTools,
) -> None:
    path = tools.task.source
    tools = ContextTools(tools.root, replace(tools.task, path_edits=True))
    read(tools)
    before = (tools.root / path).read_text()
    changed = before.replace("return 1", "return 2")
    (tools.root / path).write_bytes(changed.encode())
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        admit_observed(
            tools.root,
            {path: changed},
            (by_path(path, "return 2", "return 3"),),
            tools,
        )
    tools.accept_source(changed)
    with pytest.raises(PatchProposalError, match="not observed"):
        admit_observed(
            tools.root,
            {path: changed},
            (by_path(path, "return 2", "return 3"),),
            tools,
        )
    read(tools)
    tools.observations[0]["text"] = "#" + tools.observations[0]["text"][1:]
    with pytest.raises(PatchProposalError, match="attestation mismatch"):
        admit_observed(
            tools.root,
            {path: changed},
            (by_path(path, "return 2", "return 3"),),
            tools,
        )
    assert (tools.root / path).read_text() == changed


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_path_anchor_creation_and_atomic_overlap(
    tools: ContextTools,
    newline: str,
) -> None:
    path = tools.task.source
    before = 'value = "caf\u00e9\U0001f98a"' + newline
    (tools.root / path).write_bytes(before.encode())
    new = "src/devtools/created.py"
    tools = ContextTools(
        tools.root,
        replace(tools.task, path_edits=True, new_paths=(new,)),
    )
    read(tools)
    sources = {path: before, new: ""}
    calls = (
        by_path(path, 'value = "caf\u00e9\U0001f98a"\n', 'value = "\u96ea"\n'),
        by_path(new, "", '"""Created source."""\n', "create"),
    )
    with pytest.raises(PatchProposalError, match="absence"):
        admit_observed(tools.root, sources, calls, tools)
    dispatch(tools, "inspect_new_source", path=new)
    _, updates, edits, _ = admit_observed(tools.root, sources, calls, tools)
    assert updates[path] == 'value = "\u96ea"' + newline
    assert edits[1]["created"]
    with pytest.raises(PatchProposalError, match="Overlapping"):
        admit_observed(tools.root, sources, (calls[0], calls[0]), tools)
    assert not (tools.root / new).exists()
    assert (tools.root / path).read_bytes() == before.encode()


def test_path_schema_and_source_blocks_preserve_exact_text_and_native_identity() -> (
    None
):
    schema = json.loads(observed_definition(path_based=True).input_schema_json)
    assert set(schema["required"]) == {"path", "old_text", "new_text"}
    assert "reference" not in schema["properties"]
    source = 'value = "\u96ea"\n# ``` must not terminate the host fence\n'
    result = {
        "path": "src/devtools/demo.py",
        "version": "v1",
        "span": [0, len(source)],
        "text": source,
        "host_projection": {"original_tool_call_id": "read"},
    }
    original = PromptMessage("tool", json.dumps(result), tool_call_id="read")
    assistant = PromptMessage(
        "assistant",
        "",
        (ModelToolCall("inspect_source", "{}", "read"),),
    )
    selected = present_sources((assistant, original))
    Prompt("", "messages", selected)
    assert selected[0] is assistant
    assert selected[1].tool_call_id == original.tool_call_id
    metadata, code = selected[1].content.split("\n\n", 1)
    assert "host_projection" in metadata
    assert "host_projection" not in code
    assert "````python\n" + source + "````" in code
    assert original.content == json.dumps(result)
    assert (
        present_sources((PromptMessage("tool", "invalid JSON", tool_call_id="x"),))[
            0
        ].content
        == "invalid JSON"
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


def test_sixteen_small_anchors_share_one_atomic_bounded_operation(
    tools: ContextTools,
) -> None:
    count = 16
    assert "16" in observed_definition().description
    assert (
        json.loads(transaction_definition(tools.task.sources).input_schema_json)[
            "properties"
        ]["edits"]["maxItems"]
        == count
    )
    before = "".join(f"value_{i} = 0\n" for i in range(count))
    (tools.root / tools.task.source).write_bytes(before.encode())
    current = ContextTools(tools.root, tools.task, direct_reads=True)
    observation = dispatch(
        current,
        "inspect_source",
        path=tools.task.source,
        start=0,
    )
    calls = tuple(
        native(observation["edit_ref"], f"value_{i} = 0", f"value_{i} = 1", str(i))
        for i in range(count)
    )
    _, updates, metadata, _ = admit_observed(
        tools.root,
        {tools.task.source: before},
        calls,
        current,
    )
    assert len(metadata) == count
    assert updates[tools.task.source] == "".join(
        f"value_{i} = 1\n" for i in range(count)
    )
    assert (tools.root / tools.task.source).read_bytes() == before.encode()
    with pytest.raises(PatchProposalError, match="sixteen"):
        admit_observed(
            tools.root,
            {tools.task.source: before},
            (*calls, calls[0]),
            current,
        )
    assert (tools.root / tools.task.source).read_bytes() == before.encode()


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
