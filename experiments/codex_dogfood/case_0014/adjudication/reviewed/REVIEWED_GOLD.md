# Case 0014 reviewed development gold

Provenance: PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. One primary review; no reconciliation or second reviewer.

# Case 0014 primary semantic review

MODEL = GPT-6 Astra; REASONING = High.

One primary adjudication with a separate self-review pass. All 515 resources and six mandatory obligations were assessed: 3,090 final cells, no unresolved judgments.

## Exact task

Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.

O1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.

O2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.

O3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.

O4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.

O5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.

O6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.

## Task-clause audit

O1 captures opt-in completed-result renderer; O5 captures deterministic human-readable domain API. Every substantive task clause is covered.

| Obligation | Applicability | Coverage | Satisfaction criterion |
|---|---|---|---|
| O1 | MANDATORY | ADEQUATELY_REPRESENTED | Accurately present existing completed-result fields through a pure opt-in renderer. |
| O2 | MANDATORY | ADEQUATELY_REPRESENTED | Both streams remain original bytes; diagnostic decoding and its loss are explicit. |
| O3 | MANDATORY | ADEQUATELY_REPRESENTED | Correct zero/default/custom display behavior independent of existing retention. |
| O4 | MANDATORY | ADEQUATELY_REPRESENTED | Accurate event-loss diagnostic and preservation of completed-result acceptance boundary. |
| O5 | MANDATORY | ADEQUATELY_REPRESENTED | Public domain-local integration compatible with existing facade and immutable structured contracts. |
| O6 | MANDATORY | ADEQUATELY_REPRESENTED | Regression coverage and documentation in designated locations without weakening the protected profile. |

Future behavior is task-backed; current representation, completion, retention, facade and validation facts require retained repository evidence.

## Cell counts

| Obligation | REQUIRED | HELPFUL_ONLY | UNNECESSARY |
|---|---:|---:|---:|
| O1 | 4 | 12 | 499 |
| O2 | 5 | 4 | 506 |
| O3 | 6 | 5 | 504 |
| O4 | 9 | 6 | 500 |
| O5 | 6 | 2 | 507 |
| O6 | 4 | 18 | 493 |
| Total | 34 | 47 | 3009 |

## Complete REQUIRED-resource union

18 resources. Membership means necessary in at least one minimal complete witness; it does not mean all listed resources must be read together.

- **RSC001**: `AGENTS.md` — `953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d`
- **RSC055**: `pyproject.toml` — `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0`
- **RSC056**: `scripts/validate_development.py` — `63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a`
- **RSC276**: `src/devtools/resources/commands/__init__.py` — `45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3`
- **RSC277**: `src/devtools/resources/commands/docs/command.md` — `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`
- **RSC278**: `src/devtools/resources/commands/docs/events.md` — `86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f`
- **RSC279**: `src/devtools/resources/commands/docs/execution.md` — `562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b`
- **RSC280**: `src/devtools/resources/commands/docs/overview.md` — `27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961`
- **RSC283**: `src/devtools/resources/commands/execution.py` — `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`
- **RSC284**: `src/devtools/resources/commands/handle.py` — `87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9`
- **RSC286**: `src/devtools/resources/commands/models/command.py` — `1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629`
- **RSC287**: `src/devtools/resources/commands/models/output.py` — `7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d`
- **RSC288**: `src/devtools/resources/commands/models/result.py` — `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`
- **RSC478**: `tests/resources/commands/test_execution.py` — `6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a`
- **RSC479**: `tests/resources/commands/test_handle.py` — `4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43`
- **RSC480**: `tests/resources/commands/test_models.py` — `914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4`
- **RSC509**: `tests/scripts/test_validate_development.py` — `aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986`
- **RSC512**: `tests/tools/test_command.py` — `5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535`

## Positive cells by obligation

### O1

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `src/devtools/agents/integrations/codex/agent.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Consumer example corroborates a completed failed result with exit_code; does not define the full result or success contract. |
| `src/devtools/core/time/docs/timestamps.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Explains Duration numeric access and precision for an optional explicit duration format; the result contract already identifies the value to preserve. |
| `src/devtools/core/time/models/duration.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Provides a human-readable Duration conversion implementation; choosing this exact format is not required. |
| `src/devtools/models/serving/llama_cpp.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/models/serving/vllm.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/resources/commands/docs/command.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R01, R02. Direct public value contract. Constructor and exact status prose. |
| `src/devtools/resources/commands/docs/execution.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates completed-result identity and direct execution; detailed executor lifecycle is unnecessary to a pure result renderer. |
| `src/devtools/resources/commands/docs/overview.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates ordinary nonzero completion but lacks the full field and status contracts. |
| `src/devtools/resources/commands/execution.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates completed result field construction and ordinary nonzero completion; does not define succeeded/failed or immutable Command shape. |
| `src/devtools/resources/commands/models/command.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R01. Frozen dataclass fields, specification contract and argv implementation. |
| `src/devtools/resources/commands/models/result.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R02. Fields and status predicates directly establish the contract. |
| `tests/core/time/test_models.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Examples corroborate Duration value/accessor/string semantics for optional formatting; the renderer need not use this exact format. |
| `tests/resources/commands/test_execution.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates completed nonzero results and duration, but lacks the complete structured immutable input contract and exact status definitions. |
| `tests/resources/commands/test_handle.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates one completed result and separately retained stream bytes; it does not establish all result semantics or prefix truncation. |
| `tests/resources/commands/test_models.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R01, R02. Explicit structured-value and frozen-input tests establish the intended public contract. The test explicitly describes nonzero completion and asserts preserved fields and both complementary status values. |
| `tests/tools/test_command.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Consumer regression corroborates command identity and ordinary nonzero completed results without defining all core result semantics. |

### O2

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `src/devtools/models/serving/llama_cpp.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/models/serving/vllm.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/resources/commands/docs/command.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R03. Direct result representation and retained-prefix prose. |
| `src/devtools/resources/commands/docs/events.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R03. Explicit independent leading result-prefix retention. |
| `src/devtools/resources/commands/execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R03. Both streams are bounded independently, converted to bytes and assigned to their result fields. |
| `src/devtools/resources/commands/models/result.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R03. Field types and retained-leading-byte documentation. |
| `tests/resources/commands/test_execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R03. Known byte chunks yield exact retained prefixes in each result stream, including zero retention. |
| `tests/resources/commands/test_handle.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates one completed result and separately retained stream bytes; it does not establish all result semantics or prefix truncation. |
| `tests/resources/commands/test_models.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts. |

### O3

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `src/devtools/agents/integrations/codex/agent.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Consumer corroborates stdout_truncated as retained-output loss; does not define both streams or retention policy. |
| `src/devtools/agents/integrations/codex/docs/cli.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Consumer documentation illustrates finite retention and caller-supplied output policy without defining the full retention contract. |
| `src/devtools/models/serving/llama_cpp.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/models/serving/vllm.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API. |
| `src/devtools/resources/commands/docs/command.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R04, R05. Independent byte limits and zero-retention behavior are documented. Explicit zero-byte and per-stream truncation contract. |
| `src/devtools/resources/commands/docs/events.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R04, R05. Independent output prefixes and retention bounds are documented. Omitted retained bytes set corresponding flags. |
| `src/devtools/resources/commands/execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R04, R05. Separate policy byte fields govern the bytearray prefixes. A flag becomes true when a chunk exceeds remaining retention; named fields receive the flags. |
| `src/devtools/resources/commands/models/output.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R04. Policy contract and distinct per-stream byte fields. |
| `src/devtools/resources/commands/models/result.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R05. Each named flag means its stream exceeded retained limit; zero-limit consequence follows from that definition. |
| `tests/resources/commands/test_execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R04, R05. Different byte limits and zero retention are controlled and asserted independently. Assertions connect bounded and zero-byte retention to each flag. |
| `tests/resources/commands/test_models.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts. |

### O4

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `src/devtools/resources/commands/docs/command.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R06, R07. Distinct result fields and explicit bounded-queue-loss meaning. Explicit no-result boundary. |
| `src/devtools/resources/commands/docs/events.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R06. Explicit event count, best-effort queue loss and independent retained output. |
| `src/devtools/resources/commands/docs/execution.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R07. Lifecycle documentation covers all three exceptional outcomes. |
| `src/devtools/resources/commands/errors.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Names not-found and timeout exceptions but alone does not establish that no completed result is produced, or cancellation behavior. |
| `src/devtools/resources/commands/events.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Shows immutable event values; the renderer accepts a result and must not reconstruct these events, so their concrete classes are optional context. |
| `src/devtools/resources/commands/execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R06, R07. The handle counts dropped events; execution copies that count into the result independently of output flags. All three failure paths raise before the successful result construction branch. |
| `src/devtools/resources/commands/handle.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R06. The handle counts dropped events; execution copies that count into the result independently of output flags. |
| `src/devtools/resources/commands/models/output.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates separate event capacity and best-effort buffering, but does not itself tie an omission count to a completed result. |
| `src/devtools/resources/commands/models/result.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R06. Separate numeric omission count and retained-output flag meanings. |
| `tests/resources/commands/test_errors.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Confirms public command error hierarchy and a nearby test style; does not establish exceptional no-result behavior. |
| `tests/resources/commands/test_events.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates immutable event values and an immutability test idiom; rendering consumes completed results, so these events need not be reconstructed. |
| `tests/resources/commands/test_execution.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R06. Independent queue capacity and stream limits produce a numeric omission count; lost exit event demonstrates results are not complete transcripts. |
| `tests/resources/commands/test_handle.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R07. Controlled awaited executions raise all three exceptions instead of returning results. |
| `tests/resources/commands/test_models.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts. |
| `tests/tools/test_command.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R07. Public command execution through the transparent Tool bridge propagates all three exceptional outcomes; no completed return is available. |

### O5

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `src/devtools/resources/commands/__init__.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R08. Exact current imports and __all__. |
| `src/devtools/resources/commands/docs/command.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R01, R09. Direct public value contract. Explicit frozen-result contract. |
| `src/devtools/resources/commands/docs/overview.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R08. Independent public API documentation names the complete current export surface. |
| `src/devtools/resources/commands/execution.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Shows existing executor ownership and usage for integration/regression context; the presentation API need not change execution. |
| `src/devtools/resources/commands/models/__init__.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Internal model reexports corroborate the public value owners but do not substitute for the full commands facade. |
| `src/devtools/resources/commands/models/command.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R01. Frozen dataclass fields, specification contract and argv implementation. |
| `src/devtools/resources/commands/models/result.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R09. Frozen dataclass declaration and immutable-valued fields. |
| `tests/resources/commands/test_models.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R01. Explicit structured-value and frozen-input tests establish the intended public contract. |

### O6

| Resource | Label | Inferability | Basis |
|---|---|---|---|
| `AGENTS.md` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R10. Operating guide explicitly supplies invocation and precollection exclusion. |
| `pyproject.toml` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R11. Actual pytest, coverage, lint and type-checking configuration; this is not a synthetic fixture. |
| `scripts/validate_development.py` | REQUIRED | DIRECT_SUPPORT | Necessary in at least one minimal complete witness as support for R10. Entry-point arguments select tests with the experiment directory ignored. |
| `src/devtools/resources/commands/docs/command.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing package documentation provides an appropriate update context and examples. The task already specifies the future documentation location and cases; this file is not required just as an edit destination. |
| `src/devtools/resources/commands/docs/events.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful existing explanation of event-loss versus retained-output coverage for documentation and regressions, without requiring this particular edit destination. |
| `src/devtools/resources/commands/docs/execution.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing lifecycle documentation is useful regression context; requesting future tests/docs does not require this file. |
| `src/devtools/resources/commands/docs/overview.md` | HELPFUL_ONLY | CORROBORATION_ONLY | Explains the package documentation organization and links; useful editing context, but the task already names the documentation destination. |
| `src/devtools/resources/commands/execution.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Shows existing executor ownership and usage for integration/regression context; the presentation API need not change execution. |
| `src/devtools/resources/commands/models/command.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful current input construction and immutability context for future controlled regression tests. |
| `src/devtools/resources/commands/models/output.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful fixture construction for independent retention scenarios; exact source resource is not required by the future coverage instruction. |
| `src/devtools/resources/commands/models/result.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful result-fixture and immutable-input context, not necessary solely because future tests are requested. |
| `tests/agents/integrations/codex/test_agent.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Shows a controlled executor double constructing completed CommandResult fixtures; useful test technique without requiring this adapter test file. |
| `tests/models/serving/test_llama_cpp.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Controlled result construction and executor fake are useful regression examples, without requiring model-service tests for the commands renderer. |
| `tests/models/serving/test_vllm.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Controlled completed-result fixtures and exception propagation examples are useful testing context, not a necessary commands test destination. |
| `tests/resources/commands/test_errors.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Confirms public command error hierarchy and a nearby test style; does not establish exceptional no-result behavior. |
| `tests/resources/commands/test_events.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Corroborates immutable event values and an immutability test idiom; rendering consumes completed results, so these events need not be reconstructed. |
| `tests/resources/commands/test_execution.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Relevant controlled retention/event-loss fixture conventions and existing coverage; the future test location and coverage requirements are task-backed. |
| `tests/resources/commands/test_handle.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Existing lifecycle fixtures are useful regression context; no requirement forces edits to this exact test resource. |
| `tests/resources/commands/test_models.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful current commands model regression organization and fixture examples; future tests can be added without this exact resource. |
| `tests/scripts/qwen/test_llama_cpp_service.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Another controlled result fixture/executor example; not a necessary source of the future regression requirements. |
| `tests/scripts/test_validate_development.py` | REQUIRED | INFERABLE_SUPPORT | Necessary in at least one minimal complete witness as support for R10. Independent contract tests assert the exact directory exclusion and unchanged pytest outcome. |
| `tests/tools/test_command.py` | HELPFUL_ONLY | CORROBORATION_ONLY | Useful exception propagation examples; future renderer regressions need not edit Tool integration tests. |

## Semantic units

30 units: 19 TASK_BACKED, 11 REPOSITORY_SUPPORTED, 0 TASK_AND_REPOSITORY_SUPPORTED.

### T01 — TASK_BACKED

The new renderer is opt-in human-readable presentation of an already completed result in the commands domain.

Applies to O1, O5.

Task span [0, 137): Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.


### T02 — TASK_BACKED

Rendering is pure: no execution, shell invocation, retry, or input mutation.

Applies to O1, O5.

Task span [310, 416): Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.


### T03 — TASK_BACKED

Preserve structured executable/arguments, exit_code, duration and succeeded/failed meaning; a nonzero exit remains ordinary completion.

Applies to O1.

Task span [143, 309): Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result.


### T04 — TASK_BACKED

Render stdout and stderr as separately labeled diagnostic excerpts.

Applies to O2.

Task span [422, 499): Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts.


### T05 — TASK_BACKED

Decode invalid or incomplete UTF-8 with explicit replacement and disclose decoding loss separately.

Applies to O2.

Task span [537, 637): Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately


### T06 — TASK_BACKED

Preserve original stream bytes and distinguish decoded diagnostic text from original bytes.

Applies to O2.

Task span [500, 701): Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.


### T07 — TASK_BACKED

Each stream has a caller-configurable nonnegative character limit, default 2048.

Applies to O3.

Task span [707, 815): Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters.


### T08 — TASK_BACKED

Display a leading decoded prefix and disclose omitted characters, including informative zero-limit output.

Applies to O3.

Task span [816, 1079): Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.


### T09 — TASK_BACKED

Display omission must be distinguished from byte retention and existing per-stream truncation flags.

Applies to O3.

Task span [892, 1011): Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`


### T10 — TASK_BACKED

Preserve and display events_dropped independently of output truncation.

Applies to O4.

Task span [1085, 1158): Preserve and display `events_dropped` independently of output truncation.


### T11 — TASK_BACKED

Never reconstruct event interleaving or fabricate missing events.

Applies to O4.

Task span [1159, 1225): Do not reconstruct event interleaving or fabricate missing events.


### T12 — TASK_BACKED

Accept only existing completed results; do not synthesize results for timeout, cancellation, or executable-not-found.

Applies to O4.

Task span [1226, 1375): Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.


### T13 — TASK_BACKED

Provide a small explicit public API through the commands package facade.

Applies to O5.

Task span [1381, 1470): Provide a small explicit public API through `src/devtools/resources/commands/__init__.py`


### T14 — TASK_BACKED

The same input and display policy produce deterministic output.

Applies to O1, O5.

Task span [1471, 1514): with deterministic output, immutable inputs


### T15 — TASK_BACKED

Document the decoding and display policies.

Applies to O5.

Task span [1519, 1554): documented decoding/display policy.


### T16 — TASK_BACKED

Presentation belongs to commands and adds none of the prohibited infrastructure or redaction claims.

Applies to O5.

Task span [1555, 1714): Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.


### T17 — TASK_BACKED

Add controlled commands tests covering success/nonzero, empty and valid/invalid/incomplete UTF-8 output, zero/default/custom display bounds, independent retention flags, event loss, determinism and immutability.

Applies to O6.

Task span [1720, 2052): Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability.


### T18 — TASK_BACKED

Update commands package documentation for the specified behavior and edge cases.

Applies to O6.

Task span [1779, 2052): update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability.


### T19 — TASK_BACKED

Preserve the protected development validation profile.

Applies to O6.

Task span [2053, 2154): Preserve the protected development validation profile documented in `docs/development/validation.md`.


### R01 — REPOSITORY_SUPPORTED

Command is an immutable structured value with separate executable and ordered argument tuple.

Applies to O1, O5.

- R01/A1 — DIRECT_SUPPORT: RSC277. Direct public value contract. Support: src/devtools/resources/commands/docs/command.md:6-31.
- R01/A2 — DIRECT_SUPPORT: RSC286. Frozen dataclass fields, specification contract and argv implementation. Support: src/devtools/resources/commands/models/command.py:14-62.
- R01/A3 — INFERABLE_SUPPORT: RSC480. Explicit structured-value and frozen-input tests establish the intended public contract. Support: tests/resources/commands/test_models.py:19-84.

### R02 — REPOSITORY_SUPPORTED

A completed result retains command, exit_code and duration; succeeded is zero exit and failed is nonzero, which is ordinary completion.

Applies to O1.

- R02/A1 — DIRECT_SUPPORT: RSC277. Constructor and exact status prose. Support: src/devtools/resources/commands/docs/command.md:49-71.
- R02/A2 — DIRECT_SUPPORT: RSC288. Fields and status predicates directly establish the contract. Support: src/devtools/resources/commands/models/result.py:14-55.
- R02/A3 — INFERABLE_SUPPORT: RSC480. The test explicitly describes nonzero completion and asserts preserved fields and both complementary status values. Support: tests/resources/commands/test_models.py:94-120.

### R03 — REPOSITORY_SUPPORTED

Result stdout and stderr are separate raw byte values holding retained leading prefixes, which may be incomplete process output.

Applies to O2.

- R03/A1 — DIRECT_SUPPORT: RSC277. Direct result representation and retained-prefix prose. Support: src/devtools/resources/commands/docs/command.md:49-67.
- R03/A2 — DIRECT_SUPPORT: RSC278. Explicit independent leading result-prefix retention. Support: src/devtools/resources/commands/docs/events.md:45-53.
- R03/A3 — INFERABLE_SUPPORT: RSC283. Both streams are bounded independently, converted to bytes and assigned to their result fields. Support: src/devtools/resources/commands/execution.py:152-160; src/devtools/resources/commands/execution.py:236-303.
- R03/A4 — DIRECT_SUPPORT: RSC288. Field types and retained-leading-byte documentation. Support: src/devtools/resources/commands/models/result.py:22-39.
- R03/A5 — INFERABLE_SUPPORT: RSC478. Known byte chunks yield exact retained prefixes in each result stream, including zero retention. Support: tests/resources/commands/test_execution.py:190-265; tests/resources/commands/test_execution.py:366-408.

### R04 — REPOSITORY_SUPPORTED

CommandOutputPolicy bounds retained output independently per stream in bytes, separately from a renderer character limit.

Applies to O3.

- R04/A1 — DIRECT_SUPPORT: RSC277. Independent byte limits and zero-retention behavior are documented. Support: src/devtools/resources/commands/docs/command.md:34-47.
- R04/A2 — DIRECT_SUPPORT: RSC278. Independent output prefixes and retention bounds are documented. Support: src/devtools/resources/commands/docs/events.md:45-53.
- R04/A3 — INFERABLE_SUPPORT: RSC283. Separate policy byte fields govern the bytearray prefixes. Support: src/devtools/resources/commands/execution.py:236-303.
- R04/A4 — DIRECT_SUPPORT: RSC287. Policy contract and distinct per-stream byte fields. Support: src/devtools/resources/commands/models/output.py:7-37.
- R04/A5 — INFERABLE_SUPPORT: RSC478. Different byte limits and zero retention are controlled and asserted independently. Support: tests/resources/commands/test_execution.py:190-265; tests/resources/commands/test_execution.py:366-408.

### R05 — REPOSITORY_SUPPORTED

stdout_truncated and stderr_truncated report bytes omitted by retention, including when retained bytes are empty under a zero bound.

Applies to O3.

- R05/A1 — DIRECT_SUPPORT: RSC277. Explicit zero-byte and per-stream truncation contract. Support: src/devtools/resources/commands/docs/command.md:44-67.
- R05/A2 — DIRECT_SUPPORT: RSC278. Omitted retained bytes set corresponding flags. Support: src/devtools/resources/commands/docs/events.md:45-53.
- R05/A3 — INFERABLE_SUPPORT: RSC283. A flag becomes true when a chunk exceeds remaining retention; named fields receive the flags. Support: src/devtools/resources/commands/execution.py:152-160; src/devtools/resources/commands/execution.py:281-303.
- R05/A4 — DIRECT_SUPPORT: RSC288. Each named flag means its stream exceeded retained limit; zero-limit consequence follows from that definition. Support: src/devtools/resources/commands/models/result.py:24-38.
- R05/A5 — INFERABLE_SUPPORT: RSC478. Assertions connect bounded and zero-byte retention to each flag. Support: tests/resources/commands/test_execution.py:190-265; tests/resources/commands/test_execution.py:366-408.

### R06 — REPOSITORY_SUPPORTED

events_dropped is the numeric count of omitted buffered events, distinct from retained-output truncation.

Applies to O4.

- R06/A1 — DIRECT_SUPPORT: RSC277. Distinct result fields and explicit bounded-queue-loss meaning. Support: src/devtools/resources/commands/docs/command.md:49-67.
- R06/A2 — DIRECT_SUPPORT: RSC278. Explicit event count, best-effort queue loss and independent retained output. Support: src/devtools/resources/commands/docs/events.md:28-53.
- R06/A3 — DIRECT_SUPPORT: RSC288. Separate numeric omission count and retained-output flag meanings. Support: src/devtools/resources/commands/models/result.py:24-39.
- R06/A4 — INFERABLE_SUPPORT: RSC284, RSC283. The handle counts dropped events; execution copies that count into the result independently of output flags. Support: src/devtools/resources/commands/execution.py:152-169; src/devtools/resources/commands/handle.py:79-133.
- R06/A5 — INFERABLE_SUPPORT: RSC478. Independent queue capacity and stream limits produce a numeric omission count; lost exit event demonstrates results are not complete transcripts. Support: tests/resources/commands/test_execution.py:190-265; tests/resources/commands/test_execution.py:366-408.

### R07 — REPOSITORY_SUPPORTED

Timeout, cancellation and missing executable propagate exceptional outcomes and produce no completed CommandResult.

Applies to O4.

- R07/A1 — DIRECT_SUPPORT: RSC277. Explicit no-result boundary. Support: src/devtools/resources/commands/docs/command.md:69-71.
- R07/A2 — DIRECT_SUPPORT: RSC279. Lifecycle documentation covers all three exceptional outcomes. Support: src/devtools/resources/commands/docs/execution.md:26-55.
- R07/A3 — INFERABLE_SUPPORT: RSC283. All three failure paths raise before the successful result construction branch. Support: src/devtools/resources/commands/execution.py:78-207.
- R07/A4 — INFERABLE_SUPPORT: RSC479. Controlled awaited executions raise all three exceptions instead of returning results. Support: tests/resources/commands/test_handle.py:101-196; tests/resources/commands/test_handle.py:231-301.
- R07/A5 — INFERABLE_SUPPORT: RSC512. Public command execution through the transparent Tool bridge propagates all three exceptional outcomes; no completed return is available. Support: tests/tools/test_command.py:59-120.

### R08 — REPOSITORY_SUPPORTED

The commands public facade explicitly exposes Command, CommandResult, CommandOutputPolicy, executor/handle, event union and values, and command errors.

Applies to O5.

- R08/A1 — DIRECT_SUPPORT: RSC276. Exact current imports and __all__. Support: src/devtools/resources/commands/__init__.py:4-38.
- R08/A2 — DIRECT_SUPPORT: RSC280. Independent public API documentation names the complete current export surface. Support: src/devtools/resources/commands/docs/overview.md:9-38.

### R09 — REPOSITORY_SUPPORTED

CommandResult is an immutable frozen value object, permitting presentation without changing retained input state.

Applies to O5.

- R09/A1 — DIRECT_SUPPORT: RSC277. Explicit frozen-result contract. Support: src/devtools/resources/commands/docs/command.md:64-67.
- R09/A2 — DIRECT_SUPPORT: RSC288. Frozen dataclass declaration and immutable-valued fields. Support: src/devtools/resources/commands/models/result.py:14-39.

### R10 — REPOSITORY_SUPPORTED

The protected ordinary-development entry point selects tests while excluding tests/experiments before collection.

Applies to O6.

- R10/A1 — DIRECT_SUPPORT: RSC001. Operating guide explicitly supplies invocation and precollection exclusion. Support: AGENTS.md:228-239.
- R10/A2 — DIRECT_SUPPORT: RSC056. Entry-point arguments select tests with the experiment directory ignored. Support: scripts/validate_development.py:14-27.
- R10/A3 — INFERABLE_SUPPORT: RSC509. Independent contract tests assert the exact directory exclusion and unchanged pytest outcome. Support: tests/scripts/test_validate_development.py:17-48; tests/scripts/test_validate_development.py:51-68.

### R11 — REPOSITORY_SUPPORTED

Configured development checks retain strict pytest configuration/markers, devtools branch coverage at 100 percent, Ruff rules and strict mypy settings.

Applies to O6.

- R11/A1 — DIRECT_SUPPORT: RSC055. Actual pytest, coverage, lint and type-checking configuration; this is not a synthetic fixture. Support: pyproject.toml:34-78.

## Minimal complete witnesses and indispensability

Every row is an ALL-resource witness; complete rows for one obligation are ANY alternatives. Task-backed units are present in every applicable witness without repository cost.

### O1 (3 witnesses)

- O1/W001: RSC480; units: T01, T02, T03, T14, R01, R02.
- O1/W002: RSC277; units: T01, T02, T03, T14, R01, R02.
- O1/W003: RSC286, RSC288; units: T01, T02, T03, T14, R01, R02.

Indispensable resources: (repository-empty).

Indispensable units: R01, R02, T01, T02, T03, T14.

### O2 (5 witnesses)

- O2/W001: RSC288; units: T04, T05, T06, R03.
- O2/W002: RSC478; units: T04, T05, T06, R03.
- O2/W003: RSC278; units: T04, T05, T06, R03.
- O2/W004: RSC277; units: T04, T05, T06, R03.
- O2/W005: RSC283; units: T04, T05, T06, R03.

Indispensable resources: (repository-empty).

Indispensable units: R03, T04, T05, T06.

### O3 (5 witnesses)

- O3/W001: RSC478; units: T07, T08, T09, R04, R05.
- O3/W002: RSC278; units: T07, T08, T09, R04, R05.
- O3/W003: RSC277; units: T07, T08, T09, R04, R05.
- O3/W004: RSC283; units: T07, T08, T09, R04, R05.
- O3/W005: RSC288, RSC287; units: T07, T08, T09, R04, R05.

Indispensable resources: (repository-empty).

Indispensable units: R04, R05, T07, T08, T09.

### O4 (14 witnesses)

- O4/W001: RSC277; units: T10, T11, T12, R06, R07.
- O4/W002: RSC479, RSC288; units: T10, T11, T12, R06, R07.
- O4/W003: RSC479, RSC478; units: T10, T11, T12, R06, R07.
- O4/W004: RSC479, RSC278; units: T10, T11, T12, R06, R07.
- O4/W005: RSC279, RSC288; units: T10, T11, T12, R06, R07.
- O4/W006: RSC279, RSC478; units: T10, T11, T12, R06, R07.
- O4/W007: RSC279, RSC278; units: T10, T11, T12, R06, R07.
- O4/W008: RSC512, RSC288; units: T10, T11, T12, R06, R07.
- O4/W009: RSC512, RSC478; units: T10, T11, T12, R06, R07.
- O4/W010: RSC512, RSC278; units: T10, T11, T12, R06, R07.
- O4/W011: RSC288, RSC283; units: T10, T11, T12, R06, R07.
- O4/W012: RSC478, RSC283; units: T10, T11, T12, R06, R07.
- O4/W013: RSC278, RSC283; units: T10, T11, T12, R06, R07.
- O4/W014: RSC284, RSC283; units: T10, T11, T12, R06, R07.

Indispensable resources: (repository-empty).

Indispensable units: R06, R07, T10, T11, T12.

### O5 (6 witnesses)

- O5/W001: RSC280, RSC277; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.
- O5/W002: RSC276, RSC277; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.
- O5/W003: RSC286, RSC280, RSC288; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.
- O5/W004: RSC286, RSC276, RSC288; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.
- O5/W005: RSC280, RSC288, RSC480; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.
- O5/W006: RSC276, RSC288, RSC480; units: T01, T02, T13, T14, T15, T16, R01, R08, R09.

Indispensable resources: (repository-empty).

Indispensable units: R01, R08, R09, T01, T02, T13, T14, T15, T16.

### O6 (3 witnesses)

- O6/W001: RSC056, RSC055; units: T17, T18, T19, R10, R11.
- O6/W002: RSC055, RSC001; units: T17, T18, T19, R10, R11.
- O6/W003: RSC055, RSC509; units: T17, T18, T19, R10, R11.

Indispensable resources: RSC055.

Indispensable units: R10, R11, T17, T18, T19.

## Task-level sufficiency

18,900 complete task combinations produce 2,850 distinct sufficient resource unions and 126 inclusion-minimal unions. Resource count range across all distinct sufficient unions: 4–10. Shared resources are counted once.

There are 1 distinct sufficient semantic-unit unions, with 30–30 units. The complete union is: R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19.

Task-indispensable resources: RSC055.

Task-indispensable units: R01, R02, R03, R04, R05, R06, R07, R08, R09, R10, R11, T01, T02, T03, T04, T05, T06, T07, T08, T09, T10, T11, T12, T13, T14, T15, T16, T17, T18, T19.

### Inclusion-minimal resource unions

- RU00001: RSC280, RSC056, RSC055, RSC277.
- RU00002: RSC280, RSC055, RSC001, RSC277.
- RU00003: RSC280, RSC055, RSC509, RSC277.
- RU00004: RSC276, RSC056, RSC055, RSC277.
- RU00005: RSC276, RSC055, RSC001, RSC277.
- RU00006: RSC276, RSC055, RSC509, RSC277.
- RU00038: RSC286, RSC280, RSC288, RSC056, RSC055, RSC283.
- RU00040: RSC286, RSC280, RSC288, RSC055, RSC001, RSC283.
- RU00042: RSC286, RSC280, RSC288, RSC055, RSC509, RSC283.
- RU00044: RSC286, RSC276, RSC288, RSC056, RSC055, RSC283.
- RU00046: RSC286, RSC276, RSC288, RSC055, RSC001, RSC283.
- RU00048: RSC286, RSC276, RSC288, RSC055, RSC509, RSC283.
- RU00080: RSC280, RSC288, RSC056, RSC055, RSC480, RSC283.
- RU00089: RSC280, RSC288, RSC055, RSC480, RSC001, RSC283.
- RU00091: RSC280, RSC288, RSC055, RSC480, RSC509, RSC283.
- RU00146: RSC276, RSC288, RSC056, RSC055, RSC480, RSC283.
- RU00155: RSC276, RSC288, RSC055, RSC480, RSC001, RSC283.
- RU00157: RSC276, RSC288, RSC055, RSC480, RSC509, RSC283.
- RU00181: RSC286, RSC280, RSC479, RSC288, RSC056, RSC055, RSC478.
- RU00182: RSC286, RSC280, RSC479, RSC288, RSC056, RSC055, RSC287.
- RU00183: RSC286, RSC280, RSC479, RSC288, RSC056, RSC055, RSC278.
- RU00186: RSC286, RSC280, RSC479, RSC288, RSC055, RSC478, RSC001.
- RU00187: RSC286, RSC280, RSC479, RSC288, RSC055, RSC478, RSC509.
- RU00188: RSC286, RSC280, RSC479, RSC288, RSC055, RSC287, RSC001.
- RU00189: RSC286, RSC280, RSC479, RSC288, RSC055, RSC287, RSC509.
- RU00190: RSC286, RSC280, RSC479, RSC288, RSC055, RSC278, RSC001.
- RU00191: RSC286, RSC280, RSC479, RSC288, RSC055, RSC278, RSC509.
- RU00196: RSC286, RSC280, RSC279, RSC288, RSC056, RSC055, RSC478.
- RU00197: RSC286, RSC280, RSC279, RSC288, RSC056, RSC055, RSC287.
- RU00198: RSC286, RSC280, RSC279, RSC288, RSC056, RSC055, RSC278.
- RU00201: RSC286, RSC280, RSC279, RSC288, RSC055, RSC478, RSC001.
- RU00202: RSC286, RSC280, RSC279, RSC288, RSC055, RSC478, RSC509.
- RU00203: RSC286, RSC280, RSC279, RSC288, RSC055, RSC287, RSC001.
- RU00204: RSC286, RSC280, RSC279, RSC288, RSC055, RSC287, RSC509.
- RU00205: RSC286, RSC280, RSC279, RSC288, RSC055, RSC278, RSC001.
- RU00206: RSC286, RSC280, RSC279, RSC288, RSC055, RSC278, RSC509.
- RU00211: RSC286, RSC280, RSC512, RSC288, RSC056, RSC055, RSC478.
- RU00212: RSC286, RSC280, RSC512, RSC288, RSC056, RSC055, RSC287.
- RU00213: RSC286, RSC280, RSC512, RSC288, RSC056, RSC055, RSC278.
- RU00216: RSC286, RSC280, RSC512, RSC288, RSC055, RSC478, RSC001.
- RU00217: RSC286, RSC280, RSC512, RSC288, RSC055, RSC478, RSC509.
- RU00218: RSC286, RSC280, RSC512, RSC288, RSC055, RSC287, RSC001.
- RU00219: RSC286, RSC280, RSC512, RSC288, RSC055, RSC287, RSC509.
- RU00220: RSC286, RSC280, RSC512, RSC288, RSC055, RSC278, RSC001.
- RU00221: RSC286, RSC280, RSC512, RSC288, RSC055, RSC278, RSC509.
- RU00256: RSC286, RSC479, RSC276, RSC288, RSC056, RSC055, RSC478.
- RU00257: RSC286, RSC479, RSC276, RSC288, RSC056, RSC055, RSC287.
- RU00258: RSC286, RSC479, RSC276, RSC288, RSC056, RSC055, RSC278.
- RU00261: RSC286, RSC479, RSC276, RSC288, RSC055, RSC478, RSC001.
- RU00262: RSC286, RSC479, RSC276, RSC288, RSC055, RSC478, RSC509.
- RU00263: RSC286, RSC479, RSC276, RSC288, RSC055, RSC287, RSC001.
- RU00264: RSC286, RSC479, RSC276, RSC288, RSC055, RSC287, RSC509.
- RU00265: RSC286, RSC479, RSC276, RSC288, RSC055, RSC278, RSC001.
- RU00266: RSC286, RSC479, RSC276, RSC288, RSC055, RSC278, RSC509.
- RU00271: RSC286, RSC276, RSC279, RSC288, RSC056, RSC055, RSC478.
- RU00272: RSC286, RSC276, RSC279, RSC288, RSC056, RSC055, RSC287.
- RU00273: RSC286, RSC276, RSC279, RSC288, RSC056, RSC055, RSC278.
- RU00276: RSC286, RSC276, RSC279, RSC288, RSC055, RSC478, RSC001.
- RU00277: RSC286, RSC276, RSC279, RSC288, RSC055, RSC478, RSC509.
- RU00278: RSC286, RSC276, RSC279, RSC288, RSC055, RSC287, RSC001.
- RU00279: RSC286, RSC276, RSC279, RSC288, RSC055, RSC287, RSC509.
- RU00280: RSC286, RSC276, RSC279, RSC288, RSC055, RSC278, RSC001.
- RU00281: RSC286, RSC276, RSC279, RSC288, RSC055, RSC278, RSC509.
- RU00286: RSC286, RSC276, RSC512, RSC288, RSC056, RSC055, RSC478.
- RU00287: RSC286, RSC276, RSC512, RSC288, RSC056, RSC055, RSC287.
- RU00288: RSC286, RSC276, RSC512, RSC288, RSC056, RSC055, RSC278.
- RU00291: RSC286, RSC276, RSC512, RSC288, RSC055, RSC478, RSC001.
- RU00292: RSC286, RSC276, RSC512, RSC288, RSC055, RSC478, RSC509.
- RU00293: RSC286, RSC276, RSC512, RSC288, RSC055, RSC287, RSC001.
- RU00294: RSC286, RSC276, RSC512, RSC288, RSC055, RSC287, RSC509.
- RU00295: RSC286, RSC276, RSC512, RSC288, RSC055, RSC278, RSC001.
- RU00296: RSC286, RSC276, RSC512, RSC288, RSC055, RSC278, RSC509.
- RU00331: RSC280, RSC479, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00333: RSC280, RSC479, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00335: RSC280, RSC479, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00340: RSC280, RSC479, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00341: RSC280, RSC479, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00344: RSC280, RSC479, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00345: RSC280, RSC479, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00348: RSC280, RSC479, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00349: RSC280, RSC479, RSC288, RSC055, RSC278, RSC480, RSC509.
- RU00373: RSC280, RSC279, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00375: RSC280, RSC279, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00377: RSC280, RSC279, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00382: RSC280, RSC279, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00383: RSC280, RSC279, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00386: RSC280, RSC279, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00387: RSC280, RSC279, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00390: RSC280, RSC279, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00391: RSC280, RSC279, RSC288, RSC055, RSC278, RSC480, RSC509.
- RU00415: RSC280, RSC512, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00417: RSC280, RSC512, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00419: RSC280, RSC512, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00424: RSC280, RSC512, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00425: RSC280, RSC512, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00428: RSC280, RSC512, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00429: RSC280, RSC512, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00432: RSC280, RSC512, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00433: RSC280, RSC512, RSC288, RSC055, RSC278, RSC480, RSC509.
- RU00520: RSC479, RSC276, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00522: RSC479, RSC276, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00524: RSC479, RSC276, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00529: RSC479, RSC276, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00530: RSC479, RSC276, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00533: RSC479, RSC276, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00534: RSC479, RSC276, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00537: RSC479, RSC276, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00538: RSC479, RSC276, RSC288, RSC055, RSC278, RSC480, RSC509.
- RU00562: RSC276, RSC279, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00564: RSC276, RSC279, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00566: RSC276, RSC279, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00571: RSC276, RSC279, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00572: RSC276, RSC279, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00575: RSC276, RSC279, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00576: RSC276, RSC279, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00579: RSC276, RSC279, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00580: RSC276, RSC279, RSC288, RSC055, RSC278, RSC480, RSC509.
- RU00604: RSC276, RSC512, RSC288, RSC056, RSC055, RSC478, RSC480.
- RU00606: RSC276, RSC512, RSC288, RSC056, RSC055, RSC287, RSC480.
- RU00608: RSC276, RSC512, RSC288, RSC056, RSC055, RSC278, RSC480.
- RU00613: RSC276, RSC512, RSC288, RSC055, RSC478, RSC480, RSC001.
- RU00614: RSC276, RSC512, RSC288, RSC055, RSC478, RSC480, RSC509.
- RU00617: RSC276, RSC512, RSC288, RSC055, RSC287, RSC480, RSC001.
- RU00618: RSC276, RSC512, RSC288, RSC055, RSC287, RSC480, RSC509.
- RU00621: RSC276, RSC512, RSC288, RSC055, RSC278, RSC480, RSC001.
- RU00622: RSC276, RSC512, RSC288, RSC055, RSC278, RSC480, RSC509.

All combinations and distinct sufficient unions are explicitly retained in stage_c_review.json.

## Gaps

- REPOSITORY_INFORMATION_GAP: NONE. Retained source, public documentation, controlled contract tests and actual validation configuration establish the necessary current facts. The absent validation prose is bounded explicitly below; no additional necessary missing fact was identified.
- TASK_GAP: NONE. The objective and required behavior are sufficiently specified; unresolved presentation choices do not prevent a compliant implementation.
- TASK_INTERPRETATION_GAP: NONE. All substantive task clauses, including the preamble, are represented by the six mandatory obligations and the audited units.

## Limitations and ambiguities

- L01: The retained 515-resource frame omits docs/development/validation.md. Its exact prose and any additional instructions cannot be asserted. The observable protected profile is established by AGENTS.md, the entry point, its contract tests, and pyproject.toml; no claim of byte-level documentation completeness is made. Basis: Exact sealed resource address frame; AGENTS.md lines 228-239; scripts/validate_development.py lines 14-27; tests/scripts/test_validate_development.py lines 35-68; pyproject.toml lines 34-78.
- L02: Repository contracts are adjudicated from retained text. No devtools module was imported and no repository feature tests or live commands were executed. Contract-bearing tests are evidence of intended behavior, not a new execution result. Basis: Inspection method and sealed packet scope.
- L03: The renderer cannot recover bytes omitted by retention or dropped events. A retained prefix may end inside UTF-8; replacement decoding discloses local decoding loss without asserting the original complete stream was invalid. Basis: Task O2-O4; commands/docs/command.md lines 44-71; commands/docs/events.md lines 45-53.
- L04: execution.py has a stale return-description line calling output complete, while its immediately preceding prose, implementation and other contracts establish retained prefixes. The specific implementation and consistent bounded-retention contract control this reading. Basis: src/devtools/resources/commands/execution.py lines 242-249 and 281-303.
- A01: Public helper name, exact text layout, separators, status wording and duration presentation remain open if deterministic, human-readable and faithful to the structured values. Preserved as nonblocking design freedom.
- A02: Character limit is a decoded-text bound, not a byte bound. Python Unicode character counting is a defensible implementation; the task does not specify terminal columns or grapheme-cluster measurement. Do not impose a terminal-width or grapheme dependency as necessary evidence.
- A03: The exact decoding-loss disclosure format and limit argument type/error policy are unspecified. A genuine U+FFFD in valid UTF-8 must not itself be treated as proof of replacement loss. Preserve policy choice while requiring explicit replacement decoding and truthful independent loss disclosure.

Unresolved cell judgments: 0.

## Self-review

Future policies and current contracts are separate units. Stream labels, replacement/loss, byte fidelity, limit configuration, omitted characters, and retention flags are distinct. The coverage matrix is one task-backed testing requirement because its individual behavioral contents already have semantic units. No unit means merely read a file.

Direct source declarations and explicit public documentation are accepted independently. Contract-bearing assertions plus controlled fixtures are inferable alternatives; incidental consumers, default-only tests, and incomplete error declarations remain corroboration. Every resource removed from a witness leaves at least one necessary repository unit unsupported.

- Promoted AGENTS.md for O6: its explicit entry-point and precollection-exclusion contract is a complete alternative, not merely corroboration.
- Accepted contract-bearing tests as alternative support for structured Command/status, retained prefixes, event count and exceptional completion. Test placement alone remains insufficient.
- Separated completed-result field/status semantics from frozen-result semantics: test_models.py supports the former and frozen Command, but does not establish frozen CommandResult.
- Retained execution.py plus handle.py as complementary event-count support; neither resource was assumed to establish the complete count-transfer fact alone.
- Kept the current public API documentation as an alternative to the facade source; the named edit path is not uniquely indispensable.
- Kept existing command tests/docs helpful under O6 because future destinations and regression cases are already specified; configured validation facts are necessary.
- Separated deterministic output from the already represented input-mutation prohibition; removed optional argv convenience and event-transcript detail from necessary units.

## Exact support spans

Coordinates use zero-based half-open Python Unicode character offsets into the exact retained resource text. Line ranges are one-based inclusive. Each distinct span below supports at least one positive cell or necessary unit.

### AGENTS.md:228-239

Resource `953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d`; content `096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a`; characters [10713, 11282).

~~~~text
The canonical protected development test profile is documented in
[docs/development/validation.md](docs/development/validation.md). Run it with:

```text
uv run python scripts/validate_development.py
```

It excludes `tests/experiments/` before collection to avoid retained
outcome-dependent tests. Keep the configured production branch-coverage gate.
Run Ruff, formatting, mypy, and diff checks separately as documented. Do not
run confirmation validation or live model/Docker tests for ordinary work;
those require explicit authorization and are reported separately.
~~~~

### pyproject.toml:34-78

Resource `6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0`; content `e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145`; characters [585, 1368).

~~~~text
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--strict-config",
    "--strict-markers",
    "--cov=devtools",
    "--cov-branch",
    "--cov-report=term-missing",
    "--cov-fail-under=100",
]
markers = [
    "live_codex: opt-in test that contacts the locally authenticated Codex CLI",
]

[tool.coverage.run]
branch = true
source = ["devtools"]

[tool.coverage.report]
show_missing = true
skip_covered = false
fail_under = 100

[tool.ruff]
target-version = "py312"
line-length = 88

[tool.ruff.lint]
select = ["ALL"]
ignore = [
    "D203",
    "D213",
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",
]

[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests", "experiments"]
explicit_package_bases = true
mypy_path = ["src"]
~~~~

### scripts/validate_development.py:14-27

Resource `63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a`; content `425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5`; characters [248, 715).

~~~~text
def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:
    """Select ordinary tests while excluding the retained experiment tree."""
    tests = repository_root / "tests"
    experiments = tests / "experiments"
    return [str(tests), f"--ignore={experiments}"]


def main() -> int:
    """Run pytest and return its exit code unchanged."""
    return int(pytest.main(pytest_arguments()))


if __name__ == "__main__":
    raise SystemExit(main())
~~~~

### src/devtools/agents/integrations/codex/agent.py:86-94

Resource `e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344`; content `11b5d1a5510bc24338ed2aab4efd3362cfe8a523423e7c23f12dc438aa8eca41`; characters [3061, 3481).

~~~~text
        command = self._build_command(message.content, conversation)
        result = await self._executor.execute(command)
        if result.failed:
            raise CodexCommandError(result.exit_code)
        if result.stdout_truncated:
            msg = "Codex JSONL stdout was truncated by the command output policy."
            raise CodexOutputError(msg)

        output = parse_codex_turn_output(result.stdout)
~~~~

### src/devtools/agents/integrations/codex/docs/cli.md:97-105

Resource `deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f`; content `30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294`; characters [3852, 4249).

~~~~text
## Retained output and stderr

JSONL is parsed from retained `CommandResult.stdout`. The executor's retention
is finite; `stdout_truncated` fails closed with `CodexOutputError`. Callers that
expect unusually large transcripts can provide `CommandExecutor` with a larger
`CommandOutputPolicy`.

Successful-turn stderr is ignored. It is not assumed empty and is not converted
into an error message.
~~~~

### src/devtools/core/time/docs/timestamps.md:81-96

Resource `12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2`; content `91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941`; characters [2345, 3061).

~~~~text
## Duration

`Duration(value: timedelta)` is a frozen, slotted non-negative value. Factories
are `nanoseconds()`, `milliseconds()`, `seconds()`, `minutes()`, and `hours()`.
`total_seconds` and `total_milliseconds` expose numeric totals.

Durations support addition, non-negative subtraction, multiplication by an
`int` or `float`, reversed multiplication, and division by an `int` or `float`.
Unsupported operands raise normal `TypeError`; division by zero raises normal
`ZeroDivisionError`.

## Precision and errors

`Duration` stores `datetime.timedelta`, not true nanoseconds. Consequently,
`Duration.nanoseconds()` follows standard-library microsecond-bounded
conversion and rounding for sub-microsecond inputs.
~~~~

### src/devtools/core/time/models/duration.py:77-98

Resource `15ea4e21efcac9c53500c2225545960280bc14698c8d34c0ea6475650e669103`; content `69baac5a2120f0c503d4db9bf454331394921e5a606fcc7288f143380ff79241`; characters [2122, 2715).

~~~~text
    @property
    def total_seconds(self) -> float:
        """Return the duration in seconds.

        :returns: Total number of seconds.
        """
        return self.value.total_seconds()

    @property
    def total_milliseconds(self) -> float:
        """Return the duration in milliseconds.

        :returns: Total number of milliseconds.
        """
        return self.total_seconds * 1000.0

    def __str__(self) -> str:
        """Return the standard timedelta representation.

        :returns: Human-readable duration representation.
        """
        return str(self.value)
~~~~

### src/devtools/models/serving/llama_cpp.py:424-444

Resource `cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c`; content `c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e`; characters [14694, 15480).

~~~~text
def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:
    return (
        result.stderr.decode(errors="replace").strip().casefold()
        == f"error: no such object: {container_id}".casefold()
    )


def _diagnostic_text(data: bytes) -> str:
    return data[:4096].decode(errors="replace").strip()


def _launch_error_message(result: CommandResult) -> str:
    return f"Docker rejected llama.cpp launch with exit code {result.exit_code}. {_diagnostic_text(result.stderr or result.stdout)}".strip()


def _stop_error_message(
    operation: str,
    result: CommandResult,
    container_id: str,
) -> str:
    return f"Docker could not {operation} owned llama.cpp container {container_id!r}. {_diagnostic_text(result.stderr or result.stdout)}".strip()
~~~~

### src/devtools/models/serving/vllm.py:489-514

Resource `102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22`; content `bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43`; characters [16439, 17701).

~~~~text
def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:
    """Return whether Docker reported this exact inspected container as absent."""
    expected = f"error: no such object: {container_id}".casefold()
    diagnostic = result.stderr.decode("utf-8", errors="replace").strip().casefold()
    return diagnostic == expected


def _inspection_error_message(result: CommandResult) -> str:
    """Create bounded diagnostics for a Docker inspection failure."""
    diagnostic = _diagnostic_text(result.stderr or result.stdout)
    message = (
        f"Docker could not inspect owned vLLM container (exit {result.exit_code})."
    )
    return f"{message} {diagnostic}" if diagnostic else message


def _launch_error_message(result: CommandResult) -> str:
    """Create bounded launch diagnostics from a nonzero Docker result."""
    diagnostic = _diagnostic_text(result.stderr or result.stdout)
    message = f"Docker rejected vLLM launch with exit code {result.exit_code}."
    return f"{message} {diagnostic}" if diagnostic else message


def _diagnostic_text(data: bytes) -> str:
    """Decode a bounded command-output prefix for an error message."""
    return data[:_MAX_DIAGNOSTIC_BYTES].decode("utf-8", errors="replace").strip()
~~~~

### src/devtools/resources/commands/__init__.py:4-38

Resource `45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3`; content `7cbc6f6b95697b5c664eb09d2779fe854fedb8d868e046e913bed2ce2fbb30b3`; characters [80, 889).

~~~~text
from devtools.resources.commands.errors import (
    CommandError,
    CommandNotFoundError,
    CommandTimeoutError,
)
from devtools.resources.commands.events import (
    CommandEvent,
    CommandExited,
    CommandStarted,
    CommandStderr,
    CommandStdout,
)
from devtools.resources.commands.execution import CommandExecutor
from devtools.resources.commands.handle import CommandExecution
from devtools.resources.commands.models import (
    Command,
    CommandOutputPolicy,
    CommandResult,
)

__all__ = [
    "Command",
    "CommandError",
    "CommandEvent",
    "CommandExecution",
    "CommandExecutor",
    "CommandExited",
    "CommandNotFoundError",
    "CommandOutputPolicy",
    "CommandResult",
    "CommandStarted",
    "CommandStderr",
    "CommandStdout",
    "CommandTimeoutError",
]
~~~~

### src/devtools/resources/commands/docs/command.md:1-71

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [0, 2115).

~~~~text
# Command values, policy, and results

See the [package overview](overview.md), [execution lifecycle](execution.md),
and [events/output semantics](events.md).

## `Command`

```python
Command(
    executable: str,
    arguments: tuple[str, ...] = (),
    working_directory: ResolvedPath | None = None,
    timeout: Duration | None = None,
)
```

`Command` is a frozen, slotted value object. Blank executables are invalid.
The executable and arguments remain separate; no shell parsing, interpolation,
or quoting occurs. `argv` returns the complete tuple passed to process launch.

All fluent methods return new values:

```text
args(...)             append arguments
with_args(...)        replace arguments
without_args()        clear arguments
with_executable(...)  replace and validate executable
cwd(...)              set ResolvedPath working directory
without_cwd()         clear working directory
with_timeout(...)     set Duration timeout
without_timeout()     clear timeout
```

## `CommandOutputPolicy`

```python
CommandOutputPolicy(
    max_stdout_bytes=1_048_576,
    max_stderr_bytes=1_048_576,
    max_pending_events=1_024,
)
```

Stdout and stderr retention limits are independent. A zero byte limit is valid:
nonempty output remains streamable but no bytes are retained in the final
result, and the matching truncation flag is true. Negative byte limits are
invalid. Pending-event capacity must be positive.

## `CommandResult`

```python
CommandResult(
    command,
    exit_code,
    stdout,
    stderr,
    duration,
    stdout_truncated=False,
    stderr_truncated=False,
    events_dropped=0,
)
```

Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.

Exit code zero means `succeeded`; every nonzero exit code means `failed` but is
still a completed result. Timeout, cancellation, process-creation failure, and
other execution exceptions produce no `CommandResult`.
~~~~

### src/devtools/resources/commands/docs/command.md:6-31

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [160, 981).

~~~~text
## `Command`

```python
Command(
    executable: str,
    arguments: tuple[str, ...] = (),
    working_directory: ResolvedPath | None = None,
    timeout: Duration | None = None,
)
```

`Command` is a frozen, slotted value object. Blank executables are invalid.
The executable and arguments remain separate; no shell parsing, interpolation,
or quoting occurs. `argv` returns the complete tuple passed to process launch.

All fluent methods return new values:

```text
args(...)             append arguments
with_args(...)        replace arguments
without_args()        clear arguments
with_executable(...)  replace and validate executable
cwd(...)              set ResolvedPath working directory
without_cwd()         clear working directory
with_timeout(...)     set Duration timeout
without_timeout()     clear timeout
~~~~

