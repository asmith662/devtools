# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independent literal admission scenarios

"""Aggregate read refusals recover without model inference or WorkCycle replay."""

from __future__ import annotations

import asyncio
import hashlib
import json
from dataclasses import replace
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import (
    ProjectionPolicy,
    request_bytes,
    source_feedback,
)
from devtools.agents.coding.protocol import read_request
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.context import Repository, RepositoryResourceAddress
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.repository.corpus import define_repository_text_corpus
from devtools.context.repository.discovery import discover_repository_resource_addresses
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelToolCall,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools.source import (
    ScopedSourceTool,
    SourceReadRefusal,
    SourceReadRequest,
    SourceScope,
)
from tests.agents.coding.fixtures import GOOD, SOURCE
from tests.agents.coding.test_repository import (
    EDIT,
    LIMITS,
    READ,
    Script,
    call,
    host_at,
)

if TYPE_CHECKING:
    from devtools.context.planning.materialization import ContextDisclosure


def host(
    root: Path,
    contents: dict[str, str],
    *,
    source: str = "module.py",
    budget: int = 8000,
    projection: ProjectionPolicy | None = None,
) -> RepositoryCodingHost:
    """Compose real owners around a few authored files, never a source-tree copy."""
    initial = host_at(root)
    for name, text in contents.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        write(TextFile(resolve_path(root / name), text))
    repo = Repository(initial.scope.snapshot.repository_id)
    scope = SourceScope.observe(
        root=initial.scope.root,
        repository=repo,
        addresses=tuple(RepositoryResourceAddress(p) for p in contents),
    )
    corpus = define_repository_text_corpus(
        discovery=discover_repository_resource_addresses(
            repository=repo,
            root=scope.root,
            requested_addresses=tuple(r.address for r in scope.snapshot.resources),
            maximum_resource_count=16,
            maximum_traversal_entry_count=256,
        ),
        selected_addresses=tuple(r.address for r in scope.snapshot.resources),
    )
    return RepositoryCodingHost(
        replace(
            initial.objective,
            scope=scope,
            editable=(RepositoryResourceAddress(source),),
            checks=replace(initial.objective.checks, source_scope=scope),
            edits=replace(initial.objective.edits, source_bytes=32768),
            disclosure_bytes=32768,
            prompt_bytes=budget,
        ),
        corpus=corpus,
        authorize=initial.authorize,
        apply_changes=initial.effect,
        archive=initial.archive,
        restore=initial.restore,
        projection=projection,
    )


