"""Publish the primary Astra judgments unchanged inside a frame-bound envelope.

Byte I/O is the case-local artifact boundary. The imported builder is used only
for invariant/statistics validation; its semantic construction is never called.
No treatment operations or reconciliation enter this publication.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, PLR2004, EM101, TRY003
import argparse
import gzip
import importlib.util
import json
import sys
from hashlib import sha256
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
ADJ = ROOT.parent
CASE = ADJ.parent
PACKET = CASE / "stage_c/packet"
PRIMARY_HASHES = "fc82fa987d7374590373d9fee0d51626e0e7ab21964835f876abfb5eab38861a"
REVIEW_HASH = "cb93fbc4c158668e4971c29fd8c3bf05c0a0d2e357a9aa66acee6888d4c51b50"


def encoded(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    ).encode()


def sha(raw: bytes) -> str:
    return sha256(raw).hexdigest()


def load(path: Path) -> Any:
    return json.loads(path.read_bytes())


def require(value: Any, message: str) -> None:
    if not value:
        raise ValueError(message)


def authenticate() -> tuple[Any, Any, Any]:
    primary = ADJ / "primary"
    require(
        sha((primary / "stage_c_hashes.json").read_bytes()) == PRIMARY_HASHES,
        "Sealed primary hash manifest",
    )
    hashes = load(primary / "stage_c_hashes.json")["sha256"]
    for name, digest in hashes.items():
        require(
            sha((primary / name).read_bytes()) == digest, "Primary artifact: " + name
        )
    require(
        sha((primary / "stage_c_review.json").read_bytes()) == REVIEW_HASH,
        "Sealed primary review",
    )
    review = load(primary / "stage_c_review.json")
    for name, digest in review["input_hashes"].items():
        require(sha((PACKET / name).read_bytes()) == digest, "Original packet: " + name)
    raw = gzip.decompress((PACKET / "resources.json.gz").read_bytes())
    require(sha(raw) == review["canonical_payload_sha256"], "Canonical packet payload")
    payload = json.loads(raw)
    require(
        len(review["blindness_attestation"]) == 26
        and set(review["blindness_attestation"].values()) == {"NO"},
        "Complete primary blindness",
    )
    spec = importlib.util.spec_from_file_location(
        "case0013_primary_invariants", primary / "stage_c_builder.py"
    )
    require(spec is not None and spec.loader is not None, "Primary validator loader")
    assert spec is not None  # noqa: S101
    assert spec.loader is not None  # noqa: S101
    module: Any = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.validate_review(review, payload, frozen=review)
    require(
        module.statistics(review) == load(primary / "stage_c_statistics.json"),
        "Sealed statistics reconstruction",
    )
    return review, payload, module


def construct_gold() -> Any:
    review, payload, _ = authenticate()
    frame = load(CASE / "frame.json")
    native = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))[
        "resources"
    ]
    require(payload["resources"] == native, "Exact semantic resource frame")
    treatment = load(CASE / "treatment.json")
    require(
        review["task_identity"] == treatment["task_identity"]
        and review["task_text"] == treatment["task_text"],
        "Task frame binding",
    )
    bindings = [
        {
            "resource": r["identity"],
            **{
                k: frame[k]
                for k in ("repository_id", "snapshot_id", "corpus_id", "frame_identity")
            },
            **{
                k: r[k]
                for k in ("address", "content_identity", "encoding", "byte_size")
            },
        }
        for r in review["resources"]
    ]
    return {
        "schema": "case-0013-reviewed-gold-v1",
        "primary": review,
        "frame": {
            k: frame[k]
            for k in ("repository_id", "snapshot_id", "corpus_id", "frame_identity")
        },
        "resource_bindings": bindings,
        "provenance": {
            "source": "PRIMARY_ASTRA_HIGH",
            "semantic_transformation": "NONE",
            "primary_review_sha256": REVIEW_HASH,
            "primary_hashes_sha256": PRIMARY_HASHES,
            "policy": {
                "MODEL": "GPT-6 Astra",
                "REASONING": "High",
                "treatment_blind": True,
                "automatic_second_review": False,
            },
            "projection": "Primary object retained in full with identical judgments, units, spans, witnesses, combinations, gaps, limitations and ambiguities. Frame envelope binds exact sealed resource content; it adds no semantic judgment.",
        },
    }


def validate(gold: Any) -> Any:
    source, payload, module = authenticate()
    module.validate_review(gold["primary"], payload, frozen=source)
    require(gold == construct_gold(), "Exact reviewed projection identity")
    return module.statistics(gold["primary"])


def markdown(gold: Any, stats: Any) -> bytes:
    lines = [
        "# Case 0013 reviewed development gold",
        "",
        "Provenance: PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. One primary review; no reconciliation or second reviewer.",
        "",
    ]
    lines.append((ADJ / "primary/STAGE_C_REVIEW.md").read_bytes().decode())
    for name, value in [
        ("Reviewed statistics", stats),
        ("Frame binding", gold["resource_bindings"]),
        ("Provenance", gold["provenance"]),
        (
            "Complete positive resource mapping",
            [c for c in gold["primary"]["cells"] if c["label"] != "UNNECESSARY"],
        ),
        ("Exact semantic units and support spans", gold["primary"]["semantic_units"]),
        ("Exact obligations and every witness", gold["primary"]["obligations"]),
        ("Exact gaps", gold["primary"]["gaps"]),
        ("All limitations", gold["primary"]["limitations"]),
        ("Preserved ambiguities", gold["primary"]["unresolved_ambiguity"]),
    ]:
        lines += [
            "## " + name,
            "",
            "```json",
            encoded(value).decode().rstrip(),
            "```",
            "",
        ]
    return ("\n".join(lines) + "\n").encode()


def write_new(files: dict[Path, bytes]) -> None:
    if any(path.exists() for path in files):
        raise FileExistsError("Refusing to overwrite reviewed artifacts")
    for path, raw in files.items():
        with path.open("xb") as stream:
            stream.write(raw)


def outputs() -> dict[str, bytes]:
    gold = construct_gold()
    stats = validate(gold)
    files = {
        "reviewed_gold.json": encoded(gold),
        "reviewed_statistics.json": encoded(stats),
        "REVIEWED_GOLD.md": markdown(gold, stats),
        "reviewed_validation.json": encoded(
            {
                "status": "PASS",
                "statistics": stats,
                "missing_cells": 0,
                "duplicate_cells": 0,
                "unexpected_cells": 0,
                "semantic_transformation": "NONE",
                "checks": [
                    "sealed primary and original packet",
                    "complete blindness categories",
                    "case/task/obligation/frame binding",
                    "complete cell Cartesian frame",
                    "exact labels/support spans/semantic units",
                    "exact witnesses and deletion minimality",
                    "Cartesian combinations and sufficient unions",
                    "obligation and task intersections",
                    "gap/limitation/ambiguity identity",
                    "sealed statistics agreement",
                    "deterministic JSON/Markdown",
                    "focused mutation rejection and overwrite refusal",
                ],
            }
        ),
    }
    files["reviewed_hashes.json"] = encoded(
        {
            "schema": "case-0013-reviewed-hashes-v1",
            "sha256": {n: sha(b) for n, b in files.items()},
            "materializer_sha256": sha(Path(__file__).read_bytes()),
            "import_metadata_sha256": sha((ADJ / "IMPORT.json").read_bytes()),
            "excluded": [".local", "self hash to avoid cycle"],
        }
    )
    return files


def verify() -> Any:
    files = outputs()
    for name, raw in files.items():
        require((ROOT / name).read_bytes() == raw, "Reviewed reconstruction: " + name)
    return {
        "status": "PASS",
        "sha256": {n: sha(b) for n, b in files.items()},
        "statistics": load(ROOT / "reviewed_statistics.json"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("build", "verify"))
    if parser.parse_args().mode == "build":
        write_new({ROOT / n: raw for n, raw in outputs().items()})
    sys.stdout.write(encoded(verify()).decode())


if __name__ == "__main__":
    main()
