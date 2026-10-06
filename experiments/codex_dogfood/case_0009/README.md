# Case 0009: prospective R1 assessment-bridge localization

R1 is now **prospectively evaluated** against clean independent Stage C gold.
[Stage D](analysis.md) selects **RETAIN AS SEPARATE RETRIEVAL VIEW**: both arms
reach all REQUIRED evidence; global completion improves 342 to 331, but maximum
own completion worsens 185 to 231 and prefix-union reduction is only 1.9455%.
The frozen separate-view criterion passes via a required readiness top-20 gain
and three improved obligation completions. No production adoption or BM25F is here.

## Task selection and ownership

[Protocol](protocol.py) contains exact task text, nine caller-authored mandatory
obligations and their queries. The full-task lane uses the complete task verbatim.
The task asks for a future caller-directed batch bridge from fully supported
candidate hypotheses to caller-selected LocalizationAssessments, preserving
accepted alternatives, complementary witnesses, provenance, applicability and
readiness boundaries. **The bridge is not implemented by this experiment.**

This is a researcher-authored realistic development task grounded in existing
public contracts, including tests, package boundaries, documentation and protected
validation obligations. It is not a tokenizer exercise and specifies no gold
resource paths. It shares the Localization family with earlier dogfood cases;
one such case is not an independent repository or broad task-population claim.
No future gold is selected or inspected. Both arms receive identical queries,
without optimizing obligation language separately for R1.

The [R1 method](../../identifier_sparse/README.md) defines frozen analyzer
semantics. [Retrieval foundation](../../../docs/architecture/retrieval.md) and
[Localization continuity](../../../docs/architecture/localization.md) own accepted
status. The preserved Localization resumption point after R1 and mandatory R2
is not changed by this task selection.

## Stage A: treatment freeze

Snapshot source is committed `main` at
`d71d741f3a91bf4c4a2b40619d1b8042853f6881`. The broad eligible frame is textual
Python/Markdown/TOML/YAML under `src/`, `tests/` and `docs/`, plus root README,
AGENTS, pyproject and the protected validation entry point. Exclude experimental
tests, research/reports, ledger, confirmation/reserve paths and all experiment
artifacts. Membership is path policy, never query hits or gold. Native observation
and corpus/document APIs build the shared whole-resource frame.

`pre_execution.json` retains repository/snapshot/corpus identities, addresses,
content identities, Git-byte digests, implementation hashes and runtime identity.
`inputs.pkl.gz` is a trusted case-local native snapshot/corpus/document/task/query
archive; verify integrity before loading it. `treatment.json` freezes settings,
metrics, attribution and decision rules. Stage A builds **no retrieval index**
and executes **no query**. The representation definition was pinned before its
outcome-free development diagnostic; both records are pinned again in Stage A.

Arm A invokes the unmodified production resource BM25 API for the full task and
nine obligation lanes, with `k1=1.2`, `b=0.75` and `content + 0.25 * filename-stem`.
Arm B changes only lexical analysis of content, filename stems and queries to
whole-plus-unique-subtokens, retaining scoring arithmetic, weights, whole resources,
positive-result policy, complete-frame bound and native corpus tie ordering.
No structural channel, fusion, reranking, field tuning or query rewriting occurs.

The frozen decision rule first requires complete valid gold and intact artifacts.
A promotion candidate requires no A-positive required cells lost, no worse
completion on any obligation or global lane, at least 20% own-prefix-union
reduction or a verified required positive-reach representation rescue, and
bounded costs (specified 3x limits). A complementary view requires a verified
required rescue or top-20 entry gain and at least one improved obligation
completion when promotion conditions fail. Otherwise park with valid complete
gold. A concrete analyzer contract defect requires a new prospective treatment,
not tuning after unwanted outcomes. Even a promotion candidate does not authorize
production adoption; one case is insufficient to change the default.

## Stage B and replay

Run from the repository root with existing dependencies:

```text
uv run --no-sync python -m experiments.codex_dogfood.case_0009.freeze freeze
uv run --no-sync python -m experiments.codex_dogfood.case_0009.freeze verify
# Commit implementation and Stage A before execution.
uv run --no-sync python -m experiments.codex_dogfood.case_0009.execute execute
uv run --no-sync python -m experiments.codex_dogfood.case_0009.execute verify
uv run --no-sync python -m experiments.codex_dogfood.case_0009.packet build
uv run --no-sync python -m experiments.codex_dogfood.case_0009.packet verify
```

The current user task authorizes one Stage B execution, after freeze. Exclusive
creation refuses stage overwrite. An execution-start marker prevents an automatic
retry after failure; recovery requires separately recorded authorization with
unchanged treatment. Verification replays hashes, query/frame identities, result
ordering and contribution sums **without rerunning treatment**.

Stage B retains complete positive universes with exact ranks, scores, field/term
evidence and analyzer terms; costs record build/query time, vocabulary/postings,
serialized index bytes and traced peak allocation. This is one instrumented
execution, not a latency benchmark. Peak includes result projection/serialization,
and native Arm A carries richer provenance objects than B; memory differences
cannot be attributed exclusively to terms. Filename indexing is per query in
both arms. No RSS claim is made.

## Independent blind Stage C and later join

The packet builder reads Stage A only, not arm results/costs. It exports **every
eligible resource**, exact task/criteria and neutral obligation metadata, with a
strict metadata-key whitelist and integrity digests. Ordinary source text is
not censored. The full frame prevents treatment-membership leakage. An independent
adjudicator must receive only `adjudication/`, without this treatment protocol,
parent implementation, arm ranks/scores/terms or prior outcome records.

Reuse obligation-relative REQUIRED, HELPFUL_ONLY, UNNECESSARY and genuinely
UNRESOLVED judgments, acceptable alternatives, required information units,
applicability and inferability-at-start. Unjudged is not unnecessary. Freeze gold
before joining it with treatment; evaluate reach, global/own completion, prefix
burden, paired gains/losses/net change, comparable top-K usefulness, unique useful
reach and exact representation attribution. This increment does not adjudicate.

**R2: true BM25F / field-aware sparse retrieval proceeds regardless of whether
R1 improves, ties or worsens canonical BM25.** No Stage C or effectiveness claim
is implied by committing Stage A/B artifacts.

## Stage D replay

Clean gold was committed at `092f9a760c1ec1ec29db5986a97b702ba5e1eff2` after
sterile isolated validation. [Analysis JSON](analysis.json) retains exact joins,
all positive universes, accepted alternatives, paired ranks, source/term
attribution and frozen cost-rule calculations. [Analysis report](analysis.md)
records the full provenance and gain/loss interpretation. Invalid quarantined
provisional gold is excluded. Stage D intentionally lifts the blind; confirmation
and reserve outcomes remain untouched.

```text
python -m experiments.codex_dogfood.case_0009.analyze build
python -m experiments.codex_dogfood.case_0009.analyze verify
```

Use the project interpreter. Build regenerates only derived Stage D outputs;
verify compares deterministic bytes. Neither reruns Stage B rankings or changes
sealed inputs. Run only the focused `test_analysis.py` with coverage options
disabled, plugin autoload disabled and `--noconftest`; frozen Stage C retains its
separate sterile validation environment. Mandatory R2 is next; semantic-resolution
effectiveness remains paused.
