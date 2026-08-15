# Copyright (c) 2026
"""Tests for the Markdown representation codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.filesystem import (
    MarkdownCodec,
    TextDecodingError,
    TextEncodingError,
)
from devtools.paths import ResolvedPath

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("source", "encoding"),
    [
        ("# Title\n", "utf-8"),
        ("# CafÃ©\r\n", "utf-8"),
        ("## MÃ¼nchen\n", "utf-16"),
    ],
)
def test_decode_preserves_exact_markdown_source_and_metadata(
    tmp_path: Path,
    source: str,
    encoding: str,
) -> None:
    """Decoding keeps Markdown source verbatim for structural interpretation."""
    content = source.encode(encoding)

    file = MarkdownCodec().decode(
        ResolvedPath(tmp_path / "document.md"),
        content,
        encoding=encoding,
    )

    assert file.content == source
    assert file.encoding == encoding
    assert file.byte_size == len(content)


def test_markdown_codec_normalizes_decoding_failures(tmp_path: Path) -> None:
    """Invalid bytes and unknown codecs use the established filesystem errors."""
    codec = MarkdownCodec()
    path = ResolvedPath(tmp_path / "document.md")

    with pytest.raises(TextDecodingError, match="utf-8"):
        codec.decode(path, b"\xff")

    with pytest.raises(TextDecodingError, match="unknown-codec"):
        codec.decode(path, b"# Title", encoding="unknown-codec")


def test_encode_uses_source_content_and_explicit_encoding_policy(
    tmp_path: Path,
) -> None:
    """Encoding never reconstructs Markdown from derived headings or sections."""
    codec = MarkdownCodec()
    source = "# CafÃ©\r\n"
    file = codec.decode(
        ResolvedPath(tmp_path / "document.md"),
        source.encode("utf-16"),
        encoding="utf-16",
    )

    assert codec.encode(file) == source.encode("utf-16")
    assert codec.encode(file, encoding="utf-8") == source.encode()


def test_markdown_codec_normalizes_encoding_failures(tmp_path: Path) -> None:
    """Unknown and restrictive encodings produce stable domain failures."""
    codec = MarkdownCodec()
    file = codec.decode(
        ResolvedPath(tmp_path / "document.md"),
        "# CafÃ©".encode(),
    )

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.encode(file, encoding="ascii")

    with pytest.raises(TextEncodingError, match="unknown-codec"):
        codec.encode(file, encoding="unknown-codec")
