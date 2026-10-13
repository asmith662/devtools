# Direct structural discrimination — prospective three-case Stage A

This experiment asks whether a direct positive cross-resource native Reference
from a lexically stronger candidate for the **same obligation** supplies useful
incremental evidence about a target already in canonical lexical acquisition.
It emits an **annotated lexical surface**. A's membership, scores and order are
unchanged. No structural ranking, promotion, Arm C, PageRank, RRF or graph-only
candidate is constructed. Effectiveness is **NOT EVALUATED** at Stage A.

## Architecture and decision boundary

Repository Intelligence owns deterministic snapshot-qualified Reference truth.
Retrieval owns native acquisition/evidence and identified ranking semantics.
Localization owns obligations, candidate hypotheses, accepted witnesses,
unresolved needs and readiness. Context Planning owns representation/disclosure.
The experiment correlates existing native BM25 and
`PythonDirectStructuralResourceEvidence` observations. It introduces only a
small experiment-owned annotation and invocation-local Reference preparation;
no universal CandidateEvidence type or production dependency is promoted.

`task != obligation != InformationNeed != query != retrieval action` remains
explicit: case records separate the original task, mandatory predicate,
desired-information uncertainty, exact query and later acquisition operation.
The mechanism is **obligation-query-relative**, not an automatic task-conditioned
semantic model. A stronger source rank is a hypothesis condition, not semantic
authority. This experiment chooses neither Retrieval ranking nor Localization
resolution as the eventual consumer. Its output could later inform either;
evidence usefulness must first be demonstrated independently of a fitted ranker.
The existing Localization witness association requires caller-authored hypotheses
and grounded subjects; manufacturing those from these annotations would prejudge
the question. They are therefore not created here.

Graph-3's completed development result remains GRAPH_HARMFUL. Its 37 novel
occurrences were unnecessary under their owning obligations, while some existing
candidates gained useful direct cross-resource support. Its broad equal-weight
fusion caused widespread unbounded regression. Those qualitative observations
motivate this narrower signal test; no Case 0016 gold, ranks, parameters or paths
are opened or tuned here. One case does not prove that discovery, diffusion or
other relation families are universally useless.

## Cohort and parent frames

The immutable historical population was frozen before this mechanism. The first
three cases, without sampling/replacement, map to Cases **0017, 0018, 0019**.
Their public tasks and exact parent identities are copied into `cohort.json`
and the individual Case Stage A records. Population-local identities remain
provenance; no restricted population builder/holdout verifier is invoked.

Only the two public population/selection files are authenticated against their
pinned committed SHA-256 values. Parent Git archives select broad source/test/
documentation/configuration text under the established Case 0015 frame policy.
Each extracted regular file must match its parent Git blob object identity.
Native observation, discovery, corpus realization and whole-document identity
then retain exact UTF-8 text and all included-resource identities. There is no
checkout, main-worktree switch, historical code execution or child read.

The evaluator is fixed at the starting current checkpoint, separately from each
historical content frame. Some parents predate current BM25/Reference APIs.
The compatibility adapter applies the current accepted canonical algorithms to
historical data; it does not claim those algorithms existed in each parent or
patch parent code. Modern evaluator APIs/source are harness bindings, not task
authoring or blind-gold evidence. They include the canonical statistics/index
machinery needed by BM25; they must not be used to infer a historical task's
desired implementation. Obligations were authored from each own parent, with
Case 0017 fixed before later parent source semantics were inspected. Historical
parent frames can overlap; future adjudications are isolated per case and receive
no other case's frame, judgments or modern evaluator source.

The vLLM task does not specify the option spelling, value domain, image-version
applicability or default. Its minimum obligations cover explicit configuration,
faithful launch propagation and bounded validation/documentation, without
inventing a flag or field name. This interpretive limitation remains visible to
Stage C; no complete provider-runtime or task-witness claim is assumed. Any
residual semantic gap/unresolved label is preserved, not forced to unnecessary.

## Exact shared mechanism

One canonical content-plus-filename BM25 query per obligation, k1=1.2, b=.75,
filename weight=.25, complete positive matches up to frame resource count.
Native descending score and document-order ties are unchanged. No exact locator
exists in the original task messages, so exact routing is inapplicable; there
are no guessed resource anchors, role gates or extra full-task query lane.

