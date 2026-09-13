# Copyright (c) 2026
"""Normalized SQLite Conversation persistence tests."""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from devtools.agents.conversation import (
    Conversation,
    ConversationId,
    ConversationMessage,
    ConversationMessageRole,
    History,
    InteractionSource,
    MessageId,
)
from devtools.core.paths import ResolvedPath
from devtools.core.time import Timestamp
from devtools.execution import Runtime
from devtools.models.interaction import (
    ConversationRef,
    ModelInteraction,
    ModelResponse,
    Prompt,
)
from devtools.persistence import (
    PersistenceConflictError,
    PersistenceFormatError,
    PersistenceVersionError,
    SqliteConversationStore,
)

if TYPE_CHECKING:
    from pathlib import Path


class FakeInteraction:
    """A structural ModelInteraction fake that records its received continuation."""

    def __init__(self, source: InteractionSource, turn: ModelResponse) -> None:
        """Configure one deterministic ModelInteraction turn."""
        self._source = source
        self._turn = turn
        self.calls: list[tuple[Prompt, ConversationRef | None]] = []

    @property
    def source(self) -> InteractionSource:
        """Return the ModelInteraction source."""
        return self._source

    async def send(
        self,
        prompt: Prompt,
        *,
        conversation: ConversationRef | None = None,
    ) -> ModelResponse:
        """Record and return the configured turn."""
        self.calls.append((prompt, conversation))
        return self._turn


def _timestamp(offset: int = 0) -> Timestamp:
    """Return a deterministic UTC timestamp."""
    value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    return Timestamp(value + timedelta(seconds=offset))


def _message(
    number: int,
    *,
    content: str = "content",
    role: ConversationMessageRole = ConversationMessageRole.USER,
    source: str = "user",
) -> ConversationMessage:
    """Build one deterministic immutable ConversationMessage."""
    return ConversationMessage(
        id=MessageId.parse(f"00000000-0000-4000-8000-{number:012d}"),
        created_at=_timestamp(number),
        content=content,
        role=role,
        source=InteractionSource(source),
    )


def _store(tmp_path: Path) -> SqliteConversationStore:
    """Create a store backed by one temporary absolute database path."""
    return SqliteConversationStore(database=ResolvedPath(tmp_path / "sessions.sqlite"))


def _session(*, messages: tuple[ConversationMessage, ...] = ()) -> Conversation:
    """Build a deterministic Conversation fixture."""
    return Conversation(
        id=ConversationId.parse("10000000-0000-4000-8000-000000000010"),
        created_at=_timestamp(),
        history=History(messages=messages),
        conversations=(
            ConversationRef(InteractionSource("codex"), "thread-codex"),
            ConversationRef(InteractionSource("qwen"), "thread-qwen"),
        ),
    )


def test_sqlite_initializes_normalized_schema_and_round_trips_empty_session(
    tmp_path: Path,
) -> None:
    """A new database initializes lazily and restores an empty Conversation."""
    store = _store(tmp_path)
    session = Conversation(
        id=ConversationId.parse("10000000-0000-4000-8000-000000000010"),
        created_at=_timestamp(),
    )

    assert store.load(session.id) is None
    store.save(session)
    loaded = store.load(session.id)

    assert loaded is not None
    assert loaded is not session
    assert loaded.id == session.id
    assert loaded.created_at == session.created_at
    assert loaded.history == History()
    assert loaded.conversations == session.conversations
    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        assert connection.execute("PRAGMA user_version").fetchone() == (1,)
        foreign_keys = connection.execute(
            "PRAGMA foreign_key_list(session_messages)",
        ).fetchall()
        assert foreign_keys
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'",
            )
        }
        assert {"sessions", "messages", "session_messages", "conversations"} <= tables
    finally:
        connection.close()


def test_sqlite_round_trips_duplicates_order_and_fresh_turn(tmp_path: Path) -> None:
    """Normalized rows preserve duplicate occurrences and ordered History."""
    first = _message(1, content="雪\n  ", source="caller")
    second = _message(2, role=ConversationMessageRole.ASSISTANT, source="agent")
    third = _message(
        3,
        content="",
        role=ConversationMessageRole.SYSTEM,
        source="system",
    )
    session = _session(messages=(first, second, first, third))
    store = _store(tmp_path)

    store.save(session)
    loaded = store.load(session.id)

    assert loaded is not None
    assert loaded.history == session.history
    assert loaded.history.messages[0] is loaded.history.messages[2]
    assert loaded.conversations == session.conversations

    async def acquire() -> None:
        async with loaded.turn():
            pass

    asyncio.run(acquire())
    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        assert connection.execute("SELECT COUNT(*) FROM messages").fetchone() == (3,)
        occurrence_count = connection.execute(
            "SELECT COUNT(*) FROM session_messages",
        ).fetchone()
        assert occurrence_count == (4,)
    finally:
        connection.close()


