# Copyright (c) 2026
# ruff: noqa: ANN401, E501, PLC0415, PLR2004, S105, T201, TC001, TRY004
"""Development-only realization of the frozen Increment-26 protocol.

This module is deliberately experiment-local.  It composes the frozen
CodeRankEmbed configuration with Increment-25's historical-snapshot and
canonical lexical machinery; it neither creates Repository Intelligence nor
selects Context.
"""

from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, cast

from huggingface_hub import HfApi, snapshot_download

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
    retrieve_repository_text_documents_by_bm25,
)
from experiments.increment_25.development import (
    DevelopmentBoundaryError,
    FrozenDevelopment,
    SnapshotCorpus,
    _build_snapshot_corpus,
    _materialize_git_snapshot,
    load_frozen_development,
)
from experiments.increment_25.task_population import TaskCard
from experiments.increment_26.configuration import (
    CAPACITY,
    CHUNK_CONTENT_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    INCREMENT_25_FREEZE_IDENTITY,
    MAX_INPUT_TOKENS,
    MODEL_REPOSITORY,
    MODEL_REVISION,
    MODEL_WEIGHT_FILENAME,
    MODEL_WEIGHT_SHA256,
    QUERY_PREFIX,
    SPECIAL_TOKEN_ALLOWANCE,
    build_freeze,
)

if TYPE_CHECKING:
    from collections.abc import Iterable, Iterator, Mapping, Sequence

SCHEMA = "devtools-increment-26-development-candidates-v1"
JUDGMENT_SCHEMA = "devtools-increment-26-development-judgment-input-v1"
EXECUTION_SEMANTICS = "increment-26-development-generator-v1"
ENCODE_BATCH_SIZE = 16


class ModelIntegrityError(RuntimeError):
    """Reject a model artifact other than the exact frozen model."""


@dataclass(frozen=True, slots=True)
class TokenChunk:
    """One tokenizer-relative raw-source window, before special tokens."""

    ordinal: int
    start_token: int
    end_token: int
    token_ids: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class SemanticResourceScore:
    """One resource projection from its scored raw-source chunks."""

    address: RepositoryResourceAddress
    score: float
    chunk_count: int
    winning_chunk: TokenChunk
    maximum_chunk_ordinals: tuple[int, ...]


def load_frozen_increment_26(path: Path, *, increment_25_freeze_path: Path) -> dict[str, object]:
    """Load the immutable configuration and reject unexpected outcome state."""
    envelope = cast("dict[str, object]", json.loads(path.read_text(encoding="utf-8")))
    payload = envelope.get("payload")
    if not isinstance(payload, dict):
        msg = "Increment-26 freeze has no mapping payload."
        raise ValueError(msg)
    if envelope.get("content_identity") != _digest(payload):
        msg = "Increment-26 freeze content identity does not match its payload."
        raise ValueError(msg)
    expected = build_freeze(increment_25_freeze_path=increment_25_freeze_path)
    if envelope != expected:
        msg = "Increment-26 freeze differs from the committed amended protocol."
        raise ValueError(msg)
    population = cast("dict[str, object]", payload.get("population"))
    if population.get("increment_25_freeze_identity") != INCREMENT_25_FREEZE_IDENTITY:
        msg = "Increment-26 freeze does not bind the committed Increment-25 population."
        raise ValueError(msg)
    protocol = cast("dict[str, object]", payload.get("protocol"))
    if protocol.get("outcomes_generated") is not False:
        msg = "Pre-outcome Increment-26 freeze unexpectedly claims generated outcomes."
        raise ValueError(msg)
    return envelope


