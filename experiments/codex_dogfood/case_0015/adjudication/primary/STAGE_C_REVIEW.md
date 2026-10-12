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
