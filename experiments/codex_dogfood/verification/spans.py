# Copyright (c) 2026
# ruff: noqa: ANN401, D102, D107 -- private bounded extraction adapter
"""Exact UTF-8 extraction using invocation-local byte and line-offset indices."""

from __future__ import annotations

from typing import Any

from devtools.context.python.function.materialization import (
    _extract_source_segment,
)


class SourceSpans:
    """Retain exact content, avoiding repeated complete-file encoding/splitting."""

    def __init__(self) -> None:
        self.indices: dict[str, tuple[bytes, tuple[int, ...], tuple[int, ...]]] = {}

    def extract(self, content: str, span: Any) -> str:
        if (span.start_line, span.start_column_utf8) > (
            span.end_line,
            span.end_column_utf8,
        ):
            return _extract_source_segment(content, span)
        hit = self.indices.get(content)
        if hit is None:
            lines = tuple(
                line.encode("utf-8") for line in content.splitlines(keepends=True)
            )
            line_starts, line_lengths, total = [], [], 0
            for line in lines:
                line_starts.append(total)
                line_lengths.append(len(line.rstrip(b"\r\n")))
                total += len(line)
            hit = (content.encode("utf-8"), tuple(line_starts), tuple(line_lengths))
            self.indices[content] = hit
        raw, starts, lengths = hit
        a, b = span.start_line, span.end_line
        x, y = span.start_column_utf8, span.end_column_utf8
        if (
            (a, x) > (b, y)
            or not 1 <= a <= len(starts)
            or not 1 <= b <= len(starts)
            or not 0 <= x <= lengths[a - 1]
            or not 0 <= y <= lengths[b - 1]
        ):
            return _extract_source_segment(content, span)
        try:
            return raw[starts[a - 1] + x : starts[b - 1] + y].decode("utf-8")
        except UnicodeDecodeError:
            return _extract_source_segment(content, span)
