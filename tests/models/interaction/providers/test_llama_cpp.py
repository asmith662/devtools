# Copyright (c) 2026
"""Deterministic tests for the llama.cpp ModelInteraction adapter."""

from __future__ import annotations

import asyncio
import json
from urllib.parse import urlsplit

import pytest

from devtools.agents.conversation import ConversationMessageRole
from devtools.models.interaction import ConversationRef, InteractionSource, Prompt
from devtools.models.interaction.providers import (
    LlamaCppHttpError,
    LlamaCppInteraction,
    LlamaCppResponseError,
    LlamaCppTransportError,
    llama_cpp,
)

_HTTP_BAD_REQUEST = 400
_OFFLINE = "offline"
_INPUT_TOKENS = 8
_OUTPUT_TOKENS = 4
_PROVIDER_TOTAL_TOKENS = 99
_MAXIMUM_OUTPUT_TOKENS = 64


def _reader(response: bytes) -> asyncio.StreamReader:
    """Create an EOF-delimited StreamReader for a deterministic response."""
    reader = asyncio.StreamReader()
    reader.feed_data(response)
    reader.feed_eof()
    return reader


class _Writer:
    """Capture one provider request."""

    def __init__(self) -> None:
        """Initialize empty captured state."""
        self.request = b""
        self.closed = False

    def write(self, data: bytes) -> None:
        """Capture request data."""
        self.request += data

    async def drain(self) -> None:
        """Model a successful socket drain."""

    def close(self) -> None:
        """Record close ownership."""
        self.closed = True

    async def wait_closed(self) -> None:
        """Model successful closure."""


def _response(status: int, body: object, *, content_length: bool = False) -> bytes:
    """Construct one minimal HTTP response with optional explicit framing."""
    encoded = json.dumps(body).encode()
    length_header = f"Content-Length: {len(encoded)}\r\n" if content_length else ""
    return (
        f"HTTP/1.1 {status} Test\r\nContent-Type: application/json\r\n"
        f"{length_header}\r\n"
    ).encode() + encoded


def _message(
    role: ConversationMessageRole,
    content: str = "Inspect the fixture.",
) -> Prompt:
    return Prompt(content=content, role=role.value)


def _interaction() -> LlamaCppInteraction:
    return LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model="qwen-local",
        source=InteractionSource("qwen"),
    )


@pytest.mark.parametrize(
    "role",
    [ConversationMessageRole.USER, ConversationMessageRole.SYSTEM],
)
def test_interaction_maps_existing_message_roles_to_non_streaming_llama_request(
    monkeypatch: pytest.MonkeyPatch,
    role: ConversationMessageRole,
) -> None:
    """Existing USER and SYSTEM Messages remain truthful provider input."""
    writer = _Writer()

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return (
            _reader(
                _response(
                    200,
                    {
                        "choices": [
                            {
                                "finish_reason": "stop",
                                "message": {
                                    "role": "assistant",
                                    "content": "Qwen reply",
                                },
                            },
                        ],
                    },
                ),
            ),
            writer,
        )

    monkeypatch.setattr(asyncio, "open_connection", connection)

    turn = asyncio.run(_interaction().send(_message(role, "exact content")))

    headers, _, body = writer.request.partition(b"\r\n\r\n")
    request = json.loads(body)
    assert headers.startswith(b"POST /v1/chat/completions HTTP/1.1\r\n")
    assert request == {
        "model": "qwen-local",
        "messages": [{"role": role.value, "content": "exact content"}],
        "stream": False,
    }
    assert turn.content == "Qwen reply"
    assert turn.source == InteractionSource("qwen")
    assert turn.conversation is None
    assert turn.usage is None
    assert writer.closed is True


