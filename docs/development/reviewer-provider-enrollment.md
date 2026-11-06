# Bounded local reviewer-provider enrollment

The operator approved the exact prospective enrollment scope
`9722f98db396dc350bfed68c057a545e1eacfe0ebe44e62cb66e6ec88f189d1f`
in response to the reviewer-model comparison. Implementation does not itself
activate that permission. The final research receipt records validation,
operator response, activation and actual service effects separately.

`routine-development-policy-v4` extends the existing
[local-work owner](routine-local-work.md), not framework governance or agent
architecture. The [reviewed policy](routine-reviewer-policy.json) preserves the
global native Qwen provider, output ceiling, attempts, protected gate and Git
rules. Earlier v1/v2/v3 policies and immutable decisions remain readable.

Each local `scope.profile` now selects an explicitly enrolled provider, allowed
roles and finite budgets in `local.provider_profiles`. Every listed profile must
have exactly one entry. Existing ordinary local limits remain unchanged; the
two enrolled reviewer profiles permit at most 8,192 output tokens and 600 seconds
per call. Actual grants narrow those limits, bind exact public source and plan
identities, and reserve aggregate output before effects. Provider qualification
must match the selected profile before every call. Native authorization continues
to use the separate global provider. No model name appears in shared Context,
WorkCycle selection logic or the reviewer protocol.

Role and resource narrowing apply to both the acting role and delegable roles.
A child cannot change profile, task, source identities or budgets to escape its
parent. Revocation/replacement invalidates the old authority at the next boundary;
consumed calls and historical decisions remain spent. Strict review delivery and
factual host assessment are unchanged. Adapter-specific settings remain captured
but are not silently made acceptable to the native conclusion validator.

The profile map authorizes bounded **inference**, not service mutation. The
operator's exact enrollment scope separately permits the trusted supervisor to
use existing ModelServing/Command owners for an idle-only sequential GPU swap:
pause the authenticated Qwen container, run only the pinned cached gpt-oss profile,
stop only that owned temporary service, and restore the same Qwen container with
identical image, mount, command and 64K configuration. It does not authorize
downloads, paid providers, arbitrary cache deletion, changing Qwen configuration,
concurrent overcommit, native task dispatch or source installation. Check custody,
other active work, actual memory and readiness at each boundary. A failed or
ambiguous lifecycle operation requires reconciliation, not blind replay.

The fixed enrollment uses loopback ports 8080/8081. Additional endpoints,
providers, roles or larger limits require explicit policy replacement. Neither a
worker Tool nor delegation can enroll a model or acquire serving permissions.

Reviewer instructions, Tools, conversation, source disclosures and task-local
working notes remain host-owned and independent of a server's KV cache. When
sharing the GPU sequentially, reconstruct the same role's authorized Context and
reauthenticate the loaded profile; never substitute the coder's private
conclusions for independent review. This adds no scheduler, memory database or
automatic agent-selection mechanism. Durable role-specific lessons remain a
separate, evidence-backed playbook-promotion direction.
