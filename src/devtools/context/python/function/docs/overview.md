# Python function knowledge and bounded Context disclosure

`devtools.context.python.function` derives source-grounded direct module-body
function declarations from explicitly observed repository resources. Exact-name
retrieval over supplied declaration knowledge remains a separate, narrow path:
its existing disclosure selects every exact-name match, materializes exact
source from a supplied snapshot, renders it, and can place the result after a
caller's task in a copied `ModelRequest`.

## Direct declaration containment

Declaration ownership was already intrinsic to production knowledge: each
`PythonFunctionDeclarationKnowledge` retains an exact source occurrence with
the resource address and span, while its subject binds to the derivation's
observed resource dependency. This increment adds a validated navigation view,
not a second `ResourceOwnsFunction` fact. Build
`PythonFunctionDeclarationContainmentView` with
`build_python_function_declaration_containment_view(snapshot, aggregate=...)`
over existing per-resource analyses. The builder checks repository, snapshot,
observed resource/content, derivation, coverage, subject, ordinal, and support
consistency without reparsing or reopening the working tree.

`direct_declarations_in(address)` returns the supported direct module-body
function and async-function declarations in source order; an analyzed resource
with none returns an empty tuple. An address absent from the selected analyses
raises an error because that selection cannot establish absence.
`containing_resource_of(declaration)` returns the exact observed resource for
a declaration in the analyses. The two directions navigate one existing
declaration proposition. Each analysis retains its own derivation and bounded
exhaustive coverage; the view creates no aggregate derivation or new identity.

```text
observed resource
  ├── direct module-body FunctionDef
  └── direct module-body AsyncFunctionDef
```

Decorated direct FunctionDef and AsyncFunctionDef have the same supported
source-declaration status as plain declarations. The exact source selector in
[modules](../../modules/docs/overview.md#exact-source-declaration-selection)
retains native identities and provenance without establishing post-decoration
binding values, imported object identity or callability.

The occurrence belongs to the resource and is directly in `Module.body` under
the current parser contract. This says nothing about runtime ownership,
importability, public API status, usefulness, or graph importance. Class,
method, nested-function, lambda, and assignment declarations are outside this
contract. A later class/method model can distinguish occurrence resource from
direct lexical parent declaration without changing this view's narrow claim.

Repository Intelligence answers which supported declaration is structurally
contained where. Retrieval decides whether that structure is evidence relevant
to an InformationNeed. Context Planning decides which declaration or resource
information to disclose. The current qualified-reference Context materializer
already uses the declaration's exact resource dependency and source span; it
does not need a new ownership fact. This view is not automatically projected
into the current resource-level Personalized PageRank graph.

## Context disclosure

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

choose_python_qualified_reference_disclosure now adapts this same validated
path to the common
[DisclosurePlan](../../../planning/docs/overview.md) boundary. A caller can
place it beside other explicit representations, including a retained whole
resource. The adapter calls the existing materializer and renderer; it does
not weaken their snapshot, content, or Reference/Call semantics. The original
narrow API remains available unchanged.
