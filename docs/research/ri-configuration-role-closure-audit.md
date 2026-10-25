# RI configuration, role and closure assurance

Delivered follow-through: [one-facade binding repair](../development/ri-facade-binding-repair.md), production `cf9db4af17516dc19092f1ae18c197783f1f5b3d`, PR#8, verified main `5a5485e98908922722ba2a4b177094364c1aac31`. Proposal ff4c4110 has implemented-and-merged advisory evidence; do not repeat the repair/adoption. Earlier P1-pending notices below are dated history. The next RI fixture/operational scope remains unchanged; A+C is unapproved and this repair adds no audit-cohort credit.

Baseline: integrated main `457defb3e97770c6ef8db4b5faf681ebc202f0a9`.
Branch: `audit/ri-config-role-assurance-20261024`. This is maintainer-authorized
audit and Intake work, not a production repair, accepted architectural decision,
scientific rerun or successor-session dossier. PRs #2–#6 and the three maintained
source repairs are ancestors of this baseline. Checkout ownership was absent;
the index and tracked worktree were clean before edits. All thirteen original
forensic files match the existing recorded SHA256 values.

The [exact review evidence](code-audit/ri-config-role-assurance.json) extends
the existing fixture and historical ledgers. The frozen input is
[ri-assurance-next-cohort.json](code-audit/ri-assurance-next-cohort.json),
Git blob `67b979be06f8a6e147c48af8bba45c48852d9c0a`. All ten selected current
blobs still match their frozen identities. All eight older bodies were read
from exact Git objects, without checking out or executing historical code.

## Result and immediate engineering priority

One independently reproduced **P1 production correctness defect** remains:
[one-facade binding fallback](../backlog/proposals/ff4c4110-9c3b-480d-8f0f-77cf4610b700/proposal.json).
It is a separate owner from the recently delivered three-owner binding repair.
The corrected direct lookup refuses competing bindings, but an older facade
fallback can override that refusal and emit a false qualified Reference.
This prevents a clean maintained-correctness signoff. Repair this bounded path
next, with real-source regressions and the exact final-tree protected gate.
No production code or tests were changed by this audit.

Original fixture coverage advances **57/93 → 67/93**, leaving **26** paths:
four substantive test/helper bodies and twenty-two namespace markers. The
augmented fixture ledger is **68/94**. Historical exact versions advance
**7 → 15 full-body reviews**; **168 NOT_REVIEWED** and **20 tip-delta-only**
remain, totaling **188** outstanding exact obligations. Experimental source
review stays **606/606**; this is not independent revalidation of all judgments,
completion of maintained RI assurance or autonomous-agent effectiveness.

## Ten maintained fixture reviews

Every listed body, helper, parametrized case, monkeypatch and error expectation
was inspected. The exact function cursors, Git blobs and byte-domain SHA256s
are in the review evidence and existing `ri-completion-fixtures.jsonl`.
Execution alone was not used to award review credit.

