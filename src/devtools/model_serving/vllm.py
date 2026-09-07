# Copyright (c) 2026
"""Experimental concrete vLLM Docker serving lifecycle."""

from __future__ import annotations

import asyncio
import json
import re
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Self
from urllib.parse import urlsplit

from devtools.commands import Command, CommandExecutor, CommandResult
from devtools.model_serving.errors import (
    ServingReadinessTimeoutError,
    VLLMInspectionError,
    VLLMLaunchError,
    VLLMOwnershipError,
    VLLMStartupError,
    VLLMStopError,
)
from devtools.time import Duration, Timestamp

if TYPE_CHECKING:
    from devtools.model_serving.huggingface import HuggingFaceModelRef
    from devtools.paths import ResolvedPath


_CONTAINER_PORT = 8000
_CACHE_DESTINATION = "/root/.cache/huggingface"
_MANAGED_LABEL = "devtools.model_serving.managed"
_MANAGED_LABEL_VALUE = "true"
_POLL_INTERVAL_SECONDS = 0.25
_MAX_DIAGNOSTIC_BYTES = 4_096
_MAX_HOST_PORT = 65_535
_HTTP_OK = 200
_HTTP_STATUS_PARTS = 2
DEFAULT_READINESS_TIMEOUT = Duration.minutes(10)
_CONTAINER_ID = re.compile(r"^[0-9a-fA-F]{64}$")
_PROVIDER_LOG_TAIL_LINES = 200
_PROVIDER_LOG_TAIL_BYTES = 16 * 1024


@dataclass(frozen=True, slots=True)
class VLLMServingConfig:
    """Describe one reproducible vLLM Docker launch.

    All fields are vLLM- or Docker-specific.  This value is deliberately not a
    base class for future providers.
    """

    model: HuggingFaceModelRef
    image: str
    cache_root: ResolvedPath
    host_port: int
    served_model_name: str
    max_model_len: int
    gpu_memory_utilization: float
    max_num_seqs: int
    trust_remote_code: bool = False

    def __post_init__(self) -> None:
        """Validate structural launch constraints."""
        if not self.image.strip() or ":" not in self.image:
            msg = "vLLM image must include an explicit tag or digest."
            raise ValueError(msg)

        if not 1 <= self.host_port <= _MAX_HOST_PORT:
            msg = "Host port must be between 1 and 65535."
            raise ValueError(msg)

        if not self.served_model_name.strip():
            msg = "Served model name cannot be empty."
            raise ValueError(msg)

        if self.max_model_len <= 0:
            msg = "Maximum model length must be positive."
            raise ValueError(msg)

        if not 0 < self.gpu_memory_utilization <= 1:
            msg = "GPU memory utilization must be greater than 0 and at most 1."
            raise ValueError(msg)

        if self.max_num_seqs <= 0:
            msg = "Maximum number of sequences must be positive."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class VLLMServerStatus:
    """Describe the current bounded status of one owned vLLM container."""

    container_running: bool
    model_ready: bool


@dataclass(frozen=True, slots=True)
class _ContainerInspection:
    """Represent the fixed Docker state projection for one exact container."""

    running: bool
    ownership_label: str


