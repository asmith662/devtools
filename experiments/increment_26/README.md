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

## Development reproducibility and blinded judgment checkpoint

The amended frozen protocol executed across all eight frozen development cases.
Candidate evidence and blinded judgment artifacts were generated. Exactly 8
development cases executed, retaining 40 semantic-arm
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

One independent full eight-case CPU replay completed in approximately 905
seconds. Its candidate evidence and blinded judgment artifacts were each
byte-identical to their committed canonical counterparts, with the same
execution/evidence identity. Semantic scores, candidate order, winning chunks,
lexical candidates, and the neutral pair union were exact matches. During the
run, the Windows process priority was corrected from Idle to BelowNormal
without restarting the process or changing computation. Process priority is
not part of retrieval semantics. The redundant replay JSON files were removed
after their hashes were verified against the canonical files.

All 69 neutral development pairs were then judged using only the blinded
judgment input: frozen purpose and lexical query, parent snapshot identity,
resource address, and parent-snapshot content. Increment-25 prior judgments
were checked under the frozen four-part identity rule; none matched these
development cases. The three-state, purpose-relative decisions and rationales
are retained in `development_frozen_judgments.json`, bound to the amended freeze,
canonical blinded input hash, and canonical evidence identity. This judgment
artifact was validated and fingerprinted before any origin join. No development
semantic-versus-lexical usefulness comparison has occurred. Confirmation and
reserve remain sealed. This checkpoint does not establish semantic usefulness,
superiority over lexical retrieval, confirmation, or production readiness.
Roadmap, backlog, and architecture updates remain deferred until a later
authorized conclusion.

Frozen development judgment content identity:

```text
36c4ab749c8829750eb5fc47bef0125ac45d2e481626b277cb2510061c510fc8
```

The frozen artifact has 24 `USEFUL`, 43 `NOT_USEFUL`, and 2 `UNJUDGED`
judgments. All 69 are new Increment-26 judgments; the prior frozen
Increment-25 confirmation population has no matching InformationNeed and
parent snapshot in this development partition. These counts do not include
candidate-origin information.

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
