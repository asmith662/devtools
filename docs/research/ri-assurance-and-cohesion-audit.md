# Integrated RI assurance and architectural cohesion audit

Reviewed baseline: `5f53f5ac34b1a8a91e3119aa5faba329b8dedfa4`, ordinary branch
`audit/ri-assurance-cohesion-20261024`. This is an audit checkpoint, not an
accepted architecture decision or production repair. PR #2 production integration
and PR #3 documentation closeout are ancestors of the baseline. Both RI source
corrections are on main; their implementation and adoption must not be scheduled
again. The canonical checkout owner was absent, tracked/index state clean, and
all thirteen original forensic hashes matched. No historical source or result
was executed or modified.

The exact [review record](code-audit/ri-assurance-cohesion.json) extends the
existing ledgers. The frozen [input cohort](code-audit/ri-completion-next-cohort.json)
is unchanged. Four current fixtures differ from the selection through integration:
three are AST-identical formatting; import declarations additionally has the
actual `RepositorySnapshot` annotation instead of `object` and obsolete ignores.
The latter already had full integration-review credit. Several older manifest
SHA256 values identify CRLF checkout bytes, not Git blob bytes; the record keeps
both domains and qualifies the deterministic CRLF correspondence. It does not
claim recovery of unavailable original physical bytes. All selected Git blobs
and all twelve current counterparts were authenticated.

## Results and limits

- Twelve selected current fixture modules received full body/helper/negative-path
  review; eleven are new path credit. **57/93 original fixtures** are fully
  reviewed, leaving **36**. The augmented universe is **58/94**.
- All seven selected historical bodies were read independently, including
  original and changed fixtures. **170** older versions remain NOT_REVIEWED and
  **26** remain tip-delta-only; seven now have full body/contract dispositions.
- Historical experimental source coverage stays **606/606** at its defined
  source-review depth. No judgment revalidation or new effectiveness claim.
- **121 selected maintained tests passed.** Twelve independent real-source
  fixture variants exposed one production binding correctness family, now
  [pending16b27e74](../backlog/proposals/16b27e74-f553-40a8-b342-c3458a7b7a01/proposal.json).
  Production source/tests were deliberately left unchanged; this checkpoint
  records the repair boundary and permanent-regression requirements.

## Selected maintained fixture assurance

All paths below are under `tests/context/`. The record and updated
[fixture ledger](code-audit/ri-completion-fixtures.jsonl) retain full Git identities,
all reviewed functions and each fixture's exact limits.

| Module | Independently specified protection and limitation |
| --- | --- |
| `python/imports/test_declarations.py` | Real observed source; twelve ordered import aliases/levels, shared statement support, direct-body exclusion, parse failure and explicit address. Rechecked; already credited during integration. Not runtime importability. |
| `python/imports/test_relations.py` | Real declarations/resolution/interpretation; repeated directed facts, relative/self imports, missing/ambiguous sources, foreign resolution, root/universe/content dependencies. Some target text deliberately need not parse: module interpretation is path-based. |
| `python/references/declarations/test_analysis.py` | Real retained source and qualified local/module/member/method routes; shadowing, wildcard/dynamic/decorated/nested unsupported states, foreign frames and no reacquisition. Isolated `_Binding`/missing-segment patches test guards, not native derivation. Missing module capture/exception alias cases permit the new defect. |
| `python/modules/test_membership.py` | Real immediate-package facts, explicit root, missing/nonpackage/ambiguous outcomes, foreign/duplicate/self containment refusal. One replaced dotted name deliberately constructs ambiguity; it is not a native ambiguity demonstration. |
| `python/modules/test_selection.py` | Native syntax derivation on a nominal manually constructed frame; declared-name/kind/order/duplicate/decorator selection and foreign frame guards. Source declaration syntax deliberately differs from unique namespace binding. Does not establish observation/content authentication. |
| `python/test_mirrored_paths.py` | Real source/test observations; exact correspondence, near-name/extension/init exclusions, retained-after-delete, snapshot/order/duplicate dependencies. No test ownership, executed coverage or semantic relevance claim. |
| `retrieval/test_composition.py` | Real observed `_facts` helper plus lexical corpus; retains multiple native supports without ranking, refuses stale entire corpus even if a hit is unchanged, foreign/purpose/conflicting statistics and resource mismatches. Post-derivation AST patch protects no reparse in composition. |
| `repository/test_corpus.py` | Explicit discovered subset, canonical realization, identity sensitivity and empty/missing/duplicate/foreign behavior. Some nominal snapshots isolate no-work projection; not an authenticity test. Empty membership correctly has no resource dependency. |
| `repository/test_document.py` | Real observed Unicode/CRLF literal text, ordered exact resources and repository/content-sensitive document identity. Identity intentionally ignores unrelated corpus members; no acquisition/parser work. |
| `retrieval/lexical/test_index.py` | Literal vocabulary/postings/term-frequency and encounter order, empty/rebuild/no-retokenization behavior. Synthetic arithmetic is appropriate; no source-authenticity claim. |
| `retrieval/lexical/test_statistics.py` | Hand-specified lengths `(3,2,0,3)`, mean2, distinct-document DF and repeated TF, empty/all-empty semantics. No model or semantic relevance claim. |
| `retrieval/lexical/test_evaluation.py` | Explicit heterogeneous fixture-designated relevance, literal rank/hit/recall/MRR, misses and invalid bounds/query/corpus cases. Repeat equality is only determinism; designated binary relevance is not task sufficiency or runtime selection. |

