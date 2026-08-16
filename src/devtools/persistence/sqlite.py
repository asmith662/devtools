# Copyright (c) 2026
"""Normalized SQLite current-snapshot Session store."""
from __future__ import annotations

import sqlite3
from typing import TYPE_CHECKING

from devtools.agents import ConversationRef
from devtools.context.message import MessageId, MessageRole, MessageSource
from devtools.persistence._snapshot import (
    _MessageSnapshot,
    _SessionSnapshot,
    capture_session,
    restore_session,
)
from devtools.persistence.errors import (
    PersistenceConflictError,
    PersistenceFormatError,
    PersistenceVersionError,
)
from devtools.time import TimeError, Timestamp

if TYPE_CHECKING:
    from devtools.context.session import Session, SessionId
    from devtools.paths import ResolvedPath


_SCHEMA_VERSION = 1
_TABLES = {"sessions", "messages", "session_messages", "conversations"}
_REQUIRED_COLUMNS = {
    "sessions": {"session_id", "created_at"},
    "messages": {"message_id", "created_at", "content", "role", "source"},
    "session_messages": {"session_id", "position", "message_id"},
    "conversations": {"session_id", "source", "value"},
}
_SCHEMA = """
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE messages (
    message_id TEXT PRIMARY KEY NOT NULL,
    created_at TEXT NOT NULL,
    content TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    source TEXT NOT NULL
);
CREATE TABLE session_messages (
    session_id TEXT NOT NULL,
    position INTEGER NOT NULL CHECK (position >= 0),
    message_id TEXT NOT NULL,
    PRIMARY KEY (session_id, position),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES messages(message_id)
);
CREATE TABLE conversations (
    session_id TEXT NOT NULL,
    source TEXT NOT NULL,
    value TEXT NOT NULL,
    PRIMARY KEY (session_id, source),
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);
CREATE INDEX idx_sessions_created_at ON sessions(created_at);
CREATE INDEX idx_session_messages_message_id ON session_messages(message_id);
CREATE INDEX idx_conversations_source ON conversations(source);
"""


