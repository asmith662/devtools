# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, ANN401, C901, PLR0912 -- literal fault schedules
"""Real neutral host preparation with bounded, scripted auxiliary interactions."""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

import pytest

from devtools.agents.coding.compaction import (
    SummaryAttempt,
    SummaryCompaction,
    SummarySelection,
)
from devtools.agents.coding.compaction.format import validate_summary
from devtools.agents.coding.compaction.operation import SemanticCompactor
from devtools.agents.coding.models import CodingEffect, CodingProgress
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    project_request,
    request_bytes,
)
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelTermination,
    ModelUsage,
    Prompt,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools.errors import ToolInputError
from tests.agents.coding.test_projection import acquire, configured, metadata
from tests.agents.coding.test_repository import EDIT, LIMITS, host_at

if TYPE_CHECKING:
    from pathlib import Path


class Summarizer:
    """Scripted notes cite actual supplied input, never synthetic execution facts."""

    source = InteractionSource("independent-summary")

    def __init__(self, fault: str = "") -> None:
        """Keep precise call count and explicitly authorized test payloads."""
        self.requests: list[ModelRequest] = []
        self.fault = fault
        self.error = RuntimeError("unknown auxiliary outcome")

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Interpret only the test script; no real inference or Tool execution."""
        self.requests.append(request)
        if self.fault == "transport":
            raise self.error
        if self.fault == "cancel":
            raise asyncio.CancelledError
        if self.fault == "timeout":
            await asyncio.sleep(2)
        value = json.loads(request.prompt.messages[1].content)
        refs = [
            {"index": i, "digest": value["records"][str(i)]["digest"]}
            for i in value["replacement_indices"]
        ]
        text = json.dumps(
            {
                "version": 1,
                "notes": [
                    {
                        "kind": "rejected_hypothesis",
                        "text": (
                            "The return-8 hypothesis failed; "
                            "preserve zero and return seven."
                        ),
                        "refs": refs,
                    },
                ],
                "sources": list(value["historical_sources"]),
            },
        )
        if self.fault == "malformed":
            text = "{"
        if self.fault == "empty":
            text = " "
        if self.fault == "oversized":
            text = "x" * 20000
        if self.fault == "foreign-ref":
            text = text.replace(refs[0]["digest"], "foreign")
        return ModelResponse(
            text,
            InteractionSource("foreign") if self.fault == "foreign" else self.source,
            usage=ModelUsage(input_tokens=10, output_tokens=20),
            termination=ModelTermination.OUTPUT_LIMIT
            if self.fault == "output-limit"
            else None
            if self.fault == "unknown-stop"
            else ModelTermination.NORMAL_STOP,
        )


def configuration(model: Summarizer, **changes: Any) -> SummaryCompaction:
    return replace(
        SummaryCompaction(
            model,
            lambda _: SummarySelection(frozenset({2, 3}), frozenset({2, 3})),
            2,
            20000,
            4096,
            ModelSettings(maximum_output_tokens=512),
            Duration.seconds(1),
        ),
        **changes,
    )


def setup(
    root: Path,
    model: Summarizer | None = None,
    **changes: Any,
) -> RepositoryCodingHost:
    host = configured(root, hard=10000)
    metadata(host, "old", "return-8 hypothesis rejected; " + "irrelevant " * 700)
    host.messages.append(PromptMessage("assistant", "Recent exact progress"))
    host.compaction = SemanticCompactor(configuration(model or Summarizer(), **changes))
    return host


def latest(host: RepositoryCodingHost) -> SummaryAttempt:
    assert host.compaction is not None
    return host.compaction.attempts[-1]


def prepare(host: RepositoryCodingHost) -> ModelRequest:
    return asyncio.run(host.prepare(CodingProgress(LIMITS)))


def test_explicit_adoption_history_native_and_separate_usage(tmp_path: Path) -> None:
    model = Summarizer()
    host = setup(tmp_path, model, retain_payloads=True)
    original = tuple(host.messages)
    deterministic = prepare(host)
    assert model.requests == []
    assert "return-8 hypothesis" not in str(deterministic)
    host.request_compaction()
    result = prepare(host)
    assert tuple(host.messages) == original
    assert "hypothesis failed" in str(result)
    assert result.prompt.messages[0] == original[0]
    assert result.prompt.messages[-2] == original[-1]
    Prompt("", "messages", result.prompt.messages)
    assert host.compaction is not None
    receipt = latest(host)
    assert receipt.status == "adopted"
    assert receipt.entered
    assert receipt.response_received
    assert receipt.validated
    assert receipt.adopted
    assert receipt.partial_coverage
    assert receipt.input_indices == (2, 3)
    assert receipt.usage == ModelUsage(input_tokens=10, output_tokens=20)
    assert receipt.request == model.requests[0]
    assert receipt.response is not None
    assert receipt.original_bytes is not None
    assert receipt.resulting_bytes == request_bytes(result) < receipt.original_bytes
    assert host.responses == []  # auxiliary evidence is not acting-model evidence
    again = prepare(host)
    assert again == result
    assert len(model.requests) == 1
    host.request_compaction()
    assert prepare(host) == result
    assert latest(host).status == "prior-entry-not-replayed"


@pytest.mark.parametrize(
    "fault",
    [
        "transport",
        "timeout",
        "malformed",
        "empty",
        "oversized",
        "foreign-ref",
        "foreign",
        "output-limit",
        "unknown-stop",
    ],
)
def test_optional_failure_preserves_exact_valid_fallback(
    tmp_path: Path,
    fault: str,
) -> None:
    model = Summarizer(fault)
    host = setup(tmp_path, model, timeout=Duration.seconds(0.01))
    original = tuple(host.messages)
    fallback = prepare(host)
    host.request_compaction()
    assert prepare(host) == fallback
    receipt = latest(host)
    assert receipt.status == "failed"
    assert not receipt.adopted
    assert receipt.entered
    assert receipt.error is not None
    assert receipt.request is None
    assert receipt.response is None
    assert tuple(host.messages) == original
    if fault == "transport":
        assert receipt.error is model.error
        assert receipt.usage is None
    host.request_compaction()
    assert prepare(host) == fallback
    assert len(model.requests) == 1


def test_cancellation_propagates_without_projection_installation(
    tmp_path: Path,
) -> None:
    host = setup(tmp_path, Summarizer("cancel"))
    host.request_compaction()
    with pytest.raises(asyncio.CancelledError):
        prepare(host)
    assert host.requests == []
    assert latest(host).status == "cancelled"
    assert len(host.messages) == 5


@pytest.mark.parametrize("budget", [1, 1500])
def test_bounded_input_never_enters_with_unavailable_material(
    tmp_path: Path,
    budget: int,
) -> None:
    model = Summarizer()
    host = setup(tmp_path, model, input_bytes=budget)
    fallback = prepare(host)
    host.request_compaction()
    assert prepare(host) == fallback
    assert model.requests == []
    assert latest(host).status in {"failed", "no-eligible-input"}


@pytest.mark.parametrize("tokens", [-1, True, 201, 100])
def test_provider_measurement_explicit_and_separate(
    tmp_path: Path,
    tokens: int,
) -> None:
    async def measure(_request: ModelRequest) -> int:
        return tokens

    model = Summarizer()
    host = setup(tmp_path, model, measure_input=measure, input_tokens=200)
    host.request_compaction()
    prepare(host)
    receipt = latest(host)
    assert receipt.measured_input_tokens == tokens
    assert receipt.entered is (type(tokens) is int and tokens == 100)


@pytest.mark.parametrize("indices", [{0}, {1}, {3}, {500}])
def test_protected_partial_and_foreign_replacements_refused(
    tmp_path: Path,
    indices: set[int],
) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        select=lambda _: SummarySelection(frozenset(indices), frozenset(indices)),
    )
    host.request_compaction()
    prepare(host)
    assert model.requests == []
    assert latest(host).status == "failed"


def test_privacy_selection_excludes_unselected_policy_and_reasoning(
    tmp_path: Path,
) -> None:
    model = Summarizer()
    host = setup(tmp_path, model)
    host.messages[0] = PromptMessage("user", "PRIVATE-POLICY-SENTINEL")
    host.messages[2] = replace(host.messages[2], reasoning_content="PRIVATE-REASONING")
    host.messages.append(PromptMessage("assistant", "PRIVATE-RECENT-SENTINEL"))
    host.request_compaction()
    result = prepare(host)
    exported = str(model.requests[0])
    assert "PRIVATE-" not in exported
    assert "PRIVATE-POLICY-SENTINEL" in str(result)
    assert "PRIVATE-RECENT-SENTINEL" in str(result)


def test_source_references_cannot_supply_active_witness(tmp_path: Path) -> None:
    host = configured(tmp_path, hard=10000)
    asyncio.run(acquire(host))
    host.messages.append(PromptMessage("assistant", "Current unrelated progress"))
    host.compaction = SemanticCompactor(configuration(Summarizer()))
    # A short result cannot be usefully compacted; preserve exact source instead.
    host.request_compaction()
    prepare(host)
    assert latest(host).validated
    assert latest(host).status == "insufficient-reduction"
    assert host.active_disclosures


def test_missing_configuration_and_constructor_boundary(tmp_path: Path) -> None:
    host = host_at(tmp_path)
    with pytest.raises(ValueError, match="authorized"):
        host.request_compaction()
    args: dict[str, Any] = {
        "corpus": host.corpus,
        "authorize": host.authorize,
        "apply_changes": host.effect,
        "archive": host.archive,
        "restore": host.restore,
        "summary": configuration(Summarizer()),
    }
    with pytest.raises(ValueError, match="requires"):
        RepositoryCodingHost(host.objective, **args)
    configured_host = RepositoryCodingHost(
        host.objective,
        projection=ProjectionPolicy(30000, 24000),
        **args,
    )
    assert configured_host.compaction is not None


@pytest.mark.parametrize(
    "change",
    [
        {"maximum_calls": 0},
        {"output_bytes": True},
        {"input_bytes": -1},
        {"recent_exchanges": 0},
        {"settings": ModelSettings()},
        {"timeout": Duration.seconds(0)},
        {"input_tokens": 10},
        {"input_tokens": 0, "measure_input": lambda _: None},
    ],
)
def test_invalid_envelopes(change: dict[str, Any]) -> None:
    with pytest.raises(ValueError, match="configuration"):
        configuration(Summarizer(), **change)


@pytest.mark.parametrize(
    ("disclose", "replace_indices"),
    [
        ({1}, frozenset({1})),
        (frozenset({1}), {1}),
        (frozenset({1}), frozenset({2})),
        (frozenset({-1}), frozenset()),
        (frozenset({True}), frozenset()),
    ],
)
def test_invalid_selections(disclose: Any, replace_indices: Any) -> None:
    with pytest.raises(ValueError, match="selection"):
        SummarySelection(disclose, replace_indices)


@pytest.mark.parametrize(
    "fault",
    [
        "duplicate",
        "shape",
        "version",
        "empty",
        "kind",
        "text",
        "long",
        "refs",
        "foreign",
        "duplicate-ref",
        "missing-citation",
        "source",
        "duplicate-source",
    ],
)
def test_structural_and_provenance_refusals(fault: str) -> None:
    value: dict[str, Any] = {
        "version": 1,
        "notes": [
            {
                "kind": "decision",
                "text": "qualified",
                "refs": [{"index": 1, "digest": "exact"}],
            },
        ],
        "sources": [],
    }
    if fault == "duplicate":
        serialized = '{"version":1,"version":1}'
    else:
        if fault == "shape":
            value["accepted"] = True
        if fault == "version":
            value["version"] = True
        if fault == "empty":
            value["notes"] = []
        if fault == "kind":
            value["notes"][0]["kind"] = "permission"
        if fault == "text":
            value["notes"][0]["text"] = " "
        if fault == "long":
            value["notes"][0]["text"] = "x" * 2049
        if fault == "refs":
            value["notes"][0]["refs"] = []
        if fault == "foreign":
            value["notes"][0]["refs"][0]["digest"] = "foreign"
        if fault == "duplicate-ref":
            value["notes"][0]["refs"] *= 2
        if fault == "source":
            value["sources"] = ["foreign"]
        if fault == "duplicate-source":
            value["sources"] = ["known", "known"]
        serialized = json.dumps(value)
    with pytest.raises(ValueError, match=r"summary|working-state|Summary"):
        validate_summary(
            serialized,
            {1: "exact"},
            frozenset({2} if fault == "missing-citation" else {1}),
            {"known": {}},
        )


def test_summary_of_acquired_source_does_not_authorize_edit(tmp_path: Path) -> None:
    host = configured(tmp_path, hard=16000)
    asyncio.run(acquire(host))
    host.messages[2] = replace(host.messages[2], content="older reasoning " * 600)
    host.messages.append(PromptMessage("assistant", "Recent exact work"))
    host.compaction = SemanticCompactor(configuration(Summarizer()))
    history = tuple(host.messages)
    host.request_compaction()
    result = prepare(host)
    assert latest(host).adopted
    assert "historical_sources" in result.prompt.messages[-1].content
    assert host.active_disclosures == ()
    assert tuple(host.messages) == history
    response = ModelResponse("propose", InteractionSource("acting"), tool_calls=(EDIT,))
    assert asyncio.run(host.propose(response)) is None
    assert json.loads(host.messages[-1].content) == {
        "status": "REFUSED",
        "reason": "Exact current edit source was not acquired.",
    }
    assert host.check_results == []


@pytest.mark.parametrize(
    "change",
    ["history", "policy", "protected", "capacity", "selector-error"],
)
def test_cached_notes_revalidated_without_auxiliary_replay(
    tmp_path: Path,
    change: str,
) -> None:
    host = setup(tmp_path)
    host.request_compaction()
    prepare(host)
    assert latest(host).adopted
    assert host.compaction is not None
    if change == "history":
        host.messages[0] = replace(host.messages[0], content="New exact constraint")
    if change == "policy":
        host.compaction.config = replace(
            host.compaction.config,
            select=lambda _: SummarySelection(frozenset(), frozenset()),
        )
    if change == "protected":
        host._check_feedback.add(2)  # noqa: SLF001 -- host-protected feedback boundary
    if change == "capacity":
        host.objective = replace(host.objective, prompt_bytes=2000)
        host.projection = ProjectionPolicy(1900, 1800, frozenset({"list_repository"}))
    if change == "selector-error":

        def fail(_messages: object) -> SummarySelection:
            message = "policy unavailable"
            raise RuntimeError(message)

        host.compaction.config = replace(host.compaction.config, select=fail)
    result = prepare(host)
    assert "derived_working_state" not in str(result)
    assert sum(a.entered for a in host.compaction.attempts) == 1


def test_multiple_compactions_original_provenance_and_call_budget(
    tmp_path: Path,
) -> None:
    model = Summarizer()
    host = setup(tmp_path, model)
    host.request_compaction()
    prepare(host)
    metadata(host, "new", "New investigation " * 400)
    host.messages.append(PromptMessage("assistant", "Newest exact work"))
    assert host.compaction is not None
    host.compaction.config = replace(
        host.compaction.config,
        select=lambda _: SummarySelection(
            frozenset({2, 3, 5, 6}),
            frozenset({2, 3, 5, 6}),
        ),
    )
    history = tuple(host.messages)
    host.request_compaction()
    prepare(host)
    assert latest(host).adopted
    assert len(model.requests) == 2
    assert "derived_working_state" not in str(model.requests[1])
    assert latest(host).replaced_indices == (2, 3, 5, 6)
    host.request_compaction()
    prepare(host)
    assert latest(host).status == "call-budget-exhausted"
    assert tuple(host.messages) == history


@pytest.mark.parametrize("mutation", ["history", "source", "observation"])
def test_changes_and_observation_failure_during_auxiliary_entry(
    tmp_path: Path,
    mutation: str,
) -> None:
    host = setup(tmp_path)

    class Changed(Summarizer):
        async def send(self, request: ModelRequest) -> ModelResponse:
            response = await super().send(request)
            if mutation == "history":
                host.messages.append(PromptMessage("user", "New host constraint"))
            elif mutation == "source":
                write(TextFile(resolve_path(tmp_path / "module.py"), "foreign bytes"))
            else:
                raise self.error  # known internally, unavailable to caller: no Option B
            return response

    model = Changed()
    host.compaction = SemanticCompactor(configuration(model))
    host.request_compaction()
    if mutation == "observation":
        prepare(host)
        assert latest(host).response_received is False
        assert latest(host).usage is None
        assert latest(host).error is model.error
    else:
        with pytest.raises((ValueError, ToolInputError), match=r"changed|current"):
            prepare(host)
        assert host.requests == []
    assert latest(host).entered
    assert not latest(host).adopted


def test_no_strategy_fits_preserves_original_history(tmp_path: Path) -> None:
    host = setup(tmp_path, Summarizer("malformed"))
    host.messages[0] = PromptMessage("user", "MANDATORY " * 1500)
    history = tuple(host.messages)
    host.request_compaction()
    with pytest.raises(ProjectionCapacityError):
        prepare(host)
    assert latest(host).status == "failed"
    assert tuple(host.messages) == history
    assert host.requests == []


def test_partial_input_coverage_and_disjoint_source_catalog(tmp_path: Path) -> None:
    host = configured(tmp_path, hard=20000)
    asyncio.run(acquire(host, "first", 0, 5))
    asyncio.run(acquire(host, "second", 5, 10))
    host.messages[2] = replace(host.messages[2], content="old investigation " * 300)
    metadata(host, "oversized", "private huge result " * 1000)
    host.messages.append(PromptMessage("assistant", "Recent exact work"))
    model = Summarizer()
    host.compaction = SemanticCompactor(
        configuration(
            model,
            input_bytes=15000,
            select=lambda _: SummarySelection(
                frozenset(range(2, 8)),
                frozenset(range(2, 8)),
            ),
        ),
    )
    host.request_compaction()
    prepare(host)
    receipt = latest(host)
    assert receipt.adopted
    assert receipt.input_indices == (2, 3, 4, 5)
    assert receipt.partial_coverage
    payload = json.loads(model.requests[0].prompt.messages[1].content)
    assert [v["span"] for v in payload["historical_sources"].values()] == [
        [0, 5],
        [5, 10],
    ]
    assert "private huge result" not in str(model.requests[0])


def test_unacknowledged_effect_prevents_auxiliary_entry(tmp_path: Path) -> None:

    model = Summarizer()
    host = setup(tmp_path, model)
    progress = CodingProgress(LIMITS)
    progress.effects.append(CodingEffect("edit", ("lost-ack",)))
    host.request_compaction()
    with pytest.raises(ValueError, match="Unacknowledged"):
        asyncio.run(host.prepare(progress))
    assert model.requests == []


def test_disclosure_permission_does_not_imply_replacement_permission(
    tmp_path: Path,
) -> None:
    model = Summarizer()
    host = setup(
        tmp_path,
        model,
        select=lambda _: SummarySelection(
            frozenset({0, 1, 2, 3, 4}),
            frozenset({2, 3}),
        ),
    )
    host.request_compaction()
    result = prepare(host)
    assert latest(host).adopted
    assert not latest(host).partial_coverage
    assert latest(host).input_indices == (0, 1, 2, 3, 4)
    assert result.prompt.messages[0] == host.messages[0]
    assert result.prompt.messages[-2] == host.messages[-1]


@pytest.mark.parametrize(
    ("indices", "note"),
    [
        (frozenset({0}), PromptMessage("assistant", "notes")),
        (frozenset({1}), PromptMessage("assistant", "notes")),
        (frozenset({2, 3}), PromptMessage("user", "untrusted promoted")),
        (frozenset({2, 3}), None),
        (frozenset(), PromptMessage("assistant", "notes")),
    ],
)
def test_projection_itself_refuses_invalid_semantic_replacement(
    tmp_path: Path,
    indices: frozenset[int],
    note: PromptMessage | None,
) -> None:
    host = setup(tmp_path)
    assert host.projection is not None
    with pytest.raises(ValueError, match="whole unprotected"):
        project_request(
            host.build_request(tuple(host.messages)),
            policy=host.projection,
            hard_bytes=10000,
            snapshot=host.scope.snapshot,
            sources={},
            summarized_indices=indices,
            summary=note,
        )


def test_summary_can_fit_when_deterministic_omission_cannot(tmp_path: Path) -> None:
    model = Summarizer()
    host = configured(tmp_path, hard=5000)
    host.messages.extend(
        (
            PromptMessage(
                "assistant",
                "Earlier investigation and rejected hypothesis. " * 200,
            ),
            PromptMessage("assistant", "Recent exact task state"),
        ),
    )
    host.compaction = SemanticCompactor(
        configuration(
            model,
            select=lambda _: SummarySelection(frozenset({2}), frozenset({2})),
        ),
    )
    history = tuple(host.messages)
    with pytest.raises(ProjectionCapacityError):
        prepare(host)
    assert model.requests == []
    host.request_compaction()
    request = prepare(host)
    assert latest(host).adopted
    assert request_bytes(request) < 5000
    assert "hypothesis failed" in str(request)
    assert tuple(host.messages) == history


def test_summarizer_source_bound_before_entry(tmp_path: Path) -> None:
    class ChangedSource(Summarizer):
        async def send(self, request: ModelRequest) -> ModelResponse:
            self.source = InteractionSource("changed-during-entry")
            return await super().send(request)

    model = ChangedSource()
    host = setup(tmp_path, model)
    selected_source = model.source
    host.request_compaction()
    prepare(host)
    assert latest(host).source == selected_source
    assert latest(host).response_received
    assert latest(host).status == "failed"
    assert not latest(host).adopted
