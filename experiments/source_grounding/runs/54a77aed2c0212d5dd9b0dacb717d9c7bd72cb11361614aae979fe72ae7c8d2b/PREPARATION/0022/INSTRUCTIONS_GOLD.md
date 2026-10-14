# One independent blind semantic gold primary

You are the designated GPT-6 Astra / High primary for this case only. Authenticate
with `python -B stage_c_builder.py packet`. Read only this packet and your outputs.
Do not access repository checkout, Git/history, parent/sibling workspace, prior
session, web, other case, prior gold, child state, confirmation or reserve. Do not
run source code, tests, retrieval, graph/RI analyses, another model or reviewer.
Do not reconcile or delegate. Never infer gold from edit destinations or filename.

Assess the original task under frozen obligations/criteria/exclusions/gaps, using
the complete parent resource frame. Do not add hidden requirements. Distinguish
necessary information from helpful-only implementation detail and unnecessary
material. REQUIRED is membership in at least one inclusion-minimal sufficient
resource witness for O, not individual indispensability. A helpful resource bears
on O but contributes no necessary semantic unit in a minimal witness. Merely
importing a relevant module does not establish necessity. Negative cells must be
actual own-content judgments, not path/keyword screening substituted for review.

Define minimal necessary semantic units with explicit statement and necessity.
Basis is TASK_BACKED, REPOSITORY_SUPPORTED or TASK_AND_REPOSITORY_SUPPORTED.
Each unit's alternatives are disjunctive; the exact spans inside one alternative
are conjunctive. Different units are conjunctive. Alternatives may include tests
that establish the same fact, without requiring unseen runtime execution. An empty
alternative is allowed only for task-backed information needing no repository
resource. Do not retire a necessary fact solely to make a witness small.
If a necessary repository fact has no available evidence, an empty alternatives
list is permitted only with an explicit repository-information gap and
unconditional_sufficiency=false. Report zero complete witnesses rather than
fabricating support. Keep any useful partial information judgments qualified.

Author canonical sorted ASCII JSON `stage_c_review.json`, UTF-8/indent=2/LF/final
newline, with exactly schema="blind-primary-review-v1", case, frame,
packet_sha256 (canonical packet.json SHA-256), attestation, cells, units, gaps,
self_review. Case/frame are exact packet values. Every resource x obligation cell
must appear exactly once in obligation then resource address order, with:

```
obligation: exact packet obligation id
source: {address, document_identity, content_identity}
label: REQUIRED | HELPFUL_ONLY | UNNECESSARY
spans: exact own-source evidence for every useful label
reason: nonempty task-relative own-content justification
```

Each span is {source: the exact three-field resource identity, start, end, quote}.
Offsets are Unicode characters, end exclusive; exact quote equality is required.
Units contain exactly {id, obligation, statement, basis, necessity, alternatives}.
Alternatives are lists of lists of these exact spans. Record a necessary unit per
obligation even if entirely task-backed; reject unsupported repository assertions.

Gaps has exactly TASK_INTERPRETATION_GAP, TASK_GAP, REPOSITORY_INFORMATION_GAP
(each a nonempty finding/explanation), unconditional_sufficiency (Boolean), and
qualification (nonempty scope statement). Preserve design freedom separately from
blocking missing information. Set unconditional_sufficiency=false if unresolved
future semantics prevent a complete unconditional task witness. The builder then
reports conditional repository integration separately and no unconditional unions
or indispensability. Conditional witnesses must never be described as closing a
task gap. An authoring qualification is visible, not a reason to silently abandon
the frozen obligations.

Attestation has model="GPT-6 Astra", reasoning="High", second_reviewer=false,
reconciliation=false, host_routing_independently_verified=false, and blindness:

```
["NO_ACCESS:repository", "NO_ACCESS:git_history", "NO_ACCESS:parent_siblings",
 "NO_ACCESS:prior_session", "NO_ACCESS:web", "NO_ACCESS:queries",
 "NO_ACCESS:ranks_scores", "NO_ACCESS:annotations", "NO_ACCESS:references_treatment",
 "NO_ACCESS:pairs", "NO_ACCESS:timings", "NO_ACCESS:graph_ppr_rrf",
 "NO_ACCESS:other_cases", "NO_ACCESS:child", "NO_ACCESS:prior_gold",
 "NO_ACCESS:confirmation_reserve"]
```

Only attest truthfully; a breached boundary stops scientific output. Host routing
is an unverified recorded limitation. No query, A ranking, source-candidate status,
grounding verdict/rationale, BROAD/QUALIFIED evidence, Reference treatment,
predecessor, treatment timing/cost or other-case information is authorized.

Conduct one same-primary audit of task interpretation, every positive cell, units,
alternatives, exact spans, unnecessary cells and minimal witnesses. Record it in
self_review; make any own corrections before publication. Run
`python -B stage_c_builder.py build` then `python -B stage_c_builder.py verify`.
Do not modify the frozen builder or packet. The seven scientific files are
authoritative only after controller authentication; handoff text is not gold. Stop.
