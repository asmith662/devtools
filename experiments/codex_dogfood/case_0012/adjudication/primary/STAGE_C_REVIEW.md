# PRIMARY blind Stage C adjudication

Case: `case-0012`; task: `case-0012-direct-source-disclosure`.

This adjudication establishes task/repository truth from the frozen packet. It does not claim the future feature is already implemented.

## Exact task

```text
Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.
Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.
Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.
Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.
Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.
Preserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.
Expose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.
Add focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.
Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.
Validate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.
```

## Boundary and packet digests

```json
{
  "exact_initial_files": [
    "README.md",
    "integrity.json",
    "manifest.json",
    "resources.json.gz",
    "validate_packet.py"
  ],
  "no_git": true,
  "no_local": true,
  "no_subdirectories": true,
  "no_symlinks_junctions_or_reparse_points": true,
  "supplied_validator_command": "python -B validate_packet.py",
  "supplied_validator_status": "VERIFIED; NO ADJUDICATION",
  "workspace": "C:\\Users\\recoveryadmin\\CodexSterile\\case_0012_stage_c_2cbc95afb120"
}
```

```json
{
  "archive_sha256": "2cbc95afb120c920ed8d919e37a187f8fe0eec4618eff28eb25203d108599fe3",
  "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
  "integrity_sha256": "89947624937675a94d6228e3c6fc6c206bc929600b4f21faf2f5cf22bf78a6f9",
  "manifest_sha256": "15c886a8af33bf2ba12c2a92e82ec3a33789a605064bded6f17ae4b603d579cf"
}
```

## Obligations and applicability

### source

Identity: `case-0012-direct-source-disclosure/source`

Statement: Establish supported direct function/class source selection and native direct-method containment, with source/binding scope distinctions.

Criterion: Complete native selection/containment contracts and unsupported runtime/import/inherited/semantic boundaries are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 209,
    "start": 0,
    "text": "Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.\n"
  },
  {
    "end": 531,
    "start": 209,
    "text": "Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.\n"
  }
]
```

### choices

Identity: `case-0012-direct-source-disclosure/choices`

Statement: Establish explicit immutable ordered Context Planning choice integration and compatibility.

Criterion: Purpose, frame, ordered choice invariants, admission and existing qualified-reference/whole-resource compatibility are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 209,
    "start": 0,
    "text": "Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.\n"
  },
  {
    "end": 752,
    "start": 531,
    "text": "Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.\n"
  }
]
```

### integrity

Identity: `case-0012-direct-source-disclosure/integrity`

Statement: Establish native frame/content/declaration validation before disclosure publication without reacquisition.

Criterion: Foreign/stale/content/missing-resource/scope/returned-identity checks and publication ordering are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 1105,
    "start": 752,
    "text": "Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.\n"
  }
]
```

### materialization

Identity: `case-0012-direct-source-disclosure/materialization`

Statement: Establish exact source-segment materialization, provenance, UTF-8 boundaries and faithful mixed-plan order.

Criterion: Source-range, derivation, owner provenance, decorators, CRLF/non-ASCII and ordered mixed representations are established without implicit expansion or sufficiency.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 1415,
    "start": 1105,
    "text": "Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.\n"
  }
]
```

### assembly

Identity: `case-0012-direct-source-disclosure/assembly`

Statement: Establish unchanged rendering and copied-request semantics without new budgets.

Criterion: Original fields/tools and prompt role, task-before-Context copying, rendering compatibility and absence of truncation changes are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 1702,
    "start": 1415,
    "text": "Preserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.\n"
  }
]
```

### exports

Identity: `case-0012-direct-source-disclosure/exports`

Statement: Establish common planning and outer facade exports and permitted dependency ownership.

Criterion: Both public boundaries and absence of Retrieval/language-specific common assembly dependencies are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 1910,
    "start": 1702,
    "text": "Expose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.\n"
  }
]
```

### tests

Identity: `case-0012-direct-source-disclosure/tests`

Statement: Establish focused and regression test conventions for every new and preserved contract.

Criterion: Direct/decorated/repeated declarations, mixed exact provenance, rejection, old choices and copied-request preservation tests are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 2158,
    "start": 1910,
    "text": "Add focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.\n"
  }
]
```

### documentation

Identity: `case-0012-direct-source-disclosure/documentation`

Statement: Establish package and architecture documentation to update with supported/deferred source-disclosure scope.

Criterion: Source versus runtime binding, explicit admission, compatibility and no automatic relevance/readiness claims are documented.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 2433,
    "start": 2158,
    "text": "Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.\n"
  }
]
```

### validation

Identity: `case-0012-direct-source-disclosure/validation`

Statement: Establish the complete protected validation/tooling contract and preserved configuration.

Criterion: Protected development entry/scope and pytest/coverage retention, Ruff lint/format, strict mypy, worktree/index checks and excluded confirmation boundary are established.

Frozen applicability: MANDATORY for the selected future source-disclosure task; independent gold may retain NOT_APPLICABLE only with explicit rationale

```json
{
  "inferability_at_task_start": "The task fixes required behavior. The cited frozen native contracts support bounded implementation reasoning; future source-choice behavior is not claimed already implemented.",
  "rationale": "This mandatory obligation has direct basis in the supplied feature task; no condition excludes it.",
  "status": "APPLICABLE"
}
```

Exact task basis/provenance:

```json
[
  {
    "end": 2668,
    "start": 2433,
    "text": "Validate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.\n"
  }
]
```

## Task-interpretation audit

48 substantive clauses covered; no TASK_INTERPRETATION_GAP.

