# `devtools.core.identity`

## Purpose

`devtools.core.identity` provides the minimal canonical opaque identity primitive
for developer tooling.

## Public API

```python
from devtools.core.identity import Identity
```

`Identity` exposes `new()`, `parse()`, the backing `value`, and canonical
string conversion through `str(identity)`.

## Construction and lifecycle

Use direct construction to rehydrate an existing UUID, `parse()` to interpret
UUID text, and `new()` to generate a fresh identity:

```python
Identity(existing_uuid)
Identity.parse(text)
Identity.new()
```

These operations are intentionally distinct.

## Generation semantics

`Identity.new()` creates a UUID4. Generated identities are random and opaque;
they have no ordering or timestamp semantics.

## Parsing semantics

`Identity.parse()` delegates UUID text interpretation to Python's standard
library. `str(identity)` returns canonical lowercase hyphenated UUID text.
Parsing accepts UUIDs of any version and raises `ValueError` for malformed
text.

## Value semantics

`value` is the backing `UUID`. `Identity` is a frozen, slotted value object;
it is immutable, compares by value, and is hashable. Its UUID backing value is
also immutable.

## Dependencies

This package depends only on Python standard-library `dataclasses` and `uuid`
facilities. It does not depend on another `devtools` package.

## Package boundaries

Identity does not own semantic typed IDs, registries, lookup, ownership,
timestamps, sequencing, persistence stores, or serialization protocols beyond
its canonical string representation.

## Limitations

UUID4 values are random and unordered. Direct runtime construction relies on
static typing rather than an explicit type guard. Parsing accepts every UUID
version, and no typed semantic IDs currently exist.

## Future evolution

When concrete consumers require them, `SessionId`, `MessageId`, `ExecutionId`,
and `ArtifactId` may be separate semantic wrappers composed around `Identity`.
UUID7 is appropriate only if ordered or time-oriented identity becomes a real
requirement. Explicit serialization support should wait for a protocol or
persistence consumer.
