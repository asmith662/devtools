"""Case-local byte import and unchanged projection of the sole sealed primary.

Physical byte I/O is the scientific artifact import/publication boundary. This
non-installable composition adds no production primitive or semantic judgment.
"""

from __future__ import annotations

# ruff: noqa: INP001, CPY001, ANN401, D103, E501, COM812, EM101, TRY003
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
STERILE = Path(r"C:\Users\recoveryadmin\CodexSterile\case_0016_stage_c_52a2c4c5abab")
HASHES = {
    "STAGE_C_REVIEW.md": "10095b46d89779f3cf62269d2020643ff0ee62dfa80b5c36bbd8f26952b8f78d",
    "stage_c_builder.py": "da2898034aa2257172b30a99404a8dfcb8daba0e4f624589763a52153d9430e3",
    "stage_c_hashes.json": "55d5e8ba911bafb871c74aa1e977480f50549a5c15c62f0c18fb5984801600f5",
    "stage_c_method.md": "b2d82110f7e6f43516a22370f0e5853e92e79f1713590b20b12f43dfc79f1bfe",
    "stage_c_review.json": "0d8d806f3fc613bdfa477a8914278423142a14ceaa6d1dd0fd11611544a6d8a8",
    "stage_c_statistics.json": "b4e2f4dc723344a2669280750fbf0a145068ad591e4079a6f4a34d76fcde8a87",
    "stage_c_validation.json": "f5c172851973d10759c0a5702a8425a7f62535125632e0bac4fa95185700622a",
}


def encoded(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"
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
        {n: sha((primary / n).read_bytes()) for n in HASHES} == HASHES,
        "Sealed primary hashes",
    )
    spec = importlib.util.spec_from_file_location(
        "case0016_sealed_primary", primary / "stage_c_builder.py"
    )
    require(spec is not None and spec.loader is not None, "Sealed validator loader")
    assert spec is not None  # noqa: S101
    assert spec.loader is not None  # noqa: S101
    module: Any = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.ROOT = primary  # Execution adapter only; imported source bytes unchanged.
    for name, expected in module.ORIGINAL_HASHES.items():
        require(
            sha((PACKET / name).read_bytes()) == expected, "Original packet: " + name
        )
    raw = gzip.decompress((PACKET / "resources.json.gz").read_bytes())
    require(sha(raw) == module.PAYLOAD_SHA256, "Canonical packet payload")
    packet = json.loads(raw)
    review = load(primary / "stage_c_review.json")
    module.validate_review(review, packet)
    for name, data in module.bundle(review, packet).items():
        require((primary / name).read_bytes() == data, "Primary replay: " + name)
    reviewer = review["primary"]["reviewer"]
    require(
        reviewer["designated_model"] == "GPT-6 Astra"
        and reviewer["designated_reasoning"] == "High"
        and reviewer["reviewers"] == 1
        and reviewer["second_reviewer"] == "NO",
        "Sole designated primary",
    )
    require(
        set(review["primary"]["blindness"]["access"].values()) == {"NO"}, "Blindness"
    )
    return review, packet, module


