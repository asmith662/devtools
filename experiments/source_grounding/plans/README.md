# Prospective unapproved controller plan

The later [controlled pipeline deployment review](PIPELINE_DEPLOYMENT_REVIEW.md)
owns the current binding-only candidate-07 successor of the four-call
candidate-06 experiment. It records PLAN_VALID / startup PASS, BUDGET_UNAVAILABLE,
approval NONE and no execution. The plan described below remains historical
evidence for its original lineage.

This is the second publication boundary, after the immutable scientific Stage A.
The [canonical plan](run-plan.json) uses experiment-controller-plan-v2 and grants
no execution authority. No approval artifact or scientific run accompanies it.

| Binding | Immutable value |
| --- | --- |
| Stage A commit | 981086bf7c15033be0f16b493002330241d4b858 |
| Stage A protocol SHA-256 | 9a88f322c39f7fd8bf19c938fd53cd2005769f8374829e18d5cb8f3bce84ae5a |
| Stage A integrity SHA-256 | c5bbb07309645d0ac46cfc74fc7404209cf255379e99f112402d63f1d24dfed8 |
| Plan SHA-256 | 01bc688a0fcbf7d133cddeea94489398460517ec32d74931d6a0050140d5d7e3 |
| Derived run ID | 5cb532eb162b3d8f7cf7c8f96c424c9a9d905307b19fbe18ad7a99ee7e91dc7a |
| Cases | 0020, 0021, 0022, in that order |
| Execution authorized | NO |

The plan binds each exact parent frame and its committed design/resource/input
blobs, Stage B adapters, source-grounding packet/worker and Sol/High configuration,
independent Stage C packet/worker and Astra/High configuration, exact gold import,
deterministic D, all 322 Stage A implementation entries and the complete current
controller implementation map. Its run ID derives only from immutable prospective
bytes and controller code; approval or operational timestamps cannot change it.
The [Stage A review](../STAGE_A_REVIEW.md) owns scientific semantics and validation.

Preparation precedes packets. All packets publish before B and C; these branches
have independent inputs. Imports require all B sealed and all C valid; D requires
committed B and C. Concurrency is three cases / three logical worker processes /
one Astra worker, with at most one nested Sol in each B slot and three simultaneous
model calls total. Worker/grounding/validator timeouts are 21600/7200/3600 seconds;
cleanup grace is ten seconds. Scientific retries are NEVER_SCIENTIFIC.

The controller serializes PACKET/B/C/D commit/push boundaries and stops on
publication divergence. LOCAL/CHECKPOINT use the frozen focused tests/static
checks. FINAL additionally verifies deterministic D, exact receipts and imports,
runs the protected production profile and the controller's mandatory static floor,
plus active-adapter checks. The preparation cache is explicitly disabled because
this adapter forwards disclosed inputs and has no distinct derived cache surface.
Native objects and treatment/primary outputs never qualify as preparation cache.

Ignored controller progress logs/status and the experiment's separate operational
timing summary expose running/interrupted/complete states and costs without
establishing scientific authority. Immutable receipts, sealed B proof, preserved
primary bytes and deterministic D replay own final verification. Fresh external
worker roots and pinned launcher version/model/reasoning remain required.

Stage A recovery completed before plan creation. Candidate schema, disclosures,
hashes, frame bindings, finite limits and zero-authority checks passed; independent
plan reconstruction reproduced its exact bytes/digest/run ID. Non-live launcher
preflight passed with codex-cli 0.162.1 and both pinned model configurations,
without making a model request. Committed prospective authentication is required
after the separate plan publication:

```text
uv run python -m experiments.orchestration plan experiments/source_grounding/plans/run-plan.json
```

Expected: PLAN_VALID, execution_authorized=NO and the exact run ID above. This
read-only command creates no approval, worker output or scientific entry.
The expensive Stage A/protected suite is retained at its immutable checkpoint;
plan-only publication uses bounded plan/Git checks. No source or science changes
are folded back into Stage A.

Exact next step: maintainer reviews the Stage A commit, this separate plan commit
and the exact run ID. Do not approve or run automatically. Confirmation/reserve
and historical children remain sealed; production behavior is unchanged.
