# Copyright (c) 2026
"""One-turn llama.cpp implementation of the interaction protocol."""

from __future__ import annotations

import asyncio
import json
from contextlib import suppress
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

from devtools.core.time import Timestamp
from devtools.models.interaction import (
    InteractionSource,
    ModelInteractionId,
    ModelInteractionObservation,
    ModelRequest,
    ModelResponse,
    ModelTermination,
    ModelToolCall,
    ModelToolDefinition,
    ModelUsage,
)
from devtools.models.interaction.providers.llama_cpp_errors import (
    LlamaCppHttpError,
    LlamaCppResponseError,
    LlamaCppTransportError,
)
from devtools.models.interaction.providers.llama_cpp_request_settings import (
    LlamaCppRequestSettings,
)

if TYPE_CHECKING:
    from urllib.parse import SplitResult

    from devtools.models.interaction import ModelInteractionObserver


_CHAT_COMPLETIONS_PATH = "/v1/chat/completions"
_MAX_ERROR_DETAIL_BYTES = 1_024
_SUCCESS_STATUS_START = 200
_SUCCESS_STATUS_END = 300
_HTTP_STATUS_PART_COUNT = 3
_HEADER_DELIMITER = b"\r\n\r\n"
_LINE_DELIMITER = b"\r\n"
_CHUNKED_TRANSFER_ENCODING = "chunked"


class LlamaCppInteraction:
    """Adapt one non-streaming llama.cpp chat interaction to ModelInteraction."""

    def __init__(
        self,
        *,
        endpoint: str,
        model: str,
        source: InteractionSource,
        observer: ModelInteractionObserver | None = None,
    ) -> None:
        """Configure one endpoint, served model name, and output source."""
        self._endpoint = _parse_endpoint(endpoint)
        if not model.strip():
            msg = "llama.cpp served model name cannot be blank."
            raise ValueError(msg)
        self._model = model
        self._source = source
        self._observer = observer

    @property
    def source(self) -> InteractionSource:
        """Return the stable source represented by this adapter."""
        return self._source

    async def send(
        self,
        request: ModelRequest,
    ) -> ModelResponse:
        """Send one Prompt through llama.cpp and return final assistant text."""
        started_at = Timestamp.now()
        interaction_id = ModelInteractionId.new()
        if request.conversation is not None:
            msg = "The stateless llama.cpp interaction does not support continuation."
            raise ValueError(msg)
        provider_settings = request.provider_settings
        if provider_settings is not None and not isinstance(
            provider_settings,
            LlamaCppRequestSettings,
        ):
            msg = "llama.cpp interaction received settings for another provider."
            raise ValueError(msg)

        payload: dict[str, object] = {
            "model": self._model,
            "messages": [
                {
                    "role": _provider_role(request.prompt.role),
                    "content": request.prompt.content,
                },
            ],
            "stream": False,
        }
        if request.settings.maximum_output_tokens is not None:
            payload["max_tokens"] = request.settings.maximum_output_tokens
        if request.settings.thinking_enabled is not None:
            payload["chat_template_kwargs"] = {
                "enable_thinking": request.settings.thinking_enabled,
            }
        if request.tools:
            payload["tools"] = [
                _provider_tool_definition(tool) for tool in request.tools
            ]
        response = await _post_chat_completion(self._endpoint, payload)
        content = _final_assistant_content(response)
        model_response = ModelResponse(
            content=content,
            reasoning_content=_model_reasoning_content(response),
            source=self.source,
            termination=_model_termination(response),
            usage=_model_usage(response),
            tool_calls=_model_tool_calls(response),
        )
        observer = self._observer
        if observer is not None:
            observer.interaction_completed(
                ModelInteractionObservation(
                    interaction_id=interaction_id,
                    provider="llama.cpp",
                    source=self.source,
                    request=request,
                    response=model_response,
                    started_at=started_at,
                    completed_at=Timestamp.now(),
                    provider_response_id=_optional_provider_text(response, "id"),
                    provider_model=_optional_provider_text(response, "model"),
                ),
            )
        return model_response


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
        msg = "llama.cpp endpoint must be an absolute HTTP origin without a path."
        raise ValueError(msg)
    try:
        _ = parsed.port
    except ValueError as error:
        msg = "llama.cpp endpoint has an invalid port."
        raise ValueError(msg) from error
    return parsed


