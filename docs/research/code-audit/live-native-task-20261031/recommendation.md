# Exact Intake review recommendation

Proposal: ff4c4110-9c3b-480d-8f0f-77cf4610b700 (original provenance retained).
Baseline main: fd6af0d951a57718233680a971d135b415e160e4.

Approve backlog publication only for the remaining narrow obligation:

When a package facade directly imports a function at module scope, an import of
the same name confined to an unrelated function, async-function or class
namespace must not prevent the existing one-facade resolver from resolving the
module reexport to its exact implementation declaration. Imports in module-level
conditional/try blocks, actual competing module bindings, star imports and
ambiguous target bindings must retain their existing conservative behavior.
No runtime import execution, general scope evaluator, new public API or registry.

Only editable implementation: src/devtools/context/python/imports/members.py
(21,395 bytes). Readable implementation dependencies may include the existing
module binding-name helper. Public diagnostic file:
tests/live_native_facade_public.py (temporary, explicitly invoked; archived as
text after the episode, never installed as a production change).

Genuine baseline evidence: three public local-namespace regressions fail and four
module-binding controls pass. Independent withheld criteria have six expected
baseline failures and twelve passing/neutral controls. All fixtures are tiny
authored retained source strings; no fixture source is executed. Exact target
declaration, source/snapshot provenance, aliases, deeper local nesting and
preservation of module-scope refusals are acceptance subjects. The private
implementation remains outside worker/reviewer read scope. No reference patch
has been written.

Selection rationale: this is a current supported RI false negative, in one
existing bounded file, with a small reproducible causal input difference and
real downstream use through imported-member/reference resolution. It exercises
Python namespace understanding while preserving the already delivered competing
binding repair. The original proposal's broader pressure and history are not
erased or declared fully closed by this episode.

The suggested SQLite, drive-relative, dangling-entry and Codex prompt leads have
current implemented guards/regressions; they are not eligible repair replays.
B-0035 remains closed; B-0048 and its consumed historical slot are excluded.

If approved/published, execution still requires separate exact native coding and
review grants. Proposed coder: existing Qwen3.8-27B, eight calls, six acquisitions,
three proposals/two repairs, 2,048 output tokens, 120s/call, 900s total. Proposed
reviewer: separately provisioned Qwen session, three calls/two reads, 2,048 output
tokens, 120s/call, 360s total. Thinking disabled is proposed. Native v1 currently
permits portable settings only; actual unchanged server sampling must be disclosed
and approved rather than silently replaced or assumed optimal. No service change,
download, paid fallback, automatic installation, candidate publication or backlog
closeout is requested by this Intake decision.

Default is No. Use the real interactive Intake review and promotion prompts.
The assistant will not type an affirmative response or fabricate approval.