def test_preserved_b0049_batch_continues_with_smaller_selected_read(
    tmp_path: Path,
) -> None:
    frozen = json.loads((Path(__file__).parent / "data/b0049.json").read_bytes())
    assert sum(len(s.encode()) for s in frozen["contents"].values()) == 51544
    assert {
        p: hashlib.sha256(s.encode()).hexdigest() for p, s in frozen["contents"].items()
    } == frozen["sha256"]
    instance = host(tmp_path, frozen["contents"], source=frozen["source"], budget=32768)
    instance.objective = replace(instance.objective, text=frozen["objective"])
    instance.messages[0] = PromptMessage("user", frozen["objective"])
    instance.settings = ModelSettings(**frozen["settings"])
    batches = [tuple(ModelToolCall(**c) for c in calls) for calls in frozen["calls"]]
    narrow_path = "tests/context/python/imports/test_members.py"
    narrow = call(
        "read_source",
        {"path": narrow_path, "start": 0, "end": 128},
        "narrow",
    )
    sent: list[ModelRequest] = []

    class Worker(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            assert request_bytes(request) <= 32768
            sent.append(request)
            if self.entries == 2:
                replies = request.prompt.messages[-3:]
                assert [m.tool_call_id for m in replies] == [
                    c.provider_call_id for c in batches[1]
                ]
                refused = json.loads(replies[1].content)
                assert refused["error"] == "SOURCE_CONTEXT_CAPACITY"
                assert refused["tool_operation_entered"] is False
                assert refused["source_disclosure_entered"] is False
                assert "explicit smaller end" in refused["instruction"]
                assert all(
                    o.unit.resource.address.value != narrow_path
                    for o in instance.disclosures
                )
            if self.entries == 3:
                value = json.loads(request.prompt.messages[-1].content)
                assert value["text"] == frozen["contents"][narrow_path][:128]
                assert value["span"] == [0, 128]
            response = await super().send(request)
            return replace(response, content="") if self.entries <= 2 else response

    # Reconstruct the old complete third request without entering any Tool/model.
    async def legacy_size() -> int:
        await instance.prepare(CodingProgress(LIMITS))
        messages = list(instance.messages)
        for batch in batches:
            messages.append(PromptMessage("assistant", "", batch))
            for native in batch:
                address = json.loads(native.arguments_json)["path"]
                unit = next(
                    u
                    for u in instance.index.views[0].units
                    if u.resource.address.value == address
                )
                option = SourceRangeDisclosureOption(
                    frozen["objective"],
                    unit,
                    0,
                    unit.end,
                    32768,
                )
                messages.append(
                    PromptMessage(
                        "tool",
                        json.dumps(
                            source_feedback(option, option.text),
                            ensure_ascii=False,
                        ),
                        tool_call_id=native.provider_call_id,
                    ),
                )
        return request_bytes(instance.build_request(tuple(messages)))

    assert asyncio.run(legacy_size()) > 51544
    worker = Worker([*batches, (narrow,), ()])
    result = asyncio.run(
        run_coding_agent(
            worker,
            limits=replace(LIMITS, model_calls=4, tool_actions=6),
            host=instance,
        ),
    )
    assert result.disposition == "stopped", result.error
    assert result.error is None
    assert len(sent) == 4
    assert [request_bytes(r) for r in sent[:2]] == frozen["observed_request_bytes"]
    assert result.progress.actions == 5
    assert all(e.acknowledged for e in result.progress.effects)
    assert len(instance.source_results) < 5
    assert instance.disclosures[-1].span == (0, 128)
    assert instance.disclosures[-1].unit.resource.address.value == narrow_path


def test_refused_batch_then_narrow_source_edit_failed_check_and_repair(
    tmp_path: Path,
) -> None:
    large = "# irrelevant source\n" * 600
    instance = host(tmp_path, {"module.py": SOURCE, "large.py": large})
    seen: dict[RepositoryResourceAddress, str | None] = {}
    instance.archive = seen.update
    plan = instance.objective.checks
    check = replace(
        plan.checks[0],
        command=plan.checks[0].command.with_args(
            "-I",
            "-c",
            "import runpy; assert runpy.run_path('module.py')['answer']() == 7",
        ),
    )
    instance.objective = replace(
        instance.objective,
        checks=replace(plan, checks=(check,)),
    )
    wrong = call(
        "replace_source",
        {"path": "module.py", "old_text": "return 6", "new_text": "return 5"},
        "wrong",
    )
    repair = call(
        "replace_source",
        {"path": "module.py", "old_text": "return 5", "new_text": "return 7"},
        "repair",
    )
    big = call("read_source", {"path": "large.py", "start": 0}, "big")
    narrow = call("read_source", {"path": "large.py", "start": 0, "end": 64}, "narrow")
    worker = Script(
        [
            (READ,),
            (big, replace(big, provider_call_id="big-again")),
            (narrow,),
            (wrong,),
            (repair,),
        ],
    )
    result = asyncio.run(
        run_coding_agent(
            worker,
            limits=replace(LIMITS, model_calls=5, proposals=2, tool_actions=4),
            host=instance,
        ),
    )
    assert result.accepted
    assert [g[0].passed for g in instance.check_results] == [False, True]
    assert result.progress.proposals == 2
    assert seen[RepositoryResourceAddress("module.py")] == GOOD
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE
    tools = {
        m.tool_call_id: json.loads(m.content)
        for m in instance.messages
        if m.role == "tool"
    }
    assert (
        tools["big"]["error"]
        == tools["big-again"]["error"]
        == "SOURCE_CONTEXT_CAPACITY"
    )
    assert tools["narrow"]["text"] == large[:64]
    assert tools["wrong"]["passed"] is False
    assert tools["repair"]["passed"] is True


@pytest.mark.parametrize(
    "projection",
    [None, ProjectionPolicy(7500, 7000, report_source_state=True)],
)
def test_unicode_crlf_batch_refusal_and_exact_partial_witness(
    tmp_path: Path,
    projection: ProjectionPolicy | None,
) -> None:
    tail = SOURCE.replace("\n", "\r\n")
    text = "# λ🙂\r\n" * 1200 + tail
    instance = host(tmp_path, {"module.py": text}, projection=projection)
    first = call("read_source", {"path": "module.py", "start": 0}, "whole")
    start = len(text) - len(tail)
    partial = call(
        "read_source",
        {"path": "module.py", "start": start, "end": len(text)},
        "tail",
    )
    worker = Script([(first,), (partial,), (EDIT,)])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert result.accepted, instance.messages[-1].content
    assert any(
        cast("SourceRangeDisclosureOption", r.items[0].native_provenance).start == start
        and r.items[0].text == tail
        for r in instance.source_results
    )
    assert any(r.items[0].text == tail for r in instance.source_results)
    refusal = next(m for m in instance.messages if m.tool_call_id == "whole")
    if projection is None:
        assert json.loads(refusal.content)["tool_operation_entered"] is False
        assert instance.source_results[0].items[0].text == tail
    else:
        assert json.loads(refusal.content)["text"] == text
    assert (tmp_path / "module.py").read_bytes() == text.encode()


def test_repeated_oversize_reads_are_finite_and_never_enter_source_tool(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    instance = host(tmp_path, {"module.py": "#" + "x" * 12000})

    def forbidden(*_args: object, **_kwargs: object) -> None:
        pytest.fail("capacity refusal entered source disclosure")

    monkeypatch.setattr(ScopedSourceTool, "execute", forbidden)
    attempts: list[tuple[ModelToolCall, ...]] = [
        (call("read_source", {"path": "module.py", "start": 0}, str(n)),)
        for n in range(4)
    ]
    worker = Script(attempts)
    result = asyncio.run(
        run_coding_agent(
            worker,
            limits=replace(LIMITS, model_calls=4, tool_actions=2),
            host=instance,
        ),
    )
    assert result.disposition == "model_limit"
    assert result.error is None
    assert result.progress.actions == 2
    assert all(e.acknowledged for e in result.progress.effects)
    assert instance.source_results == []
    assert instance.disclosures == []


def test_mandatory_input_cannot_fit_even_refusal_stops_before_tools(
    tmp_path: Path,
) -> None:
    instance = host(tmp_path, {"module.py": SOURCE})

    class Worker(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            instance.objective = replace(
                instance.objective,
                prompt_bytes=request_bytes(request),
            )
            return await super().send(request)

    result = asyncio.run(
        run_coding_agent(Worker([(READ,)]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "failed"
    assert result.failure_phase == "acquisition"
    assert "correlated refusal" in str(result.error)
    assert len(result.progress.effects) == 1
    assert result.progress.effects[0].acknowledged
    assert instance.source_results == []


@pytest.mark.parametrize("difference", [0, -1])
def test_exact_complete_request_boundary(tmp_path: Path, difference: int) -> None:
    instance = host(tmp_path, {"module.py": SOURCE + '# café\\"\r\n' * 200})

    async def run() -> None:
        await instance.prepare(CodingProgress(LIMITS))
        reading = call("read_source", {"path": "module.py", "start": 0}, "read")
        response = ModelResponse("inspect", Script.source, tool_calls=(reading,))
        instance.classify(response)
        requested = read_request(
            reading.arguments_json,
            index=instance.index,
            purpose=instance.objective.text,
            maximum_bytes=32768,
            by_unit=False,
        )
        selected = SourceRangeDisclosureOption(
            requested.purpose,
            requested.unit,
            requested.start,
            cast("int", requested.end),
            requested.maximum_bytes,
        )
        value = source_feedback(selected, selected.text)
        complete = instance.build_request(
            (
                *instance.messages,
                PromptMessage(
                    "tool",
                    json.dumps(value, ensure_ascii=False),
                    tool_call_id="read",
                ),
            ),
        )
        instance.objective = replace(
            instance.objective,
            prompt_bytes=request_bytes(complete) + difference,
        )
        await instance.acquire(response)
        assert len(instance.source_results) == (1 if difference == 0 else 0)
        assert (
            request_bytes(await instance.prepare(instance.progress))
            <= instance.objective.prompt_bytes
        )

    asyncio.run(run())


def test_capacity_refusal_never_grants_source_to_edit(tmp_path: Path) -> None:
    instance = host(tmp_path, {"module.py": "# padding\n" * 1200 + SOURCE})
    big = call("read_source", {"path": "module.py", "start": 0}, "big")
    result = asyncio.run(
        run_coding_agent(Script([(big,), (EDIT,)]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "proposal_limit"
    assert "not acquired" in instance.messages[-1].content
    assert not instance.disclosures
    assert not instance.source_results


@pytest.mark.parametrize("fault", ["exception", "payload", "refusal"])
def test_postentry_read_outcomes_are_not_effect_free_refusals(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    instance = host(tmp_path, {"module.py": SOURCE})
    actual = ScopedSourceTool.execute
    failure = OSError("read completion acknowledgement lost")
    entered: list[str] = []

    async def execute(
        tool: ScopedSourceTool,
        arguments: SourceReadRequest,
    ) -> ContextDisclosure | SourceReadRefusal:
        entered.append("entered")
        disclosure = await actual(tool, arguments)
        assert not isinstance(disclosure, SourceReadRefusal)
        if fault == "exception":
            raise failure
        if fault == "refusal":
            return SourceReadRefusal(arguments)
        return replace(
            disclosure,
            items=(replace(disclosure.items[0], text="changed"),),
        )

    monkeypatch.setattr(ScopedSourceTool, "execute", execute)
    result = asyncio.run(
        run_coding_agent(Script([(READ,)]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "failed"
    assert result.failure_phase == "acquisition"
    assert entered == ["entered"]
    assert result.progress.effects[0].acknowledged is (fault != "exception")
    assert not instance.disclosures
    if fault == "exception":
        assert result.error is failure
        assert not any(m.role == "tool" for m in instance.messages)
    else:
        assert (
            json.loads(instance.messages[-1].content)["tool_operation_entered"] is True
        )
        if fault == "payload":
            assert instance.source_results[0].items[0].text == "changed"
            assert json.loads(instance.messages[-1].content)["status"] == "UNDISCLOSED"


def test_scope_change_during_capacity_consent_is_not_refused_as_size(
    tmp_path: Path,
) -> None:
    instance = host(tmp_path, {"module.py": "# padding\n" * 1200 + SOURCE})

    async def consent(_call: object, _arguments: object) -> None:
        (tmp_path / "module.py").write_text("unknown source", encoding="utf-8")

    instance.authorize = consent
    big = call("read_source", {"path": "module.py", "start": 0}, "big")
    result = asyncio.run(
        run_coding_agent(Script([(big,)]), limits=LIMITS, host=instance),
    )
    assert result.custody.reconciliation_required
    assert "no longer current" in str(result.error)
    assert not any(m.role == "tool" for m in instance.messages)
    assert not instance.source_results
    assert (tmp_path / "module.py").read_text(encoding="utf-8") == "unknown source"


@pytest.mark.parametrize("project", [False, True])
def test_required_check_feedback_is_retained_during_capacity_recovery(
    tmp_path: Path,
    *,
    project: bool,
) -> None:
    instance = host(
        tmp_path,
        {"module.py": SOURCE, "other.py": "# padding\n" * 1200},
        projection=ProjectionPolicy(7500, 7000) if project else None,
    )
    protected = PromptMessage("user", json.dumps({"actual_failed_check": "FAIL" * 900}))
    instance.messages.append(protected)
    instance._check_feedback = {2}  # noqa: SLF001 -- authored required check observation
    big = call("read_source", {"path": "other.py", "start": 0}, "big")

    class Worker(Script):
        async def send(self, request: object) -> ModelResponse:
            assert isinstance(request, ModelRequest)
            assert protected in request.prompt.messages
            assert request_bytes(request) <= 8000
            return await super().send(request)

    result = asyncio.run(
        run_coding_agent(Worker([(big,), (READ,), ()]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "stopped"
    assert result.error is None


def test_read_batch_reserves_a_pending_fixed_check(tmp_path: Path) -> None:
    instance = host(tmp_path, {"module.py": SOURCE})
    checked = call("validate_candidate", {}, "check")
    worker = Script([(READ, checked), ()])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert result.disposition == "stopped"
    assert instance.check_results[0][0].passed
    replies = [m for m in instance.messages if m.role == "tool"]
    assert [m.tool_call_id for m in replies] == ["read", "check"]
    assert json.loads(replies[-1].content) == {"passed": True}


def test_inventory_and_tool_definitions_are_charged_to_read_budget(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    instance = host(tmp_path, {"module.py": "# padding\n" * 400})
    actual = instance.build_request

    def build(messages: tuple[PromptMessage, ...]) -> ModelRequest:
        request = actual(messages)
        return replace(
            request,
            tools=(
                replace(request.tools[0], description="x" * 5000),
                *request.tools[1:],
            ),
        )

    monkeypatch.setattr(instance, "build_request", build)
    big = call("read_source", {"path": "module.py", "start": 0}, "big")
    worker = Script([(big,), ()])
    result = asyncio.run(run_coding_agent(worker, limits=LIMITS, host=instance))
    assert result.disposition == "stopped"
    assert not instance.source_results
    assert (
        json.loads(instance.messages[-2].content)["error"] == "SOURCE_CONTEXT_CAPACITY"
    )


def test_batch_with_known_range_refusal_preserves_other_read(tmp_path: Path) -> None:
    instance = host(tmp_path, {"module.py": SOURCE})
    bad = call("read_source", {"path": "module.py", "start": 0, "end": 99999}, "bad")
    result = asyncio.run(
        run_coding_agent(Script([(bad, READ), ()]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "stopped"
    assert len(instance.source_results) == 1
    replies = [m for m in instance.messages if m.role == "tool"]
    assert [m.tool_call_id for m in replies] == ["bad", "read"]
    assert json.loads(replies[0].content)["error"] == "SOURCE_RANGE_OUT_OF_BOUNDS"
    assert json.loads(replies[0].content)["tool_operation_entered"] is False


def test_feasible_multi_read_batch_is_admitted_without_partial_refusal(
    tmp_path: Path,
) -> None:
    text = "# data\n" * 600 + SOURCE
    instance = host(tmp_path, {"module.py": text})
    calls = tuple(
        call(
            "read_source",
            {"path": "module.py", "start": n * 900, "end": (n + 1) * 900},
            str(n),
        )
        for n in range(2)
    )
    result = asyncio.run(
        run_coding_agent(Script([calls, ()]), limits=LIMITS, host=instance),
    )
    assert result.disposition == "stopped"
    assert [r.items[0].text for r in instance.source_results] == [
        text[:900],
        text[900:1800],
    ]