| Path under `tests/context/` | Independent assurance and remaining limit |
| --- | --- |
| `localization/roles/helpers.py` | Actual files, retained observation, explicit module universe/configuration frames. The title says synthetic, but snapshots are genuinely observed. Default newline conversion is appropriate here, not an independent physical-byte oracle. |
| `localization/roles/test_configuration.py` | Literal configuration roles and target hints; ordered duplicate supports, bounded case-sensitive basename globs, missing scopes, malformed/unsupported inputs, retained bytes and nested roots. Opaque pytest `addopts` never becomes collection/exclusion truth. |
| `localization/roles/test_dependency_groups.py` | Group-name grammar/collisions, whole-array refusal, empty versus absent, valid siblings, changed-source identity and forged/stale replay. A group called test/lint/docs supplies PROJECT_CONFIGURATION, not semantic resource roles. |
| `localization/roles/test_evidence.py` | Real native module/membership/mirror supports, positive multi-label conventions, deterministic dedup, empty/unknown/foreign resources. No exclusion, score, runtime validation or witness satisfaction is inferred. |
| `python/project_configuration/test_configuration.py` | Literal selectors/targets and unsupported shapes; explicit source/tool/module roots, retained bytes, stale/foreign/forged frames, ambiguous alternatives. One actual-repository pyproject smoke is config-coupled; independent literal fixtures protect the local contracts. An impossible prefix/exact collision intentionally tests resolver alternatives, not filesystem realism. |
| `python/project_configuration/test_dependency_groups.py` | Ordered raw strings, duplicate occurrences, normalized collisions, invalid/mixed/include shapes, empty/absent distinctions and native setting replay. Invalid requirement text can be retained: this is not a packaging resolver or installer. |
| `python/project_configuration/test_obstructions.py` | Scalar/array parents remain unsupported, not absent; mixed valid branches, dynamic/empty/malformed and retained-source identities. Generic enum-derived selector expectations are supplemented by literal independent branch assertions. |
| `python/project_configuration/test_settings.py` | Literal metadata/build/pytest/entrypoint shapes, reserved/unsupported/dynamic/empty states, JSON key/value shape identity, duplicate/forged replay. Raw strings and table presence do not establish registration or effective execution. |
| `python/test_source_candidacy.py` | Real discovery and literal seven-file → four suffix candidates → three token hits → one direct function → exact text/request composition. Lowercase `.py` is a narrow convention; token hits are not declarations. Projection monkeypatches correctly assert no hidden acquisition. Constructing a ModelRequest is not model invocation. |
| `retrieval/lexical/test_analysis.py` | Independently written Unicode words/casefold, character spans, repeated terms, document locality, empty and encounter order. Synthetic data is appropriate for tokenizer arithmetic. No identifier decomposition, retained-source authentication or task-relevance claim. |

No new bug was established in these ten contracts themselves. They do not test
every neighboring contract: in particular, the passing facade tests omit the
competing non-Name forms below. The lexical helper's existing concatenation
collision and explicit-empty issue remain covered by
[a88167f9](../backlog/proposals/a88167f9-2688-478c-9659-202d05e61e1e/proposal.json).
Do not duplicate that story or call synthetic arithmetic inherently invalid.
Configuration test helpers have different frames, roots and identity intent;
a universal fixture framework is not justified.

## Eight older exact versions

The table gives short blob labels for navigation; the linked evidence contains
full immutable identities, complete class/function cursors, prior depth,
maintained comparison blobs and per-version dispositions. No old runtime or
scientific controller was executed. Tests of the current replacement are not
credited as historical test execution.

| Historical owner / blob | Full-body comparison and disposition |
| --- | --- |
| roles/configuration `485f158d` | Complete supports, targets and limitations; current adds dependency-group settings as PROJECT_CONFIGURATION only. The old coherent setting producer emitted no groups. Hypothetically mixing old/new producers is not evidence of original corruption. Superseded. |
| roles/models `31ae660b` | Full role/support/query/digest body; current semantics v2 binds the additional group behavior. Stable fields do not make the semantics-version dependency identical. Superseded. |
| project_configuration/declarations `0d781829` | v2 parser/settings analysis conflates missing keys and non-table parents through `_at`. Current sentinel lookup and obstruction fixtures fix this historical false-absence behavior. Already superseded; no new repair. |
| project_configuration/declarations `c3150c4d` | v3 already distinguishes missing/non-table; current v4 incorporates the expanded setting producer. The earlier obstruction bug is absent here. Superseded. |
| project_configuration/declarations `d86c09c7` | v1 six selectors, entrypoint presence only and no setting field; same missing/non-table conflation. Current richer raw settings and sentinel distinction replace it. No obsolete API restoration. |
| project_configuration/models `16905ccf` | Full original declarations, frames, target outcomes and identities; current adds setting identities and versioned scope. No unique useful behavior lost. Superseded. |
| project_configuration/models `16e6d669` | Complete current-shaped models; SCOPEv2 → v3 is meaningful supported-contract versioning, despite otherwise matching bodies. Superseded. |
| project_configuration/settings `8544f679` | Complete metadata/build/pytest/entrypoint/dynamic/lookup producer; current adds group-name validation, normalization collisions and whole raw arrays. Neither version executes or resolves package installations. Superseded. |

