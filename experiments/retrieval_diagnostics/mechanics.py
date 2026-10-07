# Copyright (c) 2026
# ruff: noqa: C901, COM812, E501, EM101, PLR0912, PLR0915, TRY003, SLF001 -- bounded diagnostics and same-class validated cache projection

"""Replay independent-field BM25 mechanics from evidence, without reranking."""

from __future__ import annotations

import math
from collections import Counter
from copy import deepcopy
from dataclasses import asdict, replace
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Any

from devtools.context.retrieval.lexical.analysis import iter_lexical_spans
from devtools.context.retrieval.lexical.bm25 import RepositoryTextLexicalBm25Settings
from devtools.context.retrieval.lexical.scoring import (
    calculate_bm25_inverse_document_frequency,
    calculate_bm25_term_contribution,
)
from devtools.evaluation.coverage import compare_identity_coverage
from experiments.identifier_sparse.analysis import iter_terms
from experiments.retrieval_diagnostics.attribution import classify
from experiments.retrieval_diagnostics.models import (
    Configuration,
    DiagnosticPolicy,
    DiagnosticSubject,
    Judgment,
    LaneCapture,
    RankedCapture,
    SupportReference,
    TermCapture,
)
from experiments.retrieval_identifier import expand_identifier_terms

if TYPE_CHECKING:
    from devtools.context.repository.resource import RepositoryResourceOccurrence

TOLERANCE = 1e-10
DEFAULT_POLICY = DiagnosticPolicy()


def spans(text: str, term: str, analyzer: str, *, limit: int = 3) -> dict[str, Any]:
    """Retain exact whole/subtoken lineage and bounded occurrence examples."""
    return _span_profiles(text, (term,), analyzer, limit=limit)[term]


def _span_profiles(
    text: str, wanted: tuple[str, ...], analyzer: str, *, limit: int = 3
) -> dict[str, dict[str, Any]]:
    """Scan once for all lane terms without changing exact occurrence semantics."""
    profiles: dict[str, dict[str, Any]] = {
        t: {"occurrences": 0, "whole_form_counts": {}, "examples": []} for t in wanted
    }
    for observed, whole, start, end in iter_lexical_spans(text=text):
        terms = (
            expand_identifier_terms(observed_text=observed)
            if analyzer == "identifier"
            else (whole,)
        )
        for term in profiles.keys() & set(terms):
            profile = profiles[term]
            profile["occurrences"] += 1
            profile["whole_form_counts"][observed] = (
                profile["whole_form_counts"].get(observed, 0) + 1
            )
            if len(profile["examples"]) < limit:
                profile["examples"].append(
                    {
                        "observed": observed,
                        "whole": whole,
                        "term": term,
                        "derived_subtoken": term != whole,
                        "start": start,
                        "end": end,
                        "line": text.count("\n", 0, start) + 1,
                    }
                )
    return profiles


def subject_json(subject: DiagnosticSubject) -> dict[str, Any]:
    """Serialize stable native identities and explicit configuration only."""
    return {
        "repository_id": str(subject.frame.repository),
        "snapshot_id": str(subject.frame.snapshot),
        "corpus_id": str(subject.frame.corpus),
        "lane": subject.lane,
        "query_text": subject.query,
        "resource": {
            "address": subject.resource.address.value,
            "content_identity": subject.resource.content_identity.value,
        },
        "configuration_identity": subject.configuration.identity,
        "configuration": asdict(subject.configuration),
    }


