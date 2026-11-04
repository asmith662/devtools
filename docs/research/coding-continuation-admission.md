# First B-0033 live-continuation admission measurement

**ADMISSION REFUSED before any child, grant or model call.** This is an admission
measurement, not a new failed coding episode. Infrastructure and policy were unchanged.

## Authenticated state and recovery

Canonical and remote `main` matched `c85982b0d2df65ed92219e2e1815e914273ac592`.
Policy `08fcfcbfda2e51db7a7fb61a5cdd923deec75ebbff4cdad4b8e9f4520fa33662`
remained active with two total attempts. B-0051 remained reviewed BACKLOG with
one consumed original attempt, no child directory and no Checkout owner.

| Original identity | Value |
| --- | --- |
| Assignment | `47a414bee5aaba90ee1ecdcb1795e4563f153c14e20b99392fad2505ceff391c` |
| Result | `0d3cf5f97dba9561e5d448611024d4ab753320ed1cb4a10ff8b61bbd0ab100b2` |
| Historical grant | `1a5d65819a57918783af5f90f791148f657819ac6664dc389d2b33a81ef9b86f` |
| Checkout release | `9979b03270ed4e3cf96ea81c45eac45fb7245f08d630d863bf100197864a9f16` |

The original outcome remains BLOCKED / `proposal_limit`, completed with known,
acknowledged effects, restored source and authenticated release. Its 35
observations authenticate within the historical grant interval. Candidate/diff
identities authenticate; all 44 original episode files match the published
archive byte-for-byte. An additional 22 forensic files were inventoried and
preserved. Historical counts remain five model calls, four source acquisitions,
three attempted proposals and two admitted edits.

The [frozen public input](code-audit/native-scope-followup-20261101/public.py.txt)
and retained local copy match the published freeze manifest:

- Path: `tests/live_native_scope_followup_public.py`; 18,070 bytes.
- Raw SHA256: `7de45c1583dc96faeaec5ff09bc263ae649f28751cc6dfd3a0b08402cdc016aa`.
- Assignment content identity: `1f4495ac7bbda0bc6726efaf33fb0b7f1b6d0ca2f7f4304b9d792fc9410859db`.

The native owner's Intake writer serialized exact BinaryFile recovery.
`NativeMaintenance.validate` passed; all four original input identities matched.
Original source and obligations had not drifted. No assertions or acceptance
semantics changed. After refusal, the same owner verified the bytes and removed
its temporary public file, restoring the initial materialization state.

## Refusal and remaining constraint

The [continuation owner](../../scripts/backlog/native/continuation.py) scans all
Checkout-history JSON records. It raised `ValueError: Work receipt identity/schema mismatch`
on `cf08541a94353e4bac7e976c7d48d8b10dff33333f383a1480724cbd9082c07b.json`.
Schema is `backlog-checkout-owner-v1`; the stored payload digest is
`cf08541a94353e4bac7e976c7d48d8b10dff33333f383a1480724cbd9082c07b`, but the
existing digest function computes
`bd81640718eff29216d17152a7def7a9244e7a9997de5ab285c2e1531f8c5d05`.
Its operation is
`offline-proposal:e0aeda523f488d82c08cf2b6a8e050e472d5dcf18d5eb1dce2e6e0dabc672284`.
The cause is not established. The receipt was preserved. B-0051's own release
authenticates independently.

Separately, current eligibility accepts only codes 0/1 across all prior public
checks. B-0051's codes are **2, then 1**: an admitted edit caused SyntaxError
during collection, subsequently removed; the next public run reported two
failed and 19 passed, including NameError. Private acceptance was never entered.
See the [original episode](native-scope-followup.md). This existing exit-code
rule would still refuse the history after receipt reconciliation. Historical
records and eligibility rules were not changed.

## Disposition

No child identity or fresh grant exists. New Qwen calls, source acquisitions,
edits, checks and review calls are zero; new inference tokens/timings are not
applicable. `submit_review_proposal`, host candidate disposition and Integration
planning were not entered. The original slot remains consumed and the second
unused. B-0051 remains BACKLOG, B-0033 ACTIVE and B-0053 CLOSED.

Receipts: `.local/validation/b0033-b0051-live-admission.json` and
`.local/validation/b0033-b0051-parent-authentication.json`. Qwen health returned
`ok`; provider configuration, Inspector and historical evidence were preserved.
No comprehensive suite was rerun for this unchanged-code measurement.

The strongest immediate blocker is Checkout-history integrity authentication.
The next bounded action is reconciliation through that receipt's existing owner,
followed by explicit assessment of eligibility for the known, recovered
collection failure. This measurement authorizes neither action.

## Subsequent authenticated cause and correction

The later authorized investigation identified the producing historical cleanup
script, `.local/finish-offline11.py`. It assigned the sealed `_load(owner.json)`
result directly to `Checkout.record`, retaining its `sha256`. The old finish
implementation at `772d965d8a037b126219b94af647ffb59d382334` then hashed a
completion payload containing that old seal, overwriting the seal in its output.

Removing completion fields reconstructs owner digest
`964e9db05f3737acc46ed704e8d64595b97ff1fc388d142d22c01dd517105281`.
Including that value as `sha256` in the completion payload reproduces the stored
`cf08541a...` exactly. This identifies a historical double-sealing/capture defect;
no receipt was rewritten. The physical file SHA256 remains
`21097db674da2f78fc06d269f5e41e4cc6b29dfc3d251dbb4f6a7edb213226c1`.
The bounded derivation is retained in
`.local/validation/b0051-receipt-double-seal-proof.json`.

Checkout's existing trust contract is an active fenced owner and independently
authenticated operation release, not a global release chain. The correction
centralizes exact restored-release validation for native candidates and
continuation, while `work-history` separately reports all invalid historical
receipts. A sealed in-memory payload now refuses finalization.

B-0051's edit/check observations show acknowledged digest changes before both
checks. Its final archived candidate matches the second edit and final ordinary
failure; no edit followed that check. The corrected classification admits this
known terminal public failure, while refusing unrecovered collection failure,
unknown errors/effects and stale candidates. The standing two-attempt policy,
original failure records and acceptance implementation remain unchanged.

Live execution is a separate phase after validation and publication of this
correction. The original no-go above remains the result of the earlier admission
measurement and is not retrospectively changed into a coding episode.

The correction's focused validation passed 119 tests, including Checkout,
continuation and native compatibility. Ruff, formatting, strict mypy (634 source
files), layout and diff checks passed; the parent inventory and malformed receipt
remained unchanged. The exact committed candidate requires protected validation
before publication and live entry.
