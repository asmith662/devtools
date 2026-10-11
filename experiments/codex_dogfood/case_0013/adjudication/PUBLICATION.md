# Case 0013 primary and reviewed publication

The completed sterile GPT-6 Astra / High primary adjudication is the sole
semantic source. `primary/` contains seven byte-for-byte immutable scientific
artifacts. `IMPORT.json` records physical seals, original packet authentication,
deterministic replay and all excluded-access attestations. Sterile `.local/`
is excluded. Git attributes disable normalization for imported artifacts.

`reviewed/` retains the entire primary object unchanged and adds only an exact
sealed frame envelope. Provenance is PRIMARY_ASTRA_HIGH; semantic_transformation
is NONE. No reliability comparison, reconciliation or second reviewer occurs.
Statistics, evidence spans, witness minimality, Cartesian combinations and
intersections are recomputed by the authenticated primary invariant functions;
semantic construction is never invoked by this publication layer.

Replay: `uv run python -B -m experiments.codex_dogfood.case_0013.adjudication.reviewed.materialize verify`.
Focused tests: `uv run python -m pytest -c experiments/codex_dogfood/case_0013/adjudication/reviewed/pytest.ini experiments/codex_dogfood/case_0013/adjudication/reviewed`.
Build is exclusive and refuses any existing output. Physical hashes and exact
deterministic output bytes reject tampering. This is development gold only.
