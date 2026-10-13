# Direct structural discrimination Stage B mechanical review

No semantic gold, usefulness, pair utility or case outcome is inferred.

## Capture summary

```json
{
  "ablation": {
    "empty_reference_validation_ablations": 3,
    "primary_annotation_passes": 3,
    "ranking_side_effect": "NONE",
    "status": "PASS"
  },
  "case": "0019",
  "confirmation_reserve_access": "NO",
  "execution": "case-0019-stage-b-1",
  "frame": {
    "corpus_id": "eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6",
    "python_resource_count": 182,
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 222,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
    "source_head": "2465af00dc305a6c2a15a90455bf09e62e428e39",
    "source_tree": "12a504a2106467d8b32fc062d15923c7b9250fd9"
  },
  "gold_access": "NO",
  "graph_only_admissions": 0,
  "holdout_access": "NO",
  "interpretation_gaps": [
    "The task/parent do not specify the provider option spelling, value domain, provider-version applicability or default. These are not invented from child knowledge. The freeze evaluates repository integration evidence for the stated control; Stage C must retain any residual task/provider-contract gap rather than assume complete task satisfaction."
  ],
  "ppr_executions": 0,
  "queries": [
    {
      "a_results": 47,
      "local_pairs": 2,
      "obligation": "O1",
      "qualifying_occurrences": 26,
      "status": "PASS",
      "support_source_target_pairs": 2,
      "supported_targets": 2,
      "timings": {
        "annotation_construction_ns": 603300,
        "canonical_a_ns": 10808300,
        "complete_online_equivalent_ns": 44725300,
        "predecessor_pairs_ns": 37000,
        "support_projection_ns": 33276700
      }
    },
    {
      "a_results": 75,
      "local_pairs": 6,
      "obligation": "O2",
      "qualifying_occurrences": 57,
      "status": "PASS",
      "support_source_target_pairs": 7,
      "supported_targets": 6,
      "timings": {
        "annotation_construction_ns": 909500,
        "canonical_a_ns": 18971000,
        "complete_online_equivalent_ns": 51230600,
        "predecessor_pairs_ns": 47900,
        "support_projection_ns": 31302200
      }
    },
    {
      "a_results": 130,
      "local_pairs": 4,
      "obligation": "O3",
      "qualifying_occurrences": 43,
      "status": "PASS",
      "support_source_target_pairs": 5,
      "supported_targets": 4,
      "timings": {
        "annotation_construction_ns": 1048800,
        "canonical_a_ns": 12022500,
        "complete_online_equivalent_ns": 49705600,
        "predecessor_pairs_ns": 16800,
        "support_projection_ns": 36617500
      }
    }
  ],
  "rank_modifications": 0,
  "ri": {
    "assessments": 15893,
    "cross_resource_references": 328,
    "direct_cross_resource_pairs": 64,
    "outcomes": {
      "member-unresolved": 71,
      "method-unresolved": 55,
      "module-unresolved": 1124,
      "resolved": 1268,
      "shadowed-binding": 6707,
      "target-not-supported-declaration": 1724,
      "unresolved-binding": 1179,
      "unsupported-expression": 352,
      "unsupported-receiver": 432,
      "unsupported-scope": 2981
    },
    "positive_references": 1268,
    "resources_derived": 182,
    "self_references": 940
  },
  "rrf_executions": 0,
  "status": "CAPTURED; NO GOLD; NO EFFECTIVENESS INTERPRETATION",
  "task": "Add vLLM CUDA graph estimate control\n"
}
```

## Complete A/support/pair trace