Later RI computes each retained Python source once under the fixed current
bounded declaration-Reference semantics. Explicit module roots are `src` for
source files and `.` for other included Python files, without root precedence.
Functions, classes and supported method targets are eligible. Import/facade
qualification may support resolving a native Reference; it is not an independent
import edge. Call tags are retained provenance, not another edge family.
Unresolved/ambiguous outcomes remain diagnostic and never positive evidence.
Missing support is not a claim of negative relevance or exhaustive Python truth.

Qualifying source and target are both in **A(O)**, source rank is strictly lower
(stronger), they are different resources, and a positive exact native Reference
points source -> target. There is no lexical top-K source cutoff, graph-only
admission, self credit, reverse edge, multi-hop path, diffusion or PageRank.
Duplicate exact occurrence input counts once; conflicting fact identities or
occurrence bindings reject. Distinct sources/occurrences remain inspectable.

`prepare_references` validates native endpoints/dependencies and canonical fact
identity order once per snapshot. `annotate` consumes that invocation-local
prepared state and the unchanged native A, carrying exact native supports.
Targets iterate in A order, sources by A rank/address, occurrences by canonical
native identity. Preparation is not persistent trust: the new capture must bind
its source facts and implementation, and new invocations authenticate again.
The schema records obligation/query/frame, target/source document/content/rank,
native occurrence/declaration/derivation/qualification provenance, distinct source
and occurrence counts, and best source rank. No count is a relevance score.

Ablation removes References and reconstructs empty annotations/pairs while
preserving A exactly. It demonstrates channel dependence, not causal relevance.

## Local diagnostic and frozen interpretation

Each supported target T at rank r>1 is paired independently with the original
rank r-1 predecessor P. No promotion or simultaneous swap is performed. A rank-1
target cannot receive support from a strictly stronger source. Pairs are exact
case/obligation/query/resource/document/content/frame identities, not filenames.

After independent blind gold, ordinal labels are REQUIRED > HELPFUL_ONLY >
UNNECESSARY. T>P is beneficial, equal is neutral, T<P is harmful. Strong beneficial
means REQUIRED over UNNECESSARY; strong harmful means UNNECESSARY over REQUIRED.
The four case categories use only presence/absence of those strong classes:
signal, contradicted, mixed, or no material signal. Contract/proof/provenance/join
failure prevents a valid category. `decision.py` contains the exact rule and
synthetic tests cover all nine label pairs and category boundaries.

Report every pair, supported/unsupported target and useful-supported/baseline
useful rate with exact denominators. Report source counts, occurrences, best-source
rank/distance, unnecessary resources strictly between best source and target,
and indispensable target support where gold establishes it. These are descriptive;
no post-gold threshold or stronger-source gold filter may be introduced.

All three captures and all three blind judgments precede the cohort interpretation.
Sum beneficial/neutral/harmful and strong classes, report case categories and
supported target labels. The primary useful support proportion counts distinct
(case,snapshot,obligation,target) supports, with separate occurrence/source-weighted
diagnostics; do not confuse them. No significance threshold or production verdict
is claimed from three development cases. The next architecture decision may find
consistent signal, mixed/purpose-insufficient signal, or noisy/redundant/absent
signal; this freeze encodes none of those conclusions.

No rank/reach/witness-depth/burden change is possible by contract. A change is an
experimental defect, not evidence of a winning or harmful ranker. Graph-3 gates
are untouched and not repurposed as meaningless discrimination gates.

## Adversarial design review

- A Reference does not imply relevance. Strong local harmful pairs explicitly
  falsify the hoped-for direction; full useful and unnecessary counts remain.
- A lexically stronger source may be wrong or incidental. No accepted witness,
  semantic authority or source gold condition is inferred from its rank.
- Tests can reference implementation incidentally. All qualifying native sources
  are treated identically; no test-path boost, special source class or heuristic.
- Direct support may correlate with lexical proximity. The original predecessor
  and baseline useful rates expose this; the diagnostic is not causal proof or
  an independently controlled population comparison.
- A predecessor pair is only a one-position proxy. It proves no large promotion,
  optimal ordering, combined-swap safety, obligation resolution or agent success.
- Candidate restriction prevents discovery intentionally. Missing graph-only
  required evidence cannot be rescued or used to sell this as acquisition value.
