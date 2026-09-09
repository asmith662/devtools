# ruff: noqa: BLE001, C901, CPY001, D102, D105, D107, E501, EM101, FBT003, PLR2004, S104, TRY003
"""Experimental concrete llama.cpp CUDA Docker serving lifecycle."""

from __future__ import annotations

import asyncio
import re
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Literal, Self
from urllib.parse import urlsplit

from devtools.commands import Command, CommandExecutor, CommandResult
from devtools.model_serving.errors import (
    LlamaCppCapabilityError,
    LlamaCppInspectionError,
    LlamaCppLaunchError,
    LlamaCppOwnershipError,
    LlamaCppStartupError,
    LlamaCppStopError,
    ServingReadinessTimeoutError,
)
from devtools.time import Duration, Timestamp

if TYPE_CHECKING:
    from devtools.paths import ResolvedPath


_CONTAINER_PORT = 8080
_MODEL_DIRECTORY = "/models"
_MANAGED_LABEL = "devtools.model_serving.managed"
_MANAGED_VALUE = "true"
_CONTAINER_ID = re.compile(r"^[0-9a-fA-F]{64}$")
_MAX_HOST_PORT = 65_535
_POLL_INTERVAL_SECONDS = 0.25
_HTTP_OK = 200
_PROVIDER_LOG_TAIL_LINES = 200
_PROVIDER_LOG_TAIL_BYTES = 16 * 1024
_MAX_DIAGNOSTIC_BYTES = 4_096
_N_CPU_FFN_OPTION = "--n-cpu-ffn"
DEFAULT_READINESS_TIMEOUT = Duration.minutes(10)
CacheType = Literal[
    "f32",
    "f16",
    "bf16",
    "q8_0",
    "q4_0",
    "q4_1",
    "iq4_nl",
    "q5_0",
    "q5_1",
]
_FLASH_ATTENTION_VALUES = frozenset(("auto", "on", "off"))
_CACHE_TYPE_VALUES = frozenset(
    ("f32", "f16", "bf16", "q8_0", "q4_0", "q4_1", "iq4_nl", "q5_0", "q5_1"),
)


@dataclass(frozen=True, slots=True)
class GGUFModel:
    """Identify one explicit local GGUF entry artifact."""

    path: ResolvedPath

    def __post_init__(self) -> None:
        if self.path.suffix.casefold() != ".gguf":
            msg = "llama.cpp model path must name a .gguf artifact."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class LlamaCppServingConfig:
    """Describe one reproducible llama.cpp Docker launch."""

    model: GGUFModel
    image: str
    host_port: int
    served_model_name: str
    context_size: int
    gpu_layers: int | Literal["auto", "all"]
    flash_attention: Literal["auto", "on", "off"] = "auto"
    cache_type_k: CacheType = "f16"
    cache_type_v: CacheType = "f16"
    parallel_sequences: int = 1
    n_cpu_ffn: int = 0

    def __post_init__(self) -> None:
        if not self.image.strip() or ":" not in self.image:
            raise ValueError("llama.cpp image must include an explicit tag or digest.")
        if not 1 <= self.host_port <= _MAX_HOST_PORT:
            raise ValueError("Host port must be between 1 and 65535.")
        if not self.served_model_name.strip():
            raise ValueError("Served model name cannot be empty.")
        if self.context_size <= 0:
            raise ValueError("Context size must be positive.")
        if isinstance(self.gpu_layers, int) and self.gpu_layers < 0:
            raise ValueError("GPU layer count must be non-negative.")
        if self.gpu_layers not in {"auto", "all"} and not isinstance(
            self.gpu_layers,
            int,
        ):
            raise ValueError("GPU layers must be an integer, auto, or all.")
        if self.parallel_sequences <= 0:
            raise ValueError("Parallel sequence count must be positive.")
        if isinstance(self.n_cpu_ffn, bool) or not isinstance(self.n_cpu_ffn, int):
            msg = "CPU FFN layer count must be an integer."
            raise TypeError(msg)
        if self.n_cpu_ffn < 0:
            raise ValueError("CPU FFN layer count cannot be negative.")
        if self.flash_attention not in _FLASH_ATTENTION_VALUES:
            raise ValueError("Flash Attention must be auto, on, or off.")
        if self.cache_type_k not in _CACHE_TYPE_VALUES:
            raise ValueError("K cache type is not supported by this llama.cpp slice.")
        if self.cache_type_v not in _CACHE_TYPE_VALUES:
            raise ValueError("V cache type is not supported by this llama.cpp slice.")


