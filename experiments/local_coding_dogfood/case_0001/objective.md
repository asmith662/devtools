Fix `stockroom.projection.project_stock` for retried event delivery.

Required behavior:
- Preserve the public signature and use the package's canonical warehouse/SKU semantics.
- Within one call, a delivery identity is (canonical warehouse, exact opaque event_id).
- An identical repeated delivery contributes its delta only once, including differently spelled equivalent warehouse/SKU keys.
- The same delivery identity with a different canonical SKU or delta raises ValueError.
- Identical IDs in different warehouses are independent. Event IDs are case-sensitive and whitespace-sensitive opaque strings.
- Accept a one-pass iterable; preserve unrelated initial entries, zero entries and legitimate negative quantities/balances.
- Return an independent dict and never mutate the input mapping, including when a later event conflicts. Replay state is local to the call.

Only `stockroom/projection.py` is editable. Read the admitted source modules before proposing an exact replacement. Do not edit tests, other files, branches or Git state. Focused checks are immutable; a separate frozen held-out oracle grades the archived candidate after completion.

Use native tools, not fenced-code patches or shell commands. `read_source` ranges use zero-based Python character offsets with exclusive end. Read the complete events.py, keys.py and projection.py modules to satisfy host readiness. The file manifest supplies exact lengths. `replace_source` requires a unique old_text anchor actually acquired from current source. Read and edit calls belong in separate batches. `validate_candidate` and `inspect_and_validate_change` run host-fixed checks; neither accepts a command. The latter also inspects repository changes and scope. You may request it when useful. Ordinary check results are returned automatically after an admitted edit, with one bounded repair opportunity. A final prose claim is not acceptance evidence.