The lexical `_helpers.py` concatenation collision remains the already actionable
[fixture proposal](../backlog/proposals/a88167f9-2688-478c-9659-202d05e61e1e/proposal.json).
Neither synthetic arithmetic nor nominal identities are inherently bad tests.
They must not be reported as complete retained-source integration. Its existing
explicit-empty resolver-helper defect remains separate from production behavior.
Dependency-helper inspection here grants no extra fixture path credit.

## Confirmed production defect: non-Name module bindings

Minimal independently authored source, observed through the actual filesystem
and repository observation APIs:

```python
def f():
    pass
match 0:
    case f:
        pass
f()
```

`lookup_python_module_declaration(..., declared_name="f")` returns RESOLVED,
and `derive_python_declaration_references` records the final `f()` as a positive
Reference to the earlier function. The capture binds `f` to0, so the code has
another binding and cannot establish the owner's advertised unique direct
declaration claim. This is not an objection that static RI fails to execute
Python; the explicit conservative binding guard missed visible syntax.

The same false positives occur for `case [*f]`, `case {**f}` and
`except ValueError as f`. The exception name is bound and subsequently cleared;
it does not leave the original declaration safely resolved. Replacing the
function with a class also yields positive local and imported direct-base
assessments after those competing bindings. Two clean controls resolve;
two ordinary-assignment controls correctly return ambiguous/nonpositive results.
The full twelve inputs/results and reproducible probe source are retained in
[ri-assurance-probes.json](code-audit/ri-assurance-probes.json). Inputs were parsed,
never executed. An initial probe invocation omitted the observation byte bound
and failed before observation; the corrected probe includes4096 and completed.

Actual owners are `python/modules/declarations.py`,
`python/references/declarations/bindings.py:_module_bindings` and
`python/classes/bases.py:_bindings`. All recognize competing `ast.Name` stores;
the relevant names above are string attributes on other AST nodes. The existing
Reference `_scope_bindings` **already handles these names for function-local
shadowing**, demonstrating a concrete reuse opportunity with different traversal
semantics. Do not copy a whole scope visitor across module/order boundaries.

Severity: P1 incorrect qualified RI facts. `ContextTools._reference_analysis`
and `_relationships` consume Reference facts, and optional
`RepositoryMapNavigation` incorporates them. This proves a maintained host/Tool
path, not observed model invocation of this input, runtime graph truth,
historical outcome corruption or edit-authority bypass. Exact source syntax
selection should continue finding the original declaration even when namespace
binding is ambiguous. Repairing lookup must not erase source declarations.

One [pending bug](../backlog/proposals/16b27e74-f553-40a8-b342-c3458a7b7a01/proposal.json)
owns the three manifestations and independent negative matrix. Full repair needs
scope/order review across those owners, caller composition and final-tree100%
protected validation. It is the immediate bounded implementation priority;
this documentation audit does not silently widen Python binding semantics.

## Seven historical bodies and current counterparts