def test_interaction_maps_requested_output_bound_to_pinned_llama_cpp_max_tokens(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The provider receives only the established OpenAI-compatible cap field."""
    writer = _Writer()

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return (
            _reader(
                _response(
                    200,
                    {
                        "choices": [
                            {"message": {"role": "assistant", "content": "reply"}},
                        ],
                    },
                ),
            ),
            writer,
        )

    monkeypatch.setattr(asyncio, "open_connection", connection)

    turn = asyncio.run(
        _interaction().send(
            _message(ConversationMessageRole.USER),
            maximum_output_tokens=_MAXIMUM_OUTPUT_TOKENS,
        ),
    )

    _, _, body = writer.request.partition(b"\r\n\r\n")
    request = json.loads(body)
    assert request["max_tokens"] == _MAXIMUM_OUTPUT_TOKENS
    assert "max_completion_tokens" not in request
    assert "n_predict" not in request
    assert turn.content == "reply"


@pytest.mark.parametrize("value", [0, -1, True, False, "8", 8.0])
def test_interaction_rejects_invalid_output_bound_before_provider_request(
    value: object,
) -> None:
    """Invalid shared request constraints never become provider HTTP failures."""
    with pytest.raises(ValueError, match="positive integer"):
        asyncio.run(
            _interaction().send(
                _message(ConversationMessageRole.USER),
                maximum_output_tokens=value,  # type: ignore[arg-type]
            ),
        )


def test_interaction_preserves_pinned_llama_cpp_standard_usage(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The pinned provider's three standard counts form ModelUsage unchanged."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return (
            _reader(
                _response(
                    200,
                    {
                        "choices": [
                            {"message": {"role": "assistant", "content": "reply"}},
                        ],
                        "usage": {
                            "prompt_tokens": _INPUT_TOKENS,
                            "completion_tokens": _OUTPUT_TOKENS,
                            "total_tokens": _PROVIDER_TOTAL_TOKENS,
                            "prompt_tokens_details": {"cached_tokens": 3},
                        },
                        "timings": {"prompt_n": 8, "predicted_n": 4},
                    },
                ),
            ),
            _Writer(),
        )

    monkeypatch.setattr(asyncio, "open_connection", connection)

    turn = asyncio.run(
        _interaction().send(
            _message(ConversationMessageRole.USER),
            maximum_output_tokens=3,
        ),
    )

    assert turn.content == "reply"
    assert turn.usage is not None
    assert turn.usage.input_tokens == _INPUT_TOKENS
    assert turn.usage.output_tokens == _OUTPUT_TOKENS
    assert turn.usage.total_tokens == _PROVIDER_TOTAL_TOKENS


def test_interaction_allows_partial_pinned_usage_without_estimation() -> None:
    """Absent provider counts remain absent rather than becoming derived values."""
    usage = llama_cpp._model_usage(  # noqa: SLF001
        {"usage": {"prompt_tokens": _INPUT_TOKENS}},
    )

    assert usage is not None
    assert usage.input_tokens == _INPUT_TOKENS
    assert usage.output_tokens is None
    assert usage.total_tokens is None


@pytest.mark.parametrize(
    "response",
    [
        {"usage": None},
        {"usage": {}},
        {"usage": {"prompt_tokens": 0}},
    ],
)
def test_interaction_keeps_absent_or_zero_usage_honest(
    response: dict[str, object],
) -> None:
    """Missing usage remains absent while a reported zero stays a reported count."""
    usage = llama_cpp._model_usage(response)  # noqa: SLF001

    if response["usage"] == {"prompt_tokens": 0}:
        assert usage is not None
        assert usage.input_tokens == 0
    else:
        assert usage is None


@pytest.mark.parametrize(
    "response",
    [
        {"usage": []},
        {"usage": {"prompt_tokens": -1}},
        {"usage": {"completion_tokens": True}},
        {"usage": {"total_tokens": "12"}},
    ],
)
def test_interaction_rejects_malformed_usage(
    response: dict[str, object],
) -> None:
    """Malformed provider usage is a provider-local successful-response error."""
    with pytest.raises(LlamaCppResponseError, match="usage"):
        llama_cpp._model_usage(response)  # noqa: SLF001


def test_interaction_rejects_malformed_successful_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A malformed success payload cannot become a final ModelResponse."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return _reader(_response(200, {"choices": []})), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppResponseError, match="nonempty choices"):
        asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))


def test_interaction_preserves_non_success_http_as_provider_local_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Provider HTTP error payloads do not form Messages or generic errors."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return (
            _reader(
                _response(_HTTP_BAD_REQUEST, {"error": {"message": "bad model"}}),
            ),
            _Writer(),
        )

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppHttpError, match="HTTP 400: bad model") as raised:
        asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))
    assert raised.value.status == _HTTP_BAD_REQUEST


def test_interaction_rejects_continuation_for_stateless_provider() -> None:
    """The stateless provider does not silently ignore continuation."""
    with pytest.raises(ValueError, match="does not support continuation"):
        asyncio.run(
            _interaction().send(
                _message(ConversationMessageRole.USER),
                conversation=ConversationRef(InteractionSource("qwen"), "thread"),
            ),
        )


@pytest.mark.parametrize(
    "endpoint",
    [
        "https://127.0.0.1:8080",
        "relative",
        "http://127.0.0.1:8080/api",
        "http://:bad",
        "http://127.0.0.1:99999",
    ],
)
def test_interaction_rejects_endpoint_shapes_outside_its_narrow_origin_contract(
    endpoint: str,
) -> None:
    """Provider adaptation accepts only the LlamaCppServer-style HTTP origin."""
    with pytest.raises(ValueError, match="endpoint"):
        LlamaCppInteraction(
            endpoint=endpoint,
            model="qwen-local",
            source=InteractionSource("qwen"),
        )


def test_interaction_rejects_blank_model_name() -> None:
    """The explicit served-model request field cannot be blank."""
    with pytest.raises(ValueError, match="model name"):
        LlamaCppInteraction(
            endpoint="http://127.0.0.1:8080",
            model=" ",
            source=InteractionSource("qwen"),
        )


def test_interaction_uses_configured_model_and_source_on_real_request_path(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A compatible model identity changes the actual request and response source."""
    writer = _Writer()

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return (
            _reader(
                _response(
                    200,
                    {
                        "choices": [
                            {
                                "message": {
                                    "role": "assistant",
                                    "content": "DeepSeek reply",
                                },
                            },
                        ],
                    },
                ),
            ),
            writer,
        )

    monkeypatch.setattr(asyncio, "open_connection", connection)
    interaction = LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model="deepseek-local",
        source=InteractionSource("deepseek"),
    )

    turn = asyncio.run(interaction.send(_message(ConversationMessageRole.USER)))

    _, _, body = writer.request.partition(b"\r\n\r\n")
    assert json.loads(body)["model"] == "deepseek-local"
    assert turn.source == InteractionSource("deepseek")


