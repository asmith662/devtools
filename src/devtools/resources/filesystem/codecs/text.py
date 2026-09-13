# Copyright (c) 2026
"""Plain-text filesystem codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.resources.filesystem.errors import (
    TextDecodingError,
    TextEncodingError,
)
from devtools.resources.filesystem.models import TextFile

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath


class TextCodec:
    """Decode and encode plain-text file representations."""

    def decode(
        self,
        path: ResolvedPath,
        content: bytes,
        *,
        encoding: str = "utf-8",
    ) -> TextFile:
        """Decode raw bytes into a text file model.

        :param path: Resolved path associated with the text content.
        :param content: Raw source bytes.
        :param encoding: Encoding used to decode the source bytes.
        :returns: Immutable text file model.
        :raises TextDecodingError: If decoding fails or the encoding is unknown.
        """
        try:
            text = content.decode(encoding)
        except (LookupError, UnicodeDecodeError) as error:
            msg = f"Unable to decode text file using {encoding!r}: {path}."
            raise TextDecodingError(msg) from error

        return TextFile(
            path=path,
            content=text,
            encoding=encoding,
            byte_size=len(content),
        )

    def encode(
        self,
        file: TextFile,
        *,
        encoding: str | None = None,
    ) -> bytes:
        """Encode a text file model into bytes.

        :param file: Text file model to encode.
        :param encoding: Encoding override. Defaults to the file encoding.
        :returns: Encoded text bytes.
        :raises TextEncodingError: If encoding fails or is unknown.
        """
        resolved_encoding = file.encoding if encoding is None else encoding

        try:
            return file.content.encode(resolved_encoding)
        except (LookupError, UnicodeEncodeError) as error:
            msg = (
                f"Unable to encode text file using {resolved_encoding!r}: {file.path}."
            )
            raise TextEncodingError(msg) from error
