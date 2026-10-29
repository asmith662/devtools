# Reliability-0001: source interface works; summary and repair results qualified

One primary task/treatment ran on implementation
`526a54e084e0ccd2ab0e9be972a363bc2fd07947`. The
[freeze](freeze.json), [protocol](protocol.md), [original history](history.json)
and [raw evidence](evidence/result.json) remain unchanged. No candidate was
accepted, no production task was integrated, and no live attempt was repeated.

## Observed interfaces

The authenticated Qwen3.8-27B UD-IQ4_XS service used the existing 32K profile.
The auxiliary request explicitly selected llama.cpp JSON-object generation.
It nevertheless returned one lowercase Markdown JSON fence. Strict validation
rejected it; **no live acting request consumed a semantic summary**. The
normalized response was retained verbatim, and deterministic fallback preserved
the task. This demonstrates a provider/profile interoperability limitation, not
the root cause of server grammar behavior.

The acting worker made five requests and six source reads. Every read omitted
`end`, acquired the truthful bounded source and received exact version, range,
length and continuation metadata. It selected all three files on its first
request. It later reread contracts.py, focused.py and occupancy.py. There was no
natural invalid range, so live recovery competence is unmeasured; maintained
independent tests prove the invalid-call/refusal/corrected-call mechanism.

The first edit was admitted and installed. A second proposal contained two
overlapping anchors; ordinary admission refused the whole batch. No partial
second edit or automatic retry occurred. Candidate bytes were archived and all
three original files were restored. Native call IDs and all available original
history remained intact. The terminal result was `proposal_limit`, not accepted.

## Frozen-check defect and independent candidate review

Independent review found an error in the supervisor-authored focused oracle:
reservations `[1,3)` and `[5,8)` clipped to `[2,6)` have total length **2**, but
the frozen test expected **3**. The first candidate returned 2 and the host
reported that assertion as failure. This faulty feedback confounds any inference
about repair quality. The original test, actual feedback and model output are
preserved; this report does not correct the frozen trial or rerun it.

The separate pre-frozen held-out oracle also failed, independently: the archived
candidate indexes `intervals[0]` when no valid intervals remain, raising
`IndexError` for empty input. The model's second proposal attempted an empty-list
guard, but its overlapping batch was refused. Codex supplied no repair. Neither
the focused-oracle mistake nor the rejected repair makes the candidate correct.
The reported primary outcome is an interface verification with a confounded
coding/repair assessment, not a clean measure of model engineering ability.

## Measurements and semantic inspection

| Fact | Observed value |
| --- | --- |
| Original / first deterministic request | 18,323 / 1,963 serialized bytes |
| Subsequent active requests | 5,413; 5,125; 7,422; 9,059 bytes |
| Auxiliary calls / time | 1 / 72.466737 seconds |
| Auxiliary input / output tokens | 4,355 / 915 |
| Acting calls / measured inference time | 5 / 54.883229 seconds |
| Acting input / output tokens | 8,282 / 986 |
| Controlled coding run | 128.446929 seconds |
| Admitted edits / refused repair proposals | 1 / 1 |
| Primary focused / held-out exit | 1 / 1, for distinct reasons above |

Usage is provider-reported; cached and reasoning usage remain unknown. These
are serialized host bytes, not provider token counts. Exact per-request native
calls, provider settings and actual check diagnostics are retained in evidence.

The raw notes preserved the distinctive nested-interval counterexample,
observed 10 versus expected 8, and rejection of sorting by end before additive
accounting. They did not invent source witnesses or success. They also implied
that prior live activity was not retained, whereas this history was explicitly
host-authored, and misspelled `occupied_minutes` as `occupancy_minutes` in the
next step. Metadata acquisition flags were overgeneralized. Citation membership
alone does not certify any of these interpretations.

## Separately identified post-hoc maintenance

After this frozen attempt, an opt-in, single-lowercase-JSON-fence policy was
implemented in the existing semantic compactor. Defaults remain strict. No
second model request, generic salvage or JSON repair was added. Applying that
policy **offline** to the retained actual auxiliary output passed the unchanged
structural/provenance checks and produced a valid 4,301-byte projection with
zero source witnesses. This is recorded in [analysis.json](analysis.json);
it is not live adoption, consumption or a rescued original trial.

A maintained independent non-Qwen scripted host demonstrates actual subsequent
acting consumption through the same coding process, exact source acquisition,
edit and checks. That deterministic result cannot establish real-model summary
fidelity or benefit. Final implementation validation is recorded in the
[delivery contract](../../docs/development/local-agent-reliability.md).

The highest-priority evaluation improvement is independently cross-checking
fixed-check expectations before live entry. A future separately authorized repair
task can then assess valid feedback and nonoverlapping edit proposals under the
explicit envelope policy. No next trial or broader implementation is authorized
by this report.
