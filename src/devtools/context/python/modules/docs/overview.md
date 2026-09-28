# Explicit-root Python modules and immediate package membership

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
