Case 0013 — primary semantic adjudication

MODEL = GPT-6 Astra; REASONING = High. One adjudication with internal self-review.

Exact original task (quoted evidence)

~~~~text
Build a deterministic, inspectable in-memory manifest of an already materialized repository Context disclosure, keeping caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.
Inspect the existing class `devtools.context.planning.materialization.ContextDisclosure` and function `devtools.context.planning.materialization.materialize_disclosure_plan`: preserve exact plan identity, purpose, repository/snapshot applicability, ordered choices, representation names, option identities and the one-item-per-choice contract.
Use the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot. Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest; do not reacquire source, rematerialize choices or silently substitute evidence.
Introduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`. Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.
Provide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records; distinguish total item text bytes from unique supporting-resource bytes. The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.
Inspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged. Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.
Add focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases; retain existing planning, rendering and copied-request regression coverage.
Update the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope. Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.
Inspect the existing file `pyproject.toml` for test, coverage and strict typing constraints; run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.
Operational exclusion: this is a future feature specification for an acquisition experiment. Stage A freezes the experiment only; do not implement the manifest feature, production routing, R1.7, BM25F, sequential search, treatment execution or gold adjudication.
~~~~

Task interpretation and applicability

- C01: ADEQUATELY_REPRESENTED; obligations: structure, manifest, documentation. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C02: ADEQUATELY_REPRESENTED; obligations: structure. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C03: ADEQUATELY_REPRESENTED; obligations: integrity. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C04: ADEQUATELY_REPRESENTED; obligations: structure, manifest. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C05: ADEQUATELY_REPRESENTED; obligations: projection. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C06: ADEQUATELY_REPRESENTED; obligations: compatibility, exports. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C07: ADEQUATELY_REPRESENTED; obligations: tests. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C08: ADEQUATELY_REPRESENTED; obligations: documentation. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C09: ADEQUATELY_REPRESENTED; obligations: validation. All substantive requirements in this clause are represented by the linked obligation statements, satisfaction criteria and authoritative task basis.
- C10: OPERATIONAL_SCIENTIFIC_INSTRUCTION; obligations: none (operational). The final paragraph governs the original experimental operation, not mandatory software feature semantics. It neither cancels the nine prospective feature obligations nor instructs this reviewer to implement software.

Substantive clause audit

- C01.1 [ADEQUATELY_REPRESENTED → structure, manifest, documentation]: Build a deterministic, inspectable in-memory manifest of an already materialized repository Context disclosure, keeping caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.
- C02.1 [ADEQUATELY_REPRESENTED → structure]: Inspect the existing class `devtools.context.planning.materialization.ContextDisclosure` and function `devtools.context.planning.materialization.materialize_disclosure_plan`: preserve exact plan identity, purpose, repository/snapshot applicability, ordered choices, representation names, option identities and the one-item-per-choice contract.
- C03.1 [ADEQUATELY_REPRESENTED → integrity]: Use the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot.
- C03.2 [ADEQUATELY_REPRESENTED → integrity]: Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest;
- C03.3 [ADEQUATELY_REPRESENTED → integrity]: do not reacquire source, rematerialize choices or silently substitute evidence.
- C04.1 [ADEQUATELY_REPRESENTED → structure, manifest]: Introduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`.
- C04.2 [ADEQUATELY_REPRESENTED → structure, manifest]: Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.
- C05.1 [ADEQUATELY_REPRESENTED → projection]: Provide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records;
- C05.2 [ADEQUATELY_REPRESENTED → projection]: distinguish total item text bytes from unique supporting-resource bytes.
- C05.3 [ADEQUATELY_REPRESENTED → projection]: The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.
- C06.1 [ADEQUATELY_REPRESENTED → compatibility, exports]: Inspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged.
- C06.2 [ADEQUATELY_REPRESENTED → compatibility, exports]: Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.
- C07.1 [ADEQUATELY_REPRESENTED → tests]: Add focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases;
- C07.2 [ADEQUATELY_REPRESENTED → tests]: retain existing planning, rendering and copied-request regression coverage.
- C08.1 [ADEQUATELY_REPRESENTED → documentation]: Update the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope.
- C08.2 [ADEQUATELY_REPRESENTED → documentation]: Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.
- C09.1 [ADEQUATELY_REPRESENTED → validation]: Inspect the existing file `pyproject.toml` for test, coverage and strict typing constraints;
- C09.2 [ADEQUATELY_REPRESENTED → validation]: run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.

All nine obligations are APPLICABLE. No exception is asserted.

Complete label counts

| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Witnesses |
|---|---:|---:|---:|---:|
| structure | 3 | 18 | 510 | 2 |
| integrity | 5 | 12 | 514 | 3 |
| manifest | 9 | 17 | 505 | 10 |
| projection | 9 | 15 | 507 | 10 |
| compatibility | 1 | 14 | 516 | 1 |
| exports | 2 | 8 | 521 | 1 |
| tests | 11 | 25 | 495 | 16 |
| documentation | 0 | 16 | 515 | 1 |
| validation | 5 | 1 | 525 | 4 |
| TOTAL | 45 | 126 | 4608 | |

Frame: 531 × 9 = 4779 cells. Full identities, explanations and all negative judgments are in stage_c_review.json.

Complete REQUIRED resource union

- R000: `AGENTS.md`; content identity `096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a`
- R057: `docs/backlog/items/B-0047-protected-development-validation-profile.md`; content identity `68f8e62f69b0daa0dbb7aaca08db787a51e2bb910ae3c21c5c27f8e8ac10f0e6`
- R060: `docs/development/validation.md`; content identity `474b6742cbc1675e8edc369e9319560b2827c013aa2311313e8759ee74e00371`
- R064: `pyproject.toml`; content identity `e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145`
- R065: `scripts/validate_development.py`; content identity `425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5`
- R083: `src/devtools/context/__init__.py`; content identity `e2392c9351df7a0f17f23f2ccd15e3fd1436c4e59eb7e0ee9eb7d0d0c32a445c`
- R120: `src/devtools/context/planning/__init__.py`; content identity `f0a22d1b55645d1c428dd456c527cbe41e36ebbcaab3ca09229498d3e2f7f8d3`
- R122: `src/devtools/context/planning/materialization.py`; content identity `8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315`
- R123: `src/devtools/context/planning/plan.py`; content identity `8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998`
- R124: `src/devtools/context/planning/rendering.py`; content identity `741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7`
- R125: `src/devtools/context/planning/resource.py`; content identity `f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b`
- R140: `src/devtools/context/python/function/planned_reference.py`; content identity `a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381`
- R141: `src/devtools/context/python/function/qualified_reference.py`; content identity `f38207363dcef35c196eac7dd5ab939335e73a9aec507886af7bbdcee7008c69`
- R179: `src/devtools/context/repository/observation.py`; content identity `84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51`
- R180: `src/devtools/context/repository/resource.py`; content identity `a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c`
- R181: `src/devtools/context/repository/snapshot.py`; content identity `492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098`
- R383: `tests/context/planning/test_plan.py`; content identity `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`
- R424: `tests/context/repository/test_observation.py`; content identity `ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016`

Union size: 18. This is the union over alternatives, not simultaneous necessity.

Positive cells by obligation

structure

Preserve exact materialized plan/item structure and native provenance.

Satisfaction criterion: Plan purpose, frame, identities, ordered one-item-per-choice and representations are preserved.

- R000 `AGENTS.md` — HELPFUL_ONLY; units corroboration only. Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.
- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R010 `docs/architecture/taxonomy.md` — HELPFUL_ONLY; units corroboration only. Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.
- R012 `docs/backlog/epics/B-0002-coding-context-substrate.md` — HELPFUL_ONLY; units corroboration only. Backlog context motivates planning boundaries; it is not an exact current API contract.
- R061 `docs/documentation_map.md` — HELPFUL_ONLY; units corroboration only. Documentation navigation summarizes package ownership but does not define an additional necessary feature contract.
- R063 `docs/roadmap.md` — HELPFUL_ONLY; units corroboration only. Current checkpoint corroborates the two supported representations; no additional implementation decision follows.
- R083 `src/devtools/context/__init__.py` — HELPFUL_ONLY; units corroboration only. Public imports corroborate current common names; they do not replace the owning value contracts.
- R120 `src/devtools/context/planning/__init__.py` — HELPFUL_ONLY; units corroboration only. Public facade corroborates current common APIs and convenient imports.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R122 `src/devtools/context/planning/materialization.py` — REQUIRED; units S01, S02, S03, S15. Necessary in at least one complete minimal witness for structure: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout. The manifest consumes the existing disclosure interface and must not presume stronger constructor validation. The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated. Establishes the existing realization operation that inspection must preserve without invoking again.
- R123 `src/devtools/context/planning/plan.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for structure: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R124 `src/devtools/context/planning/rendering.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for structure: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R125 `src/devtools/context/planning/resource.py` — HELPFUL_ONLY; units corroboration only. Concrete whole-resource behavior illustrates representation text and native provenance; a generic manifest consumes the common interface.
- R138 `src/devtools/context/python/function/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Python-specific prose supplies bounded representation context without defining the generic manifest.
- R140 `src/devtools/context/python/function/planned_reference.py` — HELPFUL_ONLY; units corroboration only. Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.
- R141 `src/devtools/context/python/function/qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference validation and materialization provide examples; the manifest authenticates already-materialized common support without repeating semantic derivation.
- R179 `src/devtools/context/repository/observation.py` — HELPFUL_ONLY; units corroboration only. Observation gives bounded-frame context and fixture setup; inspection must not acquire another observation.
- R180 `src/devtools/context/repository/resource.py` — HELPFUL_ONLY; units corroboration only. Native address and identity validation is useful context for malformed fixtures.
- R181 `src/devtools/context/repository/snapshot.py` — HELPFUL_ONLY; units corroboration only. Snapshot storage corroborates applicability; structural preservation can retain the existing plan without independently authenticating support.
- R383 `tests/context/planning/test_plan.py` — HELPFUL_ONLY; units corroboration only. Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.

integrity

Authenticate manifest support against retained native snapshot before publication.

Satisfaction criterion: Foreign stale missing content mismatch and misaligned support are rejected without reacquisition or rematerialization.

- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R004 `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md` — HELPFUL_ONLY; units corroboration only. Broader repository/snapshot identity semantics provide context beyond the precise retained lookup contract.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R122 `src/devtools/context/planning/materialization.py` — REQUIRED; units S01, S02. Necessary in at least one complete minimal witness for integrity: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout. The manifest consumes the existing disclosure interface and must not presume stronger constructor validation.
- R123 `src/devtools/context/planning/plan.py` — HELPFUL_ONLY; units corroboration only. Plan constraints provide defensive test examples and corroborate frame checking; no new plan is constructed by the manifest operation.
- R125 `src/devtools/context/planning/resource.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for integrity: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R140 `src/devtools/context/python/function/planned_reference.py` — HELPFUL_ONLY; units corroboration only. Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.
- R141 `src/devtools/context/python/function/qualified_reference.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for integrity: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R174 `src/devtools/context/repository/__init__.py` — HELPFUL_ONLY; units corroboration only. Repository facade offers convenient access to retained native types.
- R178 `src/devtools/context/repository/identity.py` — HELPFUL_ONLY; units corroboration only. Nominal repository wrapper implementation corroborates identity presentation and supplies fixture constructors.
- R179 `src/devtools/context/repository/observation.py` — HELPFUL_ONLY; units corroboration only. Observation gives bounded-frame context and fixture setup; inspection must not acquire another observation.
- R180 `src/devtools/context/repository/resource.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for integrity: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R181 `src/devtools/context/repository/snapshot.py` — REQUIRED; units S04. Necessary in at least one complete minimal witness for integrity: Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.
- R383 `tests/context/planning/test_plan.py` — HELPFUL_ONLY; units corroboration only. Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.
- R396 `tests/context/python/function/test_qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference tests offer source/target and request fixtures and native behavior examples.
- R424 `tests/context/repository/test_observation.py` — HELPFUL_ONLY; units corroboration only. Observation tests corroborate exact bytes and resource/content identity distinctions.

manifest

Implement the future explicit manifest operation in common Context Planning.

Satisfaction criterion: Every item and repeated support occurrence is correlated with exact resource/content identities, byte counts and native provenance.

- R000 `AGENTS.md` — HELPFUL_ONLY; units corroboration only. Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.
- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R010 `docs/architecture/taxonomy.md` — HELPFUL_ONLY; units corroboration only. Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.
- R012 `docs/backlog/epics/B-0002-coding-context-substrate.md` — HELPFUL_ONLY; units corroboration only. Backlog context motivates planning boundaries; it is not an exact current API contract.
- R061 `docs/documentation_map.md` — HELPFUL_ONLY; units corroboration only. Documentation navigation summarizes package ownership but does not define an additional necessary feature contract.
- R063 `docs/roadmap.md` — HELPFUL_ONLY; units corroboration only. Current checkpoint corroborates the two supported representations; no additional implementation decision follows.
- R083 `src/devtools/context/__init__.py` — HELPFUL_ONLY; units corroboration only. Public imports corroborate current common names; they do not replace the owning value contracts.
- R120 `src/devtools/context/planning/__init__.py` — HELPFUL_ONLY; units corroboration only. Public facade corroborates current common APIs and convenient imports.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R122 `src/devtools/context/planning/materialization.py` — REQUIRED; units S01, S02, S03, S15. Necessary in at least one complete minimal witness for manifest: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout. The manifest consumes the existing disclosure interface and must not presume stronger constructor validation. The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated. Establishes the existing realization operation that inspection must preserve without invoking again.
- R123 `src/devtools/context/planning/plan.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for manifest: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R124 `src/devtools/context/planning/rendering.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for manifest: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R125 `src/devtools/context/planning/resource.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for manifest: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R138 `src/devtools/context/python/function/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Python-specific prose supplies bounded representation context without defining the generic manifest.
- R139 `src/devtools/context/python/function/materialization.py` — HELPFUL_ONLY; units corroboration only. Exact source extraction illustrates byte-column and line-ending fidelity; the manifest consumes already realized text and does not re-extract it.
- R140 `src/devtools/context/python/function/planned_reference.py` — HELPFUL_ONLY; units corroboration only. Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.
- R141 `src/devtools/context/python/function/qualified_reference.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for manifest: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R174 `src/devtools/context/repository/__init__.py` — HELPFUL_ONLY; units corroboration only. Repository facade offers convenient access to retained native types.
- R179 `src/devtools/context/repository/observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for manifest: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R180 `src/devtools/context/repository/resource.py` — REQUIRED; units S05, S14. Necessary in at least one complete minimal witness for manifest: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)). A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R181 `src/devtools/context/repository/snapshot.py` — REQUIRED; units S04. Necessary in at least one complete minimal witness for manifest: Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.
- R383 `tests/context/planning/test_plan.py` — HELPFUL_ONLY; units corroboration only. Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.
- R395 `tests/context/python/function/test_materialization.py` — HELPFUL_ONLY; units corroboration only. Older source-materialization tests illustrate exact bytes and rejection; future inspection must not repeat materialization.
- R396 `tests/context/python/function/test_qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference tests offer source/target and request fixtures and native behavior examples.
- R424 `tests/context/repository/test_observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for manifest: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.

projection

Provide deterministic JSON-compatible presentation and distinct byte accounting.

Satisfaction criterion: Stable fields, exact ordered support, total item bytes versus unique supporting resource bytes and scope limits are established.

- R000 `AGENTS.md` — HELPFUL_ONLY; units corroboration only. Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.
- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R004 `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md` — HELPFUL_ONLY; units corroboration only. Broader repository/snapshot identity semantics provide context beyond the precise retained lookup contract.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R010 `docs/architecture/taxonomy.md` — HELPFUL_ONLY; units corroboration only. Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.
- R028 `docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md` — HELPFUL_ONLY; units corroboration only. Disclosure minimization pressure supplies optional context; no policy engine is requested.
- R037 `docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md` — HELPFUL_ONLY; units corroboration only. Serialization boundary discussion corroborates the distinction between runtime values and durable representations.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R122 `src/devtools/context/planning/materialization.py` — REQUIRED; units S01, S02, S03. Necessary in at least one complete minimal witness for projection: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout. The manifest consumes the existing disclosure interface and must not presume stronger constructor validation. The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R123 `src/devtools/context/planning/plan.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for projection: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R124 `src/devtools/context/planning/rendering.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for projection: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R125 `src/devtools/context/planning/resource.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for projection: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R139 `src/devtools/context/python/function/materialization.py` — HELPFUL_ONLY; units corroboration only. Exact source extraction illustrates byte-column and line-ending fidelity; the manifest consumes already realized text and does not re-extract it.
- R140 `src/devtools/context/python/function/planned_reference.py` — HELPFUL_ONLY; units corroboration only. Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.
- R141 `src/devtools/context/python/function/qualified_reference.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for projection: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R178 `src/devtools/context/repository/identity.py` — HELPFUL_ONLY; units corroboration only. Nominal repository wrapper implementation corroborates identity presentation and supplies fixture constructors.
- R179 `src/devtools/context/repository/observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for projection: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R180 `src/devtools/context/repository/resource.py` — REQUIRED; units S05, S14. Necessary in at least one complete minimal witness for projection: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)). A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R181 `src/devtools/context/repository/snapshot.py` — REQUIRED; units S04. Necessary in at least one complete minimal witness for projection: Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.
- R276 `src/devtools/observability/evidence/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Persistent Evidence ownership provides broader context, already excluded by the task.
- R383 `tests/context/planning/test_plan.py` — HELPFUL_ONLY; units corroboration only. Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.
- R395 `tests/context/python/function/test_materialization.py` — HELPFUL_ONLY; units corroboration only. Older source-materialization tests illustrate exact bytes and rejection; future inspection must not repeat materialization.
- R396 `tests/context/python/function/test_qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference tests offer source/target and request fixtures and native behavior examples.
- R424 `tests/context/repository/test_observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for projection: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.

compatibility

Preserve rendering and copied request assembly.

Satisfaction criterion: Existing output, original request role fields tools settings and task-before-Context assembly remain unchanged.

- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R124 `src/devtools/context/planning/rendering.py` — REQUIRED; units S06, S07. Necessary in at least one complete minimal witness for compatibility: Exact current output compatibility cannot be established solely from a future instruction to leave it unchanged. The exact existing common assembly uses dataclasses.replace; that preserves fields including tools without needing a second complete ModelRequest implementation description.
- R141 `src/devtools/context/python/function/qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference validation and materialization provide examples; the manifest authenticates already-materialized common support without repeating semantic derivation.
- R142 `src/devtools/context/python/function/rendering.py` — HELPFUL_ONLY; units corroboration only. Separate Python renderer is regression context; it does not establish exact common renderer output.
- R143 `src/devtools/context/python/function/request_assembly.py` — HELPFUL_ONLY; units corroboration only. Separate Python assembler corroborates copying semantics but is not proof of the common function body.
- R254 `src/devtools/models/interaction/docs/overview.md` — HELPFUL_ONLY; units corroboration only. ModelInteraction documentation explains request context but is unnecessary to establish replace-only-Prompt behavior.
- R255 `src/devtools/models/interaction/models.py` — HELPFUL_ONLY; units corroboration only. The request field list corroborates what dataclasses.replace preserves; no request schema changes are requested.
- R257 `src/devtools/models/interaction/prompt.py` — HELPFUL_ONLY; units corroboration only. Prompt field declaration corroborates role/content copying.
- R383 `tests/context/planning/test_plan.py` — HELPFUL_ONLY; units corroboration only. Existing mixed and same-resource cases demonstrate faithful order, native preservation and unchanged request behavior. Examples do not establish every negative or exact-output contract.
- R391 `tests/context/python/function/test_cross_resource_pipeline.py` — HELPFUL_ONLY; units corroboration only. Older full pipeline supplies optional regression context across exact source and request assembly.
- R396 `tests/context/python/function/test_qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference tests offer source/target and request fixtures and native behavior examples.
- R397 `tests/context/python/function/test_rendering.py` — HELPFUL_ONLY; units corroboration only. Existing Python rendering assertions are useful regression examples, separate from the common renderer body.
- R398 `tests/context/python/function/test_request_assembly.py` — HELPFUL_ONLY; units corroboration only. Existing Python copied-request tests illustrate preservation but do not define the common operation.

exports

Expose both public facades with existing dependency ownership.

Satisfaction criterion: Common planning and outer Context exports are coherent; no Retrieval dependency or relocation of Python-specific semantics.

