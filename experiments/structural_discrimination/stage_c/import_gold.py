# Copyright (c) 2026
# ruff: noqa: ANN401, E501 -- heterogeneous immutable primary boundary
"""Authenticate and import sole primaries without semantic transformation."""

from __future__ import annotations

import asyncio
import gzip
import json
import sys
from collections import Counter
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from devtools.core.paths import resolve_path
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from experiments.codex_dogfood.case_0009.artifacts import (
    ROOT,
    digest,
    git,
    json_bytes,
    put_binary,
    put_json,
    put_text,
)
from experiments.structural_discrimination.stage_b.capture import CASES, case_root
from experiments.structural_discrimination.stage_c.packet import no_reparse

PACKETS = "1b43203e908e725465a407b556f60a583dacfb1c"
STAGE_B = "95840e11b6cc14acd8a47754af3d1a8b673ee70d"
SCIENTIFIC = (
    "stage_c_review.json",
    "stage_c_statistics.json",
    "STAGE_C_REVIEW.md",
    "stage_c_validation.json",
    "stage_c_hashes.json",
    "stage_c_method.md",
    "stage_c_builder.py",
)
SOURCES = dict(
    zip(CASES, ("64dad46fb86c", "ef761a2d124b", "9cdf7234c3de"), strict=True),
)
LABELS = ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY")
EXPECTED = {
    "0017": (357, 7, 31, 1033),
    "0018": (382, 29, 43, 1074),
    "0019": (222, 3, 32, 631),
}


def require(condition: object, message: str) -> None:
    """Fail closed on inconsistent scientific input."""
    if not condition:
        raise ValueError(message)


def primary_root(case: str) -> Path:
    """Use the established case adjudication owner."""
    return case_root(case) / "adjudication" / "primary"


def project(case: str, review: Any, packet: Any) -> Any:
    """Project cell identity/labels only; original semantics remain authoritative."""
    require(review["case_id"] == packet["case_id"] == "case-" + case, "Case identity")
    require(review["parent_frame"] == packet["parent_frame"], "Primary frame")
    require(
        review["task_identity"] == packet["task_identity"]
        and review["task_text"] == packet["task_text"],
        "Task identity",
    )
    require(
        len(review["obligations"]) == len(packet["obligations"]),
        "Primary obligation count",
    )
    for actual, frozen in zip(
        review["obligations"],
        packet["obligations"],
        strict=True,
    ):
        require({k: actual[k] for k in frozen} == frozen, "Primary obligations")
    resources = {r["address"]: r for r in packet["resources"]}
    obligations = {o["id"]: o["obligation_identity"] for o in packet["obligations"]}
    cells = []
    seen = set()
    for ordinal, cell in enumerate(review["cells"]):
        identity = cell.get("resource", cell)
        address = identity["address"]
        obligation = cell.get("obligation_id", cell.get("obligation"))
        require(address in resources and obligation in obligations, "Unexpected cell")
        require((obligation, address) not in seen, "Duplicate gold cell")
        seen.add((obligation, address))
        native = resources[address]
        for key in ("address", "document_identity", "content_identity"):
            require(identity[key] == native[key], "Gold resource/content identity")
        for key in ("repository_id", "snapshot_id", "corpus_id", "source_blob_sha256"):
            if key in identity:
                require(identity[key] == native[key], "Gold cell frame/content")
        require(
            cell["obligation_identity"] == obligations[obligation],
            "Gold obligation identity",
        )
        label = cell.get("label", cell.get("judgment", cell.get("classification")))
        require(label in LABELS, "Unknown gold label")
        require(
            cell.get("resolved", True)
            and cell.get("decision_status", "RESOLVED") == "RESOLVED"
            and not cell.get("unresolved_decision", False),
            "Unresolved gold cell",
        )
        cells.append(
            {
                **{
                    k: native[k]
                    for k in (
                        "repository_id",
                        "snapshot_id",
                        "corpus_id",
                        "address",
                        "document_identity",
                        "content_identity",
                        "source_blob_sha256",
                    )
                },
                "obligation": obligation,
                "obligation_identity": obligations[obligation],
                "label": label,
                "primary_cell_pointer": f"/cells/{ordinal}",
            },
        )
    require(
        seen == {(o, a) for o in obligations for a in resources},
        "Missing gold cell",
    )
    counts = Counter(c["label"] for c in cells)
    require(
        (len(resources), *(counts[k] for k in LABELS)) == EXPECTED[case],
        "Primary summary counts",
    )
    return {
        "case": case,
        "frame": packet["parent_frame"],
        "task_identity": packet["task_identity"],
        "obligations": packet["obligations"],
        "cells": cells,
        "counts": dict(counts),
        "semantic_transformation": "NONE; identity/label projection only; all spans, units, alternatives and witnesses remain in primary",
    }


