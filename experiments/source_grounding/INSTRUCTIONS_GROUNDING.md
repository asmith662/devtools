# One source-grounding treatment primary

You are the designated GPT-6 Sol / High primary for this case only. The host supplies
the complete frozen instructions and authenticated packet directly in this invocation.
Do not use shell or tools, inspect the filesystem, or create files. Do not access any repository checkout, Git/history, parent or
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

Return only one strict JSON object matching the supplied response schema.
The host creates canonical `stage_c_review.json`, assigns the exact disclosed case,
frame and packet digest, and records single-primary invocation/NO_ACCESS metadata.
The review and verdicts are treatment grounding, never semantic gold. Your exact fields:

```
cells: complete judgment list in packet order
units: []
gaps: []
self_review: nonempty same-primary audit of evidence, completeness and uncertainty
```

Each cell has exactly:

```
obligation: packet obligation id
source_key: exact opaque key from its packet source
verdict: one of the three frozen values
spans: [{source_key: the same key, quote: exact nonempty substring, occurrence: positive integer}]
statement: concise concrete repository fact (nonempty for GROUNDED_SOURCE)
reason: why that own-content fact bears on O, or why it does not
assumptions: list of explicit inferability assumptions, possibly empty
uncertainty: exact uncertainty, empty string if none
additional_information: information needed, or explicit inability to identify it
```

Copy quote exactly from complete disclosed source content. occurrence is 1-based
among all exact substring matches, searched left-to-right by Unicode code-point
index INCLUDING OVERLAPS (advance one code point after each match). For example
"aa" in "aaa" has occurrences 1 at index 0 and 2 at index 1. Do not supply offsets
or canonical identities. The host maps the source_key and derives start/end,
end exclusive. It rejects missing quotes, invalid occurrences and foreign keys;
it never trims, normalizes, guesses, repairs or substitutes evidence or judgments.
Grounded cells require nonempty own-source evidence locators.
Uncertain cells require nonempty uncertainty and additional_information. No cell may
be silently omitted; duplicate/foreign cells fail. Do not fabricate facts or resolve
uncertainty by pretending to inspect forbidden inputs.

The host's scientific attestation records exactly model="GPT-6 Sol", reasoning="High",
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

Do not claim unseen access or verified host routing. The host rejects tool attempts
and separately records authorized-only disclosure and no scientific filesystem dependency.

Recheck every verdict, exact quote copying, occurrence, completeness and uncertainty
once yourself. Audit content, not character arithmetic. Return your structured response.
The host runs the frozen deterministic builder and validator without revising your judgments.
The controller authenticates seven scientific files after process termination;
terminal text and `.local/codex-result.md` are operational only. Stop.