### src/devtools/resources/commands/docs/command.md:34-47

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [986, 1423).

~~~~text
## `CommandOutputPolicy`

```python
CommandOutputPolicy(
    max_stdout_bytes=1_048_576,
    max_stderr_bytes=1_048_576,
    max_pending_events=1_024,
)
```

Stdout and stderr retention limits are independent. A zero byte limit is valid:
nonempty output remains streamable but no bytes are retained in the final
result, and the matching truncation flag is true. Negative byte limits are
invalid. Pending-event capacity must be positive.
~~~~

### src/devtools/resources/commands/docs/command.md:44-67

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [1144, 1900).

~~~~text
Stdout and stderr retention limits are independent. A zero byte limit is valid:
nonempty output remains streamable but no bytes are retained in the final
result, and the matching truncation flag is true. Negative byte limits are
invalid. Pending-event capacity must be positive.

## `CommandResult`

```python
CommandResult(
    command,
    exit_code,
    stdout,
    stderr,
    duration,
    stdout_truncated=False,
    stderr_truncated=False,
    events_dropped=0,
)
```

Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.
~~~~

### src/devtools/resources/commands/docs/command.md:49-67

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [1424, 1900).

~~~~text
## `CommandResult`

```python
CommandResult(
    command,
    exit_code,
    stdout,
    stderr,
    duration,
    stdout_truncated=False,
    stderr_truncated=False,
    events_dropped=0,
)
```

Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.
~~~~

### src/devtools/resources/commands/docs/command.md:49-71

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [1424, 2115).

~~~~text
## `CommandResult`

```python
CommandResult(
    command,
    exit_code,
    stdout,
    stderr,
    duration,
    stdout_truncated=False,
    stderr_truncated=False,
    events_dropped=0,
)
```

Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.

Exit code zero means `succeeded`; every nonzero exit code means `failed` but is
still a completed result. Timeout, cancellation, process-creation failure, and
other execution exceptions produce no `CommandResult`.
~~~~

### src/devtools/resources/commands/docs/command.md:64-67

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [1620, 1900).

~~~~text
Results are frozen value objects. Stdout/stderr remain bytes and contain only
the retained leading prefix allowed by the policy; they are not necessarily the
complete process output. Truncation flags report omitted retained bytes, and
`events_dropped` reports bounded-queue loss.
~~~~

### src/devtools/resources/commands/docs/command.md:69-71

Resource `cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c`; content `dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219`; characters [1901, 2115).

~~~~text
Exit code zero means `succeeded`; every nonzero exit code means `failed` but is
still a completed result. Timeout, cancellation, process-creation failure, and
other execution exceptions produce no `CommandResult`.
~~~~

### src/devtools/resources/commands/docs/events.md:28-53

Resource `86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f`; content `376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c`; characters [556, 1758).

~~~~text
Ordering within stdout and within stderr is preserved. Interleaving between the
two streams is not guaranteed.

## `events()`

`execution.events()` is a single-consumer async stream. The claim occurs when
iteration begins; a second consumer attempt raises `RuntimeError`. Streams
close on normal completion, missing executable, timeout, cancellation, and
unexpected stream-read failure.

## Bounded queue and drop policy

The pending queue is bounded by `CommandOutputPolicy.max_pending_events`.
Producers never block when full: any newly emitted event is dropped, and
`events_dropped` records the total. No event type is privileged, so
`CommandExited` may be dropped under pressure. Event delivery is best effort.

## Event bytes versus result bytes

Process streams are read in bounded chunks and fully drained during normal
completion. Result retention independently stores only the leading stdout and
stderr prefixes allowed by the output policy. Bytes beyond a limit are omitted
from `CommandResult` and set the corresponding truncation flag.

An output event may therefore contain bytes that are absent from final retained
result output. Queue buffering and result retention are separate bounds.
~~~~

### src/devtools/resources/commands/docs/events.md:45-53

Resource `86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f`; content `376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c`; characters [1272, 1758).

~~~~text
## Event bytes versus result bytes

Process streams are read in bounded chunks and fully drained during normal
completion. Result retention independently stores only the leading stdout and
stderr prefixes allowed by the output policy. Bytes beyond a limit are omitted
from `CommandResult` and set the corresponding truncation flag.

An output event may therefore contain bytes that are absent from final retained
result output. Queue buffering and result retention are separate bounds.
~~~~

### src/devtools/resources/commands/docs/execution.md:17-34

Resource `562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b`; content `0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9`; characters [352, 1157).

~~~~text
`execute()` calls `start()` and awaits the returned handle. `start()` requires
an active asyncio event loop because it immediately creates the underlying
task.

`CommandExecution` owns one task and launches one subprocess. Repeated
successful awaits share that task and return the same `CommandResult` instance.
`is_running` and `is_complete` reflect task state. There is no async context
manager.

## Process creation

Execution uses `asyncio.create_subprocess_exec()` with direct argv, optional
native cwd, and stdout/stderr pipes. There is no shell, stdin, environment
override, or process-group configuration.

If creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with
the original error retained as its cause. No started event or result is
produced, and the event stream closes.
~~~~

### src/devtools/resources/commands/docs/execution.md:26-55

Resource `562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b`; content `0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9`; characters [751, 2062).

~~~~text
## Process creation

Execution uses `asyncio.create_subprocess_exec()` with direct argv, optional
native cwd, and stdout/stderr pipes. There is no shell, stdin, environment
override, or process-group configuration.

If creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with
the original error retained as its cause. No started event or result is
produced, and the event stream closes.

## Timeout

`Duration.total_seconds` configures an asyncio timeout around post-creation
output collection. Process creation time is not included.

On timeout, the running immediate child is killed and awaited/reaped,
`CommandTimeoutError` is raised with the timeout failure as its cause, and the
event stream closes. No `CommandExited` or final result is fabricated. Events
already observed may remain available, but partial retained output is not
exposed through a result.

## Cancellation

Before child creation completes, cancellation closes the stream and propagates.
After creation, a running immediate child is killed and awaited/reaped;
cancellation then propagates unchanged and no exit event is fabricated. An
already-exited child is awaited without another kill.

Awaiters directly await the same task. Cancelling one awaiter can therefore
cancel the shared command execution for all awaiters.
~~~~

### src/devtools/resources/commands/docs/overview.md:9-38

Resource `27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961`; content `7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8`; characters [264, 1460).

~~~~text
## Public API

```python
from devtools.resources.commands import (
    Command,
    CommandError,
    CommandEvent,
    CommandExecution,
    CommandExecutor,
    CommandExited,
    CommandNotFoundError,
    CommandOutputPolicy,
    CommandResult,
    CommandStarted,
    CommandStderr,
    CommandStdout,
    CommandTimeoutError,
)
```

| Group              | API                                                                                 |
|--------------------|-------------------------------------------------------------------------------------|
| Specification      | `Command`                                                                           |
| Execution          | `CommandExecutor`, `CommandExecution`                                               |
| Events             | `CommandEvent`, `CommandStarted`, `CommandStdout`, `CommandStderr`, `CommandExited` |
| Results and policy | `CommandResult`, `CommandOutputPolicy`                                              |
| Errors             | `CommandError`, `CommandNotFoundError`, `CommandTimeoutError`                       |

`CommandEvent` is a type alias for the concrete event values, not a runtime
event superclass.
~~~~

### src/devtools/resources/commands/docs/overview.md:40-55

Resource `27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961`; content `7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8`; characters [1461, 1762).

~~~~text
## Architecture

```text
Command
   ↓
CommandExecutor.start()
   ↓
CommandExecution
   ├── events()
   └── await
        ↓
   CommandResult
```

`execute()` is the convenience start-and-await path. See [command values](command.md),
[execution lifecycle](execution.md), and [events/output](events.md).
~~~~

### src/devtools/resources/commands/docs/overview.md:65-79

Resource `27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961`; content `7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8`; characters [2060, 2467).

~~~~text
## Errors

```text
CommandError
├── CommandNotFoundError
└── CommandTimeoutError
```

A nonzero process exit is a normal `CommandResult`, not an exception.

## Limitations and future evolution

Execution manages only the immediate child process. Output/event observation is
bounded and best effort. Shell mode, stdin, environment overrides, process
groups, pipelines, retries, and text decoding are absent.
~~~~

### src/devtools/resources/commands/errors.py:5-14

Resource `28033b6d9764ac5ab1c511d43af2440a24f1bf4bfeec8f9a15b5d40bbdcf3eee`; content `9f9b4159a7d8209d3cbd5101f6d1d5530b0768e6e72b61d8a64aecfa3ba55d7f`; characters [91, 391).

~~~~text
class CommandError(Exception):
    """Base exception for command-execution failures."""


class CommandNotFoundError(CommandError):
    """Raised when the requested executable cannot be found."""


class CommandTimeoutError(CommandError):
    """Raised when command execution exceeds its timeout."""
~~~~

### src/devtools/resources/commands/events.py:14-56

Resource `0f3ef2acc2faa6fea579de696653cfe7ed50c178f6f5939a0be590b29d105a37`; content `7bfe93cebfef47011047122901ad9756b95d28dfd82a228993d46eb8670344a6`; characters [292, 1181).

~~~~text
@dataclass(frozen=True, slots=True)
class CommandStarted:
    """Represent the start of a command execution.

    :ivar command: Command that started executing.
    """

    command: Command


@dataclass(frozen=True, slots=True)
class CommandStdout:
    """Represent bytes emitted to standard output.

    :ivar data: Bytes emitted by the process.
    """

    data: bytes


@dataclass(frozen=True, slots=True)
class CommandStderr:
    """Represent bytes emitted to standard error.

    :ivar data: Bytes emitted by the process.
    """

    data: bytes


@dataclass(frozen=True, slots=True)
class CommandExited:
    """Represent completion of a command process.

    :ivar exit_code: Process exit code.
    :ivar duration: Total elapsed execution duration.
    """

    exit_code: int
    duration: Duration


CommandEvent = CommandStarted | CommandStdout | CommandStderr | CommandExited
~~~~

### src/devtools/resources/commands/execution.py:39-76

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [844, 2078).

~~~~text
class CommandExecutor:
    """Execute commands asynchronously."""

    def __init__(
        self,
        *,
        output_policy: CommandOutputPolicy = _DEFAULT_OUTPUT_POLICY,
    ) -> None:
        """Create a command executor.

        :param output_policy: Per-execution output-retention limits.
        """
        self._output_policy = output_policy

    def start(self, command: Command) -> CommandExecution:
        """Start a command and return its live execution handle.

        The returned execution begins immediately and may be awaited for the
        final result or observed through its event stream.

        :param command: Command to execute.
        :returns: Live command execution.
        """
        return CommandExecution(
            partial(self._run, command),
            max_pending_events=self._output_policy.max_pending_events,
        )

    async def execute(self, command: Command) -> CommandResult:
        """Execute a command and await its final result.

        This is the convenience API for callers that do not need live event
        streaming.

        :param command: Command to execute.
        :returns: Completed command result.
        """
        return await self.start(command)
~~~~

### src/devtools/resources/commands/execution.py:78-207

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [2079, 6340).

~~~~text
    async def _run(
        self,
        command: Command,
        execution: CommandExecution,
    ) -> CommandResult:
        """Run one command execution.

        :param command: Command to execute.
        :param execution: Live execution receiving emitted events.
        :returns: Completed command result.
        :raises CommandNotFoundError: If the executable cannot be found.
        :raises CommandTimeoutError: If execution exceeds its timeout.
        :raises CommandError: If the process completes without an exit code.
        """
        stopwatch = Stopwatch()
        process: asyncio.subprocess.Process | None = None

        try:
            process = await self._create_process(command)

            execution._emit(CommandStarted(command=command))  # noqa: SLF001

            try:
                (
                    stdout,
                    stderr,
                    stdout_truncated,
                    stderr_truncated,
                ) = await self._collect_output(
                    process,
                    execution,
                    command,
                )
            except TimeoutError as error:
                await self._terminate_and_reap(process)
                process = None

                timeout = command.timeout

                if timeout is None:
                    msg = "Command timed out without a configured timeout."
                    raise CommandError(msg) from error

                msg = (
                    f"Command exceeded timeout of "
                    f"{timeout.total_seconds} seconds: "
                    f"{command.executable!r}."
                )
                raise CommandTimeoutError(msg) from error

        except asyncio.CancelledError:
            if process is not None:
                await self._terminate_and_reap(process)

            raise
        except (CommandNotFoundError, CommandTimeoutError):
            raise
        except Exception:
            if process is not None:
                await self._terminate_and_reap(process)

            raise

        else:
            duration = stopwatch.stop()
            exit_code = process.returncode

            if exit_code is None:
                msg = (
                    "Command process completed without an exit code: "
                    f"{command.executable!r}."
                )
                raise CommandError(msg)

            result = CommandResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                stdout_truncated=stdout_truncated,
                stderr_truncated=stderr_truncated,
            )

            execution._emit(  # noqa: SLF001
                CommandExited(
                    exit_code=exit_code,
                    duration=duration,
                ),
            )

            return replace(result, events_dropped=execution.events_dropped)
        finally:
            stopwatch.stop()
            execution._close_events()  # noqa: SLF001

    async def _terminate_and_reap(
        self,
        process: asyncio.subprocess.Process,
    ) -> None:
        """Terminate and reap a running immediate child process."""
        if process.returncode is None:
            process.kill()

        await process.wait()

    async def _create_process(
        self,
        command: Command,
    ) -> asyncio.subprocess.Process:
        """Create the subprocess for a command.

        :param command: Command to execute.
        :returns: Running subprocess.
        :raises CommandNotFoundError: If the executable cannot be found.
        """
        try:
            return await asyncio.create_subprocess_exec(
                *command.argv,
                cwd=(
                    command.working_directory.value
                    if command.working_directory is not None
                    else None
                ),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError as error:
            msg = f"Command executable not found: {command.executable!r}."
            raise CommandNotFoundError(msg) from error
~~~~

### src/devtools/resources/commands/execution.py:141-169

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [4154, 5073).

~~~~text
        else:
            duration = stopwatch.stop()
            exit_code = process.returncode

            if exit_code is None:
                msg = (
                    "Command process completed without an exit code: "
                    f"{command.executable!r}."
                )
                raise CommandError(msg)

            result = CommandResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                stdout_truncated=stdout_truncated,
                stderr_truncated=stderr_truncated,
            )

            execution._emit(  # noqa: SLF001
                CommandExited(
                    exit_code=exit_code,
                    duration=duration,
                ),
            )

            return replace(result, events_dropped=execution.events_dropped)
~~~~

### src/devtools/resources/commands/execution.py:152-160

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [4487, 4806).

~~~~text
            result = CommandResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                stdout_truncated=stdout_truncated,
                stderr_truncated=stderr_truncated,
            )
~~~~

### src/devtools/resources/commands/execution.py:152-169

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [4487, 5073).

~~~~text
            result = CommandResult(
                command=command,
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                stdout_truncated=stdout_truncated,
                stderr_truncated=stderr_truncated,
            )

            execution._emit(  # noqa: SLF001
                CommandExited(
                    exit_code=exit_code,
                    duration=duration,
                ),
            )

            return replace(result, events_dropped=execution.events_dropped)
~~~~

### src/devtools/resources/commands/execution.py:236-303

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [7245, 9512).

