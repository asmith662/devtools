# Copyright (c) 2026
"""Normalized SQLite Conversation persistence tests."""

from __future__ import annotations

import asyncio
import hashlib
import sqlite3
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
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
    ModelRequest,
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
    from typing import Any


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
        request: ModelRequest,
    ) -> ModelResponse:
        """Record and return the configured turn."""
        self.calls.append((request.prompt, request.conversation))
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


def _snapshot_pair() -> tuple[Conversation, Conversation]:
    """Two independently specified complete committed states of one entity."""
    original = _session(messages=(_message(1, content="A"),))
    first, second = (
        Conversation(
            id=original.id,
            created_at=original.created_at,
            history=History(messages=(_message(number, content=label),)),
            conversations=(ConversationRef(InteractionSource("agent"), thread),),
        )
        for number, label, thread in [(1, "A", "thread-a"), (2, "B", "thread-b")]
    )
    return first, second


def _pair_value(conversation: Conversation | None) -> tuple[list[str], str]:
    """Observe public state without deriving expected values from the store."""
    assert conversation is not None
    reference = conversation.conversation_for(InteractionSource("agent"))
    assert reference is not None
    return [m.content for m in conversation.history], reference.value


def test_sqlite_wal_load_never_mixes_committed_snapshots(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A real writer commits while an earlier reader retains one whole snapshot."""
    store = _store(tmp_path)
    first, second = _snapshot_pair()
    store.save(first)
    original_connect = sqlite3.connect
    with closing(original_connect(tmp_path / "sessions.sqlite")) as connection:
        assert connection.execute("PRAGMA journal_mode=WAL").fetchone() == ("wal",)
    paused = threading.Event()
    release = threading.Event()
    scheduling_errors: list[str] = []
    closed: list[str] = []

    class Connection(sqlite3.Connection):
        def execute(self, sql: str, parameters: Any = (), /) -> sqlite3.Cursor:  # noqa: ANN401 -- native SQLite parameter protocol
            if (
                "FROM conversations WHERE" in sql
                and threading.current_thread().name.startswith("snapshot-reader")
            ):
                paused.set()
                if not release.wait(10):
                    scheduling_errors.append("reader release missing")
            return super().execute(sql, parameters)

        def close(self) -> None:
            closed.append(threading.current_thread().name)
            super().close()

    def connect(database: str) -> sqlite3.Connection:
        return original_connect(database, factory=Connection)

    monkeypatch.setattr(sqlite3, "connect", connect)
    with ThreadPoolExecutor(
        max_workers=1,
        thread_name_prefix="snapshot-reader",
    ) as pool:
        reader = pool.submit(store.load, first.id)
        try:
            assert paused.wait(10), "reader did not reach the scheduled query"
            store.save(second)
            # The save has returned; independent queries prove the intervening
            # commit is visible before the reader may request its continuation.
            with closing(original_connect(tmp_path / "sessions.sqlite")) as witness:
                assert witness.execute(
                    "SELECT content FROM messages "
                    "JOIN session_messages USING(message_id)",
                ).fetchall() == [("B",)]
                assert witness.execute(
                    "SELECT value FROM conversations",
                ).fetchall() == [("thread-b",)]
        finally:
            release.set()
        loaded = reader.result(10)
    assert scheduling_errors == []
    assert _pair_value(loaded) == (["A"], "thread-a")
    assert _pair_value(store.load(first.id)) == (["B"], "thread-b")
    assert any(name.startswith("snapshot-reader") for name in closed)


@pytest.mark.parametrize("stage", ["table", "index", "late-index", "version"])
def test_sqlite_initialization_failure_rolls_back_and_retries(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    stage: str,
) -> None:
    """Every initial DDL/version stage belongs to the same transaction."""
    store = _store(tmp_path)
    first, _ = _snapshot_pair()
    original_connect = sqlite3.connect
    closed: list[bool] = []

    class Connection(sqlite3.Connection):
        def close(self) -> None:
            closed.append(self.in_transaction)
            super().close()

    def authorize(
        action: int,
        one: str | None,
        two: str | None,
        _db: str | None,
        _trigger: str | None,
    ) -> int:
        denied = (
            (
                stage == "table"
                and action == sqlite3.SQLITE_CREATE_TABLE
                and one == "messages"
            )
            or (
                stage == "index"
                and action == sqlite3.SQLITE_CREATE_INDEX
                and one == "idx_sessions_created_at"
            )
            or (
                stage == "late-index"
                and action == sqlite3.SQLITE_CREATE_INDEX
                and one == "idx_conversations_source"
            )
            or (
                stage == "version"
                and action == sqlite3.SQLITE_PRAGMA
                and one == "user_version"
                and two is not None
            )
        )
        return sqlite3.SQLITE_DENY if denied else sqlite3.SQLITE_OK

    def connect(database: str) -> sqlite3.Connection:
        connection = original_connect(database, factory=Connection)
        connection.set_authorizer(authorize)
        return connection

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        with pytest.raises(sqlite3.DatabaseError, match="not authorized"):
            store.save(first)
    assert closed == [False]

    with closing(original_connect(tmp_path / "sessions.sqlite")) as connection:
        tables = connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'",
        ).fetchall()
        version = connection.execute("PRAGMA user_version").fetchone()
    retry_error = None
    try:
        store.save(first)
    except PersistenceFormatError as error:
        retry_error = type(error).__name__
    assert {"tables": tables, "version": version, "retry_error": retry_error} == {
        "tables": [],
        "version": (0,),
        "retry_error": None,
    }
    assert _pair_value(store.load(first.id)) == (["A"], "thread-a")


def test_sqlite_default_journal_reader_and_waiting_writer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback journal may delay commit; one reader still retains a whole state."""
    store = _store(tmp_path)
    first, second = _snapshot_pair()
    store.save(first)
    original_connect = sqlite3.connect
    with closing(original_connect(tmp_path / "sessions.sqlite")) as c:
        assert c.execute("PRAGMA journal_mode").fetchone() == ("delete",)
        assert c.execute("PRAGMA busy_timeout").fetchone() == (5000,)
    paused, release, commit_entered = (
        threading.Event(),
        threading.Event(),
        threading.Event(),
    )
    schedule_errors: list[str] = []

    class Connection(sqlite3.Connection):
        def execute(self, sql: str, parameters: Any = (), /) -> sqlite3.Cursor:  # noqa: ANN401 -- native parameter protocol
            if (
                "FROM conversations WHERE" in sql
                and threading.current_thread().name.startswith("rollback-reader")
            ):
                paused.set()
                if not release.wait(10):
                    schedule_errors.append("reader not released")
            return super().execute(sql, parameters)

    def connect(database: str) -> sqlite3.Connection:
        c = original_connect(database, factory=Connection)
        if threading.current_thread().name.startswith("rollback-writer"):
            c.set_trace_callback(
                lambda sql: commit_entered.set() if sql == "COMMIT" else None,
            )
        return c

    monkeypatch.setattr(sqlite3, "connect", connect)
    with (
        ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="rollback-reader",
        ) as readers,
        ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="rollback-writer",
        ) as writers,
    ):
        reader = readers.submit(store.load, first.id)
        assert paused.wait(10)
        writer = writers.submit(store.save, second)
        try:
            assert commit_entered.wait(10), "writer did not attempt actual commit"
        finally:
            release.set()
        loaded = reader.result(10)
        assert writer.result(10) is None
    assert schedule_errors == []
    assert _pair_value(loaded) == (["A"], "thread-a")
    assert _pair_value(store.load(first.id)) == (["B"], "thread-b")


