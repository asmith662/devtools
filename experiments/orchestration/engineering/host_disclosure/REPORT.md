# Engineering validation and live smoke V2

Starting synchronized main: `f25daa62edc8a79584aca4347fa58d86ede865f6`.
The 14 tracked and six untracked retained candidates matched their ignored archive
byte-for-byte before editing. The earlier eight-file archive and all 235 files in
the failed host-disclosure smoke archive were reauthenticated unchanged.

## Real runtime evidence

Installed `codex-cli 0.162.1`; engineering model GPT-6 Luna / Medium.
Exactly two new invocations, zero automatic model retries, zero Sol/Astra calls,
zero scientific execution. Both actual callers use `workers.semantic.primary`:

| Path | Fresh thread | Result |
|---|---|---|
| Direct C | `01a13c17-bb33-7cf3-a71a-070975686121` | PASS |
| Nested B grounding | `01a13c17-e04f-7390-8a01-0b7880656928` | PASS |

Both copied the fresh synthetic full-source quote exactly. The host derived
`[0,48)` in the original canonical span convention. Each schema passed, every
locator resolved, every scientific-format builder/validator passed, and all seven
synthetic artifacts authenticated. Both transcripts show zero tools; empty model
CWDs stayed empty. Three unique synthetic parent/sibling/repository sentinels were
absent from disclosure, full retained streams and final response. Web/network,
shell/tools, plugins/apps and prior session/config/rules remain disabled.

[`smoke-receipt.json`](smoke-receipt.json) SHA-256:
`ddf86e8b45f31ff4a2e531e8050e63df1fe26615e9e7acaea44b7752e3b888f2`.
It embeds exact runtime/adapter/locator/schema/builder bindings, permissions,
synthetic packet/instruction/input/final digests, usage, both invocation receipts
and artifact hashes. Compatibility authentication passes against unchanged runtime
bytes. Transport/sandbox properties are assumed model-independent CLI/runtime
properties; semantic quality is model-dependent and no routing-verification claim
is made. The receipt is engineering evidence, never gold or execution authority.

Ignored full success archive: `.local/host-disclosure-smoke-v2-success/`, 251 files,
6,216,534 bytes, byte-verified manifest SHA-256:
`3e1675f8d25f32e9c7d7717c3d04d92a96fff2d844b9066a97fc8d61683af9ab`.
Original temporary workspaces remain preserved. Prior successful direct and failed
nested smoke captures remain unchanged; the failed `[0,46)` response over a
41-character source was neither repaired nor retried.

## Deterministic validation

All 148 controller test cases are covered successfully, including 31 locator
regressions, strict final extraction, authority/dead-attempt/publication controls,
process lifecycle, compact/verbose/follow and telemetry tests. The initial combined
run had 224 passes and two frozen-implementation mismatches while implementation
formatting overlapped authentication. Both affected cases passed after bytes were
frozen; all 11 approval-mutation cases also passed separately. No authority check
was relaxed. Two additional no-repair tests passed independently.

Source-grounding contracts: 74; runtime callers/designation restriction: three;
static scope/materialized payload/maintained defect/operational bridge: four.
The final focused combined run passed 129 cases before the two extra locator
regressions. Exact WinError 5 sharing reproduction and 5,000 concurrent append
updates passed. Failed observation cannot stop the child or create RETURNED.
Corrupt/missing telemetry is unavailable; scientific journals remain fail-hard.

Scoped Ruff, formatter and strict mypy pass for maintained source; supported-source
strict mypy checks 445 files. Source-grounding generated PREPARATION/PACKET payloads
are excluded by explicit ownership while maintained-source F821 defects fail.
Protected development ran once: 1,588 passed, two expected skips, 100% branch
coverage (10,453 statements / 2,550 branches), confirmation excluded before
collection. Worktree and staged diff checks precede publication.

No production source, framework abstraction, hypothesis, semantic label, witness
methodology or retry authority changes. Cases 0020/0021 remain invalidated and dead;
0022 remains scientifically unentered. Replacement scientific authoring and a new
unapproved plan are separate later checkpoints, conditional on this publication.
