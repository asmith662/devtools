# Usage evidence and operator identity repair — 2026-10-25

Three bounded P2 corrections are implemented and merged through normal
GitHub [PR #20](https://github.com/asmith662/devtools/pull/20). Starting main
`1717455a4f1f34590583fbf8085b957ece35ecbb`; final validated production `8f34dbdee381cf4493dd1f5e2a5508653dfe2891`;
accepted main `3e59c20f4c9276a7f28682a127ff95428e673564`, tree `c15b6029f8baab32bf803c635004361339977674`.
[Exact identities, original probes and validation evidence](../research/code-audit/usage-evidence-integrity-repair-20261025.json).

## Corrected owners and contracts

| Owner | Original failure | Maintained correction |
| --- | --- | --- |
| `observability/usage/collection.py` alias indexes | Local thread/invocation labels from another provider excluded legitimate usage. | Every alias map and ambiguity lookup includes backend/provider scope. Existing same-provider ambiguity still refuses. |
| Same measurement reconciliation | Last partial RESPONSE copy lost known counts; chosen TURN copy hid contradictions. | Join compatible known fields for the same measurement, retain unknowns and explicitly exclude conflicting observations. Disjoint response slices remain separate; aggregate totals do not fill unknown per-response usage or double charge. |
| Dashboard `details.py` and `Inspection.tsx` | Both missing identities compared equal and displayed MATCH. | MATCH requires a nonblank proposal ID equal to a present call ID; absent/noncomparable/mismatched identities remain NOT_ESTABLISHED. Legacy absent status renders unresolved. |

Usage commit `5a54d2d9c14ae4a197baa0cece06ecb25c6ddecb`; dashboard commit
`228c073f464e38adaa9a68c64839f347fb12085f`; complete frontend fixture commit `8f34dbdee381cf4493dd1f5e2a5508653dfe2891`.
No public storage schema, provider field-translation contract, dependency,
execution policy or normalized application Evidence ingestion was introduced.

Raw observations remain intact and persist using the same wire format.
Compatible partial facts are a derived consumption projection, marked
`RECONCILED_USAGE` with a digest of all contributor metadata. This is deterministic
provenance, not cryptographic authentication of a provider's claims. Independent
known counts remain known; contradictions (including supplied totals) exclude
the invocation rather than selecting a convenient value. Missing values are not
zero. Existing reporting may show a known subtotal alongside an explicit unknown
count; that subtotal is not complete consumption.

Explicit cumulative local snapshots retain their narrow historical ordering
contract: same-time partials merge, same-time conflicts refuse, known decreases
across unknown intermediate observations refuse, and missing timestamps do not
justify choosing different counts. A later unknown current total is not inferred
from an older known subtotal; the older observation remains raw history. Ordinary
completed TURN/RESPONSE copies have no latest-wins authority. Report outcome
precedence and cross-layer temporal accounting are not redesigned here.

## Independent reproduction and permanent controls

Original safe probes ran before production edits against actual starting main;
their two affected owner blobs equal the audit's declared baseline. Cross-provider
evidence wrongly excluded valid rows, partial copy order lost input 10, conflicting
TURN reasoning counts were hidden, and two absent IDs displayed MATCH. New
permanent baseline tests produced **12 intended failures and 4 passing controls**.
Harness/import/fixture errors are not counted as product failures.

Permanent public reconcile/report/storage tests independently specify literal
counts, source/provider boundaries, partial/unknown fields, conflicts, reported
totals, stable duplicates, compatible permutations, response slices and cumulative
snapshot controls. Dashboard tests exercise actual archived-record producers,
HTTP responses and rendered frontend for both absent, one absent, equal and
unequal identities. Archived bytes are unchanged. No live model usage is fabricated.

Final **committed-tree** protected gate: **2937 passed,
2 opt-in live skips, 100% configured production branch coverage**;
pytest 1106.79s, managed 1108.617s, exit0.
Supported Ruff/format, strict mypy, TypeScript/frontend build, frontend formatting
and 13 frontend tests pass on identical executable inputs. Python focused suites
pass 350 tests before and after merge. Coverage remains the configured `devtools`
production profile, not a new claim of exhaustive application/frontend branches.
Retained/generated broad-science tooling limitations are not claimed green.
The existing React forwardRef notice and Vite large-chunk warning remain nonfatal.

## Canonical disposition and remaining work

Existing proposals `bbba08b8-234e-4f31-bbef-972ac90189e2`,
`ca5a0aac-65b3-4d3c-b115-59a398a4087e` and
`a823db65-08fd-43d1-91dd-5602ebb47b11` receive one append-only delivered advisory
each. Intake remains administratively PENDING_REVIEW because it has no delivered
state; this is not authorization to schedule the same fixes again. No new
proposal, approval, B-number, grant or parent closure was created.

B-0011/B-0023/B-0034 remain broader usage/Evidence/correlation and consumer
responsibilities. Native Qwen/WorkCycle JSON is not automatically ingested as
normalized framework Evidence. The dashboard still consumes actual application
records directly. Broader validation-input closure under d58697fd remains open.
No architecture decision, A+C implementation, new EventBus/store or persistence
compatibility change is implied by these corrections.

All 13 forensic file hashes and historical refs are preserved. The frozen
[Core/Resources cohort](../research/code-audit/core-resources-next-cohort.json)
contains 12 source/test bodies; every pinned blob matches accepted main. Its state
remains FROZEN_NOT_STARTED. Core/Resources is the next substantive audit domain;
no further Evidence-specific cohort or audit was launched. RI original fixtures
93/93 and experimental paths 606/606 remain reviewed at their defined depth;
188 historical RI exact-version obligations remain separate and unclosed.
