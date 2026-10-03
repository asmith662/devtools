"""Focused deterministic checks for the frozen Stage D join."""

from __future__ import annotations

import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).with_name("analyze.py")
SPEC = importlib.util.spec_from_file_location("case_0006_analyze", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
ANALYZE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ANALYZE)


def test_frozen_join_metrics_and_counterfactual() -> None:
    result = ANALYZE.main_analysis()
    assert result["joins"]["resources_joined"] == 531
    assert result["joins"]["judgment_cells_joined"] == 5310
    assert result["joins"]["routed_candidates_total"] == 2069
    assert result["global_native_bm25"]["task_complete_obligation_depth"] == 155
    assert (
        result["own_obligation_native"]["obligation_wise_maximum_completion_depth"]
        == 58
    )
    assert result["role_routed"]["obligation_wise_maximum_completion_position"] == 195
    assert result["actual_generation"]["generated_hypotheses"] == 0
    assert result["actual_generation"]["generated_required_precision"] is None
    counterfactual = result["counterfactual_diagnostic_not_observed_treatment_output"]
    assert counterfactual["generated_hypotheses"] == 8
    assert counterfactual["generated_member_occurrences"] == 13
    assert counterfactual["unresolved_mirror_member_targets"] == 1
    assert counterfactual["required_resource_cell_coverage"] == 12
    assert counterfactual["unique_required_resources_covered"] == 7
    assert result["miss_classification"]["primary_counts_no_double_count"] == {
        "GROUNDING_UNSUPPORTED": 12,
        "NO_RECIPE": 8,
        "OPERATOR_CAPABILITY_GAP": 8,
    }
