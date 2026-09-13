# `devtools.tools`

## Experimental status

`devtools.tools` is an **experimental provider-neutral Tool foundation**. Its
API and behavior may change as real Tool-using Interaction workflows are exercised.
It is not frozen, persistent, instrumented, or a Runtime extension.

## Purpose

A `Tool` is a named asynchronous capability that accepts Tool-defined semantic
input and returns a Tool-defined result. A Tool is not a Command, Interaction,
Runtime Attempt, model invocation, provider schema, transport endpoint, or MCP
request.

```python
from devtools.tools import Tool, ToolInputError, ToolRunner
```

`Tool` has a nonblank local `name`, a provider-neutral `description`, semantic
`validate(arguments)`, and asynchronous `execute(arguments)`. Typed argument
construction and provider JSON decoding remain outside this package.

`validate()` is the Tool admission boundary: it rejects structurally valid
arguments that the particular Tool does not support by raising
`ToolInputError`. `ToolRunner` calls validation before execution, so rejected
input does not enter the Tool. A Tool whose domain accepts every valid argument
may intentionally have no additional semantic rejection.

## Execution

```python
runner = ToolRunner()
result = await runner.execute(tool, arguments)
```

`ToolRunner` is stateless. It validates once, executes once, and returns the
raw Tool-defined result without wrapping it. Ordinary Tool exceptions and
`asyncio.CancelledError` propagate unchanged. The runner provides no retry,
timeout, policy, registry lookup, execution identity, persistence, lifecycle
events, instrumentation, or provider translation.

## CommandTool

The first concrete experimental bridge is available only from its submodule:

```python
from devtools.tools.command import CommandTool
```

`CommandTool` accepts an existing immutable `Command`, delegates to a supplied
`CommandExecutor`, and returns the exact `CommandResult`. Commands remains an
independent subprocess-execution domain: nonzero exit codes remain normal
`CommandResult` values, and existing Command errors and cleanup semantics pass
through unchanged.

## ReadRepositoryFileTool

The second concrete experimental bridge is available only from its submodule:

```python
from devtools.tools.filesystem import ReadRepositoryFileTool
```

`ReadRepositoryFileTool(root)` is a configured read-only capability over the
existing Filesystem domain. It accepts an existing `ResolvedPath`, admits only
paths at or below its configured root, and returns the existing rich `File`
model produced by `devtools.filesystem.read()`. A path outside that configured
Tool scope raises `ToolInputError`; admitted missing paths, directories,
unsupported formats, size limits, permission failures, and codec failures
remain Filesystem-domain behavior.

The root is Tool-domain scope, not authorization or a secure filesystem
sandbox. It does not claim symlink confinement, TOCTOU protection, or a policy
about which caller may read a file. The Tool delegates directly to the existing
synchronous bounded Filesystem read beneath its async method; it does not
promise non-blocking execution or in-flight cancellation. It adds no timeout,
retry, Tool identity, result wrapper, registry, persistence, or instrumentation.

## ListRepositoryDirectoryTool

The bounded directory-enumeration capability is also available only from its
submodule:

```python
from devtools.tools.filesystem import ListRepositoryDirectoryTool
```

`ListRepositoryDirectoryTool(root)` accepts an existing `ResolvedPath`, admits
only paths at or below its configured root, and returns ordered direct-entry
names and kinds in a `RepositoryDirectoryListing`. It is non-recursive and
returns at most 64 entries by default; `truncated` explicitly records omitted
entries. It rejects paths outside its configured scope with `ToolInputError`.
Missing paths, non-directories, permission failures, and filesystem behavior
otherwise remain Filesystem-domain behavior.

Like `ReadRepositoryFileTool`, its root is scope rather than a hardened
sandbox: it does not claim symlink confinement or TOCTOU protection. It adds
no repository inventory, search, ranking, registry, persistence, or Tool
instrumentation.

## Boundaries

Tools do not change Context, Interaction, Runtime, Attempt, Evidence, Persistence, or
Commands. A Tool used inside an Interaction remains inside Runtime's existing
`INTERACTION_INVOCATION` boundary; it creates no child Attempt, Tool Evidence, Tool
Message, or Tool-specific Runtime stage.

Not implemented: registry/catalog lookup, ToolId or invocation identity,
provider Tool-call DTOs or schemas, retry, generic timeout, authorization,
side-effect metadata, Tool persistence, Tool Evidence, instrumentation,
ExecutionScope, transport, or MCP integration.
