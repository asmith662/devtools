# Retrieval

Production retrieval owns purpose-relative use of repository information. It
does not establish repository relationship truth or decide Context disclosure.

The [current retrieval foundation](../../../../../docs/architecture/retrieval.md)
owns the reconciled inventory, canonical lexical behavior, empirical limits and
open retrieval hypotheses. Production has whole-resource content BM25 plus an
independent filename-stem contribution at weight 0.25: **not BM25F**. Unicode
word/casefold terms do not split snake/camel/Pascal/acronym identifiers. There
is no production dense, learned sparse or learned ranking/reranking path.
The [first R2 Stage A](../../../../../experiments/codex_dogfood/case_0015/STAGE_A_REVIEW.md)
is frozen prospectively: only existing content/filename fields, native additive A
versus experiment-only true BM25F B; zero prospective execution, no gold and no
production integration. Maintainer review must precede execution.

Identifier/subtoken evidence and true BM25F are separately attributable mandatory
roadmap experiments; canonical production behavior is unchanged.

## Query-conditioned graph ranking

The [graph-ranking package](../graph/docs/overview.md) projects already-derived
Repository Intelligence (RI) facts into either the reproducible resource-only
view or typed resource/declaration views. Query-derived lexical rank mass seeds
weighted Personalized PageRank (PPR), which returns snapshot-bound structural
evidence. Optional equal-channel Reciprocal Rank Fusion (RRF) combines native
BM25 and PPR ranks while retaining both originals. The typed core view includes
declaration containment and direct bases; an additional navigation view
includes qualified package membership and weak mirrored paths. Neither
enumerates graph paths nor determines disclosure. The
[first replay](../../../../../experiments/graph_ranking_baseline/README.md)
and [typed replay](../../../../../experiments/typed_graph_baseline/README.md)
found worse complete required-resource depth than BM25 on one retained
development case. Graph ranking remains optional evidence.

## Direct Python structural projection

`retrieve_python_direct_structural_resources` accepts an identified
`RepositorySnapshot`, a `PythonDirectStructuralRetrievalRequest` containing a
nonempty purpose and distinct seed resource addresses, and already-derived
production RI facts: `PythonResolvedModuleImportRelation`,
`PythonDeclarationReferenceKnowledge` (or archived
`PythonFunctionReferenceKnowledge` values), and `PythonImmediatePackageMembership`.
All seeds and fact endpoints must belong to the supplied snapshot. The caller
chooses and bounds the RI fact inputs; an omitted fact family produces no
negative knowledge.

For each seed, the operation projects one direct relation to its other resource
endpoint. Imports and References can project in either direction; immediate
package membership projects child to package or package to child. A direct Call
is the `direct_call` tag on the same Reference fact, not another relation.
Self relations do not yield a new resource candidate. No transitive traversal,
ranking, score, or fixed result limit is applied.

The result retains the request and snapshot identity. Each distinct candidate
resource is keyed by its snapshot identity and repository address, ordered by
its first support. Its supports retain the seed, direction, and exact native RI
fact; repeated presentation of the same fact for the same seed/direction is
deduplicated, while distinct declarations, occurrences, and relation families
remain independently visible. The native fact supplies derivation, source span,
target, resolution, and qualification provenance as applicable. Surfacing a
resource predicts possible usefulness for this request; it does not establish
relevance, select a resource for a budget, or choose a Context representation.

## Snapshot-bound resource evidence composition

`compose_lexical_structural_resource_evidence` accepts a caller-selected
`RepositorySnapshot` and explicit nonempty purpose alongside one native lexical
BM25 result and one native direct structural result. It does not make the lexical
query text into an InformationNeed or change either mechanism's result type.
The structural result and its candidates must match the invocation snapshot;
its request purpose must exactly match the invocation purpose.

The lexical corpus retains selected observed occurrences rather than a snapshot
identity. Composition therefore checks the corpus repository, every represented
document and indexed statistic, and each returned match. Every corpus resource
must be the exact observed resource at that address in the supplied snapshot.
This checks content identity even for corpus members that were not returned as
matches, since they can affect BM25 statistics. Missing or changed resources
reject composition; no cross-snapshot applicability is inferred.

