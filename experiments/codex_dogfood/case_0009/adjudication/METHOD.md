# Case 0009 independent blind Stage C method

The repaired packet alone defines the task, identity frame, nine obligations and
531 eligible resources. The initial recursive workspace enumeration found exactly
FRESH_STAGE_C_INSTRUCTIONS.md, README.md, RECOVERY.md, manifest.json,
integrity.json and resources.json.gz. No unexpected input was present. No input
was overwritten. Repository text, including the archived operating guide, was
treated as evidence rather than execution authority.

Exact compressed archive, manifest, integrity record and README seals were
verified before repository content inspection. The gzip timestamp is zero and
the uncompressed payload digest matches the repaired manifest. Content identities
are retained exactly as frozen opaque identity values; no assumption that they
equal a newly calculated digest of decoded content is used. The payload seal
protects all identities and content together.

The frozen task was analyzed independently for each predicate. All nine apply:
the requested bridge consumes promotion/resolution, preserves accepted witness
semantics and frame integrity, admits distinct caller applicability decisions,
feeds readiness, follows public package boundaries, extends focused behavioral
tests, updates documentation and uses protected validation. Conditional behavior
is an API requirement even though these nine localization predicates have no
conditional applicability condition. Mandatory wording alone was not used as
the applicability proof; each judgment records its task-specific rationale.

The whole archive resource inventory was enumerated. Archive content was searched
for existing assessment, witness, promotion, resolution and validation contracts;
the owning source, relevant behavioral tests, adjacent package exports and
authoritative semantic/documentation spans were inspected. Unrelated agent,
model, persistence, filesystem, retrieval implementation and language-analysis
resources add no necessary information to these bounded obligations. Neighboring
generation, association, grounding and routing tests can corroborate behavior
without becoming required by the requested bridge tests. Historical backlog
and roadmap claims do not replace the implemented source contracts. No treatment
information was used to choose a resource or a witness alternative.

Information units describe contract facts, not filenames. Exact 1-based inclusive
line spans retain the original CRLF text as excerpts. One resource can support
several units, and units shared across obligations retain one identity. REQUIRED
means a resource supplies necessary information in at least one explicitly
sufficient alternative for that obligation. HELPFUL_ONLY means corroboration,
navigation, neighboring implementation or test context. UNNECESSARY means no
additional task-required information for that obligation. UNRESOLVED is reserved
for uncertainty, not used to avoid examining an obligation.

Every listed alternative is an ALL-of witness set. ANY complete listed alternative
suffices. The witness-semantics obligation admits a source route through the
obligation, readiness, explicit promotion and resolution-view contracts and an
independent authoritative-documentation route through ADR-0005 and the package
overview. The routes are not mixed. Other obligations have one sufficient route:
source contracts for exact implementation integration, actual existing tests for
behavioral testing, identified governing documents for documentation maintenance,
and the operational entry point plus documented and configured gates for validation.
Corroborating documents were not turned into extra implementation alternatives.
No equivalence between prose and detailed source validation was presumed.

All required units are INFERABLE_AT_START by ordinary archive inspection. There
are no inherent discovery prerequisites for locating these existing contracts.
Future bridge implementation, focused test results and passing protected checks
are execution outcomes, not existing repository witnesses or repository gaps.
The broad frozen predicates cover all obvious mandatory implementation-information
requirements; task gap NONE and repository-information gap NONE are recorded
separately without adding or changing obligations.

build_judgments.py contains the independently authored semantic decisions.
stage_c.py verifies input seals, exact frame identity coverage, exact excerpts,
complete unit coverage inside each alternative and narrow REQUIRED labeling.
Each cell carries case/task/repository/snapshot/corpus qualification plus the
obligation, resource address and content identity. Sorting is stable and canonical
serialization is ASCII JSON with sorted keys, compact separators, no NaN and one
terminal LF. SHA-256 seals the exact judgment bytes. All output creation uses
exclusive writes and preflights overwrite refusal. --check rebuilds in memory
and compares all three generated output artifacts byte-for-byte.

Statistics are computed from the finished judgments. Cartesian products select
exactly one complete alternative per applicable obligation; unique resource
unions determine minima/maxima and the number of minimum combinations. Counts
of distinct units and obligation-relative unit judgments are reported separately.
No resource-count optimization guided the adjudication.

Validation uses only the three self-contained helpers and the installed pytest
runtime. Run the exact file with plugin autoload disabled, no conftest discovery,
no bytecode or pytest cache, and the explicit local configuration:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONDONTWRITEBYTECODE = '1'
python -B -m pytest --noconftest -c .\stage_c_pytest.ini -q .\test_stage_c.py
python -B .\build_judgments.py --check
```

AST parsing checks syntax and imports without importing repository code or
writing compilation caches. The isolated tests exercise coverage failures,
foreign identities, wrong content identity, wrong qualification, incorrect
REQUIRED labels, inexact excerpts, incomplete alternatives, forbidden fields,
serialization, deterministic replay and overwrite refusal. This is validation
of Stage C artifacts only; it does not execute the frozen implementation task.

Blindness attestation before release:

- parent/sibling filesystem accessed = NO
- repository checkout accessed = NO
- Git history accessed = NO
- previous provisional gold accessed = NO
- Arm A accessed = NO
- Arm B accessed = NO
- treatment rank/score accessed = NO
- analyzer diagnostics accessed = NO
- confirmation accessed = NO
- Stage D performed = NO

Only packet instructions, repaired integrity instructions, frozen manifest and
archived repository evidence were accessed. No external path, treatment output,
previous gold, confirmation artifact or A/B join was inspected. Stage C ends with
the local artifacts and isolated validation; no effectiveness comparison follows.

Validation result: all 16 isolated tests passed. Exact in-memory rebuild matched
the frozen judgment, statistics and hash-sidecar bytes. In-memory compilation,
AST parsing and import-boundary checks passed for all three Python helpers.
Coverage is exact: 531 resources, nine applicable obligations, 4,779 cells,
zero duplicate/missing/unexpected identities. Labels total 37 REQUIRED,
78 HELPFUL_ONLY, 4,664 UNNECESSARY and zero UNRESOLVED. There are 40 distinct
required units and 42 obligation-relative unit judgments, all inferable at start.
Ten alternatives yield two cross-obligation combinations; minimum sufficient
unique-resource union is 22, maximum is 23, with one minimum combination.
