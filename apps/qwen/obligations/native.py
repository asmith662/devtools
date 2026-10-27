# Copyright (c) 2026
"""Native request projection and pre-edit admission for one trusted frame."""

from __future__ import annotations

import json
from dataclasses import replace
from typing import TYPE_CHECKING, Any

from apps.qwen.obligations.assessment import assess, interpretation
from apps.qwen.patch_proposal_worker import PatchProposalError
from devtools.context.localization import (
    LocalizationLexicalAcquisitionRequest,
    LocalizationQueryIdentity,
    ObligationLexicalQuery,
    acquire_localization_lexical_evidence,
)

if TYPE_CHECKING:
    from apps.qwen.context_tools import ContextTools
    from apps.qwen.obligations.frame import ObligationFrame
    from devtools.context.localization import LocalizationLexicalAcquisition
    from devtools.models.interaction import PromptMessage

MAX_STATUS_BYTES = 12000


class ReadinessRefusalError(PatchProposalError):
    """Preserve explicit unresolved criteria in existing proposal feedback."""

    def __init__(self, status: dict[str, Any]) -> None:
        """Refuse before mutation while allowing bounded authorized acquisition."""
        super().__init__(
            "Required Context obligations remain unresolved. Acquire the named "
            "exact current ranges using existing read/search Tools; relevance "
            "is not support. Do not change the host frame or scope. "
            "Exhaustion never satisfies a requirement.",
            details={"code": "CONTEXT_NOT_READY", **status},
        )


class NativeObligations:
    """Compose existing kernels; own no task authority, Tools or source state."""

    def __init__(self, frame: ObligationFrame, tools: ContextTools) -> None:
        """Admit the host's frame against the exact native task and source scope."""
        frame.validate(tools.task)
        self.frame, self.tools = frame, tools
        self.acquisition: LocalizationLexicalAcquisition | None = None
        self.messages: tuple[PromptMessage, ...] = ()
        self.status: dict[str, Any] = {}

    def _assess(self) -> bool:
        self.tools.check_current()
        if (
            self.acquisition is None
            or self.acquisition.snapshot_id != self.tools.snapshot.id
        ):
            task = interpretation(self.frame, self.tools)
            self.acquisition = acquire_localization_lexical_evidence(
                LocalizationLexicalAcquisitionRequest(
                    task,
                    self.tools.task.objective,
                    self.tools.task.objective,
                    tuple(
                        ObligationLexicalQuery(
                            LocalizationQueryIdentity(task.identity, spec.key),
                            obligation.identity,
                            spec.query,
                        )
                        for spec, obligation in zip(
                            self.frame.obligations,
                            task.obligations,
                            strict=True,
                        )
                    ),
                    self.tools.snapshot,
                    self.tools.index.views[0].lexical_index,
                    len(self.tools.addresses),
                ),
            )
        readiness, self.status = assess(
            self.frame,
            self.tools,
            self.messages,
            self.acquisition,
        )
        if len(json.dumps(self.status, ensure_ascii=False).encode()) > MAX_STATUS_BYTES:
            msg = "Obligation Context status exceeds existing bounded response size"
            raise ValueError(msg)
        return readiness.is_ready

    def project(self, messages: tuple[PromptMessage, ...]) -> tuple[PromptMessage, ...]:
        """Assess the actual selected source before presentation/token counting."""
        self.messages = messages
        self._assess()
        return (
            replace(
                messages[0],
                content=messages[0].content
                + "\nHOST OBLIGATION CONTEXT (source-changing action only):\n"
                + json.dumps(self.status, ensure_ascii=False),
            ),
            *messages[1:],
        )

    def retain(self, stage: dict[str, Any], report: dict[str, Any]) -> None:
        """Retain the exact request-time assessment without claiming durability."""
        stage["obligation_context"] = self.status
        report["obligation_context"] = self.status

    def admit(self, stage: dict[str, Any], report: dict[str, Any]) -> None:
        """Reauthenticate source and require READY before ordinary edit admission."""
        ready = self._assess()
        self.retain(stage, report)
        if not ready:
            raise ReadinessRefusalError(self.status)
        stage["edit_context_assessment"] = self.status["assessment_sha256"]
