# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- deterministic role/source/custody regressions
"""Coding working Context is useful evidence transport, not semantic acceptance."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import notes as owner
from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.models import CodingProgress
from devtools.agents.coding.projection import ProjectionPolicy
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.context import Repository
from devtools.context.planning.source import SourceRangeDisclosureOption
from devtools.context.working import NoteScope
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import InteractionSource, ModelResponse
from devtools.resources.commands import Command
from devtools.resources.filesystem import TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from devtools.tools.source import SourceScope
from tests.agents.coding.fixtures import SOURCE
from tests.agents.coding.test_post_edit import prepared_host
from tests.agents.coding.test_repository import EDIT, LIMITS, READ, call, host_at

if TYPE_CHECKING:
    from pathlib import Path


def coder(base: RepositoryCodingHost, **options: object) -> RepositoryCodingHost:
    return RepositoryCodingHost(
        base.objective,
        corpus=base.corpus,
        authorize=base.authorize,
        apply_changes=base.effect,
        archive=base.archive,
        restore=base.restore,
        working_scope=NoteScope("existing-task", "coding-worker:actor", "episode"),
        **options,  # type: ignore[arg-type]  # finite fault injection
    )


def row() -> dict[str, object]:
    start = SOURCE.index("return 6")
    return {
        "kind": "relationship",
        "text": "Provisional producer/caller contract",
        "expected_contract": "Caller requires an integer; inspect its use",
        "support": [
            {
                "reference": "source:module.py",
                "start": start,
                "end": start + 8,
                "quote": "return 6",
            },
        ],
        "contradicts": [],
        "supersedes": [],
    }


def response(content: str, *calls: object) -> ModelResponse:
    return ModelResponse(content, InteractionSource("actor"), tool_calls=calls)  # type: ignore[arg-type]


def note(value: dict[str, object] | None = None) -> str:
    return owner.PREFIX + json.dumps(
        {"working_notes": [row() if value is None else value]},
    )


async def read(host: RepositoryCodingHost) -> None:
    await host.prepare(CodingProgress(LIMITS))
    item = response("Inspect source", READ)
    host.classify(item)
    await host.acquire(item)


def test_role_contract_observed_support_and_reconstruction(tmp_path: Path) -> None:
    async def run() -> None:
        states: list[dict[str, object]] = []
        host = coder(host_at(tmp_path), observe_working=states.append)
        await read(host)
        following = response(
            note(),
            call("read_source", {"path": "module.py", "start": 0}, "note-read"),
        )
        host.classify(following)
        await host.acquire(following)
        assert host.working is not None
        retained = host.working.notes
        assert host.working.status(retained[0]) == "provisional"
        assert retained[0].verification is None
        anchor = retained[0].support[0]
        assert (
            host.working.sources[anchor.reference].reopen(anchor)["origin"]
            == "current-source"
        )
        request = await host.prepare(CodingProgress(LIMITS))
        assert request.prompt.messages[0].role == "system"
        assert "return contract" in request.prompt.messages[0].content.replace(
            "\n",
            " ",
        )
        assert "Provisional producer/caller" in request.prompt.messages[3].content
        assert states[-1]["scope"] == {
            "task": "existing-task",
            "role": "coding-worker:actor",
            "episode": "episode",
        }
        # Reconstruct from trusted retained state with the same source receipts;
        # a model response cannot supply these objects or attest a claim.
        fresh = coder(host)
        fresh.disclosures = host.disclosures.copy()
        assert fresh.working is not None
        fresh.working.restore(host.working.scope, retained)
        restored = await fresh.prepare(CodingProgress(LIMITS))
        assert "Provisional producer/caller" in restored.prompt.messages[3].content
        with pytest.raises(ValueError, match="incompatible"):
            fresh.working.restore(
                NoteScope("other", "coding-worker:actor", "episode"),
                retained,
            )

    asyncio.run(run())


@pytest.mark.parametrize(
    "role",
    ["independent-reviewer:actor", "planner:actor", "coding-worker:"],
)
def test_role_notebooks_cannot_be_inherited(tmp_path: Path, role: str) -> None:
    base = host_at(tmp_path)
    with pytest.raises(ValueError, match="coding-worker"):
        RepositoryCodingHost(
            base.objective,
            corpus=base.corpus,
            authorize=base.authorize,
            apply_changes=base.effect,
            archive=base.archive,
            restore=base.restore,
            working_scope=NoteScope("task", role, "episode"),
        )
    with pytest.raises(ValueError, match="coding-worker"):
        RepositoryCodingHost(
            base.objective,
            corpus=base.corpus,
            authorize=base.authorize,
            apply_changes=base.effect,
            archive=base.archive,
            restore=base.restore,
            observe_working=lambda _: None,
        )


def test_undisclosed_or_forged_support_is_refused_with_feedback(tmp_path: Path) -> None:
    async def run() -> None:
        host = coder(host_at(tmp_path))
        first = response(note(), READ)
        await host.prepare(CodingProgress(LIMITS))
        host.classify(first)
        assert host.working is not None
        assert not host.working.notes
        assert host.working_refusal is not None
        await host.acquire(first)
        request = await host.prepare(CodingProgress(LIMITS))
        assert json.loads(request.prompt.messages[3].content)["note_admission"]
        changed = row()
        changed["verification"] = "host:true"
        host.classify(response(note(changed)))
        assert not host.working.notes
        host.classify(response(note()))
        assert host.working_refusal is None
        assert len(host.working.notes) == 1
        host.classify(response("ordinary text"))
        assert len(host.working.notes) == 1

    asyncio.run(run())


def test_active_contract_survives_real_projection_and_source_change(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        base = prepared_host(tmp_path)
        host = coder(base)
        host.objective = replace(host.objective, prompt_bytes=24576)
        host.projection = ProjectionPolicy(16000, 12000)
        # Complete current source disclosures can be shortened, while the
        # compact provisional contract is protected independently of history.
        await host.prepare(CodingProgress(replace(LIMITS, tool_actions=30)))
        for index in range(14):
            item = response(
                "inspect",
                call(
                    "read_source",
                    {
                        "path": "module.py",
                        "start": index * 700,
                        "end": index * 700 + 1000,
                    },
                    f"r{index}",
                ),
            )
            host.classify(item)
            await host.acquire(item)
        host.classify(response(note()))
        request = await host.prepare(CodingProgress(LIMITS))
        assert "Provisional producer/caller" in request.prompt.messages[3].content
        assert host.projection_outcomes[-1].status == "reduced"
        assert host.working is not None
        fresh_read = response(
            "reopen",
            call(
                "read_source",
                {
                    "path": "module.py",
                    "start": 0,
                    "end": len(SOURCE),
                },
                "reopen",
            ),
        )
        host.classify(fresh_read)
        await host.acquire(fresh_read)
        await host.prepare(CodingProgress(LIMITS))
        edit = response("edit", EDIT)
        host.classify(edit)
        proposal = await host.propose(response("edit", EDIT))
        assert proposal is not None
        await host.apply(proposal)
        passed = await host.check(proposal)
        await host.feedback(edit, proposal, passed=passed)
        await host.prepare(CodingProgress(LIMITS))
        assert host.working.status(host.working.notes[0]) == "stale"
        assert host.working.notes[0].support[0].quote == "return 6"

    asyncio.run(run())


def test_budget_projection_is_bounded_and_explicit_about_omissions(
    tmp_path: Path,
) -> None:
    host = coder(host_at(tmp_path))
    assert host.working is not None
    for index in range(32):
        host.working.record("question", f"{index}:" + "x" * 900, "unresolved")
    result = owner.message(host.working, "error")
    assert len(result.content.encode()) <= 8192
    value = json.loads(result.content)["working_context"]
    assert value["omitted_active_sequences"]
    assert value["notes"][-1]["sequence"] == 32


def test_capture_failure_and_foreign_response_cannot_authorize_edits(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = coder(host_at(tmp_path))
        await read(host)

        def fail(_: object) -> None:
            message = "capture unavailable"
            raise ValueError(message)

        host.observe_working = fail
        with pytest.raises(ValueError, match="capture unavailable"):
            host.classify(response(note(), EDIT))
        host.observe_working = None
        assert host.working is not None
        fresh = coder(host)

        class Foreign:
            source = InteractionSource("selected")

            async def send(self, _request: object) -> ModelResponse:
                return response(note(), EDIT)

        result = await run_coding_agent(
            interaction=Foreign(),
            host=fresh,
            limits=LIMITS,
        )
        assert result.disposition == "failed"
        assert fresh.working is not None
        assert not fresh.working.notes
        assert (tmp_path / "module.py").read_text(encoding="utf-8") == SOURCE

    asyncio.run(run())


def test_fixed_type_and_consumer_checks_feed_a_real_repair(tmp_path: Path) -> None:
    """Simulated model turns, real mypy/behavior diagnostics and source effects."""

    async def run() -> None:
        base = host_at(tmp_path)
        text = (
            "def answer() -> int:\n    return 6\n\n"
            "def consume() -> int:\n    return answer() + 1\n"
        )
        path = resolve_path(tmp_path / "module.py")
        write(TextFile(path, text))
        scope = SourceScope.observe(
            root=base.scope.root,
            repository=Repository(base.scope.snapshot.repository_id),
            addresses=base.objective.editable,
        )
        plan = FixedCheckPlan(
            scope.root,
            (
                FixedCheck(
                    "return-types",
                    Command(sys.executable)
                    .args(
                        "-m",
                        "mypy",
                        "--strict",
                        "--no-incremental",
                        str(path.value),
                    )
                    .cwd(scope.root)
                    .with_timeout(Duration.seconds(30)),
                ),
                FixedCheck(
                    "consumer-behavior",
                    Command(sys.executable)
                    .args(
                        "-c",
                        "from module import consume; assert consume() == 8",
                    )
                    .cwd(scope.root)
                    .with_timeout(Duration.seconds(10)),
                ),
            ),
            scope,
        )
        base.objective = replace(base.objective, scope=scope, checks=plan)
        host = coder(base)
        unit = host.index.views[0].units[0]
        split = text.index("def consume")
        witnesses = (
            SourceRangeDisclosureOption("producer annotated int", unit, 0, split, 1024),
            SourceRangeDisclosureOption(
                "caller adds one; provisional producer relationship",
                unit,
                split,
                len(text),
                1024,
            ),
        )
        host = coder(base, contract_sources=witnesses)

        class Worker:
            source = InteractionSource("actor")
            number = 0

            async def send(self, request: object) -> ModelResponse:
                self.number += 1
                if self.number == 1:
                    serialized = str(request)
                    assert "producer annotated int" in serialized
                    assert "def answer() -> int" in serialized
                    assert "def consume() -> int" in serialized
                    assert "answer() + 1" in serialized
                    assert "provisional producer relationship" in serialized
                    return response(
                        "inspect",
                        call(
                            "read_source",
                            {
                                "path": "module.py",
                                "start": 0,
                                "end": len(text),
                            },
                            "source",
                        ),
                    )
                if self.number == 2:
                    claim = row()
                    claim["support"] = [
                        {
                            "reference": "source:module.py",
                            "start": 0,
                            "end": len("def answer() -> int:"),
                            "quote": "def answer() -> int:",
                        },
                    ]
                    return response(
                        note(claim),
                        call(
                            "replace_source",
                            {
                                "path": "module.py",
                                "old_text": "return 6",
                                "new_text": "return (7,)",
                            },
                            "wrong-type",
                        ),
                    )
                serialized = str(request)
                assert "stale; reopen" in serialized
                assert "Incompatible return value type" in serialized
                assert "TypeError" in serialized
                return response(
                    "repair",
                    call(
                        "replace_source",
                        {
                            "path": "module.py",
                            "old_text": "return (7,)",
                            "new_text": "return 7",
                        },
                        "repair",
                    ),
                )

        worker = Worker()
        result = await run_coding_agent(
            interaction=worker,
            host=host,
            limits=replace(
                LIMITS,
                model_calls=3,
                proposals=2,
                call_timeout=Duration.seconds(60),
                wall_timeout=Duration.seconds(120),
            ),
        )
        assert result.accepted
        assert worker.number == 3
        assert not host.check_results[0][0].passed
        assert not host.check_results[0][1].passed
        assert all(r.passed for r in host.check_results[1])
        assert host.working is not None
        assert host.working.notes[0].verification is None

    asyncio.run(run())


def test_contract_witness_bounds_freshness_and_projection(tmp_path: Path) -> None:
    async def run() -> None:
        base = host_at(tmp_path)
        unit = base.index.views[0].units[0]
        option = SourceRangeDisclosureOption(
            "producer and caller uncertainty",
            unit,
            0,
            unit.end,
            1024,
        )
        host = coder(
            base,
            contract_sources=(option,),
            projection=ProjectionPolicy(5000, 4000),
        )
        await read(host)
        await read_again(host)
        request = await host.prepare(CodingProgress(LIMITS))
        assert host.projection_outcomes[-1].triggered
        witnesses = [
            json.loads(m.content)
            for m in request.prompt.messages
            if '"kind": "coding_contract_witnesses"' in m.content
        ]
        assert witnesses[0]["sources"][0]["text"] == SOURCE
        assert option in host.active_disclosures
        assert host.working is not None
        assert host.working.sources["source:module.py"].spans
        with pytest.raises(ValueError, match="distinct current"):
            coder(base, contract_sources=(option, option))
        with pytest.raises(ValueError, match="distinct current"):
            coder(base, contract_sources=[option])
        with pytest.raises(ValueError, match="bounded Context"):
            coder(base, contract_sources=(replace(option, purpose="x" * 9000),))
        (tmp_path / "other").mkdir()
        other = host_at(tmp_path / "other")
        with pytest.raises(ValueError, match="distinct current"):
            coder(other, contract_sources=(option,))
        # Same snapshot ID cannot launder a foreign repository/resource witness.
        with pytest.raises(ValueError, match=r"source|Source|resource|Resource"):
            coder(
                other,
                contract_sources=(
                    replace(
                        option,
                        unit=replace(unit, snapshot_id=other.scope.snapshot.id),
                    ),
                ),
            )
        host.objective = replace(host.objective, prompt_bytes=1000)
        host.projection = ProjectionPolicy(1000, 900)
        with pytest.raises(ValueError, match=r"budget|protected input"):
            await host.prepare(CodingProgress(LIMITS))

    async def read_again(host: RepositoryCodingHost) -> None:
        item = response(
            "inspect again",
            call("read_source", {"path": "module.py", "start": 0}, "second"),
        )
        host.classify(item)
        await host.acquire(item)

    asyncio.run(run())
