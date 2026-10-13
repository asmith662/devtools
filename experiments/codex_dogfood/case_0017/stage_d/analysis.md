# Case 0017 — Stage D direct structural discrimination

Frozen category: **NO_MATERIAL_STRUCTURAL_DISCRIMINATION_SIGNAL**. No actual rank movement.

| Obligation | A R/H/U | Supported R/H/U | Supported useful | Baseline useful | REQUIRED coverage | B/N/H | Strong B/H |
|---|---|---|---|---|---|---|---|
| O1 | 2/8/86 | 0/1/1 | 1/2 | 10/96 | 0/2 | 1/1/0 | 0/0 |
| O2 | 2/8/114 | 0/1/4 | 1/5 | 10/124 | 0/2 | 1/4/0 | 0/0 |
| O3 | 3/14/167 | 0/1/5 | 1/6 | 17/184 | 0/3 | 1/5/0 | 0/0 |

R/H/U = REQUIRED / HELPFUL_ONLY / UNNECESSARY. B/N/H = BENEFICIAL / NEUTRAL / HARMFUL. Rates are descriptive, not causal improvement.

## Case totals

```json
{
  "A_candidate_occurrences": 404,
  "A_gold_labels": {
    "HELPFUL_ONLY": 30,
    "REQUIRED": 7,
    "UNNECESSARY": 367
  },
  "baseline_A_useful_candidate_occurrences": 37,
  "baseline_A_useful_rate": {
    "denominator": 404,
    "numerator": 37,
    "proportion": 0.09158415841584158
  },
  "distinct_source_target_obligation_pairs": 16,
  "local_pairs": 13,
  "pair_counts": {
    "BENEFICIAL": 3,
    "HARMFUL": 0,
    "NEUTRAL": 10,
    "STRONG_BENEFICIAL": 0,
    "STRONG_HARMFUL": 0
  },
  "qualifying_support_occurrences": 84,
  "required_in_A": 7,
  "required_in_A_support_coverage": {
    "denominator": 7,
    "numerator": 0,
    "proportion": 0.0
  },
  "supported_REQUIRED_in_A": 0,
  "supported_gold_labels": {
    "HELPFUL_ONLY": 3,
    "REQUIRED": 0,
    "UNNECESSARY": 10
  },
  "supported_targets": 13,
  "supported_useful_rate": {
    "denominator": 13,
    "numerator": 3,
    "proportion": 0.23076923076923078
  },
  "supported_useful_target_occurrences": 3,
  "unsupported_REQUIRED_in_A": 7
}
```


Captured self References: 1287; primary contribution = 0.

## Exact join validation

```json
{
  "A_ablation_identity": "PASS",
  "a_gold_cell_joins": 404,
  "frame_obligation_resource_document_content": "EXACT",
  "gold_cells": 1071,
  "join_defects": 0,
  "predecessor_gold_cell_joins": 13,
  "qualifying_occurrences": 84,
  "status": "PASS",
  "supporting_source_gold_cell_joins": 16,
  "target_gold_cell_joins": 13
}
```


## O1 coverage and diagnostics

FROZEN GOLD INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 887200,
    "canonical_a_ns": 20173900,
    "complete_online_equivalent_ns": 107019100,
    "predecessor_pairs_ns": 44500,
    "support_projection_ns": 85913500
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 2,
        "median": 2,
        "min": 2,
        "n": 1,
        "values": [
          2
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
        "max": 23,
        "median": 23,
        "min": 23,
        "n": 1,
        "values": [
          23
        ]
      },
      "native_occurrence_count": {
        "max": 2,
        "median": 2,
        "min": 2,
        "n": 1,
        "values": [
          2
        ]
      },
      "rank_distance": {
        "max": 31,
        "median": 31,
        "min": 31,
        "n": 1,
        "values": [
          31
        ]
      },
      "target_lexical_rank": {
        "max": 33,
        "median": 33,
        "min": 33,
        "n": 1,
        "values": [
          33
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
        "max": 89,
        "median": 89,
        "min": 89,
        "n": 1,
        "values": [
          89
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
        "max": 5,
        "median": 5,
        "min": 5,
        "n": 1,
        "values": [
          5
        ]
      },
      "native_occurrence_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
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
        "max": 95,
        "median": 95,
        "min": 95,
        "n": 1,
        "values": [
          95
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "AGENTS.md",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "src/devtools/context/retrieval/lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/291",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/retrieval/test_lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/810",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 0,
      "UNNECESSARY": 1
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 0,
      "UNNECESSARY": 1
    },
    "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
  }
}
```


## O2 coverage and diagnostics

FROZEN GOLD INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 1430000,
    "canonical_a_ns": 21624100,
    "complete_online_equivalent_ns": 106710900,
    "predecessor_pairs_ns": 46000,
    "support_projection_ns": 83610800
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
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
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
        ]
      },
      "native_occurrence_count": {
        "max": 1,
        "median": 1,
        "min": 1,
        "n": 1,
        "values": [
          1
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
        "max": 8,
        "median": 8,
        "min": 8,
        "n": 1,
        "values": [
          8
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
        "max": 116,
        "median": 61.0,
        "min": 23,
        "n": 4,
        "values": [
          23,
          42,
          80,
          116
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1.0,
        "min": 1,
        "n": 4,
        "values": [
          1,
          1,
          1,
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 41,
        "median": 23.0,
        "min": 7,
        "n": 4,
        "values": [
          7,
          21,
          25,
          41
        ]
      },
      "native_occurrence_count": {
        "max": 12,
        "median": 1.5,
        "min": 1,
        "n": 4,
        "values": [
          1,
          1,
          2,
          12
        ]
      },
      "rank_distance": {
        "max": 42,
        "median": 24.5,
        "min": 8,
        "n": 4,
        "values": [
          8,
          23,
          26,
          42
        ]
      },
      "target_lexical_rank": {
        "max": 124,
        "median": 95.0,
        "min": 46,
        "n": 4,
        "values": [
          46,
          68,
          122,
          124
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "AGENTS.md",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "src/devtools/context/retrieval/lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/292",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/retrieval/test_lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/811",
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
      "HELPFUL_ONLY": 1,
      "REQUIRED": 0,
      "UNNECESSARY": 16
    },
    "scope": "SECONDARY/DESCRIPTIVE; no eligibility filtering"
  }
}
```