- A positive signal does not settle Retrieval ownership. Localization could be
  the proper consumer of explicit candidate evidence under a stronger purpose.
- A negative signal does not reject all structure; this tests this source condition,
  direct Reference family, candidate universe and three historical tasks only.
- One hop may be insufficient. Diffusion is deferred until a semantic rationale
  earns it, rather than being installed as the default representation.
- Historical tasks differ from present tasks and parent APIs differ from the
  evaluator. Exact historical content/current harness bindings and per-case
  interpretation limits make this explicit; no cross-repository generalization.

These objections limit interpretation rather than require a scalar score,
promotion policy or gold-driven eligibility adjustment. The design survives as
a diagnostic of the signal, not a proposed production relevance rule.

## Later stages, proof ownership and performance

Stage B is **not authorized or executed here**. It later authenticates Stage A,
claims each execution, journals a fixed exactly-once scientific schedule, derives
all eligible native References once, captures each A and its annotation once,
and seals native/canonical evidence without gold. No automatic retry or partial
prefix may masquerade as a completed capture. The same mechanism is used for all
three cases; no earlier case outcome can redesign a later member.

Capture finalization performs the deep proof once and publishes the existing
CompletionBindings/proof model anchored by an authoritative capture commit.
Normal downstream checks authenticate that sealed proof and canonical inputs;
missing proof fails explicitly without silently entering raw forensic replay.
No completed Case 0016 deep replay is required here.

Stage C uses one clean designated Astra High primary per case, with exact task,
obligations and complete included parent resources. No query/needs, ranks, support
annotations, pair identities, modern evaluator code, other case inputs/results,
child implementation or changed paths are disclosed. Retain all cells, positive
spans, semantic units/alternatives, minimal witnesses and indispensability, as
well as interpretive gaps/limitations. Reviewed publication is byte-authenticated
and semantic_transformation=NONE, without automatic second review/reconciliation.

Stage D authenticates sealed capture and gold once, joins exact owning identities,
classifies supported targets/pairs and applies the four-case-category rule.
The cohort summary follows all three cases. Child implementation remains off-limits
until capture, blind gold and primary scientific evaluation are frozen. It is not
gold; an optional post-result external-validity comparison requires separate
authorization and cannot retroactively change any judgment or category.

Warm computation timing uses perf_counter_ns around query analysis/BM25 and
direct lookup/projection/annotation, including normal API guards. Snapshot/RI/
index/fact preparation is offline. Journal serialization, deep proof, hashing,
validation, diagnostic materialization/reporting and Git are outside the timed
closures. Complete warm online-equivalent latency is their same-query sum.
There is one scientific sample per obligation (three per case/nine cohort), with
raw times, n, median and nearest-rank p95 disclosed as a single-run workload
description, not a stable repeated-query distribution. No scientific acquisition
is repeated merely to obtain a percentile. Target <=250 ms median; concern >1 s
p95. Performance is descriptive and changes no effectiveness category.

Non-goals include all new ranking/discovery treatments, self/multi-hop/other
relation-family usefulness, Context budgets, agent success, changed-file recall,
child similarity, SEARCH_POLICY_FAILURE, production changes, incremental RI and
filename-index optimization. Accepted scientific/performance/verifier states and
the frozen historical population remain unchanged.

## Build and verification

```text
python -m experiments.structural_discrimination.freeze build
python -m experiments.structural_discrimination.freeze verify
python -m experiments.structural_discrimination.freeze verify --checkpoint STAGE_A_COMMIT
```

These entry points perform public-source authentication, parent observation and
deterministic Stage A construction only. They never invoke retrieval or RI.
BUILD refuses any existing expected output. VERIFY reconstructs exactly from
public inputs/parent Git objects and compares bytes. This new experiment package
is non-installable and depends one way on existing experiment helpers/devtools;
no production abstraction, persistence schema or dependency direction changes.
Without `--checkpoint`, VERIFY proves prepublication reconstruction/byte equality
only. Later capture must supply the accepted external Stage A commit; that mode
also authenticates every artifact and implementation against its committed bytes.
The integrity manifest is not its own authority. This Stage A input seal is
distinct from the later capture-time completion proof.

Next: maintainer reviews the frozen protocol. If approved, execute Stage B for
ALL THREE cases under it before any semantic gold is used to revise the mechanism.
