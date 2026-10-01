# Bounded Python declaration References and direct Call syntax

Repository Intelligence (RI) derives exact `ast.Name` and outermost
`ast.Attribute` load occurrences from retained snapshot content. Each positive
`PythonDeclarationReferenceKnowledge` identifies an observed source occurrence,
a supported target function, class, or direct method declaration, its exact
target resource, a resolution route, and native support. The source span covers
the whole resolved expression (`pkg.mod.f`, not only `f`). Its structural
subject is the declaration's existing subject; display names are not identity.

`derive_python_declaration_references` is the sole active Reference derivation.
It requires a caller supplied module interpretation universe and, for relative
imports, source interpretations. It never reopens the working tree. The older
function-only fact value classes remain importable solely so frozen development
archives can be replayed; the old function-only derivation is gone.

## Supported resolution

- A unique, undecorated direct module-body function or class binding may be
  referenced in its own module. Its binding must be unambiguous; a module-body
  use before that binding is not resolved.
- A named `from module import member` binding may target a direct supported
  function or class. The existing one-facade imported-function route remains
  available. Import declaration, module resolution, and direct-member or facade
  support are retained independently of the Reference.
- `import module` and `import module as alias` can support a directly contained
  function or class via a complete static module-qualified attribute chain.
- A statically identified supported class can support a direct method target
  (`Class.method`, including an imported or module-qualified class) when the
  class body has one unambiguous direct method binding of that name. Its
  containing class is retained. No inherited dispatch is inferred.

Direct module declaration lookup belongs to Python module interpretation. It
uses function and class declaration analyses and rejects competing bindings,
unsupported declarations, wildcard imports, and dynamic namespaces. Directness
is relative to the observed module, not a context-free property of a symbol.

`direct_call=True` means only that the resolved Name or Attribute expression
occupies `ast.Call.func`. It neither proves runtime invocation nor class
construction, descriptor behavior, or dispatch. An imported class in `C()` is
therefore a class Reference tagged with direct Call syntax.

Every assessed candidate retains an outcome, including unresolved binding,
ambiguous binding, unsupported scope/expression/receiver, shadowed binding,
unresolved module/member, and unsupported declaration target. Coverage is
non-exhaustive. Rebinder, decorator, wildcard, dynamic-namespace, nested-scope,
and arbitrary receiver cases yield no positive assertion when static evidence
does not establish a unique target. `self.m()`, `cls.m()`, and `obj.m()` are not
resolved by guessed receiver type. `global`, `nonlocal`, runtime mutation,
descriptor execution, and general Python import execution are outside this
contract.

The package retains syntax, declaration, import, and module provenance. It
does not select retrieval candidates, assign relevance, choose Context
disclosure, or assert a runtime call graph. Retrieval may project these facts
to resource edges; Context Planning may disclose an explicitly chosen fact
using retained source spans. Personalized PageRank (PPR) and Reciprocal Rank
Fusion (RRF) remain separate Retrieval mechanisms.
