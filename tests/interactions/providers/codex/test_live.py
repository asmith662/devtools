# Copyright (c) 2026
"""Opt-in end-to-end acceptance test for the locally installed Codex CLI."""

from __future__ import annotations

import asyncio
import os
import shutil
import uuid
from typing import TYPE_CHECKING

import pytest

from devtools.commands import Command, CommandExecutor
from devtools.context.message import Message, MessageRole, MessageSource
from devtools.interactions.providers.codex import CodexAgent
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


pytestmark = pytest.mark.live_codex


def _enabled() -> bool:
    """Return whether the caller explicitly enabled live Codex execution."""
    return os.environ.get("DEVTOOLS_LIVE_CODEX") == "1"


@pytest.mark.skipif(not _enabled(), reason="set DEVTOOLS_LIVE_CODEX=1 to run")
def test_codex_resumes_a_read_only_conversation_in_an_isolated_git_repo(
    tmp_path: Path,
) -> None:
    """A resumed Codex turn recalls a marker from the preceding user turn."""
    if shutil.which("git") is None:
        pytest.skip("git is required to initialize the isolated test repository")

    async def exercise() -> tuple[str, str, str, bool]:
        executor = CommandExecutor()
        initialized = await executor.execute(
            Command("git").args("init").cwd(ResolvedPath(tmp_path)),
        )
        assert initialized.succeeded

        agent = CodexAgent(executor, ResolvedPath(tmp_path))
        marker = f"DEVTOOLS-CONTINUITY-{uuid.uuid4()}"
        first = await agent.send(
            Message.new(
                f'Remember the exact marker "{marker}" for my next message. '
                'Reply only with "stored".',
                role=MessageRole.USER,
                source=MessageSource("live-test"),
            ),
        )
        second = await agent.send(
            Message.new(
                "What exact marker did I ask you to remember in my previous "
                "message? First use a shell command to attempt to create the "
                f"disposable file {tmp_path / 'write-probe.txt'}. You are in a "
                "read-only sandbox, so that command must be denied. Reply with "
                "only the marker.",
                role=MessageRole.USER,
                source=MessageSource("live-test"),
            ),
            conversation=first.conversation,
        )
        return (
            first.message.content.strip(),
            second.message.content.strip(),
            marker,
            first.conversation is not None
            and first.conversation == second.conversation,
        )

    first_response, response, marker, thread_continued = asyncio.run(exercise())
    assert first_response == "stored"
    assert response == marker
    assert thread_continued
    assert not (tmp_path / "write-probe.txt").exists()
