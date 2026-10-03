# Soft repository-role evidence

`devtools.context.localization.roles` derives positive, multi-label hints from
retained resource addresses and explicitly supplied native Repository
Intelligence (RI) analyses. The derivation is independent of task, obligation,
query, ranking and acquisition. Localization owns this interpretation; RI and
core Retrieval do not import it.

```text
RI / intrinsic resource semantics
                 |
                 v
        Resource role evidence
                 |
                 v
       future routing policy
                 |
                 v
              Retrieval
```

The latter two steps are a future seam. This increment changes no Retrieval
ordering or existing Localization lexical acquisition. Repository fact, role
support, obligation-relative relevance, witness satisfaction and candidate
elimination remain distinct.

## Vocabulary and support kinds

Roles overlap. They name evidence families, not authoritative resource labels.
`RoleSupportKind` identifies the basis directly; there is no strength ladder,
manual weight, probability, score or calibrated confidence.

| Role | Positive supports in v1 |
| --- | --- |
| `PYTHON_CODE` | Exact `.py` suffix convention; supplied native Python module interpretation. |
| `TEST` | Exact `tests` parent component convention; test side of a supplied native mirrored-path pair; qualified pytest testpaths targets; bounded basename-glob observation below. |
| `DOCUMENTATION` | Case-insensitive `.md` suffix; exact `docs` parent component; case-insensitive README, README.md, README.rst or README.txt basename; supplied native project README target. |
| `PROJECT_CONFIGURATION` | Exact pyproject.toml basename convention; supported native build/project/tool declarations; recognized tool-table presence. |
| `TEST_CONFIGURATION` | Supported pytest declarations or recognized pytest ini-options table presence. |
| `BUILD_CONFIGURATION` | Supported build-system declarations; supported Hatch wheel selectors or table presence. |
| `TOOL_CONFIGURATION` | Supported tool selectors/settings or recognized tool-table presence. |
| `PACKAGE_SURFACE` | Exact __init__.py basename convention; supplied package interpretation; parent side of supplied immediate package membership. |
| `PACKAGE_MEMBER` | Child side of supplied immediate package membership. |

Each convention has a separately named support kind. Structural support retains
the corresponding native identity. Configuration declaration support retains
its semantic key and declaration/setting identity. Table support references the
native analysis identity and exact recognized table path. Target support
references the native target fact and its route/requested value. The complete
native inputs remain available on the view for inspecting scopes, values,
ambiguities, absence and unsupported results; full RI facts are not copied into
each support.

`VALIDATION` is deferred: a validation-like filename does not establish a stable
tool contract. `IMPLEMENTATION` and a `src/` role rule are not selected. Semantic
documentation subtypes, general public-API/export claims and a cross-language
ontology are deferred. A package initializer is not proven public API. Existing
import/member resolution remains available for a later bounded integration; v1
does not add `__all__` analysis or infer dynamic exports.

## Native inputs and bounded pytest observations

The caller supplies `RepositoryRoleEvidenceInputs`: zero or more module
interpretation, immediate membership, mirrored-path, configuration declaration
and configuration resolution analyses. Omitted analyses are not automatically
discovered. Configuration resolutions also supply their declaration analyses.
The derivation reproduces each analysis through its canonical owner against the
exact retained snapshot before consuming it. These calls are static inspection,
not Retrieval, filesystem rereads, collection or tool execution. Native module
roots, selections, configuration universes and tool frames remain caller-owned.
The mirrored-path input retains the existing owner's exact repository-specific
path convention, not a universal testing relationship.

Supported project metadata, scripts and entry-point declarations support the
configuration resource; their strings do not prove runtime bindings. All six
existing selector declarations can support the configuration resource. Only
pytest testpaths and project README target facts currently provide target-role
support. Ruff, mypy, Coverage and Hatch table presence is distinguished from
interpretation of all values or effective execution.

For `python_files`, v1 interprets **string arrays only**, using case-sensitive
`fnmatchcase` against POSIX-address basenames ending in `.py`. Patterns must be
nonempty and contain neither path separators nor ASCII control characters.
Glob wildcards and character classes use that standard-library operation.
Matches are bounded to the same configuration analysis's supplied, positively
resolved testpaths target facts. Each observation references both the naming
setting and testpaths target identity, plus the pattern occurrence ordinal.
Duplicate declared array occurrences retain distinct provenance; repeated
presentation of the same fact does not multiply support.

This explicitly named `case-sensitive-posix-basename-glob-v1` observation is not
a claim of complete pytest matching on every platform. Pytest's
[configuration reference](https://docs.pytest.org/en/stable/reference/reference.html)
defines filename glob declarations; its
[matching implementation](https://github.com/pytest-dev/pytest/blob/main/src/_pytest/pathlib.py)
also handles path patterns and operating-system normalization. Those behaviors,
scalar pattern splitting, implicit defaults and testpaths fallback are outside
v1. Uninterpreted pattern forms and absent supplied target scope produce explicit
`RepositoryRoleLimitation` records. Nonmatches produce no negative evidence.

`python_classes`, `python_functions`, `norecursedirs` and opaque `addopts` support
the configuration resource only. v1 does not inspect class/function test units,
apply ignore options or suppress resources. Dynamic conftest.py, plugins, hooks,
command-line overrides and runtime collection remain outside this contract.

## Identity, immutable queries and non-claims

`derive_repository_role_evidence(snapshot, inputs=...)` returns an immutable
`RepositoryRoleEvidenceView`. Its resources retain the **entire observed frame**,
including resources without support. `for_resource(address)` returns all roles,
`for_role(role)` returns the positive evidence inventory, and
`supports_for(address, role)` explains a role. An unknown address is rejected;
an empty answer for a known address is not exclusion, contradiction or absence
of relevant information.

The versioned derivation digest binds repository, snapshot, sorted native
resource addresses/content identities and canonical native input dependencies.
Evidence identities additionally bind the resource, role and exact support
membership. Supports retain source address, native references and exact bounded
observation; repository/snapshot identity is supplied by their enclosing evidence
and view. These local SHA-256 identities follow the existing bounded RI identity
pattern; they do not replace canonical repository/resource identities. No source
spans are fabricated. Identical repeated analyses/supports coalesce;
resources, evidence, supports, inputs and limitations have deterministic ordering.
Stale, foreign or altered native analyses are rejected.

Intrinsic path properties remain canonical address values plus ordinary
`PurePosixPath` operations. There are no parallel basename, suffix or path RI
facts. Address conventions are not universal repository truths:

- Under tests/ is not proven TEST; under docs/ is not proven architectural documentation.
- Declared testpaths or a basename match is not complete pytest collection.
- No positive TEST support is not NOT TEST; outside testpaths is not irrelevant.
- pyproject.toml is not every project behavior; absent entry points do not rule out runtime registration.
- PACKAGE_SURFACE support is not public-API ownership or obligation satisfaction.

No negative evidence, hard filter, elimination, satisfaction assessment or routing
policy is emitted. A later caller-directed obligation policy may consume these
supports while retaining the global lexical safety lane and an unfiltered escape
path. Its usefulness requires a new prospective experiment; historical Case 0004
gold resources and outcomes were not rule-design inputs.