@dataclass(frozen=True, slots=True)
class LlamaCppServerStatus:
    """Describe the bounded status of one owned llama.cpp container."""

    container_running: bool
    model_ready: bool


@dataclass(frozen=True, slots=True)
class _ContainerInspection:
    running: bool
    ownership_label: str


class LlamaCppServer:
    """Represent one live, explicitly owned llama.cpp server."""

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
        config: LlamaCppServingConfig,
        container_id: str,
        container_name: str,
        executor: CommandExecutor,
        started_at: Timestamp,
    ) -> None:
        self._config = config
        self._container_id = container_id
        self._container_name = container_name
        self._executor = executor
        self._started_at = started_at

    @property
    def config(self) -> LlamaCppServingConfig:
        return self._config

    @property
    def container_id(self) -> str:
        return self._container_id

    @property
    def endpoint(self) -> str:
        return f"http://127.0.0.1:{self._config.host_port}"

    @property
    def started_at(self) -> Timestamp:
        return self._started_at

    @classmethod
    async def start(
        cls,
        *,
        config: LlamaCppServingConfig,
        executor: CommandExecutor,
        readiness_timeout: Duration = DEFAULT_READINESS_TIMEOUT,
    ) -> Self:
        if not config.model.path.value.is_file():
            raise ValueError("llama.cpp GGUF model path must be an existing file.")
        await _preflight_required_features(config, executor)
        name = _new_container_name()
        result = await executor.execute(_build_launch_command(config, name))
        if result.failed:
            raise LlamaCppLaunchError(_launch_error_message(result))
        server = cls(
            config=config,
            container_id=_parse_container_id(result),
            container_name=name,
            executor=executor,
            started_at=Timestamp.now(),
        )
        try:
            await server.wait_ready(readiness_timeout=readiness_timeout)
        except BaseException as error:
            await server._stop_after_unsuccessful_start(error)
            raise
        return server

    async def wait_ready(
        self,
        *,
        readiness_timeout: Duration = DEFAULT_READINESS_TIMEOUT,
    ) -> None:
        if readiness_timeout.total_seconds <= 0:
            raise ValueError("llama.cpp readiness timeout must be positive.")
        try:
            async with asyncio.timeout(readiness_timeout.total_seconds):
                while True:
                    status = await self.status()
                    if status.model_ready:
                        return
                    if not status.container_running:
                        raise LlamaCppStartupError(
                            "Owned llama.cpp container stopped before its model became ready.",
                            provider_log_tail=await _provider_log_tail(
                                self._executor,
                                self._container_id,
                            ),
                        )
                    await asyncio.sleep(_POLL_INTERVAL_SECONDS)
        except TimeoutError as error:
            raise ServingReadinessTimeoutError(
                "llama.cpp container did not become ready within the configured timeout.",
            ) from error

    async def status(self) -> LlamaCppServerStatus:
        inspection = await _inspect_container(self._executor, self._container_id)
        if inspection is None or not inspection.running:
            return LlamaCppServerStatus(False, False)
        return LlamaCppServerStatus(True, await _probe_ready(self.endpoint))

    async def stop(self) -> None:
        inspection = await _inspect_container(self._executor, self._container_id)
        if inspection is None:
            return
        if inspection.ownership_label != _MANAGED_VALUE:
            raise LlamaCppOwnershipError(
                "Refusing to stop a container without the expected ownership label.",
            )
        if inspection.running:
            result = await self._executor.execute(
                Command("docker", ("stop", self._container_id)),
            )
            if result.failed:
                raise LlamaCppStopError(
                    _stop_error_message("stop", result, self._container_id),
                )
        result = await self._executor.execute(
            Command("docker", ("rm", self._container_id)),
        )
        if result.failed and not _is_exact_container_not_found(
            result,
            self._container_id,
        ):
            raise LlamaCppStopError(
                _stop_error_message("remove", result, self._container_id),
            )

    async def _stop_after_unsuccessful_start(self, primary: BaseException) -> None:
        try:
            await self.stop()
        except BaseException as cleanup:
            prefix = "Owned llama.cpp container cleanup also failed: "
            available = _MAX_DIAGNOSTIC_BYTES - len(prefix.encode("utf-8"))
            detail = str(cleanup).encode("utf-8", errors="replace")[:available]
            message = detail.decode("utf-8", errors="ignore").strip()
            primary.add_note(f"{prefix}{message or type(cleanup).__name__}")