class Mechanics:
    """Validate one immutable capture once and expose descriptive diagnostics."""

    def __init__(
        self,
        capture: LaneCapture,
        judgments: tuple[Judgment, ...] = (),
        policy: DiagnosticPolicy = DEFAULT_POLICY,
    ) -> None:
        """Check frame, postings, captured scores and bounded-result semantics."""
        self.capture = capture
        self.policy = policy
        self._term_cache: dict[str, list[dict[str, Any]]] = {}
        self._query_sources = _span_profiles(
            capture.query, capture.query_terms, capture.configuration.analyzer
        )
        self.resources = {r.address.value: r for r in capture.resources}
        self.positions = {r.address.value: i for i, r in enumerate(capture.resources)}
        self.fields = {f.name: f for f in capture.fields}
        self.postings = {
            f.name: {t: dict(p) for t, p in f.postings} for f in capture.fields
        }
        self.rows = {r.resource.address.value: r for r in capture.rows}
        self.judgments = {j.resource.address.value: j for j in judgments}
        if (
            not capture.lane
            or len(self.resources) != len(capture.resources)
            or len(self.fields) != len(capture.fields)
            or not self.fields
        ):
            raise ValueError("Duplicate or unnamed diagnostic frame entries.")
        if set(self.fields) - {"content", "filename"}:
            raise ValueError("Only independent content/filename BM25 is supported.")
        expected_terms = tuple(
            dict.fromkeys(
                t
                for s in iter_lexical_spans(text=capture.query)
                for t in (
                    expand_identifier_terms(observed_text=s[0])
                    if capture.configuration.analyzer == "identifier"
                    else (s[1],)
                )
            )
        )
        if expected_terms != capture.query_terms:
            raise ValueError("Query representation differs from capture.")
        for f in capture.fields:
            expected_texts = tuple(
                r.content
                if f.name == "content"
                else PurePosixPath(r.address.value).stem
                for r in capture.resources
            )
            if f.texts != expected_texts:
                raise ValueError("Field source differs from frozen occurrence.")
            expected_weight = (
                1.0 if f.name == "content" else capture.configuration.filename_weight
            )
            if (
                f.weight != expected_weight
                or len(f.texts) != len(capture.resources)
                or len(f.lengths) != len(capture.resources)
                or any(n < 0 for n in f.lengths)
                or not math.isclose(
                    f.average_length,
                    sum(f.lengths) / len(f.lengths) if f.lengths else 0.0,
                    abs_tol=TOLERANCE,
                )
            ):
                raise ValueError("Field shape, average or weight differs.")
            source_counts = [
                Counter(
                    iter_terms(
                        text, identifier=capture.configuration.analyzer == "identifier"
                    )
                )
                for text in f.texts
            ]
            if tuple(c.total() for c in source_counts) != f.lengths:
                raise ValueError("Source/index length mismatch.")
            if len(self.postings[f.name]) != len(f.postings):
                raise ValueError("Duplicate term postings.")
            for term, postings in f.postings:
                if len(dict(postings)) != len(postings) or any(
                    p < 0 or p >= len(capture.resources) or tf <= 0 or tf > f.lengths[p]
                    for p, tf in postings
                ):
                    raise ValueError("Invalid field posting.")
                # Query/source lineage must reproduce indexed occurrence counts.
                if term in capture.query_terms and dict(postings) != {
                    p: c[term] for p, c in enumerate(source_counts) if c[term]
                }:
                    raise ValueError("Source/index term frequency mismatch.")
            if any(
                term not in self.postings[f.name]
                and any(c[term] for c in source_counts)
                for term in capture.query_terms
            ):
                raise ValueError("Query postings missing from index.")
        coverage = compare_identity_coverage(
            expected=range(1, len(capture.rows) + 1),
            observed=(r.rank for r in capture.rows),
        )
        if not coverage.is_exact or len(self.rows) != len(capture.rows):
            raise ValueError("Duplicate or missing captured ranks/resources.")
        previous = (-math.inf, -1)
        for ordinal, row in enumerate(capture.rows, 1):
            if (
                self.resources.get(row.resource.address.value) != row.resource
                or row.score <= 0
                or not math.isfinite(row.score)
            ):
                raise ValueError("Captured resource or positive score differs.")
            ordering = (-row.score, self.positions[row.resource.address.value])
            if ordering < previous or row.rank != ordinal:
                raise ValueError("Captured order differs.")
            previous = ordering
            projected = self.terms(row.resource)
            supplied = {(t.field, t.term): t for t in row.terms}
            if len(supplied) != len(row.terms) or set(supplied) != {
                (t["field"], t["term"]) for t in projected
            }:
                raise ValueError("Captured contribution coverage differs.")
            for t in projected:
                original = supplied[t["field"], t["term"]]
                for key in (
                    "tf",
                    "df",
                    "length",
                    "average_length",
                    "idf",
                    "contribution",
                ):
                    if not math.isclose(
                        getattr(original, key), t[key], abs_tol=TOLERANCE
                    ):
                        raise ValueError("Captured score component mismatch.")
            if not math.isclose(
                sum(t["weighted_contribution"] for t in projected),
                row.score,
                abs_tol=TOLERANCE,
            ):
                raise ValueError("Captured combined score mismatch.")
        positive = {
            capture.resources[p].address.value
            for f in capture.fields
            if f.weight > 0
            for term in capture.query_terms
            for p in self.postings[f.name].get(term, {})
        }
        if capture.complete_positive_universe and positive != self.rows.keys():
            raise ValueError("Complete positive universe differs.")
        if len(self.judgments) != len(judgments):
            raise ValueError("Duplicate judgments.")
        for j in judgments:
            if (
                j.frame != capture.frame
                or self.resources.get(j.resource.address.value) != j.resource
                or capture.obligation != j.obligation
            ):
                raise ValueError("Judgment frame or obligation differs.")
        exclusions = {e.resource.address.value for e in capture.exclusions}
        if (
            len(exclusions) != len(capture.exclusions)
            or exclusions & self.resources.keys()
        ):
            raise ValueError("Exclusion conflicts with indexed frame.")

    def terms(self, resource: RepositoryResourceOccurrence) -> list[dict[str, Any]]:
        """Replay TF saturation and independent weighted term contributions."""
        if self.resources.get(resource.address.value) != resource:
            return []
        if resource.address.value in self._term_cache:
            return deepcopy(self._term_cache[resource.address.value])
        p = self.positions[resource.address.value]
        cfg = self.capture.configuration
        settings = RepositoryTextLexicalBm25Settings(k1=cfg.k1, b=cfg.b)
        result = []
        for field in self.capture.fields:
            source_profiles = _span_profiles(
                field.texts[p], self.capture.query_terms, cfg.analyzer
            )
            for term in self.capture.query_terms:
                posting = self.postings[field.name].get(term, {})
                tf = posting.get(p, 0)
                if not tf:
                    continue
                df = len(posting)
                idf = calculate_bm25_inverse_document_frequency(
                    document_count=len(self.capture.resources), document_frequency=df
                )
                length_factor = (
                    1 - cfg.b + cfg.b * field.lengths[p] / field.average_length
                )
                numerator = tf * (cfg.k1 + 1)
                denominator = tf + cfg.k1 * length_factor
                contribution = calculate_bm25_term_contribution(
                    term_frequency=tf,
                    inverse_document_frequency=idf,
                    document_length=field.lengths[p],
                    average_document_length=field.average_length,
                    settings=settings,
                )
                result.append(
                    {
                        "field": field.name,
                        "term": term,
                        "tf": tf,
                        "df": df,
                        "corpus_size": len(self.capture.resources),
                        "idf": idf,
                        "length": field.lengths[p],
                        "average_length": field.average_length,
                        "length_ratio": field.lengths[p] / field.average_length,
                        "normalized_length_factor": length_factor,
                        "tf_numerator": numerator,
                        "tf_denominator": denominator,
                        "tf_saturation": numerator / denominator,
                        "contribution": contribution,
                        "field_weight": field.weight,
                        "weighted_contribution": contribution * field.weight,
                        "source": source_profiles[term],
                        "query_source": self._query_sources[term],
                    }
                )
        self._term_cache[resource.address.value] = result
        return deepcopy(result)

    def reconfigured(self, configuration: Configuration) -> Mechanics:
        """Replay only scoring parameters over this already validated representation.

        Reuse immutable source/posting evidence instead of retokenizing a frozen
        corpus for each parameter point. This evaluation replay is not production
        ranking policy. Actual native scorer parity is tested independently.
        """
        old = self.capture.configuration
        if (
            configuration.analyzer != old.analyzer
            or configuration.index_identity != old.index_identity
        ):
            raise ValueError("Parameter replay cannot change representation/index.")
        settings = RepositoryTextLexicalBm25Settings(
            k1=configuration.k1, b=configuration.b
        )
        clone = object.__new__(Mechanics)
        clone.__dict__ = self.__dict__.copy()
        clone._term_cache = {}
        fields = tuple(
            replace(
                f,
                weight=configuration.filename_weight
                if f.name == "filename"
                else f.weight,
            )
            for f in self.capture.fields
        )
        scores = []
        for resource in self.capture.resources:
            address = resource.address.value
            if address not in self._term_cache:
                self.terms(resource)
            terms = []
            for original in self._term_cache[address]:
                t = original.copy()
                factor = (
                    1
                    - configuration.b
                    + configuration.b * t["length"] / t["average_length"]
                )
                numerator = t["tf"] * (configuration.k1 + 1)
                denominator = t["tf"] + configuration.k1 * factor
                contribution = calculate_bm25_term_contribution(
                    term_frequency=t["tf"],
                    inverse_document_frequency=t["idf"],
                    document_length=t["length"],
                    average_document_length=t["average_length"],
                    settings=settings,
                )
                weight = (
                    configuration.filename_weight
                    if t["field"] == "filename"
                    else t["field_weight"]
                )
                t.update(
                    normalized_length_factor=factor,
                    tf_numerator=numerator,
                    tf_denominator=denominator,
                    tf_saturation=numerator / denominator,
                    contribution=contribution,
                    field_weight=weight,
                    weighted_contribution=weight * contribution,
                )
                terms.append(t)
            clone._term_cache[address] = terms
            content = sum(t["contribution"] for t in terms if t["field"] == "content")
            filename = sum(t["contribution"] for t in terms if t["field"] == "filename")
            score = content + configuration.filename_weight * filename
            if not math.isclose(
                sum(t["weighted_contribution"] for t in terms), score, abs_tol=TOLERANCE
            ):
                raise ValueError("Reconfigured score decomposition differs.")
            if score > 0:
                scores.append(
                    (
                        resource,
                        score,
                        tuple(
                            TermCapture(
                                t["field"],
                                t["term"],
                                t["tf"],
                                t["df"],
                                t["length"],
                                t["average_length"],
                                t["idf"],
                                t["contribution"],
                            )
                            for t in terms
                        ),
                    )
                )
        scores.sort(key=lambda r: -r[1])
        rows = tuple(
            RankedCapture(resource, rank, score, terms)
            for rank, (resource, score, terms) in enumerate(scores, 1)
        )
        clone.capture = replace(
            self.capture,
            configuration=configuration,
            fields=fields,
            rows=rows,
            complete_positive_universe=True,
        )
        clone.fields = {f.name: f for f in fields}
        clone.rows = {r.resource.address.value: r for r in rows}
        return clone

    def query_profile(self) -> list[dict[str, Any]]:
        """Describe term footprint and optional independent judged yields."""
        output = []
        for term in self.capture.query_terms:
            field_rows = []
            union: set[str] = set()
            for f in self.capture.fields:
                positions = self.postings[f.name].get(term, {})
                addresses = {self.capture.resources[p].address.value for p in positions}
                if f.weight > 0:
                    union.update(addresses)
                df = len(positions)
                idf = (
                    calculate_bm25_inverse_document_frequency(
                        document_count=len(self.capture.resources),
                        document_frequency=df,
                    )
                    if self.capture.resources
                    else None
                )
                fraction = (
                    df / len(self.capture.resources) if self.capture.resources else 0.0
                )
                field_rows.append(
                    {
                        "field": f.name,
                        "weight": f.weight,
                        "df": df,
                        "idf": idf,
                        "fraction_of_frame": fraction,
                        "resources_matched": sorted(addresses),
                        "common_term": fraction >= self.policy.common_fraction
                        and idf is not None
                        and idf <= self.policy.low_idf,
                    }
                )
            labels = Counter(
                self.judgments[p].label for p in union if p in self.judgments
            )
            judged = sum(labels.values())
            output.append(
                {
                    "term": term,
                    "source_query": spans(
                        self.capture.query, term, self.capture.configuration.analyzer
                    ),
                    "fields": field_rows,
                    "positive_resources_with_term": len(union & self.rows.keys()),
                    "effective_matching_resources": sorted(union),
                    "judged_labels": dict(sorted(labels.items())),
                    "unjudged_matched": len(union - self.judgments.keys()),
                    "required_yield": labels["REQUIRED"] / judged if judged else None,
                    "useful_yield": (labels["REQUIRED"] + labels["HELPFUL_ONLY"])
                    / judged
                    if judged
                    else None,
                }
            )
        return output

    def explain(
        self,
        resource: RepositoryResourceOccurrence,
        supports: tuple[SupportReference, ...] = (),
    ) -> dict[str, Any]:
        """Explain a reached, bounded omission, zero score or excluded subject."""
        for s in supports:
            if (
                s.frame != self.capture.frame
                or s.resource != resource
                or not s.identity
                or not s.provenance
            ):
                raise ValueError("Support reference frame/provenance differs.")
        subject = DiagnosticSubject(
            self.capture.frame,
            self.capture.lane,
            resource,
            self.capture.configuration,
            self.capture.query,
        )
        terms = self.terms(resource)
        row = (
            self.rows.get(resource.address.value)
            if self.resources.get(resource.address.value) == resource
            else None
        )
        score = sum(t["weighted_contribution"] for t in terms)
        outside = self.resources.get(resource.address.value) != resource
        reason = (
            next(
                (e.reason for e in self.capture.exclusions if e.resource == resource),
                "RESOURCE_NOT_IN_FRAME",
            )
            if outside
            else "REACHED"
            if row
            else "RESULT_BOUND_OMISSION"
            if score > 0
            else "ALL_CONTRIBUTIONS_NONPOSITIVE"
            if terms
            else "NO_QUERY_TERM_OVERLAP"
        )
        ahead = self.capture.rows[: row.rank - 1] if row else ()
        labels = Counter(
            self.judgments[r.resource.address.value].label
            for r in ahead
            if r.resource.address.value in self.judgments
        )
        selected = ahead[: self.policy.overtaker_limit]
        judgment = self.judgments.get(resource.address.value) if not outside else None
        record = {
            "subject": subject_json(subject),
            "policy": asdict(self.policy),
            "status": reason,
            "rank": row.rank if row else None,
            "score": score if not outside else None,
            "captured_score": row.score if row else None,
            "score_reconstructed": math.isclose(score, row.score, abs_tol=TOLERANCE)
            if row
            else None,
            "query_terms": self.capture.query_terms,
            "terms": terms,
            "judgment": {
                "obligation": judgment.obligation.value,
                "task": judgment.obligation.task.value,
                "label": judgment.label,
                "units": judgment.units,
            }
            if judgment
            else None,
            "ranking": {
                "ahead": len(ahead),
                "ahead_labels": dict(sorted(labels.items())),
                "unjudged_ahead": len(ahead) - sum(labels.values()),
                "predecessor_gap": ahead[-1].score - row.score
                if ahead and row
                else None,
                "top_gap": ahead[0].score - row.score if ahead and row else None,
                "ahead_resources": [r.resource.address.value for r in ahead],
                "top_overtakers": [
                    {
                        "resource": r.resource.address.value,
                        "rank": r.rank,
                        "margin": r.score - score,
                        "label": self.judgments[r.resource.address.value].label
                        if r.resource.address.value in self.judgments
                        else None,
                        "comparison": self.overtaker(resource, r.resource),
                    }
                    for r in selected
                ],
            },
            "support_references": [
                {"kind": s.kind, "identity": s.identity, "provenance": s.provenance}
                for s in supports
            ],
        }
        record["failure_attribution"] = classify(record, self.policy)
        return record

    def overtaker(
        self, target: RepositoryResourceOccurrence, other: RepositoryResourceOccurrence
    ) -> dict[str, Any]:
        """Compare exact field/term mechanics within this one representation."""
        if (
            self.resources.get(target.address.value) != target
            or self.resources.get(other.address.value) != other
        ):
            raise ValueError("Overtaker subject outside frame.")
        return term_deltas(self.terms(target), self.terms(other))


