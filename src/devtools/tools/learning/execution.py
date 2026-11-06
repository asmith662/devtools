# Copyright (c) 2026
"""Host-selected managed execution for exact learning plans; no model invocation."""

from __future__ import annotations

import importlib.metadata
import json
import sys
from dataclasses import asdict
from pathlib import Path
from typing import TYPE_CHECKING

from devtools.core.paths import ResolvedPath, resolve_path
from devtools.core.time import Duration
from devtools.learning.integrations.local.classification.codec import document
from devtools.learning.integrations.local.operations import LearningPublication
from devtools.learning.integrations.local.worker import MAX_PACKET_BYTES
from devtools.learning.investigation.errors import LearningUnavailableError
from devtools.learning.investigation.plans import (
    LearningPlan,
    canonical,
    validate_authorization,
)
from devtools.resources.commands import Command, CommandExecutor, CommandOutputPolicy
from devtools.resources.filesystem import BinaryFile, TextFile, write

if TYPE_CHECKING:
    from devtools.learning.investigation.classification.contracts import (
        ExecutionAuthorization,
    )

_OPERATION_SECONDS = 300

_BOOTSTRAP = """
import importlib.abc,json,pathlib,runpy,site,sys
roots=tuple(pathlib.Path(p).resolve() for p in json.loads(sys.argv[2]))
def guard(event,args):
    if event=='open' and isinstance(args[0],(str,bytes)):
        raw=args[0].decode() if isinstance(args[0],bytes) else args[0]
        p=pathlib.Path(raw).resolve()
        parts=tuple(s.lower() for s in p.parts)
        if '.tmp' in parts or any(p.is_relative_to(r) for r in roots):
            raise PermissionError('learning source/archive read denied')
class NoDonor(importlib.abc.MetaPathFinder):
    def find_spec(self,fullname,path=None,target=None):
        if fullname.split('.')[0]=='learned_intelligence':
            raise ImportError('donor package import denied')
sys.addaudithook(guard)
sys.meta_path.insert(0,NoDonor())
site.addsitedir(sys.argv[1])
sys.argv=sys.argv[3:]
runpy.run_module('devtools.learning.integrations.local.worker',run_name='__main__')
"""


class ManagedLearningWorker:
    """Use qualified direct CPython with one selected dependency environment."""

    def __init__(
        self,
        executable: ResolvedPath,
        site_packages: ResolvedPath,
        *,
        denied_roots: tuple[ResolvedPath, ...] = (),
    ) -> None:
        """Keep interpreter and package origins explicit; never inherit PYTHONPATH."""
        self.executable = executable
        self.site_packages = site_packages
        self.denied_roots = denied_roots
        self.receipts: list[dict[str, object]] = []

    @classmethod
    def current(cls) -> ManagedLearningWorker:
        """Select CPython's actual executable and the current distribution origin."""
        executable = getattr(sys, "_base_executable", None)
        if sys.implementation.name != "cpython" or not isinstance(executable, str):
            msg = "the qualified direct CPython interpreter is required"
            raise ValueError(msg)
        try:
            site = Path(str(importlib.metadata.distribution("numpy").locate_file("")))
        except importlib.metadata.PackageNotFoundError as error:
            msg = "The optional learning numerical dependencies are not installed."
            raise LearningUnavailableError(
                msg,
            ) from error
        return cls(resolve_path(Path(executable)), resolve_path(site))

    async def execute(
        self,
        plan: LearningPlan,
        grant: ExecutionAuthorization,
        root: Path,
        *,
        timeout: Duration = Duration.seconds(300),
    ) -> LearningPublication:
        """Inspect the declared scientific contract.

        Consume one exact packet once, preserving failed/uncertain operation
        roots.
        """
        validate_authorization(plan, grant)
        packet = canonical(
            {"plan": plan.document(), "grant": document(asdict(grant))},
        ).encode()
        if len(packet) > MAX_PACKET_BYTES:
            msg = "learning packet exceeds its pre-entry limit"
            raise ValueError(msg)
        if timeout.total_seconds > _OPERATION_SECONDS:
            msg = "learning operation timeout exceeds the qualified profile"
            raise ValueError(msg)
        root.mkdir()
        (root / "temp").mkdir()
        write(BinaryFile(resolve_path(root / "request.json"), packet), overwrite=False)
        command = (
            Command(str(self.executable.value))
            .args(
                "-S",
                "-c",
                _BOOTSTRAP,
                str(self.site_packages.value),
                json.dumps([str(r.value) for r in self.denied_roots]),
            )
            .cwd(resolve_path(root))
            .with_timeout(timeout)
            .with_environment(
                {
                    "PYTHONPATH": "",
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "OMP_NUM_THREADS": "1",
                    "OPENBLAS_NUM_THREADS": "1",
                    "MKL_NUM_THREADS": "1",
                    "BLIS_NUM_THREADS": "1",
                    "NUMEXPR_NUM_THREADS": "1",
                    "TMP": str(root / "temp"),
                    "TEMP": str(root / "temp"),
                },
            )
        )
        result = await CommandExecutor(
            contained=True,
            output_policy=CommandOutputPolicy(
                max_stdout_bytes=65536,
                max_stderr_bytes=262144,
            ),
        ).execute(command)
        self.receipts.append(
            {
                "plan_identity": plan.identity,
                "executable": str(self.executable),
                "site_packages": str(self.site_packages),
                "exit_code": result.exit_code,
                "seconds": result.duration.total_seconds,
                "stderr": result.stderr.decode("utf-8", errors="replace"),
            },
        )
        write(
            TextFile(
                resolve_path(root / "execution.json"),
                canonical(
                    {
                        **self.receipts[-1],
                        "stdout": result.stdout.decode("utf-8", errors="replace"),
                        "stdout_truncated": result.stdout_truncated,
                        "stderr_truncated": result.stderr_truncated,
                        "retry": "NONE; this operation root is consumed",
                    },
                ),
            ),
            overwrite=False,
        )
        if not result.succeeded or result.stdout_truncated or result.stderr_truncated:
            msg = (
                "Learning worker failed or returned incomplete evidence; no autom"
                "atic retry."
            )
            raise RuntimeError(
                msg,
            )
        saved = json.loads(result.stdout)
        if (
            not isinstance(saved, dict)
            or set(saved) != {"generation_id", "manifest_sha256", "plan_identity"}
            or saved["plan_identity"] != plan.identity
            or not all(isinstance(v, str) for v in saved.values())
        ):
            msg = (
                "learning worker response does not correspond to this exact invocation"
            )
            raise ValueError(
                msg,
            )
        return LearningPublication(
            resolve_path(root / "science"),
            saved["generation_id"],
            saved["manifest_sha256"],
            plan.identity,
        )
