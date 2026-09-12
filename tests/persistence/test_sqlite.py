# Copyright (c) 2026
"""Normalized SQLite Session persistence tests."""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from devtools.context import (
    History,
    Message,
    MessageId,
    MessageRole,
    MessageSource,
    Session,
    SessionId,
)
from devtools.interactions import ConversationRef, Interaction, InteractionTurn
from devtools.paths import ResolvedPath
from devtools.persistence import (
    PersistenceConflictError,
    PersistenceFormatError,
    PersistenceVersionError,
    SqliteSessionStore,
)
from devtools.runtime import Runtime
from devtools.time import Timestamp

if TYPE_CHECKING:
    from pathlib import Path


class FakeInteraction:
    """A structural Interaction fake that records its received continuation."""

    def __init__(self, source: MessageSource, turn: InteractionTurn) -> None:
        """Configure one deterministic Interaction turn."""
        self._source = source
        self._turn = turn
        self.calls: list[tuple[Message, ConversationRef | None]] = []

    @property
    def source(self) -> MessageSource:
        """Return the Interaction source."""
        return self._source

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> InteractionTurn:
        """Record and return the configured turn."""
        self.calls.append((message, conversation))
        return self._turn


def _timestamp(offset: int = 0) -> Timestamp:
    """Return a deterministic UTC timestamp."""
    value = datetime(2026, 1, 2, 3, 4, 5, tzinfo=UTC)
    return Timestamp(value + timedelta(seconds=offset))


def _message(
    number: int,
    *,
    content: str = "content",
    role: MessageRole = MessageRole.USER,
    source: str = "user",
) -> Message:
    """Build one deterministic immutable Message."""
    return Message(
        id=MessageId.parse(f"00000000-0000-4000-8000-{number:012d}"),
        created_at=_timestamp(number),
        content=content,
        role=role,
        source=MessageSource(source),
    )


def _store(tmp_path: Path) -> SqliteSessionStore:
    """Create a store backed by one temporary absolute database path."""
    return SqliteSessionStore(database=ResolvedPath(tmp_path / "sessions.sqlite"))


def _session(*, messages: tuple[Message, ...] = ()) -> Session:
    """Build a deterministic Session fixture."""
    return Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000010"),
        created_at=_timestamp(),
        history=History(messages=messages),
        conversations=(
            ConversationRef(MessageSource("codex"), "thread-codex"),
            ConversationRef(MessageSource("qwen"), "thread-qwen"),
        ),
    )


def test_sqlite_initializes_normalized_schema_and_round_trips_empty_session(
    tmp_path: Path,
) -> None:
    """A new database initializes lazily and restores an empty Session."""
    store = _store(tmp_path)
    session = Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000010"),
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
    second = _message(2, role=MessageRole.ASSISTANT, source="agent")
    third = _message(3, content="", role=MessageRole.SYSTEM, source="system")
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
    second = _message(2, role=MessageRole.ASSISTANT, source="agent")
    session = _session(messages=(first, second))
    store = _store(tmp_path)
    store.save(session)
    session.add(_message(3, role=MessageRole.SYSTEM, source="system"))
    replacement = ConversationRef(MessageSource("codex"), "thread-new")
    session.set_conversation(replacement)
    store.save(session)

    loaded = store.load(session.id)

    assert loaded is not None
    assert loaded.history == session.history
    assert loaded.conversation_for(MessageSource("codex")) is not None
    assert loaded.conversation_for(MessageSource("codex")) == replacement

    shorter = Session(
        id=session.id,
        created_at=session.created_at,
        history=History(messages=(first,)),
        conversations=(replacement,),
    )
    store.save(shorter)
    shrunken = store.load(session.id)
    assert shrunken is not None
    assert shrunken.history.messages == (first,)
    assert dict(shrunken.conversations) == {MessageSource("codex"): replacement}


def test_sqlite_reuses_global_message_row_across_sessions(tmp_path: Path) -> None:
    """One MessageId can be associated with multiple current Session snapshots."""
    shared = _message(1)
    first = _session(messages=(shared, shared))
    second = Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000011"),
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
    conflicting_message = Message(
        id=original_message.id,
        created_at=original_message.created_at,
        content="changed",
        role=original_message.role,
        source=original_message.source,
    )
    conflicting = Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000012"),
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

    changed_created_at = Session(
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
    store = SqliteSessionStore(database=ResolvedPath(database))
    with pytest.raises(PersistenceVersionError):
        store.load(SessionId.parse("10000000-0000-4000-8000-000000000010"))

    unrelated = tmp_path / "unrelated.sqlite"
    connection = sqlite3.connect(unrelated)
    try:
        connection.execute("CREATE TABLE unrelated(value TEXT)")
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(PersistenceFormatError):
        SqliteSessionStore(database=ResolvedPath(unrelated)).load(
            SessionId.parse("10000000-0000-4000-8000-000000000010"),
        )


def test_sqlite_rejects_missing_required_tables_and_invalid_positions(
    tmp_path: Path,
) -> None:
    """Known schema corruption cannot silently reconstruct a Session."""
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
        connection.execute("CREATE TABLE sessions(session_id TEXT)")
        connection.execute("PRAGMA user_version = 1")
        connection.commit()
    finally:
        connection.close()
    with pytest.raises(PersistenceFormatError):
        SqliteSessionStore(database=ResolvedPath(malformed)).load(session.id)


def test_sqlite_rejects_version_one_schema_missing_required_column(
    tmp_path: Path,
) -> None:
    """Version-1 tables must expose the essential persistence columns."""
    database = tmp_path / "missing-column.sqlite"
    connection = sqlite3.connect(database)
    try:
        connection.executescript(
            """
            CREATE TABLE sessions(session_id TEXT, created_at TEXT);
            CREATE TABLE messages(
                message_id TEXT,
                created_at TEXT,
                role TEXT,
                source TEXT
            );
            CREATE TABLE session_messages(
                session_id TEXT,
                position INTEGER,
                message_id TEXT
            );
            CREATE TABLE conversations(session_id TEXT, source TEXT, value TEXT);
            PRAGMA user_version = 1;
            """,
        )
        connection.commit()
    finally:
        connection.close()

    with pytest.raises(PersistenceFormatError):
        SqliteSessionStore(database=ResolvedPath(database)).load(
            SessionId.parse("10000000-0000-4000-8000-000000000010"),
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
    final = _message(2, role=MessageRole.ASSISTANT, source="agent")
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
    """A restored Session supplies its persisted continuation to Runtime."""
    existing = ConversationRef(MessageSource("agent"), "thread-a")
    session = Session(
        id=SessionId.parse("10000000-0000-4000-8000-000000000020"),
        created_at=_timestamp(),
        conversations=(existing,),
    )
    store = _store(tmp_path)
    store.save(session)
    loaded = store.load(session.id)
    assert loaded is not None
    response = _message(2, role=MessageRole.ASSISTANT, source="agent")
    replacement = ConversationRef(MessageSource("agent"), "thread-b")
    fake: Interaction = FakeInteraction(
        MessageSource("agent"), InteractionTurn(response, replacement),
    )

    async def exercise() -> None:
        turn = await Runtime().send(
            session=loaded,
            interaction=fake,
            message=_message(1),
        )
        assert turn.message is response

    asyncio.run(exercise())
    assert isinstance(fake, FakeInteraction)
    assert fake.calls[0][1] == existing
    assert loaded.conversation_for(MessageSource("agent")) == replacement
