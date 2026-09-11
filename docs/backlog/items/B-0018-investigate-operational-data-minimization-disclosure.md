# B-0018 — Investigate operational-data minimization and disclosure

- type: INVESTIGATION
- status: DEFERRED
- decision_maturity: DISCOVERED
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: operational data from observability, diagnostics, model interaction, tools, and repository access
- parent: none

## Problem / value

Investigate collection, disclosure, retention, export, redaction, bounded
diagnostics, and sensitive-payload handling for source code, prompts, model
responses, tool/action arguments and results, paths, repository metadata,
provider payloads, exceptions, credentials/secrets, authorization/governance
information, context payloads, traces, metrics, audit records, and durable
Evidence.

## Current evidence / invariants

Terminal Evidence already minimizes payload collection. Prefer minimizing
collection before relying on downstream redaction. Permission to report that an
occurrence happened does not authorize disclosure of all associated payload.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: B-0008, B-0013, B-0017, B-0023, B-0024
- operational_dependencies: concrete diagnostic, observability, or harness payload
- consumers: future diagnostics, live validation, and governed harnesses
- established_invariants: bounded diagnostics and data minimization are existing local practices
- unresolved_semantics: collection, disclosure, retention, export, redaction, bounded diagnostics, privacy/sensitive payloads, provider payloads, and authority boundaries
- risk_if_deferred: useful diagnostics may overcollect or overdisclose operational data
- risk_if_implemented_early: classification framework, redaction engine, telemetry policy, secret scanner, or retention subsystem
- promotion_trigger: a real harness needs to retain or export sensitive operational evidence
- validation_level: NONE
- live_validation_trigger: live evidence includes payload whose collection/disclosure boundary matters
- first_harness_consumer: Local coding worker / Qwen
- second_harness_trigger: another harness requires equivalent minimization semantics
- related: B-0008, B-0013, B-0016, B-0017, B-0023, B-0024
