# Copyright (c) 2026
# ruff: noqa: S603 -- real descendant only in process-cleanup fixture
"""Spawn one delayed descendant to prove supervisor tree cleanup without models."""

import subprocess
import sys
import time
from pathlib import Path

if __name__ == "__main__":
    marker = str(Path.cwd() / "orphan.txt")
    subprocess.Popen(
        [
            sys.executable,
            "-c",
            "import time; from pathlib import Path; time.sleep(1.5); Path("
            + repr(marker)
            + ").write_text('orphan')",
        ],
    )
    time.sleep(20)
