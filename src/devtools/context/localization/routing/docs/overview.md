# Caller directed lexical role routing

`devtools.context.localization.routing` projects caller-authored role preferences
over an already produced `LocalizationLexicalAcquisition` and its
`RepositoryRoleEvidenceView`. It executes no BM25 operation and does not modify
either input.

```text
native obligation lane ------+---------------------+
                             |                     |
                             v                     v
               selected role has support?       escape
                             |                     |
                             +---- routed view ----+

full-task global lane ------ retained unchanged
```

## Preference and lane scope

For every acquired obligation query, the caller provides exactly one
`ObligationRolePreference` containing the query identity, its obligation identity
and an ordered tuple of supported `RepositoryRoleKind` values. An empty tuple is
an explicit request for no preferred tier. Duplicate/unsupported role values,
foreign task identities, unknown query lanes and mismatched obligation
associations are rejected. No role mapping is inferred from obligation/query
identities or their text. Distinct query lanes for one obligation stay distinct
and require separate preferences.

Several selected roles use OR semantics. One positive match is enough to enter
`PREFERRED_ROLE_SUPPORTED`; matching additional roles or having more support
records adds no priority. The candidate explanation references the matching
`ResourceRoleEvidence` records directly, retaining their support kinds and
native provenance without copying them. When no selected role has support, the
candidate enters `ESCAPE`. This is a lack of positive support for this preference,
not evidence against the resource.

## Lossless ordering and validation

The only tiers are `PREFERRED_ROLE_SUPPORTED` and `ESCAPE`. Candidates retain
native BM25 order within their tier. Each `RoutedLexicalCandidate` references its
exact native match and carries the one-based native rank, one-based routed
presentation position and tier. The routed position is not a score or a
replacement lexical rank. The preferred and escape sets partition every match
in the lane; the flattened view places preferred candidates first. No match,
score, query, native result or global candidate is removed. `RoutedObligationLane`
retains its original `ObligationLexicalEvidence` object, while
`LocalizationRoleRoutingView` retains the full acquisition and exposes the exact
unchanged global result.

Before routing, repository and snapshot identities must agree. Role evidence
entries must be correctly snapshot stamped, point at an equal resource in their
retained frame and have unique resource/role identities; each support source must
also be in that frame. Every native lexical corpus is checked against that frame,
every match must reference its result's own index statistics, and a native lane
may not repeat a resource candidate. All lanes must share the acquisition's
index, filename index, settings and result bound.

This is a deterministic attention-order view only. It does not mutate lexical
results or role evidence, merge query lanes, compare scores across lanes, create
Localization witness/applicability assessments, change readiness, establish
satisfaction or non-applicability, or eliminate candidates. The global full-task
lane remains the complete unmodified lexical safety lane. Any effectiveness
claim requires a prospective case with obligations, query text and role
preferences frozen before Retrieval and independently adjudicated.