def _build_launch_command(
    config: LlamaCppServingConfig,
    container_name: str,
) -> Command:
    container_model = f"{_MODEL_DIRECTORY}/{config.model.path.name}"
    host_model = config.model.path.value.resolve()
    return Command(
        "docker",
        (
            "run",
            "--detach",
            "--name",
            container_name,
            "--label",
            f"{_MANAGED_LABEL}={_MANAGED_VALUE}",
            "--gpus",
            "all",
            "--mount",
            f"type=bind,src={host_model},dst={container_model},readonly",
            "--publish",
            f"127.0.0.1:{config.host_port}:{_CONTAINER_PORT}",
            config.image,
            "--model",
            container_model,
            "--host",
            "0.0.0.0",
            "--port",
            str(_CONTAINER_PORT),
            "--alias",
            config.served_model_name,
            "--ctx-size",
            str(config.context_size),
            "--n-gpu-layers",
            str(config.gpu_layers),
            "--flash-attn",
            config.flash_attention,
            "--cache-type-k",
            config.cache_type_k,
            "--cache-type-v",
            config.cache_type_v,
            "--parallel",
            str(config.parallel_sequences),
            *(_n_cpu_ffn_arguments(config.n_cpu_ffn)),
        ),
    )


def _n_cpu_ffn_arguments(n_cpu_ffn: int) -> tuple[str, ...]:
    """Return the optional provider-local FFN placement arguments."""
    return (_N_CPU_FFN_OPTION, str(n_cpu_ffn)) if n_cpu_ffn else ()


def _help_command(config: LlamaCppServingConfig) -> Command:
    """Ask the configured image's llama-server entrypoint for its CLI help."""
    return Command("docker", ("run", "--rm", config.image, "--help"))


async def _preflight_required_features(
    config: LlamaCppServingConfig,
    executor: CommandExecutor,
) -> None:
    """Verify required recent llama.cpp options before attempting model launch."""
    if config.n_cpu_ffn == 0:
        return
    result = await executor.execute(_help_command(config))
    if result.failed:
        diagnostic = _diagnostic_text(result.stderr or result.stdout)
        message = (
            f"Could not establish whether configured llama.cpp image "
            f"{config.image!r} supports required {_N_CPU_FFN_OPTION}; "
            f"capability probe exited with code {result.exit_code}."
        )
        raise LlamaCppCapabilityError(
            f"{message} {diagnostic}" if diagnostic else message,
        )
    help_text = (result.stdout + result.stderr).decode(errors="replace")
    if not _advertises_n_cpu_ffn(help_text):
        msg = (
            f"Configured llama.cpp image {config.image!r} does not advertise "
            f"required {_N_CPU_FFN_OPTION} support. Pin an image/build that does "
            "before launching this profile."
        )
        raise LlamaCppCapabilityError(msg)


def _advertises_n_cpu_ffn(help_text: str) -> bool:
    """Match the exact long option, not a similarly named provider feature."""
    return re.search(r"(?<!\S)--n-cpu-ffn(?=\s|=|,|$)", help_text) is not None