def test_interaction_preserves_transport_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Socket failures remain provider-local transport failures."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        raise OSError(_OFFLINE)

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppTransportError, match="Could not communicate"):
        asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))


@pytest.mark.parametrize(
    ("response", "match"),
    [
        (b"", "complete HTTP headers"),
        (b"HTTP/1.1 nope\r\n\r\n{}", "invalid HTTP status"),
        (_response(200, []), "JSON object"),
        (b"HTTP/1.1 200 Test\r\n\r\nnot-json", "valid JSON"),
    ],
)
def test_interaction_rejects_invalid_http_or_success_payload_shapes(
    monkeypatch: pytest.MonkeyPatch,
    response: bytes,
    match: str,
) -> None:
    """Malformed framing and successful payloads never form ModelResponses."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return _reader(response), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppResponseError, match=match):
        asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))


@pytest.mark.parametrize(
    ("response", "match"),
    [
        ({"choices": [None]}, "choice must be an object"),
        ({"choices": [{}]}, "message object"),
        (
            {"choices": [{"message": {"role": "user", "content": "x"}}]},
            "assistant role",
        ),
        (
            {"choices": [{"message": {"role": "assistant", "content": None}}]},
            "must be text",
        ),
    ],
)
def test_interaction_rejects_invalid_final_assistant_message_shapes(
    response: dict[str, object],
    match: str,
) -> None:
    """Only final textual assistant content is consumed from provider JSON."""
    with pytest.raises(LlamaCppResponseError, match=match):
        llama_cpp._final_assistant_content(response)  # noqa: SLF001


def test_provider_error_detail_falls_back_when_error_shape_is_not_usable() -> None:
    """Nonstandard provider error bodies retain bounded text rather than a DTO."""
    assert llama_cpp._error_detail(b"not-json") == "not-json"  # noqa: SLF001
    assert llama_cpp._error_detail(b'{"error":{}}') == '{"error":{}}'  # noqa: SLF001
    assert llama_cpp._error_detail(b"[]") == "[]"  # noqa: SLF001
    assert llama_cpp._error_detail(b'{"error":[]}') == '{"error":[]}'  # noqa: SLF001


def test_provider_helpers_reject_defensive_invalid_origin_and_empty_headers() -> None:
    """Private transport helpers retain malformed provider-local failures."""
    with pytest.raises(LlamaCppTransportError):
        asyncio.run(llama_cpp._post_chat_completion(urlsplit("http:///"), {}))  # noqa: SLF001

    async def read_empty_headers() -> None:
        with pytest.raises(LlamaCppResponseError, match="status line"):
            await llama_cpp._read_http_response(_reader(b"\r\n\r\n"))  # noqa: SLF001

    asyncio.run(read_empty_headers())


def test_interaction_reads_fragmented_content_length_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Header and body fragments are consumed by their declared HTTP framing."""
    writer = _Writer()
    deliveries: list[asyncio.Task[None]] = []
    response = _response(
        200,
        {"choices": [{"message": {"role": "assistant", "content": "fragmented"}}]},
        content_length=True,
    )

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        reader = asyncio.StreamReader()

        async def deliver() -> None:
            for fragment in (response[:17], response[17:53], response[53:-5]):
                reader.feed_data(fragment)
                await asyncio.sleep(0)
            reader.feed_data(response[-5:])
            reader.feed_eof()

        deliveries.append(asyncio.create_task(deliver()))
        return reader, writer

    monkeypatch.setattr(asyncio, "open_connection", connection)

    turn = asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))

    assert turn.content == "fragmented"
    assert deliveries[0].done()


