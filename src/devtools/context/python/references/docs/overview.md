# Bounded Python function References and direct Calls

`devtools.context.python.references.derive_python_function_references` derives
source-grounded Repository Intelligence from one already observed Python resource
in a `RepositorySnapshot`. The caller supplies an explicit module interpretation
universe and, for relative imports, the source interpretations. The operation
does no filesystem acquisition or module-root discovery.

A `PythonFunctionReferenceKnowledge` value means that a specific `ast.Name`
read is conservatively bound by one direct module-body named `ImportFrom` alias
to an existing direct module-body Python function declaration. Its
`PythonSourceOccurrence` retains the exact snapshot, address, and AST UTF-8 byte
span. The target is the existing `PythonFunctionDeclarationKnowledge` and
`PythonFunctionSubject`, not a new symbol identity. The import declaration,
qualified module resolution, imported-member resolution, and direct-module or
one-facade route remain available as native support. The derivation identity
depends on the observed source, explicit universe, supplied source
interpretations, and versioned semantics; each reference has a separate
reproducible identity.

`direct_call=True` means this *same* qualified Name node occupies
`ast.Call.func`. It is not a second independent relation. It does not assert
that Python executed the call, identify an enclosing caller function, resolve
methods, or establish a function-to-function call graph. A non-call Name read
is still a Reference.

The analyzer accepts either a unique direct function in the imported module
or the existing production one-facade imported-member resolution. It rejects
competing module bindings, star imports, unresolved or ambiguous module/member
targets, dynamic namespace calls, shadowed uses, and class/comprehension scope
uses. It does not guess runtime binding, dispatch, object attributes, `__all__`,
or general Python name resolution. A reported unsupported binding is a
coverage/uncertainty observation, never a negative Reference assertion.
`PythonFunctionReferenceCoverage.IS_EXHAUSTIVE` is always false: zero returned
references does not mean no reference or call exists. Annotation and other
unsupported evaluation contexts are not claimed as covered.

This package contains repository facts only. It has no retrieval candidate,
ranking, usefulness judgment, Context disclosure, or model behavior.
The Python function Context package may consume an explicitly chosen positive
Reference fact through its bounded disclosure or a common DisclosurePlan
adapter. That consumer does not change this package's knowledge or coverage.