Two previously NOT_REVIEWED and six tip-only rows now have full body/contract
review. Current and old dependency validation remain separate evidence; no
AST similarity or replacement inspection is used to close a different blob.

## Independent production counterexample

The [preserved probe](code-audit/ri-config-role-probes.json) contains the full
independently authored programs, literal inputs, observed outputs, dependency
identities and producer blobs. Three small files suffice:

```python
# src/target.py
def f():
    pass

# src/facade.py
from target import f
match 0:
    case f:
        pass

# src/use.py
from facade import f
f()
```

Real discovery/observation and native AST derivation produce a direct facade
lookup refusal, yet `resolve_python_imported_member` returns RESOLVED and
Reference resolution emits route `one-facade-imported-member` to `target.f`.
Star capture, mapping-rest capture and an exception-handler `as f` reproduce
the same false-positive path. Plain facade import correctly resolves; ordinary
`f = 0` correctly refuses. Captures can replace the name; an exception alias has
a different handler/deletion lifetime. Neither permits asserting the previous
function as the uniquely established binding after this syntax.

`imports/members.py:_inspect_facade_bindings` only recognizes a small list of
direct competitors and nested imports. It misses these string-valued AST
binding names. `references/declarations/resolution.py:_resolve` tries this
fallback after *any* nonpositive direct member lookup, including an authenticated
ambiguous binding. It then replaces the refusal with positive ONE_FACADE truth.
The genuine direct lookup repair in `ab994225` remains correct and delivered.

A second, independently constructed task with admitted `src/devtools/target.py`,
`src/devtools/facade.py` and `tests/test_use.py` exercised actual
`ContextTools.dispatch` → ToolRunner → `source_relationships`. Capture and
handler cases returned the same false target, with current source versions and
native provenance. This establishes an exposed maintained consumer, not just
an isolated helper concern. It does **not** establish actual autonomous model
invocation, historical engineering harm, edit-admission bypass or a new
controlled effectiveness result. Source fixtures were never executed.

Pending repair acceptance must protect the complete facade/Reference/Tool
composition, including qualified refusal, genuine unchanged sync/async imports,
scope/order and handler lifetime, unrelated or nested-local names, ordinary
assignment controls, source freshness and provenance. Reuse
`modules.bindings` only where traversal semantics match. Do not repair this by
claiming runtime evaluation, hiding all valid facade imports or changing
syntactic declaration selection. The exact resolver/fallback repair belongs in
a separate production commit with permanent independent regressions and the
full protected gate; this audit has not implemented it.

## Maintained ownership, cohesion and actual consumers

