# Independent C-R semantic adjudication — Case 0012

This is a task/repository-information adjudication over the supplied sealed packet. It does not implement the feature or execute repository validation commands. Scientific resource IDs below are packet-order aliases; exact native identities and addresses remain bound in JSON.

## Packet authentication

Initial workspace: exact five-file whitelist; no directories, .git, .local, symlinks, junctions or reparse points. `python -B validate_packet.py` exited 0 with `VERIFIED; NO ADJUDICATION`. All five original input byte seals are retained in the review and rechecked on replay.

Case: `case-0012`; task: `case-0012-direct-source-disclosure`.

| Input | SHA-256 |
|---|---|
| README.md | `b33c456f8999b4343d6dbe59c311c7866ae681668c9415f4042d8ced231cf7be` |
| integrity.json | `89947624937675a94d6228e3c6fc6c206bc929600b4f21faf2f5cf22bf78a6f9` |
| manifest.json | `15c886a8af33bf2ba12c2a92e82ec3a33789a605064bded6f17ae4b603d579cf` |
| resources.json.gz | `2cbc95afb120c920ed8d919e37a187f8fe0eec4618eff28eb25203d108599fe3` |
| validate_packet.py | `f6d1ec7068ac1a86beabaebf0f76b24df919ba2662ae54c8a40df0e92416a1ca` |

Canonical payload SHA-256: `c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce`.

## Exact task

```text
Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.
Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.
Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.
Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.
Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.
Preserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.
Expose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.
Add focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.
Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.
Validate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.
```

## Frozen obligations and applicability

| Obligation | Applicability | Exact statement | Exact satisfaction criterion |
|---|---|---|---|
| source | APPLICABLE | Establish supported direct function/class source selection and native direct-method containment, with source/binding scope distinctions. | Complete native selection/containment contracts and unsupported runtime/import/inherited/semantic boundaries are established. |
| choices | APPLICABLE | Establish explicit immutable ordered Context Planning choice integration and compatibility. | Purpose, frame, ordered choice invariants, admission and existing qualified-reference/whole-resource compatibility are established. |
| integrity | APPLICABLE | Establish native frame/content/declaration validation before disclosure publication without reacquisition. | Foreign/stale/content/missing-resource/scope/returned-identity checks and publication ordering are established. |
| materialization | APPLICABLE | Establish exact source-segment materialization, provenance, UTF-8 boundaries and faithful mixed-plan order. | Source-range, derivation, owner provenance, decorators, CRLF/non-ASCII and ordered mixed representations are established without implicit expansion or sufficiency. |
| assembly | APPLICABLE | Establish unchanged rendering and copied-request semantics without new budgets. | Original fields/tools and prompt role, task-before-Context copying, rendering compatibility and absence of truncation changes are established. |
| exports | APPLICABLE | Establish common planning and outer facade exports and permitted dependency ownership. | Both public boundaries and absence of Retrieval/language-specific common assembly dependencies are established. |
| tests | APPLICABLE | Establish focused and regression test conventions for every new and preserved contract. | Direct/decorated/repeated declarations, mixed exact provenance, rejection, old choices and copied-request preservation tests are established. |
| documentation | APPLICABLE | Establish package and architecture documentation to update with supported/deferred source-disclosure scope. | Source versus runtime binding, explicit admission, compatibility and no automatic relevance/readiness claims are documented. |
| validation | APPLICABLE | Establish the complete protected validation/tooling contract and preserved configuration. | Protected development entry/scope and pytest/coverage retention, Ruff lint/format, strict mypy, worktree/index checks and excluded confirmation boundary are established. |

All nine clauses are mandatory and unconditional. The exact frozen applicability text, identities and task-basis offsets are preserved in JSON.

## Task-clause coverage

All 10 task sentences and every listed substantive subclause are covered. The validation criterion's excluded-confirmation boundary is an operational validation restriction, not an added software feature. Packet/operator instructions are not feature semantics.

| Clause | Obligations | Substantive requirements, each adequately covered | Evidence |
|---|---|---|---|
| C01 | source, choices | caller-selected direct Python source choices; common planning integration alongside qualified-reference/whole-resource choices; no automatic retrieval or selection | E0001 |
| C02 | source | reuse the exact named native selector; direct function/class source identities; method only through validated native class parent and containment; exclude runtime attributes, imported facades, inherited methods and semantic resolution | E0002 |
| C03 | choices | integrate DisclosurePlan and common planning module; retain immutable purpose/frame/ordered-choice contracts; preserve existing choices | E0003 |
| C04 | integrity | validate every supplied native declaration/resource; use retained RepositorySnapshot.resource_at; reject foreign/stale frame and content; reject missing resource; reject unsupported declaration scope; reject mismatched returned identity before publishing; no reacquisition | E0004 |
| C05 | materialization | exact declaration source segment in ContextDisclosure; native derivation/source-range/owner provenance; UTF-8 boundaries; decorators; CRLF and non-ASCII bytes; mixed caller order; no sufficiency inference; no implicit whole-owner expansion | E0005 |
| C06 | assembly | preserve common rendering; copy ModelRequest and leave original unchanged; preserve role/settings/conversation/provider settings/tools except copied prompt; task before Context; no new budget or truncation | E0006 |
| C07 | exports | common planning public API; outer Context facade; dependency direction; no Retrieval dependency; no language-specific common assembly | E0007 |
| C08 | tests | direct function/class/method tests; decorated and repeated tests; mixed order and exact source/provenance tests; stale/foreign/missing-resource rejection tests; existing-choice regression; copied-request preservation regression | E0008 |
| C09 | documentation | both exact named documentation destinations; source identity versus runtime bindings; explicit representation admission; supported/deferred scope; compatibility; no automatic relevance/readiness claim | E0009 |
| C10 | validation | named validation entry point; preserve pyproject test/coverage settings; documented protected development profile; Ruff lint/format; strict mypy; both worktree and index whitespace checks | E0010 |

## Complete cell counts

Exactly 531 × 9 = 4,779 cells; no omissions or duplicates. Every cell, including UNNECESSARY cells, has an obligation-relative semantic rationale in JSON.

| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | UNRESOLVED |
|---|---:|---:|---:|---:|
| source | 5 | 16 | 510 | 0 |
| choices | 1 | 13 | 517 | 0 |
| integrity | 8 | 18 | 505 | 0 |
| materialization | 5 | 17 | 509 | 0 |
| assembly | 1 | 13 | 517 | 0 |
| exports | 0 | 10 | 521 | 0 |
| tests | 1 | 31 | 499 | 0 |
| documentation | 0 | 18 | 513 | 0 |
| validation | 2 | 4 | 525 | 0 |
| **Total** | 23 | 140 | 4616 | 0 |

