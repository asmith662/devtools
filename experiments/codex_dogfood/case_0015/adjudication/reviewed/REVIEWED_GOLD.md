# Case 0015 reviewed development gold

Provenance: PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. One primary review; no reconciliation or second reviewer.

# Case 0015 primary semantic adjudication

MODEL = GPT-6 Astra; REASONING = High. One adjudicator, followed by one self-review.

## Exact original task

```text
Implement strict bounded acquisition for the existing codec-backed filesystem read API.

O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.

O2. Define the finite acquisition bound precisely: retain at most `max_bytes` payload bytes and acquire at most one additional byte to distinguish exact-boundary EOF from oversized input; bound individual read requests and release the stream on success and every failure. Raise `FileTooLargeError` on excess instead of returning a truncated model. Do not claim a bound on decoded model memory, a stable file snapshot, race-free pathname checks, containment, authorization or locking.

O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.

O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

O5. Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits, growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures, multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types. Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.

O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.
```

## Task-clause audit

Each obligation retains its exact original task_clause as normative alongside its evidence-discovery satisfaction summary. All substantive clauses are represented. Operational adjudication instructions are not feature requirements.

| Clause | Requirement | Obligations | Assessment | Task characters |
|---|---|---|---|---|
| C00 | Strict bounded acquisition for the existing codec-backed read API. | O1, O2, O3 | ADEQUATELY_REPRESENTED | [0, 87) |
| C01 | Replace finite whole-file acquisition inside the existing filesystem reader with bounded chunks. | O1 | ADEQUATELY_REPRESENTED | [93, 267) |
| C02 | Preserve the public ResolvedPath, file_format, max_bytes and DEFAULT_MAX_READ_BYTES contract. | O1 | ADEQUATELY_REPRESENTED | [268, 368) |
| C03 | A preliminary stat is optional and cannot permit unbounded acquisition of a file that grows. | O1 | ADEQUATELY_REPRESENTED | [521, 627) |
| C04 | For a finite limit retain no more than max_bytes payload bytes and acquire at most one additional sentinel byte to distinguish exact EOF from excess. | O2 | ADEQUATELY_REPRESENTED | [680, 815) |
| C05 | Every finite-mode read request is bounded. | O2 | ADEQUATELY_REPRESENTED | [817, 847) |
| C06 | Release the acquired stream on success and every failure. | O2 | ADEQUATELY_REPRESENTED | [852, 900) |
| C07 | Excess raises FileTooLargeError and never returns a truncated model. | O2 | ADEQUATELY_REPRESENTED | [901, 976) |
| C08 | The acquisition guarantee makes none of the excluded model-memory, snapshot, pathname-race, containment, authorization, or locking claims. | O2 | ADEQUATELY_REPRESENTED | [977, 1112) |
| C09 | Preserve format override, suffix inference and the existing resolution functions. | O3 | ADEQUATELY_REPRESENTED | [1118, 1225) |
| C10 | Delegate complete accepted bytes to the existing codecs without content rewriting. | O3 | ADEQUATELY_REPRESENTED | [1226, 1304) |
| C11 | Retain all six specified rich result classes. | O3 | ADEQUATELY_REPRESENTED | [1305, 1427) |
| C12 | Preserve UTF-8 decoding, original line endings, encoding metadata and source byte-size metadata. | O3 | ADEQUATELY_REPRESENTED | [1429, 1500) |
| C13 | Chunk boundaries may split multibyte sequences; no replacement decoding is introduced and codec-domain failures retain their existing classes. | O3 | ADEQUATELY_REPRESENTED | [1501, 1678) |
| C14 | Preserve the existing missing-path, non-regular-file, permission, unsupported-format and excess error boundaries. | O4 | ADEQUATELY_REPRESENTED | [1684, 1826) |
| C15 | Normalize stream-open and chunk-read PermissionError failures with causal FilesystemPermissionError exceptions. | O4 | ADEQUATELY_REPRESENTED | [1827, 1949) |
| C16 | Keep the change within the existing filesystem package and preserve atomic writing, format ownership, core path resolution and Tool boundaries. | O4 | ADEQUATELY_REPRESENTED | [1950, 2162) |
| C17 | Add controlled read tests at the specified test location and relevant codec/model tests covering the limit domain. | O5 | ADEQUATELY_REPRESENTED | [2168, 2343) |
| C18 | Test growth after stat, short reads, EOF, closure on exceptions and open/read permission failures. | O5 | ADEQUATELY_REPRESENTED | [2345, 2450) |
| C19 | Test multibyte splits, invalid UTF-8, explicit overrides and every supported rich result type. | O5 | ADEQUATELY_REPRESENTED | [2452, 2576) |
| C20 | Prove finite request and retention bounds using deterministic instrumented streams. | O5 | ADEQUATELY_REPRESENTED | [2577, 2740) |
| C21 | Update I/O, overview, roadmap and applicable public API documentation to state the bound and its limitations. | O6 | ADEQUATELY_REPRESENTED | [2746, 2951) |
| C22 | Preserve existing callers. | O6 | ADEQUATELY_REPRESENTED | [2952, 2977) |
| C23 | Preserve the protected validation profile and run it along with Ruff, formatting, mypy and diff checks. | O6 | ADEQUATELY_REPRESENTED | [2982, 3186) |
| C24 | Do not expand into binary codecs, new formats, streaming format parsing, secure filesystem policy or production retrieval changes. | O6 | ADEQUATELY_REPRESENTED | [3187, 3314) |
| C25 | Preserve the complete limit-value domain: 16 MiB default, None unbounded, negative rejection, zero and exact boundary. | O1 | ADEQUATELY_REPRESENTED | [370, 520) |

## Frozen obligations and applicability

- **O1: Compatible bounded read contract** — mandatory; APPLICABLE. Satisfaction: Identify current signature, default, limit semantics and allocation-before-rejection behavior; locate the owning implementation.
- **O2: Acquisition bound and lifecycle** — mandatory; APPLICABLE. Satisfaction: Establish precise max_bytes plus one sentinel acquisition, bounded requests, closure and distinction from model memory/security/snapshot guarantees.
- **O3: Codec and rich-model fidelity** — mandatory; APPLICABLE. Satisfaction: Identify complete-byte codec contracts, format override/inference, concrete models, metadata and strict decoding behavior.
- **O4: Error and ownership boundaries** — mandatory; APPLICABLE. Satisfaction: Establish existing error normalization, causal exceptions and package/atomic-write/path/authorization boundaries.
- **O5: Controlled regression tests** — mandatory; APPLICABLE. Satisfaction: Find current read/codec/model test patterns and evidence needed for deterministic instrumented-stream tests of bounds and compatibility.
- **O6: Documentation and protected validation** — mandatory; APPLICABLE. Satisfaction: Identify authoritative behavior documentation, deferred scope and protected validation policy/configuration without changing exclusions or coverage.

## Complete cell accounting

515 resources × 6 obligations = 3,090 cells. No missing, duplicate, unexpected or unresolved cells.

| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY |
|---|---:|---:|---:|
| O1 | 2 | 16 | 497 |
| O2 | 0 | 3 | 512 |
| O3 | 4 | 30 | 481 |
| O4 | 6 | 13 | 496 |
| O5 | 1 | 29 | 485 |
| O6 | 8 | 11 | 496 |
| TOTAL | 21 | 102 | 2967 |

The JSON contains every cell, its native identity, rationale and provenance. REQUIRED means membership in at least one minimal witness; it does not mean membership in every witness.

## Positive resources by obligation

### O1

**REQUIRED**

- `src/devtools/resources/filesystem/docs/io.md` — lines 20–30, characters [424, 913); lines 24–38, characters [499, 1171). Necessary in at least one complete minimal witness: R01: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.; R16: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.
- `src/devtools/resources/filesystem/reading.py` — lines 23–35, characters [526, 906); lines 107–116, characters [3200, 3504); lines 37–39, characters [907, 1121); lines 61–82, characters [1922, 2542). Necessary in at least one complete minimal witness: R01: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.; R16: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.

**HELPFUL_ONLY**

- `AGENTS.md` — lines 78–86, characters [3856, 4424). Canonical substrate guidance corroborates filesystem ownership; direct read and profile facts are narrower evidence.
- `src/devtools/context/repository/observation.py` — lines 126–158, characters [4311, 5347). An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.
- `src/devtools/core/paths/docs/overview.md` — lines 35–47, characters [1134, 1737). Explains the path wrapper and limits of absolute-path validation; the reader already shows .value usage and the task protects core resolution.
- `src/devtools/core/paths/models.py` — lines 14–38, characters [221, 963). Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.
- `src/devtools/models/benchmarks/storage.py` — lines 45–53, characters [1214, 1713). Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.
- `src/devtools/resources/filesystem/__init__.py` — lines 4–41, characters [86, 982). Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.
- `src/devtools/resources/filesystem/docs/overview.md` — lines 9–23, characters [294, 1036). The public API inventory and supported-format table corroborate compatibility without requiring each exported resource.
- `src/devtools/resources/filesystem/errors.py` — lines 5–34, characters [93, 988). Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.
- `src/devtools/resources/filesystem/models/base.py` — lines 15–37, characters [286, 761). Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.
- `src/devtools/resources/filesystem/resolution.py` — lines 20–72, characters [448, 2063). The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.
- `src/devtools/tools/filesystem.py` — lines 28–65, characters [636, 2043). Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.
- `tests/context/repository/test_observation.py` — lines 348–404, characters [12319, 14583). Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.
- `tests/core/paths/test_resolved_path.py` — lines 15–54, characters [259, 1753). Supplies path wrapper construction examples for controlled fixtures, duplicating established ResolvedPath semantics.
- `tests/resources/filesystem/test_reading.py` — lines 148–233, characters [4742, 7710). Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.
- `tests/resources/filesystem/test_resolution.py` — lines 26–61, characters [496, 1911). Exercises suffix and codec mappings; it is complementary to the final-suffix documentation when used as a complete resolver alternative.
- `tests/tools/test_filesystem.py` — lines 139–265, characters [4073, 8063). Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.

### O2

**REQUIRED**

- None.

**HELPFUL_ONLY**

- `src/devtools/resources/filesystem/docs/roadmap.md` — lines 11–37, characters [332, 1267). Corroborates deferred streaming and package exclusions, which the task already prescribes for this change.
- `src/devtools/resources/filesystem/errors.py` — lines 5–34, characters [93, 988). Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.
- `src/devtools/resources/filesystem/reading.py` — lines 50–116, characters [1608, 3504). Locates existing acquisition and error seams for implementing the task-defined lifecycle and regression tests; the future bound and fixture design do not require an additional current lifecycle fact.

### O3

**REQUIRED**

- `src/devtools/resources/filesystem/docs/io.md` — lines 3–16, characters [18, 411). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.
- `src/devtools/resources/filesystem/reading.py` — lines 78–90, characters [2435, 2737). Necessary in at least one complete minimal witness: R02: This seam is necessary to preserve codec behavior by leaving the existing resolution and decode path intact. It permits black-box preservation across every concrete codec.
- `src/devtools/resources/filesystem/resolution.py` — lines 20–72, characters [448, 2063). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.
- `tests/resources/filesystem/test_resolution.py` — lines 26–61, characters [496, 1911). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.

**HELPFUL_ONLY**

- `src/devtools/context/repository/observation.py` — lines 126–158, characters [4311, 5347). An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.
- `src/devtools/models/benchmarks/storage.py` — lines 45–53, characters [1214, 1713). Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.
- `src/devtools/resources/filesystem/__init__.py` — lines 4–41, characters [86, 982). Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.
- `src/devtools/resources/filesystem/codecs/csv.py` — lines 30–109, characters [693, 3373). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/json.py` — lines 31–125, characters [729, 3905). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/markdown.py` — lines 21–47, characters [437, 1386). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/text.py` — lines 21–47, characters [433, 1343). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/docs/codecs.md` — lines 3–29, characters [21, 1246). Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.
- `src/devtools/resources/filesystem/docs/csv.md` — lines 32–47, characters [1391, 2119). Establishes empty CSV remains a format failure and source text remains provenance; useful for choosing format-appropriate empty-input tests.
- `src/devtools/resources/filesystem/docs/json.md` — lines 43–59, characters [1425, 2354). Documents JSON source/value separation and strict format errors; useful regression guidance without rewriting the parser.
- `src/devtools/resources/filesystem/docs/markdown.md` — lines 20–38, characters [868, 1788). Distinguishes exact Markdown file content from normalized derived section content, avoiding an overbroad line-ending assertion.
- `src/devtools/resources/filesystem/docs/models.md` — lines 5–51, characters [100, 1820). Provides shared model hierarchy and source metadata semantics, corroborating unchanged codec results.
- `src/devtools/resources/filesystem/docs/overview.md` — lines 9–23, characters [294, 1036). The public API inventory and supported-format table corroborate compatibility without requiring each exported resource.
- `src/devtools/resources/filesystem/errors.py` — lines 5–34, characters [93, 988). Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.
- `src/devtools/resources/filesystem/models/base.py` — lines 15–37, characters [286, 761). Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.
- `src/devtools/resources/filesystem/models/csv.py` — lines 169–212, characters [5485, 7130). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/list.py` — lines 23–38, characters [606, 1181). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/object.py` — lines 23–42, characters [574, 1294). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/scalar.py` — lines 16–20, characters [367, 546). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/markdown/file.py` — lines 16–39, characters [453, 1189). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/text.py` — lines 12–42, characters [228, 1183). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/tools/filesystem.py` — lines 28–65, characters [636, 2043). Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.
- `tests/context/repository/test_observation.py` — lines 348–404, characters [12319, 14583). Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.
- `tests/resources/filesystem/codecs/test_csv.py` — lines 26–80, characters [445, 2391). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_json.py` — lines 27–110, characters [491, 3287). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_markdown.py` — lines 21–57, characters [364, 1499). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_text.py` — lines 21–77, characters [362, 2170). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/test_models.py` — lines 25–79, characters [391, 2350). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/test_reading.py` — lines 148–233, characters [4742, 7710). Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.
- `tests/tools/test_filesystem.py` — lines 139–265, characters [4073, 8063). Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.

### O4

**REQUIRED**

- `AGENTS.md` — lines 78–86, characters [3856, 4424); lines 173–179, characters [8227, 8549). Necessary in at least one complete minimal witness: R05: Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.
- `src/devtools/resources/filesystem/docs/io.md` — lines 3–16, characters [18, 411). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.
- `src/devtools/resources/filesystem/docs/overview.md` — lines 60–71, characters [1925, 2476). Necessary in at least one complete minimal witness: R05: Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.
- `src/devtools/resources/filesystem/reading.py` — lines 50–90, characters [1608, 2737); lines 107–116, characters [3200, 3504); lines 52–64, characters [1633, 2124); lines 72–76, characters [2231, 2434). Necessary in at least one complete minimal witness: R04: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.; R17: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.
- `src/devtools/resources/filesystem/resolution.py` — lines 20–72, characters [448, 2063). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.
- `tests/resources/filesystem/test_resolution.py` — lines 26–61, characters [496, 1911). Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.

**HELPFUL_ONLY**

- `src/devtools/core/paths/docs/overview.md` — lines 35–47, characters [1134, 1737). Explains the path wrapper and limits of absolute-path validation; the reader already shows .value usage and the task protects core resolution.
- `src/devtools/core/paths/models.py` — lines 14–38, characters [221, 963). Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.
- `src/devtools/resources/filesystem/__init__.py` — lines 4–41, characters [86, 982). Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.
- `src/devtools/resources/filesystem/docs/codecs.md` — lines 3–29, characters [21, 1246). Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.
- `src/devtools/resources/filesystem/docs/roadmap.md` — lines 11–37, characters [332, 1267). Corroborates deferred streaming and package exclusions, which the task already prescribes for this change.
- `src/devtools/resources/filesystem/errors.py` — lines 5–34, characters [93, 988). Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.
- `src/devtools/resources/filesystem/writing.py` — lines 33–45, characters [692, 1229). Shows atomic writing has its own implementation and documented durability limit. It is protected by the task; a local read acquisition change need not inspect every write operation.
- `src/devtools/tools/docs/overview.md` — lines 10–25, characters [313, 1313). Clarifies Tool adaptation and lack of authorization ownership, useful corroboration of the protected higher boundary.
- `src/devtools/tools/filesystem.py` — lines 28–65, characters [636, 2043). Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.
- `tests/context/repository/test_observation.py` — lines 348–404, characters [12319, 14583). Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.
- `tests/resources/filesystem/test_reading.py` — lines 148–233, characters [4742, 7710). Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.
- `tests/resources/filesystem/test_writing.py` — lines 28–59, characters [493, 1683). Existing atomic-write regression corroborates the unchanged adjacent lifecycle; the read-only acquisition change does not make the write test a required evidence source.
- `tests/tools/test_filesystem.py` — lines 139–265, characters [4073, 8063). Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.

### O5

**REQUIRED**

- `tests/resources/filesystem/test_reading.py` — lines 29–50, characters [529, 1225); lines 67–145, characters [1780, 4740); lines 182–233, characters [6056, 7710). Necessary in at least one complete minimal witness: R06: This is a necessary current regression constraint, not a requirement to read a test merely because new tests are requested. Leaving these injections unchanged would stop them exercising the new finite acquisition path.

**HELPFUL_ONLY**

- `src/devtools/core/paths/models.py` — lines 14–38, characters [221, 963). Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.
- `src/devtools/resources/filesystem/codecs/csv.py` — lines 30–109, characters [693, 3373). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/json.py` — lines 31–125, characters [729, 3905). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/markdown.py` — lines 21–47, characters [437, 1386). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/codecs/text.py` — lines 21–47, characters [433, 1343). Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.
- `src/devtools/resources/filesystem/docs/codecs.md` — lines 3–29, characters [21, 1246). Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.
- `src/devtools/resources/filesystem/docs/csv.md` — lines 32–47, characters [1391, 2119). Establishes empty CSV remains a format failure and source text remains provenance; useful for choosing format-appropriate empty-input tests.
- `src/devtools/resources/filesystem/docs/json.md` — lines 43–59, characters [1425, 2354). Documents JSON source/value separation and strict format errors; useful regression guidance without rewriting the parser.
- `src/devtools/resources/filesystem/docs/markdown.md` — lines 20–38, characters [868, 1788). Distinguishes exact Markdown file content from normalized derived section content, avoiding an overbroad line-ending assertion.
- `src/devtools/resources/filesystem/docs/models.md` — lines 5–51, characters [100, 1820). Provides shared model hierarchy and source metadata semantics, corroborating unchanged codec results.
- `src/devtools/resources/filesystem/errors.py` — lines 5–34, characters [93, 988). Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.
- `src/devtools/resources/filesystem/models/base.py` — lines 15–37, characters [286, 761). Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.
- `src/devtools/resources/filesystem/models/csv.py` — lines 169–212, characters [5485, 7130). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/list.py` — lines 23–38, characters [606, 1181). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/object.py` — lines 23–42, characters [574, 1294). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/json/scalar.py` — lines 16–20, characters [367, 546). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/markdown/file.py` — lines 16–39, characters [453, 1189). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/models/text.py` — lines 12–42, characters [228, 1183). Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.
- `src/devtools/resources/filesystem/reading.py` — lines 50–116, characters [1608, 3504). Locates existing acquisition and error seams for implementing the task-defined lifecycle and regression tests; the future bound and fixture design do not require an additional current lifecycle fact.
- `src/devtools/resources/filesystem/resolution.py` — lines 20–72, characters [448, 2063). The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.
- `tests/context/repository/test_observation.py` — lines 348–404, characters [12319, 14583). Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.
- `tests/core/paths/test_resolved_path.py` — lines 15–54, characters [259, 1753). Supplies path wrapper construction examples for controlled fixtures, duplicating established ResolvedPath semantics.
- `tests/resources/filesystem/codecs/test_csv.py` — lines 26–80, characters [445, 2391). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_json.py` — lines 27–110, characters [491, 3287). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_markdown.py` — lines 21–57, characters [364, 1499). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/codecs/test_text.py` — lines 21–77, characters [362, 2170). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/test_models.py` — lines 25–79, characters [391, 2350). Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.
- `tests/resources/filesystem/test_resolution.py` — lines 26–61, characters [496, 1911). Exercises suffix and codec mappings; it is complementary to the final-suffix documentation when used as a complete resolver alternative.
- `tests/tools/test_filesystem.py` — lines 139–265, characters [4073, 8063). Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.

### O6

**REQUIRED**

- `AGENTS.md` — lines 228–239, characters [10713, 11282). Necessary in at least one complete minimal witness: R12: The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.
- `pyproject.toml` — lines 34–55, characters [585, 1031); lines 57–71, characters [1032, 1227); lines 73–78, characters [1228, 1368). Necessary in at least one complete minimal witness: R13: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.; R14: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.; R15: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.
- `scripts/validate_development.py` — lines 14–23, characters [248, 657). Necessary in at least one complete minimal witness: R12: The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.
- `src/devtools/resources/filesystem/docs/io.md` — lines 18–38, characters [412, 1171); lines 40–80, characters [1172, 2499). Necessary in at least one complete minimal witness: R08: Accurate documentation requires reconciling these specific existing behavior claims, not adding a new guarantee beside contradictory text.
- `src/devtools/resources/filesystem/docs/overview.md` — lines 9–23, characters [294, 1036); lines 66–100, characters [2161, 3247). Necessary in at least one complete minimal witness: R09: The requested overview update must distinguish the new acquisition guarantee from stronger excluded pathname/security guarantees within the existing public documentation.
- `src/devtools/resources/filesystem/docs/roadmap.md` — lines 3–37, characters [31, 1267). Necessary in at least one complete minimal witness: R10: The new feature must be removed from deferred scope without promoting streaming parsers or a decoded-memory guarantee. This requires the existing roadmap distinction.
- `src/devtools/resources/filesystem/reading.py` — lines 32–49, characters [717, 1608). Necessary in at least one complete minimal witness: R11: The conditional public-API documentation update is applicable because the callable itself contains a behavior statement invalidated by the new acquisition algorithm.
- `tests/context/repository/test_observation.py` — lines 31–65, characters [672, 1755); lines 384–404, characters [13790, 14583); lines 478–497, characters [16810, 17514). Necessary in at least one complete minimal witness: R07: Without this information the finite acquisition change can invalidate existing caller regressions even if all filesystem tests are corrected.

**HELPFUL_ONLY**

- `src/devtools/context/repository/observation.py` — lines 126–158, characters [4311, 5347). An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.
- `src/devtools/models/benchmarks/storage.py` — lines 45–53, characters [1214, 1713). Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.
- `src/devtools/resources/filesystem/__init__.py` — lines 4–41, characters [86, 982). Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.
- `src/devtools/resources/filesystem/resolution.py` — lines 20–72, characters [448, 2063). The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.
- `src/devtools/resources/filesystem/writing.py` — lines 33–45, characters [692, 1229). Shows atomic writing has its own implementation and documented durability limit. It is protected by the task; a local read acquisition change need not inspect every write operation.
- `src/devtools/tools/docs/overview.md` — lines 10–25, characters [313, 1313). Clarifies Tool adaptation and lack of authorization ownership, useful corroboration of the protected higher boundary.
- `src/devtools/tools/filesystem.py` — lines 28–65, characters [636, 2043). Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.
- `tests/resources/filesystem/test_reading.py` — lines 148–233, characters [4742, 7710). Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.
- `tests/resources/filesystem/test_writing.py` — lines 28–59, characters [493, 1683). Existing atomic-write regression corroborates the unchanged adjacent lifecycle; the read-only acquisition change does not make the write test a required evidence source.
- `tests/scripts/test_validate_development.py` — lines 17–68, characters [313, 2104). The profile tests verify selected arguments and failure forwarding, but do not independently exclude additional coverage-overriding arguments. They corroborate the protected policy without substituting for the script or operating guide.
- `tests/tools/test_filesystem.py` — lines 139–265, characters [4073, 8063). Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.

## Complete REQUIRED-resource union

11 distinct resources:

- `src/devtools/resources/filesystem/docs/io.md` — `056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300`
- `tests/context/repository/test_observation.py` — `094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced`
- `src/devtools/resources/filesystem/reading.py` — `551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40`
- `scripts/validate_development.py` — `63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a`
- `pyproject.toml` — `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0`
- `src/devtools/resources/filesystem/docs/overview.md` — `8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3`
- `tests/resources/filesystem/test_resolution.py` — `87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42`
- `src/devtools/resources/filesystem/docs/roadmap.md` — `892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df`
- `tests/resources/filesystem/test_reading.py` — `8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33`
- `AGENTS.md` — `953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d`
- `src/devtools/resources/filesystem/resolution.py` — `a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56`

## Semantic-unit inventory and support alternatives

42 units: TASK_BACKED = 25, REPOSITORY_SUPPORTED = 17, TASK_AND_REPOSITORY_SUPPORTED = 0.

Coordinates are zero-based half-open Unicode character offsets; line numbers are one-based inclusive. Exact quoted spans and all provenance are retained in the JSON. Each alternative is conjunctive; alternatives substitute for one another.

### T01 — TASK_BACKED

Replace finite whole-file acquisition inside the existing filesystem reader with bounded chunks.

Obligations: O1.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [93, 267): In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite.

### T02 — TASK_BACKED

Preserve the public ResolvedPath, file_format, max_bytes and DEFAULT_MAX_READ_BYTES contract.

Obligations: O1.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [268, 368): Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract

### T03 — TASK_BACKED

A preliminary stat is optional and cannot permit unbounded acquisition of a file that grows.

Obligations: O1.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [521, 627): A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.

### T04 — TASK_BACKED

For a finite limit retain no more than max_bytes payload bytes and acquire at most one additional sentinel byte to distinguish exact EOF from excess.

Obligations: O2.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [680, 815): retain at most `max_bytes` payload bytes and acquire at most one additional byte to distinguish exact-boundary EOF from oversized input

### T05 — TASK_BACKED

Every finite-mode read request is bounded.

Obligations: O2.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [817, 847): bound individual read requests

### T06 — TASK_BACKED

Release the acquired stream on success and every failure.

Obligations: O2.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [852, 900): release the stream on success and every failure.

### T07 — TASK_BACKED

Excess raises FileTooLargeError and never returns a truncated model.

Obligations: O2.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [901, 976): Raise `FileTooLargeError` on excess instead of returning a truncated model.

### T08 — TASK_BACKED

The acquisition guarantee makes none of the excluded model-memory, snapshot, pathname-race, containment, authorization, or locking claims.

Obligations: O2.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [977, 1112): Do not claim a bound on decoded model memory, a stable file snapshot, race-free pathname checks, containment, authorization or locking.

### T09 — TASK_BACKED

Preserve format override, suffix inference and the existing resolution functions.

Obligations: O3.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1118, 1225): Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference.

### T10 — TASK_BACKED

Delegate complete accepted bytes to the existing codecs without content rewriting.

Obligations: O3.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1226, 1304): Pass complete accepted bytes to the existing codecs without rewriting content.

### T11 — TASK_BACKED

Retain all six specified rich result classes.

Obligations: O3.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1305, 1427): Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results

### T12 — TASK_BACKED

Preserve UTF-8 decoding, original line endings, encoding metadata and source byte-size metadata.

Obligations: O3.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1429, 1500): UTF-8 decoding, original line endings, encoding and byte-size metadata.

### T13 — TASK_BACKED

Chunk boundaries may split multibyte sequences; no replacement decoding is introduced and codec-domain failures retain their existing classes.

Obligations: O3.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1501, 1678): Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.

### T14 — TASK_BACKED

Preserve the existing missing-path, non-regular-file, permission, unsupported-format and excess error boundaries.

Obligations: O4.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1684, 1826): Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input.

### T15 — TASK_BACKED

Normalize stream-open and chunk-read PermissionError failures with causal FilesystemPermissionError exceptions.

Obligations: O4.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1827, 1949): Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions.

### T16 — TASK_BACKED

Keep the change within the existing filesystem package and preserve atomic writing, format ownership, core path resolution and Tool boundaries.

Obligations: O4.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [1950, 2162): Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

### T17 — TASK_BACKED

Add controlled read tests at the specified test location and relevant codec/model tests covering the limit domain.

Obligations: O5.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2168, 2343): Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits

### T18 — TASK_BACKED

Test growth after stat, short reads, EOF, closure on exceptions and open/read permission failures.

Obligations: O5.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2345, 2450): growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures

### T19 — TASK_BACKED

Test multibyte splits, invalid UTF-8, explicit overrides and every supported rich result type.

Obligations: O5.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2452, 2576): multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types.

### T20 — TASK_BACKED

Prove finite request and retention bounds using deterministic instrumented streams.

Obligations: O5.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2577, 2740): Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.

### T21 — TASK_BACKED

Update I/O, overview, roadmap and applicable public API documentation to state the bound and its limitations.

Obligations: O6.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2746, 2951): Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately.

### T22 — TASK_BACKED

Preserve existing callers.

Obligations: O6.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2952, 2977): Preserve existing callers

### T23 — TASK_BACKED

Preserve the protected validation profile and run it along with Ruff, formatting, mypy and diff checks.

Obligations: O6.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [2982, 3186): the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks.

### T24 — TASK_BACKED

Do not expand into binary codecs, new formats, streaming format parsing, secure filesystem policy or production retrieval changes.

Obligations: O6.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [3187, 3314): Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

### R01 — REPOSITORY_SUPPORTED

The current public reader takes ResolvedPath and keyword-only file_format/max_bytes, uses the 16 MiB default, permits None and rejects negative limits.

Obligations: O1.

Necessity: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.

Inferability: The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.

Task support [89, 629): O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.

**R01.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

The implementation defines the signature and both checks.

- `src/devtools/resources/filesystem/reading.py` lines 23–35, characters [526, 906).
- `src/devtools/resources/filesystem/reading.py` lines 107–116, characters [3200, 3504).

**R01.A2 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/io.md`

The I/O contract independently states the callable shape, defaults, limit meanings and allocation-before-rejection behavior.

- `src/devtools/resources/filesystem/docs/io.md` lines 20–30, characters [424, 913).

### R02 — REPOSITORY_SUPPORTED

The current integration resolves format only after successful acquisition/size validation, bypasses inference for an explicit format, calls resolve_codec, and returns codec.decode(original_path, complete_bytes) with codec defaults.

Obligations: O3.

Necessity: This seam is necessary to preserve codec behavior by leaving the existing resolution and decode path intact. It permits black-box preservation across every concrete codec.

Inferability: For identical complete bytes, original path and unchanged codec invocation, existing codec/model behavior is preserved. No independent implementation of codecs or constructors is needed. This is a preservation argument, not proof that each desired future property already exists.

Task support [1114, 1680): O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.

**R02.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

The existing integration call and its ordering are explicit.

- `src/devtools/resources/filesystem/reading.py` lines 78–90, characters [2435, 2737).

### R03 — REPOSITORY_SUPPORTED

Format resolution lowercases the final suffix; .csv, .json, .md/.markdown and .txt select four existing codecs. Unsupported suffixes and unimplemented formats, including binary, raise FileFormatError.

Obligations: O3, O4.

Necessity: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.

Inferability: A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.

Task support [1114, 1680): O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.

**R03.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/resolution.py`

The suffix map, codec map and error boundaries are explicit.

- `src/devtools/resources/filesystem/resolution.py` lines 20–72, characters [448, 2063).

**R03.A2 — INFERABLE_SUPPORT**: `src/devtools/resources/filesystem/docs/io.md`, `tests/resources/filesystem/test_resolution.py`

The I/O contract supplies final-suffix semantics; independent contract tests supply the concrete codec mappings and unsupported/binary failures.

- `src/devtools/resources/filesystem/docs/io.md` lines 3–16, characters [18, 411).
- `tests/resources/filesystem/test_resolution.py` lines 26–61, characters [496, 1911).

### R04 — REPOSITORY_SUPPORTED

The reader checks existence, regular-file status and stat before acquisition; size rejection precedes codec resolution and decoding.

Obligations: O4.

Necessity: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.

Inferability: No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.

Task support [1680, 2164): O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

**R04.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

Control flow and raise-from statements establish current error precedence and causal normalization.

- `src/devtools/resources/filesystem/reading.py` lines 50–90, characters [1608, 2737).
- `src/devtools/resources/filesystem/reading.py` lines 107–116, characters [3200, 3504).

### R05 — REPOSITORY_SUPPORTED

Filesystem owns its existing models, codecs, format resolution, reads and atomic writes; core paths and higher Tool concerns retain their separate ownership.

Obligations: O4.

Necessity: Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.

Inferability: Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.

Task support [1680, 2164): O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

**R05.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/overview.md`

The package overview identifies consumed path primitives and the filesystem ownership boundary.

- `src/devtools/resources/filesystem/docs/overview.md` lines 60–71, characters [1925, 2476).

**R05.A2 — DIRECT_SUPPORT**: `AGENTS.md`

The operating guide independently assigns canonical path/filesystem substrates and separates Resource and Tool authority.

- `AGENTS.md` lines 78–86, characters [3856, 4424).
- `AGENTS.md` lines 173–179, characters [8227, 8549).

### R06 — REPOSITORY_SUPPORTED

Existing reader regressions invoke the public rich-model API and inject growth/read failures by monkeypatching Path.read_bytes; the finite-read replacement must migrate these existing injections while retaining their assertions.

Obligations: O5.

Necessity: This is a necessary current regression constraint, not a requirement to read a test merely because new tests are requested. Leaving these injections unchanged would stop them exercising the new finite acquisition path.

Inferability: New instrumented-stream fixture names and decomposition remain free choices. The original tests establish current seams, not the design of future fixtures.

Task support [2164, 2742): O5. Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits, growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures, multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types. Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.

**R06.A1 — DIRECT_SUPPORT**: `tests/resources/filesystem/test_reading.py`

These tests contain both rich-result examples and obsolete acquisition-specific injections.

- `tests/resources/filesystem/test_reading.py` lines 29–50, characters [529, 1225).
- `tests/resources/filesystem/test_reading.py` lines 67–145, characters [1780, 4740).
- `tests/resources/filesystem/test_reading.py` lines 182–233, characters [6056, 7710).

### R07 — REPOSITORY_SUPPORTED

Two existing repository-observation permission tests also patch Path.read_bytes through finite filesystem reads, so preserving the ordinary caller regression suite requires adapting these injections.

Obligations: O6.

Necessity: Without this information the finite acquisition change can invalidate existing caller regressions even if all filesystem tests are corrected.

Inferability: The tests call the existing observation API with its finite default. The full fixture setup at lines 31-65 establishes that context. Adaptation preserves caller semantics, not production caller behavior changes.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R07.A1 — DIRECT_SUPPORT**: `tests/context/repository/test_observation.py`

Both failure-injection sites are explicit in an eligible resource outside the filesystem tests.

- `tests/context/repository/test_observation.py` lines 31–65, characters [672, 1755).
- `tests/context/repository/test_observation.py` lines 384–404, characters [13790, 14583).
- `tests/context/repository/test_observation.py` lines 478–497, characters [16810, 17514).

### R08 — REPOSITORY_SUPPORTED

The I/O document currently claims complete read_bytes acquisition with pre/post checks and says streaming bounded reads are unimplemented; its write/security sections delimit unaffected claims.

Obligations: O6.

Necessity: Accurate documentation requires reconciling these specific existing behavior claims, not adding a new guarantee beside contradictory text.

Inferability: The task provides the replacement guarantee. Current document text is necessary only to know which claims and surrounding boundaries must be reconciled.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R08.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/io.md`

Current acquisition and adjacent limitation claims are explicit.

- `src/devtools/resources/filesystem/docs/io.md` lines 18–38, characters [412, 1171).
- `src/devtools/resources/filesystem/docs/io.md` lines 40–80, characters [1172, 2499).

### R09 — REPOSITORY_SUPPORTED

The filesystem overview owns the public API inventory, supported-format table and limitations, including the current race-free-limits wording and a link to the detailed I/O contract.

Obligations: O6.

Necessity: The requested overview update must distinguish the new acquisition guarantee from stronger excluded pathname/security guarantees within the existing public documentation.

Inferability: The overview is needed for its current public claims, not merely its filename.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R09.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/overview.md`

This is the current public overview and its limitation context.

- `src/devtools/resources/filesystem/docs/overview.md` lines 9–23, characters [294, 1036).
- `src/devtools/resources/filesystem/docs/overview.md` lines 66–100, characters [2161, 3247).

### R10 — REPOSITORY_SUPPORTED

The filesystem roadmap currently groups strict bounded reads with future streaming and a hard-memory-bound suggestion, while separately deferring binary and new-format work.

