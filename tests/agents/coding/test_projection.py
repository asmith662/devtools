# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- independently specified literal projection assertions
"""Native retained history and active input are different factual accounts."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import asdict, replace
from pathlib import Path

import pytest

from devtools.agents.coding import repository as owner
from devtools.agents.coding.models import CodingEffect, CodingProgress
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    native_exchange_ranges,
    request_bytes,
)
from devtools.agents.coding.repository import _CHECK, _EDIT, _READ, RepositoryCodingHost
from devtools.agents.model_tools import normalize_tool_descriptor
from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelToolCall,
    ModelToolDefinition,
    Prompt,
    PromptMessage,
)
from devtools.resources.commands import Command
from devtools.resources.filesystem import TextFile, write
from devtools.tools.errors import ToolInputError
from tests.agents.coding.fixtures import SOURCE
from tests.agents.coding.test_repository import EDIT, LIMITS, host_at


def frozen_request() -> ModelRequest:
    """Read immutable facts; do not import or execute the experiment controller."""
    root = Path(__file__).resolve().parents[3]
    path = (
        root / "experiments/local_coding_dogfood/case_0003/evidence/worker-result.json"
    )
    original = json.loads(path.read_text(encoding="utf-8"))
    messages = tuple(
        PromptMessage(
            **{
                **message,
                "tool_calls": tuple(ModelToolCall(**c) for c in message["tool_calls"]),
            },
        )
        for message in original["messages"]
    )
    return ModelRequest(
        Prompt("", "messages", messages),
        settings=ModelSettings(maximum_output_tokens=4096, thinking_enabled=False),
        tools=tuple(normalize_tool_descriptor(d) for d in (_READ, _EDIT, _CHECK)),
    )


def test_case0003_original_bytes_and_disjoint_unconsumed_read() -> None:
    request = frozen_request()
    assert len(json.dumps(asdict(request), ensure_ascii=False).encode()) == 36640
    sources = [
        json.loads(m.content)
        for m in request.prompt.messages
        if m.role == "tool" and '"text"' in m.content
    ]
    assert [s["span"] for s in sources] == [[1, 6754], [10250, 11200], [1, 8193]]
    assert sources[-1]["partial"] is True
    assert len(sources[-1]["text"].encode()) == 8192
    assert sources[-1]["span"][1] < sources[-2]["span"][0]


def test_legacy_byte_refusal_does_not_erase_history(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    host.objective = replace(host.objective, prompt_bytes=100)
    original = tuple(host.messages)
    with pytest.raises(ValueError, match="byte budget"):
        asyncio.run(host.prepare(CodingProgress(LIMITS)))
    assert tuple(host.messages) == original
    assert host.requests == []


def configured(root: Path, *, hard: int = 5000) -> RepositoryCodingHost:
    """Configure an actual neutral host with host-only metadata classification."""
    host = host_at(root)
    host.objective = replace(host.objective, prompt_bytes=hard)
    host.projection = ProjectionPolicy(
        hard * 7 // 8,
        hard * 3 // 4,
        frozenset({"list_repository"}),
    )
    host.progress = CodingProgress(LIMITS)
    return host


def metadata(host: RepositoryCodingHost, identity: str, content: str) -> None:
    """Append authored available metadata, without pretending it executed a Tool."""
    call = ModelToolCall("list_repository", "{}", identity)
    host.messages.append(PromptMessage("assistant", "inspect inventory", (call,)))
    host._feedback(call, {"inventory": content})  # noqa: SLF001 -- host composition seam


async def acquire(
    host: RepositoryCodingHost,
    identity: str = "read",
    start: int = 0,
    end: int = len(SOURCE),
) -> None:
    """Enter actual scope admission, ToolRunner and Context materialization once."""
    response = ModelResponse(
        "read exact source",
        InteractionSource("independent"),
        tool_calls=(
            ModelToolCall(
                "read_source",
                json.dumps({"path": "module.py", "start": start, "end": end}),
                identity,
            ),
        ),
    )
    assert host.classify(response) == "acquire"
    await host.acquire(response)


def test_short_history_unchanged_and_current_read_authorizes_edit(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        originals = tuple(host.messages)
        request = await host.prepare(host.progress)
        assert request.prompt.messages == originals
        assert host.projection_outcomes[-1].status == "unchanged"
        assert not host.projection_outcomes[-1].triggered
        assert host.active_disclosures == tuple(host.disclosures)
        assert await host.propose(
            ModelResponse("edit", InteractionSource("independent"), tool_calls=(EDIT,)),
        )
        assert host.progress.actions == 1
        assert len(host.source_results) == 1

    asyncio.run(run())


@pytest.mark.parametrize("repeated", [False, True])
def test_metadata_omission_preserves_constraints_history_and_no_effects(
    tmp_path: Path,
    *,
    repeated: bool,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        host.messages[0] = PromptMessage(
            "user",
            "Only module.py; never execute an unapproved command.",
        )
        metadata(host, "inventory-1", "x" * 3000)
        metadata(host, "inventory-2", ("x" if repeated else "y") * 3000)
        await acquire(host)
        original = tuple(host.messages)
        effect_count = len(host.progress.effects)
        result = await host.prepare(host.progress)
        decision = host.projection_outcomes[-1]
        assert decision.status == "reduced"
        assert decision.target_reached
        assert decision.omitted_exchanges == (
            (1, 3, "host-classified-metadata"),
            (3, 5, "host-classified-metadata"),
        )
        assert result.prompt.messages == (original[0], *original[5:])
        assert decision.resulting_bytes == len(
            json.dumps(asdict(result), ensure_ascii=False).encode(),
        )
        assert tuple(host.messages) == original
        assert len(host.progress.effects) == effect_count == 1
        assert await host.propose(
            ModelResponse("edit", InteractionSource("independent"), tool_calls=(EDIT,)),
        )

    asyncio.run(run())


def test_duplicate_current_source_is_omitted_but_disjoint_ranges_remain(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host, "prefix", 0, 7)
        await acquire(host, "tail", 7, len(SOURCE))
        await acquire(host, "duplicate", 0, 7)
        original = host.build_request(tuple(host.messages))
        before = request_bytes(original)
        host.projection = ProjectionPolicy(before - 1, before - 400)
        await host.prepare(host.progress)
        result = host.projection_outcomes[-1]
        assert result.omitted_exchanges == ((1, 3, "duplicate-current-source"),)
        assert [o.span for o in result.active_sources] == [(7, len(SOURCE)), (0, 7)]
        assert (
            host.disclosures[0] in result.active_sources
        )  # same exact support, distinct executions retained
        assert len(host.source_results) == 3
        assert len(host.messages) == 7

    asyncio.run(run())


def test_disclosure_affordability_retains_original_and_invalidates_omitted_witness(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path, hard=2800)
        text = "# " + "x" * 1900 + "\nreturn_value = 6\n"
        write(TextFile(resolve_path(tmp_path / "module.py"), text))
        host.scope = host.scope.observe(
            root=host.scope.root,
            repository=Repository(host.scope.snapshot.repository_id),
            addresses=(RepositoryResourceAddress("module.py"),),
        )
        host._index()  # noqa: SLF001 -- refresh independently authored fixture before any invocation
        host.objective = replace(
            host.objective,
            disclosure_bytes=4096,
            edits=replace(host.objective.edits, source_bytes=4096),
        )
        await acquire(host, "tail", 1903, len(text))
        await acquire(host, "large", 0, 1903)
        original = tuple(host.messages)
        await host.prepare(host.progress)
        decision = host.projection_outcomes[-1]
        assert decision.status == "reduced"
        assert decision.omitted_exchanges == ((1, 3, "source-capacity"),)
        assert decision.shortened_indices == (4,)
        partial = json.loads(decision.request.prompt.messages[-1].content)
        assert partial["partial"] is True
        assert partial["presentation"]["acquired_partial"] is False
        assert partial["presentation"]["acquired_span"] == [0, 1903]
        assert partial["text"] == text[: partial["span"][1]]
        assert decision.resulting_bytes <= 2800
        assert tuple(host.messages) == original
        assert json.loads(host.messages[-1].content)["partial"] is False
        assert len(host.source_results[-1].items[0].text) == 1903
        edit = ModelToolCall(
            "replace_source",
            json.dumps(
                {
                    "path": "module.py",
                    "old_text": "return_value = 6",
                    "new_text": "return_value = 7",
                },
            ),
            "edit-tail",
        )
        response = ModelResponse(
            "edit",
            InteractionSource("independent"),
            tool_calls=(edit,),
        )
        assert host.classify(response) == "edit"
        assert await host.propose(response) is None
        assert "not acquired" in host.messages[-1].content
        assert host.progress.actions == 2
        # Explicit reacquisition uses the same authorized operation, never replay.
        await acquire(host, "tail-again", 1903, len(text))
        await host.prepare(host.progress)
        assert await host.propose(
            ModelResponse("edit", InteractionSource("independent"), tool_calls=(edit,)),
        )
        assert host.progress.actions == 3
        assert tuple(host.messages[: len(original)]) == original

    asyncio.run(run())


@pytest.mark.parametrize("fault", ["cancel", "failure", "capacity", "unknown-effect"])
def test_failed_projection_keeps_previous_active_state_and_original_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        await host.prepare(host.progress)
        previous = host.active_disclosures
        original = tuple(host.messages)
        requests = tuple(host.requests)
        error: BaseException = (
            asyncio.CancelledError("projection cancelled")
            if fault == "cancel"
            else OSError("projection failure")
        )
        if fault in {"cancel", "failure"}:

            def fail(*_args: object, **_kwargs: object) -> None:
                raise error

            monkeypatch.setattr(owner, "project_request", fail)
        elif fault == "capacity":
            host.objective = replace(host.objective, prompt_bytes=200)
            host.projection = ProjectionPolicy(190, 150)
        else:
            host.progress.effects.append(CodingEffect("edit", ("unknown",)))
        with pytest.raises((asyncio.CancelledError, OSError, ValueError)) as caught:
            await host.prepare(host.progress)
        assert host.projection_error is caught.value
        if fault in {"cancel", "failure"}:
            assert caught.value is error
        if fault == "capacity":
            assert isinstance(caught.value, ProjectionCapacityError)
            assert caught.value.outcome.status == "insufficient"
        assert host.active_disclosures == previous
        assert tuple(host.messages) == original
        assert tuple(host.requests) == requests

    asyncio.run(run())


def test_protected_readiness_cannot_be_dropped(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path, hard=1600)
        await acquire(host)
        host.readiness = lambda _snapshot, _sources: None
        metadata(host, "latest", "x" * 1800)
        with pytest.raises(ProjectionCapacityError):
            await host.prepare(host.progress)
        assert host.projection_outcomes[-1].omitted_exchanges == ()
        assert host.active_disclosures == ()

    asyncio.run(run())


def test_failed_check_feedback_survives_new_acquisition(tmp_path: Path) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        fixed = host.objective.checks.checks[0]
        assert fixed.command.timeout is not None
        command = (
            Command(sys.executable)
            .args(
                "-I",
                "-c",
                "import sys; print('required check failed'); sys.exit(1)",
            )
            .cwd(host.scope.root)
            .with_timeout(fixed.command.timeout)
        )
        host.objective = replace(
            host.objective,
            checks=replace(
                host.objective.checks,
                checks=(replace(fixed, command=command),),
            ),
        )
        await acquire(host)
        await host.prepare(host.progress)
        response = ModelResponse(
            "edit",
            InteractionSource("independent"),
            tool_calls=(EDIT,),
        )
        assert host.classify(response) == "edit"
        proposal = await host.propose(response)
        assert proposal is not None
        await host.apply(proposal)
        assert not await host.check(proposal)
        await host.feedback(response, proposal, passed=False)
        original_check = host.messages[-1]
        assert json.loads(original_check.content)["checks"][0]["exit_code"] == 1
        metadata(host, "later-inventory", "x" * 6000)
        await acquire(host, "current-read")
        # Even a host classifying the edit's feedback as omittable cannot remove
        # the current failed-check evidence or its complete native exchange.
        host.projection = ProjectionPolicy(
            4500,
            3500,
            frozenset({"list_repository", "replace_source"}),
        )
        request = await host.prepare(host.progress)
        assert original_check in request.prompt.messages
        assert "required check failed" in original_check.content
        assert len(host.check_results) == 1
        assert sum(e.kind == "check" for e in host.progress.effects) == 1
        assert host.projection_outcomes[-1].status == "reduced"

    asyncio.run(run())


def test_affordable_unicode_disclosure_keeps_exact_utf8_prefix(tmp_path: Path) -> None:
    async def run() -> None:
        host = configured(tmp_path, hard=2200)
        text = "\u03c0" * 1300
        write(TextFile(resolve_path(tmp_path / "module.py"), text))
        host.scope = host.scope.observe(
            root=host.scope.root,
            repository=Repository(host.scope.snapshot.repository_id),
            addresses=(RepositoryResourceAddress("module.py"),),
        )
        host._index()  # noqa: SLF001 -- independently authored UTF-8 source
        host.objective = replace(host.objective, disclosure_bytes=4096)
        await acquire(host, "unicode", 0, len(text))
        original = host.messages[-1]
        request = await host.prepare(host.progress)
        result = json.loads(request.prompt.messages[-1].content)
        assert result["partial"] is True
        assert 0 < len(result["text"]) < len(text)
        assert result["text"] == text[: result["span"][1]]
        assert len(result["text"].encode()) == 2 * len(result["text"])
        assert request_bytes(request) <= 2200
        assert host.messages[-1] == original
        assert host.source_results[-1].items[0].text == text

    asyncio.run(run())


@pytest.mark.parametrize("policy", [(-1, 1), (4, 5), (True, 1), (4, False)])
def test_invalid_watermarks_refused(policy: tuple[int, int]) -> None:
    with pytest.raises(ValueError, match="policy"):
        ProjectionPolicy(*policy)


def test_native_boundaries_preserve_intervening_instructions() -> None:
    calls = (ModelToolCall("a", "{}", "a"), ModelToolCall("b", "{}", "b"))
    messages = (
        PromptMessage("system", "mandatory"),
        PromptMessage("assistant", "", calls),
        PromptMessage("tool", "second", tool_call_id="b"),
        PromptMessage("tool", "first", tool_call_id="a"),
        PromptMessage("user", "new restriction"),
        PromptMessage("assistant", "no call"),
    )
    assert native_exchange_ranges(messages) == ((1, 4), (5, 6))
    with pytest.raises(ValueError, match="unresolved"):
        native_exchange_ranges(messages[:3])


def test_multi_turn_projection_is_repeatable_without_mutating_history(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        metadata(host, "first", "x" * 4000)
        await acquire(host, "read-1")
        await host.prepare(host.progress)
        first = tuple(host.messages)
        for number in range(2, 4):
            metadata(host, f"inventory-{number}", "y" * 4000)
            await acquire(host, f"read-{number}")
            await host.prepare(host.progress)
            outcome = host.projection_outcomes[-1]
            assert outcome.resulting_bytes <= 5000
            assert outcome.active_sources == (host.disclosures[-1],)
            assert (
                host.requests[-1].prompt.messages[-1].tool_call_id == f"read-{number}"
            )
            assert tuple(host.messages[: len(first)]) == first
        assert len(host.source_results) == host.progress.actions == 3
        assert len(host.projection_outcomes) == 3
        assert all(e.acknowledged for e in host.progress.effects)

    asyncio.run(run())


def test_unknown_operation_and_instructions_remain_protected(tmp_path: Path) -> None:
    host = configured(tmp_path, hard=1800)
    unknown = ModelToolCall("external-effect", "{}", "unknown")
    host.messages.extend(
        (
            PromptMessage("assistant", "execution outcome unknown", (unknown,)),
            PromptMessage(
                "tool",
                "unknown receipt " + "x" * 1500,
                tool_call_id="unknown",
            ),
            PromptMessage("user", "Do not repeat the operation."),
        ),
    )
    metadata(host, "new", "small")
    original = tuple(host.messages)
    with pytest.raises(ProjectionCapacityError) as failure:
        asyncio.run(host.prepare(host.progress))
    assert failure.value.outcome.omitted_exchanges == ()
    assert failure.value.outcome.request.prompt.messages == original
    assert host.requests == []


def test_foreign_binding_and_currentness_never_grant_edit_credit(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        original = host.disclosures[0]
        foreign = replace(
            original,
            unit=replace(original.unit, repository_id=Repository.new().id),
        )
        host._source_messages[2] = (foreign,)  # noqa: SLF001 -- foreign identity fault
        await host.prepare(host.progress)
        assert host.active_disclosures == ()
        assert (
            foreign.identity
            in host.projection_outcomes[-1].invalidated_source_identities
        )
        host._source_messages[2] = (original,)  # noqa: SLF001 -- restore original host binding
        write(TextFile(resolve_path(tmp_path / "module.py"), SOURCE + "# changed\n"))
        with pytest.raises(ToolInputError, match="no longer current"):
            await host.prepare(host.progress)
        assert host.active_disclosures == ()
        assert len(host.requests) == 1

    asyncio.run(run())


def test_binding_must_match_actual_presented_bytes(tmp_path: Path) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        original = host.messages[-1]
        data = json.loads(original.content)
        data["text"] = "not the acquired source"
        host.messages[-1] = replace(original, content=json.dumps(data))
        with pytest.raises(ValueError, match="does not match presented"):
            await host.prepare(host.progress)
        assert host.active_disclosures == ()
        assert host.requests == []

    asyncio.run(run())


def test_foreign_scope_or_changed_occurrence_rejected_by_context(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host)
        original = host.disclosures[0]
        changed = replace(original.unit.resource, content="x" * len(SOURCE))
        host._source_messages[2] = (  # noqa: SLF001 -- invalid retained provenance
            replace(original, unit=replace(original.unit, resource=changed)),
        )
        with pytest.raises(ValueError, match="resource changed"):
            await host.prepare(host.progress)
        assert host.active_disclosures == ()

    asyncio.run(run())


def test_duplicate_native_occurrences_refused_before_provider_entry(
    tmp_path: Path,
) -> None:
    host = configured(tmp_path)
    metadata(host, "same", "one")
    metadata(host, "same", "two")
    with pytest.raises(ValueError, match="repeats a Tool call ID"):
        asyncio.run(host.prepare(host.progress))
    assert host.requests == []


def test_all_schemas_and_settings_count_against_capacity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    host = configured(tmp_path, hard=2000)
    original = host.build_request

    def request(messages: tuple[PromptMessage, ...]) -> ModelRequest:
        return replace(
            original(messages),
            tools=(ModelToolDefinition("large_schema", "x" * 3000, "{}"),),
        )

    monkeypatch.setattr(host, "build_request", request)
    with pytest.raises(ProjectionCapacityError) as caught:
        asyncio.run(host.prepare(host.progress))
    assert caught.value.outcome.request.tools[0].name == "large_schema"
    assert caught.value.outcome.original_bytes == request_bytes(
        request(tuple(host.messages)),
    )
    assert host.requests == []


@pytest.mark.parametrize(
    "operations",
    [frozenset({""}), frozenset({" "}), frozenset({3}), {"metadata"}],
)
def test_invalid_metadata_policy_refused(operations: frozenset[str] | set[str]) -> None:
    with pytest.raises(ValueError, match="policy"):
        ProjectionPolicy(100, 80, operations)  # type: ignore[arg-type]  # malformed host policy


def test_policy_above_objective_limit_is_refused(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    with pytest.raises(ValueError, match="watermarks"):
        RepositoryCodingHost(
            host.objective,
            corpus=host.corpus,
            authorize=host.authorize,
            apply_changes=host.effect,
            archive=host.archive,
            restore=host.restore,
            projection=ProjectionPolicy(40000, 30000),
        )
    host.projection = ProjectionPolicy(40000, 30000)
    with pytest.raises(ValueError, match="watermarks"):
        asyncio.run(host.prepare(CodingProgress(LIMITS)))


def test_distinct_source_retained_above_soft_target_when_hard_limit_fits(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = configured(tmp_path)
        await acquire(host, "one", 0, 7)
        await acquire(host, "two", 7, len(SOURCE))
        host.projection = ProjectionPolicy(1400, 1000)
        await host.prepare(host.progress)
        outcome = host.projection_outcomes[-1]
        assert outcome.status == "unchanged"
        assert outcome.triggered
        assert not outcome.target_reached
        assert outcome.omitted_exchanges == ()
        assert len(outcome.active_sources) == 2

    asyncio.run(run())


def test_empty_acquired_file_is_not_fabricated_to_fit_capacity(tmp_path: Path) -> None:
    async def run() -> None:
        host = configured(tmp_path, hard=1100)
        write(TextFile(resolve_path(tmp_path / "module.py"), ""))
        host.scope = host.scope.observe(
            root=host.scope.root,
            repository=Repository(host.scope.snapshot.repository_id),
            addresses=(RepositoryResourceAddress("module.py"),),
        )
        host._index()  # noqa: SLF001 -- authored empty-file observation
        await acquire(host, "empty", 0, 0)
        original = tuple(host.messages)
        with pytest.raises(ProjectionCapacityError) as caught:
            await host.prepare(host.progress)
        assert caught.value.outcome.shortened_indices == ()
        assert caught.value.outcome.request.prompt.messages == original
        assert json.loads(host.messages[-1].content)["text"] == ""
        assert host.source_results[-1].items[0].text == ""

    asyncio.run(run())
