# Task requirement matrix

Every non-operational task line (including all semicolon clauses) maps to an obligation. Criteria explicitly inventory its complete contract. This is task-interpretation review, not repository witness completeness.

## R01 [0,209)

Add caller-selected direct Python source-declaration disclosure choices to common Context Planning, alongside existing qualified-reference and whole-resource choices, without automatic retrieval or selection.

Obligations: source, choices

## R02 [209,531)

Reuse function `devtools.context.python.modules.selection.select_python_module_source_declarations` for direct function and class source identities; support a direct method only through its validated native class parent and containment, without runtime attribute, imported-facade, inherited-method or semantic resolution.

Obligations: source

## R03 [531,752)

Integrate the choices with class `devtools.context.planning.plan.DisclosurePlan` and module `devtools.context.planning`, retaining immutable purpose/frame/ordered-choice contracts and compatibility with existing choices.

Obligations: choices

## R04 [752,1105)

Validate every supplied native declaration and resource against the retained snapshot through method `devtools.context.repository.snapshot.RepositorySnapshot.resource_at`; reject foreign or stale frame/content, missing resource, unsupported declaration scope and mismatched returned identity before publishing the disclosure, without reacquiring files.

Obligations: integrity

## R05 [1105,1415)

Materialize the exact declaration source segment with native derivation, source-range and owner-resource provenance in class `ContextDisclosure`; preserve UTF-8 boundaries, decorators, CRLF/non-ASCII bytes and caller order in mixed plans, without inferring sufficiency or expanding to whole owners implicitly.

Obligations: materialization

## R06 [1415,1702)

Preserve common rendering and copied request assembly with class `ModelRequest`: original request, prompt role, settings, conversation, provider settings and tools remain unchanged except the copied prompt; keep task text before Context and introduce no new budget or truncation policy.

Obligations: assembly

## R07 [1702,1910)

Expose the new explicit choice through the common planning public API and outer Context facade, keeping dependency direction and avoiding a Retrieval dependency or language-specific logic in common assembly.

Obligations: exports

## R08 [1910,2158)

Add focused tests for direct function/class/method choices, decorated and repeated declarations, mixed-plan ordering and exact source/provenance, stale/foreign/missing-resource rejection, unchanged existing choices and copied-request preservation.

Obligations: tests

## R09 [2158,2433)

Update file `src/devtools/context/planning/docs/overview.md` and file `docs/architecture.md` to explain source identity versus runtime bindings, explicit representation admission, supported/deferred scope and compatibility, without claiming automatic relevance or readiness.

Obligations: documentation

## R10 [2433,2668)

Validate with file `scripts/validate_development.py` and preserve file `pyproject.toml` test/coverage settings; run the documented protected development profile, Ruff lint/format, strict mypy and both worktree/index whitespace checks.

Obligations: validation

## Operational exclusions outside the feature task

Stage A freezes acquisition only: no future feature implementation, treatment, gold, confirmation/reserve or live services. `.local/codex-result.md` is operational handoff only, excluded from task text, obligations, hints, queries, witnesses, eligible resources, scientific hashes and gap judgments. These operations are not repository-information obligations.
