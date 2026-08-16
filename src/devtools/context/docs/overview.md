# `devtools.context`

## Purpose

`devtools.context` owns retained interaction context. Its implemented values
are immutable textual `Message` communication values, immutable ordered
`History` transcripts, and mutable `Session` interaction lifecycles.

Context is not a generic home for repository, filesystem, search,
command-result, provider-execution, or runtime state.

## Public API

```python
from devtools.context import (
    History,
    Message,
    MessageId,
    MessageRole,
    MessageSource,
    Session,
    SessionId,
)
```

Internal consumers use narrow submodules directly. The root export is the
supported convenience API for the currently implemented Context values.

## History

[`History`](history.md) is the immutable insertion-ordered Message transcript
primitive. It retains what messages occurred without deciding which Messages to
send to an Agent or storing provider continuation state.

## Session

[`Session`](session.md) is the application-owned mutable lifecycle for one
retained interaction. It owns one current immutable History and current
external Agent continuation references, plus local asynchronous complete-turn
coordination for that mutable state. Session retains state; it does not invoke
Agents, select model context, persist itself, or own provider configuration.

## `MessageId`

```python
MessageId(value: Identity)
```

`MessageId` is a frozen semantic wrapper composed around the generic
`Identity` primitive.

```python
MessageId.new()
MessageId.parse(text)
str(message_id)
```

`new()` delegates to `Identity.new()` and generates UUID4 values. `parse()`
delegates to `Identity.parse()` and accepts every UUID version that the generic
identity primitive accepts. Parsed IDs are not restricted to UUID4. Message
IDs compare and hash by value.

## Role and source

`MessageRole` identifies conversational perspective:

```text
USER      = "user"
ASSISTANT = "assistant"
SYSTEM    = "system"
```

`MessageSource` is an opaque producer/origin label. `user`, `codex`, `qwen`,
and `runtime` are open examples, not a provider registry. Role answers which
conversational perspective a message represents; source answers which producer
or origin created it. Neither determines the other.

Sources must be nonblank and have no leading or trailing whitespace. Case and
punctuation are preserved; `str(source)` returns the exact stored value.

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

`Message` is frozen and slotted. Equality and hashing use all five fields,
rather than only `MessageId`. Construct a known value explicitly, or create a
new local message with:

```python
Message.new(
    "Please inspect the repository.",
    role=MessageRole.USER,
    source=MessageSource("user"),
)
```

`Message.new()` creates a fresh `MessageId` and `Timestamp.now()` while
preserving content, role, and source. `created_at` is local construction time,
not provider authoring, event, session-insertion, or persistence time.

## Content and representation

Content is uninterpreted `str`. Empty, whitespace-only, multiline, Unicode,
Markdown-like, JSON-looking, and arbitrary provider text are valid. Context
does not trim, normalize newlines, encode, parse, or validate textual meaning.

```python
str(message) == message.content
```

String conversion exposes only content. Dataclass layout and representation are
not serialization or persistence contracts.

## Dependencies and boundaries

```text
context.message -> identity
context.message -> time

context.history -> context.message

context.session -> context.message
context.session -> context.history
context.session -> identity
context.session -> time
context.session -> agents
```

`agents -> context.message` and `context.session -> agents` remain acyclic:
Agents consume only the narrow Message submodule, while Session stores the
Agent-owned `ConversationRef` value.

Messages contain no session ID, sequence number, parent/reply relationship,
provider thread identity, conversation state, storage location, token usage, or
provider configuration. They do not own provider integration, persistence,
display formatting, severity/logging policy, command execution, or runtime
orchestration.

Malformed `MessageId` text preserves the Identity/UUID `ValueError`; invalid
source values raise `ValueError`. Context defines no message-specific error
hierarchy, serialization format, or storage schema.

`devtools.codex` is the first concrete downstream Message consumer: it maps final
provider output to an assistant `Message`, while its provider thread remains an
`agents.ConversationRef`. This does not make Context own Agent behavior.

## Current limitations

No structured or multimodal content, attachments, severity, TOOL role,
provider/model metadata, serialization, persistence, reply relationships,
revisions, token usage, exception embedding, or context compilation is
implemented. History- and Session-specific behavior and limitations are
documented in [history.md](history.md) and [session.md](session.md). Future
additions require concrete consumers and a separate approved milestone.
