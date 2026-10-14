# One source-grounding treatment primary

You are the designated GPT-6 Sol / High primary for this case only. Authenticate
the packet with `python -B stage_c_builder.py packet`. Read only these packet files
and your own outputs. Do not access any repository checkout, Git/history, parent or
sibling workspace, prior session, web, another case, gold, child implementation,
confirmation or reserve. Do not launch another reviewer, model, agent or delegate.
Do not execute source code, tests, retrieval or RI derivations. No reconciliation.

For every packet cell, judge only that source's OWN complete content against that
cell's obligation, criteria, exclusions and gap. Do not cite another source's verdict
or infer credibility from its inclusion in the packet. Source inclusion conveys no
target, count, relation strength or rank. Natural source text remains intact.

Use exactly GROUNDED_SOURCE, NOT_GROUNDED_SOURCE, UNCERTAIN_SOURCE. Grounded means
concrete current-repository information materially helps understand or satisfy O.
Negative means it does not. Uncertain means plausible but own disclosed content
is insufficient. Filename, lexical similarity, likely edit location or incidental
imports do not suffice. A test may establish actual behavioral facts, but mere
incidental invocation does not establish purpose-relative usefulness. A document
must establish a concrete fact bearing on O, not merely share vocabulary.

Author canonical sorted ASCII JSON `stage_c_review.json` (UTF-8, indent=2, LF,
final newline). The name is the shared controller artifact convention; its schema
and verdicts are treatment grounding, never semantic gold. Exact top-level fields:

```
schema: blind-primary-review-v1
case, frame: exact packet values
packet_sha256: SHA-256 of canonical packet.json
attestation: see below
cells: complete judgment list in packet order
units: []
gaps: []
self_review: nonempty same-primary audit of evidence, completeness and uncertainty
```

Each cell has exactly:

```
obligation: packet obligation id
source: {address, document_identity, content_identity} from its packet source
verdict: one of the three frozen values
spans: [{source: the same three-field identity, start, end, quote}]
statement: concise concrete repository fact (nonempty for GROUNDED_SOURCE)
reason: why that own-content fact bears on O, or why it does not
assumptions: list of explicit inferability assumptions, possibly empty
uncertainty: exact uncertainty, empty string if none
additional_information: information needed, or explicit inability to identify it
```

Span start/end are Unicode character offsets, end exclusive, in complete source
content; quote must match exactly. Grounded cells require nonempty own-source spans.
Uncertain cells require nonempty uncertainty and additional_information. No cell may
be silently omitted; duplicate/foreign cells fail. Do not fabricate facts or resolve
uncertainty by pretending to inspect forbidden inputs.

Attestation has exactly model="GPT-6 Sol", reasoning="High",
second_reviewer=false, reconciliation=false,
host_routing_independently_verified=false, and blindness equal to this ordered list:

```
NO_ACCESS:repository
NO_ACCESS:git_history
NO_ACCESS:parent_siblings
NO_ACCESS:prior_session
NO_ACCESS:web
NO_ACCESS:queries
NO_ACCESS:ranks_scores
NO_ACCESS:annotations
NO_ACCESS:references_treatment
NO_ACCESS:pairs
NO_ACCESS:timings
NO_ACCESS:graph_ppr_rrf
NO_ACCESS:other_cases
NO_ACCESS:child
NO_ACCESS:prior_gold
NO_ACCESS:confirmation_reserve
```

Only attest truthfully. Host routing is not independently verified. If a boundary
was breached, stop and record failure; do not publish a false clean attestation.

Recheck every positive and uncertainty once yourself, then run
`python -B stage_c_builder.py build` and `python -B stage_c_builder.py verify`.
The frozen builder produces the other scientific artifacts deterministically.
Preserve original packet and builder bytes. Do not edit the builder to pass.
The controller authenticates seven scientific files after process termination;
terminal text and `.local/codex-result.md` are operational only. Stop.
