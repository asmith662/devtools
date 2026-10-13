# Case 0019 — Stage D direct structural discrimination

Frozen category: **NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL**. No actual rank movement.

| Obligation | A R/H/U | Supported R/H/U | Supported useful | Baseline useful | REQUIRED coverage | B/N/H | Strong B/H |
|---|---|---|---|---|---|---|---|
| O1 | 1/10/36 | 1/1/0 | 2/2 | 11/47 | 1/1 | 1/1/0 | 0/0 |
| O2 | 1/11/63 | 0/1/5 | 1/6 | 12/75 | 0/1 | 0/6/0 | 0/0 |
| O3 | 1/11/118 | 0/1/3 | 1/4 | 12/130 | 0/1 | 0/4/0 | 0/0 |

R/H/U = REQUIRED / HELPFUL_ONLY / UNNECESSARY. B/N/H = BENEFICIAL / NEUTRAL / HARMFUL. Rates are descriptive, not causal improvement.

## Case totals

```json
{
  "A_candidate_occurrences": 252,
  "A_gold_labels": {
    "HELPFUL_ONLY": 32,
    "REQUIRED": 3,
    "UNNECESSARY": 217
  },
  "baseline_A_useful_candidate_occurrences": 35,
  "baseline_A_useful_rate": {
    "denominator": 252,
    "numerator": 35,
    "proportion": 0.1388888888888889
  },
  "distinct_source_target_obligation_pairs": 14,
  "local_pairs": 12,
  "pair_counts": {
    "BENEFICIAL": 1,
    "HARMFUL": 0,
    "NEUTRAL": 11,
    "STRONG_BENEFICIAL": 0,
    "STRONG_HARMFUL": 0
  },
  "qualifying_support_occurrences": 126,
  "required_in_A": 3,
  "required_in_A_support_coverage": {
    "denominator": 3,
    "numerator": 1,
    "proportion": 0.3333333333333333
  },
  "supported_REQUIRED_in_A": 1,
  "supported_gold_labels": {
    "HELPFUL_ONLY": 3,
    "REQUIRED": 1,
    "UNNECESSARY": 8
  },
  "supported_targets": 12,
  "supported_useful_rate": {
    "denominator": 12,
    "numerator": 4,
    "proportion": 0.3333333333333333
  },
  "supported_useful_target_occurrences": 4,
  "unsupported_REQUIRED_in_A": 2
}
```


Captured self References: 940; primary contribution = 0.

## Exact join validation

```json
{
  "A_ablation_identity": "PASS",
  "a_gold_cell_joins": 252,
  "frame_obligation_resource_document_content": "EXACT",
  "gold_cells": 666,
  "join_defects": 0,
  "predecessor_gold_cell_joins": 12,
  "qualifying_occurrences": 126,
  "status": "PASS",
  "supporting_source_gold_cell_joins": 14,
  "target_gold_cell_joins": 12
}
```


## O1 coverage and diagnostics

