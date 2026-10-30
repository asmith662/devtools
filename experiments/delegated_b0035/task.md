# Delegated B-0035 responsibility A

Implement complete authorized inventory representation in the existing coding
navigation presentation owner, src/devtools/agents/coding/navigation.py.
This is a useful prerequisite for the repository host's missing initial inventory;
initial Prompt insertion, refresh wiring and nonduplication are a separate stage.
Do not modify the host, tests, budgets, scope or existing navigation behavior.

Provide this callable contract in that module:
complete_inventory(scope: SourceScope, editable: tuple[RepositoryResourceAddress, ...],
maximum_bytes: int) -> dict[str, object].
The implementation choices are yours. The required observable behavior is:

- Return all and only resources in the current authorized SourceScope, in canonical
  address order, including an empty resource collection.
- Exactly these top-level fields: repository_id, snapshot_id, source_acquired=false,
  complete_inventory=true, resources. Each resource has exactly address, content_identity,
  byte_size (UTF-8 bytes, not characters) and editable (a boolean).
- Only repository-relative addresses and metadata are disclosed. Never include
  source text, absolute roots, unrelated paths, ranked-only subsets or read credit.
- Editable addresses must belong to the scope; reject a foreign editable address
  with ValueError. Duplicate editable entries need not create duplicate rows.
- Refuse a stale scope through its established currentness contract. Do not cache
  a prior inventory across source changes or invent a new source identity.
- maximum_bytes is a positive integer, excluding bool. Refuse invalid bounds with
  ValueError. The entire json.dumps(result, ensure_ascii=False).encode('utf-8')
  must fit the supplied bound. If complete metadata cannot fit, raise ValueError
  mentioning the budget; never return a truncated inventory as complete.
- This operation creates no source disclosure, edit witness, command or permission.
  Preserve existing module behavior, typing and formatting conventions.

Exact host-supplied source follows, with current identities and ranges. It is
source Context, not a model-selected read. You may select missing authorized source
using native Tools, or submit a source-grounded replacement. Use small exact anchors
from active source. Fixed checks run on admitted candidates; respond to actual
feedback within the finite budget. No reference implementation or hidden oracle
is provided. A successful representation alone does not complete B-0035.
