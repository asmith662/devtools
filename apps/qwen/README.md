# Bounded local coding worker

Maintained repository-local application composition now lives here. The existing
worker, native proposal admission, LF/CRLF handling, task configuration and
host-owned validation were relocated without changing their contracts. Framework
Context/RI, ModelInteraction, Tools, managed commands and filesystem primitives
remain in `src/devtools`. Legacy fixture helpers remain because the existing
patch-proposal CLI and deterministic acceptance still consume them; they are not
a generic Agent API.

`scripts/qwen/coding_worker.py` remains the genuine default-No terminal entrypoint.
No local inference is authorized by consolidation. Historical Markdown and source
segment task definitions pin their original Git baselines; they are reproducible
evaluation definitions, not unresolved current defects. Complete evidence and
outcomes remain in `experiments/qwen/` and `.local/qwen-coding-worker/`.

The first task was accepted and its exact Markdown correction integrated; the
second task failed and received a separately attributed Codex production repair.
B-0048 is a separate accepted candidate, not integrated source. WorkCycle/delegation/integration now uses the canonical checkout and ordinary
branches under exclusive recoverable ownership. The worker applies only the
admitted source file in place, captures the candidate, and restores original
bytes; it never copies the repository or src tree. Validation binds imports to
the exact selected source. Historical task definitions require selecting their
actual baseline branch rather than substituting old bytes under a current HEAD. Old grants
are historical and cannot be reused at this new coordinator path.