~~~~text
    async def _stream_process(
        self,
        process: asyncio.subprocess.Process,
        execution: CommandExecution,
        output_policy: CommandOutputPolicy,
    ) -> tuple[bytes, bytes, bool, bool]:
        """Stream subprocess output while retaining bounded output prefixes.

        Process streams are fully drained during normal completion. Returned
        bytes contain only the leading prefix retained by the output policy.

        :param process: Running subprocess.
        :param execution: Live execution receiving events.
        :returns: Complete stdout and stderr byte sequences.
        """
        if process.stdout is None or process.stderr is None:
            msg = "Command subprocess streams were not created."
            raise CommandError(msg)

        stdout_task = asyncio.create_task(
            self._read_stream(
                process.stdout,
                execution._emit,  # noqa: SLF001
                CommandStdout,
                output_policy.max_stdout_bytes,
            ),
        )
        stderr_task = asyncio.create_task(
            self._read_stream(
                process.stderr,
                execution._emit,  # noqa: SLF001
                CommandStderr,
                output_policy.max_stderr_bytes,
            ),
        )

        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(
            stdout_task,
            stderr_task,
        )

        await process.wait()

        return stdout, stderr, stdout_truncated, stderr_truncated

    async def _read_stream(
        self,
        stream: asyncio.StreamReader,
        emit: Callable[[CommandEvent], None],
        event_type: type[CommandStdout | CommandStderr],
        max_output_bytes: int,
    ) -> tuple[bytes, bool]:
        """Read, emit, and retain bounded chunks from one subprocess stream."""
        output = bytearray()
        truncated = False

        while chunk := await stream.read(8192):
            remaining = max_output_bytes - len(output)

            if remaining > 0:
                output.extend(chunk[:remaining])

            if len(chunk) > remaining:
                truncated = True

            emit(event_type(data=chunk))

        return bytes(output), truncated
~~~~

### src/devtools/resources/commands/execution.py:281-303

Resource `fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3`; content `5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22`; characters [8794, 9512).

~~~~text
    async def _read_stream(
        self,
        stream: asyncio.StreamReader,
        emit: Callable[[CommandEvent], None],
        event_type: type[CommandStdout | CommandStderr],
        max_output_bytes: int,
    ) -> tuple[bytes, bool]:
        """Read, emit, and retain bounded chunks from one subprocess stream."""
        output = bytearray()
        truncated = False

        while chunk := await stream.read(8192):
            remaining = max_output_bytes - len(output)

            if remaining > 0:
                output.extend(chunk[:remaining])

            if len(chunk) > remaining:
                truncated = True

            emit(event_type(data=chunk))

        return bytes(output), truncated
~~~~

### src/devtools/resources/commands/handle.py:79-133

Resource `87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9`; content `c9825687577803f98911494be5c86ddd84af006d627acdbacbc2b28d9c82b06c`; characters [2188, 3938).

~~~~text
    @property
    def events_dropped(self) -> int:
        """Return the number of events omitted by bounded buffering.

        Any newly emitted event may be dropped while the queue is full; no event
        type, including lifecycle events, is privileged.

        :returns: Number of events dropped before observation.
        """
        return self._events_dropped

    async def events(self) -> AsyncIterator[CommandEvent]:
        """Yield structured events emitted by the execution.

        Only one consumer may iterate the event stream for a given execution.

        :yields: Command execution events.
        :raises RuntimeError: If the event stream has already been claimed.
        """
        if self._events_claimed:
            msg = "Command execution events may only be consumed once."
            raise RuntimeError(msg)

        self._events_claimed = True

        while True:
            try:
                event = self._event_queue.get_nowait()
            except asyncio.QueueEmpty:
                if self._events_closed:
                    return

                await self._event_available.wait()
                self._event_available.clear()
                continue

            yield event

    def _emit(self, event: CommandEvent) -> None:
        """Emit an execution event when bounded queue capacity permits it.

        :param event: Event to emit.
        """
        try:
            self._event_queue.put_nowait(event)
        except asyncio.QueueFull:
            self._events_dropped += 1
            return

        self._event_available.set()

    def _close_events(self) -> None:
        """Close the execution event stream."""
        self._events_closed = True
        self._event_available.set()
~~~~

### src/devtools/resources/commands/models/__init__.py:1-14

Resource `161aa54cca99eaed6de081d4617501fc18a54d6c9b9fe2fc35d28d1831f91ad6`; content `663fbad9d358d6ebb6f849fe60b189a4fc48bbf688ec809f3122929d7c68836f`; characters [0, 394).

~~~~text
# Copyright (c) 2026
"""Command value objects."""

from devtools.resources.commands.models.command import Command as Command
from devtools.resources.commands.models.output import (
    CommandOutputPolicy as CommandOutputPolicy,
)
from devtools.resources.commands.models.result import CommandResult as CommandResult

__all__ = [
    "Command",
    "CommandOutputPolicy",
    "CommandResult",
]
~~~~

### src/devtools/resources/commands/models/command.py:14-62

Resource `1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629`; content `b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473`; characters [283, 1816).

~~~~text
@dataclass(frozen=True, slots=True)
class Command:
    """Describe an immutable command execution specification.

    A command identifies an executable separately from its arguments and does
    not imply shell parsing, interpolation, or quoting.

    Fluent methods return new command instances and never mutate the original.

    Example::

        command = (
            Command("uv")
            .args("run", "pytest", "-q")
            .cwd(project_root)
            .with_timeout(Duration.minutes(2))
        )

    :ivar executable: Executable name or path.
    :ivar arguments: Ordered executable arguments.
    :ivar working_directory: Optional resolved working directory.
    :ivar timeout: Optional maximum execution duration.
    """

    executable: str
    arguments: tuple[str, ...] = ()
    working_directory: ResolvedPath | None = None
    timeout: Duration | None = None

    def __post_init__(self) -> None:
        """Validate command invariants."""
        self._validate()

    def _validate(self) -> None:
        """Validate the command specification.

        :raises ValueError: If the executable is empty or whitespace-only.
        """
        if not self.executable.strip():
            msg = "Command executable cannot be empty."
            raise ValueError(msg)

    @property
    def argv(self) -> tuple[str, ...]:
        """Return the complete process argument vector.

        :returns: Executable followed by all ordered arguments.
        """
        return (self.executable, *self.arguments)
~~~~

### src/devtools/resources/commands/models/output.py:7-23

Resource `7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d`; content `bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336`; characters [97, 829).

~~~~text
@dataclass(frozen=True, slots=True)
class CommandOutputPolicy:
    """Bound memory retained for one command execution.

    Output limits apply independently to standard output and standard error.
    Event buffering is best effort: any newly emitted event is dropped when the
    pending event limit is reached so process draining never waits for a
    consumer. No event type is privileged.

    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.
    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.
    :ivar max_pending_events: Maximum events awaiting the single consumer.
    """

    max_stdout_bytes: int = 1_048_576
    max_stderr_bytes: int = 1_048_576
    max_pending_events: int = 1_024
~~~~

### src/devtools/resources/commands/models/output.py:7-37

Resource `7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d`; content `bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336`; characters [97, 1323).

~~~~text
@dataclass(frozen=True, slots=True)
class CommandOutputPolicy:
    """Bound memory retained for one command execution.

    Output limits apply independently to standard output and standard error.
    Event buffering is best effort: any newly emitted event is dropped when the
    pending event limit is reached so process draining never waits for a
    consumer. No event type is privileged.

    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.
    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.
    :ivar max_pending_events: Maximum events awaiting the single consumer.
    """

    max_stdout_bytes: int = 1_048_576
    max_stderr_bytes: int = 1_048_576
    max_pending_events: int = 1_024

    def __post_init__(self) -> None:
        """Validate output-retention invariants."""
        if self.max_stdout_bytes < 0:
            msg = "Maximum stdout bytes cannot be negative."
            raise ValueError(msg)

        if self.max_stderr_bytes < 0:
            msg = "Maximum stderr bytes cannot be negative."
            raise ValueError(msg)

        if self.max_pending_events <= 0:
            msg = "Maximum pending events must be positive."
            raise ValueError(msg)
~~~~

### src/devtools/resources/commands/models/result.py:14-39

Resource `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`; content `9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23`; characters [274, 1308).

