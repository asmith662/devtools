# R1.5 — Retrieval Diagnostics and Failure Attribution

This non-installable experimental package owns reusable retrieval/evaluation
instrumentation. It consumes frozen retrieval evidence and optional independent
obligation judgments; it neither ranks nor selects Context. Production Retrieval,
Repository Intelligence and Localization do not depend on it. Generic framework
evaluation currently owns identity coverage, which these checks reuse; it does
not own task-relative failure truth.

## Evidence and boundaries

Inspection established these existing owners before implementation:

| Evidence | Existing owner / adapter behavior |
|---|---|
| Query observations, content TF/DF/IDF, lengths, settings, scores | `devtools.context.retrieval.lexical` native result/index; project retained facts |
| Independent filename-stem BM25 | Native filename index and match contributions; project separately |
| Whole identifiers and unique subtokens | `experiments.identifier_sparse` and retained identifier splitter; preserve exact spans and lineage |
| Frozen Case 0009 JSON | Reconstruct missing field statistics using existing canonical/R1 index owners; validate every captured query contribution and score, never rerun queries |
| Exact/symbolic grounding | Native qualified grounding result; current adapter supports exact snapshot-resource referents, other symbolic referents remain native |
| Structural supports | Native direct structural candidate fact identities, seed and direction; positive observations only |
| Roles | Native snapshot-qualified soft role identity and derivation; no relevance inference |
| Independent gold and accepted alternatives | Caller-owned evaluation input; completion stays with accepted-alternative evaluation |

The historical Case 0009 Stage D helper and outputs retain their original replay
contract. R1.5 consumes that frozen checkpoint without changing its conclusions.
New experiments should use this package rather than create another diagnostic
derivation. Its interfaces support canonical and R1 independent-field BM25 now;
other scoring families require a separately validated adapter/decomposition.

## Use

`adapters.canonical(...)` and `adapters.identifier(...)` project native results.
`adapters.from_rows(...)` projects frozen Case 0009-style JSON with explicit field
statistics. Construct `Mechanics(capture, judgments=(), policy=...)` once, then:

```python
engine.query_profile()
engine.explain(resource, supports=())
engine.overtaker(required_target, overtaking_resource)
compare(engine_a, engine_b, resource)
encode(diagnostic_record)
```

An immutable subject retains native RepositoryId, SnapshotId, CorpusId, exact
resource occurrence/address/content identity, lane/exact query text, and explicit treatment/index
configuration. The caller's lane key is qualified by frame/configuration; an
attached native obligation identity also retains its task. Configuration identity
hashes analyzer, index identity, treatment name, `k1`, `b` and filename weight.
It is an experimental configuration digest, not a new framework identity type.
Gold is optional. Unknown/unjudged never means UNNECESSARY.

Inputs are immutable projections. Initialization validates native occurrence and
judgment joins, source texts, source lengths, query-term postings/frequencies,
rank uniqueness/order, stable corpus tie order, and positive-universe coverage
when declared complete. A bounded result is explicitly incomplete: a positive
resource omitted by the result bound is `RESULT_BOUND_OMISSION`, not a reach miss.
Caller-supplied exclusions retain eligibility reasons rather than guessing from
absence. Unsupported scoring fields are rejected.

Each term exposes source-query form/spans, whole/subtoken lineage, full whole-form
occurrence counts and three bounded span examples; per-field DF/N/IDF, matched
resources, TF, length/average, length ratio, normalized length factor, saturation
numerator/denominator, unweighted and weighted contribution. Both current fields
use independent BM25 statistics. Existing canonical scoring functions reconstruct
`sum(content) + filename_weight * sum(filename)` and must match actual captured
scores/components with absolute tolerance `1e-10` and relative tolerance `1e-9`.
Tests intentionally corrupt captures to ensure invented explanations are rejected.
A miss has no captured score, so reconstruction status is null rather than success.

Query profiles include positive-weight matching unions, positive captured resources
using each term, and optional obligation-relative REQUIRED/HELPFUL/UNNECESSARY/
UNRESOLVED counts and descriptive yields. The configurable defaults for common
terms are DF/N >= 0.25 and IDF <= 1.5; these are inspection labels, not query
weights or claims that common terms are bad. Zero-weight fields are visible but
cannot create an effective positive footprint.

