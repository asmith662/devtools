# First authentic B-0033 coding continuation: B-0051

**BLOCKED / `proposal_limit`.** The continuation mechanism lawfully dispatched a
distinct second attempt, but Qwen did not produce a passing repair. B-0051 remains
BACKLOG. Both coding slots are consumed; no third attempt, review, installation or
closeout was performed.

## Admission correction and publication

The [earlier admission refusal](coding-continuation-admission.md) remains historical
evidence. Its unrelated malformed Checkout receipt resulted from a historical
double-sealing capture defect: `.local/finish-offline11.py` loaded a sealed owner
mapping into the old Checkout payload before finalization. Reintroducing the
original owner seal reproduces the stored completion identity exactly. The
[bounded derivation](code-audit/coding-continuation-b0051-20261104/historical-double-seal-proof.json)
preserves the authenticated producer and digest identities.

The original `cf08541a...` receipt remains invalid and byte-for-byte unchanged.
Checkout has independent operation-bound releases, not a global release chain.
The corrected owner authenticates B-0051's exact release; `work-history` separately
reports the historical integrity failure. Relevant corrupt, missing or foreign
custody evidence still refuses. The standing authority control chain is unchanged.

Parent observations authenticate an acknowledged edit causing collection
SyntaxError (exit 2), a later acknowledged correction, and complete ordinary
public failure (exit 1) on the final archived candidate. No edit followed that
check. Eligibility now recognizes that recovered sequence while rejecting
terminal collection errors, other collection failures, unknown effects, missing
observations and stale candidates. Private rejection remains outside this pathway.

Codex published the correction at `df589ac44a25d1914ecbbad7e2459687741787d8`
and `dc89074f676f079d465f0f93589f95dc45468544` before live inference. The first
protected gate caught two Integration closeout regressions in an overly broad
in-memory equality guard. The final guard rejects embedded seals and retains the
existing disk-journal fence and host-owned Integration file registration.
No standing policy, task obligations or model budgets changed.

## Authenticated attempt and authority

| Record | Exact identity |
| --- | --- |
| Parent assignment, attempt 1 | `47a414bee5aaba90ee1ecdcb1795e4563f153c14e20b99392fad2505ceff391c` |
| Parent BLOCKED result | `0d3cf5f97dba9561e5d448611024d4ab753320ed1cb4a10ff8b61bbd0ab100b2` |
| Child assignment, attempt 2 | `0773aaf5111062511778f9e948c0071494524ab431a44ff2f690e2036e29ba02` |
| Fresh policy-derived grant | `aafba3477c2f75fc42905d6755aa4dfa9321942c5dd005584e83823b9642e2af` |
| Policy decision | `168c4d140c8c7577e07dd11dd6c0767ecd19ae568e9bb31ada0a84ae2fa142f5` |
| Child BLOCKED result | `7ce6ad6a0c3443ef53591e3f77e3ac91edea15baf44f5efb31398ff881c7c558` |
| Child Checkout release | `2d6c8b0ff9102150129e995d6b4ce66ddbe56b858307c70c4f5c46b1f0f6bb09` |

The existing native owner created `.local/backlog/work/B-0051/attempts/0002/`.
Active policy
`08fcfcbfda2e51db7a7fb61a5cdd923deec75ebbff4cdad4b8e9f4520fa33662`
authorized the fresh exact grant automatically. No manual grant or new Intake
item was used. The ordinary feature ref
`feat/native-b-0051-attempt-2-20261104` was created at published `dc89074f`;
the parent ref and all 66 inventoried parent/forensic files were preserved.

The public input was recovered directly from the
[original frozen bytes](code-audit/native-scope-followup-20261101/public.py.txt):
18,070 bytes, SHA256
`7de45c1583dc96faeaec5ff09bc263ae649f28751cc6dfd3a0b08402cdc016aa`.
Its content identity remains
`1f4495ac7bbda0bc6726efaf33fb0b7f1b6d0ca2f7f4304b9d792fc9410859db`.
All four original task input identities and the reviewed obligation authenticated.
The same native owner's Intake writer materialized and later removed the exact
temporary file; no assertions or acceptance semantics were reconstructed.

Worker provenance is `qwen38-b0051-attempt-2-coder-20261104`, source
`llama.cpp/qwen38-local/b0051-attempt-2-coder-20261104`, using the approved
`qwen38-native64-portable-defaults-v1` profile. The existing persistent Qwen
ModelInteraction adapter performed actual inference. The host supplied the
original task, current source scope and approved final public-failure feedback.
Qwen authored all three replacements. Private oracle implementation was excluded
from all six requests.
The original eight-call, three-proposal, six-acquisition, 120-second call and
900-second episode limits, 2,048-token output allowance and capture bounds held.

