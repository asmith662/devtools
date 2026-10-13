# Case 0019 — direct structural discrimination Stage A

Stage B NOT EXECUTED; gold ABSENT; effectiveness NOT EVALUATED.

[Shared architecture/protocol](../../structural_discrimination/README.md) applies unchanged to all three cohort cases.

Original task:

Add vLLM CUDA graph estimate control

Exact prospective case record:

```json
{
  "ambiguities": [
    "Caller API and helper names are unspecified.",
    "The provider-specific control encoding is unspecified; no bool, environment variable or command flag name is assumed.",
    "No live GPU/model execution or provider-performance promise is implied."
  ],
  "authoring_basis_sha256": {
    "docs/architecture.md": "1be2714652a492ed2a70f35aaed5f9e0ad9b3e8b68328ff957727940ffd24bd2",
    "src/devtools/model_serving/docs/overview.md": "ccd724b4ee6f9885d8555f7f378e5033fbae8f55d376f046f87be2eff62f8bea",
    "src/devtools/model_serving/vllm.py": "822836fc5b922e9d24fb94cf733b925f9fbfc0e846fc196ba96278f41717a222",
    "tests/model_serving/test_vllm.py": "a2a6db57c7d347b0e1ca1d70f2ee9d0483c685ad4f3f8115f571e45d2405dc29"
  },
  "case_id": "case-0019",
  "exact_route": "NOT_APPLICABLE",
  "interpretation_gaps": [
    "The task/parent do not specify the provider option spelling, value domain, provider-version applicability or default. These are not invented from child knowledge. The freeze evaluates repository integration evidence for the stated control; Stage C must retain any residual task/provider-contract gap rather than assume complete task satisfaction."
  ],
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
      "excluded_interpretation": "No automatic tuning, new serving-provider framework, assumed field name/type/default or global GPU-memory policy.",
      "facts_to_discover": "Existing immutable provider-specific serving configuration, structural validation and established caller-selected option conventions.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O1",
      "information_need_identity": "N1",
      "need": "How are explicit provider configuration choices represented and validated so a CUDA graph estimation control can be added without changing existing defaults?",
      "obligation_identity": {
        "task": "case-0019:historical-development-003",
        "value": "O1"
      },
      "query": "vLLM CUDA graph estimate control serving configuration validation defaults",
      "query_association": "O1",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0019:historical-development-003",
        "value": "Q1"
      },
      "requirement": "Expose an explicit caller-selected vLLM CUDA graph estimation control.",
      "satisfaction": "Represent the caller's CUDA graph estimation choice coherently in the existing provider configuration, with validation appropriate to its supported provider contract and reproducible retention; omission preserves the parent launch behavior.",
      "task_backed_source_span": {
        "end": 36,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No guessed provider option, server mutation, model invocation, benchmark tuning or live Docker acceptance in this retrieval experiment.",
      "facts_to_discover": "Deterministic Docker/provider argv/environment construction, pinned model/image configuration, option forwarding and owned-container lifecycle/readiness/error boundaries.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O2",
      "information_need_identity": "N2",
      "need": "Where and under which lifecycle constraints are caller settings translated into reproducible provider launch arguments or environment values?",
      "obligation_identity": {
        "task": "case-0019:historical-development-003",
        "value": "O2"
      },
      "query": "vLLM launch command Docker environment arguments configuration ownership readiness",
      "query_association": "O2",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0019:historical-development-003",
        "value": "Q2"
      },
      "requirement": "Propagate the explicit estimation control through the owned vLLM launch.",
      "satisfaction": "Forward an explicit supported choice faithfully through the existing launch representation, preserve unrelated options and omission behavior, and keep ownership/readiness/error semantics unchanged; do not claim provider runtime effects absent external proof.",
      "task_backed_source_span": {
        "end": 36,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    },
    {
      "excluded_interpretation": "No hardware latency/accuracy guarantee, external-provider implementation claim, new benchmark or inferred child test wording.",
      "facts_to_discover": "Existing mocked configuration and command-construction tests, disabled/default versus explicit option conventions and serving documentation authority.",
      "future_action": "one canonical A acquisition followed by annotation of the unchanged native result",
      "id": "O3",
      "information_need_identity": "N3",
      "need": "Which existing no-live-service tests and serving documentation constrain validation of a new caller-selected launch control?",
      "obligation_identity": {
        "task": "case-0019:historical-development-003",
        "value": "O3"
      },
      "query": "vLLM serving configuration launch tests explicit optional settings documentation",
      "query_association": "O3",
      "query_derivation": "One unweighted natural-language serialization of the authored need, using task/parent concepts only; no output tuning",
      "query_identity": {
        "task": "case-0019:historical-development-003",
        "value": "Q3"
      },
      "requirement": "Document and validate the control's bounded configuration/launch contract.",
      "satisfaction": "Add focused no-live-service checks for omitted, explicit and invalid control input/forwarding as applicable, document the supported contract and limits, and preserve existing configuration and lifecycle tests.",
      "task_backed_source_span": {
        "end": 36,
        "start": 0
      },
      "task_interpretation": "Caller-authored minimum implementation predicate; the source span supplies the task, not a claim that every criterion is verbatim original text"
    }
  ],
  "parent_frame": {
    "corpus_id": "eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6",
    "python_resource_count": 182,
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 222,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
    "source_head": "2465af00dc305a6c2a15a90455bf09e62e428e39",
    "source_tree": "12a504a2106467d8b32fc062d15923c7b9250fd9"
  },
  "population_case_id": "historical-development-003",
  "public_task_card": {
    "case_id": "historical-development-003",
    "frame": {
      "kind": "GIT_PARENT_TREE",
      "native_repository_snapshot": "NOT_CONSTRUCTED",
      "parent_commit": "2465af00dc305a6c2a15a90455bf09e62e428e39",
      "parent_tree": "12a504a2106467d8b32fc062d15923c7b9250fd9"
    },
    "population_id": "devtools-historical-development-extension-v1",
    "schema": "historical-development-public-task-v1",
    "selection_position": 3,
    "task_source": {
      "kind": "EXACT_ORIGINAL_GIT_COMMIT_MESSAGE",
      "provenance_reference": "historical-development-003/commit-message",
      "task_sha256": "3d50e75a9e222adf01648aaa7276f1e36d02c0c74ad86c22715a63bf2b1a09b1"
    },
    "task_text": "Add vLLM CUDA graph estimate control\n",
    "title": "Add vLLM CUDA graph estimate control"
  },
  "schema": "direct-structural-discrimination-case-stage-a-v1",
  "shared_protocol_sha256": "6167a9b28da52ce42ac7c9186fade322a078a3f5158ba87067b1c3cf4df0b52f",
  "status": "STAGE_A_FROZEN; STAGE_B_NOT_EXECUTED; GOLD_ABSENT; EFFECTIVENESS_NOT_EVALUATED",
  "task_identity": "case-0019:historical-development-003",
  "task_provenance": {
    "explanation": "Exact original commit message; minimum predicates interpreted from own parent only",
    "source_sha256": "3d50e75a9e222adf01648aaa7276f1e36d02c0c74ad86c22715a63bf2b1a09b1"
  },
  "task_text": "Add vLLM CUDA graph estimate control\n"
}
```

All parent identities: frame.json; exact included parent content: resources.json.gz. blind_spec.json is an input allowlist for later clean adjudication, not gold. No child implementation, changed paths or diff is available here.
