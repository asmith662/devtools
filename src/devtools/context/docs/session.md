# Session

## Purpose

`Session` is the application-owned, identified mutable lifecycle for one
retained interaction. It owns the current immutable `History` and the current
external continuation references needed to continue participating
Interactions. It does not invoke Interactions.

```text
Message          one contextual utterance
History          immutable ordered transcript
ConversationRef  opaque external Interaction continuation identity
Session          mutable retained interaction lifecycle
Runtime          stateless coordinator that invokes Interactions and updates Session
```

The first real consumer proof uses the
[Codex adapter](../../interactions/providers/codex/docs/overview.md),
but Session is generic and does not depend on Codex behavior.

## Public API

```python
from devtools.context import Session, SessionId
from devtools.context.session import Session, SessionId
```

Both import forms expose the same types.

## SessionId

```python
@dataclass(frozen=True, slots=True)
class SessionId:
    value: Identity
```

`SessionId` identifies our retained application Session. It is not a
`MessageId`, `ConversationRef`, provider thread ID, `MessageSource`, Interaction
identity, or execution identity.

```python
SessionId.new()
SessionId.parse(text)
str(session_id)
```

`new()` delegates to `Identity.new()` and therefore uses the repository's UUID4
generation behavior. It implies no ordering or temporal semantics. `parse()`
delegates to `Identity.parse()`, accepts the UUID forms and versions accepted
there, and preserves the existing `ValueError` boundary for malformed text.

`SessionId` is an immutable, hashable semantic identity value. `Session` is a
separate mutable lifecycle object.

## Construction and lifecycle state

```python
Session(
    *,
    id: SessionId,
    created_at: Timestamp,
    history: History = History(),
    conversations: Iterable[ConversationRef] = (),
)
```

The keyword-only constructor is the deterministic in-memory reconstruction
boundary. It preserves supplied `SessionId`, `Timestamp`, `History`, and
current continuation references. It is not serialization or persistence.

```python
session = Session.new()
```

`new()` creates a fresh `SessionId`, `Timestamp.now()`, empty `History`, and no
current continuation references. Every constructed Session also receives fresh
in-memory turn coordination; it is not semantic reconstruction state and is
not shared by separately reconstructed objects with equal Session IDs.

The following state is readable but not directly assignable:

```python
session.id
session.created_at
session.history
session.conversations
```

`created_at` is local Session construction time. It remains stable as the
Session changes. Session currently has no `updated_at`, status, close state,
title, metadata, owner, copy, snapshot, or custom string/repr contract.

## History ownership and messages

Session owns exactly one current `History`; History has no back-reference to
Session. Session is not itself a sequence. Use `len(session.history)` or
`session.history[-1]`, rather than `len(session)` or indexing Session.

```python
session.add(message)
```

`add(message: Message) -> None` accepts every Message role and source,
including duplicates. It preserves the exact supplied Message and replaces the
current History with `history.append(message)`.

```python
before = session.history
session.add(message)
after = session.history
```

`before` remains an unchanged immutable transcript snapshot; `after` contains
the appended Message.

## Current conversations

`ConversationRef` remains owned by
[`devtools.interactions`](../../interactions/docs/overview.md):
it is opaque continuation state returned by an Interaction. Session stores those
values because retained continuation state is needed to reconstruct and
continue an interaction.

```python
session.conversations
```

is a read-only `Mapping[MessageSource, ConversationRef]` view of current
Session state. A view obtained earlier reflects later Session-managed updates,
but callers cannot mutate it directly. Mapping-proxy object identity is not a
public contract.

```python
session.conversation_for(source)  # ConversationRef | None
session.set_conversation(conversation)  # None
```

`conversation_for()` uses normal `MessageSource` value equality and returns
the current reference or `None`. `set_conversation()` derives its key from
`conversation.source`, retains the supplied ref, and replaces any existing ref
for that source.

Constructor reconstruction accepts an `Iterable[ConversationRef]`. Two refs
with equal sources are ambiguous and raise `ValueError`. After construction,
setting a newer ref for the same source replaces the active ref; Session keeps
no reference history. Different sources coexist. A stateless Interaction returning
`conversation=None` requires no Session continuation-state mutation.

### Source-keyed limitation

The first Session milestone maintains at most one current external conversation
per `MessageSource`. Multiple logical participants sharing one source cannot
yet retain independent current conversations in one Session. For example, a
Codex implementer and reviewer using source `codex` cannot simultaneously hold
different provider threads here.

Future design must answer: what stable identity distinguishes logical
participants or Interaction instances that share one `MessageSource` while retaining
independent `ConversationRef` values inside one Session? This document does not
choose or introduce that identity.

## Equality and identity

