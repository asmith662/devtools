# `devtools.conversion`

## Purpose

`devtools.conversion` is a small framework-neutral boundary around explicit,
caller-provided conversion callables. It provides stable error normalization
for one value or an ordered batch without choosing how objects are constructed.

## Public API

```python
from devtools.conversion import (
    ConversionError,
    Converter,
    convert,
    convert_all,
)
```

| API               | Purpose                                           |
|-------------------|---------------------------------------------------|
| `Converter`       | Typing alias for one explicit conversion callable |
| `ConversionError` | Stable conversion failure context                 |
| `convert()`       | Convert one value                                 |
| `convert_all()`   | Convert an ordered iterable of values             |

## Converter contract

```python
type Converter[SourceT, TargetT] = Callable[[SourceT], TargetT]
```

The alias describes one explicit transformation, `SourceT -> TargetT`. It is a
typing-only abstraction: it has no runtime protocol, registry, target-type
inspection, or wrapper behavior.

```python
report = convert(source, lambda value: Report(**value))
```

The caller owns construction policy and supplies the callable directly.

## Single conversion

```python
convert(value, converter)
```

The converter is invoked exactly once and its result is returned unchanged.
When it raises an ordinary `Exception`, `convert()` raises `ConversionError`
with `index=None` and `source_type=type(value)`, retaining the original error
as `__cause__`.

If the converter raises an existing `ConversionError`, it is re-raised
unchanged. The package intentionally normalizes `ValueError`, `TypeError`,
domain-specific exceptions, and ordinary programmer errors alike when they
inherit from `Exception`; callers can inspect the original failure through
exception chaining. Conversion does not attempt to classify converter errors.

## Batch conversion

```python
convert_all(values, converter) -> tuple[TargetT, ...]
```

Batch conversion accepts any iterable, including generators, consumes values
in source order, and returns an immutable tuple. An empty iterable returns
`()`. Processing is fail-fast: no later converter calls occur after the first
failure, and no partial result is returned.

For an ordinary converter failure, the cause chain is:

```text
original converter exception
        ↓ cause
single ConversionError(index=None)
        ↓ cause
batch ConversionError(index=N)
```

The outer batch error records the zero-based failed index and the failed
item's runtime type. If the converter raises an existing `ConversionError`,
single conversion preserves it and batch conversion adds a new indexed error
whose cause is that existing error.

## Error semantics

`ConversionError` exposes only stable, bounded diagnostic context:

```python
error.source_type
error.index
```

`index` is `None` for a single value and a zero-based item position for batch
conversion. Error messages are deterministic, for example:

```text
Conversion failed for source type dict.
Conversion failed at index 1 for source type CsvRow.
```

Source values are not retained or rendered merely for diagnostics. This avoids
accidentally exposing large or sensitive data through conversion errors.

## `BaseException` behavior

The conversion boundary catches `Exception`, not `BaseException`. Control-flow
and process-level exceptions outside ordinary exception handling propagate
untouched. The package adds no async-specific behavior.

## Current consumers

Filesystem models are the current consumers.

- `CsvRow.convert(converter)` passes the immutable row itself; callers choose
  `row.as_dict()` explicitly when desired.
- `CsvFile.convert_rows(converter)` delegates ordered rows to `convert_all()`;
  a failed index is the CSV row position.
- `JsonObjectFile.convert(converter)` receives a thawed ordinary `dict` with
  nested ordinary `dict` and `list` values.
- `JsonScalarFile.convert(converter)` receives the scalar value.
- `JsonListFile.convert_items(converter)` thaws items independently; a failed
  index is the JSON array position.

Those adapters leave their immutable CSV and JSON source models unchanged.

## Dependencies

`devtools.conversion` uses only Python standard-library callable and iterable
facilities. It is independent of filesystem, JSON, CSV, serialization,
Pydantic, dataclasses as a conversion framework, and runtime/session domains.

```text
devtools.conversion
    standard-library only

devtools.filesystem
    ↓ consumes
devtools.conversion
```

## Boundaries

This package owns explicit callable invocation, stable ordinary-exception
normalization, and ordered fail-fast batch conversion. It does not own
automatic object construction, type introspection, framework adapters,
coercion, validation, serialization, schema mapping, registries, async work,
or tolerant batch processing.

## Limitations

- No target-type construction or framework-specific conversion exists.
- No coercion, validation framework, or serialization behavior exists.
- There is no tolerant or aggregated-error batch mode.
- There is no async conversion.
- All ordinary converter exceptions share one normalized public error boundary.

## Future evolution

Richer diagnostic context may be justified if concrete consumers need more
than source type and index. Tolerant or aggregated batch behavior, and async
conversion, should be considered only when real use cases emerge. A
`Converter` protocol, conversion registry, and automatic target-type
construction are not currently justified.
