# Copyright (c) 2026
# ruff: noqa: ANN001, D103, INP001, S101, SLF001
"""Case-specific safety checks for immutable Stage B capture."""

from __future__ import annotations

from pathlib import Path

import capture
import pytest


def test_existing_output_refuses_before_any_treatment_call(
    tmp_path,
    monkeypatch,
) -> None:
    """An existing output blocks before native acquisition or any later call."""
    monkeypatch.setattr(capture, "CASE", tmp_path)
    (tmp_path / "capture.pkl.gz").write_bytes(b"existing")

    def treatment_must_not_run(_request) -> None:
        pytest.fail("Capture called production after discovering existing output.")

    monkeypatch.setattr(
        capture,
        "acquire_localization_lexical_evidence",
        treatment_must_not_run,
    )
    with pytest.raises(FileExistsError, match="Stage B outputs already exist"):
        capture.execute()


def test_member_correspondence_uses_identity_not_constructor_order() -> None:
    """Canonical constructor order does not change frozen member identity."""
    expected = {"left", "right"}
    actual = {"right": object(), "left": object()}
    capture._validate_member_keys(expected, actual)


@pytest.mark.parametrize(
    "actual",
    [{"left": object()}, {"left": object(), "other": object()}],
)
def test_member_correspondence_rejects_identity_mismatch(actual) -> None:
    with pytest.raises(ValueError, match="member identities"):
        capture._validate_member_keys({"left", "right"}, actual)


def test_recovery_policy_has_one_additional_execution() -> None:
    assert capture.RECOVERY_ID == "case-0006-stage-b-recovery-1"
    assert capture.PRIOR_FAILED_EXECUTION_COUNT == 1
    assert (
        capture._execution_decision(
            raw_exists=False,
            started_exists=False,
            outputs=(),
        )
        == "EXECUTE"
    )


def test_raw_capture_forces_resume_and_blocks_reexecution_without_raw() -> None:
    assert (
        capture._execution_decision(
            raw_exists=True,
            started_exists=True,
            outputs=(),
        )
        == "RESUME"
    )
    with pytest.raises(FileExistsError, match="already started"):
        capture._execution_decision(
            raw_exists=False,
            started_exists=True,
            outputs=(),
        )


def test_recovery_raw_is_marked_incomplete_and_carries_native_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(capture, "CASE", tmp_path)
    state = {"native": {"frozen": True}, "invocations": {"lexical_acquisition": 1}}
    capture._save_raw(state)
    restored = capture._load_raw()
    assert restored is not None
    assert restored["native"] == {"frozen": True}
    assert restored["recovery_metadata"] == {
        "execution_kind": "RECOVERY",
        "recovery_id": capture.RECOVERY_ID,
        "prior_failed_execution_count": 1,
        "stage_a_commit": capture.STAGE_A,
        "invocation_counts": {"lexical_acquisition": 1},
        "status": "INCOMPLETE_UNVALIDATED",
    }
    assert (
        capture._execution_decision(
            raw_exists=True,
            started_exists=True,
            outputs=(),
        )
        == "RESUME"
    )


def test_corrupt_or_non_incomplete_raw_is_rejected(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(capture, "CASE", tmp_path)
    (tmp_path / capture.RAW_CAPTURE).write_bytes(b"not-pickle")
    with pytest.raises((OSError, ValueError, EOFError)):
        capture._load_raw()


def test_canonical_outputs_are_exclusive(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(capture, "CASE", tmp_path)
    with pytest.raises(FileExistsError, match="Stage B outputs"):
        capture._execution_decision(
            raw_exists=True,
            started_exists=True,
            outputs=("capture.pkl.gz",),
        )


def test_canonical_artifacts_require_validation_and_refuse_overwrite(
    tmp_path: Path,
    monkeypatch,
) -> None:
    monkeypatch.setattr(capture, "CASE", tmp_path)
    payloads = dict.fromkeys(capture.OUTPUTS, b"validated")
    with pytest.raises(ValueError, match="require successful validation"):
        capture._publish_outputs(payloads, validated=False)
    if tuple(tmp_path.iterdir()):
        pytest.fail("Unvalidated canonical outputs were created.")
    capture._publish_outputs(payloads, validated=True)
    with pytest.raises(FileExistsError, match="already exist"):
        capture._publish_outputs(payloads, validated=True)


def test_attempt_record_freezes_prior_failure_and_no_execution_in_this_checkpoint() -> (
    None
):
    case = Path(capture.__file__).parent
    record = (case / "stage_b_attempt_1.json").read_text(encoding="utf-8")
    assert '"distinct_grounding_requests": 9' in record
    assert '"generation": 1' in record
    assert '"native_results_survived": false' in record
    protocol = (case / "stage_b_recovery_protocol.md").read_text(encoding="utf-8")
    assert "Maximum additional treatment executions: **1**" in protocol
    assert "do not retry" in protocol
