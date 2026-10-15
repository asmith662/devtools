# Bounded EvidenceCard readiness gate history

The findings below describe candidate-01/02 and preserve why those candidates
stopped. The current authorization supersedes absolute maximum discovery with
[finite workload certification](CAPACITY.md). No successful capacity receipt is
claimed by this historical finding. Candidate archives remain unchanged.

This is a prospective engineering finding, not a scientific result. No model call,
new gold, Stage A, replacement plan, approval or run was made. The old run remains
blocked. Candidate source changes are unpublished and not execution-ready.

The authorized design separates raw-resource Pass A, host exact EvidenceArchive,
bounded semantic EvidenceCards for global Pass B, and host canonical reattachment.
Definitions remain intended to be preserved; the measurement procedure is amended.
The host must not relabel incomplete representation or uncertainty as a negative.

The current authenticated host disclosure renders `json_bytes(disclosure)` using
ASCII JSON escaping. Bounded decoded Unicode strings do not imply an equally
bounded wire representation: U+1F600 occupies one Unicode character but twelve
ASCII JSON characters. A complete prospective bound must include this expansion.

The deterministic stress calculator is
`experiments/source_grounding/chunked/cards.py:worst_case_cards`. It uses no case
resource content or semantic judgments, grants short five-character evidence/cell
references, and fills permitted 512-character summaries and 256-character
uncertainty notes. Every card retains the approved fields. Task, obligations,
instructions, coverage/provenance and the outer host wrapper are omitted from this
calculation, so these are already lower bounds on the full maximum input.

| Case | Cells | Card-only characters / UTF-8 bytes | Percent of 1,048,576 |
| --- | ---: | ---: | ---: |
| 0022 | 744 | 7,134,236 | 680.3738% |
| 0023 | 640 | 6,136,980 | 585.2680% |
| 0024 | 444 | 4,257,536 | 406.0303% |

All exceed the required 70% ceiling under that ASCII JSON representation. The
retained candidate-01 archive preserves the original implementation and finding.
The later [lossless card candidate](../../../source_grounding/chunked/README.md)
implements literal Unicode length framing and exact replay. Its complete candidate
inputs fit below 70% without ASCII-only restrictions, truncation or relabeling.
This is a representation improvement, not a scientific-method equivalence claim.

Local Codex 0.162.1 catalog metadata reports 272,000 default context tokens,
872,000 maximum and 95% effective context. It is reported runtime metadata, not
proof of active scientific-profile capacity. The separate
[official Astra model page](https://developers.openai.com/api/docs/models/gpt-6-astra)
reports 128,000 output tokens; that is API capability evidence, not an authenticated
Codex output reservation. Neither resolves the character gate above.

The candidate usage parser preserves five raw reported categories without an
inferred total. Missing metadata is unknown, duplicate completion rejects usage
capture, and optional observation errors remain separate from response success.
The typed measurement and pure budget checks are not yet integrated into mandatory
scientific publication, invocation pre-entry, branch adoption or chunked execution.

The remaining readiness gate is active-profile context/output capacity. The
candidate output guard refuses UNKNOWN output capacity, token-bound estimator or
reasoning reservation. The host exact archive/coverage/reattachment projection is
implemented and tested on synthetic values, but adoption, full chunked execution,
pre-entry accounting and final canonical assembly remain unintegrated. No plan or
scientific checkpoint is produced while readiness is unestablished. Native
stdin/schema/final-response and sandbox behavior have not changed; no live smoke
was invoked. No old approval authorizes candidate bytes.