def _provider_role(role: str) -> str:
    """Map the existing conversational role to its llama.cpp chat equivalent."""
    return role


async def _post_chat_completion(
    endpoint: SplitResult,
    payload: dict[str, object],
) -> dict[str, object]:
    """Perform one narrow non-streaming JSON chat request over HTTP."""
    host = endpoint.hostname
    if host is None:  # Defensive after _parse_endpoint validation.
        raise LlamaCppTransportError
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
        raise LlamaCppTransportError from error
    finally:
        if writer is not None:  # pragma: no branch - normal connection returns writer
            writer.close()
            with suppress(OSError):
                await writer.wait_closed()

    if not _SUCCESS_STATUS_START <= status < _SUCCESS_STATUS_END:
        raise LlamaCppHttpError(status, _error_detail(body_bytes))
    try:
        decoded = json.loads(body_bytes)
    except json.JSONDecodeError as error:
        msg = "llama.cpp successful response was not valid JSON."
        raise LlamaCppResponseError(msg) from error
    if not isinstance(decoded, dict):
        msg = "llama.cpp successful response must be a JSON object."
        raise LlamaCppResponseError(msg)
    return decoded


async def _read_http_response(reader: asyncio.StreamReader) -> tuple[int, bytes]:
    """Read one narrowly framed HTTP/1.1 response from llama.cpp."""
    try:
        raw_headers = await reader.readuntil(_HEADER_DELIMITER)
    except asyncio.IncompleteReadError as error:
        msg = "llama.cpp response did not contain complete HTTP headers."
        raise LlamaCppResponseError(msg) from error
    except asyncio.LimitOverrunError as error:
        msg = "llama.cpp response headers exceeded the supported reader limit."
        raise LlamaCppResponseError(msg) from error

    status, headers = _parse_http_headers(raw_headers[: -len(_HEADER_DELIMITER)])
    transfer_encoding = headers.get("transfer-encoding")
    content_length = headers.get("content-length")
    if transfer_encoding is not None and content_length is not None:
        msg = "llama.cpp response used conflicting HTTP body framing."
        raise LlamaCppResponseError(msg)
    if transfer_encoding is not None:
        if transfer_encoding.lower() != _CHUNKED_TRANSFER_ENCODING:
            msg = "llama.cpp response used unsupported HTTP transfer encoding."
            raise LlamaCppResponseError(msg)
        return status, await _read_chunked_body(reader)
    if content_length is not None:
        return status, await _read_content_length_body(reader, content_length)
    return status, await reader.read()


def _parse_http_headers(header_block: bytes) -> tuple[int, dict[str, str]]:
    """Parse only the HTTP status and headers required for response framing."""
    lines = header_block.split(_LINE_DELIMITER)
    if not lines or not lines[0]:
        msg = "llama.cpp response did not contain an HTTP status line."
        raise LlamaCppResponseError(msg)
    parts = lines[0].split()
    if len(parts) != _HTTP_STATUS_PART_COUNT or not parts[1].isdigit():
        msg = "llama.cpp response had an invalid HTTP status line."
        raise LlamaCppResponseError(msg)
    headers: dict[str, str] = {}
    for line in lines[1:]:
        name, separator, value = line.partition(b":")
        if not separator or not name:
            msg = "llama.cpp response had an invalid HTTP header."
            raise LlamaCppResponseError(msg)
        try:
            normalized_name = name.decode("ascii").lower()
            decoded_value = value.decode("latin-1").strip()
        except UnicodeDecodeError as error:
            msg = "llama.cpp response had a non-text HTTP header."
            raise LlamaCppResponseError(msg) from error
        if normalized_name in headers:
            msg = "llama.cpp response repeated an HTTP framing header."
            raise LlamaCppResponseError(msg)
        headers[normalized_name] = decoded_value
    return int(parts[1]), headers


