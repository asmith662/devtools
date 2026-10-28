# Case 0002: repository discovery and release ordering

## Frozen question and task

Could the real configured local model discover an appropriate owner in a broader
repository, acquire interacting source contracts, edit it through the generalized
coding process, and repair naturally failing validation if necessary?

Execution baseline: `559ad49033e0d2389b68fa321cee870506e814aa`.
Authored task Git revision: `38ea4c43f8f0633f6ccf3bcaea1ff937614121d1`.
Frozen snapshot: `cc0e6aaa68428ff9bdfd1393e5e2b7596df63216bd2c1ceb0a01ee9735a5118c`.
Task digest: `9ad37cffac6209a44e905c25a76e9c18afb65b36f52dcf88a1187f023e3df013`.
The [original freeze](freeze.json) binds all task, host, oracle and profile inputs
before the one primary attempt. No implementation patch was provided or supplied
afterward by Codex.

Releasevault is an independently authored 18-file Python project: 11 runtime
modules, public tests, documentation, configuration and a test entry point. The
reported defect concerns stable/prerelease ordering, numeric prerelease ordering
and build-metadata ties. Selection, eligibility, version semantics, catalog
snapshots and presentation are distinct plausible investigation points. All 11
runtime modules were editable; no correct file or mandatory source witness list
was prescribed. Tests, docs and configuration were read-only. The initial Prompt
did not contain the eventual edited module's path or a source listing.