Session uses Python object-identity equality. Separately reconstructed Sessions
with identical fields are not equal. Compare `session_a.id == session_b.id`
when semantic Session identity matters.

Session is explicitly unhashable. Do not use mutable Session objects as set
members or dictionary keys; use `SessionId` for stable identity values.

## Runtime, Interaction, and provider boundaries

Session stores retained state, not services. It stores no Interaction or CodexAgent
instances and has no `apply(turn)` operation. The implemented
[`Runtime`](../../runtime/docs/overview.md) composes the existing APIs inside
`session.turn()`:

```python
session.add(user_message)
conversation = session.conversation_for(Interaction.source)
turn = await Interaction.send(user_message, conversation=conversation)
session.add(turn.message)
if turn.conversation is not None:
    session.set_conversation(turn.conversation)
```

Session does not own Codex executable or working-directory settings, sandbox or
approval policy, model, endpoint, or credentials. It has no repository,
filesystem, command, artifact, or context compiler state.

## Turn coordination

```python
async with session.turn() as value:
    assert value is None
    # Retain input, retrieve the current ref, await an Interaction, and retain output.
```

`turn()` acquires exclusive asynchronous coordination for one complete logical
turn against this Session object. It yields no additional value. Session
mutation methods remain synchronous; `turn()` coordinates their multi-step
composition rather than making each individual method lock itself.

The context must cover input retention, continuation lookup, an awaited Interaction
call, returned-message retention, and continuation replacement. Without that
scope, overlapping callers could retain interleaved input, read the same stale
`ConversationRef`, invoke one provider continuation concurrently, overwrite
the current ref in completion order, and leave an ambiguous transcript.

```text
Session A  complete turns serialize
Session B  complete turns serialize
A and B    may proceed concurrently
```

The private coordination primitive belongs to the Session object, not its
`SessionId`. Two separately reconstructed objects with equal Session IDs do not
coordinate automatically. The primitive is not semantic state, is not exposed,
and is not reconstructed, persisted, or serialized.

Turn coordination is intended for one Session object within one asynchronous
event loop. Constructing a Session synchronously and first using it in an event
loop is supported. Cross-event-loop reuse is unsupported, even if an
uncontended case appears to work. `turn()` is asynchronous coordination, not
thread synchronization; it does not coordinate threads, distinct reconstructed
objects, processes, workers, machines, databases, or distributed execution.

`turn()` is non-reentrant. Do not nest turn contexts for the same Session
object. Cancellation while waiting propagates without acquiring the lock;
cancellation or an ordinary exception inside the context propagates and releases
coordination through normal async-context cleanup. Session does not promise
waiter fairness, FIFO turn scheduling, or caller-submission ordering.

Turn coordination is exclusive access, not a transaction or rollback boundary.
If Runtime has already retained input or output when a later step
fails, Session does not automatically revert the state already applied.

## Persistence

Session defines no save/load API, serialization format, database schema, or
filesystem persistence itself. The implemented
[`devtools.persistence`](../../persistence/docs/overview.md) domain owns durable
representation and reconstruction of Session ID, creation time, History, and
current refs. Reconstruction creates a new Session object with fresh local turn
coordination; no lock or event-loop state is persisted.

## Errors and dependencies

No `SessionError` exists. Duplicate reconstruction sources raise `ValueError`;
malformed `SessionId` text preserves Identity's `ValueError`; direct mapping
mutation and `hash(session)` raise normal `TypeError`.

```text
context.message -> identity
context.message -> time
context.history -> context.message
context.session -> context.message
context.session -> context.history
context.session -> identity
context.session -> time
context.session -> interactions
```

`interactions -> context.message`, and Interactions do not depend on
`context.session`, so the graph is acyclic.

## Live Codex acceptance

The opt-in Session/Codex acceptance uses an isolated temporary Git repository.
Each complete fresh and resumed turn runs inside its own `session.turn()`
context. The test verifies a new Session retains first user and assistant
Messages, stores the returned Codex `ConversationRef`, retrieves it from
Session for the second turn, resumes the same thread, and retains the second
user and assistant Messages in an exact four-Message History. It also verifies
stable `SessionId` and `created_at`, plus read-only resumed Codex execution
through a denied disposable write attempt.

This is evidence that generic Session continuation storage works with one real
Interaction implementation; it is not a Codex requirement of Session.

## Constrained future evolution

Justified only after concrete consumers: logical participant identity and
multiple same-source refs, storage design for persistence/serialization, and a
cross-object, cross-process, or distributed concurrency design when those
topologies become real requirements.

Speculative conveniences include clearing refs, `updated_at`, status, title,
metadata, and Session copy/snapshot behavior.

Keep out of Session: `InteractionTurn.apply()`, sequence proxies, provider execution
or configuration, continuation-reference history, context compilation, and
repository/filesystem ownership.
