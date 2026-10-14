# Copyright (c) 2026
# ruff: noqa: ANN401, C901, PLR0915, E501, T201, PLR2004 -- standalone packet-only scientific codec
"""Frozen standalone reviewer builder; stdlib only, no semantic inference.

Its selected branch is frozen into each sterile packet. This external artifact boundary uses
bounded explicit byte files, never repository imports, filesystem discovery or
process launching. Character offsets are Python Unicode offsets, end exclusive.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import stat
from collections import Counter
from pathlib import Path
from typing import Any

BLINDNESS = (
    "repository",
    "git_history",
    "parent_siblings",
    "prior_session",
    "web",
    "queries",
    "ranks_scores",
    "annotations",
    "references_treatment",
    "pairs",
    "timings",
    "graph_ppr_rrf",
    "other_cases",
    "child",
    "prior_gold",
    "confirmation_reserve",
)
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
VERDICTS = ("GROUNDED_SOURCE", "NOT_GROUNDED_SOURCE", "UNCERTAIN_SOURCE")
FORBIDDEN = {
    "rank",
    "a_rank",
    "score",
    "query",
    "queries",
    "need",
    "information_need",
    "annotations",
    "supports",
    "local_pairs",
    "timings",
    "child_commit",
    "child_tree",
    "changed_paths",
    "targets",
    "target",
    "facts",
    "references",
    "outgoing_count",
}
SOURCE = {"address", "document_identity", "content_identity", "content"}
OBLIGATION = {"id", "requirement", "satisfaction", "exclusions", "gap"}


def canonical(value: Any) -> bytes:
    """Serialize deterministic exact JSON."""
    return (
        json.dumps(value, sort_keys=True, ensure_ascii=True, indent=2) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    """Hash scientific bytes."""
    return hashlib.sha256(raw).hexdigest()


def require(value: object, reason: str) -> None:
    """Fail closed, without repairing a judgment."""
    if not value:
        raise ValueError(reason)


def semantic(name: str, *parts: str) -> str:
    """Replay the native framed content/document identity codec."""
    h = hashlib.sha256()
    for part in (name, *parts):
        raw = part.encode()
        h.update(len(raw).to_bytes(8, "big"))
        h.update(raw)
    return h.hexdigest()


def metadata(value: Any) -> None:
    """Reject structural/retrieval metadata keys, not natural source contents."""
    if isinstance(value, dict):
        require(not FORBIDDEN.intersection(value), "Forbidden disclosure metadata")
        for item in value.values():
            metadata(item)
    elif isinstance(value, list):
        for item in value:
            metadata(item)


def source(row: Any, frame: Any) -> None:
    """Authenticate content identity; full frames also authenticate order below."""
    require(set(row) == SOURCE, "Source allowlist")
    address = row["address"]
    require(
        isinstance(address, str)
        and not address.startswith(("/", "experiments/", "tests/experiments/", "."))
        and "\\" not in address
        and ":" not in address,
        "Source address",
    )
    require(
        all(
            p not in {"", ".", ".."}
            and not any(
                s in p.casefold() for s in ("holdout", "confirmation", "reserve")
            )
            for p in address.split("/")
        ),
        "Restricted source",
    )
    content = semantic("decoded-utf8-text-sha256-v1", row["content"])
    require(
        row["content_identity"] == content
        and row["document_identity"]
        == semantic(
            "whole-resource-exact-text-v1",
            frame["repository_id"],
            address,
            content,
        ),
        "Native source/content identity",
    )


def packet(root: Path) -> Any:
    """Authenticate exact packet bytes and strict input allowlists."""
    receipt = json.loads((root / "packet_integrity.json").read_bytes())
    require(
        set(receipt) == {"schema", "files"}
        and receipt["schema"] == "blind-primary-packet-integrity-v1",
        "Packet integrity schema",
    )
    require(
        set(receipt["files"])
        == {"packet.json", "INSTRUCTIONS.md", "stage_c_builder.py"},
        "Packet file allowlist",
    )
    for name, expected in receipt["files"].items():
        p = root / name
        require(
            not p.is_symlink()
            and not getattr(p.lstat(), "st_file_attributes", 0)
            & stat.FILE_ATTRIBUTE_REPARSE_POINT,
            "Packet link/reparse",
        )
        require(sha(p.read_bytes()) == expected, "Packet mutation")
    p = json.loads((root / "packet.json").read_bytes())
    require(
        p["schema"] in {"source-grounding-packet-v1", "blind-semantic-gold-packet-v1"},
        "Packet schema",
    )
    metadata(p)
    require(
        set(p["frame"]) == {"repository_id", "snapshot_id", "corpus_id", "parent_tree"},
        "Frame allowlist",
    )
    if p["schema"] == "source-grounding-packet-v1":
        require(
            set(p) == {"schema", "case", "task", "frame", "cells"},
            "Grounding packet allowlist",
        )
        cells = p["cells"]
        require(
            len({(c["obligation"]["id"], c["source"]["address"]) for c in cells})
            == len(cells),
            "Duplicate grounding cell",
        )
        for c in cells:
            require(
                set(c) == {"obligation", "source"}
                and set(c["obligation"]) == OBLIGATION,
                "Grounding cell allowlist",
            )
            source(c["source"], p["frame"])
    else:
        require(
            set(p) == {"schema", "case", "task", "frame", "obligations", "resources"},
            "Gold packet allowlist",
        )
        require(
            [o["id"] for o in p["obligations"]]
            == [f"O{i}" for i in range(1, len(p["obligations"]) + 1)],
            "Obligation order",
        )
        require(
            all(set(o) == OBLIGATION for o in p["obligations"]),
            "Gold obligation allowlist",
        )
        addresses = [r["address"] for r in p["resources"]]
        require(addresses == sorted(set(addresses)), "Resource completeness/order")
        for r in p["resources"]:
            source(r, p["frame"])
        pairs = tuple(
            x for r in p["resources"] for x in (r["address"], r["content_identity"])
        )
        require(
            p["frame"]["snapshot_id"]
            == semantic(
                "explicit-required-text-resources-sha256-v1",
                p["frame"]["repository_id"],
                *pairs,
            ),
            "Snapshot identity",
        )
        require(
            p["frame"]["corpus_id"]
            == semantic(
                "selected-observed-utf8-resource-occurrences-sha256-v1",
                p["frame"]["repository_id"],
                *pairs,
            ),
            "Corpus identity",
        )
    return p


def span(evidence: Any, resources: Any) -> str:
    """Require exact own-source spans rather than accepting approximate quotes."""
    require(set(evidence) == {"source", "start", "end", "quote"}, "Span schema")
    identity = evidence["source"]
    require(
        set(identity) == SOURCE - {"content"} and identity["address"] in resources,
        "Evidence source",
    )
    r = resources[identity["address"]]
    require(identity == {k: r[k] for k in identity}, "Stale evidence identity")
    start, end = evidence["start"], evidence["end"]
    require(
        type(start) is int
        and type(end) is int
        and 0 <= start < end <= len(r["content"]),
        "Evidence bounds",
    )
    require(
        r["content"][start:end] == evidence["quote"] and evidence["quote"].strip(),
        "Evidence exact quote",
    )
    return str(identity["address"])


def attestation(value: Any, model: str, reasoning: str = "High") -> None:
    """Authenticate the single primary's behavioral statement; no routing claims."""
    require(
        set(value)
        == {
            "model",
            "reasoning",
            "second_reviewer",
            "reconciliation",
            "host_routing_independently_verified",
            "blindness",
        },
        "Attestation schema",
    )
    require(
        value["model"] == model
        and value["reasoning"] == reasoning
        and value["second_reviewer"] is False
        and value["reconciliation"] is False
        and value["host_routing_independently_verified"] is False,
        "Primary designation",
    )
    require(
        value["blindness"] == ["NO_ACCESS:" + name for name in BLINDNESS],
        "Blindness attestation",
    )


