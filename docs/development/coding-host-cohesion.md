# Coding-host cohesion and bounded edit feasibility

## Authenticated scope and ownership decision

Starting main is `a5d58f5ed5ad0611fdeec21dd1cdfc2742a779a8`. The prior
[maintenance attempt](../../experiments/local_maintenance_feedback/REPORT.md)
is immutable: two source-grounded proposals exceeded a 32,768-byte resulting-file
limit; no edit or candidate check ran. This increment separately validates a
production extraction, then preflights a new B-0035 attempt. Refactoring success
does not establish model maintenance success.

Inspection found two responsibilities inside `repository.RepositoryCodingHost`:
coordination of native operations/authority/effects, and deterministic source
geometry for complete replacement batches. The latter already has a canonical
owner in `coding.edits.replace_exact_text`. Extend that existing owner rather
than creating another presentation layer, state bag, repository host hierarchy
or editing engine. This is an internal Agents dependency change, consistent with
the [bounded coding contract](bounded-coding-agent.md), not a change to Runtime,
Context, ToolRunner or Resources ownership.

| Responsibility | Owner after extraction |
| --- | --- |
| Model phase sequence, response identity and finite budgets | Existing `process.run_coding_agent` |
| Initial task/Prompt, continuation, discovery/index, source acquisition | Existing repository host and Context/Tools |
| Currentness, readiness, native operation count and argument decoding | Repository host, before batch admission |
| Exact anchors, disclosed-source correspondence, overlap, aggregate size and same-version composition | Existing `coding.edits` owner through `admit_source_batch` |
| Native refusal feedback, authorization and one application dispatch | Repository host and existing Model/Tool composition |
| Fixed checks, candidate archive/restoration and effect uncertainty | Existing Tools/Resources, host collaborators and SourceCustody |
| Deterministic/semantic/adaptive selection | Existing projection and compaction owners, unchanged |

The host delegates a lazily decoded sequence. This preserves refusal order:
the operation-count limit is checked before decoding any operation, and an
earlier source admission failure wins over a later invalid argument object.
The batch function returns only a complete tuple of admitted after-images;
failure exposes no partial plan. It neither reads files nor executes effects.
It has no model/provider, Prompt, ToolRunner, command or application dependency.
It uses existing Context identities and exact disclosure options, and calls the
same `replace_exact_text` primitive used by the legacy Qwen adapter.

`EditLimits` and `SourceChange` move with admission into `coding.edits`.
The documented `repository` import paths explicitly re-export the same types;
call signatures, dataclass fields and `asdict` projections remain unchanged.
Their Python definition module changes; no supported pickle checkpoint contract
exists or is introduced. The host keeps its sole mutable state; no second
history or candidate state is added. The complete `prepare`/projection behavior
and legacy Qwen task formats remain untouched.

This extraction removes source geometry and batch assembly from the lifecycle
coordinator, allowing admission to be inspected and exercised without a live
ModelInteraction or filesystem mutation. It does **not** implement B-0035's
first-request metadata inventory, and does not introduce another generic API
registry or planning abstraction. Maintained consumer tests instrument the actual
host-to-admission boundary and protect independent literal refusal/effect facts.

## Resulting-source size is not Prompt capacity

There is no hardcoded 32 KiB default in the shared edit primitive.
`EditLimits.source_bytes` is an explicit positive host value, passed to
`replace_exact_text`. That function measures the UTF-8 bytes of each complete
resulting file after literal replacement. Batch admission checks the complete
combined after-image again after composing same-file anchors in reverse-offset
order. Thus each replacement and the combined per-file materialization must fit;
this is neither a per-range limit nor the sum of resulting files in the batch.

Independent bounds remain:

- `region_bytes`: old/new anchor bytes, including line-ending adaptation.
- `aggregate_bytes`: total removed and inserted bytes across the proposal.
- `operations`: number of native replacements in the batch.
- `disclosure_bytes`: source bytes exposed per read, with exact range provenance.
- `SourceScope.maximum_resource_bytes`: observed source and subsequent reads;
  SourceCustody also uses this bound for capture and restoration verification.
- `prompt_bytes`: serialized complete ModelRequest capacity; provider token
  capacity/output reserve are separate again.

Finite after-image bounds constrain full-string materialization, observation,
hashing, writes and known-source custody. They do not authorize changes, prove
source freshness or substitute for exact acquired anchors. The particular
32,768 value is retained host/legacy experiment policy, not an established
universal optimum or a property of native Prompt correctness. Both budgets
happening to equal 32,768 in prior evaluations does not couple their semantics.