- R000 `AGENTS.md` — HELPFUL_ONLY; units corroboration only. Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.
- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R010 `docs/architecture/taxonomy.md` — HELPFUL_ONLY; units corroboration only. Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.
- R061 `docs/documentation_map.md` — HELPFUL_ONLY; units corroboration only. Documentation navigation summarizes package ownership but does not define an additional necessary feature contract.
- R083 `src/devtools/context/__init__.py` — REQUIRED; units S09. Necessary in at least one complete minimal witness for exports: Both outer import binding and explicit public list must be maintained while preserving ownership.
- R120 `src/devtools/context/planning/__init__.py` — REQUIRED; units S08. Necessary in at least one complete minimal witness for exports: Adding a coherent public export needs the actual public enumeration and module ownership, not merely the future destination name.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R133 `src/devtools/context/python/function/__init__.py` — HELPFUL_ONLY; units corroboration only. Python facade gives convenient option imports; common planning exports do not require editing this separate facade.
- R138 `src/devtools/context/python/function/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Python-specific prose supplies bounded representation context without defining the generic manifest.
- R140 `src/devtools/context/python/function/planned_reference.py` — HELPFUL_ONLY; units corroboration only. Python adapter illustrates source/target support and opaque native values. Its internals remain owned by Python; the generic feature need not inspect those internals.

tests

Establish focused and regression coverage for every new and preserved contract.

Satisfaction criterion: Mixed choices duplicate support order UTF-8 CRLF native provenance determinism and all rejection cases plus old regressions are covered.

- R057 `docs/backlog/items/B-0047-protected-development-validation-profile.md` — HELPFUL_ONLY; units corroboration only. Describes the ordinary development test boundary useful for retaining regression checks.
- R060 `docs/development/validation.md` — HELPFUL_ONLY; units corroboration only. The profile documents a convenient way to retain all ordinary regression checks.
- R064 `pyproject.toml` — HELPFUL_ONLY; units corroboration only. Test/static configuration guides implementation quality; its necessity is assigned to the separate validation obligation.
- R065 `scripts/validate_development.py` — HELPFUL_ONLY; units corroboration only. Existing profile is a convenient regression invocation, separate from the new test semantics.
- R083 `src/devtools/context/__init__.py` — HELPFUL_ONLY; units corroboration only. Public imports corroborate current common names; they do not replace the owning value contracts.
- R120 `src/devtools/context/planning/__init__.py` — HELPFUL_ONLY; units corroboration only. Public facade corroborates current common APIs and convenient imports.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R122 `src/devtools/context/planning/materialization.py` — REQUIRED; units S01, S02, S03. Necessary in at least one complete minimal witness for tests: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout. The manifest consumes the existing disclosure interface and must not presume stronger constructor validation. The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R123 `src/devtools/context/planning/plan.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for tests: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R124 `src/devtools/context/planning/rendering.py` — REQUIRED; units S03. Necessary in at least one complete minimal witness for tests: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.
- R125 `src/devtools/context/planning/resource.py` — REQUIRED; units S05, S10. Necessary in at least one complete minimal witness for tests: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)). Mixed-choice tests need the existing representation contract rather than inventing a future substitute option.
- R133 `src/devtools/context/python/function/__init__.py` — HELPFUL_ONLY; units corroboration only. Python facade gives convenient option imports; common planning exports do not require editing this separate facade.
- R138 `src/devtools/context/python/function/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Python-specific prose supplies bounded representation context without defining the generic manifest.
- R139 `src/devtools/context/python/function/materialization.py` — HELPFUL_ONLY; units corroboration only. Exact source extraction illustrates byte-column and line-ending fidelity; the manifest consumes already realized text and does not re-extract it.
- R140 `src/devtools/context/python/function/planned_reference.py` — REQUIRED; units S11. Necessary in at least one complete minimal witness for tests: Tests must cover real existing option semantics; knowing the new test filename is insufficient. Detailed parser internals and fixture construction recipes are implementation conveniences.
- R141 `src/devtools/context/python/function/qualified_reference.py` — REQUIRED; units S05. Necessary in at least one complete minimal witness for tests: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).
- R142 `src/devtools/context/python/function/rendering.py` — HELPFUL_ONLY; units corroboration only. Separate Python renderer is regression context; it does not establish exact common renderer output.
- R143 `src/devtools/context/python/function/request_assembly.py` — HELPFUL_ONLY; units corroboration only. Separate Python assembler corroborates copying semantics but is not proof of the common function body.
- R155 `src/devtools/context/python/modules/interpretation.py` — HELPFUL_ONLY; units corroboration only. Native module-universe construction is useful fixture setup, not a distinct feature acceptance fact.
- R168 `src/devtools/context/python/references/declarations/analysis.py` — HELPFUL_ONLY; units corroboration only. Native analysis construction is useful fixture setup; parser implementation is not a manifest requirement.
- R174 `src/devtools/context/repository/__init__.py` — HELPFUL_ONLY; units corroboration only. Repository facade offers convenient access to retained native types.
- R178 `src/devtools/context/repository/identity.py` — HELPFUL_ONLY; units corroboration only. Nominal repository wrapper implementation corroborates identity presentation and supplies fixture constructors.
- R179 `src/devtools/context/repository/observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for tests: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R180 `src/devtools/context/repository/resource.py` — REQUIRED; units S05, S14. Necessary in at least one complete minimal witness for tests: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)). A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R181 `src/devtools/context/repository/snapshot.py` — REQUIRED; units S04. Necessary in at least one complete minimal witness for tests: Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.
- R254 `src/devtools/models/interaction/docs/overview.md` — HELPFUL_ONLY; units corroboration only. ModelInteraction documentation explains request context but is unnecessary to establish replace-only-Prompt behavior.
- R255 `src/devtools/models/interaction/models.py` — HELPFUL_ONLY; units corroboration only. The request field list corroborates what dataclasses.replace preserves; no request schema changes are requested.
- R257 `src/devtools/models/interaction/prompt.py` — HELPFUL_ONLY; units corroboration only. Prompt field declaration corroborates role/content copying.
- R383 `tests/context/planning/test_plan.py` — REQUIRED; units S10, S11. Necessary in at least one complete minimal witness for tests: Mixed-choice tests need the existing representation contract rather than inventing a future substitute option. Tests must cover real existing option semantics; knowing the new test filename is insufficient. Detailed parser internals and fixture construction recipes are implementation conveniences.
- R391 `tests/context/python/function/test_cross_resource_pipeline.py` — HELPFUL_ONLY; units corroboration only. Older full pipeline supplies optional regression context across exact source and request assembly.
- R395 `tests/context/python/function/test_materialization.py` — HELPFUL_ONLY; units corroboration only. Older source-materialization tests illustrate exact bytes and rejection; future inspection must not repeat materialization.
- R396 `tests/context/python/function/test_qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference tests offer source/target and request fixtures and native behavior examples.
- R397 `tests/context/python/function/test_rendering.py` — HELPFUL_ONLY; units corroboration only. Existing Python rendering assertions are useful regression examples, separate from the common renderer body.
- R398 `tests/context/python/function/test_request_assembly.py` — HELPFUL_ONLY; units corroboration only. Existing Python copied-request tests illustrate preservation but do not define the common operation.
- R424 `tests/context/repository/test_observation.py` — REQUIRED; units S14. Necessary in at least one complete minimal witness for tests: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.
- R524 `tests/scripts/test_validate_development.py` — HELPFUL_ONLY; units corroboration only. Profile tests corroborate the command and exclusion but do not assert the complete argument list; they cannot independently establish that no configuration override is supplied.

documentation

Explain manifest fidelity applicability and limits in existing package documentation.

Satisfaction criterion: Byte accounting, non-persistence, no automatic selection, sufficiency or disclosure authority are documented.

- R000 `AGENTS.md` — HELPFUL_ONLY; units corroboration only. Broader ownership and persistence distinctions corroborate the task boundary; they do not define the new operation.
- R002 `docs/architecture.md` — HELPFUL_ONLY; units corroboration only. Architecture summarizes the two current representations and their realization boundary but does not supply all exact current interfaces.
- R004 `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md` — HELPFUL_ONLY; units corroboration only. Broader repository/snapshot identity semantics provide context beyond the precise retained lookup contract.
- R006 `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md` — HELPFUL_ONLY; units corroboration only. Disclosure and assembly architecture corroborates scope and semantic-strength limits already prescribed by the task.
- R010 `docs/architecture/taxonomy.md` — HELPFUL_ONLY; units corroboration only. Taxonomy corroborates caller-directed planning and limits on sufficiency and comprehension.
- R012 `docs/backlog/epics/B-0002-coding-context-substrate.md` — HELPFUL_ONLY; units corroboration only. Backlog context motivates planning boundaries; it is not an exact current API contract.
- R028 `docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md` — HELPFUL_ONLY; units corroboration only. Disclosure minimization pressure supplies optional context; no policy engine is requested.
- R037 `docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md` — HELPFUL_ONLY; units corroboration only. Serialization boundary discussion corroborates the distinction between runtime values and durable representations.
- R061 `docs/documentation_map.md` — HELPFUL_ONLY; units corroboration only. Documentation navigation summarizes package ownership but does not define an additional necessary feature contract.
- R063 `docs/roadmap.md` — HELPFUL_ONLY; units corroboration only. Current checkpoint corroborates the two supported representations; no additional implementation decision follows.
- R121 `src/devtools/context/planning/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Package prose describes existing boundaries and is useful editing context; new documentation requirements are already task-backed and precise implementation fields need their current contracts.
- R138 `src/devtools/context/python/function/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Python-specific prose supplies bounded representation context without defining the generic manifest.
- R141 `src/devtools/context/python/function/qualified_reference.py` — HELPFUL_ONLY; units corroboration only. Qualified-reference validation and materialization provide examples; the manifest authenticates already-materialized common support without repeating semantic derivation.
- R179 `src/devtools/context/repository/observation.py` — HELPFUL_ONLY; units corroboration only. Observation gives bounded-frame context and fixture setup; inspection must not acquire another observation.
- R276 `src/devtools/observability/evidence/docs/overview.md` — HELPFUL_ONLY; units corroboration only. Persistent Evidence ownership provides broader context, already excluded by the task.
- R424 `tests/context/repository/test_observation.py` — HELPFUL_ONLY; units corroboration only. Observation tests corroborate exact bytes and resource/content identity distinctions.

validation

Preserve the protected development and static validation contract.

Satisfaction criterion: Protected profile coverage strict mypy Ruff format worktree/index checks and restricted/live boundaries are established.

- R000 `AGENTS.md` — REQUIRED; units S13. Necessary in at least one complete minimal witness for validation: The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.
- R057 `docs/backlog/items/B-0047-protected-development-validation-profile.md` — REQUIRED; units S13. Necessary in at least one complete minimal witness for validation: The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.
- R060 `docs/development/validation.md` — REQUIRED; units S13. Necessary in at least one complete minimal witness for validation: The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.
- R064 `pyproject.toml` — REQUIRED; units S12, S16, S17. Necessary in at least one complete minimal witness for validation: The configured test/coverage gate must remain intact. Static and formatting checks must use the actual configured policy. The future change must satisfy the existing strict type-checking scope.
- R065 `scripts/validate_development.py` — REQUIRED; units S13. Necessary in at least one complete minimal witness for validation: The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.
- R524 `tests/scripts/test_validate_development.py` — HELPFUL_ONLY; units corroboration only. Profile tests corroborate the command and exclusion but do not assert the complete argument list; they cannot independently establish that no configuration override is supplied.

Complete semantic-unit inventory

49 units: 32 task-backed; 17 repository-supported; 0 mixed.

T01 — TASK_BACKED — structure, manifest

Build a deterministic inspectable in-memory description of an already materialized disclosure.

Necessity: Defines the object being described and its lifecycle boundary.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [0:230].

T02 — TASK_BACKED — structure, manifest

Preserve exact plan identity, caller purpose and repository/snapshot applicability.

Necessity: Changing these would describe a different decision or frame.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [230:574].

T03 — TASK_BACKED — structure, manifest

Preserve ordered choices, representation names, option identities and one item per choice.

Necessity: Defines item correspondence and order fidelity.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [230:574].

T04 — TASK_BACKED — integrity

Reject foreign repository and stale snapshot frames before publishing a manifest.

Necessity: Applicability failures cannot be presented as an authenticated manifest.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [574:980].

T05 — TASK_BACKED — integrity

Reject missing resources, content-identity mismatch and misaligned address/content pairs before publication.

Necessity: An ordered support pair must authenticate as that exact addressed occurrence.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [574:980].

T06 — TASK_BACKED — integrity, manifest

Use retained snapshot resource_at; do not reacquire source, rematerialize choices or silently substitute evidence.

Necessity: The requested operation describes an existing realization against retained state.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [574:980].

T07 — TASK_BACKED — manifest

Add ContextDisclosureManifest and describe_context_disclosure in the new common planning manifest.py destination.

Necessity: The new public operation and destination are explicitly prescribed, without asserting their prior existence.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [980:1458].

T08 — TASK_BACKED — structure, manifest, projection

Retain every item and every repeated support occurrence in plan order, correlating exact address/content identity pairs.

Necessity: Set conversion or independent ordering of support arrays would lose the requested account.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [980:1458].
Task [1458:1829].

T09 — TASK_BACKED — manifest, projection

Count exact UTF-8 text bytes without normalizing non-ASCII text or line endings.

Necessity: Byte counts must describe the retained text, including non-ASCII and CRLF cases.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [980:1458].
Task [2167:2513].

T10 — TASK_BACKED — structure, manifest, projection

Retain original native provenance as native values; do not serialize arbitrary provenance objects.

Necessity: Opaque native values must survive the in-memory operation without a fabricated universal schema.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [980:1458].

T11 — TASK_BACKED — projection

Provide deterministic JSON-compatible fields with stable explicit identities and exact ordered support records.

Necessity: Presentation must remain inspectable and deterministic independently of arbitrary object repr output.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1458:1829].

T12 — TASK_BACKED — projection

Distinguish the sum of item text byte counts from bytes of unique supporting resources.

Necessity: Item representation text and distinct retained source occurrences are different accounting domains.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1458:1829].

T13 — TASK_BACKED — projection, documentation

The projection is derived presentation, not a durable wire schema, new repository fact, source-export authority, budget policy or sufficiency claim.

Necessity: Bounds the semantic strength and persistence meaning of the result.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1458:1829].

T14 — TASK_BACKED — compatibility

Preserve existing rendering and copied ModelRequest assembly.

Necessity: The added inspection operation must leave existing consumer-visible behavior intact.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1829:2167].

T15 — TASK_BACKED — exports

Expose the manifest operation through the common planning and outer Context public facades.

Necessity: Both specified public entry boundaries must expose the operation.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1829:2167].

T16 — TASK_BACKED — exports

Keep the new common operation independent of the task-excluded selection subsystem.

Necessity: The common manifest must obey the explicitly prescribed dependency boundary.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1829:2167].

T17 — TASK_BACKED — tests

Add tests/context/planning/test_manifest.py exercising mixed existing whole-resource and qualified-reference choices.

Necessity: The tests must cover both existing representations in one disclosure.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T18 — TASK_BACKED — tests

Cover duplicate support and order independently of identical-choice duplication.

Necessity: Support multiplicity is an explicit fidelity requirement.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T19 — TASK_BACKED — tests

Test exact non-ASCII and CRLF byte accounting.

Necessity: UTF-8 length and line-ending fidelity need acceptance coverage.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T20 — TASK_BACKED — tests

Retain existing planning, rendering and copied-request regression coverage.

Necessity: Adding focused coverage must preserve the established regression boundary.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T21 — TASK_BACKED — documentation

Update the existing planning overview with fidelity, applicability, byte accounting and non-persistence scope.

Necessity: The task specifies the document and required future content; its current wording is contextual rather than an additional fact needed to restate these requirements.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2513:2858].

T22 — TASK_BACKED — documentation

Explain why a complete manifest establishes neither task completeness nor model comprehension.

Necessity: A complete account of supplied material cannot certify adequacy or consumer understanding.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2513:2858].

T23 — TASK_BACKED — documentation

Explain why the manifest does not authorize disclosure or implement automatic Context planning.

Necessity: The documentation must separate inspection from authority and autonomous selection.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2513:2858].

T24 — TASK_BACKED — structure, manifest, documentation

Keep caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.

Necessity: The inspection feature must not acquire these independent responsibilities.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [0:230].

T25 — TASK_BACKED — validation

Inspect the existing pyproject.toml test, coverage and strict typing constraints.

Necessity: The task requires current configured facts rather than assumed defaults.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2858:3150].

T26 — TASK_BACKED — exports

Retain Python-specific provenance ownership rather than relocating it into common planning.

Necessity: Preserving an opaque native object does not authorize moving its language-specific semantics.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [1829:2167].

T27 — TASK_BACKED — tests

Test exact native provenance preservation.

Necessity: Value/object fidelity is distinct from equivalent rendered text.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T28 — TASK_BACKED — tests

Test deterministic JSON-compatible projection.

Necessity: Repeated presentation of unchanged inputs must remain equal and JSON compatible.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T29 — TASK_BACKED — tests

Test every requested authentication rejection case.

Necessity: Each foreign, stale, missing, content-mismatched and misaligned case must fail before publication.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2167:2513].

T30 — TASK_BACKED — validation

Run the protected development validation profile.

Necessity: The future implementation must pass the designated ordinary test boundary.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2858:3150].

T31 — TASK_BACKED — validation

Run Ruff, formatting, strict mypy and worktree/index diff checks.

Necessity: The future implementation must pass the separate static and change-integrity gates.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2858:3150].

T32 — TASK_BACKED — validation

Do not weaken configuration or run the task-excluded restricted, live-model or Docker validation.

Necessity: The desired validation process has explicit preservation and execution boundaries.

Assumptions: A desired future behavior is prescribed here; this unit asserts no existing implementation.

Task [2858:3150].

S01 — REPOSITORY_SUPPORTED — structure, integrity, manifest, projection, tests

A materialized item exposes option_identity, representation, resource_addresses, content_identities, text and opaque object-valued native_provenance; the two support tuples are separate fields.

Necessity: The manifest must read the actual materialized interface and validate aligned pairs; the task does not supply the current field layout.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R122); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S02 — REPOSITORY_SUPPORTED — structure, integrity, manifest, projection, tests

ContextDisclosure retains plan and ordered items and rejects cardinality/option/representation disagreement; it does not check support-tuple alignment.

Necessity: The manifest consumes the existing disclosure interface and must not presume stronger constructor validation.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R122); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S03 — REPOSITORY_SUPPORTED — structure, manifest, projection, tests

The existing plan surface provides purpose, repository_id, snapshot_id, ordered disclosures and identity; these are available on the retained plan without recomputing a new plan.

Necessity: The task prescribes preservation but does not define current attribute names. The digest algorithm and lineage serialization need not be duplicated.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R123); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R122, R124); INFERABLE. Materialization reads repository_id, snapshot_id and disclosures; rendering reads purpose and identity. Together these establish the same required plan surface; neither alone does.

S04 — REPOSITORY_SUPPORTED — integrity, manifest, projection, tests

RepositorySnapshot exposes id, repository_id and retained resources; resource_at returns the occurrence at exact address equality and raises ValueError when missing.

Necessity: Authentication must use the actual retained lookup and failure contract, not a guessed lookup or filesystem read.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R181); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S05 — REPOSITORY_SUPPORTED — integrity, manifest, projection, tests

The retained occurrence surface exposes address, content_identity and exact content text; the current identity/address presentation is string-compatible.

Necessity: Source byte accounting and identity comparison require the actual retained occurrence surface. Native byte_size metadata need not be trusted in place of len(content.encode(utf-8)).

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R180); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R125); INFERABLE. The existing consumer reads and formats address/content_identity/content from resource_at output, establishing the needed surface without needing every occurrence constructor field.
Alternative 3: ALL(R141); INFERABLE. The existing consumer reads retained content and content identities and presents source/target addresses and identities as strings. Its occurrence equality checks bind these values to the addressed retained resources.

S06 — REPOSITORY_SUPPORTED — compatibility

The current common renderer emits its fixed header and purpose/plan/snapshot/item fields, then each item option/representation/text in enumeration order, retaining the original disclosure.

Necessity: Exact current output compatibility cannot be established solely from a future instruction to leave it unchanged.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R124); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S07 — REPOSITORY_SUPPORTED — compatibility

The common request assembler preserves unchanged task text before unchanged context, reports both UTF-8 lengths and replaces only Prompt content while retaining its role and every other ModelRequest field.

Necessity: The exact existing common assembly uses dataclasses.replace; that preserves fields including tools without needing a second complete ModelRequest implementation description.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R124); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S08 — REPOSITORY_SUPPORTED — exports

The common planning facade uses explicit imports from its owned modules and an explicit __all__ containing its public planning operations and values.

Necessity: Adding a coherent public export needs the actual public enumeration and module ownership, not merely the future destination name.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R120); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S09 — REPOSITORY_SUPPORTED — exports

The outer Context facade imports common planning names from the planning package and separately exposes them in its explicit __all__; Python function APIs have a separate import owner.

Necessity: Both outer import binding and explicit public list must be maintained while preserving ownership.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R083); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S10 — REPOSITORY_SUPPORTED — tests

The existing whole-resource choice is created for a purpose, snapshot and resource address, materializes retained source into one common item, and carries the retained resource as native provenance.

Necessity: Mixed-choice tests need the existing representation contract rather than inventing a future substitute option.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R125); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R383); INFERABLE. The executable example supplies the public constructor call, common materialization and an identity assertion for whole.resource provenance.

S11 — REPOSITORY_SUPPORTED — tests

The existing qualified-reference option accepts an explicit purpose plus native analysis/reference, participates in a common plan, and produces ordered source/target support, which may repeat one address.

Necessity: Tests must cover real existing option semantics; knowing the new test filename is insufficient. Detailed parser internals and fixture construction recipes are implementation conveniences.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R140); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R383); INFERABLE. The fixture and tests establish the same public option integration and ordered support contract, including repeated same-resource support. No stronger Python meaning or provenance serializer is inferred.

S12 — REPOSITORY_SUPPORTED — validation

Current pytest configuration enables strict config/markers and devtools branch coverage with a 100% threshold.

Necessity: The configured test/coverage gate must remain intact.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R064); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S13 — REPOSITORY_SUPPORTED — validation

The protected development profile runs tests/ while excluding tests/experiments/ before recursive collection, keeps project options and coverage, and is invoked through scripts/validate_development.py.

Necessity: The task names a protected profile but does not define its implementation or command. Equivalent direct documentation and executable contracts are alternatives.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R060); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R065); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 3: ALL(R057); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 4: ALL(R000); INFERABLE. The operating guide gives the command, exclusion before collection and preserved branch gate; the configured project contract supplies the remaining current settings.

S14 — REPOSITORY_SUPPORTED — manifest, projection, tests

Addressed resource occurrence and content identity are distinct: equal text at two different addresses remains two resource occurrences; unique supporting-resource bytes must preserve that distinction.

Necessity: A set of content hashes would undercount unique resources when different addresses share text. Within one authenticated frame, address or address/content pair denotes the occurrence.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R180); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.
Alternative 2: ALL(R179); INFERABLE. Content identity is computed only from decoded text, while snapshot membership separately stores each requested address; equal content therefore does not collapse addressed occurrences.
Alternative 3: ALL(R424); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S15 — REPOSITORY_SUPPORTED — structure, manifest

materialize_disclosure_plan checks repository/snapshot applicability, materializes each planned choice once in order, and rejects changed option identity or representation.

Necessity: Establishes the existing realization operation that inspection must preserve without invoking again.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R122); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S16 — REPOSITORY_SUPPORTED — validation

Current Ruff configuration targets Python 3.12, an 88-column line length and ALL rules with D203/D213 and test S101 exceptions.

Necessity: Static and formatting checks must use the actual configured policy.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R064); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

S17 — REPOSITORY_SUPPORTED — validation

Current mypy is strict for Python 3.12, covers src/tests/experiments, and uses explicit package bases and src on mypy_path.

Necessity: The future change must satisfy the existing strict type-checking scope.

Assumptions: Ordinary Python language semantics are assumed. A witness supplies necessary semantic contracts, not every transitive implementation or an executable implementation recipe.

Alternative 1: ALL(R064); DIRECT. The exact retained declarations establish the stated interface and behavior. No execution result is inferred.

Complete minimal obligation witnesses

All listed units and resources within a witness are jointly required. Any listed witness for that obligation substitutes for another. Unit evidence alternatives that use already-required resources do not create duplicate resource witnesses.

structure

Required units: S01, S02, S03, S15, T01, T02, T03, T08, T10, T24

- structure:W1: ALL(resources: R122, R123; units: S01, S02, S03, S15, T01, T02, T03, T08, T10, T24).
- structure:W2: ALL(resources: R122, R124; units: S01, S02, S03, S15, T01, T02, T03, T08, T10, T24).

Obligation-indispensable resources: R122

Obligation-indispensable units: S01, S02, S03, S15, T01, T02, T03, T08, T10, T24

integrity

Required units: S01, S02, S04, S05, T04, T05, T06

- integrity:W1: ALL(resources: R122, R125, R181; units: S01, S02, S04, S05, T04, T05, T06).
- integrity:W2: ALL(resources: R122, R141, R181; units: S01, S02, S04, S05, T04, T05, T06).
- integrity:W3: ALL(resources: R122, R180, R181; units: S01, S02, S04, S05, T04, T05, T06).

Obligation-indispensable resources: R122, R181

Obligation-indispensable units: S01, S02, S04, S05, T04, T05, T06

manifest

Required units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24

- manifest:W1: ALL(resources: R122, R123, R180, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W2: ALL(resources: R122, R124, R180, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W3: ALL(resources: R122, R123, R125, R179, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W4: ALL(resources: R122, R123, R125, R181, R424; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W5: ALL(resources: R122, R123, R141, R179, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W6: ALL(resources: R122, R123, R141, R181, R424; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W7: ALL(resources: R122, R124, R125, R179, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W8: ALL(resources: R122, R124, R125, R181, R424; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W9: ALL(resources: R122, R124, R141, R179, R181; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).
- manifest:W10: ALL(resources: R122, R124, R141, R181, R424; units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24).

Obligation-indispensable resources: R122, R181

Obligation-indispensable units: S01, S02, S03, S04, S05, S14, S15, T01, T02, T03, T06, T07, T08, T09, T10, T24

projection

Required units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13

- projection:W1: ALL(resources: R122, R123, R180, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W2: ALL(resources: R122, R124, R180, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W3: ALL(resources: R122, R123, R125, R179, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W4: ALL(resources: R122, R123, R125, R181, R424; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W5: ALL(resources: R122, R123, R141, R179, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W6: ALL(resources: R122, R123, R141, R181, R424; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W7: ALL(resources: R122, R124, R125, R179, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W8: ALL(resources: R122, R124, R125, R181, R424; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W9: ALL(resources: R122, R124, R141, R179, R181; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).
- projection:W10: ALL(resources: R122, R124, R141, R181, R424; units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13).

Obligation-indispensable resources: R122, R181

Obligation-indispensable units: S01, S02, S03, S04, S05, S14, T08, T09, T10, T11, T12, T13

compatibility

Required units: S06, S07, T14

- compatibility:W1: ALL(resources: R124; units: S06, S07, T14).

Obligation-indispensable resources: R124

Obligation-indispensable units: S06, S07, T14

exports

Required units: S08, S09, T15, T16, T26

- exports:W1: ALL(resources: R083, R120; units: S08, S09, T15, T16, T26).

Obligation-indispensable resources: R083, R120

Obligation-indispensable units: S08, S09, T15, T16, T26

tests

Required units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29

- tests:W1: ALL(resources: R122, R123, R180, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W2: ALL(resources: R122, R124, R180, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W3: ALL(resources: R122, R123, R125, R140, R179, R181; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W4: ALL(resources: R122, R123, R125, R140, R180, R181; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W5: ALL(resources: R122, R123, R125, R140, R181, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W6: ALL(resources: R122, R123, R125, R179, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W7: ALL(resources: R122, R123, R125, R181, R383, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W8: ALL(resources: R122, R123, R141, R179, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W9: ALL(resources: R122, R123, R141, R181, R383, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W10: ALL(resources: R122, R124, R125, R140, R179, R181; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W11: ALL(resources: R122, R124, R125, R140, R180, R181; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W12: ALL(resources: R122, R124, R125, R140, R181, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W13: ALL(resources: R122, R124, R125, R179, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W14: ALL(resources: R122, R124, R125, R181, R383, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W15: ALL(resources: R122, R124, R141, R179, R181, R383; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).
- tests:W16: ALL(resources: R122, R124, R141, R181, R383, R424; units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29).

Obligation-indispensable resources: R122, R181

Obligation-indispensable units: S01, S02, S03, S04, S05, S10, S11, S14, T17, T18, T19, T20, T27, T28, T29

documentation

Required units: T13, T21, T22, T23, T24

- documentation:W1: ALL(resources: empty; units: T13, T21, T22, T23, T24).

Obligation-indispensable resources: none

Obligation-indispensable units: T13, T21, T22, T23, T24

validation

Required units: S12, S13, S16, S17, T25, T30, T31, T32

- validation:W1: ALL(resources: R000, R064; units: S12, S13, S16, S17, T25, T30, T31, T32).
- validation:W2: ALL(resources: R057, R064; units: S12, S13, S16, S17, T25, T30, T31, T32).
- validation:W3: ALL(resources: R060, R064; units: S12, S13, S16, S17, T25, T30, T31, T32).
- validation:W4: ALL(resources: R064, R065; units: S12, S13, S16, S17, T25, T30, T31, T32).

Obligation-indispensable resources: R064

Obligation-indispensable units: S12, S13, S16, S17, T25, T30, T31, T32

Complete task combinations

The exact finite product below denotes every complete combination, without imposing an order of resource use. Every tuple is additionally enumerated in the JSON complete_combinations array.

{structure:W1, structure:W2} × {integrity:W1, integrity:W2, integrity:W3} × {manifest:W1, manifest:W2, manifest:W3, manifest:W4, manifest:W5, manifest:W6, manifest:W7, manifest:W8, manifest:W9, manifest:W10} × {projection:W1, projection:W2, projection:W3, projection:W4, projection:W5, projection:W6, projection:W7, projection:W8, projection:W9, projection:W10} × {compatibility:W1} × {exports:W1} × {tests:W1, tests:W2, tests:W3, tests:W4, tests:W5, tests:W6, tests:W7, tests:W8, tests:W9, tests:W10, tests:W11, tests:W12, tests:W13, tests:W14, tests:W15, tests:W16} × {documentation:W1} × {validation:W1, validation:W2, validation:W3, validation:W4}

Count: 38400 = 2 × 3 × 10 × 10 × 1 × 1 × 16 × 1 × 4.

Distinct sufficient repository-resource unions

280 distinct unions; resource-count range 9–14. Complete inventory follows.

- RU0001 (9): R000, R064, R083, R120, R122, R124, R180, R181, R383
- RU0002 (9): R057, R064, R083, R120, R122, R124, R180, R181, R383
- RU0003 (9): R060, R064, R083, R120, R122, R124, R180, R181, R383
- RU0004 (9): R064, R065, R083, R120, R122, R124, R180, R181, R383
- RU0005 (10): R000, R064, R083, R120, R122, R123, R124, R180, R181, R383
- RU0006 (10): R000, R064, R083, R120, R122, R124, R125, R140, R179, R181
- RU0007 (10): R000, R064, R083, R120, R122, R124, R125, R140, R180, R181
- RU0008 (10): R000, R064, R083, R120, R122, R124, R125, R140, R181, R424
- RU0009 (10): R000, R064, R083, R120, R122, R124, R125, R179, R181, R383
- RU0010 (10): R000, R064, R083, R120, R122, R124, R125, R180, R181, R383
- RU0011 (10): R000, R064, R083, R120, R122, R124, R125, R181, R383, R424
- RU0012 (10): R000, R064, R083, R120, R122, R124, R141, R179, R181, R383
- RU0013 (10): R000, R064, R083, R120, R122, R124, R141, R180, R181, R383
- RU0014 (10): R000, R064, R083, R120, R122, R124, R141, R181, R383, R424
- RU0015 (10): R057, R064, R083, R120, R122, R123, R124, R180, R181, R383
- RU0016 (10): R057, R064, R083, R120, R122, R124, R125, R140, R179, R181
- RU0017 (10): R057, R064, R083, R120, R122, R124, R125, R140, R180, R181
- RU0018 (10): R057, R064, R083, R120, R122, R124, R125, R140, R181, R424
- RU0019 (10): R057, R064, R083, R120, R122, R124, R125, R179, R181, R383
- RU0020 (10): R057, R064, R083, R120, R122, R124, R125, R180, R181, R383
- RU0021 (10): R057, R064, R083, R120, R122, R124, R125, R181, R383, R424
- RU0022 (10): R057, R064, R083, R120, R122, R124, R141, R179, R181, R383
- RU0023 (10): R057, R064, R083, R120, R122, R124, R141, R180, R181, R383
- RU0024 (10): R057, R064, R083, R120, R122, R124, R141, R181, R383, R424
- RU0025 (10): R060, R064, R083, R120, R122, R123, R124, R180, R181, R383
- RU0026 (10): R060, R064, R083, R120, R122, R124, R125, R140, R179, R181
- RU0027 (10): R060, R064, R083, R120, R122, R124, R125, R140, R180, R181
- RU0028 (10): R060, R064, R083, R120, R122, R124, R125, R140, R181, R424
- RU0029 (10): R060, R064, R083, R120, R122, R124, R125, R179, R181, R383
- RU0030 (10): R060, R064, R083, R120, R122, R124, R125, R180, R181, R383
- RU0031 (10): R060, R064, R083, R120, R122, R124, R125, R181, R383, R424
- RU0032 (10): R060, R064, R083, R120, R122, R124, R141, R179, R181, R383
- RU0033 (10): R060, R064, R083, R120, R122, R124, R141, R180, R181, R383
- RU0034 (10): R060, R064, R083, R120, R122, R124, R141, R181, R383, R424
- RU0035 (10): R064, R065, R083, R120, R122, R123, R124, R180, R181, R383
- RU0036 (10): R064, R065, R083, R120, R122, R124, R125, R140, R179, R181
- RU0037 (10): R064, R065, R083, R120, R122, R124, R125, R140, R180, R181
- RU0038 (10): R064, R065, R083, R120, R122, R124, R125, R140, R181, R424
- RU0039 (10): R064, R065, R083, R120, R122, R124, R125, R179, R181, R383
- RU0040 (10): R064, R065, R083, R120, R122, R124, R125, R180, R181, R383
- RU0041 (10): R064, R065, R083, R120, R122, R124, R125, R181, R383, R424
- RU0042 (10): R064, R065, R083, R120, R122, R124, R141, R179, R181, R383
- RU0043 (10): R064, R065, R083, R120, R122, R124, R141, R180, R181, R383
- RU0044 (10): R064, R065, R083, R120, R122, R124, R141, R181, R383, R424
- RU0045 (11): R000, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181
- RU0046 (11): R000, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181
- RU0047 (11): R000, R064, R083, R120, R122, R123, R124, R125, R140, R181, R424
- RU0048 (11): R000, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383
- RU0049 (11): R000, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383
- RU0050 (11): R000, R064, R083, R120, R122, R123, R124, R125, R181, R383, R424
- RU0051 (11): R000, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383
- RU0052 (11): R000, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383
- RU0053 (11): R000, R064, R083, R120, R122, R123, R124, R141, R181, R383, R424
- RU0054 (11): R000, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181
- RU0055 (11): R000, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181
- RU0056 (11): R000, R064, R083, R120, R122, R124, R125, R140, R141, R181, R424
- RU0057 (11): R000, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181
- RU0058 (11): R000, R064, R083, R120, R122, R124, R125, R140, R179, R181, R424
- RU0059 (11): R000, R064, R083, R120, R122, R124, R125, R140, R180, R181, R424
- RU0060 (11): R000, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383
- RU0061 (11): R000, R064, R083, R120, R122, R124, R125, R141, R181, R383, R424
- RU0062 (11): R000, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383
- RU0063 (11): R000, R064, R083, R120, R122, R124, R125, R179, R181, R383, R424
- RU0064 (11): R000, R064, R083, R120, R122, R124, R125, R180, R181, R383, R424
- RU0065 (11): R000, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383
- RU0066 (11): R000, R064, R083, R120, R122, R124, R141, R179, R181, R383, R424
- RU0067 (11): R000, R064, R083, R120, R122, R124, R141, R180, R181, R383, R424
- RU0068 (11): R057, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181
- RU0069 (11): R057, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181
- RU0070 (11): R057, R064, R083, R120, R122, R123, R124, R125, R140, R181, R424
- RU0071 (11): R057, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383
- RU0072 (11): R057, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383
- RU0073 (11): R057, R064, R083, R120, R122, R123, R124, R125, R181, R383, R424
- RU0074 (11): R057, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383
- RU0075 (11): R057, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383
- RU0076 (11): R057, R064, R083, R120, R122, R123, R124, R141, R181, R383, R424
- RU0077 (11): R057, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181
- RU0078 (11): R057, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181
- RU0079 (11): R057, R064, R083, R120, R122, R124, R125, R140, R141, R181, R424
- RU0080 (11): R057, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181
- RU0081 (11): R057, R064, R083, R120, R122, R124, R125, R140, R179, R181, R424
- RU0082 (11): R057, R064, R083, R120, R122, R124, R125, R140, R180, R181, R424
- RU0083 (11): R057, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383
- RU0084 (11): R057, R064, R083, R120, R122, R124, R125, R141, R181, R383, R424
- RU0085 (11): R057, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383
- RU0086 (11): R057, R064, R083, R120, R122, R124, R125, R179, R181, R383, R424
- RU0087 (11): R057, R064, R083, R120, R122, R124, R125, R180, R181, R383, R424
- RU0088 (11): R057, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383
- RU0089 (11): R057, R064, R083, R120, R122, R124, R141, R179, R181, R383, R424
- RU0090 (11): R057, R064, R083, R120, R122, R124, R141, R180, R181, R383, R424
- RU0091 (11): R060, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181
- RU0092 (11): R060, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181
- RU0093 (11): R060, R064, R083, R120, R122, R123, R124, R125, R140, R181, R424
- RU0094 (11): R060, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383
- RU0095 (11): R060, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383
- RU0096 (11): R060, R064, R083, R120, R122, R123, R124, R125, R181, R383, R424
- RU0097 (11): R060, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383
- RU0098 (11): R060, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383
- RU0099 (11): R060, R064, R083, R120, R122, R123, R124, R141, R181, R383, R424
- RU0100 (11): R060, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181
- RU0101 (11): R060, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181
- RU0102 (11): R060, R064, R083, R120, R122, R124, R125, R140, R141, R181, R424
- RU0103 (11): R060, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181
- RU0104 (11): R060, R064, R083, R120, R122, R124, R125, R140, R179, R181, R424
- RU0105 (11): R060, R064, R083, R120, R122, R124, R125, R140, R180, R181, R424
- RU0106 (11): R060, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383
- RU0107 (11): R060, R064, R083, R120, R122, R124, R125, R141, R181, R383, R424
- RU0108 (11): R060, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383
- RU0109 (11): R060, R064, R083, R120, R122, R124, R125, R179, R181, R383, R424
- RU0110 (11): R060, R064, R083, R120, R122, R124, R125, R180, R181, R383, R424
- RU0111 (11): R060, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383
- RU0112 (11): R060, R064, R083, R120, R122, R124, R141, R179, R181, R383, R424
- RU0113 (11): R060, R064, R083, R120, R122, R124, R141, R180, R181, R383, R424
- RU0114 (11): R064, R065, R083, R120, R122, R123, R124, R125, R140, R179, R181
- RU0115 (11): R064, R065, R083, R120, R122, R123, R124, R125, R140, R180, R181
- RU0116 (11): R064, R065, R083, R120, R122, R123, R124, R125, R140, R181, R424
- RU0117 (11): R064, R065, R083, R120, R122, R123, R124, R125, R179, R181, R383
- RU0118 (11): R064, R065, R083, R120, R122, R123, R124, R125, R180, R181, R383
- RU0119 (11): R064, R065, R083, R120, R122, R123, R124, R125, R181, R383, R424
- RU0120 (11): R064, R065, R083, R120, R122, R123, R124, R141, R179, R181, R383
- RU0121 (11): R064, R065, R083, R120, R122, R123, R124, R141, R180, R181, R383
- RU0122 (11): R064, R065, R083, R120, R122, R123, R124, R141, R181, R383, R424
- RU0123 (11): R064, R065, R083, R120, R122, R124, R125, R140, R141, R179, R181
- RU0124 (11): R064, R065, R083, R120, R122, R124, R125, R140, R141, R180, R181
- RU0125 (11): R064, R065, R083, R120, R122, R124, R125, R140, R141, R181, R424
- RU0126 (11): R064, R065, R083, R120, R122, R124, R125, R140, R179, R180, R181
- RU0127 (11): R064, R065, R083, R120, R122, R124, R125, R140, R179, R181, R424
- RU0128 (11): R064, R065, R083, R120, R122, R124, R125, R140, R180, R181, R424
- RU0129 (11): R064, R065, R083, R120, R122, R124, R125, R141, R179, R181, R383
- RU0130 (11): R064, R065, R083, R120, R122, R124, R125, R141, R181, R383, R424
- RU0131 (11): R064, R065, R083, R120, R122, R124, R125, R179, R180, R181, R383
- RU0132 (11): R064, R065, R083, R120, R122, R124, R125, R179, R181, R383, R424
- RU0133 (11): R064, R065, R083, R120, R122, R124, R125, R180, R181, R383, R424
- RU0134 (11): R064, R065, R083, R120, R122, R124, R141, R179, R180, R181, R383
- RU0135 (11): R064, R065, R083, R120, R122, R124, R141, R179, R181, R383, R424
- RU0136 (11): R064, R065, R083, R120, R122, R124, R141, R180, R181, R383, R424
- RU0137 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181
- RU0138 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181
- RU0139 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R181, R424
- RU0140 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181
- RU0141 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181, R424
- RU0142 (12): R000, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181, R424
- RU0143 (12): R000, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383
- RU0144 (12): R000, R064, R083, R120, R122, R123, R124, R125, R141, R181, R383, R424
- RU0145 (12): R000, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383
- RU0146 (12): R000, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383, R424
- RU0147 (12): R000, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383, R424
- RU0148 (12): R000, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383
- RU0149 (12): R000, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383, R424
- RU0150 (12): R000, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383, R424
- RU0151 (12): R000, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181
- RU0152 (12): R000, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181, R424
- RU0153 (12): R000, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181, R424
- RU0154 (12): R000, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181, R424
- RU0155 (12): R000, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383
- RU0156 (12): R000, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383, R424
- RU0157 (12): R000, R064, R083, R120, R122, R124, R125, R141, R180, R181, R383, R424
- RU0158 (12): R000, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383, R424
- RU0159 (12): R000, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383, R424
- RU0160 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181
- RU0161 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181
- RU0162 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R181, R424
- RU0163 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181
- RU0164 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181, R424
- RU0165 (12): R057, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181, R424
- RU0166 (12): R057, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383
- RU0167 (12): R057, R064, R083, R120, R122, R123, R124, R125, R141, R181, R383, R424
- RU0168 (12): R057, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383
- RU0169 (12): R057, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383, R424
- RU0170 (12): R057, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383, R424
- RU0171 (12): R057, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383
- RU0172 (12): R057, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383, R424
- RU0173 (12): R057, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383, R424
- RU0174 (12): R057, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181
- RU0175 (12): R057, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181, R424
- RU0176 (12): R057, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181, R424
- RU0177 (12): R057, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181, R424
- RU0178 (12): R057, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383
- RU0179 (12): R057, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383, R424
- RU0180 (12): R057, R064, R083, R120, R122, R124, R125, R141, R180, R181, R383, R424
- RU0181 (12): R057, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383, R424
- RU0182 (12): R057, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383, R424
- RU0183 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181
- RU0184 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181
- RU0185 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R181, R424
- RU0186 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181
- RU0187 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R179, R181, R424
- RU0188 (12): R060, R064, R083, R120, R122, R123, R124, R125, R140, R180, R181, R424
- RU0189 (12): R060, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383
- RU0190 (12): R060, R064, R083, R120, R122, R123, R124, R125, R141, R181, R383, R424
- RU0191 (12): R060, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383
- RU0192 (12): R060, R064, R083, R120, R122, R123, R124, R125, R179, R181, R383, R424
- RU0193 (12): R060, R064, R083, R120, R122, R123, R124, R125, R180, R181, R383, R424
- RU0194 (12): R060, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383
- RU0195 (12): R060, R064, R083, R120, R122, R123, R124, R141, R179, R181, R383, R424
- RU0196 (12): R060, R064, R083, R120, R122, R123, R124, R141, R180, R181, R383, R424
- RU0197 (12): R060, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181
- RU0198 (12): R060, R064, R083, R120, R122, R124, R125, R140, R141, R179, R181, R424
- RU0199 (12): R060, R064, R083, R120, R122, R124, R125, R140, R141, R180, R181, R424
- RU0200 (12): R060, R064, R083, R120, R122, R124, R125, R140, R179, R180, R181, R424
- RU0201 (12): R060, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383
- RU0202 (12): R060, R064, R083, R120, R122, R124, R125, R141, R179, R181, R383, R424
- RU0203 (12): R060, R064, R083, R120, R122, R124, R125, R141, R180, R181, R383, R424
- RU0204 (12): R060, R064, R083, R120, R122, R124, R125, R179, R180, R181, R383, R424
- RU0205 (12): R060, R064, R083, R120, R122, R124, R141, R179, R180, R181, R383, R424
- RU0206 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181
- RU0207 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181
- RU0208 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R181, R424
- RU0209 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181
- RU0210 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R179, R181, R424
- RU0211 (12): R064, R065, R083, R120, R122, R123, R124, R125, R140, R180, R181, R424
- RU0212 (12): R064, R065, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383
- RU0213 (12): R064, R065, R083, R120, R122, R123, R124, R125, R141, R181, R383, R424
- RU0214 (12): R064, R065, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383
- RU0215 (12): R064, R065, R083, R120, R122, R123, R124, R125, R179, R181, R383, R424
- RU0216 (12): R064, R065, R083, R120, R122, R123, R124, R125, R180, R181, R383, R424
- RU0217 (12): R064, R065, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383
- RU0218 (12): R064, R065, R083, R120, R122, R123, R124, R141, R179, R181, R383, R424
- RU0219 (12): R064, R065, R083, R120, R122, R123, R124, R141, R180, R181, R383, R424
- RU0220 (12): R064, R065, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181
- RU0221 (12): R064, R065, R083, R120, R122, R124, R125, R140, R141, R179, R181, R424
- RU0222 (12): R064, R065, R083, R120, R122, R124, R125, R140, R141, R180, R181, R424
- RU0223 (12): R064, R065, R083, R120, R122, R124, R125, R140, R179, R180, R181, R424
- RU0224 (12): R064, R065, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383
- RU0225 (12): R064, R065, R083, R120, R122, R124, R125, R141, R179, R181, R383, R424
- RU0226 (12): R064, R065, R083, R120, R122, R124, R125, R141, R180, R181, R383, R424
- RU0227 (12): R064, R065, R083, R120, R122, R124, R125, R179, R180, R181, R383, R424
- RU0228 (12): R064, R065, R083, R120, R122, R124, R141, R179, R180, R181, R383, R424
- RU0229 (13): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181
- RU0230 (13): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181, R424
- RU0231 (13): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181, R424
- RU0232 (13): R000, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181, R424
- RU0233 (13): R000, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383
- RU0234 (13): R000, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383, R424
- RU0235 (13): R000, R064, R083, R120, R122, R123, R124, R125, R141, R180, R181, R383, R424
- RU0236 (13): R000, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383, R424
- RU0237 (13): R000, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383, R424
- RU0238 (13): R000, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181, R424
- RU0239 (13): R000, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383, R424
- RU0240 (13): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181
- RU0241 (13): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181, R424
- RU0242 (13): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181, R424
- RU0243 (13): R057, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181, R424
- RU0244 (13): R057, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383
- RU0245 (13): R057, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383, R424
- RU0246 (13): R057, R064, R083, R120, R122, R123, R124, R125, R141, R180, R181, R383, R424
- RU0247 (13): R057, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383, R424
- RU0248 (13): R057, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383, R424
- RU0249 (13): R057, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181, R424
- RU0250 (13): R057, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383, R424
- RU0251 (13): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181
- RU0252 (13): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181, R424
- RU0253 (13): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181, R424
- RU0254 (13): R060, R064, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181, R424
- RU0255 (13): R060, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383
- RU0256 (13): R060, R064, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383, R424
- RU0257 (13): R060, R064, R083, R120, R122, R123, R124, R125, R141, R180, R181, R383, R424
- RU0258 (13): R060, R064, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383, R424
- RU0259 (13): R060, R064, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383, R424
- RU0260 (13): R060, R064, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181, R424
- RU0261 (13): R060, R064, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383, R424
- RU0262 (13): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181
- RU0263 (13): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R179, R181, R424
- RU0264 (13): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R180, R181, R424
- RU0265 (13): R064, R065, R083, R120, R122, R123, R124, R125, R140, R179, R180, R181, R424
- RU0266 (13): R064, R065, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383
- RU0267 (13): R064, R065, R083, R120, R122, R123, R124, R125, R141, R179, R181, R383, R424
- RU0268 (13): R064, R065, R083, R120, R122, R123, R124, R125, R141, R180, R181, R383, R424
- RU0269 (13): R064, R065, R083, R120, R122, R123, R124, R125, R179, R180, R181, R383, R424
- RU0270 (13): R064, R065, R083, R120, R122, R123, R124, R141, R179, R180, R181, R383, R424
- RU0271 (13): R064, R065, R083, R120, R122, R124, R125, R140, R141, R179, R180, R181, R424
- RU0272 (13): R064, R065, R083, R120, R122, R124, R125, R141, R179, R180, R181, R383, R424
- RU0273 (14): R000, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181, R424
- RU0274 (14): R000, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383, R424
- RU0275 (14): R057, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181, R424
- RU0276 (14): R057, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383, R424
- RU0277 (14): R060, R064, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181, R424
- RU0278 (14): R060, R064, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383, R424
- RU0279 (14): R064, R065, R083, R120, R122, R123, R124, R125, R140, R141, R179, R180, R181, R424
- RU0280 (14): R064, R065, R083, R120, R122, R123, R124, R125, R141, R179, R180, R181, R383, R424

Distinct sufficient semantic-unit unions

1 distinct unions; unit-count range 49–49.

- UU0001: S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15, S16, S17, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24, T25, T26, T27, T28, T29, T30, T31, T32

Task-indispensable resources: R064, R083, R120, R122, R124, R181

Task-indispensable units: S01, S02, S03, S04, S05, S06, S07, S08, S09, S10, S11, S12, S13, S14, S15, S16, S17, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24, T25, T26, T27, T28, T29, T30, T31, T32

Globally inclusion-minimal resource unions

All complete obligation-witness combinations are retained, including combinations whose shared task union contains a globally removable resource. Obligation minimality and global inclusion minimality are distinct; the latter is also reported separately.

- GM001: R000, R064, R083, R120, R122, R124, R180, R181, R383
- GM002: R057, R064, R083, R120, R122, R124, R180, R181, R383
- GM003: R060, R064, R083, R120, R122, R124, R180, R181, R383
- GM004: R064, R065, R083, R120, R122, R124, R180, R181, R383
- GM005: R000, R064, R083, R120, R122, R124, R125, R140, R179, R181
- GM006: R000, R064, R083, R120, R122, R124, R125, R140, R180, R181
- GM007: R000, R064, R083, R120, R122, R124, R125, R140, R181, R424
- GM008: R000, R064, R083, R120, R122, R124, R125, R179, R181, R383
- GM009: R000, R064, R083, R120, R122, R124, R125, R181, R383, R424
- GM010: R000, R064, R083, R120, R122, R124, R141, R179, R181, R383
- GM011: R000, R064, R083, R120, R122, R124, R141, R181, R383, R424
- GM012: R057, R064, R083, R120, R122, R124, R125, R140, R179, R181
- GM013: R057, R064, R083, R120, R122, R124, R125, R140, R180, R181
- GM014: R057, R064, R083, R120, R122, R124, R125, R140, R181, R424
- GM015: R057, R064, R083, R120, R122, R124, R125, R179, R181, R383
- GM016: R057, R064, R083, R120, R122, R124, R125, R181, R383, R424
- GM017: R057, R064, R083, R120, R122, R124, R141, R179, R181, R383
- GM018: R057, R064, R083, R120, R122, R124, R141, R181, R383, R424
- GM019: R060, R064, R083, R120, R122, R124, R125, R140, R179, R181
- GM020: R060, R064, R083, R120, R122, R124, R125, R140, R180, R181
- GM021: R060, R064, R083, R120, R122, R124, R125, R140, R181, R424
- GM022: R060, R064, R083, R120, R122, R124, R125, R179, R181, R383
- GM023: R060, R064, R083, R120, R122, R124, R125, R181, R383, R424
- GM024: R060, R064, R083, R120, R122, R124, R141, R179, R181, R383
- GM025: R060, R064, R083, R120, R122, R124, R141, R181, R383, R424
- GM026: R064, R065, R083, R120, R122, R124, R125, R140, R179, R181
- GM027: R064, R065, R083, R120, R122, R124, R125, R140, R180, R181
- GM028: R064, R065, R083, R120, R122, R124, R125, R140, R181, R424
- GM029: R064, R065, R083, R120, R122, R124, R125, R179, R181, R383
- GM030: R064, R065, R083, R120, R122, R124, R125, R181, R383, R424
- GM031: R064, R065, R083, R120, R122, R124, R141, R179, R181, R383
- GM032: R064, R065, R083, R120, R122, R124, R141, R181, R383, R424

Gaps, limitations and ambiguity

- TASK_INTERPRETATION_GAP: NONE. All nine substantive task paragraphs are covered by frozen statements, criteria and exact task basis. The tenth paragraph is operational.
- TASK_GAP: NONE. The task and eligible contracts establish required feature decisions; remaining API design choices permit multiple valid implementations.
- REPOSITORY_INFORMATION_GAP: NONE. Necessary current interfaces, ownership and configured validation contracts have complete eligible support. Future destinations need no prior implementation.
- L01 (FUTURE_DESIGN_CHOICE): The task fixes two new names and required information, but does not fix constructor signatures, helper value types, projection method name, key spelling, or a new digest algorithm. Multiple faithful designs remain valid. Blocking: False.
- L02 (OPAQUE_NATIVE_VALUE): native_provenance is typed object. Preserve the original value in memory. A JSON-compatible projection must expose selected stable fields rather than promise serialization of arbitrary native objects or infer a universal provenance schema. Blocking: False.
- L03 (BOUNDED_AUTHENTICATION): resource_at authenticates addressed membership in the supplied retained snapshot, not filesystem freshness or full semantic truth of opaque provenance. The task forbids reacquisition/rematerialization and does not require recomputing all snapshot/content digests. Blocking: False.
- L04 (SUPPORT_CARDINALITY): Item address/content tuples are not length-checked by the existing ContextDisclosure constructor. Future manifest validation must reject misalignment; repeated support can occur even though a DisclosurePlan rejects identical option identities. The task does not expressly settle whether a zero-support custom option must be rejected. Blocking: False.
- L05 (BYTE_ACCOUNTING): Materialized item text includes representation headers and framing, not just raw source. Unique resource totals concern addressed retained source occurrences, not unique hashes or a sum over repeated support records. Either address or address/content pair is a valid unique key within one authenticated frame. Blocking: False.
- L06 (BOUNDED_NATIVE_MEANING): A qualified-reference native value and its direct-call flag retain bounded source meaning; preserving provenance cannot strengthen that into execution or exhaustive semantic coverage. Blocking: False.
- L07 (VALIDATION_ENVIRONMENT): The frozen frame establishes validation configuration and the protected command; successful future checks and host environment readiness are not established by this adjudication. No repository validation was executed. Blocking: False.
- A01: BOUNDED_IMPLEMENTATION_CHOICE; see L01; blocking: False.
- A02: ZERO_SUPPORT_CUSTOM_OPTION_UNSPECIFIED; see L04; blocking: False.

Unresolved cell judgments: none.

Internal self-review corrections

- Split compound test acceptance, validation process/configuration and materialization units into independently inspectable facts; final granularity is 32 task-backed and 17 repository-supported units.
- Separated future manifest names and test destination from existing repository facts; absence of future files is not a gap.
- Removed package overview and broad architecture prose from necessary witnesses when the task already supplies the documentation/scope requirement.
- Represented plan-surface evidence from complementary materialization/rendering consumers as an alternative to the plan declaration; retained current-field evidence rather than substituting future task prose.
- Kept mixed-choice tests as a defensible alternative source for existing option contracts. Removed exact rendering and assembly bodies as required test-obligation units: retaining existing regression coverage does not require rewriting those assertions. Their current bodies remain necessary to the separate compatibility obligation.
- Kept profile documentation, implementation, operating guide and backlog implemented-contract prose as alternatives; demoted profile tests to corroboration because they do not assert the entire argument list. Retained pyproject for precise settings.
- Split resource surface from addressed-resource versus content identity. Removed observation-constructor evidence as a standalone proof of every occurrence read attribute, and removed plan constructor examples as a standalone proof of every plan read attribute. Retained these as corroboration where appropriate.
- Excluded internal digest reimplementation, source extraction and Python parser internals from necessary units; the manifest consumes retained values.
- Removed redundant resource supersets from each obligation witness; computed shared task unions without equating the full REQUIRED union with simultaneous necessity.

Exact support-span catalogue

Offsets are half-open Unicode character offsets in the sealed decoded task/resource text. Line numbers are one-based. Repeated uses of one exact span share this catalogue entry; JSON retains spans at each relevant judgment. Original quoted evidence may contain natural repository terminology.

R000 AGENTS.md [8733:10193] lines 185–214

~~~~text

## Runtime, lifecycle, Context, and evidence

Current Runtime is intentionally narrow: one selected ModelInteraction
coordinated with one Conversation plus optional specialized InteractionAttempt
observation. Evidence construction remains in observability. Do not put general Agent loops, workflow graphs, multi-Agent
coordination, scheduling, supervisor/worker logic, generic retries, or
orchestration policy into Runtime.

Conversation is distinct from Run. Generic Run, Step, and Attempt are taxonomy
concepts, not authorization to create framework classes. Do not broaden current
`Attempt` into Tool or Command attempts without explicit lifecycle work.

Context is information selected as relevant to a purpose, not a universal
mutable state bag. It may draw from Conversation, Resources, Memory, Tool
results, Evidence, documentation, or Run state without owning those sources.

Persistence stores/restores representations owned by other domains. It does
not thereby own Conversation, Run, Memory, Evidence, Agent, or Context. Do not
casually change durable compatibility or assume a wire representation equals a
runtime representation.

Evidence is factual/historical observation, not Trace, Telemetry, or current
authority. Do not create Event/Trace/Telemetry infrastructure merely for one
bounded report. Preserve:

```text
cancellation != rollback
communication failure != proof an external effect failed
persistence != exactly-once external effects
~~~~

