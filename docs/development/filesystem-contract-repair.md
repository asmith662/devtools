# Filesystem public-contract repair

## Delivered scope and accepted baseline

Audit [PR #28](https://github.com/asmith662/devtools/pull/28) was normally merged
first: accepted main `0ca4d9b908ba257e93b381c6de1bb6eef850af64`, tree
`d91ec3791eec5414a90a192f28ead6396e7c7ebc`. All thirteen recorded audit
documentation/Intake paths and64 selected/dependency identities were verified;
no executable change entered through that audit merge. Original main was
`26bd8053ab8ad8323dd3273b4b0e986de05388e9`. Local main fast-forwarded without reset or discarded work.

The three bounded P2 corrections are **implemented and merged** through normal
[PR #29](https://github.com/asmith662/devtools/pull/29): production
`39c583ba2b252b44b998b8fbf6e8ef6ecf163294`, independently accepted main `2b20f6119b5cbcdda2fcc78c276178fbcde780ee`, validated and
accepted tree `8ada637caae056fdf696ba4d76e6c9caacd88a39`. Eleven paths comprise four production owners, four
maintained regression modules and three package documents. The
[exact machine-readable receipt](../research/code-audit/filesystem-contract-repair-20261026.json)
retains commands, input identities, timestamps/durations, actual exits, coverage,
normal merge parents, post-main verification and separate canonical owners.

## Independent baseline regressions

Before changing production behavior, permanent CSV/JSON/Tool regressions yielded
**25 intended failures,8 passing controls,51 deselected** on the authentic
integrated baseline. CSV failures are native numeric coercion/string-row refusal
and leaked numeric-header AttributeError; JSON failures are absent-null and
compatible-array lookup errors. No import or collection error occurs in the
retained valid baseline. Private fixture import/newline mistakes were corrected
before retaining it and are not product defects. Final test formatting/typing
and equivalent assertion-style edits are engineering, not new audit credit.

The eight permanent stdlib compatibility tests run directly on existing
CPython3.12.13: baseline reports one failure and18 errored subtests/attempts at
the established zero-argument-super boundary. Those are manifestations of one
constructor family defect, not19 separate findings. The same eight baseline
tests pass on3.14.3. The original twelve independent compatibility probes retain
eight failures/four controls on3.12 and twelve successes on3.14. No interpreter,
pytest environment or global dependency was installed.

## Three separately reviewable implementations

1. Compatibility commit `041e8ab6369ee9683a6d23b4a503b5ab8052a0bc` changes JsonObjectFile,
   JsonListFile and CsvFile to explicit-class cooperative `super`. This follows
   each actual MRO and calls inherited initialization; it does not copy or
   bypass TextFile validation. Direct invalid metadata, parent invocation exactly
   once, root/row invariants, immutable replacements and real codec/read/Tool
   consumers are permanent tests. The affected Filesystem scope contains no
   remaining zero-argument post-init `super` call. No other dataclass family is
   silently changed and the historical Qwen object-only patch is not adopted.
2. CSV commit `04183daf31b24d6c010a49a59fa7b671a8a076f3` maps NONNUMERIC **reader** policy to
   stdlib minimal quoting. This removes stdlib numeric coercion while retaining
   standard delimiter, quote, escape, whitespace, strictness and newline grammar.
   The writer remains native NONNUMERIC. No floats are converted back to strings,
   no signature changes and no new parser occur. Literal001/1.50/1e2/-0 and
   numeric-looking headers preserve spelling through parse/decode; custom
   delimiter/escaped delimiter/doubled quote/embedded CRLF cases work. Invalid
   duplicate headers, ragged and unterminated input retain FileFormatError.
3. JSON lookup commit `39c583ba2b252b44b998b8fbf6e8ef6ecf163294` requires mapping key presence
   and compares against one canonical `freeze_json(query)` before traversal.
   Explicit null differs from absence. Ordinary list/tuple and nested mapping/list
   queries compare against immutable stored state, in first-matching-item order.
   Nonmapping entries, scalar matches/misses, provenance and immutable results
   are protected through both public parsing and actual ToolRunner disk reads.

JSON duplicate-member policy, numeric representation, exports and unrelated
constructors are unchanged. CSV NONNUMERIC writing still quotes string fields.
Structured source content remains provenance; serialization writes current
structured state. These repairs do not add filesystem authority, a sandbox,
normalized Evidence ingestion or autonomous coding effectiveness.

## Final committed-tree validation

All final executable checks ran on `39c583ba2b252b44b998b8fbf6e8ef6ecf163294`, tree `8ada637caae056fdf696ba4d76e6c9caacd88a39`. The full
canonical command `uv run python scripts/validate_development.py` passed
**3077 tests,2 opt-in live skips**, exit0, in
**1184.081s**. Configured production branch coverage is
**100%**, with zero missing lines and branches; thresholds/exclusions are unchanged.
`tests/experiments/` remains excluded before collection. No live model or
scientific controller was run.

Additional final committed-input checks:

| Check | Actual result |
| --- | --- |
| Filesystem/Core conversion/filesystem Tool/ToolRunner regressions |275 tests,15 subtests pass |
| Qwen ContextTools/change checks/development task, repository observation and Runtime Tool consumers |246 tests pass |
| Maintained stdlib compatibility module, native3.12.13 and3.14.3 |8 tests pass on each |
| Original public constructor/codec/read/Tool probes, each interpreter |12/12 agree on each |
| Supported Ruff: src/tests/apps/scripts |PASS |
| Supported formatter, excluding frozen tests/experiments |635 files formatted; advisory COM812 warning only |
| Configured strict mypy |521 files pass |
| Layout, changed package-document targets, Intake chains and whitespace |PASS;57 valid chains |
| Focused post-main behavior |275 tests,15 subtests pass |
| Native3.12 post-main maintained compatibility module |8 tests pass |

Python3.12 has no pytest installation. Its actual permanent stdlib tests and
original probes do not certify a complete3.12 package/dependency matrix, POSIX
behavior or arbitrary future interpreters. The native test module deliberately
uses stdlib exception assertions to run without pytest; the narrow PT027 style
qualification does not exclude tests or change behavior/coverage.

The gate authenticated 811 tracked source/test/app/
script/package-document/config physical inputs before and after execution.
Every recorded byte hash matches through independent remote acceptance and
post-main regression. Another120 prior-profile root settings/instructions and
excluded scientific test inputs match the earlier retained receipt; this is
separate preservation evidence. These scoped identities are not universal
transitive environment/toolchain or ignored-file closure. Broader d58697fd
validation obligations remain open.

## Publication, custody and canonical disposition

GitHub permissions, protection/rules, checks and reviews were reobserved before
normal merges. No configured requirement was bypassed and no review, CI result,
grant or WorkCycle receipt was fabricated. Accepted parents/tree and remote main
were independently observed. A non-forced fetch fast-forwarded the nonchecked-out
local main, followed by an equal-tree switch; no reset, alternate checkout,
unknown-byte replacement, historical ref deletion or force-push occurred.

All thirteen forensic files retain their original hashes. The903-row RI source/
fixture/version ledgers and frozen source-grounding/history are preserved.
This documentation-only closeout uses the same ordinary branch and normal PR
process because actual accepted-main evidence exists only after production merge.
It changes no validated executable inputs.

Existing CSV proposal67f7d086 and JSON proposal1671955c receive separate append-only
IMPLEMENTED_AND_MERGED advisories. Their administrative PENDING_REVIEW state
does not request another implementation. B-0048 object/list/CSV constructor scope
is delivered; its broader runtime/dependency matrix remains open. Historical
approvals are not rewritten; no duplicate proposal, B-number, new grant, parent
closure or architecture approval is created. Original audit conclusions and blob
pins retain their dated meaning; the cohort has a separate maintenance overlay.

## Remaining foundations and next major domain

The receipt records42 exact current paths requiring complete disposition or prior
evidence reconciliation in the three Core/Resources ledgers. This metadata-only
list includes namespace markers and the newly authored native regression module;
it is not42 newly found defects or a claim that nobody ever read those files.
Principal remaining bodies are Core regex models/search/splitting, Core system
models/detection, path-error/specification/export boundaries and their remaining
tests, Commands specification/errors/exports and remaining model/output/stdin/
environment/composition/success-result fixtures, plus conversion-test/namespace
assurance. Conversion implementation already has full immediate-dependency
review. No current Core collections package exists; old broad review wording
must not invent such a maintained owner. Exact path/blob/depth entries prevent
blanket Core/Resources signoff or repeated completed filesystem reviews.

Next major audit: the actual `src/devtools/models/interaction/` and
`src/devtools/models/serving/` owners, not historical model_serving locations.
Start with protocol/source selection, response and observation contracts,
`providers/llama_cpp.py`, request settings/errors and the corresponding protocol/
provider tests. Trace the narrow Runtime/actual application consumer and the
serving boundary as dependencies. Freeze current blobs before inspection and use
deterministic transport doubles. Then review serving lifecycle implementations
and tests without launching services. Existing clock-step/observer-versus-model
outcome pressure remains a concrete cross-domain question. No new cohort is
executed or architecturally redesigned here.

RI original fixtures93/93 (augmented94), experimental paths606/606 and188 exact
historical versions retain their existing meanings. A+C remains unapproved.
Full Agents/Runtime, Persistence/Evidence consumers, applications/dashboard,
tooling, historical reconciliation and whole-framework cohesion remain separate
audit obligations. No successor-session dossier is prepared.
