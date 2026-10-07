# Case 0010 independent blind Stage C method

This adjudication uses only the five original files in this sterile directory.
The frozen manifest supplies the exact task, predicates and frame. No task
semantics were taken from the surrounding prompt or outside repository knowledge.
The archived source and current documentation/tests supply repository truth;
the proposed implementation and its future tests or validation results are not
witnesses. No repository implementation was attempted.

## Sterility and integrity

Before reading the packet, the current directory was recursively enumerated,
including hidden entries, attributes and link information. Exactly the five
expected regular files were present. There were no directories, Git entries,
symlinks, junctions/reparse points, treatment outputs or prior judgments.
No parent or sibling path was enumerated or inspected.

The archive hash was verified before decompression. The uncompressed byte hash
was verified before semantic inspection. Every file binding in integrity.json
was checked. The integrity record itself is additionally pinned in stage_c.py.
Manifest/archive identity bindings match exactly for repository, snapshot and
corpus. All 531 retained resource content identities were independently verified
using the archive's decoded-UTF-8-text, length-framed SHA-256 semantics, along
with their UTF-8 byte sizes. This content identity is distinct from a raw UTF-8
byte digest; source supports preserve both.

The sealed archive defines the expected native resource identities. The manifest
supplies counts, not a second independent address list. Native addresses are
qualified by the frozen repository and snapshot; content identity remains an
independent binding. Expected addresses were checked for duplicates. The
observed gold resource frame and every obligation/resource cell were compared
against that complete sealed frame. Missing and unexpected identities are zero.

The initial sterility check is a recorded pre-generation check. Replays allow
only the original inputs, eight named outputs, and explicitly named runtime
caches created by this work. Tests use an explicit local temporary directory.

## Semantic decisions

The manifest freezes ten mandatory predicates. It has no separate satisfaction
criteria fields or conditional applicability clauses. No additional frozen
criteria or conditions were invented. Each predicate was evaluated against the
complete manifest task; all ten apply. The output preserves each original
obligation object and records APPLICABLE with a null frozen condition and an
explanation. Mandatory authoring alone was not used as the applicability test.

The complete resource address frame was reviewed and all archived content was
screened mechanically for the relevant planning, extraction, line-boundary and
validation contracts. Relevant source, tests and documentation were inspected
in detail. Current code/tests establish concrete behavior; package documentation
identifies the implemented owner; architecture/taxonomy provide governing
distinctions; the documentation map defines authority and update workflow.
Historical research, experiments and adjacent domains were not treated as
additional implementation authority. Links to unavailable external records
were not followed. Incidental references in frozen documentation were not
followed into experiments or used as outcomes.

The REQUIRED units are fine-grained contract facts, not files to edit. A source
resource may support several units and obligations. Sharing a resource does not
merge the obligations. Forty distinct units produce 45 obligation-relative unit
judgments. Every unit is inferable through ordinary inspection at task start;
none requires an inherent discovery prerequisite.

Important distinctions retained in the decisions:

- Common Planning owns explicit representations and realization. The native
  Python option adapts to Planning; common Planning must not gain a Python
  dependency merely for an additional language-independent resource form.
- Retained snapshot content is the source. Existing decoding preserves newline
  characters, while logical-line and Markdown projections omit or normalize
  them. These normalized projections are useful cautions, not exact-text witnesses.
- Existing Python extraction uses exclusive UTF-8 byte-column coordinates.
  That local parser contract is not the requested inclusive whole-line choice.
  It supplies preservation and defensive bounds contracts, not future feature code.
- Choice identity, plan identity and realized identity are separate. Plan order,
  explicit purpose and preceding-plan lineage remain part of their existing
  contracts. No model comprehension or current availability is inferred from lineage.
- Foreign repository, foreign snapshot, missing occurrence and unequal retained
  occurrence are distinguishable current frame failures. Materialization checks
  the frame again; it does not acquire replacement text or select another option.
- Common materialized items retain native provenance independently of rendered
  text. The existing Python adapter establishes coexistence without requiring
  the entire Python semantic-resolution implementation for this new choice.
- Rendering preserves item order and exact item text. Assembly copies an existing
  ModelRequest with only Prompt replaced, preserving its role and every other field.
- Public Planning and Context facades are relevant. Unrelated package initializers
  do not become necessary because they exist.
- Concrete common-plan and exact-source tests establish the needed preservation,
  rejection and assembly contracts. Generic neighboring tests are not mandatory.
- Protected development validation is a contract to follow in the future repository
  task. It was read as frozen text and was not executed in this sterile workspace.

## Witnesses and labels

For a unit, every support includes a snapshot-qualified native address, exact
content identity, character offsets, one-based line spans, exact excerpt,
excerpt SHA-256 and raw resource UTF-8 SHA-256. Offsets apply to the exact archived
string, including its retained carriage returns; they are not offsets into a
normalized working copy. Each excerpt, digest and content binding is mechanically
validated against the frozen archive.