Obligations: O6.

Necessity: The new feature must be removed from deferred scope without promoting streaming parsers or a decoded-memory guarantee. This requires the existing roadmap distinction.

Inferability: Future scope is not authorized by its presence in the roadmap; the task controls the narrower change.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R10.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/roadmap.md`

The current roadmap separates several deferred scopes but groups bounded acquisition with streaming.

- `src/devtools/resources/filesystem/docs/roadmap.md` lines 3–37, characters [31, 1267).

### R11 — REPOSITORY_SUPPORTED

The public read docstring currently warns that grown contents can be read into memory before the post-check rejects them.

Obligations: O6.

Necessity: The conditional public-API documentation update is applicable because the callable itself contains a behavior statement invalidated by the new acquisition algorithm.

Inferability: This location is necessary because the current text establishes a distinct stale public documentation surface; implementation ownership alone would not make it necessary.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R11.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

The public callable docstring contains the outdated acquisition claim.

- `src/devtools/resources/filesystem/reading.py` lines 32–49, characters [717, 1608).

### R12 — REPOSITORY_SUPPORTED

The protected development entry point runs ordinary tests while excluding tests/experiments before collection, retaining the configured coverage behavior.

Obligations: O6.

Necessity: The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.

Inferability: The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R12.A1 — INFERABLE_SUPPORT**: `scripts/validate_development.py`

The script passes only the test root and ignore argument into pytest; configuration therefore remains in force.

- `scripts/validate_development.py` lines 14–23, characters [248, 657).

**R12.A3 — DIRECT_SUPPORT**: `AGENTS.md`

The operating policy states the exact invocation, pre-collection exclusion and retention of configured coverage.

- `AGENTS.md` lines 228–239, characters [10713, 11282).

### R13 — REPOSITORY_SUPPORTED

Pytest uses strict config/markers and devtools branch coverage; pytest and coverage reporting retain a 100% requirement.

Obligations: O6.

Necessity: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.

Inferability: The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R13.A1 — DIRECT_SUPPORT**: `pyproject.toml`

The configuration is the authoritative current tool setup.

- `pyproject.toml` lines 34–55, characters [585, 1031).

### R14 — REPOSITORY_SUPPORTED

Ruff targets Python 3.12 with line length 88, selects ALL rules with D203/D213 ignored and S101 ignored in tests.

Obligations: O6.

Necessity: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.

Inferability: The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R14.A1 — DIRECT_SUPPORT**: `pyproject.toml`

The configuration is the authoritative current tool setup.

- `pyproject.toml` lines 57–71, characters [1032, 1227).

### R15 — REPOSITORY_SUPPORTED

Mypy is strict for Python 3.12, checks src/tests/experiments, enables explicit package bases and uses src as its search path.

Obligations: O6.

Necessity: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.

Inferability: The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.

Task support [2742, 3315): O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

**R15.A1 — DIRECT_SUPPORT**: `pyproject.toml`

The configuration is the authoritative current tool setup.

- `pyproject.toml` lines 73–78, characters [1228, 1368).

### R16 — REPOSITORY_SUPPORTED

The current acquisition performs a preliminary stat, complete read_bytes and a post-read size check, allowing grown content allocation before rejection.

Obligations: O1.

Necessity: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.

Inferability: The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.

Task support [89, 629): O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.

**R16.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

The implementation defines the signature and both checks.

- `src/devtools/resources/filesystem/reading.py` lines 37–39, characters [907, 1121).
- `src/devtools/resources/filesystem/reading.py` lines 61–82, characters [1922, 2542).

**R16.A2 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/docs/io.md`

The I/O contract independently states the callable shape, defaults, limit meanings and allocation-before-rejection behavior.

- `src/devtools/resources/filesystem/docs/io.md` lines 24–38, characters [499, 1171).

### R17 — REPOSITORY_SUPPORTED

The current reader translates inspection/read PermissionError to FilesystemPermissionError using raise-from causal exceptions.

Obligations: O4.

Necessity: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.

Inferability: No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.

Task support [1680, 2164): O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

**R17.A1 — DIRECT_SUPPORT**: `src/devtools/resources/filesystem/reading.py`

Control flow and raise-from statements establish current error precedence and causal normalization.

- `src/devtools/resources/filesystem/reading.py` lines 52–64, characters [1633, 2124).
- `src/devtools/resources/filesystem/reading.py` lines 72–76, characters [2231, 2434).

### T25 — TASK_BACKED

Preserve the complete limit-value domain: 16 MiB default, None unbounded, negative rejection, zero and exact boundary.

Obligations: O1.

Necessity: This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.

Inferability: The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.

Task support [370, 520): including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary.

## All minimal complete obligation witnesses

All listed units and resources within a witness are required together; any complete witness for that obligation substitutes for another. No helpful corroboration is part of a witness.

### O1 (2 witnesses)

- **O1.W1**: units R01, R16, T01, T02, T03, T25; resources `src/devtools/resources/filesystem/docs/io.md`.
- **O1.W2**: units R01, R16, T01, T02, T03, T25; resources `src/devtools/resources/filesystem/reading.py`.

Indispensable resources: (repository-empty).

Indispensable units: R01, R16, T01, T02, T03, T25.

### O2 (1 witnesses)

- **O2.W1**: units T04, T05, T06, T07, T08; resources (repository-empty).

Indispensable resources: (repository-empty).

Indispensable units: T04, T05, T06, T07, T08.

### O3 (2 witnesses)

- **O3.W1**: units R02, R03, T09, T10, T11, T12, T13; resources `src/devtools/resources/filesystem/reading.py`, `src/devtools/resources/filesystem/resolution.py`.
- **O3.W2**: units R02, R03, T09, T10, T11, T12, T13; resources `src/devtools/resources/filesystem/docs/io.md`, `src/devtools/resources/filesystem/reading.py`, `tests/resources/filesystem/test_resolution.py`.

Indispensable resources: `src/devtools/resources/filesystem/reading.py`.

Indispensable units: R02, R03, T09, T10, T11, T12, T13.

### O4 (4 witnesses)

- **O4.W1**: units R03, R04, R05, R17, T14, T15, T16; resources `src/devtools/resources/filesystem/reading.py`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/resolution.py`.
- **O4.W2**: units R03, R04, R05, R17, T14, T15, T16; resources `src/devtools/resources/filesystem/reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`.
- **O4.W3**: units R03, R04, R05, R17, T14, T15, T16; resources `src/devtools/resources/filesystem/docs/io.md`, `src/devtools/resources/filesystem/reading.py`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`.
- **O4.W4**: units R03, R04, R05, R17, T14, T15, T16; resources `src/devtools/resources/filesystem/docs/io.md`, `src/devtools/resources/filesystem/reading.py`, `tests/resources/filesystem/test_resolution.py`, `AGENTS.md`.

Indispensable resources: `src/devtools/resources/filesystem/reading.py`.

Indispensable units: R03, R04, R05, R17, T14, T15, T16.

### O5 (1 witnesses)

- **O5.W1**: units R06, T17, T18, T19, T20; resources `tests/resources/filesystem/test_reading.py`.

Indispensable resources: `tests/resources/filesystem/test_reading.py`.

Indispensable units: R06, T17, T18, T19, T20.

### O6 (2 witnesses)

