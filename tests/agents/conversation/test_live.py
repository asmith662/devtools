# Copyright (c) 2026
"""Opt-in real Conversation and Codex continuation acceptance."""

from __future__ import annotations

import asyncio
import os
import shutil
import uuid
from typing import TYPE_CHECKING

import pytest

from devtools.agents.conversation import (
    Conversation,
    ConversationId,
    ConversationMessage,
    ConversationMessageRole,
    InteractionSource,
)
from devtools.agents.integrations.codex import CodexAgent
from devtools.core.paths import ResolvedPath
from devtools.resources.commands import Command, CommandExecutor

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.core.time import Timestamp


pytestmark = pytest.mark.live_codex


def _enabled() -> bool:
    """Return whether the caller explicitly enabled live Codex execution."""
    return os.environ.get("DEVTOOLS_LIVE_CODEX") == "1"


@pytest.mark.skipif(not _enabled(), reason="set DEVTOOLS_LIVE_CODEX=1 to run")
def test_session_retains_a_read_only_codex_continuation(
    tmp_path: Path,
) -> None:
    """A Conversation retains history and a real Codex continuation across turns."""
    if shutil.which("git") is None:
        pytest.skip("git is required to initialize the isolated test repository")

    async def exercise() -> tuple[
        Conversation,
        ConversationId,
        Timestamp,
        str,
        str,
        bool,
        tuple[
            ConversationMessage,
            ConversationMessage,
            ConversationMessage,
            ConversationMessage,
        ],
    ]:
        executor = CommandExecutor()
        initialized = await executor.execute(
            Command("git").args("init").cwd(ResolvedPath(tmp_path)),
        )
        assert initialized.succeeded

        codex = CodexAgent(executor, ResolvedPath(tmp_path))
        session = Conversation.new()
        original_id = session.id
        original_created_at = session.created_at
        marker = f"DEVTOOLS-SESSION-CONTINUITY-{uuid.uuid4()}"
        first_user = ConversationMessage.new(
            f'Remember the exact marker "{marker}" for my next message. '
            'Reply only with "stored".',
            role=ConversationMessageRole.USER,
            source=InteractionSource("live-test"),
        )
        async with session.turn():
            session.add(first_user)
            first_conversation = session.conversation_for(codex.source)
            assert first_conversation is None

            first_turn = await codex.send(
                first_user,
                conversation=first_conversation,
            )
            assert first_turn.message.content.strip() == "stored"
            assert first_turn.conversation is not None
            session.add(first_turn.message)
            session.set_conversation(first_turn.conversation)

        second_user = ConversationMessage.new(
            "What exact marker did I ask you to remember in my previous "
            "message? First use a shell command to attempt to create the "
            f"disposable file {tmp_path / 'write-probe.txt'}. You are in a "
            "read-only sandbox, so that command must be denied. Reply with "
            "only the marker.",
            role=ConversationMessageRole.USER,
            source=InteractionSource("live-test"),
        )
        async with session.turn():
            session.add(second_user)
            stored_ref = session.conversation_for(codex.source)
            assert stored_ref == first_turn.conversation

            second_turn = await codex.send(second_user, conversation=stored_ref)
            assert second_turn.conversation is not None
            session.add(second_turn.message)
            session.set_conversation(second_turn.conversation)
            assert session.conversation_for(codex.source) == second_turn.conversation

        return (
            session,
            original_id,
            original_created_at,
            marker,
            second_turn.message.content.strip(),
            first_turn.conversation == second_turn.conversation,
            (
                first_user,
                first_turn.message,
                second_user,
                second_turn.message,
            ),
        )

    (
        session,
        original_id,
        original_created_at,
        marker,
        response,
        same_thread,
        expected_messages,
    ) = asyncio.run(exercise())
    assert response == marker
    assert session.history.messages == expected_messages
    assert session.id == original_id
    assert session.created_at == original_created_at
    assert same_thread
    assert session.conversation_for(InteractionSource("codex")) is not None
    assert not (tmp_path / "write-probe.txt").exists()
