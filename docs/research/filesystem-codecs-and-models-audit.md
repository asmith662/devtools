# Filesystem codecs and structured models audit

Delivered follow-through: [CSV strings, compatible JSON member lookup and Python3.12 structured initialization](../development/filesystem-contract-repair.md), production `39c583ba2b252b44b998b8fbf6e8ef6ecf163294`, normal PR#29, verified main `2b20f6119b5cbcdda2fcc78c276178fbcde780ee`. Final committed gate3077 passed/2 opt-in live skips/100% configured production branch coverage;275 focused tests/15 subtests and246 consumer tests pass;8 maintained stdlib tests plus12 original compatibility cases pass on each3.12.13/3.14.3 interpreter. [Exact receipt](code-audit/filesystem-contract-repair-20261026.json). CSV67f7d086 and JSON1671955c have append-only implemented-and-merged evidence; do not repeat their scope. B-0048 constructors are delivered; broader runtime matrix remains open. AuditPR#28 is integrated. Next major audit is ModelInteraction/serving; no new cohort begun. RI93/93,606/606,188 historical obligations and A+C-unapproved unchanged. Earlier notices are dated history. `repair:filesystem-contracts:39c583ba:20261026`.

## Baseline and authority

Reviewed integrated main `26bd8053ab8ad8323dd3273b4b0e986de05388e9` in the
single canonical checkout. Local HEAD and fresh remote main agreed before
review; tracked/index state was clean, no Checkout owner existed, and all
thirteen retained forensic files matched the previous repair receipt. The
ordinary audit branch is `audit/filesystem-codecs-models-20261026`.

This is maintainer-authorized source/behavior/consumer inspection and
documentation/Intake publication. It supplies no production correction,
execution grant, semantic architecture approval or protected-main promotion.
The containing Git commit authenticates publication; PR status is observed
separately rather than inferred from this prepublication report.

The [comprehensive audit](comprehensive-code-audit.md),
[review conventions](code-audit/README.md), package contracts, and canonical
backlog remain the existing authorities. The
[Duration repair](../development/duration-factory-input-repair.md) and prior
Core/Resources repairs are delivered; none is reopened here.

## Exact scope and review depth

The [frozen cohort](code-audit/filesystem-codecs-models-cohort.json) contains
43 exact path/blob records, 4,108 lines including two reused codecs. It was
selected before review on this baseline. Its original selection fields are
preserved beneath the completion overlay. The
[assurance ledger](code-audit/filesystem-codecs-models-assurance.json) records
every inspected function, fixture/helper/negative branch, per-path disposition,
actual consumer and dependency depth. No selected function remains unreviewed.

| Surface | New complete dispositions | Previously complete, identical reuse |
| --- | ---: | ---: |
| Codec/model implementation bodies | 15 | 2 binary/text codecs |
| Maintained substantive test/helper bodies | 16 | 0 |
| Public export initializers | 5 | 0 |
| Test package marker initializers | 5 | 0 |
| Total | 41 | 2 |

All five codecs and base, binary/text, CSV dialect/row/file, JSON
base/scalar/object/list/conversion, and Markdown file/heading/section surfaces
are covered. Export lists and imports were inspected, not credited merely
because initializers are short. The five test markers contain no imports,
reexports or independent executable behavior; their package roles were checked.

Prior full reading/writing/resolution/errors and bounded-read/writer tests are
reused, with the later writer repair distinguished from its original reviewed
version. No new Paths, Commands or writer-custody audit credit is assigned.
`test_reading.py`, previously only targeted, now has complete body review;
`test_resolution.py` closes static format/codec dispatch assertions. Running
other previously reviewed tests does not confer additional review credit.

Core conversion/error/export bodies were fully inspected as immediate
dependencies. ToolRunner's narrow body was read completely. Filesystem Tool,
Context, Qwen, dashboard and persistence caller inspection is explicitly
targeted. This is not complete Core, ToolRunner, application or persistence
subsystem signoff.

