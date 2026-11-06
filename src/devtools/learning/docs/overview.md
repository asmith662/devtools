# Learning values and classification inspection

This is a partial selective migration, not a qualified fitting or investigator
API. The installed package currently has no fitting entry point, worker,
execution grant issuer, scientific ledger or learning Tool. Checkpoints A and B
remain incomplete.

`representation.features.FeatureTable` retains ordered feature names, declared
continuous/discrete semantics and finite numeric observations. It rejects text,
booleans, malformed schemas and nonfinite values. Feature semantics do not follow
from numeric storage.

`representation.targets` preserves exact category scalar types. Integer `1`,
float `1.0` and boolean `True` remain distinct category identities. Only category
validation and identity were extracted; quantile target fitting is deferred.

`evaluation.classification.evaluate_classification` independently constructs
confusion counts from supplied truth and predictions, validates correspondence
and returns immutable evidence. It performs no fitting and establishes no source
role or execution authority. Held-out status must come from the caller's admitted
population, not this arithmetic.

`evaluation.classification_v2.macro_f1_value` requires an explicit version.
Version 1 retains strict harmonic F1 and propagates undefined ratios. Version 2
uses direct binary counts for integer labels 0 and 1, measures zero F1 for a
class with errors and zero true positives, and remains undefined when a required
class has neither truth nor predictions. It rejects unsupported versions and
nonbinary categories. No F1/MAE aggregation or metric-binding publication is
implemented.

These modules import only the standard library and other learning modules. They
do not import Agents, ModelInteraction, Tools, Context or a numerical backend.
Learning values confer no permission to fit, publish or access a source.

See the [migration status](../../../../docs/development/learning-integration.md)
for exact provenance, qualification and unfinished work.
