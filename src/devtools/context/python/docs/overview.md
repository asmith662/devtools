# Python Repository Intelligence

The [project configuration package](../project_configuration/docs/overview.md)
owns retained-TOML declarations and qualified observed targets for README,
Hatch wheel packages, pytest testpaths, Coverage source and mypy files/search
paths. It separates configuration-relative routes from explicit tool frames,
retains competing module/path interpretations, and makes no execution/runtime
claim. This Python-owned RI is independent of Retrieval and framework runtime
configuration. Modules own shared exact name lookup; config creates no imports.

## Mirrored source/test paths

`derive_python_mirrored_path_correspondences(snapshot)` derives exact path
correspondence from **observed resources in one `RepositorySnapshot`**. The
supported convention is:

```text
src/devtools/<directory>/<stem>.py
tests/<directory>/test_<stem>.py
```

`<directory>` may be empty or nested. Both addresses must occur in the supplied
snapshot. Source `__init__.py` and its test-side `test___init__.py` counterpart
are excluded. Other paths and near matches establish no correspondence. The
analysis reports counts for eligible, unmatched, and initializer resources
within the explicit snapshot selection; an unmatched path is not a claim about
resources outside that selection.

Each `PythonMirroredPathCorrespondence` retains distinct source and test-side
roles, repository and snapshot identity, both exact observed resource
occurrences and content identities, and the derivation identity. The derivation
identity includes the rule version and the entire observed resource selection.
Output order is canonical by source address. Derivation uses retained snapshot
state and never reopens the working tree.

```text
mirrored path correspondence ≠ semantic test relationship
```

The fact says only that the observed paths satisfy this repository's convention.
It does not say that one resource TESTS, COVERS, VALIDATES, EXERCISES, or
depends on the other. It contains no query, relevance, ranking, or disclosure
decision. Retrieval and Context consumers can use the public Python RI API
without importing Increment 31. The current direct structural retriever and
Personalized PageRank graph view do not consume this fact automatically.

[Increment 31](../../../../../experiments/increment_31/README.md) established
the exact deterministic rule while separately evaluating candidate generation.
Its weak incremental candidate reach does not weaken the path fact; its
candidate policy, labels, and graph traversals are not part of this API.