## Findings and canonical ownership

| Severity / disposition | Evidence | Existing or new owner |
| --- | --- | --- |
| P2, existing reproducible defect | NONNUMERIC numeric cells reject; numeric string headers leak AttributeError | [67f7d086](../backlog/proposals/67f7d086-86d9-400f-bfaf-d9bc4df9aea1/proposal.json) |
| P2, existing compatibility defect | Native Python3.12 object/list/CSV constructors and real read/Tool paths fail | [B-0048](../backlog/items/B-0048-restore-python-3-12-json-file-model-compatibility.md) |
| P2, new reproducible public lookup defect | Missing key matches null; compatible list/nested-array queries miss frozen arrays | [1671955c](../backlog/proposals/1671955c-42ca-4fa0-94a3-2bee570e0f0f/proposal.json) |

No new independently reproduced P0/P1 is established. P2 describes public API
correctness and declared-runtime compatibility, not an authorization bypass or
a demonstrated autonomous coding failure. No source or tests were changed.

### CSV spelling and failure contracts

The public model is string-valued; NONNUMERIC is documented as quoting policy,
not numeric conversion. On the current codec blob
`b383442f462767003fbcd28dfdf3c08d64cb6ba9`, the following literal source must
produce cells `("001", "1.50")`:

```csv
"id","value"
001,1.50
```

Actual parse and decode raise `FileFormatError`: stdlib `QUOTE_NONNUMERIC`
converted the unquoted cells to floats, then `CsvRow` rejected nonstrings.
The source spelling is not silently returned in altered form; no successful
model is returned. `1`, `1e2`, `-0`, and a custom-semicolon `007` example fail
the same contract. `1,2\n3,4\n` should preserve numeric-looking *string*
headers and cells, but floats reach `_validate_headers` and leak
`AttributeError`. Valid numeric-looking headers must not be reclassified as
intrinsically malformed merely to normalize that error.

Fully quoted NONNUMERIC, default MINIMAL, quoted embedded CRLF/delimiter,
ragged-row/duplicate-header refusal and current-state serialization controls
agree with literal expectations. Existing NONNUMERIC tests serialize strings
as quoted values before parsing; that round trip conceals the unquoted-input
defect. A future regression must start with independently authored unquoted
source, preserve spelling in parse/decode/custom dialects, and protect
source provenance, malformed-input errors and valid serialization.

The original task/oracle and retained three CSV results were inspected without
replay. Baseline failed source-version admission; improved/final failed
proposal admission. All are NOT_ACCEPTED, `candidate_modified=false`.
There is no accepted CSV patch to promote and no new effectiveness evidence.
The existing proposal received an append-only ADVISORY; no duplicate proposal,
approval, B-number or grant was created.

### JSON member lookup

Public `JsonListFile.find_by` promises the first mapping *containing* a matching
member. Given:

```json
[{"tag":"missing"},{"tag":"present","key":null}]
```

`find_by("key", None)` returns the first, absent-member item. Literal expected
tag is `present`. `item.get(key) == value` conflates absence with present null.
A real temporary JSON file read through `ToolRunner.execute` and
`ReadRepositoryFileTool` returns the same affected rich model; querying it
returns `{}` rather than the subsequent explicit-null member.

Additionally, `[{"tag":"array","key":[1,2]}]` queried with `[1,2]`, and an
equivalent nested mapping/list query, return `None`. `JsonCompatible` explicitly
accepts ordinary lists, but current stored arrays are frozen tuples and the
comparison does not normalize that boundary. Existing scalar-match/miss controls
pass; the maintained lookup tests cover scalar values only.

The new pending proposal owns these two aspects of one existing lookup contract.
Acceptance should protect member presence, explicit null, list/tuple/nested
compatible values, first-match ordering, scalars, nonmapping items, source
provenance and immutability, using public parsed and Tool-returned models.
Scoped consumer search found no maintained application invocation of `find_by`;
the Tool can expose the model, but no actual model invocation or wrong engineering
action is demonstrated. This is not a native source-identity defect.

