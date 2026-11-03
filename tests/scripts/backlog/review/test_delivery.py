# Copyright (c) 2026
# ruff: noqa: D103, SLF001, EM101, TRY003, PLR0915, C901, PLR0912, COM812 -- bounded contract controls
"""Explicit proposal transport, historical negative output and non-replay."""

from __future__ import annotations

import asyncio
import copy
import hashlib
import json
from dataclasses import asdict, replace
from pathlib import Path
from typing import TYPE_CHECKING, Any

import pytest

from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelTermination,
    ModelToolCall,
    Prompt,
    PromptMessage,
)
from devtools.models.interaction.providers import LlamaCppInteraction, llama_cpp
from scripts.backlog.native.execution import Capture
from scripts.backlog.native.review import delivery
from tests.scripts.backlog.test_native import (
    PUBLIC,
    approve_reviewer,
    conclusion,
    native_candidate,
    review_response,
    reviewer_policy,
)
from tests.scripts.backlog.test_native import repository as repository  # noqa: PLC0414

if TYPE_CHECKING:
    from scripts.backlog.work import WorkCycle


def packet() -> dict[str, Any]:
    return {
        "schema": "backlog-native-review-subject-v1",
        "sha256": "b" * 64,
        "delivery": dict(delivery.DELIVERY),
        "policy": reviewer_policy(),
        "subject": {
            "candidate_sha256": "a" * 64,
            "evidence": {
                "task": {
                    "obligations": [{"name": "owner"}],
                }
            },
        },
    }


def exchange(
    disposition: str = "accept",
) -> tuple[dict[str, Any], ModelRequest, ModelResponse]:
    p = packet()
    request = ModelRequest(
        Prompt("", "messages", (PromptMessage("system", delivery.SYSTEM),)),
        settings=ModelSettings(**p["policy"]["settings"]),
        tools=delivery.tools(p, source=False),
    )
    value = conclusion(disposition)
    if disposition == "insufficient-evidence":
        value["outstanding"] = ["A caller contract remains uninspected"]
    return (
        p,
        request,
        review_response(request, InteractionSource(p["policy"]["source"]), value),
    )


def decode(
    p: dict[str, Any], request: ModelRequest, response: ModelResponse
) -> dict[str, Any]:
    return delivery.conclusion(
        p,
        asdict(request),
        asdict(response),
        dict.fromkeys(conclusion()["evidence"], "c" * 64),
        set(),
    )


@pytest.mark.parametrize("disposition", ["accept", "reject", "insufficient-evidence"])
def test_closed_recommendations(disposition: str) -> None:
    p, request, response = exchange(disposition)
    before = asdict(response)
    assert decode(p, request, response)["disposition"] == disposition
    assert asdict(response) == before
    assert request.provider_settings is None
    assert [t.name for t in request.tools] == [delivery.NAME]
    assert [t.name for t in delivery.tools(p, source=True)] == [
        "read_source",
        delivery.NAME,
    ]
    schema = json.loads(request.tools[0].input_schema_json)
    assert schema["additionalProperties"] is False
    assert set(schema["required"]) == {
        "subject_sha256",
        "candidate_sha256",
        "conclusion",
    }
    fields = schema["properties"]["conclusion"]
    assert set(fields["required"]) == set(conclusion())
    assert fields["additionalProperties"] is False


def historical_response() -> str:
    root = Path(__file__).resolve().parents[4]
    archive = (
        root
        / "docs/research/code-audit/acceptance-review-recovery-20261102"
        / "parser-authentication.json"
    )
    original = json.loads(archive.read_bytes())
    raw: str = original["responses"][-1]["response"]["content"]
    assert (
        hashlib.sha256(raw.encode()).hexdigest()
        == "e55050c8904acaba77879cb4648dac286864bddd0dc298498368de3e6f28d0be"
    )
    assert original["responses"][-1]["response"]["termination"] == "normal_stop"
    return raw


def test_authentic_b0052_prose_is_not_a_proposal() -> None:
    p, request, response = exchange()
    raw = historical_response()
    assert "```python" in raw
    assert "<parameter=path>\nplaceholder" in raw
    with pytest.raises(ValueError, match="one disclosed final proposal"):
        decode(
            p,
            request,
            replace(
                response,
                content=raw,
                tool_calls=(),
                termination=ModelTermination.NORMAL_STOP,
            ),
        )


