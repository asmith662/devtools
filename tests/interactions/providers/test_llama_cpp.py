# Copyright (c) 2026
"""Deterministic tests for the llama.cpp Interaction adapter."""

from __future__ import annotations

import asyncio
import json
from urllib.parse import urlsplit

import pytest

from devtools.context import Message, MessageRole, MessageSource
from devtools.interactions import ConversationRef
from devtools.interactions.providers import (
    LlamaCppHttpError,
    LlamaCppInteraction,
    LlamaCppResponseError,
    LlamaCppTransportError,
    llama_cpp,
)

_HTTP_BAD_REQUEST = 400
_OFFLINE = "offline"


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


def _message(role: MessageRole, content: str = "Inspect the fixture.") -> Message:
    return Message.new(content, role=role, source=MessageSource("caller"))


def _interaction() -> LlamaCppInteraction:
    return LlamaCppInteraction(
        endpoint="http://127.0.0.1:8080",
        model="qwen-local",
        source=MessageSource("qwen"),
    )


@pytest.mark.parametrize("role", [MessageRole.USER, MessageRole.SYSTEM])
def test_interaction_maps_existing_message_roles_to_non_streaming_llama_request(
    monkeypatch: pytest.MonkeyPatch,
    role: MessageRole,
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
    assert turn.message.content == "Qwen reply"
    assert turn.message.role is MessageRole.ASSISTANT
    assert turn.message.source == MessageSource("qwen")
    assert turn.conversation is None
    assert writer.closed is True


def test_interaction_rejects_malformed_successful_response(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A malformed success payload cannot become a final InteractionTurn."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return _reader(_response(200, {"choices": []})), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppResponseError, match="nonempty choices"):
        asyncio.run(_interaction().send(_message(MessageRole.USER)))


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
        asyncio.run(_interaction().send(_message(MessageRole.USER)))
    assert raised.value.status == _HTTP_BAD_REQUEST


def test_interaction_rejects_continuation_for_stateless_provider() -> None:
    """The stateless provider does not silently ignore continuation."""
    with pytest.raises(ValueError, match="does not support continuation"):
        asyncio.run(
            _interaction().send(
                _message(MessageRole.USER),
                conversation=ConversationRef(MessageSource("qwen"), "thread"),
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
            source=MessageSource("qwen"),
        )


def test_interaction_rejects_blank_model_name() -> None:
    """The explicit served-model request field cannot be blank."""
    with pytest.raises(ValueError, match="model name"):
        LlamaCppInteraction(
            endpoint="http://127.0.0.1:8080",
            model=" ",
            source=MessageSource("qwen"),
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
        source=MessageSource("deepseek"),
    )

    turn = asyncio.run(interaction.send(_message(MessageRole.USER)))

    _, _, body = writer.request.partition(b"\r\n\r\n")
    assert json.loads(body)["model"] == "deepseek-local"
    assert turn.message.source == MessageSource("deepseek")


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
        asyncio.run(_interaction().send(_message(MessageRole.USER)))


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
    """Malformed framing and successful payloads never form InteractionTurns."""

    async def connection(
        _host: str,
        _port: int,
    ) -> tuple[asyncio.StreamReader, _Writer]:
        return _reader(response), _Writer()

    monkeypatch.setattr(asyncio, "open_connection", connection)

    with pytest.raises(LlamaCppResponseError, match=match):
        asyncio.run(_interaction().send(_message(MessageRole.USER)))


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

    turn = asyncio.run(_interaction().send(_message(MessageRole.USER)))

    assert turn.message.content == "fragmented"
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

    turn = asyncio.run(_interaction().send(_message(MessageRole.USER)))

    assert turn.message.content == "chunked"
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
        asyncio.run(_interaction().send(_message(MessageRole.USER)))


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