def minimal(unions: Any) -> list[list[str]]:
    """Compute inclusion-minimal resource unions; never a relevance heuristic."""
    sets = {frozenset(u) for u in unions}
    return sorted(
        [sorted(s) for s in sets if not any(t < s for t in sets)],
        key=lambda s: (len(s), s),
    )


def validate(review: Any, p: Any, designation: Any = None) -> Any:
    """Validate labels, units, evidence and exact complete judgment frame."""
    require(
        set(review)
        == {
            "schema",
            "case",
            "frame",
            "packet_sha256",
            "attestation",
            "cells",
            "units",
            "gaps",
            "self_review",
        },
        "Review schema",
    )
    require(
        review["schema"] == "blind-primary-review-v1"
        and review["case"] == p["case"]
        and review["frame"] == p["frame"]
        and review["packet_sha256"] == sha(canonical(p)),
        "Review frame/input identity",
    )
    gold = p["schema"] == "blind-semantic-gold-packet-v1"
    scientific = ("GPT-6 Astra" if gold else "GPT-6 Sol", "High")
    require(
        designation is None
        or designation == scientific
        or (
            p["case"].startswith("SYNTHETIC-")
            and designation == ("GPT-6 Luna", "Medium")
        ),
        "Non-scientific designation is restricted to synthetic Luna smoke",
    )
    model, reasoning = designation or scientific
    attestation(review["attestation"], model, reasoning)
    require(
        isinstance(review["self_review"], str) and review["self_review"].strip(),
        "Same-primary audit required",
    )
    if not gold:
        require(
            review["units"] == [] and review["gaps"] == [],
            "Grounding cannot adjudicate units/gold/gaps",
        )
        expected = {
            (c["obligation"]["id"], c["source"]["address"]): c for c in p["cells"]
        }
        seen = set()
        for c in review["cells"]:
            require(
                set(c)
                == {
                    "obligation",
                    "source",
                    "verdict",
                    "spans",
                    "statement",
                    "reason",
                    "assumptions",
                    "uncertainty",
                    "additional_information",
                },
                "Grounding output allowlist",
            )
            key = (c["obligation"], c["source"]["address"])
            require(
                key in expected and key not in seen,
                "Missing/duplicate/foreign grounding cell",
            )
            seen.add(key)
            r = expected[key]["source"]
            require(
                c["source"] == {k: r[k] for k in SOURCE - {"content"}},
                "Grounding source identity",
            )
            require(c["verdict"] in VERDICTS and c["reason"].strip(), "Verdict/reason")
            for s in c["spans"]:
                span(s, {r["address"]: r})
            if c["verdict"] == "GROUNDED_SOURCE":
                require(
                    c["spans"]
                    and c["statement"].strip()
                    and isinstance(c["assumptions"], list),
                    "Grounding factual evidence",
                )
            if c["verdict"] == "UNCERTAIN_SOURCE":
                require(
                    c["uncertainty"].strip() and c["additional_information"].strip(),
                    "Explicit uncertainty",
                )
        require(seen == set(expected), "Grounding completeness")
        return {
            "cells": len(seen),
            "verdicts": dict(Counter(c["verdict"] for c in review["cells"])),
        }
    resources = {r["address"]: r for r in p["resources"]}
    obligations = {o["id"] for o in p["obligations"]}
    require(
        set(review["gaps"])
        == {
            "TASK_INTERPRETATION_GAP",
            "TASK_GAP",
            "REPOSITORY_INFORMATION_GAP",
            "unconditional_sufficiency",
            "qualification",
        },
        "Gold gap record",
    )
    require(
        type(review["gaps"]["unconditional_sufficiency"]) is bool
        and all(
            isinstance(v, str) and v.strip()
            for k, v in review["gaps"].items()
            if k != "unconditional_sufficiency"
        ),
        "Explicit gap findings",
    )
    units = review["units"]
    require(len({u["id"] for u in units}) == len(units), "Duplicate semantic unit")
    witnesses = {}
    for o in sorted(obligations):
        relevant = [u for u in units if u["obligation"] == o]
        require(relevant, "Necessary units required for every obligation")
        alternatives = []
        for u in relevant:
            require(
                set(u)
                == {
                    "id",
                    "obligation",
                    "statement",
                    "basis",
                    "necessity",
                    "alternatives",
                }
                and u["basis"]
                in {
                    "TASK_BACKED",
                    "REPOSITORY_SUPPORTED",
                    "TASK_AND_REPOSITORY_SUPPORTED",
                }
                and u["statement"].strip()
                and u["necessity"].strip()
                and isinstance(u["alternatives"], list),
                "Necessary unit schema",
            )
            require(
                u["alternatives"]
                or (
                    not review["gaps"]["unconditional_sufficiency"]
                    and review["gaps"]["REPOSITORY_INFORMATION_GAP"] != "NONE"
                ),
                "Missing unit evidence requires explicit blocking repository gap",
            )
            evidence_sets = []
            for alternative in u["alternatives"]:
                require(
                    alternative or u["basis"] == "TASK_BACKED",
                    "Repository unit needs evidence",
                )
                evidence_sets.append({span(s, resources) for s in alternative})
            alternatives.append(evidence_sets)
        count = 1
        for choices in alternatives:
            count *= len(choices)
        require(
            count <= 1000000,
            "Witness expansion bound exceeded; stop without truncation",
        )
        witnesses[o] = minimal(
            set().union(*parts) for parts in itertools.product(*alternatives)
        )
    require(
        all(u["obligation"] in obligations for u in units),
        "Foreign unit obligation",
    )
    required = {(o, a) for o, sets in witnesses.items() for s in sets for a in s}
    seen = set()
    for c in review["cells"]:
        require(
            set(c) == {"obligation", "source", "label", "spans", "reason"},
            "Gold cell schema",
        )
        key = (c["obligation"], c["source"]["address"])
        require(
            key[0] in obligations and key[1] in resources and key not in seen,
            "Duplicate/foreign gold cell",
        )
        seen.add(key)
        r = resources[key[1]]
        require(
            c["source"] == {k: r[k] for k in SOURCE - {"content"}}
            and c["label"] in LABELS
            and c["reason"].strip(),
            "Gold cell identity/label/reason",
        )
        require(
            (c["label"] == "REQUIRED") == (key in required),
            "Required labels disagree with minimal witnesses",
        )
        for s in c["spans"]:
            span(s, {r["address"]: r})
        require(
            c["label"] == "UNNECESSARY" or c["spans"],
            "Useful cell needs exact own evidence",
        )
    require(
        seen == {(o, a) for o in obligations for a in resources},
        "Gold cell completeness",
    )
    combinations = 1
    for witness_choices in witnesses.values():
        combinations *= len(witness_choices)
    require(
        combinations <= 1000000,
        "Task expansion bound exceeded; stop without truncation",
    )
    task_unions = sorted(
        {
            tuple(sorted(set().union(*parts)))
            for parts in itertools.product(*witnesses.values())
        },
    )
    task_minimal = minimal(task_unions)
    indispensable = (
        sorted(set.intersection(*(set(s) for s in task_minimal)))
        if task_minimal
        else []
    )
    unconditional = review["gaps"]["unconditional_sufficiency"]
    return {
        "cells": len(seen),
        "labels": dict(Counter(c["label"] for c in review["cells"])),
        "necessary_units": dict(Counter(u["basis"] for u in units)),
        "obligation_witnesses": witnesses,
        "obligation_indispensable": {
            o: sorted(set.intersection(*(set(s) for s in sets))) if sets else None
            for o, sets in witnesses.items()
        },
        "conditional_repository_task_combinations": combinations,
        "conditional_repository_task_unions": task_unions,
        "conditional_repository_minimal_unions": task_minimal,
        "conditional_repository_indispensable": indispensable,
        "unconditional_task_unions": task_unions if unconditional else [],
        "unconditional_task_indispensable": indispensable if unconditional else None,
        "gaps": review["gaps"],
    }


