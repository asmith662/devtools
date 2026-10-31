# Copyright (c) 2026
# ruff: noqa: D103, PLR2004 -- authored independent continuation/effect assertions
"""Real edit, failed pytest check, affordable current Context and selected repair."""

from __future__ import annotations

import asyncio
import json
import sys
from dataclasses import replace
from typing import TYPE_CHECKING

import pytest

from devtools.agents.coding import run_coding_agent
from devtools.agents.coding.models import CodingLimits, CodingProgress, CodingResult
from devtools.agents.coding.projection import (
    ProjectionCapacityError,
    ProjectionPolicy,
    native_exchange_ranges,
    request_bytes,
)
from devtools.agents.coding.repository import RepositoryCodingHost
from devtools.context import Repository, RepositoryResourceAddress
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    PromptMessage,
)
from devtools.resources.filesystem import TextFile, write
from devtools.tools.checks import FixedCheck, FixedCheckPlan
from tests.agents.coding.fixtures import SOURCE
from tests.agents.coding.test_inventory import inventory
from tests.agents.coding.test_joint_projection import host_source
from tests.agents.coding.test_repository import call, host_at

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path


def prepared_host(root: Path) -> RepositoryCodingHost:
    base = host_at(root)
    text = SOURCE + ("# keep " + "x" * 1100 + "\n") * 20
    write(TextFile(resolve_path(root / "module.py"), text))
    scope = base.scope.observe(
        root=base.scope.root,
        repository=Repository(base.scope.snapshot.repository_id),
        addresses=base.objective.editable,
    )
    for folder, assertion in (
        ("behavior", "assert values['answer']() == 7"),
        ("preservation", "assert '# keep' in text"),
    ):
        path = root / folder / "focused.py"
        path.parent.mkdir()
        write(
            TextFile(
                resolve_path(path),
                "from pathlib import Path\n\ndef test_contract():\n"
                "    text = Path('module.py').read_text(encoding='utf-8')\n"
                "    values = {}\n    exec(text, values)\n    " + assertion + "\n",
            ),
        )
    check = FixedCheck.pytest(
        "focused",
        python=sys.executable,
        root=scope.root,
        targets=("behavior/focused.py", "preservation/focused.py"),
        timeout=Duration.seconds(15),
    )
    return RepositoryCodingHost(
        replace(
            base.objective,
            scope=scope,
            checks=FixedCheckPlan(scope.root, (check,), scope),
            edits=replace(base.objective.edits, source_bytes=32768, region_bytes=4096),
            disclosure_bytes=8192,
            prompt_bytes=32768,
        ),
        corpus=base.corpus,
        authorize=base.authorize,
        apply_changes=base.effect,
        archive=base.archive,
        restore=base.restore,
        projection=ProjectionPolicy(24576, 20000),
    )


async def supply(host: RepositoryCodingHost) -> tuple[PromptMessage, ...]:
    for number in range(14):
        await host_source(host, number * 700, number * 700 + 1000)
    host.messages.append(
        PromptMessage("user", "Never change checks, scope or unrelated source."),
    )
    return tuple(host.messages[2:])


