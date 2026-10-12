# Case 0015 primary import and reviewed publication

The completed GPT-6 Astra / High treatment-blind primary is imported byte-for-byte
in [primary](primary/STAGE_C_REVIEW.md). [IMPORT.json](IMPORT.json) records all
seven physical SHA-256 digests and the separate original packet digest scopes.
The sterile builder's read-only `--verify` passed with exact derived bytes,
unchanged original inputs, and 20 rejected adversarial checks. All 29 excluded
access categories attest NO; second reviewer is false. Scratch is absent and
operational `.local` artifacts are excluded. No reconciliation was performed.

[Reviewed development gold](reviewed/REVIEWED_GOLD.md) contains the entire unchanged
primary object, exact native frame bindings and publication provenance:
PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. It preserves 3,090 judgments,
all rationales/spans, 42 units, 12 minimal witnesses, 32 task combinations,
9 sufficient resource unions, 4 inclusion-minimal unions, 7 indispensable
resources, all 42 indispensable units, gaps, limitations and ambiguity.
O2 has one complete repository-empty witness; it is valid gold.

The deterministic materializer authenticates the original packet separately from
the completed outputs, reuses the immutable primary's structural validator and
support algebra, and rejects every semantic change. Physical serialization uses
exact bytes because the historical text helper normalizes line endings.
Git attributes disable newline conversion for immutable primary/publication files.

```text
python -B experiments/codex_dogfood/case_0015/adjudication/reviewed/materialize.py verify
uv run pytest -c experiments/bm25f/pytest.ini experiments/codex_dogfood/case_0015/adjudication/reviewed -q
```

Publication is representation only. Production behavior is UNCHANGED;
confirmation/reserve NOT_ACCESSED; SEARCH_POLICY_FAILURE NOT_ASSESSED.
Stage D starts only after this checkpoint validates, commits and pushes.
