# External semantic-resolution decision adapter

This is non-production experimental support, not an automatic resolver or accepted
Localization policy. It implements the bounded adapter recommended by the
[research investigation](../../../docs/research/evidence-to-witness-resolution-policy.md).
It invokes no model, associates no lexical candidates and freezes no prospective
effectiveness case. Production has no dependency on this package.

```text
existing associated member + caller claim + exact criterion
        + caller-selected frozen excerpts + native proposal evidence
                            |
                            v
                external semantic proposal
                            |
                  deterministic validation
                            |
               explicit human ACCEPT / REJECT
                            |
                explicit materialize operation
                            |
                  CandidateMemberResolution
```

Every arrow is explicit. No proposal or review constructor produces a kernel
record. No kernel record creates a witness promotion or changes assessment,
applicability, readiness, competitors or complementary members. The adapter does
not authenticate humans: the caller is responsible for obtaining actual human
review. The external proposal parser cannot submit a review or bypass the gate.

## Frozen input

`SemanticPolicyIdentity` retains name/version, decision schema version,
disclosure-policy name/version and the instruction-definition SHA-256 digest.
Definitions must be retained by the future experiment; this package does not
generate a prompt, choose a model or invoke a producer. `SemanticMemberClaim`
retains a caller key, task/obligation/hypothesis, native target, statement, caller
reason and task provenance. Its text is not inferred or machine-executable.

`SemanticDecisionRequest` admits exactly one concrete member from a validated
`CandidateWitnessView`. It revalidates association provenance and requires exact
retained hypothesis/member/claim-target objects. The criterion is the exact
obligation's `SatisfactionCriterion` value; names never select behavior. Requests
retain the full native frame in memory, but JSON exports its fingerprint instead
of dumping the corpus. Changed native frames cannot replay old request bytes.

V1 permits **only the member's exact target resource** as disclosed content.
Other resources, including equal reconstructed occurrences, are rejected.
Additional evidence-content channels require a separately authorized extension.
Native attached support metadata may name other resources; that is a qualified
observation, not disclosure of their text.

`FrozenContentSlice.select(resource, start, end)` describes an explicit selection;
it does not select a passage semantically. Offsets are nonempty half-open **Python
Unicode code-point offsets**. Excerpt digests are SHA-256 over the selected text's
UTF-8 bytes. Native `ContentIdentity` is opaque and remains repository-owned:
the adapter does not substitute a plain text digest for the canonical observation
identity algorithm. Exact occurrence/frame membership, excerpt digests and full
candidate-frame fingerprints bind content independently.

`ContentBounds` freezes nonnegative maxima for resources, excerpts and disclosed
UTF-8 text bytes. V1 resource count is zero or one. Bounds apply to selected
repository text, not JSON envelope/escaped output size, task prose or native fact
metadata. Count every selected excerpt occurrence, including overlapping bytes;
do not deduplicate overlaps or estimate tokens. Canonicalize slice order by span;
reject duplicate slices and overflows without truncation or first-K selection.
Empty disclosure with zero budgets is valid for a later explicit abstention.

`request.supports` exposes exact attached lexical, role, routed and four structural
support objects through request-bound typed handles. Canonical JSON presents
native observation/identity summaries without duplicating nested corpus text.
Full objects remain inspectable through the supplied native frame. Native ranks,
routing tiers, conventions and relations explain proposal provenance; they are
not votes, proof of adequacy or preference rules.
Native RI source ranges retain their existing typed line/UTF-8-column semantics
as provenance metadata; they are not the adapter's code-point citation offsets.

`SemanticDecisionBatch` freezes a nonempty population, one request per member,
one exact candidate/policy frame, caller inclusion reason and provenance. It
contains no proposals and executes nothing. Full-frame digest and explicit
included member identities let a later evaluator measure inclusion separately
from conditional resolution. No gold or recall is computed here.

## Proposals and citations

`SemanticResolutionProposal` retains its exact request, proposed disposition,
reason, producer provenance, citations, selected native support references and
optional structured semantic argument/abstention category. Task, obligation,
claim, criterion, policy and repository/snapshot scope derive from the request;
the JSON parser requires matching explicit scope values.

Allowed dispositions are `SUPPORTED`, `UNRESOLVED` and `ABSTAINED`.
`CONTRADICTED` is rejected even if declared by a human producer. Explicit human
contradiction using the production kernel remains outside this pilot.

A supported proposal needs at least one disclosed-content citation, at least one
exact attached support reference and a `SemanticArgument` with nonblank content
observation and criterion link. A standalone "relevant", "high BM25" or "OWNER
says so" cannot replace that structure. The adapter cannot certify that prose is
true or adequate; even a well-shaped but meaningless argument must be rejected by
human semantic review. No criterion-name, rank, relation or support-count rule
supplies support automatically.

Unresolved means adjudication was attempted but available disclosed evidence does
not establish support; it is not a negative fact. Abstained means the producer
declines adjudication and must name a capability/criterion/content/missing-
observation/ambiguity category plus reason. Both may omit citations/basis. A
request without a proposal is unprocessed and remains absent.

