# Copyright (c) 2026
# ruff: noqa: COM812, EM101, TRY003, ANN401 -- bounded capture metadata adapter
"""Stream explicit scalar state once, referencing shared statistics by position."""

from __future__ import annotations

import hashlib
from types import FunctionType
from typing import Any

from experiments.bm25f import scoring
from experiments.bm25f.fields import FieldState, validate_frame

SCHEMA = "case-0015-field-state-fingerprint-v2"


class Records:
    """Unambiguous length-prefixed scalar records, never a rich-object serializer."""

    def __init__(self) -> None:
        """Start a domain-separated incremental digest."""
        self.digest = hashlib.sha256()
        self.record("schema", SCHEMA)

    def record(self, tag: str, *values: str | float) -> None:
        """Stream record arity and typed UTF-8 scalars directly to SHA-256."""
        self.digest.update((len(values) + 1).to_bytes(8, "big"))
        for value in (tag, *values):
            if isinstance(value, float):
                encoded = b"f" + value.hex().encode("ascii")
            elif isinstance(value, int):
                encoded = b"i" + str(value).encode("ascii")
            elif isinstance(value, str):
                encoded = b"s" + value.encode("utf-8")
            else:
                raise TypeError("Scalar fingerprint records only")
            self.digest.update(len(encoded).to_bytes(8, "big"))
            self.digest.update(encoded)


def observation(records: Records, tag: str, item: Any) -> None:
    """Retain all canonical observation coordinates and lexical values."""
    records.record(
        tag,
        item.encounter_ordinal,
        item.observed_text,
        item.normalized_term,
        item.start,
        item.end,
    )


def prepared_fingerprint(frame: Any, fields: Any) -> str:
    """Read-only recovery check of returned observations without building an index."""
    records = Records()
    records.record(
        "prepared-frame",
        str(frame.snapshot.repository_id),
        str(frame.snapshot.id),
        str(frame.documents.corpus.id),
    )
    for position, (document, analysis) in enumerate(
        zip(frame.documents.documents, fields.content.analyses, strict=True)
    ):
        records.record(
            "document",
            position,
            str(document.repository_id),
            str(document.resource.address),
            str(document.id),
            str(document.resource.content_identity),
        )
        for item in analysis.observations:
            observation(records, "content-observation", item)
    # Filename is already a complete returned native index; do not rebuild it.
    field(
        records,
        "FILENAME",
        fields.filename,
        fields.filename.document_statistics,
        fields.filename.average_document_length,
    )
    return records.digest.hexdigest()


def field(  # noqa: C901 -- explicit compact projection
    records: Records, name: str, index: Any, statistics: Any, average: float
) -> None:
    """Hash each document once; postings carry only canonical document references."""
    records.record("field", name, len(statistics), average)
    positions = {id(item): position for position, item in enumerate(statistics)}
    for position, item in enumerate(statistics):
        document = item.analysis.document
        records.record(
            "field-document", position, str(document.id), item.document_length
        )
        if name == "FILENAME":
            records.record("filename-stem", item.analysis.filename_stem)
        for obs in item.analysis.observations:
            observation(records, "observation", obs)
        records.record("tf-count", len(item.term_frequencies))
        for tf in item.term_frequencies:
            records.record("tf", tf.normalized_term, tf.frequency)
            for obs in tf.observations:
                observation(records, "tf-observation", obs)
    frequencies = (
        index.corpus_statistics.document_frequencies
        if name == "CONTENT"
        else index.document_frequencies
    )
    records.record("df-count", len(frequencies))
    for freq in frequencies:
        records.record("df", freq.normalized_term, freq.document_frequency)
    records.record("posting-term-count", len(index.term_postings))
    for term in index.term_postings:
        records.record("posting-term", term.normalized_term, len(term.postings))
        for posting in term.postings:
            posting_position = positions.get(id(posting.document_statistics))
            if posting_position is None:
                raise ValueError("Foreign posting statistics reference")
            records.record(
                "posting",
                posting_position,
                posting.normalized_term,
                posting.term_frequency.normalized_term,
                posting.term_frequency.frequency,
            )
            for obs in posting.term_frequency.observations:
                observation(records, "posting-observation", obs)


def fingerprint(state: FieldState) -> str:
    """Bounded metadata seal over identities, order, exact observations and counts."""
    records = Records()
    records.record(
        "frame",
        str(state.snapshot.repository_id),
        str(state.snapshot.id),
        str(state.collection.corpus.id),
        len(state.collection.documents),
    )
    for position, document in enumerate(state.collection.documents):
        records.record(
            "document",
            position,
            str(document.repository_id),
            str(document.resource.address),
            str(document.id),
            str(document.resource.content_identity),
        )
        # Text is streamed as one resource at a time, never the complete corpus.
        records.record("text", document.text)
    content = state.content.corpus_statistics
    records.record("content-document-count", content.document_count)
    # The collection analysis also has independently retained canonical order.
    for analysis in content.collection_analysis.analyses:
        records.record("analysis-document", str(analysis.document.id))
        for obs in analysis.observations:
            observation(records, "analysis-observation", obs)
    field(
        records,
        "CONTENT",
        state.content,
        content.document_statistics,
        content.average_document_length,
    )
    field(
        records,
        "FILENAME",
        state.filename,
        state.filename.document_statistics,
        state.filename.average_document_length,
    )
    records.record(
        "filename-collection", str(state.filename.document_collection.corpus.id)
    )
    for document in state.filename.document_collection.documents:
        records.record("filename-collection-document", str(document.id))
    return SCHEMA + ":" + records.digest.hexdigest()


def validate_state(state: FieldState) -> None:
    """Replace only capture metadata validation; scientific primitives stay sealed."""
    validate_frame(state.collection, state.snapshot)
    if state.observation_sha256 != fingerprint(state):
        raise ValueError("Field observation/statistics tamper")


# Bind the BYTE-IDENTICAL frozen scorer code to the bounded capture validator.
# No global monkeypatch, altered arithmetic, new ranking logic or extra invocation.
_score = FunctionType(
    scoring.score.__code__,
    {**scoring.score.__globals__, "validate_state": validate_state},
    scoring.score.__name__,
    scoring.score.__defaults__,
    scoring.score.__closure__,
)
_score.__kwdefaults__ = scoring.score.__kwdefaults__


def score(state: FieldState, query: Any, **kwargs: Any) -> dict[str, Any]:
    """Invoke unchanged frozen scoring bytecode with capture-owned seal validation."""
    return _score(state, query, **kwargs)  # type: ignore[no-any-return]
