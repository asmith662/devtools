# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004, F811 -- bounded scripted host regressions
"""Actual scoped Git application, installed API observations and native repair."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

from apps.qwen import coding_loop
from apps.qwen.api_contracts import inspect_contract
from apps.qwen.context_tools import ContextTools
from apps.qwen.continuation import select_messages
from apps.qwen.development_task import apply_source_patches
from apps.qwen.edits import admit_transaction, transaction_definition
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.models.interaction import (
    InteractionSource,
    ModelResponse,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from tests.apps.qwen.test_context_tools import dispatch, tools  # noqa: F401

if TYPE_CHECKING:
    from apps.qwen.tasks import CodingTask
    from devtools.models.interaction import ModelRequest


@pytest.fixture
def bundle(tools: ContextTools) -> ContextTools:
    path = "src/devtools/other.py"
    target = tools.root / path
    target.write_bytes(b"def value():\n    return 3\n")
    task = replace(
        tools.task,
        additional_edit_paths=(path,),
        baseline_hashes=(
            *tools.task.baseline_hashes,
            (path, hashlib.sha256(target.read_bytes()).hexdigest()),
        ),
        context=(*tools.task.context, (path, "value", "symbol", "file")),
        api_targets=("bytes.decode",),
    )
    return ContextTools(tools.root, task)


def observe_all(bundle: ContextTools) -> None:
    for resource in bundle.snapshot.resources:
        dispatch(
            bundle,
            "read_source",
            path=resource.address.value,
            version=str(resource.content_identity),
            start=0,
            end=len(resource.content),
        )


def proposal(bundle: ContextTools) -> ModelToolCall:
    api = dispatch(bundle, "inspect_api", target="bytes.decode")
    rows = []
    for resource in bundle.snapshot.resources:
        if resource.address.value not in bundle.task.sources:
            continue
        rows.append(
            {
                "path": resource.address.value,
                "version": str(resource.content_identity),
                "old_text": "return 1"
                if resource.address.value == bundle.task.source
                else "return 3",
                "new_text": "return 2"
                if resource.address.value == bundle.task.source
                else "return 4",
            }
        )
    rows.append(
        {
            **rows[0],
            "old_text": "def caller():\n    return helper()",
            "new_text": "def caller():\n    return helper() + 1",
        }
    )
    return ModelToolCall(
        "propose_edits",
        json.dumps(
            {
                "plan": "Coordinate the observed helpers and caller; preserve class.",
                "api_evidence": [api["observation_id"]],
                "edits": rows,
            }
        ),
        "transaction-1",
    )


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_atomic_regions_files_source_refresh_and_exact_outside_bytes(
    bundle: ContextTools, tmp_path: Path, newline: str
) -> None:
    for path in bundle.task.sources:
        target = bundle.root / path
        target.write_bytes(target.read_bytes().decode().replace("\n", newline).encode())
    bundle = ContextTools(bundle.root, bundle.task)
    observe_all(bundle)
    before = {p: (bundle.root / p).read_bytes() for p in bundle.task.sources}
    sources = {p: b.decode() for p, b in before.items()}
    call = proposal(bundle)
    patches, updates, metadata, plan = admit_transaction(
        bundle.root, sources, call, bundle
    )
    assert len(metadata) == 3
    assert len(patches) == 2
    assert plan["api_evidence"]
    assert before == {p: (bundle.root / p).read_bytes() for p in sources}
    folder = tmp_path / "patch"
    folder.mkdir()
    asyncio.run(apply_source_patches(bundle.root, folder, patches))
    assert {p: (bundle.root / p).read_bytes().decode() for p in sources} == updates
    bundle.accept_transaction(updates, metadata, call_id=call.provider_call_id)
    assert bundle.observed("class Demo")
    assert bundle.observed("return 4", path=bundle.task.additional_edit_paths[0])
    assert not bundle.observed("return 1")
    assert (
        (bundle.root / bundle.task.source)
        .read_bytes()
        .startswith(before[bundle.task.source].split(b"return 1")[0])
    )
    for observation in bundle.observations:
        resource = next(
            r
            for r in bundle.snapshot.resources
            if r.address.value == observation["path"]
        )
        assert observation["text"] == resource.content[slice(*observation["span"])]
        assert observation["version"] == str(resource.content_identity)
    assert transaction_definition(bundle.task.sources).name == "propose_edits"


@pytest.mark.parametrize(
    "failure",
    [
        "stale",
        "overlap",
        "duplicate",
        "path",
        "unobserved",
        "absent",
        "ambiguous",
        "size",
        "api",
        "missing-api",
        "schema",
        "drift",
    ],
)
def test_transaction_rejects_all_components_without_partial_mutation(  # noqa: C901 -- exhaustive refusal matrix
    bundle: ContextTools, failure: str
) -> None:
    observe_all(bundle)
    call = proposal(bundle)
    values = json.loads(call.arguments_json)
    if failure == "stale":
        values["edits"][-1]["version"] = "0" * 64
    elif failure in {"overlap", "duplicate"}:
        values["edits"].append(values["edits"][0])
    elif failure == "path":
        values["edits"][-1]["path"] = "../outside.py"
    elif failure == "unobserved":
        bundle.observations.clear()
    elif failure == "absent":
        values["edits"][-1]["old_text"] = "invented source"
    elif failure == "ambiguous":
        values["edits"][-1]["old_text"] = "return helper()"
    elif failure == "size":
        values["edits"][-1]["new_text"] = "x" * 4097
    elif failure == "api":
        values["api_evidence"] = ["0" * 64]
    elif failure == "missing-api":
        values["api_evidence"] = []
    elif failure == "schema":
        values["edits"][-1]["extra"] = "no authority"
    else:
        (bundle.root / bundle.task.source).write_bytes(b"external drift\n")
    original = {p: (bundle.root / p).read_bytes() for p in bundle.task.sources}
    with pytest.raises((PatchProposalError, ValueError)):
        admit_transaction(
            bundle.root,
            {p: b.decode() for p, b in original.items()},
            replace(call, arguments_json=json.dumps(values)),
            bundle,
        )
    assert original == {p: (bundle.root / p).read_bytes() for p in original}


def test_git_preflight_refuses_the_entire_combined_patch_on_drift(
    bundle: ContextTools, tmp_path: Path
) -> None:
    observe_all(bundle)
    sources = {p: (bundle.root / p).read_bytes().decode() for p in bundle.task.sources}
    patches, _, _, _ = admit_transaction(bundle.root, sources, proposal(bundle), bundle)
    (bundle.root / bundle.task.additional_edit_paths[0]).write_bytes(
        b"external change\n"
    )
    before = {p: (bundle.root / p).read_bytes() for p in bundle.task.sources}
    folder = tmp_path / "refused-application"
    folder.mkdir()
    with pytest.raises(PatchProposalError):
        asyncio.run(apply_source_patches(bundle.root, folder, patches))
    assert before == {p: (bundle.root / p).read_bytes() for p in before}


def test_installed_api_contract_is_real_bounded_and_not_arbitrary_execution(
    bundle: ContextTools,
) -> None:
    loads = inspect_contract("json.loads", ("json.loads",))
    decoder = inspect_contract("json.JSONDecoder", ("json.JSONDecoder",))
    assert "object_pairs_hook" in decoder["signature"]
    assert "parse_object" not in decoder["signature"]
    assert loads["delegated_decoder_signature"] == decoder["signature"]
    assert len(loads["observation_id"]) == 64
    assert loads["package_version"]
    assert loads["docstring"]
    assert loads == inspect_contract("json.loads", ("json.loads",))
    assert dispatch(bundle, "inspect_api", target="bytes.decode")["observation_id"]
    for target in ("os.system", "json.loads", "__import__('os')", "bytes.__class__"):
        with pytest.raises(ValueError, match="must be one of"):
            dispatch(bundle, "inspect_api", target=target)


def test_transaction_deletion_reuses_strict_admission_without_unanchored_writes(
    bundle: ContextTools,
) -> None:
    observe_all(bundle)
    values = json.loads(proposal(bundle).arguments_json)
    values["edits"] = [
        {
            **values["edits"][0],
            "old_text": "\ndef caller():\n    return helper()\n",
            "new_text": "",
        }
    ]
    before = {p: (bundle.root / p).read_bytes().decode() for p in bundle.task.sources}
    call = ModelToolCall("propose_edits", json.dumps(values), "delete-1")
    _, updates, metadata, _ = admit_transaction(bundle.root, before, call, bundle)
    assert metadata[0]["new_length"] == 0
    assert updates[bundle.task.source] == before[bundle.task.source].replace(
        values["edits"][0]["old_text"], ""
    )
    assert before == {p: (bundle.root / p).read_bytes().decode() for p in before}
    with pytest.raises(PatchProposalError, match="Malformed"):
        admit_transaction(
            bundle.root,
            before,
            replace(call, arguments_json='{"plan":"a","plan":"b"}'),
            bundle,
        )


def test_api_evidence_is_retained_and_deduplicated_without_native_disconnection() -> (
    None
):
    observation = inspect_contract("json.loads", ("json.loads",))
    original = json.dumps(observation)
    history = [PromptMessage("user", "Preserve required behavior and API evidence")]
    for identity in ("first", "repeat"):
        history.extend(
            [
                PromptMessage(
                    "assistant",
                    "",
                    (
                        ModelToolCall(
                            "inspect_api", '{"target":"json.loads"}', identity
                        ),
                    ),
                ),
                PromptMessage("tool", original, tool_call_id=identity),
            ]
        )
    selected, omitted = select_messages(history, maximum_bytes=12000)
    Prompt("", "messages", selected)
    assert omitted == 0
    assert json.loads(selected[2].content)["signature"] == observation["signature"]
    assert "DUPLICATE" in selected[-1].content
    assert history[-1].content == original
    with pytest.raises(ValueError, match="budget"):
        select_messages(history, maximum_bytes=100)


class Engineering:
    """Scripted investigation/atomic edit/repair through actual host validation."""

    source = InteractionSource("scripted-atomic-engineering")

    def __init__(self, *, exhausted: bool = False, flat: bool = False) -> None:
        """Freeze one scripted validation/repair outcome."""
        self.requests: list[ModelRequest] = []
        self.exhausted = exhausted
        self.flat = flat

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Return correlated native calls driven by actual host observations."""
        self.requests.append(request)
        number = len(self.requests)
        source = InteractionSource("scripted-atomic-engineering")
        if number == 1:
            calls = tuple(
                ModelToolCall(
                    "lookup_symbol", json.dumps({"name": name}), f"lookup-{name}"
                )
                for name in ("helper", "value")
            )
            calls += (
                ModelToolCall("inspect_api", '{"target":"bytes.decode"}', "api-1"),
            )
        elif number == 2:
            values = [
                json.loads(m.content)
                for m in request.prompt.messages
                if m.role == "tool"
            ]
            hits = [v["matches"][0] for v in values if "matches" in v]
            calls = tuple(
                ModelToolCall(
                    "inspect_source" if self.flat else "read_source",
                    json.dumps(
                        {"path": h["path"], "start": h["span"][0]}
                        if self.flat
                        else {
                            "path": h["path"],
                            "version": h["version"],
                            "start": h["span"][0],
                            "end": h["span"][1],
                        }
                    ),
                    "read-" + str(i),
                )
                for i, h in enumerate(hits)
            )
        else:
            Prompt("", "messages", request.prompt.messages)
            values = [
                json.loads(m.content)
                for m in request.prompt.messages
                if m.role == "tool"
            ]
            api = next(v["observation_id"] for v in values if "observation_id" in v)
            observations = [
                o
                for v in values
                for o in [v, *v.get("source_observations", [])]
                if "text" in o
            ]
            if number > 3:
                feedback = next(v for v in reversed(values) if "validation" in v)
                assert feedback["validation"]["repair_contract"]["failed_checks"]
                assert (
                    len(feedback["validation"]["repair_contract"]["source_versions"])
                    == 2
                )
                assert feedback["sources_after"]
            rows = []
            for path in ("src/devtools/demo.py", "src/devtools/other.py"):
                if number > 3 and path.endswith("other.py"):
                    continue  # retain the already correct second-file behavior
                o = next(
                    o
                    for o in reversed(observations)
                    if o["path"] == path and "return" in o["text"]
                )
                if number == 3:
                    old = "return 1" if path.endswith("demo.py") else "return 3"
                    new = "return 3" if path.endswith("demo.py") else "return 4"
                else:
                    old = f"return {number - 1}"
                    new = f"return {number}" if self.exhausted else "return 2"
                rows.append(
                    {
                        "path": path,
                        "version": o["version"],
                        "old_text": old,
                        "new_text": new,
                    }
                )
            calls = (
                ModelToolCall(
                    "propose_edits",
                    json.dumps(
                        {
                            "plan": "Preserve secondary behavior; repair helper.",
                            "api_evidence": [api],
                            "edits": rows,
                        }
                    ),
                    f"edit-{number}",
                ),
            )
        if self.flat and number > 2:
            calls = tuple(
                ModelToolCall(
                    "replace_source",
                    json.dumps(
                        {
                            "reference": next(
                                o["edit_ref"]
                                for o in reversed(observations)
                                if o["path"] == row["path"]
                                and o["version"] == row["version"]
                                and row["old_text"] in o["text"]
                            ),
                            "old_text": row["old_text"],
                            "new_text": row["new_text"],
                        }
                    ),
                    f"flat-{number}-{i}",
                )
                for i, row in enumerate(rows)
            )
        return ModelResponse(
            "Observed-source implementation proposal.", source, tool_calls=calls
        )


