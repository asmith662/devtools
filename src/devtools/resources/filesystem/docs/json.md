# JSON models and codec

## Models and immutability

```text
JsonFile
├── JsonObjectFile
├── JsonListFile
└── JsonScalarFile
```

JSON objects are recursively immutable mappings backed by `MappingProxyType`;
arrays are tuples; scalars are `str | int | float | bool | None`. JSON object
and list transformations recursively freeze inserted values.

```text
parsed mutable JSON → freeze_json() → immutable model value
immutable model value → thaw_json() → fresh dict/list/scalar values
```

Thawing is used at serialization and explicit callable-conversion boundaries.
The helpers remain in the JSON model representation boundary, not the root
filesystem API.

## Structured access

`JsonObjectFile` behaves as `Mapping[str, JsonValue]`, supports `find()` and
`find_all()` predicates over `(key, value)`, and has `with_item()`,
`with_items()`, `without()`, and `convert()`.

`JsonListFile` behaves as `Sequence[JsonValue]`, including negative indexing
and slices. It supports `find()`, `find_all()`, top-level-mapping `find_by()`,
`appended()`, `extended()`, `with_item()`, `without_index()`, and
`convert_items()`.

`find_by()` requires the member to be present: an absent member does not match
an explicit null query. It freezes a compatible query once, so ordinary lists
and nested mapping/list values compare against immutable arrays/mappings without
changing the model. Matching mappings remain in first-item order.

`JsonScalarFile` is a valid scalar-root model with `.value` and `.convert()`;
it does not pretend to be a collection. Every JSON model inherits source
regex search from TextFile. Structured predicates operate on current frozen
state; regex operations search original `.content`.

## Provenance and conversion

`.content` is original decoded JSON source provenance. `.value` is current
structured state. Immutable transformations retain `.content`; serialization
uses `.value`. Object conversion receives a thawed ordinary dict, scalar
conversion receives the scalar, and list conversion thaws each item.

## `JsonCodec`

`decode()` converts bytes to source text; `parse()` selects object, list, or
scalar models; `serialize()` renders current `.value`; `encode()` produces
bytes. The codec never reads or writes disk.

Parsing is strict: nonstandard constants such as `NaN` and floating-point literals
that overflow to non-finite values are rejected at every nesting depth. Finite
floats, underflow and arbitrary-size integers retain their normal Python JSON
semantics. Conversion failures retain their cause through `FileFormatError`. Invalid
source becomes `FileFormatError`, with line/column information for ordinary
JSON decode failures. Serialization defaults to indent `2`, `ensure_ascii=False`,
unsorted keys, and a trailing newline; indentation, ASCII escaping, key sorting,
and final newline are configurable. JSON5/comments and source-format-preserving
writes are unsupported.
