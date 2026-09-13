# Copyright (c) 2026
"""Tests for the plain-text representation codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from devtools.core.paths import ResolvedPath
from devtools.resources.filesystem import (
    TextCodec,
    TextDecodingError,
    TextEncodingError,
)

if TYPE_CHECKING:
    from pathlib import Path


@pytest.mark.parametrize(
    ("source", "encoding"),
    [
        ("", "utf-8"),
        ("first\r\nsecond\n", "utf-8"),
        ("cafÃ©", "utf-8"),
        ("MÃ¼nchen", "utf-16"),
    ],
)
def test_decode_preserves_exact_text_and_source_metadata(
    tmp_path: Path,
    source: str,
    encoding: str,
) -> None:
    """Decoding retains text verbatim, including whitespace and newlines."""
    content = source.encode(encoding)

    file = TextCodec().decode(
        ResolvedPath(tmp_path / "source.txt"),
        content,
        encoding=encoding,
    )

    assert file.content == source
    assert file.encoding == encoding
    assert file.byte_size == len(content)


def test_decode_normalizes_unknown_encodings_and_invalid_bytes(tmp_path: Path) -> None:
    """Text decoding exposes stable domain failures rather than codec details."""
    codec = TextCodec()
    path = ResolvedPath(tmp_path / "source.txt")

    with pytest.raises(TextDecodingError, match="utf-8"):
        codec.decode(path, b"\xff")

    with pytest.raises(TextDecodingError, match="unknown-codec"):
        codec.decode(path, b"text", encoding="unknown-codec")


def test_codec_created_text_files_retain_rich_source_operations(tmp_path: Path) -> None:
    """Codec output remains a full text model without implicit iteration."""
    file = TextCodec().decode(
        ResolvedPath(tmp_path / "source.txt"),
        b"alpha\nbeta\n",
    )

    assert file.lines == ("alpha", "beta")
    expected_line_count = 2
    assert file.line_count == expected_line_count
    assert file.character_count == len("alpha\nbeta\n")
    assert file.contains("pha") is True
    assert file.search_regex(r"b.ta") is not None
    assert tuple(match.value for match in file.find_all_regex(r"[a-z]+")) == (
        "alpha",
        "beta",
    )


def test_encode_uses_model_metadata_and_allows_an_override(tmp_path: Path) -> None:
    """Encoding defaults to metadata while retaining an explicit override."""
    codec = TextCodec()
    source = "cafÃ©"
    file = codec.decode(
        ResolvedPath(tmp_path / "source.txt"),
        source.encode("utf-16"),
        encoding="utf-16",
    )

    assert codec.encode(file) == source.encode("utf-16")
    assert codec.encode(file, encoding="utf-8") == source.encode("utf-8")


def test_encode_normalizes_unknown_and_unencodable_text(tmp_path: Path) -> None:
    """Encoding failures are consistently translated to domain errors."""
    codec = TextCodec()
    file = codec.decode(
        ResolvedPath(tmp_path / "source.txt"),
        "cafÃ©".encode(),
    )

    with pytest.raises(TextEncodingError, match="ascii"):
        codec.encode(file, encoding="ascii")

    with pytest.raises(TextEncodingError, match="unknown-codec"):
        codec.encode(file, encoding="unknown-codec")
