# Case 0012 reviewed-gold publication

This final target inherits 4,673 exact source-label agreements and applies all
106 sealed cell verdicts plus the other 42 reconciliation decisions. The sealed
reconciliation is authoritative on disputed propositions. No new adjudication,
reviewer weighting, reliability review or treatment access enters materialization.

[REVIEWED_GOLD.md](REVIEWED_GOLD.md) exposes all positive cells, units, exact support,
witnesses, 32 task combinations, four minimal 14-resource unions, intersections,
gaps, limitations and decision provenance. [reviewed_gold.json](reviewed_gold.json)
also exposes the complete 4,779-cell queryable mapping.

The resource join explicitly compares address, byte_size, content_identity,
document_identity, encoding and text. Its only admitted schema enrichment is the
reconciliation packet's text_sha256: SHA-256 of exact retained text encoded as
UTF-8, without normalization. Exact schema and roster checks reject unrelated
extra fields, omissions, duplicate identities and foreign resources.

The earlier whole-record equality guard was an implementation defect: the blind
schema has six fields and the reconciliation schema seven. Focused tests prove
the corrected join and adversarial rejection. Test invocation uses Python's
module entry point so the repository namespace is available. Draft validation
metadata and builder hashes were resealed after adding coverage assertions and
formatting, with semantic gold/statistics/Markdown bytes checked unchanged.
The draft's source-only limitation additions were removed before publication:
final limitations contain only exact sealed reconciliation decisions and its
decorator-range semantic unit.

Replay without writing:

```text
uv run python -B -m experiments.codex_dogfood.case_0012.adjudication.reviewed.materialize verify
uv run python -B -m pytest -c experiments/codex_dogfood/case_0012/adjudication/reviewed/pytest.ini experiments/codex_dogfood/case_0012/adjudication/reviewed/test_materialize.py
```

Build refuses any existing complete or partial scientific destination. Validation
authenticates the full original blind resource payload at its explicitly sealed
sterile source path; the imported reconciliation builder retains its original
sterile workspace identity and is replayed there. Imported outputs remain byte
identical and are protected from Git text conversion. Source, destination, staged
blob and committed blob equality use physical SHA-256, not Git object IDs.

This is bounded experimental publication tooling, not framework Evaluation,
Resource acquisition or a new persistence contract. Package APIs, architecture,
backlog and historical ledger need no behavior/authority changes. Only case status,
roadmap and documentation-map navigation change. No production source behavior,
confirmation/reserve access, U3, R1.7, BM25F or feature implementation occurs.

Stage D may begin only after this validated target and immutable import are
committed, pushed, and the tracked worktree/index are clean. It must use only the
captured authoritative Stage B attempt. `.local/codex-result.md` is ignored and
excluded from gold, semantics, evidence and scientific hashes.
