# Copyright (c) 2026
"""Binary filesystem codec."""

from __future__ import annotations

from typing import TYPE_CHECKING

from devtools.resources.filesystem.models import BinaryFile

if TYPE_CHECKING:
    from devtools.core.paths import ResolvedPath


class BinaryCodec:
    """Encode and decode arbitrary binary file bytes without interpretation."""

    def decode(
        self,
        path: ResolvedPath,
        content: bytes,
    ) -> BinaryFile:
        """Wrap exact file bytes into an immutable binary file model.

        :param path: Resolved path associated with the binary content.
        :param content: Raw file bytes retained verbatim.
        :returns: Immutable binary file model preserving the supplied bytes.
        """
        return BinaryFile(
            path=path,
            content=bytes(content),
        )

    def encode(self, file: BinaryFile) -> bytes:
        """Serialize a binary file model into its exact bytes.

        :param file: Binary file model to encode.
        :returns: Exact retained file bytes.
        """
        return bytes(file.content)
