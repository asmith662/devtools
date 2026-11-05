# Copyright (c) 2026
"""Fixed public P3 producer probe; never import or execute candidate code."""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path


def main() -> None:
    """Observe the literal regex producer on frozen public contract examples.

    This narrow public probe is not full Markdown acceptance. Only the literal
    pattern is evaluated; arbitrary candidate statements are never executed.
    The managed fixed-check timeout bounds even a hostile regex.
    """
    source = Path(sys.argv[1]).read_text(encoding="utf-8")
    node = next(
        n
        for n in ast.walk(ast.parse(source))
        if isinstance(n, ast.AnnAssign)
        and isinstance(n.target, ast.Name)
        and n.target.id == "_ATX_HEADING_PATTERN"
    )
    if not isinstance(node.value, ast.Call):
        msg = "Public producer shape is unavailable"
        raise TypeError(msg)
    pattern = re.compile(ast.literal_eval(node.value.args[0]))
    outputs = []
    for text in ("# C#", "# C# #", "# Title #", "# ##"):
        match = pattern.fullmatch(text)
        outputs.append(
            {
                "input": text,
                "observed_title": match.group("text").strip() if match else None,
            },
        )
    print(  # noqa: T201 -- fixed public command stdout
        json.dumps(
            {
                "producer": "_ATX_HEADING_PATTERN text group followed by strip",
                "outputs": outputs,
            },
        ),
    )


if __name__ == "__main__":
    main()