def test_interaction_reads_fragmented_chunked_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """HTTP chunk framing is decoded before llama.cpp JSON response parsing."""
    body = json.dumps(
        {"choices": [{"message": {"role": "assistant", "content": "chunked"}}]},
    ).encode()
    split = len(body) // 2
    chunked = (
        f"{split:X}\r\n".encode()
        + body[:split]
        + b"\r\n"
        + f"{len(body) - split:X}\r\n".encode()
        + body[split:]
        + b"\r\n0\r\n\r\n"
    )
    response = b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n\r\n" + chunked
    deliveries: list[asyncio.Task[None]] = []

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        reader = asyncio.StreamReader()

        async def deliver() -> None:
            fragments = [
                response[index : index + 7] for index in range(0, len(response), 7)
            ]
            for fragment in fragments[:-1]:
                reader.feed_data(fragment)
                await asyncio.sleep(0)
            reader.feed_data(fragments[-1])
            reader.feed_eof()

        deliveries.append(asyncio.create_task(deliver()))
        return reader, _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    turn = asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))

    assert turn.content == "chunked"
    assert deliveries[0].done()


@pytest.mark.parametrize(
    ("response", "match"),
    [
        (b"HTTP/1.1 200 Test\r\nContent-Length: nope\r\n\r\n", "Content-Length"),
        (b"HTTP/1.1 200 Test\r\nContent-Length: 4\r\n\r\n{}", "ended before"),
        (
            b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n\r\nnope\r\n",
            "chunk size",
        ),
        (
            b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n\r\n3\r\nab",
            "chunk body",
        ),
    ],
)
def test_interaction_rejects_malformed_http_body_framing(
    monkeypatch: pytest.MonkeyPatch,
    response: bytes,
    match: str,
) -> None:
    """Malformed provider HTTP framing remains a provider-local response failure."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return _reader(response), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppResponseError, match=match):
        asyncio.run(_interaction().send(_message(ConversationMessageRole.USER)))


async def _read_framed_response(
    response: bytes,
    *,
    limit: int = 65_536,
) -> tuple[int, bytes]:
    """Run the private framing reader with an EOF-delimited test socket."""
    reader = asyncio.StreamReader(limit=limit)
    reader.feed_data(response)
    reader.feed_eof()
    return await llama_cpp._read_http_response(reader)  # noqa: SLF001


@pytest.mark.parametrize(
    ("response", "match"),
    [
        (b"HTTP/1.1 200 Test\r\nBroken\r\n\r\n", "invalid HTTP header"),
        (b"HTTP/1.1 200 Test\r\n\xff: value\r\n\r\n", "non-text HTTP header"),
        (
            b"HTTP/1.1 200 Test\r\nContent-Length: 0\r\nContent-Length: 0\r\n\r\n",
            "repeated",
        ),
        (
            (
                b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n"
                b"Content-Length: 0\r\n\r\n"
            ),
            "conflicting",
        ),
        (
            b"HTTP/1.1 200 Test\r\nTransfer-Encoding: gzip\r\n\r\n",
            "unsupported",
        ),
        (
            (
                b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n\r\n"
                b"1\r\naZZ0\r\n\r\n"
            ),
            "chunk delimiter",
        ),
    ],
)
def test_private_http_reader_rejects_invalid_header_or_framing(
    response: bytes,
    match: str,
) -> None:
    """Header and framing ambiguity stay inside the provider's private transport."""
    with pytest.raises(LlamaCppResponseError, match=match):
        asyncio.run(_read_framed_response(response))


