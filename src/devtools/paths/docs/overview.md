# `devtools.paths`

## Purpose

`devtools.paths` owns path representation, parsing, absolute resolution, and a
small set of known-location constructors. It does not own filesystem contents
or I/O. See [resolution details](resolution.md) for the operational contract.

## Public API

```python
from devtools.paths import (
    PathError,
    PathParsingError,
    PathResolutionError,
    ResolvedPath,
    get_downloads_dir,
    get_home_dir,
    get_temp_dir,
    parse_dot_path,
    parse_path,
    resolve_dot_path,
    resolve_path,
)
```

| Group             | API                                                       |
|-------------------|-----------------------------------------------------------|
| Model             | `ResolvedPath`                                            |
| Errors            | `PathError`, `PathParsingError`, `PathResolutionError`    |
| Parsing           | `parse_path()`, `parse_dot_path()`                        |
| Resolution        | `resolve_path()`, `resolve_dot_path()`                    |
| Known directories | `get_home_dir()`, `get_temp_dir()`, `get_downloads_dir()` |

## `ResolvedPath`

`ResolvedPath(value: Path)` is a frozen, slotted absolute-path value object.
Its `value` field is authoritative. It supports `os.PathLike[str]`, value
equality, hashing, `str()`, and `os.fspath()`.

Its mechanical accessors are `name`, `stem`, `suffix`, `suffixes`, `parent`,
`parts`, `as_posix()`, and `as_uri()`. `parent` intentionally returns a plain
`Path`.

Direct construction validates only that `value` is absolute. `ResolvedPath`
means an absolute path value; it does not imply that the path exists, is safe,
is contained beneath a trusted root, or is authorized for access.

## Package architecture

```text
representation
    ResolvedPath

parsing
    parse_path()
    parse_dot_path()

resolution
    resolve_path()
    resolve_dot_path()

known locations
    get_home_dir()
    get_temp_dir()
    get_downloads_dir()
```

Parsing and resolution are deliberately separate. Parsing interprets a
representation; resolution applies an explicit absolute-path policy.

## Dependencies and consumers

The package uses Python standard-library `os`, `pathlib`, and `tempfile`
facilities. It has no dependency on `devtools.system` or `devtools.filesystem`.
Domains such as commands and filesystem consume `ResolvedPath` as their
absolute-path input value.

## Package boundaries

`devtools.system` is not needed for the current standard-library home and
temporary-directory mechanisms or the documented Downloads convention.

`devtools.paths` does not own reading, writing, format detection, file models,
filesystem traversal, mutation, or file metadata inspection; these belong to
`devtools.filesystem` where applicable.

## Limitations

- Absolute does not mean existing, contained, safe, trusted, or authorized.
- There is no sandbox, allowed-root, path-traversal, or symlink-escape policy.
- `parse_path()` does not expand `~` and uses platform-native separators.
- Direct `ResolvedPath` construction relies on its `Path` input contract rather
  than broad runtime input validation.
- Downloads is `home / "Downloads"`, not an operating-system known-folder
  lookup.

## Future evolution

Containment or allowed-root checks, explicit symlink policy for a
security-sensitive consumer, relative/common-root helpers, and platform-known
or application-configuration directories may be added when real consumers
require them. Filesystem I/O and mutation remain outside this package.
