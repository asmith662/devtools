# Copyright (c) 2026
"""Deterministic coding-input selection over retained native facts and Context."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from typing import TYPE_CHECKING, Literal

from devtools.context.planning.source import (
    SourceRangeDisclosureOption,
    materialize_source_range,
)
from devtools.models.interaction import ModelRequest, Prompt, PromptMessage
from devtools.tools.source import source_read_bounds

if TYPE_CHECKING:
    from collections.abc import Mapping

    from devtools.context.repository.snapshot import RepositorySnapshot


def request_bytes(request: ModelRequest) -> int:
    """Count complete host serialization, not provider tokens or HTTP bytes."""
    return len(json.dumps(asdict(request), ensure_ascii=False).encode())


def native_exchange_ranges(
    messages: tuple[PromptMessage, ...],
) -> tuple[tuple[int, int], ...]:
    """Validate Prompt and locate indivisible assistant/result blocks.

    User/system instructions are never included in an evictable range. This
    operation neither selects content nor invokes an operation from history.
    """
    Prompt("", "messages", messages)
    ranges = []
    for index, message in enumerate(messages):
        if message.role == "assistant":
            end = index + 1
            while end < len(messages) and messages[end].role == "tool":
                end += 1
            ranges.append((index, end))
    return tuple(ranges)


@dataclass(frozen=True, slots=True)
class ProjectionPolicy:
    """Host-selected byte watermarks and known metadata-only operation names.

    Operation names permit presentation omission, never execution. Unknown
    operations and non-Tool assistant text remain protected.
    Optional source status is a bounded host annotation charged to the same
    complete-request budget; it never becomes retained history or a witness.
    """

    trigger_bytes: int
    target_bytes: int
    metadata_operations: frozenset[str] = frozenset()
    report_source_state: bool = False

    def __post_init__(self) -> None:
        """Require explicit bounded watermarks and immutable host classification."""
        if (
            type(self.trigger_bytes) is not int
            or type(self.target_bytes) is not int
            or not 0 < self.target_bytes <= self.trigger_bytes
            or not isinstance(self.metadata_operations, frozenset)
            or type(self.report_source_state) is not bool
            or any(
                not isinstance(n, str) or not n.strip()
                for n in self.metadata_operations
            )
        ):
            msg = "Invalid active Context projection policy."
            raise ValueError(msg)


@dataclass(frozen=True, slots=True)
class ProjectionOutcome:
    """Transient projection facts; not a task result or durable execution receipt."""

    request: ModelRequest
    status: Literal["unchanged", "reduced", "insufficient"]
    triggered: bool
    original_bytes: int
    resulting_bytes: int
    target_bytes: int
    hard_bytes: int
    selected_indices: tuple[int, ...]
    omitted_exchanges: tuple[tuple[int, int, str], ...]
    shortened_indices: tuple[int, ...]
    active_sources: tuple[SourceRangeDisclosureOption, ...]
    invalidated_source_identities: tuple[str, ...]

    @property
    def target_reached(self) -> bool:
        """Distinguish usable headroom from merely fitting the hard ceiling."""
        return self.resulting_bytes <= self.target_bytes


class ProjectionCapacityError(ValueError):
    """No permitted active representation fits; original facts remain retained."""

    def __init__(self, outcome: ProjectionOutcome) -> None:
        """Retain the qualified decision without exposing private Tool payloads."""
        self.outcome = outcome
        super().__init__(
            f"Active Context cannot fit protected input: "
            f"{outcome.resulting_bytes} bytes > {outcome.hard_bytes}.",
        )


def source_feedback(
    option: SourceRangeDisclosureOption,
    text: str,
) -> dict[str, object]:
    """Project one already materialized exact range into the neutral native format."""
    bounds = source_read_bounds(option)
    # The native descriptor defines coordinates; do not repeat that prose in
    # every disclosure, especially a capacity-limited partial projection.
    del bounds["coordinate_convention"]
    return {
        **bounds,
        "continuation_start": option.start + len(text),
        "remaining_range": [option.start + len(text), option.unit.end],
        "text": text,
        "path": str(option.unit.resource.address),
        "snapshot": str(option.snapshot_id),
        "version": str(option.unit.resource.content_identity),
        "span": option.span,
        "partial": option.truncated,
    }


def _current_sources(
    messages: tuple[PromptMessage, ...],
    sources: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
    snapshot: RepositorySnapshot,
) -> dict[int, tuple[SourceRangeDisclosureOption, ...]]:
    """Authenticate host bindings against actually presented text and Context."""
    current = {}
    for index, options in sources.items():
        value = json.loads(messages[index].content)
        presented = value.get("sources", [value])
        selected = []
        for option in options:
            if (
                option.snapshot_id != snapshot.id
                or option.repository_id != snapshot.repository_id
            ):
                continue
            materialized = materialize_source_range(snapshot, option).items[0]
            expected = {
                "text": materialized.text,
                "path": str(option.unit.resource.address),
                "version": str(option.unit.resource.content_identity),
                "span": list(option.span),
            }
            if not any(
                all(v.get(k) == item for k, item in expected.items())
                and v.get("snapshot", str(snapshot.id)) == str(snapshot.id)
                for v in presented
            ):
                msg = "Source binding does not match presented Context."
                raise ValueError(msg)
            selected.append(option)
        current[index] = tuple(selected)
    return current


def _source_state(
    selected: Mapping[int, PromptMessage],
    current: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
    sources: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
    previous: tuple[SourceRangeDisclosureOption, ...],
) -> PromptMessage:
    """Describe available source facts, not inferred intent or new authority."""
    active = {o.identity: o for i in selected for o in current.get(i, ())}
    records = [i for i, values in current.items() if values]
    latest = max(records) if records else None
    acquisition: dict[str, object] | None = None
    if latest is not None:
        observed = next(
            o
            for o in sources[latest]
            if o.unit == current[latest][0].unit and o.start == current[latest][0].start
        )

        def same_source(other: SourceRangeDisclosureOption) -> bool:
            return (
                other.repository_id == observed.repository_id
                and other.snapshot_id == observed.snapshot_id
                and other.unit.resource == observed.unit.resource
            )

        acquisition = {
            "path": str(observed.unit.resource.address),
            "span": observed.span,
            "earlier_same_range_disclosures": sum(
                same_source(o) and o.span == observed.span
                for i in records
                if i < latest
                for o in sources[i]
            ),
            "covered_by_one_previous_disclosure": any(
                same_source(o)
                and o.span[0] <= observed.span[0] <= observed.span[1] <= o.span[1]
                for o in previous
            ),
        }
    return PromptMessage(
        "user",
        json.dumps(
            {
                "kind": "active_source_status",
                "scope": "current repository/snapshot; metadata is not source",
                "coordinates": "half-open Unicode offsets",
                "active_ranges": [
                    {
                        "path": str(o.unit.resource.address),
                        "snapshot": str(o.snapshot_id),
                        "version": str(o.unit.resource.content_identity),
                        "span": o.span,
                    }
                    for o in list(active.values())[-4:]
                ],
                "active_list_partial": len(active) > 4,  # noqa: PLR2004 -- bounded status rows
                "omitted_current_disclosure_records": sum(
                    i not in selected for i in records
                ),
                "latest_current_disclosure": acquisition,
                "instruction": (
                    "Only exact source presented here can ground edits. Historical "
                    "acquisition is not active evidence. Continuation offsets are "
                    "optional, not a requirement to read whole files. Select missing "
                    "methods/windows, propose a grounded edit or request an authorized "
                    "check when ready, or stop with a specific blocker. Repeating "
                    "an identical active range adds no source information."
                ),
            },
            ensure_ascii=False,
        ),
    )


def project_request(  # noqa: C901, PLR0912, PLR0913, PLR0915 -- bounded ordered selection, no effect execution
    request: ModelRequest,
    *,
    policy: ProjectionPolicy,
    hard_bytes: int,
    snapshot: RepositorySnapshot,
    sources: Mapping[int, tuple[SourceRangeDisclosureOption, ...]],
    protected_indices: frozenset[int] = frozenset(),
    previous_sources: tuple[SourceRangeDisclosureOption, ...] = (),
    summarized_indices: frozenset[int] = frozenset(),
    summary: PromptMessage | None = None,
) -> ProjectionOutcome:
    """Select complete exchanges and affordable exact source without editing history.

    Cheap reductions target the lower watermark. Distinct current source is
    sacrificed only under hard pressure. Newest feedback cannot be dropped;
    a plain source result may instead be explicitly presented as a partial range.
    Source bindings, not native roles, distinguish host disclosures from user
    instructions. Only their exact source fields are replaced; other fields
    remain verbatim. Protected source/check messages cannot be shortened.
    Unclassified exchanges
    are retained, including all effectful operations and unknown outcomes.
    """
    if not 0 < policy.target_bytes <= policy.trigger_bytes <= hard_bytes:
        msg = "Projection watermarks exceed the host byte ceiling."
        raise ValueError(msg)
    messages = request.prompt.messages
    ranges = native_exchange_ranges(messages)
    ids = [c.provider_call_id for m in messages for c in m.tool_calls]
    if len(ids) != len(set(ids)):
        msg = "Active native history repeats a Tool call ID."
        raise ValueError(msg)
    current = _current_sources(messages, sources, snapshot)
    selected = dict(enumerate(messages))
    original = request_bytes(request)
    omitted: list[tuple[int, int, str]] = []
    shortened: list[int] = []
    if summarized_indices or summary is not None:
        eligible = {
            i
            for first, end in ranges[:-1]
            if not protected_indices.intersection(range(first, end))
            and set(range(first, end)) <= summarized_indices
            for i in range(first, end)
        }
        if (
            not summarized_indices
            or eligible != summarized_indices
            or summary is None
            or summary.role != "assistant"
            or not summary.content.strip()
            or summary.tool_calls
            or summary.tool_call_id is not None
            or summary.reasoning_content is not None
        ):
            msg = "Semantic projection must replace whole unprotected exchanges."
            raise ValueError(msg)
        for first, end in ranges:
            if first in summarized_indices:
                omitted.append((first, end, "semantic-summary"))
        for i in summarized_indices:
            del selected[i]
    # Only bound plain source results can be shortened or classified as reads.
    plain = {
        i
        for i, options in sources.items()
        if len(options) == 1 and "text" in json.loads(messages[i].content)
    }

    def assembled() -> ModelRequest:
        active = tuple(selected.values())
        if summary is not None:
            active += (summary,)
        if policy.report_source_state:
            active += (_source_state(selected, current, sources, previous_sources),)
        return replace(request, prompt=Prompt("", "messages", active))

    def size() -> int:
        return request_bytes(assembled())

    candidates = []
    for first, end in ranges:
        block = messages[first:end]
        if (
            first not in selected
            or (first, end) == ranges[-1]
            or any(i in protected_indices for i in range(first, end))
            or not block[0].tool_calls
            or any(
                i not in plain
                and next(
                    c.name
                    for c in block[0].tool_calls
                    if c.provider_call_id == messages[i].tool_call_id
                )
                not in policy.metadata_operations
                for i in range(first + 1, end)
            )
        ):
            continue
        options = tuple(o for i in range(first, end) for o in current.get(i, ()))
        later = tuple(o for i, values in current.items() if i >= end for o in values)
        if options and all(
            any(
                o.unit.resource == other.unit.resource
                and other.span[0] <= o.span[0] <= o.span[1] <= other.span[1]
                for other in later
            )
            for o in options
        ):
            priority, reason = 0, "duplicate-current-source"
        elif any(i in plain for i in range(first, end)):
            priority, reason = (
                (2, "source-capacity") if options else (0, "stale-source")
            )
        else:
            priority, reason = 1, "host-classified-metadata"
        candidates.append((priority, first, end, reason))
    triggered = (
        size() if policy.report_source_state else original
    ) > policy.trigger_bytes
    if triggered:
        for priority, first, end, reason in sorted(candidates):
            if size() <= policy.target_bytes:
                break
            if priority == 2 and size() <= hard_bytes:  # noqa: PLR2004 -- distinct current source tier
                break
            for i in range(first, end):
                del selected[i]
            omitted.append((first, end, reason))
        # Older bound disclosures yield first, including host-selected user
        # source. Retain savings across disclosures: a single reduction need
        # not make the whole request affordable. No subset search is needed.
        for index in sorted(plain):
            if size() <= hard_bytes:
                break
            if (
                index not in selected
                or index in protected_indices
                or not current[index]
            ):
                continue
            option = current[index][0]
            if not option.text:
                continue
            original_message = selected[index]
            before = size()

            def partial(
                budget: int,
                *,
                option: SourceRangeDisclosureOption = option,
                original_message: PromptMessage = original_message,
                index: int = index,
            ) -> SourceRangeDisclosureOption:
                smaller = replace(option, maximum_bytes=budget)
                text = materialize_source_range(snapshot, smaller).items[0].text
                value = {
                    **json.loads(original_message.content),
                    **source_feedback(smaller, text),
                }
                value["presentation"] = {
                    "reason": "active-context-capacity",
                    "original_message_sha256": hashlib.sha256(
                        original_message.content.encode(),
                    ).hexdigest(),
                    "acquired_span": option.span,
                    "acquired_partial": option.truncated,
                }
                selected[index] = replace(
                    original_message,
                    content=json.dumps(value, ensure_ascii=False),
                )
                current[index] = (smaller,)
                return smaller

            minimum = len(option.text[0].encode())
            maximum = len(option.text.encode())
            partial(minimum)
            if size() >= before:
                selected[index] = original_message
                current[index] = (option,)
                continue
            shortened.append(index)
            target = (
                policy.target_bytes if size() <= policy.target_bytes else hard_bytes
            )
            if size() > target:
                # Keep this useful reduction while trying the next disclosure.
                # An insufficient final outcome is never installed by the host.
                continue
            low, high = minimum, maximum
            while low < high:
                middle = (low + high + 1) // 2
                partial(middle)
                if size() <= target:
                    low = middle
                else:
                    high = middle - 1
            current[index] = (partial(low),)
    active = tuple(o for i in selected for o in current.get(i, ()))
    active_ids = {o.identity for o in active}
    projected = assembled()
    resulting = request_bytes(projected)
    return ProjectionOutcome(
        projected,
        "insufficient"
        if resulting > hard_bytes
        else "unchanged"
        if projected == request
        else "reduced",
        triggered,
        original,
        resulting,
        policy.target_bytes,
        hard_bytes,
        tuple(selected),
        tuple(omitted),
        tuple(shortened),
        active,
        tuple(
            dict.fromkeys(
                o.identity
                for values in sources.values()
                for o in values
                if o.identity not in active_ids
            ),
        ),
    )