async def _read_content_length_body(
    reader: asyncio.StreamReader,
    content_length: str,
) -> bytes:
    """Read exactly the provider body bytes declared by Content-Length."""
    if not content_length.isascii() or not content_length.isdecimal():
        msg = "llama.cpp response had an invalid Content-Length."
        raise LlamaCppResponseError(msg)
    try:
        return await reader.readexactly(int(content_length))
    except asyncio.IncompleteReadError as error:
        msg = "llama.cpp response ended before its Content-Length body completed."
        raise LlamaCppResponseError(msg) from error


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
            raise LlamaCppResponseError(msg)
        size = int(size_text, 16)
        if size == 0:
            await _consume_chunk_trailers(reader)
            return b"".join(chunks)
        try:
            chunks.append(await reader.readexactly(size))
            delimiter = await reader.readexactly(len(_LINE_DELIMITER))
        except asyncio.IncompleteReadError as error:
            msg = "llama.cpp response ended during an HTTP chunk body."
            raise LlamaCppResponseError(msg) from error
        if delimiter != _LINE_DELIMITER:
            msg = "llama.cpp response had an invalid HTTP chunk delimiter."
            raise LlamaCppResponseError(msg)


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
        raise LlamaCppResponseError(msg) from error
    except asyncio.LimitOverrunError as error:
        msg = (
            "llama.cpp response HTTP "
            f"{description} exceeded the supported reader limit."
        )
        raise LlamaCppResponseError(msg) from error


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


def _optional_provider_text(response: dict[str, object], field: str) -> str | None:
    """Read optional provider identity text without retaining raw response data."""
    value = response.get(field)
    return value if isinstance(value, str) else None


def _provider_tool_definition(tool: ModelToolDefinition) -> dict[str, object]:
    """Translate one normalized Tool definition at the llama.cpp boundary."""
    parameters = json.loads(tool.input_schema_json)
    return {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": parameters,
        },
    }


def _model_tool_calls(response: dict[str, object]) -> tuple[ModelToolCall, ...]:
    """Map pinned native function calls without admitting or executing them."""
    choice = _first_choice(response)
    message = choice.get("message")
    if not isinstance(message, dict):
        msg = "llama.cpp successful response choice must contain a message object."
        raise LlamaCppResponseError(msg)
    raw_calls = message.get("tool_calls")
    if raw_calls is None:
        return ()
    if not isinstance(raw_calls, list):
        msg = "llama.cpp successful response tool_calls must be a list."
        raise LlamaCppResponseError(msg)
    return tuple(_model_tool_call(raw_call) for raw_call in raw_calls)


def _model_tool_call(raw_call: object) -> ModelToolCall:
    """Map one pinned llama.cpp native function-call object honestly."""
    if not isinstance(raw_call, dict):
        msg = "llama.cpp successful response Tool call must be an object."
        raise LlamaCppResponseError(msg)
    call_type = raw_call.get("type")
    if call_type != "function":
        msg = "llama.cpp successful response Tool call type must be function."
        raise LlamaCppResponseError(msg)
    function = raw_call.get("function")
    if not isinstance(function, dict):
        msg = "llama.cpp successful response Tool call must contain a function object."
        raise LlamaCppResponseError(msg)
    name = function.get("name")
    arguments = function.get("arguments")
    if not isinstance(name, str) or not isinstance(arguments, str):
        msg = "llama.cpp successful response Tool call name and arguments must be text."
        raise LlamaCppResponseError(msg)
    call_id = raw_call.get("id")
    if call_id is not None and not isinstance(call_id, str):
        msg = "llama.cpp successful response Tool call ID must be text."
        raise LlamaCppResponseError(msg)
    try:
        return ModelToolCall(
            name=name,
            arguments_json=arguments,
            provider_call_id=call_id,
        )
    except (TypeError, ValueError) as error:
        raise LlamaCppResponseError(str(error)) from error