`ContentCitation` binds request identity to **one exact disclosed slice**; sub-slice
citations require that sub-slice to have been explicitly disclosed. No free-form
quote, foreign content identity, invalid offset, mismatched digest, undisclosed
span or other-request citation is admitted. Display line ranges are not a second
offset system and are not provided in v1.

Producer provenance declares human, external model or another explicit resolver,
source artifact, input-request digest and producer identity. Future model metadata
must include model/provider/runtime/configuration identities; non-model producers
cannot carry those fields. These are inert metadata, not model configuration or
execution. V1 producer source references are nonblank strings with no task span,
so the external JSON contract is portable. Output proposal identity is computed
and included in the serialized artifact, avoiding a self-referential digest field.

`parse_proposal(json, request)` accepts the exact `proposal_payload` schema.
Reject missing/unknown fields, duplicate JSON keys, wrong frames, malformed
producer data, unsupported dispositions and invalid/duplicate evidence. Opaque
support handles resolve only to this request's retained native objects; equal
copied support objects cannot replace them. The parser returns a proposal, never
a kernel record, and performs no repair or semantic inference.

## Human review and explicit materialization

`SemanticResolutionReview` retains proposal identity, named human reviewer,
separate source provenance, `ACCEPT` or `REJECT`, and a nonblank reason. There are
no runtime timestamps/random keys and no implicit acceptance. Model producer
metadata cannot stand in for human review. V1 reviewer source identities are
nonblank strings. Rejected proposals remain audit artifacts.

```python
# request and proposal were explicitly constructed/validated beforehand.
review = SemanticResolutionReview(
    proposal.identity,
    "named-human-reviewer",
    TaskProvenance("review-artifact"),
    ReviewDecision.ACCEPT,
    "Reviewed claim, criterion and cited content",
)
record = materialize_accepted_resolution(
    request,
    proposal,
    review,
    request.candidates,
)
# A caller may later construct WitnessResolutionView(..., (record,)).
```

Materialization rejects absent/REJECT/wrong-proposal reviews and foreign current
contexts. It constructs existing `CandidateMemberResolution`, mapping the three
pilot dispositions unchanged. The claim and rationale are retained. Supported
basis uses only exact attached native support objects in existing
`LocalizationEvidenceReference`; kernel canonicalization remains authoritative.
Content citations are **external**, never smuggled into the native basis.

`TaskProvenance.source_identity` links the request/proposal/review artifact IDs;
caller/explanation retain policy, producer and reviewer context. Keep the actual
artifacts durably in the future case so those identities remain auditable.
Unresolved/abstained proposals may materialize with empty basis, following the
kernel contract. Complements need independent requests/proposals/reviews; siblings
and competing explanations remain unchanged and may all be supported.

`SemanticDecisionLedger` retains at most one proposal per request and one review
per proposal in a partial immutable snapshot. It reports unprocessed, accepted,
rejected, unreviewed, proposed dispositions, member identities and content costs.
`report(materialized=...)` validates independently supplied accepted kernel records
and reports their dispositions; reporting does not materialize or equate ACCEPT
with materialization. The ledger contains no gold, precision or necessity labels.

## Stable artifacts and replay

Request/claim/policy/proposal/review/batch keys are deterministic SHA-256 hashes
of canonical, type-qualified native values. Citation/support collections and batch
members canonicalize independent of list order. No repr fallback, randomness,
timestamps, model runtime execution IDs or arbitrary native-class deserialization
is used. Unsupported native provenance values fail closed.

`serialize(value)` emits canonical UTF-8 JSON, a schema/kind, semantic artifact
identity and payload digest. Payload digests cover canonical JSON payload bytes
including the final LF; semantic artifact/frame IDs cover type-qualified native
values. `freeze(ResolvedPath, value)` uses the canonical filesystem writer with
overwrite disabled. `replay(path, value)` uses the bounded
filesystem reader and checks exact frozen bytes against an explicitly supplied
retained native context. It makes no writes, repository reads or model calls.
Keep that context in the future experiment's canonical input capture: these JSON
artifacts are not a replacement native-corpus persistence format and cannot
rehydrate arbitrary candidate evidence by themselves. The writer's overwrite
refusal is a single-writer check, not a new concurrent publication protocol.

## Validation and next step

Tests live under `tests/experiments/semantic_resolution/` and run isolated with
`pytest --no-cov`. They exercise generic lexical, role/routed, OWNER, MIRROR,
Reference and Import fixtures; Unicode offsets/byte budgets, strict parser
rejection, review/materialization, independent members, serialization/replay,
overwrite refusal and reporting. No retained effectiveness case is replayed.
Production resolution/association tests are compatibility checks only. The
protected production coverage gate excludes experimental tests by existing
repository convention and remains unchanged.

Next freeze a **new prospective claim-level semantic-resolution case**, including
caller-associated batch/claims, exact criteria, bounded disclosures, policy and
definition identities, actual human-review protocol and blind independent
claim/witness gold **before** executing any external resolver or model arm.
Effectiveness is conditional on candidate inclusion; measure inclusion and
conditional resolution separately. This increment neither freezes nor runs it.
