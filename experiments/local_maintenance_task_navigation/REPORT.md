# Maintenance-task-navigation-0001: failed B-0035 attempt

The task-directed entry was used to read the relevant file immediately, but the
real worker did not implement the inventory obligation. Ten requests produced ten
successful source reads, zero search calls, zero proposals, zero worker checks and
zero repairs. Seven reads repeated one of three previously acquired broad regions.
The worker stopped truthfully at `model_limit`; no model-authored code is accepted.

## Frozen authority and inputs

The [freeze](freeze.json) binds source revision `ffb5d25e3f4956b4f665e157a7739e50d7cf74f7`, snapshot
`2c4551f77f6bd29e1db7611689c1fc49c313c4457ef55722f71c3ac4581fdbf7`, exact task, 17 readable resources, eight existing editable
modules, independent oracles, profile/settings and all limits. It was committed
before inference in `ed16110e60f11940babfce6bc8fedd7322994b14`. Its digest is
`eba46fd3c96c2586514fd8f0b1770470b3492cd8b2f5eb7660597914aa5d33b3`. The [protocol](protocol.md), [objective](objective.md),
[preflight](preflight.json) and [manifest](manifest.json) retain the independent
definition. Ten positive/negative reference controls passed; baseline failures
were exactly the three focused/five withheld obligations, without runtime errors.
No intended patch or withheld reference source was model-readable.

The pinned local Qwen3.8-27B UD-IQ4_XS artifact, llama.cpp image, 32768-token profile
and alias were authenticated before freeze and again before entry. The existing
shared coding process owned continuation, source effects, edits, checks and custody.
No provider substitution, download, paid fallback or service mutation occurred.

Bounds: ten acting requests, four proposals, at most three applied candidates/two
natural repairs, twenty acquisition actions, 150 seconds per call, 1080 seconds
process/1200 seconds outer limit; input 28160/output 4096 tokens. Prompt/resulting
source 32768 bytes, disclosure 8192, edit-region 4096, aggregate 8192, two operations.
NavigationPolicy(6,6144,2) and deterministic projection 24576/20000 were frozen.
No auxiliary inference was configured or entered. Tests, scope and grading were
not changed after output.

## Actual model choices and exact source

The first complete request was 9345 bytes. Its incomplete candidate view occupied
3394 bytes and included the relevant host file/class, package docs and a less
directly relevant `request_compaction` method. The model chose the **file** unit,
not a method-sized symbol, then continued broad character-range reads. This is
host-conditioned source selection, not evidence of model-selected task queries.
It never called `find_source`, requested an outline or exercised the outline limit.

All reads targeted `src/devtools/agents/coding/repository.py` at the frozen content
identity. Coordinates are Unicode character offsets, half-open; these particular
regions also contain 8192 UTF-8 bytes each. Source length was 31897. The initial
file-unit read was explicitly partial with `continuation_start=8192`. No invalid
range, permission refusal, stale read or uncertain Tool outcome occurred.

| Request | Model-selected operation | Acquired range | Retained-input bytes | Active-input bytes | Repeated range |
| --- | --- | --- | ---: | ---: | --- |
| 1 | read_source_unit | [0, 8192] | 9345 | 9345 | no |
| 2 | read_source | [8192, 16384] | 20166 | 20166 | no |
| 3 | read_source | [16384, 24576] | 30158 | 30158 | no |
| 4 | read_source | [0, 8192] | 40312 | 29491 | yes |
| 5 | read_source | [8192, 16384] | 50774 | 29961 | yes |
| 6 | read_source | [16384, 24576] | 60624 | 29657 | yes |
| 7 | read_source | [0, 8192] | 70778 | 29349 | yes |
| 8 | read_source | [8192, 16384] | 81240 | 29961 | yes |
| 9 | read_source | [16384, 24576] | 91090 | 29657 | yes |
| 10 | read_source | [0, 8192] | 101244 | 29349 | yes |

The host disclosed 81920 bytes across ten actual operations;
there were 24576 unique source bytes. Nine results (73728 bytes)
were consumed in subsequent requests. The tenth result was retained but never
consumed because the request budget ended. Acquired does not imply consumed.

From request 4, projection retained two broad regions and omitted the third for
source capacity. Each subsequent reread selected a region absent from that active
Prompt. All three broad results plus objective, metadata, native exchange and Tool
overhead already required 40312 bytes at request 4, above the unchanged 32768 ceiling.
Duplicate historical acquisitions were also omitted; exact active witnesses still
matched the presented source. The retained-history request before the tenth model
entry measured 101244 bytes; its actual projected input was 29349. The final Tool
result was retained afterward. All actual requests fit (maximum 30158).

This establishes a repeated acquisition/projection pattern, not the model's private
intention or proof that omission alone caused it. No smaller method search was
selected despite availability. A different shortlist or retained view is not a
measured counterfactual. No semantic summary was produced, adopted or consumed.

## Independent review and grading

Every archived editable file equals its frozen baseline byte-for-byte; the
[candidate archive](evidence/candidate.json) includes exact content and hashes.
[Independent review](independent-review.json) reports one passing currentness
control and three failed focused inventory checks; one passing no-witness control
and five failed withheld checks. Both pytest exits are known 1, with no errors,
skips or truncated capture. The [focused XML](evidence/grade-focused.xml) and
[withheld XML](evidence/grade-heldout.xml) survived alongside immediate per-command
receipts. The grading wrapper exited 0, meaning grading completed, not acceptance.
Outer grading duration was not measured separately; captured pytest output reports
test durations. No candidate was repaired or substituted by Codex.

Checkout released normally after both worker and grading. All artifacts remained
in ignored staging until release, then were copied exactly. SourceCustody restored
known source; no unknown bytes required reconciliation. This case does not alter
the prior recovery receipt or its unknown grading-wrapper exit qualification.

## Usage and outcome qualification

All ten provider entries returned normalized responses. Known usage was
68179 input and 779 output tokens;
cache/reasoning counts remain unknown. Model time was 92.137005s,
shared coding-process time 93.256725s. All ten native call identities
are unique, with truthful correlated feedback and known acknowledgments. Required
objective/policy text was retained. There were no edits, model-requested procedures,
host candidate checks or repair feedback. Independent grading is separate from
worker validation. No effectiveness rate or causal improvement follows from one run.

The [trace analysis](evidence/trace-analysis.json), raw requests/responses, original
results, [measurements](measurements.json), [verification](verification.json) and
exact archive retain available facts.
Command observations cover framework-owned preparation/control Commands; they do
not invent absent check executions or private model reasoning.

## Framework result and next bounded question

The production navigation increment passed 3889 protected tests, two optional skips,
100% configured production line/branch coverage on committed executable tree
`4d5ad371dd4d43cb677ad2c7d9ac40549a3fd573` with 1191 unchanged physical inputs.
See the [development contract](../../docs/development/task-directed-navigation.md)
and [delivery receipt](../../docs/research/code-audit/task-directed-navigation-20261029.json).
The new entry avoided the old metadata-only trajectory in this sample, but did
not produce useful maintenance. B-0035 and broader B-0043 remain open.

The highest-leverage next question is **method-sized working-set selection**:
make existing precise method/window candidates easier to select than whole-file
chunk traversal, then measure whether a small exact working set survives projection
long enough for an edit. Initial file/class candidates were reachable but too broad
for this worker's chosen strategy. This is a proposed bounded interface experiment,
not authorization for another retriever, loop, larger budget or automatic repair.
No next increment or second model attempt is started here.
