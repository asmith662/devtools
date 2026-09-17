# `devtools.tools`

## Status

The current Tool protocol, `ToolRunner`, and adapters are implemented but
experimental and unfrozen mechanisms. They implement the established narrow
Tool boundary; they do not establish a reusable Agent Tool loop, authorization
system, Action framework, or general orchestration.

This package owns typed reusable capability boundaries. A `Tool` defines a
name, description, typed input validation, and asynchronous execution;
`ToolRunner` validates and executes one Tool. The package currently includes
bounded command and repository-filesystem Tools.

Tools may adapt lower-level Resources such as
`devtools.resources.filesystem` and `devtools.resources.commands`, but a
Resource is not a Tool. Tool validation is not authorization. A Tool does not
make itself model-visible, parse an Action proposal, decide permission, or
project its result into a Prompt; those are separate caller responsibilities.

`ReadRepositoryFileTool` preserves generic Filesystem format inference for
recognized structured formats. For an unclassified repository extension, it
uses the same bounded Filesystem text-decoding path, allowing ordinary source
and configuration text without assigning a FileFormat per language. Undecodable
content still fails through the Filesystem text-decoding boundary.

ToolRunner's scope is one Tool execution, not generic execution lifecycle,
orchestration, observability, governance, or persistence.

`ToolDescriptor` is an explicit disclosure value. The Qwen composition seam
`experiments.qwen.model_tool_composition.normalize_tool_descriptor` crosses
from this tools-owned representation into the models-owned
`ModelToolDefinition`; disclosure does not execute, validate, authorize, or
implicitly expose a Tool.
