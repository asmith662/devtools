# Python function knowledge and bounded Context disclosure

`devtools.context.python.function` derives source-grounded direct module-body
function declarations from explicitly observed repository resources. Exact-name
retrieval over supplied declaration knowledge remains a separate, narrow path:
its existing disclosure selects every exact-name match, materializes exact
source from a supplied snapshot, renders it, and can place the result after a
caller's task in a copied `ModelRequest`.

The qualified-reference path accepts one **caller-chosen**
`PythonFunctionReferenceKnowledge` from a supplied
`PythonFunctionReferenceAnalysis`, plus an explicit purpose. It does not find,
rank, or choose a fact. Call `disclose_python_qualified_reference`, then
`materialize_python_qualified_reference_source` with the retained
`RepositorySnapshot`, then `render_python_qualified_reference_context`.
`assemble_python_qualified_reference_model_request` places that rendered
Context after the unchanged task while preserving the other request fields.

Materialization checks fact membership and derivation, the source resource
dependency, the target declaration's snapshot and subject dependency, and the
qualified import-resolution support against the supplied snapshot. It rejects
missing, stale, or redirected resources. Both source ranges are checked using
one-based lines and zero-based UTF-8 byte columns with exclusive ends. Exact
text comes only from retained snapshot contents; no working-tree file is read.
An invalid dependency or range fails observably. There is no whole-file
fallback.

The rendered relationship is distinct from the exact source text. The source
span is the qualified `ast.Name` occurrence, not a complete call expression.
`direct_call=True` means that Name occupies `ast.Call.func`; it is not a
runtime invocation claim. The target span is the established direct module-body
function declaration, not an assertion about decorators, surrounding source,
or all definitions. Reference analysis is non-exhaustive; one rendered fact
does not claim complete repository coverage. Resource addresses and locations
are navigation pointers to the identified snapshot state.

This is Context disclosure from an explicitly resolved RI fact. It neither
changes Retrieval nor establishes a general resource-Selection subsystem,
sufficiency decision, summary policy, or progressive controller.