def test_sqlite_default_read_lock_refuses_impatient_commit_then_releases(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test-only zero wait establishes locking, rollback and subsequent release."""
    store = _store(tmp_path)
    first, second = _snapshot_pair()
    store.save(first)
    original_connect = sqlite3.connect
    paused, release = threading.Event(), threading.Event()
    closed: list[bool] = []
    schedule_errors: list[str] = []

    class Connection(sqlite3.Connection):
        def execute(self, sql: str, parameters: Any = (), /) -> sqlite3.Cursor:  # noqa: ANN401 -- native parameter protocol
            if (
                "FROM conversations WHERE" in sql
                and threading.current_thread().name.startswith("held-reader")
            ):
                paused.set()
                if not release.wait(10):
                    schedule_errors.append("reader not released")
            return super().execute(sql, parameters)

        def close(self) -> None:
            closed.append(self.in_transaction)
            super().close()

    def connect(database: str) -> sqlite3.Connection:
        return original_connect(database, timeout=0, factory=Connection)

    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        with ThreadPoolExecutor(
            max_workers=1,
            thread_name_prefix="held-reader",
        ) as readers:
            reader = readers.submit(store.load, first.id)
            try:
                assert paused.wait(10)
                with pytest.raises(sqlite3.OperationalError, match="locked"):
                    store.save(second)
            finally:
                release.set()
            assert _pair_value(reader.result(10)) == (["A"], "thread-a")
    assert schedule_errors == []
    assert closed == [False, False]
    assert _pair_value(store.load(first.id)) == (["A"], "thread-a")
    store.save(second)
    assert _pair_value(store.load(first.id)) == (["B"], "thread-b")


def test_sqlite_concurrent_first_initializers_recheck_after_reservation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Both observe v0; the waiting initializer rechecks installed v1."""
    original_connect = sqlite3.connect
    barrier = threading.Barrier(2)
    seen: list[int] = []

    class Cursor(sqlite3.Cursor):
        first_version: bool = False

        def fetchone(self) -> Any:  # noqa: ANN401 -- native row protocol
            row = super().fetchone()
            if self.first_version:
                self.close()
                seen.append(row[0])
                barrier.wait(10)
            return row

    class Connection(sqlite3.Connection):
        first_version: bool = True

        def execute(self, sql: str, parameters: Any = (), /) -> sqlite3.Cursor:  # noqa: ANN401 -- native parameter protocol
            cursor = self.cursor(factory=Cursor)
            cursor.execute(sql, parameters)
            if sql == "PRAGMA user_version" and self.first_version:
                self.first_version = False
                cursor.first_version = True
            return cursor

    def connect(database: str) -> sqlite3.Connection:
        return original_connect(database, factory=Connection)

    store = _store(tmp_path)
    first, _ = _snapshot_pair()
    with monkeypatch.context() as patch:
        patch.setattr(sqlite3, "connect", connect)
        with ThreadPoolExecutor(max_workers=2) as workers:
            futures = [workers.submit(store.load, first.id) for _ in range(2)]
            assert [f.result(10) for f in futures] == [None, None]
    assert seen == [0, 0]
    store.save(first)
    assert _pair_value(store.load(first.id)) == (["A"], "thread-a")
    with closing(original_connect(tmp_path / "sessions.sqlite")) as c:
        assert c.execute("PRAGMA user_version").fetchone() == (1,)
        assert c.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'",
        ).fetchone() == (4,)