@pytest.mark.parametrize("outcome", ["repair", "exhausted", "interrupted"])
@pytest.mark.parametrize("flat", [False, True])
def test_native_atomic_engineering_repair_restoration_and_interruption(
    bundle: ContextTools,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    outcome: str,
    *,
    flat: bool,
) -> None:
    root = bundle.root
    maintained = Path(__file__).resolve().parents[3] / "src/devtools"
    (root / "src/devtools/__init__.py").write_text(
        f"__path__ = {[str(root / 'src/devtools'), str(maintained)]!r}\n",
        encoding="utf-8",
    )
    test = root / bundle.task.tests[0]
    test.write_text(
        "from devtools.demo import helper\ndef test_baseline():\n"
        "    assert isinstance(helper(), int)\n",
        encoding="utf-8",
    )
    task = replace(
        bundle.task,
        maximum_calls=6,
        oracle=(
            "from devtools.other import value\n"
            "assert module.helper()==2 and value()==4\n"
        ),
        baseline_hashes=tuple(
            (p, hashlib.sha256((root / p).read_bytes()).hexdigest())
            for p, _ in bundle.task.baseline_hashes
        ),
    )
    before = {p: (root / p).read_bytes() for p in task.sources}

    async def authenticate(_root: Path, workspace: Path, task: CodingTask) -> None:
        for path, digest in task.baseline_hashes:
            assert hashlib.sha256((workspace / path).read_bytes()).hexdigest() == digest

    monkeypatch.setattr(coding_loop, "_authenticate_inputs", authenticate)
    if outcome == "interrupted":
        original = apply_source_patches

        async def interrupt(root: Path, folder: Path, patches: dict[str, str]) -> None:
            await original(root, folder, patches)
            raise asyncio.CancelledError

        monkeypatch.setattr("apps.qwen.turns.loop.apply_source_patches", interrupt)
    folder = tmp_path / "engineering"
    model = Engineering(exhausted=outcome == "exhausted", flat=flat)
    operation = coding_loop.run_coding_task(
        root, folder, model, task=task, coordinated_edits=True, observed_edits=flat
    )
    if outcome == "interrupted":
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(operation)
        result = json.loads((folder / "result.json").read_text())
        assert result["disposition"] == "HOST_CANCELLED"
        stage = json.loads((folder / "turn-03/stage.json").read_text())
        assert stage["proposed_sources"]
    else:
        result = asyncio.run(operation)
        assert result["accepted"] is (outcome == "repair"), result
        assert result["disposition"] == (
            "ACCEPTED" if outcome == "repair" else "REPAIR_BUDGET_EXHAUSTED"
        )
    assert result["source_restored"]
    assert result["original_unchanged"]
    assert len(result["candidates"]) == 2
    assert before == {p: (root / p).read_bytes() for p in before}