| Exact Git blob | Substantive review and disposition |
| --- | --- |
| `8927e55d1126c2ec0af6925ab8bc827e514e735e` | Full old `classes/bases.py`: local/member/module routes, explicit unsupported/ambiguous states, source support and target cache. Current code replaces ad hoc target bindings with canonical module declaration lookup and includes that lookup in identity. Old local capture/alias gap persists in current owner. Superseded implementation, not a lost alternate graph capability. |
| `7d0357aca237718a88959d494734099ea9a14230` | Single-resource function materializer: snapshot/address checks, splitlines and slice-decode geometry; no selected-match/dependency correspondence. Superseded by physical-line/endpoint validation and integrated exact-name repair. |
| `a6375e143fa10850e307d6efc2e4ac955d461ac4` | Multi-resource `resource_at` plus translated missing-address error; same old extraction/identity limitation. Multi-resource behavior adopted; integrity strengthened. |
| `905d79805a1c31c9109cfa202e551467575c1f32` |239-line real-source fixture: literal sync/async, CRLF/Unicode, bounds, changed snapshot/address, zero and no-upstream work. Uses obsolete single-resource `replace(resource=...)`; does not test legitimate equal-geometry redirection. |
| `c40a4804a80fe8703ba7b43274f4e61d17b2d7ed` |239-line fixture separately read; `replace(resources=(...))` is a meaningful snapshot-schema adaptation, not formatting. Same negative limits. |
| `b6512dc0dcb19c6427d1a0e0e04e333253127886` |304-line fixture adds actual two-resource redirect but `b.py` is too short for the selected source range. Proves bad geometry/missing resource only. No equal-geometry identity oracle. |
| `78eae937fb4a7b2c9087a74ae18792cb05e5c3a6` |306-line relocated fixture; monkeypatch targets move to actual new module paths. Fully read rather than inherited from b651. Namespace/call-site dependency changes matter despite almost identical tests. Current repaired regressions close the geometry gap. |

These dispositions update [ri-followup-history.jsonl](code-audit/ri-followup-history.jsonl).
No historical code ran, old APIs were restored or preserved bytes were edited.
Historical materializer limitations do not reopen the delivered main repair.

## Current ownership, cohesion and real control flow

Accepted ADR-0002/3/4/5 remain the architectural owners. Concrete current flow:

1. `CodingTask` binds objective, baseline, explicit source/test/read paths, limits
   and checks. It does not supply a Localization interpretation or claim to
   decompose the objective exhaustively.
2. `ContextTools` discovers only admitted addresses, observes retained source,
   realizes an explicit corpus and builds the existing file/symbol/window source
   index. Repository observation owns bounded UTF-8 acquisition and identities;
   it explicitly makes no atomic whole-filesystem claim.
3. Python owners derive declarations, explicit-root module interpretations,
   imports, qualified References/Calls, membership and direct bases. Facts are
   native support, not task relevance, runtime execution or permission.
4. Canonical lexical analysis/statistics/index/scoring feed source search.
   Source mixed mode consolidates native ranks using existing RRF while retaining
   original evidence. `retrieval.composition` instead correlates lexical and
   direct structural evidence as a neutral inventory; these are different owners
   and contracts, not duplicate rankers.
5. Model-selected search/lookup returns bounded metadata. `_read` uses the
   existing `SourceSearchDisclosureOption` → plan → materialization pipeline,
   then bounded exact character text and observation records. The separate
   exact-name function path authenticates selected knowledge/dependency before
   returning text. No evidence was found that these are interchangeable APIs.
6. The native loop sends correlated Tool results to the model; exact observed
   text is a prerequisite for admitted edits. Independent checks and host
   freshness remain separate from source evidence, review and publication.

The original [agent receipts](code-audit/agent-use.json) and
[follow-up receipts](code-audit/ri-followup-agent-use.json) establish genuine
search/read/edit use in bounded tasks. This audit reuses that qualified evidence,
not newly generated inference. Neither source imports nor121 passing tests prove
model strategy or controlled effectiveness. The new binding defect demonstrates
that authentic source dependencies can still support an incorrect derived fact.

