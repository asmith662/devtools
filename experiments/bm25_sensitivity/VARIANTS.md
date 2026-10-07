# Nearby BM25 variant audit (pre-outcome)

Scope: retained Increment 27 development protocol/results and installed pinned
`bm25s==0.3.11` scoring source. No confirmation/reserve data or new variant
execution. This is an audit of the actual retained formulations, not a claim
that all papers/libraries implement the same version.

| Variant | Retained test / judged evidence | Exact retained or available formulation | Production / unresolved issue |
|---|---|---|---|
| Canonical Okapi-style positive-IDF BM25 | Native production comparator in historical tasks | IDF=ln(1+(N-df+0.5)/(df+0.5)); TF=tf*(k1+1)/(tf+k1*(1-b+b*L/avg)); independent content + weighted filename | Production defaults unchanged; R1.6 measures parameter robustness |
| BM25+ | Increment 27 frozen k1=1.2,b=0.75,delta=0.5, two fields and 0.25 filename weight; useful@5=63 versus canonical 63; two top-five gains/two losses, identical positive membership | `bm25s` TF=tf*(k1+1)/(tf+k1*norm)+delta; IDF=ln((N+1)/df). Adapter excludes nonmatching documents despite delta/background scores. NumPy float64; native comparator does not use this library | Experimental only; redundancy at one setting/top-K is not a universal negative result, nor prospective obligation-completion proof |
| BM25L | No judged retained comparison identified in this audited development evidence; installed implementation exists | `bm25s` c=tf/norm; TF=(k1+1)*(c+delta)/(k1+c+delta); IDF=ln((N+1)/(df+0.5)); library has explicit nonoccurrence/background handling | Not production; any later trial must freeze delta, zero-overlap eligibility/background handling and formula/library provenance |
| Lucene, Robertson, ATIRE | Increment 27 identifier/path views use `bm25s` Lucene; not separate judged canonical-token variant arms | Installed Lucene TF=tf/(k1*norm+tf), positive log1p IDF; Robertson IDF=ln((N-df+0.5)/(df+0.5)) clamped nonnegative by default; ATIRE IDF=ln(N/df). These differ in scaling/IDF, not this parameter treatment | No promotion. Library support is not effectiveness evidence; index representation and query analysis must remain separately attributable |

Evidence: `experiments/increment_27/lexical_comparison.py` / freeze JSON / README,
its development top-five result table, and installed `bm25s/scoring.py` functions
`_score_tfc_*`, `_score_idf_*`, plus background-score calculation.

**Decision: no additional variant experiment justified before BM25F on the
currently retained evidence. R1.6b is not required.** BM25+ demonstrates no
aggregate top-five gain/new positive universe in the available same-representation
development trial; BM25L has available code but no verified case establishing a
specific canonical-formula defect that requires it as a prerequisite. Neither
fact rules out a future bounded variant study. Keep BM25L/BM25+ open hypotheses,
with a promotion trigger of an independently demonstrated length/TF/formula
failure not adequately answered by canonical sensitivity or field attribution.
This decision avoids treating parameter movement as a new formula or treating
unexplored library options as mandatory exhaustive search. It does not erase
BM25 variants, change R1.7/R2 order, or infer BM25F field weights from filename
weight. Prospective R1.6 effectiveness remains unknown until fresh gold.