- **O6.W1**: units R07, R08, R09, R10, R11, R12, R13, R14, R15, T21, T22, T23, T24; resources `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`.
- **O6.W2**: units R07, R08, R09, R10, R11, R12, R13, R14, R15, T21, T22, T23, T24; resources `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `AGENTS.md`.

Indispensable resources: `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`.

Indispensable units: R07, R08, R09, R10, R11, R12, R13, R14, R15, T21, T22, T23, T24.

## Complete task sufficiency

32 complete combinations; 9 distinct sufficient resource unions; 4 inclusion-minimal resource unions.

Sufficient resource-count range: 9–11. Cross-obligation reuse is retained.

| Combination | Witness choices |
|---|---|
| TC001 | O1.W1, O2.W1, O3.W1, O4.W1, O5.W1, O6.W1 |
| TC002 | O1.W1, O2.W1, O3.W1, O4.W1, O5.W1, O6.W2 |
| TC003 | O1.W1, O2.W1, O3.W1, O4.W2, O5.W1, O6.W1 |
| TC004 | O1.W1, O2.W1, O3.W1, O4.W2, O5.W1, O6.W2 |
| TC005 | O1.W1, O2.W1, O3.W1, O4.W3, O5.W1, O6.W1 |
| TC006 | O1.W1, O2.W1, O3.W1, O4.W3, O5.W1, O6.W2 |
| TC007 | O1.W1, O2.W1, O3.W1, O4.W4, O5.W1, O6.W1 |
| TC008 | O1.W1, O2.W1, O3.W1, O4.W4, O5.W1, O6.W2 |
| TC009 | O1.W1, O2.W1, O3.W2, O4.W1, O5.W1, O6.W1 |
| TC010 | O1.W1, O2.W1, O3.W2, O4.W1, O5.W1, O6.W2 |
| TC011 | O1.W1, O2.W1, O3.W2, O4.W2, O5.W1, O6.W1 |
| TC012 | O1.W1, O2.W1, O3.W2, O4.W2, O5.W1, O6.W2 |
| TC013 | O1.W1, O2.W1, O3.W2, O4.W3, O5.W1, O6.W1 |
| TC014 | O1.W1, O2.W1, O3.W2, O4.W3, O5.W1, O6.W2 |
| TC015 | O1.W1, O2.W1, O3.W2, O4.W4, O5.W1, O6.W1 |
| TC016 | O1.W1, O2.W1, O3.W2, O4.W4, O5.W1, O6.W2 |
| TC017 | O1.W2, O2.W1, O3.W1, O4.W1, O5.W1, O6.W1 |
| TC018 | O1.W2, O2.W1, O3.W1, O4.W1, O5.W1, O6.W2 |
| TC019 | O1.W2, O2.W1, O3.W1, O4.W2, O5.W1, O6.W1 |
| TC020 | O1.W2, O2.W1, O3.W1, O4.W2, O5.W1, O6.W2 |
| TC021 | O1.W2, O2.W1, O3.W1, O4.W3, O5.W1, O6.W1 |
| TC022 | O1.W2, O2.W1, O3.W1, O4.W3, O5.W1, O6.W2 |
| TC023 | O1.W2, O2.W1, O3.W1, O4.W4, O5.W1, O6.W1 |
| TC024 | O1.W2, O2.W1, O3.W1, O4.W4, O5.W1, O6.W2 |
| TC025 | O1.W2, O2.W1, O3.W2, O4.W1, O5.W1, O6.W1 |
| TC026 | O1.W2, O2.W1, O3.W2, O4.W1, O5.W1, O6.W2 |
| TC027 | O1.W2, O2.W1, O3.W2, O4.W2, O5.W1, O6.W1 |
| TC028 | O1.W2, O2.W1, O3.W2, O4.W2, O5.W1, O6.W2 |
| TC029 | O1.W2, O2.W1, O3.W2, O4.W3, O5.W1, O6.W1 |
| TC030 | O1.W2, O2.W1, O3.W2, O4.W3, O5.W1, O6.W2 |
| TC031 | O1.W2, O2.W1, O3.W2, O4.W4, O5.W1, O6.W1 |
| TC032 | O1.W2, O2.W1, O3.W2, O4.W4, O5.W1, O6.W2 |

**All distinct sufficient resource unions**

1. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`
2. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `src/devtools/resources/filesystem/resolution.py`
3. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`
4. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`
5. (10 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`
6. (10 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `src/devtools/resources/filesystem/resolution.py`
7. (10 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`
8. (10 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`
9. (11 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`

**Inclusion-minimal resource unions**

1. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`
2. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `scripts/validate_development.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `src/devtools/resources/filesystem/resolution.py`
3. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `tests/resources/filesystem/test_resolution.py`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`
4. (9 resources) `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`, `AGENTS.md`, `src/devtools/resources/filesystem/resolution.py`

Sufficient semantic-unit unions: 1; size range 42–42.

- R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24, T25

Task-indispensable resources: `src/devtools/resources/filesystem/docs/io.md`, `tests/context/repository/test_observation.py`, `src/devtools/resources/filesystem/reading.py`, `pyproject.toml`, `src/devtools/resources/filesystem/docs/overview.md`, `src/devtools/resources/filesystem/docs/roadmap.md`, `tests/resources/filesystem/test_reading.py`.

Task-indispensable units: R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, R12, R13, R14, R15, R16, R17, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19, T20, T21, T22, T23, T24, T25.

## Gaps, limitations and ambiguities

- REPOSITORY_INFORMATION_GAP: None.
- TASK_GAP: None.
- TASK_INTERPRETATION_GAP: None.

**Nonblocking limitations**

- L01: The exact text of docs/development/validation.md is absent from the 515-resource frame. The required current profile semantics are established independently by the operating guide, script, its tests and project configuration; no missing fact is necessary to decide this case.
- L02: Chunk size, accumulator/helper decomposition and instrumented-stream fixture shape are implementation choices. The task supplies their acceptance constraints and does not freeze names.
- L03: Exact file content and source-byte metadata must be preserved; derived logical lines or Markdown section content need not reproduce raw newline separators. Tests must assert the correct representation layer.

**Preserved ambiguities**

- A01: The task does not select the stream buffering layer or transient buffer strategy. A defensible implementation can use bounded binary requests and an unbuffered stream to avoid hidden acquisition beyond the sentinel. No process-memory, operating-system prefetch or stable-snapshot claim is inferred. Preserve the strict byte-acquisition requirement and document its layer; do not weaken it into a stat-only or returned-model-size limit.

Unresolved cell decisions: none.

## Separate self-review

Future policy and existing integration facts are separate units. The finite limit domain is one coherent API policy; payload bound, request bound and closure are separate independently checkable constraints. Existing documentation surfaces are separate because their current claims differ. Codec internals are corroboration when the unchanged complete-byte delegation seam already preserves their behavior.

- Demoted tests/scripts/test_validate_development.py from a complete protected-profile alternative to HELPFUL_ONLY: its argument assertions do not independently rule out extra coverage-overriding arguments. The script or the explicit operating policy remains necessary.
- Split API preservation from limit-value policy; split current API facts from allocation-before-rejection behavior; split causal permission normalization from error sequencing; split pytest/coverage, Ruff and mypy configuration facts. No change to witnesses was forced by these semantic granularity corrections.
- Retained O2 as a repository-empty witness: its precise acquisition, request, sentinel, closure and exclusion requirements are entirely prescribed by the task. Existing reader and exception resources corroborate implementation context but are not separate O2 prerequisites.
- Kept codecs and model implementations HELPFUL_ONLY for O3/O5 when complete accepted bytes continue through the unchanged decode seam. Existing result behavior is preserved compositionally; the future task explicitly specifies the required rich results, text fidelity and decoding failures.
- Included the repository-observation read_bytes permission injections under O6 after inspecting their complete test functions and finite-bound fixture setup; package locality does not exclude current caller regression dependencies.
- Treated the absent validation documentation page as a bounded limitation rather than a repository-information gap because its required policy facts are available from eligible independent sources.
- Kept atomic-write internals, path implementation and Tool adapter details as corroboration where the task already excludes changes. Ownership evidence remains a compact alternative, rather than a union of every adjacent implementation.
- Recomputed every minimal witness, all cross-obligation combinations and sufficient unions after revisions; REQUIRED membership was checked against witness membership rather than equated with indispensability.

## Validation and provenance

The standalone builder authenticates all original inputs, exact native identities, every cell/span, semantic commitments, support algebra, all minimal witnesses and task arithmetic. It derives statistics and this Markdown deterministically, exercises adversarial mutations, and verifies scientific byte hashes. Verification runs independently in a separate Python process.

All excluded access categories are attested NO in the machine-readable review. One primary adjudicator performed the work and its separate self-review. No second reviewer was used.

Scientific artifacts: `stage_c_review.json`, `stage_c_statistics.json`, `STAGE_C_REVIEW.md`, `stage_c_validation.json`, `stage_c_hashes.json`, `stage_c_method.md`, `stage_c_builder.py`.

Scratch navigation/ledger state and the local handoff are excluded from scientific evidence and hashes.

## Reviewed statistics

```json
{
  "actual_cells": 3090,
  "ambiguity_count": 1,
  "applicability": {
    "O1": "APPLICABLE",
    "O2": "APPLICABLE",
    "O3": "APPLICABLE",
    "O4": "APPLICABLE",
    "O5": "APPLICABLE",
    "O6": "APPLICABLE"
  },
  "case": "0015",
  "duplicate_cells": 0,
  "evidence_class_counts": {
    "REPOSITORY_SUPPORTED": 17,
    "TASK_AND_REPOSITORY_SUPPORTED": 0,
    "TASK_BACKED": 25
  },
  "expected_cells": 3090,
  "gap_counts": {
    "REPOSITORY_INFORMATION_GAP": 0,
    "TASK_GAP": 0,
    "TASK_INTERPRETATION_GAP": 0
  },
  "inclusion_minimal_resource_union_count": 4,
  "label_counts_by_obligation": {
    "O1": {
      "HELPFUL_ONLY": 16,
      "REQUIRED": 2,
      "UNNECESSARY": 497
    },
    "O2": {
      "HELPFUL_ONLY": 3,
      "REQUIRED": 0,
      "UNNECESSARY": 512
    },
    "O3": {
      "HELPFUL_ONLY": 30,
      "REQUIRED": 4,
      "UNNECESSARY": 481
    },
    "O4": {
      "HELPFUL_ONLY": 13,
      "REQUIRED": 6,
      "UNNECESSARY": 496
    },
    "O5": {
      "HELPFUL_ONLY": 29,
      "REQUIRED": 1,
      "UNNECESSARY": 485
    },
    "O6": {
      "HELPFUL_ONLY": 11,
      "REQUIRED": 8,
      "UNNECESSARY": 496
    }
  },
  "limitation_count": 3,
  "maximum_sufficient_resource_count": 11,
  "maximum_sufficient_unit_count": 42,
  "minimum_sufficient_resource_count": 9,
  "minimum_sufficient_unit_count": 42,
  "missing_cells": 0,
  "obligation_indispensability": {
    "O1": {
      "resources": [],
      "units": [
        "R01",
        "R16",
        "T01",
        "T02",
        "T03",
        "T25"
      ]
    },
    "O2": {
      "resources": [],
      "units": [
        "T04",
        "T05",
        "T06",
        "T07",
        "T08"
      ]
    },
    "O3": {
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
      ],
      "units": [
        "R02",
        "R03",
        "T09",
        "T10",
        "T11",
        "T12",
        "T13"
      ]
    },
    "O4": {
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
      ],
      "units": [
        "R03",
        "R04",
        "R05",
        "R17",
        "T14",
        "T15",
        "T16"
      ]
    },
    "O5": {
      "resources": [
        "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
      ],
      "units": [
        "R06",
        "T17",
        "T18",
        "T19",
        "T20"
      ]
    },
    "O6": {
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df"
      ],
      "units": [
        "R07",
        "R08",
        "R09",
        "R10",
        "R11",
        "R12",
        "R13",
        "R14",
        "R15",
        "T21",
        "T22",
        "T23",
        "T24"
      ]
    }
  },
  "obligations": 6,
  "required_resource_count": 11,
  "required_resource_union": [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  "resources": 515,
  "semantic_unit_count": 42,
  "sufficient_resource_union_count": 9,
  "sufficient_semantic_unit_union_count": 1,
  "task_combination_count": 32,
  "task_indispensable_resources": [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
  ],
  "task_indispensable_units": [
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R08",
    "R09",
    "R10",
    "R11",
    "R12",
    "R13",
    "R14",
    "R15",
    "R16",
    "R17",
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T08",
    "T09",
    "T10",
    "T11",
    "T12",
    "T13",
    "T14",
    "T15",
    "T16",
    "T17",
    "T18",
    "T19",
    "T20",
    "T21",
    "T22",
    "T23",
    "T24",
    "T25"
  ],
  "total_label_counts": {
    "HELPFUL_ONLY": 102,
    "REQUIRED": 21,
    "UNNECESSARY": 2967
  },
  "total_witness_count": 12,
  "unexpected_cells": 0,
  "unresolved_cells": 0,
  "witness_counts": {
    "O1": 2,
    "O2": 1,
    "O3": 2,
    "O4": 4,
    "O5": 1,
    "O6": 2
  }
}
```

## Exact frame and provenance

```json
{
  "frame": {
    "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
  },
  "provenance": {
    "MODEL": "GPT-6 Astra",
    "REASONING": "High",
    "automatic_second_reviewer": false,
    "primary_sha256": {
      "STAGE_C_REVIEW.md": "08f9ea50efbec6586f69629872874461e56335f68178cc29364d46fa3aaaa1be",
      "stage_c_builder.py": "5322777cd14c485ba72e388731d11da3fa63903466a51ddbbbb8f32bcee45e19",
      "stage_c_hashes.json": "1e5420fb77646cf19dbaa869861a89718ac4e68b1060cf3b1a02ff25c26c2efd",
      "stage_c_method.md": "8dd63021d327c9be33f3e639927b457e56b1d4cc7c4cf7cdfb7ffafd8665c6ac",
      "stage_c_review.json": "20b2c858bd8d02a79576b1d48f9d773738e32231f03277232c6d9e84b148cd77",
      "stage_c_statistics.json": "496b5fbb1e76c108b62448c8a3dddf35daf3c8ac344a7645b24526918fc24d3b",
      "stage_c_validation.json": "9a9637af76d8d5271da6d25018eb7c08f0eeacff23ba54560eda906b433d533c"
    },
    "projection": "Full unchanged primary object; exact frame bindings only.",
    "semantic_transformation": "NONE",
    "source": "PRIMARY_ASTRA_HIGH",
    "treatment_blind": true
  }
}
```

## Complete positive cells and exact spans

```json
[
  {
    "address": "AGENTS.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "packet_ordinal": 0
    },
    "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "semantic_rationale": "Canonical substrate guidance corroborates filesystem ownership; direct read and profile facts are narrower evidence.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "AGENTS.md",
        "end": 4424,
        "end_line": 86,
        "quote": "- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do\n  not reimplement path normalization, repository-root resolution, or existing\n  containment behavior.\n- Use `devtools.resources.commands` for managed subprocess work. Higher domains must\n  not call direct `subprocess` or `asyncio` subprocess APIs without explicit\n  architectural justification.\n- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded\n  reads, and atomic writes. Do not recreate those semantics in Tools, Context,\n  Agents, or experiments.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 3856,
        "start_line": 78
      }
    ]
  },
  {
    "address": "AGENTS.md",
    "inferability_rationale": "Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "packet_ordinal": 0
    },
    "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R05: Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "AGENTS.md",
        "end": 4424,
        "end_line": 86,
        "quote": "- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do\n  not reimplement path normalization, repository-root resolution, or existing\n  containment behavior.\n- Use `devtools.resources.commands` for managed subprocess work. Higher domains must\n  not call direct `subprocess` or `asyncio` subprocess APIs without explicit\n  architectural justification.\n- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded\n  reads, and atomic writes. Do not recreate those semantics in Tools, Context,\n  Agents, or experiments.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 3856,
        "start_line": 78
      },
      {
        "address": "AGENTS.md",
        "end": 8549,
        "end_line": 179,
        "quote": "Resources such as filesystem and commands may be adapted into Tools. A Tool is\nnot an Action; an Action request is not authority. Preserve:\n\n```text\nmodel proposal != authority       visibility != authorization\nTool validation != authorization  approval != automatically authority\ncapability availability != authorization\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 8227,
        "start_line": 173
      }
    ]
  },
  {
    "address": "AGENTS.md",
    "inferability_rationale": "The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "packet_ordinal": 0
    },
    "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R12: The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "AGENTS.md",
        "end": 11282,
        "end_line": 239,
        "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 10713,
        "start_line": 228
      }
    ]
  },
  {
    "address": "pyproject.toml",
    "inferability_rationale": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "packet_ordinal": 54
    },
    "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R13: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.; R14: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.; R15: Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "pyproject.toml",
        "end": 1031,
        "end_line": 55,
        "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 585,
        "start_line": 34
      },
      {
        "address": "pyproject.toml",
        "end": 1227,
        "end_line": 71,
        "quote": "[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 1032,
        "start_line": 57
      },
      {
        "address": "pyproject.toml",
        "end": 1368,
        "end_line": 78,
        "quote": "[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 1228,
        "start_line": 73
      }
    ]
  },
  {
    "address": "scripts/validate_development.py",
    "inferability_rationale": "The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "packet_ordinal": 55
    },
    "resource": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R12: The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.",
    "support_kind": [
      "INFERABLE_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "scripts/validate_development.py",
        "end": 657,
        "end_line": 23,
        "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n",
        "resource": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "start": 248,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/context/repository/observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "packet_ordinal": 165
    },
    "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
    "semantic_rationale": "An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/context/repository/observation.py",
        "end": 5347,
        "end_line": 158,
        "quote": "def _observe_resource(\n    *,\n    root: ResolvedPath,\n    address: RepositoryResourceAddress,\n    maximum_resource_bytes: int,\n) -> RepositoryResourceOccurrence:\n    \"\"\"Acquire one required occurrence within a normalized observation root.\"\"\"\n    candidate = resolve_path(\n        Path(*address.parts),\n        base_directory=root.value,\n    )\n    if not candidate.value.is_relative_to(root.value):\n        msg = f\"Repository resource resolves outside the observation root: {address}.\"\n        raise RepositoryObservationError(msg)\n\n    file = cast(\n        \"TextFile\",\n        read(\n            candidate,\n            file_format=FileFormat.TEXT,\n            max_bytes=maximum_resource_bytes,\n        ),\n    )\n    content_identity = ContentIdentity(\n        _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, file.content),\n    )\n    return RepositoryResourceOccurrence(\n        address=address,\n        content_identity=content_identity,\n        content=file.content,\n        encoding=file.encoding,\n        byte_size=file.byte_size,\n    )\n",
        "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "start": 4311,
        "start_line": 126
      }
    ]
  },
  {
    "address": "src/devtools/context/repository/observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "packet_ordinal": 165
    },
    "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
    "semantic_rationale": "An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/context/repository/observation.py",
        "end": 5347,
        "end_line": 158,
        "quote": "def _observe_resource(\n    *,\n    root: ResolvedPath,\n    address: RepositoryResourceAddress,\n    maximum_resource_bytes: int,\n) -> RepositoryResourceOccurrence:\n    \"\"\"Acquire one required occurrence within a normalized observation root.\"\"\"\n    candidate = resolve_path(\n        Path(*address.parts),\n        base_directory=root.value,\n    )\n    if not candidate.value.is_relative_to(root.value):\n        msg = f\"Repository resource resolves outside the observation root: {address}.\"\n        raise RepositoryObservationError(msg)\n\n    file = cast(\n        \"TextFile\",\n        read(\n            candidate,\n            file_format=FileFormat.TEXT,\n            max_bytes=maximum_resource_bytes,\n        ),\n    )\n    content_identity = ContentIdentity(\n        _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, file.content),\n    )\n    return RepositoryResourceOccurrence(\n        address=address,\n        content_identity=content_identity,\n        content=file.content,\n        encoding=file.encoding,\n        byte_size=file.byte_size,\n    )\n",
        "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "start": 4311,
        "start_line": 126
      }
    ]
  },
  {
    "address": "src/devtools/context/repository/observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "packet_ordinal": 165
    },
    "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
    "semantic_rationale": "An existing finite caller uses a text override and retains content, encoding and byte size; retaining the public read contract preserves it without a new caller-specific requirement.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/context/repository/observation.py",
        "end": 5347,
        "end_line": 158,
        "quote": "def _observe_resource(\n    *,\n    root: ResolvedPath,\n    address: RepositoryResourceAddress,\n    maximum_resource_bytes: int,\n) -> RepositoryResourceOccurrence:\n    \"\"\"Acquire one required occurrence within a normalized observation root.\"\"\"\n    candidate = resolve_path(\n        Path(*address.parts),\n        base_directory=root.value,\n    )\n    if not candidate.value.is_relative_to(root.value):\n        msg = f\"Repository resource resolves outside the observation root: {address}.\"\n        raise RepositoryObservationError(msg)\n\n    file = cast(\n        \"TextFile\",\n        read(\n            candidate,\n            file_format=FileFormat.TEXT,\n            max_bytes=maximum_resource_bytes,\n        ),\n    )\n    content_identity = ContentIdentity(\n        _semantic_digest(_CONTENT_IDENTITY_SEMANTICS, file.content),\n    )\n    return RepositoryResourceOccurrence(\n        address=address,\n        content_identity=content_identity,\n        content=file.content,\n        encoding=file.encoding,\n        byte_size=file.byte_size,\n    )\n",
        "resource": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "start": 4311,
        "start_line": 126
      }
    ]
  },
  {
    "address": "src/devtools/core/paths/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "packet_ordinal": 199
    },
    "resource": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
    "semantic_rationale": "Explains the path wrapper and limits of absolute-path validation; the reader already shows .value usage and the task protects core resolution.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/core/paths/docs/overview.md",
        "end": 1737,
        "end_line": 47,
        "quote": "## `ResolvedPath`\n\n`ResolvedPath(value: Path)` is a frozen, slotted absolute-path value object.\nIts `value` field is authoritative. It supports `os.PathLike[str]`, value\nequality, hashing, `str()`, and `os.fspath()`.\n\nIts mechanical accessors are `name`, `stem`, `suffix`, `suffixes`, `parent`,\n`parts`, `as_posix()`, and `as_uri()`. `parent` intentionally returns a plain\n`Path`.\n\nDirect construction validates only that `value` is absolute. `ResolvedPath`\nmeans an absolute path value; it does not imply that the path exists, is safe,\nis contained beneath a trusted root, or is authorized for access.\n",
        "resource": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "start": 1134,
        "start_line": 35
      }
    ]
  },
  {
    "address": "src/devtools/core/paths/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "packet_ordinal": 199
    },
    "resource": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
    "semantic_rationale": "Explains the path wrapper and limits of absolute-path validation; the reader already shows .value usage and the task protects core resolution.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/core/paths/docs/overview.md",
        "end": 1737,
        "end_line": 47,
        "quote": "## `ResolvedPath`\n\n`ResolvedPath(value: Path)` is a frozen, slotted absolute-path value object.\nIts `value` field is authoritative. It supports `os.PathLike[str]`, value\nequality, hashing, `str()`, and `os.fspath()`.\n\nIts mechanical accessors are `name`, `stem`, `suffix`, `suffixes`, `parent`,\n`parts`, `as_posix()`, and `as_uri()`. `parent` intentionally returns a plain\n`Path`.\n\nDirect construction validates only that `value` is absolute. `ResolvedPath`\nmeans an absolute path value; it does not imply that the path exists, is safe,\nis contained beneath a trusted root, or is authorized for access.\n",
        "resource": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "start": 1134,
        "start_line": 35
      }
    ]
  },
  {
    "address": "src/devtools/core/paths/models.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "b2dd2079ca43e7c470834f3bd1f6362e4d2b9f119dd7b304f7759be65cd6567b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
      "packet_ordinal": 202
    },
    "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
    "semantic_rationale": "Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/core/paths/models.py",
        "end": 963,
        "end_line": 38,
        "quote": "@dataclass(frozen=True, slots=True)\nclass ResolvedPath(os.PathLike[str]):\n    \"\"\"Represent an immutable absolute filesystem path.\n\n    The model validates only that its value is absolute. Filesystem\n    normalization and resolution are performed by the path-resolution\n    operations.\n\n    :ivar value: Absolute filesystem path.\n    \"\"\"\n\n    value: Path\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate model invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the resolved path value.\n\n        :raises ValueError: If the path is not absolute.\n        \"\"\"\n        if not self.value.is_absolute():\n            msg = \"ResolvedPath requires an absolute path.\"\n            raise ValueError(msg)\n",
        "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
        "start": 221,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/core/paths/models.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "b2dd2079ca43e7c470834f3bd1f6362e4d2b9f119dd7b304f7759be65cd6567b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
      "packet_ordinal": 202
    },
    "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
    "semantic_rationale": "Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/core/paths/models.py",
        "end": 963,
        "end_line": 38,
        "quote": "@dataclass(frozen=True, slots=True)\nclass ResolvedPath(os.PathLike[str]):\n    \"\"\"Represent an immutable absolute filesystem path.\n\n    The model validates only that its value is absolute. Filesystem\n    normalization and resolution are performed by the path-resolution\n    operations.\n\n    :ivar value: Absolute filesystem path.\n    \"\"\"\n\n    value: Path\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate model invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the resolved path value.\n\n        :raises ValueError: If the path is not absolute.\n        \"\"\"\n        if not self.value.is_absolute():\n            msg = \"ResolvedPath requires an absolute path.\"\n            raise ValueError(msg)\n",
        "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
        "start": 221,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/core/paths/models.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "b2dd2079ca43e7c470834f3bd1f6362e4d2b9f119dd7b304f7759be65cd6567b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
      "packet_ordinal": 202
    },
    "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
    "semantic_rationale": "Shows ResolvedPath construction and absolute-value validation, useful for fixtures without requiring path implementation changes.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/core/paths/models.py",
        "end": 963,
        "end_line": 38,
        "quote": "@dataclass(frozen=True, slots=True)\nclass ResolvedPath(os.PathLike[str]):\n    \"\"\"Represent an immutable absolute filesystem path.\n\n    The model validates only that its value is absolute. Filesystem\n    normalization and resolution are performed by the path-resolution\n    operations.\n\n    :ivar value: Absolute filesystem path.\n    \"\"\"\n\n    value: Path\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate model invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the resolved path value.\n\n        :raises ValueError: If the path is not absolute.\n        \"\"\"\n        if not self.value.is_absolute():\n            msg = \"ResolvedPath requires an absolute path.\"\n            raise ValueError(msg)\n",
        "resource": "ce645a9d233fc34655d04ace039a4f75c757001e169c3bb98d9c41b4914479b4",
        "start": 221,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/models/benchmarks/storage.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "packet_ordinal": 236
    },
    "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
    "semantic_rationale": "Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/models/benchmarks/storage.py",
        "end": 1713,
        "end_line": 53,
        "quote": "def load_benchmark_result(path: ResolvedPath) -> ModelBenchmarkResult:\n    \"\"\"Load a supported benchmark artifact into its immutable result value.\"\"\"\n    try:\n        source = cast(\"TextFile\", read(path, file_format=FileFormat.TEXT))\n        raw = json.loads(source.content)\n        return _from_json(cast(\"object\", raw))\n    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:\n        msg = f\"Invalid model benchmark artifact: {path}.\"\n        raise ValueError(msg) from error\n",
        "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "start": 1214,
        "start_line": 45
      }
    ]
  },
  {
    "address": "src/devtools/models/benchmarks/storage.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "packet_ordinal": 236
    },
    "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
    "semantic_rationale": "Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/models/benchmarks/storage.py",
        "end": 1713,
        "end_line": 53,
        "quote": "def load_benchmark_result(path: ResolvedPath) -> ModelBenchmarkResult:\n    \"\"\"Load a supported benchmark artifact into its immutable result value.\"\"\"\n    try:\n        source = cast(\"TextFile\", read(path, file_format=FileFormat.TEXT))\n        raw = json.loads(source.content)\n        return _from_json(cast(\"object\", raw))\n    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:\n        msg = f\"Invalid model benchmark artifact: {path}.\"\n        raise ValueError(msg) from error\n",
        "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "start": 1214,
        "start_line": 45
      }
    ]
  },
  {
    "address": "src/devtools/models/benchmarks/storage.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "packet_ordinal": 236
    },
    "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
    "semantic_rationale": "Shows a default-limit caller with an explicit text override; the unchanged public contract already covers this caller.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/models/benchmarks/storage.py",
        "end": 1713,
        "end_line": 53,
        "quote": "def load_benchmark_result(path: ResolvedPath) -> ModelBenchmarkResult:\n    \"\"\"Load a supported benchmark artifact into its immutable result value.\"\"\"\n    try:\n        source = cast(\"TextFile\", read(path, file_format=FileFormat.TEXT))\n        raw = json.loads(source.content)\n        return _from_json(cast(\"object\", raw))\n    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as error:\n        msg = f\"Invalid model benchmark artifact: {path}.\"\n        raise ValueError(msg) from error\n",
        "resource": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "start": 1214,
        "start_line": 45
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/__init__.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "packet_ordinal": 288
    },
    "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
    "semantic_rationale": "Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/__init__.py",
        "end": 982,
        "end_line": 41,
        "quote": "from devtools.resources.filesystem.codecs import (\n    CsvCodec,\n    JsonCodec,\n    MarkdownCodec,\n    TextCodec,\n)\nfrom devtools.resources.filesystem.errors import (\n    FileFormatError,\n    FilesystemError,\n    FilesystemNotFoundError,\n    FilesystemPermissionError,\n    FileTooLargeError,\n    NotAFileError,\n    TextDecodingError,\n    TextEncodingError,\n)\nfrom devtools.resources.filesystem.models import (\n    BinaryFile,\n    CsvDialect,\n    CsvFile,\n    CsvQuoting,\n    CsvRow,\n    File,\n    FileFormat,\n    JsonFile,\n    JsonListFile,\n    JsonObjectFile,\n    JsonScalar,\n    JsonScalarFile,\n    JsonValue,\n    MarkdownFile,\n    MarkdownHeading,\n    MarkdownSection,\n    TextFile,\n)\nfrom devtools.resources.filesystem.reading import DEFAULT_MAX_READ_BYTES, read\nfrom devtools.resources.filesystem.resolution import resolve_file_format\nfrom devtools.resources.filesystem.writing import write\n",
        "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "start": 86,
        "start_line": 4
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/__init__.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "packet_ordinal": 288
    },
    "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
    "semantic_rationale": "Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/__init__.py",
        "end": 982,
        "end_line": 41,
        "quote": "from devtools.resources.filesystem.codecs import (\n    CsvCodec,\n    JsonCodec,\n    MarkdownCodec,\n    TextCodec,\n)\nfrom devtools.resources.filesystem.errors import (\n    FileFormatError,\n    FilesystemError,\n    FilesystemNotFoundError,\n    FilesystemPermissionError,\n    FileTooLargeError,\n    NotAFileError,\n    TextDecodingError,\n    TextEncodingError,\n)\nfrom devtools.resources.filesystem.models import (\n    BinaryFile,\n    CsvDialect,\n    CsvFile,\n    CsvQuoting,\n    CsvRow,\n    File,\n    FileFormat,\n    JsonFile,\n    JsonListFile,\n    JsonObjectFile,\n    JsonScalar,\n    JsonScalarFile,\n    JsonValue,\n    MarkdownFile,\n    MarkdownHeading,\n    MarkdownSection,\n    TextFile,\n)\nfrom devtools.resources.filesystem.reading import DEFAULT_MAX_READ_BYTES, read\nfrom devtools.resources.filesystem.resolution import resolve_file_format\nfrom devtools.resources.filesystem.writing import write\n",
        "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "start": 86,
        "start_line": 4
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/__init__.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "packet_ordinal": 288
    },
    "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
    "semantic_rationale": "Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/__init__.py",
        "end": 982,
        "end_line": 41,
        "quote": "from devtools.resources.filesystem.codecs import (\n    CsvCodec,\n    JsonCodec,\n    MarkdownCodec,\n    TextCodec,\n)\nfrom devtools.resources.filesystem.errors import (\n    FileFormatError,\n    FilesystemError,\n    FilesystemNotFoundError,\n    FilesystemPermissionError,\n    FileTooLargeError,\n    NotAFileError,\n    TextDecodingError,\n    TextEncodingError,\n)\nfrom devtools.resources.filesystem.models import (\n    BinaryFile,\n    CsvDialect,\n    CsvFile,\n    CsvQuoting,\n    CsvRow,\n    File,\n    FileFormat,\n    JsonFile,\n    JsonListFile,\n    JsonObjectFile,\n    JsonScalar,\n    JsonScalarFile,\n    JsonValue,\n    MarkdownFile,\n    MarkdownHeading,\n    MarkdownSection,\n    TextFile,\n)\nfrom devtools.resources.filesystem.reading import DEFAULT_MAX_READ_BYTES, read\nfrom devtools.resources.filesystem.resolution import resolve_file_format\nfrom devtools.resources.filesystem.writing import write\n",
        "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "start": 86,
        "start_line": 4
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/__init__.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "packet_ordinal": 288
    },
    "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
    "semantic_rationale": "Confirms facade exports and module ownership; retaining existing names and imports does not require changing this facade.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/__init__.py",
        "end": 982,
        "end_line": 41,
        "quote": "from devtools.resources.filesystem.codecs import (\n    CsvCodec,\n    JsonCodec,\n    MarkdownCodec,\n    TextCodec,\n)\nfrom devtools.resources.filesystem.errors import (\n    FileFormatError,\n    FilesystemError,\n    FilesystemNotFoundError,\n    FilesystemPermissionError,\n    FileTooLargeError,\n    NotAFileError,\n    TextDecodingError,\n    TextEncodingError,\n)\nfrom devtools.resources.filesystem.models import (\n    BinaryFile,\n    CsvDialect,\n    CsvFile,\n    CsvQuoting,\n    CsvRow,\n    File,\n    FileFormat,\n    JsonFile,\n    JsonListFile,\n    JsonObjectFile,\n    JsonScalar,\n    JsonScalarFile,\n    JsonValue,\n    MarkdownFile,\n    MarkdownHeading,\n    MarkdownSection,\n    TextFile,\n)\nfrom devtools.resources.filesystem.reading import DEFAULT_MAX_READ_BYTES, read\nfrom devtools.resources.filesystem.resolution import resolve_file_format\nfrom devtools.resources.filesystem.writing import write\n",
        "resource": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "start": 86,
        "start_line": 4
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "d9ddfd29e02486d5f88d36ee9f7e88f466eaa068fc22b2513afb907018717a90",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
      "packet_ordinal": 290
    },
    "resource": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/csv.py",
        "end": 3373,
        "end_line": 109,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n        dialect: CsvDialect = _DEFAULT_DIALECT,\n    ) -> CsvFile:\n        \"\"\"Decode and parse CSV bytes without accessing the filesystem.\"\"\"\n        try:\n            source = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode CSV file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return self.parse(\n            path,\n            source,\n            encoding=encoding,\n            byte_size=len(content),\n            dialect=dialect,\n        )\n\n    def parse(\n        self,\n        path: ResolvedPath,\n        content: str,\n        *,\n        encoding: str = \"utf-8\",\n        byte_size: int | None = None,\n        dialect: CsvDialect = _DEFAULT_DIALECT,\n    ) -> CsvFile:\n        \"\"\"Parse header-based CSV source into an immutable file model.\"\"\"\n        source_size = byte_size\n\n        if source_size is None:\n            try:\n                source_size = len(content.encode(encoding))\n            except (LookupError, UnicodeEncodeError) as error:\n                msg = f\"Unable to encode CSV source using {encoding!r}.\"\n                raise TextEncodingError(msg) from error\n\n        try:\n            reader = csv.reader(\n                StringIO(content, newline=\"\"),\n                delimiter=dialect.delimiter,\n                quotechar=dialect.quotechar,\n                escapechar=dialect.escapechar,\n                doublequote=dialect.doublequote,\n                skipinitialspace=dialect.skipinitialspace,\n                lineterminator=dialect.lineterminator,\n                quoting=_to_csv_quoting(dialect.quoting),\n                strict=True,\n            )\n            headers = tuple(next(reader))\n        except StopIteration as error:\n            msg = \"CSV files require a header row.\"\n            raise FileFormatError(msg) from error\n        except (csv.Error, ValueError) as error:\n            msg = f\"Invalid CSV source: {error}.\"\n            raise FileFormatError(msg) from error\n\n        _validate_headers(headers)\n        rows: list[CsvRow] = []\n\n        try:\n            rows.extend(CsvRow(headers, tuple(values)) for values in reader)\n        except (csv.Error, ValueError) as error:\n            msg = f\"Invalid CSV row: {error}.\"\n            raise FileFormatError(msg) from error\n\n        return CsvFile(\n            path,\n            content,\n            encoding=encoding,\n            byte_size=source_size,\n            headers=headers,\n            rows=tuple(rows),\n            dialect=dialect,\n        )\n",
        "resource": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
        "start": 693,
        "start_line": 30
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "d9ddfd29e02486d5f88d36ee9f7e88f466eaa068fc22b2513afb907018717a90",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
      "packet_ordinal": 290
    },
    "resource": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/csv.py",
        "end": 3373,
        "end_line": 109,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n        dialect: CsvDialect = _DEFAULT_DIALECT,\n    ) -> CsvFile:\n        \"\"\"Decode and parse CSV bytes without accessing the filesystem.\"\"\"\n        try:\n            source = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode CSV file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return self.parse(\n            path,\n            source,\n            encoding=encoding,\n            byte_size=len(content),\n            dialect=dialect,\n        )\n\n    def parse(\n        self,\n        path: ResolvedPath,\n        content: str,\n        *,\n        encoding: str = \"utf-8\",\n        byte_size: int | None = None,\n        dialect: CsvDialect = _DEFAULT_DIALECT,\n    ) -> CsvFile:\n        \"\"\"Parse header-based CSV source into an immutable file model.\"\"\"\n        source_size = byte_size\n\n        if source_size is None:\n            try:\n                source_size = len(content.encode(encoding))\n            except (LookupError, UnicodeEncodeError) as error:\n                msg = f\"Unable to encode CSV source using {encoding!r}.\"\n                raise TextEncodingError(msg) from error\n\n        try:\n            reader = csv.reader(\n                StringIO(content, newline=\"\"),\n                delimiter=dialect.delimiter,\n                quotechar=dialect.quotechar,\n                escapechar=dialect.escapechar,\n                doublequote=dialect.doublequote,\n                skipinitialspace=dialect.skipinitialspace,\n                lineterminator=dialect.lineterminator,\n                quoting=_to_csv_quoting(dialect.quoting),\n                strict=True,\n            )\n            headers = tuple(next(reader))\n        except StopIteration as error:\n            msg = \"CSV files require a header row.\"\n            raise FileFormatError(msg) from error\n        except (csv.Error, ValueError) as error:\n            msg = f\"Invalid CSV source: {error}.\"\n            raise FileFormatError(msg) from error\n\n        _validate_headers(headers)\n        rows: list[CsvRow] = []\n\n        try:\n            rows.extend(CsvRow(headers, tuple(values)) for values in reader)\n        except (csv.Error, ValueError) as error:\n            msg = f\"Invalid CSV row: {error}.\"\n            raise FileFormatError(msg) from error\n\n        return CsvFile(\n            path,\n            content,\n            encoding=encoding,\n            byte_size=source_size,\n            headers=headers,\n            rows=tuple(rows),\n            dialect=dialect,\n        )\n",
        "resource": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
        "start": 693,
        "start_line": 30
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/json.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "packet_ordinal": 291
    },
    "resource": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "end": 3905,
        "end_line": 125,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> JsonFile:\n        \"\"\"Decode and parse JSON bytes without accessing the filesystem.\n\n        :param path: Source path represented by the resulting model.\n        :param content: Raw JSON bytes.\n        :param encoding: Encoding used for byte decoding.\n        :returns: Concrete immutable JSON file model.\n        :raises TextDecodingError: If the bytes cannot be decoded.\n        \"\"\"\n        try:\n            source = content.decode(encoding)\n        except (UnicodeDecodeError, LookupError) as error:\n            msg = f\"Unable to decode {path} using encoding {encoding!r}.\"\n            raise TextDecodingError(msg) from error\n\n        return self.parse(\n            path,\n            source,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n\n    def parse(\n        self,\n        path: ResolvedPath,\n        content: str,\n        *,\n        encoding: str = \"utf-8\",\n        byte_size: int | None = None,\n    ) -> JsonFile:\n        \"\"\"Parse JSON source text into a concrete immutable model.\n\n        :param path: Source path represented by the resulting model.\n        :param content: Decoded JSON source text.\n        :param encoding: Encoding metadata for the source text.\n        :param byte_size: Source byte size, derived from the encoding when omitted.\n        :returns: Concrete immutable JSON file model.\n        :raises FileFormatError: If the source is not valid strict JSON.\n        :raises TextEncodingError: If byte-size derivation cannot encode content.\n        \"\"\"\n        source_size = byte_size\n\n        if source_size is None:\n            try:\n                source_size = len(content.encode(encoding))\n            except (UnicodeEncodeError, LookupError) as error:\n                msg = f\"Unable to encode JSON source using {encoding!r}.\"\n                raise TextEncodingError(msg) from error\n\n        try:\n            parsed = json.loads(\n                content,\n                parse_constant=_reject_nonstandard_constant,\n            )\n        except (json.JSONDecodeError, ValueError) as error:\n            msg = _format_parse_error(error)\n            raise FileFormatError(msg) from error\n\n        value = freeze_json(parsed)\n\n        if isinstance(value, Mapping):\n            return JsonObjectFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        if isinstance(value, tuple):\n            return JsonListFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        if isinstance(value, str | int | float | bool) or value is None:\n            return JsonScalarFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        msg = f\"Unsupported frozen JSON root type: {type(value).__name__}.\"\n        raise FileFormatError(msg)\n",
        "resource": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "start": 729,
        "start_line": 31
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/json.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "packet_ordinal": 291
    },
    "resource": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "end": 3905,
        "end_line": 125,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> JsonFile:\n        \"\"\"Decode and parse JSON bytes without accessing the filesystem.\n\n        :param path: Source path represented by the resulting model.\n        :param content: Raw JSON bytes.\n        :param encoding: Encoding used for byte decoding.\n        :returns: Concrete immutable JSON file model.\n        :raises TextDecodingError: If the bytes cannot be decoded.\n        \"\"\"\n        try:\n            source = content.decode(encoding)\n        except (UnicodeDecodeError, LookupError) as error:\n            msg = f\"Unable to decode {path} using encoding {encoding!r}.\"\n            raise TextDecodingError(msg) from error\n\n        return self.parse(\n            path,\n            source,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n\n    def parse(\n        self,\n        path: ResolvedPath,\n        content: str,\n        *,\n        encoding: str = \"utf-8\",\n        byte_size: int | None = None,\n    ) -> JsonFile:\n        \"\"\"Parse JSON source text into a concrete immutable model.\n\n        :param path: Source path represented by the resulting model.\n        :param content: Decoded JSON source text.\n        :param encoding: Encoding metadata for the source text.\n        :param byte_size: Source byte size, derived from the encoding when omitted.\n        :returns: Concrete immutable JSON file model.\n        :raises FileFormatError: If the source is not valid strict JSON.\n        :raises TextEncodingError: If byte-size derivation cannot encode content.\n        \"\"\"\n        source_size = byte_size\n\n        if source_size is None:\n            try:\n                source_size = len(content.encode(encoding))\n            except (UnicodeEncodeError, LookupError) as error:\n                msg = f\"Unable to encode JSON source using {encoding!r}.\"\n                raise TextEncodingError(msg) from error\n\n        try:\n            parsed = json.loads(\n                content,\n                parse_constant=_reject_nonstandard_constant,\n            )\n        except (json.JSONDecodeError, ValueError) as error:\n            msg = _format_parse_error(error)\n            raise FileFormatError(msg) from error\n\n        value = freeze_json(parsed)\n\n        if isinstance(value, Mapping):\n            return JsonObjectFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        if isinstance(value, tuple):\n            return JsonListFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        if isinstance(value, str | int | float | bool) or value is None:\n            return JsonScalarFile(\n                path,\n                content,\n                encoding=encoding,\n                byte_size=source_size,\n                value=value,\n            )\n\n        msg = f\"Unsupported frozen JSON root type: {type(value).__name__}.\"\n        raise FileFormatError(msg)\n",
        "resource": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "start": 729,
        "start_line": 31
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/markdown.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "packet_ordinal": 292
    },
    "resource": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "end": 1386,
        "end_line": 47,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> MarkdownFile:\n        \"\"\"Decode raw Markdown bytes into a rich Markdown file model.\n\n        :param path: Resolved path associated with the Markdown source.\n        :param content: Raw Markdown bytes.\n        :param encoding: Encoding used to decode the source bytes.\n        :returns: Immutable Markdown file model.\n        :raises TextDecodingError: If decoding fails or the encoding is unknown.\n        \"\"\"\n        try:\n            text = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode Markdown file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return MarkdownFile(\n            path=path,\n            content=text,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n",
        "resource": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "start": 437,
        "start_line": 21
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/markdown.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "packet_ordinal": 292
    },
    "resource": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "end": 1386,
        "end_line": 47,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> MarkdownFile:\n        \"\"\"Decode raw Markdown bytes into a rich Markdown file model.\n\n        :param path: Resolved path associated with the Markdown source.\n        :param content: Raw Markdown bytes.\n        :param encoding: Encoding used to decode the source bytes.\n        :returns: Immutable Markdown file model.\n        :raises TextDecodingError: If decoding fails or the encoding is unknown.\n        \"\"\"\n        try:\n            text = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode Markdown file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return MarkdownFile(\n            path=path,\n            content=text,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n",
        "resource": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "start": 437,
        "start_line": 21
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "packet_ordinal": 293
    },
    "resource": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "end": 1343,
        "end_line": 47,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> TextFile:\n        \"\"\"Decode raw bytes into a text file model.\n\n        :param path: Resolved path associated with the text content.\n        :param content: Raw source bytes.\n        :param encoding: Encoding used to decode the source bytes.\n        :returns: Immutable text file model.\n        :raises TextDecodingError: If decoding fails or the encoding is unknown.\n        \"\"\"\n        try:\n            text = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode text file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return TextFile(\n            path=path,\n            content=text,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n",
        "resource": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "start": 433,
        "start_line": 21
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/codecs/text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "packet_ordinal": 293
    },
    "resource": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
    "semantic_rationale": "Directly corroborates codec decoding, metadata and concrete result construction and supplies useful regression examples. Preserving the existing decode call with identical complete bytes avoids any independent codec implementation obligation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "end": 1343,
        "end_line": 47,
        "quote": "    def decode(\n        self,\n        path: ResolvedPath,\n        content: bytes,\n        *,\n        encoding: str = \"utf-8\",\n    ) -> TextFile:\n        \"\"\"Decode raw bytes into a text file model.\n\n        :param path: Resolved path associated with the text content.\n        :param content: Raw source bytes.\n        :param encoding: Encoding used to decode the source bytes.\n        :returns: Immutable text file model.\n        :raises TextDecodingError: If decoding fails or the encoding is unknown.\n        \"\"\"\n        try:\n            text = content.decode(encoding)\n        except (LookupError, UnicodeDecodeError) as error:\n            msg = f\"Unable to decode text file using {encoding!r}: {path}.\"\n            raise TextDecodingError(msg) from error\n\n        return TextFile(\n            path=path,\n            content=text,\n            encoding=encoding,\n            byte_size=len(content),\n        )\n",
        "resource": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "start": 433,
        "start_line": 21
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/codecs.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "packet_ordinal": 294
    },
    "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
    "semantic_rationale": "Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "end": 1246,
        "end_line": 29,
        "quote": "Codecs convert representations and models; they do not access disk. Generic\ndisk I/O is owned by [`read()` and `write()`](io.md).\n\n## Current codecs\n\n`TextCodec`, `JsonCodec`, `MarkdownCodec`, and `CsvCodec` support bytes/text\nconversion for their corresponding models. There is no BinaryCodec.\n\n- TextCodec performs `bytes <-> decoded text` without structural parsing.\n- JsonCodec provides `decode`, `parse`, `serialize`, and `encode`.\n- MarkdownCodec encodes and decodes authoritative Markdown `.content`.\n- CsvCodec provides `decode`, `parse`, `serialize`, and `encode` for headers,\n  rows, and dialects.\n\nDecode failures and unknown encodings normalize to `TextDecodingError`; output\nencoding failures normalize to `TextEncodingError`. Format parsing and\nserialization failures use `FileFormatError` where appropriate.\n\n## Architecture\n\nCodec resolution is a static internal format-to-codec-class map. No common\ncodec base class or Protocol exists because the four concrete codecs remain\nsmall and their signatures differ meaningfully. There is no registry or plugin\ndiscovery.\n\nJSON and CSV serialization uses current structured state, not source\nprovenance. Markdown and text encoding preserve their `.content` source.\n",
        "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "start": 21,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/codecs.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "packet_ordinal": 294
    },
    "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
    "semantic_rationale": "Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "end": 1246,
        "end_line": 29,
        "quote": "Codecs convert representations and models; they do not access disk. Generic\ndisk I/O is owned by [`read()` and `write()`](io.md).\n\n## Current codecs\n\n`TextCodec`, `JsonCodec`, `MarkdownCodec`, and `CsvCodec` support bytes/text\nconversion for their corresponding models. There is no BinaryCodec.\n\n- TextCodec performs `bytes <-> decoded text` without structural parsing.\n- JsonCodec provides `decode`, `parse`, `serialize`, and `encode`.\n- MarkdownCodec encodes and decodes authoritative Markdown `.content`.\n- CsvCodec provides `decode`, `parse`, `serialize`, and `encode` for headers,\n  rows, and dialects.\n\nDecode failures and unknown encodings normalize to `TextDecodingError`; output\nencoding failures normalize to `TextEncodingError`. Format parsing and\nserialization failures use `FileFormatError` where appropriate.\n\n## Architecture\n\nCodec resolution is a static internal format-to-codec-class map. No common\ncodec base class or Protocol exists because the four concrete codecs remain\nsmall and their signatures differ meaningfully. There is no registry or plugin\ndiscovery.\n\nJSON and CSV serialization uses current structured state, not source\nprovenance. Markdown and text encoding preserve their `.content` source.\n",
        "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "start": 21,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/codecs.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "packet_ordinal": 294
    },
    "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
    "semantic_rationale": "Documents codec ownership and error families; useful corroboration of the unchanged codec delegation boundary.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "end": 1246,
        "end_line": 29,
        "quote": "Codecs convert representations and models; they do not access disk. Generic\ndisk I/O is owned by [`read()` and `write()`](io.md).\n\n## Current codecs\n\n`TextCodec`, `JsonCodec`, `MarkdownCodec`, and `CsvCodec` support bytes/text\nconversion for their corresponding models. There is no BinaryCodec.\n\n- TextCodec performs `bytes <-> decoded text` without structural parsing.\n- JsonCodec provides `decode`, `parse`, `serialize`, and `encode`.\n- MarkdownCodec encodes and decodes authoritative Markdown `.content`.\n- CsvCodec provides `decode`, `parse`, `serialize`, and `encode` for headers,\n  rows, and dialects.\n\nDecode failures and unknown encodings normalize to `TextDecodingError`; output\nencoding failures normalize to `TextEncodingError`. Format parsing and\nserialization failures use `FileFormatError` where appropriate.\n\n## Architecture\n\nCodec resolution is a static internal format-to-codec-class map. No common\ncodec base class or Protocol exists because the four concrete codecs remain\nsmall and their signatures differ meaningfully. There is no registry or plugin\ndiscovery.\n\nJSON and CSV serialization uses current structured state, not source\nprovenance. Markdown and text encoding preserve their `.content` source.\n",
        "resource": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "start": 21,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/csv.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
      "packet_ordinal": 295
    },
    "resource": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
    "semantic_rationale": "Establishes empty CSV remains a format failure and source text remains provenance; useful for choosing format-appropriate empty-input tests.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/csv.md",
        "end": 2119,
        "end_line": 47,
        "quote": "## Parsing and provenance\n\nAn empty source is invalid. A nonempty unique, nonblank header is required;\nheader-only CSV is valid. Empty cells are valid strings, but blank records and\nmalformed row widths are invalid. No numeric or date coercion occurs.\n\n`.content` is original decoded source provenance. `.headers` and `.rows` are\ncurrent state. Transformations preserve `.content`; CsvCodec serializes current\nheaders and rows.\n\n## Codec\n\n`CsvCodec` uses standard-library `csv.reader` and `csv.writer` with\n`StringIO(newline=\"\")`, applies the file dialect, supports quoted delimiters and\nembedded newlines, and performs encoding normalization. It does not read or\nwrite disk directly and does not provide typed cell conversion.\n",
        "resource": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
        "start": 1391,
        "start_line": 32
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/csv.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
      "packet_ordinal": 295
    },
    "resource": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
    "semantic_rationale": "Establishes empty CSV remains a format failure and source text remains provenance; useful for choosing format-appropriate empty-input tests.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/csv.md",
        "end": 2119,
        "end_line": 47,
        "quote": "## Parsing and provenance\n\nAn empty source is invalid. A nonempty unique, nonblank header is required;\nheader-only CSV is valid. Empty cells are valid strings, but blank records and\nmalformed row widths are invalid. No numeric or date coercion occurs.\n\n`.content` is original decoded source provenance. `.headers` and `.rows` are\ncurrent state. Transformations preserve `.content`; CsvCodec serializes current\nheaders and rows.\n\n## Codec\n\n`CsvCodec` uses standard-library `csv.reader` and `csv.writer` with\n`StringIO(newline=\"\")`, applies the file dialect, supports quoted delimiters and\nembedded newlines, and performs encoding normalization. It does not read or\nwrite disk directly and does not provide typed cell conversion.\n",
        "resource": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
        "start": 1391,
        "start_line": 32
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/io.md",
    "inferability_rationale": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
    "label": "REQUIRED",
    "obligation": "O1",
    "provenance": {
      "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "packet_ordinal": 296
    },
    "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R01: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.; R16: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 913,
        "end_line": 30,
        "quote": "```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 424,
        "start_line": 20
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 1171,
        "end_line": 38,
        "quote": "`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 499,
        "start_line": 24
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/io.md",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O3",
    "provenance": {
      "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "packet_ordinal": 296
    },
    "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "INFERABLE_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 411,
        "end_line": 16,
        "quote": "## Format resolution\n\n`resolve_file_format(path)` resolves the final suffix case-insensitively:\n\n| Suffix | Format |\n|---|---|\n| `.csv` | CSV |\n| `.json` | JSON |\n| `.md`, `.markdown` | Markdown |\n| `.txt` | Text |\n\nUnsupported or unimplemented formats raise `FileFormatError`. An explicit\n`file_format` passed to `read()` bypasses suffix inference. Binary has no\ncodec-backed suffix support.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 18,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/io.md",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "packet_ordinal": 296
    },
    "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "INFERABLE_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 411,
        "end_line": 16,
        "quote": "## Format resolution\n\n`resolve_file_format(path)` resolves the final suffix case-insensitively:\n\n| Suffix | Format |\n|---|---|\n| `.csv` | CSV |\n| `.json` | JSON |\n| `.md`, `.markdown` | Markdown |\n| `.txt` | Text |\n\nUnsupported or unimplemented formats raise `FileFormatError`. An explicit\n`file_format` passed to `read()` bypasses suffix inference. Binary has no\ncodec-backed suffix support.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 18,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/io.md",
    "inferability_rationale": "The task provides the replacement guarantee. Current document text is necessary only to know which claims and surrounding boundaries must be reconciled.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "packet_ordinal": 296
    },
    "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R08: Accurate documentation requires reconciling these specific existing behavior claims, not adding a new guarantee beside contradictory text.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 1171,
        "end_line": 38,
        "quote": "## Reading\n\n```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 412,
        "start_line": 18
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 2499,
        "end_line": 80,
        "quote": "## Writing\n\n```python\nwrite(file, *, overwrite=True)\n```\n\nThe model's `format`, not the target suffix, selects its codec. Explicit model\nand codec matching prevents JSON, Markdown, and CSV TextFile subclasses from\nbeing encoded by TextCodec. Missing parent directories are not created.\n`overwrite=False` raises built-in `FileExistsError` when the destination exists.\n\nThe normal write lifecycle is:\n\n```text\nencode current model state\n    \u2193\ncreate sibling temporary file\n    \u2193\nrecord its path for cleanup\n    \u2193\nwrite, flush, fsync\n    \u2193\nos.replace(destination)\n    \u2193\nremove temporary file on failure\n```\n\nUnder normal local atomic-replace filesystem semantics, observers should see\neither the previous destination or the complete replacement, rather than a\npartially written destination. The temporary file is in the target directory,\nso replacement stays on that filesystem.\n\nThis is not a full crash transaction: the parent directory is not fsynced,\ndirectory-entry durability after sudden power loss is filesystem-dependent, and\nthere is no locking or concurrent-writer coordination.\n\n## Security boundaries\n\nI/O does not guarantee allowed-root containment, symlink-escape prevention,\npath authorization, TOCTOU elimination, ownership/permission policy, locking,\nor secure deletion. Those concerns are outside this package.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 1172,
        "start_line": 40
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/json.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "packet_ordinal": 297
    },
    "resource": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
    "semantic_rationale": "Documents JSON source/value separation and strict format errors; useful regression guidance without rewriting the parser.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "end": 2354,
        "end_line": 59,
        "quote": "`.content` is original decoded JSON source provenance. `.value` is current\nstructured state. Immutable transformations retain `.content`; serialization\nuses `.value`. Object conversion receives a thawed ordinary dict, scalar\nconversion receives the scalar, and list conversion thaws each item.\n\n## `JsonCodec`\n\n`decode()` converts bytes to source text; `parse()` selects object, list, or\nscalar models; `serialize()` renders current `.value`; `encode()` produces\nbytes. The codec never reads or writes disk.\n\nParsing is strict: nonstandard constants such as `NaN` are rejected. Invalid\nsource becomes `FileFormatError`, with line/column information for ordinary\nJSON decode failures. Serialization defaults to indent `2`, `ensure_ascii=False`,\nunsorted keys, and a trailing newline; indentation, ASCII escaping, key sorting,\nand final newline are configurable. JSON5/comments and source-format-preserving\nwrites are unsupported.\n",
        "resource": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "start": 1425,
        "start_line": 43
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/json.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "packet_ordinal": 297
    },
    "resource": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
    "semantic_rationale": "Documents JSON source/value separation and strict format errors; useful regression guidance without rewriting the parser.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "end": 2354,
        "end_line": 59,
        "quote": "`.content` is original decoded JSON source provenance. `.value` is current\nstructured state. Immutable transformations retain `.content`; serialization\nuses `.value`. Object conversion receives a thawed ordinary dict, scalar\nconversion receives the scalar, and list conversion thaws each item.\n\n## `JsonCodec`\n\n`decode()` converts bytes to source text; `parse()` selects object, list, or\nscalar models; `serialize()` renders current `.value`; `encode()` produces\nbytes. The codec never reads or writes disk.\n\nParsing is strict: nonstandard constants such as `NaN` are rejected. Invalid\nsource becomes `FileFormatError`, with line/column information for ordinary\nJSON decode failures. Serialization defaults to indent `2`, `ensure_ascii=False`,\nunsorted keys, and a trailing newline; indentation, ASCII escaping, key sorting,\nand final newline are configurable. JSON5/comments and source-format-preserving\nwrites are unsupported.\n",
        "resource": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "start": 1425,
        "start_line": 43
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/markdown.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
      "packet_ordinal": 298
    },
    "resource": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
    "semantic_rationale": "Distinguishes exact Markdown file content from normalized derived section content, avoiding an overbroad line-ending assertion.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "end": 1788,
        "end_line": 38,
        "quote": "## Sections and lookup\n\nA section starts at its owning heading and ends immediately before the next\nheading of the same or higher level. Lower-level headings remain in the parent\nsection. Boundaries use one-based inclusive lines.\n\n`MarkdownSection.content` excludes the heading line and is normalized logical\nsource: `splitlines()` plus `\"\\n\"` joining means CRLF becomes logical newline\ntext and final-newline/exact source-slice fidelity is not retained.\n`find_heading()` and `find_section()` return the first matching structure and\nare case-insensitive by default.\n\n## Codec and inherited text behavior\n\n`MarkdownCodec` only decodes and encodes `.content`. Headings and sections are\nalways derived and are never serialized independently. Markdown inherits\nliteral contains, logical lines, and source regex operations from TextFile.\nThere is no structural Markdown rewriting, Setext support, or full CommonMark\nparsing.\n",
        "resource": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "start": 868,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/markdown.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
      "packet_ordinal": 298
    },
    "resource": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
    "semantic_rationale": "Distinguishes exact Markdown file content from normalized derived section content, avoiding an overbroad line-ending assertion.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "end": 1788,
        "end_line": 38,
        "quote": "## Sections and lookup\n\nA section starts at its owning heading and ends immediately before the next\nheading of the same or higher level. Lower-level headings remain in the parent\nsection. Boundaries use one-based inclusive lines.\n\n`MarkdownSection.content` excludes the heading line and is normalized logical\nsource: `splitlines()` plus `\"\\n\"` joining means CRLF becomes logical newline\ntext and final-newline/exact source-slice fidelity is not retained.\n`find_heading()` and `find_section()` return the first matching structure and\nare case-insensitive by default.\n\n## Codec and inherited text behavior\n\n`MarkdownCodec` only decodes and encodes `.content`. Headings and sections are\nalways derived and are never serialized independently. Markdown inherits\nliteral contains, logical lines, and source regex operations from TextFile.\nThere is no structural Markdown rewriting, Setext support, or full CommonMark\nparsing.\n",
        "resource": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "start": 868,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/models.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "packet_ordinal": 299
    },
    "resource": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
    "semantic_rationale": "Provides shared model hierarchy and source metadata semantics, corroborating unchanged codec results.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "end": 1820,
        "end_line": 51,
        "quote": "## Hierarchy\n\n```text\nFile\n\u251c\u2500\u2500 BinaryFile\n\u2514\u2500\u2500 TextFile\n    \u251c\u2500\u2500 JsonFile\n    \u2502   \u251c\u2500\u2500 JsonObjectFile\n    \u2502   \u251c\u2500\u2500 JsonListFile\n    \u2502   \u2514\u2500\u2500 JsonScalarFile\n    \u251c\u2500\u2500 MarkdownFile\n    \u2514\u2500\u2500 CsvFile\n```\n\nInheritance expresses shared source representation, not interchangeable\nserialization semantics. Structured models retain their own operations and\ntheir codecs are selected explicitly by format.\n\n## `File`\n\n`File` is the minimal frozen, slotted base. It associates a `ResolvedPath`\nwith an abstract `FileFormat`. It does not promise text, structured values,\nserialization, or universal hashability.\n\nModels are immutable and value-oriented, but hashability is not universal:\nrecursively immutable JSON mappings use `MappingProxyType`, which is not\nhashable. Equality remains predictable; callers must not assume every file\nmodel can be used as a dictionary key.\n\n## Binary and text\n\n`BinaryFile` stores immutable `bytes`, a `truncated` flag, and `size_bytes` for\nthe retained byte count. It is currently model-only; there is no BinaryCodec or\ngeneric binary I/O.\n\n`TextFile` stores `content`, `encoding`, `byte_size`, and `truncated`. It\nprovides `character_count`, literal `contains()`, and regex wrappers\n`search_regex()` / `find_all_regex()`. It deliberately has no `__iter__()`.\nLogical lines are exactly `tuple(content.splitlines())`: separators are\nremoved, and a final newline does not retain a terminal empty line.\n\n## Provenance\n\nJSON and CSV `.content` is original decoded source provenance. Their structured\nstate can diverge through immutable transformations; codecs persist that state\nrather than stale source. Markdown headings/sections are derived from\nauthoritative `.content`; TextFile has no secondary state.\n",
        "resource": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "start": 100,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/models.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "packet_ordinal": 299
    },
    "resource": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
    "semantic_rationale": "Provides shared model hierarchy and source metadata semantics, corroborating unchanged codec results.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "end": 1820,
        "end_line": 51,
        "quote": "## Hierarchy\n\n```text\nFile\n\u251c\u2500\u2500 BinaryFile\n\u2514\u2500\u2500 TextFile\n    \u251c\u2500\u2500 JsonFile\n    \u2502   \u251c\u2500\u2500 JsonObjectFile\n    \u2502   \u251c\u2500\u2500 JsonListFile\n    \u2502   \u2514\u2500\u2500 JsonScalarFile\n    \u251c\u2500\u2500 MarkdownFile\n    \u2514\u2500\u2500 CsvFile\n```\n\nInheritance expresses shared source representation, not interchangeable\nserialization semantics. Structured models retain their own operations and\ntheir codecs are selected explicitly by format.\n\n## `File`\n\n`File` is the minimal frozen, slotted base. It associates a `ResolvedPath`\nwith an abstract `FileFormat`. It does not promise text, structured values,\nserialization, or universal hashability.\n\nModels are immutable and value-oriented, but hashability is not universal:\nrecursively immutable JSON mappings use `MappingProxyType`, which is not\nhashable. Equality remains predictable; callers must not assume every file\nmodel can be used as a dictionary key.\n\n## Binary and text\n\n`BinaryFile` stores immutable `bytes`, a `truncated` flag, and `size_bytes` for\nthe retained byte count. It is currently model-only; there is no BinaryCodec or\ngeneric binary I/O.\n\n`TextFile` stores `content`, `encoding`, `byte_size`, and `truncated`. It\nprovides `character_count`, literal `contains()`, and regex wrappers\n`search_regex()` / `find_all_regex()`. It deliberately has no `__iter__()`.\nLogical lines are exactly `tuple(content.splitlines())`: separators are\nremoved, and a final newline does not retain a terminal empty line.\n\n## Provenance\n\nJSON and CSV `.content` is original decoded source provenance. Their structured\nstate can diverge through immutable transformations; codecs persist that state\nrather than stale source. Markdown headings/sections are derived from\nauthoritative `.content`; TextFile has no secondary state.\n",
        "resource": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "start": 100,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "packet_ordinal": 300
    },
    "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "semantic_rationale": "The public API inventory and supported-format table corroborate compatibility without requiring each exported resource.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 1036,
        "end_line": 23,
        "quote": "## Public API\n\nThe root package exports generic I/O (`read`, `write`, `resolve_file_format`,\nand `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file\nmodels, structured JSON/Markdown/CSV models, and filesystem errors. Internal\ncodec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain\nat the representation-model boundary rather than the root package.\n\n| Format   | Model | Codec | Generic read/write |\n|----------|------:|------:|-------------------:|\n| Binary   |   Yes |    No |                 No |\n| Text     |   Yes |   Yes |                Yes |\n| JSON     |   Yes |   Yes |                Yes |\n| CSV      |   Yes |   Yes |                Yes |\n| Markdown |   Yes |   Yes |                Yes |\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 294,
        "start_line": 9
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "packet_ordinal": 300
    },
    "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "semantic_rationale": "The public API inventory and supported-format table corroborate compatibility without requiring each exported resource.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 1036,
        "end_line": 23,
        "quote": "## Public API\n\nThe root package exports generic I/O (`read`, `write`, `resolve_file_format`,\nand `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file\nmodels, structured JSON/Markdown/CSV models, and filesystem errors. Internal\ncodec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain\nat the representation-model boundary rather than the root package.\n\n| Format   | Model | Codec | Generic read/write |\n|----------|------:|------:|-------------------:|\n| Binary   |   Yes |    No |                 No |\n| Text     |   Yes |   Yes |                Yes |\n| JSON     |   Yes |   Yes |                Yes |\n| CSV      |   Yes |   Yes |                Yes |\n| Markdown |   Yes |   Yes |                Yes |\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 294,
        "start_line": 9
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/overview.md",
    "inferability_rationale": "Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "packet_ordinal": 300
    },
    "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R05: Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 2476,
        "end_line": 71,
        "quote": "## Dependencies\n\nFilesystem consumes `ResolvedPath` from `devtools.core.paths`, generic regex\nmechanics from `devtools.core.regex`, and callable conversion from\n`devtools.core.conversion`. It does not depend on `devtools.core.system`.\n\n## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 1925,
        "start_line": 60
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/overview.md",
    "inferability_rationale": "The overview is needed for its current public claims, not merely its filename.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "packet_ordinal": 300
    },
    "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R09: The requested overview update must distinguish the new acquisition guarantee from stronger excluded pathname/security guarantees within the existing public documentation.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 1036,
        "end_line": 23,
        "quote": "## Public API\n\nThe root package exports generic I/O (`read`, `write`, `resolve_file_format`,\nand `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file\nmodels, structured JSON/Markdown/CSV models, and filesystem errors. Internal\ncodec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain\nat the representation-model boundary rather than the root package.\n\n| Format   | Model | Codec | Generic read/write |\n|----------|------:|------:|-------------------:|\n| Binary   |   Yes |    No |                 No |\n| Text     |   Yes |   Yes |                Yes |\n| JSON     |   Yes |   Yes |                Yes |\n| CSV      |   Yes |   Yes |                Yes |\n| Markdown |   Yes |   Yes |                Yes |\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 294,
        "start_line": 9
      },
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 3247,
        "end_line": 100,
        "quote": "## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n\n## Errors\n\n```text\nFilesystemError\n\u251c\u2500\u2500 FilesystemNotFoundError\n\u251c\u2500\u2500 NotAFileError\n\u251c\u2500\u2500 FileTooLargeError\n\u251c\u2500\u2500 FilesystemPermissionError\n\u251c\u2500\u2500 TextDecodingError\n\u251c\u2500\u2500 TextEncodingError\n\u2514\u2500\u2500 FileFormatError\n```\n\n`FileExistsError` intentionally remains the built-in failure for\n`write(..., overwrite=False)`.\n\n## Limitations\n\nGeneric I/O does not provide containment, symlink-escape prevention,\nauthorization, race-free limits, locking, ownership policy, secure deletion,\nor parent-directory durability after power loss. See [io.md](io.md) for the\nexact read and write limits.\n\n## Future evolution\n\nConcrete deferred work is recorded in [roadmap.md](roadmap.md). It does not\nauthorize dynamic codec registries, plugin discovery, repository indexing, or\nfilesystem security policy.\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 2161,
        "start_line": 66
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/roadmap.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O2",
    "provenance": {
      "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "packet_ordinal": 301
    },
    "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "semantic_rationale": "Corroborates deferred streaming and package exclusions, which the task already prescribes for this change.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "end": 1267,
        "end_line": 37,
        "quote": "## Strict bounded and streaming reads\n\nStreaming or chunk-bounded reads could enforce a hard memory bound where\ncurrent stat/read/post-check behavior is insufficient. Format-specific\nstreaming should be added only where consumers require it.\n\n## Source-format-preserving writes\n\nStructured JSON and CSV transformations currently serialize current state,\nnot original formatting. More faithful output could be evaluated if consumers\ndemonstrate a need; arbitrary round-trip fidelity is not promised.\n\n## Markdown source fidelity\n\nExact Markdown section source slices, and richer structure, may be justified\nonly by concrete consumers.\n\n## Format evaluation\n\nTOML, YAML, XML, and source-code models are candidates for future evaluation,\nnot commitments.\n\n## Explicit non-goals\n\nPlugin discovery, dynamic codec registries, filesystem authorization,\nsandbox policy, and repository indexing remain outside the immediate\nfilesystem roadmap.\n",
        "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "start": 332,
        "start_line": 11
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/roadmap.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "packet_ordinal": 301
    },
    "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "semantic_rationale": "Corroborates deferred streaming and package exclusions, which the task already prescribes for this change.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "end": 1267,
        "end_line": 37,
        "quote": "## Strict bounded and streaming reads\n\nStreaming or chunk-bounded reads could enforce a hard memory bound where\ncurrent stat/read/post-check behavior is insufficient. Format-specific\nstreaming should be added only where consumers require it.\n\n## Source-format-preserving writes\n\nStructured JSON and CSV transformations currently serialize current state,\nnot original formatting. More faithful output could be evaluated if consumers\ndemonstrate a need; arbitrary round-trip fidelity is not promised.\n\n## Markdown source fidelity\n\nExact Markdown section source slices, and richer structure, may be justified\nonly by concrete consumers.\n\n## Format evaluation\n\nTOML, YAML, XML, and source-code models are candidates for future evaluation,\nnot commitments.\n\n## Explicit non-goals\n\nPlugin discovery, dynamic codec registries, filesystem authorization,\nsandbox policy, and repository indexing remain outside the immediate\nfilesystem roadmap.\n",
        "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "start": 332,
        "start_line": 11
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/docs/roadmap.md",
    "inferability_rationale": "Future scope is not authorized by its presence in the roadmap; the task controls the narrower change.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "packet_ordinal": 301
    },
    "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R10: The new feature must be removed from deferred scope without promoting streaming parsers or a decoded-memory guarantee. This requires the existing roadmap distinction.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "end": 1267,
        "end_line": 37,
        "quote": "This document records concrete evaluation areas, not committed implementation\nwork. See the current [overview](overview.md) and [I/O contract](io.md).\n\n## Binary I/O\n\nA BinaryCodec and explicit generic binary read/write policy may be justified.\nThis does not imply arbitrary binary format detection.\n\n## Strict bounded and streaming reads\n\nStreaming or chunk-bounded reads could enforce a hard memory bound where\ncurrent stat/read/post-check behavior is insufficient. Format-specific\nstreaming should be added only where consumers require it.\n\n## Source-format-preserving writes\n\nStructured JSON and CSV transformations currently serialize current state,\nnot original formatting. More faithful output could be evaluated if consumers\ndemonstrate a need; arbitrary round-trip fidelity is not promised.\n\n## Markdown source fidelity\n\nExact Markdown section source slices, and richer structure, may be justified\nonly by concrete consumers.\n\n## Format evaluation\n\nTOML, YAML, XML, and source-code models are candidates for future evaluation,\nnot commitments.\n\n## Explicit non-goals\n\nPlugin discovery, dynamic codec registries, filesystem authorization,\nsandbox policy, and repository indexing remain outside the immediate\nfilesystem roadmap.\n",
        "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "start": 31,
        "start_line": 3
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/errors.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "packet_ordinal": 302
    },
    "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
    "semantic_rationale": "Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/errors.py",
        "end": 988,
        "end_line": 34,
        "quote": "class FilesystemError(Exception):\n    \"\"\"Base exception for filesystem-domain failures.\"\"\"\n\n\nclass FilesystemNotFoundError(FilesystemError):\n    \"\"\"Raised when a requested filesystem path does not exist.\"\"\"\n\n\nclass NotAFileError(FilesystemError):\n    \"\"\"Raised when an operation requires a regular file.\"\"\"\n\n\nclass FileTooLargeError(FilesystemError):\n    \"\"\"Raised when a file exceeds an allowed read size.\"\"\"\n\n\nclass FilesystemPermissionError(FilesystemError):\n    \"\"\"Raised when a filesystem operation is denied by permissions.\"\"\"\n\n\nclass TextDecodingError(FilesystemError):\n    \"\"\"Raised when file bytes cannot be decoded using the requested encoding.\"\"\"\n\n\nclass TextEncodingError(FilesystemError):\n    \"\"\"Raised when text cannot be encoded using the requested encoding.\"\"\"\n\n\nclass FileFormatError(FilesystemError):\n    \"\"\"Raised when file content does not conform to its expected format.\"\"\"\n",
        "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "start": 93,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/errors.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O2",
    "provenance": {
      "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "packet_ordinal": 302
    },
    "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
    "semantic_rationale": "Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/errors.py",
        "end": 988,
        "end_line": 34,
        "quote": "class FilesystemError(Exception):\n    \"\"\"Base exception for filesystem-domain failures.\"\"\"\n\n\nclass FilesystemNotFoundError(FilesystemError):\n    \"\"\"Raised when a requested filesystem path does not exist.\"\"\"\n\n\nclass NotAFileError(FilesystemError):\n    \"\"\"Raised when an operation requires a regular file.\"\"\"\n\n\nclass FileTooLargeError(FilesystemError):\n    \"\"\"Raised when a file exceeds an allowed read size.\"\"\"\n\n\nclass FilesystemPermissionError(FilesystemError):\n    \"\"\"Raised when a filesystem operation is denied by permissions.\"\"\"\n\n\nclass TextDecodingError(FilesystemError):\n    \"\"\"Raised when file bytes cannot be decoded using the requested encoding.\"\"\"\n\n\nclass TextEncodingError(FilesystemError):\n    \"\"\"Raised when text cannot be encoded using the requested encoding.\"\"\"\n\n\nclass FileFormatError(FilesystemError):\n    \"\"\"Raised when file content does not conform to its expected format.\"\"\"\n",
        "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "start": 93,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/errors.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "packet_ordinal": 302
    },
    "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
    "semantic_rationale": "Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/errors.py",
        "end": 988,
        "end_line": 34,
        "quote": "class FilesystemError(Exception):\n    \"\"\"Base exception for filesystem-domain failures.\"\"\"\n\n\nclass FilesystemNotFoundError(FilesystemError):\n    \"\"\"Raised when a requested filesystem path does not exist.\"\"\"\n\n\nclass NotAFileError(FilesystemError):\n    \"\"\"Raised when an operation requires a regular file.\"\"\"\n\n\nclass FileTooLargeError(FilesystemError):\n    \"\"\"Raised when a file exceeds an allowed read size.\"\"\"\n\n\nclass FilesystemPermissionError(FilesystemError):\n    \"\"\"Raised when a filesystem operation is denied by permissions.\"\"\"\n\n\nclass TextDecodingError(FilesystemError):\n    \"\"\"Raised when file bytes cannot be decoded using the requested encoding.\"\"\"\n\n\nclass TextEncodingError(FilesystemError):\n    \"\"\"Raised when text cannot be encoded using the requested encoding.\"\"\"\n\n\nclass FileFormatError(FilesystemError):\n    \"\"\"Raised when file content does not conform to its expected format.\"\"\"\n",
        "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "start": 93,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/errors.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "packet_ordinal": 302
    },
    "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
    "semantic_rationale": "Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/errors.py",
        "end": 988,
        "end_line": 34,
        "quote": "class FilesystemError(Exception):\n    \"\"\"Base exception for filesystem-domain failures.\"\"\"\n\n\nclass FilesystemNotFoundError(FilesystemError):\n    \"\"\"Raised when a requested filesystem path does not exist.\"\"\"\n\n\nclass NotAFileError(FilesystemError):\n    \"\"\"Raised when an operation requires a regular file.\"\"\"\n\n\nclass FileTooLargeError(FilesystemError):\n    \"\"\"Raised when a file exceeds an allowed read size.\"\"\"\n\n\nclass FilesystemPermissionError(FilesystemError):\n    \"\"\"Raised when a filesystem operation is denied by permissions.\"\"\"\n\n\nclass TextDecodingError(FilesystemError):\n    \"\"\"Raised when file bytes cannot be decoded using the requested encoding.\"\"\"\n\n\nclass TextEncodingError(FilesystemError):\n    \"\"\"Raised when text cannot be encoded using the requested encoding.\"\"\"\n\n\nclass FileFormatError(FilesystemError):\n    \"\"\"Raised when file content does not conform to its expected format.\"\"\"\n",
        "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "start": 93,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/errors.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "packet_ordinal": 302
    },
    "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
    "semantic_rationale": "Defines existing exception classes and common domain base; the required raised names and integration are already established by task and reader/resolver.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/errors.py",
        "end": 988,
        "end_line": 34,
        "quote": "class FilesystemError(Exception):\n    \"\"\"Base exception for filesystem-domain failures.\"\"\"\n\n\nclass FilesystemNotFoundError(FilesystemError):\n    \"\"\"Raised when a requested filesystem path does not exist.\"\"\"\n\n\nclass NotAFileError(FilesystemError):\n    \"\"\"Raised when an operation requires a regular file.\"\"\"\n\n\nclass FileTooLargeError(FilesystemError):\n    \"\"\"Raised when a file exceeds an allowed read size.\"\"\"\n\n\nclass FilesystemPermissionError(FilesystemError):\n    \"\"\"Raised when a filesystem operation is denied by permissions.\"\"\"\n\n\nclass TextDecodingError(FilesystemError):\n    \"\"\"Raised when file bytes cannot be decoded using the requested encoding.\"\"\"\n\n\nclass TextEncodingError(FilesystemError):\n    \"\"\"Raised when text cannot be encoded using the requested encoding.\"\"\"\n\n\nclass FileFormatError(FilesystemError):\n    \"\"\"Raised when file content does not conform to its expected format.\"\"\"\n",
        "resource": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "start": 93,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/base.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "ada2cec083ac5e9dd101a357401c7d7f18091fbb4c45ddaf8cf09d37b31caa3c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
      "packet_ordinal": 304
    },
    "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
    "semantic_rationale": "Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/base.py",
        "end": 761,
        "end_line": 37,
        "quote": "class FileFormat(StrEnum):\n    \"\"\"Supported file content formats.\"\"\"\n\n    BINARY = \"binary\"\n    TEXT = \"text\"\n    JSON = \"json\"\n    CSV = \"csv\"\n    MARKDOWN = \"markdown\"\n\n\n@dataclass(frozen=True, slots=True)\nclass File(ABC):\n    \"\"\"Represent an immutable filesystem-backed file.\n\n    :ivar path: Resolved filesystem path.\n    \"\"\"\n\n    path: ResolvedPath\n\n    @property\n    @abstractmethod\n    def format(self) -> FileFormat:\n        \"\"\"Return the represented file format.\"\"\"\n",
        "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
        "start": 286,
        "start_line": 15
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/base.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "ada2cec083ac5e9dd101a357401c7d7f18091fbb4c45ddaf8cf09d37b31caa3c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
      "packet_ordinal": 304
    },
    "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
    "semantic_rationale": "Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/base.py",
        "end": 761,
        "end_line": 37,
        "quote": "class FileFormat(StrEnum):\n    \"\"\"Supported file content formats.\"\"\"\n\n    BINARY = \"binary\"\n    TEXT = \"text\"\n    JSON = \"json\"\n    CSV = \"csv\"\n    MARKDOWN = \"markdown\"\n\n\n@dataclass(frozen=True, slots=True)\nclass File(ABC):\n    \"\"\"Represent an immutable filesystem-backed file.\n\n    :ivar path: Resolved filesystem path.\n    \"\"\"\n\n    path: ResolvedPath\n\n    @property\n    @abstractmethod\n    def format(self) -> FileFormat:\n        \"\"\"Return the represented file format.\"\"\"\n",
        "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
        "start": 286,
        "start_line": 15
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/base.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "ada2cec083ac5e9dd101a357401c7d7f18091fbb4c45ddaf8cf09d37b31caa3c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
      "packet_ordinal": 304
    },
    "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
    "semantic_rationale": "Shows FileFormat members and abstract File path/format shape; useful typing context, not a new required model implementation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/base.py",
        "end": 761,
        "end_line": 37,
        "quote": "class FileFormat(StrEnum):\n    \"\"\"Supported file content formats.\"\"\"\n\n    BINARY = \"binary\"\n    TEXT = \"text\"\n    JSON = \"json\"\n    CSV = \"csv\"\n    MARKDOWN = \"markdown\"\n\n\n@dataclass(frozen=True, slots=True)\nclass File(ABC):\n    \"\"\"Represent an immutable filesystem-backed file.\n\n    :ivar path: Resolved filesystem path.\n    \"\"\"\n\n    path: ResolvedPath\n\n    @property\n    @abstractmethod\n    def format(self) -> FileFormat:\n        \"\"\"Return the represented file format.\"\"\"\n",
        "resource": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
        "start": 286,
        "start_line": 15
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "0cade3699fe596ba492a6509405496cba9b3e2b616d8c0de6f19b47ca0ba9d40",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
      "packet_ordinal": 306
    },
    "resource": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/csv.py",
        "end": 7130,
        "end_line": 212,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CsvFile(TextFile):\n    \"\"\"Represent immutable header-based CSV source and structured rows.\n\n    ``content`` is original decoded source provenance. ``headers`` and ``rows``\n    are the current structured state; ``CsvCodec`` serializes that state after\n    immutable transformations.\n\n    :ivar headers: Unique, non-blank CSV headers.\n    :ivar rows: Immutable rows sharing the file headers.\n    :ivar dialect: CSV parsing and serialization policy.\n    \"\"\"\n\n    headers: tuple[str, ...] = field(kw_only=True)\n    rows: tuple[CsvRow, ...] = field(kw_only=True)\n    dialect: CsvDialect = field(default_factory=CsvDialect, kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate text metadata and freeze structured CSV state.\"\"\"\n        super().__post_init__()\n        object.__setattr__(self, \"headers\", tuple(self.headers))\n        object.__setattr__(self, \"rows\", tuple(self.rows))\n\n        if not self.headers:\n            msg = \"CSV files require a header row.\"\n            raise ValueError(msg)\n\n        if any(not header.strip() for header in self.headers):\n            msg = \"CSV headers cannot be blank.\"\n            raise ValueError(msg)\n\n        if len(set(self.headers)) != len(self.headers):\n            msg = \"CSV headers must be unique.\"\n            raise ValueError(msg)\n\n        for row in self.rows:\n            if row.headers != self.headers:\n                msg = \"CSV row headers must match the file headers.\"\n                raise ValueError(msg)\n\n    @property\n    def format(self) -> FileFormat:\n        \"\"\"Return the CSV file format.\"\"\"\n        return FileFormat.CSV\n",
        "resource": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
        "start": 5485,
        "start_line": 169
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "0cade3699fe596ba492a6509405496cba9b3e2b616d8c0de6f19b47ca0ba9d40",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
      "packet_ordinal": 306
    },
    "resource": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/csv.py",
        "end": 7130,
        "end_line": 212,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CsvFile(TextFile):\n    \"\"\"Represent immutable header-based CSV source and structured rows.\n\n    ``content`` is original decoded source provenance. ``headers`` and ``rows``\n    are the current structured state; ``CsvCodec`` serializes that state after\n    immutable transformations.\n\n    :ivar headers: Unique, non-blank CSV headers.\n    :ivar rows: Immutable rows sharing the file headers.\n    :ivar dialect: CSV parsing and serialization policy.\n    \"\"\"\n\n    headers: tuple[str, ...] = field(kw_only=True)\n    rows: tuple[CsvRow, ...] = field(kw_only=True)\n    dialect: CsvDialect = field(default_factory=CsvDialect, kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate text metadata and freeze structured CSV state.\"\"\"\n        super().__post_init__()\n        object.__setattr__(self, \"headers\", tuple(self.headers))\n        object.__setattr__(self, \"rows\", tuple(self.rows))\n\n        if not self.headers:\n            msg = \"CSV files require a header row.\"\n            raise ValueError(msg)\n\n        if any(not header.strip() for header in self.headers):\n            msg = \"CSV headers cannot be blank.\"\n            raise ValueError(msg)\n\n        if len(set(self.headers)) != len(self.headers):\n            msg = \"CSV headers must be unique.\"\n            raise ValueError(msg)\n\n        for row in self.rows:\n            if row.headers != self.headers:\n                msg = \"CSV row headers must match the file headers.\"\n                raise ValueError(msg)\n\n    @property\n    def format(self) -> FileFormat:\n        \"\"\"Return the CSV file format.\"\"\"\n        return FileFormat.CSV\n",
        "resource": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
        "start": 5485,
        "start_line": 169
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/list.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "b855a01565970c7c0cf19e77c796713ed08ddf8905fa1beb37d3cabe85811424",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
      "packet_ordinal": 310
    },
    "resource": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/list.py",
        "end": 1181,
        "end_line": 38,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonListFile(JsonFile, Sequence[JsonValue]):\n    \"\"\"Represent a JSON document whose root value is an array.\"\"\"\n\n    value: tuple[JsonValue, ...] = field(kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate inherited text fields and freeze JSON storage.\"\"\"\n        super().__post_init__()\n        frozen = freeze_json(self.value)\n\n        if not isinstance(frozen, tuple):\n            msg = \"JsonListFile requires an array value.\"\n            raise TypeError(msg)\n\n        object.__setattr__(self, \"value\", frozen)\n",
        "resource": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
        "start": 606,
        "start_line": 23
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/list.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "b855a01565970c7c0cf19e77c796713ed08ddf8905fa1beb37d3cabe85811424",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
      "packet_ordinal": 310
    },
    "resource": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/list.py",
        "end": 1181,
        "end_line": 38,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonListFile(JsonFile, Sequence[JsonValue]):\n    \"\"\"Represent a JSON document whose root value is an array.\"\"\"\n\n    value: tuple[JsonValue, ...] = field(kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate inherited text fields and freeze JSON storage.\"\"\"\n        super().__post_init__()\n        frozen = freeze_json(self.value)\n\n        if not isinstance(frozen, tuple):\n            msg = \"JsonListFile requires an array value.\"\n            raise TypeError(msg)\n\n        object.__setattr__(self, \"value\", frozen)\n",
        "resource": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
        "start": 606,
        "start_line": 23
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/object.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "6a5b17b886fdb64baf279da53a8e07a78be8bdc38a590fce40f20979ede87891",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
      "packet_ordinal": 311
    },
    "resource": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/object.py",
        "end": 1294,
        "end_line": 42,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonObjectFile(JsonFile, Mapping[str, JsonValue]):\n    \"\"\"Represent a JSON document whose root value is an object.\n\n    The object provides normal read-only mapping behavior while immutable\n    transformation methods return new file values.\n    \"\"\"\n\n    value: Mapping[str, JsonValue] = field(kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate inherited text fields and freeze JSON storage.\"\"\"\n        super().__post_init__()\n        frozen = freeze_json(self.value)\n\n        if not isinstance(frozen, Mapping):\n            msg = \"JsonObjectFile requires an object value.\"\n            raise TypeError(msg)\n\n        object.__setattr__(self, \"value\", frozen)\n",
        "resource": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
        "start": 574,
        "start_line": 23
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/object.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "6a5b17b886fdb64baf279da53a8e07a78be8bdc38a590fce40f20979ede87891",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
      "packet_ordinal": 311
    },
    "resource": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/object.py",
        "end": 1294,
        "end_line": 42,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonObjectFile(JsonFile, Mapping[str, JsonValue]):\n    \"\"\"Represent a JSON document whose root value is an object.\n\n    The object provides normal read-only mapping behavior while immutable\n    transformation methods return new file values.\n    \"\"\"\n\n    value: Mapping[str, JsonValue] = field(kw_only=True)\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate inherited text fields and freeze JSON storage.\"\"\"\n        super().__post_init__()\n        frozen = freeze_json(self.value)\n\n        if not isinstance(frozen, Mapping):\n            msg = \"JsonObjectFile requires an object value.\"\n            raise TypeError(msg)\n\n        object.__setattr__(self, \"value\", frozen)\n",
        "resource": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
        "start": 574,
        "start_line": 23
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/scalar.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "adb1025a200bdce3fb68c5fd4f082ce102b3b5691774b84212d59da3555da6a7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
      "packet_ordinal": 312
    },
    "resource": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/scalar.py",
        "end": 546,
        "end_line": 20,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonScalarFile(JsonFile):\n    \"\"\"Represent a JSON document whose root is a scalar value.\"\"\"\n\n    value: JsonScalar = field(kw_only=True)\n",
        "resource": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
        "start": 367,
        "start_line": 16
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/json/scalar.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "adb1025a200bdce3fb68c5fd4f082ce102b3b5691774b84212d59da3555da6a7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
      "packet_ordinal": 312
    },
    "resource": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/json/scalar.py",
        "end": 546,
        "end_line": 20,
        "quote": "@dataclass(frozen=True, slots=True)\nclass JsonScalarFile(JsonFile):\n    \"\"\"Represent a JSON document whose root is a scalar value.\"\"\"\n\n    value: JsonScalar = field(kw_only=True)\n",
        "resource": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
        "start": 367,
        "start_line": 16
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/markdown/file.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
      "packet_ordinal": 314
    },
    "resource": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/markdown/file.py",
        "end": 1189,
        "end_line": 39,
        "quote": "@dataclass(frozen=True, slots=True)\nclass MarkdownFile(TextFile):\n    \"\"\"Represent immutable Markdown source with structural access.\n\n    The model currently recognizes ATX headings only. Headings inside fenced\n    code blocks are ignored.\n\n    :ivar content: Original decoded Markdown source.\n    \"\"\"\n\n    _ATX_HEADING_PATTERN: ClassVar[re.Pattern[str]] = re.compile(\n        r\"^(?P<marker>#{1,6})[ \\t]+(?P<text>.*?)[ \\t]*#*[ \\t]*$\",\n    )\n    _FENCE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(\n        r\"^[ \\t]{0,3}(?P<fence>`{3,}|~{3,})\",\n    )\n\n    @property\n    def format(self) -> FileFormat:\n        \"\"\"Return the Markdown file format.\n\n        :returns: Markdown file format.\n        \"\"\"\n        return FileFormat.MARKDOWN\n",
        "resource": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
        "start": 453,
        "start_line": 16
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/markdown/file.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
      "packet_ordinal": 314
    },
    "resource": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/markdown/file.py",
        "end": 1189,
        "end_line": 39,
        "quote": "@dataclass(frozen=True, slots=True)\nclass MarkdownFile(TextFile):\n    \"\"\"Represent immutable Markdown source with structural access.\n\n    The model currently recognizes ATX headings only. Headings inside fenced\n    code blocks are ignored.\n\n    :ivar content: Original decoded Markdown source.\n    \"\"\"\n\n    _ATX_HEADING_PATTERN: ClassVar[re.Pattern[str]] = re.compile(\n        r\"^(?P<marker>#{1,6})[ \\t]+(?P<text>.*?)[ \\t]*#*[ \\t]*$\",\n    )\n    _FENCE_PATTERN: ClassVar[re.Pattern[str]] = re.compile(\n        r\"^[ \\t]{0,3}(?P<fence>`{3,}|~{3,})\",\n    )\n\n    @property\n    def format(self) -> FileFormat:\n        \"\"\"Return the Markdown file format.\n\n        :returns: Markdown file format.\n        \"\"\"\n        return FileFormat.MARKDOWN\n",
        "resource": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
        "start": 453,
        "start_line": 16
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "packet_ordinal": 317
    },
    "resource": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/text.py",
        "end": 1183,
        "end_line": 42,
        "quote": "@dataclass(frozen=True, slots=True)\nclass TextFile(File):\n    \"\"\"Represent immutable decoded text file content.\n\n    :ivar content: Decoded source content.\n    :ivar encoding: Encoding used to decode source bytes.\n    :ivar byte_size: Number of retained source bytes.\n    :ivar truncated: Whether source content was truncated.\n    \"\"\"\n\n    content: str\n    encoding: str = \"utf-8\"\n    byte_size: int = 0\n    truncated: bool = False\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate text-file invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the text file.\n\n        :raises ValueError: If the encoding is blank or byte size is negative.\n        \"\"\"\n        if not self.encoding.strip():\n            msg = \"Text file encoding cannot be empty.\"\n            raise ValueError(msg)\n\n        if self.byte_size < 0:\n            msg = \"Text file byte size cannot be negative.\"\n            raise ValueError(msg)\n",
        "resource": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "start": 228,
        "start_line": 12
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/models/text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "packet_ordinal": 317
    },
    "resource": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
    "semantic_rationale": "Shows current concrete or shared model state, useful for rich-result assertions. Reusing unchanged codec construction preserves these invariants without independently reimplementing them.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/models/text.py",
        "end": 1183,
        "end_line": 42,
        "quote": "@dataclass(frozen=True, slots=True)\nclass TextFile(File):\n    \"\"\"Represent immutable decoded text file content.\n\n    :ivar content: Decoded source content.\n    :ivar encoding: Encoding used to decode source bytes.\n    :ivar byte_size: Number of retained source bytes.\n    :ivar truncated: Whether source content was truncated.\n    \"\"\"\n\n    content: str\n    encoding: str = \"utf-8\"\n    byte_size: int = 0\n    truncated: bool = False\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate text-file invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the text file.\n\n        :raises ValueError: If the encoding is blank or byte size is negative.\n        \"\"\"\n        if not self.encoding.strip():\n            msg = \"Text file encoding cannot be empty.\"\n            raise ValueError(msg)\n\n        if self.byte_size < 0:\n            msg = \"Text file byte size cannot be negative.\"\n            raise ValueError(msg)\n",
        "resource": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "start": 228,
        "start_line": 12
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
    "label": "REQUIRED",
    "obligation": "O1",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R01: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.; R16: These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 906,
        "end_line": 35,
        "quote": "DEFAULT_MAX_READ_BYTES = 16 * 1024 * 1024\n\n\ndef read(\n    path: ResolvedPath,\n    *,\n    file_format: FileFormat | None = None,\n    max_bytes: int | None = DEFAULT_MAX_READ_BYTES,\n) -> File:\n    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 526,
        "start_line": 23
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 3200,
        "start_line": 107
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 1121,
        "end_line": 39,
        "quote": "    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 907,
        "start_line": 37
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2542,
        "end_line": 82,
        "quote": "        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1922,
        "start_line": 61
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O2",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Locates existing acquisition and error seams for implementing the task-defined lifecycle and regression tests; the future bound and fixture design do not require an additional current lifecycle fact.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    source = path.value\n\n    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n\n\ndef _validate_read_size(\n    path: ResolvedPath,\n    *,\n    size_bytes: int,\n    max_bytes: int | None,\n) -> None:\n    \"\"\"Validate a file against the configured read limit.\n\n    :param path: File being validated.\n    :param size_bytes: File size reported by the filesystem.\n    :param max_bytes: Maximum permitted byte count.\n    :raises ValueError: If ``max_bytes`` is negative.\n    :raises FileTooLargeError: If the file exceeds the configured limit.\n    \"\"\"\n    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1608,
        "start_line": 50
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "For identical complete bytes, original path and unchanged codec invocation, existing codec/model behavior is preserved. No independent implementation of codecs or constructors is needed. This is a preservation argument, not proof that each desired future property already exists.",
    "label": "REQUIRED",
    "obligation": "O3",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R02: This seam is necessary to preserve codec behavior by leaving the existing resolution and decode path intact. It permits black-box preservation across every concrete codec.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2737,
        "end_line": 90,
        "quote": "    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 2435,
        "start_line": 78
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R04: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.; R17: The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2737,
        "end_line": 90,
        "quote": "    source = path.value\n\n    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1608,
        "start_line": 50
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 3200,
        "start_line": 107
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2124,
        "end_line": 64,
        "quote": "    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1633,
        "start_line": 52
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2434,
        "end_line": 76,
        "quote": "    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 2231,
        "start_line": 72
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Locates existing acquisition and error seams for implementing the task-defined lifecycle and regression tests; the future bound and fixture design do not require an additional current lifecycle fact.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    source = path.value\n\n    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n\n\ndef _validate_read_size(\n    path: ResolvedPath,\n    *,\n    size_bytes: int,\n    max_bytes: int | None,\n) -> None:\n    \"\"\"Validate a file against the configured read limit.\n\n    :param path: File being validated.\n    :param size_bytes: File size reported by the filesystem.\n    :param max_bytes: Maximum permitted byte count.\n    :raises ValueError: If ``max_bytes`` is negative.\n    :raises FileTooLargeError: If the file exceeds the configured limit.\n    \"\"\"\n    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1608,
        "start_line": 50
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/reading.py",
    "inferability_rationale": "This location is necessary because the current text establishes a distinct stale public documentation surface; implementation ownership alone would not make it necessary.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "packet_ordinal": 318
    },
    "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R11: The conditional public-API documentation update is applicable because the callable itself contains a behavior statement invalidated by the new acquisition algorithm.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 1608,
        "end_line": 49,
        "quote": "    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n\n    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n\n    :param path: Resolved path to the file.\n    :param file_format: Explicit file format override.\n    :param max_bytes: Maximum permitted file size, or ``None`` for no limit.\n    :returns: Decoded file model.\n    :raises FilesystemNotFoundError: If the target does not exist.\n    :raises NotAFileError: If the target is not a regular file.\n    :raises FileTooLargeError: If the file exceeds ``max_bytes``.\n    :raises FilesystemPermissionError: If filesystem access is denied.\n    \"\"\"\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 717,
        "start_line": 32
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/resolution.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "packet_ordinal": 319
    },
    "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
    "semantic_rationale": "The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/resolution.py",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O3",
    "provenance": {
      "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "packet_ordinal": 319
    },
    "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/resolution.py",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "packet_ordinal": 319
    },
    "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/resolution.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "packet_ordinal": 319
    },
    "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
    "semantic_rationale": "The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/resolution.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "packet_ordinal": 319
    },
    "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
    "semantic_rationale": "The existing resolver map helps choose formats and tests; preserve the unchanged resolver without making all its details separate obligations here.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/writing.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "packet_ordinal": 320
    },
    "resource": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
    "semantic_rationale": "Shows atomic writing has its own implementation and documented durability limit. It is protected by the task; a local read acquisition change need not inspect every write operation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/writing.py",
        "end": 1229,
        "end_line": 45,
        "quote": "def write(\n    file: File,\n    *,\n    overwrite: bool = True,\n) -> None:\n    \"\"\"Persist a file model using its format codec.\n\n    The file model's format determines the codec used for serialization.\n    Writes are performed through a sibling temporary file and atomically\n    replace the destination on success. This prevents a normally observing\n    destination from seeing partial replacement contents. It does not fsync\n    the parent directory, so directory-entry durability after sudden power\n    loss remains filesystem-dependent.\n",
        "resource": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "start": 692,
        "start_line": 33
      }
    ]
  },
  {
    "address": "src/devtools/resources/filesystem/writing.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "packet_ordinal": 320
    },
    "resource": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
    "semantic_rationale": "Shows atomic writing has its own implementation and documented durability limit. It is protected by the task; a local read acquisition change need not inspect every write operation.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/resources/filesystem/writing.py",
        "end": 1229,
        "end_line": 45,
        "quote": "def write(\n    file: File,\n    *,\n    overwrite: bool = True,\n) -> None:\n    \"\"\"Persist a file model using its format codec.\n\n    The file model's format determines the codec used for serialization.\n    Writes are performed through a sibling temporary file and atomically\n    replace the destination on success. This prevents a normally observing\n    destination from seeing partial replacement contents. It does not fsync\n    the parent directory, so directory-entry durability after sudden power\n    loss remains filesystem-dependent.\n",
        "resource": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "start": 692,
        "start_line": 33
      }
    ]
  },
  {
    "address": "src/devtools/tools/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "packet_ordinal": 324
    },
    "resource": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
    "semantic_rationale": "Clarifies Tool adaptation and lack of authorization ownership, useful corroboration of the protected higher boundary.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/docs/overview.md",
        "end": 1313,
        "end_line": 25,
        "quote": "This package owns typed reusable capability boundaries. A `Tool` defines a\nname, description, typed input validation, and asynchronous execution;\n`ToolRunner` validates and executes one Tool. The package currently includes\nbounded command and repository-filesystem Tools.\n\nTools may adapt lower-level Resources such as\n`devtools.resources.filesystem` and `devtools.resources.commands`, but a\nResource is not a Tool. Tool validation is not authorization. A Tool does not\nmake itself model-visible, parse an Action proposal, decide permission, or\nproject its result into a Prompt; those are separate caller responsibilities.\n\n`ReadRepositoryFileTool` preserves generic Filesystem format inference for\nrecognized structured formats. For an unclassified repository extension, it\nuses the same bounded Filesystem text-decoding path, allowing ordinary source\nand configuration text without assigning a FileFormat per language. Undecodable\ncontent still fails through the Filesystem text-decoding boundary.\n",
        "resource": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "start": 313,
        "start_line": 10
      }
    ]
  },
  {
    "address": "src/devtools/tools/docs/overview.md",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "packet_ordinal": 324
    },
    "resource": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
    "semantic_rationale": "Clarifies Tool adaptation and lack of authorization ownership, useful corroboration of the protected higher boundary.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/docs/overview.md",
        "end": 1313,
        "end_line": 25,
        "quote": "This package owns typed reusable capability boundaries. A `Tool` defines a\nname, description, typed input validation, and asynchronous execution;\n`ToolRunner` validates and executes one Tool. The package currently includes\nbounded command and repository-filesystem Tools.\n\nTools may adapt lower-level Resources such as\n`devtools.resources.filesystem` and `devtools.resources.commands`, but a\nResource is not a Tool. Tool validation is not authorization. A Tool does not\nmake itself model-visible, parse an Action proposal, decide permission, or\nproject its result into a Prompt; those are separate caller responsibilities.\n\n`ReadRepositoryFileTool` preserves generic Filesystem format inference for\nrecognized structured formats. For an unclassified repository extension, it\nuses the same bounded Filesystem text-decoding path, allowing ordinary source\nand configuration text without assigning a FileFormat per language. Undecodable\ncontent still fails through the Filesystem text-decoding boundary.\n",
        "resource": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "start": 313,
        "start_line": 10
      }
    ]
  },
  {
    "address": "src/devtools/tools/filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "packet_ordinal": 327
    },
    "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
    "semantic_rationale": "Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/filesystem.py",
        "end": 2043,
        "end_line": 65,
        "quote": "class ReadRepositoryFileTool:\n    \"\"\"Read bounded textual repository files within one configured root scope.\"\"\"\n\n    _NAME = \"read_repository_file\"\n    _DESCRIPTION = \"Read one bounded textual file below the configured repository root.\"\n\n    def __init__(self, root: ResolvedPath) -> None:\n        \"\"\"Create a read-only Tool scoped to one repository root.\"\"\"\n        self._root = _normalize(root)\n\n    @property\n    def name(self) -> str:\n        \"\"\"Return the local capability label.\"\"\"\n        return self._NAME\n\n    @property\n    def description(self) -> str:\n        \"\"\"Return the provider-neutral capability description.\"\"\"\n        return self._DESCRIPTION\n\n    def validate(self, arguments: ResolvedPath) -> None:\n        \"\"\"Reject paths outside this Tool's configured semantic scope.\"\"\"\n        normalized_arguments = _normalize(arguments)\n\n        if normalized_arguments.value.is_relative_to(self._root.value):\n            return\n\n        msg = f\"Path is outside the configured repository root: {arguments}.\"\n        raise ToolInputError(msg)\n\n    async def execute(self, arguments: ResolvedPath) -> File:\n        \"\"\"Read inferred structured formats or arbitrary decodable repository text.\"\"\"\n        path = _normalize(arguments)\n        try:\n            resolve_file_format(path)\n        except FileFormatError:\n            return read(path, file_format=FileFormat.TEXT)\n        return read(path)\n",
        "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "start": 636,
        "start_line": 28
      }
    ]
  },
  {
    "address": "src/devtools/tools/filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "packet_ordinal": 327
    },
    "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
    "semantic_rationale": "Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/filesystem.py",
        "end": 2043,
        "end_line": 65,
        "quote": "class ReadRepositoryFileTool:\n    \"\"\"Read bounded textual repository files within one configured root scope.\"\"\"\n\n    _NAME = \"read_repository_file\"\n    _DESCRIPTION = \"Read one bounded textual file below the configured repository root.\"\n\n    def __init__(self, root: ResolvedPath) -> None:\n        \"\"\"Create a read-only Tool scoped to one repository root.\"\"\"\n        self._root = _normalize(root)\n\n    @property\n    def name(self) -> str:\n        \"\"\"Return the local capability label.\"\"\"\n        return self._NAME\n\n    @property\n    def description(self) -> str:\n        \"\"\"Return the provider-neutral capability description.\"\"\"\n        return self._DESCRIPTION\n\n    def validate(self, arguments: ResolvedPath) -> None:\n        \"\"\"Reject paths outside this Tool's configured semantic scope.\"\"\"\n        normalized_arguments = _normalize(arguments)\n\n        if normalized_arguments.value.is_relative_to(self._root.value):\n            return\n\n        msg = f\"Path is outside the configured repository root: {arguments}.\"\n        raise ToolInputError(msg)\n\n    async def execute(self, arguments: ResolvedPath) -> File:\n        \"\"\"Read inferred structured formats or arbitrary decodable repository text.\"\"\"\n        path = _normalize(arguments)\n        try:\n            resolve_file_format(path)\n        except FileFormatError:\n            return read(path, file_format=FileFormat.TEXT)\n        return read(path)\n",
        "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "start": 636,
        "start_line": 28
      }
    ]
  },
  {
    "address": "src/devtools/tools/filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "packet_ordinal": 327
    },
    "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
    "semantic_rationale": "Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/filesystem.py",
        "end": 2043,
        "end_line": 65,
        "quote": "class ReadRepositoryFileTool:\n    \"\"\"Read bounded textual repository files within one configured root scope.\"\"\"\n\n    _NAME = \"read_repository_file\"\n    _DESCRIPTION = \"Read one bounded textual file below the configured repository root.\"\n\n    def __init__(self, root: ResolvedPath) -> None:\n        \"\"\"Create a read-only Tool scoped to one repository root.\"\"\"\n        self._root = _normalize(root)\n\n    @property\n    def name(self) -> str:\n        \"\"\"Return the local capability label.\"\"\"\n        return self._NAME\n\n    @property\n    def description(self) -> str:\n        \"\"\"Return the provider-neutral capability description.\"\"\"\n        return self._DESCRIPTION\n\n    def validate(self, arguments: ResolvedPath) -> None:\n        \"\"\"Reject paths outside this Tool's configured semantic scope.\"\"\"\n        normalized_arguments = _normalize(arguments)\n\n        if normalized_arguments.value.is_relative_to(self._root.value):\n            return\n\n        msg = f\"Path is outside the configured repository root: {arguments}.\"\n        raise ToolInputError(msg)\n\n    async def execute(self, arguments: ResolvedPath) -> File:\n        \"\"\"Read inferred structured formats or arbitrary decodable repository text.\"\"\"\n        path = _normalize(arguments)\n        try:\n            resolve_file_format(path)\n        except FileFormatError:\n            return read(path, file_format=FileFormat.TEXT)\n        return read(path)\n",
        "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "start": 636,
        "start_line": 28
      }
    ]
  },
  {
    "address": "src/devtools/tools/filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "packet_ordinal": 327
    },
    "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
    "semantic_rationale": "Shows higher Tool path validation and inferred/text-fallback reads. Existing public behavior preservation covers this adapter without changing Tool authorization.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "src/devtools/tools/filesystem.py",
        "end": 2043,
        "end_line": 65,
        "quote": "class ReadRepositoryFileTool:\n    \"\"\"Read bounded textual repository files within one configured root scope.\"\"\"\n\n    _NAME = \"read_repository_file\"\n    _DESCRIPTION = \"Read one bounded textual file below the configured repository root.\"\n\n    def __init__(self, root: ResolvedPath) -> None:\n        \"\"\"Create a read-only Tool scoped to one repository root.\"\"\"\n        self._root = _normalize(root)\n\n    @property\n    def name(self) -> str:\n        \"\"\"Return the local capability label.\"\"\"\n        return self._NAME\n\n    @property\n    def description(self) -> str:\n        \"\"\"Return the provider-neutral capability description.\"\"\"\n        return self._DESCRIPTION\n\n    def validate(self, arguments: ResolvedPath) -> None:\n        \"\"\"Reject paths outside this Tool's configured semantic scope.\"\"\"\n        normalized_arguments = _normalize(arguments)\n\n        if normalized_arguments.value.is_relative_to(self._root.value):\n            return\n\n        msg = f\"Path is outside the configured repository root: {arguments}.\"\n        raise ToolInputError(msg)\n\n    async def execute(self, arguments: ResolvedPath) -> File:\n        \"\"\"Read inferred structured formats or arbitrary decodable repository text.\"\"\"\n        path = _normalize(arguments)\n        try:\n            resolve_file_format(path)\n        except FileFormatError:\n            return read(path, file_format=FileFormat.TEXT)\n        return read(path)\n",
        "resource": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "start": 636,
        "start_line": 28
      }
    ]
  },
  {
    "address": "tests/context/repository/test_observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "packet_ordinal": 408
    },
    "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "semantic_rationale": "Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_resource_bound_is_passed_to_canonical_text_read(tmp_path: Path) -> None:\n    \"\"\"An oversized required resource prevents snapshot publication.\"\"\"\n    (tmp_path / \"module.py\").write_text(\"12345\", encoding=\"utf-8\")\n    with pytest.raises(FileTooLargeError):\n        observe_repository_resource(\n            repository=_repository(),\n            root=ResolvedPath(tmp_path),\n            address=RepositoryResourceAddress(\"module.py\"),\n            maximum_resource_bytes=4,\n        )\n\n\ndef test_required_multi_resource_failure_does_not_publish_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A missing required member fails the whole bounded observation operation.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n\n    with pytest.raises(FilesystemNotFoundError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"missing.py\")\n\n\ndef test_unsupported_and_undecodable_multi_resources_prevent_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Every requested member must be a decodable regular UTF-8 text file.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    (tmp_path / \"directory\").mkdir()\n    (tmp_path / \"undecodable.py\").write_bytes(b\"\\xff\")\n\n    with pytest.raises(NotAFileError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"directory\")\n    with pytest.raises(TextDecodingError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"undecodable.py\")\n\n\ndef test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 12319,
        "start_line": 348
      }
    ]
  },
  {
    "address": "tests/context/repository/test_observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "packet_ordinal": 408
    },
    "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "semantic_rationale": "Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_resource_bound_is_passed_to_canonical_text_read(tmp_path: Path) -> None:\n    \"\"\"An oversized required resource prevents snapshot publication.\"\"\"\n    (tmp_path / \"module.py\").write_text(\"12345\", encoding=\"utf-8\")\n    with pytest.raises(FileTooLargeError):\n        observe_repository_resource(\n            repository=_repository(),\n            root=ResolvedPath(tmp_path),\n            address=RepositoryResourceAddress(\"module.py\"),\n            maximum_resource_bytes=4,\n        )\n\n\ndef test_required_multi_resource_failure_does_not_publish_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A missing required member fails the whole bounded observation operation.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n\n    with pytest.raises(FilesystemNotFoundError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"missing.py\")\n\n\ndef test_unsupported_and_undecodable_multi_resources_prevent_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Every requested member must be a decodable regular UTF-8 text file.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    (tmp_path / \"directory\").mkdir()\n    (tmp_path / \"undecodable.py\").write_bytes(b\"\\xff\")\n\n    with pytest.raises(NotAFileError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"directory\")\n    with pytest.raises(TextDecodingError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"undecodable.py\")\n\n\ndef test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 12319,
        "start_line": 348
      }
    ]
  },
  {
    "address": "tests/context/repository/test_observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "packet_ordinal": 408
    },
    "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "semantic_rationale": "Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_resource_bound_is_passed_to_canonical_text_read(tmp_path: Path) -> None:\n    \"\"\"An oversized required resource prevents snapshot publication.\"\"\"\n    (tmp_path / \"module.py\").write_text(\"12345\", encoding=\"utf-8\")\n    with pytest.raises(FileTooLargeError):\n        observe_repository_resource(\n            repository=_repository(),\n            root=ResolvedPath(tmp_path),\n            address=RepositoryResourceAddress(\"module.py\"),\n            maximum_resource_bytes=4,\n        )\n\n\ndef test_required_multi_resource_failure_does_not_publish_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A missing required member fails the whole bounded observation operation.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n\n    with pytest.raises(FilesystemNotFoundError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"missing.py\")\n\n\ndef test_unsupported_and_undecodable_multi_resources_prevent_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Every requested member must be a decodable regular UTF-8 text file.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    (tmp_path / \"directory\").mkdir()\n    (tmp_path / \"undecodable.py\").write_bytes(b\"\\xff\")\n\n    with pytest.raises(NotAFileError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"directory\")\n    with pytest.raises(TextDecodingError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"undecodable.py\")\n\n\ndef test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 12319,
        "start_line": 348
      }
    ]
  },
  {
    "address": "tests/context/repository/test_observation.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "packet_ordinal": 408
    },
    "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "semantic_rationale": "Provides caller-level failure propagation examples and a current injection seam. Its indispensable regression migration belongs to preservation of existing callers/profile in O6.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_resource_bound_is_passed_to_canonical_text_read(tmp_path: Path) -> None:\n    \"\"\"An oversized required resource prevents snapshot publication.\"\"\"\n    (tmp_path / \"module.py\").write_text(\"12345\", encoding=\"utf-8\")\n    with pytest.raises(FileTooLargeError):\n        observe_repository_resource(\n            repository=_repository(),\n            root=ResolvedPath(tmp_path),\n            address=RepositoryResourceAddress(\"module.py\"),\n            maximum_resource_bytes=4,\n        )\n\n\ndef test_required_multi_resource_failure_does_not_publish_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A missing required member fails the whole bounded observation operation.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n\n    with pytest.raises(FilesystemNotFoundError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"missing.py\")\n\n\ndef test_unsupported_and_undecodable_multi_resources_prevent_a_snapshot(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Every requested member must be a decodable regular UTF-8 text file.\"\"\"\n    (tmp_path / \"available.py\").write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    (tmp_path / \"directory\").mkdir()\n    (tmp_path / \"undecodable.py\").write_bytes(b\"\\xff\")\n\n    with pytest.raises(NotAFileError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"directory\")\n    with pytest.raises(TextDecodingError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"undecodable.py\")\n\n\ndef test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 12319,
        "start_line": 348
      }
    ]
  },
  {
    "address": "tests/context/repository/test_observation.py",
    "inferability_rationale": "The tests call the existing observation API with its finite default. The full fixture setup at lines 31-65 establishes that context. Adaptation preserves caller semantics, not production caller behavior changes.",
    "label": "REQUIRED",
    "obligation": "O6",
    "provenance": {
      "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "packet_ordinal": 408
    },
    "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R07: Without this information the finite acquisition change can invalidate existing caller regressions even if all filesystem tests are corrected.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 1755,
        "end_line": 65,
        "quote": "_REPOSITORY_ID = \"00000000-0000-4000-8000-000000000001\"\n_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024\n\n\ndef _repository() -> Repository:\n    \"\"\"Return one deterministic logical Repository.\"\"\"\n    return Repository(RepositoryId.parse(_REPOSITORY_ID))\n\n\ndef _observe(\n    repository: Repository,\n    root: Path,\n    address: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe one fixture resource through the public boundary.\"\"\"\n    return observe_repository_resource(\n        repository=repository,\n        root=ResolvedPath(root),\n        address=RepositoryResourceAddress(address),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n\n\ndef _observe_many(\n    repository: Repository,\n    root: Path,\n    *addresses: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe an explicit fixture resource collection through the public boundary.\"\"\"\n    return observe_repository_resources(\n        repository=repository,\n        root=ResolvedPath(root),\n        addresses=tuple(RepositoryResourceAddress(value) for value in addresses),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 672,
        "start_line": 31
      },
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 13790,
        "start_line": 384
      },
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 17514,
        "end_line": 497,
        "quote": "def test_unreadable_and_undecodable_resources_do_not_produce_snapshots(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Read and UTF-8 decoding failures remain unsuccessful observations.\"\"\"\n    source = tmp_path / \"module.py\"\n    source.write_bytes(b\"content\")\n\n    def deny_read(_path: Path) -> bytes:\n        msg = \"denied\"\n        raise PermissionError(msg)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n    with pytest.raises(FilesystemPermissionError):\n        _observe(_repository(), tmp_path, \"module.py\")\n\n    monkeypatch.undo()\n    source.write_bytes(b\"\\xff\")\n    with pytest.raises(TextDecodingError):\n        _observe(_repository(), tmp_path, \"module.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 16810,
        "start_line": 478
      }
    ]
  },
  {
    "address": "tests/core/paths/test_resolved_path.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "73a33d57bf507dd3c4406a1c4b537fb7322222ff13f5c9366c74743403f9e767",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
      "packet_ordinal": 433
    },
    "resource": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
    "semantic_rationale": "Supplies path wrapper construction examples for controlled fixtures, duplicating established ResolvedPath semantics.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/core/paths/test_resolved_path.py",
        "end": 1753,
        "end_line": 54,
        "quote": "def test_constructs_from_an_absolute_path(tmp_path: Path) -> None:\n    \"\"\"An absolute path is retained unchanged.\"\"\"\n    path = tmp_path / \"example.txt\"\n\n    resolved_path = ResolvedPath(path)\n\n    assert resolved_path.value == path\n\n\ndef test_rejects_a_relative_path() -> None:\n    \"\"\"A relative path violates the value object's invariant.\"\"\"\n    with pytest.raises(ValueError, match=\"requires an absolute path\"):\n        ResolvedPath(Path(\"relative.txt\"))\n\n\ndef test_is_immutable(tmp_path: Path) -> None:\n    \"\"\"The stored path cannot be reassigned.\"\"\"\n    resolved_path = ResolvedPath(tmp_path)\n    attribute = \"value\"\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(resolved_path, attribute, tmp_path.parent)\n\n\ndef test_exposes_path_metadata_and_representations(tmp_path: Path) -> None:\n    \"\"\"Path metadata and string forms delegate to the stored path.\"\"\"\n    path = tmp_path / \"directory\" / \"archive.tar.gz\"\n    resolved_path = ResolvedPath(path)\n\n    assert resolved_path.value == path\n    assert resolved_path.name == \"archive.tar.gz\"\n    assert resolved_path.stem == \"archive.tar\"\n    assert resolved_path.suffix == \".gz\"\n    assert resolved_path.suffixes == (\".tar\", \".gz\")\n    assert resolved_path.parent == path.parent\n    assert resolved_path.parts == path.parts\n    assert resolved_path.as_posix() == path.as_posix()\n    assert resolved_path.as_uri() == path.as_uri()\n    assert str(resolved_path) == str(path)\n    assert os.fspath(resolved_path) == os.fspath(path)\n",
        "resource": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
        "start": 259,
        "start_line": 15
      }
    ]
  },
  {
    "address": "tests/core/paths/test_resolved_path.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "73a33d57bf507dd3c4406a1c4b537fb7322222ff13f5c9366c74743403f9e767",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
      "packet_ordinal": 433
    },
    "resource": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
    "semantic_rationale": "Supplies path wrapper construction examples for controlled fixtures, duplicating established ResolvedPath semantics.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/core/paths/test_resolved_path.py",
        "end": 1753,
        "end_line": 54,
        "quote": "def test_constructs_from_an_absolute_path(tmp_path: Path) -> None:\n    \"\"\"An absolute path is retained unchanged.\"\"\"\n    path = tmp_path / \"example.txt\"\n\n    resolved_path = ResolvedPath(path)\n\n    assert resolved_path.value == path\n\n\ndef test_rejects_a_relative_path() -> None:\n    \"\"\"A relative path violates the value object's invariant.\"\"\"\n    with pytest.raises(ValueError, match=\"requires an absolute path\"):\n        ResolvedPath(Path(\"relative.txt\"))\n\n\ndef test_is_immutable(tmp_path: Path) -> None:\n    \"\"\"The stored path cannot be reassigned.\"\"\"\n    resolved_path = ResolvedPath(tmp_path)\n    attribute = \"value\"\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(resolved_path, attribute, tmp_path.parent)\n\n\ndef test_exposes_path_metadata_and_representations(tmp_path: Path) -> None:\n    \"\"\"Path metadata and string forms delegate to the stored path.\"\"\"\n    path = tmp_path / \"directory\" / \"archive.tar.gz\"\n    resolved_path = ResolvedPath(path)\n\n    assert resolved_path.value == path\n    assert resolved_path.name == \"archive.tar.gz\"\n    assert resolved_path.stem == \"archive.tar\"\n    assert resolved_path.suffix == \".gz\"\n    assert resolved_path.suffixes == (\".tar\", \".gz\")\n    assert resolved_path.parent == path.parent\n    assert resolved_path.parts == path.parts\n    assert resolved_path.as_posix() == path.as_posix()\n    assert resolved_path.as_uri() == path.as_uri()\n    assert str(resolved_path) == str(path)\n    assert os.fspath(resolved_path) == os.fspath(path)\n",
        "resource": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
        "start": 259,
        "start_line": 15
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "packet_ordinal": 482
    },
    "resource": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "end": 2391,
        "end_line": 80,
        "quote": "def test_decode_preserves_metadata_and_parses_quoted_csv(tmp_path: Path) -> None:\n    \"\"\"Decoded CSV retains exact source provenance and structured string cells.\"\"\"\n    source = 'id,description\\n1,\"contains, delimiter\"\\n2,\"line one\\nline two\"\\n'\n    encoded = source.encode()\n\n    file = CsvCodec().decode(ResolvedPath(tmp_path / \"data.csv\"), encoded)\n\n    assert file.content == source\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert file.headers == (\"id\", \"description\")\n    assert file[0][\"description\"] == \"contains, delimiter\"\n    assert file[1][\"description\"] == \"line one\\nline two\"\n\n\ndef test_decode_supports_alternate_encodings_and_normalizes_errors(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Byte decoding follows the established codec encoding-error contract.\"\"\"\n    codec = CsvCodec()\n    path = ResolvedPath(tmp_path / \"data.csv\")\n    source = \"city\\nM\u00c3\u00bcnchen\\n\"\n\n    file = codec.decode(path, source.encode(\"utf-16\"), encoding=\"utf-16\")\n\n    assert file.encoding == \"utf-16\"\n    assert file[0][\"city\"] == \"M\u00c3\u00bcnchen\"\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"city\\n\", encoding=\"unknown-codec\")\n\n\n@pytest.mark.parametrize(\n    (\"source\", \"match\"),\n    [\n        (\"\", \"header row\"),\n        (\"\\n\", \"header row\"),\n        (\"id,id\\n1,2\\n\", \"unique\"),\n        (\",name\\n1,Ada\\n\", \"blank\"),\n        (\"id,name\\n1\\n\", \"values\"),\n        ('\"unterminated', \"Invalid CSV\"),\n        ('id,name\\n1,\"unterminated', \"Invalid CSV\"),\n    ],\n)\ndef test_parse_rejects_invalid_header_based_source(\n    tmp_path: Path,\n    source: str,\n    match: str,\n) -> None:\n    \"\"\"Headerless, ambiguous, ragged, and malformed CSV cannot form a model.\"\"\"\n    with pytest.raises(FileFormatError, match=match):\n        CsvCodec().parse(ResolvedPath(tmp_path / \"invalid.csv\"), source)\n",
        "resource": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "start": 445,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_csv.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "packet_ordinal": 482
    },
    "resource": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "end": 2391,
        "end_line": 80,
        "quote": "def test_decode_preserves_metadata_and_parses_quoted_csv(tmp_path: Path) -> None:\n    \"\"\"Decoded CSV retains exact source provenance and structured string cells.\"\"\"\n    source = 'id,description\\n1,\"contains, delimiter\"\\n2,\"line one\\nline two\"\\n'\n    encoded = source.encode()\n\n    file = CsvCodec().decode(ResolvedPath(tmp_path / \"data.csv\"), encoded)\n\n    assert file.content == source\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert file.headers == (\"id\", \"description\")\n    assert file[0][\"description\"] == \"contains, delimiter\"\n    assert file[1][\"description\"] == \"line one\\nline two\"\n\n\ndef test_decode_supports_alternate_encodings_and_normalizes_errors(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Byte decoding follows the established codec encoding-error contract.\"\"\"\n    codec = CsvCodec()\n    path = ResolvedPath(tmp_path / \"data.csv\")\n    source = \"city\\nM\u00c3\u00bcnchen\\n\"\n\n    file = codec.decode(path, source.encode(\"utf-16\"), encoding=\"utf-16\")\n\n    assert file.encoding == \"utf-16\"\n    assert file[0][\"city\"] == \"M\u00c3\u00bcnchen\"\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"city\\n\", encoding=\"unknown-codec\")\n\n\n@pytest.mark.parametrize(\n    (\"source\", \"match\"),\n    [\n        (\"\", \"header row\"),\n        (\"\\n\", \"header row\"),\n        (\"id,id\\n1,2\\n\", \"unique\"),\n        (\",name\\n1,Ada\\n\", \"blank\"),\n        (\"id,name\\n1\\n\", \"values\"),\n        ('\"unterminated', \"Invalid CSV\"),\n        ('id,name\\n1,\"unterminated', \"Invalid CSV\"),\n    ],\n)\ndef test_parse_rejects_invalid_header_based_source(\n    tmp_path: Path,\n    source: str,\n    match: str,\n) -> None:\n    \"\"\"Headerless, ambiguous, ragged, and malformed CSV cannot form a model.\"\"\"\n    with pytest.raises(FileFormatError, match=match):\n        CsvCodec().parse(ResolvedPath(tmp_path / \"invalid.csv\"), source)\n",
        "resource": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "start": 445,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_json.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "packet_ordinal": 483
    },
    "resource": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "end": 3287,
        "end_line": 110,
        "quote": "def test_decode_preserves_utf8_source_metadata_and_immutable_object(\n    tmp_path: Path,\n) -> None:\n    \"\"\"UTF-8 decoding preserves source provenance and freezes nested values.\"\"\"\n    codec = JsonCodec()\n    source = '{\"name\":\"Jos\u00e9\",\"items\":[{\"active\":true}]}'\n    encoded = source.encode()\n\n    file = codec.decode(ResolvedPath(tmp_path), encoded)\n\n    assert isinstance(file, JsonObjectFile)\n    assert file.content == source\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert isinstance(file[\"items\"], tuple)\n    nested = file[\"items\"][0]\n    assert isinstance(nested, Mapping)\n\n    with pytest.raises(TypeError):\n        cast(\"dict[str, object]\", nested)[\"changed\"] = True\n\n\ndef test_decode_supports_alternate_encodings_and_rejects_invalid_bytes(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Decode honors explicit encoding and wraps invalid encoded source bytes.\"\"\"\n    codec = JsonCodec()\n    source = '{\"city\":\"M\u00fcnchen\"}'\n    utf16 = source.encode(\"utf-16\")\n\n    file = codec.decode(ResolvedPath(tmp_path), utf16, encoding=\"utf-16\")\n\n    assert isinstance(file, JsonObjectFile)\n    assert file.content == source\n    assert file.encoding == \"utf-16\"\n    assert file.byte_size == len(utf16)\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(ResolvedPath(tmp_path), b\"\\xff\")\n\n\n@pytest.mark.parametrize(\n    (\"source\", \"model_type\", \"expected_value\"),\n    [\n        (\"{}\", JsonObjectFile, {}),\n        (\"[]\", JsonListFile, ()),\n        ('\"hello\"', JsonScalarFile, \"hello\"),\n        (\"42\", JsonScalarFile, 42),\n        (\"4.5\", JsonScalarFile, 4.5),\n        (\"true\", JsonScalarFile, True),\n        (\"null\", JsonScalarFile, None),\n    ],\n)\ndef test_parse_selects_the_correct_concrete_root_model(\n    tmp_path: Path,\n    source: str,\n    model_type: type[JsonFile],\n    expected_value: object,\n) -> None:\n    \"\"\"JSON root types resolve to their concrete immutable model classes.\"\"\"\n    file = JsonCodec().parse(ResolvedPath(tmp_path), source)\n\n    assert isinstance(file, model_type)\n    assert isinstance(file, JsonObjectFile | JsonListFile | JsonScalarFile)\n    assert file.value == expected_value\n\n\ndef test_parse_derives_byte_size_and_wraps_parse_and_encoding_errors(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Parsing derives source size and preserves useful domain-level failures.\"\"\"\n    codec = JsonCodec()\n    source = '\"\u00e9\"'\n    file = codec.parse(ResolvedPath(tmp_path), source)\n\n    assert file.byte_size == len(source.encode())\n\n    with pytest.raises(FileFormatError, match=\"line 1, column\") as malformed:\n        codec.parse(ResolvedPath(tmp_path), \"{\")\n\n    assert malformed.value.__cause__ is not None\n\n    with pytest.raises(FileFormatError, match=\"Invalid JSON constant\"):\n        codec.parse(ResolvedPath(tmp_path), \"NaN\")\n",
        "resource": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "start": 491,
        "start_line": 27
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_json.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "packet_ordinal": 483
    },
    "resource": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "end": 3287,
        "end_line": 110,
        "quote": "def test_decode_preserves_utf8_source_metadata_and_immutable_object(\n    tmp_path: Path,\n) -> None:\n    \"\"\"UTF-8 decoding preserves source provenance and freezes nested values.\"\"\"\n    codec = JsonCodec()\n    source = '{\"name\":\"Jos\u00e9\",\"items\":[{\"active\":true}]}'\n    encoded = source.encode()\n\n    file = codec.decode(ResolvedPath(tmp_path), encoded)\n\n    assert isinstance(file, JsonObjectFile)\n    assert file.content == source\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert isinstance(file[\"items\"], tuple)\n    nested = file[\"items\"][0]\n    assert isinstance(nested, Mapping)\n\n    with pytest.raises(TypeError):\n        cast(\"dict[str, object]\", nested)[\"changed\"] = True\n\n\ndef test_decode_supports_alternate_encodings_and_rejects_invalid_bytes(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Decode honors explicit encoding and wraps invalid encoded source bytes.\"\"\"\n    codec = JsonCodec()\n    source = '{\"city\":\"M\u00fcnchen\"}'\n    utf16 = source.encode(\"utf-16\")\n\n    file = codec.decode(ResolvedPath(tmp_path), utf16, encoding=\"utf-16\")\n\n    assert isinstance(file, JsonObjectFile)\n    assert file.content == source\n    assert file.encoding == \"utf-16\"\n    assert file.byte_size == len(utf16)\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(ResolvedPath(tmp_path), b\"\\xff\")\n\n\n@pytest.mark.parametrize(\n    (\"source\", \"model_type\", \"expected_value\"),\n    [\n        (\"{}\", JsonObjectFile, {}),\n        (\"[]\", JsonListFile, ()),\n        ('\"hello\"', JsonScalarFile, \"hello\"),\n        (\"42\", JsonScalarFile, 42),\n        (\"4.5\", JsonScalarFile, 4.5),\n        (\"true\", JsonScalarFile, True),\n        (\"null\", JsonScalarFile, None),\n    ],\n)\ndef test_parse_selects_the_correct_concrete_root_model(\n    tmp_path: Path,\n    source: str,\n    model_type: type[JsonFile],\n    expected_value: object,\n) -> None:\n    \"\"\"JSON root types resolve to their concrete immutable model classes.\"\"\"\n    file = JsonCodec().parse(ResolvedPath(tmp_path), source)\n\n    assert isinstance(file, model_type)\n    assert isinstance(file, JsonObjectFile | JsonListFile | JsonScalarFile)\n    assert file.value == expected_value\n\n\ndef test_parse_derives_byte_size_and_wraps_parse_and_encoding_errors(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Parsing derives source size and preserves useful domain-level failures.\"\"\"\n    codec = JsonCodec()\n    source = '\"\u00e9\"'\n    file = codec.parse(ResolvedPath(tmp_path), source)\n\n    assert file.byte_size == len(source.encode())\n\n    with pytest.raises(FileFormatError, match=\"line 1, column\") as malformed:\n        codec.parse(ResolvedPath(tmp_path), \"{\")\n\n    assert malformed.value.__cause__ is not None\n\n    with pytest.raises(FileFormatError, match=\"Invalid JSON constant\"):\n        codec.parse(ResolvedPath(tmp_path), \"NaN\")\n",
        "resource": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "start": 491,
        "start_line": 27
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_markdown.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "packet_ordinal": 484
    },
    "resource": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "end": 1499,
        "end_line": 57,
        "quote": "@pytest.mark.parametrize(\n    (\"source\", \"encoding\"),\n    [\n        (\"# Title\\n\", \"utf-8\"),\n        (\"# Caf\u00c3\u00a9\\r\\n\", \"utf-8\"),\n        (\"## M\u00c3\u00bcnchen\\n\", \"utf-16\"),\n    ],\n)\ndef test_decode_preserves_exact_markdown_source_and_metadata(\n    tmp_path: Path,\n    source: str,\n    encoding: str,\n) -> None:\n    \"\"\"Decoding keeps Markdown source verbatim for structural interpretation.\"\"\"\n    content = source.encode(encoding)\n\n    file = MarkdownCodec().decode(\n        ResolvedPath(tmp_path / \"document.md\"),\n        content,\n        encoding=encoding,\n    )\n\n    assert file.content == source\n    assert file.encoding == encoding\n    assert file.byte_size == len(content)\n\n\ndef test_markdown_codec_normalizes_decoding_failures(tmp_path: Path) -> None:\n    \"\"\"Invalid bytes and unknown codecs use the established filesystem errors.\"\"\"\n    codec = MarkdownCodec()\n    path = ResolvedPath(tmp_path / \"document.md\")\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"# Title\", encoding=\"unknown-codec\")\n",
        "resource": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "start": 364,
        "start_line": 21
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_markdown.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "packet_ordinal": 484
    },
    "resource": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "end": 1499,
        "end_line": 57,
        "quote": "@pytest.mark.parametrize(\n    (\"source\", \"encoding\"),\n    [\n        (\"# Title\\n\", \"utf-8\"),\n        (\"# Caf\u00c3\u00a9\\r\\n\", \"utf-8\"),\n        (\"## M\u00c3\u00bcnchen\\n\", \"utf-16\"),\n    ],\n)\ndef test_decode_preserves_exact_markdown_source_and_metadata(\n    tmp_path: Path,\n    source: str,\n    encoding: str,\n) -> None:\n    \"\"\"Decoding keeps Markdown source verbatim for structural interpretation.\"\"\"\n    content = source.encode(encoding)\n\n    file = MarkdownCodec().decode(\n        ResolvedPath(tmp_path / \"document.md\"),\n        content,\n        encoding=encoding,\n    )\n\n    assert file.content == source\n    assert file.encoding == encoding\n    assert file.byte_size == len(content)\n\n\ndef test_markdown_codec_normalizes_decoding_failures(tmp_path: Path) -> None:\n    \"\"\"Invalid bytes and unknown codecs use the established filesystem errors.\"\"\"\n    codec = MarkdownCodec()\n    path = ResolvedPath(tmp_path / \"document.md\")\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"# Title\", encoding=\"unknown-codec\")\n",
        "resource": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "start": 364,
        "start_line": 21
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
      "packet_ordinal": 485
    },
    "resource": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "end": 2170,
        "end_line": 77,
        "quote": "@pytest.mark.parametrize(\n    (\"source\", \"encoding\"),\n    [\n        (\"\", \"utf-8\"),\n        (\"first\\r\\nsecond\\n\", \"utf-8\"),\n        (\"caf\u00c3\u00a9\", \"utf-8\"),\n        (\"M\u00c3\u00bcnchen\", \"utf-16\"),\n    ],\n)\ndef test_decode_preserves_exact_text_and_source_metadata(\n    tmp_path: Path,\n    source: str,\n    encoding: str,\n) -> None:\n    \"\"\"Decoding retains text verbatim, including whitespace and newlines.\"\"\"\n    content = source.encode(encoding)\n\n    file = TextCodec().decode(\n        ResolvedPath(tmp_path / \"source.txt\"),\n        content,\n        encoding=encoding,\n    )\n\n    assert file.content == source\n    assert file.encoding == encoding\n    assert file.byte_size == len(content)\n\n\ndef test_decode_normalizes_unknown_encodings_and_invalid_bytes(tmp_path: Path) -> None:\n    \"\"\"Text decoding exposes stable domain failures rather than codec details.\"\"\"\n    codec = TextCodec()\n    path = ResolvedPath(tmp_path / \"source.txt\")\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"text\", encoding=\"unknown-codec\")\n\n\ndef test_codec_created_text_files_retain_rich_source_operations(tmp_path: Path) -> None:\n    \"\"\"Codec output remains a full text model without implicit iteration.\"\"\"\n    file = TextCodec().decode(\n        ResolvedPath(tmp_path / \"source.txt\"),\n        b\"alpha\\nbeta\\n\",\n    )\n\n    assert file.lines == (\"alpha\", \"beta\")\n    expected_line_count = 2\n    assert file.line_count == expected_line_count\n    assert file.character_count == len(\"alpha\\nbeta\\n\")\n    assert file.contains(\"pha\") is True\n    assert file.search_regex(r\"b.ta\") is not None\n    assert tuple(match.value for match in file.find_all_regex(r\"[a-z]+\")) == (\n        \"alpha\",\n        \"beta\",\n    )\n",
        "resource": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "start": 362,
        "start_line": 21
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/codecs/test_text.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
      "packet_ordinal": 485
    },
    "resource": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "end": 2170,
        "end_line": 77,
        "quote": "@pytest.mark.parametrize(\n    (\"source\", \"encoding\"),\n    [\n        (\"\", \"utf-8\"),\n        (\"first\\r\\nsecond\\n\", \"utf-8\"),\n        (\"caf\u00c3\u00a9\", \"utf-8\"),\n        (\"M\u00c3\u00bcnchen\", \"utf-16\"),\n    ],\n)\ndef test_decode_preserves_exact_text_and_source_metadata(\n    tmp_path: Path,\n    source: str,\n    encoding: str,\n) -> None:\n    \"\"\"Decoding retains text verbatim, including whitespace and newlines.\"\"\"\n    content = source.encode(encoding)\n\n    file = TextCodec().decode(\n        ResolvedPath(tmp_path / \"source.txt\"),\n        content,\n        encoding=encoding,\n    )\n\n    assert file.content == source\n    assert file.encoding == encoding\n    assert file.byte_size == len(content)\n\n\ndef test_decode_normalizes_unknown_encodings_and_invalid_bytes(tmp_path: Path) -> None:\n    \"\"\"Text decoding exposes stable domain failures rather than codec details.\"\"\"\n    codec = TextCodec()\n    path = ResolvedPath(tmp_path / \"source.txt\")\n\n    with pytest.raises(TextDecodingError, match=\"utf-8\"):\n        codec.decode(path, b\"\\xff\")\n\n    with pytest.raises(TextDecodingError, match=\"unknown-codec\"):\n        codec.decode(path, b\"text\", encoding=\"unknown-codec\")\n\n\ndef test_codec_created_text_files_retain_rich_source_operations(tmp_path: Path) -> None:\n    \"\"\"Codec output remains a full text model without implicit iteration.\"\"\"\n    file = TextCodec().decode(\n        ResolvedPath(tmp_path / \"source.txt\"),\n        b\"alpha\\nbeta\\n\",\n    )\n\n    assert file.lines == (\"alpha\", \"beta\")\n    expected_line_count = 2\n    assert file.line_count == expected_line_count\n    assert file.character_count == len(\"alpha\\nbeta\\n\")\n    assert file.contains(\"pha\") is True\n    assert file.search_regex(r\"b.ta\") is not None\n    assert tuple(match.value for match in file.find_all_regex(r\"[a-z]+\")) == (\n        \"alpha\",\n        \"beta\",\n    )\n",
        "resource": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "start": 362,
        "start_line": 21
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_models.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "packet_ordinal": 497
    },
    "resource": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_models.py",
        "end": 2350,
        "end_line": 79,
        "quote": "def test_file_models_expose_their_format_and_value_semantics(tmp_path: Path) -> None:\n    \"\"\"Concrete file models retain their path and format identity.\"\"\"\n    path = ResolvedPath(tmp_path / \"example.txt\")\n    binary = BinaryFile(path, b\"abc\")\n    expected_size = len(b\"abc\")\n\n    assert binary.format is FileFormat.BINARY\n    assert binary.size_bytes == expected_size\n    assert binary == BinaryFile(path, b\"abc\")\n    assert TextFile(path, \"text\").format is FileFormat.TEXT\n    assert (\n        CsvFile(\n            path,\n            \"a,b\",\n            headers=(\"a\", \"b\"),\n            rows=(CsvRow((\"a\", \"b\"), (\"1\", \"2\")),),\n        ).format\n        is FileFormat.CSV\n    )\n    assert MarkdownFile(path, \"# Title\").format is FileFormat.MARKDOWN\n    assert JsonFile(path, \"{}\").format is FileFormat.JSON\n\n\n@pytest.mark.parametrize(\n    (\"encoding\", \"byte_size\", \"match\"),\n    [(\"\", 0, \"encoding\"), (\"utf-8\", -1, \"byte size\")],\n)\ndef test_text_file_rejects_invalid_metadata(\n    tmp_path: Path,\n    encoding: str,\n    byte_size: int,\n    match: str,\n) -> None:\n    \"\"\"Text metadata requires a non-blank encoding and non-negative byte size.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        TextFile(ResolvedPath(tmp_path), \"text\", encoding, byte_size)\n\n\ndef test_text_file_exposes_explicit_line_literal_and_regex_operations(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Text files provide deterministic source-text access without iteration.\"\"\"\n    text = TextFile(ResolvedPath(tmp_path), \"alpha\\nbeta\\n\")\n    expected_line_count = len((\"alpha\", \"beta\"))\n\n    assert text.lines == (\"alpha\", \"beta\")\n    assert text.line_count == expected_line_count\n    assert text.character_count == len(\"alpha\\nbeta\\n\")\n    assert text.contains(\"pha\") is True\n    assert text.contains(\"missing\") is False\n    assert text.search_regex(r\"b.ta\") is not None\n    assert tuple(match.value for match in text.find_all_regex(r\"[a-z]+\")) == (\n        \"alpha\",\n        \"beta\",\n    )\n",
        "resource": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "start": 391,
        "start_line": 25
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_models.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "packet_ordinal": 497
    },
    "resource": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
    "semantic_rationale": "Current codec/model regressions corroborate source and metadata behavior and provide useful assertion patterns; future expected behavior is specified by the task and no acquisition-specific fixture here must be migrated.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_models.py",
        "end": 2350,
        "end_line": 79,
        "quote": "def test_file_models_expose_their_format_and_value_semantics(tmp_path: Path) -> None:\n    \"\"\"Concrete file models retain their path and format identity.\"\"\"\n    path = ResolvedPath(tmp_path / \"example.txt\")\n    binary = BinaryFile(path, b\"abc\")\n    expected_size = len(b\"abc\")\n\n    assert binary.format is FileFormat.BINARY\n    assert binary.size_bytes == expected_size\n    assert binary == BinaryFile(path, b\"abc\")\n    assert TextFile(path, \"text\").format is FileFormat.TEXT\n    assert (\n        CsvFile(\n            path,\n            \"a,b\",\n            headers=(\"a\", \"b\"),\n            rows=(CsvRow((\"a\", \"b\"), (\"1\", \"2\")),),\n        ).format\n        is FileFormat.CSV\n    )\n    assert MarkdownFile(path, \"# Title\").format is FileFormat.MARKDOWN\n    assert JsonFile(path, \"{}\").format is FileFormat.JSON\n\n\n@pytest.mark.parametrize(\n    (\"encoding\", \"byte_size\", \"match\"),\n    [(\"\", 0, \"encoding\"), (\"utf-8\", -1, \"byte size\")],\n)\ndef test_text_file_rejects_invalid_metadata(\n    tmp_path: Path,\n    encoding: str,\n    byte_size: int,\n    match: str,\n) -> None:\n    \"\"\"Text metadata requires a non-blank encoding and non-negative byte size.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        TextFile(ResolvedPath(tmp_path), \"text\", encoding, byte_size)\n\n\ndef test_text_file_exposes_explicit_line_literal_and_regex_operations(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Text files provide deterministic source-text access without iteration.\"\"\"\n    text = TextFile(ResolvedPath(tmp_path), \"alpha\\nbeta\\n\")\n    expected_line_count = len((\"alpha\", \"beta\"))\n\n    assert text.lines == (\"alpha\", \"beta\")\n    assert text.line_count == expected_line_count\n    assert text.character_count == len(\"alpha\\nbeta\\n\")\n    assert text.contains(\"pha\") is True\n    assert text.contains(\"missing\") is False\n    assert text.search_regex(r\"b.ta\") is not None\n    assert tuple(match.value for match in text.find_all_regex(r\"[a-z]+\")) == (\n        \"alpha\",\n        \"beta\",\n    )\n",
        "resource": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "start": 391,
        "start_line": 25
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "packet_ordinal": 498
    },
    "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "semantic_rationale": "Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rejects_missing_paths_and_directories(tmp_path: Path) -> None:\n    \"\"\"Generic reading accepts existing regular files only.\"\"\"\n    with pytest.raises(FilesystemNotFoundError, match=\"does not exist\"):\n        read(ResolvedPath(tmp_path / \"missing.json\"))\n\n    with pytest.raises(NotAFileError, match=\"not a regular file\"):\n        read(ResolvedPath(tmp_path))\n\n\ndef test_read_enforces_configured_size_limits(tmp_path: Path) -> None:\n    \"\"\"Bounded reads reject oversized files but accept an exact boundary.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    assert isinstance(read(ResolvedPath(source), max_bytes=2), JsonObjectFile)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=1)\n\n    with pytest.raises(ValueError, match=\"cannot be negative\"):\n        read(ResolvedPath(source), max_bytes=-1)\n\n\ndef test_read_supports_an_explicitly_unbounded_limit(tmp_path: Path) -> None:\n    \"\"\"A ``None`` limit opts into an unbounded complete read.\"\"\"\n    source = tmp_path / \"large.json\"\n    source.write_bytes(b'\"' + (b\"a\" * (DEFAULT_MAX_READ_BYTES + 1)) + b'\"')\n\n    file = read(ResolvedPath(source), max_bytes=None)\n\n    assert isinstance(file, JsonScalarFile)\n    assert file.character_count == DEFAULT_MAX_READ_BYTES + 3\n\n\ndef test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 4742,
        "start_line": 148
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "packet_ordinal": 498
    },
    "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "semantic_rationale": "Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rejects_missing_paths_and_directories(tmp_path: Path) -> None:\n    \"\"\"Generic reading accepts existing regular files only.\"\"\"\n    with pytest.raises(FilesystemNotFoundError, match=\"does not exist\"):\n        read(ResolvedPath(tmp_path / \"missing.json\"))\n\n    with pytest.raises(NotAFileError, match=\"not a regular file\"):\n        read(ResolvedPath(tmp_path))\n\n\ndef test_read_enforces_configured_size_limits(tmp_path: Path) -> None:\n    \"\"\"Bounded reads reject oversized files but accept an exact boundary.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    assert isinstance(read(ResolvedPath(source), max_bytes=2), JsonObjectFile)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=1)\n\n    with pytest.raises(ValueError, match=\"cannot be negative\"):\n        read(ResolvedPath(source), max_bytes=-1)\n\n\ndef test_read_supports_an_explicitly_unbounded_limit(tmp_path: Path) -> None:\n    \"\"\"A ``None`` limit opts into an unbounded complete read.\"\"\"\n    source = tmp_path / \"large.json\"\n    source.write_bytes(b'\"' + (b\"a\" * (DEFAULT_MAX_READ_BYTES + 1)) + b'\"')\n\n    file = read(ResolvedPath(source), max_bytes=None)\n\n    assert isinstance(file, JsonScalarFile)\n    assert file.character_count == DEFAULT_MAX_READ_BYTES + 3\n\n\ndef test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 4742,
        "start_line": 148
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "packet_ordinal": 498
    },
    "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "semantic_rationale": "Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rejects_missing_paths_and_directories(tmp_path: Path) -> None:\n    \"\"\"Generic reading accepts existing regular files only.\"\"\"\n    with pytest.raises(FilesystemNotFoundError, match=\"does not exist\"):\n        read(ResolvedPath(tmp_path / \"missing.json\"))\n\n    with pytest.raises(NotAFileError, match=\"not a regular file\"):\n        read(ResolvedPath(tmp_path))\n\n\ndef test_read_enforces_configured_size_limits(tmp_path: Path) -> None:\n    \"\"\"Bounded reads reject oversized files but accept an exact boundary.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    assert isinstance(read(ResolvedPath(source), max_bytes=2), JsonObjectFile)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=1)\n\n    with pytest.raises(ValueError, match=\"cannot be negative\"):\n        read(ResolvedPath(source), max_bytes=-1)\n\n\ndef test_read_supports_an_explicitly_unbounded_limit(tmp_path: Path) -> None:\n    \"\"\"A ``None`` limit opts into an unbounded complete read.\"\"\"\n    source = tmp_path / \"large.json\"\n    source.write_bytes(b'\"' + (b\"a\" * (DEFAULT_MAX_READ_BYTES + 1)) + b'\"')\n\n    file = read(ResolvedPath(source), max_bytes=None)\n\n    assert isinstance(file, JsonScalarFile)\n    assert file.character_count == DEFAULT_MAX_READ_BYTES + 3\n\n\ndef test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 4742,
        "start_line": 148
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_reading.py",
    "inferability_rationale": "New instrumented-stream fixture names and decomposition remain free choices. The original tests establish current seams, not the design of future fixtures.",
    "label": "REQUIRED",
    "obligation": "O5",
    "provenance": {
      "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "packet_ordinal": 498
    },
    "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R06: This is a necessary current regression constraint, not a requirement to read a test merely because new tests are requested. Leaving these injections unchanged would stop them exercising the new finite acquisition path.",
    "support_kind": [
      "DIRECT_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 1225,
        "end_line": 50,
        "quote": "@pytest.mark.parametrize(\n    (\"name\", \"content\", \"model_type\"),\n    [\n        (\"object.json\", b'{\"name\":\"Ada\",\"id\":2}', JsonObjectFile),\n        (\"array.JSON\", b'[{\"id\":1}]', JsonListFile),\n        (\"scalar.json\", b\"true\", JsonScalarFile),\n    ],\n)\ndef test_read_returns_the_concrete_json_root_model(\n    tmp_path: Path,\n    name: str,\n    content: bytes,\n    model_type: type[JsonObjectFile | JsonListFile | JsonScalarFile],\n) -> None:\n    \"\"\"Suffix resolution and decoding preserve the rich JSON root type.\"\"\"\n    source = tmp_path / name\n    source.write_bytes(content)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, model_type)\n    assert file.byte_size == len(content)\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 529,
        "start_line": 29
      },
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 4740,
        "end_line": 145,
        "quote": "def test_read_returns_text_models_with_exact_source_behavior(tmp_path: Path) -> None:\n    \"\"\"Text suffix resolution retains bytes, metadata, and text-model operations.\"\"\"\n    source = tmp_path / \"notes.TXT\"\n    content = \"caf\u00c3\u00a9\\r\\nstatus: ready\\n\"\n    encoded = content.encode(\"utf-8\")\n    source.write_bytes(encoded)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, TextFile)\n    assert file.content == content\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert file.contains(\"ready\") is True\n    assert file.search_regex(r\"status: \\w+\") is not None\n\n\ndef test_read_allows_an_explicit_text_override(tmp_path: Path) -> None:\n    \"\"\"Text format overrides bypass unsupported or absent suffix inference.\"\"\"\n    source = tmp_path / \"message.data\"\n    source.write_bytes(b\"hello\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.TEXT)\n\n    assert isinstance(file, TextFile)\n    assert file.content == \"hello\\n\"\n\n\n@pytest.mark.parametrize(\"suffix\", [\".md\", \".MARKDOWN\"])\ndef test_read_returns_rich_markdown_models(tmp_path: Path, suffix: str) -> None:\n    \"\"\"Markdown suffixes decode to structural models with source access intact.\"\"\"\n    source = tmp_path / f\"document{suffix}\"\n    content = \"# Title\\n## Detail\\nText\\n\"\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, MarkdownFile)\n    assert file.content == content\n    assert file.headings[1].text == \"Detail\"\n    assert file.find_section(\"title\") is not None\n    assert file.search_regex(\"Text\") is not None\n\n\ndef test_read_allows_an_explicit_markdown_override(tmp_path: Path) -> None:\n    \"\"\"Markdown overrides bypass suffix inference for source files without a suffix.\"\"\"\n    source = tmp_path / \"readme\"\n    source.write_bytes(b\"# Title\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.MARKDOWN)\n\n    assert isinstance(file, MarkdownFile)\n    assert file.headings[0].text == \"Title\"\n\n\ndef test_read_returns_rich_csv_models(tmp_path: Path) -> None:\n    \"\"\"Mixed-case CSV paths decode to header-addressable immutable row models.\"\"\"\n    source = tmp_path / \"reports.CSV\"\n    content = 'id,status\\nreport-1,passed\\nreport-2,\"needs, review\"\\n'\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, CsvFile)\n    assert file.headers == (\"id\", \"status\")\n    assert file.column(\"status\") == (\"passed\", \"needs, review\")\n    assert file.find_by(\"id\", \"report-2\") == file[1]\n    assert file.search_regex(\"review\") is not None\n\n\ndef test_read_allows_an_explicit_csv_override(tmp_path: Path) -> None:\n    \"\"\"CSV overrides bypass suffix inference for a source without a suffix.\"\"\"\n    source = tmp_path / \"reports\"\n    source.write_bytes(b\"id,status\\nreport-1,passed\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.CSV)\n\n    assert isinstance(file, CsvFile)\n    assert file[0][\"status\"] == \"passed\"\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 1780,
        "start_line": 67
      },
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 6056,
        "start_line": 182
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_reading.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "packet_ordinal": 498
    },
    "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "semantic_rationale": "Current read integration tests corroborate limit/error behavior and require an injection migration already captured under controlled regression work.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rejects_missing_paths_and_directories(tmp_path: Path) -> None:\n    \"\"\"Generic reading accepts existing regular files only.\"\"\"\n    with pytest.raises(FilesystemNotFoundError, match=\"does not exist\"):\n        read(ResolvedPath(tmp_path / \"missing.json\"))\n\n    with pytest.raises(NotAFileError, match=\"not a regular file\"):\n        read(ResolvedPath(tmp_path))\n\n\ndef test_read_enforces_configured_size_limits(tmp_path: Path) -> None:\n    \"\"\"Bounded reads reject oversized files but accept an exact boundary.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    assert isinstance(read(ResolvedPath(source), max_bytes=2), JsonObjectFile)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=1)\n\n    with pytest.raises(ValueError, match=\"cannot be negative\"):\n        read(ResolvedPath(source), max_bytes=-1)\n\n\ndef test_read_supports_an_explicitly_unbounded_limit(tmp_path: Path) -> None:\n    \"\"\"A ``None`` limit opts into an unbounded complete read.\"\"\"\n    source = tmp_path / \"large.json\"\n    source.write_bytes(b'\"' + (b\"a\" * (DEFAULT_MAX_READ_BYTES + 1)) + b'\"')\n\n    file = read(ResolvedPath(source), max_bytes=None)\n\n    assert isinstance(file, JsonScalarFile)\n    assert file.character_count == DEFAULT_MAX_READ_BYTES + 3\n\n\ndef test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 4742,
        "start_line": 148
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_resolution.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "packet_ordinal": 499
    },
    "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "semantic_rationale": "Exercises suffix and codec mappings; it is complementary to the final-suffix documentation when used as a complete resolver alternative.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_resolution.py",
        "end": 1911,
        "end_line": 61,
        "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
        "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "start": 496,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_resolution.py",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O3",
    "provenance": {
      "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "packet_ordinal": 499
    },
    "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "INFERABLE_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_resolution.py",
        "end": 1911,
        "end_line": 61,
        "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
        "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "start": 496,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_resolution.py",
    "inferability_rationale": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "label": "REQUIRED",
    "obligation": "O4",
    "provenance": {
      "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "packet_ordinal": 499
    },
    "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "semantic_rationale": "Necessary in at least one complete minimal witness: R03: Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "support_kind": [
      "INFERABLE_SUPPORT"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_resolution.py",
        "end": 1911,
        "end_line": 61,
        "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
        "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "start": 496,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_resolution.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "packet_ordinal": 499
    },
    "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "semantic_rationale": "Exercises suffix and codec mappings; it is complementary to the final-suffix documentation when used as a complete resolver alternative.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_resolution.py",
        "end": 1911,
        "end_line": 61,
        "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
        "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "start": 496,
        "start_line": 26
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_writing.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "packet_ordinal": 500
    },
    "resource": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
    "semantic_rationale": "Existing atomic-write regression corroborates the unchanged adjacent lifecycle; the read-only acquisition change does not make the write test a required evidence source.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_writing.py",
        "end": 1683,
        "end_line": 59,
        "quote": "def test_write_persists_a_new_json_file_and_fsyncs_before_replacement(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Writing uses a sibling temporary file, fsync, then atomic replacement.\"\"\"\n    target = tmp_path / \"result.json\"\n    file = JsonCodec().parse(ResolvedPath(target), '{\"name\":\"Ada\"}')\n    fsync_calls: list[int] = []\n    replace_calls: list[tuple[Path, Path]] = []\n    original_fsync = os.fsync\n    original_replace = os.replace\n\n    def record_fsync(file_descriptor: int) -> None:\n        fsync_calls.append(file_descriptor)\n        original_fsync(file_descriptor)\n\n    def record_replace(source: Path, destination: Path) -> None:\n        replace_calls.append((source, destination))\n        original_replace(source, destination)\n\n    monkeypatch.setattr(\"devtools.resources.filesystem.writing.os.fsync\", record_fsync)\n    monkeypatch.setattr(\n        \"devtools.resources.filesystem.writing.os.replace\",\n        record_replace,\n    )\n\n    write(file)\n\n    assert json.loads(target.read_text(encoding=\"utf-8\")) == {\"name\": \"Ada\"}\n    assert fsync_calls\n    assert replace_calls[0][0].parent == target.parent\n    assert replace_calls[0][1] == target\n",
        "resource": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "start": 493,
        "start_line": 28
      }
    ]
  },
  {
    "address": "tests/resources/filesystem/test_writing.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "packet_ordinal": 500
    },
    "resource": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
    "semantic_rationale": "Existing atomic-write regression corroborates the unchanged adjacent lifecycle; the read-only acquisition change does not make the write test a required evidence source.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/resources/filesystem/test_writing.py",
        "end": 1683,
        "end_line": 59,
        "quote": "def test_write_persists_a_new_json_file_and_fsyncs_before_replacement(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Writing uses a sibling temporary file, fsync, then atomic replacement.\"\"\"\n    target = tmp_path / \"result.json\"\n    file = JsonCodec().parse(ResolvedPath(target), '{\"name\":\"Ada\"}')\n    fsync_calls: list[int] = []\n    replace_calls: list[tuple[Path, Path]] = []\n    original_fsync = os.fsync\n    original_replace = os.replace\n\n    def record_fsync(file_descriptor: int) -> None:\n        fsync_calls.append(file_descriptor)\n        original_fsync(file_descriptor)\n\n    def record_replace(source: Path, destination: Path) -> None:\n        replace_calls.append((source, destination))\n        original_replace(source, destination)\n\n    monkeypatch.setattr(\"devtools.resources.filesystem.writing.os.fsync\", record_fsync)\n    monkeypatch.setattr(\n        \"devtools.resources.filesystem.writing.os.replace\",\n        record_replace,\n    )\n\n    write(file)\n\n    assert json.loads(target.read_text(encoding=\"utf-8\")) == {\"name\": \"Ada\"}\n    assert fsync_calls\n    assert replace_calls[0][0].parent == target.parent\n    assert replace_calls[0][1] == target\n",
        "resource": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "start": 493,
        "start_line": 28
      }
    ]
  },
  {
    "address": "tests/scripts/test_validate_development.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
      "packet_ordinal": 508
    },
    "resource": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
    "semantic_rationale": "The profile tests verify selected arguments and failure forwarding, but do not independently exclude additional coverage-overriding arguments. They corroborate the protected policy without substituting for the script or operating guide.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/scripts/test_validate_development.py",
        "end": 2104,
        "end_line": 68,
        "quote": "_SCRIPT_PATH = Path(\"scripts/validate_development.py\")\n\n\n@pytest.fixture\ndef validation_script() -> ModuleType:\n    \"\"\"Load the operational script without making scripts a library package.\"\"\"\n    specification = importlib.util.spec_from_file_location(\n        \"test_validate_development_script\",\n        _SCRIPT_PATH,\n    )\n    assert specification is not None\n    assert specification.loader is not None\n    module = importlib.util.module_from_spec(specification)\n    sys.modules[specification.name] = module\n    specification.loader.exec_module(module)\n    return module\n\n\ndef test_profile_selects_tests_and_excludes_experiment_tests_before_collection(\n    validation_script: ModuleType,\n) -> None:\n    \"\"\"The directory boundary covers the whole retained experiment population.\"\"\"\n    arguments = validation_script.pytest_arguments(Path.cwd())\n    tests = Path(arguments[0])\n    ignored = Path(arguments[1].removeprefix(\"--ignore=\"))\n\n    assert tests == Path.cwd() / \"tests\"\n    assert ignored == tests / \"experiments\"\n    assert tests.is_dir()\n    assert ignored.is_dir()\n    assert (tests / \"context\").is_dir()\n    assert (tests / \"scripts\" / \"test_validate_development.py\").is_file()\n\n\ndef test_profile_propagates_pytest_failure_code(\n    validation_script: ModuleType,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A failed pytest run remains a failed profile invocation.\"\"\"\n    observed_arguments: list[str] | None = None\n\n    def failed_pytest(arguments: list[str]) -> int:\n        nonlocal observed_arguments\n        observed_arguments = arguments\n        return 1\n\n    monkeypatch.setattr(validation_script.pytest, \"main\", failed_pytest)\n\n    result = validation_script.main()\n\n    assert result == 1\n    assert observed_arguments == validation_script.pytest_arguments()\n",
        "resource": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "start": 313,
        "start_line": 17
      }
    ]
  },
  {
    "address": "tests/tools/test_filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O1",
    "provenance": {
      "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "packet_ordinal": 513
    },
    "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
    "semantic_rationale": "Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/tools/test_filesystem.py",
        "end": 8063,
        "end_line": 265,
        "quote": "def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted missing path remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(FilesystemNotFoundError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root / \"missing.md\"),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_leaves_directories_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted in-root directory remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    directory = root / \"directory\"\n    directory.mkdir(parents=True)\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(directory),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(\n    tmp_path: Path,\n) -> None:\n    \"\"\"The configured root itself is in scope but normally is not a file.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_unknown_text_extension_as_text(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified repository extension uses the Filesystem text decoder.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"notes.unknown\"\n    source.parent.mkdir()\n    source.write_text(\"notes\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content == \"notes\"\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_python_source_as_text(tmp_path: Path) -> None:\n    \"\"\"A coding-oriented Tool reads Python source through the Filesystem boundary.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"reader.py\"\n    source.parent.mkdir(parents=True)\n    source.write_text(\"MARKER = 'source-text'\\n\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content.splitlines() == [\"MARKER = 'source-text'\"]\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_text_decoding_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified binary payload remains an honest text-decoding failure.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"binary.py\"\n    source.parent.mkdir(parents=True)\n    source.write_bytes(b\"\\xff\")\n\n    async def exercise() -> None:\n        with pytest.raises(TextDecodingError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_structured_format_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A recognized structured suffix does not fall back to unstructured text.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"invalid.json\"\n    source.parent.mkdir()\n    source.write_text(\"{not json\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        with pytest.raises(FileFormatError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n",
        "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "start": 4073,
        "start_line": 139
      }
    ]
  },
  {
    "address": "tests/tools/test_filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O3",
    "provenance": {
      "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "packet_ordinal": 513
    },
    "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
    "semantic_rationale": "Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/tools/test_filesystem.py",
        "end": 8063,
        "end_line": 265,
        "quote": "def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted missing path remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(FilesystemNotFoundError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root / \"missing.md\"),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_leaves_directories_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted in-root directory remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    directory = root / \"directory\"\n    directory.mkdir(parents=True)\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(directory),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(\n    tmp_path: Path,\n) -> None:\n    \"\"\"The configured root itself is in scope but normally is not a file.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_unknown_text_extension_as_text(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified repository extension uses the Filesystem text decoder.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"notes.unknown\"\n    source.parent.mkdir()\n    source.write_text(\"notes\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content == \"notes\"\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_python_source_as_text(tmp_path: Path) -> None:\n    \"\"\"A coding-oriented Tool reads Python source through the Filesystem boundary.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"reader.py\"\n    source.parent.mkdir(parents=True)\n    source.write_text(\"MARKER = 'source-text'\\n\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content.splitlines() == [\"MARKER = 'source-text'\"]\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_text_decoding_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified binary payload remains an honest text-decoding failure.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"binary.py\"\n    source.parent.mkdir(parents=True)\n    source.write_bytes(b\"\\xff\")\n\n    async def exercise() -> None:\n        with pytest.raises(TextDecodingError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_structured_format_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A recognized structured suffix does not fall back to unstructured text.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"invalid.json\"\n    source.parent.mkdir()\n    source.write_text(\"{not json\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        with pytest.raises(FileFormatError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n",
        "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "start": 4073,
        "start_line": 139
      }
    ]
  },
  {
    "address": "tests/tools/test_filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O4",
    "provenance": {
      "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "packet_ordinal": 513
    },
    "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
    "semantic_rationale": "Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/tools/test_filesystem.py",
        "end": 8063,
        "end_line": 265,
        "quote": "def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted missing path remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(FilesystemNotFoundError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root / \"missing.md\"),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_leaves_directories_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted in-root directory remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    directory = root / \"directory\"\n    directory.mkdir(parents=True)\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(directory),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(\n    tmp_path: Path,\n) -> None:\n    \"\"\"The configured root itself is in scope but normally is not a file.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_unknown_text_extension_as_text(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified repository extension uses the Filesystem text decoder.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"notes.unknown\"\n    source.parent.mkdir()\n    source.write_text(\"notes\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content == \"notes\"\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_python_source_as_text(tmp_path: Path) -> None:\n    \"\"\"A coding-oriented Tool reads Python source through the Filesystem boundary.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"reader.py\"\n    source.parent.mkdir(parents=True)\n    source.write_text(\"MARKER = 'source-text'\\n\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content.splitlines() == [\"MARKER = 'source-text'\"]\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_text_decoding_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified binary payload remains an honest text-decoding failure.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"binary.py\"\n    source.parent.mkdir(parents=True)\n    source.write_bytes(b\"\\xff\")\n\n    async def exercise() -> None:\n        with pytest.raises(TextDecodingError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_structured_format_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A recognized structured suffix does not fall back to unstructured text.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"invalid.json\"\n    source.parent.mkdir()\n    source.write_text(\"{not json\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        with pytest.raises(FileFormatError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n",
        "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "start": 4073,
        "start_line": 139
      }
    ]
  },
  {
    "address": "tests/tools/test_filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O5",
    "provenance": {
      "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "packet_ordinal": 513
    },
    "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
    "semantic_rationale": "Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/tools/test_filesystem.py",
        "end": 8063,
        "end_line": 265,
        "quote": "def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted missing path remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(FilesystemNotFoundError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root / \"missing.md\"),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_leaves_directories_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted in-root directory remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    directory = root / \"directory\"\n    directory.mkdir(parents=True)\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(directory),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(\n    tmp_path: Path,\n) -> None:\n    \"\"\"The configured root itself is in scope but normally is not a file.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_unknown_text_extension_as_text(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified repository extension uses the Filesystem text decoder.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"notes.unknown\"\n    source.parent.mkdir()\n    source.write_text(\"notes\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content == \"notes\"\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_python_source_as_text(tmp_path: Path) -> None:\n    \"\"\"A coding-oriented Tool reads Python source through the Filesystem boundary.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"reader.py\"\n    source.parent.mkdir(parents=True)\n    source.write_text(\"MARKER = 'source-text'\\n\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content.splitlines() == [\"MARKER = 'source-text'\"]\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_text_decoding_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified binary payload remains an honest text-decoding failure.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"binary.py\"\n    source.parent.mkdir(parents=True)\n    source.write_bytes(b\"\\xff\")\n\n    async def exercise() -> None:\n        with pytest.raises(TextDecodingError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_structured_format_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A recognized structured suffix does not fall back to unstructured text.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"invalid.json\"\n    source.parent.mkdir()\n    source.write_text(\"{not json\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        with pytest.raises(FileFormatError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n",
        "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "start": 4073,
        "start_line": 139
      }
    ]
  },
  {
    "address": "tests/tools/test_filesystem.py",
    "inferability_rationale": "These spans provide corroboration or implementation examples, but the obligation has a complete minimal evidence route without this information. Task-prescribed future behavior is not recast as a new current-state prerequisite.",
    "label": "HELPFUL_ONLY",
    "obligation": "O6",
    "provenance": {
      "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "packet_ordinal": 513
    },
    "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
    "semantic_rationale": "Existing Tool regressions confirm filesystem failure propagation and text fallback; they provide caller compatibility examples without an obsolete read_bytes injection.",
    "support_kind": [
      "CORROBORATION_ONLY"
    ],
    "support_spans": [
      {
        "address": "tests/tools/test_filesystem.py",
        "end": 8063,
        "end_line": 265,
        "quote": "def test_read_repository_file_tool_leaves_missing_paths_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted missing path remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(FilesystemNotFoundError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root / \"missing.md\"),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_leaves_directories_to_filesystem(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An admitted in-root directory remains a Filesystem execution failure.\"\"\"\n    root = tmp_path / \"repository\"\n    directory = root / \"directory\"\n    directory.mkdir(parents=True)\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(directory),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_admits_root_then_filesystem_rejects_directory(\n    tmp_path: Path,\n) -> None:\n    \"\"\"The configured root itself is in scope but normally is not a file.\"\"\"\n    root = tmp_path / \"repository\"\n    root.mkdir()\n\n    async def exercise() -> None:\n        with pytest.raises(NotAFileError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(root),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_unknown_text_extension_as_text(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified repository extension uses the Filesystem text decoder.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"notes.unknown\"\n    source.parent.mkdir()\n    source.write_text(\"notes\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content == \"notes\"\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_reads_python_source_as_text(tmp_path: Path) -> None:\n    \"\"\"A coding-oriented Tool reads Python source through the Filesystem boundary.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"reader.py\"\n    source.parent.mkdir(parents=True)\n    source.write_text(\"MARKER = 'source-text'\\n\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        result = await ToolRunner().execute(\n            ReadRepositoryFileTool(_resolved(root)),\n            _resolved(source),\n        )\n\n        assert isinstance(result, TextFile)\n        assert result.content.splitlines() == [\"MARKER = 'source-text'\"]\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_text_decoding_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"An unclassified binary payload remains an honest text-decoding failure.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"src\" / \"binary.py\"\n    source.parent.mkdir(parents=True)\n    source.write_bytes(b\"\\xff\")\n\n    async def exercise() -> None:\n        with pytest.raises(TextDecodingError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n    asyncio.run(exercise())\n\n\ndef test_read_repository_file_tool_preserves_structured_format_failure(\n    tmp_path: Path,\n) -> None:\n    \"\"\"A recognized structured suffix does not fall back to unstructured text.\"\"\"\n    root = tmp_path / \"repository\"\n    source = root / \"invalid.json\"\n    source.parent.mkdir()\n    source.write_text(\"{not json\", encoding=\"utf-8\")\n\n    async def exercise() -> None:\n        with pytest.raises(FileFormatError):\n            await ToolRunner().execute(\n                ReadRepositoryFileTool(_resolved(root)),\n                _resolved(source),\n            )\n\n",
        "resource": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "start": 4073,
        "start_line": 139
      }
    ]
  }
]
```

## All semantic units and exact support alternatives/spans

```json
[
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T01",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Replace finite whole-file acquisition inside the existing filesystem reader with bounded chunks.",
    "task_support": [
      {
        "end": 267,
        "quote": "In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite.",
        "start": 93
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T02",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve the public ResolvedPath, file_format, max_bytes and DEFAULT_MAX_READ_BYTES contract.",
    "task_support": [
      {
        "end": 368,
        "quote": "Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract",
        "start": 268
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T03",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "A preliminary stat is optional and cannot permit unbounded acquisition of a file that grows.",
    "task_support": [
      {
        "end": 627,
        "quote": "A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.",
        "start": 521
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T04",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O2"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "For a finite limit retain no more than max_bytes payload bytes and acquire at most one additional sentinel byte to distinguish exact EOF from excess.",
    "task_support": [
      {
        "end": 815,
        "quote": "retain at most `max_bytes` payload bytes and acquire at most one additional byte to distinguish exact-boundary EOF from oversized input",
        "start": 680
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T05",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O2"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Every finite-mode read request is bounded.",
    "task_support": [
      {
        "end": 847,
        "quote": "bound individual read requests",
        "start": 817
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T06",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O2"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Release the acquired stream on success and every failure.",
    "task_support": [
      {
        "end": 900,
        "quote": "release the stream on success and every failure.",
        "start": 852
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T07",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O2"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Excess raises FileTooLargeError and never returns a truncated model.",
    "task_support": [
      {
        "end": 976,
        "quote": "Raise `FileTooLargeError` on excess instead of returning a truncated model.",
        "start": 901
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T08",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O2"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "The acquisition guarantee makes none of the excluded model-memory, snapshot, pathname-race, containment, authorization, or locking claims.",
    "task_support": [
      {
        "end": 1112,
        "quote": "Do not claim a bound on decoded model memory, a stable file snapshot, race-free pathname checks, containment, authorization or locking.",
        "start": 977
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T09",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve format override, suffix inference and the existing resolution functions.",
    "task_support": [
      {
        "end": 1225,
        "quote": "Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference.",
        "start": 1118
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T10",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Delegate complete accepted bytes to the existing codecs without content rewriting.",
    "task_support": [
      {
        "end": 1304,
        "quote": "Pass complete accepted bytes to the existing codecs without rewriting content.",
        "start": 1226
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T11",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Retain all six specified rich result classes.",
    "task_support": [
      {
        "end": 1427,
        "quote": "Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results",
        "start": 1305
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T12",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve UTF-8 decoding, original line endings, encoding metadata and source byte-size metadata.",
    "task_support": [
      {
        "end": 1500,
        "quote": "UTF-8 decoding, original line endings, encoding and byte-size metadata.",
        "start": 1429
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T13",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Chunk boundaries may split multibyte sequences; no replacement decoding is introduced and codec-domain failures retain their existing classes.",
    "task_support": [
      {
        "end": 1678,
        "quote": "Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.",
        "start": 1501
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T14",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve the existing missing-path, non-regular-file, permission, unsupported-format and excess error boundaries.",
    "task_support": [
      {
        "end": 1826,
        "quote": "Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input.",
        "start": 1684
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T15",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Normalize stream-open and chunk-read PermissionError failures with causal FilesystemPermissionError exceptions.",
    "task_support": [
      {
        "end": 1949,
        "quote": "Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions.",
        "start": 1827
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T16",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Keep the change within the existing filesystem package and preserve atomic writing, format ownership, core path resolution and Tool boundaries.",
    "task_support": [
      {
        "end": 2162,
        "quote": "Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.",
        "start": 1950
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T17",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O5"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Add controlled read tests at the specified test location and relevant codec/model tests covering the limit domain.",
    "task_support": [
      {
        "end": 2343,
        "quote": "Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits",
        "start": 2168
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T18",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O5"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Test growth after stat, short reads, EOF, closure on exceptions and open/read permission failures.",
    "task_support": [
      {
        "end": 2450,
        "quote": "growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures",
        "start": 2345
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T19",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O5"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Test multibyte splits, invalid UTF-8, explicit overrides and every supported rich result type.",
    "task_support": [
      {
        "end": 2576,
        "quote": "multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types.",
        "start": 2452
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T20",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O5"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Prove finite request and retention bounds using deterministic instrumented streams.",
    "task_support": [
      {
        "end": 2740,
        "quote": "Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.",
        "start": 2577
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T21",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Update I/O, overview, roadmap and applicable public API documentation to state the bound and its limitations.",
    "task_support": [
      {
        "end": 2951,
        "quote": "Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately.",
        "start": 2746
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T22",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve existing callers.",
    "task_support": [
      {
        "end": 2977,
        "quote": "Preserve existing callers",
        "start": 2952
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T23",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve the protected validation profile and run it along with Ruff, formatting, mypy and diff checks.",
    "task_support": [
      {
        "end": 3186,
        "quote": "the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks.",
        "start": 2982
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T24",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Do not expand into binary codecs, new formats, streaming format parsing, secure filesystem policy or production retrieval changes.",
    "task_support": [
      {
        "end": 3314,
        "quote": "Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.",
        "start": 3187
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R01.A1",
        "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The implementation defines the signature and both checks.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 906,
            "end_line": 35,
            "quote": "DEFAULT_MAX_READ_BYTES = 16 * 1024 * 1024\n\n\ndef read(\n    path: ResolvedPath,\n    *,\n    file_format: FileFormat | None = None,\n    max_bytes: int | None = DEFAULT_MAX_READ_BYTES,\n) -> File:\n    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 526,
            "start_line": 23
          },
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 3504,
            "end_line": 116,
            "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 3200,
            "start_line": 107
          }
        ]
      },
      {
        "id": "R01.A2",
        "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The I/O contract independently states the callable shape, defaults, limit meanings and allocation-before-rejection behavior.",
        "resources": [
          "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/io.md",
            "end": 913,
            "end_line": 30,
            "quote": "```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n",
            "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
            "start": 424,
            "start_line": 20
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R01",
    "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
    "necessity_rationale": "These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 906,
        "end_line": 35,
        "quote": "DEFAULT_MAX_READ_BYTES = 16 * 1024 * 1024\n\n\ndef read(\n    path: ResolvedPath,\n    *,\n    file_format: FileFormat | None = None,\n    max_bytes: int | None = DEFAULT_MAX_READ_BYTES,\n) -> File:\n    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 526,
        "start_line": 23
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 3200,
        "start_line": 107
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 913,
        "end_line": 30,
        "quote": "```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 424,
        "start_line": 20
      }
    ],
    "statement": "The current public reader takes ResolvedPath and keyword-only file_format/max_bytes, uses the 16 MiB default, permits None and rejects negative limits.",
    "task_support": [
      {
        "end": 629,
        "quote": "O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.\n\n",
        "start": 89
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R02.A1",
        "inferability_assumptions": "For identical complete bytes, original path and unchanged codec invocation, existing codec/model behavior is preserved. No independent implementation of codecs or constructors is needed. This is a preservation argument, not proof that each desired future property already exists.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The existing integration call and its ordering are explicit.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 2737,
            "end_line": 90,
            "quote": "    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 2435,
            "start_line": 78
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R02",
    "inferability_assumptions": "For identical complete bytes, original path and unchanged codec invocation, existing codec/model behavior is preserved. No independent implementation of codecs or constructors is needed. This is a preservation argument, not proof that each desired future property already exists.",
    "necessity_rationale": "This seam is necessary to preserve codec behavior by leaving the existing resolution and decode path intact. It permits black-box preservation across every concrete codec.",
    "obligations": [
      "O3"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2737,
        "end_line": 90,
        "quote": "    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 2435,
        "start_line": 78
      }
    ],
    "statement": "The current integration resolves format only after successful acquisition/size validation, bypasses inference for an explicit format, calls resolve_codec, and returns codec.decode(original_path, complete_bytes) with codec defaults.",
    "task_support": [
      {
        "end": 1680,
        "quote": "O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.\n\n",
        "start": 1114
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R03.A1",
        "inferability_assumptions": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The suffix map, codec map and error boundaries are explicit.",
        "resources": [
          "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/resolution.py",
            "end": 2063,
            "end_line": 72,
            "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
            "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
            "start": 448,
            "start_line": 20
          }
        ]
      },
      {
        "id": "R03.A2",
        "inferability_assumptions": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "The I/O contract supplies final-suffix semantics; independent contract tests supply the concrete codec mappings and unsupported/binary failures.",
        "resources": [
          "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
          "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/io.md",
            "end": 411,
            "end_line": 16,
            "quote": "## Format resolution\n\n`resolve_file_format(path)` resolves the final suffix case-insensitively:\n\n| Suffix | Format |\n|---|---|\n| `.csv` | CSV |\n| `.json` | JSON |\n| `.md`, `.markdown` | Markdown |\n| `.txt` | Text |\n\nUnsupported or unimplemented formats raise `FileFormatError`. An explicit\n`file_format` passed to `read()` bypasses suffix inference. Binary has no\ncodec-backed suffix support.\n",
            "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
            "start": 18,
            "start_line": 3
          },
          {
            "address": "tests/resources/filesystem/test_resolution.py",
            "end": 1911,
            "end_line": 61,
            "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
            "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
            "start": 496,
            "start_line": 26
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R03",
    "inferability_assumptions": "A supported code/test/documentation contract is accepted as evidence of current behavior when uncontradicted. The documentation and tests in the second alternative are complementary, not individually complete.",
    "necessity_rationale": "Preserving resolver behavior and unsupported-format boundaries requires current mapping/ownership facts absent from the task, which names the functions without defining the mappings.",
    "obligations": [
      "O3",
      "O4"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/resolution.py",
        "end": 2063,
        "end_line": 72,
        "quote": "_SUFFIX_FORMATS = {\n    \".csv\": FileFormat.CSV,\n    \".json\": FileFormat.JSON,\n    \".md\": FileFormat.MARKDOWN,\n    \".markdown\": FileFormat.MARKDOWN,\n    \".txt\": FileFormat.TEXT,\n}\n_CODEC_TYPES: dict[\n    FileFormat,\n    type[CsvCodec | JsonCodec | MarkdownCodec | TextCodec],\n] = {\n    FileFormat.CSV: CsvCodec,\n    FileFormat.JSON: JsonCodec,\n    FileFormat.MARKDOWN: MarkdownCodec,\n    FileFormat.TEXT: TextCodec,\n}\n\n\ndef resolve_file_format(path: ResolvedPath) -> FileFormat:\n    \"\"\"Resolve a file format from a path.\n\n    Resolution is based on the final filename suffix. Only formats with an\n    implemented codec are currently recognized.\n\n    :param path: Resolved filesystem path.\n    :returns: Resolved file format.\n    :raises FileFormatError: If the path suffix has no supported format.\n    \"\"\"\n    suffix = path.suffix.lower()\n\n    try:\n        return _SUFFIX_FORMATS[suffix]\n    except KeyError as error:\n        msg = f\"Unsupported file format for path: {path}.\"\n        raise FileFormatError(msg) from error\n\n\ndef resolve_codec(\n    file_format: FileFormat,\n) -> CsvCodec | JsonCodec | MarkdownCodec | TextCodec:\n    \"\"\"Resolve the codec for a file format.\n\n    :param file_format: File format requiring representation conversion.\n    :returns: Codec supporting the supplied format.\n    :raises FileFormatError: If no codec is implemented for the format.\n    \"\"\"\n    try:\n        codec_type = _CODEC_TYPES[file_format]\n    except KeyError as error:\n        msg = f\"No codec is implemented for file format: {file_format.value!r}.\"\n        raise FileFormatError(msg) from error\n\n    return codec_type()\n",
        "resource": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "start": 448,
        "start_line": 20
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 411,
        "end_line": 16,
        "quote": "## Format resolution\n\n`resolve_file_format(path)` resolves the final suffix case-insensitively:\n\n| Suffix | Format |\n|---|---|\n| `.csv` | CSV |\n| `.json` | JSON |\n| `.md`, `.markdown` | Markdown |\n| `.txt` | Text |\n\nUnsupported or unimplemented formats raise `FileFormatError`. An explicit\n`file_format` passed to `read()` bypasses suffix inference. Binary has no\ncodec-backed suffix support.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 18,
        "start_line": 3
      },
      {
        "address": "tests/resources/filesystem/test_resolution.py",
        "end": 1911,
        "end_line": 61,
        "quote": "@pytest.mark.parametrize(\n    (\"filename\", \"file_format\"),\n    [\n        (\"report.JsOn\", FileFormat.JSON),\n        (\"report.CsV\", FileFormat.CSV),\n        (\"report.MD\", FileFormat.MARKDOWN),\n        (\"report.MarkDown\", FileFormat.MARKDOWN),\n        (\"report.TxT\", FileFormat.TEXT),\n    ],\n)\ndef test_resolve_file_format_is_case_insensitive_for_supported_codecs(\n    tmp_path: Path,\n    filename: str,\n    file_format: FileFormat,\n) -> None:\n    \"\"\"JSON, text, and Markdown suffixes resolve regardless of case.\"\"\"\n    path = ResolvedPath(tmp_path / filename)\n\n    assert resolve_file_format(path) is file_format\n\n\ndef test_resolution_rejects_unsupported_formats(tmp_path: Path) -> None:\n    \"\"\"Only formats with real codecs resolve during this milestone.\"\"\"\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        resolve_file_format(ResolvedPath(tmp_path / \"report.unsupported\"))\n\n    with pytest.raises(FileFormatError, match=\"No codec\"):\n        resolve_codec(FileFormat.BINARY)\n\n\ndef test_resolve_codec_returns_implemented_codecs() -> None:\n    \"\"\"Each supported format resolves to its concrete representation codec.\"\"\"\n    assert isinstance(resolve_codec(FileFormat.JSON), JsonCodec)\n    assert isinstance(resolve_codec(FileFormat.CSV), CsvCodec)\n    assert isinstance(resolve_codec(FileFormat.MARKDOWN), MarkdownCodec)\n    assert isinstance(resolve_codec(FileFormat.TEXT), TextCodec)\n",
        "resource": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "start": 496,
        "start_line": 26
      }
    ],
    "statement": "Format resolution lowercases the final suffix; .csv, .json, .md/.markdown and .txt select four existing codecs. Unsupported suffixes and unimplemented formats, including binary, raise FileFormatError.",
    "task_support": [
      {
        "end": 1680,
        "quote": "O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.\n\n",
        "start": 1114
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R04.A1",
        "inferability_assumptions": "No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Control flow and raise-from statements establish current error precedence and causal normalization.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 2737,
            "end_line": 90,
            "quote": "    source = path.value\n\n    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 1608,
            "start_line": 50
          },
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 3504,
            "end_line": 116,
            "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 3200,
            "start_line": 107
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R04",
    "inferability_assumptions": "No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.",
    "necessity_rationale": "The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2737,
        "end_line": 90,
        "quote": "    source = path.value\n\n    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n\n    resolved_format = resolve_file_format(path) if file_format is None else file_format\n    codec = resolve_codec(resolved_format)\n\n    return codec.decode(\n        path,\n        content,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1608,
        "start_line": 50
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 3504,
        "end_line": 116,
        "quote": "    if max_bytes is None:\n        return\n\n    if max_bytes < 0:\n        msg = \"Maximum read size cannot be negative.\"\n        raise ValueError(msg)\n\n    if size_bytes > max_bytes:\n        msg = f\"File size {size_bytes} exceeds maximum read size {max_bytes}: {path}.\"\n        raise FileTooLargeError(msg)\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 3200,
        "start_line": 107
      }
    ],
    "statement": "The reader checks existence, regular-file status and stat before acquisition; size rejection precedes codec resolution and decoding.",
    "task_support": [
      {
        "end": 2164,
        "quote": "O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.\n\n",
        "start": 1680
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R05.A1",
        "inferability_assumptions": "Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The package overview identifies consumed path primitives and the filesystem ownership boundary.",
        "resources": [
          "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/overview.md",
            "end": 2476,
            "end_line": 71,
            "quote": "## Dependencies\n\nFilesystem consumes `ResolvedPath` from `devtools.core.paths`, generic regex\nmechanics from `devtools.core.regex`, and callable conversion from\n`devtools.core.conversion`. It does not depend on `devtools.core.system`.\n\n## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n",
            "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
            "start": 1925,
            "start_line": 60
          }
        ]
      },
      {
        "id": "R05.A2",
        "inferability_assumptions": "Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The operating guide independently assigns canonical path/filesystem substrates and separates Resource and Tool authority.",
        "resources": [
          "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
        ],
        "support_spans": [
          {
            "address": "AGENTS.md",
            "end": 4424,
            "end_line": 86,
            "quote": "- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do\n  not reimplement path normalization, repository-root resolution, or existing\n  containment behavior.\n- Use `devtools.resources.commands` for managed subprocess work. Higher domains must\n  not call direct `subprocess` or `asyncio` subprocess APIs without explicit\n  architectural justification.\n- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded\n  reads, and atomic writes. Do not recreate those semantics in Tools, Context,\n  Agents, or experiments.\n",
            "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
            "start": 3856,
            "start_line": 78
          },
          {
            "address": "AGENTS.md",
            "end": 8549,
            "end_line": 179,
            "quote": "Resources such as filesystem and commands may be adapted into Tools. A Tool is\nnot an Action; an Action request is not authority. Preserve:\n\n```text\nmodel proposal != authority       visibility != authorization\nTool validation != authorization  approval != automatically authority\ncapability availability != authorization\n",
            "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
            "start": 8227,
            "start_line": 173
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R05",
    "inferability_assumptions": "Ownership documentation establishes the boundary. The task supplies the prohibition on changing adjacent behavior; it does not require implementation of those adjacent domains.",
    "necessity_rationale": "Knowing the current ownership boundary supports a local acquisition change without moving existing responsibilities. Detailed atomic-write, path-parser or Tool implementations are not required merely because they are protected.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 2476,
        "end_line": 71,
        "quote": "## Dependencies\n\nFilesystem consumes `ResolvedPath` from `devtools.core.paths`, generic regex\nmechanics from `devtools.core.regex`, and callable conversion from\n`devtools.core.conversion`. It does not depend on `devtools.core.system`.\n\n## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 1925,
        "start_line": 60
      },
      {
        "address": "AGENTS.md",
        "end": 4424,
        "end_line": 86,
        "quote": "- Use `devtools.core.paths` for semantic resolved paths and resolution policy. Do\n  not reimplement path normalization, repository-root resolution, or existing\n  containment behavior.\n- Use `devtools.resources.commands` for managed subprocess work. Higher domains must\n  not call direct `subprocess` or `asyncio` subprocess APIs without explicit\n  architectural justification.\n- Use `devtools.resources.filesystem` for its existing file models, decoding, bounded\n  reads, and atomic writes. Do not recreate those semantics in Tools, Context,\n  Agents, or experiments.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 3856,
        "start_line": 78
      },
      {
        "address": "AGENTS.md",
        "end": 8549,
        "end_line": 179,
        "quote": "Resources such as filesystem and commands may be adapted into Tools. A Tool is\nnot an Action; an Action request is not authority. Preserve:\n\n```text\nmodel proposal != authority       visibility != authorization\nTool validation != authorization  approval != automatically authority\ncapability availability != authorization\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 8227,
        "start_line": 173
      }
    ],
    "statement": "Filesystem owns its existing models, codecs, format resolution, reads and atomic writes; core paths and higher Tool concerns retain their separate ownership.",
    "task_support": [
      {
        "end": 2164,
        "quote": "O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.\n\n",
        "start": 1680
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R06.A1",
        "inferability_assumptions": "New instrumented-stream fixture names and decomposition remain free choices. The original tests establish current seams, not the design of future fixtures.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "These tests contain both rich-result examples and obsolete acquisition-specific injections.",
        "resources": [
          "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
        ],
        "support_spans": [
          {
            "address": "tests/resources/filesystem/test_reading.py",
            "end": 1225,
            "end_line": 50,
            "quote": "@pytest.mark.parametrize(\n    (\"name\", \"content\", \"model_type\"),\n    [\n        (\"object.json\", b'{\"name\":\"Ada\",\"id\":2}', JsonObjectFile),\n        (\"array.JSON\", b'[{\"id\":1}]', JsonListFile),\n        (\"scalar.json\", b\"true\", JsonScalarFile),\n    ],\n)\ndef test_read_returns_the_concrete_json_root_model(\n    tmp_path: Path,\n    name: str,\n    content: bytes,\n    model_type: type[JsonObjectFile | JsonListFile | JsonScalarFile],\n) -> None:\n    \"\"\"Suffix resolution and decoding preserve the rich JSON root type.\"\"\"\n    source = tmp_path / name\n    source.write_bytes(content)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, model_type)\n    assert file.byte_size == len(content)\n",
            "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
            "start": 529,
            "start_line": 29
          },
          {
            "address": "tests/resources/filesystem/test_reading.py",
            "end": 4740,
            "end_line": 145,
            "quote": "def test_read_returns_text_models_with_exact_source_behavior(tmp_path: Path) -> None:\n    \"\"\"Text suffix resolution retains bytes, metadata, and text-model operations.\"\"\"\n    source = tmp_path / \"notes.TXT\"\n    content = \"caf\u00c3\u00a9\\r\\nstatus: ready\\n\"\n    encoded = content.encode(\"utf-8\")\n    source.write_bytes(encoded)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, TextFile)\n    assert file.content == content\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert file.contains(\"ready\") is True\n    assert file.search_regex(r\"status: \\w+\") is not None\n\n\ndef test_read_allows_an_explicit_text_override(tmp_path: Path) -> None:\n    \"\"\"Text format overrides bypass unsupported or absent suffix inference.\"\"\"\n    source = tmp_path / \"message.data\"\n    source.write_bytes(b\"hello\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.TEXT)\n\n    assert isinstance(file, TextFile)\n    assert file.content == \"hello\\n\"\n\n\n@pytest.mark.parametrize(\"suffix\", [\".md\", \".MARKDOWN\"])\ndef test_read_returns_rich_markdown_models(tmp_path: Path, suffix: str) -> None:\n    \"\"\"Markdown suffixes decode to structural models with source access intact.\"\"\"\n    source = tmp_path / f\"document{suffix}\"\n    content = \"# Title\\n## Detail\\nText\\n\"\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, MarkdownFile)\n    assert file.content == content\n    assert file.headings[1].text == \"Detail\"\n    assert file.find_section(\"title\") is not None\n    assert file.search_regex(\"Text\") is not None\n\n\ndef test_read_allows_an_explicit_markdown_override(tmp_path: Path) -> None:\n    \"\"\"Markdown overrides bypass suffix inference for source files without a suffix.\"\"\"\n    source = tmp_path / \"readme\"\n    source.write_bytes(b\"# Title\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.MARKDOWN)\n\n    assert isinstance(file, MarkdownFile)\n    assert file.headings[0].text == \"Title\"\n\n\ndef test_read_returns_rich_csv_models(tmp_path: Path) -> None:\n    \"\"\"Mixed-case CSV paths decode to header-addressable immutable row models.\"\"\"\n    source = tmp_path / \"reports.CSV\"\n    content = 'id,status\\nreport-1,passed\\nreport-2,\"needs, review\"\\n'\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, CsvFile)\n    assert file.headers == (\"id\", \"status\")\n    assert file.column(\"status\") == (\"passed\", \"needs, review\")\n    assert file.find_by(\"id\", \"report-2\") == file[1]\n    assert file.search_regex(\"review\") is not None\n\n\ndef test_read_allows_an_explicit_csv_override(tmp_path: Path) -> None:\n    \"\"\"CSV overrides bypass suffix inference for a source without a suffix.\"\"\"\n    source = tmp_path / \"reports\"\n    source.write_bytes(b\"id,status\\nreport-1,passed\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.CSV)\n\n    assert isinstance(file, CsvFile)\n    assert file[0][\"status\"] == \"passed\"\n",
            "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
            "start": 1780,
            "start_line": 67
          },
          {
            "address": "tests/resources/filesystem/test_reading.py",
            "end": 7710,
            "end_line": 233,
            "quote": "def test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
            "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
            "start": 6056,
            "start_line": 182
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R06",
    "inferability_assumptions": "New instrumented-stream fixture names and decomposition remain free choices. The original tests establish current seams, not the design of future fixtures.",
    "necessity_rationale": "This is a necessary current regression constraint, not a requirement to read a test merely because new tests are requested. Leaving these injections unchanged would stop them exercising the new finite acquisition path.",
    "obligations": [
      "O5"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 1225,
        "end_line": 50,
        "quote": "@pytest.mark.parametrize(\n    (\"name\", \"content\", \"model_type\"),\n    [\n        (\"object.json\", b'{\"name\":\"Ada\",\"id\":2}', JsonObjectFile),\n        (\"array.JSON\", b'[{\"id\":1}]', JsonListFile),\n        (\"scalar.json\", b\"true\", JsonScalarFile),\n    ],\n)\ndef test_read_returns_the_concrete_json_root_model(\n    tmp_path: Path,\n    name: str,\n    content: bytes,\n    model_type: type[JsonObjectFile | JsonListFile | JsonScalarFile],\n) -> None:\n    \"\"\"Suffix resolution and decoding preserve the rich JSON root type.\"\"\"\n    source = tmp_path / name\n    source.write_bytes(content)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, model_type)\n    assert file.byte_size == len(content)\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 529,
        "start_line": 29
      },
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 4740,
        "end_line": 145,
        "quote": "def test_read_returns_text_models_with_exact_source_behavior(tmp_path: Path) -> None:\n    \"\"\"Text suffix resolution retains bytes, metadata, and text-model operations.\"\"\"\n    source = tmp_path / \"notes.TXT\"\n    content = \"caf\u00c3\u00a9\\r\\nstatus: ready\\n\"\n    encoded = content.encode(\"utf-8\")\n    source.write_bytes(encoded)\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, TextFile)\n    assert file.content == content\n    assert file.encoding == \"utf-8\"\n    assert file.byte_size == len(encoded)\n    assert file.contains(\"ready\") is True\n    assert file.search_regex(r\"status: \\w+\") is not None\n\n\ndef test_read_allows_an_explicit_text_override(tmp_path: Path) -> None:\n    \"\"\"Text format overrides bypass unsupported or absent suffix inference.\"\"\"\n    source = tmp_path / \"message.data\"\n    source.write_bytes(b\"hello\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.TEXT)\n\n    assert isinstance(file, TextFile)\n    assert file.content == \"hello\\n\"\n\n\n@pytest.mark.parametrize(\"suffix\", [\".md\", \".MARKDOWN\"])\ndef test_read_returns_rich_markdown_models(tmp_path: Path, suffix: str) -> None:\n    \"\"\"Markdown suffixes decode to structural models with source access intact.\"\"\"\n    source = tmp_path / f\"document{suffix}\"\n    content = \"# Title\\n## Detail\\nText\\n\"\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, MarkdownFile)\n    assert file.content == content\n    assert file.headings[1].text == \"Detail\"\n    assert file.find_section(\"title\") is not None\n    assert file.search_regex(\"Text\") is not None\n\n\ndef test_read_allows_an_explicit_markdown_override(tmp_path: Path) -> None:\n    \"\"\"Markdown overrides bypass suffix inference for source files without a suffix.\"\"\"\n    source = tmp_path / \"readme\"\n    source.write_bytes(b\"# Title\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.MARKDOWN)\n\n    assert isinstance(file, MarkdownFile)\n    assert file.headings[0].text == \"Title\"\n\n\ndef test_read_returns_rich_csv_models(tmp_path: Path) -> None:\n    \"\"\"Mixed-case CSV paths decode to header-addressable immutable row models.\"\"\"\n    source = tmp_path / \"reports.CSV\"\n    content = 'id,status\\nreport-1,passed\\nreport-2,\"needs, review\"\\n'\n    source.write_bytes(content.encode())\n\n    file = read(ResolvedPath(source))\n\n    assert isinstance(file, CsvFile)\n    assert file.headers == (\"id\", \"status\")\n    assert file.column(\"status\") == (\"passed\", \"needs, review\")\n    assert file.find_by(\"id\", \"report-2\") == file[1]\n    assert file.search_regex(\"review\") is not None\n\n\ndef test_read_allows_an_explicit_csv_override(tmp_path: Path) -> None:\n    \"\"\"CSV overrides bypass suffix inference for a source without a suffix.\"\"\"\n    source = tmp_path / \"reports\"\n    source.write_bytes(b\"id,status\\nreport-1,passed\\n\")\n\n    file = read(ResolvedPath(source), file_format=FileFormat.CSV)\n\n    assert isinstance(file, CsvFile)\n    assert file[0][\"status\"] == \"passed\"\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 1780,
        "start_line": 67
      },
      {
        "address": "tests/resources/filesystem/test_reading.py",
        "end": 7710,
        "end_line": 233,
        "quote": "def test_read_rechecks_size_after_the_content_is_loaded(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A file that grows after stat is rejected rather than returned oversized.\"\"\"\n    source = tmp_path / \"racing.json\"\n    source.write_bytes(b\"{}\")\n    grown_content = b'{\"name\":\"longer\"}'\n\n    def read_grown_content(_path: Path) -> bytes:\n        return grown_content\n\n    monkeypatch.setattr(Path, \"read_bytes\", read_grown_content)\n\n    with pytest.raises(FileTooLargeError, match=\"exceeds\"):\n        read(ResolvedPath(source), max_bytes=2)\n\n\ndef test_read_normalizes_permission_failures(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Inspection and content-read permission failures use domain errors.\"\"\"\n    source = tmp_path / \"value.json\"\n    source.write_bytes(b\"{}\")\n\n    def deny_exists(_path: Path) -> bool:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"exists\", deny_exists)\n\n    with pytest.raises(FilesystemPermissionError, match=\"inspecting\"):\n        read(ResolvedPath(source))\n\n    monkeypatch.undo()\n\n    def deny_read(_path: Path) -> bytes:\n        raise PermissionError\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n\n    with pytest.raises(FilesystemPermissionError, match=\"reading\"):\n        read(ResolvedPath(source))\n\n\ndef test_read_reports_unsupported_inferred_suffixes(tmp_path: Path) -> None:\n    \"\"\"An unsupported suffix fails after a complete bounded file read.\"\"\"\n    source = tmp_path / \"value.unknown\"\n    source.write_bytes(b\"{}\")\n\n    with pytest.raises(FileFormatError, match=\"Unsupported file format\"):\n        read(ResolvedPath(source))\n",
        "resource": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "start": 6056,
        "start_line": 182
      }
    ],
    "statement": "Existing reader regressions invoke the public rich-model API and inject growth/read failures by monkeypatching Path.read_bytes; the finite-read replacement must migrate these existing injections while retaining their assertions.",
    "task_support": [
      {
        "end": 2742,
        "quote": "O5. Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits, growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures, multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types. Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.\n\n",
        "start": 2164
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R07.A1",
        "inferability_assumptions": "The tests call the existing observation API with its finite default. The full fixture setup at lines 31-65 establishes that context. Adaptation preserves caller semantics, not production caller behavior changes.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Both failure-injection sites are explicit in an eligible resource outside the filesystem tests.",
        "resources": [
          "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
        ],
        "support_spans": [
          {
            "address": "tests/context/repository/test_observation.py",
            "end": 1755,
            "end_line": 65,
            "quote": "_REPOSITORY_ID = \"00000000-0000-4000-8000-000000000001\"\n_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024\n\n\ndef _repository() -> Repository:\n    \"\"\"Return one deterministic logical Repository.\"\"\"\n    return Repository(RepositoryId.parse(_REPOSITORY_ID))\n\n\ndef _observe(\n    repository: Repository,\n    root: Path,\n    address: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe one fixture resource through the public boundary.\"\"\"\n    return observe_repository_resource(\n        repository=repository,\n        root=ResolvedPath(root),\n        address=RepositoryResourceAddress(address),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n\n\ndef _observe_many(\n    repository: Repository,\n    root: Path,\n    *addresses: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe an explicit fixture resource collection through the public boundary.\"\"\"\n    return observe_repository_resources(\n        repository=repository,\n        root=ResolvedPath(root),\n        addresses=tuple(RepositoryResourceAddress(value) for value in addresses),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n",
            "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
            "start": 672,
            "start_line": 31
          },
          {
            "address": "tests/context/repository/test_observation.py",
            "end": 14583,
            "end_line": 404,
            "quote": "def test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
            "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
            "start": 13790,
            "start_line": 384
          },
          {
            "address": "tests/context/repository/test_observation.py",
            "end": 17514,
            "end_line": 497,
            "quote": "def test_unreadable_and_undecodable_resources_do_not_produce_snapshots(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Read and UTF-8 decoding failures remain unsuccessful observations.\"\"\"\n    source = tmp_path / \"module.py\"\n    source.write_bytes(b\"content\")\n\n    def deny_read(_path: Path) -> bytes:\n        msg = \"denied\"\n        raise PermissionError(msg)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n    with pytest.raises(FilesystemPermissionError):\n        _observe(_repository(), tmp_path, \"module.py\")\n\n    monkeypatch.undo()\n    source.write_bytes(b\"\\xff\")\n    with pytest.raises(TextDecodingError):\n        _observe(_repository(), tmp_path, \"module.py\")\n",
            "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
            "start": 16810,
            "start_line": 478
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R07",
    "inferability_assumptions": "The tests call the existing observation API with its finite default. The full fixture setup at lines 31-65 establishes that context. Adaptation preserves caller semantics, not production caller behavior changes.",
    "necessity_rationale": "Without this information the finite acquisition change can invalidate existing caller regressions even if all filesystem tests are corrected.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 1755,
        "end_line": 65,
        "quote": "_REPOSITORY_ID = \"00000000-0000-4000-8000-000000000001\"\n_MAXIMUM_RESOURCE_BYTES = 16 * 1024 * 1024\n\n\ndef _repository() -> Repository:\n    \"\"\"Return one deterministic logical Repository.\"\"\"\n    return Repository(RepositoryId.parse(_REPOSITORY_ID))\n\n\ndef _observe(\n    repository: Repository,\n    root: Path,\n    address: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe one fixture resource through the public boundary.\"\"\"\n    return observe_repository_resource(\n        repository=repository,\n        root=ResolvedPath(root),\n        address=RepositoryResourceAddress(address),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n\n\ndef _observe_many(\n    repository: Repository,\n    root: Path,\n    *addresses: str,\n) -> RepositorySnapshot:\n    \"\"\"Observe an explicit fixture resource collection through the public boundary.\"\"\"\n    return observe_repository_resources(\n        repository=repository,\n        root=ResolvedPath(root),\n        addresses=tuple(RepositoryResourceAddress(value) for value in addresses),\n        maximum_resource_bytes=_MAXIMUM_RESOURCE_BYTES,\n    )\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 672,
        "start_line": 31
      },
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 14583,
        "end_line": 404,
        "quote": "def test_unreadable_multi_resource_prevents_a_snapshot(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A read failure for one required member fails the complete operation.\"\"\"\n    available = tmp_path / \"available.py\"\n    denied = tmp_path / \"denied.py\"\n    available.write_text(\"VALUE = 1\\n\", encoding=\"utf-8\")\n    denied.write_text(\"VALUE = 2\\n\", encoding=\"utf-8\")\n    original_read_bytes = Path.read_bytes\n\n    def deny_one(path: Path) -> bytes:\n        if path == denied:\n            msg = \"denied\"\n            raise PermissionError(msg)\n        return original_read_bytes(path)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_one)\n\n    with pytest.raises(FilesystemPermissionError):\n        _observe_many(_repository(), tmp_path, \"available.py\", \"denied.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 13790,
        "start_line": 384
      },
      {
        "address": "tests/context/repository/test_observation.py",
        "end": 17514,
        "end_line": 497,
        "quote": "def test_unreadable_and_undecodable_resources_do_not_produce_snapshots(\n    tmp_path: Path,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Read and UTF-8 decoding failures remain unsuccessful observations.\"\"\"\n    source = tmp_path / \"module.py\"\n    source.write_bytes(b\"content\")\n\n    def deny_read(_path: Path) -> bytes:\n        msg = \"denied\"\n        raise PermissionError(msg)\n\n    monkeypatch.setattr(Path, \"read_bytes\", deny_read)\n    with pytest.raises(FilesystemPermissionError):\n        _observe(_repository(), tmp_path, \"module.py\")\n\n    monkeypatch.undo()\n    source.write_bytes(b\"\\xff\")\n    with pytest.raises(TextDecodingError):\n        _observe(_repository(), tmp_path, \"module.py\")\n",
        "resource": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "start": 16810,
        "start_line": 478
      }
    ],
    "statement": "Two existing repository-observation permission tests also patch Path.read_bytes through finite filesystem reads, so preserving the ordinary caller regression suite requires adapting these injections.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R08.A1",
        "inferability_assumptions": "The task provides the replacement guarantee. Current document text is necessary only to know which claims and surrounding boundaries must be reconciled.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Current acquisition and adjacent limitation claims are explicit.",
        "resources": [
          "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/io.md",
            "end": 1171,
            "end_line": 38,
            "quote": "## Reading\n\n```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
            "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
            "start": 412,
            "start_line": 18
          },
          {
            "address": "src/devtools/resources/filesystem/docs/io.md",
            "end": 2499,
            "end_line": 80,
            "quote": "## Writing\n\n```python\nwrite(file, *, overwrite=True)\n```\n\nThe model's `format`, not the target suffix, selects its codec. Explicit model\nand codec matching prevents JSON, Markdown, and CSV TextFile subclasses from\nbeing encoded by TextCodec. Missing parent directories are not created.\n`overwrite=False` raises built-in `FileExistsError` when the destination exists.\n\nThe normal write lifecycle is:\n\n```text\nencode current model state\n    \u2193\ncreate sibling temporary file\n    \u2193\nrecord its path for cleanup\n    \u2193\nwrite, flush, fsync\n    \u2193\nos.replace(destination)\n    \u2193\nremove temporary file on failure\n```\n\nUnder normal local atomic-replace filesystem semantics, observers should see\neither the previous destination or the complete replacement, rather than a\npartially written destination. The temporary file is in the target directory,\nso replacement stays on that filesystem.\n\nThis is not a full crash transaction: the parent directory is not fsynced,\ndirectory-entry durability after sudden power loss is filesystem-dependent, and\nthere is no locking or concurrent-writer coordination.\n\n## Security boundaries\n\nI/O does not guarantee allowed-root containment, symlink-escape prevention,\npath authorization, TOCTOU elimination, ownership/permission policy, locking,\nor secure deletion. Those concerns are outside this package.\n",
            "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
            "start": 1172,
            "start_line": 40
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R08",
    "inferability_assumptions": "The task provides the replacement guarantee. Current document text is necessary only to know which claims and surrounding boundaries must be reconciled.",
    "necessity_rationale": "Accurate documentation requires reconciling these specific existing behavior claims, not adding a new guarantee beside contradictory text.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 1171,
        "end_line": 38,
        "quote": "## Reading\n\n```python\nread(path, *, file_format=None, max_bytes=16 * 1024 * 1024)\n```\n\n`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 412,
        "start_line": 18
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 2499,
        "end_line": 80,
        "quote": "## Writing\n\n```python\nwrite(file, *, overwrite=True)\n```\n\nThe model's `format`, not the target suffix, selects its codec. Explicit model\nand codec matching prevents JSON, Markdown, and CSV TextFile subclasses from\nbeing encoded by TextCodec. Missing parent directories are not created.\n`overwrite=False` raises built-in `FileExistsError` when the destination exists.\n\nThe normal write lifecycle is:\n\n```text\nencode current model state\n    \u2193\ncreate sibling temporary file\n    \u2193\nrecord its path for cleanup\n    \u2193\nwrite, flush, fsync\n    \u2193\nos.replace(destination)\n    \u2193\nremove temporary file on failure\n```\n\nUnder normal local atomic-replace filesystem semantics, observers should see\neither the previous destination or the complete replacement, rather than a\npartially written destination. The temporary file is in the target directory,\nso replacement stays on that filesystem.\n\nThis is not a full crash transaction: the parent directory is not fsynced,\ndirectory-entry durability after sudden power loss is filesystem-dependent, and\nthere is no locking or concurrent-writer coordination.\n\n## Security boundaries\n\nI/O does not guarantee allowed-root containment, symlink-escape prevention,\npath authorization, TOCTOU elimination, ownership/permission policy, locking,\nor secure deletion. Those concerns are outside this package.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 1172,
        "start_line": 40
      }
    ],
    "statement": "The I/O document currently claims complete read_bytes acquisition with pre/post checks and says streaming bounded reads are unimplemented; its write/security sections delimit unaffected claims.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R09.A1",
        "inferability_assumptions": "The overview is needed for its current public claims, not merely its filename.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "This is the current public overview and its limitation context.",
        "resources": [
          "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/overview.md",
            "end": 1036,
            "end_line": 23,
            "quote": "## Public API\n\nThe root package exports generic I/O (`read`, `write`, `resolve_file_format`,\nand `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file\nmodels, structured JSON/Markdown/CSV models, and filesystem errors. Internal\ncodec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain\nat the representation-model boundary rather than the root package.\n\n| Format   | Model | Codec | Generic read/write |\n|----------|------:|------:|-------------------:|\n| Binary   |   Yes |    No |                 No |\n| Text     |   Yes |   Yes |                Yes |\n| JSON     |   Yes |   Yes |                Yes |\n| CSV      |   Yes |   Yes |                Yes |\n| Markdown |   Yes |   Yes |                Yes |\n",
            "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
            "start": 294,
            "start_line": 9
          },
          {
            "address": "src/devtools/resources/filesystem/docs/overview.md",
            "end": 3247,
            "end_line": 100,
            "quote": "## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n\n## Errors\n\n```text\nFilesystemError\n\u251c\u2500\u2500 FilesystemNotFoundError\n\u251c\u2500\u2500 NotAFileError\n\u251c\u2500\u2500 FileTooLargeError\n\u251c\u2500\u2500 FilesystemPermissionError\n\u251c\u2500\u2500 TextDecodingError\n\u251c\u2500\u2500 TextEncodingError\n\u2514\u2500\u2500 FileFormatError\n```\n\n`FileExistsError` intentionally remains the built-in failure for\n`write(..., overwrite=False)`.\n\n## Limitations\n\nGeneric I/O does not provide containment, symlink-escape prevention,\nauthorization, race-free limits, locking, ownership policy, secure deletion,\nor parent-directory durability after power loss. See [io.md](io.md) for the\nexact read and write limits.\n\n## Future evolution\n\nConcrete deferred work is recorded in [roadmap.md](roadmap.md). It does not\nauthorize dynamic codec registries, plugin discovery, repository indexing, or\nfilesystem security policy.\n",
            "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
            "start": 2161,
            "start_line": 66
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R09",
    "inferability_assumptions": "The overview is needed for its current public claims, not merely its filename.",
    "necessity_rationale": "The requested overview update must distinguish the new acquisition guarantee from stronger excluded pathname/security guarantees within the existing public documentation.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 1036,
        "end_line": 23,
        "quote": "## Public API\n\nThe root package exports generic I/O (`read`, `write`, `resolve_file_format`,\nand `DEFAULT_MAX_READ_BYTES`), codecs, `File`/`FileFormat`, concrete file\nmodels, structured JSON/Markdown/CSV models, and filesystem errors. Internal\ncodec resolution remains private. JSON `freeze_json()` and `thaw_json()` remain\nat the representation-model boundary rather than the root package.\n\n| Format   | Model | Codec | Generic read/write |\n|----------|------:|------:|-------------------:|\n| Binary   |   Yes |    No |                 No |\n| Text     |   Yes |   Yes |                Yes |\n| JSON     |   Yes |   Yes |                Yes |\n| CSV      |   Yes |   Yes |                Yes |\n| Markdown |   Yes |   Yes |                Yes |\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 294,
        "start_line": 9
      },
      {
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "end": 3247,
        "end_line": 100,
        "quote": "## Boundaries\n\nThis package owns file models, codecs, format resolution, bounded reads,\natomic writes, and format-native access/search/transformation. It does not own\npath parsing, directory traversal, repository indexing, sessions, context\ncompilation, watching, synchronization, authorization, or sandbox policy.\n\n## Errors\n\n```text\nFilesystemError\n\u251c\u2500\u2500 FilesystemNotFoundError\n\u251c\u2500\u2500 NotAFileError\n\u251c\u2500\u2500 FileTooLargeError\n\u251c\u2500\u2500 FilesystemPermissionError\n\u251c\u2500\u2500 TextDecodingError\n\u251c\u2500\u2500 TextEncodingError\n\u2514\u2500\u2500 FileFormatError\n```\n\n`FileExistsError` intentionally remains the built-in failure for\n`write(..., overwrite=False)`.\n\n## Limitations\n\nGeneric I/O does not provide containment, symlink-escape prevention,\nauthorization, race-free limits, locking, ownership policy, secure deletion,\nor parent-directory durability after power loss. See [io.md](io.md) for the\nexact read and write limits.\n\n## Future evolution\n\nConcrete deferred work is recorded in [roadmap.md](roadmap.md). It does not\nauthorize dynamic codec registries, plugin discovery, repository indexing, or\nfilesystem security policy.\n",
        "resource": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "start": 2161,
        "start_line": 66
      }
    ],
    "statement": "The filesystem overview owns the public API inventory, supported-format table and limitations, including the current race-free-limits wording and a link to the detailed I/O contract.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R10.A1",
        "inferability_assumptions": "Future scope is not authorized by its presence in the roadmap; the task controls the narrower change.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The current roadmap separates several deferred scopes but groups bounded acquisition with streaming.",
        "resources": [
          "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/roadmap.md",
            "end": 1267,
            "end_line": 37,
            "quote": "This document records concrete evaluation areas, not committed implementation\nwork. See the current [overview](overview.md) and [I/O contract](io.md).\n\n## Binary I/O\n\nA BinaryCodec and explicit generic binary read/write policy may be justified.\nThis does not imply arbitrary binary format detection.\n\n## Strict bounded and streaming reads\n\nStreaming or chunk-bounded reads could enforce a hard memory bound where\ncurrent stat/read/post-check behavior is insufficient. Format-specific\nstreaming should be added only where consumers require it.\n\n## Source-format-preserving writes\n\nStructured JSON and CSV transformations currently serialize current state,\nnot original formatting. More faithful output could be evaluated if consumers\ndemonstrate a need; arbitrary round-trip fidelity is not promised.\n\n## Markdown source fidelity\n\nExact Markdown section source slices, and richer structure, may be justified\nonly by concrete consumers.\n\n## Format evaluation\n\nTOML, YAML, XML, and source-code models are candidates for future evaluation,\nnot commitments.\n\n## Explicit non-goals\n\nPlugin discovery, dynamic codec registries, filesystem authorization,\nsandbox policy, and repository indexing remain outside the immediate\nfilesystem roadmap.\n",
            "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
            "start": 31,
            "start_line": 3
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R10",
    "inferability_assumptions": "Future scope is not authorized by its presence in the roadmap; the task controls the narrower change.",
    "necessity_rationale": "The new feature must be removed from deferred scope without promoting streaming parsers or a decoded-memory guarantee. This requires the existing roadmap distinction.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "end": 1267,
        "end_line": 37,
        "quote": "This document records concrete evaluation areas, not committed implementation\nwork. See the current [overview](overview.md) and [I/O contract](io.md).\n\n## Binary I/O\n\nA BinaryCodec and explicit generic binary read/write policy may be justified.\nThis does not imply arbitrary binary format detection.\n\n## Strict bounded and streaming reads\n\nStreaming or chunk-bounded reads could enforce a hard memory bound where\ncurrent stat/read/post-check behavior is insufficient. Format-specific\nstreaming should be added only where consumers require it.\n\n## Source-format-preserving writes\n\nStructured JSON and CSV transformations currently serialize current state,\nnot original formatting. More faithful output could be evaluated if consumers\ndemonstrate a need; arbitrary round-trip fidelity is not promised.\n\n## Markdown source fidelity\n\nExact Markdown section source slices, and richer structure, may be justified\nonly by concrete consumers.\n\n## Format evaluation\n\nTOML, YAML, XML, and source-code models are candidates for future evaluation,\nnot commitments.\n\n## Explicit non-goals\n\nPlugin discovery, dynamic codec registries, filesystem authorization,\nsandbox policy, and repository indexing remain outside the immediate\nfilesystem roadmap.\n",
        "resource": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "start": 31,
        "start_line": 3
      }
    ],
    "statement": "The filesystem roadmap currently groups strict bounded reads with future streaming and a hard-memory-bound suggestion, while separately deferring binary and new-format work.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R11.A1",
        "inferability_assumptions": "This location is necessary because the current text establishes a distinct stale public documentation surface; implementation ownership alone would not make it necessary.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The public callable docstring contains the outdated acquisition claim.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 1608,
            "end_line": 49,
            "quote": "    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n\n    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n\n    :param path: Resolved path to the file.\n    :param file_format: Explicit file format override.\n    :param max_bytes: Maximum permitted file size, or ``None`` for no limit.\n    :returns: Decoded file model.\n    :raises FilesystemNotFoundError: If the target does not exist.\n    :raises NotAFileError: If the target is not a regular file.\n    :raises FileTooLargeError: If the file exceeds ``max_bytes``.\n    :raises FilesystemPermissionError: If filesystem access is denied.\n    \"\"\"\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 717,
            "start_line": 32
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R11",
    "inferability_assumptions": "This location is necessary because the current text establishes a distinct stale public documentation surface; implementation ownership alone would not make it necessary.",
    "necessity_rationale": "The conditional public-API documentation update is applicable because the callable itself contains a behavior statement invalidated by the new acquisition algorithm.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 1608,
        "end_line": 49,
        "quote": "    \"\"\"Read a filesystem file into its rich file model.\n\n    When ``file_format`` is omitted, the format is inferred from the path.\n    An explicit format overrides suffix-based inference.\n\n    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n\n    :param path: Resolved path to the file.\n    :param file_format: Explicit file format override.\n    :param max_bytes: Maximum permitted file size, or ``None`` for no limit.\n    :returns: Decoded file model.\n    :raises FilesystemNotFoundError: If the target does not exist.\n    :raises NotAFileError: If the target is not a regular file.\n    :raises FileTooLargeError: If the file exceeds ``max_bytes``.\n    :raises FilesystemPermissionError: If filesystem access is denied.\n    \"\"\"\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 717,
        "start_line": 32
      }
    ],
    "statement": "The public read docstring currently warns that grown contents can be read into memory before the post-check rejects them.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R12.A1",
        "inferability_assumptions": "The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "The script passes only the test root and ignore argument into pytest; configuration therefore remains in force.",
        "resources": [
          "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a"
        ],
        "support_spans": [
          {
            "address": "scripts/validate_development.py",
            "end": 657,
            "end_line": 23,
            "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n",
            "resource": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
            "start": 248,
            "start_line": 14
          }
        ]
      },
      {
        "id": "R12.A3",
        "inferability_assumptions": "The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The operating policy states the exact invocation, pre-collection exclusion and retention of configured coverage.",
        "resources": [
          "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
        ],
        "support_spans": [
          {
            "address": "AGENTS.md",
            "end": 11282,
            "end_line": 239,
            "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
            "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
            "start": 10713,
            "start_line": 228
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R12",
    "inferability_assumptions": "The script/test alternatives combine with R13 for actual coverage configuration. These alternatives establish the required existing profile contract, not the unseen validation document wording.",
    "necessity_rationale": "The profile cannot be reconstructed from the future request alone; its existing exclusion must be preserved, and the current policy must not be weakened.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "scripts/validate_development.py",
        "end": 657,
        "end_line": 23,
        "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n",
        "resource": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "start": 248,
        "start_line": 14
      },
      {
        "address": "AGENTS.md",
        "end": 11282,
        "end_line": 239,
        "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 10713,
        "start_line": 228
      }
    ],
    "statement": "The protected development entry point runs ordinary tests while excluding tests/experiments before collection, retaining the configured coverage behavior.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R13.A1",
        "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The configuration is the authoritative current tool setup.",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
        ],
        "support_spans": [
          {
            "address": "pyproject.toml",
            "end": 1031,
            "end_line": 55,
            "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n",
            "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
            "start": 585,
            "start_line": 34
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R13",
    "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
    "necessity_rationale": "Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "pyproject.toml",
        "end": 1031,
        "end_line": 55,
        "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 585,
        "start_line": 34
      }
    ],
    "statement": "Pytest uses strict config/markers and devtools branch coverage; pytest and coverage reporting retain a 100% requirement.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R14.A1",
        "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The configuration is the authoritative current tool setup.",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
        ],
        "support_spans": [
          {
            "address": "pyproject.toml",
            "end": 1227,
            "end_line": 71,
            "quote": "[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n",
            "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
            "start": 1032,
            "start_line": 57
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R14",
    "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
    "necessity_rationale": "Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "pyproject.toml",
        "end": 1227,
        "end_line": 71,
        "quote": "[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 1032,
        "start_line": 57
      }
    ],
    "statement": "Ruff targets Python 3.12 with line length 88, selects ALL rules with D203/D213 ignored and S101 ignored in tests.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R15.A1",
        "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The configuration is the authoritative current tool setup.",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
        ],
        "support_spans": [
          {
            "address": "pyproject.toml",
            "end": 1368,
            "end_line": 78,
            "quote": "[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
            "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
            "start": 1228,
            "start_line": 73
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R15",
    "inferability_assumptions": "The task requires running the profile during implementation; this adjudication validates its own artifacts only and does not execute the captured repository.",
    "necessity_rationale": "Preserving configured exclusions and coverage and invoking the requested checks requires these current settings rather than guessed validation defaults.",
    "obligations": [
      "O6"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "pyproject.toml",
        "end": 1368,
        "end_line": 78,
        "quote": "[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 1228,
        "start_line": 73
      }
    ],
    "statement": "Mypy is strict for Python 3.12, checks src/tests/experiments, enables explicit package bases and uses src as its search path.",
    "task_support": [
      {
        "end": 3315,
        "quote": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
        "start": 2742
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R16.A1",
        "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The implementation defines the signature and both checks.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 1121,
            "end_line": 39,
            "quote": "    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 907,
            "start_line": 37
          },
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 2542,
            "end_line": 82,
            "quote": "        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 1922,
            "start_line": 61
          }
        ]
      },
      {
        "id": "R16.A2",
        "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "The I/O contract independently states the callable shape, defaults, limit meanings and allocation-before-rejection behavior.",
        "resources": [
          "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/docs/io.md",
            "end": 1171,
            "end_line": 38,
            "quote": "`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
            "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
            "start": 499,
            "start_line": 24
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R16",
    "inferability_assumptions": "The preservation task supplies the desired zero/exact behavior. The documentation alternative establishes current public contract and acquisition order without pretending to establish internal helper names or Python annotations.",
    "necessity_rationale": "These current compatibility and acquisition facts identify what changes and what must be preserved; the task alone is not proof of the existing implementation.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 1121,
        "end_line": 39,
        "quote": "    The file is size-checked before loading and again after reading. A file\n    that grows between those checks can still be read into memory before the\n    second check rejects it; no oversized model is returned.\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 907,
        "start_line": 37
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2542,
        "end_line": 82,
        "quote": "        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=size_bytes,\n        max_bytes=max_bytes,\n    )\n\n    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n\n    _validate_read_size(\n        path,\n        size_bytes=len(content),\n        max_bytes=max_bytes,\n    )\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1922,
        "start_line": 61
      },
      {
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "end": 1171,
        "end_line": 38,
        "quote": "`read()` requires a `ResolvedPath` to an existing regular file. It checks the\nreported size before a complete `read_bytes()`, checks the loaded size again,\nresolves the codec, and returns the rich concrete model. `max_bytes=None`\ndisables the limit; negative values raise `ValueError`. Permission failures\nnormalize to `FilesystemPermissionError`.\n\nThe default is 16 MiB. Its bound is intentionally not race-free:\n\n```text\nstat \u2192 pre-read check \u2192 read_bytes() \u2192 post-read check\n```\n\nA growing file is rejected after the second check and no oversized model is\nreturned, but its grown contents can be allocated before rejection. Streaming\nbounded reads are not implemented.\n",
        "resource": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "start": 499,
        "start_line": 24
      }
    ],
    "statement": "The current acquisition performs a preliminary stat, complete read_bytes and a post-read size check, allowing grown content allocation before rejection.",
    "task_support": [
      {
        "end": 629,
        "quote": "O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.\n\n",
        "start": 89
      }
    ]
  },
  {
    "alternatives": [
      {
        "id": "R17.A1",
        "inferability_assumptions": "No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Control flow and raise-from statements establish current error precedence and causal normalization.",
        "resources": [
          "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
        ],
        "support_spans": [
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 2124,
            "end_line": 64,
            "quote": "    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 1633,
            "start_line": 52
          },
          {
            "address": "src/devtools/resources/filesystem/reading.py",
            "end": 2434,
            "end_line": 76,
            "quote": "    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
            "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
            "start": 2231,
            "start_line": 72
          }
        ]
      }
    ],
    "evidence_class": "REPOSITORY_SUPPORTED",
    "id": "R17",
    "inferability_assumptions": "No new promise is inferred for disappearance after the preliminary checks, OSError subclasses other than PermissionError, or adversarial pathname changes.",
    "necessity_rationale": "The new stream operations must preserve current domain boundaries and placement of catches; the task prescribes new catches but not the current sequencing.",
    "obligations": [
      "O4"
    ],
    "provenance": {
      "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
      "kind": "eligible_repository_text",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
    },
    "repository_support": [
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2124,
        "end_line": 64,
        "quote": "    try:\n        if not source.exists():\n            msg = f\"Filesystem path does not exist: {path}.\"\n            raise FilesystemNotFoundError(msg)\n\n        if not source.is_file():\n            msg = f\"Filesystem path is not a regular file: {path}.\"\n            raise NotAFileError(msg)\n\n        size_bytes = source.stat().st_size\n    except PermissionError as error:\n        msg = f\"Permission denied while inspecting file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 1633,
        "start_line": 52
      },
      {
        "address": "src/devtools/resources/filesystem/reading.py",
        "end": 2434,
        "end_line": 76,
        "quote": "    try:\n        content = source.read_bytes()\n    except PermissionError as error:\n        msg = f\"Permission denied while reading file: {path}.\"\n        raise FilesystemPermissionError(msg) from error\n",
        "resource": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "start": 2231,
        "start_line": 72
      }
    ],
    "statement": "The current reader translates inspection/read PermissionError to FilesystemPermissionError using raise-from causal exceptions.",
    "task_support": [
      {
        "end": 2164,
        "quote": "O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.\n\n",
        "start": 1680
      }
    ]
  },
  {
    "alternatives": [],
    "evidence_class": "TASK_BACKED",
    "id": "T25",
    "inferability_assumptions": "The original task is normative for desired behavior, not evidence that the current implementation already behaves this way.",
    "necessity_rationale": "This is a mandatory prescribed future requirement; omitting it permits an implementation that violates the quoted clause.",
    "obligations": [
      "O1"
    ],
    "provenance": {
      "kind": "original_task",
      "task_identity": "case-0015-strict-bounded-filesystem-read-v1"
    },
    "repository_support": [],
    "statement": "Preserve the complete limit-value domain: 16 MiB default, None unbounded, negative rejection, zero and exact boundary.",
    "task_support": [
      {
        "end": 520,
        "quote": "including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary.",
        "start": 370
      }
    ]
  }
]
```

## All minimal witnesses

```json
{
  "O1": [
    {
      "id": "O1.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
      ],
      "unit_support": {
        "R01": [
          "R01.A2"
        ],
        "R16": [
          "R16.A2"
        ]
      },
      "units": [
        "R01",
        "R16",
        "T01",
        "T02",
        "T03",
        "T25"
      ]
    },
    {
      "id": "O1.W2",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
      ],
      "unit_support": {
        "R01": [
          "R01.A1"
        ],
        "R16": [
          "R16.A1"
        ]
      },
      "units": [
        "R01",
        "R16",
        "T01",
        "T02",
        "T03",
        "T25"
      ]
    }
  ],
  "O2": [
    {
      "id": "O2.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [],
      "unit_support": {},
      "units": [
        "T04",
        "T05",
        "T06",
        "T07",
        "T08"
      ]
    }
  ],
  "O3": [
    {
      "id": "O3.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      "unit_support": {
        "R02": [
          "R02.A1"
        ],
        "R03": [
          "R03.A1"
        ]
      },
      "units": [
        "R02",
        "R03",
        "T09",
        "T10",
        "T11",
        "T12",
        "T13"
      ]
    },
    {
      "id": "O3.W2",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42"
      ],
      "unit_support": {
        "R02": [
          "R02.A1"
        ],
        "R03": [
          "R03.A2"
        ]
      },
      "units": [
        "R02",
        "R03",
        "T09",
        "T10",
        "T11",
        "T12",
        "T13"
      ]
    }
  ],
  "O4": [
    {
      "id": "O4.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      "unit_support": {
        "R03": [
          "R03.A1"
        ],
        "R04": [
          "R04.A1"
        ],
        "R05": [
          "R05.A1"
        ],
        "R17": [
          "R17.A1"
        ]
      },
      "units": [
        "R03",
        "R04",
        "R05",
        "R17",
        "T14",
        "T15",
        "T16"
      ]
    },
    {
      "id": "O4.W2",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      "unit_support": {
        "R03": [
          "R03.A1"
        ],
        "R04": [
          "R04.A1"
        ],
        "R05": [
          "R05.A2"
        ],
        "R17": [
          "R17.A1"
        ]
      },
      "units": [
        "R03",
        "R04",
        "R05",
        "R17",
        "T14",
        "T15",
        "T16"
      ]
    },
    {
      "id": "O4.W3",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42"
      ],
      "unit_support": {
        "R03": [
          "R03.A2"
        ],
        "R04": [
          "R04.A1"
        ],
        "R05": [
          "R05.A1"
        ],
        "R17": [
          "R17.A1"
        ]
      },
      "units": [
        "R03",
        "R04",
        "R05",
        "R17",
        "T14",
        "T15",
        "T16"
      ]
    },
    {
      "id": "O4.W4",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
      ],
      "unit_support": {
        "R03": [
          "R03.A2"
        ],
        "R04": [
          "R04.A1"
        ],
        "R05": [
          "R05.A2"
        ],
        "R17": [
          "R17.A1"
        ]
      },
      "units": [
        "R03",
        "R04",
        "R05",
        "R17",
        "T14",
        "T15",
        "T16"
      ]
    }
  ],
  "O5": [
    {
      "id": "O5.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
      ],
      "unit_support": {
        "R06": [
          "R06.A1"
        ]
      },
      "units": [
        "R06",
        "T17",
        "T18",
        "T19",
        "T20"
      ]
    }
  ],
  "O6": [
    {
      "id": "O6.W1",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df"
      ],
      "unit_support": {
        "R07": [
          "R07.A1"
        ],
        "R08": [
          "R08.A1"
        ],
        "R09": [
          "R09.A1"
        ],
        "R10": [
          "R10.A1"
        ],
        "R11": [
          "R11.A1"
        ],
        "R12": [
          "R12.A1"
        ],
        "R13": [
          "R13.A1"
        ],
        "R14": [
          "R14.A1"
        ],
        "R15": [
          "R15.A1"
        ]
      },
      "units": [
        "R07",
        "R08",
        "R09",
        "R10",
        "R11",
        "R12",
        "R13",
        "R14",
        "R15",
        "T21",
        "T22",
        "T23",
        "T24"
      ]
    },
    {
      "id": "O6.W2",
      "minimality_rationale": "Every required unit is covered; removing any repository resource leaves at least one repository unit without a complete support alternative. Task-backed units require no repository resource.",
      "resources": [
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
      ],
      "unit_support": {
        "R07": [
          "R07.A1"
        ],
        "R08": [
          "R08.A1"
        ],
        "R09": [
          "R09.A1"
        ],
        "R10": [
          "R10.A1"
        ],
        "R11": [
          "R11.A1"
        ],
        "R12": [
          "R12.A3"
        ],
        "R13": [
          "R13.A1"
        ],
        "R14": [
          "R14.A1"
        ],
        "R15": [
          "R15.A1"
        ]
      },
      "units": [
        "R07",
        "R08",
        "R09",
        "R10",
        "R11",
        "R12",
        "R13",
        "R14",
        "R15",
        "T21",
        "T22",
        "T23",
        "T24"
      ]
    }
  ]
}
```

## Obligation intersections

```json
{
  "O1": {
    "resources": [],
    "units": [
      "R01",
      "R16",
      "T01",
      "T02",
      "T03",
      "T25"
    ]
  },
  "O2": {
    "resources": [],
    "units": [
      "T04",
      "T05",
      "T06",
      "T07",
      "T08"
    ]
  },
  "O3": {
    "resources": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
    ],
    "units": [
      "R02",
      "R03",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13"
    ]
  },
  "O4": {
    "resources": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40"
    ],
    "units": [
      "R03",
      "R04",
      "R05",
      "R17",
      "T14",
      "T15",
      "T16"
    ]
  },
  "O5": {
    "resources": [
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
    ],
    "units": [
      "R06",
      "T17",
      "T18",
      "T19",
      "T20"
    ]
  },
  "O6": {
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df"
    ],
    "units": [
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "T21",
      "T22",
      "T23",
      "T24"
    ]
  }
}
```

## All task combinations

```json
[
  {
    "id": "TC001",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W1",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC002",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W1",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC003",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W2",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC004",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W2",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC005",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W3",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC006",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W3",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC007",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W4",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC008",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W1",
      "O4.W4",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC009",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W1",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC010",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W1",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC011",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W2",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC012",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W2",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC013",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W3",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC014",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W3",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC015",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W4",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC016",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W1",
      "O2.W1",
      "O3.W2",
      "O4.W4",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC017",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W1",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC018",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W1",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC019",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W2",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC020",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W2",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC021",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W3",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC022",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W3",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC023",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W4",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC024",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W1",
      "O4.W4",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC025",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W1",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC026",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W1",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC027",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W2",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC028",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W2",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC029",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W3",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC030",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W3",
      "O5.W1",
      "O6.W2"
    ]
  },
  {
    "id": "TC031",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W4",
      "O5.W1",
      "O6.W1"
    ]
  },
  {
    "id": "TC032",
    "resources": [
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
    ],
    "units": [
      "R01",
      "R02",
      "R03",
      "R04",
      "R05",
      "R06",
      "R07",
      "R08",
      "R09",
      "R10",
      "R11",
      "R12",
      "R13",
      "R14",
      "R15",
      "R16",
      "R17",
      "T01",
      "T02",
      "T03",
      "T04",
      "T05",
      "T06",
      "T07",
      "T08",
      "T09",
      "T10",
      "T11",
      "T12",
      "T13",
      "T14",
      "T15",
      "T16",
      "T17",
      "T18",
      "T19",
      "T20",
      "T21",
      "T22",
      "T23",
      "T24",
      "T25"
    ],
    "witnesses": [
      "O1.W2",
      "O2.W1",
      "O3.W2",
      "O4.W4",
      "O5.W1",
      "O6.W2"
    ]
  }
]
```

## All sufficient resource unions

```json
[
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ]
]
```

## All inclusion-minimal resource unions

```json
[
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
  ],
  [
    "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
    "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
    "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
    "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
    "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
  ]
]
```

## Sufficient unit structure

```json
[
  [
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R08",
    "R09",
    "R10",
    "R11",
    "R12",
    "R13",
    "R14",
    "R15",
    "R16",
    "R17",
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T08",
    "T09",
    "T10",
    "T11",
    "T12",
    "T13",
    "T14",
    "T15",
    "T16",
    "T17",
    "T18",
    "T19",
    "T20",
    "T21",
    "T22",
    "T23",
    "T24",
    "T25"
  ]
]
```

## Task indispensable resources

```json
[
  "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
  "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
  "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
  "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
  "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
  "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
  "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33"
]
```

## Task indispensable units

```json
[
  "R01",
  "R02",
  "R03",
  "R04",
  "R05",
  "R06",
  "R07",
  "R08",
  "R09",
  "R10",
  "R11",
  "R12",
  "R13",
  "R14",
  "R15",
  "R16",
  "R17",
  "T01",
  "T02",
  "T03",
  "T04",
  "T05",
  "T06",
  "T07",
  "T08",
  "T09",
  "T10",
  "T11",
  "T12",
  "T13",
  "T14",
  "T15",
  "T16",
  "T17",
  "T18",
  "T19",
  "T20",
  "T21",
  "T22",
  "T23",
  "T24",
  "T25"
]
```

## All gaps

```json
{
  "REPOSITORY_INFORMATION_GAP": [],
  "TASK_GAP": [],
  "TASK_INTERPRETATION_GAP": []
}
```

## All limitations

```json
[
  {
    "blocking": false,
    "id": "L01",
    "statement": "The exact text of docs/development/validation.md is absent from the 515-resource frame. The required current profile semantics are established independently by the operating guide, script, its tests and project configuration; no missing fact is necessary to decide this case.",
    "support": [
      {
        "address": "AGENTS.md",
        "end": 11282,
        "end_line": 239,
        "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
        "resource": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 10713,
        "start_line": 228
      },
      {
        "address": "scripts/validate_development.py",
        "end": 657,
        "end_line": 23,
        "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n",
        "resource": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "start": 248,
        "start_line": 14
      },
      {
        "address": "pyproject.toml",
        "end": 1368,
        "end_line": 78,
        "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n\n[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n\n[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
        "resource": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 585,
        "start_line": 34
      }
    ]
  },
  {
    "blocking": false,
    "id": "L02",
    "statement": "Chunk size, accumulator/helper decomposition and instrumented-stream fixture shape are implementation choices. The task supplies their acceptance constraints and does not freeze names.",
    "task_support": [
      {
        "end": 847,
        "quote": "bound individual read requests",
        "start": 817
      },
      {
        "end": 2740,
        "quote": "Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.",
        "start": 2577
      }
    ]
  },
  {
    "blocking": false,
    "id": "L03",
    "statement": "Exact file content and source-byte metadata must be preserved; derived logical lines or Markdown section content need not reproduce raw newline separators. Tests must assert the correct representation layer.",
    "support": [
      {
        "address": "src/devtools/resources/filesystem/models/text.py",
        "end": 1767,
        "end_line": 66,
        "quote": "    @property\n    def lines(self) -> tuple[str, ...]:\n        \"\"\"Return immutable logical lines.\n\n        :returns: Logical lines without newline separators.\n        \"\"\"\n        return tuple(self.content.splitlines())\n",
        "resource": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "start": 1549,
        "start_line": 60
      },
      {
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "end": 1323,
        "end_line": 28,
        "quote": "A section starts at its owning heading and ends immediately before the next\nheading of the same or higher level. Lower-level headings remain in the parent\nsection. Boundaries use one-based inclusive lines.\n\n`MarkdownSection.content` excludes the heading line and is normalized logical\nsource: `splitlines()` plus `\"\\n\"` joining means CRLF becomes logical newline\ntext and final-newline/exact source-slice fidelity is not retained.\n",
        "resource": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "start": 892,
        "start_line": 22
      }
    ]
  }
]
```

## Preserved ambiguity

```json
[
  {
    "blocking": false,
    "id": "A01",
    "resolution": "Preserve the strict byte-acquisition requirement and document its layer; do not weaken it into a stat-only or returned-model-size limit.",
    "statement": "The task does not select the stream buffering layer or transient buffer strategy. A defensible implementation can use bounded binary requests and an unbuffered stream to avoid hidden acquisition beyond the sentinel. No process-memory, operating-system prefetch or stable-snapshot claim is inferred."
  }
]
```
