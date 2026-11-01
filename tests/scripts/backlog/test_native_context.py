# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, PT018, SLF001 -- exact prospective packet controls
"""Prospective configuration cannot silently upgrade old native authority."""

from __future__ import annotations

import asyncio
import copy
from typing import TYPE_CHECKING, Any

import pytest

from scripts.backlog.native.packet import (
    context_policy,
    fingerprint,
    tool_definitions,
    validate,
)
from tests.scripts.backlog.test_native import Scripted, prepared, task
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414 -- pytest fixture
)

if TYPE_CHECKING:
    from devtools.models.interaction import ModelRequest
    from scripts.backlog.work import WorkCycle


def modern() -> dict[str, Any]:
    packet = task()
    packet["context"] = {
        "schema": "native-context-v1",
        "context_tokens": 65536,
        "input_tokens": 62464,
        "reserved_output_tokens": 2048,
        "disclosure_bytes": 65536,
        "warning_bytes": 98304,
        "trigger_bytes": 114688,
        "target_bytes": 98304,
    }
    packet["budgets"]["prompt_bytes"] = 131072
    return packet


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("schema", "native-context-unknown"),
        ("context_tokens", 131073),
        ("context_tokens", 32768),
        ("input_tokens", 65536),
        ("reserved_output_tokens", 1),
        ("disclosure_bytes", 0),
        ("disclosure_bytes", True),
        ("disclosure_bytes", 131073),
        ("warning_bytes", 114689),
        ("warning_bytes", 0),
        ("target_bytes", 114689),
        ("trigger_bytes", 131073),
    ],
)
def test_invalid_profile(key: str, value: object) -> None:
    packet = modern()
    packet["context"][key] = value
    with pytest.raises(ValueError, match=r"profile|policy|allowance|capacity|budgets"):
        validate(packet)


def test_profile_is_exact_and_does_not_raise_edit_or_old_grant_limits() -> None:
    packet = modern()
    validate(packet)
    context = context_policy(packet)
    assert (
        context is not None
        and context.disclosure_bytes > packet["budgets"]["source_bytes"]
    )
    assert len(tool_definitions(packet)) == 5 and len(tool_definitions(task())) == 3
    assert context_policy(task()) is None
    assert fingerprint(packet) != fingerprint(task())
    old = task()
    old["budgets"]["prompt_bytes"] = 65536
    with pytest.raises(ValueError, match="budgets"):
        validate(old)
    changed = copy.deepcopy(packet)
    changed["budgets"]["source_bytes"] = 65536
    with pytest.raises(ValueError, match="budgets"):
        validate(changed)
    changed = copy.deepcopy(packet)
    changed["context"]["unapproved"] = True
    with pytest.raises(TypeError):
        validate(changed)


def test_provider_qualification_precedes_dispatch_and_bad_token_fit_never_enters(
    repository: tuple[WorkCycle, str],
) -> None:
    async def run() -> None:
        cycle, item = repository
        await prepared(cycle, item, modern())
        worker = Scripted("neutral-script-a")

        async def tokens(_request: ModelRequest) -> int:
            return 62465

        for callback, qualified in [
            (None, 65536),
            (tokens, None),
            (tokens, True),
            (tokens, 32768),
        ]:
            with pytest.raises(PermissionError, match="qualified"):
                await cycle.native.execute(
                    item,
                    interaction=worker,
                    profile="scripted-v1",
                    authorize=lambda _: True,
                    measure_input=callback,
                    provider_context_tokens=qualified,
                )
            assert not (cycle._folder(item) / "dispatch.json").exists()
            assert not (cycle.root / ".local/backlog/checkout-owner").exists()
        result = await cycle.native.execute(
            item,
            interaction=worker,
            profile="scripted-v1",
            authorize=lambda _: True,
            measure_input=tokens,
            provider_context_tokens=65536,
        )
        assert result["disposition"] == "BLOCKED" and not worker.requests
        assert result["facts"]["failure_phase"] == "preparation"
        assert (
            result["facts"]["restored"]
            and not result["facts"]["reconciliation_required"]
        )

    asyncio.run(run())
