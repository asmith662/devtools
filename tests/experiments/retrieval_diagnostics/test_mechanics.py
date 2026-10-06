# Copyright (c) 2026
# ruff: noqa: COM812, FBT001, PLR2004, PT011 -- parametrized mechanics and boundary rejection groups
"""Score truth, conservative misses and obligation-relative overtaker evidence."""

from __future__ import annotations

import math
from dataclasses import replace
from typing import TYPE_CHECKING, cast

import pytest

from experiments.retrieval_diagnostics.mechanics import Mechanics, spans
from experiments.retrieval_diagnostics.models import (
    Configuration,
    DiagnosticPolicy,
    Exclusion,
    SupportReference,
)
from experiments.retrieval_diagnostics.serialization import encode
from tests.context.retrieval.lexical._helpers import _document
from tests.experiments.retrieval_diagnostics.helpers import capture, judged

if TYPE_CHECKING:
    from typing import Any

    from experiments.retrieval_diagnostics.models import LaneCapture

DOCS = (("a.py", "plain plain detail"), ("b.py", "plain other"), ("plain.txt", ""))


@pytest.mark.parametrize("expanded", [False, True])
def test_actual_scores_idf_tf_lengths_and_independent_filename_weight(
    expanded: bool,
) -> None:
    """Independent arithmetic must reproduce both actual implementations."""
    c = capture(DOCS, expanded=expanded)
    engine = Mechanics(c)
    resource = c.resources[0]
    t = engine.terms(resource)[0]
    expected_idf = math.log(1 + (3 - 2 + 0.5) / (2 + 0.5))
    length_factor = 1 - 0.75 + 0.75 * 3 / (5 / 3)
    expected = expected_idf * 2 * 2.2 / (2 + 1.2 * length_factor)
    assert (t["tf"], t["df"], t["length"], t["average_length"]) == (2, 2, 3, 5 / 3)
    assert t["idf"] == pytest.approx(expected_idf)
    assert t["normalized_length_factor"] == pytest.approx(length_factor)
    assert t["contribution"] == pytest.approx(expected)
    for row in c.rows:
        record = engine.explain(row.resource)
        assert record["score"] == pytest.approx(row.score, abs=1e-10)
        assert record["score_reconstructed"] is True
    filename = engine.explain(c.resources[2])["terms"][0]
    assert filename["field"] == "filename"
    assert filename["field_weight"] == 0.25
    assert filename["weighted_contribution"] == filename["contribution"] * 0.25
    assert filename["source"]["examples"][0]["observed"] == "plain"


