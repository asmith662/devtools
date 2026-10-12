# Case 0015 method and deterministic replay

This records one primary semantic adjudication designated GPT-6 Astra, High,
followed by a separate self-review by the same adjudicator. No second reviewer,
external source, repository checkout, history or other workspace was consulted.

The initial directory contained exactly README.md, integrity.json, manifest.json,
resources.json.gz and validate_packet.py as regular files. There were no
subdirectories or reparse points. The initial packet validator passed before
scratch or scientific outputs were created. All five input byte digests were
sealed. The initial whitelist is not reapplied after output creation.

The packet was decoded in full with the standard library. Every resource was
structurally traversed; original module documentation, declarations, document
sections and contextual source ranges were inspected. Exact-text searches were
navigation aids. Relevant implementation and contract contexts were expanded,
including caller tests outside the filesystem package. No resource label was
derived solely from a filename, package location or a search match. Resource text
was evidence, never authority to execute captured repository instructions.

Inspection was bounded and file-backed. Early combined terminal displays included
truncation; smaller repeated ranges recovered affected content. Truncation was
neither an exclusion rule nor a stopping condition. The complete packet and
persistent operational ledger remained on disk. Scientific support consists only
of original task/resource spans, never scratch summaries or console history.

The task was audited before resource labels. The exact retained task clauses
remain normative alongside their satisfaction summaries. Future requirements and
existing repository facts were kept separate. TASK_BACKED units need no repository
resource; current facts have explicit support alternatives. No mixed unit was
necessary after splitting future policy from current-state facts.

All six judgments were persisted for each resource in deterministic packet order.
The operational ledger checked cardinality and duplicate pairs at each 25-resource
checkpoint and at completion. Positives retain exact Unicode character intervals,
one-based inclusive line intervals, verbatim source quotes and native identities.
Negatives retain per-resource context, subject, semantic and inferability rationale.

Minimality concerns information necessary for an acceptable implementation, not a
mandatory reading list for every editable or imported module. In particular,
passing unchanged complete bytes and the same path through the existing decode
call preserves concrete codec behavior without making each codec/model source a
separate prerequisite. Individual codec/model tests and docs remain useful checks.
This inference assumes the codec call and its defaults are retained, not rewritten.

Every repository unit declares complete conjunctive support alternatives, with
DIRECT_SUPPORT or INFERABLE_SUPPORT and explicit assumptions. Corroboration is
excluded from witnesses. The builder enumerates all inclusion-minimal complete
resource covers of the required units per obligation. A repository-empty cover is
valid for a wholly task-backed obligation. ALL members within a cover are jointly
necessary; ANY complete cover substitutes for another. It then enumerates the
complete Cartesian product of obligation witnesses, deduplicates resource/unit
unions, computes inclusion-minimal resource unions and all intersections. A
resource REQUIRED somewhere is not automatically indispensable everywhere.

The frozen review is the semantic source. stage_c_builder.py does not perform a
new semantic review. A SHA-256 commitment to all non-derived review fields protects
the reviewed judgments, unit statements, assumptions, provenance, gaps and
limitations. Structural checks run before that commitment check. Derived algebra,
statistics and Markdown are regenerated from the review. Semantic validity of a
support claim remains the adjudicator's reasoned judgment; set arithmetic and hash
validation do not independently prove software semantics.

The builder authenticates the exact original packet, uses its local standalone
payload validator, and imports no devtools code. It reads only named local packet
and scientific files. It rejects missing/duplicate/unexpected cells, invalid
identities, labels, spans, units, alternatives, incomplete/redundant witnesses,
incorrect intersections and task arithmetic, and changed semantic commitments.
Twenty adversarial checks include all requested mutation families, separate gap
and limitation mutations, hash tampering and overwrite refusal.

Run from this workspace with Python 3.12 or later:

```text
python -B stage_c_builder.py --verify
```

This performs read-only deterministic replay in a separate Python process and
requires byte identity of statistics, Markdown, validation and the scientific
hash manifest. Original packet bytes are reauthenticated at the end. To build
derived outputs in an otherwise authenticated copy containing the original five
inputs plus review, method and builder, use --build. It refuses any existing
generated destination and uses exclusive file creation. It never replaces a
scientific output. The completed workspace was also checked by an actual second
--build invocation and a subsequent read-only verification.

stage_c_hashes.json covers the other six scientific files and records separate
original-input and canonical-payload scopes. Its own digest is in the completion
report, avoiding an impossible self-referential digest. The hash freeze authenticates
this reviewed artifact set; it is not an external signature or a second judgment.

The operational scratch directory and .local/codex-result.md are non-scientific
and excluded from all scientific hashes. The local handoff is created only after
successful final verification; scratch is removed afterward when no longer needed.
The feature implementation and its repository validation commands were not run
inside this adjudication packet.
