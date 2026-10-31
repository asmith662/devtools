# Copyright (c) 2026
"""Independent auxiliary script; original facts are checked before emitting notes."""

from __future__ import annotations

import json

from devtools.agents.coding.compaction import SummaryCompaction, SummarySelection
from devtools.core.time import Duration
from devtools.models.interaction import (
    InteractionSource,
    ModelRequest,
    ModelResponse,
    ModelSettings,
    ModelTermination,
)


class RepairSummary:
    """A separate non-Qwen model identity with literal expected failure evidence."""

    source = InteractionSource("independent-repair-summary")

    def __init__(self) -> None:
        """Retain authored test requests for independent consumption checks."""
        self.requests: list[ModelRequest] = []

    async def send(self, request: ModelRequest) -> ModelResponse:
        """Verify check/source facts, then return a scripted interpretation."""
        self.requests.append(request)
        value = json.loads(request.prompt.messages[1].content)
        records = value["records"]
        feedback = json.loads(records["5"]["message"]["content"])
        assert feedback["passed"] is False
        assert feedback["checks"][0]["exit_code"] == 1
        assert "return 8" in feedback["sources"][0]["text"]
        return ModelResponse(
            json.dumps(
                {
                    "version": 1,
                    "notes": [
                        {
                            "kind": "rejected_hypothesis",
                            "text": (
                                "Return 8 failed the fixed check. "
                                "Preserve unrelated source; repair the "
                                "current return value to the required integer 7."
                            ),
                            "refs": [
                                {"index": int(i), "digest": record["digest"]}
                                for i, record in records.items()
                            ],
                        },
                    ],
                    "sources": list(value["historical_sources"]),
                },
            ),
            self.source,
            termination=ModelTermination.NORMAL_STOP,
        )


def configuration(model: RepairSummary) -> SummaryCompaction:
    """Authorize only acquired records; keep current failed-check exchange exact."""
    return SummaryCompaction(
        model,
        lambda _: SummarySelection(frozenset({2, 3, 4, 5}), frozenset({2, 3})),
        1,
        20000,
        4096,
        ModelSettings(maximum_output_tokens=512),
        Duration.seconds(2),
    )