def test_gold_profiles_and_rank_gaps_do_not_turn_unknown_into_negative() -> None:
    """Profile yields and burden remain obligation-relative and explicit."""
    c = capture(DOCS)
    labels = judged(c, ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"))
    engine = Mechanics(
        c, labels, DiagnosticPolicy(substantial_unnecessary_ahead=1, overtaker_limit=1)
    )
    p = engine.query_profile()[0]
    assert p["positive_resources_with_term"] == 3
    assert p["judged_labels"] == {"REQUIRED": 1, "HELPFUL_ONLY": 1, "UNNECESSARY": 1}
    assert p["required_yield"] == 1 / 3
    assert p["useful_yield"] == 2 / 3
    assert p["fields"][0]["df"] == 2
    assert p["fields"][0]["common_term"]
    record = engine.explain(c.rows[-1].resource)
    assert record["ranking"]["ahead"] == record["rank"] - 1
    assert record["ranking"]["predecessor_gap"] == pytest.approx(
        c.rows[-2].score - c.rows[-1].score
    )
    assert record["ranking"]["top_gap"] == pytest.approx(
        c.rows[0].score - c.rows[-1].score
    )
    assert len(record["ranking"]["top_overtakers"]) == 1
    assert record["ranking"]["top_overtakers"][0]["comparison"][
        "score_delta"
    ] == pytest.approx(c.rows[0].score - c.rows[-1].score)
    unjudged = Mechanics(c).query_profile()[0]
    assert unjudged["required_yield"] is None
    assert unjudged["unjudged_matched"] == 3
    assert (
        Mechanics(c).explain(c.rows[-1].resource)["failure_attribution"]["primary"]
        is None
    )


def test_ranking_discrimination_requires_gold_and_declared_burden() -> None:
    """A buried required witness proves local burden under the declared policy."""
    c = capture(DOCS)
    last = c.rows[-1].resource
    labels = judged(
        c, tuple("REQUIRED" if r == last else "UNNECESSARY" for r in c.resources)
    )
    engine = Mechanics(c, labels, DiagnosticPolicy(substantial_unnecessary_ahead=2))
    record = engine.explain(last)
    assert record["failure_attribution"]["primary"] == "RANKING_DISCRIMINATION_FAILURE"
    assert record["ranking"]["ahead_labels"]["UNNECESSARY"] == 2
    assert (
        record["failure_attribution"]["findings"][0]["certainty"]
        == "DETERMINISTICALLY_ESTABLISHED"
    )
    assert Mechanics(c, labels).explain(last)["failure_attribution"]["primary"] is None
    support = SupportReference(
        c.frame, last, "STRUCTURAL", "native-fact", "explicit supplied observation"
    )
    findings = engine.explain(last, (support,))["failure_attribution"]["findings"]
    relational = next(
        f for f in findings if f["classification"] == "RELATIONAL_RELEVANCE"
    )
    assert relational["diagnostic"] == "RELATIONAL_SUPPORT_PRESENT"
    assert "does not establish" in relational["limit"]
    assert all(f["certainty"] == "OUTSIDE_DIAGNOSTIC_SCOPE" for f in findings[-2:])
    with pytest.raises(ValueError, match="frame"):
        engine.explain(last, (replace(support, resource=c.rows[0].resource),))


def test_zero_bounded_and_explicit_exclusion_states_are_distinct() -> None:
    """No overlap is not semantics; bounded result omission is not lexical miss."""
    c = capture(DOCS, limit=1)
    engine = Mechanics(c)
    omitted = next(r for r in c.resources if r != c.rows[0].resource)
    assert engine.explain(omitted)["status"] == "RESULT_BOUND_OMISSION"
    assert engine.explain(omitted)["score_reconstructed"] is None
    outside = _document("absent.py", "plain").resource
    assert engine.explain(outside)["status"] == "RESOURCE_NOT_IN_FRAME"
    excluded = Mechanics(
        replace(c, exclusions=(Exclusion(outside, "UNSUPPORTED_RESOURCE_TYPE"),))
    )
    assert excluded.explain(outside)["status"] == "UNSUPPORTED_RESOURCE_TYPE"
    miss = capture(DOCS, "missing")
    assert (
        Mechanics(miss).explain(miss.resources[0])["status"] == "NO_QUERY_TERM_OVERLAP"
    )
    assert Mechanics(miss).query_profile()[0]["positive_resources_with_term"] == 0
    content = capture(DOCS, content_only=True)
    assert len(content.fields) == 1
    assert (
        Mechanics(content).explain(content.resources[2])["status"]
        == "NO_QUERY_TERM_OVERLAP"
    )


def test_zero_weight_evidence_cannot_generate_positive_universe() -> None:
    """Frozen field eligibility and score weight are separate facts."""
    c = capture(DOCS)
    zero = replace(
        c,
        configuration=replace(c.configuration, filename_weight=0),
        fields=(c.fields[0], replace(c.fields[1], weight=0)),
        rows=tuple(r for r in c.rows if r.resource != c.resources[2]),
    )
    engine = Mechanics(zero)
    assert engine.explain(c.resources[2])["status"] == "ALL_CONTRIBUTIONS_NONPOSITIVE"
    assert engine.query_profile()[0]["positive_resources_with_term"] == 2


@pytest.mark.parametrize(
    "mutation",
    [
        "query",
        "duplicate_resources",
        "duplicate_fields",
        "unknown_field",
        "source",
        "length",
        "average",
        "weight",
        "duplicate_posting",
        "bad_posting",
        "tf",
        "missing_posting",
        "duplicate_rows",
        "rank_order",
        "score",
        "term_coverage",
        "term_idf",
        "missing_positive",
        "exclusion",
    ],
)
def test_rejects_inconsistent_frozen_evidence(mutation: str) -> None:
    """Captures cannot produce plausible explanations with invented mechanics."""
    c = capture(DOCS)
    f, row = c.fields[0], c.rows[0]
    variants: dict[str, LaneCapture] = {
        "query": replace(c, query_terms=("invented",)),
        "duplicate_resources": replace(c, resources=c.resources + c.resources[:1]),
        "duplicate_fields": replace(c, fields=c.fields + c.fields[:1]),
        "unknown_field": replace(c, fields=(replace(f, name="semantic"),)),
        "source": replace(
            c, fields=(replace(f, texts=("other", *f.texts[1:])), c.fields[1])
        ),
        "length": replace(
            c,
            fields=(
                replace(
                    f,
                    lengths=(99, *f.lengths[1:]),
                    average_length=(99 + sum(f.lengths[1:])) / 3,
                ),
                c.fields[1],
            ),
        ),
        "average": replace(c, fields=(replace(f, average_length=99), c.fields[1])),
        "weight": replace(c, fields=(replace(f, weight=2), c.fields[1])),
        "duplicate_posting": replace(
            c, fields=(replace(f, postings=f.postings + f.postings[:1]), c.fields[1])
        ),
        "bad_posting": replace(
            c, fields=(replace(f, postings=(("plain", ((99, 1),)),)), c.fields[1])
        ),
        "tf": replace(
            c,
            fields=(
                replace(
                    f,
                    postings=tuple(
                        (t, ((0, 1), (1, 1))) if t == "plain" else (t, p)
                        for t, p in f.postings
                    ),
                ),
                c.fields[1],
            ),
        ),
        "missing_posting": replace(
            c,
            fields=(
                replace(
                    f, postings=tuple((t, p) for t, p in f.postings if t != "plain")
                ),
                c.fields[1],
            ),
        ),
        "duplicate_rows": replace(c, rows=c.rows + c.rows[:1]),
        "rank_order": replace(
            c,
            rows=tuple(replace(r, rank=i + 1) for i, r in enumerate(reversed(c.rows))),
        ),
        "score": replace(c, rows=(replace(row, score=row.score + 0.1), *c.rows[1:])),
        "term_coverage": replace(c, rows=(replace(row, terms=()), *c.rows[1:])),
        "term_idf": replace(
            c,
            rows=(
                replace(row, terms=(replace(row.terms[0], idf=99), *row.terms[1:])),
                *c.rows[1:],
            ),
        ),
        "missing_positive": replace(c, rows=c.rows[:-1]),
        "exclusion": replace(
            c, exclusions=(Exclusion(c.resources[0], "RESOURCE_NOT_IN_FRAME"),)
        ),
    }
    with pytest.raises(ValueError):
        Mechanics(variants[mutation])


def test_judgment_identity_and_configuration_validation_and_serialization() -> None:
    """Gold frame/type errors stop; serialization has stable explicit values."""
    c = capture(DOCS)
    labels = judged(c, ("REQUIRED", "HELPFUL_ONLY", "UNNECESSARY"))
    with pytest.raises(ValueError, match="Duplicate judgments"):
        Mechanics(c, labels + labels[:1])
    with pytest.raises(ValueError, match="obligation"):
        Mechanics(replace(c, obligation=None), labels)
    with pytest.raises(ValueError):
        replace(labels[0], units=("unit", "unit"))
    with pytest.raises(ValueError):
        Configuration("A", "index", "canonical", 1.2, 0.75, -1)
    with pytest.raises(ValueError):
        replace(DiagnosticPolicy(), common_fraction=float("nan"))
    with pytest.raises(ValueError):
        SupportReference(c.frame, c.resources[0], "EXACT", "", "source")
    assert c.configuration.identity != replace(c.configuration, b=0.5).identity
    record = Mechanics(c, labels).explain(c.resources[0])
    assert record["subject"]["query_text"] == c.query
    assert encode(record) == encode(Mechanics(c, labels).explain(c.resources[0]))
    assert encode({"b": 2, "a": 1}) == encode({"a": 1, "b": 2})
    with pytest.raises(ValueError):
        encode({"score": float("nan")})
    span = spans("CandidateMemberResolution", "member", "identifier")
    assert span["examples"][0]["derived_subtoken"]
    assert span["examples"][0]["start"] == 0
    assert spans("plain plain plain plain", "plain", "canonical")["occurrences"] == 4
    assert len(spans("plain plain plain plain", "plain", "canonical")["examples"]) == 3


def test_output_mutation_cannot_corrupt_reconstruction_cache() -> None:
    """Caller-owned JSON output cannot alter validated captured mechanical truth."""
    c = capture(DOCS)
    engine = Mechanics(c)
    record = engine.explain(c.resources[0])
    record["terms"][0]["contribution"] = 999
    assert engine.explain(c.resources[0])["score_reconstructed"] is True
    with pytest.raises(ValueError):
        Mechanics(
            replace(c, rows=(replace(c.rows[0], score=float("nan")), *c.rows[1:]))
        )


def test_exclusion_requires_a_frozen_supported_reason() -> None:
    """Semantic guesses cannot become mechanical exclusion reasons."""
    c = capture(DOCS)
    with pytest.raises(ValueError, match="exclusion reason"):
        Exclusion(c.resources[0], cast("Any", "SEMANTICALLY_IRRELEVANT"))