@pytest.mark.parametrize(
    "fault",
    [
        "json",
        "duplicate",
        "missing-envelope",
        "missing-conclusion",
        "extra",
        "subject",
        "candidate",
        "unsupported-name",
        "missing-id",
        "repeat-id",
        "mixed",
        "no-call",
        "stop",
        "truncated",
        "source",
        "references",
        "unassessed",
        "blocking",
        "diagnostic",
        "request-tools",
        "request-settings",
        "delivery",
    ],
)
def test_unsupported_or_ungrounded_delivery_fails(fault: str) -> None:
    p, request, response = exchange()
    raw = asdict(response)
    req = asdict(request)
    call = raw["tool_calls"][0]
    args = json.loads(call["arguments_json"])
    claimed: set[str] = set()
    if fault == "json":
        call["arguments_json"] = "{broken"
    elif fault == "duplicate":
        call["arguments_json"] = call["arguments_json"].replace(
            '"summary":', '"summary":"duplicate", "summary":'
        )
    elif fault == "missing-envelope":
        del args["candidate_sha256"]
    elif fault == "missing-conclusion":
        del args["conclusion"]["assessed_obligations"]
    elif fault == "extra":
        args["conclusion"]["extra"] = True
    elif fault in {"subject", "candidate"}:
        args[fault + "_sha256"] = "0" * 64
    elif fault == "unsupported-name":
        call["name"] = "accept_candidate"
    elif fault == "missing-id":
        call["provider_call_id"] = None
    elif fault == "repeat-id":
        claimed.add(call["provider_call_id"])
    elif fault == "mixed":
        raw["tool_calls"] = [*raw["tool_calls"], copy.deepcopy(call)]
    elif fault == "no-call":
        raw["tool_calls"] = []
        raw["content"] = json.dumps(conclusion())
    elif fault in {"stop", "truncated"}:
        raw["termination"] = "normal_stop" if fault == "stop" else "output_limit"
    elif fault == "source":
        raw["source"]["value"] = "foreign"
    elif fault == "references":
        args["conclusion"]["evidence"] = ["invented"]
    elif fault == "unassessed":
        args["conclusion"]["assessed_obligations"] = ["objective"]
    elif fault == "blocking":
        args["conclusion"]["findings"][0]["severity"] = "blocking"
    elif fault == "diagnostic":
        args["conclusion"] = {
            "schema": "native-diagnostic-conclusion-v1",
            "scope": "diagnostic-only",
            "disposition": "findings",
        }
    elif fault == "request-tools":
        req["tools"] = []
    elif fault == "request-settings":
        req["provider_settings"] = {
            "provider": "llama.cpp",
            "response_format": "json_object",
        }
    else:
        p["delivery"]["rule"] = "unknown"
    if fault not in {"json", "duplicate"}:
        call["arguments_json"] = json.dumps(args)
    with pytest.raises((ValueError, PermissionError)):
        delivery.conclusion(
            p, req, raw, dict.fromkeys(conclusion()["evidence"], "c" * 64), claimed
        )


def test_schema_validity_does_not_verify_a_factual_claim() -> None:
    p, request, response = exchange()
    call = response.tool_calls[0]
    args = json.loads(call.arguments_json)
    args["conclusion"]["summary"] = (
        "A model-authored claim the host must independently assess."
    )
    response = replace(
        response, tool_calls=(replace(call, arguments_json=json.dumps(args)),)
    )
    assert decode(p, request, response)["summary"] == args["conclusion"]["summary"]


def test_existing_adapter_transports_schema_and_exact_arguments(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    p, request, response = exchange()
    payloads: list[dict[str, object]] = []
    call = response.tool_calls[0]

    async def send(_endpoint: object, payload: dict[str, object]) -> dict[str, object]:
        payloads.append(payload)
        return {
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "message": {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": [
                            {
                                "id": call.provider_call_id,
                                "type": "function",
                                "function": {
                                    "name": call.name,
                                    "arguments": call.arguments_json,
                                },
                            }
                        ],
                    },
                }
            ]
        }

    monkeypatch.setattr(llama_cpp, "_post_chat_completion", send)
    actual = asyncio.run(
        LlamaCppInteraction(
            endpoint="http://127.0.0.1:1", model="scripted", source=response.source
        ).send(request)
    )
    assert actual.tool_calls == response.tool_calls
    assert decode(p, request, actual)["disposition"] == "accept"
    assert len(payloads) == 1
    assert "response_format" not in payloads[0]
    sent = payloads[0]["tools"]
    assert isinstance(sent, list)
    assert sent[0]["function"]["parameters"] == json.loads(
        request.tools[0].input_schema_json
    )