def _first_choice(response: dict[str, object]) -> dict[str, object]:
    """Return the validated selected provider choice shared by response fields."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "llama.cpp successful response must contain a nonempty choices list."
        raise LlamaCppResponseError(msg)
    choice = choices[0]
    if not isinstance(choice, dict):
        msg = "llama.cpp successful response choice must be an object."
        raise LlamaCppResponseError(msg)
    return choice


def _final_assistant_content(response: dict[str, object]) -> str:
    """Extract the minimum validated final-assistant subset from llama.cpp."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "llama.cpp successful response must contain a nonempty choices list."
        raise LlamaCppResponseError(msg)
    choice = choices[0]
    if not isinstance(choice, dict):
        msg = "llama.cpp successful response choice must be an object."
        raise LlamaCppResponseError(msg)
    message = choice.get("message")
    if not isinstance(message, dict):
        msg = "llama.cpp successful response choice must contain a message object."
        raise LlamaCppResponseError(msg)
    if message.get("role") != "assistant":
        msg = "llama.cpp successful response message must have assistant role."
        raise LlamaCppResponseError(msg)
    content = message.get("content")
    if not isinstance(content, str):
        msg = "llama.cpp successful response assistant content must be text."
        raise LlamaCppResponseError(msg)
    return content


def _model_usage(response: dict[str, object]) -> ModelUsage | None:
    """Map the pinned llama.cpp ``usage`` object without retaining raw payloads."""
    raw_usage = response.get("usage")
    if raw_usage is None:
        return None
    if not isinstance(raw_usage, dict):
        msg = "llama.cpp successful response usage must be an object."
        raise LlamaCppResponseError(msg)
    usage = ModelUsage(
        input_tokens=_usage_token_count(raw_usage, "prompt_tokens"),
        output_tokens=_usage_token_count(raw_usage, "completion_tokens"),
        total_tokens=_usage_token_count(raw_usage, "total_tokens"),
    )
    return usage if any(
        value is not None
        for value in (usage.input_tokens, usage.output_tokens, usage.total_tokens)
    ) else None


def _model_termination(response: dict[str, object]) -> ModelTermination | None:
    """Map the pinned llama.cpp completion reason without retaining provider data."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "llama.cpp successful response must contain a nonempty choices list."
        raise LlamaCppResponseError(msg)
    choice = choices[0]
    if not isinstance(choice, dict):
        msg = "llama.cpp successful response choice must be an object."
        raise LlamaCppResponseError(msg)
    finish_reason = choice.get("finish_reason")
    if finish_reason is None:
        return None
    if not isinstance(finish_reason, str):
        msg = "llama.cpp successful response finish_reason must be text."
        raise LlamaCppResponseError(msg)
    try:
        return {
            "stop": ModelTermination.NORMAL_STOP,
            "length": ModelTermination.OUTPUT_LIMIT,
            "tool_calls": ModelTermination.TOOL_CALL,
        }[finish_reason]
    except KeyError as error:
        msg = "llama.cpp successful response finish_reason is not supported."
        raise LlamaCppResponseError(msg) from error


def _model_reasoning_content(response: dict[str, object]) -> str | None:
    """Map separately returned llama.cpp reasoning without altering final content."""
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        msg = "llama.cpp successful response must contain a nonempty choices list."
        raise LlamaCppResponseError(msg)
    choice = choices[0]
    if not isinstance(choice, dict):
        msg = "llama.cpp successful response choice must be an object."
        raise LlamaCppResponseError(msg)
    message = choice.get("message")
    if not isinstance(message, dict):
        msg = "llama.cpp successful response choice must contain a message object."
        raise LlamaCppResponseError(msg)
    reasoning_content = message.get("reasoning_content")
    if reasoning_content is None:
        return None
    if not isinstance(reasoning_content, str):
        msg = "llama.cpp successful response reasoning_content must be text."
        raise LlamaCppResponseError(msg)
    return reasoning_content


def _usage_token_count(usage: dict[object, object], field: str) -> int | None:
    """Validate one optional integer count from llama.cpp's standard usage object."""
    value = usage.get(field)
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        msg = (
            "llama.cpp successful response usage "
            f"{field} must be non-negative integer."
        )
        raise LlamaCppResponseError(msg)
    return value