def construct_gold() -> Any:
    review, packet, _ = authenticate()
    frame = load(CASE / "frame.json")
    native = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))
    design = load(CASE / "protocol.json")
    require(
        packet["resources"]
        == [{k: r[k] for k in packet["resources"][0]} for r in native],
        "Exact native frame and content",
    )
    require(
        (review["case"], review["task_identity"], review["exact_task"])
        == (design["case"], design["task_identity"], design["task_text"]),
        "Exact case/task",
    )
    require(
        review["obligations"]
        == [
            {k: o[k] for k in review["obligations"][0]}
            for o in design["requirement_matrix"]
        ],
        "Exact obligations",
    )
    return {
        "schema": "case-0016-reviewed-gold-v1",
        "primary": review,
        "frame": {k: frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")},
        "provenance": {
            "MODEL": "GPT-6 Astra",
            "REASONING": "High",
            "designated_configuration": True,
            "source": "PRIMARY_ASTRA_HIGH",
            "semantic_transformation": "NONE",
            "treatment_blind": True,
            "automatic_second_reviewer": False,
            "primary_sha256": HASHES,
            "runtime_identity_note": review["primary"]["reviewer"][
                "runtime_identity_note"
            ],
        },
    }


def validate(gold: Any) -> Any:
    source, packet, module = authenticate()
    module.validate_review(gold["primary"], packet)
    require(
        gold["primary"] == source and gold == construct_gold(),
        "Exact unchanged reviewed projection",
    )
    return module.statistics(source)


def write_new(files: dict[Path, bytes]) -> None:
    if any(path.exists() for path in files):
        raise FileExistsError("Refusing artifact overwrite")
    for path, raw in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as stream:
            stream.write(raw)


def outputs() -> dict[str, bytes]:
    gold = construct_gold()
    stats = validate(gold)
    review = gold["primary"]
    parts = [
        "# Case 0016 reviewed development gold\n",
        "PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. No reconciliation or second reviewer.\n",
        (ADJ / "primary/STAGE_C_REVIEW.md").read_bytes().decode(),
    ]
    for name, value in [
        ("Provenance", gold["provenance"]),
        (
            "Complete positive cells and spans",
            {
                "cells": [c for c in review["cells"] if c["label"] != "UNNECESSARY"],
                "spans": review["primary"]["spans"],
            },
        ),
        ("All units and alternatives", review["primary"]["units"]),
        (
            "All witnesses and intersections",
            {
                k: review[k]
                for k in ("minimal_witnesses", "obligation_indispensability")
            },
        ),
        ("Complete task sufficiency", review["task_sufficiency"]),
        (
            "Gaps, limitations, ambiguities and self-review",
            {
                k: review["primary"][k]
                for k in ("gaps", "limitations", "ambiguities", "self_review")
            },
        ),
    ]:
        parts += ["## " + name + "\n", "```json\n" + encoded(value).decode() + "```\n"]
    files = {
        "reviewed_gold.json": encoded(gold),
        "reviewed_statistics.json": encoded(stats),
        "REVIEWED_GOLD.md": ("\n".join(parts).rstrip() + "\n").encode(),
        "reviewed_validation.json": encoded(
            {
                "status": "PASS",
                "semantic_transformation": "NONE",
                "statistics": stats,
                "primary_validation": load(ADJ / "primary/stage_c_validation.json"),
                "mechanical_only": True,
            }
        ),
    }
    files["reviewed_hashes.json"] = encoded(
        {
            "sha256": {n: sha(b) for n, b in files.items()},
            "materializer_sha256": sha(Path(__file__).read_bytes()),
            "import_metadata_sha256": sha((ADJ / "IMPORT.json").read_bytes()),
            "excluded": [".local", ".scratch", "self hash to avoid cycle"],
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


def import_primary() -> None:
    destination = ADJ / "primary"
    require(
        not destination.exists() and not (ADJ / "IMPORT.json").exists(),
        "Import overwrite refused",
    )
    raw = {n: (STERILE / n).read_bytes() for n in HASHES}
    require({n: sha(b) for n, b in raw.items()} == HASHES, "Sterile hashes")
    publication = load(CASE / "stage_c/publication.json")
    for name, expected in publication["packet_artifact_sha256"].items():
        require(
            sha((STERILE / name).read_bytes()) == expected
            and (STERILE / name).read_bytes() == (PACKET / name).read_bytes(),
            "Five original inputs: " + name,
        )
    write_new({destination / n: b for n, b in raw.items()})
    authenticate()
    metadata = {
        "MODEL": "GPT-6 Astra",
        "REASONING": "High",
        "designated_configuration": True,
        "source": "PRIMARY_ASTRA_HIGH",
        "semantic_transformation": "NONE",
        "treatment_blind": True,
        "automatic_second_reviewer": False,
        "sterile_source": str(STERILE),
        "sha256": HASHES,
        "packet_digest_scopes": {
            k: publication[k]
            for k in (
                "archive_sha256",
                "canonical_payload_sha256",
                "manifest_sha256",
                "integrity_sha256",
            )
        },
        "packet_preservation": "EXACT_ALL_FIVE_INPUTS",
        "sterile_replay": "PASS_EXACT_DERIVED_BYTES_22_ADVERSARIAL_CHECKS",
        "scratch": "PRESENT_OPERATIONAL_ONLY_NOT_IMPORTED",
        "operational_artifacts": "EXCLUDED",
        "confirmation_reserve": "NOT_ACCESSED",
        "writer": "Read-only process inspection found no concrete competing writer targeting this exact worktree; unrelated repository-context-retrieval process excluded. Bare Codex CLI has no target in its command line; exclusivity is not claimed.",
    }
    write_new({ADJ / "IMPORT.json": encoded(metadata)})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("import", "build", "verify"))
    mode = parser.parse_args().mode
    if mode == "import":
        import_primary()
    elif mode == "build":
        write_new({ROOT / n: raw for n, raw in outputs().items()})
    else:
        sys.stdout.write(encoded(verify()).decode())


if __name__ == "__main__":
    main()