One `LexicalStructuralResourceEntry` retains the snapshot ID and observed
resource, an optional native `RepositoryTextLexicalBm25Match`, and all distinct
native `PythonDirectStructuralResourceEvidence` supports. Repeated presentation
of the same match or structural support is deduplicated; independent supports
remain separate. The `LexicalStructuralResourceInventory` also retains the
original results and invocation purpose. Entries iterate by ascending canonical
repository address, a neutral deterministic inventory order. Native lexical
rank is retained as a separate one-based lexical rank on matching entries;
scores, field contributions, query, index, structural seed, direction, and RI
fact provenance remain available in their original forms. Missing
support from either mechanism makes no negative relevance claim.

```text
Repository Intelligence
        |
        v
mechanism-specific retrieval
   |             |
 lexical      structural
   |             |
   +------v------+
          |
resource evidence composition
          |
          v
optional rank fusion -> explicit Context disclosure choices
```

The composed result is a candidate/evidence inventory, not an actionable file
set. [ADR-0005](../../../../../docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md)
places Localization after native Retrieval evidence and before Context Planning.
The `devtools.context.localization` semantic kernel and its one-way lexical
consumer adapter exist. Core Retrieval does not own obligation semantics.
Context Planning retains disclosure representation
and capacity decisions. Retrieval still ends at native candidate evidence, not
task completeness.
The historical structural union experiments remain reproduction evidence;
future production consumers use this composition operation for native direct
facts and lexical evidence.

Localization now has a one-way consumer adapter in
`devtools.context.localization.lexical`. It invokes this package's canonical
content-plus-filename BM25 API once for the complete caller-supplied task query
and independently for each explicit obligation query. Each result remains a
native `RepositoryTextLexicalBm25RetrievalResult`; query-to-obligation association
is owned by Localization. This package does not depend on Localization types.
The full-task lane preserves global lexical reach over the authorized corpus,
while obligation lanes add caller-directed queries. Acquisition has no role
scoping or cross-lane fusion. Localization's separate implemented routing package
provides lossless preferred/escape presentation after acquisition. Query
association, rank, score, and absence do not establish
obligation satisfaction, confidence, irrelevance, or non-applicability. See the
[Localization package contract](../../localization/docs/overview.md).


## Repository-map structural relevance

The [repository-map package](../repository_map/docs/overview.md) provides an
independently inspectable channel: global structural importance, compact
symbol/path BM25, symbol rank combination and maximum-symbol resource ranking.
Resource BM25 and query-conditioned Personalized PageRank (PPR) remain separate.
Optional Reciprocal Rank Fusion (RRF) preserves native channel evidence.
Ranks and declaration spans can later support Context Planning's compact
representations, without Retrieval rendering or selecting disclosure.

## Selectable source representations

The maintained [Qwen consumer](../../../../../apps/qwen/README.md) now selects
these views on demand through native read-only Tools. Its byte/call budgets and
authority remain application concerns, not ranking or RI truth. Explicit task
corpora can call `discover_repository_resource_addresses(...,
requested_addresses=addresses)` to probe only required canonical regular-file
paths. The discovery result retains the requested selection and its `semantics`;
component probes are bounded, required links/missing paths refuse, and unrelated
directories are not enumerated. Omitting this option preserves recursive
discovery. This is metadata discovery, not acquisition or an exhaustive corpus.

`devtools.context.retrieval.source` provides `build_source_search_index` and
`search_repository_source` (also exported by `devtools.context.retrieval`).
This is in-memory composition of the existing explicit text corpus, lexical
analysis/statistics, content-plus-filename BM25 and rank-fusion arithmetic.
It adds no external dependency, discovery policy, persistent index, embedding,
or default change to legacy lexical callers. Build once, then choose a mode:

