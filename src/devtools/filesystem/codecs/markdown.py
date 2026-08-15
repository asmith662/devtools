# Copyright (c) 2026
"""Markdown filesystem codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.filesystem.errors import (
    TextDecodingError,
    TextEncodingError,
)
from devtools.filesystem.models import MarkdownFile

if TYPE_CHECKING:
    from devtools.paths import ResolvedPath


class MarkdownCodec:
    """Decode and encode Markdown file representations."""

    def decode(
        self,
        path: ResolvedPath,
        content: bytes,
        *,
        encoding: str = "utf-8",
    ) -> MarkdownFile:
        """Decode raw Markdown bytes into a rich Markdown file model.

        :param path: Resolved path associated with the Markdown source.
        :param content: Raw Markdown bytes.
        :param encoding: Encoding used to decode the source bytes.
        :returns: Immutable Markdown file model.
        :raises TextDecodingError: If decoding fails or the encoding is unknown.
        """
        try:
            text = content.decode(encoding)
        except (LookupError, UnicodeDecodeError) as error:
            msg = f"Unable to decode Markdown file using {encoding!r}: {path}."
            raise TextDecodingError(msg) from error

        return MarkdownFile(
            path=path,
            content=text,
            encoding=encoding,
            byte_size=len(content),
        )

    def encode(
        self,
        file: MarkdownFile,
        *,
        encoding: str | None = None,
    ) -> bytes:
        """Encode a Markdown file model into bytes.

        Markdown encoding preserves the model's exact source content. Structural
        models such as headings and sections are derived from that content and
        are not separately serialized.

        :param file: Markdown file model to encode.
        :param encoding: Encoding override. Defaults to the file encoding.
        :returns: Encoded Markdown bytes.
        :raises TextEncodingError: If encoding fails or is unknown.
        """
        resolved_encoding = (
            file.encoding
            if encoding is None
            else encoding
        )

        try:
            return file.content.encode(resolved_encoding)
        except (LookupError, UnicodeEncodeError) as error:
            msg = (
                f"Unable to encode Markdown file using "
                f"{resolved_encoding!r}: {file.path}."
            )
            raise TextEncodingError(msg) from error
