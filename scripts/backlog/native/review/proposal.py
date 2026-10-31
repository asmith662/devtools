# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, PLR2004, COM812, C901 -- closed prospective review contract
"""Parse model recommendations without manufacturing verified facts or authority."""

from __future__ import annotations

from typing import Any

from devtools.agents.coding.protocol import arguments


def parse(
    text: str, references: dict[str, str], obligations: set[str]
) -> dict[str, Any]:
    """Require finite grounded claims; observed/inferred remains model attribution."""
    value = arguments(
        text,
        {
            "disposition",
            "summary",
            "evidence",
            "findings",
            "outstanding",
            "requests",
            "assessed_obligations",
        },
    )
    if value["disposition"] not in {"accept", "reject", "insufficient-evidence"}:
        raise ValueError("Unsupported review disposition")

    def texts(v: object) -> list[str]:
        if (
            not isinstance(v, list)
            or len(v) > 32
            or any(not isinstance(s, str) or not s.strip() or len(s) > 2048 for s in v)
        ):
            raise ValueError("Review requires bounded text lists")
        return v

    def refs(v: object) -> list[str]:
        names = texts(v)
        if not names or not set(names) <= set(references):
            raise ValueError("Review cites unavailable evidence")
        return names

    if (
        not isinstance(value["summary"], str)
        or not value["summary"].strip()
        or len(value["summary"]) > 4096
    ):
        raise ValueError("Review requires a bounded usable conclusion")
    cited = refs(value["evidence"])
    assessed = texts(value["assessed_obligations"])
    if not set(assessed) <= obligations or len(set(assessed)) != len(assessed):
        raise ValueError("Review obligation references are invalid")
    for key in ("outstanding", "requests"):
        texts(value[key])
    findings = value["findings"]
    if not isinstance(findings, list) or len(findings) > 32:
        raise ValueError("Invalid review findings")
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != {
            "kind",
            "severity",
            "message",
            "evidence",
        }:
            raise ValueError("Invalid review finding fields")
        if finding["kind"] not in {"observed", "inference"} or finding[
            "severity"
        ] not in {"blocking", "advisory"}:
            raise ValueError("Invalid review finding qualification")
        texts([finding["message"]])
        refs(finding["evidence"])
    if value["disposition"] == "accept" and (
        set(assessed) != obligations
        or value["outstanding"]
        or value["requests"]
        or any(f["severity"] == "blocking" for f in findings)
        or not {
            "task",
            "baseline",
            "candidate",
            "public-checks",
            "acceptance",
            "custody",
        }
        <= set(cited)
    ):
        raise ValueError(
            "Acceptance proposal has incomplete obligations or blocking risks"
        )
    if value["disposition"] == "insufficient-evidence" and not (
        value["outstanding"] or value["requests"]
    ):
        raise ValueError("Insufficient evidence requires an explicit gap")
    return value
