# Copyright (c) 2026
# ruff: noqa: E501, EM101, TRY003 -- finite review budget guidance
"""Shared review-only budget visibility and reserved synthesis; never authority."""

from typing import Any

COMPLETION = {
    "schema": "native-review-completion-v1",
    "reserved_model_calls": 1,
    "known_refusals": "correlated-zero-effects-v1",
}


def view(
    packet: dict[str, Any],
    calls: int,
    reads: int,
    *,
    diagnostic: bool = True,
) -> dict[str, Any]:
    """Describe active allowances and supplied source; never create authority/evidence."""
    limits = packet["policy"]["budgets"]
    remaining_calls = limits["model_calls"] - calls
    remaining_reads = limits["reads"] - reads
    if remaining_calls <= 0:
        raise ValueError("Review model-call budget exhausted before synthesis")
    final = remaining_calls == 1 or remaining_reads == 0
    subject = packet["subject"]
    baseline, candidate = (subject["evidence"][k] for k in ("baseline", "candidate"))
    resources = [
        {
            "path": path,
            "current_identity": identity,
            "matches_supplied_baseline": path == baseline["path"]
            and identity == baseline["identity"],
            "eligible_for_acquisition": not final
            and path in packet["policy"]["read_paths"],
        }
        for path, identity in subject["inputs"].items()
    ]
    return {
        "schema": "native-diagnostic-budget-v1"
        if diagnostic
        else "native-review-budget-v1",
        "phase": "synthesis" if final else "inspection",
        "model_calls_used": calls,
        "model_calls_remaining_including_this_call": remaining_calls,
        "acquisitions_completed": reads,
        "acquisitions_remaining": remaining_reads,
        "source_tools_permitted": not final,
        "final_model_call_reserved": True,
        "supplied_source": [
            {
                "reference": "baseline",
                "path": baseline["path"],
                "identity": baseline["identity"],
                "complete_text_in_subject": True,
            },
            {
                "reference": "candidate",
                "path": candidate["path"],
                "sha256": candidate["sha256"],
                "complete_text_in_subject": True,
            },
        ],
        "current_resources": resources,
        "instruction": (
            "Produce the final structured review conclusion now. No source Tools are available. "
            "If evidence is insufficient, return disposition insufficient-evidence with specific gaps. "
            "No further model call is promised. Do not request Tools or invent findings."
            if final
            else "Use supplied baseline/candidate text directly; no reread is required. A matching current "
            "baseline identity authenticates equivalence to that baseline, not to the candidate. "
            "Acquire only missing useful evidence. You may conclude now; the last approved call is reserved for synthesis."
        ),
    }
