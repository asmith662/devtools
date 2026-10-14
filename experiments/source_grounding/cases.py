# Copyright (c) 2026
# ruff: noqa: E501 -- prospective authored clauses
"""Minimum predicates authored from public tasks and their own parent frames."""

from typing import Any

CASES: dict[str, Any] = {
    "0020": {
        "position": 4,
        "basis": [
            "AGENTS.md",
            "src/devtools/context/retrieval/lexical/bm25.py",
            "tests/context/retrieval/lexical/test_bm25.py",
        ],
        "gap": "No blocking task interpretation gap. Filename weighting value/configuration and public API names are design freedom; do not infer a historical implementation.",
        "obligations": [
            {
                "id": "O1",
                "requirement": "Implement weighted filename BM25 retrieval.",
                "facts": "Existing content BM25, document/resource identities, filename text and lexical normalization, score combination and deterministic ordering.",
                "satisfaction": "Add a separately weighted filename contribution to repository BM25 acquisition using the native document frame; retain explainable contributions, positive-match behavior and deterministic ordering without replacing existing content analysis.",
                "exclusions": "No BM25F, term weighting, graph rank, query inference, prescribed child API or requirement to select a particular weight from this short task.",
                "need": "How can filename lexical evidence contribute alongside existing content BM25 while retaining exact document identities and deterministic ranking?",
                "query": "repository filename weighted BM25 lexical document retrieval score ranking",
            },
            {
                "id": "O2",
                "requirement": "Preserve and validate the parent retrieval contracts while integrating filename weighting.",
                "facts": "Unicode/casefold observations, frequency and empty-input contracts, settings validation, exports, tests and documentation ownership.",
                "satisfaction": "Preserve the existing content contribution; define filename-only and overlapping matches, validate any exposed weighting configuration and deterministic ties, and integrate under parent package/test/documentation conventions. If zero or disabled weighting is exposed it must reproduce content-only behavior; no new public toggle is required.",
                "exclusions": "No live repository service, persistence/index maintenance, production Context selection or unrelated architecture migration.",
                "need": "What analysis, identity, compatibility and test contracts constrain an independently weighted filename retrieval channel?",
                "query": "lexical filename content analysis unicode casefold deterministic empty validation tests",
            },
        ],
    },
    "0021": {
        "position": 5,
        "basis": [
            "src/devtools/model_serving/vllm.py",
            "src/devtools/model_serving/errors.py",
            "tests/model_serving/test_vllm.py",
        ],
        "gap": "No blocking task interpretation gap. Diagnostic representation, bounded volume and API names are design freedom; no provider/version feature is assumed.",
        "obligations": [
            {
                "id": "O1",
                "requirement": "Preserve vLLM startup failure diagnostics.",
                "facts": "Detached Docker launch, exact owned container identity, readiness polling, stopped-container and timeout exceptions, available diagnostic command/result surfaces.",
                "satisfaction": "Keep useful bounded launch/readiness failure context available to the caller when startup fails, including failures after a successful detached launch, rather than losing it during cleanup or replacing the original failure.",
                "exclusions": "No changed serving provider, speculative modern vLLM flags, general telemetry platform or live Docker execution requirement.",
                "need": "Where do vLLM startup, readiness and container diagnostics originate and where can failure context be lost?",
                "query": "vLLM startup failure readiness timeout container diagnostics logs error",
            },
            {
                "id": "O2",
                "requirement": "Preserve serving lifecycle safety and validate the diagnostic behavior.",
                "facts": "Owned-container cleanup, inspection failure, cancellation, bounded command outputs, readiness error contracts and fake-executor tests.",
                "satisfaction": "Maintain exact-container ownership, cleanup and exception lineage; diagnostic collection failure must not erase the primary startup failure. Test representative launch/readiness/diagnostic failures deterministically and document the supported boundary.",
                "exclusions": "No restart/retry policy, destructive changes to unrelated containers, service-management redesign or historical child test names.",
                "need": "Which ownership, cleanup, command failure and exception contracts must diagnostic preservation retain?",
                "query": "vLLM ownership cleanup startup exception command output diagnostic failure tests",
            },
        ],
    },
    "0022": {
        "position": 6,
        "basis": [
            "AGENTS.md",
            "src/devtools/context/python/function/declarations.py",
            "src/devtools/context/python/source_candidacy.py",
        ],
        "gap": "RESOLVED_WITH_EXPLICIT_QUALIFICATION: interpret declaration derivation as static source import syntax and provenance, including absolute/from/relative forms and aliases; do not require import resolution or runtime importability. Public API/layout and bounded traversal choices remain explicit design freedom.",
        "obligations": [
            {
                "id": "O1",
                "requirement": "Implement Python import declaration derivation.",
                "facts": "Observed Python resource content, AST source ranges, absolute/from/relative import syntax, alias entries, source occurrence and derivation identity conventions.",
                "satisfaction": "Derive deterministic static import declaration records from observed Python source, retaining syntactic form, module/name/alias/relative-level information as applicable and exact native source/frame provenance.",
                "exclusions": "No target resolution, import execution, runtime binding truth, graph traversal, guessed child symbols or prescribed new public type names.",
                "need": "How are static Python import syntax and individual declaration occurrences represented with exact source and derivation provenance?",
                "query": "python import declaration syntax from relative alias source occurrence derivation",
            },
            {
                "id": "O2",
                "requirement": "Bound, integrate and validate import declaration analysis.",
                "facts": "Existing Python source candidacy, native declaration analysis and coverage, parser errors, resource selection, identity separation, exports and test conventions.",
                "satisfaction": "State the supported static traversal/coverage boundary; preserve deterministic repeated declarations and aliases, distinguish parse failure from successful empty coverage, reject foreign inputs and integrate/test/document using parent RI conventions.",
                "exclusions": "No dependency discovery policy, module interpretation service, semantic relevance inference or general language framework.",
                "need": "Which native Python analysis, coverage and resource identity contracts constrain bounded import declaration derivation?",
                "query": "python declaration analysis coverage parser resource snapshot provenance deterministic tests",
            },
        ],
    },
}
