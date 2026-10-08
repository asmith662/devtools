# Independent C.5-R semantic adjudication

Use only the four frozen packet inputs in this sterile workspace and this
instruction file. Verify `integrity.json`, the exact `packet.json.gz` bytes, the
decompressed payload digest, and all packet/manifest bindings before semantic
review. Stop if any check fails or any unexpected file is present. Do not seek a
repository checkout, Git history, other case files, external references, or
acquisition/confirmation data.

Perform a fully independent adjudication of all 18 InformationNeeds against all
32 reviewed required units: exactly 576 need/unit pairs. Do not prune pairs by
shared words, obligation, or apparent relevance. Preserve the packet's opaque
identities, exact need and unit statements, obligations, and alternative
membership. Do not change the frozen task, needs, units, alternatives, or labels.

For every pair choose exactly one label and provide a semantic rationale:

- `DIRECTLY_COVERS`: answering the need would establish the complete fact in
  the unit. State the fact sought, the fact established, and why the answer
  establishes that unit.
- `PARTIALLY_COVERS`: the need seeks an identifiable part of the unit but would
  not reasonably establish the complete unit.
- `DOES_NOT_COVER`: the need asks a materially different question.
- `AMBIGUOUS`: the packet does not support a confident semantic relationship.

Do not use shared wording alone to justify direct coverage. Preserve genuine
uncertainty; do not force a confident label. Derive unit coverage only from the
pair judgments with the packet's frozen definitions: `COVERED` when at least
one mapping is direct; `PARTIAL_ONLY` when there is no direct mapping and at
least one partial mapping; `AMBIGUOUS_ONLY` when there is no direct or partial
mapping and at least one ambiguous mapping; otherwise `UNCOVERED`. Classify
every need using the packet's frozen need labels and semantic definitions:
`NECESSARY`, `USEFUL_REDUNDANT`, `PARTIAL_ONLY`, `UNNECESSARY`,
`MISFORMULATED`, or `AMBIGUOUS`. `MISFORMULATED` and `AMBIGUOUS` require explicit
reviewer judgment; do not infer them mechanically from pair counts.

## Supplementary unit-granularity audit

Independently classify each of the 32 units with exactly one category:

- `ATOMIC_FOR_NEED_MAPPING`: one well-formed information need could reasonably
  seek the complete unit.
- `COLLECTIVELY_COVERABLE`: the unit reasonably requires several distinct
  information needs whose answers together establish it.
- `OVERCOMPOUND_FOR_PAIRWISE_MAPPING`: the unit combines independently
  searchable facts such that requiring one need to directly cover the whole
  unit is an invalid evaluation contract.
- `AMBIGUOUS_GRANULARITY`: the packet does not support a confident granularity
  judgment.

This audit is supplementary and must not alter the reviewed gold, the mapping
labels, or the direct-coverage rule. For every classification other than
`ATOMIC_FOR_NEED_MAPPING`, provide an exact semantic rationale tied to the
unit's content and the packet. Do not use source locations, inferred answer
paths, or facts outside the packet.

## Supplementary collective-coverage audit

For each unit classified `COLLECTIVELY_COVERABLE`, you may identify a minimal
set of frozen InformationNeeds whose combined answers would establish the
complete unit. Explain why the set is sufficient and minimal. Mark unavailable
or uncertain cases explicitly. This is diagnostic only: it does not revise the
frozen pair labels or the direct-coverage requirement.

## Alternative-coverage audit

For each witness alternative, preserve its ALL-complementary membership and
derive one status: fully directly covered, fully covered only through collective
need sets, incomplete, or ambiguous. Do not combine incompatible alternatives.
Keep this semantic coverage audit separate from retrieval effectiveness or any
outcome claim.

## Freeze and later comparison

Before any comparison, freeze the complete 576-pair mapping and rationales, unit
coverage, need classifications, alternative-coverage judgments, all 32
granularity judgments and rationales, collective-coverage diagnostics, identity
and completeness checks, and output digests. Preserve original bytes and record
the independent method and validation. Do not compare against another
adjudication in this task or workspace. A later reliability comparison should
separately assess direct-pair intersection/union/Jaccard, partial-pair
agreement, unit-coverage agreement, uncovered-unit agreement, need
classification agreement, alternative-completeness agreement, granularity
results, and collective-coverage results.

Do not infer retrieval performance or treatment effects. Do not perform Stage
D.
