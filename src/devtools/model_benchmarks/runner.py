# Copyright (c) 2026
"""One-run streamed vLLM benchmark execution."""
# ruff: noqa: C901, EM101, PLR0915, TRY003, TRY004

from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from devtools.model_benchmarks.models import (
    BenchmarkCase,
    ModelBenchmarkResult,
    VLLMBenchmarkServingSnapshot,
)
from devtools.time import Duration, Stopwatch, Timestamp

if TYPE_CHECKING:
    from collections.abc import AsyncIterator

    from devtools.model_serving.vllm import VLLMServer


_DEFAULT_REQUEST_TIMEOUT = Duration.minutes(2)
_HTTP_OK = 200
_HTTP_STATUS_PARTS = 2
_MAX_ERROR_BODY_BYTES = 4_096


async def run_vllm_benchmark(
    *,
    server: VLLMServer,
    case: BenchmarkCase,
    request_timeout: Duration = _DEFAULT_REQUEST_TIMEOUT,
) -> ModelBenchmarkResult:
    """Run one streamed benchmark against an already-ready vLLM server.

    The request is attempted exactly once. TTFT ends at the first non-empty
    assistant-content delta; total duration ends at the terminal ``[DONE]``.
    """
    started_at = Timestamp.now()
    stopwatch = Stopwatch()
    response_parts: list[str] = []
    ttft: Duration | None = None
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    finish_reason: str | None = None

    async for event in _stream_vllm_chat(
        endpoint=server.endpoint,
        model=server.config.served_model_name,
        case=case,
        request_timeout=request_timeout,
    ):
        usage = event.get("usage")
        if isinstance(usage, dict):
            prompt_tokens = _optional_token_count(usage.get("prompt_tokens"))
            completion_tokens = _optional_token_count(usage.get("completion_tokens"))

        choices = event.get("choices")
        if not isinstance(choices, list) or not choices:
            continue
        choice = choices[0]
        if not isinstance(choice, dict):
            raise ValueError("vLLM benchmark stream choice was not an object.")

        candidate_finish_reason = choice.get("finish_reason")
        if candidate_finish_reason is not None:
            if not isinstance(candidate_finish_reason, str):
                raise ValueError("vLLM benchmark finish reason was not text.")
            finish_reason = candidate_finish_reason

        delta = choice.get("delta")
        if not isinstance(delta, dict):
            continue
        content = delta.get("content")
        if content is None:
            continue
        if not isinstance(content, str):
            raise ValueError("vLLM benchmark content delta was not text.")
        if content and ttft is None:
            ttft = stopwatch.elapsed
        response_parts.append(content)

    total_duration = stopwatch.stop()
    response_text = "".join(response_parts)
    expectation_met = (
        response_text == case.expected_response
        if case.expected_response is not None
        else None
    )
    completion_tokens_per_second = _completion_throughput(
        completion_tokens=completion_tokens,
        total_duration=total_duration,
    )
    return ModelBenchmarkResult(
        started_at=started_at,
        case=case,
        serving=VLLMBenchmarkServingSnapshot.from_server(server),
        response_text=response_text,
        ttft=ttft,
        total_duration=total_duration,
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        completion_tokens_per_second=completion_tokens_per_second,
        finish_reason=finish_reason,
        expectation_met=expectation_met,
    )


async def _stream_vllm_chat(
    *,
    endpoint: str,
    model: str,
    case: BenchmarkCase,
    request_timeout: Duration,
) -> AsyncIterator[dict[str, object]]:
    """Yield JSON events from the bounded vLLM OpenAI-compatible SSE stream."""
    parsed = urlsplit(endpoint)
    host = parsed.hostname
    if host is None:
        msg = "vLLM benchmark endpoint must contain a host."
        raise ValueError(msg)

    port = parsed.port or 80
    request_body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": case.prompt}],
            "max_tokens": case.max_tokens,
            "temperature": case.temperature,
            "stream": True,
            "stream_options": {"include_usage": True},
        },
        separators=(",", ":"),
    ).encode()
    request = (
        "POST /v1/chat/completions HTTP/1.1\r\n"
        f"Host: {host}\r\n"
        "Content-Type: application/json\r\n"
        "Accept: text/event-stream\r\n"
        "Connection: close\r\n"
        f"Content-Length: {len(request_body)}\r\n\r\n"
    ).encode() + request_body

    try:
        async with asyncio.timeout(request_timeout.total_seconds):
            reader, writer = await asyncio.open_connection(host, port)
            try:
                writer.write(request)
                await writer.drain()
                status = await _read_http_status(reader)
                headers = await _read_http_headers(reader)
                if status != _HTTP_OK:
                    diagnostic = await reader.read(_MAX_ERROR_BODY_BYTES)
                    msg = f"vLLM benchmark request returned HTTP {status}."
                    detail = diagnostic.decode("utf-8", errors="replace").strip()
                    raise ValueError(f"{msg} {detail}" if detail else msg)

                done = False
                async for line in _iter_sse_lines(
                    _iter_http_body_chunks(reader, headers),
                ):
                    decoded = line.decode("utf-8", errors="replace").rstrip("\r\n")
                    if not decoded or decoded.startswith((":", "event:")):
                        continue
                    if not decoded.startswith("data:"):
                        msg = "vLLM benchmark stream contained an invalid SSE field."
                        raise ValueError(msg)
                    data = decoded[5:].lstrip()
                    if data == "[DONE]":
                        done = True
                        break
                    try:
                        event = json.loads(data)
                    except json.JSONDecodeError as error:
                        msg = "vLLM benchmark stream contained invalid JSON."
                        raise ValueError(msg) from error
                    if not isinstance(event, dict):
                        msg = "vLLM benchmark stream event was not an object."
                        raise ValueError(msg)
                    yield event

                if not done:
                    msg = (
                        "vLLM benchmark stream ended before its terminal [DONE] event."
                    )
                    raise ValueError(msg)
            finally:
                writer.close()
                await writer.wait_closed()
    except TimeoutError as error:
        msg = (
            f"vLLM benchmark request exceeded {request_timeout.total_seconds} seconds."
        )
        raise TimeoutError(msg) from error