def test_real_post_edit_failure_is_consumed_and_repaired(
    tmp_path: Path,
    record_property: Callable[[str, object], None],
) -> None:
    async def run() -> None:
        host = prepared_host(tmp_path)
        original = (tmp_path / "module.py").read_bytes()
        retained = await supply(host)
        old_snapshot = str(host.scope.snapshot.id)
        archived: dict[RepositoryResourceAddress, str | None] = {}
        host.archive = archived.update
        requests: list[ModelRequest] = []

        class Worker:
            source = InteractionSource("independent-post-edit-repair")

            async def send(self, request: ModelRequest) -> ModelResponse:
                requests.append(request)
                native_exchange_ranges(request.prompt.messages)
                assert request_bytes(request) <= 32768
                data = inventory(request)
                if len(requests) == 1:
                    assert data["snapshot_id"] == old_snapshot
                    old, new, identity = "return 6", "return 8", "wrong"
                else:
                    assert (
                        data["snapshot_id"]
                        == str(host.scope.snapshot.id)
                        != old_snapshot
                    )
                    feedback = json.loads(request.prompt.messages[-1].content)
                    assert request.prompt.messages[-1].tool_call_id == "wrong"
                    assert feedback["passed"] is False
                    assert feedback["checks"][0]["exit_code"] == 1
                    assert "return 8" in feedback["sources"][0]["text"]
                    outcome = host.projection_outcomes[-1]
                    assert outcome.original_bytes > 32768
                    assert len(outcome.shortened_indices) == 14
                    assert all(
                        o.snapshot_id == host.scope.snapshot.id
                        for o in host.active_disclosures
                    )
                    assert len(host.active_disclosures) == 1
                    for message in request.prompt.messages:
                        if '"restriction"' in message.content:
                            row = json.loads(message.content)
                            assert (
                                row["restriction"]
                                == "Only the authorized return value may change."
                            )
                            assert row["text"]["omitted"] == "stale-snapshot"
                    assert tuple(host.messages[2 : 2 + len(retained)]) == retained
                    record_property("post_edit_original_bytes", outcome.original_bytes)
                    record_property(
                        "post_edit_projected_bytes",
                        outcome.resulting_bytes,
                    )
                    old, new, identity = "return 8", "return 7", "repair"
                return ModelResponse(
                    "",
                    self.source,
                    tool_calls=(
                        call(
                            "replace_source",
                            {"path": "module.py", "old_text": old, "new_text": new},
                            identity,
                        ),
                    ),
                )

        result = await run_coding_agent(
            Worker(),
            host=host,
            limits=CodingLimits(4, 2, 4, Duration.seconds(10), Duration.seconds(60)),
        )
        assert result.accepted, result.error
        assert len(requests) == 2
        assert result.progress.proposals == 2
        assert [rows[0].command_result.exit_code for rows in host.check_results] == [
            1,
            0,
        ]
        assert all(e.acknowledged for e in result.progress.effects)
        candidate = next(iter(archived.values()))
        assert candidate is not None
        assert "return 7" in candidate
        assert (tmp_path / "module.py").read_bytes() == original
        assert inventory(requests[0])["snapshot_id"] == old_snapshot
        assert result.custody.restored

    asyncio.run(run())


def test_protected_after_image_overflow_and_missing_witness_refuse(
    tmp_path: Path,
) -> None:
    async def run() -> None:
        host = prepared_host(tmp_path)
        await supply(host)
        state = CodingProgress(
            CodingLimits(4, 3, 4, Duration.seconds(5), Duration.seconds(60)),
        )
        await host.prepare(state)
        response = ModelResponse(
            "",
            InteractionSource("post-edit-negative"),
            tool_calls=(
                call(
                    "replace_source",
                    {
                        "path": "module.py",
                        "old_text": "return 6",
                        "new_text": "return 8",
                    },
                    "first",
                ),
            ),
        )
        host.classify(response)
        proposal = await host.propose(response)
        assert proposal
        await host.apply(proposal)
        assert not host.active_disclosures
        assert not await host.check(proposal)
        await host.feedback(response, proposal, passed=False)
        # A known current after-image in retained feedback is not active until
        # a valid full Prompt is selected. Even an unchanged anchor needs that witness.
        forbidden = ModelResponse(
            "",
            response.source,
            tool_calls=(
                call(
                    "replace_source",
                    {
                        "path": "module.py",
                        "old_text": "# \u03c0",
                        "new_text": "# changed",
                    },
                    "no-active-source",
                ),
            ),
        )
        host.classify(forbidden)
        assert await host.propose(forbidden) is None
        assert "not acquired" in host.messages[-1].content
        host.objective = replace(host.objective, prompt_bytes=4000)
        host.projection = ProjectionPolicy(4000, 4000)
        with pytest.raises(ProjectionCapacityError) as caught:
            await host.prepare(state)
        assert caught.value.outcome.status == "insufficient"
        assert not host.active_disclosures
        assert "return 8" in (tmp_path / "module.py").read_text(encoding="utf-8")
        completion = await host.finish(
            CodingResult(
                "failed",
                candidate_validated=False,
                completed=False,
                progress=state,
            ),
        )
        assert completion.restored

    asyncio.run(run())