## Positive resources: source

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0050 | The architectural native-function/class account corroborates distinct subjects, source occurrences, direct scope and class-parent containment. It does not state every concrete identity/dependency field required by the complete native contract and therefore does not substitute for those narrower sources. |
| R004 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md |  | E0051 | The architecture explains identity/occurrence and derivation distinctions at a broader level. Native declaration contracts and the task establish the bounded facts needed here without requiring the full architectural framework. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R099 | HELPFUL_ONLY | src/devtools/context/localization/grounding/resolve.py |  | E0024, E0059 | Existing method/declaration grounding is a concrete consumer example of native source selection and validated parent containment. Canonical analysis membership and the native parent link already establish the necessary information in every minimal integrity alternative, so this consumer is corroboration rather than an additional prerequisite. |
| R129 | HELPFUL_ONLY | src/devtools/context/python/classes/containment.py |  | E0022, E0023 | The validated view is a useful direct-containment API and test example. Its necessary membership/parent information is already available from the complete canonical declaration contract; validating supplied native identities does not require one particular view implementation in addition to canonical replay/equality. |
| R130 | REQUIRED | src/devtools/context/python/classes/declarations.py | U04, U05 | E0016, E0017, E0018, E0019 | This resource establishes U04, U05. It is an indispensable member within at least one complete minimal alternative (source-A1, source-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R131 | REQUIRED | src/devtools/context/python/classes/docs/overview.md | U04, U05 | E0020 | This resource establishes U04, U05. It is an indispensable member within at least one complete minimal alternative (source-A3, source-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R135 | HELPFUL_ONLY | src/devtools/context/python/function/containment.py |  | E0065 | The function-containment view provides another validation/navigation example. Canonical selector replay plus exact native membership can satisfy the required checks without requiring this additional aggregate-view mechanism. |
| R136 | REQUIRED | src/devtools/context/python/function/declarations.py | U03 | E0013, E0014, E0015, E0035 | This resource establishes U03. It is an indispensable member within at least one complete minimal alternative (source-A1, source-A2, source-A3, source-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R153 | HELPFUL_ONLY | src/devtools/context/python/modules/declarations.py |  | E0071 | Binding lookup provides a useful contrast to source selection, retaining conservative decorated/rebound-target behavior. The task and native source selector already establish that this binding path must not be substituted. |
| R154 | REQUIRED | src/devtools/context/python/modules/docs/overview.md | U02 | E0012 | This resource establishes U02. It is an indispensable member within at least one complete minimal alternative (source-A1, source-A3); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R155 | HELPFUL_ONLY | src/devtools/context/python/modules/interpretation.py |  | E0072, E0073 | Module interpretation supplies useful fixture-construction and retained-resource context. The task accepts caller-supplied native declarations and the source selector already establishes the admitted module fields; no new module-discovery mechanism is required. |
| R158 | REQUIRED | src/devtools/context/python/modules/selection.py | U02 | E0011 | This resource establishes U02. It is an indispensable member within at least one complete minimal alternative (source-A2, source-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R172 | HELPFUL_ONLY | src/devtools/context/python/references/docs/overview.md |  | E0074 | The Reference documentation distinguishes bounded binding-based relations from direct source identity and helps explain compatibility. Source disclosure itself does not need Reference resolution. |
| R180 | HELPFUL_ONLY | src/devtools/context/repository/resource.py |  | E0029 | The immutable retained resource value is useful to construct source fixtures and understand owners. Source identity's native dependency fields and task scope can be established without separately requiring this resource for that obligation. |
| R181 | HELPFUL_ONLY | src/devtools/context/repository/snapshot.py |  | E0028 | The snapshot lookup is useful source/test setup context, with its necessary missing-resource contract separately established under integrity. |
| R387 | HELPFUL_ONLY | tests/context/python/classes/test_declarations.py |  | E0080 | Class/method tests demonstrate direct scope, native parent and decorator-keyword span boundaries. They corroborate rather than replace the complete native identity and validation contracts. |
| R390 | HELPFUL_ONLY | tests/context/python/function/test_containment.py |  | E0081 | Function-containment tests illustrate invalid aggregate/declaration support. Reusing this exact aggregate or fixture is not required for new direct choices. |
| R393 | HELPFUL_ONLY | tests/context/python/function/test_declarations.py |  | E0082, E0083 | Tests corroborate repeated native subjects and UTF-8 coordinates but do not supply a complete alternative for every native identity/provenance fact. |
| R409 | HELPFUL_ONLY | tests/context/python/modules/test_selection.py |  | E0090, E0091, E0092 | Selection tests demonstrate decorated/repeated source identity, negative kind/scope cases and foreign inputs. They are useful executable examples, but the complete selector contract also needs retained analyses and parse-failure behavior explicitly established elsewhere. |

## Positive resources: choices

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0049 | The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts. |
| R006 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md |  | E0052 | Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R120 | HELPFUL_ONLY | src/devtools/context/planning/__init__.py |  | E0060 | The planning initializer shows current public symbols and is useful for adding exports, but the existing option protocol and task-supplied public destinations establish the necessary contracts. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R122 | HELPFUL_ONLY | src/devtools/context/planning/materialization.py |  | E0032, E0031 | The result type and common materialization guards provide implementation and regression-test context for a new protocol participant; their necessity is charged to integrity/materialization rather than to a second invented choice-admission rule. |
| R123 | REQUIRED | src/devtools/context/planning/plan.py | U06, U07, U08 | E0025, E0026, E0027, E0044 | This resource establishes U06, U07, U08. It is an indispensable member within at least one complete minimal alternative (choices-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R125 | HELPFUL_ONLY | src/devtools/context/planning/resource.py |  | E0063, E0064 | The existing whole-resource option is a useful preserved-compatibility and retained-content validation example. It is not a mandatory template for a new direct-source representation or an implicit whole-owner fallback. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R140 | HELPFUL_ONLY | src/devtools/context/python/function/planned_reference.py |  | E0068 | The qualified-reference adapter is a concrete protocol example and compatibility reference. The new option can preserve it through the existing protocol without modifying or reproducing its internals. |
| R141 | HELPFUL_ONLY | src/devtools/context/python/function/qualified_reference.py |  | E0069 | The preserved qualified-reference path illustrates rechecking native membership and retained dependencies before exact extraction. Direct source declarations must not acquire its imported-reference semantics. |
| R172 | HELPFUL_ONLY | src/devtools/context/python/references/docs/overview.md |  | E0074 | The Reference documentation distinguishes bounded binding-based relations from direct source identity and helps explain compatibility. Source disclosure itself does not need Reference resolution. |
| R383 | HELPFUL_ONLY | tests/context/planning/test_plan.py |  | E0078, E0079 | Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested. |
| R396 | HELPFUL_ONLY | tests/context/python/function/test_qualified_reference.py |  | E0086, E0087 | Qualified-reference tests are useful compatibility examples of stale/redirected support and exact target preservation. Direct source disclosure can preserve the existing adapter without requiring these tests as semantic witnesses. |

## Positive resources: integrity

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0050 | The architectural native-function/class account corroborates distinct subjects, source occurrences, direct scope and class-parent containment. It does not state every concrete identity/dependency field required by the complete native contract and therefore does not substitute for those narrower sources. |
| R004 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md |  | E0051 | The architecture explains identity/occurrence and derivation distinctions at a broader level. Native declaration contracts and the task establish the bounded facts needed here without requiring the full architectural framework. |
| R099 | HELPFUL_ONLY | src/devtools/context/localization/grounding/resolve.py |  | E0024, E0059 | Existing method/declaration grounding is a concrete consumer example of native source selection and validated parent containment. Canonical analysis membership and the native parent link already establish the necessary information in every minimal integrity alternative, so this consumer is corroboration rather than an additional prerequisite. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R122 | REQUIRED | src/devtools/context/planning/materialization.py | U14 | E0031, E0033 | This resource establishes U14. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A2, integrity-A3, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R123 | HELPFUL_ONLY | src/devtools/context/planning/plan.py |  | E0025, E0026 | The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets. |
| R125 | HELPFUL_ONLY | src/devtools/context/planning/resource.py |  | E0063, E0064 | The existing whole-resource option is a useful preserved-compatibility and retained-content validation example. It is not a mandatory template for a new direct-source representation or an implicit whole-owner fallback. |
| R129 | HELPFUL_ONLY | src/devtools/context/python/classes/containment.py |  | E0022, E0023 | The validated view is a useful direct-containment API and test example. Its necessary membership/parent information is already available from the complete canonical declaration contract; validating supplied native identities does not require one particular view implementation in addition to canonical replay/equality. |
| R130 | REQUIRED | src/devtools/context/python/classes/declarations.py | U04, U05, U13 | E0016, E0017, E0018, E0019, E0021 | This resource establishes U04, U05, U13. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R131 | REQUIRED | src/devtools/context/python/classes/docs/overview.md | U04, U05, U13 | E0020 | This resource establishes U04, U05, U13. It is an indispensable member within at least one complete minimal alternative (integrity-A3, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R135 | HELPFUL_ONLY | src/devtools/context/python/function/containment.py |  | E0065 | The function-containment view provides another validation/navigation example. Canonical selector replay plus exact native membership can satisfy the required checks without requiring this additional aggregate-view mechanism. |
| R136 | REQUIRED | src/devtools/context/python/function/declarations.py | U03 | E0013, E0014, E0015, E0035 | This resource establishes U03. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A2, integrity-A3, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R139 | HELPFUL_ONLY | src/devtools/context/python/function/materialization.py |  | E0045, E0046 | The UTF-8 extractor is a useful canonical reuse candidate and supports the coordinate fact. Every minimal materialization alternative already needs the native function model, which supplies that coordinate fact; the algorithm's source is therefore not an additional necessary information member. |
| R141 | HELPFUL_ONLY | src/devtools/context/python/function/qualified_reference.py |  | E0069 | The preserved qualified-reference path illustrates rechecking native membership and retained dependencies before exact extraction. Direct source declarations must not acquire its imported-reference semantics. |
| R154 | REQUIRED | src/devtools/context/python/modules/docs/overview.md | U02, U13 | E0012 | This resource establishes U02, U13. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A3); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R155 | HELPFUL_ONLY | src/devtools/context/python/modules/interpretation.py |  | E0072, E0073 | Module interpretation supplies useful fixture-construction and retained-resource context. The task accepts caller-supplied native declarations and the source selector already establishes the admitted module fields; no new module-discovery mechanism is required. |
| R158 | REQUIRED | src/devtools/context/python/modules/selection.py | U02, U13 | E0011 | This resource establishes U02, U13. It is an indispensable member within at least one complete minimal alternative (integrity-A2, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R180 | REQUIRED | src/devtools/context/repository/resource.py | U11 | E0029, E0030 | This resource establishes U11. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A2, integrity-A3, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R181 | REQUIRED | src/devtools/context/repository/snapshot.py | U10 | E0028 | This resource establishes U10. It is an indispensable member within at least one complete minimal alternative (integrity-A1, integrity-A2, integrity-A3, integrity-A4); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R383 | HELPFUL_ONLY | tests/context/planning/test_plan.py |  | E0078, E0079 | Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested. |
| R387 | HELPFUL_ONLY | tests/context/python/classes/test_declarations.py |  | E0080 | Class/method tests demonstrate direct scope, native parent and decorator-keyword span boundaries. They corroborate rather than replace the complete native identity and validation contracts. |
| R390 | HELPFUL_ONLY | tests/context/python/function/test_containment.py |  | E0081 | Function-containment tests illustrate invalid aggregate/declaration support. Reusing this exact aggregate or fixture is not required for new direct choices. |
| R395 | HELPFUL_ONLY | tests/context/python/function/test_materialization.py |  | E0084, E0085 | Tests provide CRLF/non-ASCII and malformed-range examples for the existing function-only path; they do not prescribe a new direct-source API or solve decorator-inclusive provenance. |
| R396 | HELPFUL_ONLY | tests/context/python/function/test_qualified_reference.py |  | E0086, E0087 | Qualified-reference tests are useful compatibility examples of stale/redirected support and exact target preservation. Direct source disclosure can preserve the existing adapter without requiring these tests as semantic witnesses. |
| R409 | HELPFUL_ONLY | tests/context/python/modules/test_selection.py |  | E0090, E0091, E0092 | Selection tests demonstrate decorated/repeated source identity, negative kind/scope cases and foreign inputs. They are useful executable examples, but the complete selector contract also needs retained analyses and parse-failure behavior explicitly established elsewhere. |

## Positive resources: materialization

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0049 | The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts. |
| R004 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md |  | E0051 | The architecture explains identity/occurrence and derivation distinctions at a broader level. Native declaration contracts and the task establish the bounded facts needed here without requiring the full architectural framework. |
| R006 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md |  | E0052 | Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R122 | REQUIRED | src/devtools/context/planning/materialization.py | U15 | E0031, E0032, E0033 | This resource establishes U15. It is an indispensable member within at least one complete minimal alternative (materialization-A1, materialization-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R123 | HELPFUL_ONLY | src/devtools/context/planning/plan.py |  | E0025, E0026 | The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets. |
| R125 | HELPFUL_ONLY | src/devtools/context/planning/resource.py |  | E0063, E0064 | The existing whole-resource option is a useful preserved-compatibility and retained-content validation example. It is not a mandatory template for a new direct-source representation or an implicit whole-owner fallback. |
| R130 | REQUIRED | src/devtools/context/python/classes/declarations.py | U04, U05, U17 | E0016, E0017, E0018, E0019, E0037 | This resource establishes U04, U05, U17. It is an indispensable member within at least one complete minimal alternative (materialization-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R131 | REQUIRED | src/devtools/context/python/classes/docs/overview.md | U04, U05, U17 | E0020 | This resource establishes U04, U05, U17. It is an indispensable member within at least one complete minimal alternative (materialization-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R135 | HELPFUL_ONLY | src/devtools/context/python/function/containment.py |  | E0065 | The function-containment view provides another validation/navigation example. Canonical selector replay plus exact native membership can satisfy the required checks without requiring this additional aggregate-view mechanism. |
| R136 | REQUIRED | src/devtools/context/python/function/declarations.py | U03, U16, U17 | E0013, E0014, E0015, E0034, E0035, E0036 | This resource establishes U03, U16, U17. It is an indispensable member within at least one complete minimal alternative (materialization-A1, materialization-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R139 | HELPFUL_ONLY | src/devtools/context/python/function/materialization.py |  | E0045, E0046 | The UTF-8 extractor is a useful canonical reuse candidate and supports the coordinate fact. Every minimal materialization alternative already needs the native function model, which supplies that coordinate fact; the algorithm's source is therefore not an additional necessary information member. |
| R140 | HELPFUL_ONLY | src/devtools/context/python/function/planned_reference.py |  | E0068 | The qualified-reference adapter is a concrete protocol example and compatibility reference. The new option can preserve it through the existing protocol without modifying or reproducing its internals. |
| R141 | HELPFUL_ONLY | src/devtools/context/python/function/qualified_reference.py |  | E0069 | The preserved qualified-reference path illustrates rechecking native membership and retained dependencies before exact extraction. Direct source declarations must not acquire its imported-reference semantics. |
| R180 | REQUIRED | src/devtools/context/repository/resource.py | U11 | E0029, E0030 | This resource establishes U11. It is an indispensable member within at least one complete minimal alternative (materialization-A1, materialization-A2); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R383 | HELPFUL_ONLY | tests/context/planning/test_plan.py |  | E0078, E0079 | Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested. |
| R387 | HELPFUL_ONLY | tests/context/python/classes/test_declarations.py |  | E0080 | Class/method tests demonstrate direct scope, native parent and decorator-keyword span boundaries. They corroborate rather than replace the complete native identity and validation contracts. |
| R393 | HELPFUL_ONLY | tests/context/python/function/test_declarations.py |  | E0082, E0083 | Tests corroborate repeated native subjects and UTF-8 coordinates but do not supply a complete alternative for every native identity/provenance fact. |
| R395 | HELPFUL_ONLY | tests/context/python/function/test_materialization.py |  | E0084, E0085 | Tests provide CRLF/non-ASCII and malformed-range examples for the existing function-only path; they do not prescribe a new direct-source API or solve decorator-inclusive provenance. |
| R396 | HELPFUL_ONLY | tests/context/python/function/test_qualified_reference.py |  | E0086, E0087 | Qualified-reference tests are useful compatibility examples of stale/redirected support and exact target preservation. Direct source disclosure can preserve the existing adapter without requiring these tests as semantic witnesses. |

## Positive resources: assembly

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0049 | The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts. |
| R006 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md |  | E0052 | Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R124 | REQUIRED | src/devtools/context/planning/rendering.py | U19, U20 | E0038, E0039 | This resource establishes U19, U20. It is an indispensable member within at least one complete minimal alternative (assembly-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R143 | HELPFUL_ONLY | src/devtools/context/python/function/request_assembly.py |  | E0070 | The older function-specific request assembler corroborates the copy-and-task-first pattern. It does not establish the exact common rendering contract, so cannot substitute for the common assembler on its own. |
| R254 | HELPFUL_ONLY | src/devtools/models/interaction/docs/overview.md |  | E0075 | The interaction overview corroborates request immutability and model ownership. Task prescriptions plus the common dataclass-copy implementation suffice for preserving all request fields. |
| R255 | HELPFUL_ONLY | src/devtools/models/interaction/models.py |  | E0076 | ModelRequest's actual immutable field inventory confirms tools/settings/conversation/provider fields. The task authoritatively names the preservation target and common assembly uses replace, so this confirmation is useful but not necessary. |
| R257 | HELPFUL_ONLY | src/devtools/models/interaction/prompt.py |  | E0077 | Prompt is useful confirmation of content/role representation; the task and common assembly already establish the required copying behavior. |
| R383 | HELPFUL_ONLY | tests/context/planning/test_plan.py |  | E0078, E0079 | Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested. |
| R397 | HELPFUL_ONLY | tests/context/python/function/test_rendering.py |  | E0088 | Older function rendering tests illustrate exact source and ordered presentation. They are not a complete proof of the current common renderer's metadata contract. |
| R398 | HELPFUL_ONLY | tests/context/python/function/test_request_assembly.py |  | E0089 | Older request assembly tests illustrate task-first copying and unchanged request semantics, without requiring that older assembly path in the new common representation. |
| R473 | HELPFUL_ONLY | tests/models/interaction/test_models.py |  | E0093 | Request-value tests corroborate immutability, typed settings and Prompt semantics. The task plus common replace-based copying makes these confirmations dispensable to the required preservation information. |

## Positive resources: exports

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R000 | HELPFUL_ONLY | AGENTS.md |  | E0047, E0048 | The operating guide corroborates package ownership, documentation impact and the protected validation boundary. The needed task constraints and exact commands/settings have complete narrower support; agent-operating instructions are not additional feature obligations. |
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0049 | The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts. |
| R006 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md |  | E0052 | Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R083 | HELPFUL_ONLY | src/devtools/context/__init__.py |  | E0058 | The current facade import/export lists are useful edit context. Public destination and required exposure are supplied by the task; preserving unrelated exports does not require treating their entire inventory as new necessary feature information. |
| R120 | HELPFUL_ONLY | src/devtools/context/planning/__init__.py |  | E0060 | The planning initializer shows current public symbols and is useful for adding exports, but the existing option protocol and task-supplied public destinations establish the necessary contracts. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R123 | HELPFUL_ONLY | src/devtools/context/planning/plan.py |  | E0025, E0026 | The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets. |
| R124 | HELPFUL_ONLY | src/devtools/context/planning/rendering.py |  | E0038, E0039 | The common renderer/assembler demonstrates the desired separation and copied-request regression target. Future tests and exports do not require new knowledge of its exact formatting in addition to the assembly obligation. |
| R140 | HELPFUL_ONLY | src/devtools/context/python/function/planned_reference.py |  | E0068 | The qualified-reference adapter is a concrete protocol example and compatibility reference. The new option can preserve it through the existing protocol without modifying or reproducing its internals. |

## Positive resources: tests

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R064 | REQUIRED | pyproject.toml | U28 | E0040 | This resource establishes U28. It is an indispensable member within at least one complete minimal alternative (tests-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R099 | HELPFUL_ONLY | src/devtools/context/localization/grounding/resolve.py |  | E0024, E0059 | Existing method/declaration grounding is a concrete consumer example of native source selection and validated parent containment. Canonical analysis membership and the native parent link already establish the necessary information in every minimal integrity alternative, so this consumer is corroboration rather than an additional prerequisite. |
| R122 | HELPFUL_ONLY | src/devtools/context/planning/materialization.py |  | E0032, E0031 | The result type and common materialization guards provide implementation and regression-test context for a new protocol participant; their necessity is charged to integrity/materialization rather than to a second invented choice-admission rule. |
| R123 | HELPFUL_ONLY | src/devtools/context/planning/plan.py |  | E0025, E0026 | The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets. |
| R124 | HELPFUL_ONLY | src/devtools/context/planning/rendering.py |  | E0038, E0039 | The common renderer/assembler demonstrates the desired separation and copied-request regression target. Future tests and exports do not require new knowledge of its exact formatting in addition to the assembly obligation. |
| R125 | HELPFUL_ONLY | src/devtools/context/planning/resource.py |  | E0063, E0064 | The existing whole-resource option is a useful preserved-compatibility and retained-content validation example. It is not a mandatory template for a new direct-source representation or an implicit whole-owner fallback. |
| R129 | HELPFUL_ONLY | src/devtools/context/python/classes/containment.py |  | E0022, E0023 | The validated view is a useful direct-containment API and test example. Its necessary membership/parent information is already available from the complete canonical declaration contract; validating supplied native identities does not require one particular view implementation in addition to canonical replay/equality. |
| R130 | HELPFUL_ONLY | src/devtools/context/python/classes/declarations.py |  | E0021, E0019 | Native class/method derivation provides examples for test fixtures and precise scope descriptions, without making existing implementation details additional prescribed test/documentation outcomes. |
| R131 | HELPFUL_ONLY | src/devtools/context/python/classes/docs/overview.md |  | E0020 | The class/method package explains identities, direct containment and decorator-range limits. It is useful documentation/test context but does not add mandatory future test families or documentation destinations. |
| R135 | HELPFUL_ONLY | src/devtools/context/python/function/containment.py |  | E0065 | The function-containment view provides another validation/navigation example. Canonical selector replay plus exact native membership can satisfy the required checks without requiring this additional aggregate-view mechanism. |
| R136 | HELPFUL_ONLY | src/devtools/context/python/function/declarations.py |  | E0013, E0036 | The native function model and analyzer help author exact identity/range tests and descriptions; the task prescribes future coverage and other obligations already bind these native facts. |
| R139 | HELPFUL_ONLY | src/devtools/context/python/function/materialization.py |  | E0045, E0046 | The UTF-8 extractor is a useful canonical reuse candidate and supports the coordinate fact. Every minimal materialization alternative already needs the native function model, which supplies that coordinate fact; the algorithm's source is therefore not an additional necessary information member. |
| R140 | HELPFUL_ONLY | src/devtools/context/python/function/planned_reference.py |  | E0068 | The qualified-reference adapter is a concrete protocol example and compatibility reference. The new option can preserve it through the existing protocol without modifying or reproducing its internals. |
| R141 | HELPFUL_ONLY | src/devtools/context/python/function/qualified_reference.py |  | E0069 | The preserved qualified-reference path illustrates rechecking native membership and retained dependencies before exact extraction. Direct source declarations must not acquire its imported-reference semantics. |
| R143 | HELPFUL_ONLY | src/devtools/context/python/function/request_assembly.py |  | E0070 | The older function-specific request assembler corroborates the copy-and-task-first pattern. It does not establish the exact common rendering contract, so cannot substitute for the common assembler on its own. |
| R154 | HELPFUL_ONLY | src/devtools/context/python/modules/docs/overview.md |  | E0012 | The source-selector documentation is useful for test and documentation wording; future test coverage and documentation content are task prescriptions, not proof that new disclosure choices already exist. |
| R155 | HELPFUL_ONLY | src/devtools/context/python/modules/interpretation.py |  | E0072, E0073 | Module interpretation supplies useful fixture-construction and retained-resource context. The task accepts caller-supplied native declarations and the source selector already establishes the admitted module fields; no new module-discovery mechanism is required. |
| R158 | HELPFUL_ONLY | src/devtools/context/python/modules/selection.py |  | E0011 | The canonical selector is a useful test setup and documentation example. Its API necessity belongs to native source/integrity obligations, not to treating the future test matrix as an existing implementation contract. |
| R180 | HELPFUL_ONLY | src/devtools/context/repository/resource.py |  | E0029 | The immutable retained resource value is useful to construct source fixtures and understand owners. Source identity's native dependency fields and task scope can be established without separately requiring this resource for that obligation. |
| R181 | HELPFUL_ONLY | src/devtools/context/repository/snapshot.py |  | E0028 | The snapshot lookup is useful source/test setup context, with its necessary missing-resource contract separately established under integrity. |
| R255 | HELPFUL_ONLY | src/devtools/models/interaction/models.py |  | E0076 | ModelRequest's actual immutable field inventory confirms tools/settings/conversation/provider fields. The task authoritatively names the preservation target and common assembly uses replace, so this confirmation is useful but not necessary. |
| R257 | HELPFUL_ONLY | src/devtools/models/interaction/prompt.py |  | E0077 | Prompt is useful confirmation of content/role representation; the task and common assembly already establish the required copying behavior. |
| R383 | HELPFUL_ONLY | tests/context/planning/test_plan.py |  | E0078, E0079 | Existing pytest cases provide concrete mixed-order, stale/missing, returned-identity and copied-request examples. New tests can be written from the task and established native contracts; this test file is not required merely because regression tests are requested. |
| R387 | HELPFUL_ONLY | tests/context/python/classes/test_declarations.py |  | E0080 | Class/method tests demonstrate direct scope, native parent and decorator-keyword span boundaries. They corroborate rather than replace the complete native identity and validation contracts. |
| R390 | HELPFUL_ONLY | tests/context/python/function/test_containment.py |  | E0081 | Function-containment tests illustrate invalid aggregate/declaration support. Reusing this exact aggregate or fixture is not required for new direct choices. |
| R393 | HELPFUL_ONLY | tests/context/python/function/test_declarations.py |  | E0082, E0083 | Tests corroborate repeated native subjects and UTF-8 coordinates but do not supply a complete alternative for every native identity/provenance fact. |
| R395 | HELPFUL_ONLY | tests/context/python/function/test_materialization.py |  | E0084, E0085 | Tests provide CRLF/non-ASCII and malformed-range examples for the existing function-only path; they do not prescribe a new direct-source API or solve decorator-inclusive provenance. |
| R396 | HELPFUL_ONLY | tests/context/python/function/test_qualified_reference.py |  | E0086, E0087 | Qualified-reference tests are useful compatibility examples of stale/redirected support and exact target preservation. Direct source disclosure can preserve the existing adapter without requiring these tests as semantic witnesses. |
| R397 | HELPFUL_ONLY | tests/context/python/function/test_rendering.py |  | E0088 | Older function rendering tests illustrate exact source and ordered presentation. They are not a complete proof of the current common renderer's metadata contract. |
| R398 | HELPFUL_ONLY | tests/context/python/function/test_request_assembly.py |  | E0089 | Older request assembly tests illustrate task-first copying and unchanged request semantics, without requiring that older assembly path in the new common representation. |
| R409 | HELPFUL_ONLY | tests/context/python/modules/test_selection.py |  | E0090, E0091, E0092 | Selection tests demonstrate decorated/repeated source identity, negative kind/scope cases and foreign inputs. They are useful executable examples, but the complete selector contract also needs retained analyses and parse-failure behavior explicitly established elsewhere. |
| R473 | HELPFUL_ONLY | tests/models/interaction/test_models.py |  | E0093 | Request-value tests corroborate immutability, typed settings and Prompt semantics. The task plus common replace-based copying makes these confirmations dispensable to the required preservation information. |

## Positive resources: documentation

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R000 | HELPFUL_ONLY | AGENTS.md |  | E0047, E0048 | The operating guide corroborates package ownership, documentation impact and the protected validation boundary. The needed task constraints and exact commands/settings have complete narrower support; agent-operating instructions are not additional feature obligations. |
| R002 | HELPFUL_ONLY | docs/architecture.md |  | E0049 | The current architectural account corroborates the narrow caller-directed plan, provenance-bearing disclosure and separated assembly, while also describing future planning. This context is useful for edits but contributes no additional necessary fact beyond the task and exact implemented contracts. |
| R004 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md |  | E0051 | The architecture explains identity/occurrence and derivation distinctions at a broader level. Native declaration contracts and the task establish the bounded facts needed here without requiring the full architectural framework. |
| R006 | HELPFUL_ONLY | docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md |  | E0052 | Planning-versus-assembly guidance corroborates the requested ownership and semantic-strength constraints. It does not supply a missing implemented contract. |
| R010 | HELPFUL_ONLY | docs/architecture/taxonomy.md |  | E0053 | The taxonomy corroborates immutable plan/disclosure distinctions and the absence of automatic sufficiency. The task and narrow native code already establish the necessary feature facts. |
| R061 | HELPFUL_ONLY | docs/documentation_map.md |  | E0055 | The document's authority-and-ownership introduction clarifies the role of current architecture versus taxonomy. The task already supplies the required documentation destinations and update content. |
| R121 | HELPFUL_ONLY | src/devtools/context/planning/docs/overview.md |  | E0061, E0062 | Package prose corroborates the two current options, immutable ordered plan and copied request. It is useful update context, without replacing the exact current protocol/materialized-item contracts or adding a semantic requirement to the task. |
| R123 | HELPFUL_ONLY | src/devtools/context/planning/plan.py |  | E0025, E0026 | The native immutable plan and protocol corroborate the frame/order and ownership behavior; the obligation's own required units use more specific realization checks or task-prescribed test/documentation targets. |
| R124 | HELPFUL_ONLY | src/devtools/context/planning/rendering.py |  | E0038, E0039 | The common renderer/assembler demonstrates the desired separation and copied-request regression target. Future tests and exports do not require new knowledge of its exact formatting in addition to the assembly obligation. |
| R130 | HELPFUL_ONLY | src/devtools/context/python/classes/declarations.py |  | E0021, E0019 | Native class/method derivation provides examples for test fixtures and precise scope descriptions, without making existing implementation details additional prescribed test/documentation outcomes. |
| R131 | HELPFUL_ONLY | src/devtools/context/python/classes/docs/overview.md |  | E0020 | The class/method package explains identities, direct containment and decorator-range limits. It is useful documentation/test context but does not add mandatory future test families or documentation destinations. |
| R136 | HELPFUL_ONLY | src/devtools/context/python/function/declarations.py |  | E0013, E0036 | The native function model and analyzer help author exact identity/range tests and descriptions; the task prescribes future coverage and other obligations already bind these native facts. |
| R138 | HELPFUL_ONLY | src/devtools/context/python/function/docs/overview.md |  | E0066, E0067 | Function package prose corroborates direct source versus binding, retained-source extraction and compatibility, but some Reference terminology is narrower than current code. It is not a unique complete native contract for this change. |
| R153 | HELPFUL_ONLY | src/devtools/context/python/modules/declarations.py |  | E0071 | Binding lookup provides a useful contrast to source selection, retaining conservative decorated/rebound-target behavior. The task and native source selector already establish that this binding path must not be substituted. |
| R154 | HELPFUL_ONLY | src/devtools/context/python/modules/docs/overview.md |  | E0012 | The source-selector documentation is useful for test and documentation wording; future test coverage and documentation content are task prescriptions, not proof that new disclosure choices already exist. |
| R158 | HELPFUL_ONLY | src/devtools/context/python/modules/selection.py |  | E0011 | The canonical selector is a useful test setup and documentation example. Its API necessity belongs to native source/integrity obligations, not to treating the future test matrix as an existing implementation contract. |
| R172 | HELPFUL_ONLY | src/devtools/context/python/references/docs/overview.md |  | E0074 | The Reference documentation distinguishes bounded binding-based relations from direct source identity and helps explain compatibility. Source disclosure itself does not need Reference resolution. |
| R409 | HELPFUL_ONLY | tests/context/python/modules/test_selection.py |  | E0090, E0091, E0092 | Selection tests demonstrate decorated/repeated source identity, negative kind/scope cases and foreign inputs. They are useful executable examples, but the complete selector contract also needs retained analyses and parse-failure behavior explicitly established elsewhere. |

## Positive resources: validation

| Resource | Label | Address | Units | Exact support | Rationale |
|---|---|---|---|---|---|
| R000 | HELPFUL_ONLY | AGENTS.md |  | E0047, E0048 | The operating guide corroborates package ownership, documentation impact and the protected validation boundary. The needed task constraints and exact commands/settings have complete narrower support; agent-operating instructions are not additional feature obligations. |
| R057 | HELPFUL_ONLY | docs/backlog/items/B-0047-protected-development-validation-profile.md |  | E0054 | The implemented-profile section corroborates protected selection, retained coverage and exit-code propagation; it is redundant with the complete development contract and actual configuration. |
| R060 | REQUIRED | docs/development/validation.md | U31, U33, U34 | E0042, E0043 | This resource establishes U31, U33, U34. It is an indispensable member within at least one complete minimal alternative (validation-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R064 | REQUIRED | pyproject.toml | U32 | E0040, E0041 | This resource establishes U32. It is an indispensable member within at least one complete minimal alternative (validation-A1); it need not occur in every acceptable alternative. The attached unit statements and removal witnesses specify the necessary information. |
| R065 | HELPFUL_ONLY | scripts/validate_development.py |  | E0056, E0057 | The script concretely corroborates the documented tests/ exclusion and returned pytest status. Its full semantic command behavior is already stated in the required development contract, so naming this entry point does not make its source additionally necessary. |
| R524 | HELPFUL_ONLY | tests/scripts/test_validate_development.py |  | E0094, E0095 | Profile tests corroborate pre-collection exclusion and failure-code propagation. They add no missing command or configuration fact beyond the complete documented profile. |

## Complete REQUIRED resource union

12 resources occur in at least one minimal acceptable obligation alternative. This union is not a simultaneous task witness.

| Alias | Address | Native document identity |
|---|---|---|
| R060 | docs/development/validation.md | `248e605c7cf568ea55bf033a8e56646806da9716a81f586d6f02318fd6311383` |
| R064 | pyproject.toml | `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0` |
| R122 | src/devtools/context/planning/materialization.py | `e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8` |
| R123 | src/devtools/context/planning/plan.py | `09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493` |
| R124 | src/devtools/context/planning/rendering.py | `edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f` |
| R130 | src/devtools/context/python/classes/declarations.py | `b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd` |
| R131 | src/devtools/context/python/classes/docs/overview.md | `f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd` |
| R136 | src/devtools/context/python/function/declarations.py | `038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa` |
| R154 | src/devtools/context/python/modules/docs/overview.md | `8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95` |
| R158 | src/devtools/context/python/modules/selection.py | `f9a7943390f82d8e1399edaa66aebd172b43ad5a85838285c134ec03f5ad89af` |
| R180 | src/devtools/context/repository/resource.py | `216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f` |
| R181 | src/devtools/context/repository/snapshot.py | `71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7` |

## Complete semantic-unit inventory

Units describe semantic contracts or task prescriptions, not reading tasks. Native function/class/method identity facts are separated; plan admission and plan identity, item shape and source coordinates, rendering and request copying are separated. Shared facts retain one unit identity across obligations. Test groups describe separable observable requirements; none is a file-per-unit decomposition.

### U01 — source, documentation

The admitted future source choices are caller-selected direct function/class declarations and direct methods under a validated native class; source identity asserts no runtime attribute, imported-facade, inherited-method, or semantic resolution.

Scope: requested feature scope. Necessity: Defines the mandatory supported/deferred boundary without substituting binding lookup for source selection.

- Support bundle 0 (TASK_BACKED): E0001, E0002; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U02 — source, integrity

Exact module source selection consumes a matching retained module, exact identifier and CLASS/FUNCTION kind, retains both canonical analyses and every matching direct declaration, preserves repeated identities, and propagates native parse failure without successful coverage.

Scope: native repository contract. Necessity: The mandated selector's actual behavior and available native analyses must be known to reuse it and check supplied identities; the task supplies its name but not this contract.

- Support bundle 0 (DIRECT): E0011; resources: R158. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 1 (DIRECT): E0012; resources: R154. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U03 — source, integrity, materialization

Function declaration knowledge retains a derivation identity, a distinct snapshot-local subject bound to resource/content dependency, parser definition and declaration ordinal, and an addressed source occurrence; a name is not the subject identity.

Scope: native repository contract. Necessity: Necessary to retain/check native function identity and provenance rather than reconstructing an identity from its name.

- Support bundle 0 (DIRECT): E0013, E0014, E0015, E0035; resources: R136. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U04 — source, integrity, materialization

A direct class has separate knowledge, subject and derivation identities; its subject is bound to snapshot, exact resource dependency, derivation definition and module-class ordinal, with its own source occurrence.

Scope: native repository contract. Necessity: Class identity and source provenance must survive selection, validation and materialization, including repeated class names.

- Support bundle 0 (DIRECT): E0016, E0017; resources: R130. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 1 (DIRECT): E0020; resources: R131. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U05 — source, integrity, materialization

A native direct method has its own source occurrence and a canonical containing_class; its subject additionally binds the parent class subject and ordinal within that class, so occurrence resource and lexical parent are distinct.

Scope: native repository contract. Necessity: A method cannot be selected/validated or disclosed as an unqualified function or a bare runtime attribute.

- Support bundle 0 (DIRECT): E0018, E0019; resources: R130. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 1 (DIRECT): E0020; resources: R131. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U06 — choices

Each plan participant exposes purpose, repository_id, snapshot_id, representation, identity and materialize(snapshot) returning MaterializedDisclosureItem through PlannedDisclosure.

Scope: native repository contract. Necessity: These are the existing integration requirements that a new concrete option must implement.

- Support bundle 0 (DIRECT): E0025; resources: R123. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U07 — choices

DisclosurePlan requires a nonblank purpose, a nonempty ordered tuple of choices with equal purpose/repository/snapshot, and distinct option identities.

Scope: native repository contract. Necessity: Preserving admission invariants requires the existing checks, not merely the task's abstract immutability request.

- Support bundle 0 (DIRECT): E0026; resources: R123. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U08 — choices

The frozen plan identity incorporates purpose, repository and snapshot, preceding-plan identity and every ordered representation/option identity pair.

Scope: native repository contract. Necessity: Order and lineage must continue to distinguish plans; a new choice must not collapse those native identity inputs.

- Support bundle 0 (DIRECT): E0027, E0044; resources: R123. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U09 — choices

Add explicit source choices alongside existing qualified-reference and whole-resource choices, retaining immutable purpose/frame/order and compatibility without automatic retrieval or selection.

Scope: requested integration behavior. Necessity: States the required compatibility and admission policy; it does not require changing or reverse-engineering preserved adapters.

- Support bundle 0 (TASK_BACKED): E0001, E0003; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U10 — integrity

RepositorySnapshot.resource_at(address) returns the retained occurrence whose address equals the requested address, and raises ValueError when none exists.

Scope: native repository contract. Necessity: The required retained-snapshot lookup and observable missing-resource behavior must be established without assuming a filesystem fallback.

- Support bundle 0 (DIRECT): E0028; resources: R181. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U11 — integrity, materialization

A retained RepositoryResourceOccurrence is an immutable value carrying address, independent ContentIdentity, exact content string, encoding and byte_size; address and content identity are distinct.

Scope: native repository contract. Necessity: Native retained content and owner-resource provenance must be checked and emitted using their actual fields, not invented from the task.

- Support bundle 0 (DIRECT): E0029, E0030; resources: R180. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U12 — integrity

Every supplied declaration/resource must be checked for foreign or stale frame/content, missing resource, unsupported scope and mismatched returned identity before disclosure publication; no files are reacquired.

Scope: requested validation behavior. Necessity: These rejection categories and ordering are mandatory future behavior, even where existing helpers supply only part of validation.

- Support bundle 0 (TASK_BACKED): E0004; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U13 — integrity

Canonical class/method analysis from the retained source supplies the parent classes and their direct methods. Requiring the supplied parent and method to equal the corresponding native values and checking the method's containing_class establishes direct source scope without runtime resolution.

Scope: native repository contract. Necessity: A matching name or resource is insufficient; the parent and method must be connected to the current native analysis. The required information is that native membership/parent relation, not the identity of a particular consumer or containment helper.

- Support bundle 0 (INFERABLE): E0021, E0019; resources: R130. The canonical traversal emits module-body classes and only methods directly in each class body, storing the actual containing_class. Equality/membership against these freshly derived native values checks the supplied pair; retained frame/content lookup and publication checks are supplied by the other integrity units.
- Support bundle 1 (INFERABLE): E0011, E0020; resources: R131, R158. The selector rederives and retains class_analysis from the matching retained module. The explicit class/method contract establishes native parent-relative identities and direct containment. Membership/equality against that canonical analysis establishes the supplied pair without an additional consumer example.
- Support bundle 2 (INFERABLE): E0012, E0020; resources: R131, R154. The two package contracts jointly establish canonical retained-source analyses, supported direct scope and the canonical containing_class link. Comparing supplied values with those native analysis members is a bounded inference from the documented contracts, not a runtime-binding assumption.
- Support bundle 3 (DIRECT): E0024; resources: R099. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 4 (INFERABLE): E0021, E0022, E0023; resources: R129, R130. This is a supported implementation route using the existing validated view. It adds no necessary fact when the same canonical membership/parent information is already established by a complete declaration-analysis support bundle.

### U14 — integrity

Common materialization rejects a foreign plan frame and checks each returned option_identity and representation before appending it; ContextDisclosure is constructed only after all options succeed and itself enforces positional item/choice alignment.

Scope: native repository contract. Necessity: The existing publication boundary must be preserved so an option cannot publish a mismatched or partial disclosure.

- Support bundle 0 (DIRECT): E0031, E0033; resources: R122. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U15 — materialization

Each common materialized item carries option identity, representation, resource-address and content-identity tuples, text and native_provenance; ContextDisclosure retains exactly one aligned item per ordered plan choice.

Scope: native repository contract. Necessity: This is the actual container contract for exact source plus native derivation/range/owner provenance in a mixed plan.

- Support bundle 0 (DIRECT): E0032, E0033, E0031; resources: R122. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U16 — materialization

Native source ranges use one-based lines, zero-based UTF-8 byte columns and exclusive ends, anchored by snapshot and resource address.

Scope: native repository contract. Necessity: Byte-preserving extraction cannot treat native columns as Python character indexes or normalize line endings.

- Support bundle 0 (DIRECT): E0034, E0035; resources: R136. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 1 (INFERABLE): E0045, E0046; resources: R139. Half-open UTF-8 byte slicing, one-based line indexing and retained line endings establish the same coordinate contract; the addressed occurrence is supplied by U03-U05.

### U17 — materialization

Current native declaration ranges start at def/async def/class and exclude preceding decorator lines; decorated source declarations remain native declarations.

Scope: native repository contract. Necessity: The decorator requirement cannot be satisfied by assuming that the existing occurrence range already includes its decorators.

- Support bundle 0 (DIRECT): E0020; resources: R131. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.
- Support bundle 1 (INFERABLE): E0036, E0037; resources: R130, R136. Both native analyzers use the declaration node's lineno/col_offset. Their code retains declarations without rejecting decorator_list; the class documentation explicitly corroborates the resulting declaration-keyword boundary.

### U18 — materialization

Materialize the selected exact declaration source with derivation/range/owner provenance, preserving decorators, UTF-8 boundaries, CRLF/non-ASCII bytes and mixed caller order; neither expand to whole owners nor claim sufficiency implicitly.

Scope: requested materialization behavior. Necessity: Defines the future faithful representation independently of any existing function-only materializer; U17 constrains how the requested decorator preservation is implemented.

- Support bundle 0 (TASK_BACKED): E0005; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U19 — assembly

Common rendering emits disclosure purpose, plan/snapshot identity, item count, then each item's ordinal, representation, option identity and already materialized text in plan order.

Scope: native repository contract. Necessity: Preserving common rendering requires its actual presentation/ordering contract, not a new language-specific renderer in common assembly.

- Support bundle 0 (DIRECT): E0038; resources: R124. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U20 — assembly

Common request assembly frames the unchanged task before rendered Context using UTF-8 byte lengths, and dataclasses.replace changes only the Prompt while preserving the original prompt role.

Scope: native repository contract. Necessity: This is the existing request-copy mechanism whose behavior must survive the new representation.

- Support bundle 0 (DIRECT): E0039; resources: R124. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U21 — assembly

Original request, prompt role, settings, conversation, provider settings and tools are preserved except for the copied prompt; no new budget or truncation policy is introduced.

Scope: requested preservation behavior. Necessity: The task supplies the preservation target, including tools; current request field names need not be independently rediscovered just to restate that target.

- Support bundle 0 (TASK_BACKED): E0006; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U22 — exports

Expose the new explicit choice through the common planning public API and the outer Context facade.

Scope: requested public exposure. Necessity: These public destinations are mandatory task-supplied interface locations. An existing initializer is a useful edit reference, but contributes no additional necessary semantic decision.

- Support bundle 0 (TASK_BACKED): E0007; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U23 — exports

Keep dependency direction: do not add a Retrieval dependency or language-specific logic in common assembly.

Scope: requested ownership boundary. Necessity: This is an authoritative constraint on the new design. Existing facade imports are not a requirement to reproduce their implementation form.

- Support bundle 0 (TASK_BACKED): E0007; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U24 — tests

Focused tests must exercise direct function/class/method choices, decorated declarations and repeated declarations.

Scope: requested test coverage. Necessity: Each family is an explicitly required future test target; repeated native identities must not be replaced by last-binding assumptions.

- Support bundle 0 (TASK_BACKED): E0008; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U25 — tests

Focused tests must verify mixed-plan order and exact source/provenance, including the exactness constraints stated for materialization.

Scope: requested test coverage. Necessity: Order and provenance are distinct observable outcomes requiring assertions.

- Support bundle 0 (TASK_BACKED): E0005, E0008; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U26 — tests

Tests must reject stale, foreign and missing-resource inputs and cover the task's supplied-identity/scope and publication guards.

Scope: requested test coverage. Necessity: Failure behavior must be exercised; new tests can be authored without adopting any existing test fixture.

- Support bundle 0 (TASK_BACKED): E0004, E0008; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U27 — tests

Regression tests must preserve existing choices and copied-request semantics, including tools and the unchanged original request.

Scope: requested test coverage. Necessity: The task explicitly requires these preserved behaviors to remain testable; existing test files are examples rather than mandatory witnesses.

- Support bundle 0 (TASK_BACKED): E0006, E0008; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U28 — tests

The repository's test framework is pytest under tests/, with strict configuration/markers and devtools branch coverage including a 100% threshold.

Scope: existing test convention. Necessity: New tests must participate in the actual configured framework and gate; the task names the settings file but does not provide its contents.

- Support bundle 0 (DIRECT): E0040; resources: R064. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U29 — documentation

Update src/devtools/context/planning/docs/overview.md and docs/architecture.md for the new explicit source-disclosure behavior.

Scope: requested documentation destinations. Necessity: The two required documentation destinations are supplied by the task; their locations are themselves the necessary fact.

- Support bundle 0 (TASK_BACKED): E0009; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U30 — documentation

The updated documentation must explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, and make no automatic relevance or readiness claim.

Scope: requested documentation content. Necessity: This future documentation content is fully prescribed by the task and U01; existing prose is context for editing, not an additional mandatory fact.

- Support bundle 0 (TASK_BACKED): E0001, E0002, E0003, E0007, E0009; resources: none; task-backed. These spans prescribe future behavior authoritatively. They are not evidence that the new feature already exists; no repository confirmation of the prescription is necessary.

### U31 — validation

The documented protected development command is uv run python scripts/validate_development.py; it runs tests/ while excluding tests/experiments/ before recursive collection, uses configured pytest settings unchanged and returns the pytest exit status.

Scope: existing protected development contract. Necessity: The documented command and precise isolation/configuration behavior are necessary; merely knowing the script filename does not establish them.

- Support bundle 0 (DIRECT): E0042; resources: R060. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U32 — validation

Preserved configuration enables strict pytest configuration/markers, devtools branch coverage, term-missing output and 100% thresholds; strict mypy covers src, tests and experiments with explicit package bases and src on mypy_path.

Scope: existing protected configuration. Necessity: These existing settings must be retained. Type-checking an experiments path does not authorize executing excluded experiment tests.

- Support bundle 0 (DIRECT): E0040, E0041; resources: R064. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U33 — validation

Run separate Ruff lint and format checks, mypy, worktree whitespace and staged-index whitespace checks using the documented commands; the protected entry point runs tests only.

Scope: existing documented quality gates. Necessity: The task's tool names alone do not supply the complete documented command contract and staged-index distinction.

- Support bundle 0 (DIRECT): E0043; resources: R060. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

### U34 — validation

The protected development profile does not validate confirmation judgments/outcomes; that activity is separately authorized, and the experiment-tree exclusion must not be removed to obtain a pass.

Scope: existing validation isolation boundary. Necessity: This is the frozen validation criterion's operational boundary, not a software-feature requirement or a reason to access excluded data.

- Support bundle 0 (DIRECT): E0042; resources: R060. The cited native implementation or explicit package contract states the fact; no outside repository state is assumed.

## All minimal acceptable alternatives

ALL members within a row are jointly required; ANY complete row for that obligation suffices. Required units are fixed semantic targets; differing rows substitute complete repository evidence. Empty resource rows rely solely on authoritative task prescriptions. Proof-bundle choices and resource-removal witnesses are retained in JSON.

| Alternative | Obligation | Required resources | Required units | Task-backed units |
|---|---|---|---|---|
| source-A1 | source | R130, R136, R154 | U01, U02, U03, U04, U05 | U01 |
| source-A2 | source | R130, R136, R158 | U01, U02, U03, U04, U05 | U01 |
| source-A3 | source | R131, R136, R154 | U01, U02, U03, U04, U05 | U01 |
| source-A4 | source | R131, R136, R158 | U01, U02, U03, U04, U05 | U01 |
| choices-A1 | choices | R123 | U06, U07, U08, U09 | U09 |
| integrity-A1 | integrity | R122, R130, R136, R154, R180, R181 | U02, U03, U04, U05, U10, U11, U12, U13, U14 | U12 |
| integrity-A2 | integrity | R122, R130, R136, R158, R180, R181 | U02, U03, U04, U05, U10, U11, U12, U13, U14 | U12 |
| integrity-A3 | integrity | R122, R131, R136, R154, R180, R181 | U02, U03, U04, U05, U10, U11, U12, U13, U14 | U12 |
| integrity-A4 | integrity | R122, R131, R136, R158, R180, R181 | U02, U03, U04, U05, U10, U11, U12, U13, U14 | U12 |
| materialization-A1 | materialization | R122, R130, R136, R180 | U03, U04, U05, U11, U15, U16, U17, U18 | U18 |
| materialization-A2 | materialization | R122, R131, R136, R180 | U03, U04, U05, U11, U15, U16, U17, U18 | U18 |
| assembly-A1 | assembly | R124 | U19, U20, U21 | U21 |
| exports-A1 | exports | ∅ | U22, U23 | U22, U23 |
| tests-A1 | tests | R064 | U24, U25, U26, U27, U28 | U24, U25, U26, U27 |
| documentation-A1 | documentation | ∅ | U01, U29, U30 | U01, U29, U30 |
| validation-A1 | validation | R060, R064 | U31, U32, U33, U34 |  |

## Complete task combinations

Inclusion-minimal complete obligation evidence alternatives, combined by Cartesian product with cross-obligation reuse. Sufficient unions are unions of those complete alternatives, not all arbitrary supersets of adequate evidence. Counts describe necessary information, not implementation execution or measured effectiveness.

| Combination | Alternatives, one per obligation | Resource union | Unit union |
|---|---|---|---|
| TC0001 | source-A1, choices-A1, integrity-A1, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0002 | source-A1, choices-A1, integrity-A1, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0003 | source-A1, choices-A1, integrity-A2, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0004 | source-A1, choices-A1, integrity-A2, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0005 | source-A1, choices-A1, integrity-A3, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0006 | source-A1, choices-A1, integrity-A3, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0007 | source-A1, choices-A1, integrity-A4, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0008 | source-A1, choices-A1, integrity-A4, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0009 | source-A2, choices-A1, integrity-A1, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0010 | source-A2, choices-A1, integrity-A1, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0011 | source-A2, choices-A1, integrity-A2, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0012 | source-A2, choices-A1, integrity-A2, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0013 | source-A2, choices-A1, integrity-A3, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0014 | source-A2, choices-A1, integrity-A3, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0015 | source-A2, choices-A1, integrity-A4, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0016 | source-A2, choices-A1, integrity-A4, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0017 | source-A3, choices-A1, integrity-A1, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0018 | source-A3, choices-A1, integrity-A1, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0019 | source-A3, choices-A1, integrity-A2, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0020 | source-A3, choices-A1, integrity-A2, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0021 | source-A3, choices-A1, integrity-A3, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0022 | source-A3, choices-A1, integrity-A3, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R131, R136, R154, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0023 | source-A3, choices-A1, integrity-A4, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0024 | source-A3, choices-A1, integrity-A4, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0025 | source-A4, choices-A1, integrity-A1, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0026 | source-A4, choices-A1, integrity-A1, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0027 | source-A4, choices-A1, integrity-A2, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0028 | source-A4, choices-A1, integrity-A2, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0029 | source-A4, choices-A1, integrity-A3, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0030 | source-A4, choices-A1, integrity-A3, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R131, R136, R154, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0031 | source-A4, choices-A1, integrity-A4, materialization-A1, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |
| TC0032 | source-A4, choices-A1, integrity-A4, materialization-A2, assembly-A1, exports-A1, tests-A1, documentation-A1, validation-A1 | R060, R064, R122, R123, R124, R131, R136, R158, R180, R181 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 |

## Distinct sufficient unions and ranges

Combinations: **32**. Distinct resource unions: **9**. Distinct unit unions: **1**. Sufficient resource count: **10–12**. Sufficient unit count: **34–34**.

| Resource-union ID | Exact members | Combinations |
|---|---|---|
| RU001 | R060, R064, R122, R123, R124, R130, R136, R154, R180, R181 | TC0001 |
| RU002 | R060, R064, R122, R123, R124, R130, R136, R158, R180, R181 | TC0011 |
| RU003 | R060, R064, R122, R123, R124, R131, R136, R154, R180, R181 | TC0022 |
| RU004 | R060, R064, R122, R123, R124, R131, R136, R158, R180, R181 | TC0032 |
| RU005 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R180, R181 | TC0002, TC0005, TC0006, TC0017, TC0018, TC0021 |
| RU006 | R060, R064, R122, R123, R124, R130, R131, R136, R158, R180, R181 | TC0012, TC0015, TC0016, TC0027, TC0028, TC0031 |
| RU007 | R060, R064, R122, R123, R124, R130, R136, R154, R158, R180, R181 | TC0003, TC0009 |
| RU008 | R060, R064, R122, R123, R124, R131, R136, R154, R158, R180, R181 | TC0024, TC0030 |
| RU009 | R060, R064, R122, R123, R124, R130, R131, R136, R154, R158, R180, R181 | TC0004, TC0007, TC0008, TC0010, TC0013, TC0014, TC0019, TC0020, TC0023, TC0025, TC0026, TC0029 |

| Unit-union ID | Exact members | Combinations |
|---|---|---|
| UU001 | U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34 | TC0001, TC0002, TC0003, TC0004, TC0005, TC0006, TC0007, TC0008, TC0009, TC0010, TC0011, TC0012, TC0013, TC0014, TC0015, TC0016, TC0017, TC0018, TC0019, TC0020, TC0021, TC0022, TC0023, TC0024, TC0025, TC0026, TC0027, TC0028, TC0029, TC0030, TC0031, TC0032 |

## Indispensability

| Obligation | Resource intersection | Unit intersection |
|---|---|---|
| source | R136 | U01, U02, U03, U04, U05 |
| choices | R123 | U06, U07, U08, U09 |
| integrity | R122, R136, R180, R181 | U02, U03, U04, U05, U10, U11, U12, U13, U14 |
| materialization | R122, R136, R180 | U03, U04, U05, U11, U15, U16, U17, U18 |
| assembly | R124 | U19, U20, U21 |
| exports | ∅ | U22, U23 |
| tests | R064 | U24, U25, U26, U27, U28 |
| documentation | ∅ | U01, U29, U30 |
| validation | R060, R064 | U31, U32, U33, U34 |

Task-indispensable resources: R060, R064, R122, R123, R124, R136, R180, R181.

Task-indispensable units: U01, U02, U03, U04, U05, U06, U07, U08, U09, U10, U11, U12, U13, U14, U15, U16, U17, U18, U19, U20, U21, U22, U23, U24, U25, U26, U27, U28, U29, U30, U31, U32, U33, U34.

## Gaps

- TASK_GAP: **NONE**. Required facts are established by task prescriptions and eligible native contracts. Choosing a new explicit API, decorator representation or new tests/documentation is implementation work, not missing task information. No complete-adjudication block.
- REPOSITORY_INFORMATION_GAP: **NONE**. The required native selection, identity/containment, snapshot, plan, realization, assembly and protected-validation facts have complete alternatives inside the frozen frame. No unprovided operational experiment is needed. No complete-adjudication block.
- TASK_INTERPRETATION_GAP: **NONE**. The clause-by-clause audit maps every mandatory feature/validation requirement to the frozen obligations without widening an unrelated obligation. No complete-adjudication block.

## Interpretation limitations and ambiguity

### L01 — native representation boundary

Native spans exclude preceding decorators although decorated declarations are selected. The task requires decorator preservation. A compliant implementation must retain the native occurrence/identity and explicitly account for any decorator-inclusive materialized extent, or evolve native range semantics with appropriate provenance; simply slicing the existing occurrence cannot meet that requirement.

All needed retained source and analyzer behavior are available. The future representation design remains to be made; this is not an unavailable repository fact. Evidence: E0005, E0020, E0036, E0037. Blocks complete adjudication: NO.

### L02 — bounded caller/API design choice

Exact source selection retains repeated same-name declarations. The task does not choose option-constructor names or a cardinality API. Callers may select exact native identities or an explicit ordered set; taking the first/last declaration as a runtime winner would violate the source/selection boundary.

The required semantics are fixed while several explicit API designs remain valid. Evidence: E0001, E0002, E0011, E0012. Blocks complete adjudication: NO.

### L03 — current documentation mixes implemented and future intent

The current package/native code implement a narrow plan, disclosure and assembler, while broad ADR status still describes an unimplemented general planning/assembly direction. Use the precise implemented contract for current behavior and keep broader claims explicitly future-scoped in updates.

The available implementation and current bounded architecture account establish repository truth despite broader status prose; this does not require guessing missing code. Evidence: E0025, E0031, E0039, E0096, E0049. Blocks complete adjudication: NO.

### L04 — existing helper validates only part of a future contract

Native containment checks validate frame/dependency/coverage/ordinal/support consistency; they do not by themselves rederive arbitrary caller-constructed names/ranges. Canonical replay and membership/equality, as illustrated by method grounding, can supply that additional admission check before publication.

No blanket claim is made that a frozen dataclass or containment view authenticates every supplied field. The task can be satisfied from retained source. Evidence: E0023, E0024, E0011, E0004. Blocks complete adjudication: NO.

Ambiguity state: BOUNDED_DESIGN_AMBIGUITY_ONLY. UNRESOLVED cells, units and obligations: zero. The limitations preserve genuine design/status boundaries but no resource necessity judgment remains unresolved.

## Internal self-review corrections

- Removed tentative necessity based only on named edit locations: existing facade initializers and the two documentation files are helpful context, while their mandatory destinations and future content are task-backed.
- Kept exact source identity and native field/range facts repository-backed; task language about the new behavior was not used to assert that it already exists.
- Did not require old test files merely because new focused/regression tests are requested. Retained actual pytest/coverage configuration as the required test convention; existing tests remain helpful examples.
- Separated function, class and parent-relative method provenance into distinct units, while keeping each coherent native identity basis together.
- Added complete source-code/package-contract alternatives. On a second minimality audit, demoted the grounding consumer and containment-helper implementations: native class/method membership and parent information already support the required validation inference, so adding those examples was redundant. Enumerated minimal covers rather than unioning all positive resources.
- Demoted the existing UTF-8 extraction helper from an additional requirement: it supports a coordinate unit already supplied by the unavoidable function model in every complete materialization alternative.
- Demoted the named validation script's implementation from additional necessity because the complete documented profile supplies its command, scope, configuration retention and exit behavior; actual project settings remain necessary.
- Rejected the tempting assumption that native spans include decorators, and the stronger assumption that a containment validator authenticates arbitrary constructed fields. Recorded bounded limitations and sufficient retained-source validation routes.
- Audited task-only export/documentation alternatives explicitly: these obligations prescribe future destinations and semantics without requiring extra discovery of repository state. Current source contracts are still required for the complete task under other obligations.
- Kept cross-obligation reuse and recomputed indispensability from complete alternative combinations; REQUIRED union membership is not simultaneous task necessity.

## Deterministic validation and artifact scope

The standalone builder reads only sealed packet inputs and named C-R outputs. It enumerates minimal evidence covers, reconstructs statistics/Markdown and validates exact task/frame/cell/evidence/unit/alternative bindings. Independent-process replay verifies byte identity. Mutation tests exercise invalid identities, missing/duplicate cells, labels, spans, memberships, combinations, unions, intersections, hashes and overwrite refusal. See stage_c_r_validation.json for actual results and stage_c_r_hashes.json for scientific SHA-256 values. The hash manifest excludes itself to avoid self-reference; its own digest is recorded in the completion report. The operational .local handoff is outside every scientific hash/evidence scope.

Native content_identity and document_identity values are preserved as opaque packet identities. Raw UTF-8 text SHA-256 is recorded separately and is not substituted for the native content identity.

## Blindness attestation

| Access category | Accessed |
|---|---|
| repository_checkout | NO |
| Git_history_or_commands | NO |
| parent_directory | NO |
| sibling_workspaces | NO |
| PRIMARY_Stage_C_adjudication | NO |
| any_prior_gold | NO |
| retrieval_queries | NO |
| analyzed_terms | NO |
| rankings | NO |
| scores | NO |
| hint_inventories | NO |
| routing_artifacts | NO |
| treatment_arms | NO |
| treatment_results | NO |
| acquisition_costs | NO |
| reliability_protocol_or_results | NO |
| known_disagreement_propositions | NO |
| confirmation_data | NO |
| reserve_data | NO |
| external_web_information | NO |
| prior_Codex_session_content | NO |

NO denotes access to excluded external/case-experimental artifacts. Natural identifiers, source code, documentation and test text embedded in the original eligible resources were treated only as repository evidence, as the packet permits. No referenced paths were followed outside the packet. No retrieval/effectiveness analysis was performed.

## Exact support evidence

Offsets refer to decoded packet text in Unicode code points, zero-based and half-open. They are distinct from native PythonSourceRange UTF-8 byte-column coordinates. Each repository span is bound to its exact document/content identity in JSON.

### E0001 — task_text

Span [0, 209), lines 1–1. Provenance: sealed packet task_text.

````text
Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.
````

### E0002 — task_text

Span [209, 531), lines 2–2. Provenance: sealed packet task_text.

````text
Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.
````

### E0003 — task_text

Span [531, 752), lines 3–3. Provenance: sealed packet task_text.

````text
Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.
````

### E0004 — task_text

Span [752, 1105), lines 4–4. Provenance: sealed packet task_text.

````text
Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.
````

### E0005 — task_text

Span [1105, 1415), lines 5–5. Provenance: sealed packet task_text.

````text
Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.
````

### E0006 — task_text

Span [1415, 1702), lines 6–6. Provenance: sealed packet task_text.

````text
Preserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.
````

### E0007 — task_text

Span [1702, 1910), lines 7–7. Provenance: sealed packet task_text.

````text
Expose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.
````

### E0008 — task_text

Span [1910, 2158), lines 8–8. Provenance: sealed packet task_text.

````text
Add focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.
````

### E0009 — task_text

Span [2158, 2433), lines 9–9. Provenance: sealed packet task_text.

````text
Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.
````

### E0010 — task_text

Span [2433, 2668), lines 10–10. Provenance: sealed packet task_text.

````text
Validate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.
````

### E0011 — R158 src/devtools/context/python/modules/selection.py

Span [1665, 3471), lines 54–98. Provenance: sealed packet resources[158].text.

````text
def select_python_module_source_declarations(
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
    kind: PythonSourceDeclarationKind,
) -> PythonModuleSourceDeclarationSelection:
    """Select direct declarations by exact kind/name in one observed module.

    Consume canonical RI without a parallel parser or binding policy. Repeated
    declarations remain distinct; decorators and other bindings do not erase
    source facts. Native parse failures propagate without successful coverage.
    """
    if not declared_name.isidentifier():
        msg = "Source declaration name must be a Python identifier."
        raise ValueError(msg)
    if not isinstance(kind, PythonSourceDeclarationKind):
        msg = "Source declaration selection has an unsupported kind."
        raise TypeError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Source declaration module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    declarations: tuple[PythonDirectModuleDeclaration, ...] = (
        classes.classes
        if kind is PythonSourceDeclarationKind.CLASS
        else functions.declarations
    )
    return PythonModuleSourceDeclarationSelection(
        module,
        declared_name,
        kind,
        functions,
        classes,
        tuple(item for item in declarations if item.declared_name == declared_name),
    )
````

### E0012 — R154 src/devtools/context/python/modules/docs/overview.md

Span [3335, 5653), lines 54–87. Provenance: sealed packet resources[154].text.

````text
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

Localization's [direct import dependency adapter](../../../localization/docs/overview.md#direct-static-python-import-dependency-resources)
uses these exact interpretations as endpoints of existing resolved module-import
relations. Module and class/function seeds retain their native owner module;
method seeds require a unique supplied owner-resource interpretation. Target
ownership is the actual interpreted resource, with ordinary/package distinctions
preserved. Membership supplies no import, export or candidate relation. The
adapter neither follows facades nor changes declaration/binding lookup policy.
````

### E0013 — R136 src/devtools/context/python/function/declarations.py

Span [4705, 5448), lines 146–167. Provenance: sealed packet resources[136].text.

````text
@dataclass(frozen=True, slots=True)
class PythonFunctionSubject:
    """Represent one analyzer-established snapshot-local function subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    declaration_ordinal: int
    derivation_definition_identity: str

    KIND: ClassVar[str] = "python-function"

    @property
    def identity(self) -> str:
        """Return a reproducible identity distinct from name and source range."""
        return _semantic_digest(
            _SUBJECT_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            self.derivation_definition_identity,
            self.resource_dependency_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
````

### E0014 — R136 src/devtools/context/python/function/declarations.py

Span [5450, 6597), lines 170–201. Provenance: sealed packet resources[136].text.

````text
@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationKnowledge:
    """Assert that one direct declaration occurrence declares one subject."""

    derivation_identity: str
    subject: PythonFunctionSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind

    PROPOSITION: ClassVar[str] = (
        PythonFunctionDeclarationDerivationDefinition.PROPOSITION
    )

    @property
    def identity(self) -> str:
        """Return reproducible identity for this separately referable result."""
        source_range = self.support.source_range
        return _semantic_digest(
            _KNOWLEDGE_IDENTITY_SEMANTICS,
            self.derivation_identity,
            self.subject.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            str(source_range.start_line),
            str(source_range.start_column_utf8),
            str(source_range.end_line),
            str(source_range.end_column_utf8),
            self.declared_name,
            self.declaration_kind.value,
            self.PROPOSITION,
        )
````

### E0015 — R136 src/devtools/context/python/function/declarations.py

Span [2324, 2963), lines 75–92. Provenance: sealed packet resources[136].text.

````text
@dataclass(frozen=True, slots=True)
class PythonModuleResourceDependency:
    """Retain the exact observed module resource consumed by a derivation."""

    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    @property
    def identity(self) -> str:
        """Return the deterministic identity of this direct semantic input."""
        return _semantic_digest(
            _DEPENDENCY_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )
````

### E0016 — R130 src/devtools/context/python/classes/declarations.py

Span [2463, 3196), lines 88–109. Provenance: sealed packet resources[130].text.

````text
@dataclass(frozen=True, slots=True)
class PythonClassSubject:
    """Identify one direct module-body class structurally, not at runtime."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-module-body-class"

    @property
    def identity(self) -> str:
        """Distinguish repeated names and classes in different resources."""
        return _digest(
            "python-class-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
````

### E0017 — R130 src/devtools/context/python/classes/declarations.py

Span [4252, 5470), lines 147–181. Provenance: sealed packet resources[130].text.

````text
@dataclass(frozen=True, slots=True)
class PythonClassDeclarationKnowledge:
    """Assert a direct module-body ``ClassDef`` occurrence and subject."""

    derivation_identity: str
    subject: PythonClassSubject
    support: PythonSourceOccurrence
    declared_name: str
    base_syntax: tuple[PythonClassBaseSyntax, ...]

    PROPOSITION: ClassVar[str] = "direct-module-body-classdef-declares-class-subject"

    @property
    def identity(self) -> str:
        """Identify this source-grounded declaration, distinct from its subject."""
        span = self.support.source_range
        return _digest(
            "python-class-declaration-knowledge-v1",
            self.PROPOSITION,
            self.derivation_identity,
            self.subject.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            *(_range_values(span)),
            self.declared_name,
            *(
                value
                for base in self.base_syntax
                for value in (
                    str(base.ordinal),
                    *_range_values(base.occurrence.source_range),
                    base.source_text,
                )
            ),
        )
````

### E0018 — R130 src/devtools/context/python/classes/declarations.py

Span [3198, 4026), lines 112–135. Provenance: sealed packet resources[130].text.

````text
@dataclass(frozen=True, slots=True)
class PythonMethodSubject:
    """Identify one direct method under a particular class subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    containing_class_subject_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-direct-class-body-method"

    @property
    def identity(self) -> str:
        """Use structural parent and ordinal, never a bare method name."""
        return _digest(
            "python-method-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.containing_class_subject_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
````

### E0019 — R130 src/devtools/context/python/classes/declarations.py

Span [5472, 6519), lines 184–211. Provenance: sealed packet resources[130].text.

````text
@dataclass(frozen=True, slots=True)
class PythonMethodDeclarationKnowledge:
    """Assert a direct class-body function syntax with one lexical parent."""

    derivation_identity: str
    subject: PythonMethodSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind
    containing_class: PythonClassDeclarationKnowledge

    PROPOSITION: ClassVar[str] = "direct-class-body-functiondef-declares-method-subject"

    @property
    def identity(self) -> str:
        """Identify this method occurrence and its direct class parent."""
        return _digest(
            "python-method-declaration-knowledge-v1",
            self.PROPOSITION,
            self.derivation_identity,
            self.subject.identity,
            self.containing_class.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            *_range_values(self.support.source_range),
            self.declared_name,
            self.declaration_kind.value,
        )
````

### E0020 — R131 src/devtools/context/python/classes/docs/overview.md

Span [1112, 4683), lines 24–80. Provenance: sealed packet resources[131].text.

````text
## Identity, provenance, and containment

The class subject identity depends on parser/derivation definition, snapshot,
the exact observed resource/content dependency, and class ordinal among direct
module-body classes. A method subject also depends on its containing class
subject and ordinal among that class's direct methods. Names are retained for
display and exact syntax knowledge, never used alone as subject identity. These
are structural repository subjects, not runtime Python `__qualname__` values.

Every class and method retains an exact source occurrence with one-based lines
and zero-based UTF-8 byte columns. The per-resource derivation retains its
repository and snapshot identities, content-bearing observed resource, parser
version, and bounded traversal semantics. A class retains the exact occurrence
and source text of each direct base expression as **syntax**. A separate
derivation assesses possible repository class targets without changing the
original declaration.
AST declaration spans begin at `class`/`def`/`async def`, excluding preceding
decorator lines. Decorators do not erase class or direct method declaration knowledge and do
not classify descriptor or runtime behavior. Exact source grounding may select
these native subjects even for staticmethod, classmethod or arbitrary method
decorators. Subject identity does not identify the runtime object after
decorators, descriptors, metaclass behavior or rebinding; binding-oriented
Reference/base checks retain their separate conservative semantics.

```text
method occurrence resource ──→ observed module resource
method direct lexical parent ──→ class declaration
class occurrence resource  ──→ observed module resource
class direct lexical parent ──→ Module.body scope (bounded analysis claim)
```

`PythonMethodDeclarationKnowledge.containing_class` is the one canonical direct
lexical-parent link. Both directions navigate it; no reverse fact is derived.
`build_python_class_method_containment_view(snapshot, aggregate=...)` validates
native analyses against the retained snapshot without reparsing or file reads.
It exposes `module_body_classes_in(address)`, `direct_methods_of(class)`,
`containing_class_of(method)`, and `occurrence_resource_of(class_or_method)`.
An analyzed resource or class can return an empty tuple. An unselected resource
or declaration raises an error rather than implying absence.

Successful coverage counts supported classes/methods, separately counted
module-body functions handled by existing function RI, and encountered class
or function syntax outside this analysis's positive scope. Excluded occurrences
retain exact source locations. Syntax failure publishes no successful coverage.
Local classes, nested classes, nested functions, methods of excluded classes,
and indirect declarations under control-flow statements are not positive facts.
Absence in this bounded result says nothing about runtime classes or methods.

Repository Intelligence records this structure. Retrieval may later decide
whether it is relevant to an InformationNeed. Context Planning may later choose
a class or method representation for disclosure. Neither decision is made here.
The current qualified Reference/direct Call analyzer still resolves only its
existing imported-function forms. Future method References/Calls need separate
qualified attribute and receiver/type resolution. The current resource-level
Personalized PageRank graph does not consume these new facts. A future graph
view may project class, method, base, and Reference relationships prospectively.
````

### E0021 — R130 src/devtools/context/python/classes/declarations.py

Span [9219, 14928), lines 291–432. Provenance: sealed packet resources[130].text.

````text
def derive_python_class_method_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonClassMethodAnalysis:
    """Derive only direct module classes and their direct sync/async methods."""
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = PythonClassMethodDerivationDefinition(
        analyzer_semantics_version=_ANALYZER_SEMANTICS_VERSION,
        parser_implementation=sys.implementation.name,
        parser_runtime_version=platform.python_version(),
        grammar_feature_version=_GRAMMAR_FEATURE_VERSION,
    )
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonClassMethodDerivation(definition, dependency)
    try:
        module = ast.parse(
            resource.content,
            filename=str(resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonClassMethodParseError(derivation, error) from error

    classes: list[PythonClassDeclarationKnowledge] = []
    methods: list[PythonMethodDeclarationKnowledge] = []
    supported_nodes: set[int] = set()
    module_functions: set[int] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            module_functions.add(id(node))
        if not isinstance(node, ast.ClassDef):
            continue
        supported_nodes.add(id(node))
        subject = PythonClassSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            derivation_definition_identity=definition.identity,
            declaration_ordinal=len(classes),
        )
        declaration = PythonClassDeclarationKnowledge(
            derivation_identity=derivation.identity,
            subject=subject,
            support=_occurrence(snapshot.id, resource.address, node),
            declared_name=node.name,
            base_syntax=tuple(
                PythonClassBaseSyntax(
                    ordinal=ordinal,
                    occurrence=_occurrence(snapshot.id, resource.address, base),
                    source_text=_base_source_text(resource.content, base),
                )
                for ordinal, base in enumerate(node.bases)
            ),
        )
        classes.append(declaration)
        method_ordinal = 0
        for child in node.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            supported_nodes.add(id(child))
            method_subject = PythonMethodSubject(
                snapshot_id=snapshot.id,
                resource_dependency_identity=dependency.identity,
                derivation_definition_identity=definition.identity,
                containing_class_subject_identity=subject.identity,
                declaration_ordinal=method_ordinal,
            )
            methods.append(
                PythonMethodDeclarationKnowledge(
                    derivation_identity=derivation.identity,
                    subject=method_subject,
                    support=_occurrence(snapshot.id, resource.address, child),
                    declared_name=child.name,
                    declaration_kind=(
                        PythonFunctionDeclarationKind.ASYNCHRONOUS
                        if isinstance(child, ast.AsyncFunctionDef)
                        else PythonFunctionDeclarationKind.SYNCHRONOUS
                    ),
                    containing_class=declaration,
                ),
            )
            method_ordinal += 1

    excluded_function_kind = (
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
    )
    excluded = tuple(
        sorted(
            (
                PythonExcludedClassMethodSyntax(
                    kind=(
                        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                        if isinstance(node, ast.ClassDef)
                        else excluded_function_kind
                    ),
                    occurrence=_occurrence(snapshot.id, resource.address, node),
                )
                for node in ast.walk(module)
                if isinstance(
                    node,
                    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and id(node) not in supported_nodes
                and id(node) not in module_functions
            ),
            key=lambda item: (
                item.occurrence.source_range.start_line,
                item.occurrence.source_range.start_column_utf8,
                item.kind.value,
            ),
        ),
    )
    return PythonClassMethodAnalysis(
        derivation=derivation,
        classes=tuple(classes),
        methods=tuple(methods),
        excluded_syntax=excluded,
        coverage=PythonClassMethodCoverage(
            derivation_identity=derivation.identity,
            class_count=len(classes),
            method_count=len(methods),
            module_body_function_count=len(module_functions),
            excluded_class_count=sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in excluded
            ),
            excluded_function_count=sum(
                item.kind is excluded_function_kind for item in excluded
            ),
        ),
    )
````

### E0022 — R129 src/devtools/context/python/classes/containment.py

Span [845, 3265), lines 30–84. Provenance: sealed packet resources[129].text.

````text
@dataclass(frozen=True, slots=True)
class PythonClassMethodContainmentView:
    """Navigate one validated selection without adding duplicate RI facts."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    aggregate: PythonClassMethodAnalysisAggregate

    def module_body_classes_in(
        self,
        resource_address: RepositoryResourceAddress,
    ) -> tuple[PythonClassDeclarationKnowledge, ...]:
        """Return supported direct classes; reject an unselected resource."""
        for analysis in self.aggregate.analyses:
            if analysis.derivation.dependency.resource.address == resource_address:
                return analysis.classes
        msg = "Resource was not selected for class/method analysis."
        raise ValueError(msg)

    def direct_methods_of(
        self,
        class_declaration: PythonClassDeclarationKnowledge,
    ) -> tuple[PythonMethodDeclarationKnowledge, ...]:
        """Return direct methods in class source order, including empty."""
        for analysis in self.aggregate.analyses:
            if class_declaration in analysis.classes:
                return tuple(
                    item
                    for item in analysis.methods
                    if item.containing_class == class_declaration
                )
        msg = "Class declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def containing_class_of(
        self,
        method: PythonMethodDeclarationKnowledge,
    ) -> PythonClassDeclarationKnowledge:
        """Return the method's one established direct lexical parent."""
        for analysis in self.aggregate.analyses:
            if method in analysis.methods:
                return method.containing_class
        msg = "Method declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def occurrence_resource_of(
        self,
        declaration: PythonClassDeclarationKnowledge | PythonMethodDeclarationKnowledge,
    ) -> RepositoryResourceOccurrence:
        """Return where a selected class or method occurs, not its lexical parent."""
        for analysis in self.aggregate.analyses:
            if declaration in analysis.classes or declaration in analysis.methods:
                return analysis.derivation.dependency.resource
        msg = "Declaration does not belong to the selected analyses."
        raise ValueError(msg)
````

### E0023 — R129 src/devtools/context/python/classes/containment.py

Span [3267, 8249), lines 87–191. Provenance: sealed packet resources[129].text.

````text
def build_python_class_method_containment_view(  # noqa: C901
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonClassMethodAnalysisAggregate,
) -> PythonClassMethodContainmentView:
    """Check native facts against the same retained observed snapshot."""
    if not aggregate.analyses:
        msg = "Class/method containment requires at least one resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Class/method containment repeats a resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Class/method analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Class/method analysis uses stale observed resource content."
            raise ValueError(msg)
        coverage = analysis.coverage
        if (
            coverage.derivation_identity != derivation.identity
            or coverage.class_count != len(analysis.classes)
            or coverage.method_count != len(analysis.methods)
            or coverage.excluded_class_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in analysis.excluded_syntax
            )
            or coverage.excluded_function_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
                for item in analysis.excluded_syntax
            )
        ):
            msg = "Class/method coverage differs from its analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.classes):
            class_subject = declaration.subject
            if (
                declaration.derivation_identity != derivation.identity
                or class_subject.snapshot_id != snapshot.id
                or class_subject.resource_dependency_identity != dependency.identity
                or class_subject.derivation_definition_identity
                != derivation.definition.identity
                or class_subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
                or any(
                    base.ordinal != base_ordinal
                    or base.occurrence.snapshot_id != snapshot.id
                    or base.occurrence.resource_address != address
                    for base_ordinal, base in enumerate(declaration.base_syntax)
                )
            ):
                msg = "Class declaration differs from its resource analysis."
                raise ValueError(msg)
        method_ordinals: dict[str, int] = {}
        for method in analysis.methods:
            parent = method.containing_class
            ordinal = method_ordinals.get(parent.subject.identity, 0)
            method_subject = method.subject
            if (
                parent not in analysis.classes
                or method.derivation_identity != derivation.identity
                or method_subject.snapshot_id != snapshot.id
                or method_subject.resource_dependency_identity != dependency.identity
                or method_subject.derivation_definition_identity
                != derivation.definition.identity
                or method_subject.containing_class_subject_identity
                != parent.subject.identity
                or method_subject.declaration_ordinal != ordinal
                or method.support.snapshot_id != snapshot.id
                or method.support.resource_address != address
            ):
                msg = "Method declaration differs from its class or resource."
                raise ValueError(msg)
            method_ordinals[parent.subject.identity] = ordinal + 1
        if any(
            item.occurrence.snapshot_id != snapshot.id
            or item.occurrence.resource_address != address
            for item in analysis.excluded_syntax
        ):
            msg = "Excluded syntax differs from its observed resource."
            raise ValueError(msg)
    return PythonClassMethodContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
````

### E0024 — R099 src/devtools/context/localization/grounding/resolve.py

Span [7427, 9271), lines 215–266. Provenance: sealed packet resources[99].text.

````text
def _ground_method(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectMethodLocator,
) -> AnchorGrounding:
    parent = locator.containing_class
    if (
        parent.subject.snapshot_id != snapshot.id
        or parent.support.snapshot_id != snapshot.id
    ):
        msg = "Direct method locator contains a foreign or stale class declaration."
        raise ValueError(msg)
    address = parent.support.resource_address
    try:
        analysis = derive_python_class_method_declarations(
            snapshot,
            resource_address=address,
        )
    except PythonClassMethodParseError:
        return _account(
            request,
            GroundingResolver.PYTHON_METHOD_CONTAINMENT,
            (),
            (),
            None,
            AnchorGroundingDisposition.UNSUPPORTED,
            "Observed Python source cannot be analyzed for direct methods.",
        )
    view = build_python_class_method_containment_view(
        snapshot,
        aggregate=PythonClassMethodAnalysisAggregate((analysis,)),
    )
    if parent not in analysis.classes:
        msg = "Direct method locator contains a stale or foreign class declaration."
        raise ValueError(msg)
    methods = tuple(
        item
        for item in view.direct_methods_of(parent)
        if item.declared_name == locator.declared_name
    )
    candidates = tuple(AnchorGroundingCandidate(item, analysis) for item in methods)
    return _account(
        request,
        GroundingResolver.PYTHON_METHOD_CONTAINMENT,
        candidates,
        (analysis,),
        None,
        _candidate_disposition(candidates),
        "Exact direct class-body method syntax matched in the observed class."
        if methods
        else "No exact direct method syntax matched in the observed class.",
    )
````

### E0025 — R123 src/devtools/context/planning/plan.py

Span [514, 1458), lines 19–49. Provenance: sealed packet resources[123].text.

````text
class PlannedDisclosure(Protocol):
    """One concrete, purpose-bound representation chosen by a caller."""

    @property
    def purpose(self) -> str:
        """Return the information purpose served by this choice."""
        ...

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the observed repository state this choice addresses."""
        ...

    @property
    def repository_id(self) -> RepositoryId:
        """Return the nominal repository identity."""
        ...

    @property
    def representation(self) -> str:
        """Name the concrete, implemented disclosure form."""
        ...

    @property
    def identity(self) -> str:
        """Identify this exact disclosure choice and its native support."""
        ...

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Realize the choice from retained, matching snapshot state."""
        ...
````

### E0026 — R123 src/devtools/context/planning/plan.py

Span [1894, 2848), lines 66–86. Provenance: sealed packet resources[123].text.

````text
    def __post_init__(self) -> None:
        """Reject mixed purposes, snapshots, and repeated choices."""
        if not self.purpose.strip():
            msg = "Disclosure plan purpose must not be blank."
            raise ValueError(msg)
        if not self.disclosures:
            msg = "Disclosure plan needs at least one explicit disclosure."
            raise ValueError(msg)
        if any(
            item.purpose != self.purpose
            or item.snapshot_id != self.snapshot_id
            or item.repository_id != self.repository_id
            for item in self.disclosures
        ):
            msg = (
                "Disclosure plan contains an incompatible purpose or repository state."
            )
            raise ValueError(msg)
        if len({item.identity for item in self.disclosures}) != len(self.disclosures):
            msg = "Disclosure plan repeats an identical disclosure choice."
            raise ValueError(msg)
````

### E0027 — R123 src/devtools/context/planning/plan.py

Span [2849, 3377), lines 88–102. Provenance: sealed packet resources[123].text.

````text
    @property
    def identity(self) -> str:
        """Identify purpose, applicability, ordered choices, and optional lineage."""
        return _digest(
            "explicit-repository-disclosure-plan-v1",
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            self.preceding_plan_identity or "",
            *(
                value
                for item in self.disclosures
                for value in (item.representation, item.identity)
            ),
        )
````

### E0028 — R181 src/devtools/context/repository/snapshot.py

Span [1594, 2018), lines 52–61. Provenance: sealed packet resources[181].text.

````text
    def resource_at(
        self,
        address: RepositoryResourceAddress,
    ) -> RepositoryResourceOccurrence:
        """Return the observed occurrence at one exact requested address."""
        for resource in self.resources:
            if resource.address == address:
                return resource
        msg = f"Repository snapshot does not contain resource address: {address}."
        raise ValueError(msg)
````

### E0029 — R180 src/devtools/context/repository/resource.py

Span [2019, 2308), lines 64–72. Provenance: sealed packet resources[180].text.

````text
@dataclass(frozen=True, slots=True)
class RepositoryResourceOccurrence:
    """Retain one addressed text occurrence and its independent content identity."""

    address: RepositoryResourceAddress
    content_identity: ContentIdentity
    content: str
    encoding: str
    byte_size: int
````

### E0030 — R180 src/devtools/context/repository/resource.py

Span [1568, 2017), lines 49–61. Provenance: sealed packet resources[180].text.

````text
@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify decoded UTF-8 text independently of its repository address."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Content identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value
````

### E0031 — R122 src/devtools/context/planning/materialization.py

Span [2392, 3297), lines 73–92. Provenance: sealed packet resources[122].text.

````text
def materialize_disclosure_plan(
    *,
    plan: DisclosurePlan,
    snapshot: RepositorySnapshot,
) -> ContextDisclosure:
    """Realize every choice against retained state, without reacquisition."""
    if snapshot.id != plan.snapshot_id or snapshot.repository_id != plan.repository_id:
        msg = "Disclosure plan does not apply to the supplied repository snapshot."
        raise DisclosureMaterializationError(msg)
    items: list[MaterializedDisclosureItem] = []
    for option in plan.disclosures:
        item = option.materialize(snapshot)
        if (
            item.option_identity != option.identity
            or item.representation != option.representation
        ):
            msg = "Materialized item differs from its planned disclosure."
            raise DisclosureMaterializationError(msg)
        items.append(item)
    return ContextDisclosure(plan=plan, items=tuple(items))
````

### E0032 — R122 src/devtools/context/planning/materialization.py

Span [657, 1014), lines 24–33. Provenance: sealed packet resources[122].text.

````text
@dataclass(frozen=True, slots=True)
class MaterializedDisclosureItem:
    """Keep rendered information separate from its native supporting value."""

    option_identity: str
    representation: str
    resource_addresses: tuple[RepositoryResourceAddress, ...]
    content_identities: tuple[ContentIdentity, ...]
    text: str
    native_provenance: object
````

### E0033 — R122 src/devtools/context/planning/materialization.py

Span [1016, 2390), lines 36–70. Provenance: sealed packet resources[122].text.

````text
@dataclass(frozen=True, slots=True)
class ContextDisclosure:
    """Retain one realized item per ordered plan choice."""

    plan: DisclosurePlan
    items: tuple[MaterializedDisclosureItem, ...]

    def __post_init__(self) -> None:
        """Keep the realized account aligned with its explicit plan."""
        if len(self.items) != len(self.plan.disclosures) or any(
            item.option_identity != option.identity
            or item.representation != option.representation
            for item, option in zip(self.items, self.plan.disclosures, strict=True)
        ):
            msg = "Context disclosure items do not match their planned choices."
            raise DisclosureMaterializationError(msg)

    @property
    def identity(self) -> str:
        """Identify exact realized text and source identities under the plan."""
        return _digest(
            "materialized-repository-context-disclosure-v1",
            self.plan.identity,
            *(
                value
                for item in self.items
                for value in (
                    item.option_identity,
                    item.representation,
                    *(str(address) for address in item.resource_addresses),
                    *(str(content) for content in item.content_identities),
                    item.text,
                )
            ),
        )
````

### E0034 — R136 src/devtools/context/python/function/declarations.py

Span [1628, 2058), lines 51–63. Provenance: sealed packet resources[136].text.

````text
@dataclass(frozen=True, slots=True)
class PythonSourceRange:
    """Locate Python syntax using the stdlib AST coordinate contract.

    Lines are one-based. Columns are zero-based UTF-8 byte offsets. The end
    position is exclusive. This is a local Python-parser coordinate value, not
    a universal source-location convention.
    """

    start_line: int
    start_column_utf8: int
    end_line: int
    end_column_utf8: int
````

### E0035 — R136 src/devtools/context/python/function/declarations.py

Span [2060, 2322), lines 66–72. Provenance: sealed packet resources[136].text.

````text
@dataclass(frozen=True, slots=True)
class PythonSourceOccurrence:
    """Anchor one declaration occurrence in observed snapshot source."""

    snapshot_id: RepositorySnapshotId
    resource_address: RepositoryResourceAddress
    source_range: PythonSourceRange
````

### E0036 — R136 src/devtools/context/python/function/declarations.py

Span [8627, 11870), lines 264–348. Provenance: sealed packet resources[136].text.

````text
def derive_python_function_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonFunctionDeclarationAnalysis:
    """Derive declarations from one explicitly selected observed resource.

    A returned value accounts exhaustively for the bounded declaration scope.
    A syntax failure raises :class:`PythonModuleParseError` and returns no
    coverage or declaration knowledge. Omitting ``resource_address`` is a
    compatibility path valid only for a snapshot containing exactly one
    resource.
    """
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = _current_definition()
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonFunctionDeclarationDerivation(
        definition=definition,
        dependency=dependency,
    )
    try:
        module = ast.parse(
            dependency.resource.content,
            filename=str(dependency.resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonModuleParseError(derivation=derivation, error=error) from error

    declarations: list[PythonFunctionDeclarationKnowledge] = []
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        declaration_ordinal = len(declarations)
        subject = PythonFunctionSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            declaration_ordinal=declaration_ordinal,
            derivation_definition_identity=definition.identity,
        )
        source_occurrence = PythonSourceOccurrence(
            snapshot_id=snapshot.id,
            resource_address=dependency.resource.address,
            source_range=PythonSourceRange(
                start_line=node.lineno,
                start_column_utf8=node.col_offset,
                end_line=cast("int", node.end_lineno),
                end_column_utf8=cast("int", node.end_col_offset),
            ),
        )
        declaration_kind = (
            PythonFunctionDeclarationKind.ASYNCHRONOUS
            if isinstance(node, ast.AsyncFunctionDef)
            else PythonFunctionDeclarationKind.SYNCHRONOUS
        )
        declarations.append(
            PythonFunctionDeclarationKnowledge(
                derivation_identity=derivation.identity,
                subject=subject,
                support=source_occurrence,
                declared_name=node.name,
                declaration_kind=declaration_kind,
            ),
        )

    immutable_declarations = tuple(declarations)
    return PythonFunctionDeclarationAnalysis(
        derivation=derivation,
        declarations=immutable_declarations,
        coverage=PythonFunctionDeclarationCoverage(
            derivation_identity=derivation.identity,
            declaration_count=len(immutable_declarations),
        ),
    )
````

### E0037 — R130 src/devtools/context/python/classes/declarations.py

Span [15808, 16381), lines 458–473. Provenance: sealed packet resources[130].text.

````text
def _occurrence(
    snapshot_id: RepositorySnapshotId,
    resource_address: RepositoryResourceAddress,
    node: ast.AST,
) -> PythonSourceOccurrence:
    located = cast("_LocatedAstNode", node)
    return PythonSourceOccurrence(
        snapshot_id=snapshot_id,
        resource_address=resource_address,
        source_range=PythonSourceRange(
            start_line=located.lineno,
            start_column_utf8=located.col_offset,
            end_line=cast("int", located.end_lineno),
            end_column_utf8=cast("int", located.end_col_offset),
        ),
    )
````

### E0038 — R124 src/devtools/context/planning/rendering.py

Span [549, 1355), lines 23–42. Provenance: sealed packet resources[124].text.

````text
def render_context_disclosure(
    disclosure: ContextDisclosure,
) -> RenderedContextDisclosure:
    """Render planned item order without reselecting or changing information."""
    parts = [
        "Repository Context disclosure\n",
        f"Purpose: {disclosure.plan.purpose}\n",
        f"Plan identity: {disclosure.plan.identity}\n",
        f"Snapshot identity: {disclosure.plan.snapshot_id}\n",
        f"Items: {len(disclosure.items)}\n",
    ]
    for ordinal, item in enumerate(disclosure.items, start=1):
        parts.extend(
            (
                f"\nDisclosure item {ordinal}: {item.representation}\n",
                f"Option identity: {item.option_identity}\n",
                item.text,
            ),
        )
    return RenderedContextDisclosure(disclosure, "".join(parts))
````

### E0039 — R124 src/devtools/context/planning/rendering.py

Span [1357, 2316), lines 45–70. Provenance: sealed packet resources[124].text.

````text
def assemble_context_disclosure_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedContextDisclosure,
) -> ModelRequest:
    """Place realized Context after the unchanged task and copy all settings."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(prompt_content, role=task_request.prompt.role),
    )
````

### E0040 — R064 pyproject.toml

Span [610, 1032), lines 34–56. Provenance: sealed packet resources[64].text.

````text

testpaths = ["tests"]
addopts = [
    "--strict-config",
    "--strict-markers",
    "--cov=devtools",
    "--cov-branch",
    "--cov-report=term-missing",
    "--cov-fail-under=100",
]
markers = [
    "live_codex: opt-in test that contacts the locally authenticated Codex CLI",
]

[tool.coverage.run]
branch = true
source = ["devtools"]

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 100
````

### E0041 — R064 pyproject.toml

Span [1228, 1368), lines 73–78. Provenance: sealed packet resources[64].text.

````text
[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests", "experiments"]
explicit_package_bases = true
mypy_path = ["src"]
````

### E0042 — R060 docs/development/validation.md

Span [26, 1423), lines 3–30. Provenance: sealed packet resources[60].text.

````text
## Protected development test profile

Run the ordinary repository test suite with:

```text
uv run python scripts/validate_development.py
```

The command runs pytest against `tests/` and ignores `tests/experiments/` before
recursive collection. The experiment test tree contains retained replay and
outcome-dependent tests alongside other experimental checks, so the protected
profile excludes the tree by its repository role rather than inspecting test
names, retained data, or confirmation outcomes to decide what to run. The
ordinary production, unit, integration, and operational-script tests outside
that tree remain in scope. Case 0003 additionally named its capture and
synthetic protocol tests explicitly for that experiment; the general profile
does not carry those case-specific additions.

The profile uses the project pytest configuration without overriding it. This
preserves strict configuration and marker checks, branch coverage, and the
100% production coverage threshold. Pytest's exit code is returned by the
command, so a failed test or coverage gate fails the command.

This profile validates development behavior. It does not validate confirmation
judgments or retained outcomes. Confirmation validation is a separate activity
that requires explicit authorization and a separately reviewed invocation.
Never remove the experiment-tree exclusion to make this profile pass.
````

### E0043 — R060 docs/development/validation.md

Span [1423, 1787), lines 31–44. Provenance: sealed packet resources[60].text.

````text
## Other quality gates

The protected command runs tests only. Run the applicable static checks as
separate commands:

```text
uv run ruff check .
uv run ruff format --check
uv run mypy
git diff --check
```

When changes are staged, also run `git diff --cached --check`. This profile is
test selection, not a general validation pipeline or confirmation mechanism.
````

### E0044 — R123 src/devtools/context/planning/plan.py

Span [1460, 3377), lines 52–102. Provenance: sealed packet resources[123].text.

````text
@dataclass(frozen=True, slots=True)
class DisclosurePlan:
    """Identify an ordered choice of disclosures for one explicit purpose.

    Construction is caller-directed. It neither retrieves nor estimates
    relevance, cost, or sufficiency.
    """

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    disclosures: tuple[PlannedDisclosure, ...]
    preceding_plan_identity: str | None = None

    def __post_init__(self) -> None:
        """Reject mixed purposes, snapshots, and repeated choices."""
        if not self.purpose.strip():
            msg = "Disclosure plan purpose must not be blank."
            raise ValueError(msg)
        if not self.disclosures:
            msg = "Disclosure plan needs at least one explicit disclosure."
            raise ValueError(msg)
        if any(
            item.purpose != self.purpose
            or item.snapshot_id != self.snapshot_id
            or item.repository_id != self.repository_id
            for item in self.disclosures
        ):
            msg = (
                "Disclosure plan contains an incompatible purpose or repository state."
            )
            raise ValueError(msg)
        if len({item.identity for item in self.disclosures}) != len(self.disclosures):
            msg = "Disclosure plan repeats an identical disclosure choice."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Identify purpose, applicability, ordered choices, and optional lineage."""
        return _digest(
            "explicit-repository-disclosure-plan-v1",
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            self.preceding_plan_identity or "",
            *(
                value
                for item in self.disclosures
                for value in (item.representation, item.identity)
            ),
        )
````

### E0045 — R139 src/devtools/context/python/function/materialization.py

Span [3649, 4784), lines 104–133. Provenance: sealed packet resources[139].text.

````text
def _extract_source_segment(content: str, source_range: PythonSourceRange) -> str:
    """Extract one half-open range using UTF-8 byte-column coordinates."""
    if (
        source_range.start_line,
        source_range.start_column_utf8,
    ) > (
        source_range.end_line,
        source_range.end_column_utf8,
    ):
        msg = "Source occurrence range ends before it starts."
        raise PythonFunctionSourceMaterializationError(msg)

    encoded_lines = tuple(
        line.encode("utf-8") for line in content.splitlines(keepends=True)
    )
    start = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.start_line,
        column=source_range.start_column_utf8,
    )
    end = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.end_line,
        column=source_range.end_column_utf8,
    )
    try:
        return content.encode("utf-8")[start:end].decode("utf-8")
    except UnicodeDecodeError as error:
        msg = "Source occurrence columns do not fall on UTF-8 character boundaries."
        raise PythonFunctionSourceMaterializationError(msg) from error
````

### E0046 — R139 src/devtools/context/python/function/materialization.py

Span [4786, 5535), lines 136–152. Provenance: sealed packet resources[139].text.

````text
def _absolute_byte_offset(
    encoded_lines: tuple[bytes, ...],
    *,
    line_number: int,
    column: int,
) -> int:
    """Translate one AST line/byte-column pair into an absolute byte offset."""
    if line_number < 1 or line_number > len(encoded_lines):
        msg = "Source occurrence line is outside the observed content."
        raise PythonFunctionSourceMaterializationError(msg)

    line = encoded_lines[line_number - 1]
    source_line = line.rstrip(b"\r\n")
    if column < 0 or column > len(source_line):
        msg = "Source occurrence column is outside the observed source line."
        raise PythonFunctionSourceMaterializationError(msg)
    return sum(len(previous) for previous in encoded_lines[: line_number - 1]) + column
````

### E0047 — R000 AGENTS.md

Span [10325, 11978), lines 220–252. Provenance: sealed packet resources[0].text.

````text
## Documentation and validation

For every source change, perform a documentation-impact check: package docs,
architecture docs, documentation map, backlog, and historical ledger as
applicable. Update behavior claims where behavior changes. Update authoritative
architecture only for actual architectural changes. Do not rewrite historical
records as if older terminology never existed.

The canonical protected development test profile is documented in
[docs/development/validation.md](docs/development/validation.md). Run it with:

```text
uv run python scripts/validate_development.py
```

It excludes `tests/experiments/` before collection to avoid retained
outcome-dependent tests. Keep the configured production branch-coverage gate.
Run Ruff, formatting, mypy, and diff checks separately as documented. Do not
run confirmation validation or live model/Docker tests for ordinary work;
those require explicit authorization and are reported separately.

For read-only audits: do not fix while inspecting; list evidence inspected,
separate fact from interpretation, report findings by severity, and do not
stage or commit.

At the end of a substantial Codex task, overwrite `.local/codex-result.md`
with the same substantive completion report provided in the terminal response.
Create `.local/` if needed. This is a local, ephemeral, non-authoritative
handoff; it is ignored by Git and must never be committed. Do not use it as the
only location for durable architectural decisions or empirical evidence. Put
those in their proper authoritative documentation, ADR, backlog record,
research artifact, experiment record, or production implementation.
````

### E0048 — R000 AGENTS.md

Span [3186, 4568), lines 65–90. Provenance: sealed packet resources[0].text.

````text
## Reuse canonical primitives and substrates

If the repository provides a canonical primitive or substrate for a
responsibility, higher layers must use it unless an explicit architectural
decision justifies bypassing it.

- Use `devtools.core.time` values such as `Timestamp` for framework timestamps;
  do not independently use `datetime.now()`, `datetime.utcnow()`, or similar
  wall-clock construction outside the time domain or a documented external
  boundary.
- Use domain semantic identity wrappers built on `devtools.core.identity.Identity`
  when the repository owns that identity concept. Do not invent parallel UUID
  strings for the same semantic identity.
- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do
  not reimplement path normalization, repository-root resolution, or existing
  containment behavior.
- Use `devtools.resources.commands` for managed subprocess work. Higher domains must
  not call direct `subprocess` or `asyncio` subprocess APIs without explicit
  architectural justification.
- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded
  reads, and atomic writes. Do not recreate those semantics in Tools, Context,
  Agents, or experiments.

These rules do not prohibit unrelated external UUIDs, timestamps, paths, or
processes at genuine external boundaries; verify ownership first.
````

### E0049 — R002 docs/architecture.md

Span [65307, 72373), lines 1011–1122. Provenance: sealed packet resources[2].text.

````text
## Accepted Context and disclosure semantics

The [heterogeneous evidence admission and recovery investigation](research/heterogeneous-context-admission-and-recovery.md)
and ADR-0004's 2026-10-02 refinement selected an **unimplemented** direction:
evidence-guided option admission inside Context Planning, with a
separate observable decision/coverage account alongside the selected plan.
Native resource, declaration, occurrence and relationship identities remain
referents; concrete representations consume disclosure capacity. There is no
mandatory intermediate file-admission service or universal evidence score.

ADR-0005 now separates obligation resolution from representation admission. The
earlier question-lane score floors/capacity weights remain historical development
research, not the next implementation policy. Context retains concrete option
choice, exact materialization, representation-relative coverage and capacity;
Localization supplies obligation witnesses and unresolved requirements.

Bounded planning assessments distinguish integrity, applicability, cost,
currently available requested representations and open questions. They do not
establish general Context sufficiency. Requests may acquire information for a
question or expand an exact target; obligation acquisition is interpreted by
Localization and exact representation expansion by Context. Context
plans/materializes, while
Agent/orchestration decides successive attempts, validation, recovery limits
and escalation. Previous plan lineage does not establish current availability.
This accepts request semantics, not a transport, Tool registry or recovery loop.

[ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
accepts the post-ranking Context layer. Context compilation is conditional
information composition, not top-K retrieval or automatic budget filling.
Disclosure planning couples candidate and representation choice and reasons
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, and multidimensional cost. It selects information rather than prompt
strings. A DisclosureOption is a future purpose-relative possibility for
exposing information through a selected representation or transformation, with
origin, form, fidelity, cost, and provenance kept semantically distinct.
Source-preserving material, existing knowledge projections, and synthesized
semantic assertions are distinct origins. A new
repository-relative assertion can be ADR-0002 DerivedKnowledge; a purpose-
relative Context synthesis remains explicit and provenance-bearing without
automatic promotion to repository intelligence. Composite provenance-preserving
representations are permitted.

DisclosurePlan, ContextDisclosure, and ModelRequest remain distinct:

```text
InformationNeed -> DisclosurePlan -> materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
```

The Plan is an immutable selected-information decision; the Disclosure is an
immutable realized information artifact under/reference to that plan; the
ModelRequest is a consumer-specific presentation. Materialization faithfully
realizes the selected representation and may perform an explicitly planned
semantic transformation or lossy synthesis. It cannot silently re-plan, invent
a materially different synthesis, or present inapplicable information as
current. Assembly arranges already-realized disclosure and must not introduce
new semantic assertions through formatting, placement, or budget handling.
Planning and possession of a disclosure are not disclosure/presentation
authority.

The implemented DisclosurePlan is intentionally narrower than this accepted
general concept: a caller chooses its purpose and concrete options. Supported
forms are a qualified Python Reference fact with exact source and target
declaration, and an explicit whole observed resource. The plan is bound to
one snapshot, preserves ordered choices and optional preceding-plan lineage,
and materializes to a ContextDisclosure with native provenance. Retrieval
rank may inform a caller but does not automatically choose a representation,
disclosure quantity, or claim of sufficiency. ADR-0004 continues to govern
future planning, cost, and disclosure semantics. The
[Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
motivates this boundary and a separate query-conditioned structural-ranking
baseline; its automatic planner, graph weighting, and fusion recommendations
are not implemented here.

Every disclosure stage preserves semantic strength: representation selection,
projection, synthesis, compression, materialization, disclosure realization,
and assembly must not turn a possible result into a definite one, a partial set
into an exhaustive set, an approximation into an exact assertion, or a
preserved disagreement into one truth unless an identified semantically capable
process establishes the stronger conclusion. Source semantics, support,
assumptions/scope, conflict state, and semantic-result coverage bound what may
be represented.

This architecture distinguishes repository history, disclosure history, and
Conversation history. Current Conversation ownership remains
`agents.conversation`; the sparse `context` namespace does not own a current
compiler or former Session semantics. Model-input assembly is a separate future
concern: it determines how a selected disclosure is realized for a model, while
disclosure planning determines what information should be available. Context
budgets are ceilings rather than targets, and repeated acquisition remains above
deterministic retrieval/compilation rather than inside Runtime.

Coherence concerns intelligible meaningful units and consumer reconstruction
burden, not source contiguity. Authority is claim-/purpose-relative evidence,
not a universal source hierarchy; relevant applicable conflicts remain
preservable rather than being silently arbitrated. Concrete coverage, fidelity,
authority, uncertainty, completeness, conflict, coherence, semantic-
transformation/synthesis validation, materialization, cache, assembly, and
evaluation mechanisms remain unimplemented.

The breadth gate makes the broader Context problem concrete: use established
facts and source spans to choose supported representations for a purpose.
The first cross-resource slice accepts a caller-chosen qualified Reference fact
and faithfully discloses its exact occurrence and target declaration. Future
planning may choose among facts, spans, pointers, and whole resources under
applicable constraints. Later or refined InformationNeeds may cause further
retrieval and disclosure, but this slice does not establish a recovery
guarantee or progressive controller. Lexical windows and structural supports are
possible localization inputs, not demonstrated disclosure policies or
permission to synthesize stronger claims than their provenance supports.
````

### E0050 — R002 docs/architecture.md

Span [25282, 29060), lines 421–471. Provenance: sealed packet resources[2].text.

````text
The first bounded derivation consumes one caller-selected resource occurrence
from that observed state and uses stdlib `ast` with explicit Python 3.12
grammar-feature semantics to establish source-grounded knowledge for direct
module-body synchronous and asynchronous function declarations. Other snapshot
resources are not direct semantic dependencies of that derivation. Its
identified definition also records the ambient parser
implementation and runtime version. Successful analysis publishes separately
referable declaration knowledge plus exhaustive coverage of exactly that scope;
syntax failure publishes neither successful coverage nor declaration knowledge.
Subjects are snapshot-local and distinct from their AST nodes, declared names,
and UTF-8-byte-column source occurrences. This local representation does not
select universal subject, source, derivation, coverage, or failure architecture.
A bounded aggregate can apply that existing derivation independently to a
caller-ordered, nonempty set of distinct selected resource addresses. It retains
each per-resource analysis and flattens their existing knowledge in selection
and source order for downstream retrieval. It is not a synthetic derivation or
aggregate coverage claim; selection or parse failure returns no aggregate.
Direct resource containment was already intrinsic to each function declaration:
its occurrence gives the resource and exact span, and its subject binds to the
derivation's observed resource dependency. A production
`PythonFunctionDeclarationContainmentView` now validates an aggregate against
one retained snapshot and navigates resource to direct declarations and
declaration to containing resource. It derives no duplicate ownership fact,
aggregate derivation, relevance judgment, or Context disclosure. The
[function package overview](../src/devtools/context/python/function/docs/overview.md)
defines its bounded contract. Classes, methods, and nested declarations remain
outside this direct module-body function analysis. A separate production
[`context.python.classes` package](../src/devtools/context/python/classes/docs/overview.md)
now establishes direct `Module.body` class declarations and synchronous/async
methods directly in each supported class body. It reuses the existing Python
source occurrence/range and observed-resource dependency values without
changing function declaration identity or exact-name/Reference consumers.
Class and method subjects have distinct structural identities: class ordinal
within the exact resource, and method ordinal within the exact class subject.
Each occurrence belongs to its observed resource; a method's direct lexical
parent is its class declaration. These are different relationships. A class
retains exact direct base-expression syntax and spans. A separate bounded
direct-base derivation assesses every expression and establishes a class-to-class
repository relation only through an unambiguous earlier local class binding,
direct imported member, or explicitly imported module attribute. It reuses
production module/import resolution, retains both class declarations and exact
resource/content dependencies, and leaves unsupported or ambiguous expressions
visible. This is a static repository relation, not runtime inheritance, Method
Resolution Order, subtype closure, or retrieval relevance. Decorators do not
imply descriptor semantics. Bounded coverage
separates supported results from encountered excluded nested syntax and from
module-body functions owned by the existing analyzer. Validated navigation
supports both directions without duplicate containment facts, ranking, or
Context disclosure. A later declaration model may add deeper lexical parents
without treating every declaration as directly resource-contained.
````

### E0051 — R004 docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md

Span [9366, 12505), lines 159–209. Provenance: sealed packet resources[4].text.

````text
### Repository subjects and source occurrences

**Subjecthood** and **derivation** are orthogonal. A **RepositorySubject** is
an identifiable thing within a repository state about which repository
intelligence can make assertions. **DerivedKnowledge** instead answers what is
known about repository things, from which dependencies, through which
derivation, and with what provenance/applicability. Analysis can establish a
RepositorySubject without making subjecthood a pre-existing filesystem fact:
parsing may establish that an identifiable Python method exists, and later
analysis may derive knowledge about that method. Thus being derived through
analysis does not make a thing ineligible to be a subject.

RepositorySubject deliberately covers heterogeneous repository artifacts, not
only code. An analyzer may establish a Python module, class, function, method,
or nested function; a Markdown document or section; a configuration table or
entry; or a workflow, job, or step. This is not a closed kind taxonomy.
Independent referential identity is justified when a repository-intelligence
domain needs to attach knowledge, relationships, queries, or dependencies to a
thing independently. Statements, expressions, parameters, and blocks are
therefore neither universally subjects nor universally excluded.

A **SourceOccurrence** is an identifiable/addressable source span or anchor
within a ResourceOccurrence: for example a declaration, reference/use, call
site, import occurrence, literal, or another source anchor. It can participate
in provenance and relationships without becoming a RepositorySubject, and is
only snapshot-locally addressable/identifiable. A source occurrence can
declare, define, or reference a subject, but source location is not semantic
subject identity. A snapshot, path, and range can locate a method; harmless
line insertion can change that locator without changing the subject an analyzer
recognizes. Concrete subject identifiers, locators, fingerprints, and matching
algorithms remain open.

RepositorySubject identity is snapshot-local. There is no foundational global
semantic entity intended to survive arbitrary repository evolution. Same
logical entity, rename/move/copy, evolution, split, and merge claims between
subjects in different snapshots are DerivedKnowledge with future evidence,
confidence, or ambiguity where appropriate.

AST and parser nodes are analysis artifacts by default, not subjects merely
because they appear in a parse tree. A `FunctionDef`-like node can establish a
function subject; a parser-internal node without independent repository-
intelligence identity need not. Conversely, a future analyzer may establish a
fine-grained subject when it has a justified identity model.

Names and qualified names are not foundational RepositorySubject identity.
Declared name, containment, qualified-name, and name-resolution facts are
DerivedKnowledge. A resolved semantic entity may itself be a RepositorySubject,
but this architecture neither requires a separate foundational `Symbol`
abstraction nor prevents a future analyzer from adding justified symbol-specific
semantics.
````

### E0052 — R006 docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md

Span [16740, 18444), lines 278–306. Provenance: sealed packet resources[6].text.

````text
### Planning versus model-input assembly

Disclosure planning determines **what** information should be available:
candidate/representation choices, coverage, marginal contribution, overlap,
complementarity, prior availability, applicability, authority, coherence, and
cost/budget. Model-input assembly determines **how** selected information is
realized and positioned for a particular model interaction: provider
serialization, prompt structure, order, separators, tokenizer/model constraints,
and coexistence with tools, instructions, and conversation.

Presentation order may affect utilization, but does not contaminate repository
relevance or coverage semantics. Selection decides what to disclose;
presentation policy arranges selected material. Positional effects are empirical,
model-specific evidence, not universal rules. Future assembly policy can depend
on identified hard capabilities and versioned empirical behavior profiles without
changing repository relevance evidence. Neither `ModelCapabilities` nor
`ModelBehaviorProfile` is selected as a model.

Assembly arranges and serializes already-realized disclosure. It must not
silently introduce a new semantic assertion through placement, formatting,
truncation, or token-budget handling. If a semantic compression or synthesis is
needed to fit a consumer constraint, disclosure planning must select it and
materialization must realize it before assembly presents it.

The same ContextDisclosure may be assembled by different identified policies
into different ModelRequests. This permits presentation/input experiments while
holding retrieval, ranking, and disclosure selection fixed. No assembly
abstraction or policy is implemented.
````

### E0053 — R010 docs/architecture/taxonomy.md

Span [42922, 49075), lines 790–884. Provenance: sealed packet resources[10].text.

````text
### Context disclosure and assembly

**Status: EMERGING.**

Context compilation conditionally composes information for a consumer; it is
not top-K retrieval or budget filling. Ranking remains an input, while
disclosure planning couples candidate and representation choice and can reason
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, coherence, and multidimensional cost. A ContextCandidate can support
multiple representations without selecting a fixed `DisclosureOption` type.

A ContextDisclosure is an identifiable, provenance-bearing account of
purpose-selected represented information. A DisclosurePlan is the distinct
identified decision about what should be made available; a ContextDisclosure is
what was actually realized with reference to that plan. Both are immutable
artifact directions, neither is a ModelRequest, and materialization between
them must not silently make a materially different plan. Repository, disclosure,
and Conversation histories may reference one another but retain separate
identities and lifecycles. Production now has one caller-directed,
snapshot-bound DisclosurePlan with qualified Python Reference and explicit
whole-resource options, and a separate faithfully realized ContextDisclosure.
That bounded implementation does not establish automatic planning, a universal
representation taxonomy, or sufficiency. Previously disclosed information
need not remain currently available or applicable. Tracking disclosure or
availability must not claim model comprehension or create a ModelKnowledgeState.

The accepted, unimplemented planning direction admits concrete disclosure
options through a Context-owned policy and records bounded coverage, constraints,
deferrals and recovery targets beside the plan. Native information referents
remain distinct from representations. No mandatory resource-Selection service
or boolean ContextSufficiency follows. Acquisition for a question and expansion
of an exact disclosure target are Context request semantics; successive attempts
and escalation remain Agent/orchestration decisions. ADR-0005 now assigns
task-obligation resolution and acquisition requests to Localization; Context
retains representation admission and exact expansion. The earlier question-lane
policy is not the next production baseline. See ADR-0004's refinement.

Disclosure selects information rather than arbitrary prompt strings. A
DisclosureOption is a conceptual purpose-relative possibility for making
identified information about one or more subjects available through a
representation or explicitly characterized transformation. Origin, form,
fidelity, and cost are separate concerns.
Source-preserving representations select/transform identified source without
new semantic assertions; knowledge projections expose existing DerivedKnowledge;
synthesized representations introduce new semantic assertions and therefore
must preserve explicit origin and support without automatically becoming
repository DerivedKnowledge. Determinism does not by itself establish semantic
certainty. Composite representations may preserve multiple constituent origins.

A representational transformation changes how available information is exposed
without intentionally establishing a materially new semantic assertion. An
epistemic derivation establishes such an assertion. Repository-relative
epistemic derivation can establish DerivedKnowledge under ADR-0002; purpose-
relative Context synthesis remains owned by ADR-0004 and can remain ephemeral.
Lossy compression can cross the epistemic boundary when it implicitly asserts
an interpretation. This conceptual distinction does not require production
classes, enums, independent identity, persistence, or a complete representation
taxonomy.

Materialization faithfully realizes the representation or transformation
selected by a DisclosurePlan. It may perform explicitly planned semantic
transformation or lossy synthesis, but it must not silently invent a materially
different synthesis or disclosure decision. Model-input assembly arranges and
serializes already-realized disclosure; formatting, placement, truncation, and
budget handling must not silently introduce new semantic assertions.

Across representation selection, projection, synthesis, compression,
materialization, ContextDisclosure realization, and assembly, semantic
commitment must not be silently strengthened beyond source semantics, support,
assumptions/scope, conflict state, and semantic-result coverage. A possible
relationship cannot become definite, a partial set exhaustive, an approximation
exact, or a disagreement one truth without an identified semantically capable
process establishing that stronger result.

Disclosure planning determines what information becomes available; model-input
assembly determines how selected information is serialized, ordered, and placed
for a particular model interaction. Presentation effects are empirical
consumer-behavior evidence, not repository relevance or coverage truth. Budget
is a ceiling, not a target, and is distinct from discovery bounds. Optional
Information-purpose decomposition may lead to subordinate purpose/acquisition
work without discarding the broader purpose or requiring persistent child
artifacts; child satisfaction does not prove parent sufficiency. See
[ADR-0004](decisions/ADR-0004-context-disclosure-planning-and-assembly.md).

Coherence is intelligibility of information presented together and the avoided
consumer reconstruction burden, not physical contiguity. Authority is
claim-/purpose-relative evidence, not a universal source ordering, and remains
distinct from relevance, confidence, coverage, and ranking influence. Material
conflicts and absence discipline remain preservable: disclosure planning does
not generally resolve truth, and missing evidence does not prove its opposite.
Provenance explains origin and support; it does not by itself establish
authority, certainty, correctness, or truth. No universal confidence,
epistemic-status, authority, or truth field is selected.
````

### E0054 — R057 docs/backlog/items/B-0047-protected-development-validation-profile.md

Span [1516, 2138), lines 33–43. Provenance: sealed packet resources[57].text.

````text
## Implemented contract

The operational entry point is `scripts/validate_development.py`. It invokes
pytest over `tests/` with `tests/experiments/` ignored before recursive
collection. This stable directory boundary excludes retained replay and
outcome-dependent material without inspecting outcomes or maintaining a list
of sensitive test node IDs. It leaves project pytest options, including the
100% production branch-coverage requirement, intact and returns pytest's
failure code. The profile contract and separate static quality gates are
documented in `docs/development/validation.md` and linked from `AGENTS.md`.
````

### E0055 — R061 docs/documentation_map.md

Span [49, 370), lines 5–9. Provenance: sealed packet resources[61].text.

````text
- [Central architecture](architecture.md) is the canonical current and accepted
  system-architecture overview: domains, boundaries, dependency direction,
  cross-domain composition, and whether architecture is implemented/current or
  accepted but not implemented. It must be understandable without replaying all
  ADRs.
````

### E0056 — R065 scripts/validate_development.py

Span [248, 531), lines 14–18. Provenance: sealed packet resources[65].text.

````text
def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    """Select ordinary tests while excluding the retained experiment tree."""
    tests = repository_root / "tests"
    experiments = tests / "experiments"
    return [str(tests), f"--ignore={experiments}"]
````

### E0057 — R065 scripts/validate_development.py

Span [533, 657), lines 21–23. Provenance: sealed packet resources[65].text.

````text
def main() -> int:
    """Run pytest and return its exit code unchanged."""
    return int(pytest.main(pytest_arguments()))
````

### E0058 — R083 src/devtools/context/__init__.py

Span [0, 497), lines 1–17. Provenance: sealed packet resources[83].text.

````text
# Copyright (c) 2026
"""Public Repository Intelligence and bounded Context API."""

from devtools.context.planning import (
    ContextDisclosure,
    DisclosureMaterializationError,
    DisclosurePlan,
    MaterializedDisclosureItem,
    PlannedDisclosure,
    RenderedContextDisclosure,
    WholeResourceDisclosureOption,
    assemble_context_disclosure_model_request,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
````

### E0059 — R099 src/devtools/context/localization/grounding/resolve.py

Span [5088, 7425), lines 152–212. Provenance: sealed packet resources[99].text.

````text
def _ground_declaration(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectDeclarationLocator,
    universe: PythonModuleInterpretationUniverse,
) -> AnchorGrounding:
    modules = tuple(
        item
        for item in lookup_python_modules(universe, locator.module.dotted_name)
        if locator.module.kind is None or item.kind is locator.module.kind
    )
    observations: list[NativeGroundingEvidence] = []
    candidates: list[AnchorGroundingCandidate] = []
    unsupported = False
    for module in modules:
        try:
            selection = select_python_module_source_declarations(
                snapshot,
                module=module,
                declared_name=locator.declared_name,
                kind=PythonSourceDeclarationKind(locator.kind.value),
            )
        except (PythonModuleParseError, PythonClassMethodParseError, SyntaxError):
            unsupported = True
            continue
        observations.append(selection)
        candidates.extend(
            AnchorGroundingCandidate(item, selection) for item in selection.declarations
        )
    disposition = (
        AnchorGroundingDisposition.AMBIGUOUS
        if len(candidates) > 1 or (unsupported and bool(candidates))
        else AnchorGroundingDisposition.UNSUPPORTED
        if unsupported
        else _candidate_disposition(tuple(candidates))
    )
    reason = {
        AnchorGroundingDisposition.RESOLVED: (
            "Exactly one native source declaration matches the exact locator; "
            "runtime binding identity is not established."
        ),
        AnchorGroundingDisposition.AMBIGUOUS: (
            "Multiple native declarations or incompletely interpreted modules prevent "
            "unique source declaration selection."
        ),
        AnchorGroundingDisposition.UNRESOLVED: (
            "No requested direct declaration was found in the supplied modules."
        ),
        AnchorGroundingDisposition.UNSUPPORTED: (
            "Relevant syntax cannot establish the requested direct declaration."
        ),
    }[disposition]
    return _account(
        request,
        GroundingResolver.PYTHON_SOURCE_DECLARATION_SELECTION,
        tuple(candidates),
        tuple(observations),
        universe,
        disposition,
        reason,
    )
````

### E0060 — R120 src/devtools/context/planning/__init__.py

Span [0, 1080), lines 1–38. Provenance: sealed packet resources[120].text.

````text
# Copyright (c) 2026
"""Explicit repository Context planning and faithful realization."""

from devtools.context.planning.materialization import (
    ContextDisclosure,
    DisclosureMaterializationError,
    MaterializedDisclosureItem,
    materialize_disclosure_plan,
)
from devtools.context.planning.plan import (
    DisclosurePlan,
    PlannedDisclosure,
    plan_disclosures,
)
from devtools.context.planning.rendering import (
    RenderedContextDisclosure,
    assemble_context_disclosure_model_request,
    render_context_disclosure,
)
from devtools.context.planning.resource import (
    WholeResourceDisclosureOption,
    choose_whole_resource_disclosure,
)

__all__ = [
    "ContextDisclosure",
    "DisclosureMaterializationError",
    "DisclosurePlan",
    "MaterializedDisclosureItem",
    "PlannedDisclosure",
    "RenderedContextDisclosure",
    "WholeResourceDisclosureOption",
    "assemble_context_disclosure_model_request",
    "choose_whole_resource_disclosure",
    "materialize_disclosure_plan",
    "plan_disclosures",
    "render_context_disclosure",
]
````

### E0061 — R121 src/devtools/context/planning/docs/overview.md

Span [1358, 1872), lines 35–41. Provenance: sealed packet resources[121].text.

````text
DisclosurePlan binds purpose, repository and snapshot identities, ordered
choices, and optional preceding-plan identity. The plan's deterministic
identity changes when purpose, applicability, order, choice, or lineage changes.
Each concrete choice names an implemented representation and retains its own
native support. The common PlannedDisclosure protocol only permits the two
current consumers to participate in one plan; it is not a generic fact ontology,
language-independent parser, or materializer registry.
````

### E0062 — R121 src/devtools/context/planning/docs/overview.md

Span [1874, 2387), lines 43–49. Provenance: sealed packet resources[121].text.

````text
materialize_disclosure_plan rechecks the supplied snapshot and requires each
materialized item to match its planned choice. It fails on stale, missing, or
incompatible dependencies. A ContextDisclosure retains one item per choice,
exact content identities and addresses, text, and the native materialized
provenance. Rendering preserves plan order and does not infer new facts.
assemble_context_disclosure_model_request copies a caller's ModelRequest and
appends already-rendered Context after the unchanged task.
````

### E0063 — R125 src/devtools/context/planning/resource.py

Span [726, 3215), lines 27–86. Provenance: sealed packet resources[125].text.

````text
@dataclass(frozen=True, slots=True)
class WholeResourceDisclosureOption:
    """Choose one exact observed resource, without inferring relevance."""

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    representation: ClassVar[str] = "whole-observed-resource-v1"

    @property
    def identity(self) -> str:
        """Identify this explicit representation of one observed occurrence."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use exact retained content; reject stale, missing, or redirected state."""
        if (
            snapshot.id != self.snapshot_id
            or snapshot.repository_id != self.repository_id
        ):
            msg = "Whole-resource disclosure belongs to another snapshot."
            raise DisclosureMaterializationError(msg)
        try:
            observed = snapshot.resource_at(self.resource.address)
        except ValueError as error:
            msg = "Whole-resource disclosure source is missing."
            raise DisclosureMaterializationError(msg) from error
        if observed != self.resource:
            msg = "Whole-resource disclosure source differs from retained evidence."
            raise DisclosureMaterializationError(msg)
        text = "".join(
            (
                "Whole observed repository resource\n",
                f"Purpose: {self.purpose}\n",
                f"Snapshot identity: {self.snapshot_id}\n",
                f"Resource pointer: {observed.address}\n",
                f"Content identity: {observed.content_identity}\n",
                f"Exact source UTF-8 bytes: {len(observed.content.encode('utf-8'))}\n",
                "--- exact resource source begins ---\n",
                observed.content,
                "\n--- exact resource source ends ---\n",
            ),
        )
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(observed.address,),
            content_identities=(observed.content_identity,),
            text=text,
            native_provenance=observed,
        )
````

### E0064 — R125 src/devtools/context/planning/resource.py

Span [3217, 3819), lines 89–104. Provenance: sealed packet resources[125].text.

````text
def choose_whole_resource_disclosure(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    resource_address: RepositoryResourceAddress,
) -> WholeResourceDisclosureOption:
    """Record an explicit coarse representation, without reading the filesystem."""
    if not purpose.strip():
        msg = "Whole-resource disclosure purpose must not be blank."
        raise ValueError(msg)
    return WholeResourceDisclosureOption(
        purpose=purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=snapshot.resource_at(resource_address),
    )
````

### E0065 — R135 src/devtools/context/python/function/containment.py

Span [2332, 5195), lines 64–124. Provenance: sealed packet resources[135].text.

````text
def build_python_function_declaration_containment_view(
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonFunctionDeclarationAnalysisAggregate,
) -> PythonFunctionDeclarationContainmentView:
    """Validate native analyses against retained state and expose navigation.

    This validation checks provenance consistency without reparsing source or
    introducing an independently identified ownership relationship.
    """
    if not aggregate.analyses:
        msg = "Containment requires at least one selected resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Containment repeats a selected resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Declaration analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Declaration analysis uses stale observed resource content."
            raise ValueError(msg)
        if (
            analysis.coverage.derivation_identity != derivation.identity
            or analysis.coverage.declaration_count != len(analysis.declarations)
        ):
            msg = "Declaration coverage differs from its retained analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.declarations):
            if (
                declaration.derivation_identity != derivation.identity
                or declaration.subject.snapshot_id != snapshot.id
                or declaration.subject.resource_dependency_identity
                != dependency.identity
                or declaration.subject.derivation_definition_identity
                != derivation.definition.identity
                or declaration.subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
            ):
                msg = "Declaration differs from its resource analysis or support."
                raise ValueError(msg)
    return PythonFunctionDeclarationContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
````

### E0066 — R138 src/devtools/context/python/function/docs/overview.md

Span [493, 3292), lines 10–58. Provenance: sealed packet resources[138].text.

````text
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
````

### E0067 — R138 src/devtools/context/python/function/docs/overview.md

Span [3292, 5665), lines 59–98. Provenance: sealed packet resources[138].text.

````text
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
````

### E0068 — R140 src/devtools/context/python/function/planned_reference.py

Span [891, 2898), lines 29–78. Provenance: sealed packet resources[140].text.

````text
@dataclass(frozen=True, slots=True)
class PythonQualifiedReferenceDisclosureOption:
    """Choose the existing relationship-plus-exact-source representation."""

    disclosure: PythonQualifiedReferenceDisclosure

    representation: ClassVar[str] = "qualified-python-reference-and-target-v1"

    @property
    def purpose(self) -> str:
        """Return the caller's explicit information purpose."""
        return self.disclosure.purpose

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the reference derivation's snapshot identity."""
        return self.disclosure.analysis.derivation.dependency.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Return the reference derivation's repository identity."""
        return self.disclosure.analysis.derivation.dependency.repository_id

    @property
    def identity(self) -> str:
        """Retain the existing fact, derivation, and caller-purpose identity."""
        return self.disclosure.identity

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use the existing fully validated Python-specific materializer."""
        materialized = materialize_python_qualified_reference_source(
            disclosure=self.disclosure,
            snapshot=snapshot,
        )
        rendered = render_python_qualified_reference_context(materialized)
        reference = self.disclosure.reference
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(
                reference.occurrence.resource_address,
                reference.target_declaration.support.resource_address,
            ),
            content_identities=(
                materialized.source_content_identity,
                materialized.target_content_identity,
            ),
            text=rendered.text,
            native_provenance=materialized,
        )
````

### E0069 — R141 src/devtools/context/python/function/qualified_reference.py

Span [4325, 9062), lines 124–227. Provenance: sealed packet resources[141].text.

````text
def materialize_python_qualified_reference_source(
    *,
    disclosure: PythonQualifiedReferenceDisclosure,
    snapshot: RepositorySnapshot,
) -> MaterializedPythonQualifiedReferenceContext:
    """Validate both dependencies and extract only the recorded source spans."""
    # Recheck membership because immutable values can still be constructed directly.
    selected = disclose_python_qualified_reference(
        purpose=disclosure.purpose,
        analysis=disclosure.analysis,
        reference=disclosure.reference,
    )
    reference = selected.reference
    dependency = selected.analysis.derivation.dependency
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        dependency.snapshot_id != snapshot.id
        or dependency.repository_id != snapshot.repository_id
        or reference.occurrence.snapshot_id != snapshot.id
        or reference.occurrence.resource_address != dependency.resource.address
    ):
        msg = "Reference source dependency does not match the supplied snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source_resource = _snapshot_resource(
        snapshot,
        reference.occurrence.resource_address,
        label="source",
    )
    if source_resource != dependency.resource:
        msg = "Reference source content differs from its derivation dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)

    if (
        target.support.snapshot_id != snapshot.id
        or target.subject.snapshot_id != snapshot.id
    ):
        msg = "Target declaration belongs to another snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_resource = _snapshot_resource(
        snapshot,
        target.support.resource_address,
        label="target",
    )
    target_dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=target_resource,
    )
    if target.subject.resource_dependency_identity != target_dependency.identity:
        msg = "Target declaration resource or content differs from its dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if target_resource != reference.target_resource:
        msg = "Target resource differs from the retained Reference support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    supporting_interpretation = (
        reference.direct_member_resolution.module
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target
        if reference.imported_member_resolution is not None
        else None
    )
    if (
        supporting_interpretation is None
        or supporting_interpretation.snapshot_id != snapshot.id
        or supporting_interpretation.repository_id != snapshot.repository_id
        or supporting_interpretation.resource != target_resource
    ):
        msg = "Target declaration differs from its qualified resolution support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_analysis = (
        reference.direct_member_resolution.function_analysis
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target_function_analysis
        if reference.imported_member_resolution is not None
        else None
    )
    if target_analysis is not None and (
        target not in target_analysis.declarations
        or target_analysis.derivation.dependency.snapshot_id != snapshot.id
        or target_analysis.derivation.dependency.repository_id != snapshot.repository_id
        or target_analysis.derivation.dependency.resource != target_resource
    ):
        msg = "Target declaration differs from its retained declaration analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)

    return MaterializedPythonQualifiedReferenceContext(
        disclosure=selected,
        snapshot_id=snapshot.id,
        source_content_identity=source_resource.content_identity,
        target_content_identity=target_resource.content_identity,
        reference_name_text=_extract_source_segment(
            source_resource.content,
            reference.occurrence.source_range,
        ),
        target_declaration_text=_extract_source_segment(
            target_resource.content,
            target.support.source_range,
        ),
    )
````

### E0070 — R143 src/devtools/context/python/function/request_assembly.py

Span [678, 1689), lines 23–51. Provenance: sealed packet resources[143].text.

````text
def assemble_python_function_context_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedPythonFunctionContext,
) -> ModelRequest:
    """Return a request preserving task and request semantics around Context."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(
            content=prompt_content,
            role=task_request.prompt.role,
        ),
    )
````

### E0071 — R153 src/devtools/context/python/modules/declarations.py

Span [2281, 6980), lines 74–192. Provenance: sealed packet resources[153].text.

````text
def lookup_python_module_declaration(  # noqa: C901, PLR0912, PLR0915
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
) -> PythonModuleDeclarationLookup:
    """Resolve only one unique undecorated direct declaration binding.

    Competing, nested, wildcard, and dynamic bindings do not establish a
    target. This is static repository syntax, never runtime attribute lookup.
    """
    if not declared_name.isidentifier():
        msg = "Direct member name must be a Python identifier."
        raise ValueError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Direct member module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    tree = ast.parse(module.resource.content, filename=str(address))
    candidates: list[PythonDirectModuleDeclaration | None] = []
    uncertain = False
    for node in tree.body:
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            if node.name == declared_name:
                if node.decorator_list:
                    candidates.append(None)
                elif isinstance(node, ast.ClassDef):
                    candidates.extend(
                        item
                        for item in classes.classes
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
                else:
                    candidates.extend(
                        item
                        for item in functions.declarations
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
            continue
        if isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    uncertain = True
                elif (
                    alias.asname
                    or (
                        alias.name
                        if isinstance(node, ast.ImportFrom)
                        else alias.name.split(".")[0]
                    )
                ) == declared_name:
                    candidates.append(None)
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(
                child.ctx,
                ast.Store | ast.Del,
            ):
                if child.id == declared_name:
                    candidates.append(None)
            elif isinstance(
                child,
                ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
            ):
                if child.name == declared_name:
                    candidates.append(None)
            elif isinstance(child, ast.Import | ast.ImportFrom):
                for alias in child.names:
                    if alias.name == "*":
                        uncertain = True
                    elif (
                        alias.asname
                        or (
                            alias.name
                            if isinstance(child, ast.ImportFrom)
                            else alias.name.split(".")[0]
                        )
                    ) == declared_name:
                        candidates.append(None)
    if any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    ):
        uncertain = True
    if uncertain or len(candidates) > 1:
        outcome = PythonModuleDeclarationLookupOutcome.AMBIGUOUS
        target = None
    elif not candidates:
        outcome = PythonModuleDeclarationLookupOutcome.UNRESOLVED
        target = None
    elif candidates[0] is None:
        outcome = PythonModuleDeclarationLookupOutcome.NOT_DECLARATION
        target = None
    else:
        outcome = PythonModuleDeclarationLookupOutcome.RESOLVED
        target = candidates[0]
    return PythonModuleDeclarationLookup(
        module,
        declared_name,
        functions,
        classes,
        outcome,
        target,
    )
````

### E0072 — R155 src/devtools/context/python/modules/interpretation.py

Span [2286, 3092), lines 77–101. Provenance: sealed packet resources[155].text.

````text
@dataclass(frozen=True, slots=True)
class PythonModuleInterpretation:
    """One exact resource's module interpretation under an explicit root."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    module_root: PythonModuleRoot
    dotted_name: str
    kind: PythonModuleKind

    SEMANTICS: ClassVar[str] = _INTERPRETATION_SEMANTICS

    @property
    def identity(self) -> str:
        """Identify this interpretation from its actual semantic inputs."""
        return _digest(
            self.SEMANTICS,
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
            self.module_root.value,
            self.dotted_name,
            self.kind.value,
        )
````

### E0073 — R155 src/devtools/context/python/modules/interpretation.py

Span [5006, 6796), lines 156–198. Provenance: sealed packet resources[155].text.

````text
def interpret_python_module_resources(
    snapshot: RepositorySnapshot,
    *,
    module_root: PythonModuleRoot,
    resource_addresses: Sequence[RepositoryResourceAddress],
) -> PythonModuleInterpretationAnalysis:
    """Interpret exactly the caller-selected observed resources for one root.

    This operation performs no acquisition, parsing, package discovery, import
    resolution, or root inference.  Every selected resource yields exactly one
    interpretation or one explicit exclusion in caller-supplied address order.
    """
    selected_addresses = tuple(resource_addresses)
    if len(set(selected_addresses)) != len(selected_addresses):
        msg = "Python module interpretation resource addresses must be distinct."
        raise ValueError(msg)

    interpretations: list[PythonModuleInterpretation] = []
    exclusions: list[PythonModuleInterpretationExclusion] = []
    for address in selected_addresses:
        resource = snapshot.resource_at(address)
        interpretation, reason = _interpret_resource(
            repository_id=snapshot.repository_id,
            snapshot_id=snapshot.id,
            resource=resource,
            module_root=module_root,
        )
        if interpretation is None:
            exclusions.append(PythonModuleInterpretationExclusion(
                resource=resource,
                module_root=module_root,
                reason=cast("PythonModuleInterpretationExclusionReason", reason),
            ))
        else:
            interpretations.append(interpretation)

    return PythonModuleInterpretationAnalysis(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        module_root=module_root,
        interpretations=tuple(interpretations),
        exclusions=tuple(exclusions),
    )
````

### E0074 — R172 src/devtools/context/python/references/docs/overview.md

Span [0, 1700), lines 1–28. Provenance: sealed packet resources[172].text.

````text
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
- A statically identified supported class can 
````

### E0075 — R254 src/devtools/models/interaction/docs/overview.md

Span [0, 1000), lines 1–20. Provenance: sealed packet resources[254].text.

````text
# `devtools.models.interaction`

This package owns one bounded model invocation boundary:

```text
ModelRequest -> ModelInteraction -> ModelResponse
```

`ModelRequest` is an immutable semantic invocation value containing a `Prompt`,
immutable portable `ModelSettings`, an optional provider continuation, and an
optional typed provider request extension. `Prompt` is per-invocation
model-facing input and deliberately has no durable conversation-message
identity or local conversation timestamp. `ModelResponse`
contains model output, its source, optional provider continuation, optional
provider-reported `ModelUsage`, and optional provider-reported
`ModelTermination`, plus optional separately returned textual reasoning. Usage
retains only reported input, output, and total token counts; absent counts are
not estimated. Termination retains only a normal stop, an output-limit end, or a
tool-call end when the provider reports one. Reasoning remains distinct from
visible response content and is n
````

### E0076 — R255 src/devtools/models/interaction/models.py

Span [3171, 4963), lines 98–138. Provenance: sealed packet resources[255].text.

````text
@dataclass(frozen=True, slots=True)
class ModelRequest:
    """Represent one immutable semantic request to a model interaction."""

    prompt: Prompt
    settings: ModelSettings = field(default_factory=ModelSettings)
    conversation: ConversationRef | None = None
    provider_settings: ProviderRequestSettings | None = None
    tools: tuple[ModelToolDefinition, ...] = ()

    def __post_init__(self) -> None:
        """Reject values outside the narrow portable request contract."""
        if not isinstance(self.prompt, Prompt):
            msg = "Model request prompt must be a Prompt."
            raise TypeError(msg)
        if not isinstance(self.settings, ModelSettings):
            msg = "Model request settings must be ModelSettings."
            raise TypeError(msg)
        if self.conversation is not None and not isinstance(
            self.conversation,
            ConversationRef,
        ):
            msg = "Model request conversation must be a ConversationRef or None."
            raise TypeError(msg)
        if self.provider_settings is not None and not isinstance(
            self.provider_settings,
            ProviderRequestSettings,
        ):
            msg = (
                "Model request provider settings must be a provider extension "
                "or None."
            )
            raise TypeError(msg)
        if not isinstance(self.tools, tuple) or not all(
            isinstance(tool, ModelToolDefinition) for tool in self.tools
        ):
            msg = "Model request tools must be a tuple of ModelToolDefinition values."
            raise TypeError(msg)
        if len({tool.name for tool in self.tools}) != len(self.tools):
            msg = "Model request Tool definition names must be unique."
            raise ValueError(msg)
````

### E0077 — R257 src/devtools/models/interaction/prompt.py

Span [110, 260), lines 7–12. Provenance: sealed packet resources[257].text.

````text
@dataclass(frozen=True, slots=True)
class Prompt:
    """Represent the currently supported single text chat input."""

    content: str
    role: str
````

### E0078 — R383 tests/context/planning/test_plan.py

Span [2904, 6375), lines 89–185. Provenance: sealed packet resources[383].text.

````text
def test_mixed_plan_preserves_purpose_sources_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nf()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    purpose = "Inspect this binding."
    reference = _reference_option(snapshot)
    whole = choose_whole_resource_disclosure(
        purpose=purpose,
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=purpose,
        snapshot=snapshot,
        disclosures=(reference, whole),
    )
    assert (
        plan.identity
        == plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(whole, reference),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
            preceding_plan_identity="prior",
        ).identity
    )
    (tmp_path / "consumer.py").unlink()
    (tmp_path / "target.py").unlink()
    materialized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert len(materialized.items) == 2
    assert materialized.items[0].option_identity == reference.identity
    assert materialized.items[0].representation == reference.representation
    assert materialized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("target.py"),
    )
    assert "ast.Call.func; no runtime invocation is asserted" in (
        materialized.items[0].text
    )
    assert "def f():\r\n    return 'π'" in materialized.items[0].text
    assert materialized.items[1].native_provenance is whole.resource
    assert whole.resource.content in materialized.items[1].text
    assert (
        materialized.identity
        == materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        ).identity
    )
    rendered = render_context_disclosure(materialized)
    assert rendered.disclosure is materialized
    assert rendered.text.index("Disclosure item 1") < rendered.text.index(
        "Disclosure item 2",
    )
    assert purpose in rendered.text
    assert plan.identity in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    task = ModelRequest(
        Prompt("Inspect source.", "system"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider,
    )
    assembled = assemble_context_disclosure_model_request(
        task_request=task,
        context=rendered,
    )
    assert task.prompt.content == "Inspect source."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is continuation
    assert assembled.provider_settings is provider
    assert assembled.prompt.content.index("Inspect source.") < (
        assembled.prompt.content.index(rendered.text)
    )
    assert replace(assembled, prompt=task.prompt) == task
````

### E0079 — R383 tests/context/planning/test_plan.py

Span [10061, 11541), lines 278–318. Provenance: sealed packet resources[383].text.

````text
@pytest.mark.parametrize("wrong_value", ["identity", "representation"])
def test_materialization_rejects_an_option_that_changes_its_plan(
    tmp_path: Path,
    wrong_value: str,
) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "source\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )

    @dataclass(frozen=True)
    class IncompatibleOption:
        purpose: str = option.purpose
        snapshot_id: RepositorySnapshotId = option.snapshot_id
        repository_id: RepositoryId = option.repository_id
        representation: str = option.representation

        @property
        def identity(self) -> str:
            return option.identity

        def materialize(
            self,
            current: RepositorySnapshot,
        ) -> MaterializedDisclosureItem:
            item = option.materialize(current)
            if wrong_value == "identity":
                return replace(item, option_identity="changed")
            return replace(item, representation="changed")

    forged = IncompatibleOption()
    plan = DisclosurePlan(
        purpose=option.purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        disclosures=(forged,),
    )
    with pytest.raises(DisclosureMaterializationError, match="differs"):
        materialize_disclosure_plan(plan=plan, snapshot=snapshot)
````

### E0080 — R387 tests/context/python/classes/test_declarations.py

Span [1748, 5948), lines 52–132. Provenance: sealed packet resources[387].text.

````text
def test_direct_classes_methods_exclusions_and_existing_function_contract(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "module.py": (
                "def module_function():\n    pass\n\n"
                "@register\nclass A(Base, pkg.Other):\n"
                "    @staticmethod\n    def run(self):\n"
                "        def nested():\n            pass\n"
                "    @property\n    async def load(self):\n        pass\n"
                "    class Nested:\n        def hidden(self):\n            pass\n\n"
                "class B:\n    def run(self):\n        pass\n\n"
                "def outer():\n    class Local:\n        pass\n"
            ),
        },
    )
    analysis = derive_python_class_method_declarations(snapshot)
    assert [item.declared_name for item in analysis.classes] == ["A", "B"]
    assert [item.declared_name for item in analysis.methods] == [
        "run",
        "load",
        "run",
    ]
    assert [item.declaration_kind for item in analysis.methods] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
        PythonFunctionDeclarationKind.SYNCHRONOUS,
    ]
    assert analysis.classes[0].support.source_range.start_line == 5
    assert analysis.classes[0].support.source_range.start_column_utf8 == 0
    assert analysis.methods[0].support.source_range.start_line == 7
    assert analysis.methods[1].support.source_range.start_line == 11
    assert analysis.methods[0].support.resource_address == snapshot.resource.address
    assert analysis.methods[0].support.snapshot_id == snapshot.id
    assert [base.ordinal for base in analysis.classes[0].base_syntax] == [0, 1]
    assert [base.source_text for base in analysis.classes[0].base_syntax] == [
        "Base",
        "pkg.Other",
    ]
    assert [
        base.occurrence.source_range.start_line
        for base in analysis.classes[0].base_syntax
    ] == [5, 5]
    assert analysis.classes[1].base_syntax == ()
    assert analysis.methods[0].containing_class == analysis.classes[0]
    assert analysis.methods[2].containing_class == analysis.classes[1]
    assert analysis.classes[0].subject.identity != analysis.classes[1].subject.identity
    assert analysis.methods[0].subject.identity != analysis.methods[2].subject.identity
    assert analysis.methods[0].identity != analysis.methods[2].identity
    assert analysis.methods[0].subject.containing_class_subject_identity == (
        analysis.classes[0].subject.identity
    )
    assert analysis.coverage.class_count == 2
    assert analysis.coverage.method_count == 3
    assert analysis.coverage.module_body_function_count == 2
    assert analysis.coverage.excluded_class_count == 2
    assert analysis.coverage.excluded_function_count == 2
    assert [item.kind for item in analysis.excluded_syntax] == [
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
    ]
    assert analysis.coverage.IS_EXHAUSTIVE_FOR_SCOPE
    assert analysis.coverage.derivation_identity == analysis.derivation.identity
    assert analysis.derivation.dependency.resource == snapshot.resource
    assert analysis.derivation.dependency.repository_id == snapshot.repository_id
    assert analysis.derivation.dependency.snapshot_id == snapshot.id
    assert analysis.classes[0].derivation_identity == analysis.derivation.identity
    assert analysis.methods[0].derivation_identity == analysis.derivation.identity
    assert analysis == derive_python_class_method_declarations(snapshot)
    module_functions = derive_python_function_declarations(snapshot)
    assert [item.declared_name for item in module_functions.declarations] == [
        "module_function",
        "outer",
    ]
    assert all(item.declared_name != "run" for item in module_functions.declarations)
    assert not hasattr(analysis.methods[0], "runtime_descriptor")
    assert not hasattr(analysis.classes[0], "resolved_bases")
````

### E0081 — R390 tests/context/python/function/test_containment.py

Span [7980, 10081), lines 213–266. Provenance: sealed packet resources[390].text.

````text
def test_rejects_inconsistent_coverage_and_declaration_support(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"a.py": "def a():\n    pass\n"})
    aggregate = _aggregate(snapshot, "a.py")
    analysis = aggregate.analyses[0]
    for changed_coverage in (
        replace(analysis.coverage, derivation_identity="other"),
        replace(analysis.coverage, declaration_count=0),
    ):
        changed = _replace_first_analysis(
            aggregate,
            replace(analysis, coverage=changed_coverage),
        )
        with pytest.raises(ValueError, match="coverage differs"):
            build_python_function_declaration_containment_view(
                snapshot,
                aggregate=changed,
            )
    declaration = analysis.declarations[0]
    subject = declaration.subject
    support = declaration.support
    changed_declarations = (
        replace(declaration, derivation_identity="other"),
        replace(
            declaration,
            subject=replace(subject, snapshot_id=replace(snapshot.id, value="0" * 64)),
        ),
        replace(
            declaration,
            subject=replace(subject, resource_dependency_identity="other"),
        ),
        replace(
            declaration,
            subject=replace(subject, derivation_definition_identity="other"),
        ),
        replace(declaration, subject=replace(subject, declaration_ordinal=1)),
        replace(
            declaration,
            support=replace(support, snapshot_id=replace(snapshot.id, value="0" * 64)),
        ),
        replace(
            declaration,
            support=replace(
                support,
                resource_address=RepositoryResourceAddress("other.py"),
            ),
        ),
    )
    for changed_declaration in changed_declarations:
        changed = _replace_first_declaration(aggregate, changed_declaration)
        with pytest.raises(ValueError, match="differs from its resource"):
            build_python_function_declaration_containment_view(
                snapshot,
                aggregate=changed,
            )
````

### E0082 — R393 tests/context/python/function/test_declarations.py

Span [7851, 8729), lines 224–253. Provenance: sealed packet resources[393].text.

````text
def test_multiple_same_name_direct_declarations_have_distinct_subjects(
    tmp_path: Path,
) -> None:
    """Declared text is not subject identity or declaration-result identity."""
    snapshot = _snapshot(
        tmp_path,
        """def repeated():
    pass

def repeated():
    pass

def repeated():
    pass
""",
    )

    result = derive_python_function_declarations(snapshot)

    expected_names = [
        "repeated",
        "repeated",
        "repeated",
    ]
    expected_count = len(expected_names)
    assert [item.declared_name for item in result.declarations] == expected_names
    subject_identities = {item.subject.identity for item in result.declarations}
    assert len(subject_identities) == expected_count
    assert len({item.identity for item in result.declarations}) == expected_count
    assert result.coverage.declaration_count == expected_count
````

### E0083 — R393 tests/context/python/function/test_declarations.py

Span [9854, 10611), lines 280–294. Provenance: sealed packet resources[393].text.

````text
def test_source_range_uses_utf8_byte_columns(tmp_path: Path) -> None:
    """Non-ASCII syntax demonstrates the local stdlib AST column contract."""
    final_line = '    return "é"'
    snapshot = _snapshot(tmp_path, f"def café():\n{final_line}\n")

    declaration = derive_python_function_declarations(snapshot).declarations[0]
    source_range = declaration.support.source_range
    expected_end_line = source_range.start_line + 1

    assert declaration.declared_name == "café"
    assert source_range.start_line == 1
    assert source_range.start_column_utf8 == 0
    assert source_range.end_line == expected_end_line
    assert source_range.end_column_utf8 == len(final_line.encode("utf-8"))
    assert source_range.end_column_utf8 != len(final_line)
````

### E0084 — R395 tests/context/python/function/test_materialization.py

Span [1968, 3758), lines 66–112. Provenance: sealed packet resources[395].text.

````text
def test_materializes_duplicate_sync_and_async_exact_multiline_source(
    tmp_path: Path,
) -> None:
    """Materialization preserves CRLF, non-ASCII text, order, and correlation."""
    snapshot = _snapshot(
        tmp_path,
        '# préface\r\ndef duplicate():\r\n    return "café"\r\n\r\n'
        'async def duplicate():\r\n    return "naïve"\r\n',
    )
    disclosure = _disclosure(snapshot, "duplicate")

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    assert materialized.disclosure is disclosure
    assert [item.source_text for item in materialized.items] == [
        'def duplicate():\r\n    return "café"',
        'async def duplicate():\r\n    return "naïve"',
    ]
    knowledge_identities = {
        item.disclosure_item.selected_match.knowledge.identity
        for item in materialized.items
    }
    assert len(knowledge_identities) == len(materialized.items)
    for materialized_item, disclosure_item in zip(
        materialized.items,
        disclosure.items,
        strict=True,
    ):
        assert materialized_item.disclosure_item is disclosure_item
        assert materialized_item.source_snapshot_id == snapshot.id
        assert (
            materialized_item.source_content_identity
            == snapshot.resource.content_identity
        )
    repeated = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    assert repeated == materialized
    assert repeated.identity == materialized.identity
    assert not hasattr(materialized, "model_request")
    assert not hasattr(materialized, "summary")
    assert not hasattr(materialized, "confidence")
    assert not hasattr(materialized, "ranking")
````

### E0085 — R395 tests/context/python/function/test_materialization.py

Span [5486, 6703), lines 156–188. Provenance: sealed packet resources[395].text.

````text
@pytest.mark.parametrize(
    ("source_range", "match"),
    [
        (PythonSourceRange(1, 30, 1, 29), "ends before"),
        (PythonSourceRange(1, 0, 2, 0), "line is outside"),
        (PythonSourceRange(1, 0, 1, 100), "column is outside"),
        (PythonSourceRange(1, 8, 1, 26), "UTF-8 character boundaries"),
    ],
)
def test_rejects_source_ranges_that_cannot_be_faithfully_applied(
    tmp_path: Path,
    source_range: PythonSourceRange,
    match: str,
) -> None:
    """Malformed coordinates fail instead of producing misleading source."""
    snapshot = _snapshot(tmp_path, 'def café(): return "olé"\n')
    disclosure = _disclosure(snapshot, "café")
    disclosure_item = disclosure.items[0]
    invalid_occurrence = replace(
        disclosure_item.source_occurrence,
        source_range=source_range,
    )
    invalid_item = replace(
        disclosure_item,
        source_occurrence=invalid_occurrence,
    )
    invalid_disclosure = replace(disclosure, items=(invalid_item,))

    with pytest.raises(PythonFunctionSourceMaterializationError, match=match):
        materialize_python_function_disclosure_source(
            disclosure=invalid_disclosure,
            snapshot=snapshot,
        )
````

### E0086 — R396 tests/context/python/function/test_qualified_reference.py

Span [8793, 10304), lines 220–263. Provenance: sealed packet resources[396].text.

````text
def test_stale_source_or_target_content_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    disclosure = disclose_python_qualified_reference(
        purpose="Inspect binding",
        analysis=analysis,
        reference=analysis.references[0],
    )
    newer = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n# change\n",
            "target.py": "def f():\n    return 1\n",
        },
    )
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="snapshot"):
        materialize_python_qualified_reference_source(
            disclosure=disclosure,
            snapshot=newer,
        )
    for stale_address, message in (
        ("consumer.py", "source content"),
        ("target.py", "Target declaration"),
    ):
        stale = replace(
            snapshot,
            resources=tuple(
                newer.resource_at(item.address)
                if item.address == RepositoryResourceAddress(stale_address)
                else item
                for item in snapshot.resources
            ),
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=stale,
            )
````

### E0087 — R396 tests/context/python/function/test_qualified_reference.py

Span [10306, 12460), lines 266–325. Provenance: sealed packet resources[396].text.

````text
def test_redirected_or_missing_resources_are_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
            "other.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    fact = analysis.references[0]
    other = RepositoryResourceAddress("other.py")
    redirected_source = replace(
        fact,
        occurrence=replace(fact.occurrence, resource_address=other),
    )
    redirected_target = replace(
        fact,
        target_declaration=replace(
            fact.target_declaration,
            support=replace(fact.target_declaration.support, resource_address=other),
        ),
    )
    for changed, message in (
        (redirected_source, "source dependency"),
        (redirected_target, "Target declaration resource"),
    ):
        altered_analysis = replace(analysis, references=(changed,))
        disclosure = disclose_python_qualified_reference(
            purpose="Inspect binding",
            analysis=altered_analysis,
            reference=changed,
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=snapshot,
            )
    disclosure = disclose_python_qualified_reference(
        purpose="Inspect binding",
        analysis=analysis,
        reference=fact,
    )
    for missing, message in (
        ("consumer.py", "source resource is missing"),
        ("target.py", "target resource is missing"),
    ):
        reduced = replace(
            snapshot,
            resources=tuple(
                item
                for item in snapshot.resources
                if item.address != RepositoryResourceAddress(missing)
            ),
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=reduced,
            )
````

### E0088 — R397 tests/context/python/function/test_rendering.py

Span [1780, 3796), lines 59–99. Provenance: sealed packet resources[397].text.

````text
def test_renders_ordered_duplicate_sync_and_async_context_exactly(
    tmp_path: Path,
) -> None:
    """The full path renders metadata and unchanged CRLF/non-ASCII source."""
    first_source = (
        'def duplicate():\r\n    return "caf\u00e9 --- exact source ends ---"'
    )
    second_source = 'async def duplicate():\r\n    return "na\u00efve"'
    context = _materialized_context(
        tmp_path,
        f"# pr\u00e9face\r\n{first_source}\r\n\r\n{second_source}\r\n",
        name="duplicate",
    )

    rendered = render_materialized_python_function_context(context)
    expected_match_count = len(context.items)

    assert isinstance(rendered, RenderedPythonFunctionContext)
    assert rendered.materialized_context is context
    assert rendered.FORMAT == "python-function-context-text-v1"
    assert "Exact declared-name purpose: duplicate\n" in rendered.text
    assert "Selected declarations: 2\n" in rendered.text
    assert rendered.text.count("Declared name: duplicate\n") == expected_match_count
    assert "Declaration kind: function-def\n" in rendered.text
    assert "Declaration kind: async-function-def\n" in rendered.text
    assert (
        rendered.text.count("Repository-relative resource: module.py\n")
        == expected_match_count
    )
    assert "Source location: 2:0-3:" in rendered.text
    assert "Source location: 5:0-6:" in rendered.text
    assert context.items[0].disclosure_item.proposition in rendered.text
    assert first_source in rendered.text
    assert second_source in rendered.text
    assert first_source.replace("\r\n", "\n") not in rendered.text
    assert second_source.replace("\r\n", "\n") not in rendered.text
    assert rendered.text.index(first_source) < rendered.text.index(second_source)
    for item in context.items:
        expected_length = len(item.source_text.encode("utf-8"))
        assert f"Exact source UTF-8 byte length: {expected_length}\n" in rendered.text
    assert render_materialized_python_function_context(context) == rendered
````

### E0089 — R398 tests/context/python/function/test_request_assembly.py

Span [2102, 4445), lines 70–132. Provenance: sealed packet resources[398].text.

````text
def test_assembles_real_context_after_distinct_unchanged_task(
    tmp_path: Path,
) -> None:
    """Assembly preserves task, Context, role, and every other request semantic."""
    rendered = _rendered_context(
        tmp_path,
        'def target():\r\n    return "caf\u00e9"\r\n',
        name="target",
    )
    task_text = "Fix target without changing behavior.\r\nKeep its public name."
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider_settings = ProviderRequestSettings("test-model")
    tools = (
        ModelToolDefinition(
            name="inspect",
            description="Inspect one value.",
            input_schema_json='{"type":"object"}',
        ),
    )
    task_request = ModelRequest(
        prompt=Prompt(content=task_text, role="user"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider_settings,
        tools=tools,
    )

    request = assemble_python_function_context_model_request(
        task_request=task_request,
        context=rendered,
    )

    assert isinstance(request, ModelRequest)
    assert request is not task_request
    assert request.prompt.role == task_request.prompt.role
    assert request.settings is settings
    assert request.conversation is continuation
    assert request.provider_settings is provider_settings
    assert request.tools is tools
    assert task_request.prompt.content == task_text
    assert task_text in request.prompt.content
    assert rendered.text in request.prompt.content
    assert request.prompt.content.index(task_text) < request.prompt.content.index(
        rendered.text,
    )
    assert (
        f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n"
        in request.prompt.content
    )
    assert (
        "Supporting repository Context UTF-8 byte length: "
        f"{len(rendered.text.encode('utf-8'))}\n"
    ) in request.prompt.content
    assert request.prompt.content.count('def target():\r\n    return "caf\u00e9"') == 1
    assert (
        assemble_python_function_context_model_request(
            task_request=task_request,
            context=rendered,
        )
        == request
    )
    assert not hasattr(request, "rendered_context")
````

### E0090 — R409 tests/context/python/modules/test_selection.py

Span [1753, 3213), lines 60–106. Provenance: sealed packet resources[409].text.

````text
@pytest.mark.parametrize(
    ("syntax", "kind"),
    [
        ("class Target: pass", Kind.CLASS),
        ("def Target(): pass", Kind.FUNCTION),
        ("async def Target(): pass", Kind.FUNCTION),
    ],
)
@pytest.mark.parametrize("prefix", ["", "@decorator\n"])
def test_plain_and_decorated_native_identity(
    syntax: str,
    kind: Kind,
    prefix: str,
) -> None:
    snapshot, module = _frame(prefix + syntax + "\n")
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == 1
    target = selected.declarations[0]
    assert target in (
        selected.class_analysis.classes
        if kind is Kind.CLASS
        else selected.function_analysis.declarations
    )
    assert target.subject.snapshot_id == snapshot.id
    assert target.support.resource_address == module.resource.address
    assert selected.module is module
    assert selected.kind is kind
    assert selected.declared_name == "Target"
    assert selected == select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    binding = lookup_python_module_declaration(
        snapshot,
        module=module,
        declared_name="Target",
    )
    assert binding.outcome is (
        BindingOutcome.NOT_DECLARATION if prefix else BindingOutcome.RESOLVED
    )
````

### E0091 — R409 tests/context/python/modules/test_selection.py

Span [3215, 4370), lines 109–137. Provenance: sealed packet resources[409].text.

````text
@pytest.mark.parametrize(
    ("content", "kind", "count"),
    [
        ("class Target: pass\nclass Target: pass\n", Kind.CLASS, 2),
        ("def Target(): pass\ndef Target(): pass\n", Kind.FUNCTION, 2),
        ("class Target: pass\ndef Target(): pass\n", Kind.CLASS, 1),
        ("class Target: pass\ndef Target(): pass\n", Kind.FUNCTION, 1),
        ("class Target: pass\n", Kind.FUNCTION, 0),
        ("def Target(): pass\n", Kind.CLASS, 0),
        ("class target: pass\n", Kind.CLASS, 0),
        ("if enabled:\n    class Target: pass\n", Kind.CLASS, 0),
        ("Target = lambda: None\n", Kind.FUNCTION, 0),
        ("@decorator\nclass Target: pass\nTarget = other\nexec(code)\n", Kind.CLASS, 1),
    ],
)
def test_exact_kind_scope_and_repeated_declarations(
    content: str,
    kind: Kind,
    count: int,
) -> None:
    snapshot, module = _frame(content)
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == count
    assert len({item.subject.identity for item in selected.declarations}) == count
````

### E0092 — R409 tests/context/python/modules/test_selection.py

Span [4372, 5620), lines 140–173. Provenance: sealed packet resources[409].text.

````text
def test_selection_rejects_invalid_and_foreign_inputs() -> None:
    snapshot, module = _frame("class Target: pass\n")
    with pytest.raises(ValueError, match="identifier"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="a.b",
            kind=Kind.CLASS,
        )
    with pytest.raises(TypeError, match="unsupported kind"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="Target",
            kind="class",  # type: ignore[arg-type]
        )
    for foreign in (
        replace(
            module,
            repository_id=RepositoryId.parse("00000000-0000-0000-0000-000000000002"),
        ),
        replace(module, snapshot_id=RepositorySnapshotId("b" * 64)),
        replace(
            module,
            resource=replace(module.resource, content="class Different: pass\n"),
        ),
    ):
        with pytest.raises(ValueError, match="differs from the supplied snapshot"):
            select_python_module_source_declarations(
                snapshot,
                module=foreign,
                declared_name="Target",
                kind=Kind.CLASS,
            )
````

### E0093 — R473 tests/models/interaction/test_models.py

Span [3269, 4005), lines 96–108. Provenance: sealed packet resources[473].text.

````text
def test_model_request_is_immutable_and_separates_input_from_settings() -> None:
    """One request contains semantic input, portable settings, and continuation."""
    source = InteractionSource("llama.cpp")
    request = ModelRequest(
        prompt=Prompt(content="question", role="user"),
        settings=ModelSettings(maximum_output_tokens=_REQUEST_OUTPUT_TOKENS),
        conversation=ConversationRef(source, "thread"),
    )
    assert request.prompt.content == "question"
    assert request.settings.maximum_output_tokens == _REQUEST_OUTPUT_TOKENS
    assert request.conversation == ConversationRef(source, "thread")
    with pytest.raises(FrozenInstanceError):
        request.settings = ModelSettings()  # type: ignore[misc]
````

### E0094 — R524 tests/scripts/test_validate_development.py

Span [888, 1503), lines 35–48. Provenance: sealed packet resources[524].text.

````text
def test_profile_selects_tests_and_excludes_experiment_tests_before_collection(
    validation_script: ModuleType,
) -> None:
    """The directory boundary covers the whole retained experiment population."""
    arguments = validation_script.pytest_arguments(Path.cwd())
    tests = Path(arguments[0])
    ignored = Path(arguments[1].removeprefix("--ignore="))

    assert tests == Path.cwd() / "tests"
    assert ignored == tests / "experiments"
    assert tests.is_dir()
    assert ignored.is_dir()
    assert (tests / "context").is_dir()
    assert (tests / "scripts" / "test_validate_development.py").is_file()
````

### E0095 — R524 tests/scripts/test_validate_development.py

Span [1505, 2104), lines 51–68. Provenance: sealed packet resources[524].text.

````text
def test_profile_propagates_pytest_failure_code(
    validation_script: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed pytest run remains a failed profile invocation."""
    observed_arguments: list[str] | None = None

    def failed_pytest(arguments: list[str]) -> int:
        nonlocal observed_arguments
        observed_arguments = arguments
        return 1

    monkeypatch.setattr(validation_script.pytest, "main", failed_pytest)

    result = validation_script.main()

    assert result == 1
    assert observed_arguments == validation_script.pytest_arguments()
````

### E0096 — R006 docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md

Span [30700, 31482), lines 512–524. Provenance: sealed packet resources[6].text.

````text
## Status and implementation boundary

This decision accepts Context/disclosure semantics only. It does not implement
a compiler, DisclosureOption, DisclosurePlan, ContextDisclosure,
representation/coverage/satisfaction model, decomposition mechanism,
utility/stopping/budget policy, availability/history store, applicability cache,
capability/behavior profile, assembly layer, tokenizer integration, derived
representation, semantic-transformation or synthesis mechanism, synthesis
store, persistence, or evaluation infrastructure. B-0002 retains this
unimplemented design pressure.
ADR-0001 remains the model-native Tool boundary; ADR-0002 remains repository
identity/derivation/graph architecture; ADR-0003 remains InformationNeed,
retrieval, evidence, and ranking architecture.
````