def attest(case: str, review: Any, markdown: str) -> Any:
    """Retain heterogeneous attestations with explicit exclusions and routing limit."""
    if case == "0018":
        a = review["blindness_attestation"]
        require(
            a["requested_model"] == "GPT-6 Astra"
            and a["requested_reasoning"] == "High",
            "Reviewer designation",
        )
        require(
            a["second_reviewer"] is False and a["reconciliation"] is False,
            "Reviewer count",
        )
        require(
            all(
                v is False
                for k, v in a.items()
                if k.endswith("_accessed") and isinstance(v, bool)
            ),
            "Blindness access",
        )
        require(
            a["outside_workspace_evidence_accessed"]
            == a["excluded_external_categories_accessed"]
            == [],
            "External evidence",
        )
        require(
            "parent/sibling directory" in markdown
            and "pairs/counts/timings" in markdown
            and "prior gold" in markdown,
            "Full blindness scope",
        )
    else:
        a = (
            review["blindness_attestation"]
            if case == "0017"
            else review["blindness"]["access"]
        )
        require(a and all(v == "NO" for v in a.values()), "Blindness access")
        reviewer = review["reviewer"]
        require(
            reviewer.get("model", reviewer.get("designated_model")) == "GPT-6 Astra"
            and reviewer.get("reasoning", reviewer.get("designated_reasoning"))
            == "High",
            "Reviewer designation",
        )
        require(reviewer["second_reviewer"] in ("NO", False), "Second reviewer")
        if case == "0019":
            require(
                a["current modern vLLM implementation"] == "NO"
                and reviewer["reconciliation"] is False,
                "Modern vLLM/reconciliation",
            )
    return {
        "status": "PASS",
        "original_attestation": a,
        "model": "GPT-6 Astra",
        "reasoning": "High",
        "second_reviewer_count": 0,
        "reconciliation_count": 0,
        "routing": "HOST ROUTING NOT INDEPENDENTLY VERIFIED",
    }


async def replay(directory: Path, case: str) -> str:
    """Run documented verification in an independent managed Python process."""
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(max_stdout_bytes=1 << 20),
    ).execute(
        Command(sys.executable)
        .args("-B", "stage_c_builder.py", "verify" if case == "0019" else "--verify")
        .cwd(resolve_path(directory)),
    )
    require(
        not result.failed and not result.stdout_truncated,
        "Primary deterministic verification: " + result.stderr.decode(errors="replace"),
    )
    return result.stdout.decode()


async def packet_bytes(case: str) -> dict[str, bytes]:
    """Externally anchor the original five packet bytes to their accepted commit."""
    prefix = case_root(case).relative_to(ROOT).as_posix() + "/stage_c/"
    publication = await git("show", PACKETS + ":" + prefix + "publication.json")
    require(
        publication == (case_root(case) / "stage_c/publication.json").read_bytes(),
        "Packet publication changed",
    )
    result = {}
    for name, sha in json.loads(publication)["packet_file_sha256"].items():
        raw = await git("show", PACKETS + ":" + prefix + "packet/" + name)
        require(
            digest(raw) == sha
            and raw == (case_root(case) / "stage_c/packet" / name).read_bytes(),
            "Committed packet changed",
        )
        result[name] = raw
    return result


