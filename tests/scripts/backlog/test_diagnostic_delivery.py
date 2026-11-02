# Copyright (c) 2026
# ruff: noqa: D103, PLR2004, SLF001, EM101, TRY003 -- authored diagnostic boundary controls
"""Presentation delivery does not relax diagnostic schema or acceptance authority."""

from __future__ import annotations

import asyncio
import hashlib
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from devtools.core.time import Duration, Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
)
from devtools.resources.filesystem import FilesystemError
from scripts.backlog.intake import _digest
from scripts.backlog.native.execution import Capture
from scripts.backlog.native.review.diagnostic import parse, response_payload
from scripts.backlog.work import _load
from tests.scripts.backlog.test_diagnostic import answer, assert_observation_envelopes
from tests.scripts.backlog.test_diagnostic import (
    failed as failed,  # noqa: PLC0414 -- fixture
)
from tests.scripts.backlog.test_native import SOURCE, reviewer_policy
from tests.scripts.backlog.test_native import (
    repository as repository,  # noqa: PLC0414 -- fixture
)

if TYPE_CHECKING:
    from devtools.models.interaction import ModelRequest
    from scripts.backlog.work import WorkCycle


@pytest.mark.parametrize("wrapper", ["raw", "json", "bare", "whitespace", "crlf"])
def test_complete_presentation(wrapper: str) -> None:
    value = answer("a" * 64)
    value["findings"][0]["message"] = "A literal ``` and non-ASCII π are data."
    raw = json.dumps(value, ensure_ascii=False)
    text = {
        "raw": " \t\n" + raw + "\r\n",
        "json": "```json\n" + raw + "\n```",
        "bare": "```\n" + raw + "\n```",
        "whitespace": " \r\n\t```json \t\n" + raw + "\n```\r\n ",
        "crlf": "```json\r\n" + raw + "\r\n```",
    }[wrapper]
    payload, rule = response_payload(text)
    assert parse(payload, dict.fromkeys(value["evidence"], "b" * 64), "a" * 64) == value
    assert rule == ("none" if wrapper == "raw" else "single-json-fence-v1")
    if wrapper == "raw":
        assert payload == text


@pytest.mark.parametrize(
    "text",
    [
        "",
        "I refuse",
        "Here is the result: {}",
        "{} trailing prose",
        "before\n```json\n{}\n```",
        "```json\n{}\n```\nafter",
        "```JSON\n{}\n```",
        "```python\n{}\n```",
        "~~~json\n{}\n~~~",
        "````json\n{}\n````",
        "```json {} ```",
        "```json\n{}",
        "{}\n```",
        "```json\n{}\n````",
        "```json\n{}\n```\n```json\n{}\n```",
        "```json\n```json\n{}\n```\n```",
        "```json\n{\n```",
        "```json\n{} {}\n```",
        "```json\n[]\n```",
        "```json\nnull\n```",
    ],
)
def test_ambiguous_or_invalid_presentation_refused(text: str) -> None:
    with pytest.raises(ValueError, match=r".+"):
        parse(response_payload(text)[0], {"candidate": "b" * 64}, "a" * 64)


@pytest.mark.parametrize(
    "fault",
    ["schema", "status", "missing", "extra", "evidence", "claim", "duplicate"],
)
def test_closed_validator_still_controls_admission(fault: str) -> None:
    value = answer("a" * 64)
    refs = dict.fromkeys(value["evidence"], "b" * 64)
    if fault == "schema":
        value["schema"] = "native-review-v1"
    elif fault == "status":
        value["disposition"] = "accept"
    elif fault == "missing":
        del value["summary"]
    elif fault == "extra":
        value["host_approved"] = True
    elif fault == "evidence":
        value["evidence"] = []
    elif fault == "claim":
        value["findings"][0]["kind"] = "verified-by-host"
    raw = json.dumps(value)
    if fault == "duplicate":
        raw = '{"scope":"diagnostic-only",' + raw[1:]
    with pytest.raises(
        ValueError,
        match=r"[Dd]iagnostic|[Ii]nvalid|[Cc]oding|[Dd]uplicate",
    ):
        parse(response_payload("```json\n" + raw + "\n```")[0], refs, "a" * 64)


def test_exact_archived_b0051_response_is_new_test_evidence() -> None:
    path = Path(__file__).parent / "fixtures/b0051-diagnostic-response.json"
    fixture = json.loads(path.read_bytes())
    raw = fixture["response"]["content"]
    assert len(raw.encode()) == 7851
    assert hashlib.sha256(raw.encode()).hexdigest() == fixture["raw_content_sha256"]
    assert fixture["response"]["usage"]["output_tokens"] == 1838
    assert fixture["response"]["termination"] == "normal_stop"
    assert fixture["response"]["tool_calls"] == []
    with pytest.raises(json.JSONDecodeError):
        parse(raw, fixture["references"], fixture["candidate_sha256"])
    payload, rule = response_payload(raw)
    value = parse(payload, fixture["references"], fixture["candidate_sha256"])
    assert rule == "single-json-fence-v1"
    assert value["disposition"] == "findings"
    assert fixture["original_status"] == "blocked"
    assert fixture["original_conclusion"] is None
    # Validation does not certify the known incorrect location inside these findings.
    assert any(
        location["end_line"] == 63
        for finding in value["findings"]
        for location in finding["locations"]
    )