def realize_pinned_encoder(
    *,
    cache_dir: Path | None = None,
    offline: bool = False,
) -> tuple[Any, Any, dict[str, object]]:
    """Download, verify, and load only the frozen CPU CodeRankEmbed artifact."""
    if not offline:
        info = HfApi().model_info(MODEL_REPOSITORY, revision=MODEL_REVISION)
        if info.sha != MODEL_REVISION:
            msg = "Remote model revision did not resolve to the frozen immutable revision."
            raise ModelIntegrityError(msg)
    local = Path(
        snapshot_download(
            repo_id=MODEL_REPOSITORY,
            revision=MODEL_REVISION,
            cache_dir=cache_dir,
            local_files_only=offline,
        ),
    )
    weight = local / MODEL_WEIGHT_FILENAME
    if not weight.is_file() or _sha256(weight) != MODEL_WEIGHT_SHA256:
        msg = "Pinned model.safetensors is absent or does not match the frozen SHA-256."
        raise ModelIntegrityError(msg)
    # Imports remain here so configuration-only tests never initialize a model.
    from transformers import AutoModel, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        local,
        revision=MODEL_REVISION,
        local_files_only=True,
        trust_remote_code=True,
    )
    model = AutoModel.from_pretrained(
        local,
        revision=MODEL_REVISION,
        local_files_only=True,
        trust_remote_code=True,
        use_safetensors=True,
    )
    model.to("cpu")
    model.eval()
    # The pinned remote model calls a PreTrainedModel helper removed in the
    # frozen Transformers runtime. Restore that helper's additive mask on this
    # model instance only; weights and model forward semantics stay unchanged.
    model.get_extended_attention_mask = _extended_attention_mask
    if tokenizer.cls_token != "[CLS]" or tokenizer.sep_token != "[SEP]":
        msg = "Pinned tokenizer special-token semantics do not match the freeze."
        raise ModelIntegrityError(msg)
    if tokenizer.num_special_tokens_to_add(pair=False) != SPECIAL_TOKEN_ALLOWANCE:
        msg = "Pinned tokenizer special-token allowance does not match the freeze."
        raise ModelIntegrityError(msg)
    if tokenizer.encode("hello", add_special_tokens=True) != [
        tokenizer.cls_token_id,
        *tokenizer.encode("hello", add_special_tokens=False),
        tokenizer.sep_token_id,
    ]:
        msg = "Pinned tokenizer does not wrap content with the frozen CLS/SEP tokens."
        raise ModelIntegrityError(msg)
    return model, tokenizer, {
        "repository": MODEL_REPOSITORY,
        "revision": MODEL_REVISION,
        "weight_filename": MODEL_WEIGHT_FILENAME,
        "weight_sha256": MODEL_WEIGHT_SHA256,
        "device": "cpu",
    }


def serialize_query(*, lexical_query: str) -> str:
    """Apply only the frozen model-native query prefix to frozen query text."""
    return QUERY_PREFIX + lexical_query


def _extended_attention_mask(attention_mask: Any, input_shape: Any) -> Any:
    """Supply the pinned model's expected additive self-attention mask."""
    import torch

    if attention_mask is None:
        attention_mask = torch.ones(input_shape, dtype=torch.long)
    if tuple(attention_mask.shape) != tuple(input_shape):
        msg = "Pinned model received an unexpected attention-mask shape."
        raise ValueError(msg)
    expanded = attention_mask[:, None, None, :].to(dtype=torch.float32)
    return (1.0 - expanded) * torch.finfo(torch.float32).min


def tokenize_source_chunks(*, content: str, tokenizer: Any) -> tuple[TokenChunk, ...]:
    """Cover all raw-source tokens with the frozen overlapping windows."""
    token_ids = tuple(cast("list[int]", tokenizer.encode(content, add_special_tokens=False)))
    if not token_ids:
        return ()
    stride = CHUNK_CONTENT_TOKENS - CHUNK_OVERLAP_TOKENS
    chunks: list[TokenChunk] = []
    for ordinal, start in enumerate(range(0, len(token_ids), stride)):
        end = min(start + CHUNK_CONTENT_TOKENS, len(token_ids))
        chunks.append(TokenChunk(ordinal, start, end, token_ids[start:end]))
        if end == len(token_ids):
            break
    return tuple(chunks)


def _encode_token_sequences(*, model: Any, tokenizer: Any, sequences: Sequence[tuple[int, ...]]) -> Any:
    """CLS-pool normalized float32 vectors without truncation or metadata."""
    import torch
    from torch.nn import functional

    prepared = [
        {
            "input_ids": [tokenizer.cls_token_id, *sequence, tokenizer.sep_token_id],
            "attention_mask": [1] * (len(sequence) + SPECIAL_TOKEN_ALLOWANCE),
        }
        for sequence in sequences
    ]
    if any(len(item["input_ids"]) > MAX_INPUT_TOKENS for item in prepared):
        msg = "Frozen maximum input length would be exceeded; refusing silent truncation."
        raise ValueError(msg)
    batch = tokenizer.pad(prepared, padding=True, return_tensors="pt")
    with torch.inference_mode():
        outputs = model(**batch, return_dict=True)
        vectors = outputs.last_hidden_state[:, 0, :].to(dtype=torch.float32)
        return functional.normalize(vectors, p=2, dim=1).to(dtype=torch.float32)