All members within an alternative are complementary ALL requirements, including
all selected support spans for a member. ANY one complete alternative satisfies
that obligation. No members from competing alternatives are combined into a
manufactured alternative. Three current documents independently state the same
Planning ownership: its package overview, current architecture, and documentation
map. Ownership and package obligations each preserve those three adequate owner
witnesses, paired with their necessary common source/facade supports. The other
eight obligations each have one complete source-contract alternative. Alternatives
were derived from equivalent content, without minimizing resource count.

REQUIRED is exactly the resource-to-unit linkage in at least one complete
acceptable alternative, relative to that obligation. HELPFUL_ONLY has a specific
resource-relative rationale for useful but unnecessary context. All other cells
are UNNECESSARY because their content supplies no additional needed contract
for the predicate. UNRESOLVED is reserved for a genuine inability to determine
necessity from the packet; none is needed here. No future implementation artifacts
are witnesses. Fine-grained choices are explicitly encoded in build_judgments.py,
making semantic decisions reviewable rather than pretending to derive judgments
from keywords or filenames.

The exact current-source extraction algorithm and its concrete tests are
necessary under the range and tests predicates. Current public API and current
documentation are separate authoring constraints, so a prose description does
not substitute for an export list or an existing test. Accepted ADR rationale
is useful context where current contracts already supply the necessary facts;
this increment does not change an accepted cross-package decision.

## Gap review

Task gap: NONE. The ten predicates cover all mandatory existing information for
the frozen implementation task. Its caller-directed bounds and exclusions
constrain those obligations rather than requiring an extra frozen obligation.

Repository-information gap: NONE. Existing contracts plus the exact task are
sufficient. New inclusive-range behavior, its future boundary tests and the
eventual protected validation outcome are work to create, not absent repository
information. New API names, representation discriminator and error wording are
ordinary implementation choices under the established conventions.

## Exact statistics and replay

Coverage is 531/531 resources, 10/10 obligations and 5,310/5,310 cells, with
zero duplicate, missing or unexpected identities/cells. All ten obligations
are applicable. Labels: 39 REQUIRED, 47 HELPFUL_ONLY, 5,224 UNNECESSARY,
zero UNRESOLVED. There are 40 distinct required units, 45 obligation-relative
unit judgments and 22 unique REQUIRED resources across all alternatives.

There are 14 acceptable alternatives and nine valid cross-obligation combinations.
Every combination is enumerated by an exact deterministic Cartesian product.
Each complete combination needs 22 unique resources: minimum and maximum are
both 22, and all nine combinations attain the minimum. Ownership variants do
not change the global union because those current documents are independently
required by the documentation obligation. Inferability is 40 INFERABLE_AT_START
and zero INHERENT_DISCOVERY_REQUIRED.

JSON uses UTF-8, sorted object keys, compact separators, no non-finite numbers,
and one terminal LF. Resources, units, supports, alternatives and cells use
stable explicit ordering. Semantic outputs contain no timestamps. The digest
file contains the SHA-256 of judgments.json and its filename. A rebuild in memory
must reproduce judgments, statistics and digest bytes exactly. The writer checks
all target names before writing and refuses any overwrite; each creation also
uses exclusive file creation.

Only this invocation is used for validation:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
python -m pytest -c stage_c_pytest.ini --noconftest --basetemp=.stage_c_test_tmp test_stage_c.py -q
```

Tests import only local Stage C helpers, Python standard-library modules and
pytest. They do not import or execute archived repository source or tests.
The local temporary-path fixture uses standard-library temporary directories
inside the named cache, avoiding pytest's convenience symlinks. Three such
links created by the initial test run were removed individually without
following them; the final suite uses the link-free fixture and the complete
post-validation workspace is checked again for links/reparse points.
They verify input hashes/bindings, complete identity coverage, exact source
support, alternative membership, deterministic replay, label/link consistency,
exact sufficient unions, overwrite refusal, recursive forbidden-field rejection
and blindness attestations. Negative cases corrupt copies of local data and
must fail verification. No bare pytest or repository-wide collection is used.

The initial build is `python build_judgments.py`. Its default path refuses
overwrites. Subsequent verification rebuilds the semantic outputs in memory;
it does not mutate the immutable gold. All five original inputs retain their
original hashes after validation. Final hashes of all eight output artifacts
are reported in the completion response, avoiding a self-referential hash in
this file. No copy, repository import or commit is performed here.

## Blindness attestation before release

- parent/sibling filesystem accessed = NO
- repository checkout accessed = NO
- Git history accessed = NO
- treatment results accessed = NO
- arm identities accessed = NO
- parameter configurations accessed = NO
- development sensitivity outcomes accessed = NO
- confirmation accessed = NO
- Stage D performed = NO

The additional frozen-instruction attestations are also NO: Arm A results;
challenger results; treatment ranks; treatment scores; treatment comparison;
treatment costs; analyzer diagnostics; historical/provisional gold;
confirmation/reserve; effectiveness analysis. These statements concern access
to experiment artifacts and outcomes, not ordinary production contracts retained
inside the authorized packet. No treatment data was sought or inferred.

The stopping point is completed local Stage C validation and immutable output
hashes. Joined analysis, effectiveness analysis and publication are outside this
adjudication and were not performed.
