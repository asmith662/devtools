# Selective numerical learning

This candidate implements general supplied-data binary classification and scalar
regression. Release acceptance remains conditional on the migration qualification
and protected development gates; see the [integration record](../../../../docs/development/learning-integration.md).

`representation` preserves finite typed features, target identity and train-only
standardization. Binary training requires both original integer classes 0 and 1.
Regression preserves target/feature units, source identity, population roles and
row memberships. No working Context is converted into a training population.

`investigation.plans.LearningPlan` is an effect-free exact scientific frame.
Only its independent trusted caller can issue `ExecutionAuthorization` for that
plan identity and singleton method. A proposal, historical EvidenceReference,
method availability or Tool validation does not confer authority.

The selected methods are standardized seven-neighbor binary classification,
SQUARE logistic and squared-hinge margin classification; Mean, standardized Ridge
and deterministic five-neighbor regression v2. Retained immutable states support
label-free prediction. SQUARE appends squared coordinates after training-only
standardization. Unsupported families and mismatched roles/schemas/units refuse.
Mean needs no native fit. No residual, ranking, selection or OOF strategy is installed.

`evaluation` retains macro F1 v1 strict harmonic/nonvalue semantics, binary-count
F1 v2 and quantitative MAE in the original target unit. Values and typed NoValue
observations remain distinct. Different metric versions/families are never pooled.

`integrations.local.operations` composes the original acknowledged scientific
execution/SQLite ledger/immutable publication contracts. `inspection.inspect_learning`
reads the pinned publication and read-only ledger, validates grants, source,
state and acknowledgment ordering, independently recomputes preparation and
prediction/metric arithmetic, and returns an `InspectedLearning` fitted artifact.
Native kNN boundary ambiguity is retained as a limited parity scope; it does not
replace deterministic retained mathematics or establish generalization.

NumPy/SciPy/sklearn/threadpoolctl are optional (`devtools[learning]`). Core values,
inspection, ordinary coding and repository imports do not load the numerical
stack. Native fitting is qualified narrowly for Windows CPython 3.12.13 and the
pinned extra; other runtimes are refused until qualified. Runtime receipts include
interpreter/ABI, distribution origins and loaded native DLL identities/threads.

The core imports no Agents, Tools, ModelInteraction, apps, scripts or experiments.
`tools.learning` adapts exact plans to existing managed Commands; it uses a
suspended-start one-process Windows Job, bounded streams, one native thread and
one operation per exclusive output root. This is process custody, not an OS file
or network sandbox. The packaged trusted numerical worker has additional Python
audit guards; no model-generated code is executed.

`agents.learning.process.investigate` composes native ModelInteraction calls,
`agents.model_tools`, ToolRunner and independent host admission. Its caller must
explicitly select `b0096-engineering-v1`, supply admitted sources and a finite
LearningBudget. Newly inspected observations precede the next decision. The
finite menu can continue, stop or abstain. A sealed terminal selection precedes
host-only protected final evaluation. The parent invokes the inspected artifact's
`predict` method with label-free inputs. This adds no generic agent/workflow runtime.

The supported operator `scripts/qualify_learning.py --execute --inputs DIR
--output FRESH_DIR --deny-root PATH` runs the two exact attributed development
fixtures with a scripted ModelInteraction. It never calls a live provider, reads
the donor or imports tests. These exposed fixtures qualify engineering behavior;
they do not establish strategy effectiveness or scientific generalization.