| Responsibility | Cohesion/consumer finding and engineering disposition |
| --- | --- |
| Observation, snapshot, corpus, document | Clear lower-layer acquisition/state/membership/representation separation. Corpus/document identities intentionally omit unrelated resource dependencies; requiring every identity to include full snapshot would change semantics. Synthetic caller objects are not independently authenticated receipts. No new identity hierarchy warranted. |
| Python module/source/binding facts | Module declaration lookup is now shared by References and direct bases; historical duplicate target derivation was removed. Remaining module-binding scans have divergent capture coverage: the new bug is concrete pressure for a small compatible binding-name helper, not a generic Python evaluator/base class. Keep function-local traversal and before-child base evaluation distinct. |
| Qualified import support | Low-level relations consume producer-owned resolution results. Localization's `validate_import_dependency_frame`, `replay_import_dependency_source` and support validation authenticate exact frame and replay canonical results before admission. Do not treat manually altered low-level dataclasses as a demonstrated live worker exploit. Preserve replay when optimizing. |
| Lexical versus source views | Whole-document arithmetic is language-neutral; Python-specific symbol derivation is explicitly in the source-representation composition. Source units and whole-resource documents have distinct populations/identities. Do not merge their hashes or assign shared score meaning. |
| Graph/map versus semantic evidence | Maintained typed graph/map and optional native navigation reuse existing declarations/References. Tool availability and deterministic host preparation are established; autonomous map benefit remains unproven. Native relationships do not yet expose direct-base assessments; existing proposalcea1b3e7 remains sufficient. Negative historical automatic expansion/ranking does not discredit native facts. |
| Localization | Grounding resolves locators; association/generation retain hypotheses; explicit criterion-specific member decisions and complete ALL-member support permit promotion; readiness assesses only supplied obligations. No native coding caller composes that chain today. Existing15bae0a6 and06c3809b exact-hint integration scopes remain the homes; no second Context compiler/planner. |
| Planning and request assembly | Explicit ordered purpose/snapshot/lineage choices, concrete disclosure/materialization and request assembly have distinct duties. Planning is representation admission, not automatic need authorship or semantic satisfaction. No new compiler needed to connect caller-reviewed needs. |
| Repeated computation | `_reference_analysis` rebuilds explicit-root interpretations per source, and map preparation invokes it per admitted address. Lookup/source selection derive both function/class analyses; Reference/base target lookups repeat work. Real consumers justify existing measured-reuse proposalaedea41e. No new latency data, cache, speedup or removed authentication is justified here. |
| Packaging and extension | Python-specific facts remain under `context/python`; repository/text/Planning contracts need not become Python APIs. Future language adapters should provide concrete native representations to existing interfaces rather than reusing Python support as universal truth. Model/provider selection is outside RI; ContextTools is application composition. Source-level imports inspected here retain application→framework direction; this is not a complete cycle proof for the entire repository. |

The deferred import in `ContextTools._navigation` resolves an application-level
composition dependency (`navigation` consumes ContextTools). It is bounded
same-owner coupling, not evidence for a framework service locator. Its actual
surface and the large coding loop deserve later operational review; file size
alone does not authorize a split. Length-framed identity functions recur, but
different domain/version/order inputs are deliberate. Replacing them with one
generic digest service is not demonstrated necessary work.

## Obligation completeness versus evidence readiness

The existing [decision preparation](task-obligation-coverage-decision.md) remains
sufficient and **RECOMMENDED, AWAITING MAINTAINER DECISION**. No accepted ADR or
implementation follows this audit. ADR-0005's supported bounded APIs do not
approve the proposed application composition automatically.

Trusted reviewed clauses/obligations plus bounded reviewed revisions (A+C)
would make missing associations visible relative to that expected roster. It
cannot establish that the roster exhaustively captures the original objective.
Agent-proposed obligations with independently authorized, delegable semantic
review remain a later milestone; model self-approval is not authority.

Structural presence, rank, resolved locator and exact source text cannot accept
a semantic witness on their own. Unsupported facts remain unknown; accepted
ALL-member evidence is not interchangeable with mixing partial alternatives.
Task-only requirements need real review/execution evidence, not fabricated
repository witnesses. The prepared native acceptance flow still requires an
initially omitted reviewed clause, corrected need acquisition, model-visible
source, explicit witness review, real admitted edit/check PASS and host freshness.
A scripted test can prove composition but not autonomous decomposition or
comparative coding effectiveness. New false-positive binding guards are a
correctness prerequisite for relevant structural evidence, not a new completeness
oracle or a reason to revisit the architectural choice without new constraints.

