# Increment 26 — independent semantic candidate generation

This is a pre-outcome experiment freeze. It tests whether one pinned pretrained
representation configuration can independently expose useful repository
resources beyond an equal-cardinality canonical lexical surface for the same
frozen task-card `lexical_query` and parent snapshot.

It is not lexically seeded semantic expansion: semantic and lexical arms each
independently receive the frozen query and the same bounded resource capacity.
It is not learned ranking, training, hybrid production retrieval, K=5 Context
selection, or Increment 27's evidence-family comparison.

The representation unit is an experiment-local tokenizer-bounded raw-source
chunk. Chunks project by maximum similarity to a repository-resource candidate;
they are not Repository Intelligence, RepositorySubjects, candidates, or
Context units. Parent snapshots, task cards, partitions, and qualifying
resource usefulness judgments are reused only under their frozen identities.

## Development first pass checkpoint

The amended frozen protocol has executed successfully once across all eight
frozen development cases. This is a DEVELOPMENT FIRST PASS. Candidate evidence
and blinded judgment artifacts were generated; no usefulness judgments have
been performed. Exactly 8 development cases executed, retaining 40 semantic-arm
candidate occurrences and 40 lexical-arm candidate occurrences. Their union
contains 69 neutral InformationNeed/resource pairs.

Candidate evidence SHA-256:

```text
3b78cd07360f277523ca195401d1bc322ad28c1d7e03c1ea569490b87afa277d
```

Blinded judgment SHA-256:

```text
7df8065b63f896e2e16d5aea29c93dd7fd46e3321ac820a656eeee795f71d69d
```

Execution/evidence identity:

```text
330a9bec94a023d1033ece21f885cdaca122f70eb7d3acb02c4588e948fb4ce2
```

The pinned model required a narrow compatibility implementation for
`get_extended_attention_mask` under the frozen Transformers runtime. Review
found it semantically equivalent to the relevant noncausal float32
encoder-mask behavior for this frozen execution path.

An attempted replay was interrupted before case execution and produced no
scientific result. A complete independent full-model replay has not yet
completed, so replay reproducibility remains pending before blinded development
usefulness judgment. Confirmation and reserve remain sealed. This checkpoint
is intermediate; it does not establish semantic usefulness, superiority over
lexical retrieval, confirmation, or production readiness. Roadmap, backlog, and
architecture updates remain deferred until a later authorized conclusion.

For replay from an already populated Hugging Face cache, the development
command supports `--offline`. This resolves only the frozen repository and
revision from local cache files, then retains the frozen weight SHA-256 check
and local-only model/tokenizer loading. Missing or mismatched artifacts fail
without an online fallback.

The pre-outcome freeze was amended only to add the omitted transitive runtime
dependency `einops==0.8.1`, required by the pinned CodeRankEmbed implementation
for model loading. The omission was discovered before CPU inference and before
any development case, query, resource, similarity, candidate, or usefulness
outcome was processed. The original freeze identity is retained in the
amendment history; no scientific parameter or experimental outcome informed
this correction.