### Python3.12 and B-0048

The already installed CPython3.12.13 interpreter was executed directly, with
only child-process `PYTHONPATH=canonical/src` and bytecode writing disabled.
No runtime, dependency or environment was installed or modified.

Eight of twelve literal compatibility cases fail with
`TypeError: super(type, obj): obj must be an instance or subtype of type`:
JsonObjectFile, JsonListFile and CsvFile construction; their three codec calls;
public object-file read; and actual ToolRunner object read. The common source
boundary is zero-argument `super()` in the three slotted dataclass post-init
implementations. Scalar JSON, Markdown, text and binary controls pass. All
twelve corresponding calls pass on the existing Python3.14.3 environment.

This is current native runtime evidence, not suspicion or a Python3.14-only
support claim. Python3.12 has no installed pytest, so a complete compatibility
suite was not run. The broader declared-version/dependency matrix remains open.
The [existing readiness record](../backlog/b-0048-integration-readiness.md)
already distinguishes the historical accepted *object-only* worker candidate
from open list/CSV siblings. Its old destination plans, reviews and grants are
not current destination validation or promotion authority. B-0048 is sufficient;
its current story/readiness overlay records evidence without altering the
approved historical Intake chain or scheduling a duplicate.

## Representation guarantees and qualified limitations

- Binary preserves exact bytes. Text/Markdown preserve decoded source content
  and encoding metadata; arbitrary decode/reencode choices do not promise the
  same BOM or wire encoding. Actual disk reads supply retained byte counts;
  directly constructed model metadata is not source authentication.
- JSON and CSV retain original `.content` as provenance while immutable
  transformations change structured state. Serialization writes current state,
  not original formatting. JSON insertion order is retained; numeric spelling
  such as `1.50` becomes normal numeric value `1.5`. Duplicate object members
  currently use stdlib last-member-wins; original source remains available.
  The documented strictness rejects nonfinite constants/float overflow, not
  every policy imposed by a durable schema.
- JSON recursive copies isolate supported mutable inputs; frozen values are
  immutable and explicit conversion receives fresh mutable structures.
  Canonical conversion preserves causal errors and ordered fail-fast behavior.
  Invalid non-JSON objects, cycles, arbitrary recursion depth and unrestricted
  resource use are not supported merely because type annotations are recursive.
- Generic disk reads enforce byte bounds before codec dispatch. Direct codec
  calls operate on already retained input; neither layer promises a CPU/depth
  sandbox, total-process memory cap or an atomic source snapshot. Stdlib JSON
  recursion/integer limits and CSV field limits remain environmental limits,
  not newly measured vulnerabilities or a reason to add a generic parser.
- CSV reader record boundaries follow native CR/LF behavior. Its dialect
  `lineterminator` is the *serialized* terminator; arbitrary custom terminators
  do not imply a compatible reader grammar. File headers are validated unique;
  standalone CsvRow dimension/string validation is a narrower contract.
- Markdown is a narrow fence-aware ATX structure, not CommonMark. Source bytes
  survive codec roundtrip; sections use logical `splitlines` and normalized LF,
  not exact source slices. Inclusive nested section ranges and first/casefolded
  lookup are deliberate display semantics, not RI edit coordinates.

These are scoped contracts or explicitly unsupported cases, not new repair
proposals. Test-oracle weaknesses are concrete: quoted CSV round trips, scalar-only
JSON member queries and absence of native3.12 execution. Synthetic arithmetic,
metadata and pure value tests remain appropriate; filesystem observation is not
required for every local conversion.

## Actual consumers and architectural cohesion

`read` owns bounded disk acquisition and static suffix/override resolution;
codecs own representation conversion; model subpackages own immutable structured
state. `write` owns shared atomic output mechanics. No codec performs disk I/O,
and no model/path result grants authority. The public export surface agrees with
the static resolver. A generic codec registry/base class is not justified by
five meaningfully different small interfaces.