The intended dependency direction remains coherent under
[ADR-0002](../architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md),
[ADR-0003](../architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md),
[ADR-0004](../architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
and [ADR-0005](../architecture/decisions/ADR-0005-obligation-driven-repository-localization.md):

1. Repository observation owns retained resources, snapshot and content identity.
   Native Python analyses derive static facts and dependencies, not runtime truth.
2. Project configuration owns raw TOML declarations/settings and explicit scoped
   target resolution. Its replay rejects forged settings/source frames. Roles
   consume canonical analyses, add qualified positive hints and leave unsupported
   or omitted inputs visible. Neither owner executes tools or interprets task
   satisfaction; RI does not depend on Localization.
3. Retrieval owns lexical/structural candidates and native rankings. Localization
   owns caller-supplied obligations, associations, semantic resolution, witnesses
   and scoped readiness. Role preference/escape is a separate caller-directed
   view after acquisition, not a source-admission veto or correctness oracle.
4. Planning owns selected representations, capacity, exact materialization and
   request assembly. Discovery, a resolved locator, role support, an accepted
   witness, disclosure and edit authority are distinct contracts.
5. Native `CodingTask` admits objective, corpus, source/read/edit bounds and fixed
   checks. `ContextTools` observes that corpus, builds the source index, exposes
   search/read/symbol/relationship operations and uses Planning exact disclosures.
   Edits/checks/freshness are separate application owners and host decisions.

The current `ContextTools._reference_analysis` and `_relationships` genuinely
consume References; optional map composition reuses that native analysis.
The new bug is harmful contract duplication: a legacy facade competitor check
disagrees with canonical module binding checks and its consumer upgrades refusal.
Consolidate only the compatible binding-name extraction/guard contract in the
bounded repair, not all scopes or parsers.

Search of supported source/apps/scripts finds configuration/role derivation
consumed by its framework validation/composition owners and tests; there is no
native coding-loop caller supplying those richer role/configuration analyses.
The exact-name candidacy test composes a genuine framework request, whereas the
native worker uses the separate source-index/SourceSearchDisclosureOption path.
Do not claim the test proves native use of every legacy function-context API.

Existing authenticated [native receipts](code-audit/agent-use.json) and
[follow-up receipts](code-audit/ri-followup-agent-use.json) establish real
source-search/read and subsequent edits/checks at their recorded evidence level.
No new receipt or inference was generated here. They do not demonstrate full
Localization, role-assisted task strategy, reviewed witness promotion or
autonomous obligation authorship. The new deterministic Tool call proves a
mechanism and its defect, not autonomous choice or effectiveness.

Repeated module interpretation/native replay may be expensive in map or future
Localization composition. It is not a measured optimization in this audit;
retain the existing measured-reuse proposal and source freshness requirements.
Raw settings, selectors, resource occurrences, role supports and witnesses
represent different facts and should not be flattened into a common score/type.
Model-neutral Tools and source-neutral lexical arithmetic are useful extension
boundaries; Python AST semantics remain in the Python package. A new language
must provide qualified derivation, not inherit Python conventions accidentally.

## RI readiness: explicit disposition

| Question | Current supported answer |
| --- | --- |
| A. Maintained correctness | **Not P1-clean**: the independently reproduced facade fallback above is live and awaiting repair. No new P0 is established. Delivered physical-line, exact-name and three-owner module-binding fixes remain delivered. |
| B. Ownership | Broad RI boundaries are reviewed and coherent. The duplicate facade guard/refusal upgrade is a concrete local contradiction to repair, not justification for a replacement graph/scope/Context system. |
| C. Test assurance | Ten selected bodies now reviewed. Four substantive original fixture/helper bodies and22 markers remain; facade tests pass while omitting real competing forms. Historical negative oracles also remain. Passing branch coverage cannot replace these semantic reviews. |
| D. Consumers | Search/read/selected source and edits/checks have original native evidence. Relationships have a real exposed native caller and this deterministic probe. Configuration roles and full Localization remain framework/host capabilities without demonstrated autonomous use. |
| E. Integration | Existing Localization/exact-hint/direct-base/Delta proposals remain the homes. A trusted/reviewed task-clause account, revised needs, authorized acquisition, actual model-visible source, explicit witness review, edit/check/freshness must compose before claiming end-to-end readiness. |
| F. History |15 full,168 unread,20 tip-only exact versions. Remaining historical risk is unique dependency/negative behavior or lost useful semantics, not evidence that current production inherits every old defect. |
| G. Backlog | New facade P1 has its own pending record and acceptance. Delivered repairs have merged evidence and should not be rescheduled. Separate science, fixture and unapproved consumer work retains canonical records; no approval/closure is inferred. |

**RI architecture reviewed** means the ownership/dataflow conclusions above,
with the listed local defect and incomplete assurance. **RI historical assurance
complete** is false while188 exact versions remain. **RI autonomous-agent
capability complete** is false while obligation authorship, semantic review and
Localization/witness consumption lack the native end-to-end consumer/evaluation.
This is not yet a final RI subsystem signoff.

The [A+C decision preparation](task-obligation-coverage-decision.md) remains
recommended and **unapproved**. This audit adds no materially new architecture
choice requiring the maintainer to revisit it. Reviewed roster accountability
does not prove exhaustive objective decomposition. A future independent,
delegable reviewer must distinguish supported/contradicted/unresolved evidence;
rank/role/relationship presence cannot promote a witness. Task-only evidence
must not be encoded as invented repository witnesses. Checks, semantic readiness,
freshness and publication remain separate claims. Agent-proposed obligations
and independent review require their explicit follow-on milestone and evidence.

## Backlog reconciliation

The [Intake evidence](code-audit/ri-config-role-intake.json) records **one new
pending bug**, an advisory on it, and **one material advisory on an existing
record**: delivered `16b27e74` versus the distinct facade/fallback dependency.
No B-number, grant, approval, dispatch, closure or parent-state change occurred.

| Existing record | Verified disposition / next operator action |
| --- | --- |
| `954a7136` | Exact-name repair `7541a1a` is on main, with permanent source-identity regressions. Reconcile delivered acceptance; do not schedule implementation or adoption again. |
| `416658bd`, `5aa7a431` | Physical-line repair `a0a6c224` is on main. Reconcile delivered primary and overlapping scope through authorized review, retaining both histories. Historical SourceSpans is a separate unfinished owner. |
| `16b27e74` | Three-owner repair `ab994225` is on main. Advisory identifies the separate facade fallback above; no reopening or duplicate scheduling of completed code. |
| `2e70de9a` | Supported versioned scientific binding verifier is delivered on main. Unchecked older public consumers and Increment24 digest closure remain unfinished. Do not close the entire concern or rerun original judgments. |
| `a88167f9` | Existing fixture collision/empty-selection/runtime-certificate record is sufficient. The newly reviewed tokenizer arithmetic does not independently authenticate source identity. |
| `15bae0a6`, exact-hint, direct-base, Delta | Existing integration records remain sufficient; no new planner/compiler or duplicate proposal. Positive role and reference facts require semantic review before witness use. A+C is not approved. |
| measured reuse / exact-tree input closure | Existing proposals remain sufficient. No timing evidence, cache implementation or validation-reuse policy change here. |

Historical span/recovery, neutral binding, diagnostic ranking, Graph3 report,
U2 missing-witness and task-normalization defects retain their distinct prior
owners and risk qualifications. This cohort neither repaired those frozen
implementations nor established a live execution-authority vulnerability.
Current configuration's old non-table false-absence behavior is verified
superseded and covered: no new story or frozen-source refactor is warranted.

## Finite assurance exit and operational transition

The [remaining exact-version grouping](code-audit/ri-config-role-history-closure.json)
reuses the203-row version universe. It is dated scheduling evidence, not a new
runtime registry or review credit. Its188 outstanding records are partitioned
once; test oracles are separate from source owners, with their owning paths
retained. Fingerprints from the earlier grouping remain prioritization only.

| Responsibility | Remaining exact versions | Owner, risk and bounded closure evidence |
| --- | ---: | --- |
| Repository observation/source admission |9 | Current `context.repository`; compare decoding, content/snapshot/dependency identity, discovery bounds and error contracts against current repairs. High priority. Related historical tests are in the57-oracle group. |
| Python module/configuration/structural relationships |6 | Current `context.python`; compare binding/scope/source-order and relationship admission, not just syntax or AST shape. The eight reviewed config/role versions are already removed from this remainder. |
| Lexical/graph/map retrieval |14 | Current Retrieval plus Planning map projection; independent numeric/tie/unknown/ranked-only inputs, production-version dependency closure. No historical benchmark replay. |
| Localization/witness/readiness |13 | Existing Localization; review scope/identity/negative and ALL/ANY transitions, review authority and current consumer migration. No automatic A+C adoption. |
| Planning/disclosure/materialization |12 | Current Planning and Python function Context; compare whole selected-source/dependency/text correspondence and byte/physical-line refusal against delivered fixes. High priority. |
| Exports/packaging/legacy Context relocation |77 | Verify public target ownership, import availability and dependency direction; legacy Conversation/history/message/session moved to Agents needs explicit relocation/consumer evidence. Namespace-only is not an algorithm, but changed exports cannot be ignored. |
| Historical tests/oracles/failure contracts |57 | Review independent literal expectations, fixture authenticity, failure/negative and old API assumptions with each source-family cohort. No self-reconstruction or current-test pass substitutes for full old-body review. |

Close these as responsibility cohorts, not170 one-file assignments. Every row
needs a complete body/contract comparison or narrowly authenticated exact-byte
equivalence *with unchanged dependencies and public/authority assumptions*.
Mechanical import/format/AST similarity alone is insufficient. Supersession
requires identifying the replacement and demonstrating no unique promised
behavior/consumer was lost; retain historical defects and limitations explicitly.
Exports can share target checks, and old tests can be paired with their source
family, while retaining a separate exact-row disposition. No such future review
credit is awarded by this partition.

The [next exact cohort](code-audit/ri-config-role-next-cohort.json) freezes all
remaining26 original fixtures (four substantive,22 markers) and22 repository
source/test/export versions, including the nine source-admission obligations.
It has **not begun**. First perform the bounded facade P1 repair, then close the
four meaningful fixture bodies and authenticate the namespace surfaces. The
remaining historical families need not indefinitely block operational auditing:
carry them as explicit parallel program obligations, prioritizing source
admission/materialization and negative-oracle differences. Do not declare RI
historical assurance complete before every remaining row has a disposition.

The next operational scope remains the prior
[cohesive lifecycle audit](ri-assurance-and-cohesion-audit.md), not new framework
implementation. Relevant entry-point blobs are unchanged by the recent binding
repair/docs merges: `scripts/backlog/{__main__,work,checkout,delegation}.py`,
`integration/{authority,local,lifecycle,validation,git,cli}.py`, native
`coding_loop`, `ContextTools`, edits/commands/checks, `tools.execution.ToolRunner`
and execution runtime/interaction-attempt. The checkpoint authenticates this
comparison. Do not begin those bodies in this assignment.

Prioritize task/scope/owner → Tool validation versus authority → mutation and
partial effects → fixed checks/freshness → interrupted recovery without blind
retry → independent review/destination integration/normal publication. Their
evidence must bind actual producers/consumers and ambiguous external effects.
This is the natural next major domain because reliable source facts alone do
not establish that agents act, recover and publish safely. Other Core/Resources,
models/Agents, persistence, observability, applications/dashboard and developer
tooling still require comparable review before the successor handoff.

## Validation and publication

Focused deterministic suites: **296 passed in6.46s** for the selected role,
configuration, candidacy/tokenizer and adjacent facade/Reference contracts.
The independent probe has four defective forms and two controls; actual
ContextTools dispatch adds three bounded composition cases without inference.
Additional delivered source/function/base/Tool regressions and final
documentation checks are recorded in the
[checkpoint validation](code-audit/ri-config-role-checkpoint.json).

All changed paths are research/navigation/Intake documentation. Source, tests,
applications, operational scripts and configuration are byte-equivalent to the
integrated baseline. Consequently no new protected production gate, mypy or
production Ruff/format success is claimed. The prior PR5 result2808 pass/two
live skips/100% remains prior validation, not a fresh gate. Broad frozen-science
lint/formatter limitations are neither fixed nor represented as passing here.
Final validation checks JSON/JSONL, exact ledgers/blobs, links/layout, Intake
hash chains, source input equality, Git whitespace and thirteen forensics.

Publication uses this one audit branch and the normal GitHub PR process,
with actual permissions/checks/reviews evaluated and no direct main write,
protection change, fake approval or deleted historical ref. The containing
commit binds these checkpoint records; the final local completion report
records the actual accepted PR/main identity after publication.
