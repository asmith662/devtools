# Copyright (c) 2026
"""One optional auxiliary interaction; original history and effects remain elsewhere."""

from __future__ import annotations

import asyncio
import json
from dataclasses import asdict, dataclass
from typing import TYPE_CHECKING

from devtools.agents.coding.projection import native_exchange_ranges, request_bytes
from devtools.models.interaction import (
    ModelRequest,
    ModelTermination,
    Prompt,
    PromptMessage,
)

from .format import INSTRUCTIONS, digest, record, summary_payload, validate_summary
from .models import SummaryAttempt, SummaryCompaction

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from devtools.agents.coding.projection import ProjectionOutcome
    from devtools.context.planning.source import SourceRangeDisclosureOption

    from .adaptive import AdaptiveCompaction


@dataclass(frozen=True, slots=True)
class _Accepted:
    message: PromptMessage
    indices: frozenset[int]
    prefix: tuple[str, ...]
    snapshot: str


class SemanticCompactor:
    """Host-local auxiliary accounting and a derived projection, not another history."""

    def __init__(self, config: SummaryCompaction) -> None:
        """Allocate per-host accounting; never share mutable auxiliary budgets."""
        self.config = config
        self.attempts: list[SummaryAttempt] = []
        self.pending = False
        self._accepted: _Accepted | None = None
        self.decisions: list[str] = []

    def protect(self, messages: tuple[PromptMessage, ...]) -> frozenset[int]:
        """Keep the configured recent exact window, including complete Tool blocks."""
        return frozenset(
            i
            for first, end in native_exchange_ranges(messages)[
                -self.config.recent_exchanges :
            ]
            for i in range(first, end)
        )

    async def project(  # noqa: C901, PLR0911, PLR0912, PLR0913, PLR0915 -- bounded auxiliary stages and explicit fallback
        self,
        original: ModelRequest,
        fallback: ProjectionOutcome,
        *,
        protected: frozenset[int],
        sources: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
        snapshot: str,
        project: Callable[[frozenset[int], PromptMessage], ProjectionOutcome],
    ) -> ProjectionOutcome:
        """Keep a usable fallback unless a validated, affordable summary is adopted."""
        messages = original.prompt.messages
        prefix = tuple(
            digest(json.dumps(record(m), ensure_ascii=False)) for m in messages
        )
        fallback = self._reuse(
            messages,
            prefix,
            snapshot,
            protected,
            project,
            fallback=fallback,
        )
        if not self.pending and self.config.adaptive is not None:
            self._automatic(self.config.adaptive, messages, fallback)
        if not self.pending:
            return fallback

        self.pending = False
        attempt = SummaryAttempt(original_bytes=request_bytes(original))
        self.attempts.append(attempt)
        try:
            if sum(a.entered for a in self.attempts) >= self.config.maximum_calls:
                attempt.status = "call-budget-exhausted"
                return fallback
            request, refs, replacements, catalog = self._input(
                messages,
                protected,
                sources,
            )
            if not replacements:
                attempt.status = "no-eligible-input"
                return fallback
            attempt.input_indices = tuple(refs)
            attempt.replaced_indices = tuple(sorted(replacements))
            attempt.partial_coverage = len(refs) != len(messages)
            attempt.input_bytes = request_bytes(request)
            attempt.request_digest = digest(
                json.dumps(asdict(request), ensure_ascii=False),
            )
            if any(
                a.entered and a.request_digest == attempt.request_digest
                for a in self.attempts
            ):
                attempt.status = "prior-entry-not-replayed"
                return fallback
            if self.config.retain_payloads:
                attempt.request = request
            selected_source = self.config.interaction.source
            attempt.source = selected_source
            async with asyncio.timeout(self.config.timeout.total_seconds):
                if self.config.measure_input is not None:
                    tokens = await self.config.measure_input(request)
                    attempt.measured_input_tokens = tokens
                    ceiling = self.config.input_tokens
                    if (
                        type(tokens) is not int
                        or tokens < 0
                        or ceiling is None
                        or tokens > ceiling
                    ):
                        msg = "Summary input token capacity unavailable or exceeded."
                        raise ValueError(msg)  # noqa: TRY301 -- retain original strategy failure
                attempt.entered = True
                response = await self.config.interaction.send(request)
            attempt.response_received = True
            attempt.usage = response.usage
            if self.config.retain_payloads:
                attempt.response = response
            if (
                response.source != selected_source
                or response.termination != ModelTermination.NORMAL_STOP
                or response.tool_calls
                or not isinstance(response.content, str)
                or not response.content.strip()
                or len(response.content.encode()) > self.config.output_bytes
            ):
                msg = "Summary response is foreign, incomplete or outside its envelope."
                raise ValueError(msg)  # noqa: TRY301 -- retain strategy failure
            attempt.response_digest = digest(response.content)
            payload, attempt.normalized_json_fence = summary_payload(
                response.content,
                allow_json_fence=self.config.allow_json_fence,
            )
            summary = validate_summary(payload, refs, replacements, catalog)
            attempt.validated = True
            result = project(replacements, summary)
            attempt.resulting_bytes = result.resulting_bytes
            if (
                result.status == "insufficient"
                or result.resulting_bytes >= request_bytes(original)
            ):
                attempt.status = "insufficient-reduction"
                return fallback
            attempt.status, attempt.adopted = "adopted", True
            self._accepted = _Accepted(summary, replacements, prefix, snapshot)
            return result  # noqa: TRY300 -- adoption and receipt form one successful stage
        except asyncio.CancelledError as error:
            attempt.status, attempt.error = "cancelled", error
            raise
        except Exception as error:  # noqa: BLE001 -- retain original optional strategy failure
            attempt.status, attempt.error = "failed", error
            return fallback

    def _automatic(
        self,
        policy: AdaptiveCompaction,
        messages: tuple[PromptMessage, ...],
        fallback: ProjectionOutcome,
    ) -> None:
        """Schedule at most one bounded strategy; failures never create retry loops."""
        try:
            if self._accepted is not None:
                decision = "cached-summary"
            elif sum(a.entered for a in self.attempts) >= self.config.maximum_calls:
                decision = "auxiliary-budget-exhausted"
            elif any(a.status != "adopted" for a in self.attempts):
                decision = "prior-strategy-failure"
            else:
                decision = policy.assess(messages, fallback)
        except Exception as error:  # noqa: BLE001 -- optional host policy preserves fallback
            self.attempts.append(SummaryAttempt(status="policy-failed", error=error))
            decision = "policy-failed"
        self.decisions.append(decision)
        self.pending = decision == "semantic-requested"

    def _reuse(  # noqa: PLR0913 -- revalidate existing derived state against current authority
        self,
        messages: tuple[PromptMessage, ...],
        prefix: tuple[str, ...],
        snapshot: str,
        protected: frozenset[int],
        project: Callable[[frozenset[int], PromptMessage], ProjectionOutcome],
        *,
        fallback: ProjectionOutcome,
    ) -> ProjectionOutcome:
        accepted = self._accepted
        if accepted is None:
            return fallback
        try:
            if (
                prefix[: len(accepted.prefix)] == accepted.prefix
                and snapshot == accepted.snapshot
                and not protected.intersection(accepted.indices)
                and accepted.indices <= self.config.select(messages).replace
            ):
                reused = project(accepted.indices, accepted.message)
                if reused.status != "insufficient":
                    return reused
        except Exception as error:  # noqa: BLE001 -- qualified cache failure, no new model entry
            self.attempts.append(SummaryAttempt(status="reuse-failed", error=error))
        self._accepted = None
        return fallback

    def _input(
        self,
        messages: tuple[PromptMessage, ...],
        protected: frozenset[int],
        sources: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
    ) -> tuple[ModelRequest, dict[int, str], frozenset[int], dict[str, object]]:
        selection = self.config.select(messages)
        ranges = native_exchange_ranges(messages)
        eligible = frozenset(
            i
            for first, end in ranges
            if not protected.intersection(range(first, end))
            and set(range(first, end)) <= selection.replace
            for i in range(first, end)
        )
        if eligible != selection.replace or any(
            i >= len(messages) for i in selection.disclose
        ):
            msg = "Summary selection includes protected, partial or foreign history."
            raise ValueError(msg)
        records: dict[int, dict[str, object]] = {}
        replacements: set[int] = set()
        catalog: dict[str, object] = {}

        def build() -> ModelRequest:
            return ModelRequest(
                Prompt(
                    "",
                    "messages",
                    (
                        PromptMessage("system", INSTRUCTIONS),
                        PromptMessage(
                            "user",
                            json.dumps(
                                {
                                    "records": records,
                                    "replacement_indices": sorted(replacements),
                                    "historical_sources": catalog,
                                    "partial_coverage": len(records) != len(messages),
                                },
                                ensure_ascii=False,
                            ),
                        ),
                    ),
                ),
                settings=self.config.settings,
                provider_settings=self.config.provider_settings,
            )

        # Original order; native blocks stay whole. Oversized groups are excluded,
        # never relabeled as fully captured. No implicit source/policy export.
        groups = {first: tuple(range(first, end)) for first, end in ranges}
        covered = {i for group in groups.values() for i in group}
        groups.update({i: (i,) for i in range(len(messages)) if i not in covered})
        for group in (groups[i] for i in sorted(groups)):
            if not set(group) <= selection.disclose:
                continue
            old_records, old_replacements, old_catalog = (
                records.copy(),
                replacements.copy(),
                catalog.copy(),
            )
            for i in group:
                records[i] = record(messages[i])
                if i in eligible:
                    replacements.add(i)
                for option in sources.get(i, ()):
                    catalog[option.identity] = {
                        "path": str(option.unit.resource.address),
                        "repository": str(option.repository_id),
                        "snapshot": str(option.snapshot_id),
                        "content": str(option.unit.resource.content_identity),
                        "span": option.span,
                    }
            if request_bytes(build()) > self.config.input_bytes:
                records, replacements, catalog = (
                    old_records,
                    old_replacements,
                    old_catalog,
                )
        request = build()
        if request_bytes(request) > self.config.input_bytes:
            msg = "Summary instructions cannot fit the input envelope."
            raise ValueError(msg)
        refs = {i: str(value["digest"]) for i, value in records.items()}
        return request, refs, frozenset(replacements), catalog
