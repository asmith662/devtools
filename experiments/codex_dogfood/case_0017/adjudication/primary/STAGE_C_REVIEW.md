# Clean primary semantic adjudication: case-0017

MODEL: GPT-6 Astra. REASONING: High. Sole primary; second reviewer: NO.
Host routing independently verified: NO.

Task: Implement repository lexical statistics and inverted index

Authentication: PASS; NO ADJUDICATION before file creation. Exact initial five files; no directories, symlinks, junctions or reparse points.

- archive_sha256: `64dad46fb86c69cdb4de0b9e6314290bbcfcd2f7a23e4f6daef2f570dab591ac`
- canonical_payload_sha256: `e80a6088e42290c7fb68ec09f2c10a2e695b1314642dc329402917efac914556`
- manifest_sha256: `5d1976523476a659d952b38bffa91e3ffce89d935ad0455b49f28f2780b29d5c`
- integrity_sha256: `b9c3f0a30e8f05710e43201da8fed9e6fc2d93cd2fc29b36a1ef10ff22dd52d6`

Frame:

- repository_id: `5cf96d9e-d6a5-44a6-83d3-1e24f6e00009`
- snapshot_id: `0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49`
- corpus_id: `32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91`

Completeness: 357 resources × 3 obligations = 1,071 resolved cells; duplicates, missing, unexpected and unresolved: 0.

| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY | Witnesses |
|---|---:|---:|---:|---:|
| O1 | 2 | 8 | 347 | 2 |
| O2 | 2 | 8 | 347 | 2 |
| O3 | 3 | 15 | 339 | 2 |
| Total | 7 | 31 | 1033 | |

REQUIRED-resource union (not one necessary solution):

- R001: `AGENTS.md`
- R098: `src/devtools/context/retrieval/lexical.py`
- R271: `tests/context/retrieval/test_lexical.py`

Semantic units: 14; classes: {"REPOSITORY_SUPPORTED": 4, "TASK_AND_REPOSITORY_SUPPORTED": 0, "TASK_BACKED": 10}.

| Unit | Obligations | Evidence class | Necessary information |
|---|---|---|---|
| T01 | O1 | TASK_BACKED | Compute per-document counts of each observed normalized term and document length as the number of observations, including repetitions. |
| T02 | O1 | TASK_BACKED | Compute collection document count, per-term document frequency, and average document length; include zero-length documents and explicitly define the empty-collection outcome. |
| T03 | O1, O2, O3 | TASK_BACKED | Make repeated derivations over equivalent admitted input deterministic, including output ordering. |
| T04 | O1, O2 | TASK_BACKED | Retain the provenance of statistics and postings to their admitted lexical documents and collection. |
| T05 | O1, O2 | TASK_BACKED | Derive the capability from the existing lexical material without new tokenization semantics, filesystem reacquisition, or relevance/scoring claims. |
| T06 | O2 | TASK_BACKED | Build a term-to-document inverted mapping retaining each posting document and its term frequency. |
| T07 | O3 | TASK_BACKED | Preserve the existing lexical observation behavior and values when adding the capability. |
| T08 | O3 | TASK_BACKED | Expose a coherent public capability consistent with the existing lexical boundary. |
| T09 | O3 | TASK_BACKED | Document the new statistics/index boundary accurately. |
| T10 | O3 | TASK_BACKED | Validate heterogeneous resources, repeated terms, and empty documents/collections, together with deterministic behavior. |
| R01 | O1, O2, O3 | REPOSITORY_SUPPORTED | Existing per-document lexical analyses expose document and ordered observations with normalized_term; collection analyses expose analyses and document_collection. Those retained objects carry the input provenance. |
| R03 | O3 | REPOSITORY_SUPPORTED | The parent baseline uses Unicode word spans with casefolding, retains repeated observations and exact string offsets/encounter order, and does not split identifiers or add statistical state to observations. |
| R04 | O3 | REPOSITORY_SUPPORTED | The parent normal deterministic validation convention is uv run ruff check ., uv run mypy, uv run pytest and git diff --check, with 100% branch coverage; live model/Docker tests require separate authorization. |
| R05 | O3 | REPOSITORY_SUPPORTED | Parent documentation distinguishes current behavior from architecture and history: inspect documentation impact, update changed behavior claims, and change architecture/navigation only when affected. |