def test_private_http_reader_accepts_chunk_extensions_and_trailers() -> None:
    """Chunk extensions and trailers do not leak framing into the JSON body."""
    response = (
        b"HTTP/1.1 200 Test\r\nTransfer-Encoding: chunked\r\n\r\n"
        b"1;extension=value\r\na\r\n0\r\nX-Trailer: value\r\n\r\n"
    )

    assert asyncio.run(_read_framed_response(response)) == (200, b"a")


def test_private_http_reader_rejects_header_limit_overrun() -> None:
    """Oversized response headers fail as provider-local framing errors."""
    with pytest.raises(LlamaCppResponseError, match="headers exceeded"):
        asyncio.run(_read_framed_response(b"HTTP/1.1 200 Test\r\n\r\n", limit=1))


async def _read_http_line_with_limit() -> bytes:
    """Exercise bounded chunk-line reading without a complete response."""
    reader = asyncio.StreamReader(limit=1)
    reader.feed_data(b"abcdef\r\n")
    reader.feed_eof()
    return await llama_cpp._read_http_line(reader, "chunk size")  # noqa: SLF001


def test_private_http_reader_rejects_chunk_line_limit_overrun() -> None:
    """Oversized chunk framing remains a bounded provider-local failure."""
    with pytest.raises(LlamaCppResponseError, match="chunk size exceeded"):
        asyncio.run(_read_http_line_with_limit())


async def _read_incomplete_http_line() -> bytes:
    """Exercise premature EOF while reading private HTTP framing."""
    reader = asyncio.StreamReader()
    reader.feed_data(b"unfinished")
    reader.feed_eof()
    return await llama_cpp._read_http_line(reader, "chunk trailer")  # noqa: SLF001


def test_private_http_reader_rejects_incomplete_chunk_line() -> None:
    """Premature EOF in chunk framing cannot become a provider body."""
    with pytest.raises(LlamaCppResponseError, match="ended during HTTP chunk trailer"):
        asyncio.run(_read_incomplete_http_line())
