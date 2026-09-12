# Copyright (c) 2026
"""One-turn llama.cpp/Qwen implementation of the existing Agent protocol."""

from __future__ import annotations

import asyncio
import json
from contextlib import suppress
from typing import TYPE_CHECKING, ClassVar
from urllib.parse import urlsplit

from devtools.agents import AgentTurn, ConversationRef
from devtools.context import Message, MessageRole, MessageSource
from devtools.qwen.errors import QwenHttpError, QwenResponseError, QwenTransportError

if TYPE_CHECKING:
    from urllib.parse import SplitResult


_CHAT_COMPLETIONS_PATH = "/v1/chat/completions"
_MAX_ERROR_DETAIL_BYTES = 1_024
_SUCCESS_STATUS_START = 200
_SUCCESS_STATUS_END = 300
_HTTP_STATUS_PART_COUNT = 3
_HEADER_DELIMITER = b"\r\n\r\n"
_LINE_DELIMITER = b"\r\n"
_CHUNKED_TRANSFER_ENCODING = "chunked"


class QwenAgent:
    """Adapt one non-streaming llama.cpp/Qwen chat interaction to Agent."""

    _SOURCE: ClassVar[MessageSource] = MessageSource("qwen")

    def __init__(self, *, endpoint: str, model: str) -> None:
        """Configure one explicit llama.cpp endpoint and served model name."""
        self._endpoint = _parse_endpoint(endpoint)
        if not model.strip():
            msg = "Qwen served model name cannot be blank."
            raise ValueError(msg)
        self._model = model

    @property
    def source(self) -> MessageSource:
        """Return the stable source represented by this adapter."""
        return self._SOURCE

    async def send(
        self,
        message: Message,
        *,
        conversation: ConversationRef | None = None,
    ) -> AgentTurn:
        """Send one Message through llama.cpp and return final assistant text."""
        if conversation is not None:
            msg = "The stateless Qwen adapter does not support continuation."
            raise ValueError(msg)

        response = await _post_chat_completion(
            self._endpoint,
            {
                "model": self._model,
                "messages": [
                    {
                        "role": _provider_role(message.role),
                        "content": message.content,
                    },
                ],
                "stream": False,
            },
        )
        content = _final_assistant_content(response)
        return AgentTurn(
            Message.new(
                content,
                role=MessageRole.ASSISTANT,
                source=self.source,
            ),
        )


def _parse_endpoint(endpoint: str) -> SplitResult:
    """Validate the narrow HTTP endpoint shape exposed by LlamaCppServer."""
    parsed = urlsplit(endpoint)
    if (
        parsed.scheme != "http"
        or parsed.hostname is None
        or parsed.path not in {"", "/"}
        or parsed.query
        or parsed.fragment
    ):
        msg = "Qwen endpoint must be an absolute HTTP origin without a path."
        raise ValueError(msg)
    try:
        _ = parsed.port
    except ValueError as error:
        msg = "Qwen endpoint has an invalid port."
        raise ValueError(msg) from error
    return parsed


def _provider_role(role: MessageRole) -> str:
    """Map the existing conversational role to its llama.cpp chat equivalent."""
    return role.value


async def _post_chat_completion(
    endpoint: SplitResult,
    payload: dict[str, object],
) -> dict[str, object]:
    """Perform one narrow non-streaming JSON chat request over HTTP."""
    host = endpoint.hostname
    if host is None:  # Defensive after _parse_endpoint validation.
        raise QwenTransportError
    port = endpoint.port or 80
    body = json.dumps(payload, separators=(",", ":")).encode()
    request = (
        f"POST {_CHAT_COMPLETIONS_PATH} HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/json\r\n"
        "Accept: application/json\r\n"
        "Connection: close\r\n"
        f"Content-Length: {len(body)}\r\n\r\n"
    ).encode() + body

    writer: asyncio.StreamWriter | None = None
    try:
        reader, writer = await asyncio.open_connection(host, port)
        writer.write(request)
        await writer.drain()
        status, body_bytes = await _read_http_response(reader)
    except OSError as error:
        raise QwenTransportError from error
    finally:
        if writer is not None:  # pragma: no branch - normal connection returns writer
            writer.close()
            with suppress(OSError):
                await writer.wait_closed()

    if not _SUCCESS_STATUS_START <= status < _SUCCESS_STATUS_END:
        raise QwenHttpError(status, _error_detail(body_bytes))
    try:
        decoded = json.loads(body_bytes)
    except json.JSONDecodeError as error:
        msg = "llama.cpp successful response was not valid JSON."
        raise QwenResponseError(msg) from error
    if not isinstance(decoded, dict):
        msg = "llama.cpp successful response must be a JSON object."
        raise QwenResponseError(msg)
    return decoded


