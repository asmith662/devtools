# R1: whole identifiers plus subtokens sparse retrieval

Experimental consumer-owned retrieval view; no production caller or canonical
API changes. [Case 0009](../codex_dogfood/case_0009/README.md) owns the first
prospective protocol. [Case 0009 Stage D](../codex_dogfood/case_0009/analysis.md)
is now **prospectively evaluated: RETAIN AS SEPARATE RETRIEVAL VIEW**. REQUIRED
positive reach is unchanged; mixed ranking gains/regressions fail the frozen
promotion gates. Canonical production BM25 is unchanged. [R1.5 diagnostics](../retrieval_diagnostics/README.md)
now explains frozen outcomes; R1.6 sensitivity is next, followed by R1.7 and
mandatory R2. No frozen R1 treatment or conclusion changes.
The [roadmap](../../docs/roadmap.md#current-sequencing) remains authoritative.

## Frozen representation

`analysis.py` reuses canonical Unicode `\w+` spans and the retained
`experiments.retrieval_identifier.expand_identifier_terms` splitter. For each
span emit its whole case-folded form first, then unique case-folded components.
Underscores separate components; split lowercase-to-uppercase transitions,
an acronym before a capitalized word, and alphabetic/digit transitions in both
directions. Leading, trailing and repeated underscores produce no empty terms.
All-uppercase components stay whole. Unicode uses Python's character predicates
and case folding, with no Unicode normalization or dictionary segmentation.

| Source span | Ordered terms |
|---|---|
| `CandidateMemberResolution` | `candidatememberresolution`, `candidate`, `member`, `resolution` |
| `candidate_member_resolution` | whole underscore form, `candidate`, `member`, `resolution` |
| `acquire_localization_lexical_evidence` | whole underscore form, `acquire`, `localization`, `lexical`, `evidence` |
| `HTTPRequest` | `httprequest`, `http`, `request` |
| `HTTPRequest2` | `httprequest2`, `http`, `request`, `2` |
| `parseHTTPResponse` | `parsehttpresponse`, `parse`, `http`, `response` |
| `ADR0005` | `adr0005`, `adr`, `0005` |
| `__all__` | `__all__`, `all` |
| `RepositoryId` | `repositoryid`, `repository`, `id` |
| `Python3Parser` | `python3parser`, `python`, `3`, `parser` |

Deduplicate **within each source span**, including whole/component equality.
`candidate` contributes once; `candidate_candidate` contributes its whole form
and `candidate` once. Separate source occurrences retain term frequency. Query
terms are distinct in first-occurrence order, as in canonical BM25. No stemming,
stopword removal, synonym expansion, identifier extraction from task prose or
query reformulation occurs. Ordinary prose spans remain unchanged.

`compare_terms(text, maximum_spans=32)` exposes bounded observed spans and
canonical/expanded terms for attribution, rather than dumping a corpus.

## Indexing and scoring

`build_index` takes the native whole-resource document collection and creates
experiment-owned content lengths and postings. `retrieve` retains document
identity and emits explicit content/filename score contributions and term
evidence. It uses production IDF and BM25 contribution functions, not a copied
generic BM25 implementation. Constants remain `k1=1.2`, `b=0.75` and filename
weight `0.25`; positive results only, ties retain corpus order. The filename-stem
index is rebuilt per query, matching the production lifecycle.

R1 changes analysis of **content, filename stems and query** together. These
remain independently scored content and filename indexes. This is **NOT BM25F**.
The paired field evidence permits later content-versus-filename attribution;
there is no third retrieval arm or field-weight tuning in this case.

The index preserves native documents and their corpus lineage. It does not add
a general snapshot-validation contract; Case 0009 validates documents against
its frozen native snapshot before execution. No persistence API is promoted.

## Historical comparability and limitations

[Analyzer definition](analyzer_definition.json) pins mechanism source hashes
before the [retrospective diagnostic](historical_diagnostic.json). The diagnostic
compares three saved Increment 27 development queries and finds exact term-stream
parity. It does not join labels, rerun historical rankings or claim effectiveness.
Increment 27 already used **whole plus subtokens**, not split-only analysis, on
content, filename and query. Therefore neither that comparison nor Case 0009
establishes that retaining whole forms prevents split-only regressions. Retention
is mechanically proved; paired prospective losses must still be evaluated.
Increment 27 used `bm25s` Lucene scoring; R1 uses shared canonical scoring
arithmetic. No full numerical historical replay is claimed.

Expansion changes lengths, frequencies and document frequencies even when whole
forms remain. A rank improvement alone is not a representation recovery. The
independent adjudication/join must report gains, losses and net change, with exact
query/content/filename term evidence for claimed representation effects.

**R2: true BM25F / field-aware sparse retrieval proceeds regardless of whether
R1 improves, ties or worsens canonical BM25.** No production adoption occurs in
this increment, including after a favorable prospective result.
