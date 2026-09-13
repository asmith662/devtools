# `devtools.tools`

This package owns typed reusable capability boundaries. A `Tool` defines a
name, description, typed input validation, and asynchronous execution;
`ToolRunner` validates and executes one Tool. The package currently includes
bounded command and repository-filesystem Tools.

Tools may adapt lower-level Resources such as
`devtools.resources.filesystem` and `devtools.resources.commands`, but a
Resource is not a Tool. Tool validation is not authorization. A Tool does not
make itself model-visible, parse an Action proposal, decide permission, or
project its result into a Prompt; those are separate caller responsibilities.

ToolRunner's scope is one Tool execution, not generic execution lifecycle,
orchestration, observability, governance, or persistence.