@pytest.mark.parametrize(
    "case",
    [
        "raw",
        "fenced",
        "invalid",
        "tools",
        "truncated",
        "oversized",
        "incompatible",
        "persistence",
        "legacy",
        "envelope",
        "bad-content",
    ],
)
def test_delivery_through_existing_owner(  # noqa: C901, PLR0915 -- finite delivery fault matrix
    failed: tuple[WorkCycle, str, str],
    monkeypatch: pytest.MonkeyPatch,
    case: str,
) -> None:
    class Model:
        source = InteractionSource("neutral-review-a")

        def __init__(self, candidate: str) -> None:
            self.candidate = candidate
            self.requests: list[ModelRequest] = []
            self.raw = ""

        async def send(self, request: ModelRequest) -> ModelResponse:
            self.requests.append(request)
            assert not request.tools
            assert request.provider_settings is None
            body = json.dumps(answer(self.candidate))
            self.raw = body if case == "raw" else "```json\n" + body + "\n```"
            if case == "invalid":
                self.raw = "```json\n{\n```"
            if case == "envelope":
                self.raw = "```python\n" + body + "\n```"
            if case == "bad-content":
                return ModelResponse(7, self.source)  # type: ignore[arg-type]
            if case == "oversized":
                self.raw += " " * 70000
            return ModelResponse(
                self.raw,
                self.source,
                termination=ModelTermination.OUTPUT_LIMIT
                if case == "truncated"
                else ModelTermination.TOOL_CALL
                if case == "incompatible"
                else ModelTermination.NORMAL_STOP,
                tool_calls=(
                    ModelToolCall(
                        "read_source",
                        json.dumps({"path": SOURCE, "start": 0}),
                        "late",
                    ),
                )
                if case == "tools"
                else (),
            )

    async def run() -> None:  # noqa: PLR0915 -- independent refusal/provenance controls
        c, item, archive = failed
        original_records = {p: p.read_bytes() for p in c._folder(item).glob("*.json")}
        policy = reviewer_policy()
        policy["read_paths"] = [SOURCE]
        policy["budgets"]["model_calls"] = 1
        reviewer = c.native.diagnostic_reviewer
        packet = await reviewer.prepare(item, reviewer=policy, archive=archive)
        if case == "legacy":
            del packet["delivery"]
            packet["sha256"] = _digest(
                {k: v for k, v in packet.items() if k != "sha256"},
            )
            (reviewer.folder(item) / "subject.json").write_text(
                json.dumps(packet),
                encoding="utf-8",
            )
        await reviewer.authorize(
            item,
            reference="fixture://delivery-only",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = Model(packet["subject"]["candidate_sha256"])
        if case == "persistence":
            original_add = Capture.add

            def fail_delivery(self: Capture, kind: str, value: dict[str, Any]) -> None:
                if kind == "review-response-delivery":
                    raise OSError("Delivery persistence unavailable")
                original_add(self, kind, value)

            monkeypatch.setattr(Capture, "add", fail_delivery)
        proposal = await reviewer.execute(
            item,
            interaction=model,
            profile=policy["profile"],
            authorize=lambda _: True,
        )
        assert len(model.requests) == 1
        assert not proposal["host_approved"]
        assert proposal["status"] == (
            "proposed" if case in {"raw", "fenced"} else "blocked"
        ), proposal
        assert_observation_envelopes(reviewer, item, proposal)
        frames = [
            _load(reviewer.folder(item) / r["file"], "backlog-native-observation-v1")
            for r in proposal["observations"]
        ]
        returned = next(f for f in frames if f["kind"] == "review-model-returned")
        assert returned["response"]["content"] == (
            7 if case == "bad-content" else model.raw
        )
        if case == "bad-content":
            assert returned["raw_content_sha256"] is None
        elif case != "legacy":
            assert (
                returned["raw_content_sha256"]
                == hashlib.sha256(model.raw.encode()).hexdigest()
            )
        deliveries = [
            f["delivery"] for f in frames if f["kind"] == "review-response-delivery"
        ]
        if case in {"raw", "fenced", "invalid", "envelope"}:
            delivery = deliveries[0]
            assert delivery["request_sha256"] == _digest(
                next(
                    f["request"] for f in frames if f["kind"] == "review-model-intent"
                ),
            )
            assert delivery["response_sha256"] == _digest(returned["response"])
            if case == "envelope":
                assert delivery["normalized_payload"] is None
                assert delivery["normalized_payload_sha256"] is None
                assert delivery["strict_validation"] == "not_entered"
            else:
                assert (
                    delivery["normalized_payload_sha256"]
                    == hashlib.sha256(
                        delivery["normalized_payload"].encode(),
                    ).hexdigest()
                )
                assert delivery["strict_validation"] == (
                    "failed" if case == "invalid" else "passed"
                )
            assert delivery["raw_content_sha256"] == returned["raw_content_sha256"]
        else:
            assert not deliveries
        with pytest.raises(PermissionError, match="Diagnostic"):
            reviewer.admit(item, proposal["sha256"], policy["actor"], accept=True)
        with pytest.raises((FilesystemError, FileExistsError)):
            await reviewer.execute(
                item,
                interaction=model,
                profile=policy["profile"],
                authorize=lambda _: True,
            )
        assert len(model.requests) == 1
        assert all(p.read_bytes() == value for p, value in original_records.items())

    asyncio.run(run())
