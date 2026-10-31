# Complete authorized inventory and post-edit continuation

RepositoryCodingHost presents the exact objective first, one complete authorized
resource inventory second, and optional ranked candidates afterward. This is a
mixed-provenance production capability: Qwen authored the accepted Stage A
representation and natural E501 repair; Codex authored integration, lifecycle and
reliability corrections. The rejected gpt-oss prefix edit was not adopted. No live
inference or model-service operation was performed for this implementation.

## Ownership and request lifecycle

`navigation.complete_inventory(scope, editable, maximum_bytes)` derives sorted
metadata from every occurrence in the actual authorized SourceScope snapshot.
It validates currentness, editable membership and complete serialization bounds.
Rows contain relative addresses, content identities, UTF-8 byte sizes and editable
flags, qualified by repository/snapshot identities and `source_acquired=False`.
It discloses no content, absolute roots or unauthorized addresses and grants no
edit witnesses. `task_entry` remains a ranked, explicitly incomplete candidate view.

The host reserves a derived metadata slot during initialization, before source
or check indices can be bound. `prepare_inventory` fills it during preparation
after the currentness gate; construction sends no Prompt or inventory-only
inference. Repeated preparation replaces only this current derived view. Immutable
previously prepared requests retain their original view; native feedback and
original source records remain in their retained positions. Host compositions
append messages rather than replacing or shifting this prefix.

`prepare_navigation` accommodates standalone objective-only input and the host's
objective/inventory prefix, without duplicating candidates. `build_request` stays
pure and assembles all native schemas before byte accounting. Source bindings
and protected feedback indices do not shift during refresh.

Existing `apply` observes the declared resource surface, verifies installed bytes
against the admitted after-image, installs the new scope and rebuilds the index.
The next preparation derives inventory from that scope. Unacknowledged/unknown
effects still refuse continuation; metadata never resolves uncertainty or resets
budgets.

An empty authorized scope can present an empty inventory and terminate without
editing; it grants no editable address. Empty SourceCustody captures/restores zero
paths and rejects foreign expectations. Canonical root and positive limits remain
required. Nonempty repair scopes still require an editable subset.

Representation and complete serialized ModelRequest bounds are both enforced.
The full request includes inventory, schemas, settings, instructions and protected
feedback. Mandatory inventory is not a source disclosure or eligible search
exchange: projection retains it or fails explicitly before model entry. Prompt,
resulting-source, edit-region and disclosure bounds remain distinct.

The host stays within the unchanged 32,768-byte resulting-source ceiling using
small initialization/preparation calls; metadata construction stays in navigation.
No new module, state store, parser, executor, provider or coding loop was introduced.

## Invalidated host source and exact repair evidence

The prior post-edit failure retained stale host-source payloads while correctly
invalidating their witnesses. Native-role protection prevented removal, and newer
protected check/after-image feedback could not fit. The defect concerned active
presentation eligibility, not permission to reuse stale text.

Existing `_source_messages` bindings identify host disclosures independently of
their user role. Projection authenticates original text, path, content identity,
span and snapshot against the bound SourceRangeDisclosureOption even when that
snapshot has expired. Current options still undergo ordinary Context materialization.

Under configured pressure, a same-repository invalidated plain host-user disclosure
can become an explicit `text` omission marker with reason `stale-snapshot`, path
and canonical disclosure identity. Only fields whose values equal canonical
source-feedback fields are removed. Other fields and differing values, including
accompanying instructions, remain verbatim. Unbound user instructions, system
messages, foreign bindings and protected records are not made eligible. Forged
bindings fail. A transformation saving no bytes is restored; selection remains
finite and deterministic in original index order.

Original disclosures and native messages are never rewritten. Omission markers,
historical references and inventory metadata supply no edit witness. After snapshot
invalidation, only current after-images actually selected in an affordable valid
Prompt become active; other source requires authorized reacquisition. Latest check
feedback stays exact. Mandatory protected content that cannot fit still raises
ProjectionCapacityError. There is no automatic Tool replay, effect acknowledgment,
auxiliary call or budget reset. Existing semantic/adaptive compaction is retained.

Read-only reconstruction authenticates all seven historical resources, both snapshot
identities and disclosure identities: the original 43,159-byte request projects to
27,714 bytes with exact protected feedback/current after-image. This is not a resumed
or regraded historical run. A maintained inventory-inclusive neutral process separately
performs a real edit, failing check, selected repair, passing check, archive and
restoration; its post-edit request drops from 33,228 to 15,777 bytes. These deterministic
measurements do not establish local-model engineering competence.

## Collision-safe focused checks

The frozen command combined two distinct `focused.py` files under pytest's default
import mode, producing an import-file mismatch rather than behavioral failures.
FixedCheckTool retained the actual exit/output; it does not own pytest configuration
and must not silently rewrite host commands.

Trusted hosts can explicitly construct `FixedCheck.pytest(name, python=..., root=...,
targets=(...), timeout=...)`. It uses importlib mode so same-named independent modules
coexist. Existing bounded Commands/ToolRunner execute it unchanged. This focused
diagnostic uses `--no-cov`; it is not protected development validation or publication
authority. The global protected profile/coverage threshold are unchanged. Interpreter,
targets, timeout and names remain host-selected, never model-controlled.

Importlib mode does not invent import paths. Legacy oracles relying on bare sibling
imports remain separate independently named commands. The actual original combined
focused shape is preflighted and all eight assertions execute; unchanged withheld
and integration oracles execute separately. Assertions, collection and environment/
launch failures retain actual exit codes or exceptions and command receipts. No
assertions are weakened, files renamed, or failures skipped.

## Acceptance and limits

Maintained neutral and guarded non-Qwen consumers exercise inventory, currentness,
native correlation, source omission, exact failed feedback, repair and custody.
Unchanged public/withheld B-0035 oracles and positive integration predicates verify
complete inventory, candidates, installed-source refresh, idempotence, privacy,
UTF-8 sizes, source authority and explicit overflow.

The [delivery receipt](../research/code-audit/b0035-production-20261031.json) records
final executable identity, physical inputs, command outcomes, source provenance and
publication. Historical Qwen implementation/repair, rejected gpt-oss partial work,
framework interruptions and the new Codex implementation remain distinct. B-0043's
broader lifecycle, durable recovery/evidence, model selection and delegation questions
remain open.
