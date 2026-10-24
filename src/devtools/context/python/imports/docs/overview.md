# Static Python import RI

`derive_python_import_declarations` retains every alias from direct module-body
`Import` and `ImportFrom` statements, with exact source spans, ordinals, aliases,
relative levels, repository/snapshot/resource and derivation identity. Coverage
is exhaustive for `Module.body` only; conditional, nested and dynamic imports
are outside it. Syntax alone asserts no target or binding.

`resolve_python_import_declaration` resolves the eligible module portion within
an explicit module interpretation universe. It preserves resolved,
unresolved-in-universe, ambiguous and unsupported outcomes. Absolute names have
no source-root precedence; relative names require one source interpretation and
cannot escape its package. `from . import X` resolves the source package, not an
inferred X submodule. Package modules and ordinary modules retain their exact
observed resource ownership. This is neither runtime importability nor an
assertion about the imported member.

`derive_python_resolved_module_import_relations` consumes declarations,
resolutions and one available source interpretation. Each uniquely resolved
declaration establishes a directed `PythonResolvedModuleImportRelation` with
exact source, resolution and target. Repeated declarations stay distinct;
nonpositive resolutions and unavailable/ambiguous sources establish no relation.
The relation is qualified repository import truth, independent of task relevance
and runtime dependency. Its derivation dependencies are distinct from the
represented source-to-target repository relationship.

`resolve_python_imported_member` separately resolves an imported member through
exactly one direct facade import binding to a direct function declaration. It
retains source/facade/target analyses, resolution results, competing bindings and
unsupported reasons. Star or nested facade imports, competing bindings,
ambiguous modules and recursive facades prevent positive selection. Direct
function/class binding lookup lives in modules RI and is also consumed by
Reference RI; its decorator and namespace guards differ from source-declaration
grounding. None of these operations establish public exports or `__all__` truth.

Facade pattern captures (including starred and mapping-rest names) and exception
aliases are competing module-scope syntax. The shared module binding-name
extractor excludes nested function/class namespaces; support is anchored to the
containing facade statement. Captures and handler aliases have different runtime
lifetimes; this resolver conservatively refuses competing names on either side
of the import and performs no later-use execution analysis. Unrelated and local
names do not compete. Canonical module lookup also guards facade namespace
uncertainty and the final target binding: a syntactic function declaration alone
cannot establish a reexport after rebinding or an unknown decorator. Such target
uncertainty is ambiguous; its declaration syntax and native analysis remain
available. The one-facade target contract remains direct functions (sync/async),
not a new class-reexport or recursive import capability. Direct class lookup is
unchanged.

The [Localization adapter](../../../localization/docs/overview.md#direct-static-python-import-dependency-resources)
consumes only the existing directed module-import relation for one forward step.
Its dependency candidate is the exact imported module's resource, including for
imported-member syntax. It excludes star declarations, does not claim member
resolution and does not follow facade chains or recursively expand target
imports. Frozen inputs and canonical native replay establish provenance;
candidate use, branching and work/result bounds belong to Localization.
Python RI has no dependency on Localization.
