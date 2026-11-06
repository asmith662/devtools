# Copyright (c) 2026
"""Finite first-slice scientific accounting, distinct from cost prediction."""

from dataclasses import dataclass, field

from devtools.core.time import Stopwatch
from devtools.learning.investigation.plans import LearningPlan

LIMITS = {
    "native_fits": 9,
    "states": 10,
    "preparations": 8,
    "squares": 3,
    "actions": 8,
    "invocations": 8,
}


@dataclass
class LearningBudget:
    """One caller-owned two-hour root account; failed effects do not refund slots."""

    limits: dict[str, int] = field(default_factory=lambda: dict(LIMITS))
    consumed: dict[str, int] = field(default_factory=lambda: dict.fromkeys(LIMITS, 0))
    _clock: Stopwatch = field(default_factory=Stopwatch, init=False, repr=False)

    def __post_init__(self) -> None:
        """A caller can narrow the reviewed envelope but cannot enlarge it."""
        if (
            set(self.limits) != set(LIMITS)
            or any(
                type(v) is not int or not 0 <= v <= LIMITS[k]
                for k, v in self.limits.items()
            )
            or self.consumed != dict.fromkeys(LIMITS, 0)
        ):
            msg = "fresh bounded first-slice learning account required"
            raise ValueError(msg)

    def remaining_seconds(self) -> float:
        """Expose an enforceable deadline, never a prediction of incremental cost."""
        return max(0.0, 7200 - self._clock.elapsed.total_seconds)

    def admit_envelope(self, menus: tuple[tuple[str, ...], ...]) -> dict[str, int]:
        """Prove the worst-case finite plan, including final scoring, before entry."""
        maximum = dict.fromkeys(LIMITS, 0)
        for menu in menus:
            if not menu or len(set(menu)) != len(menu):
                msg = "finite unique methods required for the envelope"
                raise ValueError(msg)
            count = len(menu)
            fits = sum(m != "mean" for m in menu)
            squares = sum(m.startswith("square-") for m in menu)
            for key, value in {
                "native_fits": fits + int(fits > 0),
                "preparations": fits + int(fits > 0),
                "squares": squares + int(squares > 0),
                "states": count + 1,
                "invocations": count + 1,
                "actions": count + 1,
            }.items():
                maximum[key] += value
        if any(self.consumed[k] + maximum[k] > self.limits[k] for k in LIMITS):
            msg = "the exact proposed investigation exceeds the reviewed count envelope"
            raise ValueError(
                msg,
            )
        # Per invocation: packet <=16MiB, one member <=32MiB, ledger+journal <=8MiB,
        # retained streams <1MiB. Host selection/support records reserve another MiB.
        if maximum["invocations"] * (57 << 20) + (1 << 20) > 512 << 20:
            msg = "scientific storage envelope exceeds 512MiB"
            raise ValueError(msg)
        return maximum

    def reserve(self, plan: LearningPlan | None) -> None:
        """Reserve atomically before execution; no retry/refund follows ambiguity."""
        increment = dict.fromkeys(LIMITS, 0)
        if plan is None:
            increment["actions"] = 1
        else:
            increment.update(
                native_fits=int(plan.method != "mean"),
                states=1,
                preparations=int(plan.method != "mean"),
                squares=int(plan.method.startswith("square-")),
                actions=int(plan.phase == "online"),
                invocations=1,
            )
        if not self.remaining_seconds() or any(
            self.consumed[k] + increment[k] > self.limits[k] for k in LIMITS
        ):
            msg = "learning execution budget exhausted"
            raise ValueError(msg)
        self.consumed = {k: self.consumed[k] + increment[k] for k in LIMITS}
