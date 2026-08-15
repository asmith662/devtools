# `devtools.system`

## Purpose

`devtools.system` provides a small foundational abstraction for identifying the
current operating-system family. It is intentionally coarse and is not a
machine-inventory service.

## Public API

```python
from devtools.system import OperatingSystem, get_operating_system
```

## `OperatingSystem`

`OperatingSystem` is a `StrEnum` with stable string values:

```python
OperatingSystem.WINDOWS  # "windows"
OperatingSystem.LINUX    # "linux"
OperatingSystem.MACOS    # "macos"
OperatingSystem.OTHER    # "other"
```

Its string representation is its value, so
`str(OperatingSystem.WINDOWS) == "windows"`. The `is_windows`, `is_linux`,
and `is_macos` properties identify their matching family. All three are
`False` for `OperatingSystem.OTHER`.

## Detection

`get_operating_system()` delegates to `platform.system()` and maps its result
exactly:

| `platform.system()` | Result                    |
|---------------------|---------------------------|
| `Windows`           | `OperatingSystem.WINDOWS` |
| `Linux`             | `OperatingSystem.LINUX`   |
| `Darwin`            | `OperatingSystem.MACOS`   |
| anything else       | `OperatingSystem.OTHER`   |

Matching is exact and case-sensitive; for example, `"windows"` resolves to
`OperatingSystem.OTHER`.

## Invocation semantics

Detection runs each time `get_operating_system()` is called. It is not cached
and does not retain global system state.

## Dependencies

The package uses only Python standard-library `enum` and `platform`
functionality. It has no dependency on another `devtools` package.

## Package boundaries

This package does not provide CPU architecture detection, hostname, username,
kernel or version inventory, Python runtime information, environment-variable
management, CPU or hardware inventory, host capability discovery, or general
environment inspection.

## Limitations

WSL is currently classified as Linux. BSD, Android, and other unrecognized
systems resolve to `OperatingSystem.OTHER`. Detection is operating-system-family
classification only and depends on exact standard-library `platform.system()`
values. There is no system-specific error hierarchy.

## Future evolution

Architecture detection may be added if a concrete consumer requires
architecture-dependent behavior. WSL may be distinguished if path, command, or
filesystem behavior actually requires it. Narrow platform-capability predicates
may be justified if multiple real consumers need them. Broad machine inventory
and runtime or environment inspection are not planned without a concrete
architectural need.
