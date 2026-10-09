# U2 native exact-capability inventory

Inspected before policy construction at source checkpoint
`0c0029a2d608bafe95c6792fe04b4127e17f0304`. This is capability inspection,
not Case 0012 resolution or prospective effectiveness evidence.

| Native owner / mechanism | Accepted input and native output | Uniqueness, ambiguity, unsupported scope | Frame/provenance and U2 admission |
| --- | --- | --- | --- |
| repository.resource.RepositoryResourceAddress; RepositorySnapshot.resource_at | Canonical relative POSIX address → retained resource occurrence | Exact single address; absent address raises ValueError. No basename, glob or fuzzy expansion | Snapshot and content identity; U2 checks frame uniqueness/content and maps absence to UNRESOLVED. RESOURCE_ADDRESS admitted |
| python.modules.interpretation; lookup_python_modules | Explicit root and selected observed .py resources; exact dotted name → all matching interpretations | Ordinary/package distinguished; duplicate dotted names retained, no root precedence. No root discovery, namespace packages or runtime importability | Native repository/snapshot/resource/content/root and interpretation identity. PYTHON_MODULE admitted only with frozen universe |
| python.modules.selection.select_python_module_source_declarations | Interpreted module, exact name, CLASS/FUNCTION → all native direct declarations and both analyses | Decorated source declarations remain facts; repeated declarations remain distinct. Nested/control-flow syntax outside direct scope. Parse failure propagates | Snapshot equality, derivation/dependencies/coverage retained. PYTHON_DIRECT_CLASS and PYTHON_DIRECT_FUNCTION admitted; source identity, not post-decoration binding |
| python.classes declarations and containment; grounding direct-method adapter | One native direct class plus exact method name → native direct class-body methods | No inherited/dynamic/instance method lookup. Duplicate parent or method remains ambiguous | Parent validated against fresh native analysis. PYTHON_DIRECT_METHOD admitted as bounded class source selection followed by native containment; no guessing parent |
| python.function.retrieval exact declared-name acquisition | Explicit established declaration knowledge + exact function name → all matching evidence; resource projection retains all support | Unqualified function matches are bounded to supplied knowledge, not global uniqueness; same-resource multiple declarations remain distinct | Original native knowledge/support/snapshot; safe only with predeclared complete analysis selection. Deferred in U2 v1: avoid a broad pre-analysis scan and an alternate bare-name route |
| localization.grounding AnchorGrounding | Explicit task anchor, frame, typed locator, optional native module universe → disposition/candidates/evidence | RESOLVED one; AMBIGUOUS preserves competition; UNRESOLVED bounded miss; UNSUPPORTED no applicable contract/parse. No task-text interpretation | Validates task, snapshot and native module universe; native provenance retained. U2 delegates to this adapter rather than duplicating exact RI |
| python.modules.declarations direct binding lookup | Interpreted module + exact name → unique conservative binding/declaration account | Decorators, rebinding, wildcard/dynamic syntax can block selection. Distinct from static source selection | Both native analyses and binding qualification; deferred because U2 v1 locates source declarations, not runtime objects |
| python.imports resolution/relations | Native Import syntax + explicit module universe → bounded resolutions and uniquely established directed relations | Module resolution does not establish member exports; ambiguous/unresolved/unsupported/source-unavailable do not yield relations | Source/target interpretations and native derivation. Not a task-hint route in v1 |
| python.imports.members | Direct ImportFrom member plus explicit universe → bounded one-facade direct function resolution | Exactly one direct facade binding; no recursive facade, wildcard, class/member generalization or __all__ guarantee | Source/facade/target module/declaration provenance. Deferred: task string is not a native imported-member occurrence |
| python.references | Native source occurrence + explicit analyses → qualified Reference/Call facts | Bounded same-module/import/module/class-qualified routes, non-exhaustive; no general semantic resolver | Native occurrence/target/support. Deferred: no Reference occurrence is invented from task prose |
| public package facades | Native package modules/import syntax are inspectable resources | Public name does not imply direct declaration, runtime export or defining owner | Exact package module may route as module; imported public object must remain unsupported/unresolved unless a separate native binding contract is supplied |

Source and test evidence: `src/devtools/context/repository/{resource,snapshot}.py`,
`src/devtools/context/python/modules/{interpretation,lookup,selection,declarations}.py`,
`src/devtools/context/python/classes/{declarations,containment}.py`,
`src/devtools/context/python/function/retrieval.py`,
`src/devtools/context/python/imports/{resolution,relations,members}.py`,
`src/devtools/context/python/references/docs/overview.md`,
`src/devtools/context/localization/grounding/{contract,resolve,view}.py`,
`tests/context/python/modules/test_selection.py` and the package contracts linked
by `docs/documentation_map.md`. Existing Case 0011 exact-hint diagnostics motivate
the question but are not Case 0012 answers or extractor defaults.

No universal identifier/entity resolver is available or introduced. Unqualified
class/function/method names, runtime attributes, aliases, wildcards and semantic
references are retained as unsupported under v1. Ambiguous and unsupported
requests do not promote a resource even when all referents share one owner.

Experimental frame authentication consumes the canonical observation module's
length-framed content-identity helper rather than independently implementing a
raw SHA-256 content identity. That private-helper coupling is explicitly pinned
in the implementation seal; it is not a promoted public API. Native snapshot
and module contracts plus committed-byte reconstruction validate the frame.

U2 owns task-relative syntactic observations, associations, route composition,
presentation and experiment trace only. Dependencies flow experiments → devtools;
RI, Retrieval and Localization acquire no dependency on this package. Native
grounding supplies candidates, never relevance, witnesses, satisfaction or readiness.