```json
[
  {
    "A": [
      {
        "a_rank": 1,
        "address": "src/devtools/model_benchmarks/docs/overview.md",
        "content_identity": "5e17ffbd9f5bebf7163cac0f69bf29837fb8ea5b8d0585934b48d91ed54ca8ae",
        "content_score": 16.850987334617784,
        "document_identity": "64bd6aa29544ac4e906ca4aa6a0e5737778120ffd801eca4e814fe439a775e1d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 16.850987334617784,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 2,
        "address": "src/devtools/model_serving/docs/overview.md",
        "content_identity": "10ff6484d598b13a6ad26adc41f45a7da6f1bb5cf37d8fd34aea055509f8e7ea",
        "content_score": 15.008462149284014,
        "document_identity": "5654a9afbf6e9a7c15247f73ba80e0fd9fa4d031bb180902fcb0110742f1f535",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 15.008462149284014,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 3,
        "address": "tests/model_benchmarks/test_storage.py",
        "content_identity": "80ce0263623b051a0c137d7ccb579ab0fb97b4d1a99db6ed30821d7f6782f4b6",
        "content_score": 10.595435525600559,
        "document_identity": "0108747cd2d8c830ad1462f25f94385d5e4bac401848643a8ad48bae2666afc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.595435525600559,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 4,
        "address": "src/devtools/model_serving/errors.py",
        "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
        "content_score": 10.094193943849827,
        "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.094193943849827,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "tests/model_serving/test_vllm.py",
        "content_identity": "7e82bb36c742e988201122268e9a7e24e135c1bf00dc59a09ce26620f2a1a39a",
        "content_score": 10.0175127770283,
        "document_identity": "d44d6fdafbb9f86def873e6f465fa47de4d02519cb323d8054b6ad3544eba0e5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.0175127770283,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 6,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "05b0f9f30fe3b6abc84b4fb4f67b0b323b862178fe6ff5412ebbf8fdcf37fbe7",
        "content_score": 9.563539401198113,
        "document_identity": "071ad10da57aae6617e089e907e3d6b043d0c0e076f8e988f4d3e5ca2b50fecb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.563539401198113,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 7,
        "address": "src/devtools/model_serving/vllm.py",
        "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
        "content_score": 8.180297855711807,
        "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa",
        "filename_score": 5.001706663351954,
        "filename_weight": 0.25,
        "score": 9.430724521549795,
        "weighted_filename_score": 1.2504266658379886
      },
      {
        "a_rank": 8,
        "address": "tests/model_benchmarks/test_models.py",
        "content_identity": "41dfe7dcac145b42432ed1488a93980f3a285d834a0dce4d1963602bd40381f9",
        "content_score": 8.66070761522788,
        "document_identity": "37e88862ae59e7a1b564d340f7f1db521553ed37509c3683f6d552f8d5e8ce09",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.66070761522788,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 9,
        "address": "src/devtools/model_benchmarks/storage.py",
        "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
        "content_score": 8.629389274337909,
        "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.629389274337909,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 10,
        "address": "src/devtools/model_benchmarks/models.py",
        "content_identity": "a86307830643681250686a83f3f58f28af4285f081a9699bc2c8f0c025aac32d",
        "content_score": 8.561525367189454,
        "document_identity": "db5b32f575cd2fadaa883bcb98beffa74712fce8e804ec59d3c60f6b908263ae",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.561525367189454,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "src/devtools/model_benchmarks/runner.py",
        "content_identity": "d0afb5a935a181be03814131ecd7a8af1d4be4a6c7eb7d0a5b8865f54b39665d",
        "content_score": 7.049421221077038,
        "document_identity": "8b4374f777bf3a6cd0f64aeeaa152327343b7ac96086917d397cb0c8ea275c48",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.049421221077038,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "src/devtools/conversion/docs/overview.md",
        "content_identity": "ab30aacbedac2b8206a8542fb1991417f24ba25411ba3694c7a1c493b93ad2fc",
        "content_score": 6.19783375152484,
        "document_identity": "23525f2e692359c3f25a04618e1ba12b73ca02cb8c36a11ed4bbbe5d48aab776",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.19783375152484,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 13,
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "a98caba801e659702dc5e9cd3c16c4db06b18835a2a92906c09f483e9adbda9c",
        "content_score": 6.117243585108834,
        "document_identity": "a78d421c3e63b75a5a63107b0fe42f4cf4f6e9a09089548e574f6d373159e5c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.117243585108834,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "src/devtools/runtime/docs/overview.md",
        "content_identity": "1e43fe503ab74d316fe5cabd9bae45062146e91900c96e463f2c8bb6b91a519b",
        "content_score": 5.584313010299258,
        "document_identity": "8c1e8c6f31f875a0a2fbc0c3783a481ac627231a10d5bfffe61060091e4ac9d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.584313010299258,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "src/devtools/evidence/docs/overview.md",
        "content_identity": "66adc8f581f66b172f40112de90f14d0ba3415dd8e0c146ce968bd64875fd84e",
        "content_score": 5.471748582702825,
        "document_identity": "f83119f54160aceff357e91d04396df9681642266cdee5e8547d3aaca17847e3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.471748582702825,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 16,
        "address": "src/devtools/paths/docs/overview.md",
        "content_identity": "b666f9369d8772d77c9abdc29e512f57f9146ce73494a549acf1a2136159e776",
        "content_score": 5.428712334423894,
        "document_identity": "1659fad7a2b4975dccc5dc5b8c75733ce9f99b2003ade71fb45e5421e509b416",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.428712334423894,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "src/devtools/persistence/docs/sqlite.md",
        "content_identity": "75dd9fa49b1a2c3f97ca921d5abdf6435b59992ced1835a4e61a166cc0ead988",
        "content_score": 5.2686855877307295,
        "document_identity": "efd8893881683fd42c0d9a3272b9f02b7bf79a614dd371491047e58d5381f229",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.2686855877307295,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "docs/architecture.md",
        "content_identity": "4aa8890280cd2a5e18582a6330fb79e6204212e6e5239ac6def2671153a27301",
        "content_score": 5.178849394072222,
        "document_identity": "c2f40d6caa321ca6908e902184fca3c10593079ae912ecd9497b38143ed7f98f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.178849394072222,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "tests/model_serving/__init__.py",
        "content_identity": "315fa49644e49326f585843a8e7ab22d85af9c2e86425675a143021afe86550e",
        "content_score": 4.672259255509772,
        "document_identity": "dbedecdce42ba6df9177d73fbf4ec402a7a09d984838042370d25bc2e5fe070a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.672259255509772,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "tests/conversion/test_conversion.py",
        "content_identity": "bf39df57853b170a57f39b6c0b0599e7939369e2d5605e4bf7924dbeb6166839",
        "content_score": 4.642975082142038,
        "document_identity": "2bc94e2db4dee31186a5107e5fd3a767d5a6f183d03acd49c9079755c5499041",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.642975082142038,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "src/devtools/model_serving/__init__.py",
        "content_identity": "dd774516574c2587458b0a4a2d988c1b1237e048f13742e62a615a34015e083b",
        "content_score": 4.508698937562251,
        "document_identity": "314ee2d7830272292a33cde1d474f6a765e65fd0e132e86d015f7dcc889d0e79",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.508698937562251,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "src/devtools/filesystem/codecs/text.py",
        "content_identity": "45c114f1924a962475404e3d7684acb4d3ec24f5052ae04ed4c9c23d9d159591",
        "content_score": 3.8434832937012295,
        "document_identity": "2bfa1bd9d28acf048c9465c4407031a9a270835278f7e6d897fb3d2bef8e8483",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.8434832937012295,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "src/devtools/filesystem/codecs/markdown.py",
        "content_identity": "6b8c4666332d4eb29494d409c6d8cac0807379666dcf66ab6782d4deeefcd46f",
        "content_score": 3.7213016684736986,
        "document_identity": "bd895e473d0c4fa2bd066504f7c79d7b1640573927561f721e2fb84c1981352f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7213016684736986,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "src/devtools/model_serving/huggingface.py",
        "content_identity": "94bc2f3b0875b57916b614595f79d6a440d860b3fe40ccf85d1545e23c60b961",
        "content_score": 3.720947833216112,
        "document_identity": "11cef5346b33ddae2e87098e738ad4fb6492b28318862e9283542b4d289fa33b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.720947833216112,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "src/devtools/persistence/docs/json.md",
        "content_identity": "79c8652fc035298c5075cd6df40a7cfe636278b777371fec0178e0db96d998f8",
        "content_score": 3.663078329200834,
        "document_identity": "155ca1920f305ab6c46f544549e2bffffcf2508e7eeaca5a8e6f6b4c06a4cfe8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.663078329200834,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "src/devtools/filesystem/docs/csv.md",
        "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
        "content_score": 3.543660540794059,
        "document_identity": "9b541213ab6a90a58f4d604a5c483ee9a8835d6cd3a56a82a43350eefb9b62fc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.543660540794059,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "src/devtools/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "content_score": 3.535427945373223,
        "document_identity": "d4fe14843762144d9f407bd944272e2695d5c60c925d8a4682d3bc5b2dcbe1ba",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.535427945373223,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "tests/filesystem/codecs/test_text.py",
        "content_identity": "0ff02a6315ee9bddfc14d368e1e368df13185822c94a8a44447faa419a9adbd7",
        "content_score": 3.412544144267757,
        "document_identity": "3a50bc3afdc0e045557c9098c3910fd3666f1b2dccfbbde770c1a7372c4ed65e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.412544144267757,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 29,
        "address": "tests/model_benchmarks/test_runner.py",
        "content_identity": "a251929371fea3957510e4f119190ba92238203288e881a9a5560bbb6b7bf2de",
        "content_score": 3.281906710510232,
        "document_identity": "b24da91fc545a331cdc92b6f31186d7e6d8e9b2ce6424b5fbc49a2f274f05b21",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.281906710510232,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "src/devtools/context/docs/session.md",
        "content_identity": "49bccd7bcb45ef7ba4fd51ca73ed92191dd9ef4f8f67f1c31dff4a9ecfc8ca78",
        "content_score": 3.1561695469908333,
        "document_identity": "8e53d312bec3c81992a1d3f6f99062c07d903353ec96e102930f6d3707c6981d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1561695469908333,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "src/devtools/agents/protocols.py",
        "content_identity": "ee30b82de86bc219077e6443082d3dd8aa3d0870f1de72eede73e484e3866494",
        "content_score": 3.1266065233778484,
        "document_identity": "2bc3a260764f3ccbe7becadd6c7814fe6d5d8a8c1ec1e81faa7f217f0d470447",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1266065233778484,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/agents/docs/overview.md",
        "content_identity": "0ff08aa6729dee470613e8b7dd1a77bef613edbd0f878e387b29fc793a3daa9e",
        "content_score": 3.0256206637592635,
        "document_identity": "228465edc59ed56ac12b1603e1e471cad8762dd698095f6ace7672a275ce7194",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0256206637592635,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "6afcf3ce3bd51cbd5422d3fe25aa0d27f133279187f32aecac93c193c97ffec4",
        "content_score": 2.847450522637207,
        "document_identity": "76fbfd93b880fa93f90bc492ad8a3f3aff287927b3073637daf21474b42dbc5a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.847450522637207,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "tests/runtime/test_runtime.py",
        "content_identity": "9f6915145667b647e610fa86f99d1e32520dcb04f7d1847726c20076cbb4577a",
        "content_score": 2.739353310156258,
        "document_identity": "0abaa962b16b6803945272f5ca810af1ebeb6ce67924c5a89bccbfc32aef8c2c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.739353310156258,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "src/devtools/codex/docs/overview.md",
        "content_identity": "448384c98365dd51f9fcdb028a295fcbd88e35bccb2b0035c37f8a9ed513e64a",
        "content_score": 2.636822520651698,
        "document_identity": "1ccdff2bcbf8a9c28a9fa334d40993219852f66dd64302588ec5745af642d568",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.636822520651698,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "src/devtools/context/docs/overview.md",
        "content_identity": "81687d5d90b3d6256043e0b7180499a9c2e8a38308004734f442f2bd68ef814e",
        "content_score": 2.5238562153135455,
        "document_identity": "4ea877ce43c74fc552aca23ddfa7183cb62baec0025a296839b34eb963503b1a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5238562153135455,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "src/devtools/runtime/runtime.py",
        "content_identity": "e0a00ceacd3aa37de36947ab8da276f5c46ce640544e87541415ac2da8077149",
        "content_score": 2.5087184557902873,
        "document_identity": "e19bda6e0ee724b945f6b7560137e64e4deb99024851976f19ad3b2044a1ce86",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5087184557902873,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "src/devtools/commands/docs/execution.md",
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "content_score": 2.4406314368373416,
        "document_identity": "4e3069aa5ade6ea9d8a30bf724b534a1e18e291454b3febf0bb6a34a615b11a6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4406314368373416,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "tests/evidence/test_terminal.py",
        "content_identity": "5124e9966871f62de778f967a8cbf5fec46dca4817a82dfa7f92c3bf89f73918",
        "content_score": 2.3342529054847114,
        "document_identity": "840ea06396d427bc41202473fa83a82e9043ada132ee6b236049825708344299",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3342529054847114,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "tests/filesystem/codecs/test_json.py",
        "content_identity": "05c3f70f08101c7036b46203cde9151f2ccbdf9eae53c3b51f25d69630bf74cd",
        "content_score": 2.3147251335239596,
        "document_identity": "7944912926f91e5696d59c53121d8c9fffd7f6a8e40ececf8f6f495f536a4798",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3147251335239596,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "docs/roadmap.md",
        "content_identity": "4b747349e12a0fea64c109bb067f3fda98cae0e849049f8c4a0916366c471e0d",
        "content_score": 2.0765369893456924,
        "document_identity": "d6a183448bf38da43dd86aa6bf1d3bcef7b59fd0b258de5ab311cf891b7f9289",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.0765369893456924,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "tests/filesystem/test_writing.py",
        "content_identity": "30079796e8846f8a72e450e721c29eb08260865d986146c2177666eca461876f",
        "content_score": 2.070768348683486,
        "document_identity": "c5232899c79ff013b63f61e41aca4d65f4a8bf1717a9acdb0dd64b1965081b0b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.070768348683486,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "docs/documentation_map.md",
        "content_identity": "662d0a9b30f6677959e052a88a96e9e4194cf92dde13e55d2ea165682d677492",
        "content_score": 2.0627000245625577,
        "document_identity": "dbc3e78acb0094732f6ebdc1c332b5b53db3e298c36c4e3fd069c1625f62f328",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.0627000245625577,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 44,
        "address": "src/devtools/codex/agent.py",
        "content_identity": "f9ea6307d8286b4dc9547d55553f4c2fec144099143160ebf7e31e2e9f123936",
        "content_score": 1.949268242279983,
        "document_identity": "283e13d0f5b77051160e3bbcaf101c77477bb5b9a8553b0e9b3a50a2ec4d1646",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.949268242279983,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "src/devtools/paths/resolution.py",
        "content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
        "content_score": 1.783073977557391,
        "document_identity": "f76c07f901bf265e3dd7ef1f5046120533b084e180c574736b710838872007d4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.783073977557391,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "src/devtools/codex/docs/cli.md",
        "content_identity": "3953468b726dec2f01bc64764587480964f91f8d435eeb5ff75498079781799a",
        "content_score": 1.6772523231489025,
        "document_identity": "83cfc4e15d34d8e790c3d44453d92f7802a5ee42e33cb5633640a6f39b287b4f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6772523231489025,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "tests/filesystem/test_reading.py",
        "content_identity": "b6a106c7dea09881ab91b334943f85bf0075704afe166be64027e4f6b2475d59",
        "content_score": 1.5412808125603514,
        "document_identity": "d6fc5e8fe9655ef353a712da131ad3390516dd90d2dc4104fd17c294eb474ad2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5412808125603514,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 5,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 12,
        "sources": [
          {
            "a_rank": 5,
            "address": "tests/model_serving/test_vllm.py",
            "content_identity": "7e82bb36c742e988201122268e9a7e24e135c1bf00dc59a09ce26620f2a1a39a",
            "document_identity": "d44d6fdafbb9f86def873e6f465fa47de4d02519cb323d8054b6ad3544eba0e5",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "17b2d0352884f63c6972f70f725a1f872cc6d725e767c8d3d7f8c869fb5c54fd",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 873,
                  "start_column_utf8": 13,
                  "start_line": 873
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "2038800a3847ca43ccc9d8e04bce41d6692850addf73ed3c41b3ea3aad0846a7",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 1144,
                  "start_column_utf8": 13,
                  "start_line": 1144
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "24eefc17b6183526d210489a3c2945690eded5af8ef84dfcb656ad7011ef5c04",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 342,
                  "start_column_utf8": 24,
                  "start_line": 342
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3513f85efc1694b9d80b2513c2263ab529da700b8b9c8f0fa030ba2317492404",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 560,
                  "start_column_utf8": 13,
                  "start_line": 560
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "78827405d1f707595f2502e192b2ce19ca49ca465e9657c78eb662d0802182cb",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 995,
                  "start_column_utf8": 13,
                  "start_line": 995
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "791fc88ff28aa3095a8a1857aa4f0d28b5a988b0622465bebd9d173d18ce4e04",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 902,
                  "start_column_utf8": 12,
                  "start_line": 902
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7982d8fe1c1f4ea58fba5de8eff13bac5119e4b4442e8b8d0f43ec17e7824163",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 1092,
                  "start_column_utf8": 13,
                  "start_line": 1092
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "88782bd0e67d94d994a8f193008fa75aa47bad9c3623181f54f8e61a663ae16f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 643,
                  "start_column_utf8": 24,
                  "start_line": 643
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "95d77494a639982b3d2cb689c3127a24bbba93055e27b7fab6ad14e85fbae08b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 909,
                  "start_column_utf8": 13,
                  "start_line": 909
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "9c49dce292113109f2967ec02a6b8d3b71ed348cef0a355fdb95562046d7c71d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 366,
                  "start_column_utf8": 24,
                  "start_line": 366
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "eb88ba1987b3c5eae074dba5f611a37d1ecd2792562619fd445393d8ebd9c656",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 954,
                  "start_column_utf8": 13,
                  "start_line": 954
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "fc449c0b5f7321cdb5f50587248f6312857282f4d63a2b51c0dbdc69e3f7d642",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 122,
                  "start_column_utf8": 13,
                  "start_line": 122
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/vllm.py",
                "target_content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
                "target_declaration_identity": "05130f84298c11200498625ade93b7919754339afdc649277161d5ecfda10e09",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d9703ec5a77e4a05d872e868d26355ee8d6aa9c013f8324dfc3ffa794787ae8a"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 7,
          "address": "src/devtools/model_serving/vllm.py",
          "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
          "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa"
        }
      },
      {
        "best_supporting_source_rank": 3,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 14,
        "sources": [
          {
            "a_rank": 3,
            "address": "tests/model_benchmarks/test_storage.py",
            "content_identity": "80ce0263623b051a0c137d7ccb579ab0fb97b4d1a99db6ed30821d7f6782f4b6",
            "document_identity": "0108747cd2d8c830ad1462f25f94385d5e4bac401848643a8ad48bae2666afc8",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1329a68721ab94d14f9f68194a988737daf618c7297b672138bd0deb88ae5264",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 253,
                  "start_column_utf8": 8,
                  "start_line": 253
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1a054ba4afa97a2e89c7a56a50fe71904f43f7bf228e62e83df0986ae932a6b9",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 189,
                  "start_column_utf8": 11,
                  "start_line": 189
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1a98e5840c4093f72d177fe54008515f461cc6b6cbdfb4ce16ae6be601dc252d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 122,
                  "start_column_utf8": 11,
                  "start_line": 122
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "20e58cf477716d64f7baf9640312b53e8a7877577435763beefbe21c5319a2d6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 104,
                  "start_column_utf8": 11,
                  "start_line": 104
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "2e6b0066890dbfa1f3de578b59ec61094c398c2e1c9ec0eb72b0b4fa1c27f34c",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 284,
                  "start_column_utf8": 12,
                  "start_line": 284
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3e048305584b1a618cf47d6d041699a8ccbdfc5f8438c5631b83b3e2ccaba9b0",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 206,
                  "start_column_utf8": 8,
                  "start_line": 206
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "877456173a320672cb5f8d7198da7fa61c1ca810e64f9d99acfe53a92d4b7290",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 112,
                  "start_column_utf8": 11,
                  "start_line": 112
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8c8d2838b04b3dd0df9806756f17e2a233b74188a6f797d5e32d13d4a82c7f42",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 159,
                  "start_column_utf8": 13,
                  "start_line": 159
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "91078e27dbd69dfcf1e260cbdbdfc7ba40b8f97b14560d6fd055fc769acafd9e",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 226,
                  "start_column_utf8": 11,
                  "start_line": 226
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "baaee555ea3b29cd1a681b91e164d73a4c00dc36e5bcab33d732c4bf98c2b665",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 213,
                  "start_column_utf8": 12,
                  "start_line": 213
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "bb7cac41e49790722e549fc56a58e4fae04c93f67406b52f2502f2e690edb870",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 269,
                  "start_column_utf8": 8,
                  "start_line": 269
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "dd796d53505f430b2c00056f95430d33b3218e2aeaa15284c05830cb1426c17b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 140,
                  "start_column_utf8": 11,
                  "start_line": 140
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e30eeff83f63d46bf7756c2e08b82687ab93838d9fcbd0ea990dd77a0fe5568d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 89,
                  "start_column_utf8": 11,
                  "start_line": 89
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ecd0ee1c0b4b55f1a274133740e4cfa8c1c92b1b6a44c0aca411aa1ff7c492fd",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 214,
                  "start_column_utf8": 13,
                  "start_line": 214
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 9,
          "address": "src/devtools/model_benchmarks/storage.py",
          "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
          "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62"
        }
      }
    ],
    "counts": {
      "local_pairs": 2,
      "qualifying_occurrences": 26,
      "status": "PASS",
      "support_source_target_pairs": 2,
      "supported_targets": 2
    },
    "frame": {
      "corpus_id": "eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028"
    },
    "information_need": "How are explicit provider configuration choices represented and validated so a CUDA graph estimation control can be added without changing existing defaults?",
    "local_pairs": [
      {
        "obligation": "O1",
        "predecessor": {
          "a_rank": 6,
          "address": "tests/scripts/test_vllm_benchmark_driver.py",
          "content_identity": "05b0f9f30fe3b6abc84b4fb4f67b0b323b862178fe6ff5412ebbf8fdcf37fbe7",
          "document_identity": "071ad10da57aae6617e089e907e3d6b043d0c0e076f8e988f4d3e5ca2b50fecb"
        },
        "query": "Q1",
        "target": {
          "a_rank": 7,
          "address": "src/devtools/model_serving/vllm.py",
          "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
          "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa"
        }
      },
      {
        "obligation": "O1",
        "predecessor": {
          "a_rank": 8,
          "address": "tests/model_benchmarks/test_models.py",
          "content_identity": "41dfe7dcac145b42432ed1488a93980f3a285d834a0dce4d1963602bd40381f9",
          "document_identity": "37e88862ae59e7a1b564d340f7f1db521553ed37509c3683f6d552f8d5e8ce09"
        },
        "query": "Q1",
        "target": {
          "a_rank": 9,
          "address": "src/devtools/model_benchmarks/storage.py",
          "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
          "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62"
        }
      }
    ],
    "obligation": "O1",
    "query": "vLLM CUDA graph estimate control serving configuration validation defaults",
    "query_identity": {
      "task": "case-0019:historical-development-003",
      "value": "Q1"
    },
    "task_identity": "case-0019:historical-development-003",
    "timings": {
      "annotation_construction_ns": 603300,
      "canonical_a_ns": 10808300,
      "complete_online_equivalent_ns": 44725300,
      "predecessor_pairs_ns": 37000,
      "support_projection_ns": 33276700
    }
  },
  {
    "A": [
      {
        "a_rank": 1,
        "address": "src/devtools/model_serving/vllm.py",
        "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
        "content_score": 28.933604994843332,
        "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa",
        "filename_score": 5.001706663351954,
        "filename_weight": 0.25,
        "score": 30.18403166068132,
        "weighted_filename_score": 1.2504266658379886
      },
      {
        "a_rank": 2,
        "address": "tests/model_serving/test_vllm.py",
        "content_identity": "7e82bb36c742e988201122268e9a7e24e135c1bf00dc59a09ce26620f2a1a39a",
        "content_score": 29.21960634521886,
        "document_identity": "d44d6fdafbb9f86def873e6f465fa47de4d02519cb323d8054b6ad3544eba0e5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 29.21960634521886,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 3,
        "address": "src/devtools/model_serving/docs/overview.md",
        "content_identity": "10ff6484d598b13a6ad26adc41f45a7da6f1bb5cf37d8fd34aea055509f8e7ea",
        "content_score": 27.786560602563775,
        "document_identity": "5654a9afbf6e9a7c15247f73ba80e0fd9fa4d031bb180902fcb0110742f1f535",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 27.786560602563775,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 4,
        "address": "src/devtools/model_serving/errors.py",
        "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
        "content_score": 21.53241250053592,
        "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 21.53241250053592,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "src/devtools/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "content_score": 12.12836400110264,
        "document_identity": "3d7c64d8314abc861c526718abfe4bbdfaf6cb64bce67f3bf6a41289877855d0",
        "filename_score": 4.154408802964751,
        "filename_weight": 0.25,
        "score": 13.166966201843827,
        "weighted_filename_score": 1.0386022007411877
      },
      {
        "a_rank": 6,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "05b0f9f30fe3b6abc84b4fb4f67b0b323b862178fe6ff5412ebbf8fdcf37fbe7",
        "content_score": 12.28891571098112,
        "document_identity": "071ad10da57aae6617e089e907e3d6b043d0c0e076f8e988f4d3e5ca2b50fecb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.28891571098112,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 7,
        "address": "src/devtools/commands/models/command.py",
        "content_identity": "fca918a60dbdc006190a8287ab347dec64b467573bbae1ca40d37322ca974494",
        "content_score": 9.387934221854767,
        "document_identity": "e0ba027f203c191efb2dc15d16ce0d3b6148481f93defebea9955a86ca3f9bbb",
        "filename_score": 4.154408802964751,
        "filename_weight": 0.25,
        "score": 10.426536422595955,
        "weighted_filename_score": 1.0386022007411877
      },
      {
        "a_rank": 8,
        "address": "src/devtools/tools/command.py",
        "content_identity": "831b7f3a140775322e8d4fb22d27f1e32f596074bb8effa72814d0024c053418",
        "content_score": 8.748014488699031,
        "document_identity": "10c0372bf985e2eda71b113790af99ed5f7b08451f38e3da408aea52758da203",
        "filename_score": 4.154408802964751,
        "filename_weight": 0.25,
        "score": 9.78661668944022,
        "weighted_filename_score": 1.0386022007411877
      },
      {
        "a_rank": 9,
        "address": "src/devtools/commands/docs/execution.md",
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "content_score": 9.753947501563012,
        "document_identity": "4e3069aa5ade6ea9d8a30bf724b534a1e18e291454b3febf0bb6a34a615b11a6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.753947501563012,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 10,
        "address": "src/devtools/commands/docs/overview.md",
        "content_identity": "1e56dd5df37ebd6196ce8d5c717c13db238e52b408f3ac20e82944d5874c06e6",
        "content_score": 8.950630604315894,
        "document_identity": "0d5838ad72fe347fa9c869bd0ae939b9e8ede607d954ccdd4d2235c0e1fc39e2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.950630604315894,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "tests/commands/test_models.py",
        "content_identity": "2fdda3a7f7d7909792df8cdb81628b2bd757436bc0e7512dd31a4f55b56480d2",
        "content_score": 8.638511754680305,
        "document_identity": "f07afe9d3ac89f6c2f6b993b1d0c2c79e1482af6082982fec31c01df238a33c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.638511754680305,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "tests/model_benchmarks/test_models.py",
        "content_identity": "41dfe7dcac145b42432ed1488a93980f3a285d834a0dce4d1963602bd40381f9",
        "content_score": 8.431043697060202,
        "document_identity": "37e88862ae59e7a1b564d340f7f1db521553ed37509c3683f6d552f8d5e8ce09",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.431043697060202,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 13,
        "address": "src/devtools/model_benchmarks/docs/overview.md",
        "content_identity": "5e17ffbd9f5bebf7163cac0f69bf29837fb8ea5b8d0585934b48d91ed54ca8ae",
        "content_score": 8.105736949238265,
        "document_identity": "64bd6aa29544ac4e906ca4aa6a0e5737778120ffd801eca4e814fe439a775e1d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.105736949238265,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "src/devtools/system/docs/overview.md",
        "content_identity": "bf0521c622d37545493dd524bc2844076002bea811dde73377c0a1614e3f1757",
        "content_score": 7.987726558486459,
        "document_identity": "44c5ad84e31deeee6247fb158f993225d22f7c902504306d7b376d93b14985fa",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.987726558486459,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "src/devtools/model_serving/huggingface.py",
        "content_identity": "94bc2f3b0875b57916b614595f79d6a440d860b3fe40ccf85d1545e23c60b961",
        "content_score": 7.9081254962271945,
        "document_identity": "11cef5346b33ddae2e87098e738ad4fb6492b28318862e9283542b4d289fa33b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.9081254962271945,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 16,
        "address": "src/devtools/model_benchmarks/models.py",
        "content_identity": "a86307830643681250686a83f3f58f28af4285f081a9699bc2c8f0c025aac32d",
        "content_score": 7.856913938190189,
        "document_identity": "db5b32f575cd2fadaa883bcb98beffa74712fce8e804ec59d3c60f6b908263ae",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.856913938190189,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "src/devtools/codex/docs/overview.md",
        "content_identity": "448384c98365dd51f9fcdb028a295fcbd88e35bccb2b0035c37f8a9ed513e64a",
        "content_score": 7.529356903186219,
        "document_identity": "1ccdff2bcbf8a9c28a9fa334d40993219852f66dd64302588ec5745af642d568",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.529356903186219,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "6afcf3ce3bd51cbd5422d3fe25aa0d27f133279187f32aecac93c193c97ffec4",
        "content_score": 7.220441102128891,
        "document_identity": "76fbfd93b880fa93f90bc492ad8a3f3aff287927b3073637daf21474b42dbc5a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.220441102128891,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "docs/documentation_map.md",
        "content_identity": "662d0a9b30f6677959e052a88a96e9e4194cf92dde13e55d2ea165682d677492",
        "content_score": 6.864048704715588,
        "document_identity": "dbc3e78acb0094732f6ebdc1c332b5b53db3e298c36c4e3fd069c1625f62f328",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.864048704715588,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "docs/architecture.md",
        "content_identity": "4aa8890280cd2a5e18582a6330fb79e6204212e6e5239ac6def2671153a27301",
        "content_score": 6.630874337291331,
        "document_identity": "c2f40d6caa321ca6908e902184fca3c10593079ae912ecd9497b38143ed7f98f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.630874337291331,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "tests/tools/test_execution.py",
        "content_identity": "ca795dd35424539b29e091e66f20e67a66c99f9b2902729a49d1f8264555c5c2",
        "content_score": 5.64678032436328,
        "document_identity": "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.64678032436328,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "src/devtools/model_benchmarks/runner.py",
        "content_identity": "d0afb5a935a181be03814131ecd7a8af1d4be4a6c7eb7d0a5b8865f54b39665d",
        "content_score": 5.508179483997875,
        "document_identity": "8b4374f777bf3a6cd0f64aeeaa152327343b7ac96086917d397cb0c8ea275c48",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.508179483997875,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "14fbd64f5aace02b3bcfd9cbeedf0183532182eadd7c3e8af3f57ea71d9bbeb9",
        "content_score": 5.479834695148004,
        "document_identity": "c9d01508be698d8466bbc4cc584b060ed368f93c38ba3b222b89e4b5ec72389e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.479834695148004,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "a976b9868ea3ec236496d2516b31bbb645f03e4a54ba2dc68476a80e3e1ee8ef",
        "content_score": 5.374195878148591,
        "document_identity": "97d27b9c43fef58875abea365716c6d39e8ed308c604ac874a2856b16ddd4ba9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.374195878148591,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "src/devtools/tools/execution.py",
        "content_identity": "83f76f63eb0214d03451ca47a806ef5e5dd70ef2bfa1b43754fe60032823c00e",
        "content_score": 5.360686805590558,
        "document_identity": "3796bdcbb444b9e2dbead6c47ad85d01f1f07d92692ebcf471bf9eb67ac6e7ec",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.360686805590558,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "src/devtools/codex/agent.py",
        "content_identity": "f9ea6307d8286b4dc9547d55553f4c2fec144099143160ebf7e31e2e9f123936",
        "content_score": 5.203603654316216,
        "document_identity": "283e13d0f5b77051160e3bbcaf101c77477bb5b9a8553b0e9b3a50a2ec4d1646",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.203603654316216,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "src/devtools/model_serving/__init__.py",
        "content_identity": "dd774516574c2587458b0a4a2d988c1b1237e048f13742e62a615a34015e083b",
        "content_score": 5.073632936230951,
        "document_identity": "314ee2d7830272292a33cde1d474f6a765e65fd0e132e86d015f7dcc889d0e79",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.073632936230951,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "src/devtools/tools/protocols.py",
        "content_identity": "f615d6d2601e48e1f7c4631873ea3d2bae26e177e73f08c3ff81833687535172",
        "content_score": 4.934423699033636,
        "document_identity": "5ae5e7b1d8590aa65651909da6656369f1f0b19f0a8517b2cc765e8036ea3ed0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.934423699033636,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 29,
        "address": "tests/model_benchmarks/test_storage.py",
        "content_identity": "80ce0263623b051a0c137d7ccb579ab0fb97b4d1a99db6ed30821d7f6782f4b6",
        "content_score": 4.736260223557276,
        "document_identity": "0108747cd2d8c830ad1462f25f94385d5e4bac401848643a8ad48bae2666afc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.736260223557276,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "src/devtools/context/docs/overview.md",
        "content_identity": "81687d5d90b3d6256043e0b7180499a9c2e8a38308004734f442f2bd68ef814e",
        "content_score": 4.453175009639359,
        "document_identity": "4ea877ce43c74fc552aca23ddfa7183cb62baec0025a296839b34eb963503b1a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.453175009639359,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "tests/model_serving/test_huggingface.py",
        "content_identity": "f51a3f3658c02df2b5ba9257cfe9d04fd28bc48a25bd29c6239ebf390b07e1c7",
        "content_score": 4.367430158650471,
        "document_identity": "b9d1e775fff180ae470f15d338184d0eca1441e149a73e3681dd7f8bb3f3807d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.367430158650471,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/agents/docs/overview.md",
        "content_identity": "0ff08aa6729dee470613e8b7dd1a77bef613edbd0f878e387b29fc793a3daa9e",
        "content_score": 4.361329374625015,
        "document_identity": "228465edc59ed56ac12b1603e1e471cad8762dd698095f6ace7672a275ce7194",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.361329374625015,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "src/devtools/context/docs/session.md",
        "content_identity": "49bccd7bcb45ef7ba4fd51ca73ed92191dd9ef4f8f67f1c31dff4a9ecfc8ca78",
        "content_score": 3.9448131399331183,
        "document_identity": "8e53d312bec3c81992a1d3f6f99062c07d903353ec96e102930f6d3707c6981d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.9448131399331183,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "src/devtools/codex/docs/cli.md",
        "content_identity": "3953468b726dec2f01bc64764587480964f91f8d435eeb5ff75498079781799a",
        "content_score": 3.935680528737526,
        "document_identity": "83cfc4e15d34d8e790c3d44453d92f7802a5ee42e33cb5633640a6f39b287b4f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.935680528737526,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "src/devtools/runtime/docs/overview.md",
        "content_identity": "1e43fe503ab74d316fe5cabd9bae45062146e91900c96e463f2c8bb6b91a519b",
        "content_score": 3.7554926791094467,
        "document_identity": "8c1e8c6f31f875a0a2fbc0c3783a481ac627231a10d5bfffe61060091e4ac9d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7554926791094467,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "docs/roadmap.md",
        "content_identity": "4b747349e12a0fea64c109bb067f3fda98cae0e849049f8c4a0916366c471e0d",
        "content_score": 3.6639102384036515,
        "document_identity": "d6a183448bf38da43dd86aa6bf1d3bcef7b59fd0b258de5ab311cf891b7f9289",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.6639102384036515,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "src/devtools/commands/execution.py",
        "content_identity": "6062be2b0271fd1e81ffc10e2b3fb8da2ab873948fc1afcfde4dd129d24ad6cd",
        "content_score": 3.5005479584705648,
        "document_identity": "d3fbdedaaa3df7f439f63fabdbd581db397a8f40a8815686454e7ed3abde2676",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.5005479584705648,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "tests/tools/test_command.py",
        "content_identity": "c01229e295c147fed7c4bfd21dd692ab5e5c5c31d2f2b3021a0fb735a1196096",
        "content_score": 3.4448705473935055,
        "document_identity": "a5366355f81d081f3296ff7e14db96aa0d0982e8aacc4fb4c0cedf185a642fdb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.4448705473935055,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "src/devtools/commands/models/result.py",
        "content_identity": "494dfafcbb7acc544e94a04a17de311a20960dd636b67fc3f33704f1955872d3",
        "content_score": 3.410956507943809,
        "document_identity": "48ea0212291b99647bbb952ffaeb7f7e49c6dacd03e829f2880902404c19cf82",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.410956507943809,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "src/devtools/commands/events.py",
        "content_identity": "9d7fd113611a567c2a01adafd1596366dd3bf385dbdcdf5d49c02e87e891a1b0",
        "content_score": 3.3928970095850044,
        "document_identity": "08f388704566f6aafcb3961caa6007b78d9d1667c309b7e7d0719dda3e841044",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3928970095850044,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "tests/commands/test_events.py",
        "content_identity": "3457f79599e0cab1cc452d0701d5898f247b5d4f6c138a6b13714e4e9940fe99",
        "content_score": 3.3910320138339225,
        "document_identity": "025d474e2fbf754aed924d2daea7994e1ae50cc09029f24771be52af3ff0e60d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3910320138339225,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "src/devtools/commands/models/__init__.py",
        "content_identity": "5c1fa00f428cec59667116269277c29ec21165255c33574e8267419d5a24e890",
        "content_score": 3.3865119059328928,
        "document_identity": "7d1d9ec51cfb26803e8fac65113911c6138dbc850fcc87b2066b5f992abcbcf9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3865119059328928,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "tests/commands/test_execution.py",
        "content_identity": "4be50311fc81376286545eb02fecf0725e24d6620fcd91e192d3b6a75dfd60f6",
        "content_score": 3.320980531400864,
        "document_identity": "fb50df1403ac0cc8b8745bfcb8dc32aae722b13ef44a6fcd1bbff883620e3478",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.320980531400864,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 44,
        "address": "src/devtools/commands/handle.py",
        "content_identity": "7cc05c460e79955c6d36edf8b46eb4ee3314eb60e7116b5f4129b9aec4863d23",
        "content_score": 3.286646310517806,
        "document_identity": "292e2106000f511491087016a527aafd75292b449a6bb8c230f6233c90d18be3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.286646310517806,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "tests/model_benchmarks/test_runner.py",
        "content_identity": "a251929371fea3957510e4f119190ba92238203288e881a9a5560bbb6b7bf2de",
        "content_score": 3.281906710510232,
        "document_identity": "b24da91fc545a331cdc92b6f31186d7e6d8e9b2ce6424b5fbc49a2f274f05b21",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.281906710510232,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "tests/commands/test_errors.py",
        "content_identity": "b186677c924cf5775178e19fa581e3eacb04d1dd8eb7cbe07619a4886036c2a3",
        "content_score": 3.2239628345669025,
        "document_identity": "31c69918a66063ef7a16d84e0907aa4284722518523f49c0d4dc14eae89d4d69",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.2239628345669025,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "src/devtools/commands/__init__.py",
        "content_identity": "e01c05a3e3deab403caaa1451d4d0712b52b9a09e3281822a56b5ab522e8b871",
        "content_score": 3.1811942736447163,
        "document_identity": "3459a0af5e6482cbbf690556226d5fd6f7b8b2a969a18cac05ce5319ba180bd8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1811942736447163,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 48,
        "address": "tests/commands/test_handle.py",
        "content_identity": "f271487d5e9bada3ede3cc752a2259e5299047f69357e52a2c430b5a342e91a9",
        "content_score": 3.133924511674287,
        "document_identity": "1d14321b52cca27bd47eb9e79a812121a5f74c698ba43a6a9f684f305e6b109c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.133924511674287,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 49,
        "address": "src/devtools/agents/protocols.py",
        "content_identity": "ee30b82de86bc219077e6443082d3dd8aa3d0870f1de72eede73e484e3866494",
        "content_score": 3.1266065233778484,
        "document_identity": "2bc3a260764f3ccbe7becadd6c7814fe6d5d8a8c1ec1e81faa7f217f0d470447",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1266065233778484,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 50,
        "address": "src/devtools/identity/docs/overview.md",
        "content_identity": "06b5801a244a5f40d898920d09d9d982f3d39c949c634e97fe1a7b308bb5d71a",
        "content_score": 3.108658421953121,
        "document_identity": "5a8c1181f7c4df5301fae0cc6d0d143ef56ad66d3855c1ccc7a4e0ebf9692442",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.108658421953121,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 51,
        "address": "tests/codex/test_agent.py",
        "content_identity": "8ff2ef564dddddd6a43757bbadf5785b54d4d7f9fc47167d0f1d0831d4f38dab",
        "content_score": 3.080331719270964,
        "document_identity": "dbecb518b7ef0578fb29b5348a4588de3b04500616218138bbcbe1d779b2dec2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.080331719270964,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 52,
        "address": "src/devtools/commands/errors.py",
        "content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
        "content_score": 3.050182451249303,
        "document_identity": "a2cb859564c6ff8bd01de9b1ab589f654d65cdff8023a216596b8dd49f714bed",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.050182451249303,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 53,
        "address": "src/devtools/commands/docs/events.md",
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "content_score": 3.01496668635219,
        "document_identity": "4cbb31e57dcb0cc774f6bd79d6f3d6739326bb7ddbb4ca72fec683f4802c938a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.01496668635219,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 54,
        "address": "tests/codex/test_live.py",
        "content_identity": "4cdf73b86dd329572a490b4c073747fcfc16cef370ee511d354e11c45be5fa64",
        "content_score": 2.9279967127136737,
        "document_identity": "9d0db5cae9246913762a5fa89d079c1b0162f3ffe690a6c0f7060b1d1f437350",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9279967127136737,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 55,
        "address": "src/devtools/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "content_score": 2.9192919575325647,
        "document_identity": "36927bf0f9fb1706f691c0c472cd72fc6810926fd1e23e6b060c9983946950a5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9192919575325647,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 56,
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "a98caba801e659702dc5e9cd3c16c4db06b18835a2a92906c09f483e9adbda9c",
        "content_score": 2.8840941614143127,
        "document_identity": "a78d421c3e63b75a5a63107b0fe42f4cf4f6e9a09089548e574f6d373159e5c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8840941614143127,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 57,
        "address": "src/devtools/model_benchmarks/storage.py",
        "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
        "content_score": 2.8541776548945434,
        "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8541776548945434,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 58,
        "address": "tests/runtime/test_live.py",
        "content_identity": "f6b41c2c813c511fdb663b25900e2dba6689e8570a21556f760e86360ceeb34d",
        "content_score": 2.796744693353303,
        "document_identity": "dab942f9e98c8a72be341b3919f9a52fffcbfd9c6e379a767dbc60c71d491969",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.796744693353303,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 59,
        "address": "src/devtools/filesystem/docs/overview.md",
        "content_identity": "44026da07ae6ed758088154f317bff5dacd64a13c985932438d59e605dfeb59f",
        "content_score": 2.783637898325438,
        "document_identity": "20bd5ce456e48f6a2471834783456f19bef99138a4a5095362cfb634aa52c46e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.783637898325438,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 60,
        "address": "tests/context/session/test_live.py",
        "content_identity": "ae3fb9bbdbd596113d17f67c4bada80ec0294f2fadb5a09848586daf98af9918",
        "content_score": 2.781533548029762,
        "document_identity": "6cbd85cff750d4b8ababc8a319fbdb3a6ba1283bb0c2bab8cfb8b0317bf52dbf",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.781533548029762,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 61,
        "address": "tests/persistence/test_live.py",
        "content_identity": "15bdf060e8650180f4dbe7f588e69bd5389446ede9f18f635bae4ae8ab01c860",
        "content_score": 2.770687039270337,
        "document_identity": "b96980df2466a80c49b5e028a648e83649cc876b84d3a1545cea857b4ac804c6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.770687039270337,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 62,
        "address": "tests/commands/__init__.py",
        "content_identity": "512f63ddf73c412067cb1c8eff784d005d70202fdae5200bd08ee33309fe67d3",
        "content_score": 2.766448634275502,
        "document_identity": "fc5db2e9c896475f484dfc3e4fcb10c50b604568c04cc45d1a387f0ee5f52426",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.766448634275502,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 63,
        "address": "tests/agents/test_models.py",
        "content_identity": "17b484383974535ec3afdd0b1c89d0226313df345d2a93ba3f0f10e33b02d002",
        "content_score": 2.76031666676463,
        "document_identity": "7d9edcced435e29e6df02437ed4d770c62f30ba092ecad2dfe8e15bd6bc0a360",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.76031666676463,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 64,
        "address": "src/devtools/commands/models/output.py",
        "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
        "content_score": 2.7581249192008186,
        "document_identity": "1763e276647a5c03c805a8ec28da2af97ed4e3160cb55f0eee00d7dbff473379",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7581249192008186,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 65,
        "address": "src/devtools/runtime/runtime.py",
        "content_identity": "e0a00ceacd3aa37de36947ab8da276f5c46ce640544e87541415ac2da8077149",
        "content_score": 2.5087184557902873,
        "document_identity": "e19bda6e0ee724b945f6b7560137e64e4deb99024851976f19ad3b2044a1ce86",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5087184557902873,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 66,
        "address": "src/devtools/codex/errors.py",
        "content_identity": "efbdeba3848aef33b7d210052496447c9d5fb190674178cebed08405a58074ff",
        "content_score": 2.4486537315021932,
        "document_identity": "e4a614a5a4c482b021a40190d1d13fd583598568f2cff6b4d9a3d8876306d4c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4486537315021932,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 67,
        "address": "src/devtools/context/docs/history.md",
        "content_identity": "5d6717b57e3f6c416a3669246ce2b5f722461a98b0a483248a92ebd15b1d3a2e",
        "content_score": 2.2882363797396326,
        "document_identity": "331385761b89288ba22d3f0b7850a017d94e9f3e05038dd5fe7875dfda6d3d8f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2882363797396326,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 68,
        "address": "src/devtools/paths/docs/overview.md",
        "content_identity": "b666f9369d8772d77c9abdc29e512f57f9146ce73494a549acf1a2136159e776",
        "content_score": 2.2109881827658957,
        "document_identity": "1659fad7a2b4975dccc5dc5b8c75733ce9f99b2003ade71fb45e5421e509b416",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2109881827658957,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 69,
        "address": "src/devtools/persistence/docs/sqlite.md",
        "content_identity": "75dd9fa49b1a2c3f97ca921d5abdf6435b59992ced1835a4e61a166cc0ead988",
        "content_score": 2.054594200255898,
        "document_identity": "efd8893881683fd42c0d9a3272b9f02b7bf79a614dd371491047e58d5381f229",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.054594200255898,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 70,
        "address": "src/devtools/time/docs/overview.md",
        "content_identity": "1b65aaadc3e577fa186a20b52c5deb4e0218750db828ae2bf25fedbacfc7ef55",
        "content_score": 1.9788577242359058,
        "document_identity": "55bd9644b6a573386a491430bf3b48f96494b5daaec5db9eaaebf8f1a6ffff84",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9788577242359058,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 71,
        "address": "src/devtools/paths/resolution.py",
        "content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
        "content_score": 1.783073977557391,
        "document_identity": "f76c07f901bf265e3dd7ef1f5046120533b084e180c574736b710838872007d4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.783073977557391,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 72,
        "address": "tests/evidence/test_inspection.py",
        "content_identity": "7ab0e6767e722953631ad21d61e67dcc73752b5c97128dfe8f1aaa556ce7159e",
        "content_score": 1.648319025713652,
        "document_identity": "41554b22d5b3ffe5f636a63bce770b52af6fe408f048ea254f44cbcc18404f4e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.648319025713652,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 73,
        "address": "src/devtools/evidence/docs/overview.md",
        "content_identity": "66adc8f581f66b172f40112de90f14d0ba3415dd8e0c146ce968bd64875fd84e",
        "content_score": 1.611042352602711,
        "document_identity": "f83119f54160aceff357e91d04396df9681642266cdee5e8547d3aaca17847e3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.611042352602711,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 74,
        "address": "tests/filesystem/test_reading.py",
        "content_identity": "b6a106c7dea09881ab91b334943f85bf0075704afe166be64027e4f6b2475d59",
        "content_score": 1.5412808125603514,
        "document_identity": "d6fc5e8fe9655ef353a712da131ad3390516dd90d2dc4104fd17c294eb474ad2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5412808125603514,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 75,
        "address": "tests/runtime/test_runtime.py",
        "content_identity": "9f6915145667b647e610fa86f99d1e32520dcb04f7d1847726c20076cbb4577a",
        "content_score": 0.2984268854766727,
        "document_identity": "0abaa962b16b6803945272f5ca810af1ebeb6ce67924c5a89bccbfc32aef8c2c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.2984268854766727,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 1,
        "distinct_supporting_source_count": 2,
        "native_occurrence_count": 32,
        "sources": [
          {
            "a_rank": 1,
            "address": "src/devtools/model_serving/vllm.py",
            "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
            "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0d5b9478577cf933360306c77bd771932d4a8fed681b88a1639fd1a9894ea851",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 306,
                  "start_column_utf8": 18,
                  "start_line": 306
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "7454ca2a362c06adda66001eeb1ad2a695e62cbcfc640a26f462c0d07a57142a",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "c47b5dad90276426081fad8e24f33d740403b50b8d15160ca161fda3d8c17a8b"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "240850255488cdcdd8827fb835fd62219accdafba4811a757d6bc9c342635ce6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 472,
                  "start_column_utf8": 14,
                  "start_line": 472
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "32343a1d95a21ed1309b4b7feed0c58381adf0c3c1aec7862adfb943009dc523",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 46,
                  "end_line": 284,
                  "start_column_utf8": 18,
                  "start_line": 284
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "35a0bb8944e5cff8d28bd3056be0abf2c1ef1148bff60afdbe76dbd05e121ab1",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "11ce40971c9c3108ca4a2c928f6aaf92ef15d3789c5a6bf485b0c609ee6125ff"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3ac5ed56512a7b9f3730c540cf2fa701733321eb5abc16dfdd6f95176f95dc9c",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 31,
                  "end_line": 332,
                  "start_column_utf8": 18,
                  "start_line": 332
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7e0fea29ecb26bbbec28b5f0682bdc5cd1e9c0b29d367ea9be71884a83e20810",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 462,
                  "start_column_utf8": 14,
                  "start_line": 462
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7f23768907e664e11b9cb1026d131a8848a3a5f875eb482aa5856b5375839877",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 35,
                  "end_line": 318,
                  "start_column_utf8": 22,
                  "start_line": 318
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8c915be8a2834205204b93e970bcf7987f9c45f282daf628fd0b9c13360529d3",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 46,
                  "end_line": 270,
                  "start_column_utf8": 30,
                  "start_line": 270
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d12bd11ebffd1b035ddedba616ea02a3447e187d3ef7bc89c3df6f08759713e2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 447,
                  "start_column_utf8": 14,
                  "start_line": 447
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e11e88a912c83b628355c9a8f2d104f7fb15aa6e9dfc96a23a2de67136a3cb78",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 478,
                  "start_column_utf8": 14,
                  "start_line": 478
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ea9fd7099e2b91cc9c98957bc31be322568547ee36d045d1ca6dec9de8bb0b49",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 229,
                  "start_column_utf8": 18,
                  "start_line": 229
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              }
            ]
          },
          {
            "a_rank": 2,
            "address": "tests/model_serving/test_vllm.py",
            "content_identity": "7e82bb36c742e988201122268e9a7e24e135c1bf00dc59a09ce26620f2a1a39a",
            "document_identity": "d44d6fdafbb9f86def873e6f465fa47de4d02519cb323d8054b6ad3544eba0e5",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0a100079d6d903e2a719fe4d6d601a5ad83c03365c84792ff569879da91e8b47",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 30,
                  "end_line": 1143,
                  "start_column_utf8": 14,
                  "start_line": 1143
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "1507fd9f9a36595625313b327f3d8a7ff136c8f47100e4d18e9b369245eef985",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 1108,
                  "start_column_utf8": 23,
                  "start_line": 1108
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "2321ea96758fe2c75468c0250b8163a681570b44e5774c708388008731717fe2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 1166,
                  "start_column_utf8": 23,
                  "start_line": 1166
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "43ef3f304325884529ef605457e13ff5df9310323f3d11ce67a45027db490908",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 1163,
                  "start_column_utf8": 23,
                  "start_line": 1163
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "4c71a2c57fb65ac0eb959fd81cb59fd049fb811e5c44500ba8fc8bb26f0a7ff1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 730,
                  "start_column_utf8": 23,
                  "start_line": 730
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "5a72b6516b170588a2510a85f37ea286f27633a8be35868cafa51d230c66b59d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 1003,
                  "start_column_utf8": 23,
                  "start_line": 1003
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "62c0f9c3b628ad00135e1442ebfd28534c873a12b2206b508447f54381c76547",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 965,
                  "start_column_utf8": 23,
                  "start_line": 965
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "7a14d6a8ef919f982fb62cc999c1f8fc5de18bac692d0c188f1d7b21426e100f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 844,
                  "start_column_utf8": 23,
                  "start_line": 844
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "7cfbaeed8345844e1cc236631580278fc0ae6d6d0ae7209db7a5006042340bce",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 415,
                  "start_column_utf8": 23,
                  "start_line": 415
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "82cfb46a62da3669b37ed80868e6562124e7865e87278de83fda276f44e24760",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 1135,
                  "start_column_utf8": 23,
                  "start_line": 1135
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "8ba2b0254f5d185de843992dff5039e6aab7ea80e398c9d796420232129d1130",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 51,
                  "end_line": 1033,
                  "start_column_utf8": 23,
                  "start_line": 1033
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "35a0bb8944e5cff8d28bd3056be0abf2c1ef1148bff60afdbe76dbd05e121ab1",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "11ce40971c9c3108ca4a2c928f6aaf92ef15d3789c5a6bf485b0c609ee6125ff"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "90190d7f6f4f262f7bb04bb01bf803bd07882772769bae9cc69cab44540f169a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 51,
                  "end_line": 691,
                  "start_column_utf8": 23,
                  "start_line": 691
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "35a0bb8944e5cff8d28bd3056be0abf2c1ef1148bff60afdbe76dbd05e121ab1",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "11ce40971c9c3108ca4a2c928f6aaf92ef15d3789c5a6bf485b0c609ee6125ff"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "96e1a051f5c85746567a1cb67a8357b12218565291d1293146534f3c4ac67fb6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 770,
                  "start_column_utf8": 23,
                  "start_line": 770
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "aa0e841315a34f2416f4eea9a799b8d0b573b5af51a5c65b2b229e8fb29cfd85",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 441,
                  "start_column_utf8": 23,
                  "start_line": 441
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "c298a64a891442cca361a0cfbe9a56aec20dd53fa5b3c9242510253849d055f3",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 1126,
                  "start_column_utf8": 23,
                  "start_line": 1126
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "c59ceef991fa19bf4b6cfd5184d01737af2d7392d947dbad28ed79c3e52aed9f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 51,
                  "end_line": 539,
                  "start_column_utf8": 23,
                  "start_line": 539
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "35a0bb8944e5cff8d28bd3056be0abf2c1ef1148bff60afdbe76dbd05e121ab1",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "11ce40971c9c3108ca4a2c928f6aaf92ef15d3789c5a6bf485b0c609ee6125ff"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "caf91ee1be274dd4deeb29efe93272ad991500ba7694a310e0b0d8fb32cc0c2f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 478,
                  "start_column_utf8": 23,
                  "start_line": 478
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "d97e7f44e2a3ebcad599b36922e21af4a29ca400c229775646cf8474f370427e",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 41,
                  "end_line": 917,
                  "start_column_utf8": 23,
                  "start_line": 917
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "7454ca2a362c06adda66001eeb1ad2a695e62cbcfc640a26f462c0d07a57142a",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "c47b5dad90276426081fad8e24f33d740403b50b8d15160ca161fda3d8c17a8b"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "dea959eb768567fac78411f40f8fe97ac83bc16d253136fae6c002a1d29c24ab",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 813,
                  "start_column_utf8": 23,
                  "start_line": 813
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "e125c990554b31f4b0354c3f66cd7b42a43196dce465848b5e193cea15545c1a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 962,
                  "start_column_utf8": 23,
                  "start_line": 962
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "ec6cdaa5e1e6ec3c42eca58bb8aff580b1df8054b8bb36dd137acd3a8cbcca52",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 505,
                  "start_column_utf8": 23,
                  "start_line": 505
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "46abc9c1b1b01ac3076f5df83b17625a2d03f20ba003dc70a9303a6921c29f63",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "fefad34c08499d09cbfbb30bd964bf4e93459e93e2da7c30cc2ec66e2a8c3171",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 1117,
                  "start_column_utf8": 23,
                  "start_line": 1117
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 4,
          "address": "src/devtools/model_serving/errors.py",
          "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
          "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57"
        }
      },
      {
        "best_supporting_source_rank": 37,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 37,
            "address": "src/devtools/commands/execution.py",
            "content_identity": "6062be2b0271fd1e81ffc10e2b3fb8da2ab873948fc1afcfde4dd129d24ad6cd",
            "document_identity": "d3fbdedaaa3df7f439f63fabdbd581db397a8f40a8815686454e7ed3abde2676",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "32225c608ef488a16b02c8c3f30ddd381f6da94588973c8f98577cd11aaf3f8e",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 31,
                  "end_line": 58,
                  "start_column_utf8": 15,
                  "start_line": 58
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/handle.py",
                "target_content_identity": "7cc05c460e79955c6d36edf8b46eb4ee3314eb60e7116b5f4129b9aec4863d23",
                "target_declaration_identity": "9edededc280a6a290edce9f8b4328283ccaefe6dab2dfa8daf1ce5bea4bba401",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "db0063249633c6f6b54d82f060e5be2e2e8d7f2820fad8a0cd2377b601b4b2d6"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 44,
          "address": "src/devtools/commands/handle.py",
          "content_identity": "7cc05c460e79955c6d36edf8b46eb4ee3314eb60e7116b5f4129b9aec4863d23",
          "document_identity": "292e2106000f511491087016a527aafd75292b449a6bb8c230f6233c90d18be3"
        }
      },
      {
        "best_supporting_source_rank": 37,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 7,
        "sources": [
          {
            "a_rank": 37,
            "address": "src/devtools/commands/execution.py",
            "content_identity": "6062be2b0271fd1e81ffc10e2b3fb8da2ab873948fc1afcfde4dd129d24ad6cd",
            "document_identity": "d3fbdedaaa3df7f439f63fabdbd581db397a8f40a8815686454e7ed3abde2676",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1397a8157b12e0ebe93c4fb0dc4eae43696bf6016cd9fd50c15c591dfb6f8014",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 30,
                  "end_line": 249,
                  "start_column_utf8": 18,
                  "start_line": 249
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "7aa0641e45834e2216642a17ecb27479905e921b1a30744c887f663c2c3bc8d6",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "fe75ae35cee4cb363b31cf103c3c4ca2c7360bb32dd2048e897786d0ac0bb058"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "40c88e977f138e7031ffaf0a2ae08a4c67bd0bdc113b00b864a6e8b5d4032141",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 57,
                  "end_line": 129,
                  "start_column_utf8": 38,
                  "start_line": 129
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "44e7b7e6167510001de8069e5cb86bad3c1bd5a3ab5fcfb450f70e536e134922",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "73fd8b2c2820090404cb5fdddd4945addb11c07b97e22e73c14693ec42fcb916"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7c9dbd141ec9b049294e5aa8945e666c2e3f9f104559b71d82d22d96d0c806d9",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 41,
                  "end_line": 122,
                  "start_column_utf8": 22,
                  "start_line": 122
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "44e7b7e6167510001de8069e5cb86bad3c1bd5a3ab5fcfb450f70e536e134922",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "73fd8b2c2820090404cb5fdddd4945addb11c07b97e22e73c14693ec42fcb916"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "b244b7f226f94831a9820fd03596c33613069d18236fc424c3e8f5dcc883ecde",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 203,
                  "start_column_utf8": 18,
                  "start_line": 203
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "a6cc75bc896e0f506df7c821a3e4c6c7335019712fb092fe3dd0d0a473d82fd4",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "50187b40e83b208fa6d990877fdc432dea5afcdc57f6a719002b0f831fff296f"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cec7d5463c5ecb401466c575f575898fd557e9fc6b708efc1614c83005f98a0d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 115,
                  "start_column_utf8": 26,
                  "start_line": 115
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "7aa0641e45834e2216642a17ecb27479905e921b1a30744c887f663c2c3bc8d6",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "fe75ae35cee4cb363b31cf103c3c4ca2c7360bb32dd2048e897786d0ac0bb058"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "f06afa5030e7ba07f8e496775d67bc14851e7d4186f3024316c9a43ff1c90a25",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 146,
                  "start_column_utf8": 22,
                  "start_line": 146
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "7aa0641e45834e2216642a17ecb27479905e921b1a30744c887f663c2c3bc8d6",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "fe75ae35cee4cb363b31cf103c3c4ca2c7360bb32dd2048e897786d0ac0bb058"
              },
              {
                "derivation_identity": "1e8a689958f76dee4c84e7aa7262967e80d02d65d6010037ba1f1ab00e734d18",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "fd285a41655d3c645df255a9edff6471ee02b86aa56aff9dabc84d5d15afdff1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/commands/execution.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 129,
                  "start_column_utf8": 16,
                  "start_line": 129
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/commands/errors.py",
                "target_content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
                "target_declaration_identity": "a6cc75bc896e0f506df7c821a3e4c6c7335019712fb092fe3dd0d0a473d82fd4",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "50187b40e83b208fa6d990877fdc432dea5afcdc57f6a719002b0f831fff296f"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 52,
          "address": "src/devtools/commands/errors.py",
          "content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
          "document_identity": "a2cb859564c6ff8bd01de9b1ab589f654d65cdff8023a216596b8dd49f714bed"
        }
      },
      {
        "best_supporting_source_rank": 29,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 14,
        "sources": [
          {
            "a_rank": 29,
            "address": "tests/model_benchmarks/test_storage.py",
            "content_identity": "80ce0263623b051a0c137d7ccb579ab0fb97b4d1a99db6ed30821d7f6782f4b6",
            "document_identity": "0108747cd2d8c830ad1462f25f94385d5e4bac401848643a8ad48bae2666afc8",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1329a68721ab94d14f9f68194a988737daf618c7297b672138bd0deb88ae5264",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 253,
                  "start_column_utf8": 8,
                  "start_line": 253
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1a054ba4afa97a2e89c7a56a50fe71904f43f7bf228e62e83df0986ae932a6b9",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 189,
                  "start_column_utf8": 11,
                  "start_line": 189
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1a98e5840c4093f72d177fe54008515f461cc6b6cbdfb4ce16ae6be601dc252d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 122,
                  "start_column_utf8": 11,
                  "start_line": 122
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "20e58cf477716d64f7baf9640312b53e8a7877577435763beefbe21c5319a2d6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 104,
                  "start_column_utf8": 11,
                  "start_line": 104
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "2e6b0066890dbfa1f3de578b59ec61094c398c2e1c9ec0eb72b0b4fa1c27f34c",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 284,
                  "start_column_utf8": 12,
                  "start_line": 284
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3e048305584b1a618cf47d6d041699a8ccbdfc5f8438c5631b83b3e2ccaba9b0",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 206,
                  "start_column_utf8": 8,
                  "start_line": 206
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "877456173a320672cb5f8d7198da7fa61c1ca810e64f9d99acfe53a92d4b7290",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 112,
                  "start_column_utf8": 11,
                  "start_line": 112
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8c8d2838b04b3dd0df9806756f17e2a233b74188a6f797d5e32d13d4a82c7f42",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 159,
                  "start_column_utf8": 13,
                  "start_line": 159
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "91078e27dbd69dfcf1e260cbdbdfc7ba40b8f97b14560d6fd055fc769acafd9e",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 226,
                  "start_column_utf8": 11,
                  "start_line": 226
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "baaee555ea3b29cd1a681b91e164d73a4c00dc36e5bcab33d732c4bf98c2b665",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 213,
                  "start_column_utf8": 12,
                  "start_line": 213
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "bb7cac41e49790722e549fc56a58e4fae04c93f67406b52f2502f2e690edb870",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 269,
                  "start_column_utf8": 8,
                  "start_line": 269
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "dd796d53505f430b2c00056f95430d33b3218e2aeaa15284c05830cb1426c17b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 140,
                  "start_column_utf8": 11,
                  "start_line": 140
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "38ce61f68e96c79659b20cf0705806cbaabc6445af11ac187815f2448621e36e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "5c576088970188bbb398d076dac9a1956c270b8fc875f3cc747736219614eaf1"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e30eeff83f63d46bf7756c2e08b82687ab93838d9fcbd0ea990dd77a0fe5568d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 89,
                  "start_column_utf8": 11,
                  "start_line": 89
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              },
              {
                "derivation_identity": "e15dfcfc0fbe54e96f192cdb45b7584a63f4df04413fb898ed1fdd603940774b",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ecd0ee1c0b4b55f1a274133740e4cfa8c1c92b1b6a44c0aca411aa1ff7c492fd",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/model_benchmarks/test_storage.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 214,
                  "start_column_utf8": 13,
                  "start_line": 214
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_benchmarks/storage.py",
                "target_content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
                "target_declaration_identity": "7aa1aa986b2227cc06626889f13ca838d8dfa45016257c7d5af04a2e10c15b69",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9a0ca417397770603c5a25e08c72befb8f133d317fc28c3c9d0bf5f024b28206"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 57,
          "address": "src/devtools/model_benchmarks/storage.py",
          "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
          "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62"
        }
      },
      {
        "best_supporting_source_rank": 26,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 2,
        "sources": [
          {
            "a_rank": 26,
            "address": "src/devtools/codex/agent.py",
            "content_identity": "f9ea6307d8286b4dc9547d55553f4c2fec144099143160ebf7e31e2e9f123936",
            "document_identity": "283e13d0f5b77051160e3bbcaf101c77477bb5b9a8553b0e9b3a50a2ec4d1646",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "2c6650e6a4de995617967f614b3e5eb61e99594eee7508550fa83467ad5e3367",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7cc3836098ef37f69622586d17c38d14a2be75faeb83f76aa0ce72fdfc8aeb51",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/codex/agent.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 85,
                  "start_column_utf8": 18,
                  "start_line": 85
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/codex/errors.py",
                "target_content_identity": "efbdeba3848aef33b7d210052496447c9d5fb190674178cebed08405a58074ff",
                "target_declaration_identity": "a70a8e640cf1cc42fbef54b70bf25dec1bb243b0e30d93cbd11ae81e2ea050de",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "4cdfd570f697e2f5e9774e17aeeaa8d8790d874487f6b6b9f19050a5144ec559"
              },
              {
                "derivation_identity": "2c6650e6a4de995617967f614b3e5eb61e99594eee7508550fa83467ad5e3367",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c56cf5492e8fa73a53cb8f9f4caaa0ca09206f9a9e66e7dda70eae1023135a7b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/codex/agent.py",
                "source_range_utf8": {
                  "end_column_utf8": 35,
                  "end_line": 82,
                  "start_column_utf8": 18,
                  "start_line": 82
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/codex/errors.py",
                "target_content_identity": "efbdeba3848aef33b7d210052496447c9d5fb190674178cebed08405a58074ff",
                "target_declaration_identity": "f9a6df8e75821247bf326be13f245196da795321935d5b5a64d5b300dceaf1ae",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "360117cf9b8b595632b1252e7fb854fef0e5f3fdc455490c64ccf31fcd8f6f96"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 66,
          "address": "src/devtools/codex/errors.py",
          "content_identity": "efbdeba3848aef33b7d210052496447c9d5fb190674178cebed08405a58074ff",
          "document_identity": "e4a614a5a4c482b021a40190d1d13fd583598568f2cff6b4d9a3d8876306d4c7"
        }
      },
      {
        "best_supporting_source_rank": 24,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 24,
            "address": "src/devtools/tools/filesystem.py",
            "content_identity": "a976b9868ea3ec236496d2516b31bbb645f03e4a54ba2dc68476a80e3e1ee8ef",
            "document_identity": "97d27b9c43fef58875abea365716c6d39e8ed308c604ac874a2856b16ddd4ba9",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "f7489f04b320afd67dedbc6068734cb8b5c115553891c676bebfe10b7a666548",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0896f94c5a0bf75cd0703a49359b91874e34cc9c842b81bf4445dbc7b379483a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/tools/filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 54,
                  "start_column_utf8": 11,
                  "start_line": 54
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/paths/resolution.py",
                "target_content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
                "target_declaration_identity": "24e09f6bc62869f09c95d071b64f0fc1f49907e211b233711299c7db233bcf6c",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "c3aebb284cb7a8c446f415396c9df2e95bd5cdd9c6e74ab588fd98d110ddc645"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 71,
          "address": "src/devtools/paths/resolution.py",
          "content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
          "document_identity": "f76c07f901bf265e3dd7ef1f5046120533b084e180c574736b710838872007d4"
        }
      }
    ],
    "counts": {
      "local_pairs": 6,
      "qualifying_occurrences": 57,
      "status": "PASS",
      "support_source_target_pairs": 7,
      "supported_targets": 6
    },
    "frame": {
      "corpus_id": "eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028"
    },
    "information_need": "Where and under which lifecycle constraints are caller settings translated into reproducible provider launch arguments or environment values?",
    "local_pairs": [
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 3,
          "address": "src/devtools/model_serving/docs/overview.md",
          "content_identity": "10ff6484d598b13a6ad26adc41f45a7da6f1bb5cf37d8fd34aea055509f8e7ea",
          "document_identity": "5654a9afbf6e9a7c15247f73ba80e0fd9fa4d031bb180902fcb0110742f1f535"
        },
        "query": "Q2",
        "target": {
          "a_rank": 4,
          "address": "src/devtools/model_serving/errors.py",
          "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
          "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 43,
          "address": "tests/commands/test_execution.py",
          "content_identity": "4be50311fc81376286545eb02fecf0725e24d6620fcd91e192d3b6a75dfd60f6",
          "document_identity": "fb50df1403ac0cc8b8745bfcb8dc32aae722b13ef44a6fcd1bbff883620e3478"
        },
        "query": "Q2",
        "target": {
          "a_rank": 44,
          "address": "src/devtools/commands/handle.py",
          "content_identity": "7cc05c460e79955c6d36edf8b46eb4ee3314eb60e7116b5f4129b9aec4863d23",
          "document_identity": "292e2106000f511491087016a527aafd75292b449a6bb8c230f6233c90d18be3"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 51,
          "address": "tests/codex/test_agent.py",
          "content_identity": "8ff2ef564dddddd6a43757bbadf5785b54d4d7f9fc47167d0f1d0831d4f38dab",
          "document_identity": "dbecb518b7ef0578fb29b5348a4588de3b04500616218138bbcbe1d779b2dec2"
        },
        "query": "Q2",
        "target": {
          "a_rank": 52,
          "address": "src/devtools/commands/errors.py",
          "content_identity": "f9c739a2cd9c2aa41ccbbb4fefce66e11db348845f51a4c9c5f6019ac2192795",
          "document_identity": "a2cb859564c6ff8bd01de9b1ab589f654d65cdff8023a216596b8dd49f714bed"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 56,
          "address": "src/devtools/persistence/docs/overview.md",
          "content_identity": "a98caba801e659702dc5e9cd3c16c4db06b18835a2a92906c09f483e9adbda9c",
          "document_identity": "a78d421c3e63b75a5a63107b0fe42f4cf4f6e9a09089548e574f6d373159e5c7"
        },
        "query": "Q2",
        "target": {
          "a_rank": 57,
          "address": "src/devtools/model_benchmarks/storage.py",
          "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
          "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 65,
          "address": "src/devtools/runtime/runtime.py",
          "content_identity": "e0a00ceacd3aa37de36947ab8da276f5c46ce640544e87541415ac2da8077149",
          "document_identity": "e19bda6e0ee724b945f6b7560137e64e4deb99024851976f19ad3b2044a1ce86"
        },
        "query": "Q2",
        "target": {
          "a_rank": 66,
          "address": "src/devtools/codex/errors.py",
          "content_identity": "efbdeba3848aef33b7d210052496447c9d5fb190674178cebed08405a58074ff",
          "document_identity": "e4a614a5a4c482b021a40190d1d13fd583598568f2cff6b4d9a3d8876306d4c7"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 70,
          "address": "src/devtools/time/docs/overview.md",
          "content_identity": "1b65aaadc3e577fa186a20b52c5deb4e0218750db828ae2bf25fedbacfc7ef55",
          "document_identity": "55bd9644b6a573386a491430bf3b48f96494b5daaec5db9eaaebf8f1a6ffff84"
        },
        "query": "Q2",
        "target": {
          "a_rank": 71,
          "address": "src/devtools/paths/resolution.py",
          "content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
          "document_identity": "f76c07f901bf265e3dd7ef1f5046120533b084e180c574736b710838872007d4"
        }
      }
    ],
    "obligation": "O2",
    "query": "vLLM launch command Docker environment arguments configuration ownership readiness",
    "query_identity": {
      "task": "case-0019:historical-development-003",
      "value": "Q2"
    },
    "task_identity": "case-0019:historical-development-003",
    "timings": {
      "annotation_construction_ns": 909500,
      "canonical_a_ns": 18971000,
      "complete_online_equivalent_ns": 51230600,
      "predecessor_pairs_ns": 47900,
      "support_projection_ns": 31302200
    }
  },
  {
    "A": [
      {
        "a_rank": 1,
        "address": "src/devtools/model_benchmarks/docs/overview.md",
        "content_identity": "5e17ffbd9f5bebf7163cac0f69bf29837fb8ea5b8d0585934b48d91ed54ca8ae",
        "content_score": 20.058005506767522,
        "document_identity": "64bd6aa29544ac4e906ca4aa6a0e5737778120ffd801eca4e814fe439a775e1d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 20.058005506767522,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 2,
        "address": "src/devtools/model_serving/docs/overview.md",
        "content_identity": "10ff6484d598b13a6ad26adc41f45a7da6f1bb5cf37d8fd34aea055509f8e7ea",
        "content_score": 19.756760791521355,
        "document_identity": "5654a9afbf6e9a7c15247f73ba80e0fd9fa4d031bb180902fcb0110742f1f535",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 19.756760791521355,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 3,
        "address": "src/devtools/model_serving/vllm.py",
        "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
        "content_score": 14.572668341757282,
        "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa",
        "filename_score": 5.001706663351954,
        "filename_weight": 0.25,
        "score": 15.82309500759527,
        "weighted_filename_score": 1.2504266658379886
      },
      {
        "a_rank": 4,
        "address": "src/devtools/model_serving/errors.py",
        "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
        "content_score": 14.418190879215214,
        "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 14.418190879215214,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "src/devtools/model_benchmarks/storage.py",
        "content_identity": "886b1b55f3d848778fdd338d578fe41e336bebc9fe00d17cebac2873340c551f",
        "content_score": 14.054754742900037,
        "document_identity": "e6010f6f5ba5b3f5f127086bada5900ad2f51859c524b3cc041cae57e139fc62",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 14.054754742900037,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 6,
        "address": "tests/model_benchmarks/test_storage.py",
        "content_identity": "80ce0263623b051a0c137d7ccb579ab0fb97b4d1a99db6ed30821d7f6782f4b6",
        "content_score": 12.756245527927176,
        "document_identity": "0108747cd2d8c830ad1462f25f94385d5e4bac401848643a8ad48bae2666afc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.756245527927176,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 7,
        "address": "tests/model_serving/test_vllm.py",
        "content_identity": "7e82bb36c742e988201122268e9a7e24e135c1bf00dc59a09ce26620f2a1a39a",
        "content_score": 12.504161426654614,
        "document_identity": "d44d6fdafbb9f86def873e6f465fa47de4d02519cb323d8054b6ad3544eba0e5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.504161426654614,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 8,
        "address": "docs/roadmap.md",
        "content_identity": "4b747349e12a0fea64c109bb067f3fda98cae0e849049f8c4a0916366c471e0d",
        "content_score": 12.22776793084763,
        "document_identity": "d6a183448bf38da43dd86aa6bf1d3bcef7b59fd0b258de5ab311cf891b7f9289",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.22776793084763,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 9,
        "address": "src/devtools/model_benchmarks/models.py",
        "content_identity": "a86307830643681250686a83f3f58f28af4285f081a9699bc2c8f0c025aac32d",
        "content_score": 11.689949634811933,
        "document_identity": "db5b32f575cd2fadaa883bcb98beffa74712fce8e804ec59d3c60f6b908263ae",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.689949634811933,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 10,
        "address": "docs/documentation_map.md",
        "content_identity": "662d0a9b30f6677959e052a88a96e9e4194cf92dde13e55d2ea165682d677492",
        "content_score": 11.378268534221633,
        "document_identity": "dbc3e78acb0094732f6ebdc1c332b5b53db3e298c36c4e3fd069c1625f62f328",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.378268534221633,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "tests/model_benchmarks/test_models.py",
        "content_identity": "41dfe7dcac145b42432ed1488a93980f3a285d834a0dce4d1963602bd40381f9",
        "content_score": 11.001279924257265,
        "document_identity": "37e88862ae59e7a1b564d340f7f1db521553ed37509c3683f6d552f8d5e8ce09",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.001279924257265,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "docs/architecture.md",
        "content_identity": "4aa8890280cd2a5e18582a6330fb79e6204212e6e5239ac6def2671153a27301",
        "content_score": 10.609027890724077,
        "document_identity": "c2f40d6caa321ca6908e902184fca3c10593079ae912ecd9497b38143ed7f98f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.609027890724077,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 13,
        "address": "src/devtools/model_serving/__init__.py",
        "content_identity": "dd774516574c2587458b0a4a2d988c1b1237e048f13742e62a615a34015e083b",
        "content_score": 9.582331873793201,
        "document_identity": "314ee2d7830272292a33cde1d474f6a765e65fd0e132e86d015f7dcc889d0e79",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.582331873793201,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "05b0f9f30fe3b6abc84b4fb4f67b0b323b862178fe6ff5412ebbf8fdcf37fbe7",
        "content_score": 8.400685302291024,
        "document_identity": "071ad10da57aae6617e089e907e3d6b043d0c0e076f8e988f4d3e5ca2b50fecb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.400685302291024,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "src/devtools/model_benchmarks/runner.py",
        "content_identity": "d0afb5a935a181be03814131ecd7a8af1d4be4a6c7eb7d0a5b8865f54b39665d",
        "content_score": 8.361090828037652,
        "document_identity": "8b4374f777bf3a6cd0f64aeeaa152327343b7ac96086917d397cb0c8ea275c48",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.361090828037652,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 16,
        "address": "src/devtools/model_serving/huggingface.py",
        "content_identity": "94bc2f3b0875b57916b614595f79d6a440d860b3fe40ccf85d1545e23c60b961",
        "content_score": 7.9081254962271945,
        "document_identity": "11cef5346b33ddae2e87098e738ad4fb6492b28318862e9283542b4d289fa33b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.9081254962271945,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "src/devtools/paths/resolution.py",
        "content_identity": "fe70de9698af2e43c5f82df8196976eee2c7ed18300174075cf646a53141a116",
        "content_score": 6.915309976763278,
        "document_identity": "f76c07f901bf265e3dd7ef1f5046120533b084e180c574736b710838872007d4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.915309976763278,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "tests/model_serving/__init__.py",
        "content_identity": "315fa49644e49326f585843a8e7ab22d85af9c2e86425675a143021afe86550e",
        "content_score": 6.211922571865392,
        "document_identity": "dbedecdce42ba6df9177d73fbf4ec402a7a09d984838042370d25bc2e5fe070a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.211922571865392,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "src/devtools/runtime/runtime.py",
        "content_identity": "e0a00ceacd3aa37de36947ab8da276f5c46ce640544e87541415ac2da8077149",
        "content_score": 5.788251174611271,
        "document_identity": "e19bda6e0ee724b945f6b7560137e64e4deb99024851976f19ad3b2044a1ce86",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.788251174611271,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "tests/model_serving/test_huggingface.py",
        "content_identity": "f51a3f3658c02df2b5ba9257cfe9d04fd28bc48a25bd29c6239ebf390b07e1c7",
        "content_score": 5.646390244403125,
        "document_identity": "b9d1e775fff180ae470f15d338184d0eca1441e149a73e3681dd7f8bb3f3807d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.646390244403125,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "src/devtools/time/docs/timestamps.md",
        "content_identity": "99624791d382952604772ffd166b2d4bba5dfda31762d8c680d6c60a6a9b3bae",
        "content_score": 5.394713331292329,
        "document_identity": "43fa6ed9f8db160717ea0094e31faa5b48f8cbc119c5a1ffc30d2b8cb3177523",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.394713331292329,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "src/devtools/commands/docs/execution.md",
        "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
        "content_score": 5.126906477780095,
        "document_identity": "4e3069aa5ade6ea9d8a30bf724b534a1e18e291454b3febf0bb6a34a615b11a6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.126906477780095,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "src/devtools/runtime/docs/overview.md",
        "content_identity": "1e43fe503ab74d316fe5cabd9bae45062146e91900c96e463f2c8bb6b91a519b",
        "content_score": 4.827054130460504,
        "document_identity": "8c1e8c6f31f875a0a2fbc0c3783a481ac627231a10d5bfffe61060091e4ac9d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.827054130460504,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "src/devtools/commands/models/command.py",
        "content_identity": "fca918a60dbdc006190a8287ab347dec64b467573bbae1ca40d37322ca974494",
        "content_score": 4.797336871795768,
        "document_identity": "e0ba027f203c191efb2dc15d16ce0d3b6148481f93defebea9955a86ca3f9bbb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.797336871795768,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "src/devtools/codex/docs/overview.md",
        "content_identity": "448384c98365dd51f9fcdb028a295fcbd88e35bccb2b0035c37f8a9ed513e64a",
        "content_score": 4.767374778115492,
        "document_identity": "1ccdff2bcbf8a9c28a9fa334d40993219852f66dd64302588ec5745af642d568",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.767374778115492,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "src/devtools/paths/docs/resolution.md",
        "content_identity": "75a34ebc5ec26232444c717f0caddf1fd15e96d9d4b50909d9ca2926b597c8c2",
        "content_score": 4.494171582883721,
        "document_identity": "01b5edf89f0d6bc4e18e407e28f6d5b3644b87aae3fd12c0408227aa3f0d7f08",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.494171582883721,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "src/devtools/paths/docs/overview.md",
        "content_identity": "b666f9369d8772d77c9abdc29e512f57f9146ce73494a549acf1a2136159e776",
        "content_score": 4.456726123097251,
        "document_identity": "1659fad7a2b4975dccc5dc5b8c75733ce9f99b2003ade71fb45e5421e509b416",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.456726123097251,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "tests/conversion/__init__.py",
        "content_identity": "dd56c70d043fa64eb4f375989b1c5536b234c0b37fdf7009a44955cda33def1b",
        "content_score": 4.224721958586645,
        "document_identity": "9773cfd38690f2ea949bbfd0649dd8d439d5a8478515d917c69ad8d54a8df2ff",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.224721958586645,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 29,
        "address": "tests/model_benchmarks/test_runner.py",
        "content_identity": "a251929371fea3957510e4f119190ba92238203288e881a9a5560bbb6b7bf2de",
        "content_score": 4.170294513404597,
        "document_identity": "b24da91fc545a331cdc92b6f31186d7e6d8e9b2ce6424b5fbc49a2f274f05b21",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.170294513404597,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "src/devtools/codex/agent.py",
        "content_identity": "f9ea6307d8286b4dc9547d55553f4c2fec144099143160ebf7e31e2e9f123936",
        "content_score": 4.006283558660208,
        "document_identity": "283e13d0f5b77051160e3bbcaf101c77477bb5b9a8553b0e9b3a50a2ec4d1646",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.006283558660208,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "src/devtools/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "content_score": 3.7441911294935286,
        "document_identity": "3d7c64d8314abc861c526718abfe4bbdfaf6cb64bce67f3bf6a41289877855d0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7441911294935286,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/filesystem/docs/csv.md",
        "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
        "content_score": 3.717746826637259,
        "document_identity": "9b541213ab6a90a58f4d604a5c483ee9a8835d6cd3a56a82a43350eefb9b62fc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.717746826637259,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "tests/filesystem/models/csv/test_dialect.py",
        "content_identity": "fcc452b53b8db5bdd1063454999e9bbe262c30f2f2b72e6122e8bbec96de7df0",
        "content_score": 3.459726073993173,
        "document_identity": "1e879ca248e39813c3c354c21de8b5982dc80d7fff6bea34739ff82a4897fef9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.459726073993173,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "tests/agents/test_models.py",
        "content_identity": "17b484383974535ec3afdd0b1c89d0226313df345d2a93ba3f0f10e33b02d002",
        "content_score": 3.3439808220260008,
        "document_identity": "7d9edcced435e29e6df02437ed4d770c62f30ba092ecad2dfe8e15bd6bc0a360",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3439808220260008,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "tests/filesystem/test_reading.py",
        "content_identity": "b6a106c7dea09881ab91b334943f85bf0075704afe166be64027e4f6b2475d59",
        "content_score": 3.343665763775607,
        "document_identity": "d6fc5e8fe9655ef353a712da131ad3390516dd90d2dc4104fd17c294eb474ad2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.343665763775607,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "src/devtools/regex/docs/overview.md",
        "content_identity": "a44d453d2c67e0ac5e0b065eccf37b4101fbbb4c69b3d7adfd26a0804460cd0c",
        "content_score": 3.1303001694376524,
        "document_identity": "d5960f9eea0bd1ff93ed35e008073d8f790d54e6ac86eeb7fb33536951cd515d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1303001694376524,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "src/devtools/agents/protocols.py",
        "content_identity": "ee30b82de86bc219077e6443082d3dd8aa3d0870f1de72eede73e484e3866494",
        "content_score": 3.1266065233778484,
        "document_identity": "2bc3a260764f3ccbe7becadd6c7814fe6d5d8a8c1ec1e81faa7f217f0d470447",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1266065233778484,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "tests/conversion/test_conversion.py",
        "content_identity": "bf39df57853b170a57f39b6c0b0599e7939369e2d5605e4bf7924dbeb6166839",
        "content_score": 3.123915230793965,
        "document_identity": "2bc94e2db4dee31186a5107e5fd3a767d5a6f183d03acd49c9079755c5499041",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.123915230793965,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "tests/commands/test_models.py",
        "content_identity": "2fdda3a7f7d7909792df8cdb81628b2bd757436bc0e7512dd31a4f55b56480d2",
        "content_score": 3.0765616906494677,
        "document_identity": "f07afe9d3ac89f6c2f6b993b1d0c2c79e1482af6082982fec31c01df238a33c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0765616906494677,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "src/devtools/agents/docs/overview.md",
        "content_identity": "0ff08aa6729dee470613e8b7dd1a77bef613edbd0f878e387b29fc793a3daa9e",
        "content_score": 3.0256206637592635,
        "document_identity": "228465edc59ed56ac12b1603e1e471cad8762dd698095f6ace7672a275ce7194",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0256206637592635,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "src/devtools/filesystem/models/csv.py",
        "content_identity": "6f687de872e55eb58981ea47b71b9dc0a493619631f38a47b675a04f6f6c4b0c",
        "content_score": 3.0182789924201865,
        "document_identity": "9f2f8892cad21f3c7916cf1c7692f4e46dd97c0e0b2a9ce793dc9a96ae799e52",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0182789924201865,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "src/devtools/agents/models.py",
        "content_identity": "b5e7d49ac43f8b75f46d10eb707cc7e42d40ebafd0d6b8961fd67d38efd30ec0",
        "content_score": 2.98983441873901,
        "document_identity": "9f61f8fa11f2fe8bbc8d19d6a3d75aa2c7f6443917c5c7b9d01269bd0d931a2f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.98983441873901,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "a98caba801e659702dc5e9cd3c16c4db06b18835a2a92906c09f483e9adbda9c",
        "content_score": 2.8840941614143127,
        "document_identity": "a78d421c3e63b75a5a63107b0fe42f4cf4f6e9a09089548e574f6d373159e5c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8840941614143127,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 44,
        "address": "tests/filesystem/test_writing.py",
        "content_identity": "30079796e8846f8a72e450e721c29eb08260865d986146c2177666eca461876f",
        "content_score": 2.8242462022541943,
        "document_identity": "c5232899c79ff013b63f61e41aca4d65f4a8bf1717a9acdb0dd64b1965081b0b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8242462022541943,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "tests/filesystem/codecs/test_json.py",
        "content_identity": "05c3f70f08101c7036b46203cde9151f2ccbdf9eae53c3b51f25d69630bf74cd",
        "content_score": 2.8054939483084134,
        "document_identity": "7944912926f91e5696d59c53121d8c9fffd7f6a8e40ececf8f6f495f536a4798",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8054939483084134,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "src/devtools/context/docs/session.md",
        "content_identity": "49bccd7bcb45ef7ba4fd51ca73ed92191dd9ef4f8f67f1c31dff4a9ecfc8ca78",
        "content_score": 2.7824850271284634,
        "document_identity": "8e53d312bec3c81992a1d3f6f99062c07d903353ec96e102930f6d3707c6981d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7824850271284634,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "tests/filesystem/codecs/test_csv.py",
        "content_identity": "80cf94d96accf77ccc6033044449713d04ca932bbb5dbc166b00609eeeab2ffa",
        "content_score": 2.7632561071609447,
        "document_identity": "f673deb0a746afdfe14d2beb54c4d85793f15325a705573bac5e7eddcfd866c0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7632561071609447,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 48,
        "address": "tests/filesystem/codecs/test_text.py",
        "content_identity": "0ff02a6315ee9bddfc14d368e1e368df13185822c94a8a44447faa419a9adbd7",
        "content_score": 2.7420897788181264,
        "document_identity": "3a50bc3afdc0e045557c9098c3910fd3666f1b2dccfbbde770c1a7372c4ed65e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7420897788181264,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 49,
        "address": "src/devtools/evidence/docs/overview.md",
        "content_identity": "66adc8f581f66b172f40112de90f14d0ba3415dd8e0c146ce968bd64875fd84e",
        "content_score": 2.677748600904346,
        "document_identity": "f83119f54160aceff357e91d04396df9681642266cdee5e8547d3aaca17847e3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.677748600904346,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 50,
        "address": "src/devtools/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "content_score": 2.6316693025388194,
        "document_identity": "5a479701e724b9494b94e51f94b81f7f92736f61dfdc72d0e2e39f5fce9a108d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6316693025388194,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 51,
        "address": "src/devtools/conversion/conversion.py",
        "content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
        "content_score": 2.6183697453035117,
        "document_identity": "635c003c50d44b1b2fb96fddf8d418cd935a97cc778c8237b227af1a39480452",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6183697453035117,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 52,
        "address": "src/devtools/conversion/__init__.py",
        "content_identity": "04afbeed88f3abe28bb1222c2be2f59a420cb26cd402f73b1743e3bc6bb278d8",
        "content_score": 2.604086554886396,
        "document_identity": "032269b62334e1c583e4d1a4dc4042c6843e5fed15b4c370fa2b3bf95890585c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.604086554886396,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 53,
        "address": "src/devtools/context/docs/overview.md",
        "content_identity": "81687d5d90b3d6256043e0b7180499a9c2e8a38308004734f442f2bd68ef814e",
        "content_score": 2.5238562153135455,
        "document_identity": "4ea877ce43c74fc552aca23ddfa7183cb62baec0025a296839b34eb963503b1a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5238562153135455,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 54,
        "address": "tests/context/message/test_message.py",
        "content_identity": "c938aa9bb8f681e511cb4bc77599638a6a0e3bcfd4c0a5db2631cbbb362bdfd3",
        "content_score": 2.4816349195233256,
        "document_identity": "4ad8961afb5eb615b83b1754449de8fc7def8f8b080e07fe62add9d97e85cb42",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4816349195233256,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 55,
        "address": "tests/evidence/test_terminal.py",
        "content_identity": "5124e9966871f62de778f967a8cbf5fec46dca4817a82dfa7f92c3bf89f73918",
        "content_score": 2.4678464476572186,
        "document_identity": "840ea06396d427bc41202473fa83a82e9043ada132ee6b236049825708344299",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4678464476572186,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 56,
        "address": "tests/filesystem/test_json_conversion.py",
        "content_identity": "11f62e3a545609cabf1370692ff5f87f8df06c79f4b1a350ffa78704d5b895ec",
        "content_score": 2.438593517047546,
        "document_identity": "52685390a733b4f131d80fa17a48a21a99f478ba1e4de940e65109de02f8d911",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.438593517047546,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 57,
        "address": "tests/paths/test_resolution.py",
        "content_identity": "4e67e1126083c9291f2b447c707eea484e0568c4d08cf3a74a8bad05ae72dcd9",
        "content_score": 2.4216904557037893,
        "document_identity": "4f6e81d7e7b3f289d22b876c5e388b0288a70043258cd65f2f51640e4d9e2f28",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4216904557037893,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 58,
        "address": "src/devtools/conversion/docs/overview.md",
        "content_identity": "ab30aacbedac2b8206a8542fb1991417f24ba25411ba3694c7a1c493b93ad2fc",
        "content_score": 2.4182619656968116,
        "document_identity": "23525f2e692359c3f25a04618e1ba12b73ca02cb8c36a11ed4bbbe5d48aab776",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4182619656968116,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 59,
        "address": "src/devtools/identity/docs/overview.md",
        "content_identity": "06b5801a244a5f40d898920d09d9d982f3d39c949c634e97fe1a7b308bb5d71a",
        "content_score": 2.416840618275297,
        "document_identity": "5a8c1181f7c4df5301fae0cc6d0d143ef56ad66d3855c1ccc7a4e0ebf9692442",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.416840618275297,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 60,
        "address": "src/devtools/codex/docs/cli.md",
        "content_identity": "3953468b726dec2f01bc64764587480964f91f8d435eeb5ff75498079781799a",
        "content_score": 2.392064287984616,
        "document_identity": "83cfc4e15d34d8e790c3d44453d92f7802a5ee42e33cb5633640a6f39b287b4f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.392064287984616,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 61,
        "address": "src/devtools/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "content_score": 2.3177350332141744,
        "document_identity": "36927bf0f9fb1706f691c0c472cd72fc6810926fd1e23e6b060c9983946950a5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3177350332141744,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 62,
        "address": "src/devtools/filesystem/models/json/scalar.py",
        "content_identity": "09dc9004664f8298b9291c883978a8f54d66838fbb2dbe29fd31c821ce88c4ef",
        "content_score": 2.299711223973266,
        "document_identity": "25174fb2a0b7abb3e3a255ea4340968d4c3bfed2e16d7c1d51b7b3774f994ab5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.299711223973266,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 63,
        "address": "src/devtools/conversion/errors.py",
        "content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
        "content_score": 2.2963137341269397,
        "document_identity": "357ff96b0096e1a6a07c3fefa44426868762d7183d9973c40623bcaeb5c408fd",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2963137341269397,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 64,
        "address": "src/devtools/filesystem/reading.py",
        "content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
        "content_score": 2.2392672793651274,
        "document_identity": "d1dead5ca20598c9246405ae3cf3f7b832014c3a90f062e715bebe2cda006f7b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2392672793651274,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 65,
        "address": "src/devtools/persistence/docs/sqlite.md",
        "content_identity": "75dd9fa49b1a2c3f97ca921d5abdf6435b59992ced1835a4e61a166cc0ead988",
        "content_score": 2.054594200255898,
        "document_identity": "efd8893881683fd42c0d9a3272b9f02b7bf79a614dd371491047e58d5381f229",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.054594200255898,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 66,
        "address": "src/devtools/filesystem/models/json/object.py",
        "content_identity": "4cc52345aaa32122f78f2093f58a3e3ce1bef9d462246b0e7e4ef49b397796d6",
        "content_score": 2.04081046368883,
        "document_identity": "8b3ef1f3220d6e1822e4349773168a52a94c3bffacd4bbd8ce1a41b53d25e14f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.04081046368883,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 67,
        "address": "tests/evidence/test_inspection.py",
        "content_identity": "7ab0e6767e722953631ad21d61e67dcc73752b5c97128dfe8f1aaa556ce7159e",
        "content_score": 1.945972853680872,
        "document_identity": "41554b22d5b3ffe5f636a63bce770b52af6fe408f048ea254f44cbcc18404f4e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.945972853680872,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 68,
        "address": "src/devtools/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "content_score": 1.8055146867134328,
        "document_identity": "d4fe14843762144d9f407bd944272e2695d5c60c925d8a4682d3bc5b2dcbe1ba",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8055146867134328,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 69,
        "address": "tests/codex/test_agent.py",
        "content_identity": "8ff2ef564dddddd6a43757bbadf5785b54d4d7f9fc47167d0f1d0831d4f38dab",
        "content_score": 1.7395655610091771,
        "document_identity": "dbecb518b7ef0578fb29b5348a4588de3b04500616218138bbcbe1d779b2dec2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.7395655610091771,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 70,
        "address": "pyproject.toml",
        "content_identity": "8b8936cdb9c1fcb9e096f1f4a64012a6c284669c8a28f3d5c3c92c204318b5e7",
        "content_score": 1.6873731906212757,
        "document_identity": "29d835b504b045e6868447878ab28cd3ac606a99ee8b597c4c767ddb95abdc6e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6873731906212757,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 71,
        "address": "tests/persistence/__init__.py",
        "content_identity": "edb967950ec1437b730ec9317b1ddf71b553e84dcc71fff66825f0afa8f6ee5e",
        "content_score": 1.55037615307401,
        "document_identity": "19c8ab310844f246f4889dfbb4b029952f3172a3576b86e161c4f1d732494dcb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.55037615307401,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 72,
        "address": "tests/runtime/__init__.py",
        "content_identity": "a8e0b0ba8f3dea608da98b13393f44ffa1d9e82a6e51a7196a785d81141cfc52",
        "content_score": 1.55037615307401,
        "document_identity": "e8249d7600667a38cb2464b7f0dfda83b23e816551d96605dc3647554baacd35",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.55037615307401,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 73,
        "address": "tests/identity/__init__.py",
        "content_identity": "318fe561871bac625099c7ec765f72d50cde7864749d33f99f94b088425fdb12",
        "content_score": 1.545001164584613,
        "document_identity": "064f900a915349bac6ddea09315a583d618d723afaef99e07f9100be21510906",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.545001164584613,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 74,
        "address": "tests/paths/__init__.py",
        "content_identity": "112b94984c3496a1b7b06dd0cbb40e3a542c54d32e54ef132770bf73844a4f22",
        "content_score": 1.545001164584613,
        "document_identity": "74d39d9b6e344a0a94b9f570427cfe23737d3df68e79e68a8b9b21a083408e49",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.545001164584613,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 75,
        "address": "tests/system/__init__.py",
        "content_identity": "879a8d83b877842bb5884828375b7858051aef530e6956484ad4506ac1d157f2",
        "content_score": 1.545001164584613,
        "document_identity": "f20759cc18cdcda0327044828c74bc0f7ba1e854f7ed4054f6a60cdb6ccb6eae",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.545001164584613,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 76,
        "address": "tests/time/__init__.py",
        "content_identity": "ab3d3080eb977f91154f659e95d5f6b4af74df4a692c5154c10ac24ac7f7a017",
        "content_score": 1.545001164584613,
        "document_identity": "24bc9f2b4745aeeaa399d748f6936a24be41a23e1298b50df1ef756c749774eb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.545001164584613,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 77,
        "address": "tests/agents/__init__.py",
        "content_identity": "7f0aa609323b9af763340572b2e2e3629b621e04f26e7928c6de2efeb5e0a927",
        "content_score": 1.5423276220385347,
        "document_identity": "dbcc4261e93330a1a9c1b7c2289fa29529a5a80aa943346e22eeba2febe906d1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 78,
        "address": "tests/codex/__init__.py",
        "content_identity": "c6569230aa9715ce791dfc758505187aefbe4e40773a8f65a50cd6bb533adda3",
        "content_score": 1.5423276220385347,
        "document_identity": "0184ca54e8decce05659ceb2896e24bc08c7cb835ad8fac9369ba48de48ccc22",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 79,
        "address": "tests/commands/__init__.py",
        "content_identity": "512f63ddf73c412067cb1c8eff784d005d70202fdae5200bd08ee33309fe67d3",
        "content_score": 1.5423276220385347,
        "document_identity": "fc5db2e9c896475f484dfc3e4fcb10c50b604568c04cc45d1a387f0ee5f52426",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 80,
        "address": "tests/context/__init__.py",
        "content_identity": "58623efe5365f3cc950f64e91eba2c7b6cca17cb6716fa89a7e81419a5ef14f3",
        "content_score": 1.5423276220385347,
        "document_identity": "0a8416e0d8602ad70e32746b4e0d49674a90309c5c6612a3b905faaa6ffa26b9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 81,
        "address": "tests/filesystem/__init__.py",
        "content_identity": "4240eddd87df34f3412dede0acb7700e2cae0d0c227a48387a218f58cc5273af",
        "content_score": 1.5423276220385347,
        "document_identity": "e5dad26866b771de0261adbeafafb22f63d54ac577e7ce77e81b514f803ed1f6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 82,
        "address": "tests/filesystem/codecs/__init__.py",
        "content_identity": "70a9ca92be20c4c09ee6bfe45d22e53fe190f7941f433c41120500ac890b7933",
        "content_score": 1.5423276220385347,
        "document_identity": "19dafc4688aaa4ffdc57c98b01f48f0ef4ee15d3106c6bc1a511d8d76681f45c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 83,
        "address": "tests/filesystem/models/__init__.py",
        "content_identity": "76b2736bb28edb7484c63fb8bed213e99b1cb9e50fc3db45c965238bb6e54063",
        "content_score": 1.5423276220385347,
        "document_identity": "4288d717dc1b8775bef3fc4f61486ae3eeab62badb6d2e0b9b1b701a36abf880",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 84,
        "address": "tests/filesystem/models/markdown/__init__.py",
        "content_identity": "6b9f9de506cce6e898f7615d1a9e281049b49a5e38dc9d972448026723e131d0",
        "content_score": 1.5423276220385347,
        "document_identity": "1bc3aca730eadccff14602f69f6b81bf0cae81b58462d1bb3def896c8e0333bd",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 85,
        "address": "tests/regex/__init__.py",
        "content_identity": "42b00e65be97c2eab3e15b11883b4d62713d53628284936c1e267ad57917156a",
        "content_score": 1.5423276220385347,
        "document_identity": "ef9304f7f4211c73ebb499ec15e4c11cfd05d849ad94d1cb1df95b71dda37645",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 86,
        "address": "tests/tools/__init__.py",
        "content_identity": "726ac7b7eaccd4faa8c34c92b0aabf4908155cb121acca9d9f6e1b5a7af37a86",
        "content_score": 1.5423276220385347,
        "document_identity": "924b469a2755d8ee3880e4ce308979ba04cc4def8e1d3e432acc5278f56956e1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5423276220385347,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 87,
        "address": "tests/context/history/__init__.py",
        "content_identity": "fb971876e84280fcf876d920ba63c3489996909491f3619afc47581d73c3bde4",
        "content_score": 1.53966331635562,
        "document_identity": "41d1e8e6a17578e62fa13829976a6c0deadb3c6f95c62eb35ee7aaa066f61d79",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 88,
        "address": "tests/context/message/__init__.py",
        "content_identity": "942554696a222dd1b81578626dd33b9d86b279c32e0d62f50db3b30cae2dc096",
        "content_score": 1.53966331635562,
        "document_identity": "b1f89a2500819e605e279d7c7d2f72dd5d268608b4aa2282e83d07db4b0f5314",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 89,
        "address": "tests/context/session/__init__.py",
        "content_identity": "9f5397d715d29761fc822da1f983e6ff9d40493db453220331f50d124d44e042",
        "content_score": 1.53966331635562,
        "document_identity": "45304e91e8c619995210661c0e5170cb2b7d1e4c5fa4f1fb26a37fb14c60650f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 90,
        "address": "tests/evidence/__init__.py",
        "content_identity": "37136bb17f12fef8583d72a6c90ce621b1205613cbd74c638645c2d0ea59203c",
        "content_score": 1.53966331635562,
        "document_identity": "9ddb18f9bcadaa88323e78510225046753b4374893a26725ec48af0827fa8bc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 91,
        "address": "tests/filesystem/models/csv/__init__.py",
        "content_identity": "35f61202fe77fed04ffe0db8d2b53a6be7d7bbdff668c95fc9f355d5b04a3a43",
        "content_score": 1.53966331635562,
        "document_identity": "d702757cf33bc63320334105f61cdde3e889745b8584086bb6b98462782295f2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 92,
        "address": "tests/model_benchmarks/__init__.py",
        "content_identity": "6f388c3c8108a3c79ced840380f96ed4c835a05f3f05e8426834dae767f07299",
        "content_score": 1.53966331635562,
        "document_identity": "dc19ffd8ef35e841d80a71bb4f0324960cb13ceab0964b2db002848b04ded639",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.53966331635562,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 93,
        "address": "tests/commands/test_errors.py",
        "content_identity": "b186677c924cf5775178e19fa581e3eacb04d1dd8eb7cbe07619a4886036c2a3",
        "content_score": 1.4590111558978973,
        "document_identity": "31c69918a66063ef7a16d84e0907aa4284722518523f49c0d4dc14eae89d4d69",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4590111558978973,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 94,
        "address": "tests/paths/test_errors.py",
        "content_identity": "8dcedeea8e5b73ffb00d0fd86fd7bc3b5adb5c85c7ecd6a3f81bff03d455fb78",
        "content_score": 1.4590111558978973,
        "document_identity": "833573e3a38fe5c3677d314a9e6dacded76fd61f28ff29391d73a781e4c6ff3d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4590111558978973,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 95,
        "address": "tests/system/test_detection.py",
        "content_identity": "6a17065fcb2da9b8f4fc63747133754a21522aca26ac9dc8ee392ad498510fd8",
        "content_score": 1.3950680554613482,
        "document_identity": "fc696d022e9345bde114d1602047963ba32da2c76053c20f86a7d21825e80677",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3950680554613482,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 96,
        "address": "src/devtools/filesystem/models/json/list.py",
        "content_identity": "67fea3963523d9fd7ff04d1caf4a8efdfbd72d25f5121e69fafb8f885a39cf86",
        "content_score": 1.3830068680511194,
        "document_identity": "ebb48cb98ceb1a5c9912f523920a137f07b05d5e5dfa11496331045729f12341",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3830068680511194,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 97,
        "address": "tests/commands/test_events.py",
        "content_identity": "3457f79599e0cab1cc452d0701d5898f247b5d4f6c138a6b13714e4e9940fe99",
        "content_score": 1.3305090866245795,
        "document_identity": "025d474e2fbf754aed924d2daea7994e1ae50cc09029f24771be52af3ff0e60d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3305090866245795,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 98,
        "address": "tests/system/test_models.py",
        "content_identity": "7916fd7aa8da35f04cf9b2d94be20c5626968551fe9c458118344e61d3dff9db",
        "content_score": 1.303271880492082,
        "document_identity": "6c97dbb97b128236d5e250958769db4c9cc3ea868e267a1a4ff49d004bddf054",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.303271880492082,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 99,
        "address": "tests/filesystem/models/markdown/test_heading.py",
        "content_identity": "f63a25546fa7119eff99d43cb0da76ff1b662d0e168b14347189e90fa6841830",
        "content_score": 1.2680425724936342,
        "document_identity": "c4bf8a72558f2d8fd6ba544a0dfbece30dfd6685fee1f42f398ac3c53c778285",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2680425724936342,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 100,
        "address": "tests/persistence/test_sqlite.py",
        "content_identity": "b16e3a85a9841f86d3673aaefa14bd711e2b2d9811e9d6d363d5302fce4ba35f",
        "content_score": 1.2346144896549522,
        "document_identity": "3a38fbaf30c283ab20157a649ea1b236dd5dd785d44e16ba7dd09d7ee910313a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2346144896549522,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 101,
        "address": "tests/regex/test_models.py",
        "content_identity": "29685a4333ff2e0dd9931262d8259fc169a858b18580a68bf8432843c739e89f",
        "content_score": 1.2078957110483468,
        "document_identity": "70684749fa98609cd89e02c62b08a70cff937b0705cb12b18b0e3e423b3c6a95",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2078957110483468,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 102,
        "address": "tests/filesystem/test_resolution.py",
        "content_identity": "8c58508f66200e8dcb2c8e25cdaf065bbbfb8ff6a4db8a0a715bdac184bb43f7",
        "content_score": 1.1997659528459983,
        "document_identity": "025fa87b20bec0792d6d1e28a335c5c90a6bbc44a20fc41b72dd4798a8a2cd01",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1997659528459983,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 103,
        "address": "tests/filesystem/models/markdown/test_section.py",
        "content_identity": "dc55bc8dd8c3d6a23caf880d24ddc4ba8a911c527c08d285a94d201aadf90c93",
        "content_score": 1.1854048629970724,
        "document_identity": "350899f26be009104937cc5287731032c72dea1480d46d4805f08cc5959c628c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1854048629970724,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 104,
        "address": "tests/filesystem/models/markdown/test_file.py",
        "content_identity": "8fc98f16c62bea1176de92cd1a7de44b0df7de27dc48e8da139d9eb8531a2098",
        "content_score": 1.1756418053365654,
        "document_identity": "25044fb52f46e7848adcf473de1678b67c28aac6242ed55507ec71209ee18aba",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1756418053365654,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 105,
        "address": "tests/time/test_timing.py",
        "content_identity": "2bf397f939ecf8489ebb2656259e8ede05f9ca4ae65b65276af39d3a89c04153",
        "content_score": 1.165257709562839,
        "document_identity": "ea2a19b6e69bcd396a65d4f56a356ffe172d6ac3a0633a2fb702636d9ceb895f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.165257709562839,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 106,
        "address": "tests/context/session/test_session_id.py",
        "content_identity": "dbed821724f9b71c759c0d1d791535088b06a0412d41183040c80b031d27ed0d",
        "content_score": 1.1637362577479875,
        "document_identity": "fc0957b9cf3ba56e5424db4c900be14761ce23499db55ff3a0c3178f81391e7d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1637362577479875,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 107,
        "address": "tests/identity/test_models.py",
        "content_identity": "d8d1033d6b85181be44258843d7db8b418af2af16a2a22d231466a211434f599",
        "content_score": 1.1576899746007085,
        "document_identity": "ef760be56e1d73740cb82a2da195197dfcd6a686d33a39a83d65469961b9f2a8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1576899746007085,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 108,
        "address": "tests/runtime/test_runtime.py",
        "content_identity": "9f6915145667b647e610fa86f99d1e32520dcb04f7d1847726c20076cbb4577a",
        "content_score": 1.1560705745858348,
        "document_identity": "0abaa962b16b6803945272f5ca810af1ebeb6ce67924c5a89bccbfc32aef8c2c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1560705745858348,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 109,
        "address": "tests/agents/test_protocols.py",
        "content_identity": "985d90d00ff7fa785cec0e72b7eac5e8090034fe765f8435b1a5f372b7e0807a",
        "content_score": 1.1156651611824173,
        "document_identity": "fbca648a1ee4627ce5769e435417f0c314e481cfd573ca4508db5fd5aa486b0e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1156651611824173,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 110,
        "address": "tests/regex/test_search.py",
        "content_identity": "2f4cba6f6c05c42e1b5ff5b75b4d2f815d2612e65e26d1b9df8b84ec3b639cba",
        "content_score": 1.0978010052849851,
        "document_identity": "8280843dea298acaccf9f4e54f1a8e0774a26b0f0cf9e329acbab69a851365ec",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0978010052849851,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 111,
        "address": "tests/filesystem/codecs/test_markdown.py",
        "content_identity": "31f383749d1c9f95ebe444ab4b03b7e1a3c4fae30358025a0a54dfa84dbb4dc1",
        "content_score": 1.0910815742306086,
        "document_identity": "d5140467d7e1279f4140e9cfac00ffa7712d592ba5fbb355736b281543ee369c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0910815742306086,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 112,
        "address": "tests/filesystem/models/csv/test_row.py",
        "content_identity": "333965a84a43f3b5834e85a5f066e6a64a67d2af27e637945b7f9435015b201f",
        "content_score": 1.0897475467571667,
        "document_identity": "47261c2bbe4e5ebd35b04753068840fa7a9c808c07e9338d0dd61004eec791ab",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0897475467571667,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 113,
        "address": "tests/filesystem/test_models.py",
        "content_identity": "032a347c8c60229e24f8df9f6fa2bb21270574d4992db332ec4aa25316af9125",
        "content_score": 1.0884167774380338,
        "document_identity": "902e4fd98b230d04c8d9bbc57a5a1308da7ad81c239ce390ec0400fcf6ea93e8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0884167774380338,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 114,
        "address": "tests/paths/test_resolved_path.py",
        "content_identity": "11796d07be58818b01aad38f38119c535af0aaa0d6b58834665f0742c7db8cd7",
        "content_score": 1.0714079221855288,
        "document_identity": "ec16116f970e49117b63b84f12b5aa32ba878e66b9a18ea293c1134e5fc18822",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0714079221855288,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 115,
        "address": "tests/evidence/test_protocols.py",
        "content_identity": "c587602672eab6c64447338097a640f5445965d009a743376d24ee541da44e60",
        "content_score": 1.0650067593686388,
        "document_identity": "619658d48813645ecc336c713e3fa3144873173d5412f3e83e4c0a020f74ebbe",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0650067593686388,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 116,
        "address": "tests/codex/test_parsing.py",
        "content_identity": "cbd03645a8d8d958f87c22dd4736bfcea11b87d049ec523f70ed98940770b9be",
        "content_score": 0.9817192859359922,
        "document_identity": "bcee14c62e44f314c11949f78eeebe14234875dd121158631840d625dfc3d48d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9817192859359922,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 117,
        "address": "tests/time/test_parsing.py",
        "content_identity": "626697abc94ac0b5ccf0d6dc9df9c8857af221b6037004ebaf5af259de14c6e7",
        "content_score": 0.9077318040561699,
        "document_identity": "0dd80ef360ebb19ca1b6fa34605e22fcfa19b994271200f293590f30fa719c2a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9077318040561699,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 118,
        "address": "tests/tools/test_command.py",
        "content_identity": "c01229e295c147fed7c4bfd21dd692ab5e5c5c31d2f2b3021a0fb735a1196096",
        "content_score": 0.8878389955942066,
        "document_identity": "a5366355f81d081f3296ff7e14db96aa0d0982e8aacc4fb4c0cedf185a642fdb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.8878389955942066,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 119,
        "address": "tests/tools/test_execution.py",
        "content_identity": "ca795dd35424539b29e091e66f20e67a66c99f9b2902729a49d1f8264555c5c2",
        "content_score": 0.8851936925384243,
        "document_identity": "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.8851936925384243,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 120,
        "address": "tests/filesystem/models/csv/test_file.py",
        "content_identity": "6b1717a0496b803dd345cdbde76c158e8bc538338b15e13fc2500df28870912a",
        "content_score": 0.877351525156694,
        "document_identity": "a78b0b3279f6314e24ac2792f3e52ef2112357af5b30f53d44c9a124bb4e2e98",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.877351525156694,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 121,
        "address": "tests/time/test_models.py",
        "content_identity": "7f6e96f3f34915d9b3add3d039ca9d319b2fdb475439ffa1a018372dbc28e3cb",
        "content_score": 0.8276540886784324,
        "document_identity": "b34e3c77c110106f36ba847bb929cd0ae8e0d4b9ca4d50d5128dfebb8f677587",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.8276540886784324,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 122,
        "address": "tests/persistence/test_json.py",
        "content_identity": "02a3c7266311b81b9dca25a71561c404a8b314c261b4625f1bfd2b49f2cebd2c",
        "content_score": 0.7744373189288581,
        "document_identity": "6dab9a97ea0a5742c1863a66e223dff719d76631ad8af888d20447d676f406d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7744373189288581,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 123,
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "67d786bd55e831ba837083ba29230d5110d5460d58a0c46ed3fad9a5a6cb0d1f",
        "content_score": 0.7684281597841864,
        "document_identity": "607fdb76c3a1a99496e75391fe63f28d9368516dcfc1c9a3cb2ab4a6b2b603cc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7684281597841864,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 124,
        "address": "tests/filesystem/test_json_models.py",
        "content_identity": "2fc65e2331f1049968d7ce696dd05d2e77ddcd3bc76e5601847f56dea3fa77d2",
        "content_score": 0.7306330602285954,
        "document_identity": "9f5a08a5992a28e6efef97b33ae813036b118bc1aaa14f8f13df59638400f546",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7306330602285954,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 125,
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "14fbd64f5aace02b3bcfd9cbeedf0183532182eadd7c3e8af3f57ea71d9bbeb9",
        "content_score": 0.7264644300676014,
        "document_identity": "c9d01508be698d8466bbc4cc584b060ed368f93c38ba3b222b89e4b5ec72389e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7264644300676014,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 126,
        "address": "tests/context/history/test_history.py",
        "content_identity": "85245f2ed3177f5d17fd2239b916561e6441fb2fe8557e67efc2a386cb40e29c",
        "content_score": 0.6899130544668103,
        "document_identity": "6c6befa8951f79da1cced3bef08adbfec30e96c9fae46e23c127f1d348ba8fba",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6899130544668103,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 127,
        "address": "tests/commands/test_execution.py",
        "content_identity": "4be50311fc81376286545eb02fecf0725e24d6620fcd91e192d3b6a75dfd60f6",
        "content_score": 0.528676860229451,
        "document_identity": "fb50df1403ac0cc8b8745bfcb8dc32aae722b13ef44a6fcd1bbff883620e3478",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.528676860229451,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 128,
        "address": "tests/evidence/test_attempt.py",
        "content_identity": "3ba8b648ae2de681fecce151091d24b5c6e7fb28c8620d64961a7a7561d97ccd",
        "content_score": 0.5252497310240196,
        "document_identity": "b162f0507538623e226cda7ac2ea2e2f948c4bccf435f6fe0210215258f99b52",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.5252497310240196,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 129,
        "address": "tests/commands/test_handle.py",
        "content_identity": "f271487d5e9bada3ede3cc752a2259e5299047f69357e52a2c430b5a342e91a9",
        "content_score": 0.5152298526724078,
        "document_identity": "1d14321b52cca27bd47eb9e79a812121a5f74c698ba43a6a9f684f305e6b109c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.5152298526724078,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 130,
        "address": "tests/context/session/test_session.py",
        "content_identity": "3652b64ac4d167f6531b5fc824400cc218bdbdb26378448738ddc57036ec6a72",
        "content_score": 0.4836375605995034,
        "document_identity": "128916442ad2b247e09663beb0a9b533a62db936bc39d0f71427048e2ceda253",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.4836375605995034,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 3,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 10,
        "sources": [
          {
            "a_rank": 3,
            "address": "src/devtools/model_serving/vllm.py",
            "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
            "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0d5b9478577cf933360306c77bd771932d4a8fed681b88a1639fd1a9894ea851",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 306,
                  "start_column_utf8": 18,
                  "start_line": 306
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "7454ca2a362c06adda66001eeb1ad2a695e62cbcfc640a26f462c0d07a57142a",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "c47b5dad90276426081fad8e24f33d740403b50b8d15160ca161fda3d8c17a8b"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "240850255488cdcdd8827fb835fd62219accdafba4811a757d6bc9c342635ce6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 472,
                  "start_column_utf8": 14,
                  "start_line": 472
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "32343a1d95a21ed1309b4b7feed0c58381adf0c3c1aec7862adfb943009dc523",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 46,
                  "end_line": 284,
                  "start_column_utf8": 18,
                  "start_line": 284
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "35a0bb8944e5cff8d28bd3056be0abf2c1ef1148bff60afdbe76dbd05e121ab1",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "11ce40971c9c3108ca4a2c928f6aaf92ef15d3789c5a6bf485b0c609ee6125ff"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3ac5ed56512a7b9f3730c540cf2fa701733321eb5abc16dfdd6f95176f95dc9c",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 31,
                  "end_line": 332,
                  "start_column_utf8": 18,
                  "start_line": 332
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7e0fea29ecb26bbbec28b5f0682bdc5cd1e9c0b29d367ea9be71884a83e20810",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 462,
                  "start_column_utf8": 14,
                  "start_line": 462
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7f23768907e664e11b9cb1026d131a8848a3a5f875eb482aa5856b5375839877",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 35,
                  "end_line": 318,
                  "start_column_utf8": 22,
                  "start_line": 318
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "e5d6777d8247adf4cb22435a1df1f49f5041be0c6cd31a14bb1f9386f3ab2959",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "1999907699407c67ecc2257a03a1dacfd182311bc96e5879014bd7e266691b99"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8c915be8a2834205204b93e970bcf7987f9c45f282daf628fd0b9c13360529d3",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 46,
                  "end_line": 270,
                  "start_column_utf8": 30,
                  "start_line": 270
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "f717011e62f1d193811930a88edf74b837a1f7fc75f4058a09a2774103bfbf80",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "a338753b652b7237e2c3e42b554269472492380461b4c485ef5a8b75fa2112fc"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d12bd11ebffd1b035ddedba616ea02a3447e187d3ef7bc89c3df6f08759713e2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 447,
                  "start_column_utf8": 14,
                  "start_line": 447
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e11e88a912c83b628355c9a8f2d104f7fb15aa6e9dfc96a23a2de67136a3cb78",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 478,
                  "start_column_utf8": 14,
                  "start_line": 478
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "513c8082339915cd036ebc325c2f1c7b9f634b5af94f8e0caf35bcbb924761f2",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "9c418305fc227aff7525744be98e64ef5a675647dcf4bc5ac474429de65d01c3"
              },
              {
                "derivation_identity": "5f22f07ebb7004bb82f60eef06de1c57e2f772942c381c8a9b97522314709361",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ea9fd7099e2b91cc9c98957bc31be322568547ee36d045d1ca6dec9de8bb0b49",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/model_serving/vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 229,
                  "start_column_utf8": 18,
                  "start_line": 229
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/model_serving/errors.py",
                "target_content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
                "target_declaration_identity": "d70b7c42cbd4268057d2349654199ab58659e9046efd764008ce38a01bf0e63d",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "e8a7fb2c033f88a4cde5aee25993f30ac082065274935272d0bb32186741354f"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 4,
          "address": "src/devtools/model_serving/errors.py",
          "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
          "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57"
        }
      },
      {
        "best_supporting_source_rank": 38,
        "distinct_supporting_source_count": 2,
        "native_occurrence_count": 11,
        "sources": [
          {
            "a_rank": 38,
            "address": "tests/conversion/test_conversion.py",
            "content_identity": "bf39df57853b170a57f39b6c0b0599e7939369e2d5605e4bf7924dbeb6166839",
            "document_identity": "2bc94e2db4dee31186a5107e5fd3a767d5a6f183d03acd49c9079755c5499041",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "07b52def09b1f79a25cb746474253d36494d0789efbe67334b76fdea65d889da",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 25,
                  "start_column_utf8": 16,
                  "start_line": 25
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "13ba1be74f437bbde143bcffaebd1e170b19582a7d0afb99c6c1bc00540a104b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 18,
                  "end_line": 35,
                  "start_column_utf8": 11,
                  "start_line": 35
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "233545075c0fdeb036ff5fd01f0f7aba85e4401e90a7a421d3cbb670da8670d2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 65,
                  "start_column_utf8": 8,
                  "start_line": 65
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "468da9cf2b7d1197faacfce38afd589a16b4d4bfb7abcedfceb768b3e1b142b3",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 19,
                  "end_line": 119,
                  "start_column_utf8": 8,
                  "start_line": 119
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "724f76b6a0154f711e37c0306809ca0eb76a82cd1bbc486dc7c2095f2776d1ed",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d215e8100e7c64459ea61689470da2335b3e888bf0b558da34e0b047758d410e"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "474fd7ae7c91e380ccf342da18e4379f77e5bb940d34c091d1122fb8c986a05a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 47,
                  "start_column_utf8": 8,
                  "start_line": 47
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "47e1b399faa36f29f43e6573d4666e3dbd3ca5b5a9eaa3a8960d02e354e26e7f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 19,
                  "end_line": 100,
                  "start_column_utf8": 8,
                  "start_line": 100
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "724f76b6a0154f711e37c0306809ca0eb76a82cd1bbc486dc7c2095f2776d1ed",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d215e8100e7c64459ea61689470da2335b3e888bf0b558da34e0b047758d410e"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "49f0a29ee2e99cfe077727105fe3f1735e1433083d3303bc5e04e4ebaf5e86cb",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 76,
                  "start_column_utf8": 8,
                  "start_line": 76
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "559e0695574b83ea0d6651f03be8e61956d89c49353b9a5c8301bce2058bfa2d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 84,
                  "start_column_utf8": 11,
                  "start_line": 84
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "724f76b6a0154f711e37c0306809ca0eb76a82cd1bbc486dc7c2095f2776d1ed",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d215e8100e7c64459ea61689470da2335b3e888bf0b558da34e0b047758d410e"
              },
              {
                "derivation_identity": "3dd945534a3102fa202970441705749125459a0afc4ec2a560ddaabd557ce931",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7da853967612c50f19ae0f0ff5e0c6c8db9a348f6b10752138715574b2dbde05",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/conversion/test_conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 83,
                  "start_column_utf8": 11,
                  "start_line": 83
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "724f76b6a0154f711e37c0306809ca0eb76a82cd1bbc486dc7c2095f2776d1ed",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d215e8100e7c64459ea61689470da2335b3e888bf0b558da34e0b047758d410e"
              }
            ]
          },
          {
            "a_rank": 41,
            "address": "src/devtools/filesystem/models/csv.py",
            "content_identity": "6f687de872e55eb58981ea47b71b9dc0a493619631f38a47b675a04f6f6c4b0c",
            "document_identity": "9f2f8892cad21f3c7916cf1c7692f4e46dd97c0e0b2a9ce793dc9a96ae799e52",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "8cc30e8e6e1855aec010b82cb6c0b457fd19dee285e9169fdbf28806916ab799",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "2fb34eafcec460be1365e0037562b664d66eb326e71a9ff3ca0f8426469f1548",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/filesystem/models/csv.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 277,
                  "start_column_utf8": 15,
                  "start_line": 277
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "724f76b6a0154f711e37c0306809ca0eb76a82cd1bbc486dc7c2095f2776d1ed",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "d215e8100e7c64459ea61689470da2335b3e888bf0b558da34e0b047758d410e"
              },
              {
                "derivation_identity": "8cc30e8e6e1855aec010b82cb6c0b457fd19dee285e9169fdbf28806916ab799",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3b8271dc7137d5bae21cedf638ca1f535526b3021fdae862884d0adc29680dab",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/filesystem/models/csv.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 166,
                  "start_column_utf8": 15,
                  "start_line": 166
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/conversion.py",
                "target_content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
                "target_declaration_identity": "8226485fe7c44d2e53617ff6397f04b7384cf016ba804b96dc0e430a79718328",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "7ef62b94855da4a82513a5c212b4ef4dd6eba94315da729fcda38e5257d6341c"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 51,
          "address": "src/devtools/conversion/conversion.py",
          "content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
          "document_identity": "635c003c50d44b1b2fb96fddf8d418cd935a97cc778c8237b227af1a39480452"
        }
      },
      {
        "best_supporting_source_rank": 51,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 4,
        "sources": [
          {
            "a_rank": 51,
            "address": "src/devtools/conversion/conversion.py",
            "content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
            "document_identity": "635c003c50d44b1b2fb96fddf8d418cd935a97cc778c8237b227af1a39480452",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "fd32c47ae27cc6555e7cd9964dfc74bde724612dd5106da9114b3fd786f4e3c6",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "c5a399337b82b84fd26fd7177f50ccd32a709295e317b91bfb2b1936a55c4560",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/conversion/conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 26,
                  "start_column_utf8": 11,
                  "start_line": 26
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/errors.py",
                "target_content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
                "target_declaration_identity": "f29d73c17937f9ac438a5eef2e10c76847fb642710d202897fd4393659e20a0e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "51972bc42849a4df76fe3f7a069f1c915c4630bf72ead264195c34b7858a7ecf"
              },
              {
                "derivation_identity": "fd32c47ae27cc6555e7cd9964dfc74bde724612dd5106da9114b3fd786f4e3c6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d9a71650deb1d4a309bcf3318ea560ded9aa1804467f8cb504de2a677fe490c4",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/conversion/conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 33,
                  "end_line": 49,
                  "start_column_utf8": 18,
                  "start_line": 49
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/errors.py",
                "target_content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
                "target_declaration_identity": "f29d73c17937f9ac438a5eef2e10c76847fb642710d202897fd4393659e20a0e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "51972bc42849a4df76fe3f7a069f1c915c4630bf72ead264195c34b7858a7ecf"
              },
              {
                "derivation_identity": "fd32c47ae27cc6555e7cd9964dfc74bde724612dd5106da9114b3fd786f4e3c6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e05eaee5e66811207efba5dda53b4618e2daa7b9fa6f8455dad4aa9f2c32c982",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/conversion/conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 29,
                  "end_line": 29,
                  "start_column_utf8": 14,
                  "start_line": 29
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/errors.py",
                "target_content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
                "target_declaration_identity": "f29d73c17937f9ac438a5eef2e10c76847fb642710d202897fd4393659e20a0e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "51972bc42849a4df76fe3f7a069f1c915c4630bf72ead264195c34b7858a7ecf"
              },
              {
                "derivation_identity": "fd32c47ae27cc6555e7cd9964dfc74bde724612dd5106da9114b3fd786f4e3c6",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "f2d3ece893da4abf2d00fa4d4aff4265d038b8946f8d159a7798838b34979e52",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/conversion/conversion.py",
                "source_range_utf8": {
                  "end_column_utf8": 30,
                  "end_line": 48,
                  "start_column_utf8": 15,
                  "start_line": 48
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/conversion/errors.py",
                "target_content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
                "target_declaration_identity": "f29d73c17937f9ac438a5eef2e10c76847fb642710d202897fd4393659e20a0e",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "51972bc42849a4df76fe3f7a069f1c915c4630bf72ead264195c34b7858a7ecf"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 63,
          "address": "src/devtools/conversion/errors.py",
          "content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
          "document_identity": "357ff96b0096e1a6a07c3fefa44426868762d7183d9973c40623bcaeb5c408fd"
        }
      },
      {
        "best_supporting_source_rank": 35,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 18,
        "sources": [
          {
            "a_rank": 35,
            "address": "tests/filesystem/test_reading.py",
            "content_identity": "b6a106c7dea09881ab91b334943f85bf0075704afe166be64027e4f6b2475d59",
            "document_identity": "d6fc5e8fe9655ef353a712da131ad3390516dd90d2dc4104fd17c294eb474ad2",
            "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
            "supports": [
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "09e9e713b45666ec6ac3e37aae13dd3a3103ca4fa53f4f7d2ddd93ceae1fc022",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 168,
                  "start_column_utf8": 8,
                  "start_line": 168
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0b5d4dae8a1c722819d2143e36acb2c742daa6df3ab004b769c9c603f744407a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 128,
                  "start_column_utf8": 11,
                  "start_line": 128
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "149be7df0571d656d6f914e080feed101b26471e469ef0884bfbf0eb7338c15d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 233,
                  "start_column_utf8": 8,
                  "start_line": 233
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "2f784e233e9189e2bf819d574f127e402b160cbaef46643ba5406ccdc5f321f3",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 47,
                  "start_column_utf8": 11,
                  "start_line": 47
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "335c6b7cc267ccb5bb8a7600cc183875a4013255aef8d2e2f3f223104763d512",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 176,
                  "start_column_utf8": 11,
                  "start_line": 176
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "66fb248fe0d99cee0e9335ccac4885c1ac07d4c49a341c1c051ec0d2ff2faf79",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 89,
                  "start_column_utf8": 11,
                  "start_line": 89
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "6838f5820c66802721211e9bd65770de909b2bdc82419ebc683f679a39b772f1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 142,
                  "start_column_utf8": 11,
                  "start_line": 142
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7dad41e143001d3bccd7c9b3cef16deb148bf09e594d7d617be853bbc2239d23",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 154,
                  "start_column_utf8": 8,
                  "start_line": 154
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7ecf63cf53c46c4a2fcffff1110f4391b83106e14cd7ebe483fbac11e4d21409",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 60,
                  "start_column_utf8": 11,
                  "start_line": 60
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "89cb05d47fe55e6f35b2356ec6250cb1eba526b5f3869e6137553e74a343fe83",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 197,
                  "start_column_utf8": 8,
                  "start_line": 197
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a2442106a2abb6de3b8cd039ffed3225ce78136910d63f7eaa918e01f2c6add1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 165,
                  "start_column_utf8": 8,
                  "start_line": 165
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a3f639c3aadf40be7fd53544a2a3421baa6854a722a3a4fb0270614f3c6db2ba",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 151,
                  "start_column_utf8": 8,
                  "start_line": 151
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ae6b25b8c31b9c07689a08f34f58bc290d7955f5bce1d67a869fde5bbe7fda1a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 224,
                  "start_column_utf8": 8,
                  "start_line": 224
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c4906fd35094983f4726da77113f0cef4e7b0ba04cecb88b25cbcc6316a256bd",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 12,
                  "end_line": 214,
                  "start_column_utf8": 8,
                  "start_line": 214
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cf03da28e495ba56282b078a6bff248e493c221b24f850c6fcde67814a9265a8",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 74,
                  "start_column_utf8": 11,
                  "start_line": 74
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "da596a4fb3630d7d29a4e73a6b333d70e62f56b4921d829de793199ebc361076",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 116,
                  "start_column_utf8": 11,
                  "start_line": 116
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "dc1a7785d3cef0f28f64bb79cfe4c82fa5cd1d9f3a4bb249fed54e5483699694",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 15,
                  "end_line": 102,
                  "start_column_utf8": 11,
                  "start_line": 102
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              },
              {
                "derivation_identity": "ed0a2374c49d95bd23849ffefd2bc5442e7f4f39fd26e2af3ecc3f2c50734250",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "f48144c6e74d5e6b1da9c061f034efdf1849613e27749e7eec41a22b4abf0abe",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/filesystem/test_reading.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 162,
                  "start_column_utf8": 22,
                  "start_line": 162
                },
                "source_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_address": "src/devtools/filesystem/reading.py",
                "target_content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
                "target_declaration_identity": "492f3e665ae725691badd38ea2b293e319bef1a7231e89cb7f3b5ca5822293e9",
                "target_snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028",
                "target_subject_identity": "362c7f7963a0f93c34d8fb86a8e66aebf0848c9d2500fb10ba8ac3c7cd8894e1"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 64,
          "address": "src/devtools/filesystem/reading.py",
          "content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
          "document_identity": "d1dead5ca20598c9246405ae3cf3f7b832014c3a90f062e715bebe2cda006f7b"
        }
      }
    ],
    "counts": {
      "local_pairs": 4,
      "qualifying_occurrences": 43,
      "status": "PASS",
      "support_source_target_pairs": 5,
      "supported_targets": 4
    },
    "frame": {
      "corpus_id": "eb20830bed8817e886f21cae6ceffbb15da7dc1f6ccae8667cf2208a6b659ef6",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "6781f26ecb733009de8b1e8427211f74ed7cd8f36ad8c07fe0e7595af145e028"
    },
    "information_need": "Which existing no-live-service tests and serving documentation constrain validation of a new caller-selected launch control?",
    "local_pairs": [
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 3,
          "address": "src/devtools/model_serving/vllm.py",
          "content_identity": "bed510109590a275f6bf037824ef21f632ed9c4914dc5ed7abf26a68aa3c5086",
          "document_identity": "d475649b902f4c3af066c23c13c7db352144a4dac66d0234d13664477d23d3fa"
        },
        "query": "Q3",
        "target": {
          "a_rank": 4,
          "address": "src/devtools/model_serving/errors.py",
          "content_identity": "5b0ee25fa7867db9df35db7833ff06eddb9c9beccf2d2c32c3644f8c105d9674",
          "document_identity": "1996ccd365aeb74bf6f861371250b659bbcf7a1a5f58f24187230ac1e272bb57"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 50,
          "address": "src/devtools/filesystem/docs/roadmap.md",
          "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
          "document_identity": "5a479701e724b9494b94e51f94b81f7f92736f61dfdc72d0e2e39f5fce9a108d"
        },
        "query": "Q3",
        "target": {
          "a_rank": 51,
          "address": "src/devtools/conversion/conversion.py",
          "content_identity": "ae5365a543335e5d2c4775305071eddc124b7c427ef91aa80bc0a84d294ab105",
          "document_identity": "635c003c50d44b1b2fb96fddf8d418cd935a97cc778c8237b227af1a39480452"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 62,
          "address": "src/devtools/filesystem/models/json/scalar.py",
          "content_identity": "09dc9004664f8298b9291c883978a8f54d66838fbb2dbe29fd31c821ce88c4ef",
          "document_identity": "25174fb2a0b7abb3e3a255ea4340968d4c3bfed2e16d7c1d51b7b3774f994ab5"
        },
        "query": "Q3",
        "target": {
          "a_rank": 63,
          "address": "src/devtools/conversion/errors.py",
          "content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
          "document_identity": "357ff96b0096e1a6a07c3fefa44426868762d7183d9973c40623bcaeb5c408fd"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 63,
          "address": "src/devtools/conversion/errors.py",
          "content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
          "document_identity": "357ff96b0096e1a6a07c3fefa44426868762d7183d9973c40623bcaeb5c408fd"
        },
        "query": "Q3",
        "target": {
          "a_rank": 64,
          "address": "src/devtools/filesystem/reading.py",
          "content_identity": "11233374a76ece39c50b82486cc1d8c660d2e5fd516312b5b88c5e3d0e914688",
          "document_identity": "d1dead5ca20598c9246405ae3cf3f7b832014c3a90f062e715bebe2cda006f7b"
        }
      }
    ],
    "obligation": "O3",
    "query": "vLLM serving configuration launch tests explicit optional settings documentation",
    "query_identity": {
      "task": "case-0019:historical-development-003",
      "value": "Q3"
    },
    "task_identity": "case-0019:historical-development-003",
    "timings": {
      "annotation_construction_ns": 1048800,
      "canonical_a_ns": 12022500,
      "complete_online_equivalent_ns": 49705600,
      "predecessor_pairs_ns": 16800,
      "support_projection_ns": 36617500
    }
  }
]
```

Complete positive native Reference identities are in references.json.gz; all positive and negative native RI state is in ri_native.json.gz and the immutable journal.