def products(root: Path, designation: Any = None) -> dict[str, bytes]:
    """Derive scientific reports from immutable primary decisions only."""
    p = packet(root)
    review = json.loads((root / "stage_c_review.json").read_bytes())
    require(
        (root / "stage_c_review.json").read_bytes() == canonical(review),
        "Canonical primary review required",
    )
    statistics = validate(review, p, designation)
    files = {
        "stage_c_statistics.json": canonical(statistics),
        "stage_c_validation.json": canonical(
            {
                "status": "PASS",
                "packet_sha256": sha(canonical(p)),
                "review_sha256": sha(canonical(review)),
                "complete_cells": statistics["cells"],
            },
        ),
        "STAGE_C_REVIEW.md": (
            "# Single primary review\n\n"
            + review["self_review"]
            + "\n\n```json\n"
            + canonical(statistics).decode()
            + "```\n"
        ).encode(),
        "stage_c_method.md": (
            b"# Method\n\nOne designated primary; no second reviewer or reconciliation. Own-content spans, explicit necessary units, alternative conjunctive evidence, inclusion-minimal resource witnesses and qualified gaps. Host routing not independently verified.\n"
        ),
    }
    files["stage_c_hashes.json"] = canonical(
        {
            "schema": "blind-primary-hashes-v1",
            "sha256": {
                **{n: sha(v) for n, v in files.items()},
                "stage_c_review.json": sha(canonical(review)),
                "stage_c_builder.py": sha((root / "stage_c_builder.py").read_bytes()),
                "packet_integrity.json": sha(
                    (root / "packet_integrity.json").read_bytes(),
                ),
            },
        },
    )
    return files


def main() -> None:
    """Validate packets or build/verify outputs without overwriting science."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("packet", "build", "verify"))
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--model")
    parser.add_argument("--reasoning", default="High")
    args = parser.parse_args()
    if args.mode == "packet":
        packet(args.root)
    else:
        files = products(
            args.root,
            (args.model, args.reasoning) if args.model else None,
        )
        if args.mode == "build":
            require(
                not any((args.root / n).exists() for n in files),
                "Scientific overwrite refused",
            )
            for name, raw in files.items():
                with (args.root / name).open("xb") as stream:
                    stream.write(raw)
        else:
            require(
                all((args.root / n).read_bytes() == raw for n, raw in files.items()),
                "Exact deterministic replay differs",
            )
    print(json.dumps({"status": "PASS", "mode": args.mode}))


if __name__ == "__main__":
    main()
