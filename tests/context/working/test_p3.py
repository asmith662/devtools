# Copyright (c) 2026
"""Authenticated public P3 false positives remain claims, not verified facts."""

from __future__ import annotations

import ast
import hashlib
import json
import re
from pathlib import Path

from devtools.context.repository.resource import (
    ContentIdentity,
    RepositoryResourceAddress,
    RepositoryResourceOccurrence,
)
from devtools.context.working import NoteScope, SourceBinding, WorkingNotes


def test_published_false_claims_need_independent_checks() -> None:
    """Exact citations verify source, while a scoped host check resolves claims."""
    folder = Path(__file__).parent / "fixtures"
    source = (folder / "p3-candidate.txt").read_bytes()
    cases = json.loads((folder / "p3-claims.json").read_bytes())
    assert hashlib.sha256(source).hexdigest() == cases["source_sha256"]
    text = source.decode()
    assignment = next(
        node
        for node in ast.walk(ast.parse(text))
        if isinstance(node, ast.AnnAssign)
        and isinstance(node.target, ast.Name)
        and node.target.id == "_ATX_HEADING_PATTERN"
    )
    assert isinstance(assignment.value, ast.Call)
    pattern = re.compile(ast.literal_eval(assignment.value.args[0]))
    start = text.index("_ATX_HEADING_PATTERN")
    end = start + 120
    resource = RepositoryResourceOccurrence(
        RepositoryResourceAddress("markdown.py"),
        ContentIdentity.from_text(text),
        text,
        "utf-8",
        len(source),
    )
    binding = SourceBinding(
        "candidate",
        resource,
        cases["source_sha256"],
        ((0, len(text)),),
    )
    for case in cases["cases"]:
        notes = WorkingNotes(
            NoteScope("public-P3", "independent-reviewer", case["id"]),
            {"candidate": binding},
        )
        anchor = binding.anchor(start, end, text[start:end])
        literal = notes.observe(anchor)
        claim = notes.record(
            "hypothesis",
            case["claim"],
            "ATX closing-hash contract",
            (anchor,),
        )
        assert notes.status(literal) == "host-verified"
        assert notes.status(claim) == "provisional"
        match = pattern.fullmatch(case["input"])
        assert match is not None
        assert match.group("text").strip() == case["correct_candidate_title"]
        counter = notes.record(
            "conclusion",
            "This counterexample does not exhibit the claimed defect",
            "Disclosed candidate regex captures the expected title",
            (anchor,),
            contradicts=(claim.sequence,),
        )
        assert notes.status(claim) == "contested"
        notes.attest(
            counter.sequence,
            "host:literal-regex-countercheck:" + case["published_response_sha256"],
        )
        assert notes.status(claim) == "contradicted"
        assert claim.verification is None
        assert notes.status(notes.notes[-1]) == "host-verified"
