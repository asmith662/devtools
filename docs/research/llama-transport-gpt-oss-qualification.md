# llama.cpp transport repair and GPT-OSS qualification

The Devtools HTTP defect is corrected. GPT-OSS native conclusion delivery remains
unqualified: the captured failure combines a pinned llama.cpp grammar limitation
with generated output that names a constraint instead of a Tool recipient.
Parsing that output as ordinary content would not make it a valid review Tool
call. No failed generation is converted into a successful ModelResponse.

This follows the [published reviewer-model comparison](reviewer-model-comparison.md)
at `27c8470e5335063eac50b1af60b94bcf33e476c0`. Historical requests, judgments,
consumed grants and missing-response records remain unchanged.
The bounded [diagnosis record](code-audit/llama-transport-gpt-oss-20261106/diagnosis.json)
binds the inspected request, rendered prompt, server log and pinned upstream
source hashes; it does not duplicate or regenerate the historical archive.

## Transport correction

`_parse_http_headers` now splits only the first two literal spaces. It validates
HTTP/1.0 or HTTP/1.1 and three ASCII status digits, while allowing an empty or
multiword reason phrase and its permitted bytes. The old unbounded whitespace
split rejected a legitimate `500 Internal Server Error` as malformed framing.
This implements the relevant [RFC 9112 status-line syntax](https://www.rfc-editor.org/rfc/rfc9112.html#section-4),
without adding streaming semantics or permissive JSON recovery.

All three response-body paths (Content-Length, chunked and connection-close)
now enforce an 8 MiB ceiling before unbounded allocation. Existing header/line
limits remain. HTTP failures within these bounds raise `LlamaCppHttpError`
with their authentic numeric status and at most the existing 1 KiB diagnostic
prefix. Oversized or incomplete framing remains a response error. Failed HTTP,
malformed model payloads and invalid Tool arguments remain distinct failures.
See the maintained [adapter contract](../../src/devtools/models/interaction/docs/overview.md).

New reproductions initially produced 12 failures and one pass. After correction,
164 adapter tests passed; the affected ModelInteraction package passed 273 tests
with 100% adapter statement and branch coverage. Coverage includes valid success,
multiword/empty reasons, 4xx/5xx, malformed versions/digits/separators/control
bytes, body boundaries under each framing, incomplete bodies and bounded error
diagnostics. An overbroad recovery selection also produced collection errors:
it selected a subprocess-only audit-hook helper as a test module. Those errors
are preserved locally; explicit maintained-package selection passed. No unrelated
validation-owner change was made.

## Exact native-format failure

The archived [failed call](code-audit/reviewer-model-comparison-20261105/qualified-gpt-oss/gpt-oss-native-C01-r2/1/request.json)
contains native system/user messages and the ordinary OpenAI-compatible
`read_source` and `submit_review_proposal` schemas. Its top-level keys are
`model`, `messages`, `stream`, `max_tokens`, `tools`; neither `response_format`
nor `tool_choice` was sent. Existing [rendered templates](code-audit/reviewer-model-comparison-20261105/gpt-oss-rendered-initial.json)
and successful correlated Tool calls demonstrate template/serialization
functionality, not universal output reliability.
The exact failed-case rendering includes the functions namespace and proposal
declaration, native medium reasoning and a commentary-channel instruction.
The API system instruction becomes a native developer message under GPT-OSS's
template. No constraint token occurs in that rendered input; the rejected
constraint appears in generated output.

The server logged this rejected header:

```text
<|channel|>final <|constrain|>submit_review_proposal<|message|>
```

In the pinned [GPT-OSS parser](https://github.com/ggml-org/llama.cpp/blob/304665fe7/common/parsers/gpt-oss.cpp),
ordinary final content has no optional constraint suffix. A separate constrained
final branch requires a response-format schema, absent here. Native Tools require
a `to=functions.NAME` recipient in the role or commentary/analysis header;
this generated header supplies none. Auto Tool selection uses a lazy grammar
triggered by recipient syntax, so advertising a Tool does not force generation
down that branch. The incompatibility is already visible before JSON arguments
or factual review are considered.

The [complete-response PEG caller](https://github.com/ggml-org/llama.cpp/blob/304665fe7/common/chat.cpp)
throws on unsuccessful parsing. The retained [server log](code-audit/reviewer-model-comparison-20261105/gpt-oss-final-logs.json)
records the rejected suffix and server error code 500. Devtools then masked that
server failure with its status-line bug. The original failed response's exact
HTTP headers/body and complete generated reasoning were not captured; they are
not reconstructed or relabeled as a received ModelResponse.

Upstream [issue 31520](https://github.com/ggml-org/llama.cpp/issues/31520) and
[merged PR 31556](https://github.com/ggml-org/llama.cpp/pull/31556) address the
same missing final-constraint grammar facility. The patch accepts that suffix
as ordinary content. Its tests cover other constraint names, not this exact
captured Tool-named response; no patched runtime was tested here. This is strong
source-level mechanism evidence, not a new native-parser execution. Issues
[27720](https://github.com/ggml-org/llama.cpp/issues/27720) and
[25321](https://github.com/ggml-org/llama.cpp/issues/25321) concern different
malformed headers and do not establish this failure's cause.

Even accepting the header as content would leave independent problems. The
[diagnostic-only JSON extraction](code-audit/reviewer-model-comparison-20261105/server-output-diagnostic.json)
lacks `subject_sha256`, uses invalid finding-kind values and combines the genuine
empty-heading defect with an unsupported additional claim. It was neither
admitted nor executed. Tool transport, schema/reference admission and factual
correctness remain separate qualifications.

## Qualification boundary

| Previously captured GPT-OSS case | Native delivery | Independent limitation |
| --- | --- | --- |
| Defective C01 inspection | `read_source` delivered | Does not establish conclusion delivery |
| Correct C02 inspection | `read_source` delivered | Does not establish conclusion delivery |
| Defective C01 conclusion | Plain content JSON, finish `stop` | Correct defect judgment; no native proposal |
| Correct C02 conclusion | Native `submit_review_proposal`, finish `tool_calls` | Unavailable structural references prevent strict admission |
| Repeated C01 inspection | Server PEG failure, then masked client framing error | Consumed failure; no ModelResponse or retry |

Those five historical calls took 20.27, 25.54, 8.03, 9.03 and 52.83 seconds
respectively. Four returned usage; the failed call has no received usage or
termination reason. Server timing around 103 generated tokens/s is historical
performance, not a new stability measurement. No model is promoted from these
observations.

The active v4 policy and [separate enrollment scope](../development/reviewer-provider-enrollment.md)
permit fresh bounded local grants and explicitly reusable sequential serving
for the enrolled profiles. Prior completed transitions and spent grants cannot
be replayed. Any new entry must use a fresh intent, current provider/source
checks and a fresh automatic grant. A safe-resource condition is still required;
authority alone does not establish resource safety.

Initial and final preflight record insufficient commit headroom. The prospective
six-call packet is therefore **not entered**; the final resource check failed.
No alternate service has started and no inference grant has been consumed in
this task. The existing Qwen container remains running unchanged.
The [admission record](code-audit/llama-transport-gpt-oss-20261106/admission.json)
retains the authority boundary, proposed finite packet and zero-call disposition.
No unused historical grant or completed serving transition was replayed. Artifact
requalification was not entered after this resource refusal; the enrolled hash
is identified without claiming a fresh 12 GB artifact hash in this task.

The [initial detailed sample](code-audit/llama-transport-gpt-oss-20261106/memory-before.json)
records 1.29 GiB available physical RAM, 116.41/127.73 GiB system commit and
11.32 GiB commit headroom. Commit peak reached the limit. The 96 GiB page file
has 20.76 GiB currently used and 33.50 GiB peak use; commit charge is **not**
page-file occupancy. Values come from Windows `GetPerformanceInfo` and
[`EnumPageFilesW`](https://learn.microsoft.com/en-us/windows/win32/api/psapi/ns-psapi-enum_page_file_information),
not estimates from GPU loading. The Qwen-loaded GPU has 14,714 MiB used and
1,337 MiB free of 16,376 MiB. These are samples, not new GPT-OSS run peaks.

Once safe, the bounded qualification should pair three minimal `read_source`
controls with three unchanged `submit_review_proposal` schema requests, one
generation each, using the enrolled artifact/template and fixed literal
transport-only payloads. No proposed Tool is executed; no acceptance/custody
record is fabricated. Capture rendered requests, correlated IDs, raw HTTP before
parsing (including failures), server logs, completion/usage and sampled memory.
Score native recipient delivery, schema conformity, literal identities and
termination separately. Require at least 2 GiB available physical RAM and
16 GiB commit headroom before any pause; stop at 1 GiB/8 GiB during execution.
These conservative admission guards reserve room for the approximately
11.3 GiB artifact and restoration; they are not measured minimum requirements
or a claim that the profile is otherwise stable. Restoration must return the
same Qwen container/configuration; do not upgrade llama.cpp during qualification.

The [final sample](code-audit/llama-transport-gpt-oss-20261106/memory-final.json)
after protected validation has 2.50 GiB available RAM and 12.07 GiB commit
headroom (115.66/127.73 GiB committed). Physical RAM clears the start guard;
commit does not. Current page-file use is 21.22/96 GiB, with the same 33.50 GiB
peak; GPU memory remains 14,714 MiB used / 1,337 MiB free. No competing process,
cache, WSL setting or page-file configuration was changed to make admission pass.
There is no new alternate-run latency or memory-peak measurement.

## Publication checkpoint

Transport source/tests/package documentation are committed at
`9034fd34ad8510be8e058c95203291d09b0e45d3`. The protected profile passed once
on that committed candidate: **4,496 passed, 2 opt-in skips, 100% production
branch coverage**, 4,687.06 seconds managed wall time, exit 0. Before/after
declared executable inputs match; all 13,507 phase observations and complete
local receipts are retained. The [validation summary](code-audit/llama-transport-gpt-oss-20261106/validation.json)
binds their hashes and the unchanged 7,200-second managed deadline. Strict mypy
(646 source files), maintained Ruff/formatting, layout, links, Git object
integrity and diff checks also passed. Evidence-only closeout reuses this gate;
it does not repeat it. No persistent service, standing policy, native attempt,
Inspector or learned-intelligence worktree is modified.

## Decision

GPT-OSS is **not ready for a larger acceptance-review qualification**. The exact
server parsing limitation is identified and the misleading transport diagnosis
is repaired, but reliable native proposal delivery, real structural-reference
admission and safe host-memory headroom remain unqualified. Working-note or
reviewer-framework expansion would not resolve these blockers.

The next action is to establish safe host commit/RAM headroom without disturbing
unrelated work, then enter the bounded Tool-control/schema comparison under fresh
existing authority. If testing a server with PR 31556 is selected, separately
enroll and qualify its exact alternate-provider image pin; keep persistent Qwen
unchanged. A successful plain-content parse still cannot count as Tool delivery
or accurate review, and no production reviewer promotion is justified here.

## Capacity follow-up: 6 November 2026

The follow-up identifies substantial **non-model** commitments. It does not
enter the six-call experiment or change its guards, serving profile or scoring.
The [bounded capacity record](code-audit/gpt-oss-capacity-20261106.json) binds
20 retained local diagnostic receipts; the original comparison and transport
receipts are unchanged. No production executable inputs change.

### Owners and measurements

| Owner / counter | Private commitment or pool use | Working set / other observation |
| --- | --- | --- |
| NordVPN.exe, PID 21468 | 31.99–32.01 GiB private | About 2.12 GiB working set; started 14 October |
| vmmemWSL, PID 46260 | About 16.93 GiB private | About 0.54 GiB working set |
| svchost.exe, PID 3624 | About 7.97 GiB private | About 0.93 GiB working set; SCM identifies **Winmgmt** |
| PyCharm, PID 28016 | About 3.62 GiB private | About 2.34–2.38 GiB working set; user-owned editor |
| Windows paged pool | 19.74 GiB | Allocation owner/driver not identified |
| Windows nonpaged pool | 3.29 GiB | Allocation owner/driver not identified |

The aggregate process-private sample is 86.72 GiB across 412 processes. Adding
the separately sampled paged/nonpaged pools gives approximately 109.75 GiB,
compared with a 116.58 GiB system-commit sample. This accounts for most of the
pressure without an exact, atomic reconciliation of shared/system commitments.
Working sets are not unique RAM totals, and private commitment is not current
page-file occupancy. These counters follow Microsoft's
[memory-accounting distinctions](https://learn.microsoft.com/en-us/windows/win32/memory/memory-performance-information).
Large allocations are observed; a leak, allocation stack or common cause has
**not** been established. In particular, the kernel pool is not attributed to
NordVPN or WMI merely because those processes are large.

Only Qwen is running in Docker. Its displayed usage is 461.1 MiB after Docker's
inactive-file adjustment; the cgroup reports about 0.97 GiB including about
0.28 GiB anonymous and 0.69 GiB file memory. No per-container memory limit is
configured. Docker's WSL VM exposes 15.48 GiB total, and the Linux guest reports
14.07 GiB available; guest swap use is about 39 MiB out of 4 GiB. Host VM
commitment, guest availability and GPU allocations are different measures.
The large host VM charge therefore does not establish that Qwen's live CPU
allocations consume all that commitment or that guest-free pages can safely
be recovered as host commit. WSL is 2.5.10.0; no user `.wslconfig` exists. No
Docker/WSL settings, cache or lifecycle was changed. The only stopped container
is an unrelated old vLLM container reporting zero usage; deleting it would not
recover measured live memory.

The active Windows page file is `C:\pagefile.sys`, 96 GiB allocated, about
20.96 GiB used at the final sample, with 33.50 GiB peak use. Registry
`PagingFiles` is `?:\pagefile.sys`; its automatic-management flag could not be
queried. WMI-dependent CIM queries and `tasklist /svc` failed with requested
object errors (CIM HRESULT `0x80010114`). Direct SCM inspection succeeded and
identified Winmgmt as running in PID 3624. This establishes the process owner,
not a diagnosis of global WMI corruption. One page-table counter was unavailable;
all six retained performance-counter samples have status zero. No usable
pool-tag result was obtained and no debug privilege or driver instrumentation
was enabled. Further driver attribution requires a supported administrative
method such as [PoolMon](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/using-poolmon-to-find-a-kernel-mode-memory-leak).

### Admission and remediation

The final sample at **21:03:57 UTC** has **0.91 GiB available physical RAM**,
**117.70/127.73 GiB committed**, and **10.03 GiB commit headroom**. Commit peak
equals the limit. GPU memory remains 14,714 MiB used and 1,337 MiB free of
16,376 MiB. Both entry guards fail; available RAM is also below the 1 GiB
in-experiment stop floor. No inference or serving transition is safe here.

No clearly owned completed temporary resource was found to release. The completed
protected driver no longer exists; all current Python processes together account
for only about 99 MiB private memory. Inspector and the learned-intelligence
worktree remain untouched. **Zero resources were released, zero fresh grants
issued, zero generations entered, and no new Tool/schema/parser results exist.**

The active policy remains
`4fe32fc6bd33762ce7b166fc8031e16a7bcd7584c1d9c65676a280983e0b78a9`.
The existing enrolled profile and reusable sequential transition remain
authorized. Eligible inference would receive a fresh exact-scope automatic grant
through `WorkCycle.routine.local`, without a per-run operator prompt. Resource
failure prevents entry before any grant, model load or service stop; no consumed
operation is replayed. Qwen's original container, image, mount, command and 64K
configuration match the previous receipt and remain healthy and idle. Its start
time remains `2026-11-06T03:49:59.986796034Z`; restoration is unnecessary because
it was never paused or restarted.

The smallest concrete remediation is **operator/security-owner inspection and
controlled graceful restart or repair of NordVPN**, after checking VPN/network
and protection requirements. Its roughly 32 GiB private charge is the largest
identified potential recovery; no amount of recovery is guaranteed. Windows
administration should separately investigate the 8 GiB Winmgmt process, failed
WMI queries and large kernel pools, with service dependencies preserved. None
of these are completed Devtools resources or authorized automatic cleanup.
Do not kill services, disable protection, change the page file, reboot WSL or
clear model caches to make admission pass. WSL memory-policy review is a separate
owner action if still needed; its settings and restart effects are documented
by [Microsoft](https://learn.microsoft.com/en-us/windows/wsl/wsl-config).

After remediation, remeasure the unchanged 2 GiB physical / 16 GiB commit guards,
then reauthenticate custody, provider and authority before the existing packet.
GPT-OSS remains unqualified for a larger reviewer evaluation. This follow-up
adds no new model-quality or native-delivery measurement, and reuses the
published protected transport validation without another comprehensive run.
