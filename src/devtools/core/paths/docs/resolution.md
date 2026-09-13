# Path parsing and resolution

This document defines the operational contract for `devtools.core.paths`. See the
[package overview](overview.md) for package boundaries and the public API.

## Parsing versus resolution

```text
parse
    representation -> Path

resolve
    path representation + base policy -> ResolvedPath
```

Parsing does not make a path absolute or inspect filesystem state. Resolution
applies explicit base-directory policy and `pathlib` normalization.

## `parse_path()`

`parse_path(value)` accepts exactly `str | pathlib.Path`.

- A `Path` is returned unchanged.
- A nonblank string becomes `Path(value)`.
- Blank or whitespace-only strings raise `PathParsingError`.
- Relative and absolute representations remain relative or absolute.
- `~` is not expanded.
- No filesystem access, symlink resolution, or normalization occurs beyond
  ordinary `Path` construction.
- Nonblank surrounding whitespace remains part of a string path.
- Separator interpretation is platform-native.

```python
parse_path("reports/latest.json")
parse_path(Path("reports/latest.json"))
```

## `parse_dot_path()`

`parse_dot_path()` mechanically splits nonempty dot components into a relative
path. It is not a Python import or identifier parser.

```python
parse_dot_path("devtools.core.paths.models")
# Path("devtools", "paths", "models")

parse_dot_path("devtools.core.paths.models", suffix=".py")
# Path("devtools", "paths", "models.py")
```

Outer whitespace is stripped. Empty input, leading dots, trailing dots, and
repeated dots raise `PathParsingError`. Optional suffixes use ordinary
`Path.with_suffix()` semantics; forms such as `"py"` and `".py"` are accepted.
Invalid suffix-application failures are normalized to `PathParsingError`.

Components have no Python-module semantics and are not otherwise validated as
identifiers. Embedded platform-native separators are not prohibited.

## `resolve_path()`

`resolve_path(value, *, base_directory=None)` parses first. Absolute input
resolves without a base. Relative input requires an explicit absolute base;
missing or relative bases raise `PathResolutionError`.

Resolution uses `Path.resolve(strict=False)`. A target need not exist; `.` and
`..` are normalized, and existing symlink components are handled according to
`pathlib` behavior. The result is `ResolvedPath`.

Here, “resolved” means a normalized absolute path produced by
`Path.resolve(strict=False)`. It does not mean existing, contained, trusted,
sandboxed, or authorized.

## `resolve_dot_path()`

`resolve_dot_path()` composes dot parsing with normal resolution:

```text
parse_dot_path()
    ↓
resolve_path()
```

It retains the same parsing and base-directory errors.

## Known directories

- `get_home_dir()` returns `Path.home().resolve(strict=False)`.
- `get_temp_dir()` returns `Path(tempfile.gettempdir()).resolve(strict=False)`.
- `get_downloads_dir()` resolves the conventional `home / "Downloads"` path.

All return uncached `ResolvedPath` values. The locations, including Downloads,
need not exist. Downloads is not an operating-system known-folder lookup.

## Errors

```text
PathError
├── PathParsingError
└── PathResolutionError
```

`PathParsingError` represents invalid textual path or dot-path input.
`PathResolutionError` represents missing or nonabsolute bases for relative
resolution. Direct construction of `ResolvedPath` with a relative `Path` raises
`ValueError`.

Not every operational exception is normalized: exceptions raised by
`Path.resolve()` itself retain their standard-library behavior.