class SqliteSessionStore:
    """Persist current Session snapshots in a normalized SQLite database."""

    __slots__ = ("_database",)

    def __init__(self, *, database: ResolvedPath) -> None:
        """Configure a store for one absolute SQLite database path."""
        self._database = database

    def save(self, session: Session) -> None:
        """Atomically replace the persisted semantic snapshot for one Session."""
        snapshot = capture_session(session)
        connection = self._open_connection()
        try:
            with connection:
                self._save_snapshot(connection, snapshot)
        finally:
            connection.close()

    def load(self, session_id: SessionId) -> Session | None:
        """Load one persisted Session into a new Session object, if present."""
        connection = self._open_connection()
        try:
            row = connection.execute(
                "SELECT created_at FROM sessions WHERE session_id = ?",
                (str(session_id),),
            ).fetchone()
            if row is None:
                return None
            try:
                snapshot = _SessionSnapshot(
                    id=session_id,
                    created_at=Timestamp.from_isoformat(row[0]),
                    messages=self._load_messages(connection, session_id),
                    conversations=self._load_conversations(connection, session_id),
                )
                return restore_session(snapshot)
            except (TimeError, TypeError, ValueError) as error:
                msg = f"Invalid persisted Session state for SessionId {session_id}."
                raise PersistenceFormatError(msg) from error
        finally:
            connection.close()

    def _open_connection(self) -> sqlite3.Connection:
        """Open, configure, and validate one short-lived SQLite connection."""
        connection = sqlite3.connect(str(self._database))
        try:
            connection.execute("PRAGMA foreign_keys = ON")
            self._ensure_schema(connection)
        except Exception:
            connection.close()
            raise
        else:
            return connection

    def _ensure_schema(self, connection: sqlite3.Connection) -> None:
        """Initialize an empty database or validate the supported schema."""
        version = connection.execute("PRAGMA user_version").fetchone()[0]
        if version == 0:
            tables = _user_tables(connection)
            if tables:
                msg = "SQLite database is not an empty persistence database."
                raise PersistenceFormatError(msg)
            with connection:
                connection.executescript(_SCHEMA)
                connection.execute(f"PRAGMA user_version = {_SCHEMA_VERSION}")
            return
        if version != _SCHEMA_VERSION:
            msg = f"Unsupported SQLite persistence schema version: {version}."
            raise PersistenceVersionError(msg)
        if not _TABLES.issubset(_user_tables(connection)):
            msg = "SQLite persistence schema is missing required tables."
            raise PersistenceFormatError(msg)
        _validate_required_columns(connection)

    def _save_snapshot(
        self,
        connection: sqlite3.Connection,
        snapshot: _SessionSnapshot,
    ) -> None:
        """Save one validated snapshot inside the caller's transaction."""
        session_id = str(snapshot.id)
        created_at = snapshot.created_at.isoformat()
        existing = connection.execute(
            "SELECT created_at FROM sessions WHERE session_id = ?",
            (session_id,),
        ).fetchone()
        if existing is None:
            connection.execute(
                "INSERT INTO sessions(session_id, created_at) VALUES (?, ?)",
                (session_id, created_at),
            )
        elif existing[0] != created_at:
            msg = f"Conflicting created_at for SessionId {snapshot.id}."
            raise PersistenceConflictError(msg)

        for message in snapshot.messages:
            self._save_message(connection, message)

        connection.execute(
            "DELETE FROM session_messages WHERE session_id = ?",
            (session_id,),
        )
        connection.execute(
            "DELETE FROM conversations WHERE session_id = ?",
            (session_id,),
        )
        connection.executemany(
            "INSERT INTO session_messages(session_id, position, message_id) "
            "VALUES (?, ?, ?)",
            [
                (session_id, position, str(message.id))
                for position, message in enumerate(snapshot.messages)
            ],
        )
        connection.executemany(
            "INSERT INTO conversations(session_id, source, value) VALUES (?, ?, ?)",
            [
                (session_id, str(conversation.source), conversation.value)
                for conversation in snapshot.conversations
            ],
        )

    def _save_message(
        self,
        connection: sqlite3.Connection,
        message: _MessageSnapshot,
    ) -> None:
        """Insert one immutable Message or validate its existing row."""
        message_id = str(message.id)
        values = (
            message.created_at.isoformat(),
            message.content,
            message.role.value,
            str(message.source),
        )
        existing = connection.execute(
            "SELECT created_at, content, role, source "
            "FROM messages WHERE message_id = ?",
            (message_id,),
        ).fetchone()
        if existing is None:
            connection.execute(
                "INSERT INTO messages(message_id, created_at, content, role, source) "
                "VALUES (?, ?, ?, ?, ?)",
                (message_id, *values),
            )
            return
        if tuple(existing) != values:
            msg = f"Conflicting immutable state for MessageId {message.id}."
            raise PersistenceConflictError(msg)

    def _load_messages(
        self,
        connection: sqlite3.Connection,
        session_id: SessionId,
    ) -> tuple[_MessageSnapshot, ...]:
        """Load ordered Message occurrences and validate contiguous positions."""
        rows = connection.execute(
            "SELECT session_messages.position, session_messages.message_id, "
            "messages.message_id, "
            "messages.created_at, "
            "messages.content, messages.role, messages.source "
            "FROM session_messages LEFT JOIN messages "
            "ON messages.message_id = session_messages.message_id "
            "WHERE session_messages.session_id = ? "
            "ORDER BY session_messages.position",
            (str(session_id),),
        ).fetchall()
        for row in rows:
            if row[2] is None:
                msg = (
                    "Persisted History references a missing Message row for "
                    f"SessionId {session_id} at position {row[0]} "
                    f"with MessageId {row[1]}."
                )
                raise PersistenceFormatError(msg)
        positions = [row[0] for row in rows]
        if positions != list(range(len(rows))):
            msg = f"Persisted History positions are invalid for SessionId {session_id}."
            raise PersistenceFormatError(msg)
        return tuple(
            _MessageSnapshot(
                id=MessageId.parse(row[2]),
                created_at=Timestamp.from_isoformat(row[3]),
                content=row[4],
                role=MessageRole(row[5]),
                source=MessageSource(row[6]),
            )
            for row in rows
        )

    def _load_conversations(
        self,
        connection: sqlite3.Connection,
        session_id: SessionId,
    ) -> tuple[ConversationRef, ...]:
        """Load current source-keyed opaque conversation references."""
        rows = connection.execute(
            "SELECT source, value FROM conversations "
            "WHERE session_id = ? ORDER BY source",
            (str(session_id),),
        ).fetchall()
        return tuple(
            ConversationRef(MessageSource(row[0]), row[1])
            for row in rows
        )


def _user_tables(connection: sqlite3.Connection) -> set[str]:
    """Return ordinary user table names from one SQLite database."""
    rows = connection.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' "
        "AND name NOT LIKE 'sqlite_%'",
    ).fetchall()
    return {row[0] for row in rows}


def _validate_required_columns(connection: sqlite3.Connection) -> None:
    """Reject version-1 tables that lack essential persistence columns."""
    for table, required_columns in _REQUIRED_COLUMNS.items():
        rows = connection.execute(f"PRAGMA table_info({table})").fetchall()
        columns = {row[1] for row in rows}
        if not required_columns.issubset(columns):
            msg = f"SQLite persistence table {table} lacks required columns."
            raise PersistenceFormatError(msg)
