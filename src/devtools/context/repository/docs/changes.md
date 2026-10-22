# Retained snapshot resource differences

`compare_repository_snapshots(before, after)` returns an immutable
`RepositorySnapshotDelta` through both `devtools.context.repository` and
`devtools.context`. The existing repository package owns it. Dependencies are
the exact supplied snapshots and their addressed resource occurrences; it uses
no filesystem, Git, acquisition, Commands, Tool execution or new identity owner.

The result retains `before` and `after` directly. `added`, `removed`, `modified`
and `unchanged` are tuples of existing RepositoryResourceAddress values sorted
by canonical address.value. Added/removed describe membership in these finite
observed collections, not a physical creation/deletion, rename, copy, move,
whole repository inventory or ordered mutation history. Common addresses compare
the complete occurrence value, not only snapshot or content identity. Equal
content at distinct addresses does not collapse occurrences. Empty/no-change
collections work. Repository mismatch and duplicate addresses raise ValueError.

```python
delta = compare_repository_snapshots(before, after)
for address in delta.modified:
    old_occurrence = delta.before.resource_at(address)
    new_occurrence = delta.after.resource_at(address)
```

The taxonomy concept is SnapshotDelta: a difference relationship between retained
states. This bounded implementation supports the existing explicit-required-text
snapshot contract. It is not a new repository state model, observation validator,
incremental-maintenance process, applicability decision, cache, mutation API or
persistence schema. Callers retain their own acquisition and validation authority.
General snapshot policy, incremental RI/index maintenance and invalidation remain
open B-0002 work. Framework consumers can use these differences as input without
treating collection absence as evidence about an unobserved filesystem.

Tests: tests/context/repository/test_changes.py. Delivery and exact source-bound
validation: apps/qwen/evaluation/new-module-22/README.md. This implementation is
Codex-authored following a separately preserved failed Qwen attempt.
