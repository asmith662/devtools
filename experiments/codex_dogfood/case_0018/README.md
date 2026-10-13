# Case 0018 — direct structural discrimination Stage A

Stage B NOT EXECUTED; gold ABSENT; effectiveness NOT EVALUATED.

[Shared architecture/protocol](../../structural_discrimination/README.md) applies unchanged to all three cohort cases.

Original task:

Implement qualified repository import relations

Exact prospective case record:

```json
{
  "ambiguities": [
    "New relation type/helper names and representation are unspecified.",
    "Only the bounded module portion of imports is required; imported-member/runtime semantics are excluded by parent contracts."
  ],
  "authoring_basis_sha256": {
    "AGENTS.md": "f4f697a819463771b8805a312777435de41e7270741cbd607354a979122c08f5",
    "docs/architecture.md": "a875c1413841f5edfa98819a971d0ca52b91e24c98a69cabc464ce868e05bee0",
    "src/devtools/context/python/imports/declarations.py": "556d2752adf7bec22cf17fc5cdf886c6bf1933654b5904a27dab92a6cac25178",
    "src/devtools/context/python/imports/resolution.py": "f8826818723cf63ff6e6b735a20bc7fceb4c68fcb90454f98a0931349f45675c",
    "src/devtools/context/python/modules/interpretation.py": "513c653a2f35578ff2cfeb19cc96badd6de10688c0c5bf2732a04ac2ec84d14c",
    "tests/context/python/imports/test_resolution.py": "81008500a67f3898e5c707ce6617feda178c2a6b0c00fdd4f81eb4f43e7543e8"
  },
  "case_id": "case-0018",
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
      "excluded_interpretation": "No runtime importability, imported-member binding, synthetic reverse edges or external dependency truth.",
      "facts_to_discover": "Source declaration occurrence and source module/resource, uniquely resolved target module/resource, explicit interpretation universe and native identity dependencies.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O1",
      "information_need_identity": "N1",
      "need": "Which native import declaration, resolution and module interpretation evidence supports a qualified source-to-target repository relationship?",
      "obligation_identity": {
        "task": "case-0018:historical-development-002",
        "value": "O1"
      },
      "query": "qualified repository module import relation source target snapshot provenance",
      "query_association": "O1",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0018:historical-development-002",
        "value": "Q1"
      },
      "requirement": "Represent qualified repository import relationships from established import resolution.",
      "satisfaction": "Establish a directed source-to-target repository relation only from a unique positive bounded import-module resolution, retaining declaration, source/target resource content, snapshot and interpretation provenance.",
      "task_backed_source_span": {
        "end": 47,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No guessing by path, root precedence, target-first selection or external-versus-missing classification.",
      "facts_to_discover": "Absolute/relative module-portion rules, multiple module roots, missing/ambiguous sources, unresolved targets, unsupported relative levels and universe-qualified absence.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O2",
      "information_need_identity": "N2",
      "need": "What resolution and frame guards prevent unsupported or competing import interpretations from becoming unqualified repository relations?",
      "obligation_identity": {
        "task": "case-0018:historical-development-002",
        "value": "O2"
      },
      "query": "import resolution resolved ambiguous unsupported module universe relative repository identity",
      "query_association": "O2",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0018:historical-development-002",
        "value": "Q2"
      },
      "requirement": "Preserve qualified nonpositive and ambiguous import outcomes.",
      "satisfaction": "Do not turn unresolved, ambiguous, unsupported or stale/foreign resolution into a positive relation; retain bounded disposition and provenance, with deterministic duplicate/occurrence accounting.",
      "task_backed_source_span": {
        "end": 47,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No new retrieval treatment, recursive import closure, generic graph framework or child-specific API shape.",
      "facts_to_discover": "Existing declarations/resolutions/module universe APIs, tests and documentation authority; static repository truth versus Retrieval and runtime behavior.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O3",
      "information_need_identity": "N3",
      "need": "How can the relation consumer integrate with existing import/module identities and validation while preserving the static Repository Intelligence boundary?",
      "obligation_identity": {
        "task": "case-0018:historical-development-002",
        "value": "O3"
      },
      "query": "python import declarations module interpretation relations deterministic tests static repository intelligence",
      "query_association": "O3",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0018:historical-development-002",
        "value": "Q3"
      },
      "requirement": "Integrate and validate qualified import relations without changing existing import truth.",
      "satisfaction": "Reuse parent import/module primitives, expose and document the bounded relation capability, and test positive, nonpositive, relative, duplicate and changed-frame behavior without adding ranking or runtime execution.",
      "task_backed_source_span": {
        "end": 47,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    }
  ],
  "parent_frame": {
    "corpus_id": "7ce2a9e4a048fcb3d1a4e8c625be8c951a84dc0c5cac70809c6427a8bb50eb33",
    "python_resource_count": 287,
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 382,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "bf0f8d2a30e2be56053a2098a4800ad3d43a70c41707b618ad36c197b6b6b827",
    "source_head": "d493c26bbb1866cb9e5ead8f23f02aac3a7f12b9",
    "source_tree": "be89449e1f2c89c307130868aa51cf9e717a2f49"
  },
  "population_case_id": "historical-development-002",
  "public_task_card": {
    "case_id": "historical-development-002",
    "frame": {
      "kind": "GIT_PARENT_TREE",
      "native_repository_snapshot": "NOT_CONSTRUCTED",
      "parent_commit": "d493c26bbb1866cb9e5ead8f23f02aac3a7f12b9",
      "parent_tree": "be89449e1f2c89c307130868aa51cf9e717a2f49"
    },
    "population_id": "devtools-historical-development-extension-v1",
    "schema": "historical-development-public-task-v1",
    "selection_position": 2,
    "task_source": {
      "kind": "EXACT_ORIGINAL_GIT_COMMIT_MESSAGE",
      "provenance_reference": "historical-development-002/commit-message",
      "task_sha256": "c540758bc3ab5600a985737892b93beb9045e7c56f00f44ef78ada4ab4369c97"
    },
    "task_text": "Implement qualified repository import relations\n",
    "title": "Implement qualified repository import relations"
  },
  "schema": "direct-structural-discrimination-case-stage-a-v1",
  "shared_protocol_sha256": "6167a9b28da52ce42ac7c9186fade322a078a3f5158ba87067b1c3cf4df0b52f",
  "status": "STAGE_A_FROZEN; STAGE_B_NOT_EXECUTED; GOLD_ABSENT; EFFECTIVENESS_NOT_EVALUATED",
  "task_identity": "case-0018:historical-development-002",
  "task_provenance": {
    "explanation": "Exact original commit message; minimum predicates interpreted from own parent only",
    "source_sha256": "c540758bc3ab5600a985737892b93beb9045e7c56f00f44ef78ada4ab4369c97"
  },
  "task_text": "Implement qualified repository import relations\n"
}
```

All parent identities: frame.json; exact included parent content: resources.json.gz. blind_spec.json is an input allowlist for later clean adjudication, not gold. No child implementation, changed paths or diff is available here.