CONDITIONAL REPOSITORY-INTEGRATION INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 603300,
    "canonical_a_ns": 10808300,
    "complete_online_equivalent_ns": 44725300,
    "predecessor_pairs_ns": 37000,
    "support_projection_ns": 33276700
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 1,
        "values": [
          3
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "native_occurrence_count": {
        "max": 14,
        "median": 14,
        "min": 14,
        "n": 1,
        "values": [
          14
        ]
      },
      "rank_distance": {
        "max": 6,
        "median": 6,
        "min": 6,
        "n": 1,
        "values": [
          6
        ]
      },
      "target_lexical_rank": {
        "max": 9,
        "median": 9,
        "min": 9,
        "n": 1,
        "values": [
          9
        ]
      }
    },
    "REQUIRED": {
      "best_supporting_source_rank": {
        "max": 5,
        "median": 5,
        "min": 5,
        "n": 1,
        "values": [
          5
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 0,
        "median": 0,
        "min": 0,
        "n": 1,
        "values": [
          0
        ]
      },
      "native_occurrence_count": {
        "max": 12,
        "median": 12,
        "min": 12,
        "n": 1,
        "values": [
          12
        ]
      },
      "rank_distance": {
        "max": 2,
        "median": 2,
        "min": 2,
        "n": 1,
        "values": [
          2
        ]
      },
      "target_lexical_rank": {
        "max": 7,
        "median": 7,
        "min": 7,
        "n": 1,
        "values": [
          7
        ]
      }
    },
    "UNNECESSARY": {
      "best_supporting_source_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "distinct_supporting_source_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "intervening_unnecessary": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "native_occurrence_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "rank_distance": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "target_lexical_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "tests/model_serving/test_vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": true,
      "unsupported": false
    }
  ],
  "required_cells": [
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/276",
      "structurally_supported": true,
      "unsupported": false
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 0,
      "UNNECESSARY": 0
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 26,
      "REQUIRED": 0,
      "UNNECESSARY": 0
    },
    "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
  }
}
```


## O2 coverage and diagnostics

CONDITIONAL REPOSITORY-INTEGRATION INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 909500,
    "canonical_a_ns": 18971000,
    "complete_online_equivalent_ns": 51230600,
    "predecessor_pairs_ns": 47900,
    "support_projection_ns": 31302200
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "distinct_supporting_source_count": {
        "max": 2,
        "median": 2,
        "min": 2,
        "n": 1,
        "values": [
          2
        ]
      },
      "intervening_unnecessary": {
        "max": 0,
        "median": 0,
        "min": 0,
        "n": 1,
        "values": [
          0
        ]
      },
      "native_occurrence_count": {
        "max": 32,
        "median": 32,
        "min": 32,
        "n": 1,
        "values": [
          32
        ]
      },
      "rank_distance": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 1,
        "values": [
          3
        ]
      },
      "target_lexical_rank": {
        "max": 4,
        "median": 4,
        "min": 4,
        "n": 1,
        "values": [
          4
        ]
      }
    },
    "REQUIRED": {
      "best_supporting_source_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "distinct_supporting_source_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "intervening_unnecessary": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "native_occurrence_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "rank_distance": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "target_lexical_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      }
    },
    "UNNECESSARY": {
      "best_supporting_source_rank": {
        "max": 37,
        "median": 29,
        "min": 24,
        "n": 5,
        "values": [
          24,
          26,
          29,
          37,
          37
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 5,
        "values": [
          1,
          1,
          1,
          1,
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 43,
        "median": 25,
        "min": 5,
        "n": 5,
        "values": [
          5,
          13,
          25,
          36,
          43
        ]
      },
      "native_occurrence_count": {
        "max": 14,
        "median": 2,
        "min": 1,
        "n": 5,
        "values": [
          1,
          1,
          2,
          7,
          14
        ]
      },
      "rank_distance": {
        "max": 47,
        "median": 28,
        "min": 7,
        "n": 5,
        "values": [
          7,
          15,
          28,
          40,
          47
        ]
      },
      "target_lexical_rank": {
        "max": 71,
        "median": 57,
        "min": 44,
        "n": 5,
        "values": [
          44,
          52,
          57,
          66,
          71
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/model_serving/test_vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/277",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 3,
      "REQUIRED": 1,
      "UNNECESSARY": 3
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 30,
      "REQUIRED": 10,
      "UNNECESSARY": 17
    },
    "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
  }
}
```


## O3 coverage and diagnostics