- **task-clause-01-01 — COVERED**: Add caller-selected direct Python source-declaration disclosure choices to common Context Planning
  Obligations: case-0012-direct-source-disclosure/source, case-0012-direct-source-disclosure/choices. [evidence-0098](#evidence-0098)

- **task-clause-01-02 — COVERED**: alongside existing qualified-reference and whole-resource choices
  Obligations: case-0012-direct-source-disclosure/source, case-0012-direct-source-disclosure/choices. [evidence-0099](#evidence-0099)

- **task-clause-01-03 — COVERED**: without automatic retrieval or selection.
  Obligations: case-0012-direct-source-disclosure/source, case-0012-direct-source-disclosure/choices. [evidence-0100](#evidence-0100)

- **task-clause-02-01 — COVERED**: Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities
  Obligations: case-0012-direct-source-disclosure/source. [evidence-0101](#evidence-0101)

- **task-clause-02-02 — COVERED**: support a direct method only through its validated native class parent and containment
  Obligations: case-0012-direct-source-disclosure/source. [evidence-0102](#evidence-0102)

- **task-clause-02-03 — COVERED**: without runtime attribute, imported-facade, inherited-method or semantic resolution.
  Obligations: case-0012-direct-source-disclosure/source. [evidence-0103](#evidence-0103)

- **task-clause-03-01 — COVERED**: Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`
  Obligations: case-0012-direct-source-disclosure/choices. [evidence-0104](#evidence-0104)

- **task-clause-03-02 — COVERED**: retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.
  Obligations: case-0012-direct-source-disclosure/choices. [evidence-0105](#evidence-0105)

- **task-clause-04-01 — COVERED**: Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0106](#evidence-0106)

- **task-clause-04-02 — COVERED**: reject foreign or stale frame/content
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0107](#evidence-0107)

- **task-clause-04-03 — COVERED**: missing resource
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0108](#evidence-0108)

- **task-clause-04-04 — COVERED**: unsupported declaration scope
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0109](#evidence-0109)

- **task-clause-04-05 — COVERED**: mismatched returned identity before publishing the disclosure
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0110](#evidence-0110)

- **task-clause-04-06 — COVERED**: without reacquiring files.
  Obligations: case-0012-direct-source-disclosure/integrity. [evidence-0111](#evidence-0111)

- **task-clause-05-01 — COVERED**: Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0112](#evidence-0112)

- **task-clause-05-02 — COVERED**: preserve UTF-8 boundaries
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0113](#evidence-0113)

- **task-clause-05-03 — COVERED**: decorators
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0115](#evidence-0115)

- **task-clause-05-04 — COVERED**: CRLF/non-ASCII bytes
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0116](#evidence-0116)

- **task-clause-05-05 — COVERED**: caller order in mixed plans
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0117](#evidence-0117)

- **task-clause-05-06 — COVERED**: without inferring sufficiency or expanding to whole owners implicitly.
  Obligations: case-0012-direct-source-disclosure/materialization. [evidence-0118](#evidence-0118)

- **task-clause-06-01 — COVERED**: Preserve common rendering and copied request assembly with class `ModelRequest`
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0119](#evidence-0119)

- **task-clause-06-02 — COVERED**: original request
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0120](#evidence-0120)

- **task-clause-06-03 — COVERED**: prompt role
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0122](#evidence-0122)

- **task-clause-06-04 — COVERED**: settings
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0123](#evidence-0123)

- **task-clause-06-05 — COVERED**: conversation
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0124](#evidence-0124)

- **task-clause-06-06 — COVERED**: provider settings and tools remain unchanged except the copied prompt
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0125](#evidence-0125)

- **task-clause-06-07 — COVERED**: keep task text before Context
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0126](#evidence-0126)

- **task-clause-06-08 — COVERED**: introduce no new budget or truncation policy.
  Obligations: case-0012-direct-source-disclosure/assembly. [evidence-0127](#evidence-0127)

- **task-clause-07-01 — COVERED**: Expose the new explicit choice through the common planning public API and outer Context facade
  Obligations: case-0012-direct-source-disclosure/exports. [evidence-0128](#evidence-0128)

- **task-clause-07-02 — COVERED**: keeping dependency direction
  Obligations: case-0012-direct-source-disclosure/exports. [evidence-0129](#evidence-0129)

- **task-clause-07-03 — COVERED**: avoiding a Retrieval dependency or language-specific logic in common assembly.
  Obligations: case-0012-direct-source-disclosure/exports. [evidence-0130](#evidence-0130)

- **task-clause-08-01 — COVERED**: Add focused tests for direct function/class/method choices
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0131](#evidence-0131)

- **task-clause-08-02 — COVERED**: decorated and repeated declarations
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0133](#evidence-0133)

- **task-clause-08-03 — COVERED**: mixed-plan ordering and exact source/provenance
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0134](#evidence-0134)

- **task-clause-08-04 — COVERED**: stale/foreign/missing-resource rejection
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0135](#evidence-0135)

- **task-clause-08-05 — COVERED**: unchanged existing choices
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0136](#evidence-0136)

- **task-clause-08-06 — COVERED**: copied-request preservation.
  Obligations: case-0012-direct-source-disclosure/tests. [evidence-0137](#evidence-0137)

- **task-clause-09-01 — COVERED**: Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md`
  Obligations: case-0012-direct-source-disclosure/documentation. [evidence-0138](#evidence-0138)

- **task-clause-09-02 — COVERED**: to explain source identity versus runtime bindings
  Obligations: case-0012-direct-source-disclosure/documentation. [evidence-0139](#evidence-0139)

- **task-clause-09-03 — COVERED**: explicit representation admission
  Obligations: case-0012-direct-source-disclosure/documentation. [evidence-0141](#evidence-0141)

- **task-clause-09-04 — COVERED**: supported/deferred scope and compatibility
  Obligations: case-0012-direct-source-disclosure/documentation. [evidence-0142](#evidence-0142)

- **task-clause-09-05 — COVERED**: without claiming automatic relevance or readiness.
  Obligations: case-0012-direct-source-disclosure/documentation. [evidence-0143](#evidence-0143)

- **task-clause-10-01 — COVERED**: Validate with file `scripts/validate_development.py`
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0144](#evidence-0144)

- **task-clause-10-02 — COVERED**: preserve file `pyproject.toml` test/coverage settings
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0145](#evidence-0145)

- **task-clause-10-03 — COVERED**: run the documented protected development profile
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0146](#evidence-0146)

- **task-clause-10-04 — COVERED**: Ruff lint/format
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0147](#evidence-0147)

- **task-clause-10-05 — COVERED**: strict mypy
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0148](#evidence-0148)

- **task-clause-10-06 — COVERED**: both worktree/index whitespace checks.
  Obligations: case-0012-direct-source-disclosure/validation. [evidence-0149](#evidence-0149)


## Cell counts and required-resource union

```json
{
  "cell_count": 4779,
  "cell_counts": {
    "HELPFUL_ONLY": 49,
    "REQUIRED": 28,
    "UNNECESSARY": 4702,
    "UNRESOLVED": 0
  }
}
```

```json
{
  "assembly": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 5,
      "REQUIRED": 1,
      "UNNECESSARY": 525,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/planning/rendering.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/planning/rendering.py"
    ],
    "required_unit_count": 3
  },
  "choices": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 7,
      "REQUIRED": 3,
      "UNNECESSARY": 521,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/function/planned_reference.py"
      ],
      "units": [
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/function/planned_reference.py"
    ],
    "required_unit_count": 7
  },
  "documentation": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 6,
      "REQUIRED": 2,
      "UNNECESSARY": 523,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "docs/architecture.md",
        "src/devtools/context/planning/docs/overview.md"
      ],
      "units": [
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims"
      ]
    },
    "required_resource_union": [
      "docs/architecture.md",
      "src/devtools/context/planning/docs/overview.md"
    ],
    "required_unit_count": 3
  },
  "exports": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 3,
      "REQUIRED": 4,
      "UNNECESSARY": 524,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py"
      ],
      "units": [
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py"
    ],
    "required_unit_count": 4
  },
  "integrity": {
    "alternative_count": 2,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 6,
      "REQUIRED": 5,
      "UNNECESSARY": 520,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    "required_unit_count": 7
  },
  "materialization": {
    "alternative_count": 2,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 4,
      "REQUIRED": 5,
      "UNNECESSARY": 522,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/python/function/materialization.py"
      ],
      "units": [
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py"
    ],
    "required_unit_count": 6
  },
  "source": {
    "alternative_count": 4,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 6,
      "REQUIRED": 6,
      "UNNECESSARY": 519,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "src/devtools/context/python/function/declarations.py"
      ],
      "units": [
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector"
      ]
    },
    "required_resource_union": [
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py"
    ],
    "required_unit_count": 6
  },
  "tests": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 9,
      "REQUIRED": 0,
      "UNNECESSARY": 522,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [],
      "units": [
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation"
      ]
    },
    "required_resource_union": [],
    "required_unit_count": 10
  },
  "validation": {
    "alternative_count": 1,
    "applicability": "APPLICABLE",
    "cell_counts": {
      "HELPFUL_ONLY": 3,
      "REQUIRED": 2,
      "UNNECESSARY": 526,
      "UNRESOLVED": 0
    },
    "indispensable": {
      "resources": [
        "docs/development/validation.md",
        "pyproject.toml"
      ],
      "units": [
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    "required_resource_union": [
      "docs/development/validation.md",
      "pyproject.toml"
    ],
    "required_unit_count": 6
  }
}
```

The required-resource union is a union of acceptable alternatives, not a requirement to read all resources together.

```json
[
  "docs/architecture.md",
  "docs/development/validation.md",
  "pyproject.toml",
  "src/devtools/context/__init__.py",
  "src/devtools/context/planning/__init__.py",
  "src/devtools/context/planning/docs/overview.md",
  "src/devtools/context/planning/materialization.py",
  "src/devtools/context/planning/plan.py",
  "src/devtools/context/planning/rendering.py",
  "src/devtools/context/planning/resource.py",
  "src/devtools/context/python/classes/containment.py",
  "src/devtools/context/python/classes/declarations.py",
  "src/devtools/context/python/classes/docs/overview.md",
  "src/devtools/context/python/function/declarations.py",
  "src/devtools/context/python/function/materialization.py",
  "src/devtools/context/python/function/planned_reference.py",
  "src/devtools/context/python/modules/docs/overview.md",
  "src/devtools/context/python/modules/selection.py",
  "src/devtools/context/repository/snapshot.py",
  "tests/context/planning/test_plan.py"
]
```

## All positive resources by obligation

### source

- **HELPFUL_ONLY — `src/devtools/context/localization/grounding/resolve.py`**
  Document: `7776e3bf22c9fc0658855e1b11bc84f78d9d6970fd6bb59987594c506cce0f35`; content: `cc9086d27d2929f521f47680bd5a7e64b78f88e4e035bdbcbe87d549b9ff7ba8`.
  An existing consumer demonstrates canonical selector reuse and method-parent containment, without becoming necessary for Context implementation or introducing a Localization dependency.
  Units: none required. Evidence: [evidence-0019](#evidence-0019), [evidence-0020](#evidence-0020)

- **REQUIRED — `src/devtools/context/python/classes/containment.py`**
  Document: `fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175`; content: `47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f`.
  Establishes necessary unit(s) source.containment. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.containment. Evidence: [evidence-0037](#evidence-0037), [evidence-0038](#evidence-0038)

- **REQUIRED — `src/devtools/context/python/classes/declarations.py`**
  Document: `b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd`; content: `f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73`.
  Establishes necessary unit(s) source.class-identity, source.method-identity. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.class-identity, source.method-identity. Evidence: [evidence-0040](#evidence-0040), [evidence-0041](#evidence-0041), [evidence-0042](#evidence-0042)

- **REQUIRED — `src/devtools/context/python/classes/docs/overview.md`**
  Document: `f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd`; content: `83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9`.
  Establishes necessary unit(s) source.class-identity, source.containment, source.method-identity. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.class-identity, source.containment, source.method-identity. Evidence: [evidence-0045](#evidence-0045), [evidence-0048](#evidence-0048)

- **HELPFUL_ONLY — `src/devtools/context/python/function/containment.py`**
  Document: `c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8`; content: `7af4524a28e61dc608e35c9ab4ff34c0bc486fb1ef54a3521f9fb0735eb25d69`.
  A validated function-ownership navigation example is useful, but direct function selection already carries native owner support and the task only mandates the native method-parent route.
  Units: none required. Evidence: [evidence-0049](#evidence-0049)

- **REQUIRED — `src/devtools/context/python/function/declarations.py`**
  Document: `038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa`; content: `2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66`.
  Establishes necessary unit(s) source.function-identity. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.function-identity. Evidence: [evidence-0051](#evidence-0051), [evidence-0053](#evidence-0053), [evidence-0054](#evidence-0054)

- **HELPFUL_ONLY — `src/devtools/context/python/function/docs/overview.md`**
  Document: `5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920`; content: `6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d`.
  Explains intrinsic function ownership and source-versus-binding scope; native identity schema and selector already supply the required facts.
  Units: none required. Evidence: [evidence-0056](#evidence-0056)

- **HELPFUL_ONLY — `src/devtools/context/python/modules/declarations.py`**
  Document: `e2cc21c89da653801bf7f0ac37d116e358f959b729b7fcb941fc483bbca7dd3a`; content: `e54171b465bb78a21c1c380321d1f04f69771982db02f4cd1b140b36423283be`.
  The competing binding-oriented API illustrates why decorated/repeated source selection must not use unique runtime-like binding policy; the canonical selector already establishes the needed boundary.
  Units: none required. Evidence: [evidence-0065](#evidence-0065)

- **REQUIRED — `src/devtools/context/python/modules/docs/overview.md`**
  Document: `8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95`; content: `fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08`.
  Establishes necessary unit(s) source.selector. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.selector. Evidence: [evidence-0067](#evidence-0067)

- **HELPFUL_ONLY — `src/devtools/context/python/modules/interpretation.py`**
  Document: `54ffd27dd2b175d1f12987c030f3ec13b4718f6237127bcdd7163f838f12e15b`; content: `b858bbdd8ea4d0a8e9a3193ae29176947ef0796f949025a6bf3866ea7caf9dbd`.
  Defines the retained module interpretation input. The needed frame/resource fields are already exposed by the selector and task; no new root discovery is required.
  Units: none required. Evidence: [evidence-0068](#evidence-0068)

- **REQUIRED — `src/devtools/context/python/modules/selection.py`**
  Document: `f9a7943390f82d8e1399edaa66aebd172b43ad5a85838285c134ec03f5ad89af`; content: `8017f8d2153eb217b57cee49b78841073b752e675539254d54c13a6979eadc6f`.
  Establishes necessary unit(s) source.selector. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: source.selector. Evidence: [evidence-0069](#evidence-0069), [evidence-0070](#evidence-0070)

- **HELPFUL_ONLY — `tests/context/python/modules/test_selection.py`**
  Document: `87491fef6cbd5c7986a6522574fccb34cddbe0194fe73e4563404c29d8acdf83`; content: `97ec04ba3d29c5c4984678ec389ca11172738134335ad17b160171e7e5192541`.
  Concrete cases corroborate decorated and repeated native source identities; they do not replace the full selected native function subject schema.
  Units: none required. Evidence: [evidence-0090](#evidence-0090), [evidence-0091](#evidence-0091)



### choices

- **HELPFUL_ONLY — `docs/architecture.md`**
  Document: `04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391`; content: `fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b`.
  Corroborates the bounded explicit plan and two old representations; the concrete protocol/options provide complete necessary contracts.
  Units: none required. Evidence: [evidence-0002](#evidence-0002)

- **HELPFUL_ONLY — `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md`**
  Document: `3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb`; content: `d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f`.
  Accepted architectural distinction between selection and assembly is useful background; the task and concrete common contracts already establish the necessary bounded change.
  Units: none required. Evidence: [evidence-0006](#evidence-0006)

- **HELPFUL_ONLY — `docs/architecture/taxonomy.md`**
  Document: `e13fc10a26ce00bb5fc7641ea0ac13d59bbf6872873bac1c00021fd86a762f01`; content: `24677a057596cb8157bd77407c35ff82c4cc58c27908ddb72e32f79e266a010e`.
  Taxonomy corroborates immutable plan/disclosure and semantic-strength boundaries; it is not necessary merely because it is broad architectural background.
  Units: none required. Evidence: [evidence-0008](#evidence-0008)

- **HELPFUL_ONLY — `src/devtools/context/planning/docs/overview.md`**
  Document: `de0155f1cfe9bdb78fffb3e8897785e5a32f6147ddcd291c3bc7d67f7f9b274a`; content: `a679cfa5ee0591036eaab418fa386a0885ef748f98287b8dd49846c093b068bd`.
  Summarizes the common plan and materialization contracts, but does not replace the exact admission protocol/invariants and old adapters.
  Units: none required. Evidence: [evidence-0022](#evidence-0022)

- **REQUIRED — `src/devtools/context/planning/plan.py`**
  Document: `09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493`; content: `8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998`.
  Establishes necessary unit(s) choices.admission, choices.plan-admission, choices.plan-identity, choices.plan-value. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: choices.admission, choices.plan-admission, choices.plan-identity, choices.plan-value. Evidence: [evidence-0027](#evidence-0027), [evidence-0028](#evidence-0028), [evidence-0029](#evidence-0029), [evidence-0030](#evidence-0030)

- **REQUIRED — `src/devtools/context/planning/resource.py`**
  Document: `0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5`; content: `f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b`.
  Establishes necessary unit(s) choices.whole-compatibility. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: choices.whole-compatibility. Evidence: [evidence-0035](#evidence-0035), [evidence-0036](#evidence-0036)

- **HELPFUL_ONLY — `src/devtools/context/python/function/docs/overview.md`**
  Document: `5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920`; content: `6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d`.
  Corroborates unchanged qualified-reference adaptation without independently providing the complete common item contract.
  Units: none required. Evidence: [evidence-0057](#evidence-0057)

- **REQUIRED — `src/devtools/context/python/function/planned_reference.py`**
  Document: `0e85d7f5109d5129516027b53f9a466471a2317aded85a7d7e7761777a94b701`; content: `a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381`.
  Establishes necessary unit(s) choices.reference-compatibility. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: choices.reference-compatibility. Evidence: [evidence-0060](#evidence-0060), [evidence-0061](#evidence-0061)

- **HELPFUL_ONLY — `src/devtools/context/python/function/qualified_reference.py`**
  Document: `e9818d20ebf2bf2abdb3e49ac8b43398512fcb0d90e5736e7b9d60c4ce28fdb3`; content: `f38207363dcef35c196eac7dd5ab939335e73a9aec507886af7bbdcee7008c69`.
  Underlying reference implementation adds useful rejection details. The adapter delegates unchanged, so re-establishing its entire resolver is not necessary for adding the direct-source choice.
  Units: none required. Evidence: [evidence-0062](#evidence-0062), [evidence-0063](#evidence-0063)

- **HELPFUL_ONLY — `tests/context/planning/test_plan.py`**
  Document: `7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088`; content: `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`.
  Regresses existing plan order and old choices, but does not replace the complete choice identity/admission contract.
  Units: none required. Evidence: [evidence-0076](#evidence-0076), [evidence-0077](#evidence-0077)



### integrity

- **HELPFUL_ONLY — `src/devtools/context/localization/grounding/resolve.py`**
  Document: `7776e3bf22c9fc0658855e1b11bc84f78d9d6970fd6bb59987594c506cce0f35`; content: `cc9086d27d2929f521f47680bd5a7e64b78f88e4e035bdbcbe87d549b9ff7ba8`.
  Corroborates canonical parent membership checking after retained-source derivation. The canonical native selector and containment mechanisms already establish the needed strategy.
  Units: none required. Evidence: [evidence-0020](#evidence-0020)

- **REQUIRED — `src/devtools/context/planning/materialization.py`**
  Document: `e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8`; content: `8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315`.
  Establishes necessary unit(s) integrity.plan-frame, integrity.publication, integrity.returned-identity. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: integrity.plan-frame, integrity.publication, integrity.returned-identity. Evidence: [evidence-0025](#evidence-0025), [evidence-0026](#evidence-0026)

- **HELPFUL_ONLY — `src/devtools/context/planning/resource.py`**
  Document: `0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5`; content: `f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b`.
  Provides a retained-resource validation pattern; resource_at and native selector/containment already establish required facts.
  Units: none required. Evidence: [evidence-0035](#evidence-0035)

- **REQUIRED — `src/devtools/context/python/classes/containment.py`**
  Document: `fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175`; content: `47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f`.
  Establishes necessary unit(s) integrity.canonical-membership, integrity.method-frame. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: integrity.canonical-membership, integrity.method-frame. Evidence: [evidence-0038](#evidence-0038)

- **HELPFUL_ONLY — `src/devtools/context/python/function/containment.py`**
  Document: `c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8`; content: `7af4524a28e61dc608e35c9ab4ff34c0bc486fb1ef54a3521f9fb0735eb25d69`.
  Useful provenance checks for supplied function analyses; canonical selector membership and native dependency facts already establish the mandatory validation strategy.
  Units: none required. Evidence: [evidence-0049](#evidence-0049)

- **HELPFUL_ONLY — `src/devtools/context/python/function/qualified_reference.py`**
  Document: `e9818d20ebf2bf2abdb3e49ac8b43398512fcb0d90e5736e7b9d60c4ce28fdb3`; content: `f38207363dcef35c196eac7dd5ab939335e73a9aec507886af7bbdcee7008c69`.
  Corroborates validation before exact extraction; imported-reference route is preserved rather than required for new direct-source admission.
  Units: none required. Evidence: [evidence-0063](#evidence-0063)

- **HELPFUL_ONLY — `src/devtools/context/python/modules/docs/overview.md`**
  Document: `8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95`; content: `fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08`.
  Supports a duplicated fact, but other jointly necessary members already supply that fact in every minimal alternative; requiring it would add a redundant member.
  Units: none required. Evidence: [evidence-0066](#evidence-0066)

- **REQUIRED — `src/devtools/context/python/modules/selection.py`**
  Document: `f9a7943390f82d8e1399edaa66aebd172b43ad5a85838285c134ec03f5ad89af`; content: `8017f8d2153eb217b57cee49b78841073b752e675539254d54c13a6979eadc6f`.
  Establishes necessary unit(s) integrity.canonical-membership, integrity.selection-frame. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: integrity.canonical-membership, integrity.selection-frame. Evidence: [evidence-0070](#evidence-0070)

- **HELPFUL_ONLY — `src/devtools/context/repository/observation.py`**
  Document: `3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da`; content: `84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51`.
  Explains the native length-framed content identity of retained resources. The task requires comparison to retained occurrences rather than recomputing observation or reacquiring files, so observation is optional background.
  Units: none required. Evidence: [evidence-0071](#evidence-0071), [evidence-0072](#evidence-0072)

- **REQUIRED — `src/devtools/context/repository/snapshot.py`**
  Document: `71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7`; content: `492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098`.
  Establishes necessary unit(s) integrity.lookup. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: integrity.lookup. Evidence: [evidence-0073](#evidence-0073)

- **REQUIRED — `tests/context/planning/test_plan.py`**
  Document: `7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088`; content: `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`.
  Establishes necessary unit(s) integrity.plan-frame, integrity.publication, integrity.returned-identity. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: integrity.plan-frame, integrity.publication, integrity.returned-identity. Evidence: [evidence-0078](#evidence-0078), [evidence-0079](#evidence-0079), [evidence-0080](#evidence-0080)



### materialization

- **HELPFUL_ONLY — `docs/architecture/taxonomy.md`**
  Document: `e13fc10a26ce00bb5fc7641ea0ac13d59bbf6872873bac1c00021fd86a762f01`; content: `24677a057596cb8157bd77407c35ff82c4cc58c27908ddb72e32f79e266a010e`.
  Taxonomy corroborates immutable plan/disclosure and semantic-strength boundaries; it is not necessary merely because it is broad architectural background.
  Units: none required. Evidence: [evidence-0008](#evidence-0008)

- **REQUIRED — `src/devtools/context/planning/materialization.py`**
  Document: `e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8`; content: `8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315`.
  Establishes necessary unit(s) materialization.item-provenance, materialization.mixed-order. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: materialization.item-provenance, materialization.mixed-order. Evidence: [evidence-0024](#evidence-0024), [evidence-0025](#evidence-0025), [evidence-0026](#evidence-0026)

- **HELPFUL_ONLY — `src/devtools/context/planning/resource.py`**
  Document: `0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5`; content: `f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b`.
  Shows exact retained CRLF-bearing whole-resource realization; this is a different representation and cannot be necessary for exact declaration extraction.
  Units: none required. Evidence: [evidence-0035](#evidence-0035)

- **REQUIRED — `src/devtools/context/python/classes/declarations.py`**
  Document: `b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd`; content: `f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73`.
  Establishes necessary unit(s) materialization.decorator-boundary. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: materialization.decorator-boundary. Evidence: [evidence-0043](#evidence-0043), [evidence-0044](#evidence-0044)

- **REQUIRED — `src/devtools/context/python/classes/docs/overview.md`**
  Document: `f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd`; content: `83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9`.
  Establishes necessary unit(s) materialization.coordinates, materialization.decorator-boundary. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: materialization.coordinates, materialization.decorator-boundary. Evidence: [evidence-0046](#evidence-0046), [evidence-0047](#evidence-0047)

- **REQUIRED — `src/devtools/context/python/function/declarations.py`**
  Document: `038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa`; content: `2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66`.
  Establishes necessary unit(s) materialization.coordinates, materialization.decorator-boundary. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: materialization.coordinates, materialization.decorator-boundary. Evidence: [evidence-0050](#evidence-0050), [evidence-0055](#evidence-0055)

- **REQUIRED — `src/devtools/context/python/function/materialization.py`**
  Document: `0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5`; content: `d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5`.
  Establishes necessary unit(s) materialization.extraction. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: materialization.extraction. Evidence: [evidence-0058](#evidence-0058), [evidence-0059](#evidence-0059)

- **HELPFUL_ONLY — `src/devtools/context/python/function/planned_reference.py`**
  Document: `0e85d7f5109d5129516027b53f9a466471a2317aded85a7d7e7761777a94b701`; content: `a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381`.
  Concrete common-item native provenance example; the common carrier and native source contracts suffice.
  Units: none required. Evidence: [evidence-0060](#evidence-0060)

- **HELPFUL_ONLY — `tests/context/planning/test_plan.py`**
  Document: `7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088`; content: `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`.
  Existing mixed-plan CRLF/non-ASCII regression is useful; the common item/publication carrier already entails caller order in every complete alternative, so this duplicate order evidence is optional.
  Units: none required. Evidence: [evidence-0076](#evidence-0076)



### assembly

- **HELPFUL_ONLY — `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md`**
  Document: `3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb`; content: `d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f`.
  Accepted architectural distinction between selection and assembly is useful background; the task and concrete common contracts already establish the necessary bounded change.
  Units: none required. Evidence: [evidence-0006](#evidence-0006)

- **REQUIRED — `src/devtools/context/planning/rendering.py`**
  Document: `edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f`; content: `741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7`.
  Establishes necessary unit(s) assembly.rendering, assembly.request-copy. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: assembly.rendering, assembly.request-copy. Evidence: [evidence-0032](#evidence-0032), [evidence-0033](#evidence-0033), [evidence-0034](#evidence-0034)

- **HELPFUL_ONLY — `src/devtools/context/python/function/request_assembly.py`**
  Document: `d0683bff077bc951cd4f02a215e96323dbb4ed78587cbcddd9a12df9ec0b9c8a`; content: `27bfd8eb7c177577cc410c7e19c47cd8724a6b93200dd15e2ac8d55d4bb4d152`.
  Older language-specific assembly demonstrates the same copy pattern; preserving common assembly requires its own renderer/assembler.
  Units: none required. Evidence: [evidence-0064](#evidence-0064)

- **HELPFUL_ONLY — `src/devtools/models/interaction/models.py`**
  Document: `4e1cded7a20da8216abfbe52f6dc2db1ca2c04cdede2d40793162e86c4d87d17`; content: `6eb9d64480b0c9ab9ad6e0185f63006d0b7635e824cac8d7c111211d9926466f`.
  Corroborates the typed field inventory and immutability. The task names preserved fields and the common replace-only-prompt implementation preserves all of them.
  Units: none required. Evidence: [evidence-0074](#evidence-0074)

- **HELPFUL_ONLY — `src/devtools/models/interaction/prompt.py`**
  Document: `b79574a0110b54911e28921f9b7f5228a985b8921de1181a962e459d9c8c7fec`; content: `39cb6fee3466d10d96f263871246453ab95137459390d0f2553642c965b731f4`.
  Corroborates the immutable content/role value; those fields are directly used in the necessary common assembler.
  Units: none required. Evidence: [evidence-0075](#evidence-0075)

- **HELPFUL_ONLY — `tests/context/planning/test_plan.py`**
  Document: `7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088`; content: `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`.
  Corroborates original request, role and settings preservation but does not supply a complete common rendering contract.
  Units: none required. Evidence: [evidence-0076](#evidence-0076)



### exports

- **HELPFUL_ONLY — `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md`**
  Document: `3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb`; content: `d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f`.
  Accepted architectural distinction between selection and assembly is useful background; the task and concrete common contracts already establish the necessary bounded change.
  Units: none required. Evidence: [evidence-0006](#evidence-0006)

- **REQUIRED — `src/devtools/context/__init__.py`**
  Document: `e44bbb91c8804801b3ec8c1731768a79edb711856c5773559b29b654d25ac198`; content: `e2392c9351df7a0f17f23f2ccd15e3fd1436c4e59eb7e0ee9eb7d0d0c32a445c`.
  Establishes necessary unit(s) exports.outer-surface. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: exports.outer-surface. Evidence: [evidence-0017](#evidence-0017), [evidence-0018](#evidence-0018)

- **REQUIRED — `src/devtools/context/planning/__init__.py`**
  Document: `4950d26efdac0ac7b2855daddf9406849e26a401d0a5f6a31840aca64f4eea5d`; content: `f0a22d1b55645d1c428dd456c527cbe41e36ebbcaab3ca09229498d3e2f7f8d3`.
  Establishes necessary unit(s) exports.planning-surface. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: exports.planning-surface. Evidence: [evidence-0021](#evidence-0021)

- **HELPFUL_ONLY — `src/devtools/context/planning/materialization.py`**
  Document: `e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8`; content: `8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315`.
  Shows generic option dispatch as a dependency ownership example. The public surfaces, protocol, and common assembly already supply the required seams.
  Units: none required. Evidence: [evidence-0026](#evidence-0026)

- **REQUIRED — `src/devtools/context/planning/plan.py`**
  Document: `09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493`; content: `8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998`.
  Establishes necessary unit(s) exports.option-ownership. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: exports.option-ownership. Evidence: [evidence-0027](#evidence-0027)

- **REQUIRED — `src/devtools/context/planning/rendering.py`**
  Document: `edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f`; content: `741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7`.
  Establishes necessary unit(s) exports.assembly-ownership. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: exports.assembly-ownership. Evidence: [evidence-0031](#evidence-0031)

- **HELPFUL_ONLY — `src/devtools/context/python/function/planned_reference.py`**
  Document: `0e85d7f5109d5129516027b53f9a466471a2317aded85a7d7e7761777a94b701`; content: `a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381`.
  Provides an existing Python-owned adapter pattern; no redesign of this adapter is required.
  Units: none required. Evidence: [evidence-0060](#evidence-0060)



### tests

- **HELPFUL_ONLY — `pyproject.toml`**
  Document: `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0`; content: `e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145`.
  Confirms the configured pytest/strict-marker/coverage convention used to add tests. The mandatory semantic test matrix comes from the task; exact configuration preservation is required separately under validation.
  Units: none required. Evidence: [evidence-0013](#evidence-0013)

- **HELPFUL_ONLY — `tests/context/planning/test_plan.py`**
  Document: `7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088`; content: `641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492`.
  Reusable mixed-plan, rejection and copied-request regression examples; the mandatory test categories are fully fixed by the task.
  Units: none required. Evidence: [evidence-0076](#evidence-0076), [evidence-0079](#evidence-0079)

- **HELPFUL_ONLY — `tests/context/python/classes/test_declarations.py`**
  Document: `750c22bae743779b23838b909394f7cb83dae21e4f04ceab4a972bc02d4460b0`; content: `40acd74906703279d4d9251d72820354d488dabb5603c2bbd265d761755a726c`.
  Direct class/method containment regression examples; equivalent focused cases can be written from native contracts.
  Units: none required. Evidence: [evidence-0081](#evidence-0081), [evidence-0082](#evidence-0082)

- **HELPFUL_ONLY — `tests/context/python/function/test_declarations.py`**
  Document: `a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6`; content: `9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50`.
  Repeated subject and UTF-8 occurrence examples; no requirement to reuse these exact tests.
  Units: none required. Evidence: [evidence-0083](#evidence-0083), [evidence-0084](#evidence-0084)

- **HELPFUL_ONLY — `tests/context/python/function/test_materialization.py`**
  Document: `95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c`; content: `d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7`.
  CRLF/non-ASCII and invalid-range cases corroborate the task test matrix without becoming mandatory repository witnesses.
  Units: none required. Evidence: [evidence-0085](#evidence-0085), [evidence-0086](#evidence-0086)

- **HELPFUL_ONLY — `tests/context/python/function/test_qualified_reference.py`**
  Document: `9c7dfe605bbc376cbb99024b56ae468cdaefab9766bcbe2612175b46106e3c2d`; content: `d8ede2921942e6f4acabc9e4176190781eae10fba4c7e0d894aedbb831b2dafb`.
  Preserved qualified-reference path regression examples; the task requires behavior preservation, not reading every existing test.
  Units: none required. Evidence: [evidence-0087](#evidence-0087), [evidence-0088](#evidence-0088)

- **HELPFUL_ONLY — `tests/context/python/function/test_request_assembly.py`**
  Document: `014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810`; content: `2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b`.
  Copied-request regression example from an older Python path; common source and task semantics support a new equivalent test.
  Units: none required. Evidence: [evidence-0089](#evidence-0089)

- **HELPFUL_ONLY — `tests/context/python/modules/test_selection.py`**
  Document: `87491fef6cbd5c7986a6522574fccb34cddbe0194fe73e4563404c29d8acdf83`; content: `97ec04ba3d29c5c4984678ec389ca11172738134335ad17b160171e7e5192541`.
  Native source-selector fixture and decorated/repeated/foreign cases; a useful test convention rather than necessary evidence.
  Units: none required. Evidence: [evidence-0090](#evidence-0090), [evidence-0091](#evidence-0091), [evidence-0092](#evidence-0092)

- **HELPFUL_ONLY — `tests/models/interaction/test_models.py`**
  Document: `5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a`; content: `03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d`.
  Request-value immutability examples; no unique new-choice test requirement originates here.
  Units: none required. Evidence: [evidence-0093](#evidence-0093), [evidence-0094](#evidence-0094)



### documentation

- **REQUIRED — `docs/architecture.md`**
  Document: `04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391`; content: `fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b`.
  Establishes necessary unit(s) documentation.architecture-baseline. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: documentation.architecture-baseline. Evidence: [evidence-0003](#evidence-0003)

- **HELPFUL_ONLY — `docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md`**
  Document: `3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb`; content: `d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f`.
  Accepted architectural distinction between selection and assembly is useful background; the task and concrete common contracts already establish the necessary bounded change.
  Units: none required. Evidence: [evidence-0006](#evidence-0006)

- **HELPFUL_ONLY — `docs/architecture/taxonomy.md`**
  Document: `e13fc10a26ce00bb5fc7641ea0ac13d59bbf6872873bac1c00021fd86a762f01`; content: `24677a057596cb8157bd77407c35ff82c4cc58c27908ddb72e32f79e266a010e`.
  Taxonomy corroborates immutable plan/disclosure and semantic-strength boundaries; it is not necessary merely because it is broad architectural background.
  Units: none required. Evidence: [evidence-0008](#evidence-0008)

- **HELPFUL_ONLY — `docs/documentation_map.md`**
  Document: `522793a2217a50bdc6e54b0eff3f79a3f67fe15a31ebfbc05002f327971f55ba`; content: `a5b938a9ff8d24c0f569e5ad30a4f513f01ed381ee15a5fd924506f2974c3ed8`.
  The map provides navigation/context; it is not a requested update and does not supply a unique mandatory documentation fact.
  Units: none required. Evidence: [evidence-0011](#evidence-0011)

- **HELPFUL_ONLY — `docs/roadmap.md`**
  Document: `c5a530215f102a343d68092d0f1664b3adc60dc57b27ed49ee6f54d68fc9e5ec`; content: `59aa61e214977c4a25e60c1f69fca8ee7688e71ba7d8ab9361f3de0c84bf8671`.
  Corroborates the implemented representation inventory in a continuity document; no roadmap update is required and the requested package/architecture claims suffice.
  Units: none required. Evidence: [evidence-0012](#evidence-0012)

- **REQUIRED — `src/devtools/context/planning/docs/overview.md`**
  Document: `de0155f1cfe9bdb78fffb3e8897785e5a32f6147ddcd291c3bc7d67f7f9b274a`; content: `a679cfa5ee0591036eaab418fa386a0885ef748f98287b8dd49846c093b068bd`.
  Establishes necessary unit(s) documentation.package-baseline. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: documentation.package-baseline. Evidence: [evidence-0023](#evidence-0023)

- **HELPFUL_ONLY — `src/devtools/context/python/classes/docs/overview.md`**
  Document: `f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd`; content: `83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9`.
  Supplies supported/deferred Python source scope to explain in the requested documents; those semantic units are established independently under source/materialization and the task fixes the required claims.
  Units: none required. Evidence: [evidence-0045](#evidence-0045)

- **HELPFUL_ONLY — `src/devtools/context/python/modules/docs/overview.md`**
  Document: `8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95`; content: `fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08`.
  Useful wording for source versus binding semantics; the package/architecture baseline claims and task requirements determine this documentation obligation.
  Units: none required. Evidence: [evidence-0067](#evidence-0067)



### validation

- **HELPFUL_ONLY — `AGENTS.md`**
  Document: `953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d`; content: `096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a`.
  Corroborates protected selection/confirmation separation, but the documented commands already cover these facts. Repository operating prose is evidence here, not an instruction to access Git.
  Units: none required. Evidence: [evidence-0001](#evidence-0001)

- **REQUIRED — `docs/development/validation.md`**
  Document: `248e605c7cf568ea55bf033a8e56646806da9716a81f586d6f02318fd6311383`; content: `474b6742cbc1675e8edc369e9319560b2827c013aa2311313e8759ee74e00371`.
  Establishes necessary unit(s) validation.protected-profile, validation.quality-commands. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: validation.protected-profile, validation.quality-commands. Evidence: [evidence-0009](#evidence-0009), [evidence-0010](#evidence-0010)

- **REQUIRED — `pyproject.toml`**
  Document: `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0`; content: `e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145`.
  Establishes necessary unit(s) validation.coverage-config, validation.mypy-config, validation.pytest-config, validation.ruff-config. It belongs to at least one complete minimal alternative; alternative union is not simultaneous necessity.
  Units: validation.coverage-config, validation.mypy-config, validation.pytest-config, validation.ruff-config. Evidence: [evidence-0013](#evidence-0013), [evidence-0014](#evidence-0014)

- **HELPFUL_ONLY — `scripts/validate_development.py`**
  Document: `63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a`; content: `425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5`.
  Confirms actual protected selection and failure propagation. The required documented commands already entail the full profile in docs/development/validation.md, making the script redundant in minimal alternatives.
  Units: none required. Evidence: [evidence-0015](#evidence-0015), [evidence-0016](#evidence-0016)

- **HELPFUL_ONLY — `tests/scripts/test_validate_development.py`**
  Document: `aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986`; content: `861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b`.
  Corroborates the protected entry behavior; existing tests are not required evidence for preserving a documented/configured validation profile.
  Units: none required. Evidence: [evidence-0095](#evidence-0095), [evidence-0096](#evidence-0096)



## Every required semantic information unit

### source.selector

Obligation: `case-0012-direct-source-disclosure/source`

**Exact kind/name selection in one retained interpreted module returns all native direct class or sync/async function declarations, including decorated and repeated declarations, without binding resolution.**

Scope: Canonical direct-source selector contract

Necessary because: The task expressly requires reusing this selector and retaining source identities rather than runtime bindings.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `source.selector.support-01` — DIRECT; jointly required resources: src/devtools/context/python/modules/selection.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0070](#evidence-0070), [evidence-0069](#evidence-0069)

- `source.selector.support-02` — DIRECT; jointly required resources: src/devtools/context/python/modules/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0067](#evidence-0067)



### source.function-identity

Obligation: `case-0012-direct-source-disclosure/source`

**A direct function is native knowledge with derivation identity, structural subject bound to snapshot/definition/resource dependency/ordinal, and a source occurrence; its name alone is not identity.**

Scope: Direct module-body function identity and provenance

Necessary because: Caller choices and repeated declarations need the actual native identity and support contract.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `source.function-identity.support-01` — DIRECT; jointly required resources: src/devtools/context/python/function/declarations.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0053](#evidence-0053), [evidence-0054](#evidence-0054), [evidence-0051](#evidence-0051)



### source.class-identity

Obligation: `case-0012-direct-source-disclosure/source`

**A direct module-body class has a native structural subject bound to snapshot, parser/definition, exact observed resource dependency and direct-class ordinal.**

Scope: Native class subject identity

Necessary because: Repeated same-name classes must remain independently selectable native subjects.

Granularity: Split from source.class-method-identity: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `source.class-identity.support-01` — DIRECT; jointly required resources: src/devtools/context/python/classes/declarations.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0040](#evidence-0040), [evidence-0041](#evidence-0041), [evidence-0042](#evidence-0042)

- `source.class-identity.support-02` — DIRECT; jointly required resources: src/devtools/context/python/classes/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0045](#evidence-0045)



### source.method-identity

Obligation: `case-0012-direct-source-disclosure/source`

**A direct sync/async method has native knowledge/support and a subject bound to its containing class subject and per-class ordinal; containing_class is its canonical lexical-parent link.**

Scope: Native direct-method identity and parent

Necessary because: Method support cannot substitute a name or runtime owner for its native lexical parent.

Granularity: Split from source.class-method-identity: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `source.method-identity.support-01` — DIRECT; jointly required resources: src/devtools/context/python/classes/declarations.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0040](#evidence-0040), [evidence-0041](#evidence-0041), [evidence-0042](#evidence-0042)

- `source.method-identity.support-02` — DIRECT; jointly required resources: src/devtools/context/python/classes/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0045](#evidence-0045)



### source.containment

Obligation: `case-0012-direct-source-disclosure/source`

**The native class/method containment builder validates supplied analyses against retained state, then navigates direct methods and their established lexical class parent; unselected declarations fail.**

Scope: Native method containment admission and navigation

Necessary because: The task restricts method support to validated native class-parent containment.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `source.containment.support-01` — DIRECT; jointly required resources: src/devtools/context/python/classes/containment.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0038](#evidence-0038), [evidence-0037](#evidence-0037)

- `source.containment.support-02` — DIRECT; jointly required resources: src/devtools/context/python/classes/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0048](#evidence-0048)



### source.excluded-resolution

Obligation: `case-0012-direct-source-disclosure/source`

**Source disclosure must not resolve runtime attributes, imported facades, inherited methods, or semantic targets.**

Scope: Explicit negative feature scope

Necessary because: The task makes these boundaries mandatory.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `source.excluded-resolution.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0103](#evidence-0103)



### choices.plan-value

Obligation: `case-0012-direct-source-disclosure/choices`

**The plan is an immutable value retaining purpose, repository/snapshot identities, ordered disclosures and optional preceding-plan lineage.**

Scope: Plan value shape and immutability

Necessary because: New concrete choices must participate in this existing immutable value.

Granularity: Split from choices.plan: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `choices.plan-value.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0028](#evidence-0028), [evidence-0029](#evidence-0029)



### choices.plan-admission

Obligation: `case-0012-direct-source-disclosure/choices`

**Plan construction rejects blank purpose, empty choices, mixed purpose/repository/snapshot applicability and repeated identical choice identities.**

Scope: Plan admission invariant

Necessary because: Integration must preserve actual admissibility rather than silently weaken validation.

Granularity: Split from choices.plan: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `choices.plan-admission.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0028](#evidence-0028), [evidence-0029](#evidence-0029)



### choices.plan-identity

Obligation: `case-0012-direct-source-disclosure/choices`

**Plan identity is a deterministic length-framed digest of purpose, frame, optional lineage and ordered representation/choice identities.**

Scope: Plan deterministic identity and order

Necessary because: Choice/order changes must retain their effect on the existing identity contract.

Granularity: Split from choices.plan: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `choices.plan-identity.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0028](#evidence-0028), [evidence-0029](#evidence-0029), [evidence-0030](#evidence-0030)



### choices.admission

Obligation: `case-0012-direct-source-disclosure/choices`

**Each admitted concrete choice provides purpose, frame, representation, deterministic identity and materialize(snapshot) returning a common item through PlannedDisclosure.**

Scope: Common concrete-choice participation protocol

Necessary because: The new option needs the existing semantic admission seam.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `choices.admission.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0027](#evidence-0027)



### choices.whole-compatibility

Obligation: `case-0012-direct-source-disclosure/choices`

**WholeResourceDisclosureOption is an explicit coarse retained-resource choice with resource/frame identity, validated snapshot materialization, and common item provenance; it remains distinct from declaration disclosure.**

Scope: Existing whole-resource choice boundary

Necessary because: Compatibility must preserve the coarse choice without turning it into an implicit fallback.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `choices.whole-compatibility.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/resource.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0035](#evidence-0035), [evidence-0036](#evidence-0036)



### choices.reference-compatibility

Obligation: `case-0012-direct-source-disclosure/choices`

**The existing qualified-reference option adapts its purpose/frame/identity and delegates to its validated Python materializer/renderer before returning a common item with both owner addresses/content identities and native provenance.**

Scope: Existing qualified-reference common-plan adapter

Necessary because: Compatibility includes this native delegation boundary rather than replacing it with new source-choice resolution.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `choices.reference-compatibility.support-01` — DIRECT; jointly required resources: src/devtools/context/python/function/planned_reference.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0060](#evidence-0060), [evidence-0061](#evidence-0061)



### choices.caller-selection

Obligation: `case-0012-direct-source-disclosure/choices`

**Choice integration remains caller-selected and performs no automatic retrieval or selection.**

Scope: Explicit feature admission policy

Necessary because: The feature explicitly forbids automatic choice.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `choices.caller-selection.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0100](#evidence-0100)



### integrity.lookup

Obligation: `case-0012-direct-source-disclosure/integrity`

**resource_at(address) returns the retained occurrence at that exact address and raises ValueError for an absent address, without file acquisition.**

Scope: Retained snapshot lookup contract

Necessary because: The task expressly binds every resource validation to this method.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `integrity.lookup.support-01` — DIRECT; jointly required resources: src/devtools/context/repository/snapshot.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0073](#evidence-0073)



### integrity.selection-frame

Obligation: `case-0012-direct-source-disclosure/integrity`

**Canonical direct-source selection checks module repository, snapshot and exact resource equality against resource_at before deriving declarations from retained content.**

Scope: Module/frame/content validation before source selection

Necessary because: Foreign/stale module inputs must not become disclosure support.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `integrity.selection-frame.support-01` — DIRECT; jointly required resources: src/devtools/context/python/modules/selection.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0070](#evidence-0070)

- `integrity.selection-frame.support-02` — DIRECT; jointly required resources: src/devtools/context/python/modules/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0066](#evidence-0066)



### integrity.method-frame

Obligation: `case-0012-direct-source-disclosure/integrity`

**Validated class/method containment checks exact retained resource equality, coverage, derivation, subject ordinals, support frame/address and method parent consistency.**

Scope: Native class-parent validation details

Necessary because: The task requires validating supplied method and parent support, not accepting nominal names.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `integrity.method-frame.support-01` — DIRECT; jointly required resources: src/devtools/context/python/classes/containment.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0038](#evidence-0038)



### integrity.canonical-membership

Obligation: `case-0012-direct-source-disclosure/integrity`

**Supplied declaration identity/scope must agree with canonical native declarations reproduced from retained content; structurally stamped containment alone does not prove source-range/name authenticity.**

Scope: Native declaration authenticity at admission

Necessary because: The task requires rejecting unsupported scope and mismatched native declaration identity.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `integrity.canonical-membership.support-01` — INFERABLE; jointly required resources: src/devtools/context/python/classes/containment.py, src/devtools/context/python/modules/selection.py.
  The selector reproduces canonical facts from retained content. The containment validator checks provenance fields but does not reparse or compare every range/name; full canonical membership/equality is the necessary admission check inferred from the task and these mechanisms. No existing source-choice implementation is claimed.
  Exact evidence: [evidence-0070](#evidence-0070), [evidence-0038](#evidence-0038)



### integrity.plan-frame

Obligation: `case-0012-direct-source-disclosure/integrity`

**Common materialization rejects a supplied snapshot with repository/snapshot identity different from its plan before realizing choices.**

Scope: Plan frame admission before materialization

Necessary because: A valid native declaration does not make a foreign or stale overall plan applicable.

Granularity: Split from integrity.publication: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `integrity.plan-frame.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0026](#evidence-0026), [evidence-0025](#evidence-0025)

- `integrity.plan-frame.support-02` — DIRECT; jointly required resources: tests/context/planning/test_plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0079](#evidence-0079), [evidence-0080](#evidence-0080), [evidence-0078](#evidence-0078)



### integrity.returned-identity

Obligation: `case-0012-direct-source-disclosure/integrity`

**Common materialization and ContextDisclosure alignment require every returned item option identity/representation to equal its planned choice.**

Scope: Returned item identity/representation integrity

Necessary because: The task explicitly requires rejecting mismatched returned identity before publication.

Granularity: Split from integrity.publication: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `integrity.returned-identity.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0026](#evidence-0026), [evidence-0025](#evidence-0025)

- `integrity.returned-identity.support-02` — DIRECT; jointly required resources: tests/context/planning/test_plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0079](#evidence-0079), [evidence-0080](#evidence-0080), [evidence-0078](#evidence-0078)



### integrity.publication

Obligation: `case-0012-direct-source-disclosure/integrity`

**A failed or incomplete materialization must not return a successfully published ContextDisclosure; every aligned ordered item must be realized first.**

Scope: Complete disclosure publication boundary

Necessary because: Publication must follow all required validation and successful realization, rather than exposing a partial disclosure.

Granularity: Split from integrity.publication: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `integrity.publication.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0026](#evidence-0026), [evidence-0025](#evidence-0025)

- `integrity.publication.support-02` — DIRECT; jointly required resources: tests/context/planning/test_plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0079](#evidence-0079), [evidence-0080](#evidence-0080), [evidence-0078](#evidence-0078)



### materialization.coordinates

Obligation: `case-0012-direct-source-disclosure/materialization`

**Native source ranges use one-based lines, zero-based UTF-8 byte columns and exclusive ends.**

Scope: Python occurrence coordinate semantics

Necessary because: Exact source extraction cannot interpret UTF-8 columns as character offsets.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.coordinates.support-01` — DIRECT; jointly required resources: src/devtools/context/python/function/declarations.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0050](#evidence-0050)

- `materialization.coordinates.support-02` — DIRECT; jointly required resources: src/devtools/context/python/classes/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0046](#evidence-0046)



### materialization.extraction

Obligation: `case-0012-direct-source-disclosure/materialization`

**The existing source extractor computes retained UTF-8 absolute offsets with line endings intact, rejects reversed/out-of-bounds ranges and invalid UTF-8 boundaries, and decodes only the exact selected byte segment.**

Scope: Exact source segment algorithm and failure boundaries

Necessary because: CRLF/non-ASCII fidelity and invalid-range rejection require the actual byte-boundary semantics.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.extraction.support-01` — DIRECT; jointly required resources: src/devtools/context/python/function/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0058](#evidence-0058), [evidence-0059](#evidence-0059)



### materialization.decorator-boundary

Obligation: `case-0012-direct-source-disclosure/materialization`

**Existing native declaration ranges begin at class/def/async def and exclude preceding decorators; decorator-preserving disclosure therefore needs an explicit faithful extension or additional source-range provenance.**

Scope: Native range versus decorator-inclusive requested representation

Necessary because: The task requires decorators, and a literal existing-range slice would omit them.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.decorator-boundary.support-01` — INFERABLE; jointly required resources: src/devtools/context/python/classes/docs/overview.md.
  The native range starts at the declaration AST node. Its stated exclusion and task decorator requirement imply additional explicitly accounted representation work; no undocumented decorator-inclusive native range is assumed.
  Exact evidence: [evidence-0047](#evidence-0047)

- `materialization.decorator-boundary.support-02` — INFERABLE; jointly required resources: src/devtools/context/python/classes/declarations.py, src/devtools/context/python/function/declarations.py.
  The native range starts at the declaration AST node. Its stated exclusion and task decorator requirement imply additional explicitly accounted representation work; no undocumented decorator-inclusive native range is assumed.
  Exact evidence: [evidence-0055](#evidence-0055), [evidence-0044](#evidence-0044), [evidence-0043](#evidence-0043)



### materialization.item-provenance

Obligation: `case-0012-direct-source-disclosure/materialization`

**A common materialized item carries option identity, representation, owner addresses/content identities, text and native provenance, while ContextDisclosure retains the plan and aligned items.**

Scope: Realized declaration representation and supporting provenance carrier

Necessary because: The task places native derivation/range/owner support inside ContextDisclosure through the existing item carrier.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.item-provenance.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0024](#evidence-0024), [evidence-0025](#evidence-0025)



### materialization.mixed-order

Obligation: `case-0012-direct-source-disclosure/materialization`

**Common materialization appends exactly one item per planned choice in caller order, without implicit owner expansion or re-selection.**

Scope: Mixed-plan exact realization order

Necessary because: New declarations must coexist faithfully with old representations.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.mixed-order.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/materialization.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0026](#evidence-0026)

- `materialization.mixed-order.support-02` — DIRECT; jointly required resources: tests/context/planning/test_plan.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0076](#evidence-0076)



### materialization.bounded-meaning

Obligation: `case-0012-direct-source-disclosure/materialization`

**Exact source realization must not infer sufficiency or implicitly expand to the whole owner resource.**

Scope: Source-choice representation fidelity

Necessary because: These are mandatory feature boundaries rather than additional implementation facts.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `materialization.bounded-meaning.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0118](#evidence-0118)



### assembly.rendering

Obligation: `case-0012-direct-source-disclosure/assembly`

**The common renderer consumes realized items in plan order, adds common metadata and item text, and retains the exact ContextDisclosure.**

Scope: Current common rendering behavior

Necessary because: The new choice must preserve common presentation compatibility.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `assembly.rendering.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/rendering.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0033](#evidence-0033), [evidence-0032](#evidence-0032)



### assembly.request-copy

Obligation: `case-0012-direct-source-disclosure/assembly`

**The common assembler places unchanged task text before rendered Context and uses dataclass replacement to create a new prompt with the original role, retaining every other request field including tools.**

Scope: Pure copied-request assembly

Necessary because: The task explicitly requires original request, role, settings, conversation, provider settings and tools preservation.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `assembly.request-copy.support-01` — INFERABLE; jointly required resources: src/devtools/context/planning/rendering.py.
  The code explicitly reuses the original prompt role and calls replace(task_request, prompt=...). The task supplies the required field inventory; replacing only prompt retains other fields, including tools. The original immutable request is not mutated.
  Exact evidence: [evidence-0034](#evidence-0034)



### assembly.no-budget

Obligation: `case-0012-direct-source-disclosure/assembly`

**The feature introduces no new budget or truncation policy.**

Scope: Assembly policy boundary

Necessary because: This is a mandatory preservation constraint.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `assembly.no-budget.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0127](#evidence-0127)



### exports.planning-surface

Obligation: `case-0012-direct-source-disclosure/exports`

**The common planning initializer explicitly imports its public choices and realization APIs and lists them in __all__; this is the new choice exposure seam.**

Scope: Common planning public API surface

Necessary because: Actual current export structure is needed to extend both public boundaries compatibly.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `exports.planning-surface.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/__init__.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0021](#evidence-0021)



### exports.outer-surface

Obligation: `case-0012-direct-source-disclosure/exports`

**The outer Context facade re-exports common planning values/functions and qualified-reference choices through explicit imports and __all__.**

Scope: Outer Context public API surface

Necessary because: The task requires adding exposure at this second distinct boundary.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `exports.outer-surface.support-01` — DIRECT; jointly required resources: src/devtools/context/__init__.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0017](#evidence-0017), [evidence-0018](#evidence-0018)



### exports.option-ownership

Obligation: `case-0012-direct-source-disclosure/exports`

**Language-specific choices participate through the common PlannedDisclosure protocol; its contract does not require common planning to parse Python or depend on Retrieval.**

Scope: Dependency ownership through concrete-choice protocol

Necessary because: Permitted direction requires the existing structural participation seam.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `exports.option-ownership.support-01` — INFERABLE; jointly required resources: src/devtools/context/planning/plan.py.
  The protocol accepts frame/representation values and a materialize method rather than Python declarations or retrieval values. The explicit task dependency prohibition therefore fits a Python-owned concrete adapter, with public exposure through the common API.
  Exact evidence: [evidence-0027](#evidence-0027)



### exports.assembly-ownership

Obligation: `case-0012-direct-source-disclosure/exports`

**Common rendering/request assembly depends on realized common disclosure and ModelRequest/Prompt, with no Retrieval calls or Python-specific parsing/resolution.**

Scope: Common assembly dependency boundary

Necessary because: The task forbids moving language-specific logic into common assembly.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `exports.assembly-ownership.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/rendering.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0031](#evidence-0031)



### tests.function-choice

Obligation: `case-0012-direct-source-disclosure/tests`

**Focused tests must exercise direct native function source disclosure choices.**

Scope: Direct function choice test coverage

Necessary because: Function support is a separately required positive feature behavior.

Granularity: Split from tests.direct-choices: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.function-choice.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0132](#evidence-0132)



### tests.class-choice

Obligation: `case-0012-direct-source-disclosure/tests`

**Focused tests must exercise direct native class source disclosure choices.**

Scope: Direct class choice test coverage

Necessary because: Class support can fail independently of function support.

Granularity: Split from tests.direct-choices: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.class-choice.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0132](#evidence-0132)



### tests.method-choice

Obligation: `case-0012-direct-source-disclosure/tests`

**Focused tests must exercise direct native method source choices admitted through validated native class-parent containment.**

Scope: Direct method choice test coverage

Necessary because: Method admission has a distinct mandatory parent/containment boundary.

Granularity: Split from tests.direct-choices: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.method-choice.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0132](#evidence-0132)



### tests.decorated

Obligation: `case-0012-direct-source-disclosure/tests`

**Tests must exercise decorated native declarations without runtime-binding substitution.**

Scope: Decorated direct-source test coverage

Necessary because: Decorator support is expressly required and can fail independently of repeated-name handling.

Granularity: Split from tests.decorated-repeated: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.decorated.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0133](#evidence-0133)



### tests.repeated

Obligation: `case-0012-direct-source-disclosure/tests`

**Tests must exercise repeated native declarations as distinct source identities.**

Scope: Repeated declaration test coverage

Necessary because: Repeated source identities are expressly required and can fail independently of decorators.

Granularity: Split from tests.decorated-repeated: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.repeated.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0133](#evidence-0133)



### tests.mixed-order

Obligation: `case-0012-direct-source-disclosure/tests`

**Tests must exercise caller ordering in mixed declaration/reference/whole-resource plans.**

Scope: Mixed-plan order test coverage

Necessary because: Ordering can fail independently of exact source/provenance preservation.

Granularity: Split from tests.mixed-fidelity: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.mixed-order.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0134](#evidence-0134)



### tests.exact-fidelity

Obligation: `case-0012-direct-source-disclosure/tests`

**Tests must exercise exact selected source and native provenance, including mandatory UTF-8, CRLF and decorator fidelity.**

Scope: Exact source/provenance test coverage

Necessary because: The requested source representation must be verified with its native support, not only its position.

Granularity: Split from tests.mixed-fidelity: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `tests.exact-fidelity.support-01` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0134](#evidence-0134), [evidence-0114](#evidence-0114)



### tests.rejection

Obligation: `case-0012-direct-source-disclosure/tests`

**Tests must exercise stale, foreign and missing-resource rejection.**

Scope: Mandatory test coverage category

Necessary because: This category is expressly required by the feature task; existing test examples are replaceable.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `tests.rejection.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0135](#evidence-0135)



### tests.existing-choices

Obligation: `case-0012-direct-source-disclosure/tests`

**Regression tests must preserve existing qualified-reference and whole-resource choices.**

Scope: Mandatory test coverage category

Necessary because: This category is expressly required by the feature task; existing test examples are replaceable.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `tests.existing-choices.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0136](#evidence-0136)



### tests.request-preservation

Obligation: `case-0012-direct-source-disclosure/tests`

**Regression tests must preserve copied requests and the original request, role and all non-prompt fields.**

Scope: Mandatory test coverage category

Necessary because: This category is expressly required by the feature task; existing test examples are replaceable.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `tests.request-preservation.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0137](#evidence-0137), [evidence-0121](#evidence-0121)



### documentation.package-baseline

Obligation: `case-0012-direct-source-disclosure/documentation`

**The package overview currently describes only qualified-reference and whole-resource choices and says the common protocol permits its two current consumers, while preserving caller direction and native provenance.**

Scope: Package documentation claims that must evolve with the feature

Necessary because: Updating the package accurately requires identifying these concrete implemented-scope claims, not merely its filename.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `documentation.package-baseline.support-01` — DIRECT; jointly required resources: src/devtools/context/planning/docs/overview.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0023](#evidence-0023)



### documentation.architecture-baseline

Obligation: `case-0012-direct-source-disclosure/documentation`

**The architecture separates native referents from capacity-consuming representations and Localization resolution from Context admission, while identifying the implemented plan as narrower than general planning with only reference and whole-resource forms.**

Scope: Cross-package architectural status claims to preserve/update

Necessary because: The architecture update must preserve ownership/status distinctions and accurately extend its current representation inventory.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `documentation.architecture-baseline.support-01` — DIRECT; jointly required resources: docs/architecture.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0003](#evidence-0003)



### documentation.scope-claims

Obligation: `case-0012-direct-source-disclosure/documentation`

**Documentation must distinguish source identities from runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.**

Scope: Mandatory content of both requested documentation updates

Necessary because: The feature task fixes these claims and exclusions.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `documentation.scope-claims.support-task` — DIRECT; jointly required resources: (none; task evidence).
  The mandatory feature task itself fixes this behavior; no pre-existing implementation example is necessary.
  Exact evidence: [evidence-0140](#evidence-0140)



### validation.protected-profile

Obligation: `case-0012-direct-source-disclosure/validation`

**The documented protected development entry runs tests/ while excluding tests/experiments/ before collection, preserves pytest configuration and returns pytest failure status; confirmation is outside ordinary development validation.**

Scope: Protected test selection and invocation boundary

Necessary because: The task requires this documented protected profile, not outcome-dependent selection.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `validation.protected-profile.support-01` — DIRECT; jointly required resources: docs/development/validation.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0009](#evidence-0009)

- `validation.protected-profile.support-02` — DIRECT; jointly required resources: AGENTS.md, scripts/validate_development.py.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0015](#evidence-0015), [evidence-0016](#evidence-0016), [evidence-0001](#evidence-0001)



### validation.pytest-config

Obligation: `case-0012-direct-source-disclosure/validation`

**Actual pytest settings select tests with strict configuration and strict marker checks, retaining the live_codex opt-in marker declaration.**

Scope: Actual test-selection/admission configuration

Necessary because: The task requires preserving the concrete test settings in pyproject.toml.

Granularity: Split from validation.pytest-coverage: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `validation.pytest-config.support-01` — DIRECT; jointly required resources: pyproject.toml.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0013](#evidence-0013)



### validation.coverage-config

Obligation: `case-0012-direct-source-disclosure/validation`

**Actual pytest/coverage settings retain devtools branch coverage, term-missing reporting, a 100% fail threshold, configured source, show_missing=true and skip_covered=false.**

Scope: Actual production coverage configuration

Necessary because: The task requires retaining coverage settings independently of test selection and strict marker admission.

Granularity: Split from validation.pytest-coverage: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `validation.coverage-config.support-01` — DIRECT; jointly required resources: pyproject.toml.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0013](#evidence-0013)



### validation.ruff-config

Obligation: `case-0012-direct-source-disclosure/validation`

**Actual Ruff settings select py312, 88 columns, ALL lint with D203/D213 ignored and S101 ignored for tests.**

Scope: Preserved lint/format configuration

Necessary because: The requested static checks must retain actual configured lint/format semantics.

Granularity: Split from validation.static-config: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `validation.ruff-config.support-01` — DIRECT; jointly required resources: pyproject.toml.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0014](#evidence-0014)



### validation.mypy-config

Obligation: `case-0012-direct-source-disclosure/validation`

**Actual mypy configuration is strict Python 3.12 over src/tests/experiments with explicit package bases and src path.**

Scope: Preserved strict type-checking configuration

Necessary because: Strict mypy has a separate scope/configuration from Ruff and protected pytest.

Granularity: Split from validation.static-config: this fact can fail independently of the other original facts; supporting text overlap does not merge the facts.

- `validation.mypy-config.support-01` — DIRECT; jointly required resources: pyproject.toml.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0014](#evidence-0014)



### validation.quality-commands

Obligation: `case-0012-direct-source-disclosure/validation`

**The documented separate gates are uv run ruff check ., uv run ruff format --check, uv run mypy, git diff --check, and git diff --cached --check for the staged/index view.**

Scope: Documented complete static and whitespace command contract

Necessary because: The task explicitly requires the documented profile and both whitespace views.

Granularity: One independently necessary contract fact; inseparable fields describe one identity, boundary, or invariant. Other independent contracts are separate units.

- `validation.quality-commands.support-01` — DIRECT; jointly required resources: docs/development/validation.md.
  The cited retained text states or implements this fact directly.
  Exact evidence: [evidence-0010](#evidence-0010)



## Acceptable ALL-of alternatives

ANY complete alternative may substitute for another for its obligation. Each proof variant covers ALL required units with ALL listed resource members. Proof variants are substitutable, not cumulative.

### source.alternative-01

```json
{
  "identity": "source.alternative-01",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/source",
  "proof_variants": [
    [
      {
        "support": "source.selector.support-02",
        "unit": "source.selector"
      },
      {
        "support": "source.function-identity.support-01",
        "unit": "source.function-identity"
      },
      {
        "support": "source.class-identity.support-01",
        "unit": "source.class-identity"
      },
      {
        "support": "source.method-identity.support-01",
        "unit": "source.method-identity"
      },
      {
        "support": "source.containment.support-01",
        "unit": "source.containment"
      },
      {
        "support": "source.excluded-resolution.support-task",
        "unit": "source.excluded-resolution"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/python/classes/containment.py",
    "src/devtools/context/python/classes/declarations.py",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/modules/docs/overview.md"
  ],
  "required_units": [
    "source.selector",
    "source.function-identity",
    "source.class-identity",
    "source.method-identity",
    "source.containment",
    "source.excluded-resolution"
  ]
}
```

### source.alternative-02

```json
{
  "identity": "source.alternative-02",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/source",
  "proof_variants": [
    [
      {
        "support": "source.selector.support-01",
        "unit": "source.selector"
      },
      {
        "support": "source.function-identity.support-01",
        "unit": "source.function-identity"
      },
      {
        "support": "source.class-identity.support-01",
        "unit": "source.class-identity"
      },
      {
        "support": "source.method-identity.support-01",
        "unit": "source.method-identity"
      },
      {
        "support": "source.containment.support-01",
        "unit": "source.containment"
      },
      {
        "support": "source.excluded-resolution.support-task",
        "unit": "source.excluded-resolution"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/python/classes/containment.py",
    "src/devtools/context/python/classes/declarations.py",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/modules/selection.py"
  ],
  "required_units": [
    "source.selector",
    "source.function-identity",
    "source.class-identity",
    "source.method-identity",
    "source.containment",
    "source.excluded-resolution"
  ]
}
```

### source.alternative-03

```json
{
  "identity": "source.alternative-03",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/source",
  "proof_variants": [
    [
      {
        "support": "source.selector.support-02",
        "unit": "source.selector"
      },
      {
        "support": "source.function-identity.support-01",
        "unit": "source.function-identity"
      },
      {
        "support": "source.class-identity.support-02",
        "unit": "source.class-identity"
      },
      {
        "support": "source.method-identity.support-02",
        "unit": "source.method-identity"
      },
      {
        "support": "source.containment.support-02",
        "unit": "source.containment"
      },
      {
        "support": "source.excluded-resolution.support-task",
        "unit": "source.excluded-resolution"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/python/classes/docs/overview.md",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/modules/docs/overview.md"
  ],
  "required_units": [
    "source.selector",
    "source.function-identity",
    "source.class-identity",
    "source.method-identity",
    "source.containment",
    "source.excluded-resolution"
  ]
}
```

### source.alternative-04

```json
{
  "identity": "source.alternative-04",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/source",
  "proof_variants": [
    [
      {
        "support": "source.selector.support-01",
        "unit": "source.selector"
      },
      {
        "support": "source.function-identity.support-01",
        "unit": "source.function-identity"
      },
      {
        "support": "source.class-identity.support-02",
        "unit": "source.class-identity"
      },
      {
        "support": "source.method-identity.support-02",
        "unit": "source.method-identity"
      },
      {
        "support": "source.containment.support-02",
        "unit": "source.containment"
      },
      {
        "support": "source.excluded-resolution.support-task",
        "unit": "source.excluded-resolution"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/python/classes/docs/overview.md",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/modules/selection.py"
  ],
  "required_units": [
    "source.selector",
    "source.function-identity",
    "source.class-identity",
    "source.method-identity",
    "source.containment",
    "source.excluded-resolution"
  ]
}
```

### choices.alternative-01

```json
{
  "identity": "choices.alternative-01",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/choices",
  "proof_variants": [
    [
      {
        "support": "choices.plan-value.support-01",
        "unit": "choices.plan-value"
      },
      {
        "support": "choices.plan-admission.support-01",
        "unit": "choices.plan-admission"
      },
      {
        "support": "choices.plan-identity.support-01",
        "unit": "choices.plan-identity"
      },
      {
        "support": "choices.admission.support-01",
        "unit": "choices.admission"
      },
      {
        "support": "choices.whole-compatibility.support-01",
        "unit": "choices.whole-compatibility"
      },
      {
        "support": "choices.reference-compatibility.support-01",
        "unit": "choices.reference-compatibility"
      },
      {
        "support": "choices.caller-selection.support-task",
        "unit": "choices.caller-selection"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/planning/plan.py",
    "src/devtools/context/planning/resource.py",
    "src/devtools/context/python/function/planned_reference.py"
  ],
  "required_units": [
    "choices.plan-value",
    "choices.plan-admission",
    "choices.plan-identity",
    "choices.admission",
    "choices.whole-compatibility",
    "choices.reference-compatibility",
    "choices.caller-selection"
  ]
}
```

### integrity.alternative-01

```json
{
  "identity": "integrity.alternative-01",
  "inferability_assumptions": [
    "The selector reproduces canonical facts from retained content. The containment validator checks provenance fields but does not reparse or compare every range/name; full canonical membership/equality is the necessary admission check inferred from the task and these mechanisms. No existing source-choice implementation is claimed."
  ],
  "obligation": "case-0012-direct-source-disclosure/integrity",
  "proof_variants": [
    [
      {
        "support": "integrity.lookup.support-01",
        "unit": "integrity.lookup"
      },
      {
        "support": "integrity.selection-frame.support-01",
        "unit": "integrity.selection-frame"
      },
      {
        "support": "integrity.method-frame.support-01",
        "unit": "integrity.method-frame"
      },
      {
        "support": "integrity.canonical-membership.support-01",
        "unit": "integrity.canonical-membership"
      },
      {
        "support": "integrity.plan-frame.support-01",
        "unit": "integrity.plan-frame"
      },
      {
        "support": "integrity.returned-identity.support-01",
        "unit": "integrity.returned-identity"
      },
      {
        "support": "integrity.publication.support-01",
        "unit": "integrity.publication"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/planning/materialization.py",
    "src/devtools/context/python/classes/containment.py",
    "src/devtools/context/python/modules/selection.py",
    "src/devtools/context/repository/snapshot.py"
  ],
  "required_units": [
    "integrity.lookup",
    "integrity.selection-frame",
    "integrity.method-frame",
    "integrity.canonical-membership",
    "integrity.plan-frame",
    "integrity.returned-identity",
    "integrity.publication"
  ]
}
```

### integrity.alternative-02

```json
{
  "identity": "integrity.alternative-02",
  "inferability_assumptions": [
    "The selector reproduces canonical facts from retained content. The containment validator checks provenance fields but does not reparse or compare every range/name; full canonical membership/equality is the necessary admission check inferred from the task and these mechanisms. No existing source-choice implementation is claimed."
  ],
  "obligation": "case-0012-direct-source-disclosure/integrity",
  "proof_variants": [
    [
      {
        "support": "integrity.lookup.support-01",
        "unit": "integrity.lookup"
      },
      {
        "support": "integrity.selection-frame.support-01",
        "unit": "integrity.selection-frame"
      },
      {
        "support": "integrity.method-frame.support-01",
        "unit": "integrity.method-frame"
      },
      {
        "support": "integrity.canonical-membership.support-01",
        "unit": "integrity.canonical-membership"
      },
      {
        "support": "integrity.plan-frame.support-02",
        "unit": "integrity.plan-frame"
      },
      {
        "support": "integrity.returned-identity.support-02",
        "unit": "integrity.returned-identity"
      },
      {
        "support": "integrity.publication.support-02",
        "unit": "integrity.publication"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/python/classes/containment.py",
    "src/devtools/context/python/modules/selection.py",
    "src/devtools/context/repository/snapshot.py",
    "tests/context/planning/test_plan.py"
  ],
  "required_units": [
    "integrity.lookup",
    "integrity.selection-frame",
    "integrity.method-frame",
    "integrity.canonical-membership",
    "integrity.plan-frame",
    "integrity.returned-identity",
    "integrity.publication"
  ]
}
```

### materialization.alternative-01

```json
{
  "identity": "materialization.alternative-01",
  "inferability_assumptions": [
    "The native range starts at the declaration AST node. Its stated exclusion and task decorator requirement imply additional explicitly accounted representation work; no undocumented decorator-inclusive native range is assumed."
  ],
  "obligation": "case-0012-direct-source-disclosure/materialization",
  "proof_variants": [
    [
      {
        "support": "materialization.coordinates.support-01",
        "unit": "materialization.coordinates"
      },
      {
        "support": "materialization.extraction.support-01",
        "unit": "materialization.extraction"
      },
      {
        "support": "materialization.decorator-boundary.support-02",
        "unit": "materialization.decorator-boundary"
      },
      {
        "support": "materialization.item-provenance.support-01",
        "unit": "materialization.item-provenance"
      },
      {
        "support": "materialization.mixed-order.support-01",
        "unit": "materialization.mixed-order"
      },
      {
        "support": "materialization.bounded-meaning.support-task",
        "unit": "materialization.bounded-meaning"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/planning/materialization.py",
    "src/devtools/context/python/classes/declarations.py",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/function/materialization.py"
  ],
  "required_units": [
    "materialization.coordinates",
    "materialization.extraction",
    "materialization.decorator-boundary",
    "materialization.item-provenance",
    "materialization.mixed-order",
    "materialization.bounded-meaning"
  ]
}
```

### materialization.alternative-02

```json
{
  "identity": "materialization.alternative-02",
  "inferability_assumptions": [
    "The native range starts at the declaration AST node. Its stated exclusion and task decorator requirement imply additional explicitly accounted representation work; no undocumented decorator-inclusive native range is assumed."
  ],
  "obligation": "case-0012-direct-source-disclosure/materialization",
  "proof_variants": [
    [
      {
        "support": "materialization.coordinates.support-02",
        "unit": "materialization.coordinates"
      },
      {
        "support": "materialization.extraction.support-01",
        "unit": "materialization.extraction"
      },
      {
        "support": "materialization.decorator-boundary.support-01",
        "unit": "materialization.decorator-boundary"
      },
      {
        "support": "materialization.item-provenance.support-01",
        "unit": "materialization.item-provenance"
      },
      {
        "support": "materialization.mixed-order.support-01",
        "unit": "materialization.mixed-order"
      },
      {
        "support": "materialization.bounded-meaning.support-task",
        "unit": "materialization.bounded-meaning"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/planning/materialization.py",
    "src/devtools/context/python/classes/docs/overview.md",
    "src/devtools/context/python/function/materialization.py"
  ],
  "required_units": [
    "materialization.coordinates",
    "materialization.extraction",
    "materialization.decorator-boundary",
    "materialization.item-provenance",
    "materialization.mixed-order",
    "materialization.bounded-meaning"
  ]
}
```

### assembly.alternative-01

```json
{
  "identity": "assembly.alternative-01",
  "inferability_assumptions": [
    "The code explicitly reuses the original prompt role and calls replace(task_request, prompt=...). The task supplies the required field inventory; replacing only prompt retains other fields, including tools. The original immutable request is not mutated."
  ],
  "obligation": "case-0012-direct-source-disclosure/assembly",
  "proof_variants": [
    [
      {
        "support": "assembly.rendering.support-01",
        "unit": "assembly.rendering"
      },
      {
        "support": "assembly.request-copy.support-01",
        "unit": "assembly.request-copy"
      },
      {
        "support": "assembly.no-budget.support-task",
        "unit": "assembly.no-budget"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/planning/rendering.py"
  ],
  "required_units": [
    "assembly.rendering",
    "assembly.request-copy",
    "assembly.no-budget"
  ]
}
```

### exports.alternative-01

```json
{
  "identity": "exports.alternative-01",
  "inferability_assumptions": [
    "The protocol accepts frame/representation values and a materialize method rather than Python declarations or retrieval values. The explicit task dependency prohibition therefore fits a Python-owned concrete adapter, with public exposure through the common API."
  ],
  "obligation": "case-0012-direct-source-disclosure/exports",
  "proof_variants": [
    [
      {
        "support": "exports.planning-surface.support-01",
        "unit": "exports.planning-surface"
      },
      {
        "support": "exports.outer-surface.support-01",
        "unit": "exports.outer-surface"
      },
      {
        "support": "exports.option-ownership.support-01",
        "unit": "exports.option-ownership"
      },
      {
        "support": "exports.assembly-ownership.support-01",
        "unit": "exports.assembly-ownership"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "src/devtools/context/__init__.py",
    "src/devtools/context/planning/__init__.py",
    "src/devtools/context/planning/plan.py",
    "src/devtools/context/planning/rendering.py"
  ],
  "required_units": [
    "exports.planning-surface",
    "exports.outer-surface",
    "exports.option-ownership",
    "exports.assembly-ownership"
  ]
}
```

### tests.alternative-01

```json
{
  "identity": "tests.alternative-01",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/tests",
  "proof_variants": [
    [
      {
        "support": "tests.function-choice.support-01",
        "unit": "tests.function-choice"
      },
      {
        "support": "tests.class-choice.support-01",
        "unit": "tests.class-choice"
      },
      {
        "support": "tests.method-choice.support-01",
        "unit": "tests.method-choice"
      },
      {
        "support": "tests.decorated.support-01",
        "unit": "tests.decorated"
      },
      {
        "support": "tests.repeated.support-01",
        "unit": "tests.repeated"
      },
      {
        "support": "tests.mixed-order.support-01",
        "unit": "tests.mixed-order"
      },
      {
        "support": "tests.exact-fidelity.support-01",
        "unit": "tests.exact-fidelity"
      },
      {
        "support": "tests.rejection.support-task",
        "unit": "tests.rejection"
      },
      {
        "support": "tests.existing-choices.support-task",
        "unit": "tests.existing-choices"
      },
      {
        "support": "tests.request-preservation.support-task",
        "unit": "tests.request-preservation"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [],
  "required_units": [
    "tests.function-choice",
    "tests.class-choice",
    "tests.method-choice",
    "tests.decorated",
    "tests.repeated",
    "tests.mixed-order",
    "tests.exact-fidelity",
    "tests.rejection",
    "tests.existing-choices",
    "tests.request-preservation"
  ]
}
```

### documentation.alternative-01

```json
{
  "identity": "documentation.alternative-01",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/documentation",
  "proof_variants": [
    [
      {
        "support": "documentation.package-baseline.support-01",
        "unit": "documentation.package-baseline"
      },
      {
        "support": "documentation.architecture-baseline.support-01",
        "unit": "documentation.architecture-baseline"
      },
      {
        "support": "documentation.scope-claims.support-task",
        "unit": "documentation.scope-claims"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "docs/architecture.md",
    "src/devtools/context/planning/docs/overview.md"
  ],
  "required_units": [
    "documentation.package-baseline",
    "documentation.architecture-baseline",
    "documentation.scope-claims"
  ]
}
```

### validation.alternative-01

```json
{
  "identity": "validation.alternative-01",
  "inferability_assumptions": [],
  "obligation": "case-0012-direct-source-disclosure/validation",
  "proof_variants": [
    [
      {
        "support": "validation.protected-profile.support-01",
        "unit": "validation.protected-profile"
      },
      {
        "support": "validation.pytest-config.support-01",
        "unit": "validation.pytest-config"
      },
      {
        "support": "validation.coverage-config.support-01",
        "unit": "validation.coverage-config"
      },
      {
        "support": "validation.ruff-config.support-01",
        "unit": "validation.ruff-config"
      },
      {
        "support": "validation.mypy-config.support-01",
        "unit": "validation.mypy-config"
      },
      {
        "support": "validation.quality-commands.support-01",
        "unit": "validation.quality-commands"
      }
    ]
  ],
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "rationale_for_completeness": "Each proof variant supports every required semantic unit. All listed resource members are jointly required for this alternative; task-backed units contribute no repository resource.",
  "rationale_for_minimality": "No complete support assignment covers this obligation with a proper subset of these resources. Equivalent assignments over the same resource set are proof variants, not extra simultaneously required evidence.",
  "required_resources": [
    "docs/development/validation.md",
    "pyproject.toml"
  ],
  "required_units": [
    "validation.protected-profile",
    "validation.pytest-config",
    "validation.coverage-config",
    "validation.ruff-config",
    "validation.mypy-config",
    "validation.quality-commands"
  ]
}
```

## Complete task combinations and sufficient unions

```json
{
  "complete_task_combinations": [
    {
      "alternatives": [
        "source.alternative-01",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0001",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-01",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0002",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-01",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0003",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-01",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0004",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-02",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0005",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-02",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0006",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-02",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0007",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-02",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0008",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-03",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0009",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-03",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0010",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-03",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0011",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-03",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0012",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/docs/overview.md",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-04",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0013",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-04",
        "choices.alternative-01",
        "integrity.alternative-01",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0014",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-04",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-01",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0015",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/declarations.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    },
    {
      "alternatives": [
        "source.alternative-04",
        "choices.alternative-01",
        "integrity.alternative-02",
        "materialization.alternative-02",
        "assembly.alternative-01",
        "exports.alternative-01",
        "tests.alternative-01",
        "documentation.alternative-01",
        "validation.alternative-01"
      ],
      "identity": "task-combination-0016",
      "resources": [
        "docs/architecture.md",
        "docs/development/validation.md",
        "pyproject.toml",
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/docs/overview.md",
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/classes/docs/overview.md",
        "src/devtools/context/python/function/declarations.py",
        "src/devtools/context/python/function/materialization.py",
        "src/devtools/context/python/function/planned_reference.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py",
        "tests/context/planning/test_plan.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy",
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility",
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims",
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface",
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame",
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order",
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector",
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation",
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    }
  ],
  "distinct_sufficient_resource_unions": [
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/declarations.py",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/docs/overview.md",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py"
    ],
    [
      "docs/architecture.md",
      "docs/development/validation.md",
      "pyproject.toml",
      "src/devtools/context/__init__.py",
      "src/devtools/context/planning/__init__.py",
      "src/devtools/context/planning/docs/overview.md",
      "src/devtools/context/planning/materialization.py",
      "src/devtools/context/planning/plan.py",
      "src/devtools/context/planning/rendering.py",
      "src/devtools/context/planning/resource.py",
      "src/devtools/context/python/classes/containment.py",
      "src/devtools/context/python/classes/docs/overview.md",
      "src/devtools/context/python/function/declarations.py",
      "src/devtools/context/python/function/materialization.py",
      "src/devtools/context/python/function/planned_reference.py",
      "src/devtools/context/python/modules/selection.py",
      "src/devtools/context/repository/snapshot.py",
      "tests/context/planning/test_plan.py"
    ]
  ],
  "distinct_sufficient_unit_unions": [
    [
      "assembly.no-budget",
      "assembly.rendering",
      "assembly.request-copy",
      "choices.admission",
      "choices.caller-selection",
      "choices.plan-admission",
      "choices.plan-identity",
      "choices.plan-value",
      "choices.reference-compatibility",
      "choices.whole-compatibility",
      "documentation.architecture-baseline",
      "documentation.package-baseline",
      "documentation.scope-claims",
      "exports.assembly-ownership",
      "exports.option-ownership",
      "exports.outer-surface",
      "exports.planning-surface",
      "integrity.canonical-membership",
      "integrity.lookup",
      "integrity.method-frame",
      "integrity.plan-frame",
      "integrity.publication",
      "integrity.returned-identity",
      "integrity.selection-frame",
      "materialization.bounded-meaning",
      "materialization.coordinates",
      "materialization.decorator-boundary",
      "materialization.extraction",
      "materialization.item-provenance",
      "materialization.mixed-order",
      "source.class-identity",
      "source.containment",
      "source.excluded-resolution",
      "source.function-identity",
      "source.method-identity",
      "source.selector",
      "tests.class-choice",
      "tests.decorated",
      "tests.exact-fidelity",
      "tests.existing-choices",
      "tests.function-choice",
      "tests.method-choice",
      "tests.mixed-order",
      "tests.rejection",
      "tests.repeated",
      "tests.request-preservation",
      "validation.coverage-config",
      "validation.mypy-config",
      "validation.protected-profile",
      "validation.pytest-config",
      "validation.quality-commands",
      "validation.ruff-config"
    ]
  ],
  "maximum_sufficient_resource_count": 20,
  "maximum_sufficient_unit_count": 52,
  "minimum_sufficient_resource_count": 17,
  "minimum_sufficient_unit_count": 52,
  "obligation_indispensable": {
    "assembly": {
      "resources": [
        "src/devtools/context/planning/rendering.py"
      ],
      "units": [
        "assembly.no-budget",
        "assembly.rendering",
        "assembly.request-copy"
      ]
    },
    "choices": {
      "resources": [
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/resource.py",
        "src/devtools/context/python/function/planned_reference.py"
      ],
      "units": [
        "choices.admission",
        "choices.caller-selection",
        "choices.plan-admission",
        "choices.plan-identity",
        "choices.plan-value",
        "choices.reference-compatibility",
        "choices.whole-compatibility"
      ]
    },
    "documentation": {
      "resources": [
        "docs/architecture.md",
        "src/devtools/context/planning/docs/overview.md"
      ],
      "units": [
        "documentation.architecture-baseline",
        "documentation.package-baseline",
        "documentation.scope-claims"
      ]
    },
    "exports": {
      "resources": [
        "src/devtools/context/__init__.py",
        "src/devtools/context/planning/__init__.py",
        "src/devtools/context/planning/plan.py",
        "src/devtools/context/planning/rendering.py"
      ],
      "units": [
        "exports.assembly-ownership",
        "exports.option-ownership",
        "exports.outer-surface",
        "exports.planning-surface"
      ]
    },
    "integrity": {
      "resources": [
        "src/devtools/context/python/classes/containment.py",
        "src/devtools/context/python/modules/selection.py",
        "src/devtools/context/repository/snapshot.py"
      ],
      "units": [
        "integrity.canonical-membership",
        "integrity.lookup",
        "integrity.method-frame",
        "integrity.plan-frame",
        "integrity.publication",
        "integrity.returned-identity",
        "integrity.selection-frame"
      ]
    },
    "materialization": {
      "resources": [
        "src/devtools/context/planning/materialization.py",
        "src/devtools/context/python/function/materialization.py"
      ],
      "units": [
        "materialization.bounded-meaning",
        "materialization.coordinates",
        "materialization.decorator-boundary",
        "materialization.extraction",
        "materialization.item-provenance",
        "materialization.mixed-order"
      ]
    },
    "source": {
      "resources": [
        "src/devtools/context/python/function/declarations.py"
      ],
      "units": [
        "source.class-identity",
        "source.containment",
        "source.excluded-resolution",
        "source.function-identity",
        "source.method-identity",
        "source.selector"
      ]
    },
    "tests": {
      "resources": [],
      "units": [
        "tests.class-choice",
        "tests.decorated",
        "tests.exact-fidelity",
        "tests.existing-choices",
        "tests.function-choice",
        "tests.method-choice",
        "tests.mixed-order",
        "tests.rejection",
        "tests.repeated",
        "tests.request-preservation"
      ]
    },
    "validation": {
      "resources": [
        "docs/development/validation.md",
        "pyproject.toml"
      ],
      "units": [
        "validation.coverage-config",
        "validation.mypy-config",
        "validation.protected-profile",
        "validation.pytest-config",
        "validation.quality-commands",
        "validation.ruff-config"
      ]
    }
  },
  "task_indispensable_resources": [
    "docs/architecture.md",
    "docs/development/validation.md",
    "pyproject.toml",
    "src/devtools/context/__init__.py",
    "src/devtools/context/planning/__init__.py",
    "src/devtools/context/planning/docs/overview.md",
    "src/devtools/context/planning/materialization.py",
    "src/devtools/context/planning/plan.py",
    "src/devtools/context/planning/rendering.py",
    "src/devtools/context/planning/resource.py",
    "src/devtools/context/python/classes/containment.py",
    "src/devtools/context/python/function/declarations.py",
    "src/devtools/context/python/function/materialization.py",
    "src/devtools/context/python/function/planned_reference.py",
    "src/devtools/context/python/modules/selection.py",
    "src/devtools/context/repository/snapshot.py"
  ],
  "task_indispensable_units": [
    "assembly.no-budget",
    "assembly.rendering",
    "assembly.request-copy",
    "choices.admission",
    "choices.caller-selection",
    "choices.plan-admission",
    "choices.plan-identity",
    "choices.plan-value",
    "choices.reference-compatibility",
    "choices.whole-compatibility",
    "documentation.architecture-baseline",
    "documentation.package-baseline",
    "documentation.scope-claims",
    "exports.assembly-ownership",
    "exports.option-ownership",
    "exports.outer-surface",
    "exports.planning-surface",
    "integrity.canonical-membership",
    "integrity.lookup",
    "integrity.method-frame",
    "integrity.plan-frame",
    "integrity.publication",
    "integrity.returned-identity",
    "integrity.selection-frame",
    "materialization.bounded-meaning",
    "materialization.coordinates",
    "materialization.decorator-boundary",
    "materialization.extraction",
    "materialization.item-provenance",
    "materialization.mixed-order",
    "source.class-identity",
    "source.containment",
    "source.excluded-resolution",
    "source.function-identity",
    "source.method-identity",
    "source.selector",
    "tests.class-choice",
    "tests.decorated",
    "tests.exact-fidelity",
    "tests.existing-choices",
    "tests.function-choice",
    "tests.method-choice",
    "tests.mixed-order",
    "tests.rejection",
    "tests.repeated",
    "tests.request-preservation",
    "validation.coverage-config",
    "validation.mypy-config",
    "validation.protected-profile",
    "validation.pytest-config",
    "validation.quality-commands",
    "validation.ruff-config"
  ]
}
```

## Task and repository-information gaps

```json
{
  "blocks_judgment": false,
  "evidence": [
    {
      "coordinate_system": "zero-based Unicode character offsets; half-open",
      "end": 2668,
      "kind": "task",
      "provenance": {
        "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
        "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
        "frame": {
          "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
          "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
          "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
          "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
          "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
        }
      },
      "start": 0,
      "task_identity": "case-0012-direct-source-disclosure",
      "text": "Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.\nReuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.\nIntegrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.\nValidate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.\nMaterialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.\nPreserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.\nExpose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.\nAdd focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.\nUpdate file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.\nValidate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.\n"
    }
  ],
  "rationale": "The task requests future software behavior, not an already completed implementation. All mandatory source, integration, integrity, representation, assembly, public API, test, documentation and development-profile semantics can be established/design-bounded from the task and frozen native contracts. Operational handoff/reliability work is outside feature semantics.",
  "status": "NONE"
}
```

```json
{
  "blocks_judgment": false,
  "evidence_unit_ids": [
    "source.selector",
    "source.function-identity",
    "source.class-identity",
    "source.method-identity",
    "source.containment",
    "source.excluded-resolution",
    "choices.plan-value",
    "choices.plan-admission",
    "choices.plan-identity",
    "choices.admission",
    "choices.whole-compatibility",
    "choices.reference-compatibility",
    "choices.caller-selection",
    "integrity.lookup",
    "integrity.selection-frame",
    "integrity.method-frame",
    "integrity.canonical-membership",
    "integrity.plan-frame",
    "integrity.returned-identity",
    "integrity.publication",
    "materialization.coordinates",
    "materialization.extraction",
    "materialization.decorator-boundary",
    "materialization.item-provenance",
    "materialization.mixed-order",
    "materialization.bounded-meaning",
    "assembly.rendering",
    "assembly.request-copy",
    "assembly.no-budget",
    "exports.planning-surface",
    "exports.outer-surface",
    "exports.option-ownership",
    "exports.assembly-ownership",
    "tests.function-choice",
    "tests.class-choice",
    "tests.method-choice",
    "tests.decorated",
    "tests.repeated",
    "tests.mixed-order",
    "tests.exact-fidelity",
    "tests.rejection",
    "tests.existing-choices",
    "tests.request-preservation",
    "documentation.package-baseline",
    "documentation.architecture-baseline",
    "documentation.scope-claims",
    "validation.protected-profile",
    "validation.pytest-config",
    "validation.coverage-config",
    "validation.ruff-config",
    "validation.mypy-config",
    "validation.quality-commands"
  ],
  "rationale": "Every necessary unit has complete retained support alternatives. No unavailable checkout file, external runtime binding, confirmation artifact or proposed API name is needed to judge these obligations.",
  "status": "NONE"
}
```

## Limitations and preserved ambiguities

### limitation.decorator-range

CONSTRAINS_IMPLEMENTATION; blocks judgment: False.

Native spans exclude decorator lines; the task requires preserving decorators. Existing extraction alone is insufficient. The new representation needs explicit decorator-inclusive support/range accounting or an authorized native-range extension without runtime evaluation.

These facts bound the implementation rather than prove it impossible. The frozen source contains the ranges and retained text needed to define a faithful extension; no absent repository fact or inferred runtime semantics is required.

[evidence-0114](#evidence-0114), [evidence-0047](#evidence-0047)

### limitation.explicit-cardinality

CONSTRAINS_IMPLEMENTATION; blocks judgment: False.

The task fixes caller-selected native identities and repeated-declaration preservation, but does not select final new option names or whether a factory offers one explicit declaration or a caller-approved tuple of native matches.

Both explicit per-declaration choice and explicit caller selection of a multi-match group are defensible if native identity, order and no automatic selection/owner expansion remain intact. This is not an unresolved resource label or an invented behavior requirement.

[evidence-0097](#evidence-0097), [evidence-0069](#evidence-0069), [evidence-0028](#evidence-0028)

### limitation.architecture-status

NOTEWORTHY; blocks judgment: False.

Broad architecture/ADR prose still describes general assembly/materializer mechanisms as future, while concrete source and narrower implemented-status paragraphs establish the existing common boundary.

Preserve the distinction between bounded implemented functions and general future infrastructure; documentation of the feature must not promote broad automatic planning/readiness. This constrains claims, not the repository fact judgment.

[evidence-0004](#evidence-0004), [evidence-0005](#evidence-0005), [evidence-0007](#evidence-0007), [evidence-0034](#evidence-0034)

### limitation.definition-replay

CONSTRAINS_IMPLEMENTATION; blocks judgment: False.

Native subject/derivation identity binds parser implementation/runtime version and grammar. Canonical native comparison must use compatible derivation-definition semantics rather than assuming only content controls identity.

The native definitions directly bound reproducibility. No external runtime reproduction is required for this semantic adjudication.

[evidence-0052](#evidence-0052), [evidence-0039](#evidence-0039)

```json
[
  {
    "blocks_judgment": false,
    "identity": "ambiguity.new-choice-cardinality",
    "interpretations": [
      "One caller-selected native declaration per new choice.",
      "A caller explicitly approves an ordered group of native selection matches."
    ],
    "limitation": "limitation.explicit-cardinality",
    "rationale": "The task leaves new API shape open; neither interpretation permits automatic selection, merging repeated identities, or implicit whole-owner expansion.",
    "status": "PRESERVED"
  }
]
```

## Unresolved judgments

```json
[]
```

## Internal PRIMARY self-review

```json
{
  "findings": [
    "Broad architectural background retained as helpful unless a specific mandatory baseline fact is supplied.",
    "Named script retained helpful because documented gates already supply its selection contract; filenames alone do not establish necessity.",
    "Existing tests retained helpful for test obligation. Task-backed test categories need zero repository witnesses.",
    "Whole-resource test alternative removed: it did not establish the full old choice identity schema.",
    "Separable plan identity/admission, class/method identities, Ruff/mypy and decorator/repetition/order/fidelity test units split.",
    "Redundant support members pruned at obligation level; cross-obligation reuse retained in distinct task unions.",
    "Containment provenance checks do not authenticate all source facts; canonical membership inference explicitly retained.",
    "Decorator exclusion, API cardinality and derivation-definition boundaries preserved as limitations without fabricated gaps."
  ],
  "kind": "Internal review of the same PRIMARY adjudication",
  "status": "COMPLETED_AND_REVISED"
}
```

## Blind access attestation

```json
{
  "Git_history": "NO",
  "acquisition_costs": "NO",
  "confirmation_or_reserve_data": "NO",
  "experiment_arms": "NO",
  "external_web_information": "NO",
  "hint_or_routing_artifacts": "NO",
  "parent_or_sibling_workspace_files": "NO",
  "prior_gold": "NO",
  "rankings": "NO",
  "repository_checkout": "NO",
  "retrieval_queries": "NO",
  "scores": "NO",
  "treatment_results": "NO"
}
```

NO denotes access to excluded artifacts/information, not natural vocabulary, frame provenance or historical references occurring inside original frozen repository text. No such references were used to infer the present adjudication.

## Exact evidence registry

Offsets below are Unicode character offsets within the original frozen text, half-open. Native Python source coordinates remain separate.

<a id="evidence-0001"></a>

### evidence-0001

```json
{
  "address": "AGENTS.md",
  "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
  "end": 11283,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 10713
}
```

````text
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

````

<a id="evidence-0002"></a>

### evidence-0002

```json
{
  "address": "docs/architecture.md",
  "content_identity": "fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391",
  "end": 41021,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 40103
}
```

```text
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

```

<a id="evidence-0003"></a>

### evidence-0003

```json
{
  "address": "docs/architecture.md",
  "content_identity": "fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391",
  "end": 69971,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 65307
}
```

````text
## Accepted Context and disclosure semantics

The [heterogeneous evidence admission and recovery investigation](research/heterogeneous-context-admission-and-recovery.md)
and ADR-0004's 2026-10-02 refinement selected an **unimplemented** direction:
evidence-guided option admission inside Context Planning, with a
separate observable decision/coverage account alongside the selected plan.
Native resource, declaration, occurrence and relationship identities remain
referents; concrete representations consume disclosure capacity. There is no
mandatory intermediate file-admission service or universal evidence score.

ADR-0005 now separates obligation resolution from representation admission. The
earlier question-lane score floors/capacity weights remain historical development
research, not the next implementation policy. Context retains concrete option
choice, exact materialization, representation-relative coverage and capacity;
Localization supplies obligation witnesses and unresolved requirements.

Bounded planning assessments distinguish integrity, applicability, cost,
currently available requested representations and open questions. They do not
establish general Context sufficiency. Requests may acquire information for a
question or expand an exact target; obligation acquisition is interpreted by
Localization and exact representation expansion by Context. Context
plans/materializes, while
Agent/orchestration decides successive attempts, validation, recovery limits
and escalation. Previous plan lineage does not establish current availability.
This accepts request semantics, not a transport, Tool registry or recovery loop.

[ADR-0004](architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md)
accepts the post-ranking Context layer. Context compilation is conditional
information composition, not top-K retrieval or automatic budget filling.
Disclosure planning couples candidate and representation choice and reasons
about coverage, marginal contribution, complementarity, representation-relative
overlap, prior currently available information, applicability, sufficiency,
authority, and multidimensional cost. It selects information rather than prompt
strings. A DisclosureOption is a future purpose-relative possibility for
exposing information through a selected representation or transformation, with
origin, form, fidelity, cost, and provenance kept semantically distinct.
Source-preserving material, existing knowledge projections, and synthesized
semantic assertions are distinct origins. A new
repository-relative assertion can be ADR-0002 DerivedKnowledge; a purpose-
relative Context synthesis remains explicit and provenance-bearing without
automatic promotion to repository intelligence. Composite provenance-preserving
representations are permitted.

DisclosurePlan, ContextDisclosure, and ModelRequest remain distinct:

```text
InformationNeed -> DisclosurePlan -> materialization -> ContextDisclosure
    -> model-input assembly -> ModelRequest
```

The Plan is an immutable selected-information decision; the Disclosure is an
immutable realized information artifact under/reference to that plan; the
ModelRequest is a consumer-specific presentation. Materialization faithfully
realizes the selected representation and may perform an explicitly planned
semantic transformation or lossy synthesis. It cannot silently re-plan, invent
a materially different synthesis, or present inapplicable information as
current. Assembly arranges already-realized disclosure and must not introduce
new semantic assertions through formatting, placement, or budget handling.
Planning and possession of a disclosure are not disclosure/presentation
authority.

The implemented DisclosurePlan is intentionally narrower than this accepted
general concept: a caller chooses its purpose and concrete options. Supported
forms are a qualified Python Reference fact with exact source and target
declaration, and an explicit whole observed resource. The plan is bound to
one snapshot, preserves ordered choices and optional preceding-plan lineage,
and materializes to a ContextDisclosure with native provenance. Retrieval
rank may inform a caller but does not automatically choose a representation,
disclosure quantity, or claim of sufficiency. ADR-0004 continues to govern
future planning, cost, and disclosure semantics. The
[Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
motivates this boundary and a separate query-conditioned structural-ranking
baseline; its automatic planner, graph weighting, and fusion recommendations
are not implemented here.

````

<a id="evidence-0004"></a>

### evidence-0004

```json
{
  "address": "docs/architecture.md",
  "content_identity": "fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391",
  "end": 69971,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 69006
}
```

```text
The implemented DisclosurePlan is intentionally narrower than this accepted
general concept: a caller chooses its purpose and concrete options. Supported
forms are a qualified Python Reference fact with exact source and target
declaration, and an explicit whole observed resource. The plan is bound to
one snapshot, preserves ordered choices and optional preceding-plan lineage,
and materializes to a ContextDisclosure with native provenance. Retrieval
rank may inform a caller but does not automatically choose a representation,
disclosure quantity, or claim of sufficiency. ADR-0004 continues to govern
future planning, cost, and disclosure semantics. The
[Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
motivates this boundary and a separate query-conditioned structural-ranking
baseline; its automatic planner, graph weighting, and fusion recommendations
are not implemented here.

```

<a id="evidence-0005"></a>

### evidence-0005

```json
{
  "address": "docs/architecture.md",
  "content_identity": "fea96cb29341a4b8fa8b409c223870b155f0e51a350db6c6b9a9f4d650b75c8b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "04da2f220007ae00b8c35c5d6c0a0c39ae027df5f7eea6add7a9c43b45519391",
  "end": 71617,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 71399
}
```

```text
Concrete coverage, fidelity,
authority, uncertainty, completeness, conflict, coherence, semantic-
transformation/synthesis validation, materialization, cache, assembly, and
evaluation mechanisms remain unimplemented.

```

<a id="evidence-0006"></a>

### evidence-0006

```json
{
  "address": "docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md",
  "content_identity": "d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb",
  "end": 18444,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 16740
}
```

```text
### Planning versus model-input assembly

Disclosure planning determines **what** information should be available:
candidate/representation choices, coverage, marginal contribution, overlap,
complementarity, prior availability, applicability, authority, coherence, and
cost/budget. Model-input assembly determines **how** selected information is
realized and positioned for a particular model interaction: provider
serialization, prompt structure, order, separators, tokenizer/model constraints,
and coexistence with tools, instructions, and conversation.

Presentation order may affect utilization, but does not contaminate repository
relevance or coverage semantics. Selection decides what to disclose;
presentation policy arranges selected material. Positional effects are empirical,
model-specific evidence, not universal rules. Future assembly policy can depend
on identified hard capabilities and versioned empirical behavior profiles without
changing repository relevance evidence. Neither `ModelCapabilities` nor
`ModelBehaviorProfile` is selected as a model.

Assembly arranges and serializes already-realized disclosure. It must not
silently introduce a new semantic assertion through placement, formatting,
truncation, or token-budget handling. If a semantic compression or synthesis is
needed to fit a consumer constraint, disclosure planning must select it and
materialization must realize it before assembly presents it.

The same ContextDisclosure may be assembled by different identified policies
into different ModelRequests. This permits presentation/input experiments while
holding retrieval, ranking, and disclosure selection fixed. No assembly
abstraction or policy is implemented.

```

<a id="evidence-0007"></a>

### evidence-0007

```json
{
  "address": "docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md",
  "content_identity": "d0290dfb94b0f778386c2c3b49ec6794e74af6ada402d260c34221bbf267a63f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "3ef8f4c17bde748518e7990711d199b054ba95cdf67fe9e92da548a643782ceb",
  "end": 31482,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 30700
}
```

```text
## Status and implementation boundary

This decision accepts Context/disclosure semantics only. It does not implement
a compiler, DisclosureOption, DisclosurePlan, ContextDisclosure,
representation/coverage/satisfaction model, decomposition mechanism,
utility/stopping/budget policy, availability/history store, applicability cache,
capability/behavior profile, assembly layer, tokenizer integration, derived
representation, semantic-transformation or synthesis mechanism, synthesis
store, persistence, or evaluation infrastructure. B-0002 retains this
unimplemented design pressure.
ADR-0001 remains the model-native Tool boundary; ADR-0002 remains repository
identity/derivation/graph architecture; ADR-0003 remains InformationNeed,
retrieval, evidence, and ranking architecture.
```

<a id="evidence-0008"></a>

### evidence-0008

```json
{
  "address": "docs/architecture/taxonomy.md",
  "content_identity": "24677a057596cb8157bd77407c35ff82c4cc58c27908ddb72e32f79e266a010e",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e13fc10a26ce00bb5fc7641ea0ac13d59bbf6872873bac1c00021fd86a762f01",
  "end": 49075,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 42922
}
```

```text
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

The accepted, unimplemented planning direction admits concrete disclosure
options through a Context-owned policy and records bounded coverage, constraints,
deferrals and recovery targets beside the plan. Native information referents
remain distinct from representations. No mandatory resource-Selection service
or boolean ContextSufficiency follows. Acquisition for a question and expansion
of an exact disclosure target are Context request semantics; successive attempts
and escalation remain Agent/orchestration decisions. ADR-0005 now assigns
task-obligation resolution and acquisition requests to Localization; Context
retains representation admission and exact expansion. The earlier question-lane
policy is not the next production baseline. See ADR-0004's refinement.

Disclosure selects information rather than arbitrary prompt strings. A
DisclosureOption is a conceptual purpose-relative possibility for making
identified information about one or more subjects available through a
representation or explicitly characterized transformation. Origin, form,
fidelity, and cost are separate concerns.
Source-preserving representations select/transform identified source without
new semantic assertions; knowledge projections expose existing DerivedKnowledge;
synthesized representations introduce new semantic assertions and therefore
must preserve explicit origin and support without automatically becoming
repository DerivedKnowledge. Determinism does not by itself establish semantic
certainty. Composite representations may preserve multiple constituent origins.

A representational transformation changes how available information is exposed
without intentionally establishing a materially new semantic assertion. An
epistemic derivation establishes such an assertion. Repository-relative
epistemic derivation can establish DerivedKnowledge under ADR-0002; purpose-
relative Context synthesis remains owned by ADR-0004 and can remain ephemeral.
Lossy compression can cross the epistemic boundary when it implicitly asserts
an interpretation. This conceptual distinction does not require production
classes, enums, independent identity, persistence, or a complete representation
taxonomy.

Materialization faithfully realizes the representation or transformation
selected by a DisclosurePlan. It may perform explicitly planned semantic
transformation or lossy synthesis, but it must not silently invent a materially
different synthesis or disclosure decision. Model-input assembly arranges and
serializes already-realized disclosure; formatting, placement, truncation, and
budget handling must not silently introduce new semantic assertions.

Across representation selection, projection, synthesis, compression,
materialization, ContextDisclosure realization, and assembly, semantic
commitment must not be silently strengthened beyond source semantics, support,
assumptions/scope, conflict state, and semantic-result coverage. A possible
relationship cannot become definite, a partial set exhaustive, an approximation
exact, or a disagreement one truth without an identified semantically capable
process establishing that stronger result.

Disclosure planning determines what information becomes available; model-input
assembly determines how selected information is serialized, ordered, and placed
for a particular model interaction. Presentation effects are empirical
consumer-behavior evidence, not repository relevance or coverage truth. Budget
is a ceiling, not a target, and is distinct from discovery bounds. Optional
Information-purpose decomposition may lead to subordinate purpose/acquisition
work without discarding the broader purpose or requiring persistent child
artifacts; child satisfaction does not prove parent sufficiency. See
[ADR-0004](decisions/ADR-0004-context-disclosure-planning-and-assembly.md).

Coherence is intelligibility of information presented together and the avoided
consumer reconstruction burden, not physical contiguity. Authority is
claim-/purpose-relative evidence, not a universal source ordering, and remains
distinct from relevance, confidence, coverage, and ranking influence. Material
conflicts and absence discipline remain preservable: disclosure planning does
not generally resolve truth, and missing evidence does not prove its opposite.
Provenance explains origin and support; it does not by itself establish
authority, certainty, correctness, or truth. No universal confidence,
epistemic-status, authority, or truth field is selected.

```

<a id="evidence-0009"></a>

### evidence-0009

```json
{
  "address": "docs/development/validation.md",
  "content_identity": "474b6742cbc1675e8edc369e9319560b2827c013aa2311313e8759ee74e00371",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "248e605c7cf568ea55bf033a8e56646806da9716a81f586d6f02318fd6311383",
  "end": 1423,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 26
}
```

````text
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

````

<a id="evidence-0010"></a>

### evidence-0010

```json
{
  "address": "docs/development/validation.md",
  "content_identity": "474b6742cbc1675e8edc369e9319560b2827c013aa2311313e8759ee74e00371",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "248e605c7cf568ea55bf033a8e56646806da9716a81f586d6f02318fd6311383",
  "end": 1787,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1423
}
```

````text
## Other quality gates

The protected command runs tests only. Run the applicable static checks as
separate commands:

```text
uv run ruff check .
uv run ruff format --check
uv run mypy
git diff --check
```

When changes are staged, also run `git diff --cached --check`. This profile is
test selection, not a general validation pipeline or confirmation mechanism.
````

<a id="evidence-0011"></a>

### evidence-0011

```json
{
  "address": "docs/documentation_map.md",
  "content_identity": "a5b938a9ff8d24c0f569e5ad30a4f513f01ed381ee15a5fd924506f2974c3ed8",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "522793a2217a50bdc6e54b0eff3f79a3f67fe15a31ebfbc05002f327971f55ba",
  "end": 22656,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 22161
}
```

```text
The [Context Planning package](../src/devtools/context/planning/docs/overview.md)
owns a bounded caller-directed DisclosurePlan over one explicit purpose and
snapshot. It currently composes qualified Python Reference and whole retained
resource representations, rejects stale dependencies, preserves native
provenance in realized ContextDisclosure items, and renders/assembles them
after materialization. It does not retrieve, rank, autonomously select,
optimize budgets, or judge sufficiency.

```

<a id="evidence-0012"></a>

### evidence-0012

```json
{
  "address": "docs/roadmap.md",
  "content_identity": "59aa61e214977c4a25e60c1f69fca8ee7688e71ba7d8ab9361f3de0c84bf8671",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "c5a530215f102a343d68092d0f1664b3adc60dc57b27ed49ee6f54d68fc9e5ec",
  "end": 26853,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 26179
}
```

```text
The current Context checkpoint establishes a caller-directed, snapshot-bound
DisclosurePlan with multiple ordered concrete choices and a distinct realized
ContextDisclosure. The existing qualified Reference path participates without
losing its native checks; an explicitly chosen whole observed resource is a
second faithful representation. This is a production planning boundary, not
automatic ranking, budget allocation, sufficiency, or a recovery controller.
The [Context Planning and graph-assisted retrieval research](research/repository-context-planning-and-graph-assisted-retrieval.md)
provides comparative motivation; ADR-0003 and ADR-0004 govern accepted meaning.

```

<a id="evidence-0013"></a>

### evidence-0013

```json
{
  "address": "pyproject.toml",
  "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
  "end": 1032,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 585
}
```

```text
[tool.pytest.ini_options]
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

```

<a id="evidence-0014"></a>

### evidence-0014

```json
{
  "address": "pyproject.toml",
  "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
  "end": 1368,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1032
}
```

```text
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
```

<a id="evidence-0015"></a>

### evidence-0015

```json
{
  "address": "scripts/validate_development.py",
  "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
  "end": 531,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 248
}
```

```text
def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    """Select ordinary tests while excluding the retained experiment tree."""
    tests = repository_root / "tests"
    experiments = tests / "experiments"
    return [str(tests), f"--ignore={experiments}"]
```

<a id="evidence-0016"></a>

### evidence-0016

```json
{
  "address": "scripts/validate_development.py",
  "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
  "end": 657,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 533
}
```

```text
def main() -> int:
    """Run pytest and return its exit code unchanged."""
    return int(pytest.main(pytest_arguments()))
```

<a id="evidence-0017"></a>

### evidence-0017

```json
{
  "address": "src/devtools/context/__init__.py",
  "content_identity": "e2392c9351df7a0f17f23f2ccd15e3fd1436c4e59eb7e0ee9eb7d0d0c32a445c",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e44bbb91c8804801b3ec8c1731768a79edb711856c5773559b29b654d25ac198",
  "end": 497,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 84
}
```

```text
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
```

<a id="evidence-0018"></a>

### evidence-0018

```json
{
  "address": "src/devtools/context/__init__.py",
  "content_identity": "e2392c9351df7a0f17f23f2ccd15e3fd1436c4e59eb7e0ee9eb7d0d0c32a445c",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e44bbb91c8804801b3ec8c1731768a79edb711856c5773559b29b654d25ac198",
  "end": 9619,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4841
}
```

```text
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
```

<a id="evidence-0019"></a>

### evidence-0019

```json
{
  "address": "src/devtools/context/localization/grounding/resolve.py",
  "content_identity": "cc9086d27d2929f521f47680bd5a7e64b78f88e4e035bdbcbe87d549b9ff7ba8",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7776e3bf22c9fc0658855e1b11bc84f78d9d6970fd6bb59987594c506cce0f35",
  "end": 7425,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5088
}
```

```text
def _ground_declaration(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectDeclarationLocator,
    universe: PythonModuleInterpretationUniverse,
) -> AnchorGrounding:
    modules = tuple(
        item
        for item in lookup_python_modules(universe, locator.module.dotted_name)
        if locator.module.kind is None or item.kind is locator.module.kind
    )
    observations: list[NativeGroundingEvidence] = []
    candidates: list[AnchorGroundingCandidate] = []
    unsupported = False
    for module in modules:
        try:
            selection = select_python_module_source_declarations(
                snapshot,
                module=module,
                declared_name=locator.declared_name,
                kind=PythonSourceDeclarationKind(locator.kind.value),
            )
        except (PythonModuleParseError, PythonClassMethodParseError, SyntaxError):
            unsupported = True
            continue
        observations.append(selection)
        candidates.extend(
            AnchorGroundingCandidate(item, selection) for item in selection.declarations
        )
    disposition = (
        AnchorGroundingDisposition.AMBIGUOUS
        if len(candidates) > 1 or (unsupported and bool(candidates))
        else AnchorGroundingDisposition.UNSUPPORTED
        if unsupported
        else _candidate_disposition(tuple(candidates))
    )
    reason = {
        AnchorGroundingDisposition.RESOLVED: (
            "Exactly one native source declaration matches the exact locator; "
            "runtime binding identity is not established."
        ),
        AnchorGroundingDisposition.AMBIGUOUS: (
            "Multiple native declarations or incompletely interpreted modules prevent "
            "unique source declaration selection."
        ),
        AnchorGroundingDisposition.UNRESOLVED: (
            "No requested direct declaration was found in the supplied modules."
        ),
        AnchorGroundingDisposition.UNSUPPORTED: (
            "Relevant syntax cannot establish the requested direct declaration."
        ),
    }[disposition]
    return _account(
        request,
        GroundingResolver.PYTHON_SOURCE_DECLARATION_SELECTION,
        tuple(candidates),
        tuple(observations),
        universe,
        disposition,
        reason,
    )
```

<a id="evidence-0020"></a>

### evidence-0020

```json
{
  "address": "src/devtools/context/localization/grounding/resolve.py",
  "content_identity": "cc9086d27d2929f521f47680bd5a7e64b78f88e4e035bdbcbe87d549b9ff7ba8",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7776e3bf22c9fc0658855e1b11bc84f78d9d6970fd6bb59987594c506cce0f35",
  "end": 9271,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 7427
}
```

```text
def _ground_method(
    snapshot: RepositorySnapshot,
    request: AnchorGroundingRequest,
    locator: PythonDirectMethodLocator,
) -> AnchorGrounding:
    parent = locator.containing_class
    if (
        parent.subject.snapshot_id != snapshot.id
        or parent.support.snapshot_id != snapshot.id
    ):
        msg = "Direct method locator contains a foreign or stale class declaration."
        raise ValueError(msg)
    address = parent.support.resource_address
    try:
        analysis = derive_python_class_method_declarations(
            snapshot,
            resource_address=address,
        )
    except PythonClassMethodParseError:
        return _account(
            request,
            GroundingResolver.PYTHON_METHOD_CONTAINMENT,
            (),
            (),
            None,
            AnchorGroundingDisposition.UNSUPPORTED,
            "Observed Python source cannot be analyzed for direct methods.",
        )
    view = build_python_class_method_containment_view(
        snapshot,
        aggregate=PythonClassMethodAnalysisAggregate((analysis,)),
    )
    if parent not in analysis.classes:
        msg = "Direct method locator contains a stale or foreign class declaration."
        raise ValueError(msg)
    methods = tuple(
        item
        for item in view.direct_methods_of(parent)
        if item.declared_name == locator.declared_name
    )
    candidates = tuple(AnchorGroundingCandidate(item, analysis) for item in methods)
    return _account(
        request,
        GroundingResolver.PYTHON_METHOD_CONTAINMENT,
        candidates,
        (analysis,),
        None,
        _candidate_disposition(candidates),
        "Exact direct class-body method syntax matched in the observed class."
        if methods
        else "No exact direct method syntax matched in the observed class.",
    )
```

<a id="evidence-0021"></a>

### evidence-0021

```json
{
  "address": "src/devtools/context/planning/__init__.py",
  "content_identity": "f0a22d1b55645d1c428dd456c527cbe41e36ebbcaab3ca09229498d3e2f7f8d3",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "4950d26efdac0ac7b2855daddf9406849e26a401d0a5f6a31840aca64f4eea5d",
  "end": 1080,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 0
}
```

```text
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
```

<a id="evidence-0022"></a>

### evidence-0022

```json
{
  "address": "src/devtools/context/planning/docs/overview.md",
  "content_identity": "a679cfa5ee0591036eaab418fa386a0885ef748f98287b8dd49846c093b068bd",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "de0155f1cfe9bdb78fffb3e8897785e5a32f6147ddcd291c3bc7d67f7f9b274a",
  "end": 2389,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1358
}
```

```text
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

```

<a id="evidence-0023"></a>

### evidence-0023

```json
{
  "address": "src/devtools/context/planning/docs/overview.md",
  "content_identity": "a679cfa5ee0591036eaab418fa386a0885ef748f98287b8dd49846c093b068bd",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "de0155f1cfe9bdb78fffb3e8897785e5a32f6147ddcd291c3bc7d67f7f9b274a",
  "end": 2836,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1358
}
```

```text
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

```

<a id="evidence-0024"></a>

### evidence-0024

```json
{
  "address": "src/devtools/context/planning/materialization.py",
  "content_identity": "8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8",
  "end": 1014,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 657
}
```

```text
@dataclass(frozen=True, slots=True)
class MaterializedDisclosureItem:
    """Keep rendered information separate from its native supporting value."""

    option_identity: str
    representation: str
    resource_addresses: tuple[RepositoryResourceAddress, ...]
    content_identities: tuple[ContentIdentity, ...]
    text: str
    native_provenance: object
```

<a id="evidence-0025"></a>

### evidence-0025

```json
{
  "address": "src/devtools/context/planning/materialization.py",
  "content_identity": "8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8",
  "end": 2390,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1016
}
```

```text
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
```

<a id="evidence-0026"></a>

### evidence-0026

```json
{
  "address": "src/devtools/context/planning/materialization.py",
  "content_identity": "8c7b2c0dd17e5c8a4f79f3ff48403b92b3ecce5cf4845d85a8723da296cb3315",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e980ecd96c4e962999c8155e2ba0bcce3e438ed4ce00981aede274dc27f34da8",
  "end": 3297,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2392
}
```

```text
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
```

<a id="evidence-0027"></a>

### evidence-0027

```json
{
  "address": "src/devtools/context/planning/plan.py",
  "content_identity": "8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493",
  "end": 1458,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 514
}
```

```text
class PlannedDisclosure(Protocol):
    """One concrete, purpose-bound representation chosen by a caller."""

    @property
    def purpose(self) -> str:
        """Return the information purpose served by this choice."""
        ...

    @property
    def snapshot_id(self) -> RepositorySnapshotId:
        """Return the observed repository state this choice addresses."""
        ...

    @property
    def repository_id(self) -> RepositoryId:
        """Return the nominal repository identity."""
        ...

    @property
    def representation(self) -> str:
        """Name the concrete, implemented disclosure form."""
        ...

    @property
    def identity(self) -> str:
        """Identify this exact disclosure choice and its native support."""
        ...

    def materialize(self, snapshot: RepositorySnapshot) -> MaterializedDisclosureItem:
        """Realize the choice from retained, matching snapshot state."""
        ...
```

<a id="evidence-0028"></a>

### evidence-0028

```json
{
  "address": "src/devtools/context/planning/plan.py",
  "content_identity": "8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493",
  "end": 3377,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1460
}
```

```text
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
```

<a id="evidence-0029"></a>

### evidence-0029

```json
{
  "address": "src/devtools/context/planning/plan.py",
  "content_identity": "8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493",
  "end": 3881,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3379
}
```

```text
def plan_disclosures(
    *,
    purpose: str,
    snapshot: RepositorySnapshot,
    disclosures: tuple[PlannedDisclosure, ...],
    preceding_plan_identity: str | None = None,
) -> DisclosurePlan:
    """Record caller-chosen representations without performing retrieval."""
    return DisclosurePlan(
        purpose=purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        disclosures=disclosures,
        preceding_plan_identity=preceding_plan_identity,
    )
```

<a id="evidence-0030"></a>

### evidence-0030

```json
{
  "address": "src/devtools/context/planning/plan.py",
  "content_identity": "8e1ccfa2286a3bad1f832a2611770b6c655e65ff4c39adde07f9757d47253998",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "09cd96dea039214b6365b48a3142d2f45a44ed8127a418be321022ad89be4493",
  "end": 4128,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3883
}
```

```text
def _digest(*values: str) -> str:
    digest = hashlib.sha256()
    for value in values:
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, "big"))
        digest.update(encoded)
    return digest.hexdigest()
```

<a id="evidence-0031"></a>

### evidence-0031

```json
{
  "address": "src/devtools/context/planning/rendering.py",
  "content_identity": "741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f",
  "end": 2316,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 0
}
```

```text
# Copyright (c) 2026
"""Deterministic presentation of a realized repository disclosure."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import TYPE_CHECKING

from devtools.models.interaction import ModelRequest, Prompt

if TYPE_CHECKING:
    from devtools.context.planning.materialization import ContextDisclosure


@dataclass(frozen=True, slots=True)
class RenderedContextDisclosure:
    """Retain text and the exact realized Context it presents."""

    disclosure: ContextDisclosure
    text: str


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
```

<a id="evidence-0032"></a>

### evidence-0032

```json
{
  "address": "src/devtools/context/planning/rendering.py",
  "content_identity": "741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f",
  "end": 547,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 363
}
```

```text
@dataclass(frozen=True, slots=True)
class RenderedContextDisclosure:
    """Retain text and the exact realized Context it presents."""

    disclosure: ContextDisclosure
    text: str
```

<a id="evidence-0033"></a>

### evidence-0033

```json
{
  "address": "src/devtools/context/planning/rendering.py",
  "content_identity": "741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f",
  "end": 1355,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 549
}
```

```text
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
```

<a id="evidence-0034"></a>

### evidence-0034

```json
{
  "address": "src/devtools/context/planning/rendering.py",
  "content_identity": "741a33e77ec223f64a1b381a156cb25db53473d818bb556432c3b36cbec75ea7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "edf8c256628048ad28d0a4acc1b6f81f2d6945c556922faafa945e0bb786974f",
  "end": 2316,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1357
}
```

```text
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
```

<a id="evidence-0035"></a>

### evidence-0035

```json
{
  "address": "src/devtools/context/planning/resource.py",
  "content_identity": "f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5",
  "end": 3215,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 726
}
```

```text
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
```

<a id="evidence-0036"></a>

### evidence-0036

```json
{
  "address": "src/devtools/context/planning/resource.py",
  "content_identity": "f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5",
  "end": 3819,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3217
}
```

```text
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
```

<a id="evidence-0037"></a>

### evidence-0037

```json
{
  "address": "src/devtools/context/python/classes/containment.py",
  "content_identity": "47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
  "end": 3265,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 845
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonClassMethodContainmentView:
    """Navigate one validated selection without adding duplicate RI facts."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    aggregate: PythonClassMethodAnalysisAggregate

    def module_body_classes_in(
        self,
        resource_address: RepositoryResourceAddress,
    ) -> tuple[PythonClassDeclarationKnowledge, ...]:
        """Return supported direct classes; reject an unselected resource."""
        for analysis in self.aggregate.analyses:
            if analysis.derivation.dependency.resource.address == resource_address:
                return analysis.classes
        msg = "Resource was not selected for class/method analysis."
        raise ValueError(msg)

    def direct_methods_of(
        self,
        class_declaration: PythonClassDeclarationKnowledge,
    ) -> tuple[PythonMethodDeclarationKnowledge, ...]:
        """Return direct methods in class source order, including empty."""
        for analysis in self.aggregate.analyses:
            if class_declaration in analysis.classes:
                return tuple(
                    item
                    for item in analysis.methods
                    if item.containing_class == class_declaration
                )
        msg = "Class declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def containing_class_of(
        self,
        method: PythonMethodDeclarationKnowledge,
    ) -> PythonClassDeclarationKnowledge:
        """Return the method's one established direct lexical parent."""
        for analysis in self.aggregate.analyses:
            if method in analysis.methods:
                return method.containing_class
        msg = "Method declaration does not belong to the selected analyses."
        raise ValueError(msg)

    def occurrence_resource_of(
        self,
        declaration: PythonClassDeclarationKnowledge | PythonMethodDeclarationKnowledge,
    ) -> RepositoryResourceOccurrence:
        """Return where a selected class or method occurs, not its lexical parent."""
        for analysis in self.aggregate.analyses:
            if declaration in analysis.classes or declaration in analysis.methods:
                return analysis.derivation.dependency.resource
        msg = "Declaration does not belong to the selected analyses."
        raise ValueError(msg)
```

<a id="evidence-0038"></a>

### evidence-0038

```json
{
  "address": "src/devtools/context/python/classes/containment.py",
  "content_identity": "47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
  "end": 8249,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3267
}
```

```text
def build_python_class_method_containment_view(  # noqa: C901
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonClassMethodAnalysisAggregate,
) -> PythonClassMethodContainmentView:
    """Check native facts against the same retained observed snapshot."""
    if not aggregate.analyses:
        msg = "Class/method containment requires at least one resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Class/method containment repeats a resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Class/method analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Class/method analysis uses stale observed resource content."
            raise ValueError(msg)
        coverage = analysis.coverage
        if (
            coverage.derivation_identity != derivation.identity
            or coverage.class_count != len(analysis.classes)
            or coverage.method_count != len(analysis.methods)
            or coverage.excluded_class_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in analysis.excluded_syntax
            )
            or coverage.excluded_function_count
            != sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
                for item in analysis.excluded_syntax
            )
        ):
            msg = "Class/method coverage differs from its analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.classes):
            class_subject = declaration.subject
            if (
                declaration.derivation_identity != derivation.identity
                or class_subject.snapshot_id != snapshot.id
                or class_subject.resource_dependency_identity != dependency.identity
                or class_subject.derivation_definition_identity
                != derivation.definition.identity
                or class_subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
                or any(
                    base.ordinal != base_ordinal
                    or base.occurrence.snapshot_id != snapshot.id
                    or base.occurrence.resource_address != address
                    for base_ordinal, base in enumerate(declaration.base_syntax)
                )
            ):
                msg = "Class declaration differs from its resource analysis."
                raise ValueError(msg)
        method_ordinals: dict[str, int] = {}
        for method in analysis.methods:
            parent = method.containing_class
            ordinal = method_ordinals.get(parent.subject.identity, 0)
            method_subject = method.subject
            if (
                parent not in analysis.classes
                or method.derivation_identity != derivation.identity
                or method_subject.snapshot_id != snapshot.id
                or method_subject.resource_dependency_identity != dependency.identity
                or method_subject.derivation_definition_identity
                != derivation.definition.identity
                or method_subject.containing_class_subject_identity
                != parent.subject.identity
                or method_subject.declaration_ordinal != ordinal
                or method.support.snapshot_id != snapshot.id
                or method.support.resource_address != address
            ):
                msg = "Method declaration differs from its class or resource."
                raise ValueError(msg)
            method_ordinals[parent.subject.identity] = ordinal + 1
        if any(
            item.occurrence.snapshot_id != snapshot.id
            or item.occurrence.resource_address != address
            for item in analysis.excluded_syntax
        ):
            msg = "Excluded syntax differs from its observed resource."
            raise ValueError(msg)
    return PythonClassMethodContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
```

<a id="evidence-0039"></a>

### evidence-0039

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 1938,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 950
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonClassMethodDerivationDefinition:
    """Identify the parser and the bounded class/method traversal contract."""

    analyzer_semantics_version: str
    parser_implementation: str
    parser_runtime_version: str
    grammar_feature_version: tuple[int, int]

    TRAVERSAL_SEMANTICS: ClassVar[str] = "module-class-direct-method-v1"
    NODE_VOCABULARY: ClassVar[tuple[str, str, str]] = (
        "ast.ClassDef",
        "ast.FunctionDef",
        "ast.AsyncFunctionDef",
    )

    @property
    def identity(self) -> str:
        """Bind every result-affecting definition setting."""
        return _digest(
            "python-class-method-definition-v1",
            self.analyzer_semantics_version,
            self.parser_implementation,
            self.parser_runtime_version,
            ".".join(str(part) for part in self.grammar_feature_version),
            self.TRAVERSAL_SEMANTICS,
            *self.NODE_VOCABULARY,
        )
```

<a id="evidence-0040"></a>

### evidence-0040

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 3196,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2463
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonClassSubject:
    """Identify one direct module-body class structurally, not at runtime."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-module-body-class"

    @property
    def identity(self) -> str:
        """Distinguish repeated names and classes in different resources."""
        return _digest(
            "python-class-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
```

<a id="evidence-0041"></a>

### evidence-0041

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 4026,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3198
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonMethodSubject:
    """Identify one direct method under a particular class subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    derivation_definition_identity: str
    containing_class_subject_identity: str
    declaration_ordinal: int

    KIND: ClassVar[str] = "python-direct-class-body-method"

    @property
    def identity(self) -> str:
        """Use structural parent and ordinal, never a bare method name."""
        return _digest(
            "python-method-subject-v1",
            str(self.snapshot_id),
            self.resource_dependency_identity,
            self.derivation_definition_identity,
            self.containing_class_subject_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
```

<a id="evidence-0042"></a>

### evidence-0042

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 6519,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5472
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonMethodDeclarationKnowledge:
    """Assert a direct class-body function syntax with one lexical parent."""

    derivation_identity: str
    subject: PythonMethodSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind
    containing_class: PythonClassDeclarationKnowledge

    PROPOSITION: ClassVar[str] = "direct-class-body-functiondef-declares-method-subject"

    @property
    def identity(self) -> str:
        """Identify this method occurrence and its direct class parent."""
        return _digest(
            "python-method-declaration-knowledge-v1",
            self.PROPOSITION,
            self.derivation_identity,
            self.subject.identity,
            self.containing_class.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            *_range_values(self.support.source_range),
            self.declared_name,
            self.declaration_kind.value,
        )
```

<a id="evidence-0043"></a>

### evidence-0043

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 14928,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 9219
}
```

```text
def derive_python_class_method_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonClassMethodAnalysis:
    """Derive only direct module classes and their direct sync/async methods."""
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = PythonClassMethodDerivationDefinition(
        analyzer_semantics_version=_ANALYZER_SEMANTICS_VERSION,
        parser_implementation=sys.implementation.name,
        parser_runtime_version=platform.python_version(),
        grammar_feature_version=_GRAMMAR_FEATURE_VERSION,
    )
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonClassMethodDerivation(definition, dependency)
    try:
        module = ast.parse(
            resource.content,
            filename=str(resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonClassMethodParseError(derivation, error) from error

    classes: list[PythonClassDeclarationKnowledge] = []
    methods: list[PythonMethodDeclarationKnowledge] = []
    supported_nodes: set[int] = set()
    module_functions: set[int] = set()
    for node in module.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            module_functions.add(id(node))
        if not isinstance(node, ast.ClassDef):
            continue
        supported_nodes.add(id(node))
        subject = PythonClassSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            derivation_definition_identity=definition.identity,
            declaration_ordinal=len(classes),
        )
        declaration = PythonClassDeclarationKnowledge(
            derivation_identity=derivation.identity,
            subject=subject,
            support=_occurrence(snapshot.id, resource.address, node),
            declared_name=node.name,
            base_syntax=tuple(
                PythonClassBaseSyntax(
                    ordinal=ordinal,
                    occurrence=_occurrence(snapshot.id, resource.address, base),
                    source_text=_base_source_text(resource.content, base),
                )
                for ordinal, base in enumerate(node.bases)
            ),
        )
        classes.append(declaration)
        method_ordinal = 0
        for child in node.body:
            if not isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            supported_nodes.add(id(child))
            method_subject = PythonMethodSubject(
                snapshot_id=snapshot.id,
                resource_dependency_identity=dependency.identity,
                derivation_definition_identity=definition.identity,
                containing_class_subject_identity=subject.identity,
                declaration_ordinal=method_ordinal,
            )
            methods.append(
                PythonMethodDeclarationKnowledge(
                    derivation_identity=derivation.identity,
                    subject=method_subject,
                    support=_occurrence(snapshot.id, resource.address, child),
                    declared_name=child.name,
                    declaration_kind=(
                        PythonFunctionDeclarationKind.ASYNCHRONOUS
                        if isinstance(child, ast.AsyncFunctionDef)
                        else PythonFunctionDeclarationKind.SYNCHRONOUS
                    ),
                    containing_class=declaration,
                ),
            )
            method_ordinal += 1

    excluded_function_kind = (
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS
    )
    excluded = tuple(
        sorted(
            (
                PythonExcludedClassMethodSyntax(
                    kind=(
                        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                        if isinstance(node, ast.ClassDef)
                        else excluded_function_kind
                    ),
                    occurrence=_occurrence(snapshot.id, resource.address, node),
                )
                for node in ast.walk(module)
                if isinstance(
                    node,
                    (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
                )
                and id(node) not in supported_nodes
                and id(node) not in module_functions
            ),
            key=lambda item: (
                item.occurrence.source_range.start_line,
                item.occurrence.source_range.start_column_utf8,
                item.kind.value,
            ),
        ),
    )
    return PythonClassMethodAnalysis(
        derivation=derivation,
        classes=tuple(classes),
        methods=tuple(methods),
        excluded_syntax=excluded,
        coverage=PythonClassMethodCoverage(
            derivation_identity=derivation.identity,
            class_count=len(classes),
            method_count=len(methods),
            module_body_function_count=len(module_functions),
            excluded_class_count=sum(
                item.kind
                is PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY
                for item in excluded
            ),
            excluded_function_count=sum(
                item.kind is excluded_function_kind for item in excluded
            ),
        ),
    )
```

<a id="evidence-0044"></a>

### evidence-0044

```json
{
  "address": "src/devtools/context/python/classes/declarations.py",
  "content_identity": "f283a78b7bebb29f155653b03f47be9f0d74f55593b30a3e4b2f552c91cf4a73",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b38664916a128ac4e218cfd4adb4c1070e79618c68930eefc3b1eba8d70cabbd",
  "end": 16381,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 15808
}
```

```text
def _occurrence(
    snapshot_id: RepositorySnapshotId,
    resource_address: RepositoryResourceAddress,
    node: ast.AST,
) -> PythonSourceOccurrence:
    located = cast("_LocatedAstNode", node)
    return PythonSourceOccurrence(
        snapshot_id=snapshot_id,
        resource_address=resource_address,
        source_range=PythonSourceRange(
            start_line=located.lineno,
            start_column_utf8=located.col_offset,
            end_line=cast("int", located.end_lineno),
            end_column_utf8=cast("int", located.end_col_offset),
        ),
    )
```

<a id="evidence-0045"></a>

### evidence-0045

```json
{
  "address": "src/devtools/context/python/classes/docs/overview.md",
  "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
  "end": 4683,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1112
}
```

````text
## Identity, provenance, and containment

The class subject identity depends on parser/derivation definition, snapshot,
the exact observed resource/content dependency, and class ordinal among direct
module-body classes. A method subject also depends on its containing class
subject and ordinal among that class's direct methods. Names are retained for
display and exact syntax knowledge, never used alone as subject identity. These
are structural repository subjects, not runtime Python `__qualname__` values.

Every class and method retains an exact source occurrence with one-based lines
and zero-based UTF-8 byte columns. The per-resource derivation retains its
repository and snapshot identities, content-bearing observed resource, parser
version, and bounded traversal semantics. A class retains the exact occurrence
and source text of each direct base expression as **syntax**. A separate
derivation assesses possible repository class targets without changing the
original declaration.
AST declaration spans begin at `class`/`def`/`async def`, excluding preceding
decorator lines. Decorators do not erase class or direct method declaration knowledge and do
not classify descriptor or runtime behavior. Exact source grounding may select
these native subjects even for staticmethod, classmethod or arbitrary method
decorators. Subject identity does not identify the runtime object after
decorators, descriptors, metaclass behavior or rebinding; binding-oriented
Reference/base checks retain their separate conservative semantics.

```text
method occurrence resource ──→ observed module resource
method direct lexical parent ──→ class declaration
class occurrence resource  ──→ observed module resource
class direct lexical parent ──→ Module.body scope (bounded analysis claim)
```

`PythonMethodDeclarationKnowledge.containing_class` is the one canonical direct
lexical-parent link. Both directions navigate it; no reverse fact is derived.
`build_python_class_method_containment_view(snapshot, aggregate=...)` validates
native analyses against the retained snapshot without reparsing or file reads.
It exposes `module_body_classes_in(address)`, `direct_methods_of(class)`,
`containing_class_of(method)`, and `occurrence_resource_of(class_or_method)`.
An analyzed resource or class can return an empty tuple. An unselected resource
or declaration raises an error rather than implying absence.

Successful coverage counts supported classes/methods, separately counted
module-body functions handled by existing function RI, and encountered class
or function syntax outside this analysis's positive scope. Excluded occurrences
retain exact source locations. Syntax failure publishes no successful coverage.
Local classes, nested classes, nested functions, methods of excluded classes,
and indirect declarations under control-flow statements are not positive facts.
Absence in this bounded result says nothing about runtime classes or methods.

Repository Intelligence records this structure. Retrieval may later decide
whether it is relevant to an InformationNeed. Context Planning may later choose
a class or method representation for disclosure. Neither decision is made here.
The current qualified Reference/direct Call analyzer still resolves only its
existing imported-function forms. Future method References/Calls need separate
qualified attribute and receiver/type resolution. The current resource-level
Personalized PageRank graph does not consume these new facts. A future graph
view may project class, method, base, and Reference relationships prospectively.

````

<a id="evidence-0046"></a>

### evidence-0046

```json
{
  "address": "src/devtools/context/python/classes/docs/overview.md",
  "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
  "end": 2104,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1623
}
```

```text
Every class and method retains an exact source occurrence with one-based lines
and zero-based UTF-8 byte columns. The per-resource derivation retains its
repository and snapshot identities, content-bearing observed resource, parser
version, and bounded traversal semantics. A class retains the exact occurrence
and source text of each direct base expression as **syntax**. A separate
derivation assesses possible repository class targets without changing the
original declaration.
```

<a id="evidence-0047"></a>

### evidence-0047

```json
{
  "address": "src/devtools/context/python/classes/docs/overview.md",
  "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
  "end": 2647,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2104
}
```

```text
AST declaration spans begin at `class`/`def`/`async def`, excluding preceding
decorator lines. Decorators do not erase class or direct method declaration knowledge and do
not classify descriptor or runtime behavior. Exact source grounding may select
these native subjects even for staticmethod, classmethod or arbitrary method
decorators. Subject identity does not identify the runtime object after
decorators, descriptors, metaclass behavior or rebinding; binding-oriented
Reference/base checks retain their separate conservative semantics.

```

<a id="evidence-0048"></a>

### evidence-0048

```json
{
  "address": "src/devtools/context/python/classes/docs/overview.md",
  "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
  "end": 3509,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2898
}
```

```text
`PythonMethodDeclarationKnowledge.containing_class` is the one canonical direct
lexical-parent link. Both directions navigate it; no reverse fact is derived.
`build_python_class_method_containment_view(snapshot, aggregate=...)` validates
native analyses against the retained snapshot without reparsing or file reads.
It exposes `module_body_classes_in(address)`, `direct_methods_of(class)`,
`containing_class_of(method)`, and `occurrence_resource_of(class_or_method)`.
An analyzed resource or class can return an empty tuple. An unselected resource
or declaration raises an error rather than implying absence.

```

<a id="evidence-0049"></a>

### evidence-0049

```json
{
  "address": "src/devtools/context/python/function/containment.py",
  "content_identity": "7af4524a28e61dc608e35c9ab4ff34c0bc486fb1ef54a3521f9fb0735eb25d69",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
  "end": 5195,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2332
}
```

```text
def build_python_function_declaration_containment_view(
    snapshot: RepositorySnapshot,
    *,
    aggregate: PythonFunctionDeclarationAnalysisAggregate,
) -> PythonFunctionDeclarationContainmentView:
    """Validate native analyses against retained state and expose navigation.

    This validation checks provenance consistency without reparsing source or
    introducing an independently identified ownership relationship.
    """
    if not aggregate.analyses:
        msg = "Containment requires at least one selected resource analysis."
        raise ValueError(msg)
    seen_addresses: set[RepositoryResourceAddress] = set()
    for analysis in aggregate.analyses:
        derivation = analysis.derivation
        dependency = derivation.dependency
        address = dependency.resource.address
        if address in seen_addresses:
            msg = "Containment repeats a selected resource analysis."
            raise ValueError(msg)
        seen_addresses.add(address)
        if (
            dependency.repository_id != snapshot.repository_id
            or dependency.snapshot_id != snapshot.id
        ):
            msg = "Declaration analysis belongs to another repository snapshot."
            raise ValueError(msg)
        try:
            observed = snapshot.resource_at(address)
        except ValueError as error:
            msg = "Analyzed resource is absent from the supplied snapshot."
            raise ValueError(msg) from error
        if observed != dependency.resource:
            msg = "Declaration analysis uses stale observed resource content."
            raise ValueError(msg)
        if (
            analysis.coverage.derivation_identity != derivation.identity
            or analysis.coverage.declaration_count != len(analysis.declarations)
        ):
            msg = "Declaration coverage differs from its retained analysis."
            raise ValueError(msg)
        for ordinal, declaration in enumerate(analysis.declarations):
            if (
                declaration.derivation_identity != derivation.identity
                or declaration.subject.snapshot_id != snapshot.id
                or declaration.subject.resource_dependency_identity
                != dependency.identity
                or declaration.subject.derivation_definition_identity
                != derivation.definition.identity
                or declaration.subject.declaration_ordinal != ordinal
                or declaration.support.snapshot_id != snapshot.id
                or declaration.support.resource_address != address
            ):
                msg = "Declaration differs from its resource analysis or support."
                raise ValueError(msg)
    return PythonFunctionDeclarationContainmentView(
        repository_id=snapshot.repository_id,
        snapshot_id=snapshot.id,
        aggregate=aggregate,
    )
```

<a id="evidence-0050"></a>

### evidence-0050

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 2058,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1628
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonSourceRange:
    """Locate Python syntax using the stdlib AST coordinate contract.

    Lines are one-based. Columns are zero-based UTF-8 byte offsets. The end
    position is exclusive. This is a local Python-parser coordinate value, not
    a universal source-location convention.
    """

    start_line: int
    start_column_utf8: int
    end_line: int
    end_column_utf8: int
```

<a id="evidence-0051"></a>

### evidence-0051

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 2963,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2324
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonModuleResourceDependency:
    """Retain the exact observed module resource consumed by a derivation."""

    snapshot_id: RepositorySnapshotId
    repository_id: RepositoryId
    resource: RepositoryResourceOccurrence

    @property
    def identity(self) -> str:
        """Return the deterministic identity of this direct semantic input."""
        return _semantic_digest(
            _DEPENDENCY_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
        )
```

<a id="evidence-0052"></a>

### evidence-0052

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 4152,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2965
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationDerivationDefinition:
    """Identify the reusable semantics of the bounded declaration analysis."""

    analyzer_semantics_version: str
    parser_implementation: str
    parser_runtime_version: str
    grammar_feature_version: tuple[int, int]

    TRAVERSAL_SEMANTICS: ClassVar[str] = "direct-ast-module-body-only-v1"
    NODE_VOCABULARY: ClassVar[tuple[str, str]] = (
        "ast.FunctionDef",
        "ast.AsyncFunctionDef",
    )
    PROPOSITION: ClassVar[str] = (
        "direct-module-body-python-function-source-occurrence-"
        "syntactically-declares-snapshot-local-function-subject"
    )

    @property
    def identity(self) -> str:
        """Return identity for all result-affecting definition semantics."""
        return _semantic_digest(
            _DEFINITION_IDENTITY_SEMANTICS,
            self.analyzer_semantics_version,
            self.parser_implementation,
            self.parser_runtime_version,
            ".".join(str(part) for part in self.grammar_feature_version),
            self.TRAVERSAL_SEMANTICS,
            *self.NODE_VOCABULARY,
            self.PROPOSITION,
        )
```

<a id="evidence-0053"></a>

### evidence-0053

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 5448,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4705
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonFunctionSubject:
    """Represent one analyzer-established snapshot-local function subject."""

    snapshot_id: RepositorySnapshotId
    resource_dependency_identity: str
    declaration_ordinal: int
    derivation_definition_identity: str

    KIND: ClassVar[str] = "python-function"

    @property
    def identity(self) -> str:
        """Return a reproducible identity distinct from name and source range."""
        return _semantic_digest(
            _SUBJECT_IDENTITY_SEMANTICS,
            str(self.snapshot_id),
            self.derivation_definition_identity,
            self.resource_dependency_identity,
            self.KIND,
            str(self.declaration_ordinal),
        )
```

<a id="evidence-0054"></a>

### evidence-0054

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 6597,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5450
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonFunctionDeclarationKnowledge:
    """Assert that one direct declaration occurrence declares one subject."""

    derivation_identity: str
    subject: PythonFunctionSubject
    support: PythonSourceOccurrence
    declared_name: str
    declaration_kind: PythonFunctionDeclarationKind

    PROPOSITION: ClassVar[str] = (
        PythonFunctionDeclarationDerivationDefinition.PROPOSITION
    )

    @property
    def identity(self) -> str:
        """Return reproducible identity for this separately referable result."""
        source_range = self.support.source_range
        return _semantic_digest(
            _KNOWLEDGE_IDENTITY_SEMANTICS,
            self.derivation_identity,
            self.subject.identity,
            str(self.support.snapshot_id),
            str(self.support.resource_address),
            str(source_range.start_line),
            str(source_range.start_column_utf8),
            str(source_range.end_line),
            str(source_range.end_column_utf8),
            self.declared_name,
            self.declaration_kind.value,
            self.PROPOSITION,
        )
```

<a id="evidence-0055"></a>

### evidence-0055

```json
{
  "address": "src/devtools/context/python/function/declarations.py",
  "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
  "end": 11870,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 8627
}
```

```text
def derive_python_function_declarations(
    snapshot: RepositorySnapshot,
    *,
    resource_address: RepositoryResourceAddress | None = None,
) -> PythonFunctionDeclarationAnalysis:
    """Derive declarations from one explicitly selected observed resource.

    A returned value accounts exhaustively for the bounded declaration scope.
    A syntax failure raises :class:`PythonModuleParseError` and returns no
    coverage or declaration knowledge. Omitting ``resource_address`` is a
    compatibility path valid only for a snapshot containing exactly one
    resource.
    """
    resource = (
        snapshot.resource
        if resource_address is None
        else snapshot.resource_at(resource_address)
    )
    definition = _current_definition()
    dependency = PythonModuleResourceDependency(
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        resource=resource,
    )
    derivation = PythonFunctionDeclarationDerivation(
        definition=definition,
        dependency=dependency,
    )
    try:
        module = ast.parse(
            dependency.resource.content,
            filename=str(dependency.resource.address),
            mode="exec",
            type_comments=False,
            feature_version=definition.grammar_feature_version,
        )
    except SyntaxError as error:
        raise PythonModuleParseError(derivation=derivation, error=error) from error

    declarations: list[PythonFunctionDeclarationKnowledge] = []
    for node in module.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        declaration_ordinal = len(declarations)
        subject = PythonFunctionSubject(
            snapshot_id=snapshot.id,
            resource_dependency_identity=dependency.identity,
            declaration_ordinal=declaration_ordinal,
            derivation_definition_identity=definition.identity,
        )
        source_occurrence = PythonSourceOccurrence(
            snapshot_id=snapshot.id,
            resource_address=dependency.resource.address,
            source_range=PythonSourceRange(
                start_line=node.lineno,
                start_column_utf8=node.col_offset,
                end_line=cast("int", node.end_lineno),
                end_column_utf8=cast("int", node.end_col_offset),
            ),
        )
        declaration_kind = (
            PythonFunctionDeclarationKind.ASYNCHRONOUS
            if isinstance(node, ast.AsyncFunctionDef)
            else PythonFunctionDeclarationKind.SYNCHRONOUS
        )
        declarations.append(
            PythonFunctionDeclarationKnowledge(
                derivation_identity=derivation.identity,
                subject=subject,
                support=source_occurrence,
                declared_name=node.name,
                declaration_kind=declaration_kind,
            ),
        )

    immutable_declarations = tuple(declarations)
    return PythonFunctionDeclarationAnalysis(
        derivation=derivation,
        declarations=immutable_declarations,
        coverage=PythonFunctionDeclarationCoverage(
            derivation_identity=derivation.identity,
            declaration_count=len(immutable_declarations),
        ),
    )
```

<a id="evidence-0056"></a>

### evidence-0056

```json
{
  "address": "src/devtools/context/python/function/docs/overview.md",
  "content_identity": "6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
  "end": 3292,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 493
}
```

````text
## Direct declaration containment

Declaration ownership was already intrinsic to production knowledge: each
`PythonFunctionDeclarationKnowledge` retains an exact source occurrence with
the resource address and span, while its subject binds to the derivation's
observed resource dependency. This increment adds a validated navigation view,
not a second `ResourceOwnsFunction` fact. Build
`PythonFunctionDeclarationContainmentView` with
`build_python_function_declaration_containment_view(snapshot, aggregate=...)`
over existing per-resource analyses. The builder checks repository, snapshot,
observed resource/content, derivation, coverage, subject, ordinal, and support
consistency without reparsing or reopening the working tree.

`direct_declarations_in(address)` returns the supported direct module-body
function and async-function declarations in source order; an analyzed resource
with none returns an empty tuple. An address absent from the selected analyses
raises an error because that selection cannot establish absence.
`containing_resource_of(declaration)` returns the exact observed resource for
a declaration in the analyses. The two directions navigate one existing
declaration proposition. Each analysis retains its own derivation and bounded
exhaustive coverage; the view creates no aggregate derivation or new identity.

```text
observed resource
  ├── direct module-body FunctionDef
  └── direct module-body AsyncFunctionDef
```

Decorated direct FunctionDef and AsyncFunctionDef have the same supported
source-declaration status as plain declarations. The exact source selector in
[modules](../../modules/docs/overview.md#exact-source-declaration-selection)
retains native identities and provenance without establishing post-decoration
binding values, imported object identity or callability.

The occurrence belongs to the resource and is directly in `Module.body` under
the current parser contract. This says nothing about runtime ownership,
importability, public API status, usefulness, or graph importance. Class,
method, nested-function, lambda, and assignment declarations are outside this
contract. A later class/method model can distinguish occurrence resource from
direct lexical parent declaration without changing this view's narrow claim.

Repository Intelligence answers which supported declaration is structurally
contained where. Retrieval decides whether that structure is evidence relevant
to an InformationNeed. Context Planning decides which declaration or resource
information to disclose. The current qualified-reference Context materializer
already uses the declaration's exact resource dependency and source span; it
does not need a new ownership fact. This view is not automatically projected
into the current resource-level Personalized PageRank graph.

````

<a id="evidence-0057"></a>

### evidence-0057

```json
{
  "address": "src/devtools/context/python/function/docs/overview.md",
  "content_identity": "6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
  "end": 5665,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5225
}
```

```text
choose_python_qualified_reference_disclosure now adapts this same validated
path to the common
[DisclosurePlan](../../../planning/docs/overview.md) boundary. A caller can
place it beside other explicit representations, including a retained whole
resource. The adapter calls the existing materializer and renderer; it does
not weaken their snapshot, content, or Reference/Call semantics. The original
narrow API remains available unchanged.
```

<a id="evidence-0058"></a>

### evidence-0058

```json
{
  "address": "src/devtools/context/python/function/materialization.py",
  "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
  "end": 4784,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3649
}
```

```text
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
```

<a id="evidence-0059"></a>

### evidence-0059

```json
{
  "address": "src/devtools/context/python/function/materialization.py",
  "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
  "end": 5535,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4786
}
```

```text
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
```

<a id="evidence-0060"></a>

### evidence-0060

```json
{
  "address": "src/devtools/context/python/function/planned_reference.py",
  "content_identity": "a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0e85d7f5109d5129516027b53f9a466471a2317aded85a7d7e7761777a94b701",
  "end": 2898,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 891
}
```

```text
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
```

<a id="evidence-0061"></a>

### evidence-0061

```json
{
  "address": "src/devtools/context/python/function/planned_reference.py",
  "content_identity": "a1e96fb89604e70bc163fa267a3a53a03ed24515ce4b00d421d1f0dda5d17381",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "0e85d7f5109d5129516027b53f9a466471a2317aded85a7d7e7761777a94b701",
  "end": 3410,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2900
}
```

```text
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
```

<a id="evidence-0062"></a>

### evidence-0062

```json
{
  "address": "src/devtools/context/python/function/qualified_reference.py",
  "content_identity": "f38207363dcef35c196eac7dd5ab939335e73a9aec507886af7bbdcee7008c69",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e9818d20ebf2bf2abdb3e49ac8b43398512fcb0d90e5736e7b9d60c4ce28fdb3",
  "end": 4323,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3053
}
```

```text
def disclose_python_qualified_reference(
    *,
    purpose: str,
    analysis: PythonDeclarationReferenceAnalysis,
    reference: PythonDeclarationReferenceKnowledge,
) -> PythonQualifiedReferenceDisclosure:
    """Fix one caller-chosen fact; do not search for or choose another fact."""
    if not purpose.strip():
        msg = "Qualified reference disclosure purpose must not be blank."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if (
        reference.derivation_identity != analysis.derivation.identity
        or analysis.coverage.derivation_identity != analysis.derivation.identity
        or reference not in analysis.references
    ):
        msg = "Selected reference does not belong to the supplied analysis."
        raise PythonQualifiedReferenceDisclosureError(msg)
    if not isinstance(
        reference.target_declaration,
        PythonFunctionDeclarationKnowledge,
    ) or reference.route not in {
        PythonDeclarationReferenceRoute.IMPORTED_MEMBER,
        PythonDeclarationReferenceRoute.ONE_FACADE,
    }:
        msg = "Qualified function Context requires an imported function Name."
        raise PythonQualifiedReferenceDisclosureError(msg)
    return PythonQualifiedReferenceDisclosure(purpose, analysis, reference)
```

<a id="evidence-0063"></a>

### evidence-0063

```json
{
  "address": "src/devtools/context/python/function/qualified_reference.py",
  "content_identity": "f38207363dcef35c196eac7dd5ab939335e73a9aec507886af7bbdcee7008c69",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e9818d20ebf2bf2abdb3e49ac8b43398512fcb0d90e5736e7b9d60c4ce28fdb3",
  "end": 9062,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4325
}
```

```text
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
```

<a id="evidence-0064"></a>

### evidence-0064

```json
{
  "address": "src/devtools/context/python/function/request_assembly.py",
  "content_identity": "27bfd8eb7c177577cc410c7e19c47cd8724a6b93200dd15e2ac8d55d4bb4d152",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "d0683bff077bc951cd4f02a215e96323dbb4ed78587cbcddd9a12df9ec0b9c8a",
  "end": 1689,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 678
}
```

```text
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
```

<a id="evidence-0065"></a>

### evidence-0065

```json
{
  "address": "src/devtools/context/python/modules/declarations.py",
  "content_identity": "e54171b465bb78a21c1c380321d1f04f69771982db02f4cd1b140b36423283be",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "e2cc21c89da653801bf7f0ac37d116e358f959b729b7fcb941fc483bbca7dd3a",
  "end": 6980,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2281
}
```

```text
def lookup_python_module_declaration(  # noqa: C901, PLR0912, PLR0915
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
) -> PythonModuleDeclarationLookup:
    """Resolve only one unique undecorated direct declaration binding.

    Competing, nested, wildcard, and dynamic bindings do not establish a
    target. This is static repository syntax, never runtime attribute lookup.
    """
    if not declared_name.isidentifier():
        msg = "Direct member name must be a Python identifier."
        raise ValueError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Direct member module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    tree = ast.parse(module.resource.content, filename=str(address))
    candidates: list[PythonDirectModuleDeclaration | None] = []
    uncertain = False
    for node in tree.body:
        if isinstance(node, ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef):
            if node.name == declared_name:
                if node.decorator_list:
                    candidates.append(None)
                elif isinstance(node, ast.ClassDef):
                    candidates.extend(
                        item
                        for item in classes.classes
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
                else:
                    candidates.extend(
                        item
                        for item in functions.declarations
                        if item.support.source_range.start_line == node.lineno
                        and item.support.source_range.start_column_utf8
                        == node.col_offset
                    )
            continue
        if isinstance(node, ast.Import | ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    uncertain = True
                elif (
                    alias.asname
                    or (
                        alias.name
                        if isinstance(node, ast.ImportFrom)
                        else alias.name.split(".")[0]
                    )
                ) == declared_name:
                    candidates.append(None)
            continue
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(
                child.ctx,
                ast.Store | ast.Del,
            ):
                if child.id == declared_name:
                    candidates.append(None)
            elif isinstance(
                child,
                ast.ClassDef | ast.FunctionDef | ast.AsyncFunctionDef,
            ):
                if child.name == declared_name:
                    candidates.append(None)
            elif isinstance(child, ast.Import | ast.ImportFrom):
                for alias in child.names:
                    if alias.name == "*":
                        uncertain = True
                    elif (
                        alias.asname
                        or (
                            alias.name
                            if isinstance(child, ast.ImportFrom)
                            else alias.name.split(".")[0]
                        )
                    ) == declared_name:
                        candidates.append(None)
    if any(
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id in {"exec", "globals", "locals"}
        for node in ast.walk(tree)
    ):
        uncertain = True
    if uncertain or len(candidates) > 1:
        outcome = PythonModuleDeclarationLookupOutcome.AMBIGUOUS
        target = None
    elif not candidates:
        outcome = PythonModuleDeclarationLookupOutcome.UNRESOLVED
        target = None
    elif candidates[0] is None:
        outcome = PythonModuleDeclarationLookupOutcome.NOT_DECLARATION
        target = None
    else:
        outcome = PythonModuleDeclarationLookupOutcome.RESOLVED
        target = candidates[0]
    return PythonModuleDeclarationLookup(
        module,
        declared_name,
        functions,
        classes,
        outcome,
        target,
    )
```

<a id="evidence-0066"></a>

### evidence-0066

```json
{
  "address": "src/devtools/context/python/modules/docs/overview.md",
  "content_identity": "fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
  "end": 4038,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3335
}
```

```text
## Exact source declaration selection

`modules.selection.select_python_module_source_declarations` answers which
native direct source declarations match this exact interpreted module,
`PythonSourceDeclarationKind` (CLASS or FUNCTION), and identifier name.
It validates repository/snapshot/resource state and consumes canonical class
and function declaration RI, with no parallel parser or binding-policy flag.
`PythonModuleSourceDeclarationSelection` retains the module, name/kind, both
native analyses (derivation, dependencies and coverage), and all matching native
knowledge values. Its `SEMANTICS` identifies this operation. It introduces no
new declaration subject or persistence representation.

```

<a id="evidence-0067"></a>

### evidence-0067

```json
{
  "address": "src/devtools/context/python/modules/docs/overview.md",
  "content_identity": "fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
  "end": 5043,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3335
}
```

```text
## Exact source declaration selection

`modules.selection.select_python_module_source_declarations` answers which
native direct source declarations match this exact interpreted module,
`PythonSourceDeclarationKind` (CLASS or FUNCTION), and identifier name.
It validates repository/snapshot/resource state and consumes canonical class
and function declaration RI, with no parallel parser or binding-policy flag.
`PythonModuleSourceDeclarationSelection` retains the module, name/kind, both
native analyses (derivation, dependencies and coverage), and all matching native
knowledge values. Its `SEMANTICS` identifies this operation. It introduces no
new declaration subject or persistence representation.

Direct decorated ClassDef, FunctionDef and AsyncFunctionDef remain source
facts. Rebinding, assignments, imports and dynamic namespace syntax do not
erase those facts or create additional direct source declarations. Repeated
same-kind names have distinct native subjects and are all retained; source
order is never a uniqueness rule. Kind mismatch and no supported direct syntax
return no matches, including nested/control-flow declarations outside RI scope.
A native parse failure propagates without positive facts or successful coverage.

This selection establishes static repository/source declaration identity only.
It does not establish the module attribute or imported object after decorators,
descriptors, metaclass behavior or rebinding, public exports, callability or
runtime importability. Binding-oriented References and class-base resolution
continue using `lookup_python_module_declaration` with its unchanged guards.
Localization exact declaration grounding consumes this source selection.

```

<a id="evidence-0068"></a>

### evidence-0068

```json
{
  "address": "src/devtools/context/python/modules/interpretation.py",
  "content_identity": "b858bbdd8ea4d0a8e9a3193ae29176947ef0796f949025a6bf3866ea7caf9dbd",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "54ffd27dd2b175d1f12987c030f3ec13b4718f6237127bcdd7163f838f12e15b",
  "end": 3092,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2286
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonModuleInterpretation:
    """One exact resource's module interpretation under an explicit root."""

    repository_id: RepositoryId
    snapshot_id: RepositorySnapshotId
    resource: RepositoryResourceOccurrence
    module_root: PythonModuleRoot
    dotted_name: str
    kind: PythonModuleKind

    SEMANTICS: ClassVar[str] = _INTERPRETATION_SEMANTICS

    @property
    def identity(self) -> str:
        """Identify this interpretation from its actual semantic inputs."""
        return _digest(
            self.SEMANTICS,
            str(self.repository_id),
            str(self.resource.address),
            str(self.resource.content_identity),
            self.module_root.value,
            self.dotted_name,
            self.kind.value,
        )
```

<a id="evidence-0069"></a>

### evidence-0069

```json
{
  "address": "src/devtools/context/python/modules/selection.py",
  "content_identity": "8017f8d2153eb217b57cee49b78841073b752e675539254d54c13a6979eadc6f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f9a7943390f82d8e1399edaa66aebd172b43ad5a85838285c134ec03f5ad89af",
  "end": 1663,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 987
}
```

```text
@dataclass(frozen=True, slots=True)
class PythonModuleSourceDeclarationSelection:
    """Retain all exact source matches and their native analysis provenance.

    Declaration subjects are static source identities. This result establishes
    neither post-decoration binding values nor runtime/import object identity.
    """

    module: PythonModuleInterpretation
    declared_name: str
    kind: PythonSourceDeclarationKind
    function_analysis: PythonFunctionDeclarationAnalysis
    class_analysis: PythonClassMethodAnalysis
    declarations: tuple[PythonDirectModuleDeclaration, ...]

    SEMANTICS: ClassVar[str] = "exact-python-module-source-declaration-selection-v1"
```

<a id="evidence-0070"></a>

### evidence-0070

```json
{
  "address": "src/devtools/context/python/modules/selection.py",
  "content_identity": "8017f8d2153eb217b57cee49b78841073b752e675539254d54c13a6979eadc6f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "f9a7943390f82d8e1399edaa66aebd172b43ad5a85838285c134ec03f5ad89af",
  "end": 3471,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1665
}
```

```text
def select_python_module_source_declarations(
    snapshot: RepositorySnapshot,
    *,
    module: PythonModuleInterpretation,
    declared_name: str,
    kind: PythonSourceDeclarationKind,
) -> PythonModuleSourceDeclarationSelection:
    """Select direct declarations by exact kind/name in one observed module.

    Consume canonical RI without a parallel parser or binding policy. Repeated
    declarations remain distinct; decorators and other bindings do not erase
    source facts. Native parse failures propagate without successful coverage.
    """
    if not declared_name.isidentifier():
        msg = "Source declaration name must be a Python identifier."
        raise ValueError(msg)
    if not isinstance(kind, PythonSourceDeclarationKind):
        msg = "Source declaration selection has an unsupported kind."
        raise TypeError(msg)
    if (
        module.repository_id != snapshot.repository_id
        or module.snapshot_id != snapshot.id
        or module.resource != snapshot.resource_at(module.resource.address)
    ):
        msg = "Source declaration module differs from the supplied snapshot."
        raise ValueError(msg)
    address = module.resource.address
    functions = derive_python_function_declarations(snapshot, resource_address=address)
    classes = derive_python_class_method_declarations(
        snapshot,
        resource_address=address,
    )
    declarations: tuple[PythonDirectModuleDeclaration, ...] = (
        classes.classes
        if kind is PythonSourceDeclarationKind.CLASS
        else functions.declarations
    )
    return PythonModuleSourceDeclarationSelection(
        module,
        declared_name,
        kind,
        functions,
        classes,
        tuple(item for item in declarations if item.declared_name == declared_name),
    )
```

<a id="evidence-0071"></a>

### evidence-0071

```json
{
  "address": "src/devtools/context/repository/observation.py",
  "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
  "end": 5347,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4311
}
```

```text
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
```

<a id="evidence-0072"></a>

### evidence-0072

```json
{
  "address": "src/devtools/context/repository/observation.py",
  "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
  "end": 5717,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5349
}
```

```text
def _semantic_digest(semantics: str, *values: str) -> str:
    """Hash unambiguous length-framed semantic values for this module."""
    digest = hashlib.sha256()
    for value in (semantics, *values):
        encoded = value.encode("utf-8")
        digest.update(len(encoded).to_bytes(8, byteorder="big"))
        digest.update(encoded)
    return digest.hexdigest()
```

<a id="evidence-0073"></a>

### evidence-0073

```json
{
  "address": "src/devtools/context/repository/snapshot.py",
  "content_identity": "492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7",
  "end": 2018,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1594
}
```

```text
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
```

<a id="evidence-0074"></a>

### evidence-0074

```json
{
  "address": "src/devtools/models/interaction/models.py",
  "content_identity": "6eb9d64480b0c9ab9ad6e0185f63006d0b7635e824cac8d7c111211d9926466f",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "4e1cded7a20da8216abfbe52f6dc2db1ca2c04cdede2d40793162e86c4d87d17",
  "end": 4963,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3171
}
```

```text
@dataclass(frozen=True, slots=True)
class ModelRequest:
    """Represent one immutable semantic request to a model interaction."""

    prompt: Prompt
    settings: ModelSettings = field(default_factory=ModelSettings)
    conversation: ConversationRef | None = None
    provider_settings: ProviderRequestSettings | None = None
    tools: tuple[ModelToolDefinition, ...] = ()

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
```

<a id="evidence-0075"></a>

### evidence-0075

```json
{
  "address": "src/devtools/models/interaction/prompt.py",
  "content_identity": "39cb6fee3466d10d96f263871246453ab95137459390d0f2553642c965b731f4",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "b79574a0110b54911e28921f9b7f5228a985b8921de1181a962e459d9c8c7fec",
  "end": 260,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 110
}
```

```text
@dataclass(frozen=True, slots=True)
class Prompt:
    """Represent the currently supported single text chat input."""

    content: str
    role: str
```

<a id="evidence-0076"></a>

### evidence-0076

```json
{
  "address": "tests/context/planning/test_plan.py",
  "content_identity": "641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088",
  "end": 6375,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2904
}
```

```text
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
```

<a id="evidence-0077"></a>

### evidence-0077

```json
{
  "address": "tests/context/planning/test_plan.py",
  "content_identity": "641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088",
  "end": 8421,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 7130
}
```

```text
def test_plan_rejects_mixed_or_duplicate_choices(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "def f():\n    pass\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    with pytest.raises(ValueError, match="purpose"):
        plan_disclosures(purpose=" ", snapshot=snapshot, disclosures=(option,))
    with pytest.raises(ValueError, match="at least one"):
        plan_disclosures(purpose="Inspect target.", snapshot=snapshot, disclosures=())
    with pytest.raises(ValueError, match="incompatible"):
        plan_disclosures(
            purpose="Different purpose.",
            snapshot=snapshot,
            disclosures=(option,),
        )
    with pytest.raises(ValueError, match="incompatible"):
        plan_disclosures(
            purpose=option.purpose,
            snapshot=snapshot,
            disclosures=(
                replace(option, snapshot_id=replace(snapshot.id, value="0" * 64)),
            ),
        )
    with pytest.raises(ValueError, match="repeats"):
        plan_disclosures(
            purpose=option.purpose,
            snapshot=snapshot,
            disclosures=(option, option),
        )
```

<a id="evidence-0078"></a>

### evidence-0078

```json
{
  "address": "tests/context/planning/test_plan.py",
  "content_identity": "641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088",
  "end": 10059,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 8423
}
```

```text
def test_whole_resource_rejects_stale_or_missing_state(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "first\r\nline\r\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    newer = _snapshot(tmp_path, {"target.py": "changed\r\nline\r\n"})
    with pytest.raises(DisclosureMaterializationError, match="snapshot"):
        materialize_disclosure_plan(plan=plan, snapshot=newer)
    with pytest.raises(DisclosureMaterializationError, match="another snapshot"):
        option.materialize(newer)
    stale = replace(snapshot, resources=newer.resources)
    with pytest.raises(DisclosureMaterializationError, match="differs"):
        materialize_disclosure_plan(plan=plan, snapshot=stale)
    missing = replace(snapshot, resources=())
    with pytest.raises(DisclosureMaterializationError, match="missing"):
        materialize_disclosure_plan(plan=plan, snapshot=missing)
    with pytest.raises(ValueError, match="purpose"):
        choose_whole_resource_disclosure(
            purpose=" ",
            snapshot=snapshot,
            resource_address=RepositoryResourceAddress("target.py"),
        )
    with pytest.raises(ValueError, match="does not contain"):
        choose_whole_resource_disclosure(
            purpose=option.purpose,
            snapshot=snapshot,
            resource_address=RepositoryResourceAddress("absent.py"),
        )
```

<a id="evidence-0079"></a>

### evidence-0079

```json
{
  "address": "tests/context/planning/test_plan.py",
  "content_identity": "641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088",
  "end": 11541,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 10061
}
```

```text
@pytest.mark.parametrize("wrong_value", ["identity", "representation"])
def test_materialization_rejects_an_option_that_changes_its_plan(
    tmp_path: Path,
    wrong_value: str,
) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "source\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )

    @dataclass(frozen=True)
    class IncompatibleOption:
        purpose: str = option.purpose
        snapshot_id: RepositorySnapshotId = option.snapshot_id
        repository_id: RepositoryId = option.repository_id
        representation: str = option.representation

        @property
        def identity(self) -> str:
            return option.identity

        def materialize(
            self,
            current: RepositorySnapshot,
        ) -> MaterializedDisclosureItem:
            item = option.materialize(current)
            if wrong_value == "identity":
                return replace(item, option_identity="changed")
            return replace(item, representation="changed")

    forged = IncompatibleOption()
    plan = DisclosurePlan(
        purpose=option.purpose,
        snapshot_id=snapshot.id,
        repository_id=snapshot.repository_id,
        disclosures=(forged,),
    )
    with pytest.raises(DisclosureMaterializationError, match="differs"):
        materialize_disclosure_plan(plan=plan, snapshot=snapshot)
```

<a id="evidence-0080"></a>

### evidence-0080

```json
{
  "address": "tests/context/planning/test_plan.py",
  "content_identity": "641a5ffab748722ab2118dec73331c88dbbe16b2bf9500876cc5e117871be492",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "7485eaa77a31915c0fbbde306135637263392bfba88e102dcacde31d00794088",
  "end": 12299,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 11543
}
```

```text
def test_realized_context_rejects_items_outside_the_plan(tmp_path: Path) -> None:
    snapshot = _snapshot(tmp_path, {"target.py": "source\n"})
    option = choose_whole_resource_disclosure(
        purpose="Inspect target.",
        snapshot=snapshot,
        resource_address=RepositoryResourceAddress("target.py"),
    )
    plan = plan_disclosures(
        purpose=option.purpose,
        snapshot=snapshot,
        disclosures=(option,),
    )
    item = option.materialize(snapshot)
    with pytest.raises(DisclosureMaterializationError, match="do not match"):
        ContextDisclosure(plan, ())
    with pytest.raises(DisclosureMaterializationError, match="do not match"):
        ContextDisclosure(plan, (replace(item, option_identity="other"),))
```

<a id="evidence-0081"></a>

### evidence-0081

```json
{
  "address": "tests/context/python/classes/test_declarations.py",
  "content_identity": "40acd74906703279d4d9251d72820354d488dabb5603c2bbd265d761755a726c",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "750c22bae743779b23838b909394f7cb83dae21e4f04ceab4a972bc02d4460b0",
  "end": 5948,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1748
}
```

```text
def test_direct_classes_methods_exclusions_and_existing_function_contract(
    tmp_path: Path,
) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "module.py": (
                "def module_function():\n    pass\n\n"
                "@register\nclass A(Base, pkg.Other):\n"
                "    @staticmethod\n    def run(self):\n"
                "        def nested():\n            pass\n"
                "    @property\n    async def load(self):\n        pass\n"
                "    class Nested:\n        def hidden(self):\n            pass\n\n"
                "class B:\n    def run(self):\n        pass\n\n"
                "def outer():\n    class Local:\n        pass\n"
            ),
        },
    )
    analysis = derive_python_class_method_declarations(snapshot)
    assert [item.declared_name for item in analysis.classes] == ["A", "B"]
    assert [item.declared_name for item in analysis.methods] == [
        "run",
        "load",
        "run",
    ]
    assert [item.declaration_kind for item in analysis.methods] == [
        PythonFunctionDeclarationKind.SYNCHRONOUS,
        PythonFunctionDeclarationKind.ASYNCHRONOUS,
        PythonFunctionDeclarationKind.SYNCHRONOUS,
    ]
    assert analysis.classes[0].support.source_range.start_line == 5
    assert analysis.classes[0].support.source_range.start_column_utf8 == 0
    assert analysis.methods[0].support.source_range.start_line == 7
    assert analysis.methods[1].support.source_range.start_line == 11
    assert analysis.methods[0].support.resource_address == snapshot.resource.address
    assert analysis.methods[0].support.snapshot_id == snapshot.id
    assert [base.ordinal for base in analysis.classes[0].base_syntax] == [0, 1]
    assert [base.source_text for base in analysis.classes[0].base_syntax] == [
        "Base",
        "pkg.Other",
    ]
    assert [
        base.occurrence.source_range.start_line
        for base in analysis.classes[0].base_syntax
    ] == [5, 5]
    assert analysis.classes[1].base_syntax == ()
    assert analysis.methods[0].containing_class == analysis.classes[0]
    assert analysis.methods[2].containing_class == analysis.classes[1]
    assert analysis.classes[0].subject.identity != analysis.classes[1].subject.identity
    assert analysis.methods[0].subject.identity != analysis.methods[2].subject.identity
    assert analysis.methods[0].identity != analysis.methods[2].identity
    assert analysis.methods[0].subject.containing_class_subject_identity == (
        analysis.classes[0].subject.identity
    )
    assert analysis.coverage.class_count == 2
    assert analysis.coverage.method_count == 3
    assert analysis.coverage.module_body_function_count == 2
    assert analysis.coverage.excluded_class_count == 2
    assert analysis.coverage.excluded_function_count == 2
    assert [item.kind for item in analysis.excluded_syntax] == [
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
        PythonExcludedClassMethodSyntaxKind.FUNCTION_OUTSIDE_SUPPORTED_CLASS,
        PythonExcludedClassMethodSyntaxKind.CLASS_OUTSIDE_MODULE_BODY,
    ]
    assert analysis.coverage.IS_EXHAUSTIVE_FOR_SCOPE
    assert analysis.coverage.derivation_identity == analysis.derivation.identity
    assert analysis.derivation.dependency.resource == snapshot.resource
    assert analysis.derivation.dependency.repository_id == snapshot.repository_id
    assert analysis.derivation.dependency.snapshot_id == snapshot.id
    assert analysis.classes[0].derivation_identity == analysis.derivation.identity
    assert analysis.methods[0].derivation_identity == analysis.derivation.identity
    assert analysis == derive_python_class_method_declarations(snapshot)
    module_functions = derive_python_function_declarations(snapshot)
    assert [item.declared_name for item in module_functions.declarations] == [
        "module_function",
        "outer",
    ]
    assert all(item.declared_name != "run" for item in module_functions.declarations)
    assert not hasattr(analysis.methods[0], "runtime_descriptor")
    assert not hasattr(analysis.classes[0], "resolved_bases")
```

<a id="evidence-0082"></a>

### evidence-0082

```json
{
  "address": "tests/context/python/classes/test_declarations.py",
  "content_identity": "40acd74906703279d4d9251d72820354d488dabb5603c2bbd265d761755a726c",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "750c22bae743779b23838b909394f7cb83dae21e4f04ceab4a972bc02d4460b0",
  "end": 15474,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 12436
}
```

```text
def test_containment_rejects_inconsistent_native_facts(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "a.py": (
                "class A(Base):\n    def run(self):\n        pass\n"
                "    class Nested:\n        pass\n"
            ),
        },
    )
    address = RepositoryResourceAddress("a.py")
    aggregate = analyze_python_class_method_resources(
        snapshot,
        resource_addresses=(address,),
    )
    analysis = aggregate.analyses[0]

    def reject(changed_analysis: PythonClassMethodAnalysis, message: str) -> None:
        changed = replace(aggregate, analyses=(changed_analysis,))
        with pytest.raises(ValueError, match=message):
            build_python_class_method_containment_view(
                snapshot,
                aggregate=changed,
            )

    for coverage in (
        replace(analysis.coverage, derivation_identity="other"),
        replace(analysis.coverage, class_count=0),
        replace(analysis.coverage, method_count=0),
        replace(analysis.coverage, excluded_class_count=0),
        replace(analysis.coverage, excluded_function_count=1),
    ):
        reject(replace(analysis, coverage=coverage), "coverage differs")

    declaration = analysis.classes[0]
    base = declaration.base_syntax[0]
    for changed_class in (
        replace(declaration, derivation_identity="other"),
        replace(
            declaration,
            subject=replace(declaration.subject, declaration_ordinal=1),
        ),
        replace(
            declaration,
            base_syntax=(
                replace(
                    base,
                    occurrence=replace(
                        base.occurrence,
                        snapshot_id=replace(snapshot.id, value="0" * 64),
                    ),
                ),
            ),
        ),
    ):
        reject(replace(analysis, classes=(changed_class,)), "Class declaration differs")

    method = analysis.methods[0]
    for changed_method in (
        replace(method, containing_class=replace(declaration, declared_name="Other")),
        replace(
            method,
            subject=replace(method.subject, containing_class_subject_identity="other"),
        ),
        replace(
            method,
            support=replace(
                method.support,
                resource_address=RepositoryResourceAddress("other.py"),
            ),
        ),
    ):
        reject(
            replace(analysis, methods=(changed_method,)),
            "Method declaration differs",
        )

    excluded = analysis.excluded_syntax[0]
    reject(
        replace(
            analysis,
            excluded_syntax=(
                replace(
                    excluded,
                    occurrence=replace(
                        excluded.occurrence,
                        resource_address=RepositoryResourceAddress("other.py"),
                    ),
                ),
            ),
        ),
        "Excluded syntax differs",
    )
```

<a id="evidence-0083"></a>

### evidence-0083

```json
{
  "address": "tests/context/python/function/test_declarations.py",
  "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
  "end": 8729,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 7851
}
```

```text
def test_multiple_same_name_direct_declarations_have_distinct_subjects(
    tmp_path: Path,
) -> None:
    """Declared text is not subject identity or declaration-result identity."""
    snapshot = _snapshot(
        tmp_path,
        """def repeated():
    pass

def repeated():
    pass

def repeated():
    pass
""",
    )

    result = derive_python_function_declarations(snapshot)

    expected_names = [
        "repeated",
        "repeated",
        "repeated",
    ]
    expected_count = len(expected_names)
    assert [item.declared_name for item in result.declarations] == expected_names
    subject_identities = {item.subject.identity for item in result.declarations}
    assert len(subject_identities) == expected_count
    assert len({item.identity for item in result.declarations}) == expected_count
    assert result.coverage.declaration_count == expected_count
```

<a id="evidence-0084"></a>

### evidence-0084

```json
{
  "address": "tests/context/python/function/test_declarations.py",
  "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
  "end": 10611,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 9854
}
```

```text
def test_source_range_uses_utf8_byte_columns(tmp_path: Path) -> None:
    """Non-ASCII syntax demonstrates the local stdlib AST column contract."""
    final_line = '    return "é"'
    snapshot = _snapshot(tmp_path, f"def café():\n{final_line}\n")

    declaration = derive_python_function_declarations(snapshot).declarations[0]
    source_range = declaration.support.source_range
    expected_end_line = source_range.start_line + 1

    assert declaration.declared_name == "café"
    assert source_range.start_line == 1
    assert source_range.start_column_utf8 == 0
    assert source_range.end_line == expected_end_line
    assert source_range.end_column_utf8 == len(final_line.encode("utf-8"))
    assert source_range.end_column_utf8 != len(final_line)
```

<a id="evidence-0085"></a>

### evidence-0085

```json
{
  "address": "tests/context/python/function/test_materialization.py",
  "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
  "end": 3758,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1968
}
```

```text
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
```

<a id="evidence-0086"></a>

### evidence-0086

```json
{
  "address": "tests/context/python/function/test_materialization.py",
  "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
  "end": 6703,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5486
}
```

```text
@pytest.mark.parametrize(
    ("source_range", "match"),
    [
        (PythonSourceRange(1, 30, 1, 29), "ends before"),
        (PythonSourceRange(1, 0, 2, 0), "line is outside"),
        (PythonSourceRange(1, 0, 1, 100), "column is outside"),
        (PythonSourceRange(1, 8, 1, 26), "UTF-8 character boundaries"),
    ],
)
def test_rejects_source_ranges_that_cannot_be_faithfully_applied(
    tmp_path: Path,
    source_range: PythonSourceRange,
    match: str,
) -> None:
    """Malformed coordinates fail instead of producing misleading source."""
    snapshot = _snapshot(tmp_path, 'def café(): return "olé"\n')
    disclosure = _disclosure(snapshot, "café")
    disclosure_item = disclosure.items[0]
    invalid_occurrence = replace(
        disclosure_item.source_occurrence,
        source_range=source_range,
    )
    invalid_item = replace(
        disclosure_item,
        source_occurrence=invalid_occurrence,
    )
    invalid_disclosure = replace(disclosure, items=(invalid_item,))

    with pytest.raises(PythonFunctionSourceMaterializationError, match=match):
        materialize_python_function_disclosure_source(
            disclosure=invalid_disclosure,
            snapshot=snapshot,
        )
```

<a id="evidence-0087"></a>

### evidence-0087

```json
{
  "address": "tests/context/python/function/test_qualified_reference.py",
  "content_identity": "d8ede2921942e6f4acabc9e4176190781eae10fba4c7e0d894aedbb831b2dafb",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "9c7dfe605bbc376cbb99024b56ae468cdaefab9766bcbe2612175b46106e3c2d",
  "end": 6492,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3511
}
```

```text
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
```

<a id="evidence-0088"></a>

### evidence-0088

```json
{
  "address": "tests/context/python/function/test_qualified_reference.py",
  "content_identity": "d8ede2921942e6f4acabc9e4176190781eae10fba4c7e0d894aedbb831b2dafb",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "9c7dfe605bbc376cbb99024b56ae468cdaefab9766bcbe2612175b46106e3c2d",
  "end": 10304,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 8793
}
```

```text
def test_stale_source_or_target_content_is_rejected(tmp_path: Path) -> None:
    snapshot = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n",
            "target.py": "def f():\n    pass\n",
        },
    )
    analysis = _analysis(snapshot)
    disclosure = disclose_python_qualified_reference(
        purpose="Inspect binding",
        analysis=analysis,
        reference=analysis.references[0],
    )
    newer = _snapshot(
        tmp_path,
        {
            "consumer.py": "from target import f\nf()\n# change\n",
            "target.py": "def f():\n    return 1\n",
        },
    )
    with pytest.raises(PythonQualifiedReferenceDisclosureError, match="snapshot"):
        materialize_python_qualified_reference_source(
            disclosure=disclosure,
            snapshot=newer,
        )
    for stale_address, message in (
        ("consumer.py", "source content"),
        ("target.py", "Target declaration"),
    ):
        stale = replace(
            snapshot,
            resources=tuple(
                newer.resource_at(item.address)
                if item.address == RepositoryResourceAddress(stale_address)
                else item
                for item in snapshot.resources
            ),
        )
        with pytest.raises(PythonQualifiedReferenceDisclosureError, match=message):
            materialize_python_qualified_reference_source(
                disclosure=disclosure,
                snapshot=stale,
            )
```

<a id="evidence-0089"></a>

### evidence-0089

```json
{
  "address": "tests/context/python/function/test_request_assembly.py",
  "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
  "end": 4445,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2102
}
```

```text
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
```

<a id="evidence-0090"></a>

### evidence-0090

```json
{
  "address": "tests/context/python/modules/test_selection.py",
  "content_identity": "97ec04ba3d29c5c4984678ec389ca11172738134335ad17b160171e7e5192541",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "87491fef6cbd5c7986a6522574fccb34cddbe0194fe73e4563404c29d8acdf83",
  "end": 3213,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1753
}
```

```text
@pytest.mark.parametrize(
    ("syntax", "kind"),
    [
        ("class Target: pass", Kind.CLASS),
        ("def Target(): pass", Kind.FUNCTION),
        ("async def Target(): pass", Kind.FUNCTION),
    ],
)
@pytest.mark.parametrize("prefix", ["", "@decorator\n"])
def test_plain_and_decorated_native_identity(
    syntax: str,
    kind: Kind,
    prefix: str,
) -> None:
    snapshot, module = _frame(prefix + syntax + "\n")
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == 1
    target = selected.declarations[0]
    assert target in (
        selected.class_analysis.classes
        if kind is Kind.CLASS
        else selected.function_analysis.declarations
    )
    assert target.subject.snapshot_id == snapshot.id
    assert target.support.resource_address == module.resource.address
    assert selected.module is module
    assert selected.kind is kind
    assert selected.declared_name == "Target"
    assert selected == select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    binding = lookup_python_module_declaration(
        snapshot,
        module=module,
        declared_name="Target",
    )
    assert binding.outcome is (
        BindingOutcome.NOT_DECLARATION if prefix else BindingOutcome.RESOLVED
    )
```

<a id="evidence-0091"></a>

### evidence-0091

```json
{
  "address": "tests/context/python/modules/test_selection.py",
  "content_identity": "97ec04ba3d29c5c4984678ec389ca11172738134335ad17b160171e7e5192541",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "87491fef6cbd5c7986a6522574fccb34cddbe0194fe73e4563404c29d8acdf83",
  "end": 4370,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3215
}
```

```text
@pytest.mark.parametrize(
    ("content", "kind", "count"),
    [
        ("class Target: pass\nclass Target: pass\n", Kind.CLASS, 2),
        ("def Target(): pass\ndef Target(): pass\n", Kind.FUNCTION, 2),
        ("class Target: pass\ndef Target(): pass\n", Kind.CLASS, 1),
        ("class Target: pass\ndef Target(): pass\n", Kind.FUNCTION, 1),
        ("class Target: pass\n", Kind.FUNCTION, 0),
        ("def Target(): pass\n", Kind.CLASS, 0),
        ("class target: pass\n", Kind.CLASS, 0),
        ("if enabled:\n    class Target: pass\n", Kind.CLASS, 0),
        ("Target = lambda: None\n", Kind.FUNCTION, 0),
        ("@decorator\nclass Target: pass\nTarget = other\nexec(code)\n", Kind.CLASS, 1),
    ],
)
def test_exact_kind_scope_and_repeated_declarations(
    content: str,
    kind: Kind,
    count: int,
) -> None:
    snapshot, module = _frame(content)
    selected = select_python_module_source_declarations(
        snapshot,
        module=module,
        declared_name="Target",
        kind=kind,
    )
    assert len(selected.declarations) == count
    assert len({item.subject.identity for item in selected.declarations}) == count
```

<a id="evidence-0092"></a>

### evidence-0092

```json
{
  "address": "tests/context/python/modules/test_selection.py",
  "content_identity": "97ec04ba3d29c5c4984678ec389ca11172738134335ad17b160171e7e5192541",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "87491fef6cbd5c7986a6522574fccb34cddbe0194fe73e4563404c29d8acdf83",
  "end": 5620,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 4372
}
```

```text
def test_selection_rejects_invalid_and_foreign_inputs() -> None:
    snapshot, module = _frame("class Target: pass\n")
    with pytest.raises(ValueError, match="identifier"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="a.b",
            kind=Kind.CLASS,
        )
    with pytest.raises(TypeError, match="unsupported kind"):
        select_python_module_source_declarations(
            snapshot,
            module=module,
            declared_name="Target",
            kind="class",  # type: ignore[arg-type]
        )
    for foreign in (
        replace(
            module,
            repository_id=RepositoryId.parse("00000000-0000-0000-0000-000000000002"),
        ),
        replace(module, snapshot_id=RepositorySnapshotId("b" * 64)),
        replace(
            module,
            resource=replace(module.resource, content="class Different: pass\n"),
        ),
    ):
        with pytest.raises(ValueError, match="differs from the supplied snapshot"):
            select_python_module_source_declarations(
                snapshot,
                module=foreign,
                declared_name="Target",
                kind=Kind.CLASS,
            )
```

<a id="evidence-0093"></a>

### evidence-0093

```json
{
  "address": "tests/models/interaction/test_models.py",
  "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
  "end": 4005,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 3269
}
```

```text
def test_model_request_is_immutable_and_separates_input_from_settings() -> None:
    """One request contains semantic input, portable settings, and continuation."""
    source = InteractionSource("llama.cpp")
    request = ModelRequest(
        prompt=Prompt(content="question", role="user"),
        settings=ModelSettings(maximum_output_tokens=_REQUEST_OUTPUT_TOKENS),
        conversation=ConversationRef(source, "thread"),
    )
    assert request.prompt.content == "question"
    assert request.settings.maximum_output_tokens == _REQUEST_OUTPUT_TOKENS
    assert request.conversation == ConversationRef(source, "thread")
    with pytest.raises(FrozenInstanceError):
        request.settings = ModelSettings()  # type: ignore[misc]
```

<a id="evidence-0094"></a>

### evidence-0094

```json
{
  "address": "tests/models/interaction/test_models.py",
  "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
  "end": 6244,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 5829
}
```

```text
def test_prompt_is_an_immutable_model_input_without_conversation_identity() -> None:
    """A prompt contains only the text and role needed by current providers."""
    prompt = Prompt(content="Remember ALPHA-4821.", role="user")
    assert prompt.content == "Remember ALPHA-4821."
    assert prompt.role == "user"
    with pytest.raises(FrozenInstanceError):
        prompt.content = "other"  # type: ignore[misc]
```

<a id="evidence-0095"></a>

### evidence-0095

```json
{
  "address": "tests/scripts/test_validate_development.py",
  "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
  "end": 1503,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 888
}
```

```text
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
```

<a id="evidence-0096"></a>

### evidence-0096

```json
{
  "address": "tests/scripts/test_validate_development.py",
  "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
  "end": 2104,
  "kind": "resource",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1505
}
```

```text
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
```

<a id="evidence-0097"></a>

### evidence-0097

```json
{
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "end": 71,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 0,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Add caller-selected direct Python source-declaration disclosure choices
```

<a id="evidence-0098"></a>

### evidence-0098

```json
{
  "end": 98,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 0,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Add caller-selected direct Python source-declaration disclosure choices to common Context Planning
```

<a id="evidence-0099"></a>

### evidence-0099

```json
{
  "end": 165,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 100,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
alongside existing qualified-reference and whole-resource choices
```

<a id="evidence-0100"></a>

### evidence-0100

```json
{
  "end": 208,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 167,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
without automatic retrieval or selection.
```

<a id="evidence-0101"></a>

### evidence-0101

```json
{
  "end": 356,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 209,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities
```

<a id="evidence-0102"></a>

### evidence-0102

```json
{
  "end": 444,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 358,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
support a direct method only through its validated native class parent and containment
```

<a id="evidence-0103"></a>

### evidence-0103

```json
{
  "end": 530,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 446,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
without runtime attribute, imported-facade, inherited-method or semantic resolution.
```

<a id="evidence-0104"></a>

### evidence-0104

```json
{
  "end": 650,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 531,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`
```

<a id="evidence-0105"></a>

### evidence-0105

```json
{
  "end": 751,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 652,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.
```

<a id="evidence-0106"></a>

### evidence-0106

```json
{
  "end": 922,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 752,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`
```

<a id="evidence-0107"></a>

### evidence-0107

```json
{
  "end": 961,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 924,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
reject foreign or stale frame/content
```

<a id="evidence-0108"></a>

### evidence-0108

```json
{
  "end": 979,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 963,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
missing resource
```

<a id="evidence-0109"></a>

### evidence-0109

```json
{
  "end": 1010,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 981,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
unsupported declaration scope
```

<a id="evidence-0110"></a>

### evidence-0110

```json
{
  "end": 1076,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1015,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
mismatched returned identity before publishing the disclosure
```

<a id="evidence-0111"></a>

### evidence-0111

```json
{
  "end": 1104,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1078,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
without reacquiring files.
```

<a id="evidence-0112"></a>

### evidence-0112

```json
{
  "end": 1249,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1105,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`
```

<a id="evidence-0113"></a>

### evidence-0113

```json
{
  "end": 1276,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1251,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
preserve UTF-8 boundaries
```

<a id="evidence-0114"></a>

### evidence-0114

```json
{
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "end": 1310,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1251,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes
```

<a id="evidence-0115"></a>

### evidence-0115

```json
{
  "end": 1288,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1278,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
decorators
```

<a id="evidence-0116"></a>

### evidence-0116

```json
{
  "end": 1310,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1290,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
CRLF/non-ASCII bytes
```

<a id="evidence-0117"></a>

### evidence-0117

```json
{
  "end": 1342,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1315,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
caller order in mixed plans
```

<a id="evidence-0118"></a>

### evidence-0118

```json
{
  "end": 1414,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1344,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
without inferring sufficiency or expanding to whole owners implicitly.
```

<a id="evidence-0119"></a>

### evidence-0119

```json
{
  "end": 1494,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1415,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Preserve common rendering and copied request assembly with class `ModelRequest`
```

<a id="evidence-0120"></a>

### evidence-0120

```json
{
  "end": 1512,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1496,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
original request
```

<a id="evidence-0121"></a>

### evidence-0121

```json
{
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "end": 1620,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1496,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt
```

<a id="evidence-0122"></a>

### evidence-0122

```json
{
  "end": 1525,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1514,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
prompt role
```

<a id="evidence-0123"></a>

### evidence-0123

```json
{
  "end": 1535,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1527,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
settings
```

<a id="evidence-0124"></a>

### evidence-0124

```json
{
  "end": 1549,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1537,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
conversation
```

<a id="evidence-0125"></a>

### evidence-0125

```json
{
  "end": 1620,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1551,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
provider settings and tools remain unchanged except the copied prompt
```

<a id="evidence-0126"></a>

### evidence-0126

```json
{
  "end": 1651,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1622,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
keep task text before Context
```

<a id="evidence-0127"></a>

### evidence-0127

```json
{
  "end": 1701,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1656,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
introduce no new budget or truncation policy.
```

<a id="evidence-0128"></a>

### evidence-0128

```json
{
  "end": 1796,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1702,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Expose the new explicit choice through the common planning public API and outer Context facade
```

<a id="evidence-0129"></a>

### evidence-0129

```json
{
  "end": 1826,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1798,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
keeping dependency direction
```

<a id="evidence-0130"></a>

### evidence-0130

```json
{
  "end": 1909,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1831,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
avoiding a Retrieval dependency or language-specific logic in common assembly.
```

<a id="evidence-0131"></a>

### evidence-0131

```json
{
  "end": 1968,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1910,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Add focused tests for direct function/class/method choices
```

<a id="evidence-0132"></a>

### evidence-0132

```json
{
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "end": 1968,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1932,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
direct function/class/method choices
```

<a id="evidence-0133"></a>

### evidence-0133

```json
{
  "end": 2005,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 1970,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
decorated and repeated declarations
```

<a id="evidence-0134"></a>

### evidence-0134

```json
{
  "end": 2054,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2007,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
mixed-plan ordering and exact source/provenance
```

<a id="evidence-0135"></a>

### evidence-0135

```json
{
  "end": 2096,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2056,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
stale/foreign/missing-resource rejection
```

<a id="evidence-0136"></a>

### evidence-0136

```json
{
  "end": 2124,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2098,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
unchanged existing choices
```

<a id="evidence-0137"></a>

### evidence-0137

```json
{
  "end": 2157,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2129,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
copied-request preservation.
```

<a id="evidence-0138"></a>

### evidence-0138

```json
{
  "end": 2250,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2158,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md`
```

<a id="evidence-0139"></a>

### evidence-0139

```json
{
  "end": 2301,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2251,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
to explain source identity versus runtime bindings
```

<a id="evidence-0140"></a>

### evidence-0140

```json
{
  "coordinate_system": "zero-based Unicode character offsets; half-open",
  "end": 2432,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2251,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.
```

<a id="evidence-0141"></a>

### evidence-0141

```json
{
  "end": 2336,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2303,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
explicit representation admission
```

<a id="evidence-0142"></a>

### evidence-0142

```json
{
  "end": 2380,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2338,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
supported/deferred scope and compatibility
```

<a id="evidence-0143"></a>

### evidence-0143

```json
{
  "end": 2432,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2382,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
without claiming automatic relevance or readiness.
```

<a id="evidence-0144"></a>

### evidence-0144

```json
{
  "end": 2485,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2433,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Validate with file `scripts/validate_development.py`
```

<a id="evidence-0145"></a>

### evidence-0145

```json
{
  "end": 2543,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2490,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
preserve file `pyproject.toml` test/coverage settings
```

<a id="evidence-0146"></a>

### evidence-0146

```json
{
  "end": 2593,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2545,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
run the documented protected development profile
```

<a id="evidence-0147"></a>

### evidence-0147

```json
{
  "end": 2611,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2595,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
Ruff lint/format
```

<a id="evidence-0148"></a>

### evidence-0148

```json
{
  "end": 2624,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2613,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
strict mypy
```

<a id="evidence-0149"></a>

### evidence-0149

```json
{
  "end": 2667,
  "kind": "task",
  "provenance": {
    "authorship": "PRIMARY treatment-blind semantic adjudication in this session",
    "canonical_payload_sha256": "c774aa5f8fa82d8271fbaf801393f3f942e33b6e686417c4b7f195317344d3ce",
    "frame": {
      "corpus_id": "a348059425edb51e8296900cd570f16aedb394b871b5cfb98144625cb34c93af",
      "frame_identity": "c78f7b4bd23b95117058470c673c7c376c40018323e583228e67b88a3f1f311a",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "07f8c054b5aea9c7c893231a53fb2271d9df74f91c71ee19975c0ba86f52d7ca",
      "source_head": "0c0029a2d608bafe95c6792fe04b4127e17f0304"
    }
  },
  "start": 2629,
  "task_identity": "case-0012-direct-source-disclosure"
}
```

```text
both worktree/index whitespace checks.
```
