# B-0007 — Correct model-serving documentation drift

- type: STORY
- status: ACTIVE
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: SUPPORTING
- urgency: NOW
- evidence_basis: REAL_USE
- scope: authoritative model-serving documentation only
- parent: B-0001

## Problem / value

Correct obsolete llama.cpp documentation that described a parent-directory model
mount. Live snapshot/blob behavior established the implemented file-mount contract.

## Established invariants

The public GGUF path retains semantic identity. Docker resolves the host backing
file, mounts it read-only at a semantic container filename, and passes that same
path to --model.

## Dependencies / risks / validation

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: committed llama.cpp mount behavior
- consumers: model-serving operators
- unresolved_semantics: none for this bounded correction
- risk_if_deferred: operators follow obsolete topology
- risk_if_implemented_early: none; behavior is already validated
- promotion_trigger: documentation review and commit
- validation_level: INTEGRATION
- live_validation_trigger: not applicable; implemented behavior is documented
- related: B-0001, B-0006
