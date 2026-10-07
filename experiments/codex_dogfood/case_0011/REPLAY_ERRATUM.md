# Stage B replay ordering erratum

All 28 frozen queries executed exactly once. The original run published every
capture and hash before its terminal verifier reported a trace-order mismatch.
Canonical JSON sorts object keys; the original overlap-pair builder iterated
those keys on replay rather than using the frozen query sequence. This changed
pair orientation/order, not any query, resource, rank, score, membership or cost.

`replay.py` retains every original verification check and restores the frozen
query sequence only when deriving the overlap trace from decoded captures.
No retrieval is rerun. No Stage A or captured Stage B artifact is overwritten.
The original implementation remains committed and hash-bound at the Stage A
checkpoint; its original verify command still reproduces the diagnostic failure.
The corrected post-capture verifier is separately committed at Stage B.

Focused validation retains the original failure as a regression check, prohibits
native retrieval during corrected replay, and checks all score evidence, trace,
Markdown and blind packet integrity. This is a serialization/replay repair,
not a treatment change or a gold/effectiveness conclusion.