def term_deltas(a: list[dict[str, Any]], b: list[dict[str, Any]]) -> dict[str, Any]:
    """Explain paired resource or treatment effects, including configuration changes."""
    left = {(t["field"], t["term"]): t for t in a}
    right = {(t["field"], t["term"]): t for t in b}
    terms = []
    fields: Counter[str] = Counter()
    for key in sorted(left.keys() | right.keys()):
        x, y = left.get(key), right.get(key)
        delta = (y["weighted_contribution"] if y else 0) - (
            x["weighted_contribution"] if x else 0
        )
        fields[key[0]] += delta
        terms.append(
            {
                "field": key[0],
                "term": key[1],
                "A": x,
                "B": y,
                "weighted_delta": delta,
                "favors": "B" if delta > 0 else "A" if delta < 0 else "NEITHER",
                "tf_delta": (y["tf"] if y else 0) - (x["tf"] if x else 0),
                "idf_delta": y["idf"] - x["idf"] if x and y else None,
                "df_delta": y["df"] - x["df"] if x and y else None,
                "length_factor_delta": y["normalized_length_factor"]
                - x["normalized_length_factor"]
                if x and y
                else None,
            }
        )
    return {
        "term_deltas": terms,
        "field_weighted_deltas": dict(sorted(fields.items())),
        "score_delta": sum(fields.values()),
        "causal_limit": "Exact observable differences; interacting rank-causal allocations require separately frozen ablations.",
    }
