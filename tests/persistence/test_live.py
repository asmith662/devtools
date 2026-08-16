# Copyright (c) 2026
"""Opt-in SQLite reconstruction through Runtime and real Codex acceptance."""
from __future__ import annotations

import asyncio
import os
import shutil
import uuid
from typing import TYPE_CHECKING

import pytest

from devtools.codex import CodexAgent
from devtools.commands import Command, CommandExecutor
from devtools.context import Message, MessageRole, MessageSource, Session, SessionId
from devtools.paths import ResolvedPath
from devtools.persistence import SqliteSessionStore
from devtools.runtime import Runtime

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.time import Timestamp


pytestmark = pytest.mark.live_codex


def _enabled() -> bool:
    """Return whether the caller explicitly enabled live Codex execution."""
    return os.environ.get("DEVTOOLS_LIVE_CODEX") == "1"


@pytest.mark.skipif(not _enabled(), reason="set DEVTOOLS_LIVE_CODEX=1 to run")
def test_sqlite_restores_session_for_runtime_codex_continuation(tmp_path: Path) -> None:
    """SQLite reconstruction preserves a real Codex continuation for Runtime."""
    if shutil.which("git") is None:
        pytest.skip("git is required to initialize the isolated test repository")

    async def exercise() -> tuple[
        Session,
        SessionId,
        Timestamp,
        str,
        str,
        bool,
        tuple[Message, Message, Message, Message],
    ]:
        executor = CommandExecutor()
        initialized = await executor.execute(
            Command("git").args("init").cwd(ResolvedPath(tmp_path)),
        )
        assert initialized.succeeded
        runtime = Runtime()
        codex = CodexAgent(executor, ResolvedPath(tmp_path))
        store = SqliteSessionStore(database=ResolvedPath(tmp_path / "session.sqlite"))
        original = Session.new()
        original_id = original.id
        original_created_at = original.created_at
        marker = f"DEVTOOLS-PERSISTENCE-CONTINUITY-{uuid.uuid4()}"
        first_user = Message.new(
            f'Remember the exact marker "{marker}" for my next message. '
            'Reply only with "stored".',
            role=MessageRole.USER,
            source=MessageSource("live-test"),
        )
        first_turn = await runtime.send(
            session=original,
            agent=codex,
            message=first_user,
        )
        assert first_turn.message.content.strip() == "stored"
        assert first_turn.conversation is not None
        store.save(original)
        loaded = store.load(original_id)
        assert loaded is not None
        assert loaded is not original
        assert loaded.id == original_id
        assert loaded.created_at == original_created_at
        assert loaded.history.messages == (first_user, first_turn.message)
        assert loaded.conversation_for(codex.source) == first_turn.conversation

        second_user = Message.new(
            "What exact marker did I ask you to remember in my previous "
            "message? First use a shell command to attempt to create the "
            f"disposable file {tmp_path / 'write-probe.txt'}. You are in a "
            "read-only sandbox, so that command must be denied. Reply with "
            "only the marker.",
            role=MessageRole.USER,
            source=MessageSource("live-test"),
        )
        second_turn = await runtime.send(
            session=loaded,
            agent=codex,
            message=second_user,
        )
        assert second_turn.conversation is not None
        return (
            loaded,
            original_id,
            original_created_at,
            marker,
            second_turn.message.content.strip(),
            first_turn.conversation == second_turn.conversation,
            (first_user, first_turn.message, second_user, second_turn.message),
        )

    (
        loaded,
        original_id,
        original_created_at,
        marker,
        response,
        same_thread,
        expected_messages,
    ) = asyncio.run(exercise())
    assert response == marker
    assert loaded.history.messages == expected_messages
    assert loaded.id == original_id
    assert loaded.created_at == original_created_at
    assert same_thread
    assert loaded.conversation_for(MessageSource("codex")) is not None
    assert not (tmp_path / "write-probe.txt").exists()