def encode_query(*, lexical_query: str, model: Any, tokenizer: Any) -> Any:
    """Encode the frozen lexical query with its frozen model-native prefix."""
    tokens = tuple(
        cast("list[int]", tokenizer.encode(serialize_query(lexical_query=lexical_query), add_special_tokens=False)),
    )
    if len(tokens) > CHUNK_CONTENT_TOKENS:
        msg = "Frozen query exceeds 2046 content tokens; refusing silent truncation."
        raise ValueError(msg)
    return _encode_token_sequences(model=model, tokenizer=tokenizer, sequences=(tokens,))[0]


def score_snapshot_resources(*, corpus: SnapshotCorpus, model: Any, tokenizer: Any, query_vector: Any, embedding_cache: dict[tuple[int, ...], Any] | None = None) -> tuple[SemanticResourceScore, ...]:
    """Score every nonempty raw-source resource and deterministically project it."""
    import torch

    all_chunks: list[tuple[RepositoryResourceAddress, TokenChunk]] = []
    for resource in corpus.snapshot.resources:
        all_chunks.extend(
            (resource.address, chunk)
            for chunk in tokenize_source_chunks(content=resource.content, tokenizer=tokenizer)
        )
    # Stable length grouping reduces padded CPU work without changing any
    # chunk content, representation, or resource aggregation semantics.
    all_chunks.sort(key=lambda item: len(item[1].token_ids))
    vectors_by_tokens = {} if embedding_cache is None else embedding_cache
    missing = tuple(dict.fromkeys(
        chunk.token_ids for _, chunk in all_chunks if chunk.token_ids not in vectors_by_tokens
    ))
    for batch in _batches(missing, ENCODE_BATCH_SIZE):
        vectors = _encode_token_sequences(
            model=model, tokenizer=tokenizer, sequences=batch,
        )
        vectors_by_tokens.update(zip(batch, vectors, strict=True))
    scores_by_address: dict[RepositoryResourceAddress, list[tuple[TokenChunk, float]]] = {}
    for address, chunk in all_chunks:
        scores_by_address.setdefault(address, []).append(
            (chunk, float(torch.dot(query_vector, vectors_by_tokens[chunk.token_ids]).item())),
        )
    scored: list[SemanticResourceScore] = []
    for resource in corpus.snapshot.resources:
        chunk_scores = scores_by_address.get(resource.address)
        if not chunk_scores:
            continue
        maximum = max(score for _, score in chunk_scores)
        winners = tuple(sorted(
            chunk.ordinal for chunk, score in chunk_scores if score == maximum
        ))
        winner = next(chunk for chunk, _ in chunk_scores if chunk.ordinal == winners[0])
        scored.append(
            SemanticResourceScore(
                address=resource.address,
                score=maximum,
                chunk_count=len(chunk_scores),
                winning_chunk=winner,
                maximum_chunk_ordinals=winners,
            ),
        )
    return tuple(sorted(scored, key=lambda item: (-item.score, item.address.value)))


