# Copyright (c) 2026
# ruff: noqa: ANN401 -- explicit JSON boundary

"""Use canonical text I/O and the established explicit gzip codec boundary."""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

from devtools.core.paths import resolve_path
from devtools.resources.filesystem import TextFile, write
from experiments.codex_dogfood.case_0009.artifacts import binary, put_binary
from experiments.retrieval_diagnostics.serialization import encode

HERE = Path(__file__).resolve().parent


def put(path: Path, value: Any) -> None:
    """Publish deterministic JSON exclusively, refusing existing outputs."""
    content = encode(value)
    if path.suffix == ".gz":
        put_binary(path, gzip.compress(content, mtime=0))
    else:
        write(TextFile(resolve_path(path), content.decode()), overwrite=False)


def get(path: Path) -> Any:
    """Read a named bounded experiment artifact with explicit gzip semantics."""
    data = binary(path)
    return json.loads(gzip.decompress(data) if path.suffix == ".gz" else data)
