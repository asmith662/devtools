# Case 0013 — U3 Stage A review

**FROZEN PROSPECTIVE DESIGN; no treatment execution or gold.**

Hypothesis: task-only mechanism permission preserves useful exact-first witness gains while reducing unnecessary invocations/cost. U2 is development evidence only; this is a new task, not reused evaluation.

## Exact future task

```text
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
```

# Case 0013 task requirement matrix

## R01

Build a deterministic, inspectable in-memory manifest of an already materialized repository Context disclosure, keeping caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.

Obligations: structure

Exclusion: NONE

## R02

Inspect the existing class `devtools.context.planning.materialization.ContextDisclosure` and function `devtools.context.planning.materialization.materialize_disclosure_plan`: preserve exact plan identity, purpose, repository/snapshot applicability, ordered choices, representation names, option identities and the one-item-per-choice contract.

Obligations: structure

Exclusion: NONE

## R03

Use the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot. Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest; do not reacquire source, rematerialize choices or silently substitute evidence.

Obligations: integrity

Exclusion: NONE

## R04

Introduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`. Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.

Obligations: structure, manifest

Exclusion: NONE

## R05

Provide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records; distinguish total item text bytes from unique supporting-resource bytes. The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.

Obligations: projection

Exclusion: NONE

## R06

Inspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged. Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.

Obligations: compatibility, exports

Exclusion: NONE

## R07

Add focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases; retain existing planning, rendering and copied-request regression coverage.

Obligations: tests

Exclusion: NONE

## R08

Update the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope. Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.

Obligations: documentation

Exclusion: NONE

## R09

Inspect the existing file `pyproject.toml` for test, coverage and strict typing constraints; run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.

Obligations: validation

Exclusion: NONE

## R10

Operational exclusion: this is a future feature specification for an acquisition experiment. Stage A freezes the experiment only; do not implement the manifest feature, production routing, R1.7, BM25F, sequential search, treatment execution or gold adjudication.

Obligations: NONE

Exclusion: NON_FEATURE/OPERATIONAL; explicitly no feature implementation or scientific treatment

## Obligations and lexical queries

| Obligation | Satisfaction criterion | Exact query |
| --- | --- | --- |
| structure | Plan purpose, frame, identities, ordered one-item-per-choice and representations are preserved. | ContextDisclosure materialized disclosure plan purpose snapshot ordered items option identity representation native provenance |
| integrity | Foreign stale missing content mismatch and misaligned support are rejected without reacquisition or rematerialization. | RepositorySnapshot resource_at content identity foreign stale missing resources support validation materialization |
| manifest | Every item and repeated support occurrence is correlated with exact resource/content identities, byte counts and native provenance. | Context planning disclosure manifest items support resource content identities repeated order byte count native provenance |
| projection | Stable fields, exact ordered support, total item bytes versus unique supporting resource bytes and scope limits are established. | deterministic Context disclosure projection JSON stable identity UTF-8 byte count unique resource item text native provenance |
| compatibility | Existing output, original request role fields tools settings and task-before-Context assembly remain unchanged. | Context planning rendering assemble copied ModelRequest prompt role settings tools task unchanged |
| exports | Common planning and outer Context exports are coherent; no Retrieval dependency or relocation of Python-specific semantics. | Context planning __init__ exports public facade dependency Python qualified reference Retrieval |
| tests | Mixed choices duplicate support order UTF-8 CRLF native provenance determinism and all rejection cases plus old regressions are covered. | Context planning tests mixed whole resource qualified reference duplicate support non ASCII CRLF rejection provenance rendering copied request |
| documentation | Byte accounting, non-persistence, no automatic selection, sufficiency or disclosure authority are documented. | Context planning documentation manifest fidelity applicability byte accounting persistence completeness authorization |
| validation | Protected profile coverage strict mypy Ruff format worktree/index checks and restricted/live boundaries are established. | protected development validation pytest coverage pyproject strict mypy Ruff formatting confirmation exclusion |

## Hints, roles, native inputs and route decisions

B admits all ten explicit hints; C selects the six existing-evidence hints. Four new-destination hints retain full lexical coverage. These are requests, not claims that a native target exists or is relevant.

| Hint | Literal | Family | Obligation | Role | B | C |
| --- | --- | --- | --- | --- | --- | --- |
| H01 | `devtools.context.planning.materialization.ContextDisclosure` | PYTHON_DIRECT_CLASS | structure | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |
| H02 | `devtools.context.planning.materialization.materialize_disclosure_plan` | PYTHON_DIRECT_FUNCTION | structure | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |
| H03 | `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` | PYTHON_DIRECT_METHOD | integrity | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |
| H04 | `devtools.context.planning.manifest.ContextDisclosureManifest` | PYTHON_DIRECT_CLASS | manifest | INTRODUCE_NEW | EXACT_PLUS_LEXICAL | LEXICAL_ONLY |
| H05 | `devtools.context.planning.manifest.describe_context_disclosure` | PYTHON_DIRECT_FUNCTION | manifest | INTRODUCE_NEW | EXACT_PLUS_LEXICAL | LEXICAL_ONLY |
| H06 | `src/devtools/context/planning/manifest.py` | RESOURCE_ADDRESS | manifest | INTRODUCE_NEW | EXACT_PLUS_LEXICAL | LEXICAL_ONLY |
| H07 | `devtools.context.planning.rendering` | PYTHON_MODULE | compatibility | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |
| H08 | `tests/context/planning/test_manifest.py` | RESOURCE_ADDRESS | tests | INTRODUCE_NEW | EXACT_PLUS_LEXICAL | LEXICAL_ONLY |
| H09 | `src/devtools/context/planning/docs/overview.md` | RESOURCE_ADDRESS | documentation | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |
| H10 | `pyproject.toml` | RESOURCE_ADDRESS | validation | INSPECT_EXISTING | EXACT_PLUS_LEXICAL | EXACT_PLUS_LEXICAL |

## Router contract

A lexical only; B every admissible explicit hint; C only INSPECT_EXISTING admissible hints. INTRODUCE_NEW/CONCEPTUAL lexical only; unsupported explicit native scopes preserve fallback. Same inventory and lexical coverage, no repository inputs.

Caller role grammar: Inspect existing / Introduce new / Understand. Unknown grammar is an authoring error. Every obligation also has a conceptual purpose. These purposes do not replace complete obligation query coverage. No rank, score, resolution, gold or repository content is accepted by the policy API.

## Frozen arms, settings and safety lane

```json
{
  "arms": {
    "A": "LEXICAL_BASELINE",
    "B": "ALWAYS_ON_EXACT_FIRST",
    "C": "SELECTIVE_MECHANISM_ROUTER"
  },
  "settings": {
    "k1": 1.2,
    "b": 0.75,
    "filename_weight": 0.25,
    "maximum_results": "entire frozen resource count; all positive native rows",
    "tokenizer": "unicode-word-span-casefold-v1",
    "representation": "whole-resource-exact-text-v1",
    "tie_order": "native descending score then frozen document order",
    "fusion": false,
    "reformulation": false,
    "BM25F": false,
    "identifier_aware_view": false
  },
  "global_safety_query": {
    "text": "Build a deterministic, inspectable in-memory manifest of an already materialized repository Context disclosure, keeping caller-directed selection distinct from relevance, sufficiency, persistent Evidence and model-input assembly.\nInspect the existing class `devtools.context.planning.materialization.ContextDisclosure` and function `devtools.context.planning.materialization.materialize_disclosure_plan`: preserve exact plan identity, purpose, repository/snapshot applicability, ordered choices, representation names, option identities and the one-item-per-choice contract.\nUse the existing method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at` contract to authenticate each manifest resource against the supplied retained snapshot. Reject foreign or stale frames, missing resources, content-identity mismatch and misaligned address/content pairs before publishing a manifest; do not reacquire source, rematerialize choices or silently substitute evidence.\nIntroduce a new class `devtools.context.planning.manifest.ContextDisclosureManifest` and a new function `devtools.context.planning.manifest.describe_context_disclosure` in the new file `src/devtools/context/planning/manifest.py`. Preserve every item and repeated support occurrence in plan order, correlate exact supporting resource/content identities and UTF-8 text byte counts, and retain original native provenance as native values rather than serializing arbitrary objects.\nProvide a deterministic JSON-compatible projection of that manifest with explicit stable identity fields and exact ordered support records; distinguish total item text bytes from unique supporting-resource bytes. The projection is a derived presentation, not a durable wire schema, new repository fact, authorization to export source, budget policy or sufficiency claim.\nInspect the existing module `devtools.context.planning.rendering` for compatibility: existing rendering and copied ModelRequest assembly must remain unchanged. Export the manifest operation through the common planning and outer Context facades without depending on Retrieval or relocating Python-specific provenance into common planning.\nAdd focused tests in the new file `tests/context/planning/test_manifest.py` for mixed existing whole-resource and qualified-reference choices, duplicate support, order, non-ASCII and CRLF bytes, exact native provenance, deterministic projection and all rejection cases; retain existing planning, rendering and copied-request regression coverage.\nUpdate the existing file `src/devtools/context/planning/docs/overview.md` to explain the manifest's fidelity, applicability, byte-accounting and non-persistence scope. Explain why manifest completeness does not establish task completeness or model comprehension, and why it does not authorize disclosure or implement automatic Context planning.\nInspect the existing file `pyproject.toml` for test, coverage and strict typing constraints; run the protected development profile, Ruff, formatting, strict mypy and worktree/index diff checks without weakening configuration or running confirmation, reserve, live-model or Docker validation.\nOperational exclusion: this is a future feature specification for an acquisition experiment. Stage A freezes the experiment only; do not implement the manifest feature, production routing, R1.7, BM25F, sequential search, treatment execution or gold adjudication.\n",
    "analyzed_terms": [
      "build",
      "a",
      "deterministic",
      "inspectable",
      "in",
      "memory",
      "manifest",
      "of",
      "an",
      "already",
      "materialized",
      "repository",
      "context",
      "disclosure",
      "keeping",
      "caller",
      "directed",
      "selection",
      "distinct",
      "from",
      "relevance",
      "sufficiency",
      "persistent",
      "evidence",
      "and",
      "model",
      "input",
      "assembly",
      "inspect",
      "the",
      "existing",
      "class",
      "devtools",
      "planning",
      "materialization",
      "contextdisclosure",
      "function",
      "materialize_disclosure_plan",
      "preserve",
      "exact",
      "plan",
      "identity",
      "purpose",
      "snapshot",
      "applicability",
      "ordered",
      "choices",
      "representation",
      "names",
      "option",
      "identities",
      "one",
      "item",
      "per",
      "choice",
      "contract",
      "use",
      "method",
      "repositorysnapshot",
      "resource_at",
      "to",
      "authenticate",
      "each",
      "resource",
      "against",
      "supplied",
      "retained",
      "reject",
      "foreign",
      "or",
      "stale",
      "frames",
      "missing",
      "resources",
      "content",
      "mismatch",
      "misaligned",
      "address",
      "pairs",
      "before",
      "publishing",
      "do",
      "not",
      "reacquire",
      "source",
      "rematerialize",
      "silently",
      "substitute",
      "introduce",
      "new",
      "contextdisclosuremanifest",
      "describe_context_disclosure",
      "file",
      "src",
      "py",
      "every",
      "repeated",
      "support",
      "occurrence",
      "order",
      "correlate",
      "supporting",
      "utf",
      "8",
      "text",
      "byte",
      "counts",
      "retain",
      "original",
      "native",
      "provenance",
      "as",
      "values",
      "rather",
      "than",
      "serializing",
      "arbitrary",
      "objects",
      "provide",
      "json",
      "compatible",
      "projection",
      "that",
      "with",
      "explicit",
      "stable",
      "fields",
      "records",
      "distinguish",
      "total",
      "bytes",
      "unique",
      "is",
      "derived",
      "presentation",
      "durable",
      "wire",
      "schema",
      "fact",
      "authorization",
      "export",
      "budget",
      "policy",
      "claim",
      "module",
      "rendering",
      "for",
      "compatibility",
      "copied",
      "modelrequest",
      "must",
      "remain",
      "unchanged",
      "operation",
      "through",
      "common",
      "outer",
      "facades",
      "without",
      "depending",
      "on",
      "retrieval",
      "relocating",
      "python",
      "specific",
      "into",
      "add",
      "focused",
      "tests",
      "test_manifest",
      "mixed",
      "whole",
      "qualified",
      "reference",
      "duplicate",
      "non",
      "ascii",
      "crlf",
      "all",
      "rejection",
      "cases",
      "request",
      "regression",
      "coverage",
      "update",
      "docs",
      "overview",
      "md",
      "explain",
      "s",
      "fidelity",
      "accounting",
      "persistence",
      "scope",
      "why",
      "completeness",
      "does",
      "establish",
      "task",
      "comprehension",
      "it",
      "authorize",
      "implement",
      "automatic",
      "pyproject",
      "toml",
      "test",
      "strict",
      "typing",
      "constraints",
      "run",
      "protected",
      "development",
      "profile",
      "ruff",
      "formatting",
      "mypy",
      "worktree",
      "index",
      "diff",
      "checks",
      "weakening",
      "configuration",
      "running",
      "confirmation",
      "reserve",
      "live",
      "docker",
      "validation",
      "operational",
      "exclusion",
      "this",
      "future",
      "feature",
      "specification",
      "acquisition",
      "experiment",
      "stage",
      "freezes",
      "only",
      "production",
      "routing",
      "r1",
      "7",
      "bm25f",
      "sequential",
      "search",
      "treatment",
      "execution",
      "gold",
      "adjudication"
    ],
    "scope": "unchanged reporting safety lane, not a fictional task-global acquisition order"
  }
}
```

## Frame preparation

Source HEAD: `b42dcb3fd93bd6ddb8af35f1cf8b3273f6486b4b`; resources: 531; RepositoryId: `5cf96d9e-d6a5-44a6-83d3-1e24f6e00009`; SnapshotId: `724d78c6bf7677c1db06228e3826f891467b32a43af848df030ae116a0cd9371`; CorpusId: `33afe5a67237b2743ee4ecc9bdb43c3c7edaf765f246d2c1fc704c9d31847d25`; exact frame: `1d6ddb8cc25ba05e133b760337a932f6c1d783fa1350353aaaa29a1d98edd30a`.

Module universe: `68f711d0e0578f5330d4a719f23e81df15084e99ae37922f1bb797ff59f69969` (416 address-only interpretations). Native resource/content/document/module identities and the complete Python declaration resource universe are in frame.json; retained contents in inputs.json.gz/resources.json.gz. No declaration analysis, exact lookup, index build or retrieval has occurred. Source frame excludes all experiment/operational/confirmation/reserve data.

## Prospective metrics

- required_resource_reach
- required_cell_reach
- required_semantic_unit_reach
- all_witness_completion_depths
- chosen_witness_depth
- unique_completion_prefix_resources
- prefix_occurrences
- duplicate_occurrences
- unnecessary_occurrences
- owning_label_composition
- unique_UTF8_bytes
- admitted_native_invocations
- selected_skipped_unsupported_requests
- ambiguous_unresolved_resolved_requests
- resolution_presentation_ns
- charged_treatment_ns
- useful_routes_avoided
- low_value_routes_avoided
- selected_REQUIRED_HELPFUL_ONLY_UNNECESSARY_targets
- family_specific_effectiveness
- bottleneck_shifts

All gold-dependent metrics are unavailable until a separately authorized blind adjudication.

## Cost plan

### shared

Observe committed broad frame, address-only module universe and document representation separately; charge equally. Native lexical index build and identical nine obligation plus global queries execute once and are captured, reused unchanged by A/B/C.

### arm

B/C use identical task-only hint inventory and associations. Charge common hint projection/extraction to B/C, isolated arm policy time (B always-on, C classify/select), each admitted top-level native route separately, and each obligation presentation. A retains unmodified lexical output with zero exact/policy overhead.

### mechanism

Sum nonoverlapping per-request resolution elapsed ns plus nonoverlapping per-lane presentation ns. A direct-method timer includes parent selection and method containment; child timings are descriptive, never added. Unsupported admission attempts and selected/skipped requests counted separately from admitted native invocations.

### charged

Common index + common query elapsed + common hint projection for B/C + arm policy + exact resolution + presentation; no nested composite plus children. Frame setup and durability/publication wall time reported separately; arm composites descriptive cross-checks. No benchmarks/reruns. Captured single-run timings are descriptive development evidence, not calibrated causal speed estimates.

### inspection

Prefix burden is counterfactual complete-evidence inspection, not measured human effort. No actual coding or model execution.

## Frozen decision rule

### contract

Exact task/obligation/query/frame joins, blind gold and complete candidate/native match/global safety preservation; complete mandatory task interpretation, truthful full per-arm route/cost disclosure. Invalid or unassessable required evidence => EXPERIMENTAL_CONTRACT_DEFECT; do not fill missing measures with zero.

### soundness

C decisions must equal frozen task-only policy; locators derive only from literal explicit hint components. Every promotion uniquely native RESOLVED in the frozen frame; no invented owner. Violations => ROUTER_DEFECT. Genuine unsupported/ambiguous/unresolved native outcomes alone are scope outcomes.

### reach

C loses no A- or B-reached REQUIRED resources, owning cells or distinct/owning semantic units. All original lexical positive matches, ranks, scores and contributions survive; the global safety lane is unchanged. Loss => ROUTER_DEFECT.

### completion

For each mandatory applicable obligation evaluate every complete reviewed witness, ALL members jointly necessary, ANY complete alternative admissible. Select minimum completion depth then stable reviewed witness identity. Missing completion is null; null cannot pass numeric gates. Do not mix alternatives or invent task-global ranking. Chosen mandatory prefixes are unioned; occurrences remain repeated and labels are owning-obligation relative. Resource bytes count distinct exact UTF-8 whole-resource contents. Task combinations constrain reported semantic sufficiency, not a fabricated global treatment order.

### obligation_safety

Every B-complete mandatory obligation remains C-complete; C selected completion depth and unique prefix count each <= B. Failure => ROUTER_DEFECT. An undefined complete B baseline makes selective-support gates unassessable, not successful.

### meaningful_B_gain

A B-versus-A obligation gain is meaningful when A is incomplete and B completes, or A depth >0 and 5*B_depth <=4*A_depth. All such B improvements must retain C_depth <= B_depth for branch 1. Report every skipped useful B route even outside this threshold.

### branch_1

At least one meaningful B-versus-A witness gain retained; C preserves every such gain; native admitted top-level route invocations reduced at least 25% (4*C<=3*B); exact-resolution-plus-presentation aggregate cost reduced at least 10% (10*C<=9*B); charged treatment cost no more than 5% higher (20*C<=21*B). B invocation and cost denominators must be positive.

### branch_2

Case-wide chosen completion-prefix unique resources reduced at least 10% over B (10*C<=9*B, B>0); unique UTF-8 bytes <= B; charged C cost <= B with positive B cost. Obligation safety and required reach still mandatory.

### precedence

1 contract defect; 2 router soundness/reach/obligation defect; 3 all safety gates plus either selective-value branch => SELECTIVE_MECHANISM_ROUTING_SUPPORTED; 4 sound reach/obligation-safe C has any strict positive C-over-B depth, unique prefix, occurrences, unnecessary, bytes, invocation or mechanism-cost reduction => COMPLEMENTARY_BUT_NOT_CLEARLY_BETTER; 5 otherwise NO_MATERIAL_VALUE. Equality with B never supplies selective value. Use gates.evaluate integer arithmetic; no tuned thresholds or rounded decisions.

### undefined

Report NOT_ASSESSED for individual missing metrics. If missing data prevents contract/safety or selected-branch evaluation, classify contract defect, rather than constructing GateEvidence with a synthetic zero. Zero B noise supplies no reduction evidence; positive counters only define reduction percentages.

### attribution

ROUTE_SELECTION_MISS means a frozen task-visible intent's applicable sound B route was skipped by C and either supplies REQUIRED witness evidence absent from C exact routes or preserves a B witness-depth gain lost by C. Report witness membership and actual depth effect separately. Low-value avoided routes: genuine native nonresolution, non-REQUIRED targets, or REQUIRED targets with no B-versus-A selected witness completion improvement; report these subtypes separately, not as universal uselessness. OVERREACH means C admission violates the explicit frozen role or native scope. Authoring defect concerns incomplete/contradictory task-only intent meaning, not poor retrieval alone. SEARCH_POLICY_FAILURE=NOT_ASSESSED; no sequential pursuit.

### threshold_rationale

25% fewer native route requests is an operationally noticeable discrete reduction; 10% mechanism cost or task union improvement requires a measurable benefit beyond equality; 5% charged-cost tolerance bounds added classification overhead. These are prospective development thresholds, not fitted to Case 0013 outcomes or Case 0012 ranks.

## Failure taxonomy

- ROUTE_SELECTION_MISS
- ROUTE_SELECTION_OVERREACH
- UNSUPPORTED_ROUTE
- AMBIGUOUS_ROUTE
- UNRESOLVED_ROUTE
- SELECTED_ROUTE_TARGET_NOT_REQUIRED
- SELECTED_ROUTE_NOT_COMPLETION_BOTTLENECK
- LEXICAL_FALLBACK_RANKING_FAILURE
- ACQUISITION_INTENT_AUTHORING_DEFECT
- EXPERIMENTAL_CONTRACT_DEFECT

SEARCH_POLICY_FAILURE = NOT_ASSESSED.

## Future blind gold

```json
{
  "model": "GPT-6 Astra",
  "reasoning": "High",
  "policy": "One clean treatment-blind primary adjudication of complete resource-by-obligation cells, semantic units, complete witnesses/alternatives, gaps and limitations. No automatic second adjudication. Separately authorized reliability uses same model family and reasoning.",
  "packet_allowlist": [
    "case",
    "task_identity",
    "task_text",
    "obligations",
    "resources"
  ],
  "excluded": [
    "queries",
    "intents",
    "router roles",
    "hints metadata",
    "locators",
    "arms",
    "decisions",
    "costs",
    "results",
    "ranks",
    "scores",
    "treatment reports"
  ]
}
```

## Exact execution counters and exclusions

```json
{
  "execution": {
    "retrieval": 0,
    "exact_routes": 0,
    "specialized_mechanisms": 0,
    "treatments": 0,
    "index_builds": 0
  },
  "stage_b": "NOT_EXECUTED",
  "gold": "ABSENT",
  "excluded": [
    "production routing",
    "manifest feature implementation",
    "R1.7",
    "BM25F",
    "confirmation/reserve",
    "sequential search",
    "gold adjudication",
    ".local/codex-result.md as scientific input"
  ]
}
```

## Complete task-only intent and locator trace

This appendix includes every native task/obligation/query identity, exact span, purpose, role, association, locator and per-arm deterministic decision identity. The complete machine trace is trace.json. It contains no acquisition outcome.

```json
{
  "native_task_interpretation": {
    "identity": {
      "value": "case-0013-context-disclosure-manifest"
    },
    "provenance": {
      "source_identity": "case-0013-context-disclosure-manifest",
      "span": null,
      "explanation": "Exact prospective manifest task"
    },
    "anchors": [
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
        },
        "text": "devtools.context.planning.materialization.ContextDisclosure",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 258,
            "end": 317
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
        },
        "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 333,
            "end": 402
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
        },
        "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 599,
            "end": 666
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
        },
        "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1003,
            "end": 1063
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
        },
        "text": "devtools.context.planning.manifest.describe_context_disclosure",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1085,
            "end": 1147
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
        },
        "text": "src/devtools/context/planning/manifest.py",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1166,
            "end": 1207
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
        },
        "text": "devtools.context.planning.rendering",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1858,
            "end": 1893
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
        },
        "text": "tests/context/planning/test_manifest.py",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2202,
            "end": 2241
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
        },
        "text": "src/devtools/context/planning/docs/overview.md",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2539,
            "end": 2585
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
        },
        "text": "pyproject.toml",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2885,
            "end": 2899
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      }
    ],
    "obligations": [
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "predicate": "Preserve exact materialized plan/item structure and native provenance.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
          },
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 0,
            "end": 1458
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "structure",
          "statement": "Plan purpose, frame, identities, ordered one-item-per-choice and representations are preserved."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "integrity"
        },
        "predicate": "Authenticate manifest support against retained native snapshot before publication.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 574,
            "end": 980
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "integrity",
          "statement": "Foreign stale missing content mismatch and misaligned support are rejected without reacquisition or rematerialization."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "predicate": "Implement the future explicit manifest operation in common Context Planning.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
          },
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
          },
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 980,
            "end": 1458
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "manifest",
          "statement": "Every item and repeated support occurrence is correlated with exact resource/content identities, byte counts and native provenance."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "projection"
        },
        "predicate": "Provide deterministic JSON-compatible presentation and distinct byte accounting.",
        "anchors": [],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1458,
            "end": 1829
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "projection",
          "statement": "Stable fields, exact ordered support, total item bytes versus unique supporting resource bytes and scope limits are established."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "compatibility"
        },
        "predicate": "Preserve rendering and copied request assembly.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1829,
            "end": 2167
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "compatibility",
          "statement": "Existing output, original request role fields tools settings and task-before-Context assembly remain unchanged."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "exports"
        },
        "predicate": "Expose both public facades with existing dependency ownership.",
        "anchors": [],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1829,
            "end": 2167
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "exports",
          "statement": "Common planning and outer Context exports are coherent; no Retrieval dependency or relocation of Python-specific semantics."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "tests"
        },
        "predicate": "Establish focused and regression coverage for every new and preserved contract.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2167,
            "end": 2513
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "tests",
          "statement": "Mixed choices duplicate support order UTF-8 CRLF native provenance determinism and all rejection cases plus old regressions are covered."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "documentation"
        },
        "predicate": "Explain manifest fidelity applicability and limits in existing package documentation.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2513,
            "end": 2858
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "documentation",
          "statement": "Byte accounting, non-persistence, no automatic selection, sufficiency or disclosure authority are documented."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      },
      {
        "identity": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "validation"
        },
        "predicate": "Preserve the protected development and static validation contract.",
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
          }
        ],
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2858,
            "end": 3150
          },
          "explanation": "Caller complete task interpretation, no witness gold"
        },
        "requirement": "mandatory",
        "satisfaction": {
          "name": "validation",
          "statement": "Protected profile coverage strict mypy Ruff format worktree/index checks and restricted/live boundaries are established."
        },
        "witness_alternatives": [],
        "applicability_condition": "MANDATORY; later independent gold may mark NOT_APPLICABLE only with exact task-supported rationale"
      }
    ]
  },
  "native_obligation_queries": [
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/structure"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "structure"
      },
      "text": "ContextDisclosure materialized disclosure plan purpose snapshot ordered items option identity representation native provenance"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/integrity"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "integrity"
      },
      "text": "RepositorySnapshot resource_at content identity foreign stale missing resources support validation materialization"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/manifest"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "manifest"
      },
      "text": "Context planning disclosure manifest items support resource content identities repeated order byte count native provenance"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/projection"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "projection"
      },
      "text": "deterministic Context disclosure projection JSON stable identity UTF-8 byte count unique resource item text native provenance"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/compatibility"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "compatibility"
      },
      "text": "Context planning rendering assemble copied ModelRequest prompt role settings tools task unchanged"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/exports"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "exports"
      },
      "text": "Context planning __init__ exports public facade dependency Python qualified reference Retrieval"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/tests"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "tests"
      },
      "text": "Context planning tests mixed whole resource qualified reference duplicate support non ASCII CRLF rejection provenance rendering copied request"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/documentation"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "documentation"
      },
      "text": "Context planning documentation manifest fidelity applicability byte accounting persistence completeness authorization"
    },
    {
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "obligation/validation"
      },
      "obligation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "validation"
      },
      "text": "protected development validation pytest coverage pyproject strict mypy Ruff formatting confirmation exclusion"
    }
  ],
  "hint_inventory": [
    {
      "key": "H01",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.planning.materialization.ContextDisclosure",
      "span": {
        "start": 258,
        "end": 317
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_DIRECT_CLASS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 258,
          "end": 317
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
      }
    },
    {
      "key": "H02",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
      "span": {
        "start": 333,
        "end": 402
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_DIRECT_FUNCTION",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 333,
          "end": 402
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
      }
    },
    {
      "key": "H03",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
      "span": {
        "start": 599,
        "end": 666
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_DIRECT_METHOD",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 599,
          "end": 666
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
      }
    },
    {
      "key": "H04",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
      "span": {
        "start": 1003,
        "end": 1063
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_DIRECT_CLASS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1003,
          "end": 1063
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
      }
    },
    {
      "key": "H05",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.planning.manifest.describe_context_disclosure",
      "span": {
        "start": 1085,
        "end": 1147
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_DIRECT_FUNCTION",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1085,
          "end": 1147
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
      }
    },
    {
      "key": "H06",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "src/devtools/context/planning/manifest.py",
      "span": {
        "start": 1166,
        "end": 1207
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "RESOURCE_ADDRESS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1166,
          "end": 1207
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
      }
    },
    {
      "key": "H07",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "devtools.context.planning.rendering",
      "span": {
        "start": 1858,
        "end": 1893
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "PYTHON_MODULE",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1858,
          "end": 1893
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
      }
    },
    {
      "key": "H08",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "tests/context/planning/test_manifest.py",
      "span": {
        "start": 2202,
        "end": 2241
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "RESOURCE_ADDRESS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2202,
          "end": 2241
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
      }
    },
    {
      "key": "H09",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "src/devtools/context/planning/docs/overview.md",
      "span": {
        "start": 2539,
        "end": 2585
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "RESOURCE_ADDRESS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2539,
          "end": 2585
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
      }
    },
    {
      "key": "H10",
      "task": {
        "value": "case-0013-context-disclosure-manifest"
      },
      "text": "pyproject.toml",
      "span": {
        "start": 2885,
        "end": 2899
      },
      "rule": "caller-task-review-v1",
      "syntactic_form": "caller-reviewed-task-syntax",
      "category": "RESOURCE_ADDRESS",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2885,
          "end": 2899
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      },
      "identity": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
      }
    }
  ],
  "hint_associations": [
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "structure"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 258,
          "end": 317
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "structure"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 333,
          "end": 402
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "integrity"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 599,
          "end": 666
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "manifest"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1003,
          "end": 1063
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "manifest"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1085,
          "end": 1147
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "manifest"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1166,
          "end": 1207
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "compatibility"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1858,
          "end": 1893
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "tests"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2202,
          "end": 2241
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "documentation"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2539,
          "end": 2585
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
      },
      "lane": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "value": "validation"
      },
      "reason": "Explicit task clause associates this hint with this obligation, without gold",
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2885,
          "end": 2899
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    }
  ],
  "acquisition_intents": [
    {
      "identity": "case-0013-context-disclosure-manifest/structure/I01",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I01",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "statement": "Inspect existing devtools.context.planning.materialization.ContextDisclosure: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 258,
            "end": 317
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.materialization.ContextDisclosure",
        "span": {
          "start": 258,
          "end": 317
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_DIRECT_CLASS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 258,
            "end": 317
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 258,
            "end": 317
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 258,
          "end": 317
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/structure/I02",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I02",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "statement": "Inspect existing devtools.context.planning.materialization.materialize_disclosure_plan: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 333,
            "end": 402
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
        "span": {
          "start": 333,
          "end": 402
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_DIRECT_FUNCTION",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 333,
            "end": 402
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 333,
            "end": 402
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 333,
          "end": 402
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/integrity/I03",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I03",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "integrity"
        },
        "statement": "Inspect existing devtools.context.repository.snapshot.RepositorySnapshot.resource_at: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 599,
            "end": 666
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
        "span": {
          "start": 599,
          "end": 666
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_DIRECT_METHOD",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 599,
            "end": 666
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "integrity"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 599,
            "end": 666
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 599,
          "end": 666
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/manifest/I04",
      "role": "INTRODUCE_NEW",
      "need": {
        "key": "I04",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "statement": "Introduce new devtools.context.planning.manifest.ContextDisclosureManifest: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1003,
            "end": 1063
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
        "span": {
          "start": 1003,
          "end": 1063
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_DIRECT_CLASS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1003,
            "end": 1063
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1003,
            "end": 1063
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1003,
          "end": 1063
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/manifest/I05",
      "role": "INTRODUCE_NEW",
      "need": {
        "key": "I05",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "statement": "Introduce new devtools.context.planning.manifest.describe_context_disclosure: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1085,
            "end": 1147
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.manifest.describe_context_disclosure",
        "span": {
          "start": 1085,
          "end": 1147
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_DIRECT_FUNCTION",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1085,
            "end": 1147
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1085,
            "end": 1147
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1085,
          "end": 1147
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/manifest/I06",
      "role": "INTRODUCE_NEW",
      "need": {
        "key": "I06",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "statement": "Introduce new src/devtools/context/planning/manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1166,
            "end": 1207
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "src/devtools/context/planning/manifest.py",
        "span": {
          "start": 1166,
          "end": 1207
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1166,
            "end": 1207
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1166,
            "end": 1207
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1166,
          "end": 1207
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/compatibility/I07",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I07",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "compatibility"
        },
        "statement": "Inspect existing devtools.context.planning.rendering: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1858,
            "end": 1893
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.rendering",
        "span": {
          "start": 1858,
          "end": 1893
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "PYTHON_MODULE",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1858,
            "end": 1893
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "compatibility"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1858,
            "end": 1893
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1858,
          "end": 1893
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/tests/I08",
      "role": "INTRODUCE_NEW",
      "need": {
        "key": "I08",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "tests"
        },
        "statement": "Introduce new tests/context/planning/test_manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2202,
            "end": 2241
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "tests/context/planning/test_manifest.py",
        "span": {
          "start": 2202,
          "end": 2241
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2202,
            "end": 2241
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "tests"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2202,
            "end": 2241
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2202,
          "end": 2241
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/documentation/I09",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I09",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "documentation"
        },
        "statement": "Inspect existing src/devtools/context/planning/docs/overview.md: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2539,
            "end": 2585
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "src/devtools/context/planning/docs/overview.md",
        "span": {
          "start": 2539,
          "end": 2585
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2539,
            "end": 2585
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "documentation"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2539,
            "end": 2585
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2539,
          "end": 2585
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/validation/I10",
      "role": "INSPECT_EXISTING",
      "need": {
        "key": "I10",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "validation"
        },
        "statement": "Inspect existing pyproject.toml: establish its native contract specified by this task clause",
        "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2885,
            "end": 2899
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        },
        "anchors": [
          {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
          }
        ]
      },
      "hint": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "pyproject.toml",
        "span": {
          "start": 2885,
          "end": 2899
        },
        "rule": "caller-task-review-v1",
        "syntactic_form": "caller-reviewed-task-syntax",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2885,
            "end": 2899
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "association": {
        "hint": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
        },
        "lane": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "validation"
        },
        "reason": "Explicit task clause associates this hint with this obligation, without gold",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2885,
            "end": 2899
          },
          "explanation": "Task-only caller syntax reference before frame preparation"
        }
      },
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2885,
          "end": 2899
        },
        "explanation": "Task-only caller syntax reference before frame preparation"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/structure/conceptual/structure",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/structure",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "structure"
        },
        "statement": "Understand Preserve exact materialized plan/item structure and native provenance.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 0,
            "end": 230
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 0,
          "end": 230
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/integrity/conceptual/integrity",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/integrity",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "integrity"
        },
        "statement": "Understand Authenticate manifest support against retained native snapshot before publication.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 574,
            "end": 980
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 574,
          "end": 980
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/manifest/conceptual/manifest",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/manifest",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "manifest"
        },
        "statement": "Understand Implement the future explicit manifest operation in common Context Planning.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 980,
            "end": 1458
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 980,
          "end": 1458
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/projection/conceptual/projection",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/projection",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "projection"
        },
        "statement": "Understand Provide deterministic JSON-compatible presentation and distinct byte accounting.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1458,
            "end": 1829
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1458,
          "end": 1829
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/compatibility/conceptual/compatibility",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/compatibility",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "compatibility"
        },
        "statement": "Understand Preserve rendering and copied request assembly.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1829,
            "end": 2167
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1829,
          "end": 2167
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/exports/conceptual/exports",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/exports",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "exports"
        },
        "statement": "Understand Expose both public facades with existing dependency ownership.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1829,
            "end": 2167
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 1829,
          "end": 2167
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/tests/conceptual/tests",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/tests",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "tests"
        },
        "statement": "Understand Establish focused and regression coverage for every new and preserved contract.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2167,
            "end": 2513
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2167,
          "end": 2513
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/documentation/conceptual/documentation",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/documentation",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "documentation"
        },
        "statement": "Understand Explain manifest fidelity applicability and limits in existing package documentation.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2513,
            "end": 2858
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2513,
          "end": 2858
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    },
    {
      "identity": "case-0013-context-disclosure-manifest/validation/conceptual/validation",
      "role": "CONCEPTUAL",
      "need": {
        "key": "conceptual/validation",
        "obligation": {
          "task": {
            "value": "case-0013-context-disclosure-manifest"
          },
          "value": "validation"
        },
        "statement": "Understand Preserve the protected development and static validation contract.",
        "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2858,
            "end": 3150
          },
          "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
        },
        "anchors": []
      },
      "hint": null,
      "association": null,
      "provenance": {
        "source_identity": "case-0013-context-disclosure-manifest",
        "span": {
          "start": 2858,
          "end": 3150
        },
        "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
      }
    }
  ],
  "route_decisions": {
    "A": [
      {
        "identity": "1e7844e5e5bde9c249fdca480ab74d3363b147090ee43c75e7408abae559202f",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I01",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.ContextDisclosure: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.ContextDisclosure",
            "span": {
              "start": 258,
              "end": 317
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 258,
              "end": 317
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "74744c6172b485b6abe8471c2e0c8f80556cd547b443cd9a5ff81481556bad49",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I02",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.materialize_disclosure_plan: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
            "span": {
              "start": 333,
              "end": 402
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 333,
              "end": 402
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "c5bcfd49cfe8db26b33ebcb8f304d8816c731ef23e4b54aa593c89b3276b2409",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I03",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Inspect existing devtools.context.repository.snapshot.RepositorySnapshot.resource_at: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
            "span": {
              "start": 599,
              "end": 666
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_METHOD",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 599,
              "end": 666
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "7451c09e410bf15dabd871363c8ba9ca2a95310686b4de78c9132a1552721774",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I04",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.ContextDisclosureManifest: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "173be730c7f99d7c39007b892d94cbe32146867857bf4b70dcacbc79be626914",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I05",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.describe_context_disclosure: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.describe_context_disclosure",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "c2de3c3481535860233190acc4d49e71236425d97009721a363fe2256b4da758",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I06",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new src/devtools/context/planning/manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/manifest.py",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "1f61247ab945d210aa15d0056e848cf1aee7078792b8b0104ee110041250ae93",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I07",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Inspect existing devtools.context.planning.rendering: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.rendering",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_MODULE",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "4ae67e479d51844a8820226b2ea4c358bd6b6ae3d93b6d9b83581f67ffc10bc6",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I08",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Introduce new tests/context/planning/test_manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "tests/context/planning/test_manifest.py",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "65b7eec776577ccfa1e55d9891734c24fbe7db5adb65825b5b0aa0548d35721d",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I09",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Inspect existing src/devtools/context/planning/docs/overview.md: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/docs/overview.md",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "9941b6772f04e5164d1c5f2c2d9b3a2bf23425d26724b5d9c1637e998d80743c",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "I10",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Inspect existing pyproject.toml: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "pyproject.toml",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "Baseline excludes exact mechanisms"
      },
      {
        "identity": "dcb2de9d7435ed854b89a8ae49d0710019f95e883ec0ee48bb3920c143dc24a0",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/structure",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Understand Preserve exact materialized plan/item structure and native provenance.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 0,
                "end": 230
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 0,
              "end": 230
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "0d20a8ec157ed03ec5cedf88c3debf2c482d9d3ddcbd8911c6df77828b38fafb",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/integrity",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Understand Authenticate manifest support against retained native snapshot before publication.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 574,
                "end": 980
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 574,
              "end": 980
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "97d8607896d04fb4ef790eab7774c302fa4ab5a2b625a3b8f43feff39e763343",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/manifest",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Understand Implement the future explicit manifest operation in common Context Planning.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 980,
                "end": 1458
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 980,
              "end": 1458
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "75156d05f5ab5e218d4c124fc653686f1a8080f8f0dffc61c2122b93426e5434",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/projection",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "projection"
            },
            "statement": "Understand Provide deterministic JSON-compatible presentation and distinct byte accounting.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1458,
                "end": 1829
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1458,
              "end": 1829
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "969625fece93bd8ef584e1820e36257e2ac948fe0d2b6e544d514183b8c177f6",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/compatibility",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Understand Preserve rendering and copied request assembly.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "2505a2229c2ecddad7c52596fb0c812c19d878fc55abc7d02755fe3bbf87ed4f",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/exports",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "exports"
            },
            "statement": "Understand Expose both public facades with existing dependency ownership.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "cca7ff3eb83650a4b87813ad2ecdd4320c5e20044f9d32018e39de31a4cb0a29",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/tests",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Understand Establish focused and regression coverage for every new and preserved contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2167,
                "end": 2513
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2167,
              "end": 2513
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "66186f751c4149feabde5390fd89f8c3461beb441db38e65a28625ce4e8fe538",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/documentation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Understand Explain manifest fidelity applicability and limits in existing package documentation.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2513,
                "end": 2858
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2513,
              "end": 2858
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "63fd225f85d51368f5bf41ea03636a818542be68f946686c3cb38fa9c967fd0e",
        "arm": "LEXICAL_BASELINE",
        "basis": {
          "need": {
            "key": "conceptual/validation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Understand Preserve the protected development and static validation contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2858,
                "end": 3150
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2858,
              "end": 3150
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      }
    ],
    "B": [
      {
        "identity": "35cf31c193f88b03862bcd369b4189e7ecefda0e45de8eb5db721c0a4a7cb25d",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I01",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.ContextDisclosure: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.ContextDisclosure",
            "span": {
              "start": 258,
              "end": 317
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 258,
              "end": 317
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.ContextDisclosure",
            "span": {
              "start": 258,
              "end": 317
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.materialization",
              "kind": null
            },
            "declared_name": "ContextDisclosure",
            "kind": "class"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "479f3d6ab067bad2ed406e9b373e3dbf8770cc1080c8b7f9c85ab24e45ae9580",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I02",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.materialize_disclosure_plan: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
            "span": {
              "start": 333,
              "end": 402
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 333,
              "end": 402
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
            "span": {
              "start": 333,
              "end": 402
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.materialization",
              "kind": null
            },
            "declared_name": "materialize_disclosure_plan",
            "kind": "function"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "dee5684342a95c6bf6fc4319657cc59fdfe0b2c99175b4222bd45b2e9171cdcf",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I03",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Inspect existing devtools.context.repository.snapshot.RepositorySnapshot.resource_at: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
            "span": {
              "start": 599,
              "end": 666
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_METHOD",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 599,
              "end": 666
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
            "span": {
              "start": 599,
              "end": 666
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_METHOD",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.repository.snapshot",
              "kind": null
            },
            "class_name": "RepositorySnapshot",
            "method_name": "resource_at"
          },
          "mechanism": "exact-source-class-then-native-direct-method-containment-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "01e8a07877745a1b1450cec9316d52fd0a71efce5f8b316ff2426ffddde34cfd",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I04",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.ContextDisclosureManifest: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.manifest",
              "kind": null
            },
            "declared_name": "ContextDisclosureManifest",
            "kind": "class"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "3c4b29e14618c06b203fb278425aa578557f7f382616b06bf5e5fc6baf89181e",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I05",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.describe_context_disclosure: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.describe_context_disclosure",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.describe_context_disclosure",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.manifest",
              "kind": null
            },
            "declared_name": "describe_context_disclosure",
            "kind": "function"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "b65225df385763d2ca9be5e61cecaa01e8231f388aedeef6625cfd48d04c644c",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I06",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new src/devtools/context/planning/manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/manifest.py",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/manifest.py",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "src/devtools/context/planning/manifest.py"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "883b6258ef4d68f14b54ff3940fdeb9acdf61f51981a78c70bd309668a1dc64c",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I07",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Inspect existing devtools.context.planning.rendering: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.rendering",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_MODULE",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.rendering",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_MODULE",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "dotted_name": "devtools.context.planning.rendering",
            "kind": null
          },
          "mechanism": "python-module-exact-name-lookup",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "21e3a8a5d8d9c4536cf9f44059ae0e1f5fb0dcb47823a9ef7f87469d9fafec27",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I08",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Introduce new tests/context/planning/test_manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "tests/context/planning/test_manifest.py",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "tests/context/planning/test_manifest.py",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "tests/context/planning/test_manifest.py"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "ef16c9e194fd82b4e95261ee4b74ca96f3bc0b4134f41906365cd7d611fbef39",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I09",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Inspect existing src/devtools/context/planning/docs/overview.md: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/docs/overview.md",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/docs/overview.md",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "src/devtools/context/planning/docs/overview.md"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "2fd005c133064f932a7a3b33b7a0b11bd25c5850394ffd1a9dd5d63f2f9c45b6",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "I10",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Inspect existing pyproject.toml: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "pyproject.toml",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "pyproject.toml",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "pyproject.toml"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "cbf488bfe77011ae3b23816c2fdcd0143277e7f444745c34923ee1c80cf50ab4",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/structure",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Understand Preserve exact materialized plan/item structure and native provenance.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 0,
                "end": 230
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 0,
              "end": 230
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "fd6d8996f24719aa8421e422f0f98c651da6a45e838d8ed9a546683a814b88c3",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/integrity",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Understand Authenticate manifest support against retained native snapshot before publication.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 574,
                "end": 980
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 574,
              "end": 980
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "646714c2ef3ad2fd1e9fc31fce68fbf5c3aca6f2986ff4dc47b04f8f1d458107",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/manifest",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Understand Implement the future explicit manifest operation in common Context Planning.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 980,
                "end": 1458
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 980,
              "end": 1458
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "c30b2614881259a144b9a5f1dee4e180cdce1800c6da23dbf83ae2897f74493e",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/projection",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "projection"
            },
            "statement": "Understand Provide deterministic JSON-compatible presentation and distinct byte accounting.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1458,
                "end": 1829
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1458,
              "end": 1829
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "94431c13f68c8bb183b10d38529b2876342dbafbac198cc0603216826925816d",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/compatibility",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Understand Preserve rendering and copied request assembly.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "d8dd231935ebdf8b30346feeb73a72f66ec326a8c7c9130b2ed6cc4346321a4a",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/exports",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "exports"
            },
            "statement": "Understand Expose both public facades with existing dependency ownership.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "c5f1f5f9ff4d5362a1b4482ed1e5da21350408870b2062ade521251294994ccd",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/tests",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Understand Establish focused and regression coverage for every new and preserved contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2167,
                "end": 2513
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2167,
              "end": 2513
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "38ac0803c0ab61808b24df89e3296e5a41daf1698634fa308568796e2cf906c8",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/documentation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Understand Explain manifest fidelity applicability and limits in existing package documentation.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2513,
                "end": 2858
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2513,
              "end": 2858
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "84389b8db654d0f152f92231317780915f1d4fc1f0ec15c21afa171c4f1f939b",
        "arm": "ALWAYS_ON_EXACT_FIRST",
        "basis": {
          "need": {
            "key": "conceptual/validation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Understand Preserve the protected development and static validation contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2858,
                "end": 3150
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2858,
              "end": 3150
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      }
    ],
    "C": [
      {
        "identity": "8345438362170fc98a54a5c5f564e17f491af0e0ffdea709accdbd5008aac8f6",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I01",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.ContextDisclosure: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.ContextDisclosure",
            "span": {
              "start": 258,
              "end": 317
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 258,
              "end": 317
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.ContextDisclosure",
            "span": {
              "start": 258,
              "end": 317
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "1ab7e8b1be7a34f08412218db588c864255478c036de449572cf2254b2c9577d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 258,
                "end": 317
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.materialization",
              "kind": null
            },
            "declared_name": "ContextDisclosure",
            "kind": "class"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "3b220ec331398020b10816d2e64dda344ac3550e319bb0656ac64120ec200b93",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I02",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Inspect existing devtools.context.planning.materialization.materialize_disclosure_plan: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
            "span": {
              "start": 333,
              "end": 402
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 333,
              "end": 402
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
            "span": {
              "start": 333,
              "end": 402
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d69727149c91b87f9e23aa8a8026a1843641feb0933f93dfcefbb1df8af407b1"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 333,
                "end": 402
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.planning.materialization",
              "kind": null
            },
            "declared_name": "materialize_disclosure_plan",
            "kind": "function"
          },
          "mechanism": "exact-python-module-source-declaration-selection-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "da4dfda9580e19c750c17741f6b16adc047127371746b386e7b447c4a914a1e4",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I03",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Inspect existing devtools.context.repository.snapshot.RepositorySnapshot.resource_at: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
            "span": {
              "start": 599,
              "end": 666
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_METHOD",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 599,
              "end": 666
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
            "span": {
              "start": 599,
              "end": 666
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_METHOD",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "cf1c9669156f1680068aad976936c93c4952ce089fdd57408998c346177f2c34"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 599,
                "end": 666
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "module": {
              "dotted_name": "devtools.context.repository.snapshot",
              "kind": null
            },
            "class_name": "RepositorySnapshot",
            "method_name": "resource_at"
          },
          "mechanism": "exact-source-class-then-native-direct-method-containment-v1",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "8b055f287e6586d9672aeff1cf692bb3d6e09148a7eee6cd5ed7a8d28611cd70",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I04",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.ContextDisclosureManifest: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_CLASS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "da5ce9184d6e0acdadf0d257685551671eed86b7ab9f0beac15de0a74b18ff42"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1003,
                "end": 1063
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1003,
              "end": 1063
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "New destinations and conceptual purposes do not request existing exact evidence"
      },
      {
        "identity": "c308c3cebd9894e37ed8f086ff78edbf7e2e0e8ecac90a34d009993a7cdfd8cd",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I05",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new devtools.context.planning.manifest.describe_context_disclosure: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.manifest.describe_context_disclosure",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_DIRECT_FUNCTION",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "61cfacc7c887ac636e0a99bb1dfa3600946f955d13e272f7039ba540d1477a05"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1085,
                "end": 1147
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1085,
              "end": 1147
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "New destinations and conceptual purposes do not request existing exact evidence"
      },
      {
        "identity": "ba43b880968a3894d0e9ba2c379b6b2708ea197c9a5db65e37542777bece68f0",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I06",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Introduce new src/devtools/context/planning/manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/manifest.py",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6eb085a6c986efa5c0c2fc0095f9b094b4ff0642f9444ca99c7b9273ca0c7d06"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1166,
                "end": 1207
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1166,
              "end": 1207
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "New destinations and conceptual purposes do not request existing exact evidence"
      },
      {
        "identity": "245cffc10aff48e734eed349367fab92808c2d8297685b126d66b0d2863bbe3c",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I07",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Inspect existing devtools.context.planning.rendering: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.rendering",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_MODULE",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "devtools.context.planning.rendering",
            "span": {
              "start": 1858,
              "end": 1893
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "PYTHON_MODULE",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "d9100147c6fbdd12dc162735ce8ca06095a3aabc0f94618693d712299b215beb"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1858,
                "end": 1893
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "dotted_name": "devtools.context.planning.rendering",
            "kind": null
          },
          "mechanism": "python-module-exact-name-lookup",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "25c3d0c17e5ec56cf6d03360e76f3aaa3f2d871168e8f0348e95165d6a3e606c",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I08",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Introduce new tests/context/planning/test_manifest.py: establish surrounding integration contracts; this literal is a future destination, not an existing-evidence request",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "tests/context/planning/test_manifest.py",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "94ae0c2a8958c9e96cd918e354d8c343b31bdbd29e710c5e0f135110e27da21d"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2202,
                "end": 2241
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2202,
              "end": 2241
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "New destinations and conceptual purposes do not request existing exact evidence"
      },
      {
        "identity": "ec16d3be60d36912675c4b25a37790a976abd01376f615c633e1a9a375b843ea",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I09",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Inspect existing src/devtools/context/planning/docs/overview.md: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/docs/overview.md",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "src/devtools/context/planning/docs/overview.md",
            "span": {
              "start": 2539,
              "end": 2585
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "00fdd66ff260770b2dc6715e971b285106a97b12ae6e424403fdbee83b353cff"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2539,
                "end": 2585
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "src/devtools/context/planning/docs/overview.md"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "a673b02498327e27c529700b0df22cba26a9bd9c64af05c96a727e8b6371538d",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "I10",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Inspect existing pyproject.toml: establish its native contract specified by this task clause",
            "reason": "Caller explicitly distinguishes existing evidence from new feature destinations; lexical obligation coverage remains complete",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            },
            "anchors": [
              {
                "task": {
                  "value": "case-0013-context-disclosure-manifest"
                },
                "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
              }
            ]
          },
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "pyproject.toml",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "explanation": "Task-only caller syntax reference before frame preparation"
          }
        },
        "request": {
          "hint": {
            "task": {
              "value": "case-0013-context-disclosure-manifest"
            },
            "text": "pyproject.toml",
            "span": {
              "start": 2885,
              "end": 2899
            },
            "rule": "caller-task-review-v1",
            "syntactic_form": "caller-reviewed-task-syntax",
            "category": "RESOURCE_ADDRESS",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "association": {
            "hint": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "6f05d43a1a6346a973fd41349d2d10969431e7e13707cebfbfa4e0c2e340a31f"
            },
            "lane": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "reason": "Explicit task clause associates this hint with this obligation, without gold",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2885,
                "end": 2899
              },
              "explanation": "Task-only caller syntax reference before frame preparation"
            }
          },
          "locator": {
            "address": {
              "value": "pyproject.toml"
            }
          },
          "mechanism": "repository-snapshot-resource-at",
          "reason": "Explicit task syntax; static source locator in a frozen universe; no inferred owner"
        },
        "disposition": "EXACT_PLUS_LEXICAL",
        "reason": "Explicit typed native locator; original lexical lane remains complete"
      },
      {
        "identity": "3116249dca5b5f4350cc32de2c1a1688ada15407a372a41ac4cb4f31d85999d1",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/structure",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "structure"
            },
            "statement": "Understand Preserve exact materialized plan/item structure and native provenance.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 0,
                "end": 230
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 0,
              "end": 230
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "8df89421e6d8c3eb96ce97d6e1ae510668bb1699ed3343099fc89ef3fc61dd08",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/integrity",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "integrity"
            },
            "statement": "Understand Authenticate manifest support against retained native snapshot before publication.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 574,
                "end": 980
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 574,
              "end": 980
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "38279ae50ba1d3f0291bbed39ffe029c2f81930aaddfca371ca2e4794f8d830b",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/manifest",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "manifest"
            },
            "statement": "Understand Implement the future explicit manifest operation in common Context Planning.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 980,
                "end": 1458
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 980,
              "end": 1458
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "55e43b71fe604ecf4a4ef006dda1d7b3dd1abab03b3859c9724c5a8702fd9cf0",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/projection",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "projection"
            },
            "statement": "Understand Provide deterministic JSON-compatible presentation and distinct byte accounting.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1458,
                "end": 1829
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1458,
              "end": 1829
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "d081d5c7d5a7742dd52aa2e3b752b842aa8e773e3fcaf3cf4af549eb69a5a98e",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/compatibility",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "compatibility"
            },
            "statement": "Understand Preserve rendering and copied request assembly.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "226df641cbadaec613de4a9b8426e35204955c840163ca6ed27221200ee30e29",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/exports",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "exports"
            },
            "statement": "Understand Expose both public facades with existing dependency ownership.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 1829,
                "end": 2167
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 1829,
              "end": 2167
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "9cab74e392d53f786c6af46a108c021457c9c373c302c41de6b7d53622c8f909",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/tests",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "tests"
            },
            "statement": "Understand Establish focused and regression coverage for every new and preserved contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2167,
                "end": 2513
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2167,
              "end": 2513
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "a04b3eeedb93b8e48c49a770a13c20c87629fe567c8672ed8bec78ebf5e05865",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/documentation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "documentation"
            },
            "statement": "Understand Explain manifest fidelity applicability and limits in existing package documentation.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2513,
                "end": 2858
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2513,
              "end": 2858
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      },
      {
        "identity": "40708d5656d11faa6e170880207c382f2c36f6302daf4ff64a41301a4e46167c",
        "arm": "SELECTIVE_MECHANISM_ROUTER",
        "basis": {
          "need": {
            "key": "conceptual/validation",
            "obligation": {
              "task": {
                "value": "case-0013-context-disclosure-manifest"
              },
              "value": "validation"
            },
            "statement": "Understand Preserve the protected development and static validation contract.",
            "reason": "All conceptual obligation evidence remains eligible under canonical lexical fallback",
            "provenance": {
              "source_identity": "case-0013-context-disclosure-manifest",
              "span": {
                "start": 2858,
                "end": 3150
              },
              "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
            },
            "anchors": []
          },
          "hint": null,
          "association": null,
          "provenance": {
            "source_identity": "case-0013-context-disclosure-manifest",
            "span": {
              "start": 2858,
              "end": 3150
            },
            "explanation": "Caller conceptual purpose; exact anchors are optional and do not bound obligation coverage"
          }
        },
        "request": null,
        "disposition": "LEXICAL_ONLY",
        "reason": "No explicit native locator input"
      }
    ]
  },
  "extraction_decisions": [
    {
      "span": {
        "start": 258,
        "end": 317
      },
      "text": "devtools.context.planning.materialization.ContextDisclosure",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.materialization.ContextDisclosure",
        "span": {
          "start": 258,
          "end": 317
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_DIRECT_CLASS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 258,
            "end": 317
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 333,
        "end": 402
      },
      "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.materialization.materialize_disclosure_plan",
        "span": {
          "start": 333,
          "end": 402
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_DIRECT_FUNCTION",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 333,
            "end": 402
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 599,
        "end": 666
      },
      "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.repository.snapshot.RepositorySnapshot.resource_at",
        "span": {
          "start": 599,
          "end": 666
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_DIRECT_METHOD",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 599,
            "end": 666
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 1003,
        "end": 1063
      },
      "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.manifest.ContextDisclosureManifest",
        "span": {
          "start": 1003,
          "end": 1063
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_DIRECT_CLASS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1003,
            "end": 1063
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 1085,
        "end": 1147
      },
      "text": "devtools.context.planning.manifest.describe_context_disclosure",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.manifest.describe_context_disclosure",
        "span": {
          "start": 1085,
          "end": 1147
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_DIRECT_FUNCTION",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1085,
            "end": 1147
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 1166,
        "end": 1207
      },
      "text": "src/devtools/context/planning/manifest.py",
      "reason": "code-address-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "src/devtools/context/planning/manifest.py",
        "span": {
          "start": 1166,
          "end": 1207
        },
        "rule": "u2-task-syntax-v1/code-address-v1",
        "syntactic_form": "inline-code",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1166,
            "end": 1207
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 1858,
        "end": 1893
      },
      "text": "devtools.context.planning.rendering",
      "reason": "explicit-api-introduction-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "devtools.context.planning.rendering",
        "span": {
          "start": 1858,
          "end": 1893
        },
        "rule": "u2-task-syntax-v1/explicit-api-introduction-v1",
        "syntactic_form": "inline-code",
        "category": "PYTHON_MODULE",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 1858,
            "end": 1893
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 2202,
        "end": 2241
      },
      "text": "tests/context/planning/test_manifest.py",
      "reason": "code-address-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "tests/context/planning/test_manifest.py",
        "span": {
          "start": 2202,
          "end": 2241
        },
        "rule": "u2-task-syntax-v1/code-address-v1",
        "syntactic_form": "inline-code",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2202,
            "end": 2241
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 2539,
        "end": 2585
      },
      "text": "src/devtools/context/planning/docs/overview.md",
      "reason": "code-address-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "src/devtools/context/planning/docs/overview.md",
        "span": {
          "start": 2539,
          "end": 2585
        },
        "rule": "u2-task-syntax-v1/code-address-v1",
        "syntactic_form": "inline-code",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2539,
            "end": 2585
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    },
    {
      "span": {
        "start": 2885,
        "end": 2899
      },
      "text": "pyproject.toml",
      "reason": "code-address-v1",
      "observation": {
        "task": {
          "value": "case-0013-context-disclosure-manifest"
        },
        "text": "pyproject.toml",
        "span": {
          "start": 2885,
          "end": 2899
        },
        "rule": "u2-task-syntax-v1/code-address-v1",
        "syntactic_form": "inline-code",
        "category": "RESOURCE_ADDRESS",
        "provenance": {
          "source_identity": "case-0013-context-disclosure-manifest",
          "span": {
            "start": 2885,
            "end": 2899
          },
          "explanation": "Task text only; no repository lookup"
        }
      }
    }
  ]
}
```

Next: maintainer reviews this Stage A. Only after authorization execute frozen A/B/C once. No Stage B, feature implementation, productionization, R1.7 or BM25F is authorized by this freeze.

## Available mechanism inventory

# U3 mechanism inventory

Inspected at `b42dcb3fd93bd6ddb8af35f1cf8b3273f6486b4b`. This inventory is
contract inspection, not Case 0013 acquisition or target verification.

| Mechanism / owner | Accepted purpose and native input | Native output and qualification | Cost / frame and provenance | First U3 slice |
| --- | --- | --- | --- | --- |
| Canonical lexical resource BM25, context.retrieval.lexical | Conceptual or explicit evidence question; exact frozen query and whole-resource collection | All positive native rows; rank/score/contributions, native tie order; zero positive rows is a bounded miss | Full corpus analysis/index plus queries; native RepositoryId/SnapshotId/CorpusId and document/content identities | Always admitted, entire positive lane, k1=1.2/b=.75/filename=.25 |
| RESOURCE_ADDRESS, repository.snapshot.resource_at | Existing resource content; canonical relative address | One retained resource or bounded absence; no basename/glob expansion | Snapshot lookup and adapter validation; exact content identity | Admitted; new destination skipped only in C |
| PYTHON_MODULE, modules.lookup | Existing module contract; explicit dotted name and frozen explicit-root universe | All matching interpretations, duplicates ambiguous; no runtime importability/namespace inference | Address-only universe preparation shared; lookup and adapter cost; native root/resource/content identity | Admitted |
| PYTHON_DIRECT_FUNCTION / PYTHON_DIRECT_CLASS, modules.selection | Existing source declaration; explicit module/name/kind | Direct source declarations with selection analyses; repeats ambiguous, parser failure unsupported; decorators do not prove runtime binding | Per-request native parsing/selection and full provenance, no cross-arm outcome cache | Admitted as two reporting families; shared direct-declaration implementation |
| PYTHON_DIRECT_METHOD, classes.declarations/containment | Existing direct method; explicit module/class/method | Direct native class-body method after unique parent grounding; duplicate parent/method ambiguous; inherited/dynamic lookup unsupported | Parent selection plus method containment; retain both native accounts, aggregate route timer includes children | Admitted; no standalone broad containment scan |
| Exact declared-name acquisition, function.retrieval | Exact function name over explicit already established declaration knowledge | All matching evidence/supporting resources; bare names do not imply global uniqueness | Requires complete chosen analysis knowledge and its derivation/snapshot | Deferred alternate bare-name route; direct-source acquisition above is sufficient |
| Qualified Reference acquisition, function.qualified_reference / python.references | Native source Reference/Call occurrence and explicit established analyses | Bounded qualified reference/target disclosure, not task-prose symbol resolution | Native occurrence, derivation, dependencies and retained source validation; analysis/materialization cost | Deferred: task prose cannot fabricate native occurrence |
| Module binding lookup, modules.declarations | Explicit module/name over conservative binding analysis | Rebinding/decorators/dynamic syntax can block selection; runtime contract differs from source | Native source plus binding analyses | Deferred: first slice asks for source contracts |
| Import resolution/relations, python.imports | Native Import occurrence and explicit module universe | Directed relation only when uniquely established; module resolution does not prove exports | Native source/target/module/derivation dependencies, analysis cost | Deferred: no native Import occurrence in task text |
| Imported member resolution, imports.members | Native ImportFrom occurrence and one direct facade binding | Bounded one-facade direct function resolution; recursive/wildcard/class generalization unsupported | Source/facade/target support and snapshot; parse/resolution cost | Deferred |
| General bounded containment/declaration relationships | Already established native declarations/occurrences | Explicit partial native structural facts, not relevance or sufficiency | Native derivation, coverage and frame checks; chosen analysis costs | Only direct-method dependency admitted; no universal repository graph |

Evidence: existing U2 CAPABILITIES.md and routing/presentation contracts; native
repository resource/snapshot; module interpretation/lookup/selection/declarations;
class declarations/containment; function retrieval/planned_reference; imports
members/resolution/relations; references overview; grounding contract/resolve;
their existing controlled U2 tests. No production contracts were extended.
Unsupported/ambiguous/unresolved routes promote nothing, retain full fallback,
and remain qualified outcomes rather than automatic router defects.