## O3 coverage and diagnostics

FROZEN GOLD INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 1498100,
    "canonical_a_ns": 18243000,
    "complete_online_equivalent_ns": 112298900,
    "predecessor_pairs_ns": 46600,
    "support_projection_ns": 92511200
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 7,
        "median": 7,
        "min": 7,
        "n": 1,
        "values": [
          7
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
        "max": 71,
        "median": 71,
        "min": 71,
        "n": 1,
        "values": [
          71
        ]
      },
      "native_occurrence_count": {
        "max": 2,
        "median": 2,
        "min": 2,
        "n": 1,
        "values": [
          2
        ]
      },
      "rank_distance": {
        "max": 79,
        "median": 79,
        "min": 79,
        "n": 1,
        "values": [
          79
        ]
      },
      "target_lexical_rank": {
        "max": 86,
        "median": 86,
        "min": 86,
        "n": 1,
        "values": [
          86
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
        "max": 82,
        "median": 53,
        "min": 15,
        "n": 5,
        "values": [
          15,
          19,
          53,
          79,
          82
        ]
      },
      "distinct_supporting_source_count": {
        "max": 2,
        "median": 1,
        "min": 1,
        "n": 5,
        "values": [
          1,
          1,
          1,
          1,
          2
        ]
      },
      "intervening_unnecessary": {
        "max": 118,
        "median": 19,
        "min": 9,
        "n": 5,
        "values": [
          9,
          15,
          19,
          79,
          118
        ]
      },
      "native_occurrence_count": {
        "max": 22,
        "median": 10,
        "min": 2,
        "n": 5,
        "values": [
          2,
          7,
          10,
          21,
          22
        ]
      },
      "rank_distance": {
        "max": 125,
        "median": 22,
        "min": 11,
        "n": 5,
        "values": [
          11,
          16,
          22,
          86,
          125
        ]
      },
      "target_lexical_rank": {
        "max": 144,
        "median": 101,
        "min": 69,
        "n": 5,
        "values": [
          69,
          90,
          101,
          104,
          144
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "AGENTS.md",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "AGENTS.md",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "AGENTS.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/2",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/retrieval/lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/293",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/retrieval/test_lexical.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/812",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 0,
      "UNNECESSARY": 6
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 0,
      "UNNECESSARY": 62
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
      "max": 7,
      "median": 5,
      "min": 2,
      "n": 3,
      "values": [
        2,
        5,
        7
      ]
    },
    "distinct_supporting_source_count": {
      "max": 2,
      "median": 2,
      "min": 1,
      "n": 3,
      "values": [
        1,
        2,
        2
      ]
    },
    "intervening_unnecessary": {
      "max": 71,
      "median": 23,
      "min": 1,
      "n": 3,
      "values": [
        1,
        23,
        71
      ]
    },
    "native_occurrence_count": {
      "max": 2,
      "median": 2,
      "min": 1,
      "n": 3,
      "values": [
        1,
        2,
        2
      ]
    },
    "rank_distance": {
      "max": 79,
      "median": 31,
      "min": 3,
      "n": 3,
      "values": [
        3,
        31,
        79
      ]
    },
    "target_lexical_rank": {
      "max": 86,
      "median": 33,
      "min": 8,
      "n": 3,
      "values": [
        8,
        33,
        86
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
      "max": 116,
      "median": 66.0,
      "min": 15,
      "n": 10,
      "values": [
        15,
        19,
        23,
        42,
        53,
        79,
        80,
        82,
        89,
        116
      ]
    },
    "distinct_supporting_source_count": {
      "max": 2,
      "median": 1.0,
      "min": 1,
      "n": 10,
      "values": [
        1,
        1,
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
      "max": 118,
      "median": 20.0,
      "min": 5,
      "n": 10,
      "values": [
        5,
        7,
        9,
        15,
        19,
        21,
        25,
        41,
        79,
        118
      ]
    },
    "native_occurrence_count": {
      "max": 22,
      "median": 4.5,
      "min": 1,
      "n": 10,
      "values": [
        1,
        1,
        1,
        2,
        2,
        7,
        10,
        12,
        21,
        22
      ]
    },
    "rank_distance": {
      "max": 125,
      "median": 22.5,
      "min": 6,
      "n": 10,
      "values": [
        6,
        8,
        11,
        16,
        22,
        23,
        26,
        42,
        86,
        125
      ]
    },
    "target_lexical_rank": {
      "max": 144,
      "median": 98.0,
      "min": 46,
      "n": 10,
      "values": [
        46,
        68,
        69,
        90,
        95,
        101,
        104,
        122,
        124,
        144
      ]
    }
  }
}
```


## Source gold — secondary/descriptive

```json
{
  "distinct_source_target_obligation_pairs": {
    "HELPFUL_ONLY": 5,
    "REQUIRED": 0,
    "UNNECESSARY": 11
  },
  "qualifying_occurrences": {
    "HELPFUL_ONLY": 5,
    "REQUIRED": 0,
    "UNNECESSARY": 79
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