def test_sqlite_replaces_snapshot_history_and_conversations(tmp_path: Path) -> None:
    """Repeated save replaces stale occurrence rows and current refs exactly."""
    first = _message(1)
    second = _message(2, role=ConversationMessageRole.ASSISTANT, source="agent")
    session = _session(messages=(first, second))
    store = _store(tmp_path)
    store.save(session)
    session.add(_message(3, role=ConversationMessageRole.SYSTEM, source="system"))
    replacement = ConversationRef(InteractionSource("codex"), "thread-new")
    session.set_conversation(replacement)
    store.save(session)

    loaded = store.load(session.id)

    assert loaded is not None
    assert loaded.history == session.history
    assert loaded.conversation_for(InteractionSource("codex")) is not None
    assert loaded.conversation_for(InteractionSource("codex")) == replacement

    shorter = Conversation(
        id=session.id,
        created_at=session.created_at,
        history=History(messages=(first,)),
        conversations=(replacement,),
    )
    store.save(shorter)
    shrunken = store.load(session.id)
    assert shrunken is not None
    assert shrunken.history.messages == (first,)
    assert dict(shrunken.conversations) == {InteractionSource("codex"): replacement}


def test_sqlite_reuses_global_message_row_across_sessions(tmp_path: Path) -> None:
    """One MessageId can be associated with multiple current Conversation snapshots."""
    shared = _message(1)
    first = _session(messages=(shared, shared))
    second = Conversation(
        id=ConversationId.parse("10000000-0000-4000-8000-000000000011"),
        created_at=_timestamp(1),
        history=History(messages=(shared,)),
    )
    store = _store(tmp_path)

    store.save(first)
    store.save(second)

    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        assert connection.execute("SELECT COUNT(*) FROM messages").fetchone() == (1,)
        occurrence_count = connection.execute(
            "SELECT COUNT(*) FROM session_messages",
        ).fetchone()
        assert occurrence_count == (3,)
    finally:
        connection.close()
    assert store.load(first.id) is not None
    assert store.load(second.id) is not None


def test_sqlite_rejects_message_and_session_identity_conflicts_atomically(
    tmp_path: Path,
) -> None:
    """Conflicts roll back a candidate snapshot without damaging prior state."""
    original_message = _message(1, content="original")
    original = _session(messages=(original_message,))
    store = _store(tmp_path)
    store.save(original)
    conflicting_message = ConversationMessage(
        id=original_message.id,
        created_at=original_message.created_at,
        content="changed",
        role=original_message.role,
        source=original_message.source,
    )
    conflicting = Conversation(
        id=ConversationId.parse("10000000-0000-4000-8000-000000000012"),
        created_at=_timestamp(2),
        history=History(messages=(_message(2), conflicting_message)),
    )

    with pytest.raises(PersistenceConflictError):
        store.save(conflicting)
    restored = store.load(original.id)
    assert restored is not None
    assert restored.history.messages == (original_message,)
    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        assert connection.execute(
            "SELECT COUNT(*) FROM sessions WHERE session_id = ?",
            (str(conflicting.id),),
        ).fetchone() == (0,)
        assert connection.execute(
            "SELECT COUNT(*) FROM messages WHERE message_id = ?",
            (str(_message(2).id),),
        ).fetchone() == (0,)
        assert connection.execute(
            "SELECT COUNT(*) FROM session_messages WHERE session_id = ?",
            (str(conflicting.id),),
        ).fetchone() == (0,)
    finally:
        connection.close()

    changed_created_at = Conversation(
        id=original.id,
        created_at=_timestamp(10),
        history=original.history,
    )
    with pytest.raises(PersistenceConflictError):
        store.save(changed_created_at)
    assert store.load(original.id) is not None


def test_sqlite_rejects_unsupported_and_unrelated_databases(tmp_path: Path) -> None:
    """Version and unrelated-schema protection remain explicit."""
    database = tmp_path / "sessions.sqlite"
    connection = sqlite3.connect(database)
    try:
        connection.execute("PRAGMA user_version = 2")
        connection.commit()
    finally:
        connection.close()
    store = SqliteConversationStore(database=ResolvedPath(database))
    with pytest.raises(PersistenceVersionError):
        store.load(ConversationId.parse("10000000-0000-4000-8000-000000000010"))

    unrelated = tmp_path / "unrelated.sqlite"
    connection = sqlite3.connect(unrelated)
    try:
        connection.execute("CREATE TABLE unrelated(value TEXT)")
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(PersistenceFormatError):
        SqliteConversationStore(database=ResolvedPath(unrelated)).load(
            ConversationId.parse("10000000-0000-4000-8000-000000000010"),
        )


