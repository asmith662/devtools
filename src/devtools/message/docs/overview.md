# `devtools.message`

## Purpose

`devtools.message` provides the repository's generic immutable textual
communication value. It owns semantic message identity, conversational role,
producer/source provenance, textual content, and the local construction time
of a message.

It does not own provider integration or provider conversation state, session
ordering, persistence, display formatting, severity or logging policy, runtime
orchestration, command execution, or serialization.

## Public API

```python
from devtools.message import (
    Message,
    MessageId,
    MessageRole,
    MessageSource,
)
```

## `MessageId`

```python
MessageId(value: Identity)
```

`MessageId` is a frozen semantic wrapper composed around the generic
`Identity` primitive. It establishes the current repository pattern for
semantic IDs without implying that other semantic ID types already exist.

```python
MessageId.new()
MessageId.parse(text)
str(message_id)
```

`new()` delegates to `Identity.new()` and therefore generates UUID4 values.
`parse()` delegates to `Identity.parse()` and accepts every UUID version that
the generic identity primitive accepts. Parsed IDs are not restricted to UUID4.
Like other frozen dataclass values, message IDs compare and hash by value.

## Role and source

`MessageRole` identifies conversational perspective:

```text
USER      = "user"
ASSISTANT = "assistant"
SYSTEM    = "system"
```

`MessageSource` is an opaque producer/origin label. Examples such as `user`,
`codex`, `qwen`, and `runtime` are open examples, not a provider registry.

```text
role=USER       source=user
role=ASSISTANT  source=codex
role=ASSISTANT  source=qwen
role=SYSTEM     source=runtime
```

Role answers what conversational perspective a message represents. Source
answers what producer or origin created it. Neither determines the other.

Sources must not be blank or whitespace-only and may not contain leading or
trailing whitespace. Case is preserved; `str(source)` returns the exact stored
value. A source is not a provider enum because future producers should not
require a change to the message type definition.

## `Message`

```python
Message(
    id: MessageId,
    created_at: Timestamp,
    content: str,
    role: MessageRole,
    source: MessageSource,
)
```

`Message` is frozen and slotted. Equality and hashing use all five fields; they
are not based solely on `MessageId`.

Construct explicitly when reconstructing a known value:

```python
Message(
    id=message_id,
    created_at=timestamp,
    content="Please inspect the repository.",
    role=MessageRole.USER,
    source=MessageSource("user"),
)
```

Create a new local message with:

```python
Message.new(
    "Please inspect the repository.",
    role=MessageRole.USER,
    source=MessageSource("user"),
)
```

`Message.new()` creates a fresh `MessageId` and `Timestamp.now()` while
preserving the supplied content, role, and source.

`created_at` means local construction time. It is not remote provider authoring
time, provider event time, session insertion time, or persistence time.

## Content and representation

Content is uninterpreted `str`. It may be empty, whitespace-only, multiline,
Unicode, Markdown-like, JSON-looking, or arbitrary textual provider output.
The package performs no trimming, newline normalization, encoding, parsing,
format detection, or validation of textual meaning.

```python
str(message) == message.content
```

String conversion exposes communicative text only. Presentation of message ID,
role, source, or timestamp belongs to higher layers. Neither `str(message)`,
`repr(message)`, nor dataclass field layout is a serialization or persistence
contract.

## Immutability and dependencies

The current message graph is deeply immutable under supported values:

```text
Message
├── MessageId
│   └── Identity
│       └── UUID
├── Timestamp
├── str
├── MessageRole
└── MessageSource
```

The only production dependencies are:

```text
message -> identity
message -> time
```

Identity supplies the generic opaque identity primitive; time supplies
`Timestamp`. Python annotations define expected direct-construction field
types. The package does not perform broad runtime type enforcement; it checks
only intrinsic implemented invariants such as MessageSource whitespace rules.

## Boundaries and errors

Messages intentionally contain no session ID, sequence number, parent/reply
relationship, provider thread identifier, conversation state, or storage
location. A future session may order or reference message values without making
those concerns intrinsic message fields.

No message-specific error hierarchy exists. Malformed `MessageId` text exposes
the existing Identity/UUID `ValueError`; invalid source values raise
`ValueError`.

The package defines no canonical serialization, deserialization, persistence,
wire format, or storage schema.

Future provider integrations can construct an assistant message conceptually:

```python
Message.new(
    final_text,
    role=MessageRole.ASSISTANT,
    source=MessageSource("codex"),
)
```

This example does not imply that a Codex integration exists.

## Limitations and future evolution

Current boundaries include textual content only; no structured or multimodal
content, attachments, severity, TOOL role, provider/model metadata,
serialization, persistence, reply relationships, revision model, token usage,
exception embedding, session identity, or provider conversation identity.

When concrete consumers require them, MessageLevel/severity, structured
content, serialization, and provider/model metadata may be justified.
MessageKind, TOOL role, attachments, and revision/editing remain speculative.
Arbitrary metadata dumping, persistence ownership, parent/session ordering,
token usage, and exception embedding remain outside this package unless the
architecture materially changes.