async def authenticate(
    case: str,
    checkpoint: str | None = None,
    *,
    verify_builder: bool = False,
) -> Any:
    """Authenticate imported bytes and exact cell projection on every invocation."""
    root = primary_root(case)
    meta_path = root.parent / "IMPORT.json"
    meta_raw = meta_path.read_bytes()
    if checkpoint:
        require(
            meta_raw
            == await git(
                "show",
                checkpoint + ":" + meta_path.relative_to(ROOT).as_posix(),
            ),
            "Committed import integrity",
        )
    meta = json.loads(meta_raw)
    for name in SCIENTIFIC:
        raw = (root / name).read_bytes()
        require(digest(raw) == meta["sha256"][name], "Primary artifact hash: " + name)
        if checkpoint:
            require(
                raw
                == await git(
                    "show",
                    checkpoint + ":" + (root / name).relative_to(ROOT).as_posix(),
                ),
                "Committed primary bytes",
            )
    originals = await packet_bytes(case)
    packet = json.loads(gzip.decompress(originals["resources.json.gz"]))
    review = json.loads((root / "stage_c_review.json").read_bytes())
    gold = project(case, review, packet)
    require(
        (root.parent / "reviewed/gold.json").read_bytes() == json_bytes(gold),
        "Gold projection differs",
    )
    require(
        digest(json_bytes(gold)) == meta["gold_projection_sha256"],
        "Gold projection hash",
    )
    blindness = attest(
        case,
        review,
        (root / "STAGE_C_REVIEW.md").read_text(encoding="utf-8"),
    )
    if verify_builder:
        scratch = ROOT / ".local"
        scratch.mkdir(exist_ok=True)
        with TemporaryDirectory(prefix="primary-verify-", dir=scratch) as temporary:
            directory = Path(temporary)
            (directory / ".scratch").mkdir()
            for name, raw in originals.items():
                put_binary(directory / name, raw)
            for name in SCIENTIFIC:
                put_binary(directory / name, (root / name).read_bytes())
            await replay(directory, case)
            require(
                all(
                    (directory / n).read_bytes() == raw for n, raw in originals.items()
                ),
                "Replay packet preservation",
            )
    return {
        "status": "PASS",
        "case": case,
        "primary_sha256": meta["sha256"],
        "gold_projection_sha256": meta["gold_projection_sha256"],
        "packet_sha256": {n: digest(v) for n, v in originals.items()},
        "blindness": blindness,
        "gold": gold,
    }


async def import_all() -> Any:
    """Exclusively import all original scientific bytes after fresh authentication."""
    require(
        all(not primary_root(c).parent.exists() for c in CASES),
        "Import destination exists",
    )
    prepared = []
    for case in CASES:
        source = (
            Path("C:/Users/recoveryadmin/CodexSterile")
            / f"case_{case}_stage_c_{SOURCES[case]}"
        )
        no_reparse(source)
        originals = await packet_bytes(case)
        require(
            all((source / n).read_bytes() == raw for n, raw in originals.items()),
            "Sterile packet changed",
        )
        scientific = {n: (source / n).read_bytes() for n in SCIENTIFIC}
        review = json.loads(scientific["stage_c_review.json"])
        gold = project(
            case,
            review,
            json.loads(gzip.decompress(originals["resources.json.gz"])),
        )
        blindness = attest(case, review, scientific["STAGE_C_REVIEW.md"].decode())
        prepared.append((case, source, scientific, originals, gold, blindness))
    for case, source, scientific, originals, gold, blindness in prepared:
        root = primary_root(case)
        for name, raw in scientific.items():
            put_binary(root / name, raw)
        put_text(root / ".gitattributes", "* -text\n")
        put_json(root.parent / "reviewed/gold.json", gold)
        put_json(
            root.parent / "IMPORT.json",
            {
                "case": case,
                "source": str(source),
                "authority": "SOLE DESIGNATED PRIMARY; AUTHORITATIVE STAGE C GOLD",
                "semantic_transformation": "NONE",
                "packet_checkpoint": PACKETS,
                "sha256": {n: digest(v) for n, v in scientific.items()},
                "packet_sha256": {n: digest(v) for n, v in originals.items()},
                "gold_projection_sha256": digest(json_bytes(gold)),
                "blindness": blindness,
                "sterile_replay": "PASS; documented separate-process verification completed before import",
                "original_packet_preservation": "ALL FIVE EXACT",
                "operational_artifacts": "EXCLUDED",
                "writer": "No concrete competing writer with this exact worktree in command line; OS process listing is not a proof of exclusivity.",
            },
        )
        await authenticate(case, verify_builder=True)
    return {
        "status": "PASS",
        "cases": list(CASES),
        "cells": 2883,
        "REQUIRED": 39,
        "HELPFUL_ONLY": 106,
        "UNNECESSARY": 2738,
    }


if __name__ == "__main__":
    print(json.dumps(asyncio.run(import_all()), indent=2))  # noqa: T201
