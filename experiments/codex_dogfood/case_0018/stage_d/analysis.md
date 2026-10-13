# Case 0018 — Stage D direct structural discrimination

Frozen category: **STRUCTURAL_DISCRIMINATION_SIGNAL**. No actual rank movement.

| Obligation | A R/H/U | Supported R/H/U | Supported useful | Baseline useful | REQUIRED coverage | B/N/H | Strong B/H |
|---|---|---|---|---|---|---|---|
| O1 | 10/8/272 | 3/1/29 | 4/33 | 18/290 | 3/10 | 1/30/2 | 0/0 |
| O2 | 9/13/274 | 2/0/25 | 2/27 | 22/296 | 2/9 | 1/25/1 | 1/0 |
| O3 | 10/22/286 | 0/2/34 | 2/36 | 32/318 | 0/10 | 1/34/1 | 0/0 |

R/H/U = REQUIRED / HELPFUL_ONLY / UNNECESSARY. B/N/H = BENEFICIAL / NEUTRAL / HARMFUL. Rates are descriptive, not causal improvement.

## Case totals

```json
{
  "A_candidate_occurrences": 904,
  "A_gold_labels": {
    "HELPFUL_ONLY": 43,
    "REQUIRED": 29,
    "UNNECESSARY": 832
  },
  "baseline_A_useful_candidate_occurrences": 72,
  "baseline_A_useful_rate": {
    "denominator": 904,
    "numerator": 72,
    "proportion": 0.07964601769911504
  },
  "distinct_source_target_obligation_pairs": 188,
  "local_pairs": 96,
  "pair_counts": {
    "BENEFICIAL": 3,
    "HARMFUL": 4,
    "NEUTRAL": 89,
    "STRONG_BENEFICIAL": 1,
    "STRONG_HARMFUL": 0
  },
  "qualifying_support_occurrences": 1071,
  "required_in_A": 29,
  "required_in_A_support_coverage": {
    "denominator": 29,
    "numerator": 5,
    "proportion": 0.1724137931034483
  },
  "supported_REQUIRED_in_A": 5,
  "supported_gold_labels": {
    "HELPFUL_ONLY": 3,
    "REQUIRED": 5,
    "UNNECESSARY": 88
  },
  "supported_targets": 96,
  "supported_useful_rate": {
    "denominator": 96,
    "numerator": 8,
    "proportion": 0.08333333333333333
  },
  "supported_useful_target_occurrences": 8,
  "unsupported_REQUIRED_in_A": 24
}
```


Captured self References: 1416; primary contribution = 0.

## Exact join validation

```json
{
  "A_ablation_identity": "PASS",
  "a_gold_cell_joins": 904,
  "frame_obligation_resource_document_content": "EXACT",
  "gold_cells": 1146,
  "join_defects": 0,
  "predecessor_gold_cell_joins": 96,
  "qualifying_occurrences": 1071,
  "status": "PASS",
  "supporting_source_gold_cell_joins": 188,
  "target_gold_cell_joins": 96
}
```


## O1 coverage and diagnostics

FROZEN GOLD INDISPENSABILITY