R000 AGENTS.md [10713:11283] lines 228–240

~~~~text
The canonical protected development test profile is documented in
[docs/development/validation.md](docs/development/validation.md). Run it with:

```text
uv run python scripts/validate_development.py
```

It excludes `tests/experiments/` before collection to avoid retained
outcome-dependent tests. Keep the configured production branch-coverage gate.
Run Ruff, formatting, mypy, and diff checks separately as documented. Do not
run confirmation validation or live model/Docker tests for ordinary work;
those require explicit authorization and are reported separately.
~~~~

R002 docs/architecture.md [39280:41020] lines 621–645

~~~~text
A sibling bounded Context path accepts an explicit purpose and one
caller-chosen qualified Python Reference/direct Call fact from its production
analysis. It validates fact membership, source and target dependencies, and
qualified resolution support against an identified RepositorySnapshot. It
extracts the exact Reference Name occurrence and resolved direct function
declaration span from retained snapshot content, renders the relationship
separately from both source segments with locations and navigation pointers,
and can place the result beside an unchanged task in a copied ModelRequest.
The Call tag describes syntax at ast.Call.func, not execution; Reference
coverage remains non-exhaustive. No fact is chosen automatically, and invalid
dependencies fail without whole-file fallback or filesystem reacquisition.

The first common Context Planning foundation now records a caller-directed,
immutable DisclosurePlan under one purpose and RepositorySnapshot identity.
It can hold multiple ordered concrete disclosure choices. One adapter
realizes the existing qualified Reference path; another explicitly discloses
one whole retained resource. Materialization rechecks applicability, retains
native provenance and content identities in ContextDisclosure items, and
fails on missing or stale state. Rendering and ModelRequest assembly happen
after realization. This is a production plan/materialization boundary, not
an automatic planner, resource Selector, sufficiency judgment, or retrieval
operation. A later plan may identify a preceding plan, without claiming
agent recovery or prior model comprehension. The
[Context Planning package](../src/devtools/context/planning/docs/overview.md)
describes the implemented API and limits.
~~~~