def test_sqlite_preexisting_partial_database_is_preserved(tmp_path: Path) -> None:
    """Unknown v0 content is never reclaimed as a fresh installation."""
    path = tmp_path / "sessions.sqlite"
    with closing(sqlite3.connect(path)) as c, c:
        c.execute("CREATE TABLE sessions(value TEXT)")
        c.execute("INSERT INTO sessions VALUES ('unknown original content')")
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    first, _ = _snapshot_pair()
    with pytest.raises(PersistenceFormatError, match="not an empty"):
        _store(tmp_path).load(first.id)
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
    with closing(sqlite3.connect(path)) as c:
        assert c.execute("SELECT value FROM sessions").fetchall() == [
            ("unknown original content",),
        ]
        assert c.execute("PRAGMA user_version").fetchone() == (0,)


@pytest.mark.parametrize(
    "failure",
    ["missing", "malformed", "begin", "query", "commit"],
)
def test_sqlite_read_transaction_always_settles_and_closes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: str,
) -> None:
    """Early return, decode refusal and native transaction errors close custody."""
    store = _store(tmp_path)
    first, _ = _snapshot_pair()
    store.save(first)
    original_connect = sqlite3.connect
    if failure == "malformed":
        with closing(original_connect(tmp_path / "sessions.sqlite")) as c, c:
            c.execute("UPDATE conversations SET value=?", (b"PRIVATE_SENTINEL",))
    closed: list[bool] = []

    class Connection(sqlite3.Connection):
        def close(self) -> None:
            closed.append(self.in_transaction)
            super().close()

    def authorize(
        action: int,
        one: str | None,
        _two: str | None,
        _db: str | None,
        _trigger: str | None,
    ) -> int:
        denied = (
            (
                failure == "begin"
                and action == sqlite3.SQLITE_TRANSACTION
                and one == "BEGIN"
            )
            or (
                failure == "commit"
                and action == sqlite3.SQLITE_TRANSACTION
                and one == "COMMIT"
            )
            or (
                failure == "query"
                and action == sqlite3.SQLITE_READ
                and one == "messages"
            )
        )
        return sqlite3.SQLITE_DENY if denied else sqlite3.SQLITE_OK

    def connect(database: str) -> sqlite3.Connection:
        c = original_connect(database, factory=Connection)
        c.set_authorizer(authorize)
        return c

    monkeypatch.setattr(sqlite3, "connect", connect)
    if failure == "missing":
        missing = ConversationId.parse("10000000-0000-4000-8000-000000000999")
        assert store.load(missing) is None
    elif failure == "malformed":
        with pytest.raises(PersistenceFormatError):
            store.load(first.id)
    else:
        with pytest.raises(sqlite3.DatabaseError):
            store.load(first.id)
    assert closed == [False]