Minimal complete witnesses:

- O1-W01: resources R098; units R01, T01, T02, T03, T04, T05.
- O1-W02: resources R271; units R01, T01, T02, T03, T04, T05.
- O1 indispensable resources: none; indispensable units: R01, T01, T02, T03, T04, T05.
- O2-W01: resources R098; units R01, T03, T04, T05, T06.
- O2-W02: resources R271; units R01, T03, T04, T05, T06.
- O2 indispensable resources: none; indispensable units: R01, T03, T04, T05, T06.
- O3-W01: resources R001, R098; units R01, R03, R04, R05, T03, T07, T08, T09, T10.
- O3-W02: resources R001, R271; units R01, R03, R04, R05, T03, T07, T08, T09, T10.
- O3 indispensable resources: R001; indispensable units: R01, R03, R04, R05, T03, T07, T08, T09, T10.

Task combinations: 8. Distinct sufficient resource unions: 3.

All distinct sufficient resource unions:

- R001, R098
- R001, R271
- R001, R098, R271

Inclusion-minimal sufficient resource unions:

- R001, R098
- R001, R271

Resource-count range across all sufficient unions: [2, 3]; inclusion-minimal range: [2, 2].
Sufficient semantic-unit unions: 1; count range: [14, 14].
Task-indispensable resources: R001.
Task-indispensable units: R01, R03, R04, R05, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10.

Positive evidence (all exact quotes, rationale, inference and native identities are retained in stage_c_review.json):