R004 docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md [3034:4495] lines 57–78

~~~~text
another supported resource arrangement. `ResolvedPath` and filesystem
Resources remain access and location mechanisms; they do not acquire
repository-identity meaning.

A **RepositorySnapshot** is an immutable, logically complete description of
successfully observed repository state under explicit snapshot and observation
semantics. Its identity is content-derived, not merely timestamp- or
Git-commit-derived. Logical completeness is relative to declared inclusion
semantics; it does not require every filesystem object below a root, physical
copying of all state, or rescanning/rebuilding all intelligence. A snapshot can
share unchanged physical representation with another snapshot while each still
describes a complete state. Git metadata may be provenance associated with a
snapshot, but does not define snapshot identity: dirty working-tree states can
share a Git HEAD while being different snapshots.

Snapshot semantics must be able to establish root, inclusion/exclusion and
ignore treatment, generated/vendor/binary treatment, symlink/nested-repository/
submodule behavior, identity-relevant resource attributes, and necessary path
interpretation. The exact SnapshotPolicy API and universal default remain open.
Policy/observation semantics and resulting repository-state identity are not
casually identical: distinct policies can potentially observe equivalent state,
while some policy differences can be identity-relevant. The exact relationship
~~~~

R006 docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md [12520:16413] lines 209–270

~~~~text
A **DisclosurePlan** is the identified decision about what information should be
made available, through selected disclosure possibilities, representations, or
transformations under its purpose, evidence, constraints, and planning
semantics. A **ContextDisclosure** is the identifiable, provenance-bearing
information artifact actually realized with reference to a DisclosurePlan.
Neither is a ModelRequest. Concrete models, identities, and cardinality are
open: a plan can fail to produce a disclosure, revision creates a new plan, and
future semantics may permit more than one realized disclosure from a plan. Once
established as identified planning/evidence artifacts, plans and disclosures
are immutable.

Representation or transformation choice is part of the disclosure decision.
An evaluation that varies representation therefore cannot generally claim to
hold the exact DisclosurePlan fixed: it can hold selected supporting
information, purpose, budget, and relevant constraints fixed while comparing
distinct plans, or compare conforming realizations of one selected
transformation. Ordering can instead be an assembly intervention when the same
realized ContextDisclosure is retained. The concrete experimental record is
Evaluation responsibility, not a new disclosure artifact.

The materialization boundary is:

```text
DisclosurePlan -> materialization -> ContextDisclosure -> model-input assembly -> ModelRequest
```

Materialization faithfully realizes the disclosure decision selected by the
DisclosurePlan. It can resolve applicable source, extract source-preserving
material, project existing DerivedKnowledge, format or structurally transform
information, and perform a semantic transformation or lossy synthesis when that
transformation was explicitly selected by the plan. For example, a plan may
select a bounded task-focused summary of identified supporting information.
Materialization does not thereby promote that purpose-relative synthesis to
repository DerivedKnowledge.

Materialization must not silently invent a materially different synthesis or
substitute a materially different disclosure decision under the guise of
formatting or faithful realization. When material to correct interpretation,
the realized information preserves its origin, support, assumptions,
uncertainty, conflicts, and purpose-relative nature. Changed dependencies,
inapplicable knowledge, unresolved source, unavailable knowledge, failed
transformation, cost violation, or disclosure policy can make faithful
realization impossible and require an observable failure or later re-planning/
acquisition. No mandatory independent global identity, persistent synthesis
artifact, or synthesis store follows from performing the selected work.

Planning-time applicability does not guarantee applicability when realization
occurs: repository dependencies may change. Materialization must not silently
present selected information as current when it is no longer applicable; future
handling may re-plan, re-derive, or re-acquire without selecting race/atomicity
mechanics here. Planning may use estimated cost, while materialization and
assembly expose actual realized cost. Those remain distinct so future evaluation
can assess representation, derivation-latency, token, and other predictions.

A ContextDisclosure may be reusable independently of one ModelRequest or one
assembly policy when its information remains applicable and appropriate to a
later purpose/consumer. Applicability alone does not establish relevance.
Possible future reuse levels include DerivedKnowledge, materialized
representation, and ContextDisclosure; cache keys, storage, and granularity are
open. Provenance must eventually distinguish planning failure, materialization
failure, assembly failure, and model-utilization failure rather than collapse
differences between selected, realized, and presented information.
~~~~

R010 docs/architecture/taxonomy.md [43456:45114] lines 798–823

~~~~text
### Context disclosure and assembly

**Status: EMERGING.**

Context compilation conditionally composes information for a consumer; it is
not top-K retrieval or budget filling. Ranking remains an input, while
disclosure planning couples candidate and representation choice and can reason
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, coherence, and multidimensional cost. A ContextCandidate can support
multiple representations without selecting a fixed `DisclosureOption` type.

A ContextDisclosure is an identifiable, provenance-bearing account of
purpose-selected represented information. A DisclosurePlan is the distinct
identified decision about what should be made available; a ContextDisclosure is
what was actually realized with reference to that plan. Both are immutable
artifact directions, neither is a ModelRequest, and materialization between
them must not silently make a materially different plan. Repository, disclosure,
and Conversation histories may reference one another but retain separate
identities and lifecycles. Production now has one caller-directed,
snapshot-bound DisclosurePlan with qualified Python Reference and explicit
whole-resource options, and a separate faithfully realized ContextDisclosure.
That bounded implementation does not establish automatic planning, a universal
representation taxonomy, or sufficiency. Previously disclosed information
need not remain currently available or applicable. Tracking disclosure or
availability must not claim model comprehension or create a ModelKnowledgeState.
~~~~

R012 docs/backlog/epics/B-0002-coding-context-substrate.md [9332:10666] lines 145–163

~~~~text
A bounded pre-analysis operation also filters an explicit caller-ordered set of
observed resources by exact stdlib Python `NAME` token presence for that same
purpose. It retains its eligible and candidate occurrences plus native token
match evidence. Candidate presence is weaker than declaration knowledge and
expected to include calls, references, or methods; candidate zero is bounded to
the eligible resources, and declaration derivation remains authoritative for
the implemented syntactic proposition.

