# Copyright (c) 2026
"""Case-local recording/profile utilities, reused before the frozen second case."""

from __future__ import annotations

import asyncio
import hashlib
import json
import sys
import urllib.request
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from devtools.core.paths import resolve_path
from devtools.core.time import Duration, Stopwatch, Timestamp
from devtools.models.interaction import InteractionSource
from devtools.models.interaction.providers.llama_cpp import LlamaCppInteraction
from devtools.models.interaction.providers.llama_cpp_request_settings import (
    LlamaCppRequestSettings,
)
from devtools.observability.commands.inspection import completed_observation
from devtools.observability.commands.models import CommandOrigin, CommandPattern
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import TextFile, write
from scripts.qwen.llama_cpp_profile import (
    QWEN38_27B_UD_IQ4_XS,
    QWEN38_INSTRUCT_SAMPLING,
)

CASE = Path(__file__).resolve().parent
CANONICAL = CASE.parents[1]
STATE = CANONICAL / ".local/supervisor-feedback/run"
CONTAINER = "devtools-qwen38-llama-cpp"
OBSERVATIONS = []
RECORDS = []


def plain(value):
    if is_dataclass(value):
        return {k: plain(v) for k, v in asdict(value).items()}
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def save(path, value, *, fresh=False):
    text = json.dumps(plain(value), ensure_ascii=True, indent=2) + "\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    if fresh and path.exists():
        raise FileExistsError(path)
    write(TextFile(resolve_path(path), text), overwrite=not fresh)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_files():
    return {
        str(p.relative_to(CASE)).replace("\\", "/"): digest(p)
        for p in sorted(CASE.rglob("*"))
        if p.is_file()
        and (p.suffix in {".py", ".md"} or p.name == ".gitignore")
        and "__pycache__" not in p.parts
    }


async def managed(command, label, *, retain=True):
    timer = Stopwatch()
    result = await CommandExecutor(
        output_policy=CommandOutputPolicy(
            max_stdout_bytes=131072, max_stderr_bytes=65536
        )
    ).execute(command)
    timer.stop()
    observation = completed_observation(
        result,
        origin=CommandOrigin(
            "local-dogfood-host", "B-0035-inventory", "maintenance-feedback-0001", label
        ),
        pattern=CommandPattern(
            command.executable.rsplit("/", 1)[-1]
            .replace("\\", "/")
            .rsplit("/", 1)[-1]
            .replace(":", "_"),
            label,
            ("opaque",),
            (sys.platform,),
        ),
    )
    OBSERVATIONS.append(observation)
    RECORDS.append(
        {
            "label": label,
            "exit_code": result.exit_code,
            "seconds": timer.elapsed.total_seconds,
            "stdout": result.stdout.decode(errors="replace") if retain else None,
            "stderr": result.stderr.decode(errors="replace") if retain else None,
            "stdout_truncated": result.stdout_truncated,
            "stderr_truncated": result.stderr_truncated,
        }
    )
    return result


async def git(root, *args):
    result = await managed(
        Command("git")
        .args(*args)
        .cwd(resolve_path(root))
        .with_timeout(Duration.seconds(30)),
        "git-" + str(len(RECORDS)),
    )
    if result.exit_code != 0:
        raise RuntimeError("Authored repository Git operation failed")
    return result.stdout.decode().strip()