| Resource | Obligation | Label | Original lines |
|---|---|---|---|
| R001 `AGENTS.md` | O3 | REQUIRED | 207-219, 199-205 |
| R003 `docs/architecture.md` | O1 | HELPFUL_ONLY | 284-322 |
| R003 `docs/architecture.md` | O2 | HELPFUL_ONLY | 284-322 |
| R003 `docs/architecture.md` | O3 | HELPFUL_ONLY | 284-322 |
| R005 `docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md` | O3 | HELPFUL_ONLY | 340-359 |
| R006 `docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md` | O3 | HELPFUL_ONLY | 91-115 |
| R008 `docs/architecture/taxonomy.md` | O3 | HELPFUL_ONLY | 301-335 |
| R010 `docs/backlog/epics/B-0002-coding-context-substrate.md` | O1 | HELPFUL_ONLY | 204-222 |
| R010 `docs/backlog/epics/B-0002-coding-context-substrate.md` | O2 | HELPFUL_ONLY | 204-222 |
| R010 `docs/backlog/epics/B-0002-coding-context-substrate.md` | O3 | HELPFUL_ONLY | 204-222 |
| R057 `docs/documentation_map.md` | O1 | HELPFUL_ONLY | 61-88, 143-149 |
| R057 `docs/documentation_map.md` | O2 | HELPFUL_ONLY | 61-88, 143-149 |
| R057 `docs/documentation_map.md` | O3 | HELPFUL_ONLY | 61-88, 143-149 |
| R060 `pyproject.toml` | O3 | HELPFUL_ONLY | 19-70 |
| R078 `src/devtools/context/__init__.py` | O3 | HELPFUL_ONLY | 50-78, 114-147 |
| R089 `src/devtools/context/repository/__init__.py` | O3 | HELPFUL_ONLY | 4-60 |
| R090 `src/devtools/context/repository/corpus.py` | O1 | HELPFUL_ONLY | 59-71, 102-163 |
| R090 `src/devtools/context/repository/corpus.py` | O2 | HELPFUL_ONLY | 59-71, 102-163 |
| R090 `src/devtools/context/repository/corpus.py` | O3 | HELPFUL_ONLY | 59-71, 102-163 |
| R092 `src/devtools/context/repository/document.py` | O1 | HELPFUL_ONLY | 18-58, 61-89 |
| R092 `src/devtools/context/repository/document.py` | O2 | HELPFUL_ONLY | 18-58, 61-89 |
| R092 `src/devtools/context/repository/document.py` | O3 | HELPFUL_ONLY | 18-58, 61-89 |
| R095 `src/devtools/context/repository/resource.py` | O1 | HELPFUL_ONLY | 49-72 |
| R095 `src/devtools/context/repository/resource.py` | O2 | HELPFUL_ONLY | 49-72 |
| R095 `src/devtools/context/repository/resource.py` | O3 | HELPFUL_ONLY | 49-72 |
| R097 `src/devtools/context/retrieval/__init__.py` | O3 | HELPFUL_ONLY | 1-18 |
| R098 `src/devtools/context/retrieval/lexical.py` | O1 | REQUIRED | 19-49, 52-85 |
| R098 `src/devtools/context/retrieval/lexical.py` | O2 | REQUIRED | 19-49, 52-85 |
| R098 `src/devtools/context/retrieval/lexical.py` | O3 | REQUIRED | 19-49, 52-85, 16-74 |
| R266 `tests/context/repository/test_corpus.py` | O1 | HELPFUL_ONLY | 180-226 |
| R266 `tests/context/repository/test_corpus.py` | O2 | HELPFUL_ONLY | 180-226 |
| R266 `tests/context/repository/test_corpus.py` | O3 | HELPFUL_ONLY | 180-226 |
| R268 `tests/context/repository/test_document.py` | O1 | HELPFUL_ONLY | 94-170, 209-245 |
| R268 `tests/context/repository/test_document.py` | O2 | HELPFUL_ONLY | 94-170, 209-245 |
| R268 `tests/context/repository/test_document.py` | O3 | HELPFUL_ONLY | 94-170, 209-245 |
| R271 `tests/context/retrieval/test_lexical.py` | O1 | REQUIRED | 89-116, 119-170, 173-201 |
| R271 `tests/context/retrieval/test_lexical.py` | O2 | REQUIRED | 89-116, 119-170, 173-201 |
| R271 `tests/context/retrieval/test_lexical.py` | O3 | REQUIRED | 89-116, 119-170, 173-201, 89-170, 191-201, 239-258 |

Gap audit:

- TASK_INTERPRETATION_GAP: NONE. The frozen interpretation is authoritative and internally consistent; its original empty record is preserved exactly.
- TASK_GAP: NONE. The frozen criteria are sufficient for a bounded implementation. API names, representation, deterministic ordering and explicit empty-average policy are design freedoms.
- REPOSITORY_INFORMATION_GAP: NONE. All necessary current-parent facts have packet-contained support alternatives. No external resource is needed under the stated retained-input assumptions.

Frozen interpretation gaps: `[]`, preserved exactly.

Ambiguities:

- A01: Public type/helper names and package layout are unspecified. Preserved exactly; coherent exposure does not mandate a particular changed path.
- A02: Index representation and construction API are unspecified; no scoring/ranking capability is requested. Preserved exactly; immutable postings or other deterministic representations remain possible.
- A03: The empty-collection average-length representation and exact term/posting ordering are unspecified. Document an explicit empty policy and deterministic order; this is bounded design freedom, not a missing repository fact.
- A04: Defensive handling of manually assembled inconsistent analyses or duplicate document identities is unspecified. Do not manufacture a validation subsystem requirement; state admitted-input assumptions or a narrow rejection policy.

Self-review corrections:

- Kept the observation field protocol distinct from behavioral preservation. Architectural lexical descriptions support R03 but cannot replace R01; they remain HELPFUL_ONLY in complete witnesses.
- Accepted the lexical tests as an inferable alternative for the consumed observation protocol; did not require source solely because it is source.
- After the complete 1,071-cell draft, removed proposed R02 (document identity field internals) as an unnecessary semantic unit and downgraded R092/O2 and R268/O2 from REQUIRED to HELPFUL_ONLY. Postings can retain analysis.document directly, preserving its existing identity without knowing its internal id fields or digest algorithm. R02 is retired, not renumbered.
- Recomputed O2 witnesses after removing R02: each existing observation-interface alternative suffices independently. Eliminated supersets containing additional document source/tests or both independent interface alternatives.
- Did not require corpus construction or observation/acquisition internals: retained input objects preserve that provenance.
- Kept public initializers HELPFUL_ONLY because the frozen package-layout ambiguity permits coherent exposure without any particular initializer edit.
- Distinguished the complete AGENTS validation convention from corroborating pyproject configuration. Documentation-map support for R05 is redundant once the indispensable AGENTS validation rule is present.
- Recorded average-length empty policy and malformed manually assembled input handling as design ambiguities, preserving the frozen empty interpretation-gap list.

Limitations:

- The model/reasoning designation is GPT-6 Astra / High as requested; host routing was not independently verified. No claim of routing verification is made.
- Semantic necessity is the judgment of this one primary over the frozen packet, not proof of a unique implementation or an empirical effectiveness result.
- All 357 resources received content-based screening in packet order; candidate support received close reading. Unrelated resources were screened through content purpose, declarations/headings and full-text lexical-contract matching, not asserted to have received exhaustive line-by-line reading.
- The retained parent frame is authoritative; absent checkout resources were not sought. Completeness of alternatives is within this supplied resource frame and the explicit inferability assumptions.
- Validation proves identity/span/schema consistency and exhaustive arithmetic over the authored support model. It cannot mechanically prove the semantic truth or exhaustive discovery of that model.
- No repository tests were run and no implementation was written. Parent tests are source-text evidence only.
- Natural mentions of queries, graphs, scores, history and evaluation inside original parent text are permitted evidence; they are not access to treatment metadata or another case.

Blindness attestation (excluded external evidence access):

- repository checkout: NO
- Git/history: NO
- parent directories: NO
- sibling workspaces: NO
- prior Codex session: NO
- web: NO
- queries: NO
- lexical ranks/scores: NO
- structural annotations: NO
- Reference treatment evidence: NO
- support pairs: NO
- predecessor pairs: NO
- treatment timings: NO
- graph/PPR/RRF: NO
- other cohort cases: NO
- child implementation: NO
- child paths: NO
- child diff: NO
- prior gold: NO
- confirmation: NO
- reserve: NO

Access means excluded external experiment/repository evidence, not natural identifiers or descriptions inside authenticated original task/parent resource text. Parent source identity hashes in the frozen frame were not followed to Git.

Validation: exhaustive cell/frame/span checks; independent subset witness validation; exact task arithmetic; 22 representative adversarial mutations including overwrite and scientific-hash rejection. Deterministic replay requires exact generated-byte identity in a separate Python process. Original packet SHA-256 values are rechecked on every build and verification.

Scientific artifacts: stage_c_review.json, stage_c_statistics.json, STAGE_C_REVIEW.md, stage_c_validation.json, stage_c_hashes.json, stage_c_method.md, stage_c_builder.py. SHA-256 bindings are in stage_c_hashes.json; its own digest and separate-process outcome are reported in the operational handoff.

Exact next step:

Import this clean Astra / High primary adjudication byte-for-byte into the
devtools repository.

Do NOT run another semantic reviewer.

Do NOT inspect the historical child implementation.

Wait until the other independently blinded cohort primaries are also complete
before any structural-discrimination effectiveness interpretation.

STOP.
