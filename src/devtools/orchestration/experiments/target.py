# Copyright (c) 2026
"""Fixed read-only adapter evaluated by the target checkout's interpreter.

This program imports only the target's packages, through normal Python startup.
No feature-checkout Python path or implementation is substituted into the target.
"""

PROGRAM = r"""
import asyncio
import hashlib
import json
import sys
from pathlib import Path

from devtools.core.time import Timestamp
from devtools.observability.usage import UsageWindow, report
from devtools.observability.usage.storage import load as observations
from devtools.resources import commands
from experiments.orchestration import controller, usage_budget
from experiments.orchestration.storage import binary, load, require, safe


async def main():
    stage, address, expected_head, expected_digest = sys.argv[1:]
    root = Path.cwd().resolve()
    require(
        Path(controller.__file__).resolve().is_relative_to(root / "experiments"),
        "Target controller imported from another checkout",
    )
    require(
        Path(commands.__file__).resolve().is_relative_to(root / "src"),
        "Target devtools imported from another checkout; use its environment",
    )
    repo = controller.Repository(root, push=False)
    require(
        (await repo.git("rev-parse", "HEAD")).decode().strip() == expected_head,
        "Target HEAD changed",
    )
    raw = binary(safe(root, address))
    require(hashlib.sha256(raw).hexdigest() == expected_digest, "Plan identity changed")
    value = json.loads(raw)
    repo.preserved_evidence = dict(value.get("preserved_evidence", {}))
    repo.remote, repo.push_enabled = (
        value["publication"]["remote"],
        value["publication"]["push"],
    )
    await repo.authenticate(expected_head)
    if stage == "validation":
        checked = await controller.Controller.from_plan(
            root, address, root.parent / "pipeline-unused-worker-root"
        )
        checked.require_not_superseded()
        require(
            not checked.science.exists(),
            "Existing scientific state requires controller reconciliation; no retry",
        )
        result = checked.plan_report()
        result["name"] = value["name"]
        result["executable"] = {
            "path": sys.executable,
            "version": sys.version,
            "sha256": hashlib.sha256(binary(Path(sys.executable))).hexdigest(),
        }
        await checked.repository.authenticate(expected_head)
    elif stage == "usage":
        path = root / ".local/usage/ledger.json"
        result = {
            "status": "PARTIAL" if path.exists() else "UNAVAILABLE",
            "ledger": str(path),
            "ledger_sha256": hashlib.sha256(binary(path)).hexdigest()
            if path.exists()
            else None,
            "observation": report(
                observations(path), UsageWindow.rolling(Timestamp.now())
            ) if path.exists() else None,
        }
    elif stage == "budget":
        snapshot = {
            name: {
                "path": str(root / ".local/usage" / name),
                "sha256": hashlib.sha256(
                    binary(root / ".local/usage" / name)
                ).hexdigest()
                if (root / ".local/usage" / name).exists()
                else None,
            }
            for name in (
                "policy.json",
                "backfill.json",
                "reservations.json",
                "ledger.json",
            )
        }
        plan = controller.RunPlan.parse(value)
        if not hasattr(usage_budget, "preview"):
            result = {
                "status": "UNAVAILABLE",
                "reason": "Target has no read-only budget preview contract",
            }
        else:
            result = usage_budget.preview(
                root, value, plan.identity(controller.implementation())
            )
        after = {
            name: {
                "path": str(root / ".local/usage" / name),
                "sha256": hashlib.sha256(
                    binary(root / ".local/usage" / name)
                ).hexdigest()
                if (root / ".local/usage" / name).exists()
                else None,
            }
            for name in (
                "policy.json",
                "backfill.json",
                "reservations.json",
                "ledger.json",
            )
        }
        require(snapshot == after, "Budget evidence changed during preparation")
        result["evidence"] = after
    else:
        raise ValueError("Unknown preparation stage")
    await repo.authenticate(expected_head)
    print(json.dumps(result))


try:
    asyncio.run(main())
except (ValueError, OSError, KeyError) as error:
    print(json.dumps({"error": str(error)}))
    sys.exit(1)
"""
