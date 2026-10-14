# Real semantic-worker runtime: blocked preflight

Approved run `54a77aed2c0212d5dd9b0dacb717d9c7bd72cb11361614aae979fe72ae7c8d2b`
published PACKET at `c40abeed691e82ce4b26afc451b08ae3a7e3398b`, then entered
0020 B/C and 0021 B. The
[invalidation record](../../../source_grounding/invalidations/54a77aed2c0212d5dd9b0dacb717d9c7bd72cb11361614aae979fe72ae7c8d2b/invalidation.json)
records infrastructure failure, no scientific evidence, no retry, no gold and no D.
0022 remains scientifically unentered. The old approval is historical-only.

All 1,630 repository/controller/worker-root files (213,648,067 bytes) were copied
and independently reread byte-for-byte under the ignored archive
`.local/experiment-failures/54a77aed2c0212d5dd9b0dacb717d9c7bd72cb11361614aae979fe72ae7c8d2b/`.
Manifest SHA-256:
`041c9f61cdd6a3f1905b22eb897182b2442a84d31059f368bf3f6921a364d3c5`.
Every original remains in place. Partial model text was used only for operational
file-access and process diagnosis; no treatment or gold judgment was used.

## Progress failure

0020 B failed at canonical filesystem `os.replace` with WinError 5 while replacing
`progress.json`. The worker saved this non-authoritative view before each required
native journal call. The supervisor read it with ordinary Python binary opens,
which do not grant Windows delete sharing. Holding the same kind of reader open
reproduces the exact canonical `FilesystemPermissionError`; writing succeeds once
the reader closes. The historical file has Archive attribute 32, no read-only bit,
and inherited authenticated-user Modify rights. No run-owned process remains alive.
The heartbeat sampled position 61 at 18:17:13.748489 UTC; B exited at
18:17:14.712064 UTC. The precise historical handle owner was not recorded, so
attribution to that observer is a supported explanation rather than captured proof.

An unpublished candidate uses append-only operational JSONL outside scientific
captures, contains observer exceptions, and treats failed convenience snapshots as
telemetry loss. Its local Windows fixture completed 5,000 updates under concurrent
and deliberately held readers. Corrupt/missing telemetry reports unavailable and
never establishes scientific success. Required immutable journals remain fail-hard.
The eight-file candidate is preserved in `.local/semantic-runtime-hardening-candidate/`
and the working tree; it is not a published runtime implementation.

## Real CLI failure and isolation limit

Both old semantic workers received command-policy rejection before their attempted
instruction-read processes could start. Astra tried PowerShell Get-Content and rg;
Sol tried Get-Content, cmd type, and cmd.exe. Both completed a CLI turn with exit 0
and no required review. Exit 0 is transport completion, not authenticated science.
The old launcher ignored user config/rules, selected workspace-write, and never
authenticated an actual Windows runtime permission profile. The policy logs do not
identify the internal rejecting rule; no stronger attribution is claimed.

The actual host is Windows 11 Home 25H2, build 26200.9711, Codex CLI 0.162.1.
The documented MXC startup check succeeds on the host. The old environment
allowlist omits platform directory variables; the native launcher then reports
`cannot locate required Windows platform directory: HRESULT 0x80070003`.
Adding platform directory variables fixes that distinct MXC startup problem.

The [failed live smoke receipt](smoke-failure.json) records one fresh, explicitly
authorized GPT-6 Luna / Medium invocation on synthetic data. It used MXC,
approval never, ignored user config/rules, ephemeral/no daemon, disabled web,
disabled plugins/apps/host skill discovery, root read denial, minimal runtime
reads, immutable input reads and named output writes. Allowed reads and packet
validation succeeded. Three external synthetic sentinel reads and HTTP access
were denied. Inputs remained byte-identical. Both shell and patch writers were
denied creation of the permitted `stage_c_review.json`; builder build/verify and
artifact authentication therefore failed. This receipt is **FAIL** and cannot
satisfy a future plan preflight.

Three non-model host probes distinguish the remaining limit:

| Write grant | Required new review | Unauthorized extra file | Frozen input |
| --- | --- | --- | --- |
| Workspace read + relative named-file write | denied | denied | denied |
| Workspace read + absolute named-file write | denied | denied | denied |
| Workspace write + input read carveout | written | written | denied |

The tested CLI cannot simultaneously create new flat named artifacts and enforce
the requested output-only write boundary. Existing frozen builders create files
exclusively and reject preexisting outputs, so precreating placeholders would alter
their contract. Broad workspace writes do not satisfy the requested boundary.
No bypass, full host access or weakened blindness was selected. Work stopped at
this gate: no nested live smoke, replacement cohort, replacement Stage A, new plan,
new approval or scientific run was created.

Official guidance describes permissions and Windows implementations:
[permission profiles](https://learn.chatgpt.com/docs/permissions) and
[Windows sandbox](https://learn.chatgpt.com/docs/windows/windows-sandbox).
Those documents establish supported intent; the real probes above establish this
installed runtime's observed limit. CLI configuration and tool isolation are
expected to be model-independent, but a failed Luna receipt cannot justify any
Sol/Astra launch.

## Required next action

Resolve the new-file permission limitation with an enforceable runtime that keeps
the flat frozen builder and output contract unchanged. Then repeat authenticated
direct and nested Luna synthetic smoke, finish the retained engineering candidate
and required regressions/protected validation, and only afterward freeze the fresh
cohort and an unapproved plan. Do not retry 0020/0021 or reuse the old approval.
