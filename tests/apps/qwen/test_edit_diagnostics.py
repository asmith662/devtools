# Copyright (c) 2026
# ruff: noqa: COM812, D103, PLR2004, F811 -- independent deterministic admission fixtures
"""Component refusals preserve exact atomic admission; no model inference."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from apps.qwen.commands import CodingCommands
from apps.qwen.context_tools import ContextTools
from apps.qwen.development_task import _hash
from apps.qwen.edits import admit_observed, admit_transaction
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.context import RepositoryResourceAddress
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    ModelToolCall,
    Prompt,
)
from scripts.backlog.coordinator import designate, git
from scripts.qwen import coding_worker
from tests.apps.qwen.test_change_checks import _contract
from tests.apps.qwen.test_coding_loop import Scripted
from tests.apps.qwen.test_context_tools import dispatch, tools  # noqa: F401
from tests.apps.qwen.test_edits import bundle, observe_all  # noqa: F401

if TYPE_CHECKING:
    from pathlib import Path


@pytest.fixture
def scoped(bundle: ContextTools) -> ContextTools:
    task = replace(bundle.task, path_edits=True, new_paths=("src/devtools/created.py",))
    result = ContextTools(bundle.root, task)
    observe_all(result)
    dispatch(result, "inspect_api", target="bytes.decode")
    return result


def sources(scoped: ContextTools) -> dict[str, str]:
    return {
        p: (scoped.root / p).read_bytes().decode() if (scoped.root / p).exists() else ""
        for p in scoped.task.sources
    }


def change(
    path: str, old: object, new: object, identity: str = "edit-1"
) -> ModelToolCall:
    return ModelToolCall(
        "replace_source",
        json.dumps({"path": path, "old_text": old, "new_text": new}),
        identity,
    )


def reject(scoped: ContextTools, calls: tuple[ModelToolCall, ...]) -> dict[str, Any]:
    before = {
        p: (scoped.root / p).read_bytes() if (scoped.root / p).exists() else None
        for p in scoped.task.sources
    }
    with pytest.raises(PatchProposalError) as caught:
        admit_observed(scoped.root, sources(scoped), calls, scoped)
    assert before == {
        p: (scoped.root / p).read_bytes() if (scoped.root / p).exists() else None
        for p in scoped.task.sources
    }
    details = caught.value.details
    assert "old_text" not in details
    assert "new_text" not in details
    return details


@pytest.mark.parametrize(
    ("old", "new", "code", "new_bytes"),
    [
        ("return 3", "x" * 6584, "REGION_BYTE_LIMIT", 6584),
        ("return 3", "x" * 5871, "REGION_BYTE_LIMIT", 5871),
        ("return 3", "x" * 4864, "REGION_BYTE_LIMIT", 4864),
        ("return 3", "\u96ea" * 1400, "REGION_BYTE_LIMIT", 4200),
        ("return 3", "return 3", "NO_OP", 8),
        ("NOT_REAL_SOURCE", "return 4", "OLD_TEXT_NOT_UNIQUE", 8),
        # Engineering22's anchor belongs to the other owner, not this path.
        ("return 1", "return 4", "OLD_TEXT_NOT_UNIQUE", 8),
        ("return 3", "\0", "NUL_TEXT", 1),
        ("", "return 4", "EMPTY_TEXT", 8),
    ],
)
def test_historical_failure_classes_identify_original_component(
    scoped: ContextTools, old: str, new: str, code: str, new_bytes: int
) -> None:
    secondary = scoped.task.additional_edit_paths[0]
    details = reject(
        scoped,
        (
            change(scoped.task.source, "return 1", "return 2"),
            change(secondary, old, new, "offending-native-call"),
        ),
    )
    assert details["component_index"] == 2
    assert details["index_base"] == 1
    assert details["proposal_call_id"] == "offending-native-call"
    assert details["path"] == secondary
    assert details["code"] == code
    assert details["old_bytes"] == len(old.encode())
    assert details["new_bytes"] == new_bytes
    assert details["region_limit_bytes"] == 4096
    assert details["match_scope"] == "current_disclosed_regions"
    if code == "NO_OP":
        assert details["no_op"]
    if code == "OLD_TEXT_NOT_UNIQUE":
        assert details["observed_match_count"] == 0
        assert scoped.task.source not in json.dumps(details)


@pytest.mark.parametrize("create", [False, True])
def test_aggregate_overflow_reports_crossing_component_and_actual_bytes(
    scoped: ContextTools, *, create: bool
) -> None:
    secondary = (
        scoped.task.new_paths[0] if create else scoped.task.additional_edit_paths[0]
    )
    if create:
        dispatch(scoped, "inspect_new_source", path=secondary)
    details = reject(
        scoped,
        (
            change(scoped.task.source, "return 1", "a" * 4096),
            change(secondary, "" if create else "return 3", "b" * 4096, "edit-2"),
        ),
    )
    assert details["code"] == "AGGREGATE_BYTE_LIMIT"
    assert details["component_index"] == 2
    assert details["aggregate_bytes_through_component"] == (8200 if create else 8208)
    assert details["aggregate_limit_bytes"] == 8192


def test_overlap_names_both_original_indices(scoped: ContextTools) -> None:
    details = reject(
        scoped,
        (
            change(scoped.task.source, "return 1", "return 2"),
            change(
                scoped.task.source,
                "def helper():\n    return 1",
                "def helper():\n    return 5",
                "edit-2",
            ),
        ),
    )
    assert details["code"] == "OVERLAPPING_COMPONENTS"
    assert details["overlapping_components"] == [1, 2]
    assert details["component_index"] == 2


def test_unauthorized_path_does_not_disclose_source_or_match_information(
    scoped: ContextTools,
) -> None:
    details = reject(
        scoped,
        (
            change(scoped.task.source, "return 1", "return 2"),
            change("../private.py", "SECRET", "something", "bad"),
        ),
    )
    assert details == {
        "code": "UNAUTHORIZED_PATH",
        "component_index": 2,
        "index_base": 1,
        "proposal_call_id": "bad",
    }


def test_counts_are_limited_to_disclosed_unions_and_do_not_duplicate_reads(
    scoped: ContextTools,
) -> None:
    path = scoped.task.source
    # The same text occurs twice physically, but only one occurrence is disclosed.
    scoped.observations[:] = [o for o in scoped.observations if o["path"] != path]
    source = scoped.snapshot.resource_at(RepositoryResourceAddress(path))
    start = source.content.index("return helper()")
    for _ in range(2):
        dispatch(
            scoped,
            "read_source",
            path=path,
            version=str(source.content_identity),
            start=start,
            end=start + len("return helper()"),
        )
    details = reject(scoped, (change(path, "return helper()", "return 2"),))
    assert details["code"] == "OLD_TEXT_NOT_UNIQUE"
    assert details["observed_match_count"] == 1
    assert "source_match_count" not in details
    assert "return helper()" not in json.dumps(details)
    # Repeated/overlapping observations contribute one union, not repeated matches.
    observe_all(scoped)
    details = reject(scoped, (change(path, "return helper()", "return 2"),))
    assert details["observed_match_count"] == 2


def test_unobserved_source_does_not_disclose_its_current_identity(
    scoped: ContextTools,
) -> None:
    path = scoped.task.additional_edit_paths[0]
    scoped.observations[:] = [o for o in scoped.observations if o["path"] != path]
    details = reject(scoped, (change(path, "return 3", "return 4"),))
    assert details["code"] == "OBSERVATION_MISSING"
    assert details["observed_match_count"] == 0
    assert not details["source_observed"]
    assert "observed_source_version" not in details


@pytest.mark.parametrize("stale", [False, True])
def test_new_file_absence_authority_and_version_are_not_invented(
    scoped: ContextTools, *, stale: bool
) -> None:
    path = scoped.task.new_paths[0]
    if not stale:
        details = reject(scoped, (change(path, "", "VALUE = 1\n"),))
        assert details["code"] == "ABSENCE_NOT_OBSERVED"
        assert not details["absence_observed"]
        assert "observed_absence_version" not in details
        return
    absence = dispatch(scoped, "inspect_new_source", path=path)
    call = ModelToolCall(
        "propose_edits",
        json.dumps(
            {
                "plan": "Create authorized source",
                "api_evidence": list(scoped.api_observations),
                "edits": [
                    {
                        "path": path,
                        "version": "0" * 64,
                        "old_text": "",
                        "new_text": "VALUE = 1\n",
                    }
                ],
            }
        ),
        "stale-absence",
    )
    with pytest.raises(PatchProposalError) as caught:
        admit_transaction(scoped.root, sources(scoped), call, scoped)
    assert caught.value.details["code"] == "ABSENCE_VERSION_MISMATCH"
    assert caught.value.details["observed_absence_version"] == absence["version"]
    assert not (scoped.root / path).exists()


def test_stale_source_version_and_occupied_absence_remain_refused(
    scoped: ContextTools,
) -> None:
    path = scoped.task.source
    call = ModelToolCall(
        "propose_edits",
        json.dumps(
            {
                "plan": "Change source",
                "api_evidence": list(scoped.api_observations),
                "edits": [
                    {
                        "path": path,
                        "version": "0" * 64,
                        "old_text": "return 1",
                        "new_text": "return 2",
                    }
                ],
            }
        ),
        "stale-source",
    )
    before = sources(scoped)
    with pytest.raises(PatchProposalError) as caught:
        admit_transaction(scoped.root, before, call, scoped)
    assert caught.value.details["code"] == "STALE_SOURCE_VERSION"
    assert caught.value.details["component_index"] == 1
    assert caught.value.details["observed_source_version"]
    assert sources(scoped) == before
    new = scoped.task.new_paths[0]
    dispatch(scoped, "inspect_new_source", path=new)
    (scoped.root / new).write_bytes(b"externally occupied\n")
    with pytest.raises(ValueError, match="SOURCE_DRIFT"):
        admit_observed(scoped.root, before, (change(new, "", "VALUE = 1\n"),), scoped)
    assert (scoped.root / new).read_bytes() == b"externally occupied\n"


def test_reference_span_failure_keeps_legacy_contract_and_component_identity(
    scoped: ContextTools,
) -> None:
    path = scoped.task.additional_edit_paths[0]
    ref = next(k for k, o in scoped.edit_references.items() if o["path"] == path)
    call = ModelToolCall(
        "replace_source",
        json.dumps({"reference": ref, "old_text": "return 1", "new_text": "return 2"}),
        "wrong-owner",
    )
    details = reject(scoped, (change(scoped.task.source, "return 1", "return 2"), call))
    assert details["code"] == "OBSERVATION_SPAN_MISMATCH"
    assert details["component_index"] == 2
    assert details["observation_reference"] == ref
    assert details["path"] == path


def test_duplicate_creation_and_unknown_reference_are_atomic(
    scoped: ContextTools,
) -> None:
    path = scoped.task.new_paths[0]
    dispatch(scoped, "inspect_new_source", path=path)
    details = reject(
        scoped,
        (change(path, "", "VALUE = 1\n"), change(path, "", "VALUE = 2\n", "duplicate")),
    )
    assert details["code"] == "OVERLAPPING_COMPONENTS"
    assert details["overlapping_components"] == [1, 2]
    assert not (scoped.root / path).exists()
    unknown = ModelToolCall(
        "replace_source",
        json.dumps(
            {"reference": "R999", "old_text": "return 1", "new_text": "return 2"}
        ),
        "unknown",
    )
    details = reject(
        scoped, (change(scoped.task.source, "return 1", "return 2"), unknown)
    )
    assert details["component_index"] == 2
    assert details["code"] == "OBSERVATION_MISSING"
    assert "path" not in details
    assert "observed_source_version" not in details


@pytest.mark.parametrize("padding", [9000, 18000])
def test_combined_and_single_patch_limits_remain_enforced(
    scoped: ContextTools, padding: int
) -> None:
    for index, path in enumerate(
        (scoped.task.source, scoped.task.additional_edit_paths[0])
    ):
        (scoped.root / path).write_bytes(
            ("#" + "p" * padding + f"\nVALUE_{index} = 1\n").encode()
        )
    scoped = ContextTools(scoped.root, scoped.task)
    dispatch(scoped, "inspect_api", target="bytes.decode")
    calls = []
    for index, path in enumerate(
        (scoped.task.source, scoped.task.additional_edit_paths[0])
    ):
        resource = scoped.snapshot.resource_at(RepositoryResourceAddress(path))
        dispatch(
            scoped,
            "read_source",
            path=path,
            version=str(resource.content_identity),
            start=padding + 2,
            end=len(resource.content),
        )
        calls.append(
            change(path, f"VALUE_{index} = 1", f"VALUE_{index} = 2", f"patch-{index}")
        )
    details = reject(scoped, tuple(calls))
    assert details["code"] == "PATCH_BYTE_LIMIT"
    assert details["patch_bytes"] > 16384
    assert details["patch_limit_bytes"] == 16384
    if padding == 9000:
        assert details["component_indices"] == [1, 2]
    else:
        assert details["component_index"] == 1


@pytest.mark.parametrize("no_op", [False, True])
def test_normalized_byte_limits_and_no_op_are_reported(
    scoped: ContextTools, *, no_op: bool
) -> None:
    path = scoped.task.source
    source = "value = 1\r\n"
    (scoped.root / path).write_bytes(source.encode())
    scoped = ContextTools(scoped.root, scoped.task)
    observe_all(scoped)
    dispatch(scoped, "inspect_api", target="bytes.decode")
    replacement = source if no_op else "x\n" * 1400
    details = reject(scoped, (change(path, source.replace("\r\n", "\n"), replacement),))
    assert details["code"] == ("NO_OP" if no_op else "REGION_BYTE_LIMIT")
    assert details["adapted_new_bytes"] == (len(source.encode()) if no_op else 4200)
    assert details["new_bytes"] == len(replacement.encode())


def test_long_call_identity_cannot_expand_diagnostics(scoped: ContextTools) -> None:
    identity = "c" * 5000
    details = reject(
        scoped, (change(scoped.task.source, "nonexistent", "return 2", identity),)
    )
    assert "proposal_call_id" not in details
    assert (
        details["proposal_call_id_sha256"]
        == hashlib.sha256(identity.encode()).hexdigest()
    )
    assert len(json.dumps(details)) < 2048


def test_scripted_native_refusal_corrected_atomic_edit_checks_and_restoration(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, ns = _contract()
    root = tmp_path.resolve()
    task, folder = asyncio.run(ns["fixture"](root))
    overview = root / "docs/backlog/overview.md"
    overview.parent.mkdir(parents=True)
    overview.write_text("# Independent fixture backlog\n", encoding="utf-8")
    regression = root / task.tests[0]
    regression.write_text(
        regression.read_text().replace("== 2", "in (1, 2)"), encoding="utf-8"
    )
    asyncio.run(designate(root, authorize=lambda _: True))
    asyncio.run(git(root, "add", "--", "docs/backlog/overview.md", task.tests[0]))
    asyncio.run(
        git(
            root,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@invalid",
            "commit",
            "-qm",
            "Fixture backlog",
        )
    )
    task = replace(
        task,
        baseline_revision=asyncio.run(git(root, "rev-parse", "HEAD")),
        baseline_hashes=tuple((p, _hash(root / p)) for p, _ in task.baseline_hashes),
        maximum_calls=4,
        maximum_proposals=3,
    )
    run = folder.parent / "diagnostic-native"
    header = '"""Authored validation fixture."""'

    class Repair(Scripted):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            turn = len(self.requests)
            calls: tuple[ModelToolCall, ...]
            Prompt("", "messages", request.prompt.messages)
            if turn == 1:
                calls = (
                    ModelToolCall(
                        "inspect_source",
                        json.dumps({"path": task.source, "start": 0}),
                        "read",
                    ),
                )
            elif turn in (2, 3):
                if turn == 3:
                    feedback = json.loads((run / "turn-02/tools.json").read_text())
                    assert len(feedback) == 2
                    for i, record in enumerate(feedback, 1):
                        assert record["call"]["provider_call_id"] == f"edit-2-{i}"
                        assert record["result"]["error"] == "TRANSACTION_REFUSED"
                        detail = record["result"]["details"]
                        assert detail["component_index"] == 2
                        assert detail["proposal_call_id"] == "edit-2-2"
                        assert detail["code"] == "OLD_TEXT_NOT_UNIQUE"
                        assert detail["observed_match_count"] == 0
                    assert (root / task.source).read_text() == ns["BASE"]
                    returned = [
                        m.tool_call_id
                        for m in request.prompt.messages
                        if m.role == "tool"
                    ]
                    assert "edit-2-1" in returned
                    assert "edit-2-2" in returned
                calls = (
                    change(
                        task.source,
                        header,
                        '"""Checked validation fixture."""',
                        f"edit-{turn}-1",
                    ),
                    change(
                        task.source,
                        "VALUE: int = 99" if turn == 2 else "VALUE: int = 1",
                        "VALUE: int = 2",
                        f"edit-{turn}-2",
                    ),
                )
            else:
                assert turn == 4
                calls = (
                    ModelToolCall("check_changes", "{}", "check-installed-candidate"),
                )
            return ModelResponse(
                "Scripted infrastructure regression, not Qwen inference",
                self.source,
                tool_calls=calls,
            )

    async def interaction(_: Path) -> tuple[Repair, dict[str, str]]:
        return Repair([]), {"kind": "scripted; no inference"}

    monkeypatch.setattr(coding_worker, "local_interaction", interaction)
    result = asyncio.run(
        coding_worker.run_local_task(
            root,
            run,
            task=task,
            branch="feat/diagnostic-fixture",
            coordinated_edits=True,
            observed_edits=True,
            check_changes_before_completion=True,
        )
    )
    assert result["accepted"], result
    assert result["proposals_attempted"] == 2
    assert result["proposals_admitted"] == 1
    assert result["change_check_freshness"]["current"]
    assert result["original_unchanged"]
    assert (root / task.source).read_text() == ns["BASE"]
    assert not CodingCommands(root, run, task).is_current(result["change_check"])
    assert not (root / ".local/backlog/checkout-owner").exists()
