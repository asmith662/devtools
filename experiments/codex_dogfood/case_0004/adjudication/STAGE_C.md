# Case 0004 blind Stage C checkpoint

The independent adjudication uses only `blind_manifest.json` and
`blind_resources.json.gz`. No prior Case 0004 capture, Retrieval, or
protocol-authoring context was used. Repository state began as clean `main` at
`70114224aa7bf307e059468e0d543aff9796d8b7`. This checkpoint changes only new
adjudication files; it implements no production capability.

The manifest's exact task, purpose, repository/snapshot/frame identities, six
shared anchors, and eight caller-authored mandatory obligations are retained
unchanged in `blind_judgments.json`. The archive is the entire adjudication
universe. Structured packet fields were checked independently of ordinary
repository text; no Retrieval-treatment or result fields were exposed.

Manifest SHA-256:
`7810e71a91fb9d5327aeb20d00629f1347049993aff15544b5139529c9f777d5`.
Archive SHA-256:
`4d472717ba3e3306e81f96953c8fd9e6ab04e0d59fb698bd021386a40bcf147f`.
The exact task digest matches all manifest source-provenance anchors. All 498
content identities and the snapshot digest reproduce using the framing in the
frozen `observation.py`. Eligible-frame identity agrees across the packet; its
producer construction is not supplied, so no stronger independent recomputation
claim is made.

| Frozen obligation | Applicability | Required units/resources | Helpful units/resources | Alternative sizes |
| --- | --- | ---: | ---: | --- |
| ri-ownership | APPLICABLE | 3 | 3 | 3 |
| resource-path | APPLICABLE | 4 | 2 | 4 |
| python-configuration | APPLICABLE | 3 | 4 | 3 |
| test-configuration | APPLICABLE | 5 | 2 | 2 OR 4 |
| package-integration | APPLICABLE | 3 | 1 | 3 |
| tests | APPLICABLE | 1 | 2 | 1 |
| documentation | APPLICABLE | 4 | 6 | 4 |
| validation | APPLICABLE | 2 | 2 | 2 |

Each alternative is conjunctive internally. Test configuration accepts actual
pytest declarations plus the detailed static contract, or actual declarations
plus the complementary model, parser and resolver units. The other obligations
each have one defensible conjunctive set. Required classification is conditional
on the accepted alternative: it does not require obtaining every alternative
resource or every byte of a labeled resource.

The required review checks obligation, exact information, necessity rather than
convenience, smaller meaningful unit, genuine alternatives, inferability and
blind provenance. Locators name declarations, sections and grouped test cases
without manufacturing exact spans. All 25 obligation-relative required units
are INFERABLE_AT_START. Inherent discovery count is zero; no later prerequisite
is asserted. Their independent rediscovery would be avoidable exploration when
that information was missing from a later coding handoff.

All applicability findings have positive frozen-task and implemented-contract
evidence. No supported non-applicability or unresolved applicability finding is
made. Full pytest discovery, actual execution and a universal registration/role
framework are excluded from bounded contracts rather than dismissed solely
because an implementation was not found.

No unresolved information judgments or obvious mandatory task-interpretation
gap were found. The frozen frame already covers deterministic RI ownership,
snapshot/path contracts, recognized configuration, public integration, regression
tests, documentation and validation information. Soft routing itself is future
support, not a required implementation in the frozen task.

The artifact has an explicit resource-by-obligation matrix: 498 identities and
3,984 cells, with no missing, unexpected or duplicate identities. Unspecified
information is explicitly UNNECESSARY relative to that obligation and admitted
sets, not a global irrelevance or candidate-elimination judgment. Evaluation
coverage uses the exact archived production primitive executed in an isolated
module, without importing current repository implementation. No outcome formula
was added to Evaluation.

Support method:

- `inspect_blind.py`: exact archive-path reads, inventory and optional literal
  text inspection; no ranking or retrieval algorithm.
- `freeze_blind_judgments.py`: explicit human specification, deterministic JSON,
  packet/digest and judgment invariants; `--check` verifies retained output.
- `test_adjudication_support.py`: six focused isolated tests, including rejection
  of malformed coverage, witnesses, dispositions, inferability and digests.

Support tests, deterministic replay, scoped isolated Ruff lint/format checks and
both Git whitespace checks passed. No protected production suite, confirmation
validation or live service work was run for this adjudication-only checkpoint.
Current checkout target files were not consulted. Historical validation examples
in package documentation remain subordinate to the current canonical protected
development contract.

Artifact file SHA-256:
`77d28c1997e8ec8a7e22eee9a37da3d08a08e165d06ab977175d9caaa4f7fc44`.
The artifact also embeds a canonical payload SHA-256 with its digest field
omitted, avoiding a circular self-hash. These digest scopes are distinct and
documented.

No other preexisting Case 0004 artifact was accessed. No Retrieval query, lane,
rank, score, contribution, retrieved flag, provenance or result artifact was
accessed. Ordinary frozen documentation mentions existing mechanisms; those
mentions are repository evidence, not Case 0004 treatment/results. No Stage D
join or effectiveness metric was computed. Confirmation remains sealed.

The exact next step is **Stage D joined analysis**, under a separate authorized
post-freeze session. This adjudicator stops at the committed Stage C checkpoint
and does not push.
