# Copyright (c) 2026
"""One model-neutral bounded source/edit/check/repair process."""

from __future__ import annotations

import asyncio
from dataclasses import replace
from typing import TYPE_CHECKING, Literal, Protocol

from devtools.agents.coding.models import (
    CodingCompletion,
    CodingDisposition,
    CodingEffect,
    CodingLimitError,
    CodingLimits,
    CodingProgress,
    CodingResult,
)
from devtools.models.interaction import ModelTermination

if TYPE_CHECKING:
    from devtools.models.interaction import (
        ModelInteraction,
        ModelRequest,
        ModelResponse,
    )


class CodingHost[Proposal](Protocol):
    """Coding policy/effect and presentation boundary, exercised by two hosts.

    Implementations use existing Tool composition and claim_action before Tool
    dispatch. They do not own another model/repair loop. Effect admission and
    custody remain host decisions; callbacks must never retry unknown effects.
    """

    native_feedback: bool

    async def prepare(self, progress: CodingProgress) -> ModelRequest:
        """Project bounded current Context and host-selected Tools/settings."""

    async def receive(self, response: ModelResponse) -> None:
        """Retain response facts before semantic source admission."""

    def classify(self, response: ModelResponse) -> Literal["acquire", "edit", "stop"]:
        """Select only host-admitted operation families; never infer authority."""

    async def acquire(self, response: ModelResponse) -> bool:
        """Dispatch bounded Tools and return current completion-check acceptance."""

    async def propose(self, response: ModelResponse) -> Proposal | None:
        """Admit a whole grounded proposal, or retain pre-effect refusal feedback."""

    async def apply(self, proposal: Proposal) -> None:
        """Apply once through host effect owners and verify installed source."""

    async def check(self, proposal: Proposal) -> bool:
        """Run required fixed checks; refuse invalid/unknown source correspondence."""

    async def feedback(
        self,
        response: ModelResponse,
        proposal: Proposal,
        *,
        passed: bool,
    ) -> None:
        """Retain bounded feedback without changing known validation facts."""

    async def finish(self, result: CodingResult) -> CodingCompletion:
        """Reconcile host custody and terminal projection without publication."""


async def run_coding_agent[Proposal](  # noqa: C901, PLR0912, PLR0915 -- one bounded coding phase sequence
    interaction: ModelInteraction,
    *,
    limits: CodingLimits,
    host: CodingHost[Proposal],
) -> CodingResult:
    """Pursue one bounded coding objective with no retry of an ambiguous effect.

    Request/capacity policy, scope/Tool selection, oracles, journals and Checkout
    belong to the supplied host. This owner enforces the coding phase order,
    model/proposal bounds, selected-source validation and terminal reconciliation.
    """
    state = CodingProgress(limits)
    disposition: CodingDisposition = "model_limit"
    error: BaseException | None = None
    try:
        async with asyncio.timeout(limits.wall_timeout.total_seconds):
            for number in range(1, limits.model_calls + 1):
                state.number, state.phase = number, "preparation"
                request = await host.prepare(state)
                selected_source = interaction.source
                state.phase = "model"
                state.model_calls += 1
                state.usage.append(None)
                async with asyncio.timeout(limits.call_timeout.total_seconds):
                    response = await interaction.send(request)
                state.usage[-1] = response.usage
                state.phase = "response"
                await host.receive(response)
                if response.source != selected_source:
                    msg = (
                        "Model response source does not match model interaction source."
                    )
                    raise ValueError(msg)  # noqa: TRY301 -- preserve the actual failure phase
                kind = host.classify(response)
                if response.termination == ModelTermination.OUTPUT_LIMIT:
                    msg = "Output limit: no repair dispatch"
                    raise ValueError(msg)  # noqa: TRY301 -- preserve the actual failure phase
                if kind == "stop":
                    disposition = "stopped"
                    break
                if host.native_feedback:
                    ids = [c.provider_call_id for c in response.tool_calls]
                    if not ids or not all(ids) or len(set(ids)) != len(ids):
                        msg = "Native calls require distinct nonempty IDs"
                        raise CodingLimitError(msg)  # noqa: TRY301 -- refuse before dispatch
                if kind == "acquire":
                    state.phase = "acquisition"
                    if await host.acquire(response):
                        state.candidate_validated = True
                        disposition = "validated"
                        break
                    continue
                state.phase = "admission"
                if state.proposals >= limits.proposals:
                    msg = "Edit proposal budget exhausted"
                    raise CodingLimitError(msg)  # noqa: TRY301 -- refuse before dispatch
                state.proposals += 1
                proposal = await host.propose(response)
                if proposal is None:
                    if state.proposals >= limits.proposals:
                        disposition = "proposal_limit"
                        break
                    continue
                state.candidate_validated = False
                effect = CodingEffect(
                    "edit",
                    tuple(c.provider_call_id for c in response.tool_calls),
                )
                state.effects.append(effect)
                state.phase = "application"
                await host.apply(proposal)
                effect.acknowledged = True
                state.phase = "validation"
                passed = await host.check(proposal)
                state.candidate_validated = passed
                state.phase = "feedback"
                await host.feedback(response, proposal, passed=passed)
                if passed and not limits.completion_check:
                    disposition = "validated"
                    break
                if not passed and state.proposals >= limits.proposals:
                    disposition = "proposal_limit"
                    break
    except (Exception, asyncio.CancelledError) as failure:  # noqa: BLE001 -- return known facts, never retry provider/effects
        disposition = (
            "cancelled" if isinstance(failure, asyncio.CancelledError) else "failed"
        )
        error = failure
    result = CodingResult(
        disposition,
        state.candidate_validated,
        error is None,
        state,
        error,
    )
    if error is not None:
        result = replace(result, failure_phase=state.phase)
    state.phase = "completion"
    try:
        custody = await host.finish(result)
        if (
            custody.error is not None
            or custody.reconciliation_required
            or custody.restored is False
        ):
            return replace(
                result,
                custody=custody,
                completed=False,
                disposition="reconciliation_required"
                if custody.reconciliation_required
                else "cancelled"
                if isinstance(error or custody.error, asyncio.CancelledError)
                else "failed",
                error=error or custody.error,
                completion_error=custody.error,
                failure_phase=result.failure_phase or "completion",
            )
        return replace(result, custody=custody)
    except (Exception, asyncio.CancelledError) as failure:  # noqa: BLE001 -- primary error remains authoritative
        return replace(
            result,
            completed=False,
            disposition="cancelled"
            if isinstance(error or failure, asyncio.CancelledError)
            else "failed",
            error=error or failure,
            completion_error=failure,
            failure_phase=result.failure_phase or "completion",
        )