## Efficient completion of historical assurance

The [grouping evidence](code-audit/ri-assurance-history-groups.json) authenticates
the existing203 path/blob obligations, without a new branch census. It finds
202 distinct blobs,201 full AST fingerprints and197 bodies after removal of
top-level imports. **73 records have no function/class definitions**, principally
exports/namespace surfaces; they are not automatically empty or equivalent.
Only seven records receive full credit here. Fingerprinting is triage, not
semantic equivalence: import order, reexports, monkeypatch target strings,
annotations, snapshots and durable schemas can matter.

Use this closure method:

1. Authenticate exact bytes and occurrence commits. Read a distinct immutable
   body once, retain every path's producer/caller chronology. Repeated exact bytes
   still need path/namespace dependency verification before credit transfer.
2. Review public/export surfaces as compatibility cohorts: compare actual exports,
   import direction and current consumers, not as dozens of algorithm assignments.
   Do not infer unused from absence on an archived branch tip.
3. Group implementation/test versions by owner and semantic seam, with full AST,
   imports, constants/error/schema/identity changes visible. Pure formatting can
   receive authenticated equivalence only after those dependencies agree.
   Import-stripped fingerprints are never a weaker fallback for completion.
4. Read independently each changed algorithm, validation/failure branch, scope,
   identity, field or durable contract and each new independent test oracle.
   Apply current-source comparisons, not automatic promotion of old behavior.
5. Record full-body, authenticated equivalence, superseded contract or unresolved
   evidence distinctly. Remaining obligations are closed by explained evidence,
   not deletion of ledger rows or optimistic tip comparisons.

Application here confirms meaningful changes even in tiny diffs: single-resource
to resource-set snapshots; relocated monkeypatch owners; multi-resource
materialization; central lookup replacing target derivation. Almost all203 AST
fingerprints differ, so a blanket equivalence shortcut is unsupported. Efficiency
comes from cohesive responsibility cohorts and compact export compatibility
review, not pretending the170 remaining bodies are duplicates.

The [next frozen cohort](code-audit/ri-assurance-next-cohort.json) selects ten
current configuration/role/lexical/source-candidacy fixtures and eight related
historical source versions (two NOT_REVIEWED, six tip-delta-only). It retains all
36 remaining original fixture paths and all older obligations. Do not start it
automatically. First address the bounded new binding correctness bug through
normal implementation/validation authority.

After that cohort, finish remaining substantive observation/path/coverage tests
and classify namespace surfaces explicitly; finish historical owner cohorts for
source observation/admission, retrieval graph/ranking, Localization, then exports
and legacy conversation-context relocation. RI exit requires every applicable
version to have a justified semantic/equivalence disposition, live correctness
repairs accounted for and consumer gaps assigned. It does not require implementing
every optional integration or rerunning frozen science.

## Backlog reconciliation

One new pending proposal, eight append-only ADVISORY updates; exact IDs/review
hashes in [ri-assurance-intake.json](code-audit/ri-assurance-intake.json). No B-number,
approval, grant, dispatch, parent/status change or automatic closure.

| Record | Operator-ready disposition |
| --- | --- |
|16b27e74 | New P1 production binding bug; independent real-source matrix, exact owners/consumers and final-tree acceptance. Pending implementation review. |
|a88167f9 | Existing fixture collision/empty-helper work sufficient; current genuine versus nominal fixture evidence added. Do not call it a production hash collision. |
|aedea41e | Concrete repeated current callers and historical/current target-derivation difference added; measurement before optimization. |
|15bae0a6 | Existing Localization integration scope sufficient; current-main native gap reauthenticated. A+C remains unapproved. |
|cea1b3e7 | Direct-base navigation remains missing; canonical lookup reuse is adopted. Positive relation exposure must follow corrected binding guards. |
|954a7136 | Exact-name correspondence repair delivered on main; reconcile implemented scope through operator procedure, do not schedule repair/adoption again. |
|416658bd /5aa7a431 | Physical-line repair delivered on main; reconcile overlap while preserving both histories. Historical SourceSpans remains separate. |
|2e70de9a | Supported versioned scientific binding verifier delivered on main; unchecked older consumers and Increment24 digest closure still open. No whole-parent closure or verifier reimplementation. |