A legitimate small replacement in a larger file can fail this whole-file bound
even if its anchor, aggregate edit and Prompt are tiny. Extraction improves this
host's cohesion and practical margin but does not solve arbitrary large-file
editing. No admission-contract change or limit increase is necessary here.

The next general policy review should separate bounded replacement/growth from
an explicitly host-selected maximum observable/materializable file size. Existing
configurable limits can already express a larger finite profile, but any future
profile must coordinate SourceScope, custody, after-image checks and bounded
re-disclosure; increasing only `source_bytes` is insufficient. A baseline-relative
growth allowance with a separate finite materialization ceiling is a candidate,
not approved implementation. Preserve exact identities/currentness, ambiguity and
overlap refusal, per-region/aggregate limits, atomic admission and unknown-effect
reconciliation. No streaming editor, unrestricted write Tool or new transaction
framework is justified by this one failure. B-0043 and existing cohesion owners
retain that pressure.

## Validation and maintenance separation

The original focused coding/Tools/Evaluation suite passed 439 tests. Two new
refusal-order characterizations passed against the original host before source
modification. Maintained import/projection compatibility and actual delegation
controls supplement the existing non-Qwen/Qwen, projection, compaction,
source/read/edit/check and custody regressions. The committed extraction must
pass the unchanged complete protected gate before any new model entry.

A new task will separately reuse the [oracle-integrity preflight](oracle-integrity-preflight.md).
It must establish baseline failures, independent positive/negative oracle
controls and feasible source headroom before freezing one real local-model
attempt. No reference patch, hidden oracle or manual implementation is supplied
to the model. Original cases, earlier candidate bytes and historical credit
remain unchanged. Exact validation, final sizes and the separately graded
maintenance outcome are recorded in the delivery evidence after execution.

## Measured extraction surface

| Physical source | Before | After extraction | Margin under unchanged 32,768 |
| --- | ---: | ---: | ---: |
| repository.py | 32,648 | 29,038 | 3,730 |
| edits.py | 4,550 | 9,149 | 23,619 |

The coordinator loses 3,610 bytes; its margin grows from 120 to 3,730.
Both files retain CRLF. This is source-owner reduction, not line-ending
normalization. AST comparison verifies unchanged bodies for all fourteen host
methods other than `propose`, unchanged literal replacement admission and
unchanged moved dataclass definitions. Complete behavioral validation remains
necessary; AST equality alone does not prove the delegated call boundary.

The separately prepared [new evaluation](../../experiments/local_maintenance_cohesion/README.md)
has passed ten reference checks and the same three focused/five withheld baseline
assertion failures. Its private feasibility review records a localized existing
host composition seam, more than 2 KiB file margin, and unchanged region/aggregate
bounds. It supplies no patch and guarantees no model success.

The committed extraction `11945801c1f42e2adfc1614f672fc96d3ae400eb`
passed the unchanged protected development gate on October 29: 3,836 passed,
two optional skips, 100% configured production line/branch coverage. The command
took 1,506.195 seconds; its physical inputs stayed unchanged. Supported Ruff,
formatting, strict mypy and layout checks also passed on that commit. Exact
commands, identities, timing and physical inputs are in the
[delivery receipt](../research/code-audit/coding-host-cohesion-20261029.json).
The maintenance attempt is separately frozen and graded; the extraction does
not implement B-0035 or establish local-model success.

## Separately frozen maintenance outcome

[Maintenance-cohesion-0001](../../experiments/local_maintenance_cohesion/REPORT.md)
used ten real local-model requests, one inventory, two searches and eight source
reads. It produced no proposal and stopped at the model-call limit. Three source
ranges were reread after prior exact disclosures were omitted from active input.
The final read was retained but not consumed. All archived bytes equal baseline;
three focused and five withheld behavior assertions still fail. No model-authored
implementation was integrated, and no supervisor replacement was supplied.

The extraction improves admission ownership and practical edit headroom. This
evaluation does not test a resulting candidate's size because no edit was
proposed. The next evidence-led boundary is task-relevant source working-set
selection/retention, using existing retrieval, range and projection mechanisms.
Neither larger limits nor a new loop follows from this result.

## Accepted publication

Accepted main `195035b99f97081e63fffade3313d4a481839a2f` includes the protected extraction
`11945801c1f42e2adfc1614f672fc96d3ae400eb` with matching source/test blobs and all 1,185
physical validation inputs. Publication used an authorized ordinary non-force
push after observing repository requirements. The new experiment is closed;
only extraction/support code was accepted, not a model-authored B-0035 patch.
Documentation-only closeout retains those executable identities.
