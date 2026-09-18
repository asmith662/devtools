# B-0015 — Framework Acceptance & Harness Validation

- type: EPIC
- status: BACKLOG
- decision_maturity: NEEDS_INVESTIGATION
- necessity: REQUIRED
- architectural_significance: STRUCTURAL
- urgency: SOON
- evidence_basis: MULTIPLE
- scope: progressive evaluation of reusable boundaries through specialized harnesses
- primary_domain: evaluation
- supporting_domains: observability, experiments, models, agents

## Problem / value

Ensure reusable framework semantics graduate from deterministic evidence to
task-specific live acceptance when a meaningful path exists. Evaluation judges
behavior; observability supplies factual evidence; neither authorizes a generic
live-test framework.

The durable Qwen acceptance reports are one bounded example. They do not make
Qwen semantics reusable or establish a universal acceptance harness.

Accepted Evaluation semantics require a referenceable assessment/comparison
basis, intended condition and relevant fixed factors, distinguishable
realizations when needed, evaluator/oracle/criterion meaning, heterogeneous
observations or judgments, and separation of later comparison/inference from
raw observations. Concrete fixtures and experiment-local records may satisfy
these roles. This epic does not authorize universal `EvaluationCase`,
`Treatment`, `EvaluationRun`, `EvaluationEpisode`, scalar score, causal DAG,
trajectory, oracle, metric, storage, or tracing infrastructure.

Future harnesses should correlate rather than duplicate layer-owned artifacts
and Evidence, retain failed or incomplete assigned realizations, distinguish
historical experimental truth from current predictive relevance, preserve
evaluator-only information from model disclosure, and keep layer-local
correctness distinct from downstream utility. Controlled comparisons may need
to expose marginal contribution, interaction effects, and typed resource costs
without requiring a universal utility model.

Concrete case/fixture references, condition assignment, realization
correlation, evaluator representation, outcome types, comparison methods,
regrading, protected-oracle handling, persistence, statistics, and integration
with execution/observability remain unresolved implementation pressure. The
current Qwen reports remain experiment-specific evidence rather than a reusable
Evaluation architecture.

Future reusable consumers may still pressure the exact reference/identity scope
for basis, condition, realization, evaluator application, and comparison, and
the concrete governance owner when evaluator-private information shares stores
or capabilities with an Agent. Those questions require consumer evidence; they
do not block an initial deterministic repository-intelligence slice that does
not expose protected oracle state.

- hard_dependencies: none
- pressure_dependencies: none
- operational_dependencies: meaningful specialized harness path
- children: B-0016
- promotion_trigger: structural primitive has deterministic coverage and a meaningful live path
- validation_level: INTEGRATION
