# Copyright (c) 2026
# ruff: noqa: T201, S101, D103, C901, PLR0912, PLR0915, PLR2004 -- fake processes only in test fixture
"""Small deterministic process fixture for transport/independence/cleanup tests."""

from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path
from typing import Any


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def write(path: Path, value: object) -> bytes:
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()
    path.write_bytes(raw)
    return raw


def main() -> None:
    mode, stage, case, raw_frame = sys.argv[1:5]
    frame = json.loads(raw_frame)
    root = Path.cwd()
    fault = sys.argv[5] if len(sys.argv) > 5 else ""
    selected = case == "alpha" and (
        stage == "C"
        if fault
        in {"missing-primary", "packet-mutation", "blindness", "forbidden-output"}
        else stage == "B"
    )
    if selected and fault == "nonzero" and mode == "run":
        raise SystemExit(9)
    if selected and fault == "validator" and mode == "validate":
        raise SystemExit(8)
    if mode == "validate":
        if stage == "C":
            hashes = json.loads((root / "stage_c_hashes.json").read_bytes())
            assert all(sha((root / n).read_bytes()) == h for n, h in hashes.items())
            receipt: dict[str, Any] = {
                "status": "PASS",
                "model": "fixture-primary",
                "reasoning": "high",
                "second_reviewer": False,
                "reconciliation": False,
                "host_routing_independently_verified": False,
                "blindness": dict.fromkeys(
                    (
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
                    ),
                    False,
                ),
            }
        else:
            candidate = json.loads((root / "candidate.json").read_bytes())
            assert candidate["case"] == case
            assert candidate["frame"] == frame
            assert all(
                sha((root / name).read_bytes()) == h
                for name, h in candidate["files"].items()
            )
            receipt = {"status": "PASS"}
            if stage == "prepare":
                prepared = json.loads((root / "frame.json").read_bytes())
                assert prepared == {"case": case, "frame": frame, "stage": "prepare"}
            if stage == "B":
                receipt.update(
                    mode="SEALED",
                    native_archives_decoded=0,
                    deep_correspondence_executions=0,
                    completion_proof_sha256=sha(
                        (root / "completion_proof.json").read_bytes(),
                    ),
                )
            if stage == "import":
                receipt["semantic_transformation"] = "NONE"
        if selected and fault == "blindness":
            receipt["blindness"]["other_cases"] = True
        print(json.dumps(receipt))
        return
    if mode == "check":
        if fault == "packet-preflight-leak" and case == "alpha" and stage == "packet":
            (root / ".local").mkdir(exist_ok=True)
        print(json.dumps({"status": "PASS"}))
        return
    if stage in {"B", "C"}:
        time.sleep({"alpha": 0.25, "beta": 0.12, "gamma": 0.18}[case])
    if stage == "C":
        assert {p.name for p in root.iterdir()} == {
            "README.md",
            "manifest.json",
            "validate_packet.py",
            "resources.json.gz",
            "integrity.json",
        }
        for name in (
            "stage_c_review.json",
            "stage_c_statistics.json",
            "STAGE_C_REVIEW.md",
            "stage_c_validation.json",
            "stage_c_hashes.json",
            "stage_c_method.md",
            "stage_c_builder.py",
        ):
            write(root / name, {"case": case, "artifact": name})
        if selected and fault == "missing-primary":
            (root / "stage_c_statistics.json").unlink()
        if selected and fault == "packet-mutation":
            (root / "README.md").write_bytes(b"modified")
        if selected and fault == "forbidden-output":
            write(root / "stage_c_review.json", {"rank": 1})
        write(
            root / "stage_c_hashes.json",
            {
                p.name: sha(p.read_bytes())
                for p in root.glob("stage_c_*")
                if p.name != "stage_c_hashes.json" and p.is_file()
            },
        )
        return
    files = {}
    if stage == "packet":
        for name, content in {
            "README.md": ("Only " + case + "; one frozen primary; stop.\n").encode(),
            "manifest.json": json.dumps({"case": case, "frame": frame}).encode(),
            "validate_packet.py": b"# fake packet validator\n",
            "resources.json.gz": __import__("gzip").compress(
                json.dumps({"case": case}).encode(),
                mtime=0,
            ),
            "integrity.json": b"{}\n",
        }.items():
            (root / name).write_bytes(content)
            files[name] = sha(content)
    elif stage == "import":
        for path in (root / "primary").iterdir():
            files[path.relative_to(root).as_posix()] = sha(path.read_bytes())
        files["gold.json"] = sha(
            write(root / "gold.json", {"case": case, "frame": frame}),
        )
    else:
        name = (
            "completion_proof.json"
            if stage == "B"
            else "frame.json"
            if stage == "prepare"
            else "analysis.json"
        )
        files[name] = sha(
            write(root / name, {"case": case, "frame": frame, "stage": stage}),
        )
    if stage == "D":
        for identity in ("alpha", "beta", "gamma"):
            treatment = json.loads(
                (root / "B" / identity / "completion_proof.json").read_bytes(),
            )
            gold = json.loads((root / "C" / identity / "gold.json").read_bytes())
            assert treatment["case"] == gold["case"] == identity
            assert treatment["frame"] == gold["frame"]
    if selected and fault == "missing-output":
        (root / next(iter(files))).unlink()
    if selected and fault == "hash":
        files[next(iter(files))] = "0" * 64
    write(
        root / "candidate.json",
        {
            "schema": "experiment-candidate-v1",
            "case": case,
            "frame": frame,
            "stage": stage,
            "files": files,
        },
    )
    print(json.dumps({"status": "PASS"}))


if __name__ == "__main__":
    main()
