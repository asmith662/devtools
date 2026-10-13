# Copyright (c) 2026
# ruff: noqa: E501, COM812 -- exact authored prospective task/need clauses
"""Minimum obligations authored only from each task and its own parent frame.

No child metadata, gold, rankings or Reference evidence is an authoring input.
Case 0017's clauses were fixed before inspecting Case 0018/0019 source semantics.
"""

from __future__ import annotations

from typing import Any

AUTHORING = "Task -> minimum mandatory predicates -> uncertainties -> one plain-language query each; parent architecture/source/tests constrain compatibility, never child or retrieval outputs. No exact locator is present in these original task messages."

CASES: dict[str, Any] = {
    "0017": {
        "population_case": "historical-development-001",
        "task_text": "Implement repository lexical statistics and inverted index\n",
        "authoring_basis": [
            "AGENTS.md",
            "docs/architecture.md",
            "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
            "src/devtools/context/retrieval/lexical.py",
            "tests/context/retrieval/test_lexical.py",
        ],
        "interpretation_gaps": [],
        "ambiguities": [
            "Public type/helper names and package layout are unspecified.",
            "Index representation and construction API are unspecified; no scoring/ranking capability is requested.",
        ],
        "obligations": [
            {
                "id": "O1",
                "requirement": "Implement repository lexical statistics.",
                "facts_to_discover": "Retained whole-document lexical observations, their normalized terms, repetition, exact document/resource identity and collection ordering.",
                "satisfaction": "Derive deterministic document term frequencies/lengths and corpus document counts, document frequencies and average document length from existing lexical observations, accounting explicitly for empty documents/collections and preserving provenance.",
                "excluded_interpretation": "No new tokenizer, identifier splitting, BM25 score, ranking or resource acquisition.",
                "need": "Which native observations and collection identities determine document/corpus lexical frequency and length statistics without changing text analysis?",
                "query": "repository lexical document corpus term frequency statistics",
            },
            {
                "id": "O2",
                "requirement": "Implement a repository inverted index.",
                "facts_to_discover": "Observed lexical terms and exact documents/resources to which their occurrences belong; deterministic collection order.",
                "satisfaction": "Provide deterministic term-to-document postings based on the lexical statistics/observations, retaining document identity and frequency information without rescanning the filesystem or claiming relevance.",
                "excluded_interpretation": "No query execution, relevance score, rank, persistent index service or incremental maintenance system.",
                "need": "How should normalized terms index the exact retained documents and their frequency evidence while preserving native repository provenance?",
                "query": "lexical inverted index term postings document occurrences resource identity",
            },
            {
                "id": "O3",
                "requirement": "Integrate and validate the statistics/index capability under the parent repository contracts.",
                "facts_to_discover": "Heterogeneous Unicode word/casefold analysis, public exports, test/validation conventions and separation of observation, statistics, retrieval and Context selection.",
                "satisfaction": "Keep existing lexical observations unchanged, expose the capability coherently, document its boundary and validate deterministic heterogeneous, repeated-term and empty-input behavior using the parent development conventions.",
                "excluded_interpretation": "No unrelated architectural migration, child-specific API names or treatment-dependent tests.",
                "need": "What compatibility and validation contracts must the new statistics/index preserve at the existing lexical-analysis and repository-document boundaries?",
                "query": "lexical analysis unicode word casefold ordered observations empty corpus deterministic tests exports",
            },
        ],
    },
    "0018": {
        "population_case": "historical-development-002",
        "task_text": "Implement qualified repository import relations\n",
        "authoring_basis": [
            "AGENTS.md",
            "docs/architecture.md",
            "src/devtools/context/python/imports/declarations.py",
            "src/devtools/context/python/imports/resolution.py",
            "src/devtools/context/python/modules/interpretation.py",
            "tests/context/python/imports/test_resolution.py",
        ],
        "interpretation_gaps": [],
        "ambiguities": [
            "New relation type/helper names and representation are unspecified.",
            "Only the bounded module portion of imports is required; imported-member/runtime semantics are excluded by parent contracts.",
        ],
        "obligations": [
            {
                "id": "O1",
                "requirement": "Represent qualified repository import relationships from established import resolution.",
                "facts_to_discover": "Source declaration occurrence and source module/resource, uniquely resolved target module/resource, explicit interpretation universe and native identity dependencies.",
                "satisfaction": "Establish a directed source-to-target repository relation only from a unique positive bounded import-module resolution, retaining declaration, source/target resource content, snapshot and interpretation provenance.",
                "excluded_interpretation": "No runtime importability, imported-member binding, synthetic reverse edges or external dependency truth.",
                "need": "Which native import declaration, resolution and module interpretation evidence supports a qualified source-to-target repository relationship?",
                "query": "qualified repository module import relation source target snapshot provenance",
            },
            {
                "id": "O2",
                "requirement": "Preserve qualified nonpositive and ambiguous import outcomes.",
                "facts_to_discover": "Absolute/relative module-portion rules, multiple module roots, missing/ambiguous sources, unresolved targets, unsupported relative levels and universe-qualified absence.",
                "satisfaction": "Do not turn unresolved, ambiguous, unsupported or stale/foreign resolution into a positive relation; retain bounded disposition and provenance, with deterministic duplicate/occurrence accounting.",
                "excluded_interpretation": "No guessing by path, root precedence, target-first selection or external-versus-missing classification.",
                "need": "What resolution and frame guards prevent unsupported or competing import interpretations from becoming unqualified repository relations?",
                "query": "import resolution resolved ambiguous unsupported module universe relative repository identity",
            },
            {
                "id": "O3",
                "requirement": "Integrate and validate qualified import relations without changing existing import truth.",
                "facts_to_discover": "Existing declarations/resolutions/module universe APIs, tests and documentation authority; static repository truth versus Retrieval and runtime behavior.",
                "satisfaction": "Reuse parent import/module primitives, expose and document the bounded relation capability, and test positive, nonpositive, relative, duplicate and changed-frame behavior without adding ranking or runtime execution.",
                "excluded_interpretation": "No new retrieval treatment, recursive import closure, generic graph framework or child-specific API shape.",
                "need": "How can the relation consumer integrate with existing import/module identities and validation while preserving the static Repository Intelligence boundary?",
                "query": "python import declarations module interpretation relations deterministic tests static repository intelligence",
            },
        ],
    },
    "0019": {
        "population_case": "historical-development-003",
        "task_text": "Add vLLM CUDA graph estimate control\n",
        "authoring_basis": [
            "docs/architecture.md",
            "src/devtools/model_serving/vllm.py",
            "src/devtools/model_serving/docs/overview.md",
            "tests/model_serving/test_vllm.py",
        ],
        "interpretation_gaps": [
            "The task/parent do not specify the provider option spelling, value domain, provider-version applicability or default. These are not invented from child knowledge. The freeze evaluates repository integration evidence for the stated control; Stage C must retain any residual task/provider-contract gap rather than assume complete task satisfaction."
        ],
        "ambiguities": [
            "Caller API and helper names are unspecified.",
            "The provider-specific control encoding is unspecified; no bool, environment variable or command flag name is assumed.",
            "No live GPU/model execution or provider-performance promise is implied.",
        ],
        "obligations": [
            {
                "id": "O1",
                "requirement": "Expose an explicit caller-selected vLLM CUDA graph estimation control.",
                "facts_to_discover": "Existing immutable provider-specific serving configuration, structural validation and established caller-selected option conventions.",
                "satisfaction": "Represent the caller's CUDA graph estimation choice coherently in the existing provider configuration, with validation appropriate to its supported provider contract and reproducible retention; omission preserves the parent launch behavior.",
                "excluded_interpretation": "No automatic tuning, new serving-provider framework, assumed field name/type/default or global GPU-memory policy.",
                "need": "How are explicit provider configuration choices represented and validated so a CUDA graph estimation control can be added without changing existing defaults?",
                "query": "vLLM CUDA graph estimate control serving configuration validation defaults",
            },
            {
                "id": "O2",
                "requirement": "Propagate the explicit estimation control through the owned vLLM launch.",
                "facts_to_discover": "Deterministic Docker/provider argv/environment construction, pinned model/image configuration, option forwarding and owned-container lifecycle/readiness/error boundaries.",
                "satisfaction": "Forward an explicit supported choice faithfully through the existing launch representation, preserve unrelated options and omission behavior, and keep ownership/readiness/error semantics unchanged; do not claim provider runtime effects absent external proof.",
                "excluded_interpretation": "No guessed provider option, server mutation, model invocation, benchmark tuning or live Docker acceptance in this retrieval experiment.",
                "need": "Where and under which lifecycle constraints are caller settings translated into reproducible provider launch arguments or environment values?",
                "query": "vLLM launch command Docker environment arguments configuration ownership readiness",
            },
            {
                "id": "O3",
                "requirement": "Document and validate the control's bounded configuration/launch contract.",
                "facts_to_discover": "Existing mocked configuration and command-construction tests, disabled/default versus explicit option conventions and serving documentation authority.",
                "satisfaction": "Add focused no-live-service checks for omitted, explicit and invalid control input/forwarding as applicable, document the supported contract and limits, and preserve existing configuration and lifecycle tests.",
                "excluded_interpretation": "No hardware latency/accuracy guarantee, external-provider implementation claim, new benchmark or inferred child test wording.",
                "need": "Which existing no-live-service tests and serving documentation constrain validation of a new caller-selected launch control?",
                "query": "vLLM serving configuration launch tests explicit optional settings documentation",
            },
        ],
    },
}