[ADR-0004](../../architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
now settles post-ranking Context/disclosure semantics: conditional composition,
representation-coupled selection, coverage, applicability, prior availability,
sufficiency, budgeting, ContextDisclosure, and separation from model-input
assembly. Its refinement further settles information-not-string disclosure,
DisclosureOption/DisclosurePlan/ContextDisclosure distinctions, representation
origin/form/fidelity/cost, repository-relative DerivedKnowledge distinct from
purpose-relative synthesis, representational transformation distinct from
epistemic derivation, coherence, authority, conflict preservation, and faithful
materialization of explicitly planned semantic transformation without silent
semantic strengthening. It leaves
~~~~

R028 docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md [0:1505] lines 1–33

~~~~text
# B-0018 — Investigate operational-data minimization and disclosure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: collection, disclosure, retention, and export of operational payloads
- primary_domain: governance
- supporting_domains: observability, context, persistence, models, tools

## Problem / value

Determine minimization and disclosure boundaries for repository data, prompts,
model responses, Tool inputs/results, paths, exceptions, governance facts, and
durable records. Prefer minimizing collection before downstream redaction.

An occurrence may be reportable without authority to disclose its payload.
Current terminal Evidence minimizes payload but does not resolve this pressure.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
establishes the ModelInteraction capture rule: capture policy and a manifest
must distinguish unavailable, omitted, and redacted provider facts, while
credentials and equivalent sensitive transport state are never generically
captured. Retention, export, and broader disclosure policy remain deferred.

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0013, B-0023, B-0024
- operational_dependencies: sensitive diagnostic or evidence payload
- promotion_trigger: real harness must retain or export data whose disclosure matters
- validation_level: NONE
~~~~

R037 docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md [0:1419] lines 1–33

~~~~text
# B-0027 — Investigate serialization and representation boundaries

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: translation among runtime, provider wire, and durable representations
- primary_domain: persistence
- supporting_domains: models, agents, observability

## Problem / value

Current evidence distinguishes ConversationMessage, Prompt, ModelResponse,
provider wire forms, Conversation persistence forms, and Evidence forms. A
runtime value is not automatically a provider wire or durable schema.

Investigate only when a semantic value must reliably cross distinct boundaries;
do not introduce a universal serializer or schema framework.

[ADR-0001](../../architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
establishes the ModelInteraction application of this distinction: semantic
request/response values, typed provider exchange, and capture-controlled
Evidence are separate representations. It does not authorize a universal
serializer, durable schema, or raw-payload persistence.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: boundary needing stable compatible representation
- promotion_trigger: one semantic value must reliably cross two representation boundaries
- validation_level: NONE
~~~~

R057 docs/backlog/items/B-0047-protected-development-validation-profile.md [1286:1988] lines 29–40

~~~~text
and 100% production branch coverage. The supported general profile now uses
the same pre-collection `tests/experiments/` boundary and runs the remaining
ordinary test tree through `uv run python scripts/validate_development.py`.

## Implemented contract

The operational entry point is `scripts/validate_development.py`. It invokes
pytest over `tests/` with `tests/experiments/` ignored before recursive
collection. This stable directory boundary excludes retained replay and
outcome-dependent material without inspecting outcomes or maintaining a list
of sensitive test node IDs. It leaves project pytest options, including the
100% production branch-coverage requirement, intact and returns pytest's
~~~~

R057 docs/backlog/items/B-0047-protected-development-validation-profile.md [1516:2137] lines 33–42

~~~~text
## Implemented contract

The operational entry point is `scripts/validate_development.py`. It invokes
pytest over `tests/` with `tests/experiments/` ignored before recursive
collection. This stable directory boundary excludes retained replay and
outcome-dependent material without inspecting outcomes or maintaining a list
of sensitive test node IDs. It leaves project pytest options, including the
100% production branch-coverage requirement, intact and returns pytest's
failure code. The profile contract and separate static quality gates are
documented in `docs/development/validation.md` and linked from `AGENTS.md`.
~~~~

R060 docs/development/validation.md [26:1277] lines 3–27

~~~~text
## Protected development test profile

Run the ordinary repository test suite with:

```text
uv run python scripts/validate_development.py
```

The command runs pytest against `tests/` and ignores `tests/experiments/` before
recursive collection. The experiment test tree contains retained replay and
outcome-dependent tests alongside other experimental checks, so the protected
profile excludes the tree by its repository role rather than inspecting test
names, retained data, or confirmation outcomes to decide what to run. The
ordinary production, unit, integration, and operational-script tests outside
that tree remain in scope. Case 0003 additionally named its capture and
synthetic protocol tests explicitly for that experiment; the general profile
does not carry those case-specific additions.

The profile uses the project pytest configuration without overriding it. This
preserves strict configuration and marker checks, branch coverage, and the
100% production coverage threshold. Pytest's exit code is returned by the
command, so a failed test or coverage gate fails the command.

This profile validates development behavior. It does not validate confirmation
judgments or retained outcomes. Confirmation validation is a separate activity
~~~~

R060 docs/development/validation.md [26:1422] lines 3–29

~~~~text
## Protected development test profile

Run the ordinary repository test suite with:

```text
uv run python scripts/validate_development.py
```

The command runs pytest against `tests/` and ignores `tests/experiments/` before
recursive collection. The experiment test tree contains retained replay and
outcome-dependent tests alongside other experimental checks, so the protected
profile excludes the tree by its repository role rather than inspecting test
names, retained data, or confirmation outcomes to decide what to run. The
ordinary production, unit, integration, and operational-script tests outside
that tree remain in scope. Case 0003 additionally named its capture and
synthetic protocol tests explicitly for that experiment; the general profile
does not carry those case-specific additions.

The profile uses the project pytest configuration without overriding it. This
preserves strict configuration and marker checks, branch coverage, and the
100% production coverage threshold. Pytest's exit code is returned by the
command, so a failed test or coverage gate fails the command.

This profile validates development behavior. It does not validate confirmation
judgments or retained outcomes. Confirmation validation is a separate activity
that requires explicit authorization and a separately reviewed invocation.
Never remove the experiment-tree exclusion to make this profile pass.
~~~~

R061 docs/documentation_map.md [24075:24569] lines 324–330

~~~~text
The [Context Planning package](../src/devtools/context/planning/docs/overview.md)
owns a bounded caller-directed DisclosurePlan over one explicit purpose and
snapshot. It currently composes qualified Python Reference and whole retained
resource representations, rejects stale dependencies, preserves native
provenance in realized ContextDisclosure items, and renders/assembles them
after materialization. It does not retrieve, rank, autonomously select,
optimize budgets, or judge sufficiency.
~~~~

R063 docs/roadmap.md [27689:28362] lines 462–469

~~~~text
The current Context checkpoint establishes a caller-directed, snapshot-bound
DisclosurePlan with multiple ordered concrete choices and a distinct realized
ContextDisclosure. The existing qualified Reference path participates without
losing its native checks; an explicitly chosen whole observed resource is a
second faithful representation. This is a production planning boundary, not
automatic ranking, budget allocation, sufficiency, or a recovery controller.
The [Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
provides comparative motivation; ADR-0003 and ADR-0004 govern accepted meaning.
~~~~

R064 pyproject.toml [611:1368] lines 35–78

~~~~text
testpaths = ["tests"]
addopts = [
    "--strict-config",
    "--strict-markers",
    "--cov=devtools",
    "--cov-branch",
    "--cov-report=term-missing",
    "--cov-fail-under=100",
]
markers = [
    "live_codex: opt-in test that contacts the locally authenticated Codex CLI",
]

[tool.coverage.run]
branch = true
source = ["devtools"]

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 100

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D203",
    "D213",
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",
]

[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests", "experiments"]
explicit_package_bases = true
mypy_path = ["src"]
~~~~

R065 scripts/validate_development.py [0:715] lines 1–27

~~~~text
# Copyright (c) 2026
# ruff: noqa: INP001
"""Run the repository's protected ordinary development test profile."""

from __future__ import annotations

from pathlib import Path

import pytest

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    """Select ordinary tests while excluding the retained experiment tree."""
    tests = repository_root / "tests"
    experiments = tests / "experiments"
    return [str(tests), f"--ignore={experiments}"]


def main() -> int:
    """Run pytest and return its exit code unchanged."""
    return int(pytest.main(pytest_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())
~~~~

R083 src/devtools/context/__init__.py [0:2855] lines 1–75

~~~~text
# Copyright (c) 2026
"""Public Repository Intelligence and bounded Context API."""

from devtools.context.planning import (
    ContextDisclosure,
    DisclosureMaterializationError,
    DisclosurePlan,
    MaterializedDisclosureItem,
    PlannedDisclosure,
    RenderedContextDisclosure,
    WholeResourceDisclosureOption,
    assemble_context_disclosure_model_request,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.python import (
    PythonSourceAddressCandidate,
    PythonSourceAddressCandidateEvidence,
    PythonSourceAddressCandidateSelection,
    select_python_source_address_candidates,
)
from devtools.context.python.function import (
    MaterializedPythonFunctionContext,
    MaterializedPythonFunctionDeclaration,
    MaterializedPythonQualifiedReferenceContext,
    PythonFunctionAnalysisCandidateResource,
    PythonFunctionAnalysisCandidateSelection,
    PythonFunctionCandidateTokenizationError,
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationAnalysisAggregate,
    PythonFunctionDeclarationCoverage,
    PythonFunctionDeclarationDerivation,
    PythonFunctionDeclarationDerivationDefinition,
    PythonFunctionDeclarationDisclosureItem,
    PythonFunctionDeclarationKind,
    PythonFunctionDeclarationKnowledge,
    PythonFunctionExactNameContextDisclosure,
    PythonFunctionExactNameQuery,
    PythonFunctionExactNameRelevanceEvidence,
    PythonFunctionExactNameResourceSelection,
    PythonFunctionExactNameRetrievalResult,
    PythonFunctionExactNameSelectedResource,
    PythonFunctionNameTokenCandidateEvidence,
    PythonFunctionSourceMaterializationError,
    PythonFunctionSubject,
    PythonModuleParseError,
    PythonModuleResourceDependency,
    PythonQualifiedReferenceDisclosure,
    PythonQualifiedReferenceDisclosureError,
    PythonQualifiedReferenceDisclosureOption,
    PythonSourceOccurrence,
    PythonSourceRange,
    RenderedPythonFunctionContext,
    RenderedPythonQualifiedReferenceContext,
    analyze_python_function_declaration_resources,
    assemble_python_function_context_model_request,
    assemble_python_qualified_reference_model_request,
    choose_python_qualified_reference_disclosure,
    derive_python_function_declarations,
    disclose_python_function_exact_name_retrieval,
    disclose_python_qualified_reference,
    materialize_python_function_disclosure_source,
    materialize_python_qualified_reference_source,
    render_materialized_python_function_context,
    render_python_qualified_reference_context,
    retrieve_python_functions_by_exact_name,
    select_python_function_analysis_candidates,
    select_python_function_resources_from_exact_name_retrieval,
)
from devtools.context.repository import (
    ContentIdentity,
    Repository,
    RepositoryId,
~~~~

R083 src/devtools/context/__init__.py [83:535] lines 3–18

~~~~text

from devtools.context.planning import (
    ContextDisclosure,
    DisclosureMaterializationError,
    DisclosurePlan,
    MaterializedDisclosureItem,
    PlannedDisclosure,
    RenderedContextDisclosure,
    WholeResourceDisclosureOption,
    assemble_context_disclosure_model_request,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
    render_context_disclosure,
)
from devtools.context.python import (
~~~~

R083 src/devtools/context/__init__.py [4841:9619] lines 128–242

~~~~text
__all__ = [
    "ContentIdentity",
    "ContextDisclosure",
    "DisclosureMaterializationError",
    "DisclosurePlan",
    "MaterializedDisclosureItem",
    "MaterializedPythonFunctionContext",
    "MaterializedPythonFunctionDeclaration",
    "MaterializedPythonQualifiedReferenceContext",
    "PlannedDisclosure",
    "PythonFunctionAnalysisCandidateResource",
    "PythonFunctionAnalysisCandidateSelection",
    "PythonFunctionCandidateTokenizationError",
    "PythonFunctionDeclarationAnalysis",
    "PythonFunctionDeclarationAnalysisAggregate",
    "PythonFunctionDeclarationCoverage",
    "PythonFunctionDeclarationDerivation",
    "PythonFunctionDeclarationDerivationDefinition",
    "PythonFunctionDeclarationDisclosureItem",
    "PythonFunctionDeclarationKind",
    "PythonFunctionDeclarationKnowledge",
    "PythonFunctionExactNameContextDisclosure",
    "PythonFunctionExactNameQuery",
    "PythonFunctionExactNameRelevanceEvidence",
    "PythonFunctionExactNameResourceSelection",
    "PythonFunctionExactNameRetrievalResult",
    "PythonFunctionExactNameSelectedResource",
    "PythonFunctionNameTokenCandidateEvidence",
    "PythonFunctionSourceMaterializationError",
    "PythonFunctionSubject",
    "PythonModuleParseError",
    "PythonModuleResourceDependency",
    "PythonQualifiedReferenceDisclosure",
    "PythonQualifiedReferenceDisclosureError",
    "PythonQualifiedReferenceDisclosureOption",
    "PythonSourceAddressCandidate",
    "PythonSourceAddressCandidateEvidence",
    "PythonSourceAddressCandidateSelection",
    "PythonSourceOccurrence",
    "PythonSourceRange",
    "RenderedContextDisclosure",
    "RenderedPythonFunctionContext",
    "RenderedPythonQualifiedReferenceContext",
    "Repository",
    "RepositoryId",
    "RepositoryObservationError",
    "RepositoryResourceAddress",
    "RepositoryResourceDiscovery",
    "RepositoryResourceDiscoveryError",
    "RepositoryResourceOccurrence",
    "RepositorySnapshot",
    "RepositorySnapshotId",
    "RepositoryTextCorpus",
    "RepositoryTextCorpusDefinition",
    "RepositoryTextCorpusId",
    "RepositoryTextDocument",
    "RepositoryTextDocumentCollection",
    "RepositoryTextDocumentId",
    "RepositoryTextLexicalBm25Match",
    "RepositoryTextLexicalBm25RetrievalResult",
    "RepositoryTextLexicalBm25Settings",
    "RepositoryTextLexicalBm25TermContribution",
    "RepositoryTextLexicalCollectionAnalysis",
    "RepositoryTextLexicalCorpusStatistics",
    "RepositoryTextLexicalDocumentAnalysis",
    "RepositoryTextLexicalDocumentFrequency",
    "RepositoryTextLexicalDocumentStatistics",
    "RepositoryTextLexicalInvertedIndex",
    "RepositoryTextLexicalObservation",
    "RepositoryTextLexicalPosting",
    "RepositoryTextLexicalQuery",
    "RepositoryTextLexicalQueryObservation",
    "RepositoryTextLexicalRetrievalEvaluationCase",
    "RepositoryTextLexicalRetrievalEvaluationResult",
    "RepositoryTextLexicalRetrievalEvaluationSummary",
    "RepositoryTextLexicalRetrievedRelevantResource",
    "RepositoryTextLexicalTermFrequency",
    "RepositoryTextLexicalTermPostings",
    "WholeResourceDisclosureOption",
    "analyze_python_function_declaration_resources",
    "analyze_repository_text_document",
    "analyze_repository_text_document_collection",
    "analyze_repository_text_lexical_query",
    "assemble_context_disclosure_model_request",
    "assemble_python_function_context_model_request",
    "assemble_python_qualified_reference_model_request",
    "build_repository_text_lexical_inverted_index",
    "calculate_repository_text_lexical_corpus_statistics",
    "choose_python_qualified_reference_disclosure",
    "choose_whole_resource_disclosure",
    "define_repository_text_corpus",
    "derive_python_function_declarations",
    "disclose_python_function_exact_name_retrieval",
    "disclose_python_qualified_reference",
    "discover_repository_resource_addresses",
    "evaluate_repository_text_lexical_bm25_retrieval",
    "materialize_disclosure_plan",
    "materialize_python_function_disclosure_source",
    "materialize_python_qualified_reference_source",
    "observe_repository_resource",
    "observe_repository_resources",
    "plan_disclosures",
    "realize_repository_text_corpus",
    "render_context_disclosure",
    "render_materialized_python_function_context",
    "render_python_qualified_reference_context",
    "represent_repository_text_corpus",
    "retrieve_python_functions_by_exact_name",
    "retrieve_repository_text_documents_by_bm25",
    "retrieve_repository_text_documents_by_content_bm25",
    "select_python_function_analysis_candidates",
    "select_python_function_resources_from_exact_name_retrieval",
    "select_python_source_address_candidates",
    "summarize_repository_text_lexical_retrieval_evaluations",
]
~~~~

R120 src/devtools/context/planning/__init__.py [0:1080] lines 1–38

~~~~text
# Copyright (c) 2026
"""Explicit repository Context planning and faithful realization."""

from devtools.context.planning.materialization import (
    ContextDisclosure,
    DisclosureMaterializationError,
    MaterializedDisclosureItem,
    materialize_disclosure_plan,
)
from devtools.context.planning.plan import (
    DisclosurePlan,
    PlannedDisclosure,
    plan_disclosures,
)
from devtools.context.planning.rendering import (
    RenderedContextDisclosure,
    assemble_context_disclosure_model_request,
    render_context_disclosure,
)
from devtools.context.planning.resource import (
    WholeResourceDisclosureOption,
    choose_whole_resource_disclosure,
)

__all__ = [
    "ContextDisclosure",
    "DisclosureMaterializationError",
    "DisclosurePlan",
    "MaterializedDisclosureItem",
    "PlannedDisclosure",
    "RenderedContextDisclosure",
    "WholeResourceDisclosureOption",
    "assemble_context_disclosure_model_request",
    "choose_whole_resource_disclosure",
    "materialize_disclosure_plan",
    "plan_disclosures",
    "render_context_disclosure",
]
~~~~

R121 src/devtools/context/planning/docs/overview.md [0:3309] lines 1–66

~~~~text
# Explicit repository Context plans

The devtools.context.planning package owns the first production
[ADR-0004](../../../../../docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
DisclosurePlan and ContextDisclosure values. A caller supplies a purpose,
an observed RepositorySnapshot, and an ordered set of concrete disclosure
choices. plan_disclosures records that choice; it does no retrieval, ranking,
automatic selection, cost optimization, or sufficiency assessment.

~~~text
InformationNeed / caller purpose
          |
          v
       Retrieval (optional; native evidence remains independent)
          |
          v
candidate evidence / explicitly known target
          |
          v
caller chooses representations --> DisclosurePlan
                                  /             \
                                 v               v
                      qualified Reference   whole resource
                                 \               /
                                  v             v
                            ContextDisclosure
                                  |
                          deterministic rendering
                                  |
                         copied ModelRequest / Agent
                                  |
                        later need may create another plan
~~~

DisclosurePlan binds purpose, repository and snapshot identities, ordered
choices, and optional preceding-plan identity. The plan's deterministic
identity changes when purpose, applicability, order, choice, or lineage changes.
Each concrete choice names an implemented representation and retains its own
native support. The common PlannedDisclosure protocol only permits the two
current consumers to participate in one plan; it is not a generic fact ontology,
language-independent parser, or materializer registry.

materialize_disclosure_plan rechecks the supplied snapshot and requires each
materialized item to match its planned choice. It fails on stale, missing, or
incompatible dependencies. A ContextDisclosure retains one item per choice,
exact content identities and addresses, text, and the native materialized
provenance. Rendering preserves plan order and does not infer new facts.
assemble_context_disclosure_model_request copies a caller's ModelRequest and
appends already-rendered Context after the unchanged task.

Implemented choices:

- WholeResourceDisclosureOption: explicitly chosen observed resource,
  materialized from retained snapshot content. It is a coarse representation,
  never a silent fallback.
- PythonQualifiedReferenceDisclosureOption: adapts the existing Python-specific
  qualified Reference/direct Call path. Its existing fact, derivation,
  source/target content checks, exact UTF-8 extraction, and bounded Call
  meaning remain intact.

The caller may construct a later plan with a different or refined purpose and
preceding_plan_identity. This preserves lineage but does not implement an agent
recovery controller or prove that a model retained prior information. No token
budget field is selected: ADR-0004 distinguishes hard capacity, policy budget,
and remaining capacity but selects no universal cost function. A future planner
can consume retrieval evidence and explicit constraints without changing the
~~~~

R122 src/devtools/context/planning/materialization.py [657:1014] lines 24–33

~~~~text
@dataclass(frozen=True, slots=True)
class MaterializedDisclosureItem:
    """Keep rendered information separate from its native supporting value."""

    option_identity: str
    representation: str
    resource_addresses: tuple[RepositoryResourceAddress, ...]
    content_identities: tuple[ContentIdentity, ...]
    text: str
    native_provenance: object
~~~~

R122 src/devtools/context/planning/materialization.py [1016:2390] lines 36–70

~~~~text
@dataclass(frozen=True, slots=True)
class ContextDisclosure:
    """Retain one realized item per ordered plan choice."""

    plan: DisclosurePlan
    items: tuple[MaterializedDisclosureItem, ...]

    def __post_init__(self) -> None:
        """Keep the realized account aligned with its explicit plan."""
        if len(self.items) != len(self.plan.disclosures) or any(
            item.option_identity != option.identity
            or item.representation != option.representation
            for item, option in zip(self.items, self.plan.disclosures, strict=True)
        ):
            msg = "Context disclosure items do not match their planned choices."
            raise DisclosureMaterializationError(msg)

    @property
    def identity(self) -> str:
        """Identify exact realized text and source identities under the plan."""
        return _digest(
            "materialized-repository-context-disclosure-v1",
            self.plan.identity,
            *(
                value
                for item in self.items
                for value in (
                    item.option_identity,
                    item.representation,
                    *(str(address) for address in item.resource_addresses),
                    *(str(content) for content in item.content_identities),
                    item.text,
                )
            ),
        )
~~~~

R122 src/devtools/context/planning/materialization.py [2392:3297] lines 73–92

~~~~text
def materialize_disclosure_plan(
    *,
    plan: DisclosurePlan,
    snapshot: RepositorySnapshot,
) -> ContextDisclosure:
    """Realize every choice against retained state, without reacquisition."""
    if snapshot.id != plan.snapshot_id or snapshot.repository_id != plan.repository_id:
        msg = "Disclosure plan does not apply to the supplied repository snapshot."
        raise DisclosureMaterializationError(msg)
    items: list[MaterializedDisclosureItem] = []
    for option in plan.disclosures:
        item = option.materialize(snapshot)
        if (
            item.option_identity != option.identity
            or item.representation != option.representation
        ):
            msg = "Materialized item differs from its planned disclosure."
            raise DisclosureMaterializationError(msg)
        items.append(item)
    return ContextDisclosure(plan=plan, items=tuple(items))
~~~~

R123 src/devtools/context/planning/plan.py [1460:3377] lines 52–102

~~~~text
@dataclass(frozen=True, slots=True)
class DisclosurePlan:
    """Identify an ordered choice of disclosures for one explicit purpose.

    Construction is caller-directed. It neither retrieves nor estimates
    relevance, cost, or sufficiency.
    """

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    disclosures: tuple[PlannedDisclosure, ...]
    preceding_plan_identity: str | None = None

    def __post_init__(self) -> None:
        """Reject mixed purposes, snapshots, and repeated choices."""
        if not self.purpose.strip():
            msg = "Disclosure plan purpose must not be blank."
            raise ValueError(msg)
        if not self.disclosures:
            msg = "Disclosure plan needs at least one explicit disclosure."
            raise ValueError(msg)
        if any(
            item.purpose != self.purpose
            or item.snapshot_id != self.snapshot_id
            or item.repository_id != self.repository_id
            for item in self.disclosures
        ):
            msg = (
                "Disclosure plan contains an incompatible purpose or repository state."
            )
            raise ValueError(msg)
        if len({item.identity for item in self.disclosures}) != len(self.disclosures):
            msg = "Disclosure plan repeats an identical disclosure choice."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Identify purpose, applicability, ordered choices, and optional lineage."""
        return _digest(
            "explicit-repository-disclosure-plan-v1",
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            self.preceding_plan_identity or "",
            *(
                value
                for item in self.disclosures
                for value in (item.representation, item.identity)
            ),
        )
~~~~

R123 src/devtools/context/planning/plan.py [1496:3378] lines 53–103

~~~~text
class DisclosurePlan:
    """Identify an ordered choice of disclosures for one explicit purpose.

    Construction is caller-directed. It neither retrieves nor estimates
    relevance, cost, or sufficiency.
    """

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    disclosures: tuple[PlannedDisclosure, ...]
    preceding_plan_identity: str | None = None

    def __post_init__(self) -> None:
        """Reject mixed purposes, snapshots, and repeated choices."""
        if not self.purpose.strip():
            msg = "Disclosure plan purpose must not be blank."
            raise ValueError(msg)
        if not self.disclosures:
            msg = "Disclosure plan needs at least one explicit disclosure."
            raise ValueError(msg)
        if any(
            item.purpose != self.purpose
            or item.snapshot_id != self.snapshot_id
            or item.repository_id != self.repository_id
            for item in self.disclosures
        ):
            msg = (
                "Disclosure plan contains an incompatible purpose or repository state."
            )
            raise ValueError(msg)
        if len({item.identity for item in self.disclosures}) != len(self.disclosures):
            msg = "Disclosure plan repeats an identical disclosure choice."
            raise ValueError(msg)

    @property
    def identity(self) -> str:
        """Identify purpose, applicability, ordered choices, and optional lineage."""
        return _digest(
            "explicit-repository-disclosure-plan-v1",
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            self.preceding_plan_identity or "",
            *(
                value
                for item in self.disclosures
                for value in (item.representation, item.identity)
            ),
        )
~~~~

R124 src/devtools/context/planning/rendering.py [363:547] lines 15–20

~~~~text
@dataclass(frozen=True, slots=True)
class RenderedContextDisclosure:
    """Retain text and the exact realized Context it presents."""

    disclosure: ContextDisclosure
    text: str
~~~~

R124 src/devtools/context/planning/rendering.py [549:1355] lines 23–42

~~~~text
def render_context_disclosure(
    disclosure: ContextDisclosure,
) -> RenderedContextDisclosure:
    """Render planned item order without reselecting or changing information."""
    parts = [
        "Repository Context disclosure\n",
        f"Purpose: {disclosure.plan.purpose}\n",
        f"Plan identity: {disclosure.plan.identity}\n",
        f"Snapshot identity: {disclosure.plan.snapshot_id}\n",
        f"Items: {len(disclosure.items)}\n",
    ]
    for ordinal, item in enumerate(disclosure.items, start=1):
        parts.extend(
            (
                f"\nDisclosure item {ordinal}: {item.representation}\n",
                f"Option identity: {item.option_identity}\n",
                item.text,
            ),
        )
    return RenderedContextDisclosure(disclosure, "".join(parts))
~~~~

R124 src/devtools/context/planning/rendering.py [1357:2316] lines 45–70

~~~~text
def assemble_context_disclosure_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedContextDisclosure,
) -> ModelRequest:
    """Place realized Context after the unchanged task and copy all settings."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(prompt_content, role=task_request.prompt.role),
    )
~~~~

R125 src/devtools/context/planning/resource.py [726:3215] lines 27–86

~~~~text
@dataclass(frozen=True, slots=True)
class WholeResourceDisclosureOption:
    """Choose one exact observed resource, without inferring relevance."""

    purpose: str
    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    representation: ClassVar[str] = "whole-observed-resource-v1"

    @property
    def identity(self) -> str:
        """Identify this explicit representation of one observed occurrence."""
        return _digest(
            self.representation,
            self.purpose,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use exact retained content; reject stale, missing, or redirected state."""
        if (
            snapshot.id != self.snapshot_id
            or snapshot.repository_id != self.repository_id
        ):
            msg = "Whole-resource disclosure belongs to another snapshot."
            raise DisclosureMaterializationError(msg)
        try:
            observed = snapshot.resource_at(self.resource.address)
        except ValueError as error:
            msg = "Whole-resource disclosure source is missing."
            raise DisclosureMaterializationError(msg) from error
        if observed != self.resource:
            msg = "Whole-resource disclosure source differs from retained evidence."
            raise DisclosureMaterializationError(msg)
        text = "".join(
            (
                "Whole observed repository resource\n",
                f"Purpose: {self.purpose}\n",
                f"Snapshot identity: {self.snapshot_id}\n",
                f"Resource pointer: {observed.address}\n",
                f"Content identity: {observed.content_identity}\n",
                f"Exact source UTF-8 bytes: {len(observed.content.encode('utf-8'))}\n",
                "--- exact resource source begins ---\n",
                observed.content,
                "\n--- exact resource source ends ---\n",
            ),
        )
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(observed.address,),
            content_identities=(observed.content_identity,),
            text=text,
            native_provenance=observed,
        )
~~~~

R125 src/devtools/context/planning/resource.py [3217:3819] lines 89–104

~~~~text
def choose_whole_resource_disclosure(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    resource_address: RepositoryResourceAddress,
) -> WholeResourceDisclosureOption:
    """Record an explicit coarse representation, without reading the filesystem."""
    if not purpose.strip():
        msg = "Whole-resource disclosure purpose must not be blank."
        raise ValueError(msg)
    return WholeResourceDisclosureOption(
        purpose=purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=snapshot.resource_at(resource_address),
    )
~~~~

R133 src/devtools/context/python/function/__init__.py [0:5053] lines 1–122

~~~~text
# Copyright (c) 2026
"""Bounded Python-function Repository Intelligence and Context path."""

from devtools.context.python.function.candidates import (
    PythonFunctionAnalysisCandidateResource,
    PythonFunctionAnalysisCandidateSelection,
    PythonFunctionCandidateTokenizationError,
    PythonFunctionNameTokenCandidateEvidence,
    select_python_function_analysis_candidates,
)
from devtools.context.python.function.containment import (
    PythonFunctionDeclarationContainmentView,
    build_python_function_declaration_containment_view,
)
from devtools.context.python.function.declarations import (
    PythonFunctionDeclarationAnalysis,
    PythonFunctionDeclarationAnalysisAggregate,
    PythonFunctionDeclarationCoverage,
    PythonFunctionDeclarationDerivation,
    PythonFunctionDeclarationDerivationDefinition,
    PythonFunctionDeclarationKind,
    PythonFunctionDeclarationKnowledge,
    PythonFunctionSubject,
    PythonModuleParseError,
    PythonModuleResourceDependency,
    PythonSourceOccurrence,
    PythonSourceRange,
    analyze_python_function_declaration_resources,
    derive_python_function_declarations,
)
from devtools.context.python.function.disclosure import (
    PythonFunctionDeclarationDisclosureItem,
    PythonFunctionExactNameContextDisclosure,
    disclose_python_function_exact_name_retrieval,
)
from devtools.context.python.function.materialization import (
    MaterializedPythonFunctionContext,
    MaterializedPythonFunctionDeclaration,
    PythonFunctionSourceMaterializationError,
    materialize_python_function_disclosure_source,
)
from devtools.context.python.function.planned_reference import (
    PythonQualifiedReferenceDisclosureOption,
    choose_python_qualified_reference_disclosure,
)
from devtools.context.python.function.qualified_reference import (
    MaterializedPythonQualifiedReferenceContext,
    PythonQualifiedReferenceDisclosure,
    PythonQualifiedReferenceDisclosureError,
    RenderedPythonQualifiedReferenceContext,
    assemble_python_qualified_reference_model_request,
    disclose_python_qualified_reference,
    materialize_python_qualified_reference_source,
    render_python_qualified_reference_context,
)
from devtools.context.python.function.rendering import (
    RenderedPythonFunctionContext,
    render_materialized_python_function_context,
)
from devtools.context.python.function.request_assembly import (
    assemble_python_function_context_model_request,
)
from devtools.context.python.function.retrieval import (
    PythonFunctionExactNameQuery,
    PythonFunctionExactNameRelevanceEvidence,
    PythonFunctionExactNameResourceSelection,
    PythonFunctionExactNameRetrievalResult,
    PythonFunctionExactNameSelectedResource,
    retrieve_python_functions_by_exact_name,
    select_python_function_resources_from_exact_name_retrieval,
)

__all__ = [
    "MaterializedPythonFunctionContext",
    "MaterializedPythonFunctionDeclaration",
    "MaterializedPythonQualifiedReferenceContext",
    "PythonFunctionAnalysisCandidateResource",
    "PythonFunctionAnalysisCandidateSelection",
    "PythonFunctionCandidateTokenizationError",
    "PythonFunctionDeclarationAnalysis",
    "PythonFunctionDeclarationAnalysisAggregate",
    "PythonFunctionDeclarationContainmentView",
    "PythonFunctionDeclarationCoverage",
    "PythonFunctionDeclarationDerivation",
    "PythonFunctionDeclarationDerivationDefinition",
    "PythonFunctionDeclarationDisclosureItem",
    "PythonFunctionDeclarationKind",
    "PythonFunctionDeclarationKnowledge",
    "PythonFunctionExactNameContextDisclosure",
    "PythonFunctionExactNameQuery",
    "PythonFunctionExactNameRelevanceEvidence",
    "PythonFunctionExactNameResourceSelection",
    "PythonFunctionExactNameRetrievalResult",
    "PythonFunctionExactNameSelectedResource",
    "PythonFunctionNameTokenCandidateEvidence",
    "PythonFunctionSourceMaterializationError",
    "PythonFunctionSubject",
    "PythonModuleParseError",
    "PythonModuleResourceDependency",
    "PythonQualifiedReferenceDisclosure",
    "PythonQualifiedReferenceDisclosureError",
    "PythonQualifiedReferenceDisclosureOption",
    "PythonSourceOccurrence",
    "PythonSourceRange",
    "RenderedPythonFunctionContext",
    "RenderedPythonQualifiedReferenceContext",
    "analyze_python_function_declaration_resources",
    "assemble_python_function_context_model_request",
    "assemble_python_qualified_reference_model_request",
    "build_python_function_declaration_containment_view",
    "choose_python_qualified_reference_disclosure",
    "derive_python_function_declarations",
    "disclose_python_function_exact_name_retrieval",
    "disclose_python_qualified_reference",
    "materialize_python_function_disclosure_source",
    "materialize_python_qualified_reference_source",
    "render_materialized_python_function_context",
    "render_python_qualified_reference_context",
    "retrieve_python_functions_by_exact_name",
    "select_python_function_analysis_candidates",
    "select_python_function_resources_from_exact_name_retrieval",
]
~~~~

R138 src/devtools/context/python/function/docs/overview.md [2920:5009] lines 53–86

~~~~text
to an InformationNeed. Context Planning decides which declaration or resource
information to disclose. The current qualified-reference Context materializer
already uses the declaration's exact resource dependency and source span; it
does not need a new ownership fact. This view is not automatically projected
into the current resource-level Personalized PageRank graph.

## Context disclosure

The qualified-reference path accepts one **caller-chosen**
`PythonFunctionReferenceKnowledge` from a supplied
`PythonFunctionReferenceAnalysis`, plus an explicit purpose. It does not find,
rank, or choose a fact. Call `disclose_python_qualified_reference`, then
`materialize_python_qualified_reference_source` with the retained
`RepositorySnapshot`, then `render_python_qualified_reference_context`.
`assemble_python_qualified_reference_model_request` places that rendered
Context after the unchanged task while preserving the other request fields.

Materialization checks fact membership and derivation, the source resource
dependency, the target declaration's snapshot and subject dependency, and the
qualified import-resolution support against the supplied snapshot. It rejects
missing, stale, or redirected resources. Both source ranges are checked using
one-based lines and zero-based UTF-8 byte columns with exclusive ends. Exact
text comes only from retained snapshot contents; no working-tree file is read.
An invalid dependency or range fails observably. There is no whole-file
fallback.

The rendered relationship is distinct from the exact source text. The source
span is the qualified `ast.Name` occurrence, not a complete call expression.
`direct_call=True` means that Name occupies `ast.Call.func`; it is not a
runtime invocation claim. The target span is the established direct module-body
function declaration, not an assertion about decorators, surrounding source,
or all definitions. Reference analysis is non-exhaustive; one rendered fact
does not claim complete repository coverage. Resource addresses and locations
are navigation pointers to the identified snapshot state.
~~~~

R139 src/devtools/context/python/function/materialization.py [3523:5537] lines 98–154

~~~~text
    return MaterializedPythonFunctionContext(
        disclosure=disclosure,
        items=tuple(materialized_items),
    )


def _extract_source_segment(content: str, source_range: PythonSourceRange) -> str:
    """Extract one half-open range using UTF-8 byte-column coordinates."""
    if (
        source_range.start_line,
        source_range.start_column_utf8,
    ) > (
        source_range.end_line,
        source_range.end_column_utf8,
    ):
        msg = "Source occurrence range ends before it starts."
        raise PythonFunctionSourceMaterializationError(msg)

    encoded_lines = tuple(
        line.encode("utf-8") for line in content.splitlines(keepends=True)
    )
    start = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.start_line,
        column=source_range.start_column_utf8,
    )
    end = _absolute_byte_offset(
        encoded_lines,
        line_number=source_range.end_line,
        column=source_range.end_column_utf8,
    )
    try:
        return content.encode("utf-8")[start:end].decode("utf-8")
    except UnicodeDecodeError as error:
        msg = "Source occurrence columns do not fall on UTF-8 character boundaries."
        raise PythonFunctionSourceMaterializationError(msg) from error


def _absolute_byte_offset(
    encoded_lines: tuple[bytes, ...],
    *,
    line_number: int,
    column: int,
) -> int:
    """Translate one AST line/byte-column pair into an absolute byte offset."""
    if line_number < 1 or line_number > len(encoded_lines):
        msg = "Source occurrence line is outside the observed content."
        raise PythonFunctionSourceMaterializationError(msg)

    line = encoded_lines[line_number - 1]
    source_line = line.rstrip(b"\r\n")
    if column < 0 or column > len(source_line):
        msg = "Source occurrence column is outside the observed source line."
        raise PythonFunctionSourceMaterializationError(msg)
    return sum(len(previous) for previous in encoded_lines[: line_number - 1]) + column
~~~~

R140 src/devtools/context/python/function/planned_reference.py [890:3410] lines 28–94

~~~~text

@dataclass(frozen=True, slots=True)
class PythonQualifiedReferenceDisclosureOption:
    """Choose the existing relationship-plus-exact-source representation."""

    disclosure: PythonQualifiedReferenceDisclosure

    representation: ClassVar[str] = "qualified-python-reference-and-target-v1"

    @property
    def purpose(self) -> str:
        """Return the caller's explicit information purpose."""
        return self.disclosure.purpose

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the reference derivation's snapshot identity."""
        return self.disclosure.analysis.derivation.dependency.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Return the reference derivation's repository identity."""
        return self.disclosure.analysis.derivation.dependency.repository_id

    @property
    def identity(self) -> str:
        """Retain the existing fact, derivation, and caller-purpose identity."""
        return self.disclosure.identity

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use the existing fully validated Python-specific materializer."""
        materialized = materialize_python_qualified_reference_source(
            disclosure=self.disclosure,
            snapshot=snapshot,
        )
        rendered = render_python_qualified_reference_context(materialized)
        reference = self.disclosure.reference
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(
                reference.occurrence.resource_address,
                reference.target_declaration.support.resource_address,
            ),
            content_identities=(
                materialized.source_content_identity,
                materialized.target_content_identity,
            ),
            text=rendered.text,
            native_provenance=materialized,
        )


def choose_python_qualified_reference_disclosure(
    *,
    purpose: str,
    analysis: PythonDeclarationReferenceAnalysis,
    reference: PythonDeclarationReferenceKnowledge,
) -> PythonQualifiedReferenceDisclosureOption:
    """Record an exact caller choice without discovering or ranking facts."""
    return PythonQualifiedReferenceDisclosureOption(
        disclose_python_qualified_reference(
            purpose=purpose,
            analysis=analysis,
            reference=reference,
        ),
    )
~~~~

R140 src/devtools/context/python/function/planned_reference.py [891:2898] lines 29–78

~~~~text
@dataclass(frozen=True, slots=True)
class PythonQualifiedReferenceDisclosureOption:
    """Choose the existing relationship-plus-exact-source representation."""

    disclosure: PythonQualifiedReferenceDisclosure

    representation: ClassVar[str] = "qualified-python-reference-and-target-v1"

    @property
    def purpose(self) -> str:
        """Return the caller's explicit information purpose."""
        return self.disclosure.purpose

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the reference derivation's snapshot identity."""
        return self.disclosure.analysis.derivation.dependency.snapshot_id

    @property
    def repository_id(self) -> RepositoryId:
        """Return the reference derivation's repository identity."""
        return self.disclosure.analysis.derivation.dependency.repository_id

    @property
    def identity(self) -> str:
        """Retain the existing fact, derivation, and caller-purpose identity."""
        return self.disclosure.identity

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Use the existing fully validated Python-specific materializer."""
        materialized = materialize_python_qualified_reference_source(
            disclosure=self.disclosure,
            snapshot=snapshot,
        )
        rendered = render_python_qualified_reference_context(materialized)
        reference = self.disclosure.reference
        return MaterializedDisclosureItem(
            option_identity=self.identity,
            representation=self.representation,
            resource_addresses=(
                reference.occurrence.resource_address,
                reference.target_declaration.support.resource_address,
            ),
            content_identities=(
                materialized.source_content_identity,
                materialized.target_content_identity,
            ),
            text=rendered.text,
            native_provenance=materialized,
        )
~~~~

R140 src/devtools/context/python/function/planned_reference.py [2900:3410] lines 81–94

~~~~text
def choose_python_qualified_reference_disclosure(
    *,
    purpose: str,
    analysis: PythonDeclarationReferenceAnalysis,
    reference: PythonDeclarationReferenceKnowledge,
) -> PythonQualifiedReferenceDisclosureOption:
    """Record an exact caller choice without discovering or ranking facts."""
    return PythonQualifiedReferenceDisclosureOption(
        disclose_python_qualified_reference(
            purpose=purpose,
            analysis=analysis,
            reference=reference,
        ),
    )
~~~~

R141 src/devtools/context/python/function/qualified_reference.py [4325:9062] lines 124–227

~~~~text
def materialize_python_qualified_reference_source(
    *,
    disclosure: PythonQualifiedReferenceDisclosure,
    snapshot: RepositorySnapshot,
) -> MaterializedPythonQualifiedReferenceContext:
    """Validate both dependencies and extract only the recorded source spans."""
    # Recheck membership because immutable values can still be constructed directly.
    selected = disclose_python_qualified_reference(
        purpose=disclosure.purpose,
        analysis=disclosure.analysis,
        reference=disclosure.reference,
    )
    reference = selected.reference
    dependency = selected.analysis.derivation.dependency
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        dependency.snapshot_id != snapshot.id
        or dependency.repository_id != snapshot.repository_id
        or reference.occurrence.snapshot_id != snapshot.id
        or reference.occurrence.resource_address != dependency.resource.address
    ):
        msg = "Reference source dependency does not match the supplied snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source_resource = _snapshot_resource(
        snapshot,
        reference.occurrence.resource_address,
        label="source",
    )
    if source_resource != dependency.resource:
        msg = "Reference source content differs from its derivation dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)

    if (
        target.support.snapshot_id != snapshot.id
        or target.subject.snapshot_id != snapshot.id
    ):
        msg = "Target declaration belongs to another snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_resource = _snapshot_resource(
        snapshot,
        target.support.resource_address,
        label="target",
    )
    target_dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=target_resource,
    )
    if target.subject.resource_dependency_identity != target_dependency.identity:
        msg = "Target declaration resource or content differs from its dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if target_resource != reference.target_resource:
        msg = "Target resource differs from the retained Reference support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    supporting_interpretation = (
        reference.direct_member_resolution.module
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target
        if reference.imported_member_resolution is not None
        else None
    )
    if (
        supporting_interpretation is None
        or supporting_interpretation.snapshot_id != snapshot.id
        or supporting_interpretation.repository_id != snapshot.repository_id
        or supporting_interpretation.resource != target_resource
    ):
        msg = "Target declaration differs from its qualified resolution support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_analysis = (
        reference.direct_member_resolution.function_analysis
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target_function_analysis
        if reference.imported_member_resolution is not None
        else None
    )
    if target_analysis is not None and (
        target not in target_analysis.declarations
        or target_analysis.derivation.dependency.snapshot_id != snapshot.id
        or target_analysis.derivation.dependency.repository_id != snapshot.repository_id
        or target_analysis.derivation.dependency.resource != target_resource
    ):
        msg = "Target declaration differs from its retained declaration analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)

    return MaterializedPythonQualifiedReferenceContext(
        disclosure=selected,
        snapshot_id=snapshot.id,
        source_content_identity=source_resource.content_identity,
        target_content_identity=target_resource.content_identity,
        reference_name_text=_extract_source_segment(
            source_resource.content,
            reference.occurrence.source_range,
        ),
        target_declaration_text=_extract_source_segment(
            target_resource.content,
            target.support.source_range,
        ),
    )
~~~~

R141 src/devtools/context/python/function/qualified_reference.py [4376:9296] lines 125–233

~~~~text
    *,
    disclosure: PythonQualifiedReferenceDisclosure,
    snapshot: RepositorySnapshot,
) -> MaterializedPythonQualifiedReferenceContext:
    """Validate both dependencies and extract only the recorded source spans."""
    # Recheck membership because immutable values can still be constructed directly.
    selected = disclose_python_qualified_reference(
        purpose=disclosure.purpose,
        analysis=disclosure.analysis,
        reference=disclosure.reference,
    )
    reference = selected.reference
    dependency = selected.analysis.derivation.dependency
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        dependency.snapshot_id != snapshot.id
        or dependency.repository_id != snapshot.repository_id
        or reference.occurrence.snapshot_id != snapshot.id
        or reference.occurrence.resource_address != dependency.resource.address
    ):
        msg = "Reference source dependency does not match the supplied snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source_resource = _snapshot_resource(
        snapshot,
        reference.occurrence.resource_address,
        label="source",
    )
    if source_resource != dependency.resource:
        msg = "Reference source content differs from its derivation dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)

    if (
        target.support.snapshot_id != snapshot.id
        or target.subject.snapshot_id != snapshot.id
    ):
        msg = "Target declaration belongs to another snapshot."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_resource = _snapshot_resource(
        snapshot,
        target.support.resource_address,
        label="target",
    )
    target_dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=target_resource,
    )
    if target.subject.resource_dependency_identity != target_dependency.identity:
        msg = "Target declaration resource or content differs from its dependency."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if target_resource != reference.target_resource:
        msg = "Target resource differs from the retained Reference support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    supporting_interpretation = (
        reference.direct_member_resolution.module
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target
        if reference.imported_member_resolution is not None
        else None
    )
    if (
        supporting_interpretation is None
        or supporting_interpretation.snapshot_id != snapshot.id
        or supporting_interpretation.repository_id != snapshot.repository_id
        or supporting_interpretation.resource != target_resource
    ):
        msg = "Target declaration differs from its qualified resolution support."
        raise PythonQualifiedReferenceDisclosureError(msg)
    target_analysis = (
        reference.direct_member_resolution.function_analysis
        if reference.route is PythonDeclarationReferenceRoute.IMPORTED_MEMBER
        and reference.direct_member_resolution is not None
        else reference.imported_member_resolution.target_function_analysis
        if reference.imported_member_resolution is not None
        else None
    )
    if target_analysis is not None and (
        target not in target_analysis.declarations
        or target_analysis.derivation.dependency.snapshot_id != snapshot.id
        or target_analysis.derivation.dependency.repository_id != snapshot.repository_id
        or target_analysis.derivation.dependency.resource != target_resource
    ):
        msg = "Target declaration differs from its retained declaration analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)

    return MaterializedPythonQualifiedReferenceContext(
        disclosure=selected,
        snapshot_id=snapshot.id,
        source_content_identity=source_resource.content_identity,
        target_content_identity=target_resource.content_identity,
        reference_name_text=_extract_source_segment(
            source_resource.content,
            reference.occurrence.source_range,
        ),
        target_declaration_text=_extract_source_segment(
            target_resource.content,
            target.support.source_range,
        ),
    )


def render_python_qualified_reference_context(
    context: MaterializedPythonQualifiedReferenceContext,
) -> RenderedPythonQualifiedReferenceContext:
    """Render the established relationship separately from exact source text."""
~~~~

R141 src/devtools/context/python/function/qualified_reference.py [9064:11986] lines 230–288

~~~~text
def render_python_qualified_reference_context(
    context: MaterializedPythonQualifiedReferenceContext,
) -> RenderedPythonQualifiedReferenceContext:
    """Render the established relationship separately from exact source text."""
    reference = context.disclosure.reference
    target = reference.target_declaration
    if not isinstance(target, PythonFunctionDeclarationKnowledge):
        msg = "Qualified Reference target is not a supported function."
        raise PythonQualifiedReferenceDisclosureError(msg)
    source = reference.occurrence
    source_range = source.source_range
    target_range = target.support.source_range
    call_meaning = (
        "Yes: the qualified Name occupies ast.Call.func; "
        "no runtime invocation is asserted."
        if reference.direct_call
        else "No: this qualified Name is a Reference without the "
        "direct-call syntax tag."
    )
    text = "".join(
        (
            "Qualified Python Reference Context\n",
            f"Purpose: {context.disclosure.purpose}\n",
            f"Disclosure identity: {context.disclosure.identity}\n",
            f"Snapshot identity: {context.snapshot_id}\n",
            f"Reference fact identity: {reference.identity}\n",
            f"Reference derivation identity: {reference.derivation_identity}\n",
            f"Qualified relationship: {reference.PROPOSITION}\n",
            f"Resolution path: {reference.route.value}\n",
            f"Direct Call syntax: {call_meaning}\n",
            (
                "Coverage: qualified positive fact only; Reference analysis is "
                "non-exhaustive.\n"
            ),
            f"Source resource pointer: {source.resource_address}\n",
            f"Source content identity: {context.source_content_identity}\n",
            f"Reference Name location: {_location(source_range)}\n",
            (
                "Exact Reference Name UTF-8 bytes: "
                f"{len(context.reference_name_text.encode('utf-8'))}\n"
            ),
            "--- exact Reference Name begins ---\n",
            context.reference_name_text,
            "\n--- exact Reference Name ends ---\n",
            f"Target resource pointer: {target.support.resource_address}\n",
            f"Target content identity: {context.target_content_identity}\n",
            f"Target declared name: {target.declared_name}\n",
            f"Target declaration kind: {target.declaration_kind.value}\n",
            f"Target declaration location: {_location(target_range)}\n",
            (
                "Exact target declaration UTF-8 bytes: "
                f"{len(context.target_declaration_text.encode('utf-8'))}\n"
            ),
            "--- exact target declaration begins ---\n",
            context.target_declaration_text,
            "\n--- exact target declaration ends ---\n",
        ),
    )
    return RenderedPythonQualifiedReferenceContext(context, text)
~~~~

R142 src/devtools/context/python/function/rendering.py [0:3219] lines 1–88

~~~~text
# Copyright (c) 2026
"""Deterministic text rendering for materialized Python function Context.

The renderer serializes only the existing bounded Context representation. Source
markers are visual framing, not a collision-free or machine-parseable protocol;
the recorded UTF-8 byte length identifies the unchanged source payload.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

if TYPE_CHECKING:
    from devtools.context.python.function.materialization import (
        MaterializedPythonFunctionContext,
        MaterializedPythonFunctionDeclaration,
    )


@dataclass(frozen=True, slots=True)
class RenderedPythonFunctionContext:
    """Retain model-facing text and its source materialized Context."""

    materialized_context: MaterializedPythonFunctionContext
    text: str

    FORMAT: ClassVar[str] = "python-function-context-text-v1"


def render_materialized_python_function_context(
    context: MaterializedPythonFunctionContext,
) -> RenderedPythonFunctionContext:
    """Render the bounded Context without acquiring or inferring information."""
    query = context.disclosure.retrieval.query
    parts = [
        "Python function Context\n",
        f"Exact declared-name purpose: {query.declared_name}\n",
        "Selection: all exact-name matches in retrieval order\n",
        f"Selected declarations: {len(context.items)}\n",
        (
            "Bounded meaning: each item is established only as a direct "
            "module-body Python source occurrence that syntactically declares "
            "a snapshot-local function subject.\n"
        ),
    ]
    if not context.items:
        parts.append(
            "No declarations were selected from the supplied exact-name "
            "retrieval result.\n",
        )

    for ordinal, item in enumerate(context.items, start=1):
        parts.extend(_render_item(item, ordinal=ordinal))

    return RenderedPythonFunctionContext(
        materialized_context=context,
        text="".join(parts),
    )


def _render_item(
    item: MaterializedPythonFunctionDeclaration,
    *,
    ordinal: int,
) -> tuple[str, ...]:
    """Render metadata around one unchanged exact-source payload."""
    disclosure_item = item.disclosure_item
    occurrence = disclosure_item.source_occurrence
    source_range = occurrence.source_range
    source_length = len(item.source_text.encode("utf-8"))
    return (
        f"\nSelected declaration {ordinal}\n",
        f"Declared name: {disclosure_item.declared_name}\n",
        f"Declaration kind: {disclosure_item.declaration_kind.value}\n",
        f"Repository-relative resource: {occurrence.resource_address}\n",
        (
            "Source location: "
            f"{source_range.start_line}:{source_range.start_column_utf8}-"
            f"{source_range.end_line}:{source_range.end_column_utf8} "
            "(one-based lines; zero-based UTF-8 byte columns; exclusive end)\n"
        ),
        f"Bounded proposition: {disclosure_item.proposition}\n",
        f"Exact source UTF-8 byte length: {source_length}\n",
        "--- exact source begins ---\n",
        item.source_text,
        "\n--- exact source ends ---\n",
    )
~~~~

R143 src/devtools/context/python/function/request_assembly.py [0:1689] lines 1–51

~~~~text
# Copyright (c) 2026
"""Bounded model-request assembly for rendered Python function Context.

The caller's existing request supplies the task Prompt and every other request
semantic. Assembly changes only Prompt content, placing the unchanged rendered
Context after the unchanged task. Section markers are visual framing rather
than a universal or machine-parseable prompt protocol.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from devtools.context.python.function.rendering import (
        RenderedPythonFunctionContext,
    )


def assemble_python_function_context_model_request(
    *,
    task_request: ModelRequest,
    context: RenderedPythonFunctionContext,
) -> ModelRequest:
    """Return a request preserving task and request semantics around Context."""
    task_text = task_request.prompt.content
    prompt_content = "".join(
        (
            f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n",
            "--- task/instruction begins ---\n",
            task_text,
            "\n--- task/instruction ends ---\n\n",
            (
                "Supporting repository Context UTF-8 byte length: "
                f"{len(context.text.encode('utf-8'))}\n"
            ),
            "--- supporting repository Context begins ---\n",
            context.text,
            "\n--- supporting repository Context ends ---\n",
        ),
    )
    return replace(
        task_request,
        prompt=Prompt(
            content=prompt_content,
            role=task_request.prompt.role,
        ),
    )
~~~~

R155 src/devtools/context/python/modules/interpretation.py [5775:8575] lines 173–252

~~~~text
    interpretations: list[PythonModuleInterpretation] = []
    exclusions: list[PythonModuleInterpretationExclusion] = []
    for address in selected_addresses:
        resource = snapshot.resource_at(address)
        interpretation, reason = _interpret_resource(
            repository_id=snapshot.repository_id,
            snapshot_id=snapshot.id,
            resource=resource,
            module_root=module_root,
        )
        if interpretation is None:
            exclusions.append(PythonModuleInterpretationExclusion(
                resource=resource,
                module_root=module_root,
                reason=cast("PythonModuleInterpretationExclusionReason", reason),
            ))
        else:
            interpretations.append(interpretation)

    return PythonModuleInterpretationAnalysis(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        module_root=module_root,
        interpretations=tuple(interpretations),
        exclusions=tuple(exclusions),
    )


def _interpret_resource(
    *,
    repository_id: RepositoryId,
    snapshot_id: RepositorySnapshotId,
    resource: RepositoryResourceOccurrence,
    module_root: PythonModuleRoot,
) -> tuple[
    PythonModuleInterpretation | None,
    PythonModuleInterpretationExclusionReason | None,
]:
    address_parts = resource.address.parts
    root_parts = module_root.parts
    if address_parts[: len(root_parts)] != root_parts:
        return None, PythonModuleInterpretationExclusionReason.OUTSIDE_MODULE_ROOT

    relative_parts = address_parts[len(root_parts) :]
    filename = relative_parts[-1]
    if not filename.endswith(".py"):
        return None, PythonModuleInterpretationExclusionReason.NON_PYTHON_RESOURCE

    stem = filename.removesuffix(".py")
    if stem == "__init__":
        if len(relative_parts) == 1:
            return None, PythonModuleInterpretationExclusionReason.ROOT_LEVEL_INIT
        name_parts = relative_parts[:-1]
        kind = PythonModuleKind.PACKAGE
    else:
        name_parts = (*relative_parts[:-1], stem)
        kind = PythonModuleKind.ORDINARY

    if not all(part.isidentifier() for part in name_parts):
        return None, PythonModuleInterpretationExclusionReason.NON_IDENTIFIER_COMPONENT
    return (
        PythonModuleInterpretation(
            repository_id=repository_id,
            snapshot_id=snapshot_id,
            resource=resource,
            module_root=module_root,
            dotted_name=".".join(name_parts),
            kind=kind,
        ),
        None,
    )


def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
~~~~

R168 src/devtools/context/python/references/declarations/analysis.py [1382:5699] lines 40–160

~~~~text


def derive_python_declaration_references(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress,
    module_universe: PythonModuleInterpretationUniverse,
    source_interpretations: Sequence[PythonModuleInterpretation] = (),
) -> PythonDeclarationReferenceAnalysis:
    """Assess static Name and outermost Attribute loads over retained content."""
    resource = snapshot.resource_at(resource_address)
    if module_universe.repository_id != snapshot.repository_id or any(
        item.snapshot_id != snapshot.id
        or item.resource != snapshot.resource_at(item.resource.address)
        for item in module_universe.interpretations
    ):
        msg = "Reference module universe differs from the snapshot."
        raise ValueError(msg)
    if any(
        item.snapshot_id != snapshot.id or item.resource != resource
        for item in source_interpretations
    ):
        msg = "Reference source interpretation differs from the snapshot."
        raise ValueError(msg)
    tree = ast.parse(
        resource.content,
        filename=str(resource_address),
        feature_version=(3, 12),
    )
    imports = derive_python_import_declarations(
        snapshot,
        resource_address=resource_address,
    )
    functions = derive_python_function_declarations(
        snapshot,
        resource_address=resource_address,
    )
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=resource_address,
    )
    derivation = PythonDeclarationReferenceDerivation(
        PythonModuleResourceDependency(snapshot.id, snapshot.repository_id, resource),
        module_universe.identity,
        tuple(sorted(item.identity for item in source_interpretations)),
    )
    bindings, uncertain_namespace = _module_bindings(
        tree,
        imports,
        functions.declarations,
        classes.classes,
    )
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    candidates = tuple(
        sorted(
            (
                node
                for node in ast.walk(tree)
                if isinstance(node, (ast.Name, ast.Attribute))
                and isinstance(node.ctx, ast.Load)
                and not _is_inner_attribute(node, parents.get(node))
            ),
            key=lambda node: (
                node.lineno,
                node.col_offset,
                cast("int", node.end_lineno),
                cast("int", node.end_col_offset),
            ),
        ),
    )
    assessments: list[PythonDeclarationReferenceAssessment] = []
    references: list[PythonDeclarationReferenceKnowledge] = []
    for node in candidates:
        occurrence = _occurrence(snapshot, resource_address, node)
        source_text = ast.get_source_segment(resource.content, node)
        if source_text is None:
            msg = "Reference candidate lacks retained exact source text."
            raise ValueError(msg)
        resolved = _resolve(
            snapshot,
            node,
            parents,
            bindings,
            uncertain_namespace,
            imports,
            module_universe,
            source_interpretations,
            classes.classes,
            classes.methods,
        )
        reference = None
        if resolved.target is not None and resolved.route is not None:
            target_resource = snapshot.resource_at(
                resolved.target.support.resource_address,
            )
            reference = PythonDeclarationReferenceKnowledge(
                derivation.identity,
                occurrence,
                resolved.target,
                target_resource,
                resolved.route,
                _is_direct_call(node, parents.get(node)),
                resolved.import_declaration,
                resolved.module_resolution,
                resolved.direct_member_resolution,
                resolved.imported_member_resolution,
                resolved.containing_class,
            )
            references.append(reference)
        assessments.append(
            PythonDeclarationReferenceAssessment(
                occurrence,
                source_text,
                resolved.outcome,
                reference,
            ),
        )
~~~~

R174 src/devtools/context/repository/__init__.py [0:1872] lines 1–61

~~~~text
# Copyright (c) 2026
"""Public repository identity, state, observation, and discovery API."""

from devtools.context.repository.corpus import (
    RepositoryTextCorpus,
    RepositoryTextCorpusDefinition,
    RepositoryTextCorpusId,
    define_repository_text_corpus,
    realize_repository_text_corpus,
)
from devtools.context.repository.discovery import (
    RepositoryResourceDiscovery,
    RepositoryResourceDiscoveryError,
    discover_repository_resource_addresses,
)
from devtools.context.repository.document import (
    RepositoryTextDocument,
    RepositoryTextDocumentCollection,
    RepositoryTextDocumentId,
    represent_repository_text_corpus,
)
from devtools.context.repository.identity import Repository, RepositoryId
from devtools.context.repository.observation import (
    RepositoryObservationError,
    observe_repository_resource,
    observe_repository_resources,
)
from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)

__all__ = [
    "ContentIdentity",
    "Repository",
    "RepositoryId",
    "RepositoryObservationError",
    "RepositoryResourceAddress",
    "RepositoryResourceDiscovery",
    "RepositoryResourceDiscoveryError",
    "RepositoryResourceOccurrence",
    "RepositorySnapshot",
    "RepositorySnapshotId",
    "RepositoryTextCorpus",
    "RepositoryTextCorpusDefinition",
    "RepositoryTextCorpusId",
    "RepositoryTextDocument",
    "RepositoryTextDocumentCollection",
    "RepositoryTextDocumentId",
    "define_repository_text_corpus",
    "discover_repository_resource_addresses",
    "observe_repository_resource",
    "observe_repository_resources",
    "realize_repository_text_corpus",
    "represent_repository_text_corpus",
]
~~~~

R178 src/devtools/context/repository/identity.py [0:1076] lines 1–41

~~~~text
# Copyright (c) 2026
"""Nominal identity for one logical repository."""

from __future__ import annotations

from dataclasses import dataclass

from devtools.core.identity import Identity


@dataclass(frozen=True, slots=True)
class RepositoryId:
    """Identify one logical Repository independently of its location or state."""

    value: Identity

    @classmethod
    def new(cls) -> RepositoryId:
        """Generate a new nominal Repository identity."""
        return cls(Identity.new())

    @classmethod
    def parse(cls, value: str) -> RepositoryId:
        """Parse a Repository identity from UUID text."""
        return cls(Identity.parse(value))

    def __str__(self) -> str:
        """Return canonical UUID text."""
        return str(self.value)


@dataclass(frozen=True, slots=True)
class Repository:
    """Represent a logical software repository across changing states."""

    id: RepositoryId

    @classmethod
    def new(cls) -> Repository:
        """Create a logical Repository with a new nominal identity."""
        return cls(RepositoryId.new())
~~~~

R179 src/devtools/context/repository/observation.py [0:332] lines 1–7

~~~~text
# Copyright (c) 2026
"""Bounded observation of explicitly addressed repository text resources.

Observation is complete for exactly the finite caller-requested collection of
UTF-8 text resources. Resources are acquired sequentially in canonical address
order; the operation makes no atomic, repository-wide, or discovery claim.
"""
~~~~

R179 src/devtools/context/repository/observation.py [0:4213] lines 1–119

~~~~text
# Copyright (c) 2026
"""Bounded observation of explicitly addressed repository text resources.

Observation is complete for exactly the finite caller-requested collection of
UTF-8 text resources. Resources are acquired sequentially in canonical address
order; the operation makes no atomic, repository-wide, or discovery claim.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from collections.abc import Collection

    from devtools.context.repository.identity import Repository

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.repository.snapshot import (
    RepositorySnapshot,
    RepositorySnapshotId,
)
from devtools.core.paths import ResolvedPath, resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read

_CONTENT_IDENTITY_SEMANTICS = "decoded-utf8-text-sha256-v1"
_SNAPSHOT_IDENTITY_SEMANTICS = RepositorySnapshot.OBSERVATION_SEMANTICS


class RepositoryObservationError(Exception):
    """Reject an observation that cannot satisfy its declared boundary."""


def observe_repository_resource(
    *,
    repository: Repository,
    root: ResolvedPath,
    address: RepositoryResourceAddress,
    maximum_resource_bytes: int,
) -> RepositorySnapshot:
    """Observe one required UTF-8 text resource through one bounded read.

    Success means the exact requested address resolved beneath ``root`` and was
    read completely according to :func:`devtools.resources.filesystem.read`.
    The operation does not discover other resources or claim an atomic view of
    the containing filesystem.

    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If the required resource cannot be read completely.
    """
    return observe_repository_resources(
        repository=repository,
        root=root,
        addresses=(address,),
        maximum_resource_bytes=maximum_resource_bytes,
    )


def observe_repository_resources(
    *,
    repository: Repository,
    root: ResolvedPath,
    addresses: Collection[RepositoryResourceAddress],
    maximum_resource_bytes: int,
) -> RepositorySnapshot:
    """Observe a finite explicit collection of required UTF-8 text resources.

    Addresses are canonicalized into repository-relative lexical order before
    sequential acquisition. Success means every distinct requested address was
    read completely. A failure raises without publishing a partial snapshot.
    Equivalent collections therefore produce equivalent state regardless of
    caller ordering or observation root, but no simultaneous filesystem view is
    claimed.

    :raises ValueError: If the byte bound is nonpositive or an address is repeated.
    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If any required resource cannot be read completely.
    """
    requested_addresses = tuple(addresses)
    if maximum_resource_bytes <= 0:
        msg = "Repository observation maximum resource bytes must be positive."
        raise ValueError(msg)
    if len(set(requested_addresses)) != len(requested_addresses):
        msg = "Repository observation resource addresses must be distinct."
        raise ValueError(msg)

    ordered_addresses = tuple(
        sorted(requested_addresses, key=lambda requested: requested.value),
    )
    normalized_root = resolve_path(root.value)
    resources = tuple(
        _observe_resource(
            root=normalized_root,
            address=requested,
            maximum_resource_bytes=maximum_resource_bytes,
        )
        for requested in ordered_addresses
    )
    snapshot_id = RepositorySnapshotId(
        _semantic_digest(
            _SNAPSHOT_IDENTITY_SEMANTICS,
            str(repository.id),
            *(
                value
                for resource in resources
                for value in (
                    str(resource.address),
                    str(resource.content_identity),
                )
            ),
        ),
    )
    return RepositorySnapshot(
~~~~

R179 src/devtools/context/repository/observation.py [2090:4309] lines 65–123

~~~~text
def observe_repository_resources(
    *,
    repository: Repository,
    root: ResolvedPath,
    addresses: Collection[RepositoryResourceAddress],
    maximum_resource_bytes: int,
) -> RepositorySnapshot:
    """Observe a finite explicit collection of required UTF-8 text resources.

    Addresses are canonicalized into repository-relative lexical order before
    sequential acquisition. Success means every distinct requested address was
    read completely. A failure raises without publishing a partial snapshot.
    Equivalent collections therefore produce equivalent state regardless of
    caller ordering or observation root, but no simultaneous filesystem view is
    claimed.

    :raises ValueError: If the byte bound is nonpositive or an address is repeated.
    :raises RepositoryObservationError: If resolution escapes the supplied root.
    :raises FilesystemError: If any required resource cannot be read completely.
    """
    requested_addresses = tuple(addresses)
    if maximum_resource_bytes <= 0:
        msg = "Repository observation maximum resource bytes must be positive."
        raise ValueError(msg)
    if len(set(requested_addresses)) != len(requested_addresses):
        msg = "Repository observation resource addresses must be distinct."
        raise ValueError(msg)

    ordered_addresses = tuple(
        sorted(requested_addresses, key=lambda requested: requested.value),
    )
    normalized_root = resolve_path(root.value)
    resources = tuple(
        _observe_resource(
            root=normalized_root,
            address=requested,
            maximum_resource_bytes=maximum_resource_bytes,
        )
        for requested in ordered_addresses
    )
    snapshot_id = RepositorySnapshotId(
        _semantic_digest(
            _SNAPSHOT_IDENTITY_SEMANTICS,
            str(repository.id),
            *(
                value
                for resource in resources
                for value in (
                    str(resource.address),
                    str(resource.content_identity),
                )
            ),
        ),
    )
    return RepositorySnapshot(
        id=snapshot_id,
        repository_id=repository.id,
        resources=resources,
    )
~~~~

R179 src/devtools/context/repository/observation.py [4311:5347] lines 126–158

~~~~text
def _observe_resource(
    *,
    root: ResolvedPath,
    address: RepositoryResourceAddress,
    maximum_resource_bytes: int,
) -> RepositoryResourceOccurrence:
    """Acquire one required occurrence within a normalized observation root."""
    candidate = resolve_path(
        Path(*address.parts),
        base_directory=root.value,
    )
    if not candidate.value.is_relative_to(root.value):
        msg = f"Repository resource resolves outside the observation root: {address}."
        raise RepositoryObservationError(msg)

    file = cast(
        "TextFile",
        read(
            candidate,
            file_format=FileFormat.TEXT,
            max_bytes=maximum_resource_bytes,
        ),
    )
    content_identity = ContentIdentity(
        _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, file.content),
    )
    return RepositoryResourceOccurrence(
        address=address,
        content_identity=content_identity,
        content=file.content,
        encoding=file.encoding,
        byte_size=file.byte_size,
    )
~~~~

R180 src/devtools/context/repository/resource.py [255:2289] lines 12–71

~~~~text

@dataclass(frozen=True, slots=True)
class RepositoryResourceAddress:
    """Represent one canonical POSIX-style path relative to a repository root."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty, absolute, noncanonical, or traversing addresses."""
        if not self.value:
            msg = "Repository resource address cannot be empty."
            raise ValueError(msg)
        if "\\" in self.value:
            msg = "Repository resource address must use forward slashes."
            raise ValueError(msg)

        posix_path = PurePosixPath(self.value)
        windows_path = PureWindowsPath(self.value)
        if posix_path.is_absolute() or windows_path.drive:
            msg = "Repository resource address must be relative."
            raise ValueError(msg)

        parts = self.value.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            msg = "Repository resource address must be canonical without traversal."
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return canonical repository-relative path components."""
        return tuple(self.value.split("/"))

    def __str__(self) -> str:
        """Return the canonical repository-relative address."""
        return self.value


@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify decoded UTF-8 text independently of its repository address."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Content identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value


@dataclass(frozen=True, slots=True)
class RepositoryResourceOccurrence:
    """Retain one addressed text occurrence and its independent content identity."""

    address: RepositoryResourceAddress
    content_identity: ContentIdentity
    content: str
    encoding: str
~~~~

R180 src/devtools/context/repository/resource.py [256:1566] lines 13–46

~~~~text
@dataclass(frozen=True, slots=True)
class RepositoryResourceAddress:
    """Represent one canonical POSIX-style path relative to a repository root."""

    value: str

    def __post_init__(self) -> None:
        """Reject empty, absolute, noncanonical, or traversing addresses."""
        if not self.value:
            msg = "Repository resource address cannot be empty."
            raise ValueError(msg)
        if "\\" in self.value:
            msg = "Repository resource address must use forward slashes."
            raise ValueError(msg)

        posix_path = PurePosixPath(self.value)
        windows_path = PureWindowsPath(self.value)
        if posix_path.is_absolute() or windows_path.drive:
            msg = "Repository resource address must be relative."
            raise ValueError(msg)

        parts = self.value.split("/")
        if any(part in {"", ".", ".."} for part in parts):
            msg = "Repository resource address must be canonical without traversal."
            raise ValueError(msg)

    @property
    def parts(self) -> tuple[str, ...]:
        """Return canonical repository-relative path components."""
        return tuple(self.value.split("/"))

    def __str__(self) -> str:
        """Return the canonical repository-relative address."""
        return self.value
~~~~

R180 src/devtools/context/repository/resource.py [1568:2017] lines 49–61

~~~~text
@dataclass(frozen=True, slots=True)
class ContentIdentity:
    """Identify decoded UTF-8 text independently of its repository address."""

    value: str

    def __post_init__(self) -> None:
        """Validate the local SHA-256 hexadecimal representation."""
        _validate_sha256(self.value, label="Content identity")

    def __str__(self) -> str:
        """Return the local hexadecimal identity representation."""
        return self.value
~~~~

R180 src/devtools/context/repository/resource.py [2019:2308] lines 64–72

~~~~text
@dataclass(frozen=True, slots=True)
class RepositoryResourceOccurrence:
    """Retain one addressed text occurrence and its independent content identity."""

    address: RepositoryResourceAddress
    content_identity: ContentIdentity
    content: str
    encoding: str
    byte_size: int
~~~~

R181 src/devtools/context/repository/snapshot.py [906:2018] lines 34–61

~~~~text
@dataclass(frozen=True, slots=True)
class RepositorySnapshot:
    """Represent complete state for an explicit required resource collection."""

    OBSERVATION_SEMANTICS: ClassVar[str] = "explicit-required-text-resources-sha256-v1"

    id: RepositorySnapshotId
    repository_id: RepositoryId
    resources: tuple[RepositoryResourceOccurrence, ...]

    @property
    def resource(self) -> RepositoryResourceOccurrence:
        """Return the sole occurrence for compatible single-resource consumers."""
        if len(self.resources) != 1:
            msg = "Repository snapshot does not contain exactly one resource."
            raise ValueError(msg)
        return self.resources[0]

    def resource_at(
        self,
        address: RepositoryResourceAddress,
    ) -> RepositoryResourceOccurrence:
        """Return the observed occurrence at one exact requested address."""
        for resource in self.resources:
            if resource.address == address:
                return resource
        msg = f"Repository snapshot does not contain resource address: {address}."
        raise ValueError(msg)
~~~~

R254 src/devtools/models/interaction/docs/overview.md [0:4266] lines 1–74

~~~~text
# `devtools.models.interaction`

This package owns one bounded model invocation boundary:

```text
ModelRequest -> ModelInteraction -> ModelResponse
```

`ModelRequest` is an immutable semantic invocation value containing a `Prompt`,
immutable portable `ModelSettings`, an optional provider continuation, and an
optional typed provider request extension. `Prompt` is per-invocation
model-facing input and deliberately has no durable conversation-message
identity or local conversation timestamp. `ModelResponse`
contains model output, its source, optional provider continuation, optional
provider-reported `ModelUsage`, and optional provider-reported
`ModelTermination`, plus optional separately returned textual reasoning. Usage
retains only reported input, output, and total token counts; absent counts are
not estimated. Termination retains only a normal stop, an output-limit end, or a
tool-call end when the provider reports one. Reasoning remains distinct from
visible response content and is never substituted or concatenated into it.
None of these provider facts is automatically retained as a
`ConversationMessage` or treated as an Agent result.

`ModelInteraction` performs provider request/response translation and exposes
provider-local failure and continuation behavior. It does not own conversation
history, goals, tools, authorization, Runtime orchestration, or model-serving
lifecycle. `ConversationRef` and `InteractionSource` are narrow model-provider
values used at this boundary.

`ModelSettings.maximum_output_tokens` is an optional positive,
provider-neutral completion-token limit for that single invocation. Its absence
requests no cap. This request constraint is distinct from provider-reported
`ModelUsage`, model context-window capacity, and any future Context or run
budget. An adapter must honor a supplied limit or reject it explicitly.

`ModelSettings.thinking_enabled` is optional: `None` preserves provider
defaults, while `True` or `False` explicitly requests thinking on or off. An
adapter must honor an explicit value or reject it; it must not silently ignore
the request.

`ProviderRequestSettings` is an immutable typed extension seam for one
provider's per-request settings. Portable core does not import provider types;
an adapter rejects another provider's extension instead of silently ignoring
it. `LlamaCppRequestSettings` currently has no extra field because the two
established llama.cpp controls are portable settings. It reserves a typed
provider-owned seam rather than an untyped options dictionary.

All three phases of [ADR-0001](../../../../../docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md)
are implemented. A provider may emit a completed `ModelInteractionObservation`
to an optional `ModelInteractionObserver`; that transient seam does not change
`send()` or `ModelResponse`, and it does not import observability.
Observability may use it to construct immutable Evidence, while an interaction
remains usable without an observer.

The current observation is completed-success-only: provider transport,
provider-response parsing, or normalization failures do not emit an equivalent
`ModelInteractionObservation`. An observer exception occurs after a normalized
response exists and currently propagates from `send()`, so caller-visible
invocation failure does not by itself prove provider/model failure. This seam
does not automatically correlate `ModelInteractionId` with Runtime
`InteractionAttemptId`, identify an Evaluation realization, or retain exact
replay material.

`ModelRequest.tools` contains an ordered immutable tuple of normalized
`ModelToolDefinition` values. `ModelResponse.tool_calls` contains normalized
`ModelToolCall` requests returned by a provider. Neither references executable
Tools, ToolRunner, authorization, or conversation history. A call is descriptive
model output, not execution. The composition seam that converts a tools-owned
`ToolDescriptor` into this normalized model value is outside both packages.
Structured output and capabilities remain unimplemented.

The configurable llama.cpp implementation is under `providers/`; it communicates
with an already-running model endpoint. Endpoint lifecycle is separately owned
by `devtools.models.serving`.
~~~~

R255 src/devtools/models/interaction/models.py [3546:4963] lines 107–138

~~~~text

    def __post_init__(self) -> None:
        """Reject values outside the narrow portable request contract."""
        if not isinstance(self.prompt, Prompt):
            msg = "Model request prompt must be a Prompt."
            raise TypeError(msg)
        if not isinstance(self.settings, ModelSettings):
            msg = "Model request settings must be ModelSettings."
            raise TypeError(msg)
        if self.conversation is not None and not isinstance(
            self.conversation,
            ConversationRef,
        ):
            msg = "Model request conversation must be a ConversationRef or None."
            raise TypeError(msg)
        if self.provider_settings is not None and not isinstance(
            self.provider_settings,
            ProviderRequestSettings,
        ):
            msg = (
                "Model request provider settings must be a provider extension "
                "or None."
            )
            raise TypeError(msg)
        if not isinstance(self.tools, tuple) or not all(
            isinstance(tool, ModelToolDefinition) for tool in self.tools
        ):
            msg = "Model request tools must be a tuple of ModelToolDefinition values."
            raise TypeError(msg)
        if len({tool.name for tool in self.tools}) != len(self.tools):
            msg = "Model request Tool definition names must be unique."
            raise ValueError(msg)
~~~~

R257 src/devtools/models/interaction/prompt.py [0:260] lines 1–12

~~~~text
# Copyright (c) 2026
"""Model-facing input for one model interaction."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Prompt:
    """Represent the currently supported single text chat input."""

    content: str
    role: str
~~~~

R276 src/devtools/observability/evidence/docs/overview.md [0:2619] lines 1–48

~~~~text
# `devtools.observability.evidence`

This package owns immutable factual Evidence about completed execution
boundaries. `InteractionAttemptTerminalEvidence` records the terminal outcome
of one specialized `InteractionAttempt`; `EvidenceSink` accepts such records;
and `ExecutionInspector` observes execution lifecycle facts, constructs
terminal Evidence, and retains or forwards it for process-local diagnostics.

Execution owns the mutable `InteractionAttempt` lifecycle and its observer
contract. It does not import this package. Observability may depend on
execution lifecycle facts to construct Evidence, preserving the dependency
direction:

```text
execution -> InteractionAttemptObserver -> observability/evidence
```

Evidence is historical observation, not authorization, tracing, telemetry, or
current authority.

`ModelInteractionEvidence` is a separate Evidence form for one completed model
invocation. `ModelInteractionInspector` is optional process-local observation:
models and Runtime work normally when it is absent. The inspector owns capture
policy, evidence construction, capture manifests, collection, and inspection.
It currently receives only successfully completed normalized interaction
observations. Its capture-controlled request/response representation is not
necessarily exact replay material, is not automatically correlated to a
Runtime `InteractionAttempt`, and is not an Evaluation realization or judgment.
Failed provider/model realizations and observer failures require distinct
accounting by a future consumer that claims a complete evaluation population.
Payload manifests distinguish captured, omitted, redacted, and unavailable;
credentials, transport headers, and equivalent sensitive transport state have
no generic capture path.

For collections of Tool schemas or arguments, a `partial` manifest state means
the occurrences have differing retention states. It never claims that a
collection was wholly captured, omitted, redacted, or unavailable.

Structural request settings, normalized usage and termination, serving-profile
provenance, and bounded provider exchange facts remain inspectable. Prompt,
visible content, reasoning, and selected provider identity strings are retained
only under explicit capture policy. This package does not own Trace, Telemetry,
persistence, request policy, or model execution.

When present, disclosed normalized Tool names/descriptions are structural
Evidence. Tool schemas and returned untrusted call arguments are capture
controlled. Evidence never retains executable Tool objects, ToolRunner state,
authorization, or execution outcomes.
~~~~

R383 tests/context/planning/test_plan.py [2061:2902] lines 64–86

~~~~text
def _reference_option(
    snapshot: RepositorySnapshot,
    *,
    purpose: str = "Inspect this binding.",
) -> PythonQualifiedReferenceDisclosureOption:
    universe = define_python_module_interpretation_universe(
        repository_id=snapshot.repository_id,
        interpretations=interpret_python_module_resources(
            snapshot,
            module_root=PythonModuleRoot("."),
            resource_addresses=tuple(item.address for item in snapshot.resources),
        ).interpretations,
    )
    analysis = derive_python_declaration_references(
        snapshot,
        resource_address=RepositoryResourceAddress("consumer.py"),
        module_universe=universe,
    )
    return choose_python_qualified_reference_disclosure(
        purpose=purpose,
        analysis=analysis,
        reference=analysis.references[0],
    )
~~~~

R383 tests/context/planning/test_plan.py [2903:7128] lines 88–205

~~~~text

def test_mixed_plan_preserves_purpose_sources_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nf()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    purpose = "Inspect this binding."
    reference = _reference_option(snapshot)
    whole = choose_whole_resource_disclosure(
        purpose=purpose,
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=purpose,
        snapshot=snapshot,
        disclosures=(reference, whole),
    )
    assert (
        plan.identity
        == plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(whole, reference),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
            preceding_plan_identity="prior",
        ).identity
    )
    (tmp_path / "consumer.py").unlink()
    (tmp_path / "target.py").unlink()
    materialized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert len(materialized.items) == 2
    assert materialized.items[0].option_identity == reference.identity
    assert materialized.items[0].representation == reference.representation
    assert materialized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("target.py"),
    )
    assert "ast.Call.func; no runtime invocation is asserted" in (
        materialized.items[0].text
    )
    assert "def f():\r\n    return 'π'" in materialized.items[0].text
    assert materialized.items[1].native_provenance is whole.resource
    assert whole.resource.content in materialized.items[1].text
    assert (
        materialized.identity
        == materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        ).identity
    )
    rendered = render_context_disclosure(materialized)
    assert rendered.disclosure is materialized
    assert rendered.text.index("Disclosure item 1") < rendered.text.index(
        "Disclosure item 2",
    )
    assert purpose in rendered.text
    assert plan.identity in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    task = ModelRequest(
        Prompt("Inspect source.", "system"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider,
    )
    assembled = assemble_context_disclosure_model_request(
        task_request=task,
        context=rendered,
    )
    assert task.prompt.content == "Inspect source."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is continuation
    assert assembled.provider_settings is provider
    assert assembled.prompt.content.index("Inspect source.") < (
        assembled.prompt.content.index(rendered.text)
    )
    assert replace(assembled, prompt=task.prompt) == task


def test_same_resource_reference_uses_same_plan_boundary(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from consumer import f as g\ndef f():\n    pass\nvalue = g\n"},
    )
    option = _reference_option(snapshot)
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    realized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert realized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("consumer.py"),
    )
    assert "without the direct-call syntax tag" in realized.items[0].text
    assert "def f():\n    pass" in realized.items[0].text
~~~~

R383 tests/context/planning/test_plan.py [2904:6375] lines 89–185

~~~~text
def test_mixed_plan_preserves_purpose_sources_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nf()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    purpose = "Inspect this binding."
    reference = _reference_option(snapshot)
    whole = choose_whole_resource_disclosure(
        purpose=purpose,
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=purpose,
        snapshot=snapshot,
        disclosures=(reference, whole),
    )
    assert (
        plan.identity
        == plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(whole, reference),
        ).identity
    )
    assert (
        plan.identity
        != plan_disclosures(
            purpose=purpose,
            snapshot=snapshot,
            disclosures=(reference, whole),
            preceding_plan_identity="prior",
        ).identity
    )
    (tmp_path / "consumer.py").unlink()
    (tmp_path / "target.py").unlink()
    materialized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert len(materialized.items) == 2
    assert materialized.items[0].option_identity == reference.identity
    assert materialized.items[0].representation == reference.representation
    assert materialized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("target.py"),
    )
    assert "ast.Call.func; no runtime invocation is asserted" in (
        materialized.items[0].text
    )
    assert "def f():\r\n    return 'π'" in materialized.items[0].text
    assert materialized.items[1].native_provenance is whole.resource
    assert whole.resource.content in materialized.items[1].text
    assert (
        materialized.identity
        == materialize_disclosure_plan(
            plan=plan,
            snapshot=snapshot,
        ).identity
    )
    rendered = render_context_disclosure(materialized)
    assert rendered.disclosure is materialized
    assert rendered.text.index("Disclosure item 1") < rendered.text.index(
        "Disclosure item 2",
    )
    assert purpose in rendered.text
    assert plan.identity in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    task = ModelRequest(
        Prompt("Inspect source.", "system"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider,
    )
    assembled = assemble_context_disclosure_model_request(
        task_request=task,
        context=rendered,
    )
    assert task.prompt.content == "Inspect source."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is continuation
    assert assembled.provider_settings is provider
    assert assembled.prompt.content.index("Inspect source.") < (
        assembled.prompt.content.index(rendered.text)
    )
    assert replace(assembled, prompt=task.prompt) == task
~~~~

R383 tests/context/planning/test_plan.py [6377:7128] lines 188–205

~~~~text
def test_same_resource_reference_uses_same_plan_boundary(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from consumer import f as g\ndef f():\n    pass\nvalue = g\n"},
    )
    option = _reference_option(snapshot)
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    realized = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
    assert realized.items[0].resource_addresses == (
        RepositoryResourceAddress("consumer.py"),
        RepositoryResourceAddress("consumer.py"),
    )
    assert "without the direct-call syntax tag" in realized.items[0].text
    assert "def f():\n    pass" in realized.items[0].text
~~~~

R391 tests/context/python/function/test_cross_resource_pipeline.py [2140:4792] lines 65–127

~~~~text
def test_cross_resource_match_reaches_request_without_reacquisition(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Only matching knowledge is resolved, rendered, and assembled."""
    selected_source = 'def selected_function():\n    return "TARGET"'
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": 'def helper():\n    return "A"\n',
            "b.py": f"{selected_source}\n",
            "unrelated.py": 'def selected_function():\n    return "UNSELECTED"\n',
        },
    )
    first_address = RepositoryResourceAddress("a.py")
    selected_address = RepositoryResourceAddress("b.py")
    _forbid_reacquisition(monkeypatch)

    aggregate = analyze_python_function_declaration_resources(
        snapshot,
        resource_addresses=(first_address, selected_address),
    )
    retrieval = retrieve_python_functions_by_exact_name(
        declarations=aggregate.declarations,
        query=PythonFunctionExactNameQuery("selected_function"),
    )
    disclosure = disclose_python_function_exact_name_retrieval(retrieval)
    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    rendered = render_materialized_python_function_context(materialized)
    task_request = ModelRequest(Prompt("Return the selected value.", "user"))
    request = assemble_python_function_context_model_request(
        task_request=task_request,
        context=rendered,
    )

    selected_knowledge = aggregate.analyses[1].declarations[0]
    assert [
        analysis.derivation.dependency.resource.address
        for analysis in aggregate.analyses
    ] == [first_address, selected_address]
    assert tuple(match.knowledge for match in retrieval.matches) == (
        selected_knowledge,
    )
    assert disclosure.selected_matches == retrieval.matches
    assert disclosure.items[0].selected_match is retrieval.matches[0]
    assert materialized.items[0].disclosure_item is disclosure.items[0]
    assert materialized.items[0].source_snapshot_id == snapshot.id
    assert materialized.items[0].source_content_identity == (
        snapshot.resource_at(selected_address).content_identity
    )
    assert materialized.items[0].source_text == selected_source
    assert "Repository-relative resource: b.py\n" in rendered.text
    assert selected_source in rendered.text
    assert "helper" not in rendered.text
    assert "UNSELECTED" not in rendered.text
    assert request.prompt.content.count(rendered.text) == 1
    assert rendered.text in request.prompt.content
    assert task_request.prompt.content in request.prompt.content
~~~~

R395 tests/context/python/function/test_materialization.py [1968:5812] lines 66–164

~~~~text
def test_materializes_duplicate_sync_and_async_exact_multiline_source(
    tmp_path: Path,
) -> None:
    """Materialization preserves CRLF, non-ASCII text, order, and correlation."""
    snapshot = _snapshot(
        tmp_path,
        '# préface\r\ndef duplicate():\r\n    return "café"\r\n\r\n'
        'async def duplicate():\r\n    return "naïve"\r\n',
    )
    disclosure = _disclosure(snapshot, "duplicate")

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    assert materialized.disclosure is disclosure
    assert [item.source_text for item in materialized.items] == [
        'def duplicate():\r\n    return "café"',
        'async def duplicate():\r\n    return "naïve"',
    ]
    knowledge_identities = {
        item.disclosure_item.selected_match.knowledge.identity
        for item in materialized.items
    }
    assert len(knowledge_identities) == len(materialized.items)
    for materialized_item, disclosure_item in zip(
        materialized.items,
        disclosure.items,
        strict=True,
    ):
        assert materialized_item.disclosure_item is disclosure_item
        assert materialized_item.source_snapshot_id == snapshot.id
        assert (
            materialized_item.source_content_identity
            == snapshot.resource.content_identity
        )
    repeated = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )
    assert repeated == materialized
    assert repeated.identity == materialized.identity
    assert not hasattr(materialized, "model_request")
    assert not hasattr(materialized, "summary")
    assert not hasattr(materialized, "confidence")
    assert not hasattr(materialized, "ranking")


def test_materializes_single_line_using_utf8_byte_columns(tmp_path: Path) -> None:
    """UTF-8 byte columns extract non-ASCII single-line syntax exactly."""
    expected = 'def café(): return "olé"'
    snapshot = _snapshot(tmp_path, f"# naïve\n{expected}\n")
    disclosure = _disclosure(snapshot, "café")

    materialized = materialize_python_function_disclosure_source(
        disclosure=disclosure,
        snapshot=snapshot,
    )

    source_range = disclosure.items[0].source_occurrence.source_range
    assert source_range.end_column_utf8 == len(expected.encode("utf-8"))
    assert source_range.end_column_utf8 != len(expected)
    assert materialized.items[0].source_text == expected


def test_rejects_mismatched_snapshot_and_resource_state(tmp_path: Path) -> None:
    """Coordinates cannot be applied to another snapshot or addressed resource."""
    snapshot = _snapshot(tmp_path, "def target():\n    return 1\n")
    disclosure = _disclosure(snapshot, "target")
    changed_snapshot = _snapshot(tmp_path, "def target():\n    return 2\n")

    with pytest.raises(PythonFunctionSourceMaterializationError, match="snapshot"):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=changed_snapshot,
        )

    mismatched_resource = replace(
        snapshot.resource,
        address=RepositoryResourceAddress("other.py"),
    )
    mismatched_address_snapshot = replace(snapshot, resources=(mismatched_resource,))
    with pytest.raises(PythonFunctionSourceMaterializationError, match="resource"):
        materialize_python_function_disclosure_source(
            disclosure=disclosure,
            snapshot=mismatched_address_snapshot,
        )


@pytest.mark.parametrize(
    ("source_range", "match"),
    [
        (PythonSourceRange(1, 30, 1, 29), "ends before"),
        (PythonSourceRange(1, 0, 2, 0), "line is outside"),
        (PythonSourceRange(1, 0, 1, 100), "column is outside"),
        (PythonSourceRange(1, 8, 1, 26), "UTF-8 character boundaries"),
    ],
)
~~~~

R396 tests/context/python/function/test_qualified_reference.py [3511:8792] lines 104–218

~~~~text
def test_cross_resource_call_exact_source_and_request(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\r\nlabel = 'π'; f()\r\n",
            "target.py": "def f():\r\n    return 'π'\r\n",
        },
    )
    analysis = _analysis(snapshot)
    reference = analysis.references[0]
    materialized = _materialized(snapshot, analysis, reference)
    assert materialized.reference_name_text == "f"
    assert materialized.target_declaration_text == "def f():\r\n    return 'π'"
    assert reference.occurrence.source_range.start_column_utf8 == 14
    assert materialized.snapshot_id == snapshot.id
    assert (
        materialized.identity == _materialized(snapshot, analysis, reference).identity
    )
    rendered = render_python_qualified_reference_context(materialized)
    assert "Purpose: Understand this established reference." in rendered.text
    assert "bounded-expression-references-python-declaration" in rendered.text
    assert "ast.Call.func; no runtime invocation is asserted" in rendered.text
    assert "Reference analysis is non-exhaustive" in rendered.text
    assert "Source resource pointer: consumer.py" in rendered.text
    assert "Target resource pointer: target.py" in rendered.text
    assert "--- exact Reference Name begins ---\nf\n" in rendered.text
    assert "--- exact target declaration begins ---\ndef f():\r\n" in rendered.text
    assert str(reference.identity) in rendered.text
    assert str(snapshot.id) in rendered.text
    assert str(materialized.source_content_identity) in rendered.text
    assert str(materialized.target_content_identity) in rendered.text
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    conversation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider = ProviderRequestSettings("test-model")
    tools = (
        ModelToolDefinition(
            name="inspect",
            description="Inspect one value.",
            input_schema_json='{"type":"object"}',
        ),
    )
    task_request = ModelRequest(
        Prompt("Inspect the binding.", "system"),
        settings=settings,
        conversation=conversation,
        provider_settings=provider,
        tools=tools,
    )
    assembled = assemble_python_qualified_reference_model_request(
        task_request=task_request,
        context=rendered,
    )
    assert task_request.prompt.content == "Inspect the binding."
    assert assembled.prompt.role == "system"
    assert assembled.settings is settings
    assert assembled.conversation is conversation
    assert assembled.provider_settings is provider
    assert assembled.tools is tools
    assert assembled.prompt.content.startswith("Task/instruction UTF-8 byte length:")
    assert "Inspect the binding." in assembled.prompt.content
    assert rendered.text in assembled.prompt.content
    assert replace(assembled, prompt=task_request.prompt) == task_request


def test_same_resource_non_call_reference_and_exact_target(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {"consumer.py": "from consumer import f as g\ndef f():\n    pass\nvalue = g\n"},
    )
    analysis = _analysis(snapshot)
    assert len(analysis.references) == 1
    reference = analysis.references[0]
    assert not reference.direct_call
    materialized = _materialized(snapshot, analysis, reference)
    assert materialized.reference_name_text == "g"
    assert materialized.target_declaration_text == "def f():\n    pass"
    assert materialized.source_content_identity == materialized.target_content_identity
    rendered = render_python_qualified_reference_context(materialized)
    assert "without the direct-call syntax tag" in rendered.text
    assert "Source resource pointer: consumer.py" in rendered.text
    assert "Target resource pointer: consumer.py" in rendered.text


def test_duplicate_names_preserve_exact_qualified_target(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    return 'chosen'\n",
            "other.py": "def f():\n    return 'not chosen'\n",
        },
    )
    analysis = _analysis(snapshot)
    materialized = _materialized(snapshot, analysis, analysis.references[0])
    assert "'chosen'" in materialized.target_declaration_text
    assert "not chosen" not in materialized.target_declaration_text


def test_one_facade_target_support_is_preserved(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from package import exported as local\nlocal()\n",
            "package/__init__.py": "from .impl import f as exported\n",
            "package/impl.py": "def f():\n    return 1\n",
        },
    )
    analysis = _analysis(snapshot)
    materialized = _materialized(snapshot, analysis, analysis.references[0])
    assert materialized.reference_name_text == "local"
    assert materialized.target_declaration_text == "def f():\n    return 1"
    rendered = render_python_qualified_reference_context(materialized)
    assert "Resolution path: one-facade" in rendered.text
    assert "Target resource pointer: package/impl.py" in rendered.text
~~~~

R397 tests/context/python/function/test_rendering.py [1780:3798] lines 59–101

~~~~text
def test_renders_ordered_duplicate_sync_and_async_context_exactly(
    tmp_path: Path,
) -> None:
    """The full path renders metadata and unchanged CRLF/non-ASCII source."""
    first_source = (
        'def duplicate():\r\n    return "caf\u00e9 --- exact source ends ---"'
    )
    second_source = 'async def duplicate():\r\n    return "na\u00efve"'
    context = _materialized_context(
        tmp_path,
        f"# pr\u00e9face\r\n{first_source}\r\n\r\n{second_source}\r\n",
        name="duplicate",
    )

    rendered = render_materialized_python_function_context(context)
    expected_match_count = len(context.items)

    assert isinstance(rendered, RenderedPythonFunctionContext)
    assert rendered.materialized_context is context
    assert rendered.FORMAT == "python-function-context-text-v1"
    assert "Exact declared-name purpose: duplicate\n" in rendered.text
    assert "Selected declarations: 2\n" in rendered.text
    assert rendered.text.count("Declared name: duplicate\n") == expected_match_count
    assert "Declaration kind: function-def\n" in rendered.text
    assert "Declaration kind: async-function-def\n" in rendered.text
    assert (
        rendered.text.count("Repository-relative resource: module.py\n")
        == expected_match_count
    )
    assert "Source location: 2:0-3:" in rendered.text
    assert "Source location: 5:0-6:" in rendered.text
    assert context.items[0].disclosure_item.proposition in rendered.text
    assert first_source in rendered.text
    assert second_source in rendered.text
    assert first_source.replace("\r\n", "\n") not in rendered.text
    assert second_source.replace("\r\n", "\n") not in rendered.text
    assert rendered.text.index(first_source) < rendered.text.index(second_source)
    for item in context.items:
        expected_length = len(item.source_text.encode("utf-8"))
        assert f"Exact source UTF-8 byte length: {expected_length}\n" in rendered.text
    assert render_materialized_python_function_context(context) == rendered
~~~~

R398 tests/context/python/function/test_request_assembly.py [2102:4447] lines 70–134

~~~~text
def test_assembles_real_context_after_distinct_unchanged_task(
    tmp_path: Path,
) -> None:
    """Assembly preserves task, Context, role, and every other request semantic."""
    rendered = _rendered_context(
        tmp_path,
        'def target():\r\n    return "caf\u00e9"\r\n',
        name="target",
    )
    task_text = "Fix target without changing behavior.\r\nKeep its public name."
    settings = ModelSettings(maximum_output_tokens=128, thinking_enabled=False)
    continuation = ConversationRef(InteractionSource("test-model"), "thread-1")
    provider_settings = ProviderRequestSettings("test-model")
    tools = (
        ModelToolDefinition(
            name="inspect",
            description="Inspect one value.",
            input_schema_json='{"type":"object"}',
        ),
    )
    task_request = ModelRequest(
        prompt=Prompt(content=task_text, role="user"),
        settings=settings,
        conversation=continuation,
        provider_settings=provider_settings,
        tools=tools,
    )

    request = assemble_python_function_context_model_request(
        task_request=task_request,
        context=rendered,
    )

    assert isinstance(request, ModelRequest)
    assert request is not task_request
    assert request.prompt.role == task_request.prompt.role
    assert request.settings is settings
    assert request.conversation is continuation
    assert request.provider_settings is provider_settings
    assert request.tools is tools
    assert task_request.prompt.content == task_text
    assert task_text in request.prompt.content
    assert rendered.text in request.prompt.content
    assert request.prompt.content.index(task_text) < request.prompt.content.index(
        rendered.text,
    )
    assert (
        f"Task/instruction UTF-8 byte length: {len(task_text.encode('utf-8'))}\n"
        in request.prompt.content
    )
    assert (
        "Supporting repository Context UTF-8 byte length: "
        f"{len(rendered.text.encode('utf-8'))}\n"
    ) in request.prompt.content
    assert request.prompt.content.count('def target():\r\n    return "caf\u00e9"') == 1
    assert (
        assemble_python_function_context_model_request(
            task_request=task_request,
            context=rendered,
        )
        == request
    )
    assert not hasattr(request, "rendered_context")
~~~~

R424 tests/context/repository/test_observation.py [3312:6367] lines 109–184

~~~~text
def test_observes_one_required_resource_into_identified_snapshot_state(
    tmp_path: Path,
) -> None:
    """Successful observation retains repository, occurrence, and content facts."""
    source = tmp_path / "src" / "module.py"
    source.parent.mkdir()
    source.write_bytes(b"def function():\r\n    pass\r\n")

    snapshot = _observe(_repository(), tmp_path, "src/module.py")

    assert snapshot.repository_id == _repository().id
    assert snapshot.OBSERVATION_SEMANTICS == (
        "explicit-required-text-resources-sha256-v1"
    )
    assert snapshot.resources == (snapshot.resource,)
    assert isinstance(snapshot.id, RepositorySnapshotId)
    assert isinstance(snapshot.resource, RepositoryResourceOccurrence)
    assert snapshot.resource.address.parts == ("src", "module.py")
    assert str(snapshot.resource.address) == "src/module.py"
    assert isinstance(snapshot.resource.content_identity, ContentIdentity)
    assert snapshot.resource.content == "def function():\r\n    pass\r\n"
    assert snapshot.resource.encoding == "utf-8"
    assert snapshot.resource.byte_size == len(source.read_bytes())
    assert str(snapshot.id) == snapshot.id.value
    assert str(snapshot.resource.content_identity) == (
        snapshot.resource.content_identity.value
    )


def test_repeated_observation_of_unchanged_state_is_equivalent(
    tmp_path: Path,
) -> None:
    """Equivalent admitted state yields the same snapshot and content identities."""
    source = tmp_path / "module.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    repository = _repository()

    first = _observe(repository, tmp_path, "module.py")
    second = _observe(repository, tmp_path, "module.py")

    assert first == second
    assert hash(first) == hash(second)


def test_changed_content_changes_content_and_snapshot_identity(tmp_path: Path) -> None:
    """A content edit establishes different content and snapshot state."""
    source = tmp_path / "module.py"
    source.write_text("VALUE = 1\n", encoding="utf-8")
    repository = _repository()
    first = _observe(repository, tmp_path, "module.py")

    source.write_text("VALUE = 2\n", encoding="utf-8")
    second = _observe(repository, tmp_path, "module.py")

    assert first.resource.content_identity != second.resource.content_identity
    assert first.id != second.id


def test_equal_content_at_distinct_addresses_preserves_distinct_occurrences(
    tmp_path: Path,
) -> None:
    """Address changes occurrence and snapshot while content identity stays equal."""
    content = "VALUE = 1\n"
    (tmp_path / "first.py").write_text(content, encoding="utf-8")
    (tmp_path / "second.py").write_text(content, encoding="utf-8")
    repository = _repository()

    first = _observe(repository, tmp_path, "first.py")
    second = _observe(repository, tmp_path, "second.py")

    assert first.resource.content_identity == second.resource.content_identity
    assert first.resource != second.resource
    assert first.resource.address != second.resource.address
    assert first.id != second.id
~~~~

R424 tests/context/repository/test_observation.py [5647:6365] lines 167–182

~~~~text
def test_equal_content_at_distinct_addresses_preserves_distinct_occurrences(
    tmp_path: Path,
) -> None:
    """Address changes occurrence and snapshot while content identity stays equal."""
    content = "VALUE = 1\n"
    (tmp_path / "first.py").write_text(content, encoding="utf-8")
    (tmp_path / "second.py").write_text(content, encoding="utf-8")
    repository = _repository()

    first = _observe(repository, tmp_path, "first.py")
    second = _observe(repository, tmp_path, "second.py")

    assert first.resource.content_identity == second.resource.content_identity
    assert first.resource != second.resource
    assert first.resource.address != second.resource.address
    assert first.id != second.id
~~~~

R424 tests/context/repository/test_observation.py [8745:9343] lines 250–263

~~~~text
def test_equal_content_at_two_addresses_retains_distinct_multi_occurrences(
    tmp_path: Path,
) -> None:
    """Equal content identity does not collapse address-contextual occurrences."""
    content = "VALUE = 1\n"
    (tmp_path / "alpha.py").write_text(content, encoding="utf-8")
    (tmp_path / "beta.py").write_text(content, encoding="utf-8")

    snapshot = _observe_many(_repository(), tmp_path, "alpha.py", "beta.py")
    first, second = snapshot.resources

    assert first.address != second.address
    assert first != second
    assert first.content_identity == second.content_identity
~~~~

R524 tests/scripts/test_validate_development.py [313:2104] lines 17–68

~~~~text
_SCRIPT_PATH = Path("scripts/validate_development.py")


@pytest.fixture
def validation_script() -> ModuleType:
    """Load the operational script without making scripts a library package."""
    specification = importlib.util.spec_from_file_location(
        "test_validate_development_script",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def test_profile_selects_tests_and_excludes_experiment_tests_before_collection(
    validation_script: ModuleType,
) -> None:
    """The directory boundary covers the whole retained experiment population."""
    arguments = validation_script.pytest_arguments(Path.cwd())
    tests = Path(arguments[0])
    ignored = Path(arguments[1].removeprefix("--ignore="))

    assert tests == Path.cwd() / "tests"
    assert ignored == tests / "experiments"
    assert tests.is_dir()
    assert ignored.is_dir()
    assert (tests / "context").is_dir()
    assert (tests / "scripts" / "test_validate_development.py").is_file()


def test_profile_propagates_pytest_failure_code(
    validation_script: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed pytest run remains a failed profile invocation."""
    observed_arguments: list[str] | None = None

    def failed_pytest(arguments: list[str]) -> int:
        nonlocal observed_arguments
        observed_arguments = arguments
        return 1

    monkeypatch.setattr(validation_script.pytest, "main", failed_pytest)

    result = validation_script.main()

    assert result == 1
    assert observed_arguments == validation_script.pytest_arguments()
~~~~

TASK original task [0:230]

~~~~text
Build a deterministic, inspectable in-memory manifest of an already materialized repository Context disclosure, keeping caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.
~~~~

TASK original task [230:574]

~~~~text
Inspect the existing class `devtools.context.planning.materialization.ContextDisclosure` and function `devtools.context.planning.materialization.materialize_disclosure_plan`: preserve exact plan identity, purpose, repository/snapshot applicability, ordered choices, representation names, option identities and the one-item-per-choice contract.
~~~~

TASK original task [574:756]

~~~~text
Use the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot. 
~~~~

TASK original task [574:980] lines 3–3

~~~~text
Use the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot. Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest; do not reacquire source, rematerialize choices or silently substitute evidence.
~~~~

TASK original task [756:900]

~~~~text
Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest; 
~~~~

TASK original task [900:980]

~~~~text
do not reacquire source, rematerialize choices or silently substitute evidence.
~~~~

TASK original task [980:1210]

~~~~text
Introduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`. 
~~~~

TASK original task [980:1458] lines 4–4

~~~~text
Introduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`. Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.
~~~~

TASK original task [1210:1458]

~~~~text
Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.
~~~~

TASK original task [1458:1598]

~~~~text
Provide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records; 
~~~~

TASK original task [1458:1829] lines 5–5

~~~~text
Provide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records; distinguish total item text bytes from unique supporting-resource bytes. The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.
~~~~

TASK original task [1598:1671]

~~~~text
distinguish total item text bytes from unique supporting-resource bytes. 
~~~~

TASK original task [1671:1829]

~~~~text
The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.
~~~~

TASK original task [1829:1989]

~~~~text
Inspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged. 
~~~~

TASK original task [1829:2167] lines 6–6

~~~~text
Inspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged. Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.
~~~~

TASK original task [1989:2167]

~~~~text
Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.
~~~~

TASK original task [2167:2437]

~~~~text
Add focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases; 
~~~~

TASK original task [2167:2513] lines 7–7

~~~~text
Add focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases; retain existing planning, rendering and copied-request regression coverage.
~~~~

TASK original task [2437:2513]

~~~~text
retain existing planning, rendering and copied-request regression coverage.
~~~~

TASK original task [2513:2681]

~~~~text
Update the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope. 
~~~~

TASK original task [2513:2858] lines 8–8

~~~~text
Update the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope. Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.
~~~~

TASK original task [2681:2858]

~~~~text
Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.
~~~~

TASK original task [2858:2951]

~~~~text
Inspect the existing file `pyproject.toml` for test, coverage and strict typing constraints; 
~~~~

TASK original task [2858:3150] lines 9–9

~~~~text
Inspect the existing file `pyproject.toml` for test, coverage and strict typing constraints; run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.
~~~~

TASK original task [2951:3150]

~~~~text
run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.
~~~~

TASK original task [3150:3413] lines 10–10

~~~~text
Operational exclusion: this is a future feature specification for an acquisition experiment. Stage A freezes the experiment only; do not implement the manifest feature, production routing, R1.7, BM25F, sequential search, treatment execution or gold adjudication.
~~~~

Authentication and method

The initial five-file whitelist and packet validator passed before output creation. The four declared digest scopes were checked. All original packet bytes are sealed by exact hashes. The builder performs deterministic reconstruction, invariant checks, independent-process byte comparison and adversarial rejection tests. The output hash manifest authenticates scientific files; its own digest is supplied by the operational final report.

All requested excluded-access categories are NO; confirmation and reserve access are NO. The machine review retains the category-by-category attestation. Original task/resource text is legitimate evidence. No repository checkout or external source was used.