def generate_case(*, card: TaskCard, corpus: SnapshotCorpus, model: Any, tokenizer: Any, embedding_cache: dict[tuple[int, ...], Any] | None = None) -> dict[str, object]:
    """Generate independent semantic and canonical lexical development surfaces."""
    query_vector = encode_query(lexical_query=card.lexical_query, model=model, tokenizer=tokenizer)
    semantic = score_snapshot_resources(corpus=corpus, model=model, tokenizer=tokenizer, query_vector=query_vector, embedding_cache=embedding_cache)
    lexical_query = analyze_repository_text_lexical_query(text=card.lexical_query)
    lexical_matches = retrieve_repository_text_documents_by_bm25(
        query=lexical_query, index=corpus.index, maximum_results=max(1, len(corpus.addresses)),
    ).matches
    lexical = tuple(
        (match.document_statistics.analysis.document.resource.address, match.score)
        for match in lexical_matches
        if match.score > 0
    )
    n = min(CAPACITY, len(semantic), len(lexical))
    semantic_surface = semantic[:n]
    lexical_surface = lexical[:n]
    lexical_ranks = {address: rank for rank, (address, _) in enumerate(lexical, start=1)}
    semantic_addresses = tuple(item.address for item in semantic_surface)
    lexical_addresses = tuple(address for address, _ in lexical_surface)
    overlap = tuple(address for address in semantic_addresses if address in set(lexical_addresses))
    return {
        "case_id": card.case_id,
        "parent_snapshot_sha": card.parent_snapshot_sha,
        "information_need": {"purpose": card.information_need_purpose, "lexical_query": card.lexical_query},
        "corpus": {"snapshot_id": str(corpus.snapshot.id), "corpus_id": corpus.corpus_id, "resource_count": len(corpus.addresses)},
        "capacity": {"n": n, "semantic_available": len(semantic), "positive_lexical_available": len(lexical), "semantic_exhausted": len(semantic) < CAPACITY, "lexical_exhausted": len(lexical) < CAPACITY},
        "semantic_candidates": [_semantic_item(item, lexical_ranks=lexical_ranks) for item in semantic_surface],
        "lexical_candidates": [{"rank": rank, "address": str(address), "score": score} for rank, (address, score) in enumerate(lexical_surface, start=1)],
        "overlap": {"intersection": [str(address) for address in overlap], "semantic_only": [str(address) for address in semantic_addresses if address not in set(lexical_addresses)], "lexical_only": [str(address) for address in lexical_addresses if address not in set(semantic_addresses)]},
        "chunk_diagnostics": {"scored_resource_count": len(semantic), "total_chunk_count": sum(item.chunk_count for item in semantic), "maximum_chunks_for_one_resource": max((item.chunk_count for item in semantic), default=0)},
    }


def run_development(*, repository_root: Path, increment_25_freeze_path: Path, increment_26_freeze_path: Path, cache_dir: Path | None = None, offline: bool = False) -> tuple[dict[str, object], dict[str, object]]:
    """Execute exactly the sealed development partition and no usefulness work."""
    increment_26 = load_frozen_increment_26(
        increment_26_freeze_path, increment_25_freeze_path=increment_25_freeze_path,
    )
    frozen = load_frozen_development(increment_25_freeze_path)
    model, tokenizer, model_identity = realize_pinned_encoder(cache_dir=cache_dir, offline=offline)
    cases: list[dict[str, object]] = []
    judgment_cases: list[dict[str, object]] = []
    embedding_cache: dict[tuple[int, ...], Any] = {}
    for case_id in frozen.development_case_ids:
        case_started = time.perf_counter()
        print(f"Increment 26 development: {case_id} started", file=sys.stderr, flush=True)
        card = frozen.require_case(case_id)
        with _temporary_snapshot(repository_root=repository_root, card=card) as snapshot_root:
            corpus = _build_snapshot_corpus(snapshot_root=snapshot_root, source_roots=card.corpus_source_roots)
            case = generate_case(card=card, corpus=corpus, model=model, tokenizer=tokenizer, embedding_cache=embedding_cache)
            cases.append(case)
            judgment_cases.append(_judgment_case(card=card, case=case, corpus=corpus))
        print(
            f"Increment 26 development: {case_id} completed in {time.perf_counter() - case_started:.1f}s",
            file=sys.stderr,
            flush=True,
        )
    evidence: dict[str, object] = {"schema": SCHEMA, "execution": {"semantics": EXECUTION_SEMANTICS, "mode": "development-only", "freeze_identity": increment_26["content_identity"], "increment_25_freeze_identity": frozen.freeze_identity, "model": model_identity, "batch_size": ENCODE_BATCH_SIZE, "batch_order": "ascending content-token length; stable corpus and chunk order for ties", "embedding_cache": "exact tokenizer token ids within one development pass; cleared before replay", "case_count": len(cases)}, "cases": cases}
    evidence["execution_identity"] = _digest(evidence)
    judgment: dict[str, object] = {"schema": JUDGMENT_SCHEMA, "execution_identity": evidence["execution_identity"], "scope": "neutral development resources awaiting human judgment", "cases": judgment_cases}
    _assert_evidence(evidence=evidence, frozen=frozen)
    _assert_judgment(judgment)
    return evidence, judgment


