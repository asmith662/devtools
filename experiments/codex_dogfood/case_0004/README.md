# Case 0004: obligation-specific lexical acquisition

**FROZEN BEFORE RETRIEVAL. Stage A only.**

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

## Stage B: later acquisition procedure

**Do not execute this stage as part of the protocol-freeze task.**

1. Identify the Stage A commit in Git history. Require that it contains exactly
   the protocol, native archive and this record, with no Case 0004 outputs.
   Compare the local protocol/archive against those committed blobs. Require
   a clean checkout and validate the archive SHA-256 against the manifest.
2. Use the same locked environment and original production implementation.
   Check every `implementation_sha256` entry against the canonical Git blob
   at `starting_head` and current source text normalized to LF. Fail on any
   difference. Check the loaded request against every manifest field: exact
   task/purpose/queries, identities, anchors, obligations, settings, snapshot,
   corpus membership/content and bound. Do not reconstruct queries from
   predicates or use current repository content as the corpus.
3. In a reviewed case-specific capture script, load the trusted frozen request
   and execute exactly this acquisition call once:

   ```python
   import gzip
   import pickle
   from devtools.context.localization.lexical import acquire_localization_lexical_evidence

   request = pickle.loads(gzip.decompress(archive_bytes))
   acquisition = acquire_localization_lexical_evidence(request)
   ```

   The script must perform the preceding checks before this call. Invoke the
   reviewed script with `uv run python <capture-script-path>`. There is no
   Stage B executable in this checkpoint; this procedure specifies the exact
   production operation and inputs rather than advertising a nonexistent
   command. Adding capture/serialization code later must not change treatment.
4. Preserve the complete native acquisition as `capture.pkl.gz`; serialize
   `retrieval.json` with the protocol/archive hashes, snapshot/corpus IDs,
   ordered lane/query/obligation identities, exact query text, settings, native
   one-based ranks, resource/content identities, scores and lexical
   contributions. Retain zero-result lanes. Refuse to overwrite existing
   outputs. Do not join judgments, fuse lanes or produce a selected Context.
   Record total acquisition runtime with a monotonic clock. Per-lane runtime
   is optional if it cannot be captured without changing native behavior;
   report it unavailable rather than timing a different algorithm.
5. Freeze and commit those outputs before independent adjudication. A failure
   or necessary protocol correction must be recorded openly and cannot be
   retroactively described as an unchanged prospective treatment.

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