async def _read_http_status(reader: asyncio.StreamReader) -> int:
    """Read the HTTP status line for one benchmark request."""
    line = await reader.readline()
    parts = line.split()
    if len(parts) < _HTTP_STATUS_PARTS:
        msg = "vLLM benchmark response did not contain a valid HTTP status line."
        raise ValueError(msg)
    try:
        return int(parts[1])
    except ValueError as error:
        msg = "vLLM benchmark response status was not an integer."
        raise ValueError(msg) from error


async def _read_http_headers(reader: asyncio.StreamReader) -> dict[str, list[str]]:
    """Read HTTP headers needed to select the bounded response-body framing."""
    headers: dict[str, list[str]] = {}
    while True:
        line = await reader.readline()
        if not line or line in {b"\r\n", b"\n"}:
            return headers
        name, separator, value = line.partition(b":")
        if not separator:
            msg = "vLLM benchmark response contained an invalid HTTP header."
            raise ValueError(msg)
        header_name = name.decode("ascii", errors="strict").strip().lower()
        if not header_name:
            msg = "vLLM benchmark response contained an empty HTTP header name."
            raise ValueError(msg)
        headers.setdefault(header_name, []).append(
            value.decode("latin-1").strip(),
        )


def _uses_chunked_transfer_encoding(headers: dict[str, list[str]]) -> bool:
    """Return whether HTTP transfer framing uses a case-insensitive chunked token."""
    return any(
        token.strip().lower() == "chunked"
        for value in headers.get("transfer-encoding", [])
        for token in value.split(",")
    )


async def _iter_http_body_chunks(
    reader: asyncio.StreamReader,
    headers: dict[str, list[str]],
) -> AsyncIterator[bytes]:
    """Yield decoded HTTP body bytes without exposing transfer framing to SSE."""
    if not _uses_chunked_transfer_encoding(headers):
        while line := await reader.readline():
            yield line
        return

    while True:
        size_line = await reader.readline()
        if not size_line:
            msg = "vLLM benchmark chunked response ended before a chunk size."
            raise ValueError(msg)
        size_text = size_line.rstrip(b"\r\n").split(b";", maxsplit=1)[0]
        if not size_text:
            msg = "vLLM benchmark response contained an empty chunk size."
            raise ValueError(msg)
        if any(byte not in b"0123456789abcdefABCDEF" for byte in size_text):
            msg = "vLLM benchmark response contained an invalid chunk size."
            raise ValueError(msg)
        size = int(size_text, 16)
        if size == 0:
            await _consume_chunked_trailers(reader)
            return

        try:
            chunk = await reader.readexactly(size)
            terminator = await reader.readexactly(2)
        except asyncio.IncompleteReadError as error:
            msg = "vLLM benchmark response ended within an HTTP chunk."
            raise ValueError(msg) from error
        if terminator != b"\r\n":
            msg = "vLLM benchmark response contained an invalid chunk terminator."
            raise ValueError(msg)
        yield chunk


async def _consume_chunked_trailers(reader: asyncio.StreamReader) -> None:
    """Discard HTTP trailers after a terminal chunk without assigning semantics."""
    while True:
        line = await reader.readline()
        if not line:
            msg = "vLLM benchmark response ended before chunked trailers completed."
            raise ValueError(msg)
        if line in {b"\r\n", b"\n"}:
            return


async def _iter_sse_lines(chunks: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
    """Split decoded body bytes into SSE lines independently of HTTP chunks."""
    pending = bytearray()
    async for chunk in chunks:
        pending.extend(chunk)
        while (newline := pending.find(b"\n")) >= 0:
            line = bytes(pending[: newline + 1])
            del pending[: newline + 1]
            yield line
    if pending:
        yield bytes(pending)


def _optional_token_count(value: object) -> int | None:
    """Validate an optional provider-reported non-negative token count."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        msg = "vLLM benchmark usage token count was invalid."
        raise ValueError(msg)
    return value


def _completion_throughput(
    *,
    completion_tokens: int | None,
    total_duration: Duration,
) -> float | None:
    """Derive whole-request completion throughput from reported provider usage."""
    if completion_tokens is None or total_duration.total_seconds <= 0:
        return None
    return completion_tokens / total_duration.total_seconds