The task follows [SemVer 2 precedence](https://semver.org/spec/v2.0.0.html#spec-item-11)
while preserving existing project/platform eligibility, strict syntax, first
publication on precedence ties, immutable object/input ownership, interchange and
standard-library-only runtime. Seven focused tests and ten held-out tests were
frozen. Before inference, focused tests had four assertion failures and held-out
tests had three. An independent finite literal precedence-table reference passed
all seven focused and ten held-out tests before entry. It invokes no candidate
ordering/selector and was not placed in the model's repository or Context. This
positive control validates these finite oracles, not a new general SemVer parser.

## Operational route and limits

The already-running Qwen3.8-27B UD-IQ4_XS llama.cpp service was reused, with
matching profile fingerprint, pinned image, 32K context and native-host GGUF
SHA-256 verification. Endpoint `http://127.0.0.1:8080`, alias `qwen38-local`.
The profile and instruct sampling matched Case0001; thinking was disabled.
No download, cloud fallback, model substitution or service restart occurred.

Frozen ceilings: six model requests, three proposals (at most two repairs),
16 acquisition actions, 180 seconds/request, 1,080 seconds in the framework coding
process and a 1,200-second outer managed-process ceiling. Each request permits
4,096 output tokens and at most 28,160 measured input tokens inside 32K. The
32,768-byte Prompt, 8,192-byte disclosure, 4,096-byte anchor, 32,768-byte resulting
source and 8,192-byte aggregate edit limits were fixed before entry. No setting
or rule changed in response to model output. Shared request limits constrain the
number of repair turns actually reachable; the proposal limit does not reserve
additional inference calls.

The actual `run_coding_agent` and `RepositoryCodingHost` perform sequencing,
grounded admission, effects, current-source refresh, fixed validation, feedback,
candidate custody and terminal reconciliation. Experiment composition adds six
native operations: list_repository, search_source, read_source, replace_source,
validate_candidate and inspect_and_validate_change. It reuses existing native
Model/Tool composition, ToolRunner, canonical RI observations/discovery,
SourceSearchIndex file/symbol/window retrieval, ScopedSourceTool, Context
materialization, fixed checks/procedures and managed Commands/Filesystem.
There is no second coding loop, index, registry or provider.

Listing and search return metadata only. Search directly invokes the maintained
mixed retrieval API, retaining native ranks/views and snapshot/unit/content
identities. It does not disclose source text or grant edit authority. Source
disclosure requires a separate admitted read. Preflight exercised the actual
shared Tool boundary and retrieval implementation, including three rejected
argument controls, without a model. No repository map was rendered or consumed;
the capability exercised here was canonical lexical/source retrieval.

## Observed model lifecycle

| Request | Actual native calls | Reported input/output tokens | Provider elapsed |
| --- | --- | --- | --- |
| 1 | list_repository | 1,060 / 29 | 10.486883s |
| 2 | search_source plus read versions.py | 2,712 / 102 | 6.144049s |
| 3 | read selection.py, display.py, policy.py, catalog.py | 5,346 / 226 | 12.369769s |
| 4 | read two public test modules and architecture documentation | 6,704 / 171 | 8.810560s |
| 5 | one replace_source call | 8,315 / 442 | 21.057085s |

The model made the query `semver version comparison prerelease sort key ordering`.
The six ranked units came from versions.py, display.py, policy.py, selection.py,
cli.py and tests/test_catalog.py. It actually read eight resources: versions,
selection, display, policy, catalog, both public test modules and architecture
documentation. It did not read the CLI hit. Source acquisition and retrieval
candidates are separate in the retained journal.

The first version read was requested in the same batch as search. Its choice
therefore preceded receipt of search results and cannot be attributed to those
results. Later requests contained the actual search metadata and earlier source
feedback under original native IDs. Five of six hit resources were eventually
read; catalog and other selected reads were not all ranked hits. Input presence
does not reveal the model's internal reasoning.

The edit changed only releasevault/versions.py. It preserved the strict parser,
introduced a small identifier-key helper, ranked stable releases above previews,
compared numeric identifiers numerically and ignored build metadata. Selection
and display continued to call the same ordering owner; no second policy was
introduced. The exact old anchor was uniquely present in source actually read,
and host admission/currentness checks preceded application. All other 17 fixture
files, including the other ten editable runtime files, remained byte-identical.

The host ran InspectAndValidateTool deterministically after the edit. It inspected
authorized Git changes, executed the immutable seven-test focused check through
FixedCheckTool/ToolRunner and checked currentness. All seven passed. The model
requested neither validation operation. Passing feedback was appended under the
edit ID but never sent in a sixth inference. The process archived the candidate,
restored known original sources, and returned validated/completed/accepted.
Separate post-completion grading passed all ten held-out tests and a fresh focused
invocation. Read-only verification independently regraded both frozen oracles.

No failed-check feedback or model-driven repair occurred. No failure was injected
to force one. With four acquisition rounds and the first edit on request five,
only request six would have remained for repair under the shared ceiling.
Live repair competence remains unestablished by this case.

## Outcome, usage and limitations

Actual result: five real inference entries/responses, ten acquisition actions,
one proposal and one admitted applied batch. All known dispatch effects were
acknowledged; no invalid native call, admission refusal, timeout, unknown installed
source or retry was observed. The original task Git worktree was clean after
restoration. Candidate correctness and worker completion are separately recorded.

Provider-reported totals: 24,137 input tokens, 970 output tokens, 25,107 total.
Template/tokenizer counts agreed with reported input for each request. Cache,
cache-write and reasoning-token counts remain unknown. Provider elapsed sum:
58.868346s; framework worker: 60.225809s; complete controlled evaluation:
61.364488s. Preparation and later repository verification are separate timings.
Seventeen selected command observations/patterns retain normalized operation,
provenance and known results separately from bounded synthetic test diagnostics.
This is not complete global event capture or durable task recovery.

No production integration defect or required correction was demonstrated.
The discovery Tool is narrow experimental composition of existing framework
capabilities, not promoted production API. Scoped write admission is not an OS
sandbox for adversarial candidate Python; this candidate introduced no external
I/O. No personal logs, secrets or environment analytics were collected.

This one successful task demonstrates model-selected investigation and a correct
shared-owner edit within an explicitly authorized small corpus. It does not
establish large-repository discovery, causal benefit of each retrieval hit,
general autonomous effectiveness, cross-provider performance or repair ability.
Settings were stochastic without an explicit seed guarantee; exact artifacts and
oracle grading are reproducible, not an assertion that another generation would
emit identical bytes. Case0001 remains a separate unchanged observation; no
multi-case success rate is estimated. All its original files and collection
checkpoint records are preserved byte-for-byte.

## Single recommended improvement

Project a **bounded, complete authorized resource inventory into initial Context**
using existing snapshot/discovery metadata, rather than requiring a model request
solely to list it. Preserve the broad edit surface, model-selected investigation
and separate grounded source acquisition. The first request here did only listing;
four acquisition rounds consumed most of the six-call budget. Removing that
avoidable round trip could leave more budget for natural repair without increasing
limits or introducing abstractions. This is a recommendation for a separately
authorized increment, not a measured improvement or permission to begin it.
