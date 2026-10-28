# Copyright (c) 2026
"""Known-source candidate custody, with host-owned archival and restoration effects."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, cast

from devtools.agents.coding.models import CodingCompletion
from devtools.context.repository.resource import ContentIdentity
from devtools.core.paths import resolve_path
from devtools.resources.filesystem import FileFormat, TextFile, read

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from devtools.context import RepositoryResourceAddress
    from devtools.core.paths import ResolvedPath


class SourceCustody:
    """Retain admitted before/after text identities, never discard unknown bytes.

    This is not Checkout authority, a lock, filesystem sandbox or transaction.
    The host supplies the initial scope, admitted expectations and every effect.
    """

    def __init__(
        self,
        root: ResolvedPath,
        baseline: Mapping[RepositoryResourceAddress, str | None],
        *,
        maximum_bytes: int,
    ) -> None:
        """Freeze one host-selected baseline without reading or changing source."""
        if not baseline or maximum_bytes <= 0:
            msg = "Source custody needs nonempty scope and a positive read limit."
            raise ValueError(msg)
        self.root, self.maximum_bytes = root, maximum_bytes
        self.baseline = MappingProxyType(dict(baseline))
        self._known = {path: {self._identity(text)} for path, text in baseline.items()}

    @staticmethod
    def _identity(text: str | None) -> ContentIdentity | None:
        """Reuse the canonical decoded-text identity, keeping absence distinct."""
        return None if text is None else ContentIdentity.from_text(text)

    def expect(self, path: RepositoryResourceAddress, text: str | None) -> None:
        """Retain admitted source before a potentially ambiguous effect."""
        if path not in self._known:
            msg = "Candidate path is outside host custody."
            raise ValueError(msg)
        self._known[path].add(self._identity(text))

    def capture(self) -> dict[RepositoryResourceAddress, str | None]:
        """Capture bounded source, refusing aliases before disclosure."""
        if resolve_path(self.root.value) != self.root:
            msg = "Custody root changed."
            raise ValueError(msg)
        result = {}
        for path in self.baseline:
            raw = self.root.value / path.value
            resolved = resolve_path(raw)
            if resolved.value != raw or raw.is_symlink() or raw.is_junction():
                msg = "Custody path aliases are not admitted."
                raise ValueError(msg)
            result[path] = (
                cast(
                    "TextFile",
                    read(
                        resolved,
                        file_format=FileFormat.TEXT,
                        max_bytes=self.maximum_bytes,
                    ),
                ).content
                if raw.exists()
                else None
            )
        return result

    def restore_known(
        self,
        current: Mapping[RepositoryResourceAddress, str | None],
        restore: Callable[[RepositoryResourceAddress, str | None], None],
    ) -> CodingCompletion:
        """Require complete known correspondence before calling any host restoration.

        Recheck after archive work; an intervening unknown change is not erased.
        Individual host writes can still fail; no cross-file atomicity is claimed.
        """
        if (
            set(current) != set(self.baseline)
            or any(
                self._identity(text) not in self._known[path]
                for path, text in current.items()
            )
            or self.capture() != current
        ):
            return CodingCompletion(restored=False, reconciliation_required=True)
        for path, text in self.baseline.items():
            restore(path, text)
        restored = self.capture() == self.baseline
        return CodingCompletion(restored=restored, reconciliation_required=not restored)
