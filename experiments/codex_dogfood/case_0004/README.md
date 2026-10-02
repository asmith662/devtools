# Case 0004: obligation-specific lexical acquisition

**STAGE B CAPTURED — NOT ADJUDICATED.** The treatment below was committed at
Stage A before Retrieval. Stage C has not started.

This prospective acquisition experiment precedes implementation of bounded
repository-role intelligence. The complete task, purpose, shared anchors,
caller-authored obligation frame, exact queries, corpus membership, content
identities and acquisition settings are in [pre_retrieval.json](pre_retrieval.json).
That file is the authoritative experimental treatment. It must be committed
before any Retrieval execution. [inputs.pkl.gz](inputs.pkl.gz) retains the native
`LocalizationLexicalAcquisitionRequest`, including snapshot content and index.
It contains no ranked result or assessment. Load this repository-owned pickle
only after checking its committed digest; it is not an interchange format.

## Scope and interpretation

Repository Intelligence (RI) owns snapshot-qualified facts. Retrieval owns
native acquisition evidence. Localization owns obligation-relative resolution;
this experiment does not implement that resolution. Context Planning and agent
execution are outside the treatment.

The task is genuine upcoming work authorized by the experiment request and
consistent with [ADR-0005](../../../docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
and the [roadmap](../../../docs/roadmap.md#repository-map-checkpoint-and-next-evidence-gate).
The caller interpretation has six shared textual anchors and eight mandatory
obligations. Each has one explicit query; there is one unchanged complete-task
control query. Their order is the array order in the manifest.

The obligations locate RI extension ownership, native resource/path semantics,
Python-project configuration semantics, test-configuration semantics, applicable
package/API conventions, test expectations, documentation authority and the
protected validation contract. None asserts that registration, a particular
export route or a particular test framework applies. Determining the bounded
supported configuration, including supported absence, is mandatory information;
it is not conditional on assuming that a configuration feature exists.

All obligations start open. Their named satisfaction criteria are frozen, but
witness alternatives are empty because native target identities are unknown.
This is permitted by the production kernel. Empty alternatives neither satisfy
an obligation nor provide a gold answer. The later independent adjudicator may
identify conjunctive witness sets and competing acceptable alternatives; those
evaluation judgments must not be inserted into the acquisition request.
Provenance references the exact task's UTF-8 SHA-256 and quoted task phrases,
with caller interpretation explanations rather than fabricated source spans.

Queries use task language and accepted architectural/development terminology.
Infrastructure inspection was not used to add candidate filenames to queries.
No query authoring uses Retrieval results, resource judgments or historical
rankings. The caller interpretation is itself an experimental treatment, not
automatic decomposition or proof that the task frame is exhaustive.

## Frozen corpus and machinery

The starting Git commit is `3cfda0a81ae95f578f42b8fd6b17cc8bcf751bc1`.
The logical RepositoryId is the same as Case 0003. The manifest records the
native RepositorySnapshotId and corpus identity and every eligible address with
its decoded-content identity. Only eligible tracked blobs were exported from
that commit. Excluded blobs were never opened. Observation and corpus/index
construction use production primitives; index construction is not query
execution. The archive retains exact native inputs for later execution without
reopening working-tree content.

Selection follows Case 0003: Python, Markdown, TOML and YAML resources under
`src/`, `docs/` and ordinary `tests/`; exclude the historical implementation
ledger, cache components and `tests/experiments/`, with the same explicitly
included capture module/package/test and root README, AGENTS and pyproject.
Additionally include the canonical `scripts/validate_development.py`: the task
requires protected development validation and that entry point is a governing
worker requirement known before Retrieval. This change is frozen now, rather
than repaired after observing a miss. Other scripts, experimental outcome
artifacts, local files, binaries and untracked files are outside the corpus.
Corpus completeness is relative to this selection, not every repository file.

The manifest freezes discovery bounds of 10,000 resources and 20,000 traversal
entries and observation's 1 MiB per-resource limit. It retains lexically ordered
native resource occurrences. Production corpus representation, lexical document
analysis, statistics and inverted-index construction are reused. The archive
and implementation digests bind these inputs to the original production code.

All nine lanes use production content-plus-filename BM25: `k1=1.2`, `b=0.75`,
filename weight `0.25`, distinct casefolded Unicode-word query terms, positive
native scores only. The bound is `max(1, eligible document count)` for every
lane, permitting the complete positive ranking. Ties retain corpus order,
which is lexical resource-address order. This is an acquisition bound, not a
top-K admission rule or an obligation cardinality assumption.

There is no role scoping, fusion, agreement bonus, score normalization,
automatic witness construction, candidate elimination or rank-to-satisfaction
inference. Resources appearing in several lanes retain separate native supports.
Purpose remains separate from exact query text. No graph or repository-map
channel participates.

Case 0003's `_eligible` selection and separate freeze/capture discipline and
the shared capture module's complete-corpus work-bound semantics inform this
record. Their capture functions are not called. Native repository observation,
corpus/index and Localization identity/task/query/request constructors are
reused directly. No new experiment framework or production schema is added.

## Stage B capture (complete)

The case-specific script [capture.py](capture.py) verified the Stage A commit,
committed README/protocol/archive, input digest, every retained request field,
all source digests, snapshot/corpus membership, lane text/order and settings
before acquisition. It uses the trusted native request without rebuilding it
from current repository contents. It refuses to run if either frozen output
already exists.

The invoked entry point was:

```text
uv run python experiments/codex_dogfood/case_0004/capture.py
```

Two initial launches stopped during preflight, before the acquisition call:
first due to Windows text line endings, then due to confusing the original task
snapshot commit with the later Stage A commit. The script was corrected to
compare canonical text content and keep those commit identities distinct. The
adapter was then invoked exactly once. No treatment field changed.

The script retained the complete native request/result pair in
[`capture.pkl.gz`](capture.pkl.gz) and its field-by-field deterministic JSON
serialization in [`retrieval.json`](retrieval.json). JSON preserves every lane,
including empty lanes, exact query observations, native rank/order, resource
and content identities, native scores and content/filename contributions.
It records the total acquisition runtime; it contains no usefulness labels,
satisfaction claims, winner labels, fusion or cross-lane ranks.

Frozen output identities:

| Artifact | SHA-256 |
| --- | --- |
| `capture.pkl.gz` | `e4cde5de6ed3fc3d8ea2a74eed40772972eebd4edb910c4091b7359276587f93` |
| `retrieval.json` | `37fa5b7a53efbe326b9cfc9d0da4e7761fed0d83607bc184ba09b4765f548848` |

Verified: nine lanes (one global, eight obligation), 498 eligible resources,
native-to-JSON correspondence for every match and evidence contribution,
protocol/archive/source identities, settings and result bound. A separate
read-only verification loaded the retained aggregate; it did not call
Retrieval. A second script launch confirmed overwrite refusal before acquisition
and left both hashes unchanged. There are no adjudication, judgment or joined
analysis artifacts. No semantic retrieval-quality interpretation was performed.
Confirmation outcomes remain sealed.

Commit this capture and record before any blind adjudication. Stage C receives
the frozen task/frame and eligible content without queries, lane membership,
ranks, scores, contributions, Retrieval provenance or retrieved flags.

## Later blind adjudication and analysis

Prepare a separate neutral adjudication input containing the frozen task,
anchors and obligation frame (including criteria/provenance), eligible addresses
and retained content identities. Supply retained content and accepted
architecture as needed. **Exclude exact acquisition queries as well as lane
membership, ranks, scores, contributions, provenance and retrieved flags.**
Do not supply exploration, opened-file or modified-file flags. The adjudicator
can inspect the entire eligible frame, including resources with no lexical hit.

Independently judge applicability and obligation-relative `REQUIRED`,
`HELPFUL_ONLY`, `UNNECESSARY` or unresolved/indeterminate outcomes. Identify
acceptable alternative all-member witness sets, and distinguish task-start
inferability from information requiring a named later observation. Absence of
evidence is not non-applicability. Freeze judgments and their identity coverage
before joining to retrieval. Reuse the production Evaluation identity-coverage
kernel for expected/observed frame completeness; this protocol owns outcome
meaning. Retain foreign, duplicate, missing and unresolved judgments explicitly.
Resource-level judgments do not automatically establish fine-grained witness
or future Context adequacy.

The joined analysis must report:

- Global native rank and acquisition-bound reach for every independently
  required resource; required-resource count, recall within the bound and
  last-required rank. Helpful/unnecessary counts remain separately available.
- For each obligation, every required resource and accepted alternative set,
  native rank in every query, best obligation-lane rank, conjunctive completion
  depth for each alternative and whether each alternative is fully reachable.
  Compare these with the same resources/sets in the global control.
- For an all-member set, completion depth is its maximum member rank. Any
  missing member makes that set incomplete, with no finite completion depth.
  The minimum complete-alternative depth measures acquisition reach of one
  acceptable solution; report reach of *all* alternatives separately. Do not
  require all competing alternatives for mandatory coverage.
- Complete applicable mandatory obligation coverage under frozen judgments:
  every such obligation must have a fully reachable accepted set; separately
  report supported non-applicability, inherent discovery and unresolved
  adjudication. Lexical reach is not production resolution or readiness.
  For this case there is one query per obligation, so best native rank has
  no cross-query ambiguity. There is no global cross-lane completion rank.
- Nine lane counts, summed candidate occurrences, unique union size, overlap,
  duplicates, zero-result lanes, native lexical contributions and available
  acquisition runtime. Duplication is provenance, not utility or agreement
  weighting. Report construction cost separately if measured.
- Global-only, obligation-only, both and neither for the independently required
  resource set. Also report resources missed by their own obligation's lane
  but found by another obligation lane. Out-of-frame information discovered
  later is a corpus limitation, not a silent addition to the frozen universe.

If a required set is empty, report that explicitly rather than a misleading
rank zero. Missing or unresolved adjudication prevents an unconditional
complete-coverage claim. Do not average native scores across lanes. Recall at
depths 5/10/20/50/100 may be reported descriptively with denominators; it is
not the primary obligation-completeness criterion. No exploration savings can
be claimed without a comparable control.

## Freeze integrity and next step

The JSON manifest uses an experiment-owned versioned format mapped to existing
production immutable types; it is not a new general protocol API. Verify all
identity references, unique IDs, exact text, provenance, settings, ordered frame
and archive digest using those constructors before commit. The initial archive
contains only request inputs. Neither `retrieval.json`, `capture.pkl.gz`,
adjudication judgments nor joined analysis may exist at this stage.

Stage A validation passed: JSON/native-request correspondence, six anchor and
eight obligation/query identity checks, exact task/query text and provenance,
all 498 address/content identities, settings/bound correspondence, archive and
implementation digests, native snapshot/corpus reconstruction from retained
content, and touched-document link checks. The case directory contains only
this README, `pre_retrieval.json` and `inputs.pkl.gz`. No executable source was
changed, so the protected pytest profile and static Python gates were not run.
Diff and staged-diff whitespace checks are required before checkpointing.

After freeze, do not change task/purpose, anchors, obligations, queries, corpus,
index, acquisition settings, bounds, measurements or adjudication rules using
outcomes. Substantive changes require a separately identified prospective
treatment and an explanation preserving this original record.

The exact next step is Stage B acquisition and output freezing, followed by
independent blind adjudication and joined analysis. The repository-role
implementation remains subsequent work, with freely permitted repository
exploration when authorized; this experiment does not constrain an agent to
retrieved candidates. Confirmation outcomes remain sealed throughout.