| Mode | Search population |
| --- | --- |
| `file` (default) | Every admitted corpus resource; identical text, document identity, BM25 score and ordering to existing whole-file retrieval |
| `symbol` | Recursive Python classes, synchronous/asynchronous functions and methods; decorator-inclusive exact slices and lexical qualified names |
| `window` | Exact contiguous line windows, default 80 lines with 20 lines of overlap; configurable when building the index |
| `mixed` | All three native rankings, consolidated through equal-view RRF with constant 60; native scores are never added across populations |

Python syntax uses stdlib AST with the existing Python 3.12 grammar contract.
Canonical RI module functions/classes/direct methods retain their original
declaration and subject objects. Nested/conditional declarations outside those
bounded RI analyzers retain `PythonSourceOccurrence` and a representation
identity, **not an invented semantic subject**. Qualified names describe syntax
nesting; they do not assert runtime binding resolution. Qualified names are
metadata; body/filename BM25 retains existing tokenization and adds no separate
qualified-name field scorer. Decorators are included
in the search occurrence, while the native declaration's original support is
unchanged. Invalid Python, other file types and Python with no declarations
fall back to the original file in symbol mode; `view.fallbacks` gives the reason.
Window mode also covers code outside definitions and long functions. Empty
windows and already-contained tail windows are not emitted. It is a line bound,
not a byte/token budget: one long line can still be large.

`RepositorySourceUnit` specializes the existing `RepositoryTextDocument` and
uses its existing identity wrapper; it does not create another document system
or RepositorySubject. Its parent is the original observed resource. Every unit
retains repository/snapshot identity, parent content identity, representation
kind, half-open decoded-character offsets `[start, end)`, physical line numbers,
exact original `text`, and symbol/parent metadata where applicable. Python
occurrences additionally retain canonical one-based line/UTF-8 byte-column
ranges. UTF-8 columns and character offsets are distinct. LF, CRLF and bare-CR
source bytes are preserved. Only LF, CRLF and CR delimit physical lines; VT,
FF, FS, GS, RS, NEL, LS and PS remain source characters. The source index uses
the same untranslated universal-newline convention as exact function source
materialization. Window boundaries and displayed line numbers follow that
convention for non-Python resources too. This corrects affected slices, not
identity rules: correctly indexed units keep their existing identities, while
previously incorrect offsets produce the identities of the corrected slices.
No native declaration, source-observation or edit authority is broadened.
The snapshot is the existing bounded text
observation; the API does not claim an authenticated Git revision or a
repository-wide simultaneous filesystem observation.

Mixed results retain `native_results` and, on every hit, `evidence` with native
view/rank/match/source unit. Exact or contained non-symbol evidence is assigned
once to the highest native-ranked eligible symbol, then window. Each view
contributes only its best rank in that group to RRF. File-fallback origins retain
provenance, but contribute no duplicate symbol vote. Distinct symbol declarations
(including nested classes/methods) remain selectable. Partially overlapping
windows with novel source remain separate; this avoids discarding their tails.
All original candidate evidence remains in the retained native results even
when the final hit limit truncates presentation. This deterministic consolidation
is an engineering baseline, not calibrated relevance or empirical superiority.

Source-level native populations contain multiple representations of a resource;
they are not inputs to legacy one-document-per-resource composition/graph-fusion
contracts. Those contracts and their validation remain unchanged. Use the source
result's consolidation and native evidence for source-level consumers.

### Python caller examples

Use the existing discovery/observation and `define_repository_text_corpus` /
`realize_repository_text_corpus` APIs to prepare `snapshot` and `corpus` with
explicit authorized membership. An all-repository corpus searches all admitted
text resources; a selected corpus searches only that scope. Indexing does no
additional filesystem acquisition or implicit inclusion of ignored/private files.