CONDITIONAL REPOSITORY-INTEGRATION INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 1048800,
    "canonical_a_ns": 12022500,
    "complete_online_equivalent_ns": 49705600,
    "predecessor_pairs_ns": 16800,
    "support_projection_ns": 36617500
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 1,
        "values": [
          3
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 0,
        "median": 0,
        "min": 0,
        "n": 1,
        "values": [
          0
        ]
      },
      "native_occurrence_count": {
        "max": 10,
        "median": 10,
        "min": 10,
        "n": 1,
        "values": [
          10
        ]
      },
      "rank_distance": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "target_lexical_rank": {
        "max": 4,
        "median": 4,
        "min": 4,
        "n": 1,
        "values": [
          4
        ]
      }
    },
    "REQUIRED": {
      "best_supporting_source_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "distinct_supporting_source_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "intervening_unnecessary": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "native_occurrence_count": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "rank_distance": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      },
      "target_lexical_rank": {
        "max": null,
        "median": null,
        "min": null,
        "n": 0,
        "values": []
      }
    },
    "UNNECESSARY": {
      "best_supporting_source_rank": {
        "max": 51,
        "median": 38,
        "min": 35,
        "n": 3,
        "values": [
          35,
          38,
          51
        ]
      },
      "distinct_supporting_source_count": {
        "max": 2,
        "median": 1,
        "min": 1,
        "n": 3,
        "values": [
          1,
          1,
          2
        ]
      },
      "intervening_unnecessary": {
        "max": 28,
        "median": 12,
        "min": 11,
        "n": 3,
        "values": [
          11,
          12,
          28
        ]
      },
      "native_occurrence_count": {
        "max": 18,
        "median": 11,
        "min": 4,
        "n": 3,
        "values": [
          4,
          11,
          18
        ]
      },
      "rank_distance": {
        "max": 29,
        "median": 13,
        "min": 12,
        "n": 3,
        "values": [
          12,
          13,
          29
        ]
      },
      "target_lexical_rank": {
        "max": 64,
        "median": 63,
        "min": 51,
        "n": 3,
        "values": [
          51,
          63,
          64
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/model_serving/vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/model_serving/test_vllm.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/model_serving/test_vllm.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "tests/model_serving/test_vllm.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/584",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 1,
      "REQUIRED": 0,
      "UNNECESSARY": 4
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 10,
      "REQUIRED": 0,
      "UNNECESSARY": 33
    },
    "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
  }
}
```


## Structural characteristics by target label

```json
{
  "HELPFUL_ONLY": {
    "best_supporting_source_rank": {
      "max": 3,
      "median": 3,
      "min": 1,
      "n": 3,
      "values": [
        1,
        3,
        3
      ]
    },
    "distinct_supporting_source_count": {
      "max": 2,
      "median": 1,
      "min": 1,
      "n": 3,
      "values": [
        1,
        1,
        2
      ]
    },
    "intervening_unnecessary": {
      "max": 1,
      "median": 0,
      "min": 0,
      "n": 3,
      "values": [
        0,
        0,
        1
      ]
    },
    "native_occurrence_count": {
      "max": 32,
      "median": 14,
      "min": 10,
      "n": 3,
      "values": [
        10,
        14,
        32
      ]
    },
    "rank_distance": {
      "max": 6,
      "median": 3,
      "min": 1,
      "n": 3,
      "values": [
        1,
        3,
        6
      ]
    },
    "target_lexical_rank": {
      "max": 9,
      "median": 4,
      "min": 4,
      "n": 3,
      "values": [
        4,
        4,
        9
      ]
    }
  },
  "REQUIRED": {
    "best_supporting_source_rank": {
      "max": 5,
      "median": 5,
      "min": 5,
      "n": 1,
      "values": [
        5
      ]
    },
    "distinct_supporting_source_count": {
      "max": 1,
      "median": 1,
      "min": 1,
      "n": 1,
      "values": [
        1
      ]
    },
    "intervening_unnecessary": {
      "max": 0,
      "median": 0,
      "min": 0,
      "n": 1,
      "values": [
        0
      ]
    },
    "native_occurrence_count": {
      "max": 12,
      "median": 12,
      "min": 12,
      "n": 1,
      "values": [
        12
      ]
    },
    "rank_distance": {
      "max": 2,
      "median": 2,
      "min": 2,
      "n": 1,
      "values": [
        2
      ]
    },
    "target_lexical_rank": {
      "max": 7,
      "median": 7,
      "min": 7,
      "n": 1,
      "values": [
        7
      ]
    }
  },
  "UNNECESSARY": {
    "best_supporting_source_rank": {
      "max": 51,
      "median": 36.0,
      "min": 24,
      "n": 8,
      "values": [
        24,
        26,
        29,
        35,
        37,
        37,
        38,
        51
      ]
    },
    "distinct_supporting_source_count": {
      "max": 2,
      "median": 1.0,
      "min": 1,
      "n": 8,
      "values": [
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2
      ]
    },
    "intervening_unnecessary": {
      "max": 43,
      "median": 19.0,
      "min": 5,
      "n": 8,
      "values": [
        5,
        11,
        12,
        13,
        25,
        28,
        36,
        43
      ]
    },
    "native_occurrence_count": {
      "max": 18,
      "median": 5.5,
      "min": 1,
      "n": 8,
      "values": [
        1,
        1,
        2,
        4,
        7,
        11,
        14,
        18
      ]
    },
    "rank_distance": {
      "max": 47,
      "median": 21.5,
      "min": 7,
      "n": 8,
      "values": [
        7,
        12,
        13,
        15,
        28,
        29,
        40,
        47
      ]
    },
    "target_lexical_rank": {
      "max": 71,
      "median": 60.0,
      "min": 44,
      "n": 8,
      "values": [
        44,
        51,
        52,
        57,
        63,
        64,
        66,
        71
      ]
    }
  }
}
```


## Source gold — secondary/descriptive

```json
{
  "distinct_source_target_obligation_pairs": {
    "HELPFUL_ONLY": 6,
    "REQUIRED": 1,
    "UNNECESSARY": 7
  },
  "qualifying_occurrences": {
    "HELPFUL_ONLY": 66,
    "REQUIRED": 10,
    "UNNECESSARY": 50
  },
  "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
}
```


## Limitations

- Three historical DEVELOPMENT cases; no statistical significance claim or formal cohort success gate.
- Structural candidate universe == A. No lexically absent REQUIRED evidence can be rescued here; no graph expansion or structural-only candidate utility is tested. Unsupported lexical misses are baseline non-reach, not structural failure.
- Actual rankings are unchanged. Local predecessor pairs are COUNTERFACTUAL DIAGNOSTICS ONLY; no rank gain/regression, witness-depth change or burden change is claimed.
- Supported-useful rates are descriptive discrimination evidence, not causal improvement. Gold labels of sources do not change frozen eligibility.
- Native resolved direct cross-resource References only; bounded/non-exhaustive resolution, no self-support, no independent Imports/Calls treatment, no multi-hop/PPR/RRF.
- One designated GPT-6 Astra / High primary per case; deterministic verification is not independent semantic validation. Host routing is not independently verified. No second reviewer or reconciliation.
- Case 0017 same-primary corrections R092/O2 and R268/O2 REQUIRED -> HELPFUL_ONLY and retired proposed unit are authoritative.
- Case 0018 TASK_INTERPRETATION_GAP = RESOLVED_WITH_EXPLICIT_QUALIFICATION; TASK_GAP = OPEN_DESIGN_FREEDOM_NOT_UNRESOLVED_CELL; REPOSITORY_INFORMATION_GAP = BOUNDED_LIMITATION_NO_BLOCKING_SUPPORT_GAP. Frozen O1-O3 remain evaluable.
- Case 0019 repository-integration judgments are CONDITIONAL on unresolved future provider-contract semantics: option spelling, value domain, version applicability and default behavior. TASK_INTERPRETATION_GAP remains PRESENT. Unconditional future task satisfaction has zero complete witnesses/combinations, empty sufficient unions, undefined ranges and indispensability. The conditional two-resource union does not close this gap. Pair classification remains valid within the frozen obligation interpretation.
- No production policy, structural score, threshold, rank movement or next experiment is authorized by this diagnostic. Historical child implementations/paths/diffs, confirmation and reserve remain unopened.

Every pair and exact supporting fact is inspectable in TRACE.md / trace.json. Gold evidence uses original primary cell pointers; no evidence quotes are reproduced.
