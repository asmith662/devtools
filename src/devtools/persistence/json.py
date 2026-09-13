# Copyright (c) 2026
"""Strict portable JSON Conversation serialization."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, NoReturn

from devtools.agents.conversation.conversation import ConversationId
from devtools.agents.conversation.message import (
    ConversationMessageRole,
    MessageId,
)
from devtools.core.time import TimeError, Timestamp
from devtools.models.interaction import ConversationRef, InteractionSource
from devtools.persistence._snapshot import (
    _MessageSnapshot,
    capture_conversation,
    restore_conversation,
    snapshot_from_values,
)
from devtools.persistence.errors import (
    PersistenceConflictError,
    PersistenceFormatError,
    PersistenceVersionError,
)

if TYPE_CHECKING:
    from devtools.agents.conversation.conversation import Conversation


_SCHEMA_VERSION = 1


def encode_conversation_json(conversation: Conversation) -> str:
    """Encode one Conversation semantic snapshot as deterministic strict JSON text."""
    snapshot = capture_conversation(conversation)
    value: dict[str, object] = {
        "schema_version": _SCHEMA_VERSION,
        "session": {
            "id": str(snapshot.id),
            "created_at": snapshot.created_at.isoformat(),
        },
        "history": [
            {
                "id": str(message.id),
                "created_at": message.created_at.isoformat(),
                "content": message.content,
                "role": message.role.value,
                "source": str(message.source),
            }
            for message in snapshot.messages
        ],
        "conversations": [
            {
                "source": str(conversation.source),
                "value": conversation.value,
            }
            for conversation in snapshot.conversations
        ],
    }
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    )
    return f"{serialized}\n"


def decode_conversation_json(text: str) -> Conversation:
    """Decode one strict JSON Conversation semantic snapshot."""
    try:
        parsed: object = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_keys,
            parse_constant=_reject_nonstandard_constant,
        )
    except PersistenceFormatError:
        raise
    except (json.JSONDecodeError, ValueError) as error:
        msg = "Invalid Conversation JSON representation."
        raise PersistenceFormatError(msg) from error

    try:
        root = _require_object(parsed, "root")
        _require_fields(
            root,
            {"schema_version", "session", "history", "conversations"},
            "root",
        )
        _validate_version(root["schema_version"])
        session_value = _require_object(root["session"], "session")
        _require_fields(session_value, {"id", "created_at"}, "session")
        conversation_id = ConversationId.parse(
            _require_string(session_value["id"], "session.id"),
        )
        created_at = Timestamp.from_isoformat(
            _require_string(session_value["created_at"], "session.created_at"),
        )
        history_value = _require_list(root["history"], "history")
        messages = tuple(
            _decode_message(value, index) for index, value in enumerate(history_value)
        )
        conversations_value = _require_list(root["conversations"], "conversations")
        conversations = tuple(
            _decode_conversation(value, index)
            for index, value in enumerate(conversations_value)
        )
        _validate_conversation_sources(conversations)
        snapshot = snapshot_from_values(
            conversation_id=conversation_id,
            created_at=created_at,
            messages=messages,
            conversations=conversations,
        )
        return restore_conversation(snapshot)
    except (PersistenceConflictError, PersistenceFormatError, PersistenceVersionError):
        raise
    except (TimeError, TypeError, ValueError) as error:
        msg = "Invalid Conversation JSON semantic value."
        raise PersistenceFormatError(msg) from error


def _decode_message(value: object, index: int) -> _MessageSnapshot:
    """Decode one History occurrence."""
    item = _require_object(value, f"history[{index}]")
    _require_fields(
        item,
        {"id", "created_at", "content", "role", "source"},
        f"history[{index}]",
    )
    return _MessageSnapshot(
        id=MessageId.parse(_require_string(item["id"], f"history[{index}].id")),
        created_at=Timestamp.from_isoformat(
            _require_string(item["created_at"], f"history[{index}].created_at"),
        ),
        content=_require_string(item["content"], f"history[{index}].content"),
        role=ConversationMessageRole(
            _require_string(item["role"], f"history[{index}].role"),
        ),
        source=InteractionSource(
            _require_string(item["source"], f"history[{index}].source"),
        ),
    )


def _decode_conversation(value: object, index: int) -> ConversationRef:
    """Decode one current opaque conversation reference."""
    item = _require_object(value, f"conversations[{index}]")
    _require_fields(item, {"source", "value"}, f"conversations[{index}]")
    return ConversationRef(
        InteractionSource(
            _require_string(item["source"], f"conversations[{index}].source"),
        ),
        _require_string(item["value"], f"conversations[{index}].value"),
    )


def _require_object(value: object, field: str) -> dict[str, object]:
    """Return an object-shaped JSON value."""
    if not isinstance(value, dict):
        msg = f"Conversation JSON field {field} must be an object."
        raise PersistenceFormatError(msg)
    return value


def _require_list(value: object, field: str) -> list[object]:
    """Return a list-shaped JSON value."""
    if not isinstance(value, list):
        msg = f"Conversation JSON field {field} must be an array."
        raise PersistenceFormatError(msg)
    return value


def _require_string(value: object, field: str) -> str:
    """Return a string-shaped JSON value."""
    if not isinstance(value, str):
        msg = f"Conversation JSON field {field} must be a string."
        raise PersistenceFormatError(msg)
    return value


def _require_fields(value: dict[str, object], expected: set[str], field: str) -> None:
    """Require an exact object field set."""
    if set(value) != expected:
        msg = f"Conversation JSON field {field} has an unsupported field set."
        raise PersistenceFormatError(msg)


def _validate_version(value: object) -> None:
    """Validate the one supported JSON schema version."""
    if type(value) is not int:
        msg = "Conversation JSON schema_version must be an integer."
        raise PersistenceFormatError(msg)
    if value != _SCHEMA_VERSION:
        msg = f"Unsupported Conversation JSON schema version: {value}."
        raise PersistenceVersionError(msg)


def _reject_duplicate_keys(pairs: list[tuple[str, object]]) -> dict[str, object]:
    """Reject duplicate object keys instead of silently collapsing them."""
    value: dict[str, object] = {}
    for key, item in pairs:
        if key in value:
            msg = f"Duplicate Conversation JSON object key: {key}."
            raise PersistenceFormatError(msg)
        value[key] = item
    return value


def _reject_nonstandard_constant(value: str) -> NoReturn:
    """Reject JSON constants outside the standard JSON grammar."""
    msg = f"Invalid Conversation JSON constant: {value}."
    raise PersistenceFormatError(msg)


def _validate_conversation_sources(conversations: tuple[ConversationRef, ...]) -> None:
    """Reject ambiguous current continuation sources."""
    sources = {conversation.source for conversation in conversations}
    if len(sources) != len(conversations):
        msg = "Conversation JSON cannot contain multiple conversations for one source."
        raise PersistenceFormatError(msg)