```python
from devtools.context.retrieval import (
    build_source_search_index,
    search_repository_source,
)

index = build_source_search_index(
    snapshot,
    corpus=corpus,
    window_lines=40,
    overlap_lines=10,
)
files = search_repository_source(index, query="timeout", mode="file")
symbols = search_repository_source(index, query="with_timeout", mode="symbol")
windows = search_repository_source(index, query="timeout", mode="window")
mixed = search_repository_source(index, query="timeout", mode="mixed")
unit = symbols.hits[0].unit
whole_file = index.expand(unit, to="file")
enclosing_class = index.expand(unit, to="class")
```

Class expansion returns the nearest containing class (including the unit itself
when it is a class); absence raises `ValueError`. Windows must lie entirely
inside a class to expand that way. Expansion and disclosure remain caller choices:

```python
from devtools.context.planning import (
    SourceSearchDisclosureOption,
    choose_whole_resource_disclosure,
    materialize_disclosure_plan,
    plan_disclosures,
)

choice = SourceSearchDisclosureOption("inspect timeout", enclosing_class)
plan = plan_disclosures(
    purpose="inspect timeout",
    snapshot=snapshot,
    disclosures=(choice,),
)
context = materialize_disclosure_plan(plan=plan, snapshot=snapshot)
# Alternatively use the existing whole-resource option:
file_choice = choose_whole_resource_disclosure(
    purpose="inspect timeout",
    snapshot=snapshot,
    resource_address=whole_file.resource.address,
)
```

The source option materializes path/span/snapshot/content metadata plus exact
retained source through the existing plan/materialization pipeline. It rejects
missing/changed resources and incompatible purpose/repository/snapshot state.

A read-only demo over this repository's maintained command package queried
`timeout` with 12-line windows and overlap 3: file mode returned
`models/command.py` (lines 1-151); symbol mode returned `Command.with_timeout`
(132-141); window mode located `execution.py` (226-237). Mixed results preserved
their contributing native ranks. These are distinct useful views of the same
coding query, not a comparative retrieval-quality experiment.

### Established patterns reviewed

The [bounded Qwen coding consumer](../../../../../experiments/qwen/docs/overview.md#retrieved-context-markdown-coding-worker)
uses this API with caller-admitted source/tests, symbol selection and explicit
file expansion through Context. Host-owned acquisition exposes no second index,
ranking policy or model-controlled filesystem mutation.

[LlamaIndex CodeSplitter](https://developers.llamaindex.ai/python/framework-api-reference/node_parsers/code/)
uses syntax-aware code chunking, while its
[hierarchical parser](https://github.com/run-llama/llama_index/blob/main/llama-index-core/llama_index/core/node_parser/relational/hierarchical.py)
retains parent/child levels.
[LangChain PythonCodeTextSplitter](https://github.com/langchain-ai/langchain/blob/master/libs/text-splitters/langchain_text_splitters/python.py)
specializes recursive text splitting with Python separators.
[Aider's map](https://aider.chat/docs/repomap.html) uses Tree-sitter-derived symbol
structure; [Sourcegraph](https://sourcegraph.com/docs/code-search/types/symbol)
distinguishes symbol declarations from ordinary file/text results. These patterns
support explicit units and source lineage. Devtools already owns the required
AST coordinates, RI subjects, lexical scoring and disclosure contracts; adding
those libraries would not remove that integration work and is unnecessary here.

### Caller-selected source resources

`search_repository_source(index, query=..., mode=..., resource_addresses=...)`
accepts an explicit tuple of unique admitted RepositoryResourceAddress values.
None preserves existing full-index behavior; () selects nothing. Selected
resources constrain hits, supporting evidence and native match lists before
final result limits/consolidation. Corpus statistics and BM25 match evidence
remain those of the original admitted index; no smaller index is rebuilt.
SourceSearchResult records the exact requested tuple, separately from index
coverage. Invalid types, duplicates or resources without admitted file source
units are refused. No filesystem acquisition, new authorization or runtime
inference occurs. Retained exact-source disclosure still uses the same units.

The maintained coding application's opt-in repository-map Tool uses existing
map/Planning/source machinery; see [its native contract](../../../../../apps/qwen/README.md#opt-in-repository-map-navigation).
Deterministic Tool integration does not prove actual model adoption.