Ranking records retain rank, score, predecessor/top gaps, all overtaker identities,
judged and unjudged counts, and a bounded top-five overtaker explanation. Pair
records compare weighted term/field contributions, TF, DF/IDF, lengths, normalization,
configuration, query terms, positive captured candidates and ahead sets. Full
term profiles preserve document-term additions/removals. Exact observable deltas
do not independently isolate interacting causes; causal allocations require
separately frozen ablations. Completion/alternative semantics remain caller-owned.

## Conservative failure assertions

| Governing class | Supported assertion and limit |
|---|---|
| REPRESENTATION_FAILURE | `VERIFIED_REPRESENTATION_FAILURE` only with exact source/query subtoken lineage, absent matching analyzer exposure, and exposure by the compared representation; can be lexical truth without gold. Partial cue recovery is separate from positive reach rescue and required-unit importance. Reverse loss witnesses are retained. |
| RANKING_DISCRIMINATION_FAILURE | `VERIFIED_RANKING_DISCRIMINATION_FAILURE` requires independent REQUIRED gold, a positive captured rank and at least the explicitly configured unnecessary-overtaker threshold (default 20). Establishes burden for that subject/policy, not a universal ranking defect. |
| VOCABULARY_SEMANTIC_MISMATCH | `POSSIBLE_VOCABULARY_SEMANTIC_MISMATCH` only for independent REQUIRED gold, no overlap in both available compared representations and no hidden match. Lexical evidence cannot establish semantic equivalence. |
| RELATIONAL_RELEVANCE | `RELATIONAL_SUPPORT_PRESENT` retains qualified positive structural facts, not why gold requires the resource. Unsupplied support is NOT_ASSESSED, not absent. |
| CONTEXT_DISCLOSURE_FAILURE | OUTSIDE_DIAGNOSTIC_SCOPE / NOT_ASSESSED without independent evaluation evidence |
| INFORMATION_NEED_OBLIGATION_FAILURE | OUTSIDE_DIAGNOSTIC_SCOPE / NOT_ASSESSED without independent evaluation evidence |

Records separate primary classification, contributing observations, certainty and
limitations. Deterministically established mechanics, strongly evidenced support
presence, possible/unresolved interpretation and outside-scope states stay distinct.
Observable common terms, unnecessary overtakers and length normalization can
coexist. No cause is invented to force every reached resource into a failure class.

## Case 0009 dogfood and deterministic capture

[Complete report](case_0009.md) covers all 37 REQUIRED cells under each arm.
`case_0009.json.gz` is deterministic gzip (`mtime=0`) of sorted-key, finite,
ASCII JSON with a final newline. It retains query profiles, explanations, pair
records, exact input digests and configuration identities. Compression keeps the
repeated bounded explanations reasonably sized. Gzip publication uses the existing
case's explicit binary boundary because the canonical filesystem writer currently
has no binary codec; text uses the canonical writer. Existing different binary
captures are refused and require an explicit new version.

```text
python -m experiments.retrieval_diagnostics.dogfood build
python -m experiments.retrieval_diagnostics.dogfood verify
```

Replay verifies frozen commits, Stage B capture hashes, clean gold and repaired
packet through existing Case 0009 verification. It recomputes only missing field
statistics and validates captured scores, ranks and paired overtaker sets against
the original Stage D record. It does not rerank, adjudicate, access quarantined
gold/confirmation or change the R1 decision.

Run focused tests with plugin autoload disabled and `--noconftest`, overriding
repository addopts; no repository-wide collection is needed. Scoped Ruff,
formatter and strict mypy checks cover only this package and its mirrored tests.

## Sequencing and future fields

**Future retrieval experiments must diagnose observed failures by class rather
than reporting only aggregate metric movement. BM25F evaluation must use this
diagnostic facility to explain field/parameter effects.**

R1 is done, retain separate view. R1.5 provides this foundation. R1.6 canonical
BM25 parameter sensitivity is next; R1.7 query-term discrimination/weighting
investigation follows R1.6, or combines only with clean attribution. R2 true
BM25F remains mandatory, followed by R3 query representation, R4 verified semantic
mismatch retrieval, R5 reranking/learning-to-rank, and R6 fusion. The documented
Localization reasoning continuation remains unchanged.

Configuration explicitly permits future comparisons of `k1`, `b` and filename
weight, without choosing or tuning values here. Field-tagged score contributions
and scorer-qualified adapters allow later field TF/length/average/weight/normalization
and aggregated-TF evidence to extend the representation. No BM25F aggregation,
field-specific b, IDF or scorer is implemented, and current Mechanics rejects
unsupported scoring semantics rather than pretending to reconstruct them.
