# Case 0016 Stage D trace

Captured inputs only; no retrieval, graph, RI, PPR or fusion execution; no semantic reviewer.

```json
{
  "artifacts_sha256": {
    "STAGE_D_REVIEW.md": "5b1b53132bf7a69a9294464578bfc84e21bea8e577a26d798986f8e0866cb56e",
    "analysis.json": "2873051fa8f9f2d2cf91f21d85d65ef7b03eb5c49c8f2c4537c94f2df4ead7e8",
    "analysis.md": "5b1b53132bf7a69a9294464578bfc84e21bea8e577a26d798986f8e0866cb56e",
    "validation.json": "b33050f2d0b6e7a7ea263779ac05ef088ff536bccc679ec34f03b134508bb6f3"
  },
  "case": "0016",
  "gate_inputs": {
    "a_burden": [
      257,
      393,
      2140989
    ],
    "c_burden": [
      270,
      432,
      2188189
    ],
    "contract_defect": false,
    "depths": [
      [
        22,
        44
      ],
      [
        36,
        6
      ],
      [
        224,
        239
      ],
      [
        17,
        28
      ],
      [
        6,
        11
      ],
      [
        88,
        104
      ]
    ],
    "graph_contributed_gain": true,
    "ranking_defect": false,
    "required_ranks": [
      [
        1,
        12
      ],
      [
        6,
        16
      ],
      [
        88,
        104
      ],
      [
        4,
        11
      ],
      [
        3,
        10
      ],
      [
        6,
        13
      ],
      [
        44,
        65
      ],
      [
        4,
        2
      ],
      [
        6,
        1
      ],
      [
        50,
        8
      ],
      [
        83,
        99
      ],
      [
        2,
        1
      ],
      [
        67,
        87
      ],
      [
        14,
        25
      ],
      [
        1,
        4
      ],
      [
        1,
        27
      ],
      [
        36,
        6
      ],
      [
        1,
        8
      ],
      [
        2,
        16
      ],
      [
        13,
        27
      ],
      [
        64,
        73
      ],
      [
        96,
        112
      ],
      [
        137,
        142
      ],
      [
        58,
        9
      ],
      [
        65,
        86
      ],
      [
        161,
        168
      ],
      [
        112,
        119
      ],
      [
        224,
        239
      ],
      [
        17,
        28
      ],
      [
        30,
        51
      ],
      [
        104,
        128
      ],
      [
        22,
        44
      ],
      [
        3,
        10
      ],
      [
        38,
        59
      ],
      [
        14,
        37
      ],
      [
        27,
        37
      ]
    ],
    "required_unit_reach_loss": false
  },
  "gates": {
    "complementary_bounds": false,
    "completion_loss": false,
    "outcome": "GRAPH_HARMFUL",
    "rank_gain": true,
    "required_reach_loss": false,
    "required_reach_rescue": false,
    "safe_material_gain": false,
    "strong_burden": false,
    "strong_safety": false,
    "witness_gain": true
  },
  "joins": {
    "gold_cells": 3084,
    "native_resources": 514,
    "rank_bindings": 3556,
    "required_cells": 36,
    "units": 48,
    "witnesses": 22
  },
  "outcome": "GRAPH_HARMFUL",
  "precedence": [
    "Contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
    "RI/view/provenance/personalization/PPR/fusion implementation defect => GRAPH_RANKING_DEFECT",
    "REQUIRED resource/cell/unit reach loss OR baseline completion loss OR any unbounded required rank/selected depth regression => GRAPH_HARMFUL",
    "Valid and no loss/unbounded regression, graph-contributed meaningful witness gain or REQUIRED reach rescue AND (strong burden improvement OR safe material reach gain) => GRAPH_HYBRID_SUPPORTED",
    "No loss/unbounded regression, graph-contributed meaningful rank/witness gain or novel REQUIRED reach rescue => COMPLEMENTARY_GRAPH_VALUE",
    "Otherwise => NO_MATERIAL_VALUE"
  ],
  "provenance": {
    "attempt_1": "FAILED_AUDIT_ONLY; authentication only; never treatment input",
    "attempt_2": "AUTHORITATIVE",
    "primary_blob_sha256": {
      "STAGE_C_REVIEW.md": "10095b46d89779f3cf62269d2020643ff0ee62dfa80b5c36bbd8f26952b8f78d",
      "stage_c_builder.py": "da2898034aa2257172b30a99404a8dfcb8daba0e4f624589763a52153d9430e3",
      "stage_c_hashes.json": "55d5e8ba911bafb871c74aa1e977480f50549a5c15c62f0c18fb5984801600f5",
      "stage_c_method.md": "b2d82110f7e6f43516a22370f0e5853e92e79f1713590b20b12f43dfc79f1bfe",
      "stage_c_review.json": "0d8d806f3fc613bdfa477a8914278423142a14ceaa6d1dd0fd11611544a6d8a8",
      "stage_c_statistics.json": "b4e2f4dc723344a2669280750fbf0a145068ad591e4079a6f4a34d76fcde8a87",
      "stage_c_validation.json": "f5c172851973d10759c0a5702a8425a7f62535125632e0bac4fa95185700622a"
    },
    "recovery": {
      "attempt_1_failed_audit_sha256": "90b6c21765505836e228182771e193aad1782d7c97f6240e748d222548267307",
      "checkpoint": "ceeb6c4da4e2a1db332316239833cf3df6a81831",
      "integrity_sha256": "47f1488cf6d82ed8672fbbc5c4257b1657a9741d66747121bfb1267e087870d1"
    },
    "reviewed_checkpoint": "fb389ac7eec1b009e6403fc0a076a0fe0f6f3af6",
    "stage_a": {
      "amended_authenticated_files": 193,
      "amended_integrity_sha256": "c93c4594c3821211d3129f4fb9c19c41c2ccf035abb12f8de7c2025f0dbbf505",
      "deterministic_stage_a_replay": "PASS",
      "frame": {
        "corpus_id": "1e0df552f370938fcbbbf489a4bf433a25b4a218b1f624b72a21e463bcbdc7b0",
        "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
        "snapshot_id": "636f86afb0fef7b8ccdd9adfd1c9f64dea76139b90d3d098f8f2b811bd90dfca"
      },
      "initial_counts": {
        "exact_seed_resolutions": 0,
        "fusion_executions": 0,
        "gold": "ABSENT",
        "graph_construction_executions": 0,
        "lexical_query_executions": 0,
        "pagerank_executions": 0,
        "reference_query_executions": 0,
        "repository_map_diagnostics": 0,
        "ri_reference_derivations": 0,
        "treatment_rankings": 0
      },
      "original_authenticated_files": 191,
      "original_integrity_sha256": "84529a786ada2d814a56039328f902fa6e28ddb93e7488d41b83282b2ee67009",
      "original_stage_a": "e2cc61600705eb5faccb814cb19f81aac5645a73",
      "protocol_sha256": "a8b4c7bc5b1fe5eea36c40c0f46c579b68f363c5aed3720a36e489089d4cb283",
      "stage_a": "e05d9d08297496c4ff5a8e0be1084c4ce1c99a35"
    },
    "stage_b_integrity_sha256": "b94bcd6dd1b7b0be12b487da70041c1f72b05fa2aa8234c589ad6b9829d734b0",
    "stage_b_top_level_sha256": {
      "STAGE_B_REVIEW.md": "957f26878f6b90a160b6ee92c5e7a6a5d6ac781431e27796ce5eb788c1091ca4",
      "TRACE.md": "957f26878f6b90a160b6ee92c5e7a6a5d6ac781431e27796ce5eb788c1091ca4",
      "arm_a.json.gz": "7ee1edda287b6a007daf821613a57a0157a253d049a257980ca4fbea85e78acf",
      "arm_b.json.gz": "b0f80a38c1943bffa7772e1eb64db51b428e9cbcffbdf9f17dc84cd5a463e591",
      "arm_c.json.gz": "41fabab4e7fd04106594ac45e2cb313d7ea49551d40f0cde5875b33537636257",
      "capture_costs.json": "03bd764093223989884e648250ab49cf547f07b93e164983720c57b5ef8de1a4",
      "costs.json": "51c33ef387907b11f624c01700df847c604a8b4c40f9a5d17540e5a232cd3106",
      "definitions.json.gz": "c24dc98f1be0ae5ed55dde0895e8969d9681482ad38de6fbbf5bae453dff2aa4",
      "exact_seeds_personalization.json.gz": "dcf3e63f99258261142e82da934e5606a9f415eb1040b0c2b29c6912fae07f0b",
      "execution.claim": "6b0d7839dfc86e3ee61fd70036f39983195c45f4f8b259d2dc30c994dc222006",
      "execution_completed.json": "9ed23b2c08c37034f09a9084eeab69940ce7a374d891ef0b66cd11188529f955",
      "execution_started.json": "1960cf3938817ae98f814db8eb33372d7d5dcd2c539177228aaeb3c984009d93",
      "lexical_fields.json.gz": "0426e1bba5d98160402278678aeb80b3136851f2646895265d11280fb99bb544",
      "maps.json.gz": "f7312c1db693f2297dfb80f80ed42d77a0a0633a5a045f7c531afef12c17dc53",
      "native_context.json": "5b3206b8f766aef2c3530f9a231b1aaa3b00ac846686e32f3422aec514dd5eb2",
      "native_statistics.json.gz": "236e6a7a41e30df7bd8eca5b6ae2443d1b931d1368c23c59f3ca4a22300f449d",
      "pair_flows.json.gz": "ca382503e82d805f86e6bfe69713960c0bd35bc5fcfa3c7335f34f3eaf6a1720",
      "ppr_states.json.gz": "53bc8979ddf479f0b196950df7649afcd7abb10ffb2e4ef7df5351fd4c1b96ec",
      "publication_costs.json": "2de6602c63df3e857d875920a9f56f317ae4dca38cb1aa0d2e74295b621d719d",
      "raw_checkpoint.json": "7a0ca2561446769d6a42e310b0496558a6198d5052e187bab988a47e3af202ce",
      "reference.json.gz": "3630fd690d97520cd1e4789b71f34c40500413800b65461be0409413ed071c6a",
      "reference_graph.json.gz": "5cc18ff1c470606cf24698ce7f06649b9e8834a57ef064fc55f78f30c00ccaf2",
      "ri_assessments.json.gz": "ac05f1739f9b35f01c2221a32068a357b992c27035a8f74b0f37188f2e96500f",
      "summary.json": "c41903c972a2e3375ab2bc6c7cb9ca586fb9b17d935a538de87d3fe31cc64821",
      "trace.json": "f1bb06b81e453194447e158197fe6352a31eb32d597714f877b8e9be7af6e466",
      "validation.json": "904e4e94c85406dd0573cdf86583ec3c4c7831085f54a424b4b7f31a237b7a2c"
    },
    "starting_checkpoint": "ef549d05acbd77edce7769d44f4377169410e80b",
    "treatment_checkpoint": "4925f8896edc49b6162d191a6d348f78dd958a48"
  },
  "reviewed_gold_sha256": {
    "REVIEWED_GOLD.md": "25b41ece48f00282ed1d8d06d0e86596a2e6953dd6b7ec47234a58afd56fb0f1",
    "reviewed_gold.json": "11e38c13de6f9a0c25e2c0545cfa83121d3da948be2ad85aa70f6c046f65bad9",
    "reviewed_hashes.json": "9e7fba1c1998d02aa4dbfb135ec97e393b4c90a9277489b7fceed48fbfce6f8e",
    "reviewed_statistics.json": "b4e2f4dc723344a2669280750fbf0a145068ad591e4079a6f4a34d76fcde8a87",
    "reviewed_validation.json": "3aeaac4a4f8d51841a179cb24c83a2fe2bb4db6e8172f0a3e3a1522348e0f3b3"
  },
  "scientific_reruns": 0,
  "semantic_reviewers": 0,
  "stages": [
    "authenticate checkpoints and sealed scientific inputs",
    "exact owning-obligation gold/native identity join",
    "all independent witness/alternative/prefix mathematics",
    "captured propagated-flow/RRF/ablation and self/cross diagnostics",
    "frozen integer gates in original precedence",
    "deterministic publication without treatment or semantic calls"
  ],
  "validation": {
    "adversarial_rejections": [
      "ranks",
      "meaningful_finite_rank_gain",
      "reach_rescue",
      "complementary_regression_bound",
      "selected_depth"
    ],
    "checks": [
      "checkpoint ancestry and original/amended Stage A seals",
      "recovery and failed-attempt isolation",
      "attempt-2 physical/committed integrity and captured-return replay",
      "sole-primary hashes/replay and committed reviewed identity",
      "514 native resource/content/frame bindings and 3084 owning cells",
      "all 36 REQUIRED ranks and 22 independent minimal witnesses",
      "stable witness selection and complete alternatives",
      "integer rank/depth/rescue/bound arithmetic",
      "independent prefix resource unions, label occurrences and UTF-8 bytes",
      "native incoming reference attribution and self/cross reconciliation",
      "captured graph-channel ablation; no new retrieval",
      "seed-only exclusion and novel labels",
      "historical development provenance and descriptive captured costs",
      "exact frozen gate precedence",
      "deterministic artifact replay; overwrite refusal and tamper rejection"
    ],
    "confirmation_reserve": "NOT_ACCESSED",
    "native_reconstruction": "PASS; sealed captured-return replay; zero treatment operations",
    "overwrite_refusal": "PASS; write_new checks every output before any write",
    "scientific_reruns": 0,
    "semantic_reviewer_calls": 0,
    "status": "PASS"
  }
}
```