class VLLMServer:
    """Represent one live, explicitly owned vLLM Docker serving instance."""

    __slots__ = (
        "_config",
        "_container_id",
        "_container_name",
        "_executor",
        "_started_at",
    )

    def __init__(
        self,
        *,
        config: VLLMServingConfig,
        container_id: str,
        container_name: str,
        executor: CommandExecutor,
        started_at: Timestamp,
    ) -> None:
        """Initialize a handle after Docker has returned an exact ID."""
        self._config = config
        self._container_id = container_id
        self._container_name = container_name
        self._executor = executor
        self._started_at = started_at

    @property
    def config(self) -> VLLMServingConfig:
        """Return the immutable launch configuration."""
        return self._config

    @property
    def container_id(self) -> str:
        """Return Docker's exact identifier for this owned container."""
        return self._container_id

    @property
    def cache_root(self) -> ResolvedPath:
        """Return the caller-visible Hugging Face cache root."""
        return self._config.cache_root

    @property
    def endpoint(self) -> str:
        """Return the loopback endpoint exposed by this container."""
        return f"http://127.0.0.1:{self._config.host_port}"

    @property
    def started_at(self) -> Timestamp:
        """Return when this handle was established."""
        return self._started_at

    @classmethod
    async def start(
        cls,
        *,
        config: VLLMServingConfig,
        executor: CommandExecutor,
        readiness_timeout: Duration = DEFAULT_READINESS_TIMEOUT,
    ) -> Self:
        """Launch one owned vLLM server and return only after model readiness.

        :raises VLLMLaunchError: If Docker rejects the detached launch.
        :raises ServingReadinessTimeoutError: If readiness does not arrive in time.
        :raises VLLMStartupError: If the container exits before readiness.
        """
        config.cache_root.value.mkdir(parents=True, exist_ok=True)
        container_name = _new_container_name()
        launch_result = await executor.execute(
            _build_launch_command(config, container_name),
        )
        if launch_result.failed:
            raise VLLMLaunchError(_launch_error_message(launch_result))

        container_id = _parse_container_id(launch_result)
        server = cls(
            config=config,
            container_id=container_id,
            container_name=container_name,
            executor=executor,
            started_at=Timestamp.now(),
        )

        try:
            await server.wait_ready(readiness_timeout=readiness_timeout)
        except BaseException as primary_error:
            await server._stop_after_unsuccessful_start(primary_error)
            raise

        return server

    async def wait_ready(
        self,
        *,
        readiness_timeout: Duration = DEFAULT_READINESS_TIMEOUT,
    ) -> None:
        """Wait until the owned container exposes the selected model."""
        if readiness_timeout.total_seconds <= 0:
            msg = "vLLM readiness timeout must be positive."
            raise ValueError(msg)

        try:
            async with asyncio.timeout(readiness_timeout.total_seconds):
                while True:
                    status = await self.status()
                    if status.model_ready:
                        return

                    if not status.container_running:
                        msg = (
                            "Owned vLLM container stopped before its model "
                            "became ready."
                        )
                        raise VLLMStartupError(
                            msg,
                            provider_log_tail=await _provider_log_tail(
                                self._executor,
                                self._container_id,
                            ),
                        )

                    await asyncio.sleep(_POLL_INTERVAL_SECONDS)
        except TimeoutError as error:
            msg = (
                "vLLM container did not expose the selected model within "
                f"{readiness_timeout.total_seconds} seconds."
            )
            raise ServingReadinessTimeoutError(msg) from error

    async def status(self) -> VLLMServerStatus:
        """Return whether the exact owned container is running and model-ready."""
        inspection = await _inspect_container(self._executor, self._container_id)
        if inspection is None:
            return VLLMServerStatus(container_running=False, model_ready=False)

        if not inspection.running:
            return VLLMServerStatus(container_running=False, model_ready=False)

        ready = await _probe_model_ready(self.endpoint, self._config.served_model_name)
        return VLLMServerStatus(container_running=True, model_ready=ready)

    async def stop(self) -> None:
        """Stop and remove only the exact Docker container owned by this handle."""
        inspection = await _inspect_container(self._executor, self._container_id)
        if inspection is None:
            return

        if inspection.ownership_label != _MANAGED_LABEL_VALUE:
            msg = "Refusing to stop a container without the expected ownership label."
            raise VLLMOwnershipError(msg)

        if inspection.running:
            result = await self._executor.execute(_stop_command(self._container_id))
            if result.failed:
                diagnostic = _diagnostic_text(result.stderr or result.stdout)
                msg = (
                    "Docker could not stop owned vLLM container "
                    f"{self._container_id!r}."
                )
                if diagnostic:
                    msg = f"{msg} {diagnostic}"
                raise VLLMStopError(msg)

        removal = await self._executor.execute(_remove_command(self._container_id))
        if removal.failed and not _is_exact_container_not_found(
            removal,
            self._container_id,
        ):
            diagnostic = _diagnostic_text(removal.stderr or removal.stdout)
            msg = (
                "Docker could not remove owned vLLM container "
                f"{self._container_id!r}."
            )
            if diagnostic:
                msg = f"{msg} {diagnostic}"
            raise VLLMStopError(msg)

    async def _stop_after_unsuccessful_start(
        self,
        primary_error: BaseException,
    ) -> None:
        """Attempt owned cleanup while preserving the primary start failure."""
        try:
            await self.stop()
        except BaseException as cleanup_error:  # noqa: BLE001
            primary_error.add_note(_cleanup_failure_note(cleanup_error))