def test_sqlite_rejects_missing_required_tables_and_invalid_positions(
    tmp_path: Path,
) -> None:
    """Known schema corruption cannot silently reconstruct a Conversation."""
    store = _store(tmp_path)
    session = _session(messages=(_message(1),))
    store.save(session)
    database = tmp_path / "sessions.sqlite"
    connection = sqlite3.connect(database)
    try:
        connection.execute(
            "UPDATE session_messages SET position = 2 WHERE session_id = ?",
            (str(session.id),),
        )
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(PersistenceFormatError):
        store.load(session.id)

    malformed = tmp_path / "malformed.sqlite"
    connection = sqlite3.connect(malformed)
    try:
        connection.execute("CREATE TABLE sessions(conversation_id TEXT)")
        connection.execute("PRAGMA user_version = 1")
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(PersistenceFormatError):
        SqliteConversationStore(database=ResolvedPath(malformed)).load(session.id)


def test_sqlite_rejects_version_one_schema_missing_required_column(
    tmp_path: Path,
) -> None:
    """Version-1 tables must expose the essential persistence columns."""
    database = tmp_path / "missing-column.sqlite"
    connection = sqlite3.connect(database)
    try:
        connection.executescript(
            """
            CREATE TABLE sessions(conversation_id TEXT, created_at TEXT);
            CREATE TABLE messages(
                message_id TEXT,
                created_at TEXT,
                role TEXT,
                source TEXT
            );
            CREATE TABLE session_messages(
                conversation_id TEXT,
                position INTEGER,
                message_id TEXT
            );
            CREATE TABLE conversations(conversation_id TEXT, source TEXT, value TEXT);
            PRAGMA user_version = 1;
            """,
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(PersistenceFormatError):
        SqliteConversationStore(database=ResolvedPath(database)).load(
            ConversationId.parse("10000000-0000-4000-8000-000000000010"),
        )


def test_sqlite_normalizes_corrupt_timestamp_rows(tmp_path: Path) -> None:
    """Invalid persisted semantic values remain persistence format failures."""
    store = _store(tmp_path)
    session = _session()
    store.save(session)
    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        connection.execute(
            "UPDATE sessions SET created_at = 'invalid' WHERE session_id = ?",
            (str(session.id),),
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(PersistenceFormatError):
        store.load(session.id)


def test_sqlite_rejects_missing_final_referenced_message_row(tmp_path: Path) -> None:
    """A damaged final occurrence cannot silently truncate persisted History."""
    first = _message(1)
    final = _message(2, role=ConversationMessageRole.ASSISTANT, source="agent")
    session = _session(messages=(first, final))
    store = _store(tmp_path)
    store.save(session)
    connection = sqlite3.connect(tmp_path / "sessions.sqlite")
    try:
        connection.execute("PRAGMA foreign_keys = OFF")
        connection.execute(
            "DELETE FROM messages WHERE message_id = ?",
            (str(final.id),),
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(PersistenceFormatError):
        store.load(session.id)


def test_sqlite_loaded_session_works_directly_with_runtime(tmp_path: Path) -> None:
    """A restored Conversation supplies its persisted continuation to Runtime."""
    existing = ConversationRef(InteractionSource("agent"), "thread-a")
    session = Conversation(
        id=ConversationId.parse("10000000-0000-4000-8000-000000000020"),
        created_at=_timestamp(),
        conversations=(existing,),
    )
    store = _store(tmp_path)
    store.save(session)
    loaded = store.load(session.id)
    assert loaded is not None
    replacement = ConversationRef(InteractionSource("agent"), "thread-b")
    fake: ModelInteraction = FakeInteraction(
        InteractionSource("agent"),
        ModelResponse(
            content="response",
            source=InteractionSource("agent"),
            conversation=replacement,
        ),
    )

    async def exercise() -> None:
        turn = await Runtime().send(
            conversation=loaded,
            interaction=fake,
            message=_message(1),
        )
        assert turn.content == "response"

    asyncio.run(exercise())
    assert isinstance(fake, FakeInteraction)
    assert fake.calls[0][1] == existing
    assert loaded.conversation_for(InteractionSource("agent")) == replacement