async def service_identity():
    template = "{{json .Config.Cmd}}"
    result = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", template)
        .with_timeout(Duration.seconds(20)),
        "service-config",
        retain=False,
    )
    if result.exit_code:
        raise RuntimeError("Configured local service unavailable")
    args = json.loads(result.stdout)
    model_path = (
        args[args.index("--model") + 1]
        if "--model" in args
        else args[args.index("-m") + 1]
    )
    fingerprint = await managed(
        Command("docker")
        .args(
            "inspect",
            CONTAINER,
            "--format",
            '{{index .Config.Labels "devtools.qwen.profile-sha256"}}',
        )
        .with_timeout(Duration.seconds(20)),
        "service-profile",
    )
    image = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", "{{.Config.Image}}")
        .with_timeout(Duration.seconds(20)),
        "service-image",
    )
    expected = QWEN38_27B_UD_IQ4_XS
    mounts = await managed(
        Command("docker")
        .args("inspect", CONTAINER, "--format", "{{json .Mounts}}")
        .with_timeout(Duration.seconds(20)),
        "service-mount",
        retain=False,
    )
    selected = next(
        m for m in json.loads(mounts.stdout) if m["Destination"] == model_path
    )
    if selected["RW"] or selected["Type"] != "bind":
        raise RuntimeError("Expected read-only pinned artifact bind mount")
    artifact = resolve_path(selected["Source"]).value

    def hash_artifact():
        # Genuine external model-artifact boundary: stream, never load into RAM.
        with artifact.open("rb") as source:
            return hashlib.file_digest(source, "sha256").hexdigest()

    async with asyncio.timeout(60):
        actual_sha = await asyncio.to_thread(hash_artifact)
    if actual_sha != expected.expected_sha256:
        raise RuntimeError(
            "Installed GGUF content identity differs from selected profile"
        )
    if image.stdout.decode().strip() != expected.image_build_identity:
        raise RuntimeError("Serving image differs from pinned profile")
    with urllib.request.urlopen("http://127.0.0.1:8080/props", timeout=10) as response:
        props = json.loads(response.read(131073))
    with urllib.request.urlopen(
        "http://127.0.0.1:8080/v1/models", timeout=10
    ) as response:
        models = json.loads(response.read(65537))
    if "qwen38-local" not in {x["id"] for x in models["data"]}:
        raise RuntimeError("Expected served model alias is unavailable")
    return dict(
        profile=plain(expected),
        profile_fingerprint=fingerprint.stdout.decode().strip(),
        artifact_sha256=expected.expected_sha256,
        image=image.stdout.decode().strip(),
        endpoint="http://127.0.0.1:8080",
        served_model="qwen38-local",
        available_models=[x["id"] for x in models["data"]],
        context=props.get("default_generation_settings", {}).get("n_ctx"),
        chat_template_sha256=hashlib.sha256(
            str(props.get("chat_template", "")).encode()
        ).hexdigest(),
    )


class MeasuredInteraction:
    def __init__(self):
        self.delegate = LlamaCppInteraction(
            endpoint="http://127.0.0.1:8080",
            model="qwen38-local",
            source=InteractionSource("local-maintenance-feedback-acting"),
        )
        self.records = []

    @property
    def source(self):
        return self.delegate.source

    async def send(self, request):
        number = len(self.records) + 1
        if number > 8:
            raise RuntimeError("Frozen inference envelope exhausted")
        effective = request
        record = dict(
            number=number,
            at=str(Timestamp.now()),
            request=plain(effective),
            inference_entered=False,
        )
        self.records.append(record)
        save(STATE / f"request-{number}.json", record, fresh=True)
        async with asyncio.timeout(20):
            count = await self.delegate.count_input_tokens(effective)
        record["measured_input_tokens"] = count
        if count > 28160 or len(json.dumps(plain(effective),ensure_ascii=False).encode()) > 32768:
            save(STATE / f"request-{number}-capacity.json", record)
            raise RuntimeError("Frozen Context/capacity envelope refused request")
        timer = Stopwatch()
        record["inference_entered"] = True
        save(STATE / f"request-{number}-entry.json", record, fresh=True)
        try:
            response = await self.delegate.send(effective)
        except BaseException as error:
            record.update(
                error_kind=type(error).__name__, error=str(error), outcome="unknown"
            )
            raise
        else:
            record.update(response=plain(response), outcome="normalized-response")
            return response
        finally:
            timer.stop()
            record.update(
                seconds=timer.elapsed.total_seconds, completed_at=str(Timestamp.now())
            )
            save(STATE / f"request-{number}-outcome.json", record, fresh=True)
