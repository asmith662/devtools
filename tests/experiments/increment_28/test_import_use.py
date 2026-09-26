# Copyright (c) 2026
# ruff: noqa: E501, PLR2004
"""Conservative source and frozen-population import-use checks."""

from __future__ import annotations

import ast
import hashlib
import json
from typing import Any

import pytest

from experiments.increment_27.depth_diagnostic import canonical_json_bytes
from experiments.increment_27.structural_imports.mechanics import (
    read_candidate_artifact,
)
from experiments.increment_28.import_use import (
    EVIDENCE_NAME,
    FREEZE_NAME,
    ROOT27,
    _qualified_read,
    build_freeze,
)


def _classify(content: str, *, requested: str, start: int = 0, end: int | None = None) -> dict[str, Any]:
    tree = ast.parse(content)
    declaration = tree.body[0]
    assert isinstance(declaration, ast.Import | ast.ImportFrom)
    alias = declaration.names[0]
    resolution = {
        "module_text": alias.name if isinstance(declaration, ast.Import) else declaration.module,
        "imported_name": None if isinstance(declaration, ast.Import) else alias.name,
        "local_alias": alias.asname,
        "requested_module": requested,
    }
    path = {
        "declaration_ordinal": 0,
        "import_source_span": [declaration.lineno, declaration.col_offset, declaration.end_lineno, declaration.end_col_offset],
    }
    return _qualified_read(
        content=content, tree=tree, resolution=resolution, path=path,
        window={"char_start": start, "char_end": len(content) if end is None else end},
    )


@pytest.mark.parametrize(
    ("content", "requested", "state", "binding"),
    [
        ("from pkg import thing\nx = thing\n", "pkg", "SUPPORTED", "thing"),
        ("from pkg import thing as local\nx = local\n", "pkg", "SUPPORTED", "local"),
        ("import pkg\nx = pkg\n", "pkg", "SUPPORTED", "pkg"),
        ("import pkg as short\nx = short\n", "pkg", "SUPPORTED", "short"),
        ("import pkg.sub\nx = pkg.sub\n", "pkg.sub", "SUPPORTED", "pkg"),
        ("import pkg.sub\nx = pkg\n", "pkg.sub", "NO_QUALIFYING_OCCURRENCE", "pkg"),
        ("from pkg import thing\nx = 'thing'\n", "pkg", "NO_QUALIFYING_OCCURRENCE", "thing"),
        ("from pkg import thing\nthing = 1\nx = thing\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\ndef f():\n    x = thing\n", "pkg", "SUPPORTED", "thing"),
        ("from pkg import thing\ndef f():\n    x = thing\n    thing = 1\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\nclass C:\n    x = thing\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\ndef f(x: thing):\n    pass\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\ndef f():\n    global thing\n    thing = 2\nx = thing\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\nmatch 1:\n    case thing:\n        pass\nx = thing\n", "pkg", "INDETERMINATE", "thing"),
        ("from pkg import thing\né = thing\n", "pkg", "SUPPORTED", "thing"),
    ],
)
def test_conservative_import_binding(
    content: str, requested: str, state: str, binding: str,
) -> None:
    """Only source-bound reads under covered scopes qualify."""
    result = _classify(content, requested=requested)
    assert result["state"] == state
    assert result["local_binding"] == binding
    if state == "SUPPORTED":
        assert result["occurrences"]
        for occurrence in result["occurrences"]:
            start, end = occurrence["char_span"]
            assert occurrence["text"] == content[start:end]


def test_import_statement_and_window_boundaries() -> None:
    """Declaration text never qualifies and partial overlaps stay uncertain."""
    content = "from pkg import thing\nx = thing\n"
    assert _classify(content, requested="pkg", end=content.index("x ="))["state"] == "NO_QUALIFYING_OCCURRENCE"
    start = content.index("thing", content.index("x ="))
    assert _classify(content, requested="pkg", start=start, end=start + 2)["state"] == "INDETERMINATE"
    assert _classify(content, requested="pkg", start=start, end=start + len("thing"))["state"] == "SUPPORTED"


def test_fixed_artifact_identity_and_population() -> None:
    """Evidence preserves every fixed pair and deterministic serialization."""
    frozen = json.loads((ROOT27.parent / "increment_28" / FREEZE_NAME).read_text(encoding="utf-8"))
    artifact_path = ROOT27.parent / "increment_28" / EVIDENCE_NAME
    evidence = json.loads(artifact_path.read_text(encoding="utf-8"))
    candidates = read_candidate_artifact(ROOT27 / "structural_import_candidates.json.gz")
    assert frozen == build_freeze()
    assert len(evidence["cases"]) == 24
    assert [case["case_id"] for case in evidence["cases"]] == frozen["payload"]["development_case_ids"]
    assert not set(frozen["payload"]["heldout_case_ids_sealed"]) & {case["case_id"] for case in evidence["cases"]}
    assert evidence["candidate_identity"] == candidates["content_identity"]
    assert evidence["freeze_identity"] == frozen["content_identity"]
    assert evidence["content_identity"] == hashlib.sha256(canonical_json_bytes({key: value for key, value in evidence.items() if key != "content_identity"})).hexdigest()
    assert artifact_path.read_bytes() == (json.dumps(evidence, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    assert evidence["usefulness_outcomes_loaded"] is False
    assert evidence["new_candidate_resources"] == 0
    assert evidence["heldout_executed"] is False
    for source, enriched in zip(candidates["cases"], evidence["cases"], strict=True):
        assert source["case_id"] == enriched["case_id"]
        source_out = {row["address"]: row for row in source["arms"]["outgoing"]["candidates"]}
        source_in = {row["address"] for row in source["arms"]["incoming"]["candidates"]}
        enriched_out = {row["address"]: row for row in enriched["outgoing"]}
        assert set(source_out) == set(enriched_out)
        assert set(enriched["incoming_only_addresses"]) == source_in - set(source_out)
        for address, row in enriched_out.items():
            assert len(row["supports"]) == source_out[address]["support_count"]
            assert [support["relation_identity"] for support in row["supports"]] == [path["relation_identity"] for path in source_out[address]["paths"]]
            assert row["incoming"] == (address in source_in)
            assert row["absent_all_saved_positive_lexical"] == source_out[address]["absent_all_saved_positive_lexical"]
            assert sum(row["state_counts"].values()) == len(row["supports"])
    assert evidence["summary"]["fixed_union_pairs"] == 109
    assert evidence["summary"]["outgoing"]["candidate_pairs"] == 99
    assert evidence["summary"]["incoming_only_pairs"] == 10


def test_no_judgment_fields_in_preoutcome_artifact() -> None:
    """The pre-outcome checkpoint contains no usefulness state or change path."""
    text = (ROOT27.parent / "increment_28" / EVIDENCE_NAME).read_text(encoding="utf-8")
    for forbidden in ('"USEFUL"', '"NOT_USEFUL"', '"UNJUDGED"', '"judgment"', '"changed_paths"'):
        assert forbidden not in text