def write_artifact(*, path: Path, payload: Mapping[str, object]) -> None:
    """Serialize one deterministic experiment-local evidence artifact."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def _semantic_item(item: SemanticResourceScore, *, lexical_ranks: Mapping[RepositoryResourceAddress, int]) -> dict[str, object]:
    return {"address": str(item.address), "score": item.score, "positive_lexical_rank": lexical_ranks.get(item.address), "has_positive_lexical_rank": item.address in lexical_ranks, "chunk_count": item.chunk_count, "winning_chunk": {"ordinal": item.winning_chunk.ordinal, "start_token": item.winning_chunk.start_token, "end_token": item.winning_chunk.end_token}, "maximum_chunk_ordinals": list(item.maximum_chunk_ordinals)}


def _judgment_case(*, card: TaskCard, case: Mapping[str, object], corpus: SnapshotCorpus) -> dict[str, object]:
    semantic = cast("list[dict[str, object]]", case["semantic_candidates"])
    lexical = cast("list[dict[str, object]]", case["lexical_candidates"])
    addresses = sorted({str(item["address"]) for item in semantic} | {str(item["address"]) for item in lexical})
    return {"case_id": card.case_id, "task": {"purpose": card.information_need_purpose, "lexical_query": card.lexical_query, "parent_snapshot_sha": card.parent_snapshot_sha}, "resources": [{"address": address, "content": corpus.snapshot.resource_at(RepositoryResourceAddress(address)).content} for address in addresses]}


def _assert_evidence(*, evidence: Mapping[str, object], frozen: FrozenDevelopment) -> None:
    cases = cast("list[dict[str, object]]", evidence["cases"])
    ids = tuple(str(case["case_id"]) for case in cases)
    if ids != frozen.development_case_ids or len(ids) != 8:
        msg = "Evidence must contain exactly the eight frozen development cases."
        raise DevelopmentBoundaryError(msg)
    if set(ids) & (frozen.confirmation_case_ids | frozen.reserve_case_ids):
        msg = "Sealed or reserve case appeared in Increment-26 development evidence."
        raise DevelopmentBoundaryError(msg)
    prohibited = {"useful", "not_useful", "usefulness", "structural_additions", "structural_only"}
    if _all_keys(evidence) & prohibited:
        msg = "Development evidence contains prohibited labels or structural input."
        raise RuntimeError(msg)


def _assert_judgment(artifact: Mapping[str, object]) -> None:
    prohibited = {"origin", "semantic_candidates", "lexical_candidates", "score", "rank", "overlap", "winning_chunk", "chunk_count", "structural", "changed_paths", "useful", "not_useful", "usefulness"}
    leaked = _all_keys(artifact) & prohibited
    if leaked:
        msg = f"Blinded judgment artifact leaks prohibited fields: {sorted(leaked)}."
        raise RuntimeError(msg)


def _all_keys(value: object) -> set[str]:
    if isinstance(value, dict):
        return set(value) | set().union(*(_all_keys(item) for item in value.values()))
    if isinstance(value, list):
        return set().union(*(_all_keys(item) for item in value)) if value else set()
    return set()


@contextmanager
def _temporary_snapshot(*, repository_root: Path, card: TaskCard) -> Iterator[Path]:
    """Materialize only this allowed development parent snapshot temporarily."""
    with tempfile.TemporaryDirectory(prefix=f"devtools-i26-{card.case_id}-") as raw:
        destination = Path(raw)
        _materialize_git_snapshot(
            repository_root=repository_root,
            snapshot_sha=card.parent_snapshot_sha,
            source_roots=card.corpus_source_roots,
            destination=destination,
        )
        yield destination


def _batches(values: Sequence[Any], size: int) -> Iterable[Sequence[Any]]:
    for start in range(0, len(values), size):
        yield values[start : start + size]


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1_048_576), b""):
            digest.update(block)
    return digest.hexdigest()


def _digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
