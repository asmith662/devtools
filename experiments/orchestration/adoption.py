# Copyright (c) 2026
# ruff: noqa: ANN401 -- bounded immutable completed-branch evidence codec
"""Adopt a sealed completed independent branch; never cache or rerun a model."""

from __future__ import annotations

import base64
import gzip
import io
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from devtools.agents.integrations.codex.usage import capture_codex_usage
from experiments.codex_dogfood.case_0009.artifacts import digest, json_bytes
from experiments.orchestration.storage import binary, materialize, require, safe

SCHEMA = "experiment-completed-branch-seal-v1"
MAX_CLOSURE_BYTES = 128 << 20


def pack(files: dict[str, bytes]) -> bytes:
    """Reuse repository compressed JSON/base64 exact-byte artifact conventions."""
    value = {
        "schema": "completed-branch-closure-v1",
        "files": {
            name: base64.b64encode(raw).decode("ascii")
            for name, raw in sorted(files.items())
        },
    }
    raw = json_bytes(value)
    require(len(raw) <= MAX_CLOSURE_BYTES, "Unreasonable completed-branch closure")
    return gzip.compress(raw, mtime=0)


@dataclass(frozen=True)
class AdoptedBranch:
    """An authenticated immutable closure, not an execution authorization."""

    canonical: bytes
    compressed: bytes

    @property
    def value(self) -> Any:
        """Return copies of exact bound provenance."""
        return json.loads(self.canonical)

    @classmethod
    def authenticate(
        cls,
        raw: bytes,
        compressed: bytes,
        expected_sha256: str,
        compatibility_sha256: str,
    ) -> AdoptedBranch:
        """Require external seal identity, eligibility and every exact owned byte."""
        require(digest(raw) == expected_sha256, "Adoption seal digest mismatch")
        value = json.loads(raw)
        require(
            json_bytes(value) == raw and value["schema"] == SCHEMA,
            "Canonical branch seal required",
        )
        require(
            value["origin"]["operation"] == "B"
            and value["closure_file"] == "closure.json.gz",
            "Unsupported adoption operation/closure",
        )
        require(
            value["compatibility_sha256"]
            == compatibility_sha256
            == digest(json_bytes(value["compatibility"])),
            "Branch compatibility mismatch",
        )
        require(
            all(
                value["eligibility"].get(k) is True
                for k in (
                    "entered",
                    "returned",
                    "complete_artifact_closure",
                    "independent",
                    "unchanged_branch_semantics",
                )
            )
            and value["eligibility"].get("failed") is False,
            "Failed/incomplete/dependent branch is ineligible",
        )
        require(
            value["validation"]["status"] == "PASS"
            and value["validation"]["mode"] == "SEALED"
            and value["validation"]["native_archives_decoded"] == 0
            and value["validation"]["deep_correspondence_executions"] == 0,
            "Original sealed validator PASS required",
        )
        require(
            digest(compressed) == value["closure_sha256"],
            "Immutable closure digest mismatch",
        )
        branch = cls(raw, compressed)
        files = branch.files()
        entered, returned = (
            json.loads(files["provenance/" + name + ".json"])
            for name in ("ENTERED", "RETURNED")
        )
        origin = value["origin"]
        context = json.loads(files["provenance/origin-run.json"])
        proof = json.loads(files["artifacts/completion_proof.json"])
        protocol = json.loads(files["provenance/Stage-A-protocol.json"])
        require(
            origin["stage_a"] == context["plan"]["stage_a"]["checkpoint"]
            and origin["attempt"] == context["plan"]["attempt"]
            and origin["packet_commit"] == value["independence"]["packet_commit"],
            "Stage A/PACKET/attempt binding mismatch",
        )
        require(
            value["implementation"] == proof["inputs"]["implementation_sha256"]
            and bool(value["runtime"]),
            "Original implementation/runtime binding required",
        )
        require(
            digest(files["provenance/Stage-A-protocol.json"])
            == context["plan"]["stage_a"]["protocol"]["sha256"]
            and value["runtime"] == protocol["workers"]["grounding"]["runtime"],
            "Original runtime/protocol mismatch",
        )
        require(
            value["independence"]["sibling_dependency"] is False
            and value["independence"]["downstream_dependency"] is False
            and value["independence"]["forbidden_later_evidence_available"] is False
            and value["compatibility"]["original_disclosure_replay_sha256"]
            == digest(files["provenance/disclosure.bin"]),
            "Causal independence/compatibility rejected",
        )
        require(
            all(entered[k] == returned[k] == origin[k] for k in ("run_id", "case")),
            "Original branch identities differ",
        )
        require(
            entered["stage"] == returned["stage"] == "B"
            and entered["frame"] == returned["frame"] == value["frame"],
            "Branch frame/stage differs",
        )
        require(
            entered["inputs_sha256"]
            == returned["inputs_sha256"]
            == value["input_sha256"],
            "Original branch input mismatch",
        )
        require(
            returned["validation"] == value["validation"]
            and returned["files"] == value["scientific_files"],
            "Original artifact/validator closure mismatch",
        )
        require(
            digest(files["artifacts/completion_proof.json"])
            == value["validation"]["completion_proof_sha256"],
            "Completion proof mismatch",
        )
        semantic = json.loads(files["provenance/semantic-receipt.json"])
        publication = json.loads(files["provenance/origin-PACKET-publication.json"])
        process = json.loads(files["provenance/process-exit.json"])
        marker = json.loads(files["artifacts/native/execution_started.json"])
        require(
            publication["boundary"] == "PACKET"
            and publication["parent_head"] == context["approval_checkpoint"]
            and marker["run_binding"]
            == {
                "run_id": origin["run_id"],
                "stage_a_checkpoint": origin["stage_a"],
                "packet_checkpoint": origin["packet_commit"],
            },
            "Original PACKET publication binding mismatch",
        )
        require(
            semantic["status"] == "PASS"
            and semantic["process_exit"] == 0
            and semantic["model"] == value["model"]
            and semantic["reasoning"] == value["reasoning"]
            and semantic["input_sha256"] == digest(files["provenance/disclosure.bin"]),
            "Semantic process/disclosure binding mismatch",
        )
        require(
            value["original_usage"]["measurement"]["completed"]
            and value["original_usage"]["measurement"]["accepted"],
            "Original usage acceptance required",
        )
        usage = capture_codex_usage(files["provenance/stdout.jsonl"])
        require(
            len(usage) == 1 and json.loads(usage[0].raw_json) == semantic["usage"],
            "Original usage stream differs",
        )
        measured = value["original_usage"]["measurement"]
        require(
            measured["invocation_id"] == semantic["invocation"]
            and measured["backend_thread_id"]["value"] == semantic["thread_id"]
            and measured["usage"]
            == {
                "input_tokens": usage[0].counts.input_tokens,
                "cached_input_tokens": usage[0].counts.cached_input_tokens,
                "cache_write_tokens": usage[0].counts.cache_write_tokens,
                "output_tokens": usage[0].counts.output_tokens,
                "reasoning_tokens": usage[0].counts.reasoning_tokens,
                "total_tokens": None,
            },
            "Normalized original usage mismatch",
        )
        require(
            measured["requested_model"] == protocol["workers"]["grounding"]["model_id"]
            and measured["reasoning_effort"] == value["reasoning"]
            and measured["wall_seconds"]["value"] == process["duration_seconds"],
            "Original model/duration measurement mismatch",
        )
        return branch

    def compatible_inputs(self, inputs: dict[str, bytes]) -> None:
        """Authenticate unchanged scientific inputs, permitting new host mechanics."""
        files = self.files()
        for name in ("design.json", "resources.json.gz"):
            require(
                digest(inputs[name]) == self.value["scientific_files"][name],
                "Adoption scientific input differs: " + name,
            )
        require(
            inputs["INSTRUCTIONS_GROUNDING.md"] == files["provenance/instruction.bin"]
            and digest(inputs["reviewer_codec.py"])
            == self.value["compatibility"]["scientific_contract"][
                "experiments/source_grounding/reviewer.py"
            ],
            "Adoption instruction/builder differs",
        )
        original = json.loads(files["provenance/Stage-A-protocol.json"])["workers"][
            "grounding"
        ]
        current = json.loads(inputs["worker_configuration.json"])["workers"][
            "grounding"
        ]
        require(
            all(
                current[k] == original[k]
                for k in (
                    "model",
                    "model_id",
                    "reasoning",
                    "evidence_locator",
                    "response_schema",
                )
            ),
            "Adoption semantic configuration differs",
        )

    def files(self) -> dict[str, bytes]:
        """Bound decompression and authenticate the complete allowlisted closure."""
        with gzip.GzipFile(fileobj=io.BytesIO(self.compressed)) as stream:
            raw = stream.read(MAX_CLOSURE_BYTES + 1)
        require(len(raw) <= MAX_CLOSURE_BYTES, "Branch closure expansion bound")
        value = json.loads(raw)
        require(
            set(value) == {"schema", "files"}
            and value["schema"] == "completed-branch-closure-v1",
            "Branch closure schema",
        )
        files = {
            name: base64.b64decode(content, validate=True)
            for name, content in value["files"].items()
        }
        inventory = {
            name: {"bytes": len(content), "sha256": digest(content)}
            for name, content in sorted(files.items())
        }
        require(
            inventory == self.value["inventory"]
            and digest(json_bytes(inventory)) == self.value["inventory_sha256"],
            "Branch artifact inventory mismatch",
        )
        for name in files:
            safe(Path.cwd(), name)
        require(
            {
                name.removeprefix("artifacts/"): digest(content)
                for name, content in files.items()
                if name.startswith("artifacts/")
            }
            == self.value["scientific_files"],
            "Scientific branch closure incomplete",
        )
        return files

    def materialize(self, root: Path) -> dict[str, bytes]:
        """Copy scientific bytes only; no worker/model/retrieval is invoked."""
        files = {
            name.removeprefix("artifacts/"): raw
            for name, raw in self.files().items()
            if name.startswith("artifacts/")
        }
        materialize(root, files)
        return files


def load_branch(root: Path, binding: Any) -> AdoptedBranch:
    """Resolve only repository-owned exact-byte branch artifacts."""
    path = safe(root, binding["path"])
    return AdoptedBranch.authenticate(
        binary(path),
        binary(path.parent / "closure.json.gz"),
        binding["sha256"],
        binding["compatibility_sha256"],
    )
