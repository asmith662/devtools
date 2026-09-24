# Copyright (c) 2026
# ruff: noqa: E501
"""Retain blinded, purpose-relative judgments for the 69 neutral pairs."""

from __future__ import annotations

import json
from pathlib import Path

from experiments.increment_26.development_judgments import (
    DEVELOPMENT_CASE_IDS,
    NEW_PROVENANCE,
    freeze_development_judgments,
)

_INPUT = Path("experiments/increment_26/development_judgment_input.json")
_OUTPUT = Path("experiments/increment_26/development_frozen_judgments.json")

# Decisions are indexed only by the committed blinded input's neutral order.
# U=USEFUL, N=NOT_USEFUL, ?=UNJUDGED. No candidate evidence is read here.
DECISIONS: dict[str, tuple[tuple[str, str], ...]] = {
    "i25-66ed2049de72": (
        (
            "N",
            "Core package marker contains no Python declaration derivation behavior.",
        ),
        (
            "N",
            "Conversion package marker concerns callable conversion, not Python declarations.",
        ),
        (
            "N",
            "Identity documentation concerns ID lifecycle rather than AST declarations.",
        ),
        ("N", "Path documentation concerns path values rather than function syntax."),
        ("N", "Path resolution documentation does not derive Python declarations."),
        ("N", "Timestamp documentation does not address Python syntax analysis."),
        ("N", "Model tool-call values are unrelated to deriving Python functions."),
        ("N", "Command value documentation does not address Python declarations."),
        ("N", "Conversion test package marker contains no declaration behavior."),
        (
            "N",
            "Model-interaction Evidence tests do not exercise Python declaration derivation.",
        ),
    ),
    "i25-858bfa85787e": (
        (
            "U",
            "Repository public API exposes resource, snapshot, and text-corpus representations.",
        ),
        (
            "U",
            "Defines addressed text occurrences and content identity used by repository documents.",
        ),
        (
            "U",
            "Defines the parent repository snapshot and its addressed resource lookup.",
        ),
        ("N", "Timestamp documentation does not define repository text documents."),
        ("N", "Tool overview does not define repository document representation."),
        ("N", "Context test package marker has no document behavior."),
        ("N", "Repository test package marker has no document behavior."),
        (
            "U",
            "Corpus tests exercise selected repository resources and snapshot membership.",
        ),
        (
            "N",
            "Markdown codec tests concern file decoding, not repository document identity.",
        ),
    ),
    "i25-6f304a8c737c": (
        (
            "U",
            "Runtime invokes ModelInteraction through the request boundary and retains its response.",
        ),
        (
            "U",
            "Package overview describes Prompt, ModelInteraction, and ModelResponse ownership.",
        ),
        ("U", "Defines values exchanged at the model invocation boundary."),
        ("U", "Defines the ModelInteraction send protocol and request parameters."),
        (
            "N",
            "Model-interaction test package marker has no request-boundary behavior.",
        ),
        ("U", "Provider tests exercise translation of model requests and responses."),
        (
            "U",
            "Value tests exercise request constraints and model-boundary invariants.",
        ),
    ),
    "i25-bb9f807bcd61": (
        (
            "U",
            "Defines established direct Python function declaration knowledge selected by name.",
        ),
        ("U", "Selects and discloses exact-name function retrieval results."),
        (
            "N",
            "Renders already selected Context and does not choose resources by name.",
        ),
        (
            "U",
            "Implements literal exact-name retrieval over declared Python functions.",
        ),
        (
            "U",
            "Cross-resource tests show exact-name matches reaching request assembly.",
        ),
        ("U", "Disclosure tests verify exact-name selection and all-match projection."),
        ("N", "Rendering tests cover downstream text output after resource selection."),
        (
            "U",
            "Retrieval tests verify literal name matching and ordered result evidence.",
        ),
    ),
    "i25-0f7a13667ef3": (
        ("U", "Evidence public exports include terminal Attempt evidence values."),
        (
            "U",
            "Documents terminal Evidence outcomes and the Runtime producer boundary.",
        ),
        (
            "U",
            "Defines immutable terminal Evidence and Attempt stages used at Runtime completion.",
        ),
        (
            "N",
            "Persistence overview concerns Session storage, not terminal Evidence delivery.",
        ),
        ("U", "Runtime terminalizes Attempts and calls its observer at completion."),
        ("N", "Evidence test package marker has no production or delivery behavior."),
        ("U", "Terminal Evidence tests verify the values produced after Attempts end."),
    ),
    "i25-739c82bd3398": (
        ("N", "Models package marker has no reasoning-content representation."),
        ("N", "Prompt contains input text and role, not model reasoning output."),
        (
            "U",
            "ModelResponse defines model output content and provider facts to extend for reasoning.",
        ),
        (
            "N",
            "JSON filesystem codec concerns file representation, not model reasoning.",
        ),
        (
            "N",
            "Markdown filesystem codec concerns file representation, not model reasoning.",
        ),
        (
            "N",
            "Text filesystem codec concerns file representation, not model reasoning.",
        ),
        ("N", "Filesystem I/O documentation does not define model reasoning content."),
        ("N", "JSON file-model documentation does not define model reasoning content."),
        (
            "N",
            "Protocol test exercises generic sends and does not inspect reasoning output.",
        ),
        ("N", "Model-serving test package marker has no reasoning-content behavior."),
    ),
    "i25-9efe3dc31e80": (
        (
            "U",
            "ModelInteraction overview establishes the request and response boundary where an output bound belongs.",
        ),
        (
            "N",
            "Current values only define source and continuation IDs, not request output limits.",
        ),
        (
            "N",
            "ModelResponse retains output and usage but does not constrain requested output length.",
        ),
        (
            "N",
            "Command output retention policy bounds subprocess output, not model tokens.",
        ),
        (
            "N",
            "Filesystem roadmap concerns file reads and writes, not model output limits.",
        ),
        ("N", "Model-interaction test package marker has no output-bound behavior."),
        (
            "?",
            "Existing value tests describe model output but do not establish whether new output-bound validation belongs here.",
        ),
        (
            "U",
            "Protocol test supplies the existing send signature that a request output bound would extend.",
        ),
    ),
    "i25-6b0e9c52fb26": (
        (
            "N",
            "Model-interaction observation records invocation facts, not repository snapshots.",
        ),
        (
            "N",
            "Model-serving documentation concerns endpoints rather than repository observation.",
        ),
        ("N", "Observability Evidence exports do not define repository snapshots."),
        (
            "N",
            "Evidence overview concerns model invocation capture, not repository observation.",
        ),
        (
            "N",
            "Model-interaction Evidence captures provider exchanges, not repository resources.",
        ),
        (
            "N",
            "Command documentation concerns subprocess execution rather than repository snapshots.",
        ),
        ("N", "Tool overview does not define bounded repository snapshot observation."),
        (
            "?",
            "Repository file Tool performs bounded reads, but its role in snapshot observation is unclear from this content.",
        ),
        ("N", "Model benchmark tests do not exercise repository resource observation."),
        (
            "N",
            "Hugging Face serving tests do not exercise repository resource observation.",
        ),
    ),
}


def main() -> None:
    """Freeze the already-adjudicated neutral population without opening origins."""
    blinded_bytes = _INPUT.read_bytes()
    blinded = json.loads(blinded_bytes)
    if tuple(case["case_id"] for case in blinded["cases"]) != DEVELOPMENT_CASE_IDS:
        msg = "Blinded input differs from the development partition."
        raise ValueError(msg)
    decisions: dict[str, dict[str, dict[str, str]]] = {}
    labels = {"U": "useful", "N": "not-useful", "?": "unjudged"}
    for case in blinded["cases"]:
        case_id = case["case_id"]
        items = DECISIONS[case_id]
        addresses = [resource["address"] for resource in case["resources"]]
        if len(items) != len(addresses):
            msg = f"Judgment decision count differs for {case_id}."
            raise ValueError(msg)
        decisions[case_id] = {
            address: {
                "judgment": labels[label],
                "rationale": rationale,
                "provenance": NEW_PROVENANCE,
            }
            for address, (label, rationale) in zip(addresses, items, strict=True)
        }
    frozen = freeze_development_judgments(
        blinded_bytes=blinded_bytes,
        decisions=decisions,
    )
    _OUTPUT.write_text(
        json.dumps(frozen, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
