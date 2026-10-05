# Case 0008 Stage C independent blind adjudication

Starting checkout: clean `main`,
`9eb910d2c9dc6fa0947e6640917c8072ed4ba010`, subject
`Freeze Case 0008 blind adjudication packet`.

The complete evidence universe was `blind_manifest.json` and
`blind_resources.json.gz` in this directory. Their SHA-256 values are respectively
`d1096ba811f050a74a0232caa34245bc6de7f263494155e97c3e0ebbf147b6e0` and
`cae456fa325a435de599da24a75ed3a3728d568b4bfc613b5b6851537a98c09d`.
No other preexisting Case 0008 artifact, current task-relevant checkout source,
experimental treatment/result, recovery history or confirmation was inspected.
No prior Case 0008 context was supplied or used. No subagents were used.

The exact manifest task, purpose, 11 anchors, 13 mandatory obligations,
satisfaction criteria, provenance and conditional package/API wording were read
before adjudication. Ordinary technical vocabulary and prospective purpose
wording are not treatment disclosure. Manifest/archive structure exposes only
the authorized frame and repository text, without treatment/result metadata.
The original task and obligation records remain verbatim in `judgments.json`.

## Inspection and decision procedure

All 523 archived addresses and addressed-content identities were enumerated.
Simple exact textual checks across archived contents identified relevant
contract mentions; no scores, rankings, Retrieval, routing, grounding,
generation, projection, repository-map or graph APIs were invoked. Selected
archived source, tests and documentation were read with inclusive line numbers.
These were static repository contracts, never experimental instances.

Selected reading included:

- Archived Localization assessment, obligation, task, identity and readiness.
- Archived candidate hypothesis/member/view, generation contract and generator
  composition, grounding contract/view/resolver and structural support replay.
- Archived public Localization, association, generation and grounding facades.
- Archived repository identity, snapshot, resource, observation and corpus
  contracts. Observation/corpus identity hashing was inspected only to verify
  the packet's native identities; it is not a requirement to reimplement their
  acquisition semantics in the proposed capability.
- Archived central architecture, taxonomy, ADR-0003, ADR-0005, documentation map,
  Localization package overview, roadmap, development validation and B-0002
  backlog context; neighboring Context Planning overview.
- Archived kernel, association, branching-generation and grounding tests;
  archived `pyproject.toml` and protected validation runner.

Necessity uses the counterfactual correctness rule with other complementary
REQUIRED information available. Exact contract spans, rather than entire
implementation files, are the information units. Every REQUIRED judgment has a
seven-part manual review: obligation, supplied information, necessity, smaller
unit, complementarity/competition, task-start inferability and blind basis.
The frozen task itself specifies the new bounded-request requirements; no
nonexistent implementation is treated as a witness.

Existing test fixtures and execution details corroborate behavioral contracts
but are not mandatory simply because new tests will be written. Behavioral
contract spans supply test oracles. Likewise, generation quotas are helpful
examples, not a required algorithm or future acquisition quota representation.
Resolution policy and autonomous acquisition execution are outside the task.

All obligations are APPLICABLE. The package/API condition is established by the
task's production reusable assessment integration together with the explicit
public kernel exports and accepted dependency direction, not by initializer
presence alone. No affirmative evidence supports non-applicability.

ALL units inside an alternative are complementary. ANY complete alternative
suffices. Only two genuine competitions were found: equivalent purpose passages
in taxonomy/ADR-0003, and equivalent execution-ownership statements in
ADR-0005/current architecture. No experimental operator structure was used.

Each occurrence has 13 explicit resource judgments. REQUIRED means it contains
one or more listed necessary spans for that obligation, not that every line in
the resource is necessary. Explicit HELPFUL_ONLY cells identify corroboration
and orientation. Remaining cells contribute no additional material information
to that bounded obligation. No universal relevance classification is implied.

## Integrity and freeze

`build_judgments.py` is the reviewable manual selection and rationale source.
`stage_c.py` verifies both blind byte digests, exact manifest frame, all content
identities using archived length-framed hashing, and recomputes SnapshotId and
CorpusId from the ordered addressed-content collection. It validates schema,
unit identities and exact excerpts, applicability, alternative membership,
inferability/discovery prerequisites, task gaps and full 6,799-cell coverage.
Structural forbidden keys and unknown schema fields fail closed; text excerpts
may legitimately contain ordinary repository vocabulary.

`freeze` exclusively creates `judgments.json` and `judgments.sha256`, refusing
either existing destination. `replay` checks the seal, validates all records,
then demands byte equality with canonical serialization and regenerated manual
gold. The helper has no unblinding or effectiveness-analysis command.
The Case-local `.gitattributes` preserves frozen JSON/seal bytes across Windows
checkouts rather than allowing newline conversion to invalidate replay.

Focused tests use a separate pytest configuration, `--no-cov` and
`--noconftest`, and import only new Stage C helpers. They cover digest tampering,
schema/frame/task corruption, spans, applicability, alternatives, inferability,
prerequisites, coverage, forbidden fields, task gaps, deterministic replay,
overwrite refusal and seal tampering. Production validation and live tests are
not executed for this experiment-only checkpoint.

Python helpers follow scoped repository Ruff rules. Local exceptions document
case-local scripts (INP001), long manual evidence prose (E501), the formatter's
COM812 conflict, straightforward case-specific validator/test branching, CLI
printing, lazy imports resolving the builder/validator cycle, and ordinary
test assertions/fixed frame cardinalities. No repository lint configuration
was changed.

```text
python experiments/codex_dogfood/case_0008/adjudication/stage_c.py replay
uv run pytest --no-cov --noconftest -c experiments/codex_dogfood/case_0008/adjudication/stage_c_pytest.ini experiments/codex_dogfood/case_0008/adjudication/test_stage_c.py -q
uv run ruff check experiments/codex_dogfood/case_0008/adjudication/build_judgments.py experiments/codex_dogfood/case_0008/adjudication/stage_c.py experiments/codex_dogfood/case_0008/adjudication/test_stage_c.py
uv run ruff format --check experiments/codex_dogfood/case_0008/adjudication/build_judgments.py experiments/codex_dogfood/case_0008/adjudication/stage_c.py experiments/codex_dogfood/case_0008/adjudication/test_stage_c.py
git diff --check
git diff --cached --check
```

## Limits and handoff

All 35 distinct REQUIRED units (71 obligation-relative judgments) were
inferable at task start. No inherent discovery or unresolved judgment was
needed. No obvious mandatory task-interpretation gap was found.

The historical implementation ledger and research references are outside the
eligible packet. Future implementation and pass/fail outcomes cannot be judged.
ADR-0005's header retains its historical unimplemented status; the central
architecture summarizes a narrower generation surface than taxonomy/source.
Source defines the implemented API; these documentation limits are recorded
without narrowing the task or inferring any treatment. No canonical future
algorithm-independent acquisition type or execution policy is invented.

`gold_statistics.json` contains gold-only counts, with no treatment comparison.
This checkpoint ends Stage C. Confirmation remains sealed. Stage D must occur
only after this checkpoint is committed and separately unblind authorized
inputs; this session performs no joined or effectiveness analysis.
