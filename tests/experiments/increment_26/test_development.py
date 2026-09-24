# Copyright (c) 2026
# ruff: noqa: ANN401, D101, D102, D103, E501, PLR2004, S105, SLF001
"""Contract checks for the frozen Increment-26 development consumer."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any, cast

import pytest
import torch

from devtools.context.repository.resource import RepositoryResourceAddress
from devtools.context.retrieval.lexical.bm25 import (
    analyze_repository_text_lexical_query,
)
from experiments.increment_25.development import (
    _build_snapshot_corpus,
    load_frozen_development,
)
from experiments.increment_25.task_population import TaskCard
from experiments.increment_26 import development
from experiments.increment_26.configuration import (
    CAPACITY,
    CHUNK_CONTENT_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    MODEL_REPOSITORY,
    MODEL_REVISION,
    QUERY_PREFIX,
)
from experiments.increment_26.run_development import parse_arguments

I25 = Path("experiments/increment_25/task_population_freeze.json")
I26 = Path("experiments/increment_26/experiment_freeze.json")


class Tokenizer:
    cls_token_id = 101
    sep_token_id = 102

    def encode(self, content: str, *, add_special_tokens: bool) -> list[int]:
        assert not add_special_tokens
        return [ord(item) for item in content]

    def pad(self, prepared: list[dict[str, list[int]]], *, padding: bool, return_tensors: str) -> dict[str, torch.Tensor]:
        assert padding
        assert return_tensors == "pt"
        width = max(len(item["input_ids"]) for item in prepared)
        return {
            name: torch.tensor([item[name] + [0] * (width - len(item[name])) for item in prepared])
            for name in ("input_ids", "attention_mask")
        }


class Model:
    def __call__(self, *, input_ids: torch.Tensor, attention_mask: torch.Tensor, return_dict: bool) -> Any:
        assert return_dict
        assert torch.all(attention_mask[:, 0] == 1)
        assert torch.all(input_ids[:, 0] == 101)
        class Output:
            last_hidden_state = torch.stack(
                (torch.stack((input_ids[:, 1].float(), torch.full_like(input_ids[:, 1], 2).float()), dim=1),
                 torch.full((len(input_ids), 2), 999.0)),
                dim=1,
            )
        return Output()


def card(*, query: str = "needle") -> TaskCard:
    return TaskCard(
        case_id="test-development", source_commit_sha="b" * 40,
        parent_snapshot_sha="a" * 40, original_subject="subject", original_body="",
        information_need_purpose="secret purpose", lexical_query=query,
        maintenance_category="feature", repository_domain="context",
        corpus_source_roots=("src", "tests"),
        evaluator_only_changed_paths=("src/secret_changed.py",),
    )


def corpus(tmp_path: Path, resources: dict[str, str]) -> Any:
    for address, content in resources.items():
        target = tmp_path / address
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return _build_snapshot_corpus(snapshot_root=tmp_path, source_roots=("src", "tests"))


def test_exact_freeze_and_partition_enforced(tmp_path: Path) -> None:
    assert development.load_frozen_increment_26(I26, increment_25_freeze_path=I25)["content_identity"] == "a8d57b68a8043b88300c8ea5f28d12266a1d74f7aa9e9a09e323a4c6ba9f22c1"
    changed = json.loads(I26.read_text(encoding="utf-8"))
    changed["payload"]["representation"]["chunking"]["overlap_tokens"] = 1
    changed["content_identity"] = development._digest(changed["payload"])
    path = tmp_path / "changed.json"
    path.write_text(json.dumps(changed), encoding="utf-8")
    with pytest.raises(ValueError, match="committed amended protocol"):
        development.load_frozen_increment_26(path, increment_25_freeze_path=I25)
    frozen = load_frozen_development(I25)
    assert len(frozen.development_case_ids) == 8
    for case_id in frozen.confirmation_case_ids | frozen.reserve_case_ids:
        with pytest.raises(ValueError, match=r"case|Case"):
            frozen.require_case(case_id)
    assert "partition" not in vars(parse_arguments(["--candidate-output", "a", "--judgment-output", "b"]))


def test_offline_encoder_uses_exact_local_revision_without_metadata_lookup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    weights = b"locally verified frozen weights"
    (tmp_path / "model.safetensors").write_bytes(weights)
    calls: list[dict[str, object]] = []

    class RejectingHfApi:
        def model_info(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError

    def resolve_snapshot(**kwargs: object) -> str:
        calls.append(kwargs)
        return str(tmp_path)

    class LoadedModel:
        def to(self, device: str) -> LoadedModel:
            assert device == "cpu"
            return self

        def eval(self) -> LoadedModel:
            return self

    class LoadedTokenizer:
        cls_token = "[CLS]"
        sep_token = "[SEP]"
        cls_token_id = 101
        sep_token_id = 102

        def num_special_tokens_to_add(self, *, pair: bool) -> int:
            assert not pair
            return 2

        def encode(self, _text: str, *, add_special_tokens: bool) -> list[int]:
            return [101, 103, 102] if add_special_tokens else [103]

    class AutoModel:
        @staticmethod
        def from_pretrained(_path: Path, **kwargs: object) -> LoadedModel:
            assert kwargs["revision"] == MODEL_REVISION
            assert kwargs["local_files_only"] is True
            return LoadedModel()

    class AutoTokenizer:
        @staticmethod
        def from_pretrained(_path: Path, **kwargs: object) -> LoadedTokenizer:
            assert kwargs["revision"] == MODEL_REVISION
            assert kwargs["local_files_only"] is True
            return LoadedTokenizer()

    monkeypatch.setattr(
        "experiments.increment_26.development.HfApi",
        RejectingHfApi,
    )
    monkeypatch.setattr(development, "snapshot_download", resolve_snapshot)
    monkeypatch.setattr(development, "MODEL_WEIGHT_SHA256", hashlib.sha256(weights).hexdigest())
    monkeypatch.setitem(
        sys.modules,
        "transformers",
        SimpleNamespace(AutoModel=AutoModel, AutoTokenizer=AutoTokenizer),
    )

    model, tokenizer, identity = development.realize_pinned_encoder(
        cache_dir=tmp_path / "hub-cache",
        offline=True,
    )

    assert isinstance(model, LoadedModel)
    assert isinstance(tokenizer, LoadedTokenizer)
    assert calls == [
        {
            "repo_id": MODEL_REPOSITORY,
            "revision": MODEL_REVISION,
            "cache_dir": tmp_path / "hub-cache",
            "local_files_only": True,
        },
    ]
    assert identity == {
        "repository": MODEL_REPOSITORY,
        "revision": MODEL_REVISION,
        "weight_filename": "model.safetensors",
        "weight_sha256": hashlib.sha256(weights).hexdigest(),
        "device": "cpu",
    }


@pytest.mark.parametrize("artifact", ["missing", "hash_mismatch"])
def test_offline_encoder_rejects_missing_or_unverified_weights_without_fallback(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    artifact: str,
) -> None:
    if artifact == "hash_mismatch":
        (tmp_path / "model.safetensors").write_bytes(b"wrong weights")
    calls: list[dict[str, object]] = []

    class RejectingHfApi:
        def model_info(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError

    def resolve_snapshot(**kwargs: object) -> str:
        calls.append(kwargs)
        return str(tmp_path)

    monkeypatch.setattr(
        "experiments.increment_26.development.HfApi",
        RejectingHfApi,
    )
    monkeypatch.setattr(development, "snapshot_download", resolve_snapshot)
    monkeypatch.setattr(development, "MODEL_WEIGHT_SHA256", "0" * 64)

    with pytest.raises(development.ModelIntegrityError, match=r"model.safetensors"):
        development.realize_pinned_encoder(offline=True)

    assert calls[0]["repo_id"] == MODEL_REPOSITORY
    assert calls[0]["revision"] == MODEL_REVISION
    assert calls[0]["local_files_only"] is True


def test_offline_encoder_propagates_missing_snapshot_without_network_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    calls: list[dict[str, object]] = []

    class RejectingHfApi:
        def model_info(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError

    def missing_snapshot(**kwargs: object) -> str:
        calls.append(kwargs)
        raise FileNotFoundError

    monkeypatch.setattr(
        "experiments.increment_26.development.HfApi",
        RejectingHfApi,
    )
    monkeypatch.setattr(development, "snapshot_download", missing_snapshot)

    with pytest.raises(FileNotFoundError):
        development.realize_pinned_encoder(offline=True)

    assert calls[0]["repo_id"] == MODEL_REPOSITORY
    assert calls[0]["revision"] == MODEL_REVISION
    assert calls[0]["local_files_only"] is True


def test_offline_option_does_not_change_frozen_computation_settings() -> None:
    freeze = json.loads(I26.read_text(encoding="utf-8"))
    execution = freeze["payload"]["encoder"]["execution"]
    assert development.ENCODE_BATCH_SIZE == 16
    assert execution["device"] == "cpu"
    assert execution["vector_dtype"] == "float32"
    assert CAPACITY == 5
    assert CHUNK_CONTENT_TOKENS == 2046
    assert CHUNK_OVERLAP_TOKENS == 256
    assert QUERY_PREFIX == "Represent this query for searching relevant code: "
    assert parse_arguments(
        ["--candidate-output", "a", "--judgment-output", "b", "--offline"],
    ).offline is True


def test_query_prefix_and_chunk_coverage() -> None:
    assert development.serialize_query(lexical_query="Exact query") == QUERY_PREFIX + "Exact query"
    tokenizer = Tokenizer()
    assert development.tokenize_source_chunks(content="", tokenizer=tokenizer) == ()
    content = "a" * (CHUNK_CONTENT_TOKENS + 1)
    chunks = development.tokenize_source_chunks(content=content, tokenizer=tokenizer)
    assert [(item.start_token, item.end_token) for item in chunks] == [(0, CHUNK_CONTENT_TOKENS), (CHUNK_CONTENT_TOKENS - CHUNK_OVERLAP_TOKENS, len(content))]
    assert chunks[0].token_ids[-CHUNK_OVERLAP_TOKENS:] == chunks[1].token_ids[:CHUNK_OVERLAP_TOKENS]
    assert chunks[-1].end_token == len(content)


def test_cls_float32_normalization_and_dot_similarity() -> None:
    tokenizer = Tokenizer()
    vectors = development._encode_token_sequences(model=Model(), tokenizer=tokenizer, sequences=((3,), (4,)))
    assert vectors.dtype == torch.float32
    assert torch.allclose(torch.linalg.vector_norm(vectors, dim=1), torch.ones(2))
    assert torch.allclose(vectors[0], torch.tensor([3 / 13**0.5, 2 / 13**0.5]))
    assert torch.dot(vectors[0], vectors[1]).item() == pytest.approx(torch.nn.functional.cosine_similarity(vectors[0], vectors[1], dim=0).item())


def test_raw_source_max_chunk_and_ties(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = corpus(tmp_path, {"src/a.py": "a" * CHUNK_CONTENT_TOKENS + "b", "src/b.py": "b", "src/empty.py": ""})
    seen: list[tuple[int, ...]] = []

    def encode(*, sequences: tuple[tuple[int, ...], ...], **_kwargs: Any) -> torch.Tensor:
        seen.extend(sequences)
        return torch.tensor([[1.0, 0.0] if ord("b") in sequence else [0.0, 1.0] for sequence in sequences])

    monkeypatch.setattr(development, "_encode_token_sequences", encode)
    cache: dict[tuple[int, ...], Any] = {}
    ranked = development.score_snapshot_resources(
        corpus=source, model=None, tokenizer=Tokenizer(), query_vector=torch.tensor([1.0, 0.0]), embedding_cache=cache,
    )
    encoded_count = len(seen)
    assert development.score_snapshot_resources(
        corpus=source, model=None, tokenizer=Tokenizer(), query_vector=torch.tensor([1.0, 0.0]), embedding_cache=cache,
    ) == ranked
    assert len(seen) == encoded_count
    assert [str(item.address) for item in ranked] == ["src/a.py", "src/b.py"]
    assert ranked[0].score == ranked[1].score == 1.0
    assert ranked[0].chunk_count == 2
    assert ranked[0].winning_chunk.ordinal == 1
    assert ranked[0].maximum_chunk_ordinals == (1,)
    assert (ord("b"),) in seen
    assert any(len(item) == CHUNK_CONTENT_TOKENS and item[0] == ord("a") for item in seen)


def test_additive_padding_mask_is_frozen_float32() -> None:
    mask = development._extended_attention_mask(torch.tensor([[1, 1, 0]]), (1, 3))
    assert mask.shape == (1, 1, 1, 3)
    assert mask.dtype == torch.float32
    assert mask[0, 0, 0, :2].tolist() == [0.0, 0.0]
    assert mask[0, 0, 0, 2].item() == torch.finfo(torch.float32).min


def test_artifact_guards_reject_sealed_cases_and_mechanism_leakage() -> None:
    frozen = load_frozen_development(I25)
    with pytest.raises(ValueError, match="exactly the eight"):
        development._assert_evidence(
            evidence={"cases": [{"case_id": next(iter(frozen.confirmation_case_ids))}]},
            frozen=frozen,
        )
    with pytest.raises(RuntimeError, match="leaks"):
        development._assert_judgment({"cases": [{"score": 0.5}]})


def test_independent_arms_blinding_and_deterministic_serialization(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source = corpus(tmp_path, {"src/a.py": "needle", "src/b.py": "needle", "src/c.py": "other", "src/d.py": ""})
    captured: list[str] = []
    canonical = analyze_repository_text_lexical_query

    def analyze(*, text: str) -> Any:
        captured.append(text)
        return canonical(text=text)

    monkeypatch.setattr(development, "analyze_repository_text_lexical_query", analyze)
    monkeypatch.setattr(development, "encode_query", lambda **_kwargs: torch.tensor([1.0, 0.0]))

    def score(**_kwargs: Any) -> tuple[development.SemanticResourceScore, ...]:
        chunk = development.TokenChunk(0, 0, 1, (1,))
        return tuple(development.SemanticResourceScore(RepositoryResourceAddress(address), value, 1, chunk, (0,)) for address, value in (("src/c.py", 1.0), ("src/b.py", 0.5), ("src/a.py", 0.5)))

    monkeypatch.setattr(development, "score_snapshot_resources", score)
    first = development.generate_case(card=card(query="needle"), corpus=source, model=None, tokenizer=None)
    second = development.generate_case(card=card(query="needle"), corpus=source, model=None, tokenizer=None)
    assert first == second
    assert captured == ["needle", "needle"]
    assert first["capacity"] == {"n": 2, "semantic_available": 3, "positive_lexical_available": 2, "semantic_exhausted": True, "lexical_exhausted": True}
    assert [item["address"] for item in cast("list[dict[str, object]]", first["semantic_candidates"])] == ["src/c.py", "src/b.py"]
    assert cast("list[dict[str, object]]", first["semantic_candidates"])[0]["positive_lexical_rank"] is None
    assert first["overlap"] == {"intersection": ["src/b.py"], "semantic_only": ["src/c.py"], "lexical_only": ["src/a.py"]}
    blinded = development._judgment_case(card=card(), case=first, corpus=source)
    assert [item["address"] for item in cast("list[dict[str, str]]", blinded["resources"])] == ["src/a.py", "src/b.py", "src/c.py"]
    development._assert_judgment(blinded)
    rendered = json.dumps(blinded).lower()
    for hidden in ("semantic_candidates", "lexical_candidates", "winning_chunk", "positive_lexical_rank", "secret_changed", "origin"):
        assert hidden not in rendered
    assert "secret purpose" in rendered
    path = tmp_path / "artifact.json"
    development.write_artifact(path=path, payload=first)
    before = path.read_bytes()
    development.write_artifact(path=path, payload=second)
    assert path.read_bytes() == before
