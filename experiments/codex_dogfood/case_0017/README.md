# Case 0017 — direct structural discrimination Stage A

Stage B NOT EXECUTED; gold ABSENT; effectiveness NOT EVALUATED.

[Shared architecture/protocol](../../structural_discrimination/README.md) applies unchanged to all three cohort cases.

Original task:

Implement repository lexical statistics and inverted index

Exact prospective case record:

```json
{
  "ambiguities": [
    "Public type/helper names and package layout are unspecified.",
    "Index representation and construction API are unspecified; no scoring/ranking capability is requested."
  ],
  "authoring_basis_sha256": {
    "AGENTS.md": "60afe4779d59d7c9ebe6e029cc60ab148301c6c87502547a198e7ba6d929061c",
    "docs/architecture.md": "3049475fe0e4682eb056ba00812a81c4e3be61f9ea6a8d5f8581f81eacaa84a3",
    "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md": "9e675dde5dd6838d69438d66e8b13dce075788bc1a8692e8f25ca7c5878688c4",
    "src/devtools/context/retrieval/lexical.py": "7f900f80a348047086f40d67f1d72135441edefc67f1e2ce844f18b7bc40ba2b",
    "tests/context/retrieval/test_lexical.py": "f2da2189b6ab56409897ca03e8e6f963b88136db7ae3ac3aa548fd472ab4cff1"
  },
  "case_id": "case-0017",
  "exact_route": "NOT_APPLICABLE",
  "interpretation_gaps": [],
  "no_execution": {
    "bm25": 0,
    "exact_lookup": 0,
    "gold": 0,
    "local_pairs": 0,
    "pagerank": 0,
    "reference_derivation": 0,
    "rrf": 0,
    "semantic_reviewer": 0,
    "structural_annotation": 0
  },
  "obligations": [
    {
      "excluded_interpretation": "No new tokenizer, identifier splitting, BM25 score, ranking or resource acquisition.",
      "facts_to_discover": "Retained whole-document lexical observations, their normalized terms, repetition, exact document/resource identity and collection ordering.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O1",
      "information_need_identity": "N1",
      "need": "Which native observations and collection identities determine document/corpus lexical frequency and length statistics without changing text analysis?",
      "obligation_identity": {
        "task": "case-0017:historical-development-001",
        "value": "O1"
      },
      "query": "repository lexical document corpus term frequency statistics",
      "query_association": "O1",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0017:historical-development-001",
        "value": "Q1"
      },
      "requirement": "Implement repository lexical statistics.",
      "satisfaction": "Derive deterministic document term frequencies/lengths and corpus document counts, document frequencies and average document length from existing lexical observations, accounting explicitly for empty documents/collections and preserving provenance.",
      "task_backed_source_span": {
        "end": 58,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No query execution, relevance score, rank, persistent index service or incremental maintenance system.",
      "facts_to_discover": "Observed lexical terms and exact documents/resources to which their occurrences belong; deterministic collection order.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O2",
      "information_need_identity": "N2",
      "need": "How should normalized terms index the exact retained documents and their frequency evidence while preserving native repository provenance?",
      "obligation_identity": {
        "task": "case-0017:historical-development-001",
        "value": "O2"
      },
      "query": "lexical inverted index term postings document occurrences resource identity",
      "query_association": "O2",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0017:historical-development-001",
        "value": "Q2"
      },
      "requirement": "Implement a repository inverted index.",
      "satisfaction": "Provide deterministic term-to-document postings based on the lexical statistics/observations, retaining document identity and frequency information without rescanning the filesystem or claiming relevance.",
      "task_backed_source_span": {
        "end": 58,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No unrelated architectural migration, child-specific API names or treatment-dependent tests.",
      "facts_to_discover": "Heterogeneous Unicode word/casefold analysis, public exports, test/validation conventions and separation of observation, statistics, retrieval and Context selection.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O3",
      "information_need_identity": "N3",
      "need": "What compatibility and validation contracts must the new statistics/index preserve at the existing lexical-analysis and repository-document boundaries?",
      "obligation_identity": {
        "task": "case-0017:historical-development-001",
        "value": "O3"
      },
      "query": "lexical analysis unicode word casefold ordered observations empty corpus deterministic tests exports",
      "query_association": "O3",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0017:historical-development-001",
        "value": "Q3"
      },
      "requirement": "Integrate and validate the statistics/index capability under the parent repository contracts.",
      "satisfaction": "Keep existing lexical observations unchanged, expose the capability coherently, document its boundary and validate deterministic heterogeneous, repeated-term and empty-input behavior using the parent development conventions.",
      "task_backed_source_span": {
        "end": 58,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    }
  ],
  "parent_frame": {
    "corpus_id": "32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91",
    "python_resource_count": 262,
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 357,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
    "source_head": "71e938d809d794f2f07dd30cb772f1e9bc89c9d3",
    "source_tree": "d6c9398be0bf36e16d6bf57a65f16d5f513eab00"
  },
  "population_case_id": "historical-development-001",
  "public_task_card": {
    "case_id": "historical-development-001",
    "frame": {
      "kind": "GIT_PARENT_TREE",
      "native_repository_snapshot": "NOT_CONSTRUCTED",
      "parent_commit": "71e938d809d794f2f07dd30cb772f1e9bc89c9d3",
      "parent_tree": "d6c9398be0bf36e16d6bf57a65f16d5f513eab00"
    },
    "population_id": "devtools-historical-development-extension-v1",
    "schema": "historical-development-public-task-v1",
    "selection_position": 1,
    "task_source": {
      "kind": "EXACT_ORIGINAL_GIT_COMMIT_MESSAGE",
      "provenance_reference": "historical-development-001/commit-message",
      "task_sha256": "d1f9e3c61d35d350e0859e2fb02595d46a8baf8e6323aed736497f1ea2ed7d43"
    },
    "task_text": "Implement repository lexical statistics and inverted index\n",
    "title": "Implement repository lexical statistics and inverted index"
  },
  "schema": "direct-structural-discrimination-case-stage-a-v1",
  "shared_protocol_sha256": "6167a9b28da52ce42ac7c9186fade322a078a3f5158ba87067b1c3cf4df0b52f",
  "status": "STAGE_A_FROZEN; STAGE_B_NOT_EXECUTED; GOLD_ABSENT; EFFECTIVENESS_NOT_EVALUATED",
  "task_identity": "case-0017:historical-development-001",
  "task_provenance": {
    "explanation": "Exact original commit message; minimum predicates interpreted from own parent only",
    "source_sha256": "d1f9e3c61d35d350e0859e2fb02595d46a8baf8e6323aed736497f1ea2ed7d43"
  },
  "task_text": "Implement repository lexical statistics and inverted index\n"
}
```

All parent identities: frame.json; exact included parent content: resources.json.gz. blind_spec.json is an input allowlist for later clean adjudication, not gold. No child implementation, changed paths or diff is available here.