`ReadRepositoryFileTool` validates repository paths and returns generic rich
files through ToolRunner. The dispatch probe uses actual temporary files. Its
default CSV dialect is MINIMAL, so this is not proof that the NONNUMERIC bug
occurs in native default Tool use. ToolRunner validation is not task permission.

Repository observation explicitly requests TEXT, then derives native content
identity; ContextTools consumes that authenticated occurrence. Qwen's `_read_text`
also requests TEXT; change-check evidence uses domain-owned JSON decoding.
Those paths do not automatically consume JsonCodec/CsvCodec structured models.
The dashboard's actual `backlog_detail` reads Markdown and derives rationale and
section names. Host-authored Qwen task oracles use MarkdownFile, which is a
different consumer claim from actual model invocation. Conversation persistence
owns its strict durable JSON schema; similar `json.loads` calls are not evidence
that it should adopt generic duplicate-member/last-wins semantics.

JSON codec freeze followed by model post-init freeze repeats recursive
projection; immutable transforms also re-freeze. That is a real local duplication
opportunity, but there is no measured bottleneck or reason to bypass constructor
invariants, add caching, or introduce another conversion owner. Any simplification
needs a concrete consumer/cost and preservation of direct-constructor isolation.
Core regex is delegated, not fully audited here. Source freshness, authorization,
runtime custody and normalized Evidence remain owned by higher domains.

## Validation, publication and remaining work

`uv run pytest --no-cov tests/resources/filesystem tests/core/conversion
tests/tools/test_filesystem.py -q` passed **228 tests in0.76s**, exit0, on
Python3.14.3. The [retained probes](code-audit/filesystem-codecs-models-probes.json)
contain complete authored source, literal expected/observed results and command
evidence: **37 representation cases +12 host compatibility +12 native3.12
compatibility =61**. Six CSV, four JSON lookup and eight compatibility expectation
failures are the reported defects; **43 controls agree**, no unexpected control
failures. Initial private harness method-name errors were corrected and are not
product findings. A probe's exit0 means its controls and expected classification
completed, not that all claimed contracts passed.

The [checkpoint](code-audit/filesystem-codecs-models-checkpoint.json) records
source/blob, JSON/JSONL, documentation target, layout, Intake-chain, whitespace,
forensic and executable-diff checks. Local link-target validation does not certify
external links or Markdown anchor rendering. No full protected gate was run:
this checkpoint changes documentation/Intake only and preserves the previously
delivered executable tree. Publication uses one ordinary branch and normal PR,
without invented independent review or protected-main authority.

The next bounded maintenance scope should separately authorize the existing CSV
spelling/type contract, the new JSON member lookup contract and the three B-0048
model constructors, with independent original-failure controls, actual supported
Python3.12/3.14 test execution and the unchanged full committed-tree production
gate. Preserve scalar arithmetic, provider/runtime behavior, source ownership and
historical candidates. There is no need for a new parser or scope engine.

After that bounded repair, the next major audit should enter **ModelInteraction
and serving**: selected source → provider request/transport → response protocol →
optional invocation/usage observation → narrow Runtime consumer, including the
already recorded observer-failure versus model-result boundary. Freeze actual
current owner/test blobs before review; use deterministic transports, not live
inference. Remaining Core regex/collections and other Core/Resources surfaces,
Agents/Runtime, complete Persistence, applications/dashboard and tooling still
need explicit domain dispositions. This assignment does not initiate that cohort.

Original RI fixtures93/93 (augmented ledger94), experimental paths606/606 and
**188 exact historical versions** retain their prior meanings and obligations.
A+C remains unapproved. Broader validation closure, normalized Evidence consumers,
application cohesion, operational recovery and cross-cutting architecture signoff
remain separate. Neither this codec audit nor earlier repairs complete the
comprehensive framework audit.
