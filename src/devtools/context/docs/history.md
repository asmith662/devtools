# History

## Purpose

`History` is an immutable, insertion-ordered transcript of
[`Message`](overview.md#message) values. It answers only what messages occurred
and in what retained order.

It is not an Interaction invocation record, provider event log, persistence model, or
context-selection mechanism.

## Public API

```python
from devtools.context import History
from devtools.context.history import History
```

Both imports refer to the same class.

## Representation and construction

```python
History(messages: tuple[Message, ...] = ())
```

`messages` is the public immutable stored transcript representation.

```python
empty = History()
restored = History(messages=(first_message, second_message))
```

Keyword construction is preferred for clarity. Type annotations describe
supported values; History does not broadly validate tuple or Message types at
runtime.

## Ordering and duplicates

Tuple position is authoritative transcript order. History does not sort by
`Message.created_at`, ID, role, or source; equal or out-of-order timestamps are
valid. Equal or identical Messages may appear at multiple independent
positions—History is a sequence, not a set.

## Sequence semantics

History is a read-only `Sequence[Message]`.

```python
len(history)
for message in history:
    ...
message in history

history[0]  # Message
history[-1]  # Message
```

Membership uses Message value equality. Integer indices use normal Python
behavior, including `IndexError` when out of range.

The standard Sequence conveniences are also available with their ordinary
semantics:

```python
history.index(message)  # first equal position; ValueError if absent
history.count(message)  # number of equal Messages
reversed(history)  # reverse iterator
```

They are standard collection behavior, not a History query language.

## Slicing

History preserves its domain when sliced:

```python
history[1:4]  # History
history[-10:]  # History
history[::2]  # History
history[::-1]  # History
```

Slice selection follows normal tuple semantics, but selected Messages are
wrapped in a new History rather than exposed as a raw tuple. The value guarantee
for a full slice is `history[:] == history`; object identity is not a contract.

## Append and snapshots

```python
after = history.append(message)
```

`append()` is the only History-specific transformation. It returns a new
History with existing Messages retained in order and the exact supplied Message
last. The source History is unchanged:

```python
before = history
after = before.append(message)
```

These immutable values provide stable transcript snapshots for testing,
debugging, selection, and reconstruction. They do not by themselves provide
persistence or replay.

## Equality and hashing

History uses ordered dataclass value equality. Equal ordered Message sequences
compare and hash equally; order matters. History is a domain value and does not
compare equal to an equivalent raw tuple or list.

## Dependencies

```text
context.history -> context.message
```

History has no direct dependency on Agents, Codex, commands, paths,
filesystem, or runtime.

## Boundaries

History has no ID, timestamps, status, custom string contract, error hierarchy,
serialization format, storage schema, or persistence behavior. Its dataclass
repr is debugging output only.

It does not provide role/source filtering, text search, `last_n`, time windows,
context windows, token budgeting, summarization, relevance, selection,
compaction, or pruning.

History stores no `ConversationRef`:

```text
History         what Messages happened
ConversationRef how an external Interaction conversation can continue
future Session  expected owner of both retained state kinds
```

## Limitations and constrained future evolution

Speculative conveniences such as `extend()`, first/last accessors, role/source
filters, `last_n`, time boundaries, search, and context windows require real
consumers. History IDs, History timestamps, generic `History[T]`, event-entry
models, provider continuation state, branching, and persistence ownership stay
out of this architecture. Session restoration may later revisit persistence at
the Session boundary rather than assigning it to History.

Tuple-backed immutable appends and slices copy references linearly with
transcript size. This is acceptable for the current milestone; optimization
requires evidence from real transcript workloads.
