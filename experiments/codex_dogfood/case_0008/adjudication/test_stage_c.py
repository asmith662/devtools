# Copyright (c) 2026
# ruff: noqa: INP001, COM812, E501, S101, PLR2004
"""Isolated Stage C integrity tests; no devtools or experiment-result imports."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from collections.abc import Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build_judgments import build
from stage_c import (
    DIGESTS,
    HERE,
    freeze,
    load_packet,
    reject_forbidden,
    replay,
    serialize,
    statistics,
    validate,
)


@pytest.fixture
def tmp_path() -> Iterator[Path]:
    """Keep newly created test artifacts inside the authorized Case directory."""
    with tempfile.TemporaryDirectory(prefix="stage-c-test-", dir=HERE) as directory:
        target = Path(directory).resolve()
        target.relative_to(HERE.resolve())
        yield target


@pytest.fixture(scope="module")
def packet() -> tuple[dict, dict]:
    """Load only the two sealed blind inputs."""
    return load_packet()


@pytest.fixture(scope="module")
def gold() -> dict:
    """Build the manually selected independent gold."""
    return build()


def test_packet_and_complete_coverage(packet: tuple[dict, dict], gold: dict) -> None:
    """Verify all native frame identities and exact full-product coverage."""
    manifest, archive = packet
    validate(gold, manifest, archive)
    assert len(manifest["shared_anchors"]) == 11
    assert len(manifest["obligations"]) == 13
    assert len(archive["resources"]) == 523
    assert gold["exact_task"] == manifest["task"]
    stats = statistics(gold)
    assert stats["coverage"] == {
        "expected_resources": 523,
        "observed_resources": 523,
        "expected_cells": 6799,
        "observed_cells": 6799,
        "duplicate_expected": 0,
        "duplicate_observed": 0,
        "missing": 0,
        "unexpected": 0,
    }
    assert sum(stats["cell_labels"].values()) == 6799
    assert set(stats["applicability"].values()) == {"APPLICABLE"}
    assert stats["inherent_discovery"] == 0


def test_digest_rejection(tmp_path: Path) -> None:
    """A changed blind input fails before its JSON can be interpreted."""
    for name in DIGESTS:
        (tmp_path / name).write_bytes((HERE / name).read_bytes())
    for name in DIGESTS:
        original = (tmp_path / name).read_bytes()
        (tmp_path / name).write_bytes(original + b" ")
        with pytest.raises(ValueError, match="digest mismatch"):
            load_packet(tmp_path)
        (tmp_path / name).write_bytes(original)


@pytest.mark.parametrize(
    "field",
    [
        "lexical_query",
        "bm25_settings",
        "role_preferences",
        "native_rank",
        "routed_position",
        "grounding_request",
        "locator",
        "grounding_disposition",
        "generation_recipe_identity",
        "generated_resources",
        "projection_operator",
        "reference_fanout",
        "import_dependency",
        "result_bound",
        "work_bound",
        "recovery_history",
        "effectiveness_comparison",
    ],
)
def test_forbidden_nested_fields(field: str) -> None:
    """Reject treatment-equivalent structural keys at arbitrary depth."""
    with pytest.raises(ValueError, match="Forbidden field"):
        reject_forbidden({"container": [{field: None}]})
    reject_forbidden(
        {
            "text": "grounding generation candidate witness readiness import Reference acquisition"
        }
    )


@pytest.mark.parametrize(
    "mutation",
    [
        "schema",
        "foreign_frame",
        "task",
        "obligation",
        "applicability",
        "unit_target",
        "span",
        "excerpt",
        "empty_alternative",
        "foreign_alternative",
        "duplicate_alternative",
        "inferability",
        "prerequisite",
        "duplicate_cell",
        "missing_cell",
        "unexpected_cell",
        "false_label",
        "unit_coverage",
        "gap",
        "unknown_field",
        "blindness",
    ],
)
def test_reject_invalid_gold(  # noqa: C901, PLR0912
    packet: tuple[dict, dict],
    gold: dict,
    mutation: str,
) -> None:
    """Exercise meaningful corruption paths before freezing gold."""
    bad = copy.deepcopy(gold)
    obligation = bad["obligations"][0]
    judgment = obligation["unit_judgments"][0]
    if mutation == "schema":
        bad["schema"] = "other"
    elif mutation == "foreign_frame":
        bad["snapshot_id"] = "f" * 64
    elif mutation == "task":
        bad["exact_task"] += "changed"
    elif mutation == "obligation":
        obligation["frozen_obligation"]["satisfaction_criterion"]["statement"] = (
            "changed"
        )
    elif mutation == "applicability":
        obligation["applicability"] = "unsupported"
    elif mutation == "unit_target":
        bad["information_units"][0]["resource"]["content_identity"] = "f" * 64
    elif mutation == "span":
        bad["information_units"][0]["spans"][0]["start_line"] = 0
    elif mutation == "excerpt":
        bad["information_units"][0]["spans"][0]["excerpt"] += "changed"
    elif mutation == "empty_alternative":
        obligation["acceptable_alternatives"][0]["all_units"] = []
    elif mutation == "foreign_alternative":
        obligation["acceptable_alternatives"][0]["all_units"].append("unknown")
    elif mutation == "duplicate_alternative":
        obligation["acceptable_alternatives"].append(
            obligation["acceptable_alternatives"][0]
        )
    elif mutation == "inferability":
        judgment["inferability"] = "unknown"
    elif mutation == "prerequisite":
        judgment["inferability"] = "INHERENT_DISCOVERY"
        judgment["discovery"] = {
            "later_observation": "observe",
            "prerequisite": "",
            "why_not_static": "unknown",
        }
    elif mutation == "duplicate_cell":
        bad["resource_judgments"][-1] = bad["resource_judgments"][0]
    elif mutation == "missing_cell":
        bad["resource_judgments"].pop()
    elif mutation == "unexpected_cell":
        bad["resource_judgments"][0]["obligation"] = "unknown"
    elif mutation == "false_label":
        bad["resource_judgments"][0]["judgment"] = "REQUIRED"
    elif mutation == "unit_coverage":
        judgment["judgment"] = "HELPFUL_ONLY"
    elif mutation == "gap":
        bad["task_gaps"] = [
            {
                "identity": "TASK_INTERPRETATION_GAP-example",
                "requirement": "invented",
                "task_evidence": "not in task",
                "why_mandatory": "invented",
                "inferability": "INFERABLE_AT_START",
                "discovery": None,
            }
        ]
    elif mutation == "unknown_field":
        obligation["extra"] = "unknown"
    elif mutation == "blindness":
        bad["blindness_attestation"]["confirmation_accessed"] = True
    with pytest.raises(ValueError, match=r".+"):
        validate(bad, *packet)


def test_freeze_replay_overwrite_and_tamper(gold: dict, tmp_path: Path) -> None:
    """Frozen bytes replay exactly and cannot be overwritten or silently changed."""
    destination = tmp_path / "judgments.json"
    digest = freeze(gold, destination)
    data = destination.read_bytes()
    assert digest == hashlib.sha256(data).hexdigest()
    assert serialize(json.loads(data)) == data == serialize(build())
    assert replay(destination) == statistics(gold)
    with pytest.raises(FileExistsError, match="Refusing to overwrite"):
        freeze(gold, destination)
    destination.write_bytes(data + b" ")
    with pytest.raises(ValueError, match="seal mismatch"):
        replay(destination)


def test_existing_seal_refuses_freeze(gold: dict, tmp_path: Path) -> None:
    """Even a lone existing seal prevents a new freeze."""
    destination = tmp_path / "judgments.json"
    destination.with_suffix(".sha256").write_text("existing", encoding="ascii")
    with pytest.raises(FileExistsError):
        freeze(gold, destination)
    assert not destination.exists()