```json
{
  "baseline_lexical_non_reach": [],
  "captured_timings_ns": {
    "annotation_construction_ns": 4171400,
    "canonical_a_ns": 27441200,
    "complete_online_equivalent_ns": 123288600,
    "predecessor_pairs_ns": 122400,
    "support_projection_ns": 91553600
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 30,
        "median": 30,
        "min": 30,
        "n": 1,
        "values": [
          30
        ]
      },
      "distinct_supporting_source_count": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 1,
        "values": [
          3
        ]
      },
      "intervening_unnecessary": {
        "max": 69,
        "median": 69,
        "min": 69,
        "n": 1,
        "values": [
          69
        ]
      },
      "native_occurrence_count": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 1,
        "values": [
          3
        ]
      },
      "rank_distance": {
        "max": 72,
        "median": 72,
        "min": 72,
        "n": 1,
        "values": [
          72
        ]
      },
      "target_lexical_rank": {
        "max": 102,
        "median": 102,
        "min": 102,
        "n": 1,
        "values": [
          102
        ]
      }
    },
    "REQUIRED": {
      "best_supporting_source_rank": {
        "max": 3,
        "median": 3,
        "min": 3,
        "n": 3,
        "values": [
          3,
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
        "max": 9,
        "median": 7,
        "min": 0,
        "n": 3,
        "values": [
          0,
          7,
          9
        ]
      },
      "native_occurrence_count": {
        "max": 28,
        "median": 14,
        "min": 12,
        "n": 3,
        "values": [
          12,
          14,
          28
        ]
      },
      "rank_distance": {
        "max": 20,
        "median": 12,
        "min": 1,
        "n": 3,
        "values": [
          1,
          12,
          20
        ]
      },
      "target_lexical_rank": {
        "max": 23,
        "median": 15,
        "min": 4,
        "n": 3,
        "values": [
          4,
          15,
          23
        ]
      }
    },
    "UNNECESSARY": {
      "best_supporting_source_rank": {
        "max": 162,
        "median": 97,
        "min": 3,
        "n": 29,
        "values": [
          3,
          29,
          33,
          33,
          35,
          42,
          45,
          46,
          47,
          51,
          59,
          75,
          80,
          84,
          97,
          97,
          97,
          97,
          105,
          114,
          116,
          120,
          120,
          128,
          130,
          135,
          139,
          145,
          162
        ]
      },
      "distinct_supporting_source_count": {
        "max": 5,
        "median": 1,
        "min": 1,
        "n": 29,
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
          1,
          1,
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          2,
          2,
          3,
          3,
          3,
          4,
          4,
          4,
          5,
          5
        ]
      },
      "intervening_unnecessary": {
        "max": 205,
        "median": 68,
        "min": 0,
        "n": 29,
        "values": [
          0,
          6,
          8,
          10,
          14,
          16,
          17,
          26,
          33,
          37,
          44,
          56,
          57,
          65,
          68,
          68,
          68,
          69,
          71,
          77,
          102,
          111,
          135,
          137,
          147,
          155,
          155,
          161,
          205
        ]
      },
      "native_occurrence_count": {
        "max": 65,
        "median": 5,
        "min": 1,
        "n": 29,
        "values": [
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          2,
          2,
          4,
          4,
          4,
          4,
          5,
          5,
          6,
          6,
          11,
          12,
          14,
          15,
          16,
          17,
          18,
          22,
          22,
          47,
          65
        ]
      },
      "rank_distance": {
        "max": 208,
        "median": 71,
        "min": 1,
        "n": 29,
        "values": [
          1,
          7,
          9,
          11,
          15,
          18,
          27,
          30,
          36,
          38,
          45,
          58,
          58,
          66,
          71,
          71,
          71,
          74,
          74,
          78,
          105,
          112,
          138,
          138,
          150,
          158,
          158,
          162,
          208
        ]
      },
      "target_lexical_rank": {
        "max": 283,
        "median": 155,
        "min": 33,
        "n": 29,
        "values": [
          33,
          46,
          51,
          62,
          78,
          100,
          103,
          116,
          117,
          121,
          131,
          133,
          144,
          151,
          155,
          164,
          169,
          172,
          177,
          206,
          209,
          211,
          235,
          242,
          247,
          255,
          258,
          282,
          283
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": true,
      "unsupported": false
    }
  ],
  "required_cells": [
    {
      "address": "docs/architecture.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/6",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/12",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/taxonomy.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/21",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/27",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/documentation_map.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/168",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/264",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "src/devtools/context/python/imports/resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/267",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "src/devtools/context/python/modules/interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/273",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "tests/context/python/imports/test_resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/831",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/python/modules/test_interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/837",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 2,
      "REQUIRED": 6,
      "UNNECESSARY": 57
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 3,
      "REQUIRED": 56,
      "UNNECESSARY": 311
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
    "annotation_construction_ns": 5877000,
    "canonical_a_ns": 26270100,
    "complete_online_equivalent_ns": 143145600,
    "predecessor_pairs_ns": 166900,
    "support_projection_ns": 110831600
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
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
    "REQUIRED": {
      "best_supporting_source_rank": {
        "max": 2,
        "median": 2.0,
        "min": 2,
        "n": 2,
        "values": [
          2,
          2
        ]
      },
      "distinct_supporting_source_count": {
        "max": 1,
        "median": 1.0,
        "min": 1,
        "n": 2,
        "values": [
          1,
          1
        ]
      },
      "intervening_unnecessary": {
        "max": 4,
        "median": 2.0,
        "min": 0,
        "n": 2,
        "values": [
          0,
          4
        ]
      },
      "native_occurrence_count": {
        "max": 15,
        "median": 13.5,
        "min": 12,
        "n": 2,
        "values": [
          12,
          15
        ]
      },
      "rank_distance": {
        "max": 11,
        "median": 6.0,
        "min": 1,
        "n": 2,
        "values": [
          1,
          11
        ]
      },
      "target_lexical_rank": {
        "max": 13,
        "median": 8.0,
        "min": 3,
        "n": 2,
        "values": [
          3,
          13
        ]
      }
    },
    "UNNECESSARY": {
      "best_supporting_source_rank": {
        "max": 257,
        "median": 75,
        "min": 2,
        "n": 25,
        "values": [
          2,
          10,
          10,
          11,
          48,
          48,
          48,
          75,
          75,
          75,
          75,
          75,
          75,
          103,
          103,
          108,
          131,
          139,
          152,
          169,
          185,
          191,
          208,
          208,
          257
        ]
      },
      "distinct_supporting_source_count": {
        "max": 5,
        "median": 2,
        "min": 1,
        "n": 25,
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
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          2,
          2,
          3,
          3,
          3,
          4,
          4,
          5,
          5
        ]
      },
      "intervening_unnecessary": {
        "max": 184,
        "median": 72,
        "min": 0,
        "n": 25,
        "values": [
          0,
          1,
          20,
          29,
          32,
          34,
          37,
          55,
          55,
          55,
          63,
          65,
          72,
          73,
          73,
          74,
          80,
          92,
          96,
          135,
          144,
          158,
          174,
          182,
          184
        ]
      },
      "native_occurrence_count": {
        "max": 65,
        "median": 5,
        "min": 1,
        "n": 25,
        "values": [
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          3,
          4,
          4,
          5,
          5,
          6,
          6,
          7,
          14,
          15,
          15,
          16,
          17,
          19,
          22,
          47,
          65
        ]
      },
      "rank_distance": {
        "max": 186,
        "median": 74,
        "min": 1,
        "n": 25,
        "values": [
          1,
          8,
          21,
          33,
          34,
          39,
          50,
          56,
          56,
          57,
          66,
          73,
          74,
          75,
          75,
          78,
          81,
          93,
          98,
          136,
          149,
          160,
          176,
          183,
          186
        ]
      },
      "target_lexical_rank": {
        "max": 291,
        "median": 208,
        "min": 10,
        "n": 25,
        "values": [
          10,
          11,
          60,
          82,
          87,
          89,
          124,
          132,
          150,
          173,
          197,
          206,
          208,
          212,
          235,
          239,
          243,
          251,
          257,
          261,
          264,
          278,
          289,
          290,
          291
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": true,
      "unsupported": false
    }
  ],
  "required_cells": [
    {
      "address": "docs/architecture.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/7",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/13",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/taxonomy.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/22",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/28",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/265",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "src/devtools/context/python/imports/resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/268",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/modules/interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/274",
      "structurally_supported": true,
      "unsupported": false
    },
    {
      "address": "tests/context/python/imports/test_resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/832",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/python/modules/test_interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/838",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 0,
      "REQUIRED": 3,
      "UNNECESSARY": 50
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 0,
      "REQUIRED": 28,
      "UNNECESSARY": 281
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
    "annotation_construction_ns": 5228300,
    "canonical_a_ns": 13981100,
    "complete_online_equivalent_ns": 122940700,
    "predecessor_pairs_ns": 226900,
    "support_projection_ns": 103504400
  },
  "evidence_characteristics": {
    "HELPFUL_ONLY": {
      "best_supporting_source_rank": {
        "max": 107,
        "median": 59.0,
        "min": 11,
        "n": 2,
        "values": [
          11,
          107
        ]
      },
      "distinct_supporting_source_count": {
        "max": 3,
        "median": 3.0,
        "min": 3,
        "n": 2,
        "values": [
          3,
          3
        ]
      },
      "intervening_unnecessary": {
        "max": 38,
        "median": 19.5,
        "min": 1,
        "n": 2,
        "values": [
          1,
          38
        ]
      },
      "native_occurrence_count": {
        "max": 4,
        "median": 3.5,
        "min": 3,
        "n": 2,
        "values": [
          3,
          4
        ]
      },
      "rank_distance": {
        "max": 57,
        "median": 30.0,
        "min": 3,
        "n": 2,
        "values": [
          3,
          57
        ]
      },
      "target_lexical_rank": {
        "max": 110,
        "median": 89.0,
        "min": 68,
        "n": 2,
        "values": [
          68,
          110
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
        "max": 286,
        "median": 102.0,
        "min": 35,
        "n": 34,
        "values": [
          35,
          35,
          35,
          35,
          53,
          53,
          54,
          59,
          61,
          64,
          66,
          66,
          66,
          79,
          83,
          94,
          101,
          103,
          119,
          124,
          127,
          130,
          133,
          138,
          142,
          165,
          171,
          171,
          177,
          178,
          214,
          215,
          216,
          286
        ]
      },
      "distinct_supporting_source_count": {
        "max": 5,
        "median": 1.0,
        "min": 1,
        "n": 34,
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
          1,
          1,
          1,
          1,
          1,
          1,
          1,
          1,
          1,
          1,
          2,
          2,
          2,
          2,
          2,
          3,
          3,
          3,
          3,
          3,
          3,
          4,
          4,
          4,
          5
        ]
      },
      "intervening_unnecessary": {
        "max": 247,
        "median": 98.5,
        "min": 0,
        "n": 34,
        "values": [
          0,
          1,
          9,
          13,
          20,
          23,
          25,
          25,
          27,
          46,
          49,
          51,
          52,
          68,
          80,
          85,
          92,
          105,
          107,
          113,
          114,
          115,
          118,
          137,
          139,
          160,
          170,
          172,
          172,
          177,
          190,
          200,
          219,
          247
        ]
      },
      "native_occurrence_count": {
        "max": 51,
        "median": 6.5,
        "min": 1,
        "n": 34,
        "values": [
          1,
          1,
          2,
          2,
          2,
          2,
          2,
          3,
          3,
          4,
          4,
          4,
          5,
          5,
          5,
          5,
          6,
          7,
          9,
          10,
          12,
          12,
          15,
          15,
          15,
          16,
          16,
          18,
          21,
          21,
          22,
          22,
          47,
          51
        ]
      },
      "rank_distance": {
        "max": 254,
        "median": 99.5,
        "min": 1,
        "n": 34,
        "values": [
          1,
          2,
          12,
          14,
          24,
          26,
          27,
          27,
          30,
          55,
          55,
          58,
          60,
          69,
          86,
          93,
          93,
          106,
          108,
          114,
          115,
          116,
          119,
          138,
          140,
          164,
          175,
          178,
          179,
          179,
          197,
          207,
          226,
          254
        ]
      },
      "target_lexical_rank": {
        "max": 313,
        "median": 246.0,
        "min": 62,
        "n": 34,
        "values": [
          62,
          66,
          80,
          90,
          95,
          96,
          106,
          125,
          128,
          133,
          137,
          138,
          231,
          239,
          240,
          242,
          245,
          247,
          251,
          267,
          271,
          273,
          276,
          279,
          280,
          283,
          286,
          290,
          293,
          302,
          308,
          311,
          312,
          313
        ]
      }
    }
  },
  "indispensable_resources": [
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "TASK",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "kind": "OBLIGATION",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "required_cells": [
    {
      "address": "docs/architecture.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/8",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/14",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/architecture/taxonomy.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/23",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/29",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "docs/documentation_map.md",
      "in_A": true,
      "primary_cell_pointer": "/cells/170",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/imports/declarations.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/266",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/imports/resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/269",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "src/devtools/context/python/modules/interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/275",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/python/imports/test_resolution.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/833",
      "structurally_supported": false,
      "unsupported": true
    },
    {
      "address": "tests/context/python/modules/test_interpretation.py",
      "in_A": true,
      "primary_cell_pointer": "/cells/839",
      "structurally_supported": false,
      "unsupported": true
    }
  ],
  "source_label_diagnostics": {
    "distinct_source_target_obligation_pairs": {
      "HELPFUL_ONLY": 4,
      "REQUIRED": 2,
      "UNNECESSARY": 64
    },
    "qualifying_occurrences": {
      "HELPFUL_ONLY": 6,
      "REQUIRED": 2,
      "UNNECESSARY": 384
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
      "max": 107,
      "median": 30,
      "min": 11,
      "n": 3,
      "values": [
        11,
        30,
        107
      ]
    },
    "distinct_supporting_source_count": {
      "max": 3,
      "median": 3,
      "min": 3,
      "n": 3,
      "values": [
        3,
        3,
        3
      ]
    },
    "intervening_unnecessary": {
      "max": 69,
      "median": 38,
      "min": 1,
      "n": 3,
      "values": [
        1,
        38,
        69
      ]
    },
    "native_occurrence_count": {
      "max": 4,
      "median": 3,
      "min": 3,
      "n": 3,
      "values": [
        3,
        3,
        4
      ]
    },
    "rank_distance": {
      "max": 72,
      "median": 57,
      "min": 3,
      "n": 3,
      "values": [
        3,
        57,
        72
      ]
    },
    "target_lexical_rank": {
      "max": 110,
      "median": 102,
      "min": 68,
      "n": 3,
      "values": [
        68,
        102,
        110
      ]
    }
  },
  "REQUIRED": {
    "best_supporting_source_rank": {
      "max": 3,
      "median": 3,
      "min": 2,
      "n": 5,
      "values": [
        2,
        2,
        3,
        3,
        3
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
      "max": 9,
      "median": 4,
      "min": 0,
      "n": 5,
      "values": [
        0,
        0,
        4,
        7,
        9
      ]
    },
    "native_occurrence_count": {
      "max": 28,
      "median": 14,
      "min": 12,
      "n": 5,
      "values": [
        12,
        12,
        14,
        15,
        28
      ]
    },
    "rank_distance": {
      "max": 20,
      "median": 11,
      "min": 1,
      "n": 5,
      "values": [
        1,
        1,
        11,
        12,
        20
      ]
    },
    "target_lexical_rank": {
      "max": 23,
      "median": 13,
      "min": 3,
      "n": 5,
      "values": [
        3,
        4,
        13,
        15,
        23
      ]
    }
  },
  "UNNECESSARY": {
    "best_supporting_source_rank": {
      "max": 286,
      "median": 97.0,
      "min": 2,
      "n": 88,
      "values": [
        2,
        3,
        10,
        10,
        11,
        29,
        33,
        33,
        35,
        35,
        35,
        35,
        35,
        42,
        45,
        46,
        47,
        48,
        48,
        48,
        51,
        53,
        53,
        54,
        59,
        59,
        61,
        64,
        66,
        66,
        66,
        75,
        75,
        75,
        75,
        75,
        75,
        75,
        79,
        80,
        83,
        84,
        94,
        97,
        97,
        97,
        97,
        101,
        103,
        103,
        103,
        105,
        108,
        114,
        116,
        119,
        120,
        120,
        124,
        127,
        128,
        130,
        130,
        131,
        133,
        135,
        138,
        139,
        139,
        142,
        145,
        152,
        162,
        165,
        169,
        171,
        171,
        177,
        178,
        185,
        191,
        208,
        208,
        214,
        215,
        216,
        257,
        286
      ]
    },
    "distinct_supporting_source_count": {
      "max": 5,
      "median": 1.0,
      "min": 1,
      "n": 88,
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
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        5
      ]
    },
    "intervening_unnecessary": {
      "max": 247,
      "median": 70.0,
      "min": 0,
      "n": 88,
      "values": [
        0,
        0,
        0,
        1,
        1,
        6,
        8,
        9,
        10,
        13,
        14,
        16,
        17,
        20,
        20,
        23,
        25,
        25,
        26,
        27,
        29,
        32,
        33,
        34,
        37,
        37,
        44,
        46,
        49,
        51,
        52,
        55,
        55,
        55,
        56,
        57,
        63,
        65,
        65,
        68,
        68,
        68,
        68,
        69,
        71,
        72,
        73,
        73,
        74,
        77,
        80,
        80,
        85,
        92,
        92,
        96,
        102,
        105,
        107,
        111,
        113,
        114,
        115,
        118,
        135,
        135,
        137,
        137,
        139,
        144,
        147,
        155,
        155,
        158,
        160,
        161,
        170,
        172,
        172,
        174,
        177,
        182,
        184,
        190,
        200,
        205,
        219,
        247
      ]
    },
    "native_occurrence_count": {
      "max": 65,
      "median": 5.0,
      "min": 1,
      "n": 88,
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
        1,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        2,
        3,
        3,
        3,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        4,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        5,
        6,
        6,
        6,
        6,
        6,
        7,
        7,
        9,
        10,
        11,
        12,
        12,
        12,
        14,
        14,
        15,
        15,
        15,
        15,
        15,
        15,
        16,
        16,
        16,
        16,
        17,
        17,
        18,
        18,
        19,
        21,
        21,
        22,
        22,
        22,
        22,
        22,
        47,
        47,
        47,
        51,
        65,
        65
      ]
    },
    "rank_distance": {
      "max": 254,
      "median": 74.0,
      "min": 1,
      "n": 88,
      "values": [
        1,
        1,
        1,
        2,
        7,
        8,
        9,
        11,
        12,
        14,
        15,
        18,
        21,
        24,
        26,
        27,
        27,
        27,
        30,
        30,
        33,
        34,
        36,
        38,
        39,
        45,
        50,
        55,
        55,
        56,
        56,
        57,
        58,
        58,
        58,
        60,
        66,
        66,
        69,
        71,
        71,
        71,
        73,
        74,
        74,
        74,
        75,
        75,
        78,
        78,
        81,
        86,
        93,
        93,
        93,
        98,
        105,
        106,
        108,
        112,
        114,
        115,
        116,
        119,
        136,
        138,
        138,
        138,
        140,
        149,
        150,
        158,
        158,
        160,
        162,
        164,
        175,
        176,
        178,
        179,
        179,
        183,
        186,
        197,
        207,
        208,
        226,
        254
      ]
    },
    "target_lexical_rank": {
      "max": 313,
      "median": 207.0,
      "min": 10,
      "n": 88,
      "values": [
        10,
        11,
        33,
        46,
        51,
        60,
        62,
        62,
        66,
        78,
        80,
        82,
        87,
        89,
        90,
        95,
        96,
        100,
        103,
        106,
        116,
        117,
        121,
        124,
        125,
        128,
        131,
        132,
        133,
        133,
        137,
        138,
        144,
        150,
        151,
        155,
        164,
        169,
        172,
        173,
        177,
        197,
        206,
        206,
        208,
        209,
        211,
        212,
        231,
        235,
        235,
        239,
        239,
        240,
        242,
        242,
        243,
        245,
        247,
        247,
        251,
        251,
        255,
        257,
        258,
        261,
        264,
        267,
        271,
        273,
        276,
        278,
        279,
        280,
        282,
        283,
        283,
        286,
        289,
        290,
        290,
        291,
        293,
        302,
        308,
        311,
        312,
        313
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
    "REQUIRED": 11,
    "UNNECESSARY": 171
  },
  "qualifying_occurrences": {
    "HELPFUL_ONLY": 9,
    "REQUIRED": 86,
    "UNNECESSARY": 976
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
