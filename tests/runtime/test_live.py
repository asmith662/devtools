# Copyright (c) 2026
"""Opt-in real Runtime, Session, and Codex continuation acceptance."""

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
from devtools.evidence import Attempt, AttemptState
from devtools.paths import ResolvedPath
from devtools.runtime import Runtime

if TYPE_CHECKING:
    from pathlib import Path

    from devtools.time import Timestamp


pytestmark = pytest.mark.live_codex


class LiveObserver:
    """Retain exact live Attempts for opt-in observation acceptance."""

    def __init__(self) -> None:
        """Initialize callback storage."""
        self.started: list[Attempt] = []
        self.finished: list[Attempt] = []

    def attempt_started(self, attempt: Attempt) -> None:
        """Retain the newly started Attempt object."""
        self.started.append(attempt)

    def attempt_finished(self, attempt: Attempt) -> None:
        """Retain the terminal Attempt object."""
        self.finished.append(attempt)


def _enabled() -> bool:
    """Return whether the caller explicitly enabled live Codex execution."""
    return os.environ.get("DEVTOOLS_LIVE_CODEX") == "1"


@pytest.mark.skipif(not _enabled(), reason="set DEVTOOLS_LIVE_CODEX=1 to run")
def test_runtime_coordinates_a_read_only_codex_continuation(tmp_path: Path) -> None:
    """Runtime retains and resumes a real Codex continuation through Session."""
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
        session = Session.new()
        original_id = session.id
        original_created_at = session.created_at
        marker = f"DEVTOOLS-RUNTIME-CONTINUITY-{uuid.uuid4()}"
        first_user = Message.new(
            f'Remember the exact marker "{marker}" for my next message. '
            'Reply only with "stored".',
            role=MessageRole.USER,
            source=MessageSource("live-test"),
        )
        first_turn = await runtime.send(
            session=session,
            agent=codex,
            message=first_user,
        )
        assert first_turn.message.content.strip() == "stored"
        assert first_turn.conversation is not None
        stored_ref = session.conversation_for(codex.source)
        assert stored_ref == first_turn.conversation
        assert session.history.messages == (first_user, first_turn.message)

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
            session=session,
            agent=codex,
            message=second_user,
        )
        assert second_turn.conversation is not None
        assert session.conversation_for(codex.source) == second_turn.conversation
        return (
            session,
            original_id,
            original_created_at,
            marker,
            second_turn.message.content.strip(),
            first_turn.conversation == second_turn.conversation,
            (first_user, first_turn.message, second_user, second_turn.message),
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
    assert session.conversation_for(MessageSource("codex")) is not None
    assert not (tmp_path / "write-probe.txt").exists()


@pytest.mark.skipif(not _enabled(), reason="set DEVTOOLS_LIVE_CODEX=1 to run")
def test_runtime_observes_a_read_only_codex_attempt(tmp_path: Path) -> None:
    """Runtime observes one real successful Codex processing Attempt."""
    if shutil.which("git") is None:
        pytest.skip("git is required to initialize the isolated test repository")

    async def exercise() -> tuple[Session, Message, Attempt, Attempt, Message]:
        executor = CommandExecutor()
        initialized = await executor.execute(
            Command("git").args("init").cwd(ResolvedPath(tmp_path)),
        )
        assert initialized.succeeded
        observer = LiveObserver()
        runtime = Runtime(observer=observer)
        codex = CodexAgent(executor, ResolvedPath(tmp_path))
        session = Session.new()
        message = Message.new(
            "Use a shell command to attempt to create the disposable file "
            f"{tmp_path / 'observed-write-probe.txt'}. You are in a read-only "
            "sandbox, so the write must be denied. Then reply briefly that "
            "the write was denied.",
            role=MessageRole.USER,
            source=MessageSource("live-test"),
        )

        turn = await runtime.send(session=session, agent=codex, message=message)

        assert len(observer.started) == len(observer.finished) == 1
        return session, message, observer.started[0], observer.finished[0], turn.message

    session, message, started, finished, response = asyncio.run(exercise())
    assert started is finished
    assert started.session_id == session.id
    assert started.message_id == message.id
    assert started.agent_source == MessageSource("codex")
    assert started.state is AttemptState.SUCCEEDED
    assert started.completed_at is not None
    assert session.history.messages == (message, response)
    assert not (tmp_path / "observed-write-probe.txt").exists()