## Genuine coding result

Six adapter entries produced six actual provider observations. Qwen made four
`read_source` acquisitions and three `replace_source` proposals; all three edits
were admitted. The fixed public command ran after each admitted edit:

| Candidate | Public result | Observed failure |
| --- | --- | --- |
| First | Exit 1; 2 failed, 19 passed | Called undefined `_iter_module_level_nodes` |
| Second | Exit 1; 1 failed, 20 passed | `guard-conditional-declaration` expected ambiguous, incorrectly resolved |
| Final | Exit 1; 2 failed, 19 passed | Caller unpacked `(child, inside_local_scope)` while helper yielded bare AST nodes |

The final failure was `TypeError: cannot unpack non-iterable Assign object`.
The exact [candidate](code-audit/coding-continuation-b0051-20261104/native/worker/final-source.py.txt)
has SHA256 `d14de3e8d727c9025890b88774af9e29ae7100e1ce69e8c7d7fd0ad25450f079`;
its [diff](code-audit/coding-continuation-b0051-20261104/native/candidate.patch)
is preserved without correction.

Public checks never all passed. Independent private acceptance was **not entered**;
none of the original 12 holdouts is claimed passed or failed. Structured
`submit_review_proposal`, trusted host candidate disposition and Integration
planning were ineligible and were not entered. There was no reviewer continuation.

Reported usage was 81,015 cumulative input and 1,535 output tokens; peak reported
request input was 22,143 against a 62,464-token input ceiling and 65,536-token
window. Cumulative input repeats request history and is not unique source tokens
or uncached prefill. Native elapsed time was 285.83 seconds, driver time 286.31,
adapter time 152.98 and public-command time 79.56. First-token latency was not
observed. Native captures used 490,628 bytes and supporting captures 11,072,
within the unchanged 1 MiB combined envelope.

## Custody, evidence and validation

All effects were acknowledged. The exact child release authenticates restored
source and return to main. Source raw SHA256 is
`2575f9af3d983d50dfe62cec64711d762da890f270648d6b4058f8bbfd355043`,
content identity
`8783209c15a9d21fa243abd7ca60d5a32a580552cf20d1c0f561e31ddf2211d1`.
The candidate was not installed. The public temporary file was removed only after
byte verification and released custody. The pinned Qwen container remained
unchanged, healthy and idle at 64K. Inspector remained clean at
`b3fa51b22b7eeabc9c74d1eff4012e597b5dc5e6`. B-0053 remains CLOSED.

The [episode receipt](code-audit/coding-continuation-b0051-20261104/episode.json)
links the exact native result, grant, candidate, observations, public checks,
usage and timing. The bounded archive contains 67 byte-exact files, 624,228 bytes;
it reuses native captures rather than rebuilding historical evidence. A scoped
`.gitattributes` preserves those evidence bytes without line-ending conversion.
The verbatim candidate and diff retain their original line endings and are binary
Git diff inputs; JSON observations remain reviewable text.
The full private assignment and all original forensic records remain immutable
locally.
No private oracle implementation is published in this new archive. The candidate
filename adds `.txt` for publication; its bytes are unchanged. Archived receipts
are historical evidence and confer no execution authority.

Focused admission validation passed 119 tests. The subsequent 38-test diagnostic
run passed its tests but failed freshness because a comment changed during it;
it is not fresh passing evidence. A frozen three-test rerun then passed both
previously failing Integration cases and seal-injection refusal, with unchanged
inputs. Ruff, formatting, strict mypy (634 files), layout and Git checks passed.

The final [protected gate receipt](code-audit/coding-continuation-b0051-20261104/protected-validation.json)
binds exact `dc89074f`: **4,347 passed, two skipped, 100% configured production
coverage**, 4,503.60 seconds, exit 0. The earlier failed gate is retained. No
comprehensive suite or model inference was rerun merely to publish this result;
the restored executable tree reuses that final validation.

The remaining blocker is engineering repair consistency: the model failed to
preserve a helper/caller contract and genuine module-level ambiguity under public
feedback. Continuation identity, standing grants and recoverable custody now have
a real measurement. Both authorized coding slots are consumed; further repair
requires a separate authorized engineering decision, not another dispatch here.
