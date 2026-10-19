# Experiment lifecycle and recovery

Each experiment collection has `SUMMARY.md` and `manifest.json`. The summary
records its scope, result/decision, limitations and reopening rule. Existing
protocols, case reports and analyses remain the exact scientific authorities;
the manifest names and hashes them. Classification is collection-level and
never changes a case's historical result.

Lifecycle values are ACTIVE (authorized work in progress), BLOCKED (a concrete
prerequisite prevents progress), INCOMPLETE (no authenticated consolidated
terminal outcome), CLOSED (the recorded checkpoint has terminated, including a
negative/failed outcome), and REOPENED (a separately identified linked
continuation). No collection is marked ACTIVE merely because executable code
exists. No model operations were launched by consolidation.

Before closing, preserve objective/hypothesis, exact methods/datasets/baselines,
configuration and revision, reproduction commands, outcomes and decision strength,
limitations, unresolved questions and reopening conditions. These may reference
existing authoritative records without duplicating or rewriting them. Never
substitute a generic cleanup description for a missing scientific conclusion.

The current inventory has 35 collections: 24 closed checkpoints, nine incomplete
collections and two blocked collections. Each closed manifest identifies a
compressed local packet under `.local/archives/experiments-2026-10-19/`. Every
packet was physically extracted and every restored member SHA-256 checked.
Packets are local same-SSD recovery, not protection against disk loss. They are
not committed binaries. Keep them when cleaning `.local/`.

Only the 22 obsolete root reports were compacted out of the current tree. Their
original paths/bytes also remain in Git at
`92250292dacfb8289d129063d5523dd87b63162b`; the archive manifest maps their new
packet member names. For example, the packet member
`root-reports/b0002-bm25-address-comparison.json` corresponds to the original
root `.b0002-bm25-address-comparison.json`. Restore packet members into a
disposable data directory and compare against the manifest before use.

Other original research files remain in place because frozen bindings,
cross-experiment dependencies and deterministic replay use their addresses.
The 2.6-GB dogfood collection is INCOMPLETE as a collection: individual final
Stage D reports retain their decisions, while sealed and unfinished records
cannot be collapsed into one success. It has a provenance inventory but no
new compressed packet. Candidate-08 source grounding remains INCOMPLETE after
the C22 pre-entry CLI-preflight log collision; its dead predecessors stay dead.
The shared development population remains BLOCKED for new confirmation work.
The orchestration collection is BLOCKED on reconciling checkout-bound contracts
with canonical-checkout operation. Neither storage restoration nor old approval
presence authorizes retry, confirmation or deployment.

To restore a committed file, use Git's `show <revision>:<original-path>` bytes
or the manifest's packet. For historical executable replay, switch the canonical
checkout to the recorded revision only after preserving current work, restore
required non-Git evidence from the preservation manifest and validate exact
bindings. Removed absolute checkout paths make old operational plans stale;
stop at authentication refusal rather than translating their grants. Reopening
requires an authorized linked continuation retaining the original summary,
manifest, packet and decision. Scientific methods must never be retroactively
changed to make a replay pass.