def _build_launch_command(config: VLLMServingConfig, container_name: str) -> Command:
    """Build the deterministic Docker argv for one vLLM container."""
    arguments = [
        "run",
        "--detach",
        "--name",
        container_name,
        "--label",
        f"{_MANAGED_LABEL}={_MANAGED_LABEL_VALUE}",
        "--gpus",
        "all",
        "--ipc",
        "host",
        "--mount",
        f"type=bind,src={config.cache_root},dst={_CACHE_DESTINATION}",
        "--publish",
        f"127.0.0.1:{config.host_port}:{_CONTAINER_PORT}",
        config.image,
        config.model.repository,
        "--revision",
        config.model.revision,
        "--served-model-name",
        config.served_model_name,
        "--max-model-len",
        str(config.max_model_len),
        "--gpu-memory-utilization",
        str(config.gpu_memory_utilization),
        "--max-num-seqs",
        str(config.max_num_seqs),
    ]
    if config.trust_remote_code:
        arguments.append("--trust-remote-code")

    return Command("docker", tuple(arguments))


def _inspect_command(container_id: str) -> Command:
    """Build an exact-container Docker inspection command."""
    return Command(
        "docker",
        (
            "inspect",
            "--format",
            (
                "{{.State.Running}}|"
                '{{index .Config.Labels "devtools.model_serving.managed"}}'
            ),
            container_id,
        ),
    )


def _stop_command(container_id: str) -> Command:
    """Build an exact-container Docker stop command."""
    return Command("docker", ("stop", container_id))


def _remove_command(container_id: str) -> Command:
    """Build an exact-container Docker removal command."""
    return Command("docker", ("rm", container_id))


def _logs_command(container_id: str) -> Command:
    """Build a bounded provider-log request for one exact container."""
    return Command(
        "docker",
        ("logs", "--tail", str(_PROVIDER_LOG_TAIL_LINES), container_id),
    )


def _new_container_name() -> str:
    """Create a non-semantic, bounded operational Docker container name."""
    return f"devtools-vllm-{uuid.uuid4().hex[:12]}"


def _parse_container_id(result: CommandResult) -> str:
    """Extract Docker's detached container ID from successful standard output."""
    output = result.stdout.decode("utf-8", errors="replace")
    lines = [line for line in output.splitlines() if line]
    if len(lines) != 1 or _CONTAINER_ID.fullmatch(lines[0]) is None:
        msg = "Docker launch output did not contain exactly one valid container ID."
        raise VLLMLaunchError(msg)

    return lines[0]


async def _inspect_container(
    executor: CommandExecutor,
    container_id: str,
) -> _ContainerInspection | None:
    """Inspect one exact container, distinguishing absence from operational error."""
    result = await executor.execute(_inspect_command(container_id))
    if result.failed:
        if _is_exact_container_not_found(result, container_id):
            return None

        raise VLLMInspectionError(_inspection_error_message(result))

    return _parse_inspection(result)