@pytest.mark.parametrize(
    "fault",
    ["prose", "capture-return", "capture-proposal", "persist", "budget", "truncated"],
)
def test_terminal_delivery_failure_consumes_dispatch(
    repository: tuple[WorkCycle, str],
    monkeypatch: pytest.MonkeyPatch,
    fault: str,
) -> None:
    async def run() -> None:
        c, item = repository
        await native_candidate(c, item)
        config = reviewer_policy()
        config["budgets"].update(model_calls=1, reads=1)
        await approve_reviewer(c, item, config)
        actor = c.native.reviewer
        before = {p: p.read_bytes() for p in c._folder(item).glob("*.json")}

        class Model:
            source = InteractionSource("neutral-review-a")
            requests: list[ModelRequest]

            def __init__(self) -> None:
                self.requests = []

            async def send(self, request: ModelRequest) -> ModelResponse:
                self.requests.append(request)
                assert [t.name for t in request.tools] == [delivery.NAME]
                assert (
                    "No source Tools" not in request.prompt.messages[0].content
                    or "submit_review_proposal" in request.prompt.messages[0].content
                )
                if fault == "prose":
                    return ModelResponse(
                        historical_response(),
                        self.source,
                        termination=ModelTermination.NORMAL_STOP,
                    )
                if fault == "budget":
                    return ModelResponse(
                        "",
                        self.source,
                        tool_calls=(
                            ModelToolCall(
                                "read_source",
                                json.dumps({"path": PUBLIC, "start": 0}),
                                "no-read-allowance",
                            ),
                        ),
                    )
                result = review_response(request, self.source, conclusion())
                return (
                    replace(result, termination=ModelTermination.OUTPUT_LIMIT)
                    if fault == "truncated"
                    else result
                )

        original = Capture.add

        def capture(self: Capture, kind: str, value: dict[str, Any]) -> None:
            if (fault == "capture-return" and kind == "review-model-returned") or (
                fault == "capture-proposal" and kind == "review-conclusion-proposal"
            ):
                raise OSError("authored mandatory capture failure")
            original(self, kind, value)

        monkeypatch.setattr(Capture, "add", capture)
        save = actor.save

        def persist(item: str, name: str, value: dict[str, Any]) -> dict[str, Any]:
            if name == "proposal" and fault == "persist":
                raise OSError("authored terminal persistence failure")
            return save(item, name, value)

        monkeypatch.setattr(actor, "save", persist)
        model = Model()
        if fault == "persist":
            with pytest.raises(OSError, match="persistence"):
                await actor.execute(
                    item,
                    interaction=model,
                    profile=config["profile"],
                    authorize=lambda _: True,
                )
        else:
            result = await actor.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=lambda _: True,
            )
            assert result["status"] == "blocked"
            assert result["conclusion"] is None
            assert result["model_calls"] == 1
            assert result["reads"] == 0
            with pytest.raises(PermissionError):
                actor.admit(item, result["sha256"], config["actor"], accept=True)
        assert len(model.requests) == 1
        with pytest.raises(FileExistsError):
            await actor.execute(
                item,
                interaction=model,
                profile=config["profile"],
                authorize=lambda _: True,
            )
        assert len(model.requests) == 1
        assert all(p.read_bytes() == v for p, v in before.items())
        assert not list(c._folder(item).glob("review-*.json"))

    asyncio.run(run())


def test_historical_raw_conclusion_remains_consumable(
    repository: tuple[WorkCycle, str],
) -> None:
    """Keep the concrete durable raw-content contract for older accepted subjects."""
    from devtools.core.time import Duration, Timestamp  # noqa: PLC0415
    from scripts.backlog.intake import _digest  # noqa: PLC0415
    from tests.scripts.backlog.test_native import ReviewModel  # noqa: PLC0415

    async def run() -> None:
        c, item = repository
        await native_candidate(c, item)
        actor = c.native.reviewer
        config = reviewer_policy()
        await actor.prepare(item, reviewer=config)
        # Author a historical subject before any grant in this tiny fixture.
        path = actor.folder(item) / "subject.json"
        historical = json.loads(path.read_bytes())
        historical.pop("sha256")
        historical.pop("delivery")
        historical["sha256"] = _digest(historical)
        path.write_text(json.dumps(historical), encoding="utf-8")
        await actor.authorize(
            item,
            reference="fixture://historical-raw-review",
            expires=Timestamp.now() + Duration.minutes(5),
            authorize=lambda _: True,
        )
        model = ReviewModel()
        proposal = await actor.execute(
            item,
            interaction=model,
            profile=config["profile"],
            authorize=lambda _: True,
        )
        assert proposal["status"] == "proposed"
        assert all(
            delivery.NAME not in {t.name for t in r.tools} for r in model.requests
        )
        review = await actor.decide(
            item,
            proposal=proposal["sha256"],
            accept=True,
            reference="fixture://historical-host-disposition",
            rationale="Independent authored assessment of the original raw response",
            authorize=lambda _: True,
        )
        assert c.native.candidate(item, review["sha256"])["review"] == review

    asyncio.run(run())
