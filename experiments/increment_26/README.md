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

No task or source embedding, similarity, candidate surface, usefulness outcome,
or semantic retrieval result has been generated at this checkpoint.
