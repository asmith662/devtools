# Copyright (c) 2026
# ruff: noqa: E501
"""Pre-outcome Increment-26 protocol configuration; no encoder execution."""

from __future__ import annotations

import hashlib
import json
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pathlib import Path

INCREMENT_25_FREEZE_IDENTITY = (
    "df4128bf1a6afc246aff072ff3922e4b9deb0205c95b74310a64d29497c02c0b"
)
SCHEMA = "devtools-increment-26-semantic-candidate-generation-freeze-v1"
MODEL_REPOSITORY = "nomic-ai/CodeRankEmbed"
MODEL_REVISION = "3c4b60807d71f79b43f3c4363786d9493691f8b1"
MODEL_WEIGHT_FILENAME = "model.safetensors"
MODEL_WEIGHT_SHA256 = "827529bcd58aef0d9082e66eeff7e7d53a02f62bd005f841a26b3d3e2fb17ebe"
MODEL_XET_HASH = "2c08597aed3bb850ee42d4c9f38cbfb646762fada0bb8e45d2084f445b43c947"
TOKENIZER_FILENAME = "tokenizer.json"
TOKENIZER_CLASS = "BertTokenizer"
TOKENIZER_MAX_LENGTH = 8192
MAX_INPUT_TOKENS = 2048
SPECIAL_TOKEN_ALLOWANCE = 2
CHUNK_CONTENT_TOKENS = MAX_INPUT_TOKENS - SPECIAL_TOKEN_ALLOWANCE
CHUNK_OVERLAP_TOKENS = 256
CAPACITY = 5
QUERY_PREFIX = "Represent this query for searching relevant code: "


def build_freeze(*, increment_25_freeze_path: Path) -> dict[str, object]:
    """Build the immutable configuration without encoding a query or resource."""
    population = _population_contract(increment_25_freeze_path)
    payload: dict[str, object] = {
        "protocol": {
            "identity": "increment-26-independent-semantic-candidate-generation-v1",
            "proposition": "For a frozen InformationNeed and historical parent-snapshot corpus, similarity under one pinned pretrained representation configuration may expose useful repository resources that an equal-cardinality canonical lexical surface does not expose.",
            "non_claims": [
                "not lexically seeded semantic expansion",
                "not learned ranking or model training",
                "not production hybrid retrieval",
                "not Context selection or K=5 insertion",
                "not Increment-27 evidence-family comparison",
            ],
            "information_need_distinction": "InformationNeed is not query text. This experiment holds the task-card lexical_query constant across independent lexical and semantic mechanisms to isolate candidate generation.",
            "outcomes_generated": False,
            "usefulness_adjudication_started": False,
            "confirmation_status": "sealed-for-semantic-outcomes",
        },
        "population": population,
        "encoder": {
            "repository": MODEL_REPOSITORY,
            "revision": MODEL_REVISION,
            "license": "MIT",
            "model_card": "https://huggingface.co/nomic-ai/CodeRankEmbed",
            "weight_artifact": {
                "filename": MODEL_WEIGHT_FILENAME,
                "sha256": MODEL_WEIGHT_SHA256,
                "xet_hash": MODEL_XET_HASH,
                "parameter_count": 136731648,
                "dtype": "float32",
            },
            "tokenizer": {
                "filename": TOKENIZER_FILENAME,
                "class": TOKENIZER_CLASS,
                "revision": MODEL_REVISION,
                "model_max_length": TOKENIZER_MAX_LENGTH,
                "special_tokens": ["[CLS]", "[SEP]"],
            },
            "execution": {
                "runtime_group": "increment-26",
                "python_requires": ">=3.12",
                "transformers": "5.17.0",
                "torch": "2.14.0",
                "device": "cpu",
                "model_mode": "eval",
                "gradient_mode": "inference_mode",
                "vector_dtype": "float32",
                "custom_code": "trust_remote_code=True at the pinned model revision only",
                "determinism": "CPU execution; stable input order; no stochastic sampling; exact replay identity required subject to documented numerical-runtime limits.",
            },
        },
        "representation": {
            "query": {
                "source": "task-card.lexical_query exactly",
                "serialization": QUERY_PREFIX + "{lexical_query}",
                "task_derived_content": "lexical_query only",
                "overlength": "reject rather than truncate when tokenized query content exceeds 2046 tokens",
            },
            "document": {
                "source": "RepositoryTextDocument resource content from the frozen parent snapshot",
                "serialization": "raw decoded source content only; no filename, address, path, language marker, diff, changed-path metadata, or post-change content",
                "empty_resource": "produces zero chunks and no semantic resource candidate",
            },
            "chunking": {
                "tokenizer_relative": True,
                "maximum_input_tokens": MAX_INPUT_TOKENS,
                "special_token_allowance": SPECIAL_TOKEN_ALLOWANCE,
                "content_tokens_per_chunk": CHUNK_CONTENT_TOKENS,
                "overlap_tokens": CHUNK_OVERLAP_TOKENS,
                "stride_tokens": CHUNK_CONTENT_TOKENS - CHUNK_OVERLAP_TOKENS,
                "coverage": "tokenize without special tokens; emit ordered overlapping windows across all content tokens; add tokenizer special tokens only when encoding each window; retain the final nonempty partial window",
                "text_decoding": "reuse the already decoded immutable RepositoryTextDocument content; introduce no additional normalization or newline rewriting",
            },
            "encoding": {
                "query_method": "documented CodeRankEmbed query instruction prefix plus frozen lexical_query",
                "chunk_method": "raw chunk text without instruction prefix",
                "pooling": "CLS-token pooling, as declared by the pinned sentence-transformers pooling configuration",
                "normalization": "L2 normalize each float32 embedding before comparison",
                "similarity": "float32 dot product of L2-normalized vectors (cosine similarity)",
                "resource_aggregation": "maximum chunk similarity per repository resource",
                "chunk_support": "retain every chunk ordinal tied at the resource maximum; winning chunk is the lowest ordinal",
                "resource_tie_break": "descending resource score, then ascending repository resource address",
            },
            "unit_boundary": "Chunks are experiment-local representations, not RepositorySubjects, Repository Intelligence, retrieval candidates, or Context units. Candidate and judgment unit is one repository resource.",
        },
        "arms": {
            "semantic": "top n distinct resources by semantic resource score",
            "lexical": "top n positive-scoring resources under canonical content-BM25 plus 0.25 * filename-stem-BM25",
            "capacity": {
                "target": CAPACITY,
                "n": "min(5, available semantic resources, available positive lexical resources)",
                "zero_padding": "prohibited",
                "exhaustion": "record separately for each arm",
                "shared_lexical_seed": False,
            },
            "structural": "not an Increment-26 candidate input, modifier, capacity control, or judgment input",
        },
        "judgment_reuse": {
            "rule": "Reuse an Increment-25 usefulness judgment if and only if InformationNeed identity, parent snapshot identity, repository resource address, and usefulness semantics are identical. Candidate origin is irrelevant.",
            "new_resources": "require blinded three-state judgment",
            "hidden_from_new_judgment": [
                "semantic versus lexical origin",
                "semantic and lexical rank or score",
                "chunk identity and support",
                "changed-path metadata",
                "structural origin or history",
            ],
        },
        "measurements": [
            "semantic and lexical candidate count",
            "per-case and aggregate overlap, semantic-only, and lexical-only counts",
            "USEFUL, NOT_USEFUL, and UNJUDGED counts per arm",
            "useful overlap, semantic-only, and lexical-only resources",
            "semantic candidates without a positive lexical rank and their positive lexical ranks when present",
            "native semantic resource score and winning-chunk/support provenance for audit",
            "arm exhaustion and deterministic replay identity",
        ],
        "falsification": [
            "no useful semantic-only resource appears on frozen confirmation",
            "all useful semantic resources occur in the equal-volume lexical arm",
            "semantic-only additions are overwhelmingly NOT_USEFUL",
            "replay is not reproducible under the frozen configuration",
            "results materially depend on undocumented truncation or runtime choices",
        ],
    }
    return {"schema": SCHEMA, "content_identity": _digest(payload), "payload": payload}


