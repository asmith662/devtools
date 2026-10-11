# Case 0014 R1.7 analysis

Outcome: **QUERY_TERM_WEIGHTING_HARMFUL**

Full discrimination improves some selected witness depths and prefix burdens, but the frozen rule rejects its unbounded REQUIRED-cell regressions. The ranking outcome uses C versus A exclusively.

[Complete human review](STAGE_D_REVIEW.md) includes every REQUIRED cell and every witness in each arm. [analysis.json](analysis.json) owns complete deterministic arithmetic and captured attribution joins.


## DID R1.7 IMPROVE?

```json
{
  "candidate_safety": {
    "A": "PRESERVED",
    "C": "PRESERVED",
    "classification": "TIED",
    "differences": 0
  },
  "distinct_utf8_bytes": {
    "A": 1585757,
    "C": 1159546,
    "C_minus_A": -426211,
    "classification": "IMPROVED"
  },
  "duplicate_occurrences": {
    "A": 53,
    "C": 33,
    "C_minus_A": -20,
    "classification": "IMPROVED"
  },
  "meaningful_required_cell_gains": {
    "A": 0,
    "C": 8,
    "C_minus_A": 8,
    "classification": "IMPROVED"
  },
  "meaningful_witness_gains": {
    "A": 0,
    "C": 2,
    "C_minus_A": 2,
    "classification": "IMPROVED"
  },
  "obligation_completeness": {
    "A": 6,
    "C": 6,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "obligation_indispensable_ranks": {
    "A": 65,
    "C": 39,
    "C_minus_A": -26,
    "cells": [
      {
        "address": "pyproject.toml",
        "change": {
          "arithmetic": {
            "five_treatment": 195,
            "four_baseline": 260,
            "gain_positions": 26,
            "regression_positions": -26,
            "six_baseline": 390
          },
          "baseline": 65,
          "bounded": true,
          "meaningful_rank_gain": true,
          "rank_delta_after_minus_before": -26,
          "state": "IMPROVED",
          "treatment": 39
        },
        "obligation": "O6",
        "ranks": {
          "A": 65,
          "B": 41,
          "C": 39
        }
      }
    ],
    "classification": "IMPROVED",
    "metric": "Sum of owning-obligation reached ranks; individual identities retained"
  },
  "prefix_occurrences": {
    "A": 249,
    "C": 151,
    "C_minus_A": -98,
    "classification": "IMPROVED"
  },
  "reference_lane_safety": {
    "A": "PRESERVED",
    "C": "PRESERVED",
    "classification": "TIED",
    "differences": 0
  },
  "required_cell_ranks_sum": {
    "A": 1151,
    "C": 1046,
    "C_minus_A": -105,
    "classification": "IMPROVED",
    "improved_cells": 13,
    "metric": "Sum of owning-obligation ranks, descriptive only; individual regression gates cannot be offset by aggregate gains",
    "regressed_cells": 10,
    "tied_cells": 11
  },
  "required_cell_regressions": {
    "A": 0,
    "C": 10,
    "C_minus_A": 10,
    "classification": "WORSENED",
    "unbounded_cells": 7
  },
  "required_cells_reach": {
    "A": 34,
    "C": 34,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "required_repository_units_reach": {
    "A": 11,
    "C": 11,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "required_resources_reach": {
    "A": 18,
    "C": 18,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "required_units_reach": {
    "A": 30,
    "C": 30,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "selected_witness_depth_per_obligation": {
    "O1": {
      "arithmetic": {
        "five_treatment": 5,
        "four_baseline": 4,
        "regression_positions": 0,
        "six_baseline": 6
      },
      "baseline": 1,
      "bounded": true,
      "classification": "TIED",
      "meaningful_witness_gain": false,
      "rank_delta_after_minus_before": 0,
      "state": "UNCHANGED",
      "treatment": 1
    },
    "O2": {
      "arithmetic": {
        "five_treatment": 5,
        "four_baseline": 4,
        "regression_positions": 0,
        "six_baseline": 6
      },
      "baseline": 1,
      "bounded": true,
      "classification": "TIED",
      "meaningful_witness_gain": false,
      "rank_delta_after_minus_before": 0,
      "state": "UNCHANGED",
      "treatment": 1
    },
    "O3": {
      "arithmetic": {
        "five_treatment": 5,
        "four_baseline": 4,
        "regression_positions": 0,
        "six_baseline": 6
      },
      "baseline": 1,
      "bounded": true,
      "classification": "TIED",
      "meaningful_witness_gain": false,
      "rank_delta_after_minus_before": 0,
      "state": "UNCHANGED",
      "treatment": 1
    },
    "O4": {
      "arithmetic": {
        "five_treatment": 5,
        "four_baseline": 4,
        "regression_positions": 0,
        "six_baseline": 6
      },
      "baseline": 1,
      "bounded": true,
      "classification": "TIED",
      "meaningful_witness_gain": false,
      "rank_delta_after_minus_before": 0,
      "state": "UNCHANGED",
      "treatment": 1
    },
    "O5": {
      "arithmetic": {
        "five_treatment": 540,
        "four_baseline": 720,
        "regression_positions": -72,
        "six_baseline": 1080
      },
      "baseline": 180,
      "bounded": true,
      "classification": "IMPROVED",
      "meaningful_witness_gain": true,
      "rank_delta_after_minus_before": -72,
      "state": "IMPROVED",
      "treatment": 108
    },
    "O6": {
      "arithmetic": {
        "five_treatment": 195,
        "four_baseline": 260,
        "regression_positions": -26,
        "six_baseline": 390
      },
      "baseline": 65,
      "bounded": true,
      "classification": "IMPROVED",
      "meaningful_witness_gain": true,
      "rank_delta_after_minus_before": -26,
      "state": "IMPROVED",
      "treatment": 39
    }
  },
  "semantic_completeness": {
    "A": 30,
    "C": 30,
    "C_minus_A": 0,
    "classification": "TIED"
  },
  "task_indispensable_ranks": {
    "A": 65,
    "C": 39,
    "C_minus_A": -26,
    "cells": [
      {
        "address": "pyproject.toml",
        "change": {
          "arithmetic": {
            "five_treatment": 195,
            "four_baseline": 260,
            "gain_positions": 26,
            "regression_positions": -26,
            "six_baseline": 390
          },
          "baseline": 65,
          "bounded": true,
          "meaningful_rank_gain": true,
          "rank_delta_after_minus_before": -26,
          "state": "IMPROVED",
          "treatment": 39
        },
        "obligation": "O6",
        "ranks": {
          "A": 65,
          "B": 41,
          "C": 39
        }
      }
    ],
    "classification": "IMPROVED",
    "metric": "Sum of owning-obligation reached ranks; individual identities retained"
  },
  "treatment_construction_cost_ns": {
    "A": 1747263700,
    "C": 1705909100,
    "C_minus_A": -41354600,
    "classification": "IMPROVED"
  },
  "unique_prefix_resources": {
    "A": 196,
    "C": 118,
    "C_minus_A": -78,
    "classification": "IMPROVED"
  },
  "unnecessary_occurrences": {
    "A": 223,
    "C": 129,
    "C_minus_A": -94,
    "classification": "IMPROVED"
  }
}
```


## Gate decisions and precedence

```json
{
  "gates": {
    "bounded_regressions": false,
    "burden_safe": true,
    "completion_safe": true,
    "depth_safe": true,
    "meaningful_obligation_indices": [
      4,
      5
    ],
    "outcome": "QUERY_TERM_WEIGHTING_HARMFUL",
    "required_rank_gain": true,
    "required_rank_safe": false,
    "ten_percent_burden_gain": true
  },
  "precedence": {
    "classification_application_or_reach_defect": false,
    "complementary_value": false,
    "contract_defect": false,
    "harmful_regression": true,
    "outcome": "QUERY_TERM_WEIGHTING_HARMFUL",
    "strong_support": false
  }
}
```

Single development case, one treatment-blind primary; no reliability inference or reconciliation. All alternatives remain authoritative. Prefix burden is counterfactual acquisition to reviewed completion, not measured human reading effort. Cost is single-run descriptive capture. No universal retrieval or production claim.