async def _read_http_response(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    """Read one narrowly framed HTTP/1.1 response from llama.cpp."""
    try:
        raw_headers = await reader.readuntil(_HEADER_DELIMITER)
    except asyncio.IncompleteReadError as error:
        msg = "llama.cpp response did not contain complete HTTP headers."
        raise QwenResponseError(msg) from error
    except asyncio.LimitOverrunError as error:
        msg = "llama.cpp response headers exceeded the supported reader limit."
        raise QwenResponseError(msg) from error

    status, headers = _parse_http_headers(raw_headers[: -len(_HEADER_DELIMITER)])
    transfer_encoding = headers.get("transfer-encoding")
    content_length = headers.get("content-length")
    if transfer_encoding is not None and content_length is not None:
        msg = "llama.cpp response used conflicting HTTP body framing."
        raise QwenResponseError(msg)
    if transfer_encoding is not None:
        if transfer_encoding.lower() != _CHUNKED_TRANSFER_ENCODING:
            msg = "llama.cpp response used unsupported HTTP transfer encoding."
            raise QwenResponseError(msg)
        return status, await _read_chunked_body(reader)
    if content_length is not None:
        return status, await _read_content_length_body(reader, content_length)
    return status, await reader.read()


def _parse_http_headers(header_block: bytes) -> tuple[int, dict[str, str]]:
    """Parse only the HTTP status and headers required for response framing."""
    lines = header_block.split(_LINE_DELIMITER)
    if not lines or not lines[0]:
        msg = "llama.cpp response did not contain an HTTP status line."
        raise QwenResponseError(msg)
    parts = lines[0].split()
    if len(parts) != _HTTP_STATUS_PART_COUNT or not parts[1].isdigit():
        msg = "llama.cpp response had an invalid HTTP status line."
        raise QwenResponseError(msg)
    headers: dict[str, str] = {}
    for line in lines[1:]:
        name, separator, value = line.partition(b":")
        if not separator or not name:
            msg = "llama.cpp response had an invalid HTTP header."
            raise QwenResponseError(msg)
        try:
            normalized_name = name.decode("ascii").lower()
            decoded_value = value.decode("latin-1").strip()
        except UnicodeDecodeError as error:
            msg = "llama.cpp response had a non-text HTTP header."
            raise QwenResponseError(msg) from error
        if normalized_name in headers:
            msg = "llama.cpp response repeated an HTTP framing header."
            raise QwenResponseError(msg)
        headers[normalized_name] = decoded_value
    return int(parts[1]), headers


async def _read_content_length_body(
    reader: asyncio.StreamReader,
    content_length: str,
) -> bytes:
    """Read exactly the provider body bytes declared by Content-Length."""
    if not content_length.isascii() or not content_length.isdecimal():
        msg = "llama.cpp response had an invalid Content-Length."
        raise QwenResponseError(msg)
    try:
        return await reader.readexactly(int(content_length))
    except asyncio.IncompleteReadError as error:
        msg = "llama.cpp response ended before its Content-Length body completed."
        raise QwenResponseError(msg) from error


async def _read_chunked_body(reader: asyncio.StreamReader) -> bytes:
    """Decode HTTP chunked framing without enabling streaming model semantics."""
    chunks: list[bytes] = []
    while True:
        line = await _read_http_line(reader, "chunk size")
        size_text = line.split(b";", maxsplit=1)[0]
        if not size_text or any(
            character not in b"0123456789abcdefABCDEF" for character in size_text
        ):
            msg = "llama.cpp response had an invalid HTTP chunk size."
            raise QwenResponseError(msg)
        size = int(size_text, 16)
        if size == 0:
            await _consume_chunk_trailers(reader)
            return b"".join(chunks)
        try:
            chunks.append(await reader.readexactly(size))
            delimiter = await reader.readexactly(len(_LINE_DELIMITER))
        except asyncio.IncompleteReadError as error:
            msg = "llama.cpp response ended during an HTTP chunk body."
            raise QwenResponseError(msg) from error
        if delimiter != _LINE_DELIMITER:
            msg = "llama.cpp response had an invalid HTTP chunk delimiter."
            raise QwenResponseError(msg)


async def _consume_chunk_trailers(reader: asyncio.StreamReader) -> None:
    """Consume optional HTTP chunk trailers through their terminating blank line."""
    while await _read_http_line(reader, "chunk trailer"):
        pass


async def _read_http_line(reader: asyncio.StreamReader, description: str) -> bytes:
    """Read one CRLF-delimited framing line as provider-local response data."""
    try:
        return (await reader.readuntil(_LINE_DELIMITER))[: -len(_LINE_DELIMITER)]
    except asyncio.IncompleteReadError as error:
        msg = f"llama.cpp response ended during HTTP {description}."
        raise QwenResponseError(msg) from error
    except asyncio.LimitOverrunError as error:
        msg = (
            "llama.cpp response HTTP "
            f"{description} exceeded the supported reader limit."
        )
        raise QwenResponseError(msg) from error


def _error_detail(body: bytes) -> str:
    """Return bounded provider failure detail without defining an error DTO."""
    bounded = body[:_MAX_ERROR_DETAIL_BYTES]
    try:
        decoded = json.loads(bounded)
    except json.JSONDecodeError:
        return bounded.decode(errors="replace").strip() or "no provider detail"
    if isinstance(decoded, dict):
        error = decoded.get("error")
        if isinstance(error, dict):
            message = error.get("message")
            if isinstance(message, str):
                return message
    return bounded.decode(errors="replace").strip() or "no provider detail"


def _final_assistant_content(response: dict[str, object]) -> str:
    """Extract the minimum validated final-assistant subset from llama.cpp."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "llama.cpp successful response must contain a nonempty choices list."
        raise QwenResponseError(msg)
    choice = choices[0]
    if not isinstance(choice, dict):
        msg = "llama.cpp successful response choice must be an object."
        raise QwenResponseError(msg)
    message = choice.get("message")
    if not isinstance(message, dict):
        msg = "llama.cpp successful response choice must contain a message object."
        raise QwenResponseError(msg)
    if message.get("role") != MessageRole.ASSISTANT.value:
        msg = "llama.cpp successful response message must have assistant role."
        raise QwenResponseError(msg)
    content = message.get("content")
    if not isinstance(content, str):
        msg = "llama.cpp successful response assistant content must be text."
        raise QwenResponseError(msg)
    return content
