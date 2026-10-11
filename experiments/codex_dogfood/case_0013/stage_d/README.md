# Case 0013 Stage D

This evaluation joins the committed reviewed development gold directly to the
authoritative case-0013-stage-b-1 capture. Primary Astra semantics and frozen
Stage A remain unchanged. It calls the existing `gates.evaluate` implementation.

Authentication reads named committed seals, all 73 ENTERED/RETURNED journal
pairs, immutable native bytes, and existing canonical JSON graphs. It never
loads pickle or instantiates native captured types. The graph reader is a
bounded case-local audit codec. No index, query, exact resolution, presentation,
policy, semantic reviewer, reliability comparison or reconciliation is rerun.
Native ContentIdentity is domain-separated semantic identity, not the physical
artifact SHA-256; joins preserve it exactly while bytes use retained UTF-8 text.

Replay: `uv run python -B -m experiments.codex_dogfood.case_0013.stage_d.analysis verify`.
Build is exclusive and refuses existing outputs. Replay reconstructs every
JSON, Markdown and trace byte and authenticates implementation/input hashes.

Focused validation: `uv run python -m pytest -c experiments/codex_dogfood/case_0013/stage_d/pytest.ini experiments/codex_dogfood/case_0013/stage_d`.
Tests independently recalculate all 144 arm/witness depths, prefixes, unions,
owning-label composition and exact UTF-8 bytes, and challenge classifications,
costs, precedence, exact threshold boundaries, stale joins, resealed output
tampering and overwrite refusal. Run scoped Ruff/format and strict mypy on
these case-local Python modules. Protected development validation remains the
production profile; confirmation/reserve and live services are excluded.

The mutable current status is in ../STATUS.md and docs/roadmap.md. Scientific
Stage A/B history stays frozen. No production behavior is changed.