def _parse_inspection(result: CommandResult) -> _ContainerInspection:
    """Parse the fixed Docker inspection projection used by this module."""
    lines = result.stdout.decode("utf-8", errors="replace").splitlines()
    if len(lines) != 1:
        msg = "Docker inspection output was not a single state projection."
        raise VLLMInspectionError(msg)

    value = lines[0]
    running_text, separator, label = value.partition("|")
    if not separator or running_text.lower() not in {"true", "false"}:
        msg = "Docker inspection output was not a valid state projection."
        raise VLLMInspectionError(msg)

    return _ContainerInspection(
        running=running_text.lower() == "true",
        ownership_label=label,
    )


def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:
    """Return whether Docker reported this exact inspected container as absent."""
    expected = f"error: no such object: {container_id}".casefold()
    diagnostic = result.stderr.decode("utf-8", errors="replace").strip().casefold()
    return diagnostic == expected


def _inspection_error_message(result: CommandResult) -> str:
    """Create bounded diagnostics for a Docker inspection failure."""
    diagnostic = _diagnostic_text(result.stderr or result.stdout)
    message = (
        "Docker could not inspect owned vLLM container "
        f"(exit {result.exit_code})."
    )
    return f"{message} {diagnostic}" if diagnostic else message


def _launch_error_message(result: CommandResult) -> str:
    """Create bounded launch diagnostics from a nonzero Docker result."""
    diagnostic = _diagnostic_text(result.stderr or result.stdout)
    message = f"Docker rejected vLLM launch with exit code {result.exit_code}."
    return f"{message} {diagnostic}" if diagnostic else message


def _diagnostic_text(data: bytes) -> str:
    """Decode a bounded command-output prefix for an error message."""
    return data[:_MAX_DIAGNOSTIC_BYTES].decode("utf-8", errors="replace").strip()


def _cleanup_failure_note(error: BaseException) -> str:
    """Describe a bounded secondary cleanup error on a primary exception."""
    prefix = "Owned vLLM container cleanup also failed: "
    available = _MAX_DIAGNOSTIC_BYTES - len(prefix.encode("utf-8"))
    diagnostic = str(error).encode("utf-8", errors="replace")[:available]
    detail = diagnostic.decode("utf-8", errors="ignore").strip()
    return f"{prefix}{detail or type(error).__name__}"


async def _provider_log_tail(
    executor: CommandExecutor,
    container_id: str,
) -> str | None:
    """Return a bounded tail of one exact container's combined provider logs."""
    try:
        result = await executor.execute(_logs_command(container_id))
    except Exception:  # noqa: BLE001
        return None

    if result.failed:
        return None

    tail = (result.stdout + result.stderr)[-_PROVIDER_LOG_TAIL_BYTES:]
    text = tail.decode("utf-8", errors="ignore").strip()
    return text or None


async def _probe_model_ready(endpoint: str, model_name: str) -> bool:
    """Probe vLLM's local health and model-list endpoints without a HTTP domain."""
    health_status, _ = await _http_get(endpoint, "/health")
    if health_status != _HTTP_OK:
        return False

    models_status, content = await _http_get(endpoint, "/v1/models")
    if models_status != _HTTP_OK:
        return False

    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return False

    data = payload.get("data")
    if not isinstance(data, list):
        return False

    return any(
        isinstance(item, dict) and item.get("id") == model_name for item in data
    )


async def _http_get(endpoint: str, path: str) -> tuple[int, str]:
    """Perform a tiny provider-local HTTP GET for readiness probing."""
    parsed = urlsplit(endpoint)
    host = parsed.hostname
    if host is None:
        return 0, ""

    port = parsed.port or 80
    try:
        reader, writer = await asyncio.open_connection(host, port)
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n\r\n"
        ).encode()
        writer.write(request)
        await writer.drain()
        response = await reader.read(65_536)
        writer.close()
        await writer.wait_closed()
    except OSError:
        return 0, ""

    head, separator, body = response.partition(b"\r\n\r\n")
    if not separator:
        return 0, ""

    status_line = head.split(b"\r\n", maxsplit=1)[0].split()
    if len(status_line) < _HTTP_STATUS_PARTS:
        return 0, ""

    try:
        return int(status_line[1]), body.decode("utf-8", errors="replace")
    except ValueError:
        return 0, ""