def _new_container_name() -> str:
    return f"devtools-llama-cpp-{uuid.uuid4().hex[:12]}"


def _parse_container_id(result: CommandResult) -> str:
    lines = [
        line for line in result.stdout.decode(errors="replace").splitlines() if line
    ]
    if len(lines) != 1 or _CONTAINER_ID.fullmatch(lines[0]) is None:
        raise LlamaCppLaunchError(
            "Docker launch output did not contain exactly one valid container ID.",
        )
    return lines[0]


def _inspect_command(container_id: str) -> Command:
    return Command(
        "docker",
        (
            "inspect",
            "--format",
            '{{.State.Running}}|{{index .Config.Labels "devtools.model_serving.managed"}}',
            container_id,
        ),
    )


async def _inspect_container(
    executor: CommandExecutor,
    container_id: str,
) -> _ContainerInspection | None:
    result = await executor.execute(_inspect_command(container_id))
    if result.failed:
        if _is_exact_container_not_found(result, container_id):
            return None
        raise LlamaCppInspectionError(
            _diagnostic_text(result.stderr or result.stdout)
            or "Docker could not inspect owned llama.cpp container.",
        )
    parts = result.stdout.decode(errors="replace").splitlines()
    if len(parts) != 1:
        raise LlamaCppInspectionError(
            "Docker inspection output was not a single state projection.",
        )
    state, sep, label = parts[0].partition("|")
    if not sep or state.casefold() not in {"true", "false"}:
        raise LlamaCppInspectionError(
            "Docker inspection output was not a valid state projection.",
        )
    return _ContainerInspection(state.casefold() == "true", label)


def _is_exact_container_not_found(result: CommandResult, container_id: str) -> bool:
    return (
        result.stderr.decode(errors="replace").strip().casefold()
        == f"error: no such object: {container_id}".casefold()
    )


def _diagnostic_text(data: bytes) -> str:
    return data[:4096].decode(errors="replace").strip()


def _launch_error_message(result: CommandResult) -> str:
    return f"Docker rejected llama.cpp launch with exit code {result.exit_code}. {_diagnostic_text(result.stderr or result.stdout)}".strip()


def _stop_error_message(
    operation: str,
    result: CommandResult,
    container_id: str,
) -> str:
    return f"Docker could not {operation} owned llama.cpp container {container_id!r}. {_diagnostic_text(result.stderr or result.stdout)}".strip()


async def _provider_log_tail(
    executor: CommandExecutor,
    container_id: str,
) -> str | None:
    try:
        result = await executor.execute(
            Command(
                "docker",
                ("logs", "--tail", str(_PROVIDER_LOG_TAIL_LINES), container_id),
            ),
        )
    except Exception:
        return None
    if result.failed:
        return None
    text = (
        (result.stdout + result.stderr)[-_PROVIDER_LOG_TAIL_BYTES:]
        .decode(errors="ignore")
        .strip()
    )
    return text or None


async def _probe_ready(endpoint: str) -> bool:
    return (await _http_get(endpoint, "/health"))[0] == _HTTP_OK


async def _http_get(endpoint: str, path: str) -> tuple[int, str]:
    parsed = urlsplit(endpoint)
    if parsed.hostname is None:
        return 0, ""
    try:
        reader, writer = await asyncio.open_connection(
            parsed.hostname,
            parsed.port or 80,
        )
        writer.write(
            f"GET {path} HTTP/1.1\r\nHost: {parsed.hostname}\r\nConnection: close\r\n\r\n".encode(),
        )
        await writer.drain()
        response = await reader.read()
        writer.close()
        await writer.wait_closed()
    except OSError:
        return 0, ""
    header, separator, body = response.partition(b"\r\n\r\n")
    if not separator:
        return 0, ""
    header_lines = header.splitlines()
    if not header_lines:
        return 0, ""
    parts = header_lines[0].split()
    if len(parts) != 3 or not parts[1].isdigit():
        return 0, ""
    return int(parts[1]), body.decode(errors="replace")