~~~~text
@dataclass(frozen=True, slots=True)
class CommandResult:
    """Represent the completed result of a command execution.

    A nonzero exit code is a valid command result and does not itself represent
    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`
    when interpreting the command's exit status.

    :ivar command: Command that was executed.
    :ivar exit_code: Process exit code.
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    events_dropped: int = 0
~~~~

### src/devtools/resources/commands/models/result.py:14-55

Resource `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`; content `9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23`; characters [274, 1729).

~~~~text
@dataclass(frozen=True, slots=True)
class CommandResult:
    """Represent the completed result of a command execution.

    A nonzero exit code is a valid command result and does not itself represent
    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`
    when interpreting the command's exit status.

    :ivar command: Command that was executed.
    :ivar exit_code: Process exit code.
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    events_dropped: int = 0

    @property
    def succeeded(self) -> bool:
        """Return whether the command exited successfully.

        :returns: ``True`` when the exit code is zero.
        """
        return self.exit_code == 0

    @property
    def failed(self) -> bool:
        """Return whether the command exited unsuccessfully.

        :returns: ``True`` when the exit code is nonzero.
        """
        return not self.succeeded
~~~~

### src/devtools/resources/commands/models/result.py:22-39

Resource `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`; content `9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23`; characters [604, 1308).

~~~~text
    :ivar command: Command that was executed.
    :ivar exit_code: Process exit code.
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    events_dropped: int = 0
~~~~

### src/devtools/resources/commands/models/result.py:24-38

Resource `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`; content `9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23`; characters [690, 1280).

~~~~text
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
~~~~

### src/devtools/resources/commands/models/result.py:24-39

Resource `5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5`; content `9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23`; characters [690, 1308).

~~~~text
    :ivar stdout: Retained leading bytes written to standard output.
    :ivar stderr: Retained leading bytes written to standard error.
    :ivar duration: Monotonic elapsed execution duration.
    :ivar stdout_truncated: Whether stdout exceeded the retained limit.
    :ivar stderr_truncated: Whether stderr exceeded the retained limit.
    :ivar events_dropped: Number of events omitted by bounded buffering.
    """

    command: Command
    exit_code: int
    stdout: bytes
    stderr: bytes
    duration: Duration
    stdout_truncated: bool = False
    stderr_truncated: bool = False
    events_dropped: int = 0
~~~~

### tests/agents/integrations/codex/test_agent.py:49-78

Resource `37524b1f8eb0f2d9faa0ab850fdf52deae56ea57ed9665ba581ccf38cd143d2e`; content `4c3636ded84b2b1feeebc2b27132308a34c2827098bde9be25d13450a647d607`; characters [1273, 2455).

~~~~text
class RecordingExecutor(CommandExecutor):
    """CommandExecutor fake retaining direct-argv invocations."""

    def __init__(self, results: Sequence[tuple[int, bytes, bool]]) -> None:
        """Initialize the queued result specifications."""
        super().__init__()
        self.commands: list[Command] = []
        self._results = list(results)

    async def execute(self, command: Command) -> CommandResult:
        """Return the next captured deterministic command result."""
        self.commands.append(command)
        exit_code, stdout, stdout_truncated = self._results.pop(0)
        return CommandResult(
            command=command,
            exit_code=exit_code,
            stdout=stdout,
            stderr=b"diagnostic output is intentionally ignored",
            duration=Duration.seconds(0),
            stdout_truncated=stdout_truncated,
        )


class MissingExecutor(CommandExecutor):
    """CommandExecutor fake preserving the command-domain missing binary error."""

    async def execute(self, _command: Command) -> CommandResult:
        """Raise the same error emitted by a missing executable at execution."""
        raise CommandNotFoundError
~~~~

### tests/core/time/test_models.py:64-83

Resource `d72f337252161b196dcd8aebdec5da0dcd2a063ff3b4882530b54dbf87d5fbb6`; content `0738320772b65625e0085212c949e34b4185fcf58ebe093ed4d45a8d358b6660`; characters [2136, 3168).

~~~~text
def test_duration_factories_create_expected_values() -> None:
    """Each public duration factory delegates to its documented unit."""
    assert Duration.nanoseconds(2_000).value == timedelta(microseconds=2)
    assert Duration.seconds(2.5).value == timedelta(seconds=2.5)
    assert Duration.milliseconds(2.5).value == timedelta(milliseconds=2.5)
    assert Duration.minutes(2.5).value == timedelta(minutes=2.5)
    assert Duration.hours(2.5).value == timedelta(hours=2.5)


def test_duration_accessors_string_and_value_semantics() -> None:
    """Duration representations expose the underlying elapsed amount."""
    expected_seconds = 1.25
    expected_milliseconds = 1250.0
    duration = Duration(timedelta(seconds=expected_seconds))

    assert duration.total_seconds == expected_seconds
    assert duration.total_milliseconds == expected_milliseconds
    assert str(duration) == "0:00:01.250000"
    assert duration == Duration.seconds(expected_seconds)
    assert hash(duration) == hash(Duration.seconds(expected_seconds))
~~~~

### tests/models/serving/test_llama_cpp.py:29-63

Resource `a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402`; content `2de258ff8b06e27cb3a0642c77839aef7a6511a39b5809a3dad19029b32c13df`; characters [785, 1936).

~~~~text
def _result(
    command: Command,
    code: int = 0,
    out: bytes = b"",
    err: bytes = b"",
) -> CommandResult:
    return CommandResult(command, code, out, err, Duration.seconds(0))


def _config(tmp_path: Path, **changes: object) -> llama_cpp.LlamaCppServingConfig:
    model = tmp_path / "model.gguf"
    model.touch(exist_ok=True)
    values: dict[str, object] = {
        "model": llama_cpp.GGUFModel(ResolvedPath(model)),
        "image": "ghcr.io/ggml-org/llama.cpp:server-cuda",
        "host_port": 8081,
        "served_model_name": "local-model",
        "context_size": 4096,
        "gpu_layers": "all",
    }
    values.update(changes)
    return llama_cpp.LlamaCppServingConfig(**values)  # type: ignore[arg-type]


class _Executor(CommandExecutor):
    def __init__(self, results: list[CommandResult | BaseException]) -> None:
        self.commands: list[Command] = []
        self.results = results

    async def execute(self, command: Command) -> CommandResult:
        self.commands.append(command)
        value = self.results.pop(0)
        if isinstance(value, BaseException):
            raise value
        return value
~~~~

### tests/models/serving/test_vllm.py:59-99

Resource `27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684`; content `66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8`; characters [1777, 3148).

~~~~text
def _result(
    command: Command,
    *,
    exit_code: int = 0,
    stdout: bytes = b"",
    stderr: bytes = b"diagnostic",
) -> CommandResult:
    """Create a compact ordinary command result."""
    return CommandResult(command, exit_code, stdout, stderr, Duration.seconds(0))


def _not_found_result(command: Command) -> CommandResult:
    """Create Docker's exact absent-container inspection result."""
    return _result(
        command,
        exit_code=1,
        stderr=f"Error: No such object: {_VALID_CONTAINER_ID}".encode(),
    )


def _assert_no_prefetch_arguments(command: Command) -> None:
    """Require that a historical command has no prefetch provider flags."""
    assert all(option not in command.arguments for option in _PREFETCH_OPTIONS)


class _Executor:
    """Record commands and return queued results or errors."""

    def __init__(self, responses: list[CommandResult | BaseException]) -> None:
        """Initialize queued execution behavior."""
        self.commands: list[Command] = []
        self._responses = responses

    async def execute(self, command: Command) -> CommandResult:
        """Record one command and apply the next planned outcome."""
        self.commands.append(command)
        response = self._responses.pop(0)
        if isinstance(response, BaseException):
            raise response

        return response
~~~~

### tests/resources/commands/test_errors.py:4-15

Resource `4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5`; content `16db7e62541ee215137cacf568e3631473a1ae31de96f0c998ddb73bb7cdf3ac`; characters [73, 491).

~~~~text
from devtools.resources.commands import (
    CommandError,
    CommandNotFoundError,
    CommandTimeoutError,
)


def test_command_errors_share_the_domain_base_type() -> None:
    """Specific command errors remain catchable as command-domain failures."""
    assert issubclass(CommandNotFoundError, CommandError)
    assert issubclass(CommandTimeoutError, CommandError)
    assert issubclass(CommandError, Exception)
~~~~

### tests/resources/commands/test_events.py:18-34

Resource `e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295`; content `229c76e8ba2d20feec3734c5a62f02b1c08941aa09daa90702d41cdafc6669ee`; characters [311, 1023).

~~~~text
def test_command_events_are_immutable_value_objects() -> None:
    """Each event retains its structured observation data immutably."""
    command = Command("python", ("-c", "pass"))
    started = CommandStarted(command)
    stdout = CommandStdout(b"out")
    stderr = CommandStderr(b"error")
    exited = CommandExited(0, Duration.seconds(1))
    attribute = "data"

    assert started == CommandStarted(command)
    assert stdout == CommandStdout(b"out")
    assert stderr == CommandStderr(b"error")
    assert exited == CommandExited(0, Duration.seconds(1))
    assert hash(started) == hash(CommandStarted(command))

    with pytest.raises(FrozenInstanceError):
        setattr(stdout, attribute, b"changed")
~~~~

### tests/resources/commands/test_execution.py:29-56

Resource `6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a`; content `aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283`; characters [556, 1553).

~~~~text
def test_executor_runs_python_and_preserves_argument_bytes() -> None:
    """The executor captures raw output from a portable Python subprocess."""
    command = Command(
        sys.executable,
        ("-c", "import sys; print('|'.join(sys.argv[1:]))", "first", "second"),
    )

    result = asyncio.run(CommandExecutor().execute(command))

    assert result.succeeded is True
    assert result.stdout.strip() == b"first|second"
    assert result.stderr == b""
    assert isinstance(result.duration, Duration)
    assert result.duration.total_seconds >= 0


def test_executor_returns_nonzero_exit_codes_as_results() -> None:
    """A process failure code is represented without an execution exception."""
    expected_exit_code = 7
    command = Command(
        sys.executable,
        ("-c", f"import sys; sys.exit({expected_exit_code})"),
    )

    result = asyncio.run(CommandExecutor().execute(command))

    assert result.exit_code == expected_exit_code
    assert result.failed is True
~~~~

### tests/resources/commands/test_execution.py:190-265

Resource `6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a`; content `aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283`; characters [5617, 7968).

~~~~text
def test_executor_bounds_retained_output_and_pending_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Configured limits truncate retained bytes and drop excess queued events."""
    process = _OutputProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _OutputProcess:
        return process

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def run() -> None:
        executor = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=3,
                max_stderr_bytes=2,
                max_pending_events=1,
            ),
        )
        execution = executor.start(Command("bounded-output-command"))
        result = await execution
        events = [event async for event in execution.events()]

        assert result.stdout == b"abc"
        assert result.stderr == b"wx"
        assert result.stdout_truncated is True
        assert result.stderr_truncated is True
        expected_dropped_events = 4

        assert result.events_dropped == expected_dropped_events
        assert len(events) == 1
        assert not any(isinstance(event, CommandExited) for event in events)

    asyncio.run(run())


def test_executor_allows_zero_output_retention_while_streaming(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Zero limits retain no bytes but do not prevent normal completion."""
    process = _OutputProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _OutputProcess:
        return process

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def run() -> None:
        executor = CommandExecutor(
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=0,
                max_stderr_bytes=0,
                max_pending_events=10,
            ),
        )
        result = await executor.execute(Command("zero-retention-command"))

        assert result.stdout == b""
        assert result.stderr == b""
        assert result.stdout_truncated is True
        assert result.stderr_truncated is True
        assert result.succeeded is True

    asyncio.run(run())
~~~~

### tests/resources/commands/test_execution.py:366-408

Resource `6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a`; content `aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283`; characters [10744, 12084).

~~~~text
class _OutputProcess:
    """Minimal completed process producing output beyond configured bounds."""

    def __init__(self) -> None:
        """Initialize deterministic output streams and completion state."""
        self.returncode: int | None = None
        self.stderr = _ChunkStream((b"wxyz",))
        self.stdout = _ChunkStream((b"abc", b"def"))

    async def wait(self) -> None:
        """Mark the process as successfully completed."""
        self.returncode = 0


class _EmptyStream:
    """Minimal stream fake that is immediately exhausted."""

    async def read(self, _size: int) -> bytes:
        """Return end-of-stream bytes."""
        return b""


class _TimeoutStream:
    """Minimal stream fake that reports a deterministic timeout."""

    async def read(self, _size: int) -> bytes:
        """Raise the timeout handled by the executor lifecycle."""
        raise TimeoutError


class _ChunkStream:
    """Minimal stream fake that returns a fixed sequence of chunks."""

    def __init__(self, chunks: tuple[bytes, ...]) -> None:
        """Initialize the remaining chunk sequence."""
        self._chunks = list(chunks)

    async def read(self, _size: int) -> bytes:
        """Return the next chunk or end-of-stream bytes."""
        if not self._chunks:
            return b""

        return self._chunks.pop(0)
~~~~

### tests/resources/commands/test_handle.py:25-76

Resource `4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43`; content `a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712`; characters [420, 2100).

~~~~text
def test_start_returns_one_awaitable_execution_handle() -> None:
    """A started command should create one awaitable live execution handle."""

    async def run() -> None:
        execution = CommandExecutor().start(
            Command(sys.executable, ("-c", "print('once')")),
        )

        assert isinstance(execution, CommandExecution)
        assert execution.is_running is True
        assert execution.is_complete is False

        first = await execution
        second = await execution

        assert first is second
        assert first.stdout.strip() == b"once"
        assert execution.is_running is False
        assert execution.is_complete is True

    asyncio.run(run())


def test_event_stream_preserves_output_and_closes_before_final_await() -> None:
    """Streaming observations and the final result share one execution."""

    async def run() -> None:
        execution = CommandExecutor().start(
            Command(
                sys.executable,
                (
                    "-c",
                    "import sys; print('out'); print('err', file=sys.stderr)",
                ),
            ),
        )
        events = [event async for event in execution.events()]
        result = await execution

        assert isinstance(events[0], CommandStarted)
        assert any(
            isinstance(event, CommandStdout) and b"out" in event.data
            for event in events
        )
        assert any(
            isinstance(event, CommandStderr) and b"err" in event.data
            for event in events
        )
        assert result.stdout.strip() == b"out"
        assert result.stderr.strip() == b"err"

    asyncio.run(run())
~~~~

### tests/resources/commands/test_handle.py:101-196

Resource `4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43`; content `a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712`; characters [2682, 5763).

~~~~text
def test_missing_executable_closes_the_event_stream(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Failure during process creation does not leave event consumers waiting."""

    async def raise_not_found(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError

    async def run() -> None:
        execution = CommandExecutor().start(Command("missing-command"))
        events = [event async for event in execution.events()]

        assert events == []

        with pytest.raises(CommandNotFoundError):
            await execution

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        raise_not_found,
    )
    asyncio.run(run())


def test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    """Timeout cleanup closes event iteration before propagating the error."""
    process = _TimedOutProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _TimedOutProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(
            Command("slow-command", timeout=Duration.seconds(0.001)),
        )
        events = [event async for event in execution.events()]

        assert len(events) == 1
        assert isinstance(events[0], CommandStarted)

        with pytest.raises(CommandTimeoutError):
            await execution

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_kills_reaps_and_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancelling a live execution cleans up its immediate child process."""
    process = _BlockingProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _BlockingProcess:
        return process

    async def await_execution(execution: CommandExecution) -> None:
        """Await one execution so caller cancellation reaches its task."""
        await execution

    async def run() -> None:
        execution = CommandExecutor().start(Command("blocking-command"))
        events_task = asyncio.create_task(_collect_events(execution))
        awaiter = asyncio.create_task(await_execution(execution))
        shared_awaiter = asyncio.create_task(await_execution(execution))

        await process.stdout.read_started.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        with pytest.raises(asyncio.CancelledError):
            await shared_awaiter

        events = await events_task

        assert process.killed is True
        assert process.waited is True
        assert any(isinstance(event, CommandStarted) for event in events)
        assert not any(isinstance(event, CommandExited) for event in events)

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())
~~~~

### tests/resources/commands/test_handle.py:125-196

Resource `4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43`; content `a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712`; characters [3407, 5763).

~~~~text
def test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:
    """Timeout cleanup closes event iteration before propagating the error."""
    process = _TimedOutProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _TimedOutProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(
            Command("slow-command", timeout=Duration.seconds(0.001)),
        )
        events = [event async for event in execution.events()]

        assert len(events) == 1
        assert isinstance(events[0], CommandStarted)

        with pytest.raises(CommandTimeoutError):
            await execution

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_kills_reaps_and_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancelling a live execution cleans up its immediate child process."""
    process = _BlockingProcess()

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _BlockingProcess:
        return process

    async def await_execution(execution: CommandExecution) -> None:
        """Await one execution so caller cancellation reaches its task."""
        await execution

    async def run() -> None:
        execution = CommandExecutor().start(Command("blocking-command"))
        events_task = asyncio.create_task(_collect_events(execution))
        awaiter = asyncio.create_task(await_execution(execution))
        shared_awaiter = asyncio.create_task(await_execution(execution))

        await process.stdout.read_started.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        with pytest.raises(asyncio.CancelledError):
            await shared_awaiter

        events = await events_task

        assert process.killed is True
        assert process.waited is True
        assert any(isinstance(event, CommandStarted) for event in events)
        assert not any(isinstance(event, CommandExited) for event in events)

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())
~~~~

### tests/resources/commands/test_handle.py:231-301

Resource `4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43`; content `a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712`; characters [6831, 9137).

~~~~text
def test_cancellation_before_process_creation_closes_events(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation while creating a process still closes its event stream."""
    process_creation_started = asyncio.Event()
    process_creation_release = asyncio.Event()

    async def create_process(*_args: object, **_kwargs: object) -> None:
        process_creation_started.set()
        await process_creation_release.wait()

    async def await_execution(
        execution: CommandExecution,
        awaiting_execution: asyncio.Event,
    ) -> None:
        """Await an execution after reporting that cancellation can propagate."""
        awaiting_execution.set()
        await execution

    async def run() -> None:
        execution = CommandExecutor().start(Command("creating-command"))
        events_task = asyncio.create_task(_collect_events(execution))
        awaiting_execution = asyncio.Event()
        awaiter = asyncio.create_task(await_execution(execution, awaiting_execution))

        await process_creation_started.wait()
        await awaiting_execution.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        assert await events_task == []

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())


def test_cancellation_reaps_an_already_exited_process(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation reaps a child without killing it after it has exited."""
    process = _BlockingProcess(returncode=0)

    async def create_process(
        *_args: object,
        **_kwargs: object,
    ) -> _BlockingProcess:
        return process

    async def run() -> None:
        execution = CommandExecutor().start(Command("completed-command"))
        awaiter = asyncio.ensure_future(execution)

        await process.stdout.read_started.wait()
        awaiter.cancel()

        with pytest.raises(asyncio.CancelledError):
            await awaiter

        assert process.killed is False
        assert process.waited is True

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )
    asyncio.run(run())
~~~~

### tests/resources/commands/test_models.py:19-84

Resource `914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4`; content `c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28`; characters [416, 2914).

~~~~text
def test_command_preserves_separate_executable_arguments_and_options(
    tmp_path: Path,
) -> None:
    """Commands retain structured process arguments and optional execution data."""
    command = Command(
        executable="python",
        arguments=("-c", "print('hello')"),
        working_directory=ResolvedPath(tmp_path),
        timeout=Duration.seconds(3),
    )

    assert command.executable == "python"
    assert command.arguments == ("-c", "print('hello')")
    assert command.working_directory == ResolvedPath(tmp_path)
    assert command.timeout == Duration.seconds(3)
    assert command.argv == ("python", "-c", "print('hello')")


def test_command_defaults_to_no_arguments_and_is_immutable() -> None:
    """Commands have an empty argument tuple and frozen value semantics."""
    command = Command("python")
    attribute = "executable"

    assert command.arguments == ()
    assert command == Command("python")
    assert hash(command) == hash(Command("python"))

    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, "other")


def test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:
    """Fluent command methods preserve unrelated immutable specification data."""
    original = (
        Command("python", ("-m",))
        .cwd(ResolvedPath(tmp_path))
        .with_timeout(Duration.seconds(1))
    )
    appended = original.args("pytest", "-q")
    replaced = appended.with_args("-c", "pass")
    cleared = replaced.without_args()
    renamed = cleared.with_executable("python3")
    without_cwd = renamed.without_cwd()
    without_timeout = without_cwd.without_timeout()

    assert original == Command(
        "python",
        ("-m",),
        ResolvedPath(tmp_path),
        Duration.seconds(1),
    )
    assert appended.arguments == ("-m", "pytest", "-q")
    assert replaced.arguments == ("-c", "pass")
    assert cleared.arguments == ()
    assert cleared.working_directory == ResolvedPath(tmp_path)
    assert cleared.timeout == Duration.seconds(1)
    assert renamed.executable == "python3"
    assert renamed.working_directory == ResolvedPath(tmp_path)
    assert renamed.timeout == Duration.seconds(1)
    assert without_cwd.working_directory is None
    assert without_cwd.timeout == Duration.seconds(1)
    assert without_timeout.timeout is None
    assert without_timeout.executable == "python3"

    with pytest.raises(ValueError, match="cannot be empty"):
        renamed.with_executable("   ")
~~~~

### tests/resources/commands/test_models.py:19-147

Resource `914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4`; content `c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28`; characters [416, 4987).

~~~~text
def test_command_preserves_separate_executable_arguments_and_options(
    tmp_path: Path,
) -> None:
    """Commands retain structured process arguments and optional execution data."""
    command = Command(
        executable="python",
        arguments=("-c", "print('hello')"),
        working_directory=ResolvedPath(tmp_path),
        timeout=Duration.seconds(3),
    )

    assert command.executable == "python"
    assert command.arguments == ("-c", "print('hello')")
    assert command.working_directory == ResolvedPath(tmp_path)
    assert command.timeout == Duration.seconds(3)
    assert command.argv == ("python", "-c", "print('hello')")


def test_command_defaults_to_no_arguments_and_is_immutable() -> None:
    """Commands have an empty argument tuple and frozen value semantics."""
    command = Command("python")
    attribute = "executable"

    assert command.arguments == ()
    assert command == Command("python")
    assert hash(command) == hash(Command("python"))

    with pytest.raises(FrozenInstanceError):
        setattr(command, attribute, "other")


def test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:
    """Fluent command methods preserve unrelated immutable specification data."""
    original = (
        Command("python", ("-m",))
        .cwd(ResolvedPath(tmp_path))
        .with_timeout(Duration.seconds(1))
    )
    appended = original.args("pytest", "-q")
    replaced = appended.with_args("-c", "pass")
    cleared = replaced.without_args()
    renamed = cleared.with_executable("python3")
    without_cwd = renamed.without_cwd()
    without_timeout = without_cwd.without_timeout()

    assert original == Command(
        "python",
        ("-m",),
        ResolvedPath(tmp_path),
        Duration.seconds(1),
    )
    assert appended.arguments == ("-m", "pytest", "-q")
    assert replaced.arguments == ("-c", "pass")
    assert cleared.arguments == ()
    assert cleared.working_directory == ResolvedPath(tmp_path)
    assert cleared.timeout == Duration.seconds(1)
    assert renamed.executable == "python3"
    assert renamed.working_directory == ResolvedPath(tmp_path)
    assert renamed.timeout == Duration.seconds(1)
    assert without_cwd.working_directory is None
    assert without_cwd.timeout == Duration.seconds(1)
    assert without_timeout.timeout is None
    assert without_timeout.executable == "python3"

    with pytest.raises(ValueError, match="cannot be empty"):
        renamed.with_executable("   ")


@pytest.mark.parametrize("executable", ["", "   "])
def test_command_rejects_blank_executables(executable: str) -> None:
    """Commands require a non-blank executable representation."""
    with pytest.raises(ValueError, match="cannot be empty"):
        Command(executable)


def test_command_result_preserves_bytes_and_exit_status() -> None:
    """Nonzero exit codes remain ordinary completed command results."""
    command = Command("python")
    expected_exit_code = 3
    successful = CommandResult(command, 0, b"out", b"", Duration.seconds(1))
    failed = CommandResult(
        command,
        expected_exit_code,
        b"",
        b"error",
        Duration.seconds(2),
    )

    assert successful.command is command
    assert successful.stdout == b"out"
    assert successful.stderr == b""
    assert successful.duration == Duration.seconds(1)
    assert successful.stdout_truncated is False
    assert successful.stderr_truncated is False
    assert successful.events_dropped == 0
    assert successful.succeeded is True
    assert successful.failed is False
    assert failed.exit_code == expected_exit_code
    assert failed.stdout == b""
    assert failed.stderr == b"error"
    assert failed.succeeded is False
    assert failed.failed is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("max_stdout_bytes", -1, "stdout"),
        ("max_stderr_bytes", -1, "stderr"),
        ("max_pending_events", 0, "pending events"),
    ],
)
def test_command_output_policy_rejects_invalid_bounds(
    field: str,
    value: int,
    match: str,
) -> None:
    """Output limits reject values that cannot form bounded policies."""
    with pytest.raises(ValueError, match=match):
        CommandOutputPolicy(**{field: value})


def test_command_output_policy_exposes_default_bounds() -> None:
    """Default output limits are positive and practical for ordinary commands."""
    policy = CommandOutputPolicy()

    assert policy.max_stdout_bytes > 0
    assert policy.max_stderr_bytes > 0
    assert policy.max_pending_events > 0
~~~~

### tests/resources/commands/test_models.py:94-120

Resource `914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4`; content `c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28`; characters [3194, 4184).

~~~~text
def test_command_result_preserves_bytes_and_exit_status() -> None:
    """Nonzero exit codes remain ordinary completed command results."""
    command = Command("python")
    expected_exit_code = 3
    successful = CommandResult(command, 0, b"out", b"", Duration.seconds(1))
    failed = CommandResult(
        command,
        expected_exit_code,
        b"",
        b"error",
        Duration.seconds(2),
    )

    assert successful.command is command
    assert successful.stdout == b"out"
    assert successful.stderr == b""
    assert successful.duration == Duration.seconds(1)
    assert successful.stdout_truncated is False
    assert successful.stderr_truncated is False
    assert successful.events_dropped == 0
    assert successful.succeeded is True
    assert successful.failed is False
    assert failed.exit_code == expected_exit_code
    assert failed.stdout == b""
    assert failed.stderr == b"error"
    assert failed.succeeded is False
    assert failed.failed is True
~~~~

### tests/resources/commands/test_models.py:94-147

Resource `914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4`; content `c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28`; characters [3194, 4987).

~~~~text
def test_command_result_preserves_bytes_and_exit_status() -> None:
    """Nonzero exit codes remain ordinary completed command results."""
    command = Command("python")
    expected_exit_code = 3
    successful = CommandResult(command, 0, b"out", b"", Duration.seconds(1))
    failed = CommandResult(
        command,
        expected_exit_code,
        b"",
        b"error",
        Duration.seconds(2),
    )

    assert successful.command is command
    assert successful.stdout == b"out"
    assert successful.stderr == b""
    assert successful.duration == Duration.seconds(1)
    assert successful.stdout_truncated is False
    assert successful.stderr_truncated is False
    assert successful.events_dropped == 0
    assert successful.succeeded is True
    assert successful.failed is False
    assert failed.exit_code == expected_exit_code
    assert failed.stdout == b""
    assert failed.stderr == b"error"
    assert failed.succeeded is False
    assert failed.failed is True


@pytest.mark.parametrize(
    ("field", "value", "match"),
    [
        ("max_stdout_bytes", -1, "stdout"),
        ("max_stderr_bytes", -1, "stderr"),
        ("max_pending_events", 0, "pending events"),
    ],
)
def test_command_output_policy_rejects_invalid_bounds(
    field: str,
    value: int,
    match: str,
) -> None:
    """Output limits reject values that cannot form bounded policies."""
    with pytest.raises(ValueError, match=match):
        CommandOutputPolicy(**{field: value})


def test_command_output_policy_exposes_default_bounds() -> None:
    """Default output limits are positive and practical for ordinary commands."""
    policy = CommandOutputPolicy()

    assert policy.max_stdout_bytes > 0
    assert policy.max_stderr_bytes > 0
    assert policy.max_pending_events > 0
~~~~

### tests/scripts/qwen/test_llama_cpp_service.py:50-66

Resource `e6e99c0bd3305061c8522f31cf1b7ddca3a9f1a5ae3acc40f5dd56026fdbc1f7`; content `d91be75d45780bd76e9606526e6d391c07e7dcc729c73fc4e62d0b6a5181b848`; characters [1447, 1926).

~~~~text
def _result(
    command: Command,
    code: int = 0,
    out: bytes = b"",
    err: bytes = b"",
) -> CommandResult:
    return CommandResult(command, code, out, err, Duration.seconds(0))


class _Executor:
    def __init__(self, values: list[CommandResult]) -> None:
        self.commands: list[Command] = []
        self._values = values

    async def execute(self, command: Command) -> CommandResult:
        self.commands.append(command)
        return self._values.pop(0)
~~~~

### tests/scripts/test_validate_development.py:17-48

Resource `aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986`; content `861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b`; characters [313, 1503).

~~~~text
_SCRIPT_PATH = Path("scripts/validate_development.py")


@pytest.fixture
def validation_script() -> ModuleType:
    """Load the operational script without making scripts a library package."""
    specification = importlib.util.spec_from_file_location(
        "test_validate_development_script",
        _SCRIPT_PATH,
    )
    assert specification is not None
    assert specification.loader is not None
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def test_profile_selects_tests_and_excludes_experiment_tests_before_collection(
    validation_script: ModuleType,
) -> None:
    """The directory boundary covers the whole retained experiment population."""
    arguments = validation_script.pytest_arguments(Path.cwd())
    tests = Path(arguments[0])
    ignored = Path(arguments[1].removeprefix("--ignore="))

    assert tests == Path.cwd() / "tests"
    assert ignored == tests / "experiments"
    assert tests.is_dir()
    assert ignored.is_dir()
    assert (tests / "context").is_dir()
    assert (tests / "scripts" / "test_validate_development.py").is_file()
~~~~

### tests/scripts/test_validate_development.py:51-68

Resource `aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986`; content `861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b`; characters [1505, 2104).

~~~~text
def test_profile_propagates_pytest_failure_code(
    validation_script: ModuleType,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A failed pytest run remains a failed profile invocation."""
    observed_arguments: list[str] | None = None

    def failed_pytest(arguments: list[str]) -> int:
        nonlocal observed_arguments
        observed_arguments = arguments
        return 1

    monkeypatch.setattr(validation_script.pytest, "main", failed_pytest)

    result = validation_script.main()

    assert result == 1
    assert observed_arguments == validation_script.pytest_arguments()
~~~~

### tests/tools/test_command.py:25-56

Resource `5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535`; content `19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6`; characters [458, 1647).

~~~~text
def test_command_tool_is_typed_tool_and_returns_command_result() -> None:
    """CommandTool preserves the existing Command-to-CommandResult contract."""

    async def exercise() -> None:
        tool: Tool[Command, CommandResult] = CommandTool(CommandExecutor())
        command = Command(sys.executable, ("-c", "print('tool command')"))

        result: CommandResult = await ToolRunner().execute(tool, command)

        assert tool.name == "run_command"
        assert tool.description
        assert result.command is command
        assert result.stdout.strip() == b"tool command"

    asyncio.run(exercise())


def test_command_tool_preserves_nonzero_exit_as_result() -> None:
    """A nonzero process exit remains a CommandResult rather than Tool failure."""

    async def exercise() -> None:
        command = Command(
            sys.executable,
            ("-c", f"import sys; sys.exit({_NONZERO_EXIT_CODE})"),
        )
        result = await ToolRunner().execute(CommandTool(CommandExecutor()), command)

        assert isinstance(result, CommandResult)
        assert result.exit_code == _NONZERO_EXIT_CODE
        assert result.failed is True

    asyncio.run(exercise())
~~~~

### tests/tools/test_command.py:59-120

Resource `5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535`; content `19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6`; characters [1649, 3569).

~~~~text
def test_command_tool_propagates_missing_command_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Command lookup failures remain owned by Commands."""

    async def raise_not_found(*_args: object, **_kwargs: object) -> None:
        raise FileNotFoundError

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        raise_not_found,
    )

    with pytest.raises(CommandNotFoundError):
        asyncio.run(
            ToolRunner().execute(CommandTool(CommandExecutor()), Command("missing")),
        )


def test_command_tool_propagates_command_timeout() -> None:
    """Command timeout policy passes through the Tool bridge unchanged."""
    command = Command(
        sys.executable,
        ("-c", "import time; time.sleep(1)"),
        timeout=Duration.seconds(0.001),
    )

    with pytest.raises(CommandTimeoutError):
        asyncio.run(ToolRunner().execute(CommandTool(CommandExecutor()), command))


def test_command_tool_cancellation_preserves_command_cleanup(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cancellation through CommandTool retains immediate-child cleanup."""
    process = _BlockingProcess()

    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:
        return process

    monkeypatch.setattr(
        "devtools.resources.commands.execution.asyncio.create_subprocess_exec",
        create_process,
    )

    async def exercise() -> None:
        operation = asyncio.create_task(
            ToolRunner().execute(
                CommandTool(CommandExecutor()),
                Command("blocking-command"),
            ),
        )
        await process.read_started.wait()
        operation.cancel()

        with pytest.raises(asyncio.CancelledError):
            await operation

    asyncio.run(exercise())

    assert process.killed is True
    assert process.waited is True
~~~~

## Authentication and method

Initial exact five-file authentication passed; the four packet digest scopes and original physical file digests are retained in the JSON review. All excluded information access is attested NO in the JSON review. No second reviewer was used or is requested.

No terminal-output truncation interrupted adjudication. Bounded file-backed reads were used throughout; a console encoding error was corrected and the affected bounded range was reread. No scientific stop was inferred from display limits.

The deterministic builder reconstructs the authored adjudication, all arithmetic, this document, validation results and scientific digests. It validates structural consistency and exact replay; it does not independently certify semantic truth. Scratch material and the local handoff are excluded from evidence and scientific digests.

## Reviewed statistics

```json
{
  "cells": 3090,
  "duplicate_cells": 0,
  "evidence_class_counts": {
    "REPOSITORY_SUPPORTED": 11,
    "TASK_AND_REPOSITORY_SUPPORTED": 0,
    "TASK_BACKED": 19
  },
  "inclusion_minimal_resource_union_count": 126,
  "label_counts_by_obligation": {
    "O1": {
      "HELPFUL_ONLY": 12,
      "REQUIRED": 4,
      "UNNECESSARY": 499
    },
    "O2": {
      "HELPFUL_ONLY": 4,
      "REQUIRED": 5,
      "UNNECESSARY": 506
    },
    "O3": {
      "HELPFUL_ONLY": 5,
      "REQUIRED": 6,
      "UNNECESSARY": 504
    },
    "O4": {
      "HELPFUL_ONLY": 6,
      "REQUIRED": 9,
      "UNNECESSARY": 500
    },
    "O5": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 6,
      "UNNECESSARY": 507
    },
    "O6": {
      "HELPFUL_ONLY": 18,
      "REQUIRED": 4,
      "UNNECESSARY": 493
    }
  },
  "label_counts_total": {
    "HELPFUL_ONLY": 47,
    "REQUIRED": 34,
    "UNNECESSARY": 3009
  },
  "missing_cells": 0,
  "obligations": 6,
  "required_resource_count": 18,
  "required_resource_union": [
    "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
    "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
    "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
    "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
  ],
  "resource_count_range": [
    4,
    10
  ],
  "resources": 515,
  "schema": "case-0014-stage-c-statistics-v1",
  "semantic_unit_count": 30,
  "sufficient_resource_union_count": 2850,
  "sufficient_unit_union_count": 1,
  "task_combination_count": 18900,
  "task_indispensable_resources": [
    "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
  ],
  "task_indispensable_units": [
    "R01",
    "R02",
    "R03",
    "R04",
    "R05",
    "R06",
    "R07",
    "R08",
    "R09",
    "R10",
    "R11",
    "T01",
    "T02",
    "T03",
    "T04",
    "T05",
    "T06",
    "T07",
    "T08",
    "T09",
    "T10",
    "T11",
    "T12",
    "T13",
    "T14",
    "T15",
    "T16",
    "T17",
    "T18",
    "T19"
  ],
  "total_witness_count": 36,
  "unexpected_cells": 0,
  "unit_count_range": [
    30,
    30
  ],
  "unresolved_cells": 0,
  "witness_counts": {
    "O1": 3,
    "O2": 5,
    "O3": 5,
    "O4": 14,
    "O5": 6,
    "O6": 3
  }
}
```

## Exact frame and provenance

```json
{
  "frame": {
    "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494"
  },
  "provenance": {
    "MODEL": "GPT-6 Astra",
    "REASONING": "High",
    "automatic_second_reviewer": false,
    "primary_sha256": {
      "STAGE_C_REVIEW.md": "628f2f1b86627c33f76807dd3875c7fd49b7dc7fb307f85a808e873de1dd4a4f",
      "stage_c_builder.py": "5f0e25a082118ee37651adc64d0d57228eaf0e7d7496d53f9798997c6762ddeb",
      "stage_c_hashes.json": "910ca60da636f3d888708a4709b95c2ca68969fb16f14a1c3f361d0249865a16",
      "stage_c_method.md": "e2a76a8feef89f0f5207333d4d3feaa67bb67c5b427f84b7844edb37703a713b",
      "stage_c_review.json": "cee15c825f70eee62162cf772f66597dfbfa6f51ef6567780ea161b08a7b59ea",
      "stage_c_statistics.json": "cb42c54dfde3cf88e492c3e40e3fe1f946b0eedeee5e172799d56ae4ffbbcefa",
      "stage_c_validation.json": "019cc61f46284e898615e911c64bd0e2c20c1356ad942c5e87d892163c7e920a"
    },
    "projection": "Full unchanged primary object; exact frame bindings only. No reconciliation or semantic modification.",
    "semantic_transformation": "NONE",
    "source": "PRIMARY_ASTRA_HIGH",
    "treatment_blind": true
  }
}
```

## Complete positive cells and exact spans

```json
[
  {
    "address": "AGENTS.md",
    "identity": "case-0014-command-result-diagnostics-v1/O6@953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Necessary in at least one minimal complete witness as support for R10. Operating guide explicitly supplies invocation and precollection exclusion.",
    "resource_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
    "support_spans": [
      {
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "end": 11282,
        "end_line": 239,
        "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
        "resource_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "start": 10713,
        "start_line": 228
      }
    ]
  },
  {
    "address": "pyproject.toml",
    "identity": "case-0014-command-result-diagnostics-v1/O6@6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Necessary in at least one minimal complete witness as support for R11. Actual pytest, coverage, lint and type-checking configuration; this is not a synthetic fixture.",
    "resource_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
    "support_spans": [
      {
        "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
        "end": 1368,
        "end_line": 78,
        "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n\n[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n\n[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
        "resource_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "start": 585,
        "start_line": 34
      }
    ]
  },
  {
    "address": "scripts/validate_development.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Necessary in at least one minimal complete witness as support for R10. Entry-point arguments select tests with the experiment directory ignored.",
    "resource_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
    "support_spans": [
      {
        "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
        "end": 715,
        "end_line": 27,
        "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n",
        "resource_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "start": 248,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/agents/integrations/codex/agent.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Consumer example corroborates a completed failed result with exit_code; does not define the full result or success contract.",
    "resource_identity": "e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
    "support_spans": [
      {
        "content_identity": "11b5d1a5510bc24338ed2aab4efd3362cfe8a523423e7c23f12dc438aa8eca41",
        "end": 3481,
        "end_line": 94,
        "quote": "        command = self._build_command(message.content, conversation)\n        result = await self._executor.execute(command)\n        if result.failed:\n            raise CodexCommandError(result.exit_code)\n        if result.stdout_truncated:\n            msg = \"Codex JSONL stdout was truncated by the command output policy.\"\n            raise CodexOutputError(msg)\n\n        output = parse_codex_turn_output(result.stdout)\n",
        "resource_identity": "e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
        "start": 3061,
        "start_line": 86
      }
    ]
  },
  {
    "address": "src/devtools/agents/integrations/codex/agent.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Consumer corroborates stdout_truncated as retained-output loss; does not define both streams or retention policy.",
    "resource_identity": "e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
    "support_spans": [
      {
        "content_identity": "11b5d1a5510bc24338ed2aab4efd3362cfe8a523423e7c23f12dc438aa8eca41",
        "end": 3481,
        "end_line": 94,
        "quote": "        command = self._build_command(message.content, conversation)\n        result = await self._executor.execute(command)\n        if result.failed:\n            raise CodexCommandError(result.exit_code)\n        if result.stdout_truncated:\n            msg = \"Codex JSONL stdout was truncated by the command output policy.\"\n            raise CodexOutputError(msg)\n\n        output = parse_codex_turn_output(result.stdout)\n",
        "resource_identity": "e7cb3055dd416a3fc68b8b3b5e997e0e7841c39e860c1c6a7aa3a5a7b1dc4344",
        "start": 3061,
        "start_line": 86
      }
    ]
  },
  {
    "address": "src/devtools/agents/integrations/codex/docs/cli.md",
    "identity": "case-0014-command-result-diagnostics-v1/O3@deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Consumer documentation illustrates finite retention and caller-supplied output policy without defining the full retention contract.",
    "resource_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
    "support_spans": [
      {
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "end": 4249,
        "end_line": 105,
        "quote": "## Retained output and stderr\n\nJSONL is parsed from retained `CommandResult.stdout`. The executor's retention\nis finite; `stdout_truncated` fails closed with `CodexOutputError`. Callers that\nexpect unusually large transcripts can provide `CommandExecutor` with a larger\n`CommandOutputPolicy`.\n\nSuccessful-turn stderr is ignored. It is not assumed empty and is not converted\ninto an error message.\n",
        "resource_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "start": 3852,
        "start_line": 97
      }
    ]
  },
  {
    "address": "src/devtools/core/time/docs/timestamps.md",
    "identity": "case-0014-command-result-diagnostics-v1/O1@12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Explains Duration numeric access and precision for an optional explicit duration format; the result contract already identifies the value to preserve.",
    "resource_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
    "support_spans": [
      {
        "content_identity": "91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941",
        "end": 3061,
        "end_line": 96,
        "quote": "## Duration\n\n`Duration(value: timedelta)` is a frozen, slotted non-negative value. Factories\nare `nanoseconds()`, `milliseconds()`, `seconds()`, `minutes()`, and `hours()`.\n`total_seconds` and `total_milliseconds` expose numeric totals.\n\nDurations support addition, non-negative subtraction, multiplication by an\n`int` or `float`, reversed multiplication, and division by an `int` or `float`.\nUnsupported operands raise normal `TypeError`; division by zero raises normal\n`ZeroDivisionError`.\n\n## Precision and errors\n\n`Duration` stores `datetime.timedelta`, not true nanoseconds. Consequently,\n`Duration.nanoseconds()` follows standard-library microsecond-bounded\nconversion and rounding for sub-microsecond inputs.\n",
        "resource_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "start": 2345,
        "start_line": 81
      }
    ]
  },
  {
    "address": "src/devtools/core/time/models/duration.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@15ea4e21efcac9c53500c2225545960280bc14698c8d34c0ea6475650e669103",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Provides a human-readable Duration conversion implementation; choosing this exact format is not required.",
    "resource_identity": "15ea4e21efcac9c53500c2225545960280bc14698c8d34c0ea6475650e669103",
    "support_spans": [
      {
        "content_identity": "69baac5a2120f0c503d4db9bf454331394921e5a606fcc7288f143380ff79241",
        "end": 2715,
        "end_line": 98,
        "quote": "    @property\n    def total_seconds(self) -> float:\n        \"\"\"Return the duration in seconds.\n\n        :returns: Total number of seconds.\n        \"\"\"\n        return self.value.total_seconds()\n\n    @property\n    def total_milliseconds(self) -> float:\n        \"\"\"Return the duration in milliseconds.\n\n        :returns: Total number of milliseconds.\n        \"\"\"\n        return self.total_seconds * 1000.0\n\n    def __str__(self) -> str:\n        \"\"\"Return the standard timedelta representation.\n\n        :returns: Human-readable duration representation.\n        \"\"\"\n        return str(self.value)\n",
        "resource_identity": "15ea4e21efcac9c53500c2225545960280bc14698c8d34c0ea6475650e669103",
        "start": 2122,
        "start_line": 77
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/llama_cpp.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "support_spans": [
      {
        "content_identity": "c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e",
        "end": 15480,
        "end_line": 444,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    return (\n        result.stderr.decode(errors=\"replace\").strip().casefold()\n        == f\"error: no such object: {container_id}\".casefold()\n    )\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    return data[:4096].decode(errors=\"replace\").strip()\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    return f\"Docker rejected llama.cpp launch with exit code {result.exit_code}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n\n\ndef _stop_error_message(\n    operation: str,\n    result: CommandResult,\n    container_id: str,\n) -> str:\n    return f\"Docker could not {operation} owned llama.cpp container {container_id!r}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n",
        "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
        "start": 14694,
        "start_line": 424
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/llama_cpp.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "support_spans": [
      {
        "content_identity": "c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e",
        "end": 15480,
        "end_line": 444,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    return (\n        result.stderr.decode(errors=\"replace\").strip().casefold()\n        == f\"error: no such object: {container_id}\".casefold()\n    )\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    return data[:4096].decode(errors=\"replace\").strip()\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    return f\"Docker rejected llama.cpp launch with exit code {result.exit_code}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n\n\ndef _stop_error_message(\n    operation: str,\n    result: CommandResult,\n    container_id: str,\n) -> str:\n    return f\"Docker could not {operation} owned llama.cpp container {container_id!r}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n",
        "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
        "start": 14694,
        "start_line": 424
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/llama_cpp.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
    "support_spans": [
      {
        "content_identity": "c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e",
        "end": 15480,
        "end_line": 444,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    return (\n        result.stderr.decode(errors=\"replace\").strip().casefold()\n        == f\"error: no such object: {container_id}\".casefold()\n    )\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    return data[:4096].decode(errors=\"replace\").strip()\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    return f\"Docker rejected llama.cpp launch with exit code {result.exit_code}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n\n\ndef _stop_error_message(\n    operation: str,\n    result: CommandResult,\n    container_id: str,\n) -> str:\n    return f\"Docker could not {operation} owned llama.cpp container {container_id!r}. {_diagnostic_text(result.stderr or result.stdout)}\".strip()\n",
        "resource_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
        "start": 14694,
        "start_line": 424
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/vllm.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "support_spans": [
      {
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "end": 17701,
        "end_line": 514,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    \"\"\"Return whether Docker reported this exact inspected container as absent.\"\"\"\n    expected = f\"error: no such object: {container_id}\".casefold()\n    diagnostic = result.stderr.decode(\"utf-8\", errors=\"replace\").strip().casefold()\n    return diagnostic == expected\n\n\ndef _inspection_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded diagnostics for a Docker inspection failure.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = (\n        f\"Docker could not inspect owned vLLM container (exit {result.exit_code}).\"\n    )\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded launch diagnostics from a nonzero Docker result.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = f\"Docker rejected vLLM launch with exit code {result.exit_code}.\"\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    \"\"\"Decode a bounded command-output prefix for an error message.\"\"\"\n    return data[:_MAX_DIAGNOSTIC_BYTES].decode(\"utf-8\", errors=\"replace\").strip()\n",
        "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "start": 16439,
        "start_line": 489
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/vllm.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "support_spans": [
      {
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "end": 17701,
        "end_line": 514,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    \"\"\"Return whether Docker reported this exact inspected container as absent.\"\"\"\n    expected = f\"error: no such object: {container_id}\".casefold()\n    diagnostic = result.stderr.decode(\"utf-8\", errors=\"replace\").strip().casefold()\n    return diagnostic == expected\n\n\ndef _inspection_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded diagnostics for a Docker inspection failure.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = (\n        f\"Docker could not inspect owned vLLM container (exit {result.exit_code}).\"\n    )\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded launch diagnostics from a nonzero Docker result.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = f\"Docker rejected vLLM launch with exit code {result.exit_code}.\"\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    \"\"\"Decode a bounded command-output prefix for an error message.\"\"\"\n    return data[:_MAX_DIAGNOSTIC_BYTES].decode(\"utf-8\", errors=\"replace\").strip()\n",
        "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "start": 16439,
        "start_line": 489
      }
    ]
  },
  {
    "address": "src/devtools/models/serving/vllm.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Existing consumer diagnostic example reads completed result bytes and exit code with replacement decoding and a byte bound; it lacks separate streams, character limits, and loss disclosure and is not normative for the new API.",
    "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
    "support_spans": [
      {
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "end": 17701,
        "end_line": 514,
        "quote": "def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:\n    \"\"\"Return whether Docker reported this exact inspected container as absent.\"\"\"\n    expected = f\"error: no such object: {container_id}\".casefold()\n    diagnostic = result.stderr.decode(\"utf-8\", errors=\"replace\").strip().casefold()\n    return diagnostic == expected\n\n\ndef _inspection_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded diagnostics for a Docker inspection failure.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = (\n        f\"Docker could not inspect owned vLLM container (exit {result.exit_code}).\"\n    )\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _launch_error_message(result: CommandResult) -> str:\n    \"\"\"Create bounded launch diagnostics from a nonzero Docker result.\"\"\"\n    diagnostic = _diagnostic_text(result.stderr or result.stdout)\n    message = f\"Docker rejected vLLM launch with exit code {result.exit_code}.\"\n    return f\"{message} {diagnostic}\" if diagnostic else message\n\n\ndef _diagnostic_text(data: bytes) -> str:\n    \"\"\"Decode a bounded command-output prefix for an error message.\"\"\"\n    return data[:_MAX_DIAGNOSTIC_BYTES].decode(\"utf-8\", errors=\"replace\").strip()\n",
        "resource_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "start": 16439,
        "start_line": 489
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/__init__.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R08. Exact current imports and __all__.",
    "resource_identity": "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
    "support_spans": [
      {
        "content_identity": "7cbc6f6b95697b5c664eb09d2779fe854fedb8d868e046e913bed2ce2fbb30b3",
        "end": 889,
        "end_line": 38,
        "quote": "from devtools.resources.commands.errors import (\n    CommandError,\n    CommandNotFoundError,\n    CommandTimeoutError,\n)\nfrom devtools.resources.commands.events import (\n    CommandEvent,\n    CommandExited,\n    CommandStarted,\n    CommandStderr,\n    CommandStdout,\n)\nfrom devtools.resources.commands.execution import CommandExecutor\nfrom devtools.resources.commands.handle import CommandExecution\nfrom devtools.resources.commands.models import (\n    Command,\n    CommandOutputPolicy,\n    CommandResult,\n)\n\n__all__ = [\n    \"Command\",\n    \"CommandError\",\n    \"CommandEvent\",\n    \"CommandExecution\",\n    \"CommandExecutor\",\n    \"CommandExited\",\n    \"CommandNotFoundError\",\n    \"CommandOutputPolicy\",\n    \"CommandResult\",\n    \"CommandStarted\",\n    \"CommandStderr\",\n    \"CommandStdout\",\n    \"CommandTimeoutError\",\n]\n",
        "resource_identity": "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
        "start": 80,
        "start_line": 4
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O1@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Necessary in at least one minimal complete witness as support for R01, R02. Direct public value contract. Constructor and exact status prose.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 981,
        "end_line": 31,
        "quote": "## `Command`\n\n```python\nCommand(\n    executable: str,\n    arguments: tuple[str, ...] = (),\n    working_directory: ResolvedPath | None = None,\n    timeout: Duration | None = None,\n)\n```\n\n`Command` is a frozen, slotted value object. Blank executables are invalid.\nThe executable and arguments remain separate; no shell parsing, interpolation,\nor quoting occurs. `argv` returns the complete tuple passed to process launch.\n\nAll fluent methods return new values:\n\n```text\nargs(...)             append arguments\nwith_args(...)        replace arguments\nwithout_args()        clear arguments\nwith_executable(...)  replace and validate executable\ncwd(...)              set ResolvedPath working directory\nwithout_cwd()         clear working directory\nwith_timeout(...)     set Duration timeout\nwithout_timeout()     clear timeout\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 160,
        "start_line": 6
      },
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 2115,
        "end_line": 71,
        "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n\nExit code zero means `succeeded`; every nonzero exit code means `failed` but is\nstill a completed result. Timeout, cancellation, process-creation failure, and\nother execution exceptions produce no `CommandResult`.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1424,
        "start_line": 49
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O2@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Necessary in at least one minimal complete witness as support for R03. Direct result representation and retained-prefix prose.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 1900,
        "end_line": 67,
        "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1424,
        "start_line": 49
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O3@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R04, R05. Independent byte limits and zero-retention behavior are documented. Explicit zero-byte and per-stream truncation contract.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 1423,
        "end_line": 47,
        "quote": "## `CommandOutputPolicy`\n\n```python\nCommandOutputPolicy(\n    max_stdout_bytes=1_048_576,\n    max_stderr_bytes=1_048_576,\n    max_pending_events=1_024,\n)\n```\n\nStdout and stderr retention limits are independent. A zero byte limit is valid:\nnonempty output remains streamable but no bytes are retained in the final\nresult, and the matching truncation flag is true. Negative byte limits are\ninvalid. Pending-event capacity must be positive.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 986,
        "start_line": 34
      },
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 1900,
        "end_line": 67,
        "quote": "Stdout and stderr retention limits are independent. A zero byte limit is valid:\nnonempty output remains streamable but no bytes are retained in the final\nresult, and the matching truncation flag is true. Negative byte limits are\ninvalid. Pending-event capacity must be positive.\n\n## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1144,
        "start_line": 44
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O4@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06, R07. Distinct result fields and explicit bounded-queue-loss meaning. Explicit no-result boundary.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 1900,
        "end_line": 67,
        "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1424,
        "start_line": 49
      },
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 2115,
        "end_line": 71,
        "quote": "Exit code zero means `succeeded`; every nonzero exit code means `failed` but is\nstill a completed result. Timeout, cancellation, process-creation failure, and\nother execution exceptions produce no `CommandResult`.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1901,
        "start_line": 69
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O5@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R01, R09. Direct public value contract. Explicit frozen-result contract.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 981,
        "end_line": 31,
        "quote": "## `Command`\n\n```python\nCommand(\n    executable: str,\n    arguments: tuple[str, ...] = (),\n    working_directory: ResolvedPath | None = None,\n    timeout: Duration | None = None,\n)\n```\n\n`Command` is a frozen, slotted value object. Blank executables are invalid.\nThe executable and arguments remain separate; no shell parsing, interpolation,\nor quoting occurs. `argv` returns the complete tuple passed to process launch.\n\nAll fluent methods return new values:\n\n```text\nargs(...)             append arguments\nwith_args(...)        replace arguments\nwithout_args()        clear arguments\nwith_executable(...)  replace and validate executable\ncwd(...)              set ResolvedPath working directory\nwithout_cwd()         clear working directory\nwith_timeout(...)     set Duration timeout\nwithout_timeout()     clear timeout\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 160,
        "start_line": 6
      },
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 1900,
        "end_line": 67,
        "quote": "Results are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 1620,
        "start_line": 64
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/command.md",
    "identity": "case-0014-command-result-diagnostics-v1/O6@cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Existing package documentation provides an appropriate update context and examples. The task already specifies the future documentation location and cases; this file is not required just as an edit destination.",
    "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
    "support_spans": [
      {
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "end": 2115,
        "end_line": 71,
        "quote": "# Command values, policy, and results\n\nSee the [package overview](overview.md), [execution lifecycle](execution.md),\nand [events/output semantics](events.md).\n\n## `Command`\n\n```python\nCommand(\n    executable: str,\n    arguments: tuple[str, ...] = (),\n    working_directory: ResolvedPath | None = None,\n    timeout: Duration | None = None,\n)\n```\n\n`Command` is a frozen, slotted value object. Blank executables are invalid.\nThe executable and arguments remain separate; no shell parsing, interpolation,\nor quoting occurs. `argv` returns the complete tuple passed to process launch.\n\nAll fluent methods return new values:\n\n```text\nargs(...)             append arguments\nwith_args(...)        replace arguments\nwithout_args()        clear arguments\nwith_executable(...)  replace and validate executable\ncwd(...)              set ResolvedPath working directory\nwithout_cwd()         clear working directory\nwith_timeout(...)     set Duration timeout\nwithout_timeout()     clear timeout\n```\n\n## `CommandOutputPolicy`\n\n```python\nCommandOutputPolicy(\n    max_stdout_bytes=1_048_576,\n    max_stderr_bytes=1_048_576,\n    max_pending_events=1_024,\n)\n```\n\nStdout and stderr retention limits are independent. A zero byte limit is valid:\nnonempty output remains streamable but no bytes are retained in the final\nresult, and the matching truncation flag is true. Negative byte limits are\ninvalid. Pending-event capacity must be positive.\n\n## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n\nExit code zero means `succeeded`; every nonzero exit code means `failed` but is\nstill a completed result. Timeout, cancellation, process-creation failure, and\nother execution exceptions produce no `CommandResult`.\n",
        "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "start": 0,
        "start_line": 1
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/events.md",
    "identity": "case-0014-command-result-diagnostics-v1/O2@86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Necessary in at least one minimal complete witness as support for R03. Explicit independent leading result-prefix retention.",
    "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "support_spans": [
      {
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "end": 1758,
        "end_line": 53,
        "quote": "## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
        "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "start": 1272,
        "start_line": 45
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/events.md",
    "identity": "case-0014-command-result-diagnostics-v1/O3@86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R04, R05. Independent output prefixes and retention bounds are documented. Omitted retained bytes set corresponding flags.",
    "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "support_spans": [
      {
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "end": 1758,
        "end_line": 53,
        "quote": "## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
        "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "start": 1272,
        "start_line": 45
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/events.md",
    "identity": "case-0014-command-result-diagnostics-v1/O4@86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06. Explicit event count, best-effort queue loss and independent retained output.",
    "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "support_spans": [
      {
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "end": 1758,
        "end_line": 53,
        "quote": "Ordering within stdout and within stderr is preserved. Interleaving between the\ntwo streams is not guaranteed.\n\n## `events()`\n\n`execution.events()` is a single-consumer async stream. The claim occurs when\niteration begins; a second consumer attempt raises `RuntimeError`. Streams\nclose on normal completion, missing executable, timeout, cancellation, and\nunexpected stream-read failure.\n\n## Bounded queue and drop policy\n\nThe pending queue is bounded by `CommandOutputPolicy.max_pending_events`.\nProducers never block when full: any newly emitted event is dropped, and\n`events_dropped` records the total. No event type is privileged, so\n`CommandExited` may be dropped under pressure. Event delivery is best effort.\n\n## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
        "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "start": 556,
        "start_line": 28
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/events.md",
    "identity": "case-0014-command-result-diagnostics-v1/O6@86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful existing explanation of event-loss versus retained-output coverage for documentation and regressions, without requiring this particular edit destination.",
    "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
    "support_spans": [
      {
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "end": 1758,
        "end_line": 53,
        "quote": "Ordering within stdout and within stderr is preserved. Interleaving between the\ntwo streams is not guaranteed.\n\n## `events()`\n\n`execution.events()` is a single-consumer async stream. The claim occurs when\niteration begins; a second consumer attempt raises `RuntimeError`. Streams\nclose on normal completion, missing executable, timeout, cancellation, and\nunexpected stream-read failure.\n\n## Bounded queue and drop policy\n\nThe pending queue is bounded by `CommandOutputPolicy.max_pending_events`.\nProducers never block when full: any newly emitted event is dropped, and\n`events_dropped` records the total. No event type is privileged, so\n`CommandExited` may be dropped under pressure. Event delivery is best effort.\n\n## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
        "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "start": 556,
        "start_line": 28
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/execution.md",
    "identity": "case-0014-command-result-diagnostics-v1/O1@562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Corroborates completed-result identity and direct execution; detailed executor lifecycle is unnecessary to a pure result renderer.",
    "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "support_spans": [
      {
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "end": 1157,
        "end_line": 34,
        "quote": "`execute()` calls `start()` and awaits the returned handle. `start()` requires\nan active asyncio event loop because it immediately creates the underlying\ntask.\n\n`CommandExecution` owns one task and launches one subprocess. Repeated\nsuccessful awaits share that task and return the same `CommandResult` instance.\n`is_running` and `is_complete` reflect task state. There is no async context\nmanager.\n\n## Process creation\n\nExecution uses `asyncio.create_subprocess_exec()` with direct argv, optional\nnative cwd, and stdout/stderr pipes. There is no shell, stdin, environment\noverride, or process-group configuration.\n\nIf creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with\nthe original error retained as its cause. No started event or result is\nproduced, and the event stream closes.\n",
        "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
        "start": 352,
        "start_line": 17
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/execution.md",
    "identity": "case-0014-command-result-diagnostics-v1/O4@562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R07. Lifecycle documentation covers all three exceptional outcomes.",
    "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "support_spans": [
      {
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "end": 2062,
        "end_line": 55,
        "quote": "## Process creation\n\nExecution uses `asyncio.create_subprocess_exec()` with direct argv, optional\nnative cwd, and stdout/stderr pipes. There is no shell, stdin, environment\noverride, or process-group configuration.\n\nIf creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with\nthe original error retained as its cause. No started event or result is\nproduced, and the event stream closes.\n\n## Timeout\n\n`Duration.total_seconds` configures an asyncio timeout around post-creation\noutput collection. Process creation time is not included.\n\nOn timeout, the running immediate child is killed and awaited/reaped,\n`CommandTimeoutError` is raised with the timeout failure as its cause, and the\nevent stream closes. No `CommandExited` or final result is fabricated. Events\nalready observed may remain available, but partial retained output is not\nexposed through a result.\n\n## Cancellation\n\nBefore child creation completes, cancellation closes the stream and propagates.\nAfter creation, a running immediate child is killed and awaited/reaped;\ncancellation then propagates unchanged and no exit event is fabricated. An\nalready-exited child is awaited without another kill.\n\nAwaiters directly await the same task. Cancelling one awaiter can therefore\ncancel the shared command execution for all awaiters.\n",
        "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
        "start": 751,
        "start_line": 26
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/execution.md",
    "identity": "case-0014-command-result-diagnostics-v1/O6@562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Existing lifecycle documentation is useful regression context; requesting future tests/docs does not require this file.",
    "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
    "support_spans": [
      {
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "end": 2062,
        "end_line": 55,
        "quote": "## Process creation\n\nExecution uses `asyncio.create_subprocess_exec()` with direct argv, optional\nnative cwd, and stdout/stderr pipes. There is no shell, stdin, environment\noverride, or process-group configuration.\n\nIf creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with\nthe original error retained as its cause. No started event or result is\nproduced, and the event stream closes.\n\n## Timeout\n\n`Duration.total_seconds` configures an asyncio timeout around post-creation\noutput collection. Process creation time is not included.\n\nOn timeout, the running immediate child is killed and awaited/reaped,\n`CommandTimeoutError` is raised with the timeout failure as its cause, and the\nevent stream closes. No `CommandExited` or final result is fabricated. Events\nalready observed may remain available, but partial retained output is not\nexposed through a result.\n\n## Cancellation\n\nBefore child creation completes, cancellation closes the stream and propagates.\nAfter creation, a running immediate child is killed and awaited/reaped;\ncancellation then propagates unchanged and no exit event is fabricated. An\nalready-exited child is awaited without another kill.\n\nAwaiters directly await the same task. Cancelling one awaiter can therefore\ncancel the shared command execution for all awaiters.\n",
        "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
        "start": 751,
        "start_line": 26
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/overview.md",
    "identity": "case-0014-command-result-diagnostics-v1/O1@27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Corroborates ordinary nonzero completion but lacks the full field and status contracts.",
    "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "support_spans": [
      {
        "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
        "end": 2467,
        "end_line": 79,
        "quote": "## Errors\n\n```text\nCommandError\n\u251c\u2500\u2500 CommandNotFoundError\n\u2514\u2500\u2500 CommandTimeoutError\n```\n\nA nonzero process exit is a normal `CommandResult`, not an exception.\n\n## Limitations and future evolution\n\nExecution manages only the immediate child process. Output/event observation is\nbounded and best effort. Shell mode, stdin, environment overrides, process\ngroups, pipelines, retries, and text decoding are absent.\n",
        "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
        "start": 2060,
        "start_line": 65
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/overview.md",
    "identity": "case-0014-command-result-diagnostics-v1/O5@27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R08. Independent public API documentation names the complete current export surface.",
    "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "support_spans": [
      {
        "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
        "end": 1460,
        "end_line": 38,
        "quote": "## Public API\n\n```python\nfrom devtools.resources.commands import (\n    Command,\n    CommandError,\n    CommandEvent,\n    CommandExecution,\n    CommandExecutor,\n    CommandExited,\n    CommandNotFoundError,\n    CommandOutputPolicy,\n    CommandResult,\n    CommandStarted,\n    CommandStderr,\n    CommandStdout,\n    CommandTimeoutError,\n)\n```\n\n| Group              | API                                                                                 |\n|--------------------|-------------------------------------------------------------------------------------|\n| Specification      | `Command`                                                                           |\n| Execution          | `CommandExecutor`, `CommandExecution`                                               |\n| Events             | `CommandEvent`, `CommandStarted`, `CommandStdout`, `CommandStderr`, `CommandExited` |\n| Results and policy | `CommandResult`, `CommandOutputPolicy`                                              |\n| Errors             | `CommandError`, `CommandNotFoundError`, `CommandTimeoutError`                       |\n\n`CommandEvent` is a type alias for the concrete event values, not a runtime\nevent superclass.\n",
        "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
        "start": 264,
        "start_line": 9
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/docs/overview.md",
    "identity": "case-0014-command-result-diagnostics-v1/O6@27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Explains the package documentation organization and links; useful editing context, but the task already names the documentation destination.",
    "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
    "support_spans": [
      {
        "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
        "end": 1762,
        "end_line": 55,
        "quote": "## Architecture\n\n```text\nCommand\n   \u2193\nCommandExecutor.start()\n   \u2193\nCommandExecution\n   \u251c\u2500\u2500 events()\n   \u2514\u2500\u2500 await\n        \u2193\n   CommandResult\n```\n\n`execute()` is the convenience start-and-await path. See [command values](command.md),\n[execution lifecycle](execution.md), and [events/output](events.md).\n",
        "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
        "start": 1461,
        "start_line": 40
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/errors.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@28033b6d9764ac5ab1c511d43af2440a24f1bf4bfeec8f9a15b5d40bbdcf3eee",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Names not-found and timeout exceptions but alone does not establish that no completed result is produced, or cancellation behavior.",
    "resource_identity": "28033b6d9764ac5ab1c511d43af2440a24f1bf4bfeec8f9a15b5d40bbdcf3eee",
    "support_spans": [
      {
        "content_identity": "9f9b4159a7d8209d3cbd5101f6d1d5530b0768e6e72b61d8a64aecfa3ba55d7f",
        "end": 391,
        "end_line": 14,
        "quote": "class CommandError(Exception):\n    \"\"\"Base exception for command-execution failures.\"\"\"\n\n\nclass CommandNotFoundError(CommandError):\n    \"\"\"Raised when the requested executable cannot be found.\"\"\"\n\n\nclass CommandTimeoutError(CommandError):\n    \"\"\"Raised when command execution exceeds its timeout.\"\"\"\n",
        "resource_identity": "28033b6d9764ac5ab1c511d43af2440a24f1bf4bfeec8f9a15b5d40bbdcf3eee",
        "start": 91,
        "start_line": 5
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/events.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@0f3ef2acc2faa6fea579de696653cfe7ed50c178f6f5939a0be590b29d105a37",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Shows immutable event values; the renderer accepts a result and must not reconstruct these events, so their concrete classes are optional context.",
    "resource_identity": "0f3ef2acc2faa6fea579de696653cfe7ed50c178f6f5939a0be590b29d105a37",
    "support_spans": [
      {
        "content_identity": "7bfe93cebfef47011047122901ad9756b95d28dfd82a228993d46eb8670344a6",
        "end": 1181,
        "end_line": 56,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandStarted:\n    \"\"\"Represent the start of a command execution.\n\n    :ivar command: Command that started executing.\n    \"\"\"\n\n    command: Command\n\n\n@dataclass(frozen=True, slots=True)\nclass CommandStdout:\n    \"\"\"Represent bytes emitted to standard output.\n\n    :ivar data: Bytes emitted by the process.\n    \"\"\"\n\n    data: bytes\n\n\n@dataclass(frozen=True, slots=True)\nclass CommandStderr:\n    \"\"\"Represent bytes emitted to standard error.\n\n    :ivar data: Bytes emitted by the process.\n    \"\"\"\n\n    data: bytes\n\n\n@dataclass(frozen=True, slots=True)\nclass CommandExited:\n    \"\"\"Represent completion of a command process.\n\n    :ivar exit_code: Process exit code.\n    :ivar duration: Total elapsed execution duration.\n    \"\"\"\n\n    exit_code: int\n    duration: Duration\n\n\nCommandEvent = CommandStarted | CommandStdout | CommandStderr | CommandExited\n",
        "resource_identity": "0f3ef2acc2faa6fea579de696653cfe7ed50c178f6f5939a0be590b29d105a37",
        "start": 292,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Corroborates completed result field construction and ordinary nonzero completion; does not define succeeded/failed or immutable Command shape.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 5073,
        "end_line": 169,
        "quote": "        else:\n            duration = stopwatch.stop()\n            exit_code = process.returncode\n\n            if exit_code is None:\n                msg = (\n                    \"Command process completed without an exit code: \"\n                    f\"{command.executable!r}.\"\n                )\n                raise CommandError(msg)\n\n            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n\n            execution._emit(  # noqa: SLF001\n                CommandExited(\n                    exit_code=exit_code,\n                    duration=duration,\n                ),\n            )\n\n            return replace(result, events_dropped=execution.events_dropped)\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 4154,
        "start_line": 141
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Necessary in at least one minimal complete witness as support for R03. Both streams are bounded independently, converted to bytes and assigned to their result fields.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 4806,
        "end_line": 160,
        "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 4487,
        "start_line": 152
      },
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 9512,
        "end_line": 303,
        "quote": "    async def _stream_process(\n        self,\n        process: asyncio.subprocess.Process,\n        execution: CommandExecution,\n        output_policy: CommandOutputPolicy,\n    ) -> tuple[bytes, bytes, bool, bool]:\n        \"\"\"Stream subprocess output while retaining bounded output prefixes.\n\n        Process streams are fully drained during normal completion. Returned\n        bytes contain only the leading prefix retained by the output policy.\n\n        :param process: Running subprocess.\n        :param execution: Live execution receiving events.\n        :returns: Complete stdout and stderr byte sequences.\n        \"\"\"\n        if process.stdout is None or process.stderr is None:\n            msg = \"Command subprocess streams were not created.\"\n            raise CommandError(msg)\n\n        stdout_task = asyncio.create_task(\n            self._read_stream(\n                process.stdout,\n                execution._emit,  # noqa: SLF001\n                CommandStdout,\n                output_policy.max_stdout_bytes,\n            ),\n        )\n        stderr_task = asyncio.create_task(\n            self._read_stream(\n                process.stderr,\n                execution._emit,  # noqa: SLF001\n                CommandStderr,\n                output_policy.max_stderr_bytes,\n            ),\n        )\n\n        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(\n            stdout_task,\n            stderr_task,\n        )\n\n        await process.wait()\n\n        return stdout, stderr, stdout_truncated, stderr_truncated\n\n    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 7245,
        "start_line": 236
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R04, R05. Separate policy byte fields govern the bytearray prefixes. A flag becomes true when a chunk exceeds remaining retention; named fields receive the flags.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 4806,
        "end_line": 160,
        "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 4487,
        "start_line": 152
      },
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 9512,
        "end_line": 303,
        "quote": "    async def _stream_process(\n        self,\n        process: asyncio.subprocess.Process,\n        execution: CommandExecution,\n        output_policy: CommandOutputPolicy,\n    ) -> tuple[bytes, bytes, bool, bool]:\n        \"\"\"Stream subprocess output while retaining bounded output prefixes.\n\n        Process streams are fully drained during normal completion. Returned\n        bytes contain only the leading prefix retained by the output policy.\n\n        :param process: Running subprocess.\n        :param execution: Live execution receiving events.\n        :returns: Complete stdout and stderr byte sequences.\n        \"\"\"\n        if process.stdout is None or process.stderr is None:\n            msg = \"Command subprocess streams were not created.\"\n            raise CommandError(msg)\n\n        stdout_task = asyncio.create_task(\n            self._read_stream(\n                process.stdout,\n                execution._emit,  # noqa: SLF001\n                CommandStdout,\n                output_policy.max_stdout_bytes,\n            ),\n        )\n        stderr_task = asyncio.create_task(\n            self._read_stream(\n                process.stderr,\n                execution._emit,  # noqa: SLF001\n                CommandStderr,\n                output_policy.max_stderr_bytes,\n            ),\n        )\n\n        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(\n            stdout_task,\n            stderr_task,\n        )\n\n        await process.wait()\n\n        return stdout, stderr, stdout_truncated, stderr_truncated\n\n    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 7245,
        "start_line": 236
      },
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 9512,
        "end_line": 303,
        "quote": "    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 8794,
        "start_line": 281
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06, R07. The handle counts dropped events; execution copies that count into the result independently of output flags. All three failure paths raise before the successful result construction branch.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 6340,
        "end_line": 207,
        "quote": "    async def _run(\n        self,\n        command: Command,\n        execution: CommandExecution,\n    ) -> CommandResult:\n        \"\"\"Run one command execution.\n\n        :param command: Command to execute.\n        :param execution: Live execution receiving emitted events.\n        :returns: Completed command result.\n        :raises CommandNotFoundError: If the executable cannot be found.\n        :raises CommandTimeoutError: If execution exceeds its timeout.\n        :raises CommandError: If the process completes without an exit code.\n        \"\"\"\n        stopwatch = Stopwatch()\n        process: asyncio.subprocess.Process | None = None\n\n        try:\n            process = await self._create_process(command)\n\n            execution._emit(CommandStarted(command=command))  # noqa: SLF001\n\n            try:\n                (\n                    stdout,\n                    stderr,\n                    stdout_truncated,\n                    stderr_truncated,\n                ) = await self._collect_output(\n                    process,\n                    execution,\n                    command,\n                )\n            except TimeoutError as error:\n                await self._terminate_and_reap(process)\n                process = None\n\n                timeout = command.timeout\n\n                if timeout is None:\n                    msg = \"Command timed out without a configured timeout.\"\n                    raise CommandError(msg) from error\n\n                msg = (\n                    f\"Command exceeded timeout of \"\n                    f\"{timeout.total_seconds} seconds: \"\n                    f\"{command.executable!r}.\"\n                )\n                raise CommandTimeoutError(msg) from error\n\n        except asyncio.CancelledError:\n            if process is not None:\n                await self._terminate_and_reap(process)\n\n            raise\n        except (CommandNotFoundError, CommandTimeoutError):\n            raise\n        except Exception:\n            if process is not None:\n                await self._terminate_and_reap(process)\n\n            raise\n\n        else:\n            duration = stopwatch.stop()\n            exit_code = process.returncode\n\n            if exit_code is None:\n                msg = (\n                    \"Command process completed without an exit code: \"\n                    f\"{command.executable!r}.\"\n                )\n                raise CommandError(msg)\n\n            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n\n            execution._emit(  # noqa: SLF001\n                CommandExited(\n                    exit_code=exit_code,\n                    duration=duration,\n                ),\n            )\n\n            return replace(result, events_dropped=execution.events_dropped)\n        finally:\n            stopwatch.stop()\n            execution._close_events()  # noqa: SLF001\n\n    async def _terminate_and_reap(\n        self,\n        process: asyncio.subprocess.Process,\n    ) -> None:\n        \"\"\"Terminate and reap a running immediate child process.\"\"\"\n        if process.returncode is None:\n            process.kill()\n\n        await process.wait()\n\n    async def _create_process(\n        self,\n        command: Command,\n    ) -> asyncio.subprocess.Process:\n        \"\"\"Create the subprocess for a command.\n\n        :param command: Command to execute.\n        :returns: Running subprocess.\n        :raises CommandNotFoundError: If the executable cannot be found.\n        \"\"\"\n        try:\n            return await asyncio.create_subprocess_exec(\n                *command.argv,\n                cwd=(\n                    command.working_directory.value\n                    if command.working_directory is not None\n                    else None\n                ),\n                stdout=asyncio.subprocess.PIPE,\n                stderr=asyncio.subprocess.PIPE,\n            )\n        except FileNotFoundError as error:\n            msg = f\"Command executable not found: {command.executable!r}.\"\n            raise CommandNotFoundError(msg) from error\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 2079,
        "start_line": 78
      },
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 5073,
        "end_line": 169,
        "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n\n            execution._emit(  # noqa: SLF001\n                CommandExited(\n                    exit_code=exit_code,\n                    duration=duration,\n                ),\n            )\n\n            return replace(result, events_dropped=execution.events_dropped)\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 4487,
        "start_line": 152
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Shows existing executor ownership and usage for integration/regression context; the presentation API need not change execution.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 2078,
        "end_line": 76,
        "quote": "class CommandExecutor:\n    \"\"\"Execute commands asynchronously.\"\"\"\n\n    def __init__(\n        self,\n        *,\n        output_policy: CommandOutputPolicy = _DEFAULT_OUTPUT_POLICY,\n    ) -> None:\n        \"\"\"Create a command executor.\n\n        :param output_policy: Per-execution output-retention limits.\n        \"\"\"\n        self._output_policy = output_policy\n\n    def start(self, command: Command) -> CommandExecution:\n        \"\"\"Start a command and return its live execution handle.\n\n        The returned execution begins immediately and may be awaited for the\n        final result or observed through its event stream.\n\n        :param command: Command to execute.\n        :returns: Live command execution.\n        \"\"\"\n        return CommandExecution(\n            partial(self._run, command),\n            max_pending_events=self._output_policy.max_pending_events,\n        )\n\n    async def execute(self, command: Command) -> CommandResult:\n        \"\"\"Execute a command and await its final result.\n\n        This is the convenience API for callers that do not need live event\n        streaming.\n\n        :param command: Command to execute.\n        :returns: Completed command result.\n        \"\"\"\n        return await self.start(command)\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 844,
        "start_line": 39
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Shows existing executor ownership and usage for integration/regression context; the presentation API need not change execution.",
    "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
    "support_spans": [
      {
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "end": 2078,
        "end_line": 76,
        "quote": "class CommandExecutor:\n    \"\"\"Execute commands asynchronously.\"\"\"\n\n    def __init__(\n        self,\n        *,\n        output_policy: CommandOutputPolicy = _DEFAULT_OUTPUT_POLICY,\n    ) -> None:\n        \"\"\"Create a command executor.\n\n        :param output_policy: Per-execution output-retention limits.\n        \"\"\"\n        self._output_policy = output_policy\n\n    def start(self, command: Command) -> CommandExecution:\n        \"\"\"Start a command and return its live execution handle.\n\n        The returned execution begins immediately and may be awaited for the\n        final result or observed through its event stream.\n\n        :param command: Command to execute.\n        :returns: Live command execution.\n        \"\"\"\n        return CommandExecution(\n            partial(self._run, command),\n            max_pending_events=self._output_policy.max_pending_events,\n        )\n\n    async def execute(self, command: Command) -> CommandResult:\n        \"\"\"Execute a command and await its final result.\n\n        This is the convenience API for callers that do not need live event\n        streaming.\n\n        :param command: Command to execute.\n        :returns: Completed command result.\n        \"\"\"\n        return await self.start(command)\n",
        "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "start": 844,
        "start_line": 39
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/handle.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06. The handle counts dropped events; execution copies that count into the result independently of output flags.",
    "resource_identity": "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
    "support_spans": [
      {
        "content_identity": "c9825687577803f98911494be5c86ddd84af006d627acdbacbc2b28d9c82b06c",
        "end": 3938,
        "end_line": 133,
        "quote": "    @property\n    def events_dropped(self) -> int:\n        \"\"\"Return the number of events omitted by bounded buffering.\n\n        Any newly emitted event may be dropped while the queue is full; no event\n        type, including lifecycle events, is privileged.\n\n        :returns: Number of events dropped before observation.\n        \"\"\"\n        return self._events_dropped\n\n    async def events(self) -> AsyncIterator[CommandEvent]:\n        \"\"\"Yield structured events emitted by the execution.\n\n        Only one consumer may iterate the event stream for a given execution.\n\n        :yields: Command execution events.\n        :raises RuntimeError: If the event stream has already been claimed.\n        \"\"\"\n        if self._events_claimed:\n            msg = \"Command execution events may only be consumed once.\"\n            raise RuntimeError(msg)\n\n        self._events_claimed = True\n\n        while True:\n            try:\n                event = self._event_queue.get_nowait()\n            except asyncio.QueueEmpty:\n                if self._events_closed:\n                    return\n\n                await self._event_available.wait()\n                self._event_available.clear()\n                continue\n\n            yield event\n\n    def _emit(self, event: CommandEvent) -> None:\n        \"\"\"Emit an execution event when bounded queue capacity permits it.\n\n        :param event: Event to emit.\n        \"\"\"\n        try:\n            self._event_queue.put_nowait(event)\n        except asyncio.QueueFull:\n            self._events_dropped += 1\n            return\n\n        self._event_available.set()\n\n    def _close_events(self) -> None:\n        \"\"\"Close the execution event stream.\"\"\"\n        self._events_closed = True\n        self._event_available.set()\n",
        "resource_identity": "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
        "start": 2188,
        "start_line": 79
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/__init__.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@161aa54cca99eaed6de081d4617501fc18a54d6c9b9fe2fc35d28d1831f91ad6",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Internal model reexports corroborate the public value owners but do not substitute for the full commands facade.",
    "resource_identity": "161aa54cca99eaed6de081d4617501fc18a54d6c9b9fe2fc35d28d1831f91ad6",
    "support_spans": [
      {
        "content_identity": "663fbad9d358d6ebb6f849fe60b189a4fc48bbf688ec809f3122929d7c68836f",
        "end": 394,
        "end_line": 14,
        "quote": "# Copyright (c) 2026\n\"\"\"Command value objects.\"\"\"\n\nfrom devtools.resources.commands.models.command import Command as Command\nfrom devtools.resources.commands.models.output import (\n    CommandOutputPolicy as CommandOutputPolicy,\n)\nfrom devtools.resources.commands.models.result import CommandResult as CommandResult\n\n__all__ = [\n    \"Command\",\n    \"CommandOutputPolicy\",\n    \"CommandResult\",\n]\n",
        "resource_identity": "161aa54cca99eaed6de081d4617501fc18a54d6c9b9fe2fc35d28d1831f91ad6",
        "start": 0,
        "start_line": 1
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Necessary in at least one minimal complete witness as support for R01. Frozen dataclass fields, specification contract and argv implementation.",
    "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "support_spans": [
      {
        "content_identity": "b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473",
        "end": 1816,
        "end_line": 62,
        "quote": "@dataclass(frozen=True, slots=True)\nclass Command:\n    \"\"\"Describe an immutable command execution specification.\n\n    A command identifies an executable separately from its arguments and does\n    not imply shell parsing, interpolation, or quoting.\n\n    Fluent methods return new command instances and never mutate the original.\n\n    Example::\n\n        command = (\n            Command(\"uv\")\n            .args(\"run\", \"pytest\", \"-q\")\n            .cwd(project_root)\n            .with_timeout(Duration.minutes(2))\n        )\n\n    :ivar executable: Executable name or path.\n    :ivar arguments: Ordered executable arguments.\n    :ivar working_directory: Optional resolved working directory.\n    :ivar timeout: Optional maximum execution duration.\n    \"\"\"\n\n    executable: str\n    arguments: tuple[str, ...] = ()\n    working_directory: ResolvedPath | None = None\n    timeout: Duration | None = None\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate command invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the command specification.\n\n        :raises ValueError: If the executable is empty or whitespace-only.\n        \"\"\"\n        if not self.executable.strip():\n            msg = \"Command executable cannot be empty.\"\n            raise ValueError(msg)\n\n    @property\n    def argv(self) -> tuple[str, ...]:\n        \"\"\"Return the complete process argument vector.\n\n        :returns: Executable followed by all ordered arguments.\n        \"\"\"\n        return (self.executable, *self.arguments)\n",
        "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
        "start": 283,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R01. Frozen dataclass fields, specification contract and argv implementation.",
    "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "support_spans": [
      {
        "content_identity": "b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473",
        "end": 1816,
        "end_line": 62,
        "quote": "@dataclass(frozen=True, slots=True)\nclass Command:\n    \"\"\"Describe an immutable command execution specification.\n\n    A command identifies an executable separately from its arguments and does\n    not imply shell parsing, interpolation, or quoting.\n\n    Fluent methods return new command instances and never mutate the original.\n\n    Example::\n\n        command = (\n            Command(\"uv\")\n            .args(\"run\", \"pytest\", \"-q\")\n            .cwd(project_root)\n            .with_timeout(Duration.minutes(2))\n        )\n\n    :ivar executable: Executable name or path.\n    :ivar arguments: Ordered executable arguments.\n    :ivar working_directory: Optional resolved working directory.\n    :ivar timeout: Optional maximum execution duration.\n    \"\"\"\n\n    executable: str\n    arguments: tuple[str, ...] = ()\n    working_directory: ResolvedPath | None = None\n    timeout: Duration | None = None\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate command invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the command specification.\n\n        :raises ValueError: If the executable is empty or whitespace-only.\n        \"\"\"\n        if not self.executable.strip():\n            msg = \"Command executable cannot be empty.\"\n            raise ValueError(msg)\n\n    @property\n    def argv(self) -> tuple[str, ...]:\n        \"\"\"Return the complete process argument vector.\n\n        :returns: Executable followed by all ordered arguments.\n        \"\"\"\n        return (self.executable, *self.arguments)\n",
        "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
        "start": 283,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful current input construction and immutability context for future controlled regression tests.",
    "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
    "support_spans": [
      {
        "content_identity": "b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473",
        "end": 1816,
        "end_line": 62,
        "quote": "@dataclass(frozen=True, slots=True)\nclass Command:\n    \"\"\"Describe an immutable command execution specification.\n\n    A command identifies an executable separately from its arguments and does\n    not imply shell parsing, interpolation, or quoting.\n\n    Fluent methods return new command instances and never mutate the original.\n\n    Example::\n\n        command = (\n            Command(\"uv\")\n            .args(\"run\", \"pytest\", \"-q\")\n            .cwd(project_root)\n            .with_timeout(Duration.minutes(2))\n        )\n\n    :ivar executable: Executable name or path.\n    :ivar arguments: Ordered executable arguments.\n    :ivar working_directory: Optional resolved working directory.\n    :ivar timeout: Optional maximum execution duration.\n    \"\"\"\n\n    executable: str\n    arguments: tuple[str, ...] = ()\n    working_directory: ResolvedPath | None = None\n    timeout: Duration | None = None\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate command invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the command specification.\n\n        :raises ValueError: If the executable is empty or whitespace-only.\n        \"\"\"\n        if not self.executable.strip():\n            msg = \"Command executable cannot be empty.\"\n            raise ValueError(msg)\n\n    @property\n    def argv(self) -> tuple[str, ...]:\n        \"\"\"Return the complete process argument vector.\n\n        :returns: Executable followed by all ordered arguments.\n        \"\"\"\n        return (self.executable, *self.arguments)\n",
        "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
        "start": 283,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/output.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R04. Policy contract and distinct per-stream byte fields.",
    "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "support_spans": [
      {
        "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
        "end": 1323,
        "end_line": 37,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandOutputPolicy:\n    \"\"\"Bound memory retained for one command execution.\n\n    Output limits apply independently to standard output and standard error.\n    Event buffering is best effort: any newly emitted event is dropped when the\n    pending event limit is reached so process draining never waits for a\n    consumer. No event type is privileged.\n\n    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.\n    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.\n    :ivar max_pending_events: Maximum events awaiting the single consumer.\n    \"\"\"\n\n    max_stdout_bytes: int = 1_048_576\n    max_stderr_bytes: int = 1_048_576\n    max_pending_events: int = 1_024\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate output-retention invariants.\"\"\"\n        if self.max_stdout_bytes < 0:\n            msg = \"Maximum stdout bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_stderr_bytes < 0:\n            msg = \"Maximum stderr bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_pending_events <= 0:\n            msg = \"Maximum pending events must be positive.\"\n            raise ValueError(msg)\n",
        "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
        "start": 97,
        "start_line": 7
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/output.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Corroborates separate event capacity and best-effort buffering, but does not itself tie an omission count to a completed result.",
    "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "support_spans": [
      {
        "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
        "end": 829,
        "end_line": 23,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandOutputPolicy:\n    \"\"\"Bound memory retained for one command execution.\n\n    Output limits apply independently to standard output and standard error.\n    Event buffering is best effort: any newly emitted event is dropped when the\n    pending event limit is reached so process draining never waits for a\n    consumer. No event type is privileged.\n\n    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.\n    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.\n    :ivar max_pending_events: Maximum events awaiting the single consumer.\n    \"\"\"\n\n    max_stdout_bytes: int = 1_048_576\n    max_stderr_bytes: int = 1_048_576\n    max_pending_events: int = 1_024\n",
        "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
        "start": 97,
        "start_line": 7
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/output.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful fixture construction for independent retention scenarios; exact source resource is not required by the future coverage instruction.",
    "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
    "support_spans": [
      {
        "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
        "end": 1323,
        "end_line": 37,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandOutputPolicy:\n    \"\"\"Bound memory retained for one command execution.\n\n    Output limits apply independently to standard output and standard error.\n    Event buffering is best effort: any newly emitted event is dropped when the\n    pending event limit is reached so process draining never waits for a\n    consumer. No event type is privileged.\n\n    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.\n    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.\n    :ivar max_pending_events: Maximum events awaiting the single consumer.\n    \"\"\"\n\n    max_stdout_bytes: int = 1_048_576\n    max_stderr_bytes: int = 1_048_576\n    max_pending_events: int = 1_024\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate output-retention invariants.\"\"\"\n        if self.max_stdout_bytes < 0:\n            msg = \"Maximum stdout bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_stderr_bytes < 0:\n            msg = \"Maximum stderr bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_pending_events <= 0:\n            msg = \"Maximum pending events must be positive.\"\n            raise ValueError(msg)\n",
        "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
        "start": 97,
        "start_line": 7
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Necessary in at least one minimal complete witness as support for R02. Fields and status predicates directly establish the contract.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1729,
        "end_line": 55,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandResult:\n    \"\"\"Represent the completed result of a command execution.\n\n    A nonzero exit code is a valid command result and does not itself represent\n    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`\n    when interpreting the command's exit status.\n\n    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n\n    @property\n    def succeeded(self) -> bool:\n        \"\"\"Return whether the command exited successfully.\n\n        :returns: ``True`` when the exit code is zero.\n        \"\"\"\n        return self.exit_code == 0\n\n    @property\n    def failed(self) -> bool:\n        \"\"\"Return whether the command exited unsuccessfully.\n\n        :returns: ``True`` when the exit code is nonzero.\n        \"\"\"\n        return not self.succeeded\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 274,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Necessary in at least one minimal complete witness as support for R03. Field types and retained-leading-byte documentation.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1308,
        "end_line": 39,
        "quote": "    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 604,
        "start_line": 22
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R05. Each named flag means its stream exceeded retained limit; zero-limit consequence follows from that definition.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1280,
        "end_line": 38,
        "quote": "    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 690,
        "start_line": 24
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06. Separate numeric omission count and retained-output flag meanings.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1308,
        "end_line": 39,
        "quote": "    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 690,
        "start_line": 24
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "DIRECT_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R09. Frozen dataclass declaration and immutable-valued fields.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1308,
        "end_line": 39,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandResult:\n    \"\"\"Represent the completed result of a command execution.\n\n    A nonzero exit code is a valid command result and does not itself represent\n    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`\n    when interpreting the command's exit status.\n\n    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 274,
        "start_line": 14
      }
    ]
  },
  {
    "address": "src/devtools/resources/commands/models/result.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful result-fixture and immutable-input context, not necessary solely because future tests are requested.",
    "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
    "support_spans": [
      {
        "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
        "end": 1729,
        "end_line": 55,
        "quote": "@dataclass(frozen=True, slots=True)\nclass CommandResult:\n    \"\"\"Represent the completed result of a command execution.\n\n    A nonzero exit code is a valid command result and does not itself represent\n    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`\n    when interpreting the command's exit status.\n\n    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n\n    @property\n    def succeeded(self) -> bool:\n        \"\"\"Return whether the command exited successfully.\n\n        :returns: ``True`` when the exit code is zero.\n        \"\"\"\n        return self.exit_code == 0\n\n    @property\n    def failed(self) -> bool:\n        \"\"\"Return whether the command exited unsuccessfully.\n\n        :returns: ``True`` when the exit code is nonzero.\n        \"\"\"\n        return not self.succeeded\n",
        "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
        "start": 274,
        "start_line": 14
      }
    ]
  },
  {
    "address": "tests/agents/integrations/codex/test_agent.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@37524b1f8eb0f2d9faa0ab850fdf52deae56ea57ed9665ba581ccf38cd143d2e",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Shows a controlled executor double constructing completed CommandResult fixtures; useful test technique without requiring this adapter test file.",
    "resource_identity": "37524b1f8eb0f2d9faa0ab850fdf52deae56ea57ed9665ba581ccf38cd143d2e",
    "support_spans": [
      {
        "content_identity": "4c3636ded84b2b1feeebc2b27132308a34c2827098bde9be25d13450a647d607",
        "end": 2455,
        "end_line": 78,
        "quote": "class RecordingExecutor(CommandExecutor):\n    \"\"\"CommandExecutor fake retaining direct-argv invocations.\"\"\"\n\n    def __init__(self, results: Sequence[tuple[int, bytes, bool]]) -> None:\n        \"\"\"Initialize the queued result specifications.\"\"\"\n        super().__init__()\n        self.commands: list[Command] = []\n        self._results = list(results)\n\n    async def execute(self, command: Command) -> CommandResult:\n        \"\"\"Return the next captured deterministic command result.\"\"\"\n        self.commands.append(command)\n        exit_code, stdout, stdout_truncated = self._results.pop(0)\n        return CommandResult(\n            command=command,\n            exit_code=exit_code,\n            stdout=stdout,\n            stderr=b\"diagnostic output is intentionally ignored\",\n            duration=Duration.seconds(0),\n            stdout_truncated=stdout_truncated,\n        )\n\n\nclass MissingExecutor(CommandExecutor):\n    \"\"\"CommandExecutor fake preserving the command-domain missing binary error.\"\"\"\n\n    async def execute(self, _command: Command) -> CommandResult:\n        \"\"\"Raise the same error emitted by a missing executable at execution.\"\"\"\n        raise CommandNotFoundError\n\n",
        "resource_identity": "37524b1f8eb0f2d9faa0ab850fdf52deae56ea57ed9665ba581ccf38cd143d2e",
        "start": 1273,
        "start_line": 49
      }
    ]
  },
  {
    "address": "tests/core/time/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@d72f337252161b196dcd8aebdec5da0dcd2a063ff3b4882530b54dbf87d5fbb6",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Examples corroborate Duration value/accessor/string semantics for optional formatting; the renderer need not use this exact format.",
    "resource_identity": "d72f337252161b196dcd8aebdec5da0dcd2a063ff3b4882530b54dbf87d5fbb6",
    "support_spans": [
      {
        "content_identity": "0738320772b65625e0085212c949e34b4185fcf58ebe093ed4d45a8d358b6660",
        "end": 3168,
        "end_line": 83,
        "quote": "def test_duration_factories_create_expected_values() -> None:\n    \"\"\"Each public duration factory delegates to its documented unit.\"\"\"\n    assert Duration.nanoseconds(2_000).value == timedelta(microseconds=2)\n    assert Duration.seconds(2.5).value == timedelta(seconds=2.5)\n    assert Duration.milliseconds(2.5).value == timedelta(milliseconds=2.5)\n    assert Duration.minutes(2.5).value == timedelta(minutes=2.5)\n    assert Duration.hours(2.5).value == timedelta(hours=2.5)\n\n\ndef test_duration_accessors_string_and_value_semantics() -> None:\n    \"\"\"Duration representations expose the underlying elapsed amount.\"\"\"\n    expected_seconds = 1.25\n    expected_milliseconds = 1250.0\n    duration = Duration(timedelta(seconds=expected_seconds))\n\n    assert duration.total_seconds == expected_seconds\n    assert duration.total_milliseconds == expected_milliseconds\n    assert str(duration) == \"0:00:01.250000\"\n    assert duration == Duration.seconds(expected_seconds)\n    assert hash(duration) == hash(Duration.seconds(expected_seconds))\n",
        "resource_identity": "d72f337252161b196dcd8aebdec5da0dcd2a063ff3b4882530b54dbf87d5fbb6",
        "start": 2136,
        "start_line": 64
      }
    ]
  },
  {
    "address": "tests/models/serving/test_llama_cpp.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Controlled result construction and executor fake are useful regression examples, without requiring model-service tests for the commands renderer.",
    "resource_identity": "a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402",
    "support_spans": [
      {
        "content_identity": "2de258ff8b06e27cb3a0642c77839aef7a6511a39b5809a3dad19029b32c13df",
        "end": 1936,
        "end_line": 63,
        "quote": "def _result(\n    command: Command,\n    code: int = 0,\n    out: bytes = b\"\",\n    err: bytes = b\"\",\n) -> CommandResult:\n    return CommandResult(command, code, out, err, Duration.seconds(0))\n\n\ndef _config(tmp_path: Path, **changes: object) -> llama_cpp.LlamaCppServingConfig:\n    model = tmp_path / \"model.gguf\"\n    model.touch(exist_ok=True)\n    values: dict[str, object] = {\n        \"model\": llama_cpp.GGUFModel(ResolvedPath(model)),\n        \"image\": \"ghcr.io/ggml-org/llama.cpp:server-cuda\",\n        \"host_port\": 8081,\n        \"served_model_name\": \"local-model\",\n        \"context_size\": 4096,\n        \"gpu_layers\": \"all\",\n    }\n    values.update(changes)\n    return llama_cpp.LlamaCppServingConfig(**values)  # type: ignore[arg-type]\n\n\nclass _Executor(CommandExecutor):\n    def __init__(self, results: list[CommandResult | BaseException]) -> None:\n        self.commands: list[Command] = []\n        self.results = results\n\n    async def execute(self, command: Command) -> CommandResult:\n        self.commands.append(command)\n        value = self.results.pop(0)\n        if isinstance(value, BaseException):\n            raise value\n        return value\n",
        "resource_identity": "a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402",
        "start": 785,
        "start_line": 29
      }
    ]
  },
  {
    "address": "tests/models/serving/test_vllm.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Controlled completed-result fixtures and exception propagation examples are useful testing context, not a necessary commands test destination.",
    "resource_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
    "support_spans": [
      {
        "content_identity": "66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8",
        "end": 3148,
        "end_line": 99,
        "quote": "def _result(\n    command: Command,\n    *,\n    exit_code: int = 0,\n    stdout: bytes = b\"\",\n    stderr: bytes = b\"diagnostic\",\n) -> CommandResult:\n    \"\"\"Create a compact ordinary command result.\"\"\"\n    return CommandResult(command, exit_code, stdout, stderr, Duration.seconds(0))\n\n\ndef _not_found_result(command: Command) -> CommandResult:\n    \"\"\"Create Docker's exact absent-container inspection result.\"\"\"\n    return _result(\n        command,\n        exit_code=1,\n        stderr=f\"Error: No such object: {_VALID_CONTAINER_ID}\".encode(),\n    )\n\n\ndef _assert_no_prefetch_arguments(command: Command) -> None:\n    \"\"\"Require that a historical command has no prefetch provider flags.\"\"\"\n    assert all(option not in command.arguments for option in _PREFETCH_OPTIONS)\n\n\nclass _Executor:\n    \"\"\"Record commands and return queued results or errors.\"\"\"\n\n    def __init__(self, responses: list[CommandResult | BaseException]) -> None:\n        \"\"\"Initialize queued execution behavior.\"\"\"\n        self.commands: list[Command] = []\n        self._responses = responses\n\n    async def execute(self, command: Command) -> CommandResult:\n        \"\"\"Record one command and apply the next planned outcome.\"\"\"\n        self.commands.append(command)\n        response = self._responses.pop(0)\n        if isinstance(response, BaseException):\n            raise response\n\n        return response\n",
        "resource_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
        "start": 1777,
        "start_line": 59
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_errors.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Confirms public command error hierarchy and a nearby test style; does not establish exceptional no-result behavior.",
    "resource_identity": "4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
    "support_spans": [
      {
        "content_identity": "16db7e62541ee215137cacf568e3631473a1ae31de96f0c998ddb73bb7cdf3ac",
        "end": 491,
        "end_line": 15,
        "quote": "from devtools.resources.commands import (\n    CommandError,\n    CommandNotFoundError,\n    CommandTimeoutError,\n)\n\n\ndef test_command_errors_share_the_domain_base_type() -> None:\n    \"\"\"Specific command errors remain catchable as command-domain failures.\"\"\"\n    assert issubclass(CommandNotFoundError, CommandError)\n    assert issubclass(CommandTimeoutError, CommandError)\n    assert issubclass(CommandError, Exception)\n",
        "resource_identity": "4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
        "start": 73,
        "start_line": 4
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_errors.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Confirms public command error hierarchy and a nearby test style; does not establish exceptional no-result behavior.",
    "resource_identity": "4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
    "support_spans": [
      {
        "content_identity": "16db7e62541ee215137cacf568e3631473a1ae31de96f0c998ddb73bb7cdf3ac",
        "end": 491,
        "end_line": 15,
        "quote": "from devtools.resources.commands import (\n    CommandError,\n    CommandNotFoundError,\n    CommandTimeoutError,\n)\n\n\ndef test_command_errors_share_the_domain_base_type() -> None:\n    \"\"\"Specific command errors remain catchable as command-domain failures.\"\"\"\n    assert issubclass(CommandNotFoundError, CommandError)\n    assert issubclass(CommandTimeoutError, CommandError)\n    assert issubclass(CommandError, Exception)\n",
        "resource_identity": "4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
        "start": 73,
        "start_line": 4
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_events.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Corroborates immutable event values and an immutability test idiom; rendering consumes completed results, so these events need not be reconstructed.",
    "resource_identity": "e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
    "support_spans": [
      {
        "content_identity": "229c76e8ba2d20feec3734c5a62f02b1c08941aa09daa90702d41cdafc6669ee",
        "end": 1023,
        "end_line": 34,
        "quote": "def test_command_events_are_immutable_value_objects() -> None:\n    \"\"\"Each event retains its structured observation data immutably.\"\"\"\n    command = Command(\"python\", (\"-c\", \"pass\"))\n    started = CommandStarted(command)\n    stdout = CommandStdout(b\"out\")\n    stderr = CommandStderr(b\"error\")\n    exited = CommandExited(0, Duration.seconds(1))\n    attribute = \"data\"\n\n    assert started == CommandStarted(command)\n    assert stdout == CommandStdout(b\"out\")\n    assert stderr == CommandStderr(b\"error\")\n    assert exited == CommandExited(0, Duration.seconds(1))\n    assert hash(started) == hash(CommandStarted(command))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(stdout, attribute, b\"changed\")\n",
        "resource_identity": "e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
        "start": 311,
        "start_line": 18
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_events.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Corroborates immutable event values and an immutability test idiom; rendering consumes completed results, so these events need not be reconstructed.",
    "resource_identity": "e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
    "support_spans": [
      {
        "content_identity": "229c76e8ba2d20feec3734c5a62f02b1c08941aa09daa90702d41cdafc6669ee",
        "end": 1023,
        "end_line": 34,
        "quote": "def test_command_events_are_immutable_value_objects() -> None:\n    \"\"\"Each event retains its structured observation data immutably.\"\"\"\n    command = Command(\"python\", (\"-c\", \"pass\"))\n    started = CommandStarted(command)\n    stdout = CommandStdout(b\"out\")\n    stderr = CommandStderr(b\"error\")\n    exited = CommandExited(0, Duration.seconds(1))\n    attribute = \"data\"\n\n    assert started == CommandStarted(command)\n    assert stdout == CommandStdout(b\"out\")\n    assert stderr == CommandStderr(b\"error\")\n    assert exited == CommandExited(0, Duration.seconds(1))\n    assert hash(started) == hash(CommandStarted(command))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(stdout, attribute, b\"changed\")\n",
        "resource_identity": "e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
        "start": 311,
        "start_line": 18
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Corroborates completed nonzero results and duration, but lacks the complete structured immutable input contract and exact status definitions.",
    "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "support_spans": [
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 1553,
        "end_line": 56,
        "quote": "def test_executor_runs_python_and_preserves_argument_bytes() -> None:\n    \"\"\"The executor captures raw output from a portable Python subprocess.\"\"\"\n    command = Command(\n        sys.executable,\n        (\"-c\", \"import sys; print('|'.join(sys.argv[1:]))\", \"first\", \"second\"),\n    )\n\n    result = asyncio.run(CommandExecutor().execute(command))\n\n    assert result.succeeded is True\n    assert result.stdout.strip() == b\"first|second\"\n    assert result.stderr == b\"\"\n    assert isinstance(result.duration, Duration)\n    assert result.duration.total_seconds >= 0\n\n\ndef test_executor_returns_nonzero_exit_codes_as_results() -> None:\n    \"\"\"A process failure code is represented without an execution exception.\"\"\"\n    expected_exit_code = 7\n    command = Command(\n        sys.executable,\n        (\"-c\", f\"import sys; sys.exit({expected_exit_code})\"),\n    )\n\n    result = asyncio.run(CommandExecutor().execute(command))\n\n    assert result.exit_code == expected_exit_code\n    assert result.failed is True\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 556,
        "start_line": 29
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Necessary in at least one minimal complete witness as support for R03. Known byte chunks yield exact retained prefixes in each result stream, including zero retention.",
    "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "support_spans": [
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 7968,
        "end_line": 265,
        "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 5617,
        "start_line": 190
      },
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 12084,
        "end_line": 408,
        "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 10744,
        "start_line": 366
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Necessary in at least one minimal complete witness as support for R04, R05. Different byte limits and zero retention are controlled and asserted independently. Assertions connect bounded and zero-byte retention to each flag.",
    "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "support_spans": [
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 7968,
        "end_line": 265,
        "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 5617,
        "start_line": 190
      },
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 12084,
        "end_line": 408,
        "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 10744,
        "start_line": 366
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R06. Independent queue capacity and stream limits produce a numeric omission count; lost exit event demonstrates results are not complete transcripts.",
    "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "support_spans": [
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 7968,
        "end_line": 265,
        "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 5617,
        "start_line": 190
      },
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 12084,
        "end_line": 408,
        "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 10744,
        "start_line": 366
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_execution.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Relevant controlled retention/event-loss fixture conventions and existing coverage; the future test location and coverage requirements are task-backed.",
    "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
    "support_spans": [
      {
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "end": 7968,
        "end_line": 265,
        "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
        "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "start": 5617,
        "start_line": 190
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_handle.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Corroborates one completed result and separately retained stream bytes; it does not establish all result semantics or prefix truncation.",
    "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "support_spans": [
      {
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "end": 2100,
        "end_line": 76,
        "quote": "def test_start_returns_one_awaitable_execution_handle() -> None:\n    \"\"\"A started command should create one awaitable live execution handle.\"\"\"\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(sys.executable, (\"-c\", \"print('once')\")),\n        )\n\n        assert isinstance(execution, CommandExecution)\n        assert execution.is_running is True\n        assert execution.is_complete is False\n\n        first = await execution\n        second = await execution\n\n        assert first is second\n        assert first.stdout.strip() == b\"once\"\n        assert execution.is_running is False\n        assert execution.is_complete is True\n\n    asyncio.run(run())\n\n\ndef test_event_stream_preserves_output_and_closes_before_final_await() -> None:\n    \"\"\"Streaming observations and the final result share one execution.\"\"\"\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(\n                sys.executable,\n                (\n                    \"-c\",\n                    \"import sys; print('out'); print('err', file=sys.stderr)\",\n                ),\n            ),\n        )\n        events = [event async for event in execution.events()]\n        result = await execution\n\n        assert isinstance(events[0], CommandStarted)\n        assert any(\n            isinstance(event, CommandStdout) and b\"out\" in event.data\n            for event in events\n        )\n        assert any(\n            isinstance(event, CommandStderr) and b\"err\" in event.data\n            for event in events\n        )\n        assert result.stdout.strip() == b\"out\"\n        assert result.stderr.strip() == b\"err\"\n\n    asyncio.run(run())\n",
        "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "start": 420,
        "start_line": 25
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_handle.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Corroborates one completed result and separately retained stream bytes; it does not establish all result semantics or prefix truncation.",
    "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "support_spans": [
      {
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "end": 2100,
        "end_line": 76,
        "quote": "def test_start_returns_one_awaitable_execution_handle() -> None:\n    \"\"\"A started command should create one awaitable live execution handle.\"\"\"\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(sys.executable, (\"-c\", \"print('once')\")),\n        )\n\n        assert isinstance(execution, CommandExecution)\n        assert execution.is_running is True\n        assert execution.is_complete is False\n\n        first = await execution\n        second = await execution\n\n        assert first is second\n        assert first.stdout.strip() == b\"once\"\n        assert execution.is_running is False\n        assert execution.is_complete is True\n\n    asyncio.run(run())\n\n\ndef test_event_stream_preserves_output_and_closes_before_final_await() -> None:\n    \"\"\"Streaming observations and the final result share one execution.\"\"\"\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(\n                sys.executable,\n                (\n                    \"-c\",\n                    \"import sys; print('out'); print('err', file=sys.stderr)\",\n                ),\n            ),\n        )\n        events = [event async for event in execution.events()]\n        result = await execution\n\n        assert isinstance(events[0], CommandStarted)\n        assert any(\n            isinstance(event, CommandStdout) and b\"out\" in event.data\n            for event in events\n        )\n        assert any(\n            isinstance(event, CommandStderr) and b\"err\" in event.data\n            for event in events\n        )\n        assert result.stdout.strip() == b\"out\"\n        assert result.stderr.strip() == b\"err\"\n\n    asyncio.run(run())\n",
        "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "start": 420,
        "start_line": 25
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_handle.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R07. Controlled awaited executions raise all three exceptions instead of returning results.",
    "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "support_spans": [
      {
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "end": 5763,
        "end_line": 196,
        "quote": "def test_missing_executable_closes_the_event_stream(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Failure during process creation does not leave event consumers waiting.\"\"\"\n\n    async def raise_not_found(*_args: object, **_kwargs: object) -> None:\n        raise FileNotFoundError\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"missing-command\"))\n        events = [event async for event in execution.events()]\n\n        assert events == []\n\n        with pytest.raises(CommandNotFoundError):\n            await execution\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        raise_not_found,\n    )\n    asyncio.run(run())\n\n\ndef test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:\n    \"\"\"Timeout cleanup closes event iteration before propagating the error.\"\"\"\n    process = _TimedOutProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _TimedOutProcess:\n        return process\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(\"slow-command\", timeout=Duration.seconds(0.001)),\n        )\n        events = [event async for event in execution.events()]\n\n        assert len(events) == 1\n        assert isinstance(events[0], CommandStarted)\n\n        with pytest.raises(CommandTimeoutError):\n            await execution\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n\n\ndef test_cancellation_kills_reaps_and_closes_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancelling a live execution cleans up its immediate child process.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _BlockingProcess:\n        return process\n\n    async def await_execution(execution: CommandExecution) -> None:\n        \"\"\"Await one execution so caller cancellation reaches its task.\"\"\"\n        await execution\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"blocking-command\"))\n        events_task = asyncio.create_task(_collect_events(execution))\n        awaiter = asyncio.create_task(await_execution(execution))\n        shared_awaiter = asyncio.create_task(await_execution(execution))\n\n        await process.stdout.read_started.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        with pytest.raises(asyncio.CancelledError):\n            await shared_awaiter\n\n        events = await events_task\n\n        assert process.killed is True\n        assert process.waited is True\n        assert any(isinstance(event, CommandStarted) for event in events)\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n",
        "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "start": 2682,
        "start_line": 101
      },
      {
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "end": 9137,
        "end_line": 301,
        "quote": "def test_cancellation_before_process_creation_closes_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation while creating a process still closes its event stream.\"\"\"\n    process_creation_started = asyncio.Event()\n    process_creation_release = asyncio.Event()\n\n    async def create_process(*_args: object, **_kwargs: object) -> None:\n        process_creation_started.set()\n        await process_creation_release.wait()\n\n    async def await_execution(\n        execution: CommandExecution,\n        awaiting_execution: asyncio.Event,\n    ) -> None:\n        \"\"\"Await an execution after reporting that cancellation can propagate.\"\"\"\n        awaiting_execution.set()\n        await execution\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"creating-command\"))\n        events_task = asyncio.create_task(_collect_events(execution))\n        awaiting_execution = asyncio.Event()\n        awaiter = asyncio.create_task(await_execution(execution, awaiting_execution))\n\n        await process_creation_started.wait()\n        await awaiting_execution.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        assert await events_task == []\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n\n\ndef test_cancellation_reaps_an_already_exited_process(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation reaps a child without killing it after it has exited.\"\"\"\n    process = _BlockingProcess(returncode=0)\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _BlockingProcess:\n        return process\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"completed-command\"))\n        awaiter = asyncio.ensure_future(execution)\n\n        await process.stdout.read_started.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        assert process.killed is False\n        assert process.waited is True\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n",
        "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "start": 6831,
        "start_line": 231
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_handle.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Existing lifecycle fixtures are useful regression context; no requirement forces edits to this exact test resource.",
    "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
    "support_spans": [
      {
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "end": 5763,
        "end_line": 196,
        "quote": "def test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:\n    \"\"\"Timeout cleanup closes event iteration before propagating the error.\"\"\"\n    process = _TimedOutProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _TimedOutProcess:\n        return process\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(\"slow-command\", timeout=Duration.seconds(0.001)),\n        )\n        events = [event async for event in execution.events()]\n\n        assert len(events) == 1\n        assert isinstance(events[0], CommandStarted)\n\n        with pytest.raises(CommandTimeoutError):\n            await execution\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n\n\ndef test_cancellation_kills_reaps_and_closes_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancelling a live execution cleans up its immediate child process.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _BlockingProcess:\n        return process\n\n    async def await_execution(execution: CommandExecution) -> None:\n        \"\"\"Await one execution so caller cancellation reaches its task.\"\"\"\n        await execution\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"blocking-command\"))\n        events_task = asyncio.create_task(_collect_events(execution))\n        awaiter = asyncio.create_task(await_execution(execution))\n        shared_awaiter = asyncio.create_task(await_execution(execution))\n\n        await process.stdout.read_started.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        with pytest.raises(asyncio.CancelledError):\n            await shared_awaiter\n\n        events = await events_task\n\n        assert process.killed is True\n        assert process.waited is True\n        assert any(isinstance(event, CommandStarted) for event in events)\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n",
        "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "start": 3407,
        "start_line": 125
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Necessary in at least one minimal complete witness as support for R01, R02. Explicit structured-value and frozen-input tests establish the intended public contract. The test explicitly describes nonzero completion and asserts preserved fields and both complementary status values.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 2914,
        "end_line": 84,
        "quote": "def test_command_preserves_separate_executable_arguments_and_options(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Commands retain structured process arguments and optional execution data.\"\"\"\n    command = Command(\n        executable=\"python\",\n        arguments=(\"-c\", \"print('hello')\"),\n        working_directory=ResolvedPath(tmp_path),\n        timeout=Duration.seconds(3),\n    )\n\n    assert command.executable == \"python\"\n    assert command.arguments == (\"-c\", \"print('hello')\")\n    assert command.working_directory == ResolvedPath(tmp_path)\n    assert command.timeout == Duration.seconds(3)\n    assert command.argv == (\"python\", \"-c\", \"print('hello')\")\n\n\ndef test_command_defaults_to_no_arguments_and_is_immutable() -> None:\n    \"\"\"Commands have an empty argument tuple and frozen value semantics.\"\"\"\n    command = Command(\"python\")\n    attribute = \"executable\"\n\n    assert command.arguments == ()\n    assert command == Command(\"python\")\n    assert hash(command) == hash(Command(\"python\"))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(command, attribute, \"other\")\n\n\ndef test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:\n    \"\"\"Fluent command methods preserve unrelated immutable specification data.\"\"\"\n    original = (\n        Command(\"python\", (\"-m\",))\n        .cwd(ResolvedPath(tmp_path))\n        .with_timeout(Duration.seconds(1))\n    )\n    appended = original.args(\"pytest\", \"-q\")\n    replaced = appended.with_args(\"-c\", \"pass\")\n    cleared = replaced.without_args()\n    renamed = cleared.with_executable(\"python3\")\n    without_cwd = renamed.without_cwd()\n    without_timeout = without_cwd.without_timeout()\n\n    assert original == Command(\n        \"python\",\n        (\"-m\",),\n        ResolvedPath(tmp_path),\n        Duration.seconds(1),\n    )\n    assert appended.arguments == (\"-m\", \"pytest\", \"-q\")\n    assert replaced.arguments == (\"-c\", \"pass\")\n    assert cleared.arguments == ()\n    assert cleared.working_directory == ResolvedPath(tmp_path)\n    assert cleared.timeout == Duration.seconds(1)\n    assert renamed.executable == \"python3\"\n    assert renamed.working_directory == ResolvedPath(tmp_path)\n    assert renamed.timeout == Duration.seconds(1)\n    assert without_cwd.working_directory is None\n    assert without_cwd.timeout == Duration.seconds(1)\n    assert without_timeout.timeout is None\n    assert without_timeout.executable == \"python3\"\n\n    with pytest.raises(ValueError, match=\"cannot be empty\"):\n        renamed.with_executable(\"   \")\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 416,
        "start_line": 19
      },
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 4184,
        "end_line": 120,
        "quote": "def test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 3194,
        "start_line": 94
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O2@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O2",
    "rationale": "Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 4987,
        "end_line": 147,
        "quote": "def test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n\n\n@pytest.mark.parametrize(\n    (\"field\", \"value\", \"match\"),\n    [\n        (\"max_stdout_bytes\", -1, \"stdout\"),\n        (\"max_stderr_bytes\", -1, \"stderr\"),\n        (\"max_pending_events\", 0, \"pending events\"),\n    ],\n)\ndef test_command_output_policy_rejects_invalid_bounds(\n    field: str,\n    value: int,\n    match: str,\n) -> None:\n    \"\"\"Output limits reject values that cannot form bounded policies.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        CommandOutputPolicy(**{field: value})\n\n\ndef test_command_output_policy_exposes_default_bounds() -> None:\n    \"\"\"Default output limits are positive and practical for ordinary commands.\"\"\"\n    policy = CommandOutputPolicy()\n\n    assert policy.max_stdout_bytes > 0\n    assert policy.max_stderr_bytes > 0\n    assert policy.max_pending_events > 0\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 3194,
        "start_line": 94
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O3@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O3",
    "rationale": "Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 4987,
        "end_line": 147,
        "quote": "def test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n\n\n@pytest.mark.parametrize(\n    (\"field\", \"value\", \"match\"),\n    [\n        (\"max_stdout_bytes\", -1, \"stdout\"),\n        (\"max_stderr_bytes\", -1, \"stderr\"),\n        (\"max_pending_events\", 0, \"pending events\"),\n    ],\n)\ndef test_command_output_policy_rejects_invalid_bounds(\n    field: str,\n    value: int,\n    match: str,\n) -> None:\n    \"\"\"Output limits reject values that cannot form bounded policies.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        CommandOutputPolicy(**{field: value})\n\n\ndef test_command_output_policy_exposes_default_bounds() -> None:\n    \"\"\"Default output limits are positive and practical for ordinary commands.\"\"\"\n    policy = CommandOutputPolicy()\n\n    assert policy.max_stdout_bytes > 0\n    assert policy.max_stderr_bytes > 0\n    assert policy.max_pending_events > 0\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 3194,
        "start_line": 94
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Corroborates original bytes, default retention flags/event count and policy validation, but lacks complete prefix-loss and event independence contracts.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 4987,
        "end_line": 147,
        "quote": "def test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n\n\n@pytest.mark.parametrize(\n    (\"field\", \"value\", \"match\"),\n    [\n        (\"max_stdout_bytes\", -1, \"stdout\"),\n        (\"max_stderr_bytes\", -1, \"stderr\"),\n        (\"max_pending_events\", 0, \"pending events\"),\n    ],\n)\ndef test_command_output_policy_rejects_invalid_bounds(\n    field: str,\n    value: int,\n    match: str,\n) -> None:\n    \"\"\"Output limits reject values that cannot form bounded policies.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        CommandOutputPolicy(**{field: value})\n\n\ndef test_command_output_policy_exposes_default_bounds() -> None:\n    \"\"\"Default output limits are positive and practical for ordinary commands.\"\"\"\n    policy = CommandOutputPolicy()\n\n    assert policy.max_stdout_bytes > 0\n    assert policy.max_stderr_bytes > 0\n    assert policy.max_pending_events > 0\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 3194,
        "start_line": 94
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O5@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O5",
    "rationale": "Necessary in at least one minimal complete witness as support for R01. Explicit structured-value and frozen-input tests establish the intended public contract.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 2914,
        "end_line": 84,
        "quote": "def test_command_preserves_separate_executable_arguments_and_options(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Commands retain structured process arguments and optional execution data.\"\"\"\n    command = Command(\n        executable=\"python\",\n        arguments=(\"-c\", \"print('hello')\"),\n        working_directory=ResolvedPath(tmp_path),\n        timeout=Duration.seconds(3),\n    )\n\n    assert command.executable == \"python\"\n    assert command.arguments == (\"-c\", \"print('hello')\")\n    assert command.working_directory == ResolvedPath(tmp_path)\n    assert command.timeout == Duration.seconds(3)\n    assert command.argv == (\"python\", \"-c\", \"print('hello')\")\n\n\ndef test_command_defaults_to_no_arguments_and_is_immutable() -> None:\n    \"\"\"Commands have an empty argument tuple and frozen value semantics.\"\"\"\n    command = Command(\"python\")\n    attribute = \"executable\"\n\n    assert command.arguments == ()\n    assert command == Command(\"python\")\n    assert hash(command) == hash(Command(\"python\"))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(command, attribute, \"other\")\n\n\ndef test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:\n    \"\"\"Fluent command methods preserve unrelated immutable specification data.\"\"\"\n    original = (\n        Command(\"python\", (\"-m\",))\n        .cwd(ResolvedPath(tmp_path))\n        .with_timeout(Duration.seconds(1))\n    )\n    appended = original.args(\"pytest\", \"-q\")\n    replaced = appended.with_args(\"-c\", \"pass\")\n    cleared = replaced.without_args()\n    renamed = cleared.with_executable(\"python3\")\n    without_cwd = renamed.without_cwd()\n    without_timeout = without_cwd.without_timeout()\n\n    assert original == Command(\n        \"python\",\n        (\"-m\",),\n        ResolvedPath(tmp_path),\n        Duration.seconds(1),\n    )\n    assert appended.arguments == (\"-m\", \"pytest\", \"-q\")\n    assert replaced.arguments == (\"-c\", \"pass\")\n    assert cleared.arguments == ()\n    assert cleared.working_directory == ResolvedPath(tmp_path)\n    assert cleared.timeout == Duration.seconds(1)\n    assert renamed.executable == \"python3\"\n    assert renamed.working_directory == ResolvedPath(tmp_path)\n    assert renamed.timeout == Duration.seconds(1)\n    assert without_cwd.working_directory is None\n    assert without_cwd.timeout == Duration.seconds(1)\n    assert without_timeout.timeout is None\n    assert without_timeout.executable == \"python3\"\n\n    with pytest.raises(ValueError, match=\"cannot be empty\"):\n        renamed.with_executable(\"   \")\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 416,
        "start_line": 19
      }
    ]
  },
  {
    "address": "tests/resources/commands/test_models.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful current commands model regression organization and fixture examples; future tests can be added without this exact resource.",
    "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
    "support_spans": [
      {
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "end": 4987,
        "end_line": 147,
        "quote": "def test_command_preserves_separate_executable_arguments_and_options(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Commands retain structured process arguments and optional execution data.\"\"\"\n    command = Command(\n        executable=\"python\",\n        arguments=(\"-c\", \"print('hello')\"),\n        working_directory=ResolvedPath(tmp_path),\n        timeout=Duration.seconds(3),\n    )\n\n    assert command.executable == \"python\"\n    assert command.arguments == (\"-c\", \"print('hello')\")\n    assert command.working_directory == ResolvedPath(tmp_path)\n    assert command.timeout == Duration.seconds(3)\n    assert command.argv == (\"python\", \"-c\", \"print('hello')\")\n\n\ndef test_command_defaults_to_no_arguments_and_is_immutable() -> None:\n    \"\"\"Commands have an empty argument tuple and frozen value semantics.\"\"\"\n    command = Command(\"python\")\n    attribute = \"executable\"\n\n    assert command.arguments == ()\n    assert command == Command(\"python\")\n    assert hash(command) == hash(Command(\"python\"))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(command, attribute, \"other\")\n\n\ndef test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:\n    \"\"\"Fluent command methods preserve unrelated immutable specification data.\"\"\"\n    original = (\n        Command(\"python\", (\"-m\",))\n        .cwd(ResolvedPath(tmp_path))\n        .with_timeout(Duration.seconds(1))\n    )\n    appended = original.args(\"pytest\", \"-q\")\n    replaced = appended.with_args(\"-c\", \"pass\")\n    cleared = replaced.without_args()\n    renamed = cleared.with_executable(\"python3\")\n    without_cwd = renamed.without_cwd()\n    without_timeout = without_cwd.without_timeout()\n\n    assert original == Command(\n        \"python\",\n        (\"-m\",),\n        ResolvedPath(tmp_path),\n        Duration.seconds(1),\n    )\n    assert appended.arguments == (\"-m\", \"pytest\", \"-q\")\n    assert replaced.arguments == (\"-c\", \"pass\")\n    assert cleared.arguments == ()\n    assert cleared.working_directory == ResolvedPath(tmp_path)\n    assert cleared.timeout == Duration.seconds(1)\n    assert renamed.executable == \"python3\"\n    assert renamed.working_directory == ResolvedPath(tmp_path)\n    assert renamed.timeout == Duration.seconds(1)\n    assert without_cwd.working_directory is None\n    assert without_cwd.timeout == Duration.seconds(1)\n    assert without_timeout.timeout is None\n    assert without_timeout.executable == \"python3\"\n\n    with pytest.raises(ValueError, match=\"cannot be empty\"):\n        renamed.with_executable(\"   \")\n\n\n@pytest.mark.parametrize(\"executable\", [\"\", \"   \"])\ndef test_command_rejects_blank_executables(executable: str) -> None:\n    \"\"\"Commands require a non-blank executable representation.\"\"\"\n    with pytest.raises(ValueError, match=\"cannot be empty\"):\n        Command(executable)\n\n\ndef test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n\n\n@pytest.mark.parametrize(\n    (\"field\", \"value\", \"match\"),\n    [\n        (\"max_stdout_bytes\", -1, \"stdout\"),\n        (\"max_stderr_bytes\", -1, \"stderr\"),\n        (\"max_pending_events\", 0, \"pending events\"),\n    ],\n)\ndef test_command_output_policy_rejects_invalid_bounds(\n    field: str,\n    value: int,\n    match: str,\n) -> None:\n    \"\"\"Output limits reject values that cannot form bounded policies.\"\"\"\n    with pytest.raises(ValueError, match=match):\n        CommandOutputPolicy(**{field: value})\n\n\ndef test_command_output_policy_exposes_default_bounds() -> None:\n    \"\"\"Default output limits are positive and practical for ordinary commands.\"\"\"\n    policy = CommandOutputPolicy()\n\n    assert policy.max_stdout_bytes > 0\n    assert policy.max_stderr_bytes > 0\n    assert policy.max_pending_events > 0\n",
        "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "start": 416,
        "start_line": 19
      }
    ]
  },
  {
    "address": "tests/scripts/qwen/test_llama_cpp_service.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@e6e99c0bd3305061c8522f31cf1b7ddca3a9f1a5ae3acc40f5dd56026fdbc1f7",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Another controlled result fixture/executor example; not a necessary source of the future regression requirements.",
    "resource_identity": "e6e99c0bd3305061c8522f31cf1b7ddca3a9f1a5ae3acc40f5dd56026fdbc1f7",
    "support_spans": [
      {
        "content_identity": "d91be75d45780bd76e9606526e6d391c07e7dcc729c73fc4e62d0b6a5181b848",
        "end": 1926,
        "end_line": 66,
        "quote": "def _result(\n    command: Command,\n    code: int = 0,\n    out: bytes = b\"\",\n    err: bytes = b\"\",\n) -> CommandResult:\n    return CommandResult(command, code, out, err, Duration.seconds(0))\n\n\nclass _Executor:\n    def __init__(self, values: list[CommandResult]) -> None:\n        self.commands: list[Command] = []\n        self._values = values\n\n    async def execute(self, command: Command) -> CommandResult:\n        self.commands.append(command)\n        return self._values.pop(0)\n",
        "resource_identity": "e6e99c0bd3305061c8522f31cf1b7ddca3a9f1a5ae3acc40f5dd56026fdbc1f7",
        "start": 1447,
        "start_line": 50
      }
    ]
  },
  {
    "address": "tests/scripts/test_validate_development.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Necessary in at least one minimal complete witness as support for R10. Independent contract tests assert the exact directory exclusion and unchanged pytest outcome.",
    "resource_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
    "support_spans": [
      {
        "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
        "end": 1503,
        "end_line": 48,
        "quote": "_SCRIPT_PATH = Path(\"scripts/validate_development.py\")\n\n\n@pytest.fixture\ndef validation_script() -> ModuleType:\n    \"\"\"Load the operational script without making scripts a library package.\"\"\"\n    specification = importlib.util.spec_from_file_location(\n        \"test_validate_development_script\",\n        _SCRIPT_PATH,\n    )\n    assert specification is not None\n    assert specification.loader is not None\n    module = importlib.util.module_from_spec(specification)\n    sys.modules[specification.name] = module\n    specification.loader.exec_module(module)\n    return module\n\n\ndef test_profile_selects_tests_and_excludes_experiment_tests_before_collection(\n    validation_script: ModuleType,\n) -> None:\n    \"\"\"The directory boundary covers the whole retained experiment population.\"\"\"\n    arguments = validation_script.pytest_arguments(Path.cwd())\n    tests = Path(arguments[0])\n    ignored = Path(arguments[1].removeprefix(\"--ignore=\"))\n\n    assert tests == Path.cwd() / \"tests\"\n    assert ignored == tests / \"experiments\"\n    assert tests.is_dir()\n    assert ignored.is_dir()\n    assert (tests / \"context\").is_dir()\n    assert (tests / \"scripts\" / \"test_validate_development.py\").is_file()\n",
        "resource_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "start": 313,
        "start_line": 17
      },
      {
        "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
        "end": 2104,
        "end_line": 68,
        "quote": "def test_profile_propagates_pytest_failure_code(\n    validation_script: ModuleType,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A failed pytest run remains a failed profile invocation.\"\"\"\n    observed_arguments: list[str] | None = None\n\n    def failed_pytest(arguments: list[str]) -> int:\n        nonlocal observed_arguments\n        observed_arguments = arguments\n        return 1\n\n    monkeypatch.setattr(validation_script.pytest, \"main\", failed_pytest)\n\n    result = validation_script.main()\n\n    assert result == 1\n    assert observed_arguments == validation_script.pytest_arguments()\n",
        "resource_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "start": 1505,
        "start_line": 51
      }
    ]
  },
  {
    "address": "tests/tools/test_command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O1@5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O1",
    "rationale": "Consumer regression corroborates command identity and ordinary nonzero completed results without defining all core result semantics.",
    "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "support_spans": [
      {
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "end": 1647,
        "end_line": 56,
        "quote": "def test_command_tool_is_typed_tool_and_returns_command_result() -> None:\n    \"\"\"CommandTool preserves the existing Command-to-CommandResult contract.\"\"\"\n\n    async def exercise() -> None:\n        tool: Tool[Command, CommandResult] = CommandTool(CommandExecutor())\n        command = Command(sys.executable, (\"-c\", \"print('tool command')\"))\n\n        result: CommandResult = await ToolRunner().execute(tool, command)\n\n        assert tool.name == \"run_command\"\n        assert tool.description\n        assert result.command is command\n        assert result.stdout.strip() == b\"tool command\"\n\n    asyncio.run(exercise())\n\n\ndef test_command_tool_preserves_nonzero_exit_as_result() -> None:\n    \"\"\"A nonzero process exit remains a CommandResult rather than Tool failure.\"\"\"\n\n    async def exercise() -> None:\n        command = Command(\n            sys.executable,\n            (\"-c\", f\"import sys; sys.exit({_NONZERO_EXIT_CODE})\"),\n        )\n        result = await ToolRunner().execute(CommandTool(CommandExecutor()), command)\n\n        assert isinstance(result, CommandResult)\n        assert result.exit_code == _NONZERO_EXIT_CODE\n        assert result.failed is True\n\n    asyncio.run(exercise())\n",
        "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "start": 458,
        "start_line": 25
      }
    ]
  },
  {
    "address": "tests/tools/test_command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O4@5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "inferability_state": "INFERABLE_SUPPORT",
    "label": "REQUIRED",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O4",
    "rationale": "Necessary in at least one minimal complete witness as support for R07. Public command execution through the transparent Tool bridge propagates all three exceptional outcomes; no completed return is available.",
    "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "support_spans": [
      {
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "end": 3569,
        "end_line": 120,
        "quote": "def test_command_tool_propagates_missing_command_error(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Command lookup failures remain owned by Commands.\"\"\"\n\n    async def raise_not_found(*_args: object, **_kwargs: object) -> None:\n        raise FileNotFoundError\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        raise_not_found,\n    )\n\n    with pytest.raises(CommandNotFoundError):\n        asyncio.run(\n            ToolRunner().execute(CommandTool(CommandExecutor()), Command(\"missing\")),\n        )\n\n\ndef test_command_tool_propagates_command_timeout() -> None:\n    \"\"\"Command timeout policy passes through the Tool bridge unchanged.\"\"\"\n    command = Command(\n        sys.executable,\n        (\"-c\", \"import time; time.sleep(1)\"),\n        timeout=Duration.seconds(0.001),\n    )\n\n    with pytest.raises(CommandTimeoutError):\n        asyncio.run(ToolRunner().execute(CommandTool(CommandExecutor()), command))\n\n\ndef test_command_tool_cancellation_preserves_command_cleanup(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation through CommandTool retains immediate-child cleanup.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def exercise() -> None:\n        operation = asyncio.create_task(\n            ToolRunner().execute(\n                CommandTool(CommandExecutor()),\n                Command(\"blocking-command\"),\n            ),\n        )\n        await process.read_started.wait()\n        operation.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await operation\n\n    asyncio.run(exercise())\n\n    assert process.killed is True\n    assert process.waited is True\n",
        "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "start": 1649,
        "start_line": 59
      }
    ]
  },
  {
    "address": "tests/tools/test_command.py",
    "identity": "case-0014-command-result-diagnostics-v1/O6@5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "inferability_state": "CORROBORATION_ONLY",
    "label": "HELPFUL_ONLY",
    "obligation_identity": "case-0014-command-result-diagnostics-v1/O6",
    "rationale": "Useful exception propagation examples; future renderer regressions need not edit Tool integration tests.",
    "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
    "support_spans": [
      {
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "end": 3569,
        "end_line": 120,
        "quote": "def test_command_tool_propagates_missing_command_error(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Command lookup failures remain owned by Commands.\"\"\"\n\n    async def raise_not_found(*_args: object, **_kwargs: object) -> None:\n        raise FileNotFoundError\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        raise_not_found,\n    )\n\n    with pytest.raises(CommandNotFoundError):\n        asyncio.run(\n            ToolRunner().execute(CommandTool(CommandExecutor()), Command(\"missing\")),\n        )\n\n\ndef test_command_tool_propagates_command_timeout() -> None:\n    \"\"\"Command timeout policy passes through the Tool bridge unchanged.\"\"\"\n    command = Command(\n        sys.executable,\n        (\"-c\", \"import time; time.sleep(1)\"),\n        timeout=Duration.seconds(0.001),\n    )\n\n    with pytest.raises(CommandTimeoutError):\n        asyncio.run(ToolRunner().execute(CommandTool(CommandExecutor()), command))\n\n\ndef test_command_tool_cancellation_preserves_command_cleanup(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation through CommandTool retains immediate-child cleanup.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def exercise() -> None:\n        operation = asyncio.create_task(\n            ToolRunner().execute(\n                CommandTool(CommandExecutor()),\n                Command(\"blocking-command\"),\n            ),\n        )\n        await process.read_started.wait()\n        operation.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await operation\n\n    asyncio.run(exercise())\n\n    assert process.killed is True\n    assert process.waited is True\n",
        "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "start": 1649,
        "start_line": 59
      }
    ]
  }
]
```

## All semantic units and exact support alternatives/spans

```json
[
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T01",
    "obligations": [
      1,
      5
    ],
    "statement": "The new renderer is opt-in human-readable presentation of an already completed result in the commands domain.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 137,
        "quote": "Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 0
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T02",
    "obligations": [
      1,
      5
    ],
    "statement": "Rendering is pure: no execution, shell invocation, retry, or input mutation.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 416,
        "quote": "Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 310
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T03",
    "obligations": [
      1
    ],
    "statement": "Preserve structured executable/arguments, exit_code, duration and succeeded/failed meaning; a nonzero exit remains ordinary completion.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 309,
        "quote": "Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 143
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T04",
    "obligations": [
      2
    ],
    "statement": "Render stdout and stderr as separately labeled diagnostic excerpts.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 499,
        "quote": "Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 422
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T05",
    "obligations": [
      2
    ],
    "statement": "Decode invalid or incomplete UTF-8 with explicit replacement and disclose decoding loss separately.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 637,
        "quote": "Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 537
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T06",
    "obligations": [
      2
    ],
    "statement": "Preserve original stream bytes and distinguish decoded diagnostic text from original bytes.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 701,
        "quote": "Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 500
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T07",
    "obligations": [
      3
    ],
    "statement": "Each stream has a caller-configurable nonnegative character limit, default 2048.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 815,
        "quote": "Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 707
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T08",
    "obligations": [
      3
    ],
    "statement": "Display a leading decoded prefix and disclose omitted characters, including informative zero-limit output.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1079,
        "quote": "Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 816
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T09",
    "obligations": [
      3
    ],
    "statement": "Display omission must be distinguished from byte retention and existing per-stream truncation flags.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1011,
        "quote": "Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 892
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T10",
    "obligations": [
      4
    ],
    "statement": "Preserve and display events_dropped independently of output truncation.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1158,
        "quote": "Preserve and display `events_dropped` independently of output truncation.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1085
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T11",
    "obligations": [
      4
    ],
    "statement": "Never reconstruct event interleaving or fabricate missing events.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1225,
        "quote": "Do not reconstruct event interleaving or fabricate missing events.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1159
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T12",
    "obligations": [
      4
    ],
    "statement": "Accept only existing completed results; do not synthesize results for timeout, cancellation, or executable-not-found.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1375,
        "quote": "Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1226
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T13",
    "obligations": [
      5
    ],
    "statement": "Provide a small explicit public API through the commands package facade.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1470,
        "quote": "Provide a small explicit public API through `src/devtools/resources/commands/__init__.py`",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1381
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T14",
    "obligations": [
      1,
      5
    ],
    "statement": "The same input and display policy produce deterministic output.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1514,
        "quote": "with deterministic output, immutable inputs",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1471
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T15",
    "obligations": [
      5
    ],
    "statement": "Document the decoding and display policies.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1554,
        "quote": "documented decoding/display policy.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1519
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T16",
    "obligations": [
      5
    ],
    "statement": "Presentation belongs to commands and adds none of the prohibited infrastructure or redaction claims.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 1714,
        "quote": "Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1555
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T17",
    "obligations": [
      6
    ],
    "statement": "Add controlled commands tests covering success/nonzero, empty and valid/invalid/incomplete UTF-8 output, zero/default/custom display bounds, independent retention flags, event loss, determinism and immutability.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 2052,
        "quote": "Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1720
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T18",
    "obligations": [
      6
    ],
    "statement": "Update commands package documentation for the specified behavior and edge cases.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 2052,
        "quote": "update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 1779
      }
    ]
  },
  {
    "evidence_class": "TASK_BACKED",
    "identity": "T19",
    "obligations": [
      6
    ],
    "statement": "Preserve the protected development validation profile.",
    "support_alternatives": [],
    "task_evidence": [
      {
        "end": 2154,
        "quote": "Preserve the protected development validation profile documented in `docs/development/validation.md`.",
        "source_identity": "case-0014-command-result-diagnostics-v1",
        "start": 2053
      }
    ]
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R01",
    "obligations": [
      1,
      5
    ],
    "statement": "Command is an immutable structured value with separate executable and ordered argument tuple.",
    "support_alternatives": [
      {
        "identity": "R01/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Direct public value contract.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 981,
            "end_line": 31,
            "quote": "## `Command`\n\n```python\nCommand(\n    executable: str,\n    arguments: tuple[str, ...] = (),\n    working_directory: ResolvedPath | None = None,\n    timeout: Duration | None = None,\n)\n```\n\n`Command` is a frozen, slotted value object. Blank executables are invalid.\nThe executable and arguments remain separate; no shell parsing, interpolation,\nor quoting occurs. `argv` returns the complete tuple passed to process launch.\n\nAll fluent methods return new values:\n\n```text\nargs(...)             append arguments\nwith_args(...)        replace arguments\nwithout_args()        clear arguments\nwith_executable(...)  replace and validate executable\ncwd(...)              set ResolvedPath working directory\nwithout_cwd()         clear working directory\nwith_timeout(...)     set Duration timeout\nwithout_timeout()     clear timeout\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 160,
            "start_line": 6
          }
        ]
      },
      {
        "identity": "R01/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Frozen dataclass fields, specification contract and argv implementation.",
        "resources": [
          "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629"
        ],
        "support_spans": [
          {
            "content_identity": "b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473",
            "end": 1816,
            "end_line": 62,
            "quote": "@dataclass(frozen=True, slots=True)\nclass Command:\n    \"\"\"Describe an immutable command execution specification.\n\n    A command identifies an executable separately from its arguments and does\n    not imply shell parsing, interpolation, or quoting.\n\n    Fluent methods return new command instances and never mutate the original.\n\n    Example::\n\n        command = (\n            Command(\"uv\")\n            .args(\"run\", \"pytest\", \"-q\")\n            .cwd(project_root)\n            .with_timeout(Duration.minutes(2))\n        )\n\n    :ivar executable: Executable name or path.\n    :ivar arguments: Ordered executable arguments.\n    :ivar working_directory: Optional resolved working directory.\n    :ivar timeout: Optional maximum execution duration.\n    \"\"\"\n\n    executable: str\n    arguments: tuple[str, ...] = ()\n    working_directory: ResolvedPath | None = None\n    timeout: Duration | None = None\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate command invariants.\"\"\"\n        self._validate()\n\n    def _validate(self) -> None:\n        \"\"\"Validate the command specification.\n\n        :raises ValueError: If the executable is empty or whitespace-only.\n        \"\"\"\n        if not self.executable.strip():\n            msg = \"Command executable cannot be empty.\"\n            raise ValueError(msg)\n\n    @property\n    def argv(self) -> tuple[str, ...]:\n        \"\"\"Return the complete process argument vector.\n\n        :returns: Executable followed by all ordered arguments.\n        \"\"\"\n        return (self.executable, *self.arguments)\n",
            "resource_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
            "start": 283,
            "start_line": 14
          }
        ]
      },
      {
        "identity": "R01/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Explicit structured-value and frozen-input tests establish the intended public contract.",
        "resources": [
          "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4"
        ],
        "support_spans": [
          {
            "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
            "end": 2914,
            "end_line": 84,
            "quote": "def test_command_preserves_separate_executable_arguments_and_options(\n    tmp_path: Path,\n) -> None:\n    \"\"\"Commands retain structured process arguments and optional execution data.\"\"\"\n    command = Command(\n        executable=\"python\",\n        arguments=(\"-c\", \"print('hello')\"),\n        working_directory=ResolvedPath(tmp_path),\n        timeout=Duration.seconds(3),\n    )\n\n    assert command.executable == \"python\"\n    assert command.arguments == (\"-c\", \"print('hello')\")\n    assert command.working_directory == ResolvedPath(tmp_path)\n    assert command.timeout == Duration.seconds(3)\n    assert command.argv == (\"python\", \"-c\", \"print('hello')\")\n\n\ndef test_command_defaults_to_no_arguments_and_is_immutable() -> None:\n    \"\"\"Commands have an empty argument tuple and frozen value semantics.\"\"\"\n    command = Command(\"python\")\n    attribute = \"executable\"\n\n    assert command.arguments == ()\n    assert command == Command(\"python\")\n    assert hash(command) == hash(Command(\"python\"))\n\n    with pytest.raises(FrozenInstanceError):\n        setattr(command, attribute, \"other\")\n\n\ndef test_command_fluent_methods_are_immutable_and_composable(tmp_path: Path) -> None:\n    \"\"\"Fluent command methods preserve unrelated immutable specification data.\"\"\"\n    original = (\n        Command(\"python\", (\"-m\",))\n        .cwd(ResolvedPath(tmp_path))\n        .with_timeout(Duration.seconds(1))\n    )\n    appended = original.args(\"pytest\", \"-q\")\n    replaced = appended.with_args(\"-c\", \"pass\")\n    cleared = replaced.without_args()\n    renamed = cleared.with_executable(\"python3\")\n    without_cwd = renamed.without_cwd()\n    without_timeout = without_cwd.without_timeout()\n\n    assert original == Command(\n        \"python\",\n        (\"-m\",),\n        ResolvedPath(tmp_path),\n        Duration.seconds(1),\n    )\n    assert appended.arguments == (\"-m\", \"pytest\", \"-q\")\n    assert replaced.arguments == (\"-c\", \"pass\")\n    assert cleared.arguments == ()\n    assert cleared.working_directory == ResolvedPath(tmp_path)\n    assert cleared.timeout == Duration.seconds(1)\n    assert renamed.executable == \"python3\"\n    assert renamed.working_directory == ResolvedPath(tmp_path)\n    assert renamed.timeout == Duration.seconds(1)\n    assert without_cwd.working_directory is None\n    assert without_cwd.timeout == Duration.seconds(1)\n    assert without_timeout.timeout is None\n    assert without_timeout.executable == \"python3\"\n\n    with pytest.raises(ValueError, match=\"cannot be empty\"):\n        renamed.with_executable(\"   \")\n",
            "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
            "start": 416,
            "start_line": 19
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R02",
    "obligations": [
      1
    ],
    "statement": "A completed result retains command, exit_code and duration; succeeded is zero exit and failed is nonzero, which is ordinary completion.",
    "support_alternatives": [
      {
        "identity": "R02/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Constructor and exact status prose.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 2115,
            "end_line": 71,
            "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n\nExit code zero means `succeeded`; every nonzero exit code means `failed` but is\nstill a completed result. Timeout, cancellation, process-creation failure, and\nother execution exceptions produce no `CommandResult`.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1424,
            "start_line": 49
          }
        ]
      },
      {
        "identity": "R02/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Fields and status predicates directly establish the contract.",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "support_spans": [
          {
            "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
            "end": 1729,
            "end_line": 55,
            "quote": "@dataclass(frozen=True, slots=True)\nclass CommandResult:\n    \"\"\"Represent the completed result of a command execution.\n\n    A nonzero exit code is a valid command result and does not itself represent\n    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`\n    when interpreting the command's exit status.\n\n    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n\n    @property\n    def succeeded(self) -> bool:\n        \"\"\"Return whether the command exited successfully.\n\n        :returns: ``True`` when the exit code is zero.\n        \"\"\"\n        return self.exit_code == 0\n\n    @property\n    def failed(self) -> bool:\n        \"\"\"Return whether the command exited unsuccessfully.\n\n        :returns: ``True`` when the exit code is nonzero.\n        \"\"\"\n        return not self.succeeded\n",
            "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
            "start": 274,
            "start_line": 14
          }
        ]
      },
      {
        "identity": "R02/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "The test explicitly describes nonzero completion and asserts preserved fields and both complementary status values.",
        "resources": [
          "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4"
        ],
        "support_spans": [
          {
            "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
            "end": 4184,
            "end_line": 120,
            "quote": "def test_command_result_preserves_bytes_and_exit_status() -> None:\n    \"\"\"Nonzero exit codes remain ordinary completed command results.\"\"\"\n    command = Command(\"python\")\n    expected_exit_code = 3\n    successful = CommandResult(command, 0, b\"out\", b\"\", Duration.seconds(1))\n    failed = CommandResult(\n        command,\n        expected_exit_code,\n        b\"\",\n        b\"error\",\n        Duration.seconds(2),\n    )\n\n    assert successful.command is command\n    assert successful.stdout == b\"out\"\n    assert successful.stderr == b\"\"\n    assert successful.duration == Duration.seconds(1)\n    assert successful.stdout_truncated is False\n    assert successful.stderr_truncated is False\n    assert successful.events_dropped == 0\n    assert successful.succeeded is True\n    assert successful.failed is False\n    assert failed.exit_code == expected_exit_code\n    assert failed.stdout == b\"\"\n    assert failed.stderr == b\"error\"\n    assert failed.succeeded is False\n    assert failed.failed is True\n",
            "resource_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
            "start": 3194,
            "start_line": 94
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R03",
    "obligations": [
      2
    ],
    "statement": "Result stdout and stderr are separate raw byte values holding retained leading prefixes, which may be incomplete process output.",
    "support_alternatives": [
      {
        "identity": "R03/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Direct result representation and retained-prefix prose.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 1900,
            "end_line": 67,
            "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1424,
            "start_line": 49
          }
        ]
      },
      {
        "identity": "R03/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Explicit independent leading result-prefix retention.",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "support_spans": [
          {
            "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
            "end": 1758,
            "end_line": 53,
            "quote": "## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
            "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
            "start": 1272,
            "start_line": 45
          }
        ]
      },
      {
        "identity": "R03/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Both streams are bounded independently, converted to bytes and assigned to their result fields.",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "support_spans": [
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 4806,
            "end_line": 160,
            "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 4487,
            "start_line": 152
          },
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 9512,
            "end_line": 303,
            "quote": "    async def _stream_process(\n        self,\n        process: asyncio.subprocess.Process,\n        execution: CommandExecution,\n        output_policy: CommandOutputPolicy,\n    ) -> tuple[bytes, bytes, bool, bool]:\n        \"\"\"Stream subprocess output while retaining bounded output prefixes.\n\n        Process streams are fully drained during normal completion. Returned\n        bytes contain only the leading prefix retained by the output policy.\n\n        :param process: Running subprocess.\n        :param execution: Live execution receiving events.\n        :returns: Complete stdout and stderr byte sequences.\n        \"\"\"\n        if process.stdout is None or process.stderr is None:\n            msg = \"Command subprocess streams were not created.\"\n            raise CommandError(msg)\n\n        stdout_task = asyncio.create_task(\n            self._read_stream(\n                process.stdout,\n                execution._emit,  # noqa: SLF001\n                CommandStdout,\n                output_policy.max_stdout_bytes,\n            ),\n        )\n        stderr_task = asyncio.create_task(\n            self._read_stream(\n                process.stderr,\n                execution._emit,  # noqa: SLF001\n                CommandStderr,\n                output_policy.max_stderr_bytes,\n            ),\n        )\n\n        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(\n            stdout_task,\n            stderr_task,\n        )\n\n        await process.wait()\n\n        return stdout, stderr, stdout_truncated, stderr_truncated\n\n    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 7245,
            "start_line": 236
          }
        ]
      },
      {
        "identity": "R03/A4",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Field types and retained-leading-byte documentation.",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "support_spans": [
          {
            "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
            "end": 1308,
            "end_line": 39,
            "quote": "    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
            "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
            "start": 604,
            "start_line": 22
          }
        ]
      },
      {
        "identity": "R03/A5",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Known byte chunks yield exact retained prefixes in each result stream, including zero retention.",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "support_spans": [
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 7968,
            "end_line": 265,
            "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 5617,
            "start_line": 190
          },
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 12084,
            "end_line": 408,
            "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 10744,
            "start_line": 366
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R04",
    "obligations": [
      3
    ],
    "statement": "CommandOutputPolicy bounds retained output independently per stream in bytes, separately from a renderer character limit.",
    "support_alternatives": [
      {
        "identity": "R04/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Independent byte limits and zero-retention behavior are documented.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 1423,
            "end_line": 47,
            "quote": "## `CommandOutputPolicy`\n\n```python\nCommandOutputPolicy(\n    max_stdout_bytes=1_048_576,\n    max_stderr_bytes=1_048_576,\n    max_pending_events=1_024,\n)\n```\n\nStdout and stderr retention limits are independent. A zero byte limit is valid:\nnonempty output remains streamable but no bytes are retained in the final\nresult, and the matching truncation flag is true. Negative byte limits are\ninvalid. Pending-event capacity must be positive.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 986,
            "start_line": 34
          }
        ]
      },
      {
        "identity": "R04/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Independent output prefixes and retention bounds are documented.",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "support_spans": [
          {
            "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
            "end": 1758,
            "end_line": 53,
            "quote": "## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
            "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
            "start": 1272,
            "start_line": 45
          }
        ]
      },
      {
        "identity": "R04/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Separate policy byte fields govern the bytearray prefixes.",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "support_spans": [
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 9512,
            "end_line": 303,
            "quote": "    async def _stream_process(\n        self,\n        process: asyncio.subprocess.Process,\n        execution: CommandExecution,\n        output_policy: CommandOutputPolicy,\n    ) -> tuple[bytes, bytes, bool, bool]:\n        \"\"\"Stream subprocess output while retaining bounded output prefixes.\n\n        Process streams are fully drained during normal completion. Returned\n        bytes contain only the leading prefix retained by the output policy.\n\n        :param process: Running subprocess.\n        :param execution: Live execution receiving events.\n        :returns: Complete stdout and stderr byte sequences.\n        \"\"\"\n        if process.stdout is None or process.stderr is None:\n            msg = \"Command subprocess streams were not created.\"\n            raise CommandError(msg)\n\n        stdout_task = asyncio.create_task(\n            self._read_stream(\n                process.stdout,\n                execution._emit,  # noqa: SLF001\n                CommandStdout,\n                output_policy.max_stdout_bytes,\n            ),\n        )\n        stderr_task = asyncio.create_task(\n            self._read_stream(\n                process.stderr,\n                execution._emit,  # noqa: SLF001\n                CommandStderr,\n                output_policy.max_stderr_bytes,\n            ),\n        )\n\n        (stdout, stdout_truncated), (stderr, stderr_truncated) = await asyncio.gather(\n            stdout_task,\n            stderr_task,\n        )\n\n        await process.wait()\n\n        return stdout, stderr, stdout_truncated, stderr_truncated\n\n    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 7245,
            "start_line": 236
          }
        ]
      },
      {
        "identity": "R04/A4",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Policy contract and distinct per-stream byte fields.",
        "resources": [
          "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d"
        ],
        "support_spans": [
          {
            "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
            "end": 1323,
            "end_line": 37,
            "quote": "@dataclass(frozen=True, slots=True)\nclass CommandOutputPolicy:\n    \"\"\"Bound memory retained for one command execution.\n\n    Output limits apply independently to standard output and standard error.\n    Event buffering is best effort: any newly emitted event is dropped when the\n    pending event limit is reached so process draining never waits for a\n    consumer. No event type is privileged.\n\n    :ivar max_stdout_bytes: Maximum stdout bytes retained in a result.\n    :ivar max_stderr_bytes: Maximum stderr bytes retained in a result.\n    :ivar max_pending_events: Maximum events awaiting the single consumer.\n    \"\"\"\n\n    max_stdout_bytes: int = 1_048_576\n    max_stderr_bytes: int = 1_048_576\n    max_pending_events: int = 1_024\n\n    def __post_init__(self) -> None:\n        \"\"\"Validate output-retention invariants.\"\"\"\n        if self.max_stdout_bytes < 0:\n            msg = \"Maximum stdout bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_stderr_bytes < 0:\n            msg = \"Maximum stderr bytes cannot be negative.\"\n            raise ValueError(msg)\n\n        if self.max_pending_events <= 0:\n            msg = \"Maximum pending events must be positive.\"\n            raise ValueError(msg)\n",
            "resource_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
            "start": 97,
            "start_line": 7
          }
        ]
      },
      {
        "identity": "R04/A5",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Different byte limits and zero retention are controlled and asserted independently.",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "support_spans": [
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 7968,
            "end_line": 265,
            "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 5617,
            "start_line": 190
          },
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 12084,
            "end_line": 408,
            "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 10744,
            "start_line": 366
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R05",
    "obligations": [
      3
    ],
    "statement": "stdout_truncated and stderr_truncated report bytes omitted by retention, including when retained bytes are empty under a zero bound.",
    "support_alternatives": [
      {
        "identity": "R05/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Explicit zero-byte and per-stream truncation contract.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 1900,
            "end_line": 67,
            "quote": "Stdout and stderr retention limits are independent. A zero byte limit is valid:\nnonempty output remains streamable but no bytes are retained in the final\nresult, and the matching truncation flag is true. Negative byte limits are\ninvalid. Pending-event capacity must be positive.\n\n## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1144,
            "start_line": 44
          }
        ]
      },
      {
        "identity": "R05/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Omitted retained bytes set corresponding flags.",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "support_spans": [
          {
            "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
            "end": 1758,
            "end_line": 53,
            "quote": "## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
            "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
            "start": 1272,
            "start_line": 45
          }
        ]
      },
      {
        "identity": "R05/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "A flag becomes true when a chunk exceeds remaining retention; named fields receive the flags.",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "support_spans": [
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 4806,
            "end_line": 160,
            "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 4487,
            "start_line": 152
          },
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 9512,
            "end_line": 303,
            "quote": "    async def _read_stream(\n        self,\n        stream: asyncio.StreamReader,\n        emit: Callable[[CommandEvent], None],\n        event_type: type[CommandStdout | CommandStderr],\n        max_output_bytes: int,\n    ) -> tuple[bytes, bool]:\n        \"\"\"Read, emit, and retain bounded chunks from one subprocess stream.\"\"\"\n        output = bytearray()\n        truncated = False\n\n        while chunk := await stream.read(8192):\n            remaining = max_output_bytes - len(output)\n\n            if remaining > 0:\n                output.extend(chunk[:remaining])\n\n            if len(chunk) > remaining:\n                truncated = True\n\n            emit(event_type(data=chunk))\n\n        return bytes(output), truncated\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 8794,
            "start_line": 281
          }
        ]
      },
      {
        "identity": "R05/A4",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Each named flag means its stream exceeded retained limit; zero-limit consequence follows from that definition.",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "support_spans": [
          {
            "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
            "end": 1280,
            "end_line": 38,
            "quote": "    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n",
            "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
            "start": 690,
            "start_line": 24
          }
        ]
      },
      {
        "identity": "R05/A5",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Assertions connect bounded and zero-byte retention to each flag.",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "support_spans": [
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 7968,
            "end_line": 265,
            "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 5617,
            "start_line": 190
          },
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 12084,
            "end_line": 408,
            "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 10744,
            "start_line": 366
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R06",
    "obligations": [
      4
    ],
    "statement": "events_dropped is the numeric count of omitted buffered events, distinct from retained-output truncation.",
    "support_alternatives": [
      {
        "identity": "R06/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Distinct result fields and explicit bounded-queue-loss meaning.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 1900,
            "end_line": 67,
            "quote": "## `CommandResult`\n\n```python\nCommandResult(\n    command,\n    exit_code,\n    stdout,\n    stderr,\n    duration,\n    stdout_truncated=False,\n    stderr_truncated=False,\n    events_dropped=0,\n)\n```\n\nResults are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1424,
            "start_line": 49
          }
        ]
      },
      {
        "identity": "R06/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Explicit event count, best-effort queue loss and independent retained output.",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "support_spans": [
          {
            "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
            "end": 1758,
            "end_line": 53,
            "quote": "Ordering within stdout and within stderr is preserved. Interleaving between the\ntwo streams is not guaranteed.\n\n## `events()`\n\n`execution.events()` is a single-consumer async stream. The claim occurs when\niteration begins; a second consumer attempt raises `RuntimeError`. Streams\nclose on normal completion, missing executable, timeout, cancellation, and\nunexpected stream-read failure.\n\n## Bounded queue and drop policy\n\nThe pending queue is bounded by `CommandOutputPolicy.max_pending_events`.\nProducers never block when full: any newly emitted event is dropped, and\n`events_dropped` records the total. No event type is privileged, so\n`CommandExited` may be dropped under pressure. Event delivery is best effort.\n\n## Event bytes versus result bytes\n\nProcess streams are read in bounded chunks and fully drained during normal\ncompletion. Result retention independently stores only the leading stdout and\nstderr prefixes allowed by the output policy. Bytes beyond a limit are omitted\nfrom `CommandResult` and set the corresponding truncation flag.\n\nAn output event may therefore contain bytes that are absent from final retained\nresult output. Queue buffering and result retention are separate bounds.\n",
            "resource_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
            "start": 556,
            "start_line": 28
          }
        ]
      },
      {
        "identity": "R06/A3",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Separate numeric omission count and retained-output flag meanings.",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "support_spans": [
          {
            "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
            "end": 1308,
            "end_line": 39,
            "quote": "    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
            "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
            "start": 690,
            "start_line": 24
          }
        ]
      },
      {
        "identity": "R06/A4",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "The handle counts dropped events; execution copies that count into the result independently of output flags.",
        "resources": [
          "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "support_spans": [
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 5073,
            "end_line": 169,
            "quote": "            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n\n            execution._emit(  # noqa: SLF001\n                CommandExited(\n                    exit_code=exit_code,\n                    duration=duration,\n                ),\n            )\n\n            return replace(result, events_dropped=execution.events_dropped)\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 4487,
            "start_line": 152
          },
          {
            "content_identity": "c9825687577803f98911494be5c86ddd84af006d627acdbacbc2b28d9c82b06c",
            "end": 3938,
            "end_line": 133,
            "quote": "    @property\n    def events_dropped(self) -> int:\n        \"\"\"Return the number of events omitted by bounded buffering.\n\n        Any newly emitted event may be dropped while the queue is full; no event\n        type, including lifecycle events, is privileged.\n\n        :returns: Number of events dropped before observation.\n        \"\"\"\n        return self._events_dropped\n\n    async def events(self) -> AsyncIterator[CommandEvent]:\n        \"\"\"Yield structured events emitted by the execution.\n\n        Only one consumer may iterate the event stream for a given execution.\n\n        :yields: Command execution events.\n        :raises RuntimeError: If the event stream has already been claimed.\n        \"\"\"\n        if self._events_claimed:\n            msg = \"Command execution events may only be consumed once.\"\n            raise RuntimeError(msg)\n\n        self._events_claimed = True\n\n        while True:\n            try:\n                event = self._event_queue.get_nowait()\n            except asyncio.QueueEmpty:\n                if self._events_closed:\n                    return\n\n                await self._event_available.wait()\n                self._event_available.clear()\n                continue\n\n            yield event\n\n    def _emit(self, event: CommandEvent) -> None:\n        \"\"\"Emit an execution event when bounded queue capacity permits it.\n\n        :param event: Event to emit.\n        \"\"\"\n        try:\n            self._event_queue.put_nowait(event)\n        except asyncio.QueueFull:\n            self._events_dropped += 1\n            return\n\n        self._event_available.set()\n\n    def _close_events(self) -> None:\n        \"\"\"Close the execution event stream.\"\"\"\n        self._events_closed = True\n        self._event_available.set()\n",
            "resource_identity": "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
            "start": 2188,
            "start_line": 79
          }
        ]
      },
      {
        "identity": "R06/A5",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Independent queue capacity and stream limits produce a numeric omission count; lost exit event demonstrates results are not complete transcripts.",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "support_spans": [
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 7968,
            "end_line": 265,
            "quote": "def test_executor_bounds_retained_output_and_pending_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Configured limits truncate retained bytes and drop excess queued events.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=3,\n                max_stderr_bytes=2,\n                max_pending_events=1,\n            ),\n        )\n        execution = executor.start(Command(\"bounded-output-command\"))\n        result = await execution\n        events = [event async for event in execution.events()]\n\n        assert result.stdout == b\"abc\"\n        assert result.stderr == b\"wx\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        expected_dropped_events = 4\n\n        assert result.events_dropped == expected_dropped_events\n        assert len(events) == 1\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    asyncio.run(run())\n\n\ndef test_executor_allows_zero_output_retention_while_streaming(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Zero limits retain no bytes but do not prevent normal completion.\"\"\"\n    process = _OutputProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _OutputProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def run() -> None:\n        executor = CommandExecutor(\n            output_policy=CommandOutputPolicy(\n                max_stdout_bytes=0,\n                max_stderr_bytes=0,\n                max_pending_events=10,\n            ),\n        )\n        result = await executor.execute(Command(\"zero-retention-command\"))\n\n        assert result.stdout == b\"\"\n        assert result.stderr == b\"\"\n        assert result.stdout_truncated is True\n        assert result.stderr_truncated is True\n        assert result.succeeded is True\n\n    asyncio.run(run())\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 5617,
            "start_line": 190
          },
          {
            "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
            "end": 12084,
            "end_line": 408,
            "quote": "class _OutputProcess:\n    \"\"\"Minimal completed process producing output beyond configured bounds.\"\"\"\n\n    def __init__(self) -> None:\n        \"\"\"Initialize deterministic output streams and completion state.\"\"\"\n        self.returncode: int | None = None\n        self.stderr = _ChunkStream((b\"wxyz\",))\n        self.stdout = _ChunkStream((b\"abc\", b\"def\"))\n\n    async def wait(self) -> None:\n        \"\"\"Mark the process as successfully completed.\"\"\"\n        self.returncode = 0\n\n\nclass _EmptyStream:\n    \"\"\"Minimal stream fake that is immediately exhausted.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return end-of-stream bytes.\"\"\"\n        return b\"\"\n\n\nclass _TimeoutStream:\n    \"\"\"Minimal stream fake that reports a deterministic timeout.\"\"\"\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Raise the timeout handled by the executor lifecycle.\"\"\"\n        raise TimeoutError\n\n\nclass _ChunkStream:\n    \"\"\"Minimal stream fake that returns a fixed sequence of chunks.\"\"\"\n\n    def __init__(self, chunks: tuple[bytes, ...]) -> None:\n        \"\"\"Initialize the remaining chunk sequence.\"\"\"\n        self._chunks = list(chunks)\n\n    async def read(self, _size: int) -> bytes:\n        \"\"\"Return the next chunk or end-of-stream bytes.\"\"\"\n        if not self._chunks:\n            return b\"\"\n\n        return self._chunks.pop(0)\n",
            "resource_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
            "start": 10744,
            "start_line": 366
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R07",
    "obligations": [
      4
    ],
    "statement": "Timeout, cancellation and missing executable propagate exceptional outcomes and produce no completed CommandResult.",
    "support_alternatives": [
      {
        "identity": "R07/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Explicit no-result boundary.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 2115,
            "end_line": 71,
            "quote": "Exit code zero means `succeeded`; every nonzero exit code means `failed` but is\nstill a completed result. Timeout, cancellation, process-creation failure, and\nother execution exceptions produce no `CommandResult`.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1901,
            "start_line": 69
          }
        ]
      },
      {
        "identity": "R07/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Lifecycle documentation covers all three exceptional outcomes.",
        "resources": [
          "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b"
        ],
        "support_spans": [
          {
            "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
            "end": 2062,
            "end_line": 55,
            "quote": "## Process creation\n\nExecution uses `asyncio.create_subprocess_exec()` with direct argv, optional\nnative cwd, and stdout/stderr pipes. There is no shell, stdin, environment\noverride, or process-group configuration.\n\nIf creation raises `FileNotFoundError`, it becomes `CommandNotFoundError` with\nthe original error retained as its cause. No started event or result is\nproduced, and the event stream closes.\n\n## Timeout\n\n`Duration.total_seconds` configures an asyncio timeout around post-creation\noutput collection. Process creation time is not included.\n\nOn timeout, the running immediate child is killed and awaited/reaped,\n`CommandTimeoutError` is raised with the timeout failure as its cause, and the\nevent stream closes. No `CommandExited` or final result is fabricated. Events\nalready observed may remain available, but partial retained output is not\nexposed through a result.\n\n## Cancellation\n\nBefore child creation completes, cancellation closes the stream and propagates.\nAfter creation, a running immediate child is killed and awaited/reaped;\ncancellation then propagates unchanged and no exit event is fabricated. An\nalready-exited child is awaited without another kill.\n\nAwaiters directly await the same task. Cancelling one awaiter can therefore\ncancel the shared command execution for all awaiters.\n",
            "resource_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
            "start": 751,
            "start_line": 26
          }
        ]
      },
      {
        "identity": "R07/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "All three failure paths raise before the successful result construction branch.",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "support_spans": [
          {
            "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
            "end": 6340,
            "end_line": 207,
            "quote": "    async def _run(\n        self,\n        command: Command,\n        execution: CommandExecution,\n    ) -> CommandResult:\n        \"\"\"Run one command execution.\n\n        :param command: Command to execute.\n        :param execution: Live execution receiving emitted events.\n        :returns: Completed command result.\n        :raises CommandNotFoundError: If the executable cannot be found.\n        :raises CommandTimeoutError: If execution exceeds its timeout.\n        :raises CommandError: If the process completes without an exit code.\n        \"\"\"\n        stopwatch = Stopwatch()\n        process: asyncio.subprocess.Process | None = None\n\n        try:\n            process = await self._create_process(command)\n\n            execution._emit(CommandStarted(command=command))  # noqa: SLF001\n\n            try:\n                (\n                    stdout,\n                    stderr,\n                    stdout_truncated,\n                    stderr_truncated,\n                ) = await self._collect_output(\n                    process,\n                    execution,\n                    command,\n                )\n            except TimeoutError as error:\n                await self._terminate_and_reap(process)\n                process = None\n\n                timeout = command.timeout\n\n                if timeout is None:\n                    msg = \"Command timed out without a configured timeout.\"\n                    raise CommandError(msg) from error\n\n                msg = (\n                    f\"Command exceeded timeout of \"\n                    f\"{timeout.total_seconds} seconds: \"\n                    f\"{command.executable!r}.\"\n                )\n                raise CommandTimeoutError(msg) from error\n\n        except asyncio.CancelledError:\n            if process is not None:\n                await self._terminate_and_reap(process)\n\n            raise\n        except (CommandNotFoundError, CommandTimeoutError):\n            raise\n        except Exception:\n            if process is not None:\n                await self._terminate_and_reap(process)\n\n            raise\n\n        else:\n            duration = stopwatch.stop()\n            exit_code = process.returncode\n\n            if exit_code is None:\n                msg = (\n                    \"Command process completed without an exit code: \"\n                    f\"{command.executable!r}.\"\n                )\n                raise CommandError(msg)\n\n            result = CommandResult(\n                command=command,\n                exit_code=exit_code,\n                stdout=stdout,\n                stderr=stderr,\n                duration=duration,\n                stdout_truncated=stdout_truncated,\n                stderr_truncated=stderr_truncated,\n            )\n\n            execution._emit(  # noqa: SLF001\n                CommandExited(\n                    exit_code=exit_code,\n                    duration=duration,\n                ),\n            )\n\n            return replace(result, events_dropped=execution.events_dropped)\n        finally:\n            stopwatch.stop()\n            execution._close_events()  # noqa: SLF001\n\n    async def _terminate_and_reap(\n        self,\n        process: asyncio.subprocess.Process,\n    ) -> None:\n        \"\"\"Terminate and reap a running immediate child process.\"\"\"\n        if process.returncode is None:\n            process.kill()\n\n        await process.wait()\n\n    async def _create_process(\n        self,\n        command: Command,\n    ) -> asyncio.subprocess.Process:\n        \"\"\"Create the subprocess for a command.\n\n        :param command: Command to execute.\n        :returns: Running subprocess.\n        :raises CommandNotFoundError: If the executable cannot be found.\n        \"\"\"\n        try:\n            return await asyncio.create_subprocess_exec(\n                *command.argv,\n                cwd=(\n                    command.working_directory.value\n                    if command.working_directory is not None\n                    else None\n                ),\n                stdout=asyncio.subprocess.PIPE,\n                stderr=asyncio.subprocess.PIPE,\n            )\n        except FileNotFoundError as error:\n            msg = f\"Command executable not found: {command.executable!r}.\"\n            raise CommandNotFoundError(msg) from error\n",
            "resource_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
            "start": 2079,
            "start_line": 78
          }
        ]
      },
      {
        "identity": "R07/A4",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Controlled awaited executions raise all three exceptions instead of returning results.",
        "resources": [
          "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43"
        ],
        "support_spans": [
          {
            "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
            "end": 5763,
            "end_line": 196,
            "quote": "def test_missing_executable_closes_the_event_stream(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Failure during process creation does not leave event consumers waiting.\"\"\"\n\n    async def raise_not_found(*_args: object, **_kwargs: object) -> None:\n        raise FileNotFoundError\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"missing-command\"))\n        events = [event async for event in execution.events()]\n\n        assert events == []\n\n        with pytest.raises(CommandNotFoundError):\n            await execution\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        raise_not_found,\n    )\n    asyncio.run(run())\n\n\ndef test_timeout_closes_the_event_stream(monkeypatch: pytest.MonkeyPatch) -> None:\n    \"\"\"Timeout cleanup closes event iteration before propagating the error.\"\"\"\n    process = _TimedOutProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _TimedOutProcess:\n        return process\n\n    async def run() -> None:\n        execution = CommandExecutor().start(\n            Command(\"slow-command\", timeout=Duration.seconds(0.001)),\n        )\n        events = [event async for event in execution.events()]\n\n        assert len(events) == 1\n        assert isinstance(events[0], CommandStarted)\n\n        with pytest.raises(CommandTimeoutError):\n            await execution\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n\n\ndef test_cancellation_kills_reaps_and_closes_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancelling a live execution cleans up its immediate child process.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _BlockingProcess:\n        return process\n\n    async def await_execution(execution: CommandExecution) -> None:\n        \"\"\"Await one execution so caller cancellation reaches its task.\"\"\"\n        await execution\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"blocking-command\"))\n        events_task = asyncio.create_task(_collect_events(execution))\n        awaiter = asyncio.create_task(await_execution(execution))\n        shared_awaiter = asyncio.create_task(await_execution(execution))\n\n        await process.stdout.read_started.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        with pytest.raises(asyncio.CancelledError):\n            await shared_awaiter\n\n        events = await events_task\n\n        assert process.killed is True\n        assert process.waited is True\n        assert any(isinstance(event, CommandStarted) for event in events)\n        assert not any(isinstance(event, CommandExited) for event in events)\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n",
            "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
            "start": 2682,
            "start_line": 101
          },
          {
            "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
            "end": 9137,
            "end_line": 301,
            "quote": "def test_cancellation_before_process_creation_closes_events(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation while creating a process still closes its event stream.\"\"\"\n    process_creation_started = asyncio.Event()\n    process_creation_release = asyncio.Event()\n\n    async def create_process(*_args: object, **_kwargs: object) -> None:\n        process_creation_started.set()\n        await process_creation_release.wait()\n\n    async def await_execution(\n        execution: CommandExecution,\n        awaiting_execution: asyncio.Event,\n    ) -> None:\n        \"\"\"Await an execution after reporting that cancellation can propagate.\"\"\"\n        awaiting_execution.set()\n        await execution\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"creating-command\"))\n        events_task = asyncio.create_task(_collect_events(execution))\n        awaiting_execution = asyncio.Event()\n        awaiter = asyncio.create_task(await_execution(execution, awaiting_execution))\n\n        await process_creation_started.wait()\n        await awaiting_execution.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        assert await events_task == []\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n\n\ndef test_cancellation_reaps_an_already_exited_process(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation reaps a child without killing it after it has exited.\"\"\"\n    process = _BlockingProcess(returncode=0)\n\n    async def create_process(\n        *_args: object,\n        **_kwargs: object,\n    ) -> _BlockingProcess:\n        return process\n\n    async def run() -> None:\n        execution = CommandExecutor().start(Command(\"completed-command\"))\n        awaiter = asyncio.ensure_future(execution)\n\n        await process.stdout.read_started.wait()\n        awaiter.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await awaiter\n\n        assert process.killed is False\n        assert process.waited is True\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n    asyncio.run(run())\n",
            "resource_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
            "start": 6831,
            "start_line": 231
          }
        ]
      },
      {
        "identity": "R07/A5",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Public command execution through the transparent Tool bridge propagates all three exceptional outcomes; no completed return is available.",
        "resources": [
          "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535"
        ],
        "support_spans": [
          {
            "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
            "end": 3569,
            "end_line": 120,
            "quote": "def test_command_tool_propagates_missing_command_error(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Command lookup failures remain owned by Commands.\"\"\"\n\n    async def raise_not_found(*_args: object, **_kwargs: object) -> None:\n        raise FileNotFoundError\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        raise_not_found,\n    )\n\n    with pytest.raises(CommandNotFoundError):\n        asyncio.run(\n            ToolRunner().execute(CommandTool(CommandExecutor()), Command(\"missing\")),\n        )\n\n\ndef test_command_tool_propagates_command_timeout() -> None:\n    \"\"\"Command timeout policy passes through the Tool bridge unchanged.\"\"\"\n    command = Command(\n        sys.executable,\n        (\"-c\", \"import time; time.sleep(1)\"),\n        timeout=Duration.seconds(0.001),\n    )\n\n    with pytest.raises(CommandTimeoutError):\n        asyncio.run(ToolRunner().execute(CommandTool(CommandExecutor()), command))\n\n\ndef test_command_tool_cancellation_preserves_command_cleanup(\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"Cancellation through CommandTool retains immediate-child cleanup.\"\"\"\n    process = _BlockingProcess()\n\n    async def create_process(*_args: object, **_kwargs: object) -> _BlockingProcess:\n        return process\n\n    monkeypatch.setattr(\n        \"devtools.resources.commands.execution.asyncio.create_subprocess_exec\",\n        create_process,\n    )\n\n    async def exercise() -> None:\n        operation = asyncio.create_task(\n            ToolRunner().execute(\n                CommandTool(CommandExecutor()),\n                Command(\"blocking-command\"),\n            ),\n        )\n        await process.read_started.wait()\n        operation.cancel()\n\n        with pytest.raises(asyncio.CancelledError):\n            await operation\n\n    asyncio.run(exercise())\n\n    assert process.killed is True\n    assert process.waited is True\n",
            "resource_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
            "start": 1649,
            "start_line": 59
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R08",
    "obligations": [
      5
    ],
    "statement": "The commands public facade explicitly exposes Command, CommandResult, CommandOutputPolicy, executor/handle, event union and values, and command errors.",
    "support_alternatives": [
      {
        "identity": "R08/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Exact current imports and __all__.",
        "resources": [
          "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3"
        ],
        "support_spans": [
          {
            "content_identity": "7cbc6f6b95697b5c664eb09d2779fe854fedb8d868e046e913bed2ce2fbb30b3",
            "end": 889,
            "end_line": 38,
            "quote": "from devtools.resources.commands.errors import (\n    CommandError,\n    CommandNotFoundError,\n    CommandTimeoutError,\n)\nfrom devtools.resources.commands.events import (\n    CommandEvent,\n    CommandExited,\n    CommandStarted,\n    CommandStderr,\n    CommandStdout,\n)\nfrom devtools.resources.commands.execution import CommandExecutor\nfrom devtools.resources.commands.handle import CommandExecution\nfrom devtools.resources.commands.models import (\n    Command,\n    CommandOutputPolicy,\n    CommandResult,\n)\n\n__all__ = [\n    \"Command\",\n    \"CommandError\",\n    \"CommandEvent\",\n    \"CommandExecution\",\n    \"CommandExecutor\",\n    \"CommandExited\",\n    \"CommandNotFoundError\",\n    \"CommandOutputPolicy\",\n    \"CommandResult\",\n    \"CommandStarted\",\n    \"CommandStderr\",\n    \"CommandStdout\",\n    \"CommandTimeoutError\",\n]\n",
            "resource_identity": "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
            "start": 80,
            "start_line": 4
          }
        ]
      },
      {
        "identity": "R08/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Independent public API documentation names the complete current export surface.",
        "resources": [
          "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961"
        ],
        "support_spans": [
          {
            "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
            "end": 1460,
            "end_line": 38,
            "quote": "## Public API\n\n```python\nfrom devtools.resources.commands import (\n    Command,\n    CommandError,\n    CommandEvent,\n    CommandExecution,\n    CommandExecutor,\n    CommandExited,\n    CommandNotFoundError,\n    CommandOutputPolicy,\n    CommandResult,\n    CommandStarted,\n    CommandStderr,\n    CommandStdout,\n    CommandTimeoutError,\n)\n```\n\n| Group              | API                                                                                 |\n|--------------------|-------------------------------------------------------------------------------------|\n| Specification      | `Command`                                                                           |\n| Execution          | `CommandExecutor`, `CommandExecution`                                               |\n| Events             | `CommandEvent`, `CommandStarted`, `CommandStdout`, `CommandStderr`, `CommandExited` |\n| Results and policy | `CommandResult`, `CommandOutputPolicy`                                              |\n| Errors             | `CommandError`, `CommandNotFoundError`, `CommandTimeoutError`                       |\n\n`CommandEvent` is a type alias for the concrete event values, not a runtime\nevent superclass.\n",
            "resource_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
            "start": 264,
            "start_line": 9
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R09",
    "obligations": [
      5
    ],
    "statement": "CommandResult is an immutable frozen value object, permitting presentation without changing retained input state.",
    "support_alternatives": [
      {
        "identity": "R09/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Explicit frozen-result contract.",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "support_spans": [
          {
            "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
            "end": 1900,
            "end_line": 67,
            "quote": "Results are frozen value objects. Stdout/stderr remain bytes and contain only\nthe retained leading prefix allowed by the policy; they are not necessarily the\ncomplete process output. Truncation flags report omitted retained bytes, and\n`events_dropped` reports bounded-queue loss.\n",
            "resource_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
            "start": 1620,
            "start_line": 64
          }
        ]
      },
      {
        "identity": "R09/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Frozen dataclass declaration and immutable-valued fields.",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "support_spans": [
          {
            "content_identity": "9bccad0fff2036c7f3059bbd3a449d51ec0faf8093d393dc48a105dae0b3fc23",
            "end": 1308,
            "end_line": 39,
            "quote": "@dataclass(frozen=True, slots=True)\nclass CommandResult:\n    \"\"\"Represent the completed result of a command execution.\n\n    A nonzero exit code is a valid command result and does not itself represent\n    an execution error. Callers may inspect :attr:`succeeded` or :attr:`failed`\n    when interpreting the command's exit status.\n\n    :ivar command: Command that was executed.\n    :ivar exit_code: Process exit code.\n    :ivar stdout: Retained leading bytes written to standard output.\n    :ivar stderr: Retained leading bytes written to standard error.\n    :ivar duration: Monotonic elapsed execution duration.\n    :ivar stdout_truncated: Whether stdout exceeded the retained limit.\n    :ivar stderr_truncated: Whether stderr exceeded the retained limit.\n    :ivar events_dropped: Number of events omitted by bounded buffering.\n    \"\"\"\n\n    command: Command\n    exit_code: int\n    stdout: bytes\n    stderr: bytes\n    duration: Duration\n    stdout_truncated: bool = False\n    stderr_truncated: bool = False\n    events_dropped: int = 0\n",
            "resource_identity": "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
            "start": 274,
            "start_line": 14
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R10",
    "obligations": [
      6
    ],
    "statement": "The protected ordinary-development entry point selects tests while excluding tests/experiments before collection.",
    "support_alternatives": [
      {
        "identity": "R10/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Operating guide explicitly supplies invocation and precollection exclusion.",
        "resources": [
          "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
        ],
        "support_spans": [
          {
            "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
            "end": 11282,
            "end_line": 239,
            "quote": "The canonical protected development test profile is documented in\n[docs/development/validation.md](docs/development/validation.md). Run it with:\n\n```text\nuv run python scripts/validate_development.py\n```\n\nIt excludes `tests/experiments/` before collection to avoid retained\noutcome-dependent tests. Keep the configured production branch-coverage gate.\nRun Ruff, formatting, mypy, and diff checks separately as documented. Do not\nrun confirmation validation or live model/Docker tests for ordinary work;\nthose require explicit authorization and are reported separately.\n",
            "resource_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
            "start": 10713,
            "start_line": 228
          }
        ]
      },
      {
        "identity": "R10/A2",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Entry-point arguments select tests with the experiment directory ignored.",
        "resources": [
          "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a"
        ],
        "support_spans": [
          {
            "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
            "end": 715,
            "end_line": 27,
            "quote": "def pytest_arguments(repository_root: Path = REPOSITORY_ROOT) -> list[str]:\n    \"\"\"Select ordinary tests while excluding the retained experiment tree.\"\"\"\n    tests = repository_root / \"tests\"\n    experiments = tests / \"experiments\"\n    return [str(tests), f\"--ignore={experiments}\"]\n\n\ndef main() -> int:\n    \"\"\"Run pytest and return its exit code unchanged.\"\"\"\n    return int(pytest.main(pytest_arguments()))\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n",
            "resource_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
            "start": 248,
            "start_line": 14
          }
        ]
      },
      {
        "identity": "R10/A3",
        "kind": "INFERABLE_SUPPORT",
        "rationale": "Independent contract tests assert the exact directory exclusion and unchanged pytest outcome.",
        "resources": [
          "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986"
        ],
        "support_spans": [
          {
            "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
            "end": 1503,
            "end_line": 48,
            "quote": "_SCRIPT_PATH = Path(\"scripts/validate_development.py\")\n\n\n@pytest.fixture\ndef validation_script() -> ModuleType:\n    \"\"\"Load the operational script without making scripts a library package.\"\"\"\n    specification = importlib.util.spec_from_file_location(\n        \"test_validate_development_script\",\n        _SCRIPT_PATH,\n    )\n    assert specification is not None\n    assert specification.loader is not None\n    module = importlib.util.module_from_spec(specification)\n    sys.modules[specification.name] = module\n    specification.loader.exec_module(module)\n    return module\n\n\ndef test_profile_selects_tests_and_excludes_experiment_tests_before_collection(\n    validation_script: ModuleType,\n) -> None:\n    \"\"\"The directory boundary covers the whole retained experiment population.\"\"\"\n    arguments = validation_script.pytest_arguments(Path.cwd())\n    tests = Path(arguments[0])\n    ignored = Path(arguments[1].removeprefix(\"--ignore=\"))\n\n    assert tests == Path.cwd() / \"tests\"\n    assert ignored == tests / \"experiments\"\n    assert tests.is_dir()\n    assert ignored.is_dir()\n    assert (tests / \"context\").is_dir()\n    assert (tests / \"scripts\" / \"test_validate_development.py\").is_file()\n",
            "resource_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
            "start": 313,
            "start_line": 17
          },
          {
            "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
            "end": 2104,
            "end_line": 68,
            "quote": "def test_profile_propagates_pytest_failure_code(\n    validation_script: ModuleType,\n    monkeypatch: pytest.MonkeyPatch,\n) -> None:\n    \"\"\"A failed pytest run remains a failed profile invocation.\"\"\"\n    observed_arguments: list[str] | None = None\n\n    def failed_pytest(arguments: list[str]) -> int:\n        nonlocal observed_arguments\n        observed_arguments = arguments\n        return 1\n\n    monkeypatch.setattr(validation_script.pytest, \"main\", failed_pytest)\n\n    result = validation_script.main()\n\n    assert result == 1\n    assert observed_arguments == validation_script.pytest_arguments()\n",
            "resource_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
            "start": 1505,
            "start_line": 51
          }
        ]
      }
    ],
    "task_evidence": []
  },
  {
    "evidence_class": "REPOSITORY_SUPPORTED",
    "identity": "R11",
    "obligations": [
      6
    ],
    "statement": "Configured development checks retain strict pytest configuration/markers, devtools branch coverage at 100 percent, Ruff rules and strict mypy settings.",
    "support_alternatives": [
      {
        "identity": "R11/A1",
        "kind": "DIRECT_SUPPORT",
        "rationale": "Actual pytest, coverage, lint and type-checking configuration; this is not a synthetic fixture.",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
        ],
        "support_spans": [
          {
            "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
            "end": 1368,
            "end_line": 78,
            "quote": "[tool.pytest.ini_options]\ntestpaths = [\"tests\"]\naddopts = [\n    \"--strict-config\",\n    \"--strict-markers\",\n    \"--cov=devtools\",\n    \"--cov-branch\",\n    \"--cov-report=term-missing\",\n    \"--cov-fail-under=100\",\n]\nmarkers = [\n    \"live_codex: opt-in test that contacts the locally authenticated Codex CLI\",\n]\n\n[tool.coverage.run]\nbranch = true\nsource = [\"devtools\"]\n\n[tool.coverage.report]\nshow_missing = true\nskip_covered = false\nfail_under = 100\n\n[tool.ruff]\ntarget-version = \"py312\"\nline-length = 88\n\n[tool.ruff.lint]\nselect = [\"ALL\"]\nignore = [\n    \"D203\",\n    \"D213\",\n]\n\n[tool.ruff.lint.per-file-ignores]\n\"tests/**/*.py\" = [\n    \"S101\",\n]\n\n[tool.mypy]\npython_version = \"3.12\"\nstrict = true\nfiles = [\"src\", \"tests\", \"experiments\"]\nexplicit_package_bases = true\nmypy_path = [\"src\"]\n",
            "resource_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
            "start": 585,
            "start_line": 34
          }
        ]
      }
    ],
    "task_evidence": []
  }
]
```

## All witnesses and obligation intersections

```json
[
  {
    "indispensable_resources": [],
    "indispensable_units": [
      "R01",
      "R02",
      "T01",
      "T02",
      "T03",
      "T14"
    ],
    "obligation": "O1",
    "witnesses": [
      {
        "identity": "O1/W001",
        "resources": [
          "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4"
        ],
        "unit_support": {
          "R01": [
            "R01/A3"
          ],
          "R02": [
            "R02/A3"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T03",
          "T14",
          "R01",
          "R02"
        ]
      },
      {
        "identity": "O1/W002",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R01": [
            "R01/A1"
          ],
          "R02": [
            "R02/A1"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T03",
          "T14",
          "R01",
          "R02"
        ]
      },
      {
        "identity": "O1/W003",
        "resources": [
          "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R01": [
            "R01/A2"
          ],
          "R02": [
            "R02/A2"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T03",
          "T14",
          "R01",
          "R02"
        ]
      }
    ]
  },
  {
    "indispensable_resources": [],
    "indispensable_units": [
      "R03",
      "T04",
      "T05",
      "T06"
    ],
    "obligation": "O2",
    "witnesses": [
      {
        "identity": "O2/W001",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R03": [
            "R03/A4"
          ]
        },
        "units": [
          "T04",
          "T05",
          "T06",
          "R03"
        ]
      },
      {
        "identity": "O2/W002",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "unit_support": {
          "R03": [
            "R03/A5"
          ]
        },
        "units": [
          "T04",
          "T05",
          "T06",
          "R03"
        ]
      },
      {
        "identity": "O2/W003",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "unit_support": {
          "R03": [
            "R03/A2"
          ]
        },
        "units": [
          "T04",
          "T05",
          "T06",
          "R03"
        ]
      },
      {
        "identity": "O2/W004",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R03": [
            "R03/A1"
          ]
        },
        "units": [
          "T04",
          "T05",
          "T06",
          "R03"
        ]
      },
      {
        "identity": "O2/W005",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R03": [
            "R03/A3"
          ]
        },
        "units": [
          "T04",
          "T05",
          "T06",
          "R03"
        ]
      }
    ]
  },
  {
    "indispensable_resources": [],
    "indispensable_units": [
      "R04",
      "R05",
      "T07",
      "T08",
      "T09"
    ],
    "obligation": "O3",
    "witnesses": [
      {
        "identity": "O3/W001",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "unit_support": {
          "R04": [
            "R04/A5"
          ],
          "R05": [
            "R05/A5"
          ]
        },
        "units": [
          "T07",
          "T08",
          "T09",
          "R04",
          "R05"
        ]
      },
      {
        "identity": "O3/W002",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "unit_support": {
          "R04": [
            "R04/A2"
          ],
          "R05": [
            "R05/A2"
          ]
        },
        "units": [
          "T07",
          "T08",
          "T09",
          "R04",
          "R05"
        ]
      },
      {
        "identity": "O3/W003",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R04": [
            "R04/A1"
          ],
          "R05": [
            "R05/A1"
          ]
        },
        "units": [
          "T07",
          "T08",
          "T09",
          "R04",
          "R05"
        ]
      },
      {
        "identity": "O3/W004",
        "resources": [
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R04": [
            "R04/A3"
          ],
          "R05": [
            "R05/A3"
          ]
        },
        "units": [
          "T07",
          "T08",
          "T09",
          "R04",
          "R05"
        ]
      },
      {
        "identity": "O3/W005",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
          "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d"
        ],
        "unit_support": {
          "R04": [
            "R04/A4"
          ],
          "R05": [
            "R05/A4"
          ]
        },
        "units": [
          "T07",
          "T08",
          "T09",
          "R04",
          "R05"
        ]
      }
    ]
  },
  {
    "indispensable_resources": [],
    "indispensable_units": [
      "R06",
      "R07",
      "T10",
      "T11",
      "T12"
    ],
    "obligation": "O4",
    "witnesses": [
      {
        "identity": "O4/W001",
        "resources": [
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R06": [
            "R06/A1"
          ],
          "R07": [
            "R07/A1"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W002",
        "resources": [
          "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R06": [
            "R06/A3"
          ],
          "R07": [
            "R07/A4"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W003",
        "resources": [
          "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "unit_support": {
          "R06": [
            "R06/A5"
          ],
          "R07": [
            "R07/A4"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W004",
        "resources": [
          "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "unit_support": {
          "R06": [
            "R06/A2"
          ],
          "R07": [
            "R07/A4"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W005",
        "resources": [
          "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R06": [
            "R06/A3"
          ],
          "R07": [
            "R07/A2"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W006",
        "resources": [
          "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "unit_support": {
          "R06": [
            "R06/A5"
          ],
          "R07": [
            "R07/A2"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W007",
        "resources": [
          "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "unit_support": {
          "R06": [
            "R06/A2"
          ],
          "R07": [
            "R07/A2"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W008",
        "resources": [
          "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R06": [
            "R06/A3"
          ],
          "R07": [
            "R07/A5"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W009",
        "resources": [
          "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a"
        ],
        "unit_support": {
          "R06": [
            "R06/A5"
          ],
          "R07": [
            "R07/A5"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W010",
        "resources": [
          "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
        ],
        "unit_support": {
          "R06": [
            "R06/A2"
          ],
          "R07": [
            "R07/A5"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W011",
        "resources": [
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R06": [
            "R06/A3"
          ],
          "R07": [
            "R07/A3"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W012",
        "resources": [
          "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R06": [
            "R06/A5"
          ],
          "R07": [
            "R07/A3"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W013",
        "resources": [
          "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R06": [
            "R06/A2"
          ],
          "R07": [
            "R07/A3"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      },
      {
        "identity": "O4/W014",
        "resources": [
          "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
          "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3"
        ],
        "unit_support": {
          "R06": [
            "R06/A4"
          ],
          "R07": [
            "R07/A3"
          ]
        },
        "units": [
          "T10",
          "T11",
          "T12",
          "R06",
          "R07"
        ]
      }
    ]
  },
  {
    "indispensable_resources": [],
    "indispensable_units": [
      "R01",
      "R08",
      "R09",
      "T01",
      "T02",
      "T13",
      "T14",
      "T15",
      "T16"
    ],
    "obligation": "O5",
    "witnesses": [
      {
        "identity": "O5/W001",
        "resources": [
          "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R01": [
            "R01/A1"
          ],
          "R08": [
            "R08/A2"
          ],
          "R09": [
            "R09/A1"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      },
      {
        "identity": "O5/W002",
        "resources": [
          "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
          "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
        ],
        "unit_support": {
          "R01": [
            "R01/A1"
          ],
          "R08": [
            "R08/A1"
          ],
          "R09": [
            "R09/A1"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      },
      {
        "identity": "O5/W003",
        "resources": [
          "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
          "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R01": [
            "R01/A2"
          ],
          "R08": [
            "R08/A2"
          ],
          "R09": [
            "R09/A2"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      },
      {
        "identity": "O5/W004",
        "resources": [
          "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
          "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5"
        ],
        "unit_support": {
          "R01": [
            "R01/A2"
          ],
          "R08": [
            "R08/A1"
          ],
          "R09": [
            "R09/A2"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      },
      {
        "identity": "O5/W005",
        "resources": [
          "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
          "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4"
        ],
        "unit_support": {
          "R01": [
            "R01/A3"
          ],
          "R08": [
            "R08/A2"
          ],
          "R09": [
            "R09/A2"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      },
      {
        "identity": "O5/W006",
        "resources": [
          "45ed3ca574f3a37d0b201658f08519780497a055514089b5472d333e681307e3",
          "5c9a097a9474c219327ace49c64493f9c6776f912391f770f077eeace63857c5",
          "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4"
        ],
        "unit_support": {
          "R01": [
            "R01/A3"
          ],
          "R08": [
            "R08/A1"
          ],
          "R09": [
            "R09/A2"
          ]
        },
        "units": [
          "T01",
          "T02",
          "T13",
          "T14",
          "T15",
          "T16",
          "R01",
          "R08",
          "R09"
        ]
      }
    ]
  },
  {
    "indispensable_resources": [
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
    ],
    "indispensable_units": [
      "R10",
      "R11",
      "T17",
      "T18",
      "T19"
    ],
    "obligation": "O6",
    "witnesses": [
      {
        "identity": "O6/W001",
        "resources": [
          "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0"
        ],
        "unit_support": {
          "R10": [
            "R10/A2"
          ],
          "R11": [
            "R11/A1"
          ]
        },
        "units": [
          "T17",
          "T18",
          "T19",
          "R10",
          "R11"
        ]
      },
      {
        "identity": "O6/W002",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
          "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d"
        ],
        "unit_support": {
          "R10": [
            "R10/A1"
          ],
          "R11": [
            "R11/A1"
          ]
        },
        "units": [
          "T17",
          "T18",
          "T19",
          "R10",
          "R11"
        ]
      },
      {
        "identity": "O6/W003",
        "resources": [
          "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
          "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986"
        ],
        "unit_support": {
          "R10": [
            "R10/A3"
          ],
          "R11": [
            "R11/A1"
          ]
        },
        "units": [
          "T17",
          "T18",
          "T19",
          "R10",
          "R11"
        ]
      }
    ]
  }
]
```

## All gaps

```json
{
  "REPOSITORY_INFORMATION_GAP": {
    "items": [],
    "rationale": "Retained source, public documentation, controlled contract tests and actual validation configuration establish the necessary current facts. The absent validation prose is bounded explicitly below; no additional necessary missing fact was identified.",
    "status": "NONE"
  },
  "TASK_GAP": {
    "items": [],
    "rationale": "The objective and required behavior are sufficiently specified; unresolved presentation choices do not prevent a compliant implementation.",
    "status": "NONE"
  },
  "TASK_INTERPRETATION_GAP": {
    "items": [],
    "rationale": "All substantive task clauses, including the preamble, are represented by the six mandatory obligations and the audited units.",
    "status": "NONE"
  }
}
```

## All limitations

```json
[
  {
    "blocking": false,
    "evidence_basis": "Exact sealed resource address frame; AGENTS.md lines 228-239; scripts/validate_development.py lines 14-27; tests/scripts/test_validate_development.py lines 35-68; pyproject.toml lines 34-78.",
    "identity": "L01",
    "statement": "The retained 515-resource frame omits docs/development/validation.md. Its exact prose and any additional instructions cannot be asserted. The observable protected profile is established by AGENTS.md, the entry point, its contract tests, and pyproject.toml; no claim of byte-level documentation completeness is made."
  },
  {
    "blocking": false,
    "evidence_basis": "Inspection method and sealed packet scope.",
    "identity": "L02",
    "statement": "Repository contracts are adjudicated from retained text. No devtools module was imported and no repository feature tests or live commands were executed. Contract-bearing tests are evidence of intended behavior, not a new execution result."
  },
  {
    "blocking": false,
    "evidence_basis": "Task O2-O4; commands/docs/command.md lines 44-71; commands/docs/events.md lines 45-53.",
    "identity": "L03",
    "statement": "The renderer cannot recover bytes omitted by retention or dropped events. A retained prefix may end inside UTF-8; replacement decoding discloses local decoding loss without asserting the original complete stream was invalid."
  },
  {
    "blocking": false,
    "evidence_basis": "src/devtools/resources/commands/execution.py lines 242-249 and 281-303.",
    "identity": "L04",
    "statement": "execution.py has a stale return-description line calling output complete, while its immediately preceding prose, implementation and other contracts establish retained prefixes. The specific implementation and consistent bounded-retention contract control this reading."
  }
]
```

## Preserved design freedom

```json
[
  {
    "identity": "A01",
    "resolution": "Preserved as nonblocking design freedom.",
    "statement": "Public helper name, exact text layout, separators, status wording and duration presentation remain open if deterministic, human-readable and faithful to the structured values."
  },
  {
    "identity": "A02",
    "resolution": "Do not impose a terminal-width or grapheme dependency as necessary evidence.",
    "statement": "Character limit is a decoded-text bound, not a byte bound. Python Unicode character counting is a defensible implementation; the task does not specify terminal columns or grapheme-cluster measurement."
  },
  {
    "identity": "A03",
    "resolution": "Preserve policy choice while requiring explicit replacement decoding and truthful independent loss disclosure.",
    "statement": "The exact decoding-loss disclosure format and limit argument type/error policy are unspecified. A genuine U+FFFD in valid UTF-8 must not itself be treated as proof of replacement loss."
  }
]
```

All 18,900 combinations, 2,850 sufficient resource unions, 126 inclusion-minimal union identities and the sufficient unit union are owned by reviewed_gold.json: primary.task_sufficiency. Their structures are unchanged from the sealed primary.