def validate_freeze(envelope: dict[str, object]) -> bool:
    """Validate configuration identity, population binding, and outcome absence."""
    if envelope.get("schema") != SCHEMA or not isinstance(envelope.get("payload"), dict):
        return False
    payload = cast("dict[str, object]", envelope["payload"])
    if envelope.get("content_identity") != _digest(payload):
        return False
    population = cast("dict[str, object]", payload["population"])
    if population.get("increment_25_freeze_identity") != INCREMENT_25_FREEZE_IDENTITY:
        return False
    return not (_keys(payload) & _PROHIBITED_OUTCOME_KEYS)


_PROHIBITED_OUTCOME_KEYS = frozenset(
    {
        "embeddings",
        "semantic_candidates",
        "semantic_results",
        "semantic_scores_by_resource",
        "semantic_similarities",
        "retrieval_outcomes",
    },
)


def _population_contract(path: Path) -> dict[str, object]:
    envelope = cast("dict[str, object]", json.loads(path.read_text(encoding="utf-8")))
    if envelope.get("content_identity") != INCREMENT_25_FREEZE_IDENTITY:
        msg = "Increment-26 must reuse the exact frozen Increment-25 population."
        raise ValueError(msg)
    payload = cast("dict[str, object]", envelope["payload"])
    split = cast("dict[str, list[str]]", payload["split"])
    cards = cast("list[dict[str, object]]", payload["task_cards"])
    card_ids = {str(card["case_id"]) for card in cards}
    if set().union(*split.values()) != card_ids:
        msg = "Increment-25 population partitions do not exactly cover its task cards."
        raise ValueError(msg)
    return {
        "increment_25_freeze_identity": str(envelope["content_identity"]),
        "source_roots": ["src", "tests"],
        "development_case_ids": split["development_case_ids"],
        "confirmation_case_ids": split["confirmation_case_ids"],
        "reserve_case_ids": split["reserve_case_ids"],
        "query_source": "each selected task card lexical_query",
    }


def _keys(value: object) -> set[str]:
    if isinstance(value, dict):
        mapping_keys = {str(key) for key in value}
        for item in value.values():
            mapping_keys.update(_keys(item))
        return mapping_keys
    if isinstance(value, list):
        list_keys: set[str] = set()
        for item in value:
            list_keys.update(_keys(item))
        return list_keys
    return set()


def _digest(payload: object) -> str:
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(),
    ).hexdigest()
