# B-0007 — Correct model-serving documentation drift

- type: STORY
- status: IMPLEMENTED
- decision_maturity: READY_FOR_IMPLEMENTATION
- necessity: REQUIRED
- architectural_significance: SUPPORTING
- urgency: NOW
- evidence_basis: REAL_USE
- scope: llama.cpp GGUF file-mount documentation correction
- primary_domain: models
- supporting_domains: documentation
- parent: B-0001

## Resolved

`models.serving` documents the validated local GGUF file-mount contract: the
caller-visible semantic artifact path identifies the file, Docker mounts its
resolved host backing file read-only at a semantic container filename, and
`--model` uses that same container path. The prior parent-directory wording is
no longer current guidance.

- related: B-0001, B-0006
- validation_level: INTEGRATION