Known diagnostic partial-ranking, Graph3 whole-report, historical span/recovery,
task normalization, U2 missing-witness and preflight-log issues keep their separate
existing proposal scopes. This cohort supplies no evidence that they became live
WorkCycle vulnerabilities or were repaired by main adoption. No new duplicate
stories or claims of historical scientific corruption.

## Next operational audit scope (not begun)

Review cohesive workflows rather than a namespace census. Existing entry points
are `scripts/backlog/__main__.py`, `work.py:WorkCycle`, `checkout.py:Checkout`,
`delegation.py`, `integration/{authority,local,lifecycle,validation,git,cli}.py`,
`apps/qwen/coding_loop.py:run_coding_task`, `tools/execution.py:ToolRunner`,
`execution/{runtime,interaction_attempt}.py`, `apps/qwen/edits.py`,
`commands.py`, `change_checks.py`, and their actual tests. Accepted taxonomy and
existing integration docs govern; this is no authorization for a new subsystem.

| Priority flow | Review obligations and independent failure evidence |
| --- | --- |
|P0 task→grant→Checkout→mutation | Separate maintainer development, host CodingTask scope and WorkCycle standing grants; canonical root/source baseline, sole owner, branch transition, unknown/untracked preservation. Test forged/stale task, competing owner and unauthorized path before entry. |
|P0 model proposal→ToolRunner→edit | Validate versus authorize versus execute once; exact observations/API contracts, atomic multi-edit admission, limits, aliases, changed source and failure after partial effect. ToolRunner itself only validates/executes; inspect real caller authority. |
|P0 interruption→recovery | Journal entry/return/durability, ambiguous effects, cancellation not rollback, owner recovery and no blind retry. Trace real process/receipt consumers; do not project historical reset-helper defects onto live code without evidence. |
|P1 candidate→checks→freshness | Fixed command/input closure, dependency configuration, status/exit/output handling, model-invoked check and host `is_current`, restored/source-changed reports and exact-tree validation reuse. Existing d58697fd bounded input-closure/reuse investigation remains priority; no asserted historical validation bypass. |
|P1 review→integration→publication | Independent review scope, actual installed candidate, destination-only Commands, actual destination gate, remote observation, normal PR/promotion permissions and closeout. Accepted worker evidence is not ordinary maintainer Git authority and neither is implied by a checksum. |
|P1 evidence/accounting | Correlate task/model/Tool/check/publication while preserving immutable Evidence, operational events, usage and durable records. Failed realization and uncertain external effects must remain visible. No EventBus/OTel implementation. |

Select exact source/test identities when that audit is authorized. It follows RI
assurance because its workflows consume authenticated source and must turn model
proposals into governed actions/recovery/publication. Other core/resources,
model/Agent, persistence, observability, applications/dashboard and developer
tooling domains still need comparable review. No successor-session dossier yet.

## Validation and publication

Focused selected tests:121 passed (`--no-cov`, twelve authenticated current paths).
Delivered-main materialization/integrity/source-search/physical-line regressions:
179 passed. An initial extra-regression invocation named a nonexistent
`test_source_integrity.py` and ran no tests; the actual maintained
`test_materialization_integrity.py` selection then passed. No failed test was
excluded or mislabeled passing, and these extra runs grant no fixture review credit.
Independent probe:12 source variants, with eight demonstrated false-positive
binding variants and four controls; no model, input-code execution, scientific
controller, pickle or adjudication. Final audit checks authenticate Git blobs,
review counts, JSON/JSONL, Intake chains, links, layout, whitespace and original
forensics. Exact results are recorded in the checkpoint manifest at publication.
No maintained production source, test, application, script or dependency input
changes; therefore no new protected production gate is claimed or required for
this documentation/Intake checkpoint. The previous2765-test/100% integrated gate
remains historical evidence, not a new assurance run.

Publish this ordinary audit branch and a normal review PR; main remains unchanged
until separately authorized integration. The containing commit binds this report
and the ledgers. Local completion files are ignored and never committed.
