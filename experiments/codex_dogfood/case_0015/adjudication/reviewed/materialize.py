"""Publish unchanged sealed Astra semantics; physical I/O is an import boundary.

The canonical historical text helper normalizes newlines and cannot authenticate
physical scientific bytes. This case-local serializer reads exact bytes only;
it adds no framework primitive, semantic reviewer, or treatment operation.
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
STERILE = Path(r"C:\Users\recoveryadmin\CodexSterile\case_0015_stage_c_a2445d3fe86b")
HASHES = {
    "stage_c_review.json": "20b2c858bd8d02a79576b1d48f9d773738e32231f03277232c6d9e84b148cd77",
    "stage_c_statistics.json": "496b5fbb1e76c108b62448c8a3dddf35daf3c8ac344a7645b24526918fc24d3b",
    "STAGE_C_REVIEW.md": "08f9ea50efbec6586f69629872874461e56335f68178cc29364d46fa3aaaa1be",
    "stage_c_validation.json": "9a9637af76d8d5271da6d25018eb7c08f0eeacff23ba54560eda906b433d533c",
    "stage_c_hashes.json": "1e5420fb77646cf19dbaa869861a89718ac4e68b1060cf3b1a02ff25c26c2efd",
    "stage_c_method.md": "8dd63021d327c9be33f3e639927b457e56b1d4cc7c4cf7cdfb7ffafd8665c6ac",
    "stage_c_builder.py": "5322777cd14c485ba72e388731d11da3fa63903466a51ddbbbb8f32bcee45e19",
}
BLIND = {
    "BM25F formula",
    "Git/history",
    "IDF",
    "candidate results",
    "confirmation data",
    "contributions",
    "costs/timings",
    "decision rule",
    "decomposition",
    "experimental field metadata",
    "external web information",
    "field parameters",
    "gates",
    "inversions",
    "metrics",
    "parent directory",
    "prior Codex-session content",
    "prior R2 interpretation",
    "prior gold",
    "prior semantic adjudication",
    "query analyses",
    "rankings",
    "repository checkout",
    "reserve data",
    "retrieval queries",
    "scores",
    "sibling workspaces",
    "treatment arms",
    "union DF",
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
    for name, expected in HASHES.items():
        require(
            sha((primary / name).read_bytes()) == expected, "Sealed primary: " + name
        )
    manifest = load(primary / "stage_c_hashes.json")
    for name, expected in manifest["input_sha256"].items():
        require(sha((PACKET / name).read_bytes()) == expected, "Sealed packet: " + name)
    raw = gzip.decompress((PACKET / "resources.json.gz").read_bytes())
    require(sha(raw) == manifest["canonical_payload_sha256"], "Canonical payload")
    payload = json.loads(raw)
    review = load(primary / "stage_c_review.json")
    require(
        set(review["blindness"]["excluded_category_access"]) == BLIND
        and set(review["blindness"]["excluded_category_access"].values()) == {"NO"},
        "Complete blindness attestation",
    )
    require(
        review["model"] == "GPT-6 Astra"
        and review["reasoning"] == "High"
        and review["reviewer_count"] == 1
        and review["blindness"]["second_reviewer"] is False,
        "Primary reviewer identity",
    )
    require(not review["unresolved_cells"], "Unresolved primary gold")
    spec = importlib.util.spec_from_file_location(
        "case0015_primary_invariants", primary / "stage_c_builder.py"
    )
    require(spec is not None and spec.loader is not None, "Primary validator loader")
    assert spec is not None  # noqa: S101
    assert spec.loader is not None  # noqa: S101
    module: Any = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    # Authenticate the original inputs separately; never reapply a five-file
    # directory whitelist to a completed workspace or import directory.
    module.validate_review(review, payload)
    generated = module.render(review, payload)
    for name, data in generated.items():
        require(
            (primary / name).read_bytes() == data,
            "Primary deterministic replay: " + name,
        )
    require(
        module.hash_manifest(generated) == manifest, "Primary scientific hashes replay"
    )
    return review, payload, module


def construct_gold() -> Any:
    review, payload, _ = authenticate()
    frame = load(CASE / "frame.json")
    native = json.loads(gzip.decompress((CASE / "resources.json.gz").read_bytes()))
    require(
        payload["eligible_resources"]
        == [{k: r[k] for k in payload["eligible_resources"][0]} for r in native],
        "Exact semantic resource frame",
    )
    require(
        review["resource_frame"]
        == [{k: r[k] for k in review["resource_frame"][0]} for r in frame["resources"]],
        "Exact gold/native metadata frame",
    )
    design = load(CASE / "protocol.json")
    require(
        (review["case"], review["task_identity"], review["task_text"])
        == (design["case"], design["task_identity"], design["task_text"]),
        "Exact case/task binding",
    )
    return {
        "schema": "case-0015-reviewed-gold-v1",
        "primary": review,
        "frame": {k: frame[k] for k in ("repository_id", "snapshot_id", "corpus_id")},
        "resource_bindings": review["resource_frame"],
        "provenance": {
            "source": "PRIMARY_ASTRA_HIGH",
            "semantic_transformation": "NONE",
            "primary_sha256": HASHES,
            "MODEL": "GPT-6 Astra",
            "REASONING": "High",
            "treatment_blind": True,
            "automatic_second_reviewer": False,
            "projection": "Full unchanged primary object; exact frame bindings only.",
        },
    }


def validate(gold: Any) -> Any:
    source, payload, module = authenticate()
    module.validate_review(gold["primary"], payload)
    require(
        gold["primary"] == source and gold == construct_gold(),
        "Exact reviewed projection identity",
    )
    return module.statistics(source)


def markdown(gold: Any, stats: Any) -> bytes:
    review = gold["primary"]
    lines = [
        "# Case 0015 reviewed development gold",
        "",
        "Provenance: PRIMARY_ASTRA_HIGH; semantic_transformation = NONE. One primary review; no reconciliation or second reviewer.",
        "",
        (ADJ / "primary/STAGE_C_REVIEW.md").read_bytes().decode(),
    ]
    for name, value in [
        ("Reviewed statistics", stats),
        (
            "Exact frame and provenance",
            {"frame": gold["frame"], "provenance": gold["provenance"]},
        ),
        (
            "Complete positive cells and exact spans",
            [c for c in review["cells"] if c["label"] != "UNNECESSARY"],
        ),
        (
            "All semantic units and exact support alternatives/spans",
            review["semantic_units"],
        ),
        ("All minimal witnesses", review["witnesses"]),
        ("Obligation intersections", review["obligation_indispensability"]),
        ("All task combinations", review["task_combinations"]),
        ("All sufficient resource unions", review["sufficient_resource_unions"]),
        (
            "All inclusion-minimal resource unions",
            review["inclusion_minimal_resource_unions"],
        ),
        ("Sufficient unit structure", review["sufficient_unit_unions"]),
        ("Task indispensable resources", review["task_indispensable_resources"]),
        ("Task indispensable units", review["task_indispensable_units"]),
        ("All gaps", review["gaps"]),
        ("All limitations", review["limitations"]),
        ("Preserved ambiguity", review["ambiguities"]),
    ]:
        lines += [
            "## " + name,
            "",
            "```json",
            encoded(value).decode().rstrip(),
            "```",
            "",
        ]
    return ("\n".join(lines).rstrip() + "\n").encode()


def write_new(files: dict[Path, bytes]) -> None:
    if any(path.exists() for path in files):
        raise FileExistsError("Refusing to overwrite reviewed artifacts")
    for path, raw in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
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
                "semantic_transformation": "NONE",
                "primary_validation": load(ADJ / "primary/stage_c_validation.json"),
                "checks": [
                    "exact sealed primary and packet bytes/replay",
                    "complete blindness",
                    "case/task/obligation/native frame",
                    "3090 exact judgments and spans",
                    "42 exact units/classes/alternatives",
                    "12 exhaustive minimal witnesses including empty O2",
                    "obligation and task intersections",
                    "32 combinations and sufficient resource/unit algebra",
                    "gaps/limitations/ambiguity unchanged",
                    "deterministic JSON/statistics/Markdown/hash replay",
                    "overwrite refusal and tamper rejection",
                ],
            }
        ),
    }
    files["reviewed_hashes.json"] = encoded(
        {
            "schema": "case-0015-reviewed-hashes-v1",
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


def import_primary() -> None:
    destination = ADJ / "primary"
    require(
        not destination.exists() and not (ADJ / "IMPORT.json").exists(),
        "Primary import overwrite refused",
    )
    raw = {n: (STERILE / n).read_bytes() for n in HASHES}
    require(
        {n: sha(b) for n, b in raw.items()} == HASHES, "Sterile primary hash mismatch"
    )
    manifest = json.loads(raw["stage_c_hashes.json"])
    for name, expected in manifest["input_sha256"].items():
        require(
            sha((STERILE / name).read_bytes()) == expected
            and (STERILE / name).read_bytes() == (PACKET / name).read_bytes(),
            "Original sealed input: " + name,
        )
    require(not (STERILE / "scratch").exists(), "Scratch must be absent")
    write_new({destination / n: b for n, b in raw.items()})
    authenticate()
    write_new(
        {
            ADJ / "IMPORT.json": encoded(
                {
                    "schema": "case-0015-primary-import-v1",
                    "MODEL": "GPT-6 Astra",
                    "REASONING": "High",
                    "treatment_blind": True,
                    "source": "PRIMARY_ASTRA_HIGH",
                    "semantic_transformation": "NONE",
                    "automatic_second_reviewer": False,
                    "sterile_source": str(STERILE),
                    "sha256": HASHES,
                    "packet_digest_scopes": load(CASE / "stage_c/publication.json")[
                        "digest_scopes"
                    ],
                    "packet_preservation": "EXACT_ALL_FIVE_INPUTS",
                    "sterile_replay": "PASS_EXACT_DERIVED_BYTES",
                    "scratch": "ABSENT",
                    "operational_artifacts": "EXCLUDED",
                    "confirmation_reserve": "NOT_ACCESSED",
                    "writer": "No concrete competing writer targeting this exact worktree found; other worktrees permitted.",
                }
            )
        }
    )


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
