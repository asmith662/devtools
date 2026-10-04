# Explicit-root Python modules and immediate package membership

`lookup_python_modules(universe, dotted_name)` owns bounded exact dotted-name
lookup. It retains every match in supplied universe order, with no root
precedence, member lookup, runtime discovery or new import declaration.
Import resolution uses this shared operation with unchanged outcomes and order;
the [project configuration package](../../project_configuration/docs/overview.md)
uses it for Coverage module alternatives, preserving competing interpretations.

`devtools.context.python.modules` interprets caller-selected observed `.py`
resources under one explicit repository-relative `PythonModuleRoot`. An
ordinary module and an `__init__.py` package module have distinct
`PythonModuleKind` values. Each interpretation retains its exact repository,
snapshot, resource occurrence, content identity, root, dotted name, and kind.
The interpretation analysis also preserves excluded selected resources and
their reasons. It does not infer source roots or namespace packages.

`derive_python_immediate_package_memberships` consumes one such analysis and
its matching `RepositorySnapshot`. For a child interpretation named `P.C`, it
establishes one `PythonImmediatePackageMembership` only when exactly one
observed `PACKAGE` interpretation named `P` occurs in that same explicit-root
selection. The fact retains the child and package interpretations and an
identified derivation. The relation is immediate only. The same fact answers
both “which immediate package contains this module?” and “which observed
modules are immediate members of this package?” through local typed queries.
The interpreted modules are the typed endpoints; this slice does not invent a
parallel RepositorySubject or a SourceOccurrence span for a whole module.

Each selected interpretation receives an assessment: established, no parent
component, missing observed package, parent name represented only by a
non-package module, or ambiguous package interpretations. Competing package
interpretations are retained; none is chosen by order. Excluded selected
resources remain available separately. Coverage accounts for the supplied
selection only. Missing means no eligible parent was in that selection, not
that no such package exists in an unobserved part of the repository.

Membership does **not** imply Python runtime importability, execution,
dependency, an Imports relation in either direction, transitive containment,
namespace-package behavior, retrieval relevance, or Context selection. It
does not read new files or create a graph/tree abstraction.
## Direct binding lookup

`lookup_python_module_declaration` finds one uniquely supported, undecorated
direct module-body function or class declaration by name within an explicitly
observed module. The result retains both declaration analyses and an outcome
for unresolved, ambiguous, or non-declaration bindings. It combines native
declaration analyses with a conservative static binding check: decorators, competing bindings, wildcard imports and dynamic namespace
syntax can prevent selection of a declaration target. It does not execute
imports or establish runtime attribute identity.
Directness is relative to this module. Class-base and Reference resolution
consume the same operation without duplicating its binding policy.


## Exact source declaration selection

`modules.selection.select_python_module_source_declarations` answers which
native direct source declarations match this exact interpreted module,
`PythonSourceDeclarationKind` (CLASS or FUNCTION), and identifier name.
It validates repository/snapshot/resource state and consumes canonical class
and function declaration RI, with no parallel parser or binding-policy flag.
`PythonModuleSourceDeclarationSelection` retains the module, name/kind, both
native analyses (derivation, dependencies and coverage), and all matching native
knowledge values. Its `SEMANTICS` identifies this operation. It introduces no
new declaration subject or persistence representation.

Direct decorated ClassDef, FunctionDef and AsyncFunctionDef remain source
facts. Rebinding, assignments, imports and dynamic namespace syntax do not
erase those facts or create additional direct source declarations. Repeated
same-kind names have distinct native subjects and are all retained; source
order is never a uniqueness rule. Kind mismatch and no supported direct syntax
return no matches, including nested/control-flow declarations outside RI scope.
A native parse failure propagates without positive facts or successful coverage.

This selection establishes static repository/source declaration identity only.
It does not establish the module attribute or imported object after decorators,
descriptors, metaclass behavior or rebinding, public exports, callability or
runtime importability. Binding-oriented References and class-base resolution
continue using `lookup_python_module_declaration` with its unchanged guards.
Localization exact declaration grounding consumes this source selection.
