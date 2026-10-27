# Operational turns

This is application-owned implementation of the bounded Qwen coding worker.
Callers continue to use `apps.qwen.coding_loop.run_coding_task` and its existing
preflight/acquisition/validation functions. `coding_loop` retains the task
lifecycle, candidate archive, source restoration and terminal outcome accounting.
It supplies its existing concrete acquisition/check/feedback adapters to
`run_turns`; the private `_turns` delegation seam remains for maintained callers.

- `loop.py` sequences prepared/native requests, source/response admission, edits,
  validation and repair under the existing limits. History, counters, ContextTools,
  CodingCommands and optional NativeObligations remain local to one invocation.
- `prompt.py` builds the original initial host instructions and fits native input
  using actual llama.cpp token measurements. `continuation` still owns selection
  and source presentation; `obligations` still owns its application readiness
  composition. Projection does not generate a response or authorize an action.
- `tools.py` dispatches one classified read/check batch through the existing
  ContextTools/CodingCommands owners, records native correlation and returns the
  consumed action count. It receives the actual history/stage/report objects,
  not a second mutable session copy. Shared-check acceptance remains provisional
  until the lifecycle coordinator completes currentness/restoration/accounting.

No generic runtime, protocol registry, persistence store or result schema is added.
Task hashes, `qwen-coding-loop-v2` records, refusal/persistence order, exact source
admission, budgets, ToolRunner authority and WorkCycle/publication separation are
unchanged. Uncertain effects are never retried because a record failed. Private
fault injection follows the actual new implementation owner; public imports and
the coordinator's restoration/finalization seams stay at `coding_loop`.

The coordinator and each extracted Python module fit the existing32,768-byte
resulting-source bound, including ordinary CRLF representation. This does not
remove the4,096-byte region,8,192-byte aggregate old/new,16,384-byte patch or
Context/action limits, and does not prove autonomous edit effectiveness.
`development_task.py` and `context_tools.py` remain oversized, separately owned
cohesion work; their bodies are unchanged by this extraction.
