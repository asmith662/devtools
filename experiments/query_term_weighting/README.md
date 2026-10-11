# Query-term discrimination experiment

This non-installable experimental package owns task-side contribution importance,
not production retrieval or a new retrieval view. Its dependents are Case 0014
and controlled synthetic tests. Native Localization identities/provenance and
lexical analysis, BM25 statistics and contribution objects retain their ownership.
No framework promotion is authorized.

Three roles are necessary to isolate literal emphasis (B) from work-verb
attenuation (C). A uses 1 for every term; B uses 2 for explicit anchors and 1
otherwise; C uses 2 / 1 / 0.5 for anchor / semantic / generic. These small
binary-exact values challenge an interpretable hypothesis without fitting a
corpus. The complete generic lexicon is `add, build, create, implement, update`:
ordinary work verbs, with no domain nouns, stopword system or frequency tuning.

For every native positive candidate:

`score = sum(content_contribution[t] * multiplier[t]) +
0.25 * sum(filename_contribution[t] * multiplier[t])`.

Both native channels keep their independent statistics and native summation
order. This is not BM25F. The scorer accepts only a complete canonical native
result, retains every original contribution object and sorts weighted scores
with original document collection position as tie-break. It does not execute
retrieval. Repeating query strings is not weighting: native distinct terms score
once, although all original spans remain available. Duplicate term occurrences
share one multiplier; any proven anchor occurrence has explicit precedence.

Classification sees only exact query/task text, native query spans, task-local
identities and copied task-marked literals. Semantic is the neutral default for
intentionally authored fact terms. Ambiguous overlapping or partial-token anchor
claims are rejected. Every term remains present and every multiplier is positive.

Case 0014's Stage A review owns the frozen rule and future execution contract.
Controlled synthetic tests are separate from prospective execution.
