# Architecture

`devtools` is one Python project and distribution. Its source is organized by
cohesive capability domains under `src/devtools/`.

`devtools.paths` owns path-related primitives. A domain may begin with its
implementation in `__init__.py` and grow internal modules only when cohesion
justifies them. Capabilities are not made separately distributable preemptively.

Path primitives remain AI-neutral and work for ordinary Python callers. The
current `ResolvedPath` proves only that its stored `pathlib.Path` is absolute.
Explicit resolution, containment, transformations, and dot-path behavior are
separate future work.
