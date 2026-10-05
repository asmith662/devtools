# Case 0008 Stage B Attempt 1

**PARTIAL STAGE B — NOT CANONICAL**
**GENERATION NOT CAPTURED**
**NOT ADJUDICATED**

Execution `2fed596a-f43d-4d35-9e32-e8a609366a6f` completed lexical acquisition once, routing once, all 11 distinct frozen grounding requests once each, and bound all 29 frozen generation specifications.

The combined generation API was entered once and did not return. It raised `ValueError: Routing view differs from its native association inputs.` during the initial `build_candidate_witness_view` consistency validation in `generate_witness_hypotheses` (`src/devtools/context/localization/generation/generate.py`, called into `src/devtools/context/localization/association/hypothesis.py`). No structural projection was reached: no fixed projection outcome, Reference projection, Import projection, hypothesis, or candidate target was produced.

The observed cause was a harness object-binding defect. The resumed harness supplied `WitnessGenerationPlan.role_evidence` from the equivalent but distinct frozen native role-evidence object. Production requires it to be the same instance retained in the captured routing view. Production semantics and identity checks remain unchanged.

The raw partial capture remains authoritative and unchanged at SHA-256 `3c2cdf45a72d470e2f8c38a6d99f2940add6a9546e5177a8d0dca13f7de6765d`; the start marker remains unchanged at `e4f202319a2e3920ee997966112f71ef04dc59310a5185a2b64148db2c90c7e8`. The earlier module-attribute lookup error occurred before lexical production function entry and did not return a treatment result. A grounding result that had been durably flushed to a temporary checkpoint was promoted after a Windows replacement error without reinvoking grounding.

This is not a grounding, operator, Reference, Import, candidate-hypothesis, or effectiveness result. There are no canonical Stage B artifacts. The only authorization frozen alongside this record permits one additional combined generation API call against the unchanged Stage A treatment and captured upstream values. If that call fails before returning, generation must not be called again and Case 0008 is `CAPTURE_FAILED`.
