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
  "case": "0017",
  "confirmation_reserve_access": "NO",
  "execution": "case-0017-stage-b-1",
  "frame": {
    "corpus_id": "32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91",
    "python_resource_count": 262,
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 357,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
    "source_head": "71e938d809d794f2f07dd30cb772f1e9bc89c9d3",
    "source_tree": "d6c9398be0bf36e16d6bf57a65f16d5f513eab00"
  },
  "gold_access": "NO",
  "graph_only_admissions": 0,
  "holdout_access": "NO",
  "interpretation_gaps": [],
  "ppr_executions": 0,
  "queries": [
    {
      "a_results": 96,
      "local_pairs": 2,
      "obligation": "O1",
      "qualifying_occurrences": 3,
      "status": "PASS",
      "support_source_target_pairs": 3,
      "supported_targets": 2,
      "timings": {
        "annotation_construction_ns": 887200,
        "canonical_a_ns": 20173900,
        "complete_online_equivalent_ns": 107019100,
        "predecessor_pairs_ns": 44500,
        "support_projection_ns": 85913500
      }
    },
    {
      "a_results": 124,
      "local_pairs": 5,
      "obligation": "O2",
      "qualifying_occurrences": 17,
      "status": "PASS",
      "support_source_target_pairs": 5,
      "supported_targets": 5,
      "timings": {
        "annotation_construction_ns": 1430000,
        "canonical_a_ns": 21624100,
        "complete_online_equivalent_ns": 106710900,
        "predecessor_pairs_ns": 46000,
        "support_projection_ns": 83610800
      }
    },
    {
      "a_results": 184,
      "local_pairs": 6,
      "obligation": "O3",
      "qualifying_occurrences": 64,
      "status": "PASS",
      "support_source_target_pairs": 8,
      "supported_targets": 6,
      "timings": {
        "annotation_construction_ns": 1498100,
        "canonical_a_ns": 18243000,
        "complete_online_equivalent_ns": 112298900,
        "predecessor_pairs_ns": 46600,
        "support_projection_ns": 92511200
      }
    }
  ],
  "rank_modifications": 0,
  "ri": {
    "assessments": 24110,
    "cross_resource_references": 431,
    "direct_cross_resource_pairs": 80,
    "outcomes": {
      "member-unresolved": 151,
      "method-unresolved": 78,
      "module-unresolved": 1493,
      "resolved": 1718,
      "shadowed-binding": 10304,
      "target-not-supported-declaration": 2270,
      "unresolved-binding": 1862,
      "unsupported-expression": 545,
      "unsupported-receiver": 635,
      "unsupported-scope": 5054
    },
    "positive_references": 1718,
    "resources_derived": 262,
    "self_references": 1287
  },
  "rrf_executions": 0,
  "status": "CAPTURED; NO GOLD; NO EFFECTIVENESS INTERPRETATION",
  "task": "Implement repository lexical statistics and inverted index\n"
}
```

## Complete A/support/pair trace

```json
[
  {
    "A": [
      {
        "a_rank": 1,
        "address": "tests/context/retrieval/test_lexical.py",
        "content_identity": "06f9ac5dd16d7b3b08ab5d85d92c13c0d64955affdd54fd1ffb8a16212f100f3",
        "content_score": 23.54642159164605,
        "document_identity": "ebf7ec0c51d025e8f21418b03f1b878e55d0f704549db0076098c4c793108557",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 23.54642159164605,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 2,
        "address": "src/devtools/context/repository/document.py",
        "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
        "content_score": 15.194404723886102,
        "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 16.853604102102437,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 3,
        "address": "src/devtools/context/retrieval/lexical.py",
        "content_identity": "6e0c2c3149119cd12e96474a48ae49e450b819fc259cd6edded2f19254759e48",
        "content_score": 14.338530171849532,
        "document_identity": "92ce6dc605cafcd14eb19f0d56ed33e4600478612f9c3006aafee4fa528a38aa",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 15.997729550065866,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 4,
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "content_score": 15.94150204090881,
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 15.94150204090881,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "docs/documentation_map.md",
        "content_identity": "e178697304c56f75541858dd0f309dc52f5ad93aff0a6c32fe3d0eb1760a6413",
        "content_score": 13.67925606285613,
        "document_identity": "ec041deebfbfa4ea1866753994b9a262dfe7b7e505416a5701857efa6da7a424",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 13.67925606285613,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 6,
        "address": "docs/architecture.md",
        "content_identity": "378a43102e1bb9872b36a605e6b302c257203d5cf4ad6ace767881594f8e7f8f",
        "content_score": 13.234908016052358,
        "document_identity": "b31200033d6232997f8fb19b7348d0a70855d00f2e52c39afbbf8837055a3ab5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 13.234908016052358,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 7,
        "address": "src/devtools/context/repository/__init__.py",
        "content_identity": "cc738de755c71f67cd21ebd290d1865996dd078387a38004d4e6a5106ae18c4b",
        "content_score": 12.367072275968225,
        "document_identity": "505c86754027c5d95f1284e158f3df600544ce793d789b042c30077b50fc2d3b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.367072275968225,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 8,
        "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
        "content_identity": "ac12ffe3463b9ae5fd2ba564d46a776459bccb368b2ae90c371fc282d413647c",
        "content_score": 12.093881140576066,
        "document_identity": "4da6e615f76b9ca55f81240bb8081bec4312dfc35bec512f1d0e055b5be74a7d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.093881140576066,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 9,
        "address": "src/devtools/context/repository/corpus.py",
        "content_identity": "3424ce325df02cd6fdca1e7a3344cb5ddfa6d48c8692777bf17dcff3f4eb0477",
        "content_score": 10.020148538190675,
        "document_identity": "eb0c8651d77d8d754a458293960a87b3df80dc51b64495fbb40268a3b3018d91",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 11.679347916407009,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 10,
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "content_score": 9.624185654983965,
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.624185654983965,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "README.md",
        "content_identity": "f7080e9cb6b51bc1795dbd54719c69e230fd737e47a2bcd0d608d5ba57db92f9",
        "content_score": 8.547383389540903,
        "document_identity": "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.547383389540903,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "src/devtools/context/retrieval/__init__.py",
        "content_identity": "8a8125b76e455ad20ac9e62d1318ec334e37db4e35f5bb8eb1e75b4bbb0b0880",
        "content_score": 7.821502259549529,
        "document_identity": "c09ed2a4f750106f5ae2275378e2d27a4a08de30f59aedcf71e21afad864ac91",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.821502259549529,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 13,
        "address": "src/devtools/context/repository/discovery.py",
        "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
        "content_score": 7.04645758987792,
        "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.04645758987792,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md",
        "content_identity": "21fdf484e58679f9731bacd6cf22f4f2635eb70d137fb0f4eeca8d1e61e4d449",
        "content_score": 6.175146942108586,
        "document_identity": "e19934b8db1cdb0943f6d0d5bfff78e198f27c542775cf03799e9a5e1178aa15",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.175146942108586,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
        "content_identity": "2ef7cb2c2d78413857d8d28bb905eb8454b11492e42432b5b9f049ee43171a25",
        "content_score": 5.607890486980744,
        "document_identity": "1444645c3ae583dbd0f72abaa45a994f411cf090479accaaa9163fd2b621837a",
        "filename_score": 2.226877027420201,
        "filename_weight": 0.25,
        "score": 6.164609743835794,
        "weighted_filename_score": 0.5567192568550503
      },
      {
        "a_rank": 16,
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "content_score": 6.08766285669478,
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.08766285669478,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
        "content_identity": "ed1952604a29a25ec99b4e0715a81b84a2fb3c3372d0ad261098ad33d56331a1",
        "content_score": 6.015665186498911,
        "document_identity": "2624a81a9e4c740f9bb8f966719f1f010e258937e64b8ef6a7c5773fd8082ccc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.015665186498911,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "content_score": 5.945890558290261,
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.945890558290261,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "content_score": 5.561663408604766,
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.561663408604766,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "src/devtools/agents/conversation/docs/overview.md",
        "content_identity": "b83cbdb84ae5d216481d0544256cbc8b4bc520b73e071a5d02bbba13fde39ee9",
        "content_score": 5.511875985059716,
        "document_identity": "22f492bc9ceb8595d4e3081786a24f3803e97aaf6150528e79ed32809b78b394",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.511875985059716,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "pyproject.toml",
        "content_identity": "275a92369ed49b4d8add7193bf2365a36a4e1b2e1989e0078d4a13bce3a3a618",
        "content_score": 5.328577797480207,
        "document_identity": "2b4b7c3f4b36cbdb3f013f86355fabc1bdbce1a06b80b174929ab973be578209",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.328577797480207,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "content_score": 4.9845284870486655,
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.9845284870486655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "tests/resources/filesystem/models/markdown/test_file.py",
        "content_identity": "4baafbfb0b8ed4829bb5ae9d6243ccf0a739f4560187bc3ed64938d4ceb3d5d0",
        "content_score": 4.724561593322172,
        "document_identity": "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.724561593322172,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "docs/roadmap.md",
        "content_identity": "7724e040cf1726b008c84b28c95eb43348d237d757a58a915c1c2d537dfa3126",
        "content_score": 4.540143640993779,
        "document_identity": "3f041421977df777605700709dc99d3a6a0043133e8c62e0d58141e1043c111e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.540143640993779,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "docs/architecture/taxonomy.md",
        "content_identity": "34f64ed49727becc5e0e1fa2132727a632daa84ca4b9ddfebfc8810cd1efcf95",
        "content_score": 3.9983202553336925,
        "document_identity": "2ccee8ac4dd6a7b891a1f6c852419f952ddea45bc3ffa2ec1df4383ae85c8c57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.9983202553336925,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "docs/backlog/overview.md",
        "content_identity": "cf65c04505519020b18c3b67c4f3e3ce1ce867e0d9e0a3d59348cbbb8afd50a0",
        "content_score": 3.9408824171901635,
        "document_identity": "d37d55c3023bec275107bc846340172dfa999440b5c9688c2cbb0ccef6f1bcbf",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.9408824171901635,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "src/devtools/resources/filesystem/models/json/scalar.py",
        "content_identity": "adb1025a200bdce3fb68c5fd4f082ce102b3b5691774b84212d59da3555da6a7",
        "content_score": 3.935464295332302,
        "document_identity": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.935464295332302,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "content_score": 2.9572207803191417,
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "filename_score": 2.488102142027763,
        "filename_weight": 0.25,
        "score": 3.5792463158260825,
        "weighted_filename_score": 0.6220255355069407
      },
      {
        "a_rank": 29,
        "address": "src/devtools/context/repository/identity.py",
        "content_identity": "ce3420ce5eaa9ddf87a9aff64ffaa58c7368efdaea17631d690a91067e100c0b",
        "content_score": 2.9961200776341395,
        "document_identity": "a372e77ec9df55620042af13827c3b4616e934917e6e6bf54f7147959960d51e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9961200776341395,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "content_score": 2.9767919273441765,
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9767919273441765,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "src/devtools/resources/filesystem/models/markdown/section.py",
        "content_identity": "be459c6f8ddc32dacfa1c70451caabced3ea2658ee078e505ef629642e7cce9f",
        "content_score": 2.97135266114393,
        "document_identity": "962c8a8f47be8815e8c55d9baa66b822b4ce837ee58e0a056be0d24d19be8c1d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.97135266114393,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/models/serving/huggingface.py",
        "content_identity": "69f8095b6883dc2d8cdf556d73f9913d89b49e2c0689d6e12f1e496c48415d1c",
        "content_score": 2.910488737617738,
        "document_identity": "4ea5572de8f23b99bc7d8358b0ea8d55741df9fbc2dbcdc324e15401f5b113ea",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.910488737617738,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "src/devtools/context/repository/resource.py",
        "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
        "content_score": 2.9083283551696084,
        "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9083283551696084,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "content_score": 2.871529187605382,
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.871529187605382,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "src/devtools/context/repository/snapshot.py",
        "content_identity": "492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098",
        "content_score": 2.8678747850016078,
        "document_identity": "71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8678747850016078,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "content_score": 2.8324774894266076,
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8324774894266076,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "content_score": 2.8310363405099626,
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8310363405099626,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "src/devtools/core/time/docs/timestamps.md",
        "content_identity": "91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941",
        "content_score": 2.7852614409889727,
        "document_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7852614409889727,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "src/devtools/context/python/source_candidacy.py",
        "content_identity": "577710fa500280cdacaa7e81aee93dfe2a7886b1a511d4fbbb094b4afe66752c",
        "content_score": 2.7842403006980314,
        "document_identity": "806eaec75c4479f6178f294e35da6a9c7d62e03179efa86bc7cb447b4a83bc97",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7842403006980314,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "tests/models/serving/test_huggingface.py",
        "content_identity": "9b7b273b3c1fa39ba2eef3158a8c248e1f8546815441314ffe39c9b9c404acc2",
        "content_score": 2.7667054450382866,
        "document_identity": "27a4f51ffab31c0935030839ae052c762bf0df7b6aec2acd04e0a06ae9a83860",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7667054450382866,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "src/devtools/core/paths/docs/resolution.md",
        "content_identity": "fa40ca033450a10898e69600e81e7e4246280aa9a9eff6ea68da740d6cd932a5",
        "content_score": 2.7642769093298187,
        "document_identity": "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7642769093298187,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "src/devtools/context/__init__.py",
        "content_identity": "42d066e1662a04b548017d991d1053c27c786ad174d12abf3bc8495b887a90ed",
        "content_score": 2.761460691499058,
        "document_identity": "448b87169ac6bd9f81f6818b08d1528e5001cc678fb7e5b12d5ecd1bd7ff28e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.761460691499058,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "content_score": 2.734610911316894,
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.734610911316894,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 44,
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "content_score": 2.6626227193933767,
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6626227193933767,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "src/devtools/context/python/function/request_assembly.py",
        "content_identity": "27bfd8eb7c177577cc410c7e19c47cd8724a6b93200dd15e2ac8d55d4bb4d152",
        "content_score": 2.6358195042841865,
        "document_identity": "d0683bff077bc951cd4f02a215e96323dbb4ed78587cbcddd9a12df9ec0b9c8a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6358195042841865,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "tests/context/python/function/test_cross_resource_pipeline.py",
        "content_identity": "3e1385c11ca543d63d7871103573a38d54df4bce21a197c9d4acb429407e9f86",
        "content_score": 2.6044249517348375,
        "document_identity": "9aad8ade9c30a6bd48667c55317b1143acf7d6d172bf530207e49e8ff9000422",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6044249517348375,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md",
        "content_identity": "6de96cf6eb92c336b7284b291a91b9220ab3147e971b1e7dd6ca9f17a41c68f2",
        "content_score": 2.5764606893431155,
        "document_identity": "242b7e1c2fb6bd3dfc4e748f07647de260c6c5942b6f00d335a5fac4d8692cbb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5764606893431155,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 48,
        "address": "tests/context/python/function/test_candidates.py",
        "content_identity": "71203dab41b8c017cd280d1bfd1097ca3abe63f7be2215c8e8749bf5a5225f0d",
        "content_score": 2.5719255635760585,
        "document_identity": "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5719255635760585,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 49,
        "address": "tests/context/python/function/test_retrieval.py",
        "content_identity": "9f34ccca57fce7274073fe508ea8ce5d98ac799e316097a9cb6501fae8802b35",
        "content_score": 2.5690385144654093,
        "document_identity": "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5690385144654093,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 50,
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "content_score": 2.555634485277421,
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.555634485277421,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 51,
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "content_score": 2.5445873030758626,
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5445873030758626,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 52,
        "address": "src/devtools/resources/filesystem/models/json/object.py",
        "content_identity": "6a5b17b886fdb64baf279da53a8e07a78be8bdc38a590fce40f20979ede87891",
        "content_score": 2.5394678066141645,
        "document_identity": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5394678066141645,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 53,
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "content_score": 2.5384114468796684,
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5384114468796684,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 54,
        "address": "src/devtools/resources/filesystem/models/json/list.py",
        "content_identity": "b855a01565970c7c0cf19e77c796713ed08ddf8905fa1beb37d3cabe85811424",
        "content_score": 2.456578271145467,
        "document_identity": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.456578271145467,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 55,
        "address": "tests/context/python/function/test_disclosure.py",
        "content_identity": "800ae8fb61b7af70b2c3dd0e48eb9147e0a3e93beef98a9e1d269b212e469151",
        "content_score": 2.442266539795311,
        "document_identity": "9258890145639d5d6c171f6571178340198186d7bd4069cd27dbd732aef127b2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.442266539795311,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 56,
        "address": "tests/context/repository/__init__.py",
        "content_identity": "a4ddb695661c9f434550d390ce57e64c963c257b60c158db9fe481753701b0af",
        "content_score": 2.4404760122683578,
        "document_identity": "d31c50ed94c13ec697ed34cc0ab10c5b15dd3c229acf94c6480ff3c43d95b476",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4404760122683578,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 57,
        "address": "tests/context/__init__.py",
        "content_identity": "3572c092e02fdfe637dd358503b0f6d6f987a86cdc480a31e0a24757c4a6b3b7",
        "content_score": 2.4291396212240994,
        "document_identity": "98b79a5da04d34f985f93b0c0a348fdf72891358de0ab46ab780c4fe837a0ea2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4291396212240994,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 58,
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "content_score": 2.409624019891946,
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.409624019891946,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 59,
        "address": "src/devtools/context/python/__init__.py",
        "content_identity": "5095bc20cf5407381fe1e6cbe8688b43107caf9c2c0e0766547a25f2f6c99764",
        "content_score": 2.3775994627078485,
        "document_identity": "4cd01d81d0173449a888d702500048e1aa4083e623d6abe889805ec4c3f1c47a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3775994627078485,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 60,
        "address": "src/devtools/context/python/function/retrieval.py",
        "content_identity": "edbb1905df9fcf9c03fa045772200a719855b3cec38dfd8ecfb486935e91a33a",
        "content_score": 2.352550899420049,
        "document_identity": "caf0f8ce539ececd78345c22cbb4e4cc809cb0e0e3b5948301717a0140d4c945",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.352550899420049,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 61,
        "address": "tests/context/python/function/test_declarations.py",
        "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
        "content_score": 2.34812136313521,
        "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.34812136313521,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 62,
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "content_score": 2.319529363094213,
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.319529363094213,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 63,
        "address": "AGENTS.md",
        "content_identity": "53d82c12ad707fee6bdab62b533c0a2f3c6f574667d7a60ef414e39b364a132b",
        "content_score": 2.31862311871161,
        "document_identity": "0efaaf039ed9cbf9354a3ae3092989c8cd0fccf574808ffc0775c2f431220d05",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.31862311871161,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 64,
        "address": "docs/experiments/qwen38_llama_cpp.md",
        "content_identity": "26c402d7fb85446b66cd0c9b014c30ab35574486483bf206b2b6b8b0f1bc4b98",
        "content_score": 2.2553080925651074,
        "document_identity": "bcbb31820957884ed9da43118412fdedc3dc62dd7313fc728935b79610fe160b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2553080925651074,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 65,
        "address": "src/devtools/core/regex/docs/overview.md",
        "content_identity": "80793fc954738ca10680ea80ae7b5031ef303b295b307fb5f342d1befe290af5",
        "content_score": 2.2494840455573257,
        "document_identity": "8bb76ffc996af5e90360cfe72c9fdfb95ed8bdfd014de7be4ad895ca0c9b9c7f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2494840455573257,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 66,
        "address": "docs/backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md",
        "content_identity": "ab260ebf43cd617cf724e076198adeaa94a0d9c0137e691cfa4c513a4ca5e064",
        "content_score": 2.1703751995143894,
        "document_identity": "fefff3cf3394291276c4e951a4109da4052f8f92051500014209e4347e0b6fe5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.1703751995143894,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 67,
        "address": "docs/backlog/items/B-0045-establish-minimal-model-interaction-core.md",
        "content_identity": "2027d6c33a43aaa8058dda068d9555659c9f4453e4b3ff4f4f1e3ee395ed2417",
        "content_score": 2.132031125550288,
        "document_identity": "3a2db47d25a527b67611d97dfdf357d6e4e74a0b57db5a8b8970df79bbb64a0a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.132031125550288,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 68,
        "address": "docs/backlog/items/B-0011-investigate-durable-execution-evidence.md",
        "content_identity": "16d7c3af19f795f4fb1cfeff45939f511c2c281f33f3f84eff1a7decef7491ca",
        "content_score": 2.1176417292422745,
        "document_identity": "2e3b78b63cc4ce797d67e523c053ada74af64b9bbd7fddd438d23c4b5da74df5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.1176417292422745,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 69,
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "content_score": 2.0935669842550753,
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.0935669842550753,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 70,
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "content_score": 2.078312869131892,
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.078312869131892,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 71,
        "address": "src/devtools/agents/integrations/codex/docs/overview.md",
        "content_identity": "76e1a5aca9a166ad5d55cdd8870ea5d83488edc89b480490b9e713ba2308072d",
        "content_score": 2.0728733088493296,
        "document_identity": "841d0d23237ae94ca6a702b9194b97ead28fe74b4d071bceec5d5e675b12aa56",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.0728733088493296,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 72,
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "content_score": 2.058586964801617,
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.058586964801617,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 73,
        "address": "src/devtools/context/python/function/__init__.py",
        "content_identity": "05822c31d934736d4d5056d1e4a717bc3aff8785f4a39adc86c167262854c2a1",
        "content_score": 2.0378692052181546,
        "document_identity": "fc731cf21e16634df92921ea169184e8b234e4dbd1b5766411d377f1a982e4af",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.0378692052181546,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 74,
        "address": "docs/backlog/epics/B-0003-local-coding-worker-harness.md",
        "content_identity": "3db4afb3931ab9a48f48c099dac1fd18448c5629e58bc1a3f7fcdae746987849",
        "content_score": 1.9913090916585854,
        "document_identity": "2776c3ceb3ec5fdff2a2543ed5eb8124035e23a9ac1f90c5d4fe378ec2b1ff92",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9913090916585854,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 75,
        "address": "docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md",
        "content_identity": "bf7de7678b9254d375920e1629742023568c61ee8b9f53cf3eff47d60c649e79",
        "content_score": 1.961433260209725,
        "document_identity": "2a8a95d5a84187802e45bd2a5c38f5b22dd0054fb08e7d464f43bb708c1bf911",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.961433260209725,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 76,
        "address": "src/devtools/context/python/function/candidates.py",
        "content_identity": "7011e4bec1b143a6ce891a7df1eaf7dde774d299039c98da26ccf09938626350",
        "content_score": 1.961386321882257,
        "document_identity": "b228f50535b7bdf088462cc743375b0b792512fda105b7eb299ebdab936d6022",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.961386321882257,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 77,
        "address": "docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md",
        "content_identity": "7680ca97d41b1bd7a21e3f6a06d07ff12a059aa72521046876eade9dffef021e",
        "content_score": 1.9492479338649997,
        "document_identity": "771790b410aced945c781e757eab8d50f3925e8f14980d59c9d0972c0bd80a95",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9492479338649997,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 78,
        "address": "docs/backlog/metadata.md",
        "content_identity": "e6d3384a4dba6ba54e4c2525ea36eb692b6c8f16fc9a33a458203d68bbe14aeb",
        "content_score": 1.9479914237576847,
        "document_identity": "51a580f32bea1a3d7e5190136f82dcedf721dd3c7ced7ffcf4ab9e39750d7abc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9479914237576847,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 79,
        "address": "src/devtools/context/python/function/materialization.py",
        "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
        "content_score": 1.9431658002330685,
        "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9431658002330685,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 80,
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "content_score": 1.9411468481499712,
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9411468481499712,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 81,
        "address": "src/devtools/context/python/function/declarations.py",
        "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
        "content_score": 1.9311829450543392,
        "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9311829450543392,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 82,
        "address": "tests/scripts/qwen/test_llama_cpp_profile.py",
        "content_identity": "f05049563bff24f129a9c1afb629b31bf5f02c2d100cf05a32a8ebbe9d441db8",
        "content_score": 1.8905239097789093,
        "document_identity": "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8905239097789093,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 83,
        "address": "src/devtools/resources/commands/docs/overview.md",
        "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
        "content_score": 1.795330725005115,
        "document_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.795330725005115,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 84,
        "address": "tests/agents/integrations/codex/test_live.py",
        "content_identity": "b705ab7d34b2b7327ec5e86563123101bb9f293b15260a627905fd8524549e64",
        "content_score": 1.658664251847384,
        "document_identity": "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.658664251847384,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 85,
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "content_score": 1.6464788676091981,
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6464788676091981,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 86,
        "address": "src/devtools/models/benchmarks/models.py",
        "content_identity": "856e9cb0a4355718d4bd7599c1a9ba038f44eacdcfeceda48958facb56b670f5",
        "content_score": 1.4972038146997708,
        "document_identity": "5dc6c417b7eeeb78afe9888232f2cac5198575bded9ab6d985b24af847c65ed3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4972038146997708,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 87,
        "address": "tests/agents/conversation/test_live.py",
        "content_identity": "8d785c1dd2043953ec624b38a3f7875ed56523421666f0cdabdadf3ff468bf20",
        "content_score": 1.484453626012009,
        "document_identity": "bcf1ba96f5651167486aa790e81cc04a5fded625f7b63324a8ad6016a3cb2342",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.484453626012009,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 88,
        "address": "docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md",
        "content_identity": "c76097ba1fd52007aa6fca327340ed3f3ef3e02bd9f26e181ae44d10d7393a82",
        "content_score": 1.4627345079174903,
        "document_identity": "721639eb62c531b6a9bec216690ab6455152585b31198c6c8fbdb44e7dcd652b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4627345079174903,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 89,
        "address": "tests/models/benchmarks/test_models.py",
        "content_identity": "582423270354ce5925f1c493a10062f906204462e976712730d51cde04f9a1df",
        "content_score": 1.395954449904133,
        "document_identity": "76b599267e9da2809aeb635279dbc7ecae6f6267a7ce611993e7d9c3ed0a5be0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.395954449904133,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 90,
        "address": "tests/scripts/qwen/test_patch_proposal_worker_acceptance.py",
        "content_identity": "39d7968ad73e318294da9a5e479e28c23736f2eb3857bcbf761109a9385be5ba",
        "content_score": 1.302625476081914,
        "document_identity": "c045e0ebdd7720591b1f4f9397c76c941cedbb9b0fce5b8d7528abf27130afb5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.302625476081914,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 91,
        "address": "tests/agents/conversation/message/test_message.py",
        "content_identity": "018edd9fec6141cd06971551c60343ee4502df935dd5133ed64396386043c941",
        "content_score": 1.2913872059101812,
        "document_identity": "ab89d2dc88f6dc9e1e6bf3e81bc12957376dabae7a73b86478af84b5f21fb541",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2913872059101812,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 92,
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "content_score": 1.2778906011589097,
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2778906011589097,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 93,
        "address": "src/devtools/agents/integrations/codex/docs/cli.md",
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "content_score": 1.1904542576309878,
        "document_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1904542576309878,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 94,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "2a5ade1094032b7b54c428459a461dcac86a507bd031ac15a2694a53115fe3cf",
        "content_score": 0.7744075489441758,
        "document_identity": "1bf8fedf436a5ce8b8bd046305c8a601e1d91b51927835fcf4ab241570163ee6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7744075489441758,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 95,
        "address": "src/devtools/models/serving/vllm.py",
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "content_score": 0.6027357724833192,
        "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6027357724833192,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 96,
        "address": "tests/models/serving/test_vllm.py",
        "content_identity": "66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8",
        "content_score": 0.30298792797035523,
        "document_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.30298792797035523,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 2,
        "distinct_supporting_source_count": 2,
        "native_occurrence_count": 2,
        "sources": [
          {
            "a_rank": 2,
            "address": "src/devtools/context/repository/document.py",
            "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
            "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "490c22003de02742d52376e99f3eb4536e017826fbd07b7db46918ca2da94e6e",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "91a7675828aa9f14b563a7ed214787b137d728b0187d2c332bb1c993a48a45c2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/context/repository/document.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 26,
                  "start_column_utf8": 8,
                  "start_line": 26
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/context/repository/resource.py",
                "target_content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
                "target_declaration_identity": "fce372e7691bd6934c0d5233f2cd2b0691fccc07277c78d6426d13435941ebe2",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "1835e9e39e8e0e484922c1f434e8b13accafce73c350cde72880d88bc0fb1706"
              }
            ]
          },
          {
            "a_rank": 9,
            "address": "src/devtools/context/repository/corpus.py",
            "content_identity": "3424ce325df02cd6fdca1e7a3344cb5ddfa6d48c8692777bf17dcff3f4eb0477",
            "document_identity": "eb0c8651d77d8d754a458293960a87b3df80dc51b64495fbb40268a3b3018d91",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "99364ae9c49b0fe03ff3a6f7c2e0171e967abc03135835ad98907768c6b5a5f9",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cd77eb64226096a8ed054e880239bd01e3d1e16fb3beef88b0f7d1bd33b29142",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/context/repository/corpus.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 31,
                  "start_column_utf8": 8,
                  "start_line": 31
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/context/repository/resource.py",
                "target_content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
                "target_declaration_identity": "fce372e7691bd6934c0d5233f2cd2b0691fccc07277c78d6426d13435941ebe2",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "1835e9e39e8e0e484922c1f434e8b13accafce73c350cde72880d88bc0fb1706"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 33,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "best_supporting_source_rank": 89,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 89,
            "address": "tests/models/benchmarks/test_models.py",
            "content_identity": "582423270354ce5925f1c493a10062f906204462e976712730d51cde04f9a1df",
            "document_identity": "76b599267e9da2809aeb635279dbc7ecae6f6267a7ce611993e7d9c3ed0a5be0",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "d2b7b71e85d237fa7b42502c6768bbaf8a22f78b0a3d8675b1bacf2a5ce82178",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "9f9ddff04f44c17ad5627faa4a0e79a9bda6176e47391c20f95a2619011b621e",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/benchmarks/test_models.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 154,
                  "start_column_utf8": 13,
                  "start_line": 154
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 95,
          "address": "src/devtools/models/serving/vllm.py",
          "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
          "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
        }
      }
    ],
    "counts": {
      "local_pairs": 2,
      "qualifying_occurrences": 3,
      "status": "PASS",
      "support_source_target_pairs": 3,
      "supported_targets": 2
    },
    "frame": {
      "corpus_id": "32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49"
    },
    "information_need": "Which native observations and collection identities determine document/corpus lexical frequency and length statistics without changing text analysis?",
    "local_pairs": [
      {
        "obligation": "O1",
        "predecessor": {
          "a_rank": 32,
          "address": "src/devtools/models/serving/huggingface.py",
          "content_identity": "69f8095b6883dc2d8cdf556d73f9913d89b49e2c0689d6e12f1e496c48415d1c",
          "document_identity": "4ea5572de8f23b99bc7d8358b0ea8d55741df9fbc2dbcdc324e15401f5b113ea"
        },
        "query": "Q1",
        "target": {
          "a_rank": 33,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "obligation": "O1",
        "predecessor": {
          "a_rank": 94,
          "address": "tests/scripts/test_vllm_benchmark_driver.py",
          "content_identity": "2a5ade1094032b7b54c428459a461dcac86a507bd031ac15a2694a53115fe3cf",
          "document_identity": "1bf8fedf436a5ce8b8bd046305c8a601e1d91b51927835fcf4ab241570163ee6"
        },
        "query": "Q1",
        "target": {
          "a_rank": 95,
          "address": "src/devtools/models/serving/vllm.py",
          "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
          "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
        }
      }
    ],
    "obligation": "O1",
    "query": "repository lexical document corpus term frequency statistics",
    "query_identity": {
      "task": "case-0017:historical-development-001",
      "value": "Q1"
    },
    "task_identity": "case-0017:historical-development-001",
    "timings": {
      "annotation_construction_ns": 887200,
      "canonical_a_ns": 20173900,
      "complete_online_equivalent_ns": 107019100,
      "predecessor_pairs_ns": 44500,
      "support_projection_ns": 85913500
    }
  },
  {
    "A": [
      {
        "a_rank": 1,
        "address": "docs/documentation_map.md",
        "content_identity": "e178697304c56f75541858dd0f309dc52f5ad93aff0a6c32fe3d0eb1760a6413",
        "content_score": 17.224920331532605,
        "document_identity": "ec041deebfbfa4ea1866753994b9a262dfe7b7e505416a5701857efa6da7a424",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 17.224920331532605,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 2,
        "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
        "content_identity": "ac12ffe3463b9ae5fd2ba564d46a776459bccb368b2ae90c371fc282d413647c",
        "content_score": 14.507441316830628,
        "document_identity": "4da6e615f76b9ca55f81240bb8081bec4312dfc35bec512f1d0e055b5be74a7d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 14.507441316830628,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 3,
        "address": "docs/architecture.md",
        "content_identity": "378a43102e1bb9872b36a605e6b302c257203d5cf4ad6ace767881594f8e7f8f",
        "content_score": 14.488556474408123,
        "document_identity": "b31200033d6232997f8fb19b7348d0a70855d00f2e52c39afbbf8837055a3ab5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 14.488556474408123,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 4,
        "address": "tests/context/retrieval/test_lexical.py",
        "content_identity": "06f9ac5dd16d7b3b08ab5d85d92c13c0d64955affdd54fd1ffb8a16212f100f3",
        "content_score": 14.360770873259408,
        "document_identity": "ebf7ec0c51d025e8f21418b03f1b878e55d0f704549db0076098c4c793108557",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 14.360770873259408,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "src/devtools/context/repository/document.py",
        "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
        "content_score": 12.130769172138095,
        "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 13.789968550354429,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 6,
        "address": "src/devtools/context/retrieval/lexical.py",
        "content_identity": "6e0c2c3149119cd12e96474a48ae49e450b819fc259cd6edded2f19254759e48",
        "content_score": 11.973544060619119,
        "document_identity": "92ce6dc605cafcd14eb19f0d56ed33e4600478612f9c3006aafee4fa528a38aa",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 13.632743438835453,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 7,
        "address": "src/devtools/context/repository/discovery.py",
        "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
        "content_score": 12.102670345108104,
        "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 12.102670345108104,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 8,
        "address": "src/devtools/context/repository/resource.py",
        "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
        "content_score": 10.205842451059434,
        "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 11.865041829275768,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 9,
        "address": "docs/roadmap.md",
        "content_identity": "7724e040cf1726b008c84b28c95eb43348d237d757a58a915c1c2d537dfa3126",
        "content_score": 11.566143083867313,
        "document_identity": "3f041421977df777605700709dc99d3a6a0043133e8c62e0d58141e1043c111e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.566143083867313,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 10,
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "content_score": 11.26569265613616,
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.26569265613616,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
        "content_identity": "ed1952604a29a25ec99b4e0715a81b84a2fb3c3372d0ad261098ad33d56331a1",
        "content_score": 11.167345609162378,
        "document_identity": "2624a81a9e4c740f9bb8f966719f1f010e258937e64b8ef6a7c5773fd8082ccc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.167345609162378,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
        "content_identity": "2ef7cb2c2d78413857d8d28bb905eb8454b11492e42432b5b9f049ee43171a25",
        "content_score": 10.580057373962086,
        "document_identity": "1444645c3ae583dbd0f72abaa45a994f411cf090479accaaa9163fd2b621837a",
        "filename_score": 2.075941143214862,
        "filename_weight": 0.25,
        "score": 11.099042659765802,
        "weighted_filename_score": 0.5189852858037155
      },
      {
        "a_rank": 13,
        "address": "src/devtools/context/repository/snapshot.py",
        "content_identity": "492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098",
        "content_score": 11.04300413057334,
        "document_identity": "71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 11.04300413057334,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "src/devtools/context/repository/__init__.py",
        "content_identity": "cc738de755c71f67cd21ebd290d1865996dd078387a38004d4e6a5106ae18c4b",
        "content_score": 9.825326108821645,
        "document_identity": "505c86754027c5d95f1284e158f3df600544ce793d789b042c30077b50fc2d3b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.825326108821645,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "src/devtools/context/repository/corpus.py",
        "content_identity": "3424ce325df02cd6fdca1e7a3344cb5ddfa6d48c8692777bf17dcff3f4eb0477",
        "content_score": 9.19088525720578,
        "document_identity": "eb0c8651d77d8d754a458293960a87b3df80dc51b64495fbb40268a3b3018d91",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.19088525720578,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 16,
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "content_score": 8.688305160055627,
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.688305160055627,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "src/devtools/context/python/function/materialization.py",
        "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
        "content_score": 8.682200394502676,
        "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.682200394502676,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "tests/context/python/function/test_cross_resource_pipeline.py",
        "content_identity": "3e1385c11ca543d63d7871103573a38d54df4bce21a197c9d4acb429407e9f86",
        "content_score": 8.458902695588979,
        "document_identity": "9aad8ade9c30a6bd48667c55317b1143acf7d6d172bf530207e49e8ff9000422",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.458902695588979,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "README.md",
        "content_identity": "f7080e9cb6b51bc1795dbd54719c69e230fd737e47a2bcd0d608d5ba57db92f9",
        "content_score": 7.700707045924532,
        "document_identity": "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.700707045924532,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "src/devtools/agents/conversation/docs/overview.md",
        "content_identity": "b83cbdb84ae5d216481d0544256cbc8b4bc520b73e071a5d02bbba13fde39ee9",
        "content_score": 7.675536265672763,
        "document_identity": "22f492bc9ceb8595d4e3081786a24f3803e97aaf6150528e79ed32809b78b394",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.675536265672763,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "docs/architecture/taxonomy.md",
        "content_identity": "34f64ed49727becc5e0e1fa2132727a632daa84ca4b9ddfebfc8810cd1efcf95",
        "content_score": 7.47524353436904,
        "document_identity": "2ccee8ac4dd6a7b891a1f6c852419f952ddea45bc3ffa2ec1df4383ae85c8c57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.47524353436904,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "content_score": 7.221829076730996,
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.221829076730996,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "src/devtools/resources/filesystem/models/json/list.py",
        "content_identity": "b855a01565970c7c0cf19e77c796713ed08ddf8905fa1beb37d3cabe85811424",
        "content_score": 7.178904792332178,
        "document_identity": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.178904792332178,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "content_score": 7.158142558756826,
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.158142558756826,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "src/devtools/context/python/function/declarations.py",
        "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
        "content_score": 7.1461861157803686,
        "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.1461861157803686,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "tests/context/python/function/test_declarations.py",
        "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
        "content_score": 6.746906761372012,
        "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.746906761372012,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "content_score": 6.340551015965575,
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.340551015965575,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "content_score": 6.203897286004789,
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.203897286004789,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 29,
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "content_score": 5.59051339716991,
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.59051339716991,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "src/devtools/context/retrieval/__init__.py",
        "content_identity": "8a8125b76e455ad20ac9e62d1318ec334e37db4e35f5bb8eb1e75b4bbb0b0880",
        "content_score": 5.454663857965735,
        "document_identity": "c09ed2a4f750106f5ae2275378e2d27a4a08de30f59aedcf71e21afad864ac91",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.454663857965735,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "pyproject.toml",
        "content_identity": "275a92369ed49b4d8add7193bf2365a36a4e1b2e1989e0078d4a13bce3a3a618",
        "content_score": 5.328577797480207,
        "document_identity": "2b4b7c3f4b36cbdb3f013f86355fabc1bdbce1a06b80b174929ab973be578209",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.328577797480207,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/observability/evidence/docs/overview.md",
        "content_identity": "98431aec7bfdfc9c7a4396d6921a5f4174312ccb791b93741b03f8eb0b27c4e7",
        "content_score": 5.1356458511530585,
        "document_identity": "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.1356458511530585,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "content_score": 4.9845284870486655,
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.9845284870486655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "docs/experiments/qwen38_llama_cpp.md",
        "content_identity": "26c402d7fb85446b66cd0c9b014c30ab35574486483bf206b2b6b8b0f1bc4b98",
        "content_score": 4.935188616087553,
        "document_identity": "bcbb31820957884ed9da43118412fdedc3dc62dd7313fc728935b79610fe160b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.935188616087553,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "src/devtools/core/conversion/errors.py",
        "content_identity": "dbac90d1b8454d004d95f4dd61d5cbc43ede986377b483f2a7861b653060ccd9",
        "content_score": 4.893377510716868,
        "document_identity": "6d0b91301e1e3d6d8285b7687305545d2fd078b426f78add3d797f4a18517761",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.893377510716868,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "content_score": 4.77140191655185,
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.77140191655185,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "AGENTS.md",
        "content_identity": "53d82c12ad707fee6bdab62b533c0a2f3c6f574667d7a60ef414e39b364a132b",
        "content_score": 4.766886335072587,
        "document_identity": "0efaaf039ed9cbf9354a3ae3092989c8cd0fccf574808ffc0775c2f431220d05",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.766886335072587,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "content_score": 4.728547475823438,
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.728547475823438,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "tests/resources/filesystem/models/markdown/test_file.py",
        "content_identity": "4baafbfb0b8ed4829bb5ae9d6243ccf0a739f4560187bc3ed64938d4ceb3d5d0",
        "content_score": 4.724561593322172,
        "document_identity": "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.724561593322172,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md",
        "content_identity": "c76097ba1fd52007aa6fca327340ed3f3ef3e02bd9f26e181ae44d10d7393a82",
        "content_score": 4.702557925312029,
        "document_identity": "721639eb62c531b6a9bec216690ab6455152585b31198c6c8fbdb44e7dcd652b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.702557925312029,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "src/devtools/agents/conversation/history.py",
        "content_identity": "25db610d54eeb1bed527bff6839a977374ef218d84e5729743fe063a09a3d1aa",
        "content_score": 4.663226663230031,
        "document_identity": "a8c7c06f5ed02b92e7e6951196b0950141eb053837515ceeb48ab5f37419a7f9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.663226663230031,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "src/devtools/persistence/json.py",
        "content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
        "content_score": 4.661754116910518,
        "document_identity": "054b8b3f80d046b70e54bee873d2bbda22f5c0098c05ce6e19300a789f03c017",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.661754116910518,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "src/devtools/context/repository/identity.py",
        "content_identity": "ce3420ce5eaa9ddf87a9aff64ffaa58c7368efdaea17631d690a91067e100c0b",
        "content_score": 3.1457366210082927,
        "document_identity": "a372e77ec9df55620042af13827c3b4616e934917e6e6bf54f7147959960d51e",
        "filename_score": 5.609715391241007,
        "filename_weight": 0.25,
        "score": 4.548165468818544,
        "weighted_filename_score": 1.4024288478102518
      },
      {
        "a_rank": 44,
        "address": "src/devtools/core/regex/models.py",
        "content_identity": "aeea94f7e37d16c6b755c752cd449f7dfddc91a80bedff98c01c9cd84b9b754d",
        "content_score": 4.531915231533184,
        "document_identity": "b31ced47f8857ac9ee797f5dcf0d4b1afbea9627d761553a7af63a091abaf252",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.531915231533184,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "src/devtools/context/python/function/candidates.py",
        "content_identity": "7011e4bec1b143a6ce891a7df1eaf7dde774d299039c98da26ccf09938626350",
        "content_score": 4.4585212624190556,
        "document_identity": "b228f50535b7bdf088462cc743375b0b792512fda105b7eb299ebdab936d6022",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.4585212624190556,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "src/devtools/core/conversion/conversion.py",
        "content_identity": "0af4ad387dbf34e649b2da8f2245e5272ae7a72592021f3cbb4f85f197e74abf",
        "content_score": 4.411034021464563,
        "document_identity": "b52a38ef3044cfc50d27b17064062c0fe839d9eb170d1c722df6e982c483ca96",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.411034021464563,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "src/devtools/core/conversion/docs/overview.md",
        "content_identity": "7068d7046cc793f13cf7e3ca039b2e5a1cfe7f2cac16e8441776a3b2d54a1c60",
        "content_score": 4.393695284654976,
        "document_identity": "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.393695284654976,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 48,
        "address": "src/devtools/resources/filesystem/models/markdown/file.py",
        "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
        "content_score": 4.281788471792686,
        "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.281788471792686,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 49,
        "address": "src/devtools/core/regex/docs/overview.md",
        "content_identity": "80793fc954738ca10680ea80ae7b5031ef303b295b307fb5f342d1befe290af5",
        "content_score": 4.181839727307118,
        "document_identity": "8bb76ffc996af5e90360cfe72c9fdfb95ed8bdfd014de7be4ad895ca0c9b9c7f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.181839727307118,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 50,
        "address": "src/devtools/resources/filesystem/models/csv.py",
        "content_identity": "0cade3699fe596ba492a6509405496cba9b3e2b616d8c0de6f19b47ca0ba9d40",
        "content_score": 4.095872694630831,
        "document_identity": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.095872694630831,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 51,
        "address": "docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md",
        "content_identity": "21fdf484e58679f9731bacd6cf22f4f2635eb70d137fb0f4eeca8d1e61e4d449",
        "content_score": 4.026804021715892,
        "document_identity": "e19934b8db1cdb0943f6d0d5bfff78e198f27c542775cf03799e9a5e1178aa15",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.026804021715892,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 52,
        "address": "tests/core/conversion/test_conversion.py",
        "content_identity": "2ec54b402be934e923753e7e92554fcc974ea330d3172e74b9aa08f3cd97cd98",
        "content_score": 4.020653886903654,
        "document_identity": "f1a56231ca6a3df1207eb40dd21fc24a4728b5feabb6aab7ec6834ea73d32aec",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.020653886903654,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 53,
        "address": "src/devtools/resources/filesystem/models/json/scalar.py",
        "content_identity": "adb1025a200bdce3fb68c5fd4f082ce102b3b5691774b84212d59da3555da6a7",
        "content_score": 3.935464295332302,
        "document_identity": "8df24eb3014b6f91172fd06d549c30d3a05ca8f9c627543a1907e40094fb3fa9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.935464295332302,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 54,
        "address": "src/devtools/models/serving/identity.py",
        "content_identity": "21687dac15413101d0d68fbb95916f87d25a1ef04f3ea4d7b00a2d0a037c3d8c",
        "content_score": 2.45420614320896,
        "document_identity": "842eb465db068d2292e552261474abb8b38edbed93aab0237b6fe0d2b0a3b102",
        "filename_score": 5.609715391241007,
        "filename_weight": 0.25,
        "score": 3.8566349910192117,
        "weighted_filename_score": 1.4024288478102518
      },
      {
        "a_rank": 55,
        "address": "tests/resources/filesystem/models/csv/test_file.py",
        "content_identity": "85401a1769cd653c8cefa839ab916e069a591a511849264f853bfd4d753db298",
        "content_score": 3.8281831550860907,
        "document_identity": "cedd9f7206edb06702108f33e291fc51299e9d2f3fc794639412b889fc5127c9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.8281831550860907,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 56,
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "content_score": 3.760334784073687,
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.760334784073687,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 57,
        "address": "src/devtools/context/python/function/retrieval.py",
        "content_identity": "edbb1905df9fcf9c03fa045772200a719855b3cec38dfd8ecfb486935e91a33a",
        "content_score": 3.7299458371180854,
        "document_identity": "caf0f8ce539ececd78345c22cbb4e4cc809cb0e0e3b5948301717a0140d4c945",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7299458371180854,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 58,
        "address": "tests/context/python/function/test_candidates.py",
        "content_identity": "71203dab41b8c017cd280d1bfd1097ca3abe63f7be2215c8e8749bf5a5225f0d",
        "content_score": 3.7157433170225156,
        "document_identity": "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7157433170225156,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 59,
        "address": "docs/backlog/overview.md",
        "content_identity": "cf65c04505519020b18c3b67c4f3e3ce1ce867e0d9e0a3d59348cbbb8afd50a0",
        "content_score": 3.6427406238815645,
        "document_identity": "d37d55c3023bec275107bc846340172dfa999440b5c9688c2cbb0ccef6f1bcbf",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.6427406238815645,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 60,
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "content_score": 3.624450334141043,
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.624450334141043,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 61,
        "address": "tests/resources/__init__.py",
        "content_identity": "4d1ff59b18a129f0df9a8ded62185ecb13330f11dde0f1c08620bad2c5eba50e",
        "content_score": 3.612614927667251,
        "document_identity": "63c10870a4738a4da222cc60eba9c7f5e05033631f9af20b5e99972790bc2789",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.612614927667251,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 62,
        "address": "src/devtools/context/python/source_candidacy.py",
        "content_identity": "577710fa500280cdacaa7e81aee93dfe2a7886b1a511d4fbbb094b4afe66752c",
        "content_score": 3.4463172784657545,
        "document_identity": "806eaec75c4479f6178f294e35da6a9c7d62e03179efa86bc7cb447b4a83bc97",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.4463172784657545,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 63,
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "content_score": 3.3099624623680883,
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3099624623680883,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 64,
        "address": "tests/core/identity/test_models.py",
        "content_identity": "0cf0d9523fbbf65faf921bf427eab8c7e824ede3c89b4e50a3eaddbb73d9b66a",
        "content_score": 3.233941768155782,
        "document_identity": "cc10c70082af72eb73a9eeb4ff5bb12db25198b1ffc6c47e79f1e3ed55f034c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.233941768155782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 65,
        "address": "tests/resources/filesystem/test_json_conversion.py",
        "content_identity": "9757259e385ae2a84440d34809686a6dbb7854b2f475bded7f409f81c87278ce",
        "content_score": 3.224906465719998,
        "document_identity": "24c1c20e2050fede03130cb6549cda56dac3e7b786f39434e1c450e4cd81f782",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.224906465719998,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 66,
        "address": "src/devtools/core/identity/docs/overview.md",
        "content_identity": "49232ef5c3a6fca94691bd6dfe84468497d1e17958a349d56dfcd731730cd3b4",
        "content_score": 3.1838303745863668,
        "document_identity": "fe91279815b097915f61055c22b9cb826efac26880e6a831bb43e6ba7fd0f38d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1838303745863668,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 67,
        "address": "src/devtools/core/identity/models.py",
        "content_identity": "e8a65769606ff11f98848952253e5ca7ab542829b992d437636c7aed785868e1",
        "content_score": 3.1707404365960197,
        "document_identity": "a22d87bd3dd2f56dab30b757d6ebb0c0add5cc1baf223c95d70c0b3e88a3c09f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1707404365960197,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 68,
        "address": "src/devtools/agents/conversation/message.py",
        "content_identity": "48bce3f036e3f1aaeb4e340ac78f57cb12f37ee8e90399abcd410ac39e9a4922",
        "content_score": 3.149361113708816,
        "document_identity": "ef792f5457abada1b9d08a53397101b077842dd0cfadd074c72e3007ba6b5286",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.149361113708816,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 69,
        "address": "src/devtools/agents/conversation/conversation.py",
        "content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
        "content_score": 3.0959802764898554,
        "document_identity": "6f120fa0ff94cba2753771027282694420452f884fbccb1c9f1c7b8d1cd64422",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0959802764898554,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 70,
        "address": "src/devtools/observability/evidence/terminal.py",
        "content_identity": "ca45ee1c0c49f49c8c6d30f36c0102ebb53c3d9f65bdaf73cdec032c187673df",
        "content_score": 3.092938265984272,
        "document_identity": "d10cd1728cba9e4d446cfbbed8dee502299450fdfa7a835f90da2e871ef1f0a7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.092938265984272,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 71,
        "address": "src/devtools/core/identity/__init__.py",
        "content_identity": "2932678678a9369d4d55d8e1b33d4e43504c5b5d6d687c91f73c63b4e8c178f4",
        "content_score": 3.080585369798377,
        "document_identity": "ccffe8b555a91babfa3432c2bed312739fbc9a21265661d1d426a8045be13aaa",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.080585369798377,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 72,
        "address": "tests/agents/conversation/test_session_id.py",
        "content_identity": "a84c2db17af8824845875aa28311978a30c75aa83bb488c6586e371b95194860",
        "content_score": 3.0316128546687686,
        "document_identity": "452c09b6282e8b1e51a4fc20b6891801f094caf0f9e96ce83d3653f8afe22446",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0316128546687686,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 73,
        "address": "src/devtools/resources/filesystem/models/markdown/section.py",
        "content_identity": "be459c6f8ddc32dacfa1c70451caabced3ea2658ee078e505ef629642e7cce9f",
        "content_score": 2.97135266114393,
        "document_identity": "962c8a8f47be8815e8c55d9baa66b822b4ce837ee58e0a056be0d24d19be8c1d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.97135266114393,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 74,
        "address": "src/devtools/execution/interaction_attempt.py",
        "content_identity": "0bb14eb1cd824d6833705cde37c4b5b95bf4989fa6ef95c689712b0f303d9dae",
        "content_score": 2.9633273526308597,
        "document_identity": "b115002f32d13800c180e57b5f40ad3dd201ec890d61a45461dc5fdb26450575",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9633273526308597,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 75,
        "address": "src/devtools/models/interaction/observation.py",
        "content_identity": "0d9f1a0763f123c8e6da9fb55ead3e317d1ad82d894c19d3dbe56c3d2b10f2ef",
        "content_score": 2.944667493373023,
        "document_identity": "12423d6c1bf7fdd3e149b6ad0f3683417722abda4a2756f25795303bd490ddff",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.944667493373023,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 76,
        "address": "src/devtools/persistence/sqlite.py",
        "content_identity": "1c7948a64811c6f37f9d7070f612e60f02fc19ac2c2346c0ec66bd37082886d2",
        "content_score": 2.903082624745669,
        "document_identity": "fb9d0eb1271935abc86461bbf5df219f6b9a046df6bd988c4a784499f8908e87",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.903082624745669,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 77,
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "content_score": 2.898653999345453,
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.898653999345453,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 78,
        "address": "tests/resources/filesystem/models/csv/test_row.py",
        "content_identity": "8d63f6babe5f23ccda12074cb4945e18975502f6f4b930ca8182314e16b8e99b",
        "content_score": 2.843151358830758,
        "document_identity": "b6325384827842a4e7782e7ef2acb6673877764a6d41499d6202d107a9a1d10b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.843151358830758,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 79,
        "address": "src/devtools/core/time/docs/timestamps.md",
        "content_identity": "91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941",
        "content_score": 2.7852614409889727,
        "document_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7852614409889727,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 80,
        "address": "tests/models/serving/test_vllm.py",
        "content_identity": "66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8",
        "content_score": 2.780242764069646,
        "document_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.780242764069646,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 81,
        "address": "src/devtools/core/paths/docs/resolution.md",
        "content_identity": "fa40ca033450a10898e69600e81e7e4246280aa9a9eff6ea68da740d6cd932a5",
        "content_score": 2.7642769093298187,
        "document_identity": "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7642769093298187,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 82,
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "content_score": 2.734610911316894,
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.734610911316894,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 83,
        "address": "docs/backlog/items/B-0022-investigate-delegation-acting-authority.md",
        "content_identity": "bd1e1a3f36e6d27289f6dc2f6e9635fabd31267a337bdc577370498b48f75964",
        "content_score": 2.7331149935669385,
        "document_identity": "801e33c2d24b10cd987dd3939af1a80d717798f2dcbd537eb3c61e4a653d838e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7331149935669385,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 84,
        "address": "tests/agents/conversation/history/test_history.py",
        "content_identity": "724c331ef5d9d8098a5138ea8721668f3af7977ca44569970e58220409e96075",
        "content_score": 2.710157246627352,
        "document_identity": "41dd3252be6e0d494afd2975e627749a27efbe11a76931078126369cc964d9b6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.710157246627352,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 85,
        "address": "docs/backlog/items/B-0039-investigate-delegated-authority.md",
        "content_identity": "8193feadd92d47c375fb26107d3d0effe8aa5efcc019ba171d5d3db377d94177",
        "content_score": 2.6992811198192244,
        "document_identity": "e2ba5c38804d23b3f45cbf39eb7c16d9487739007a9dbde75159f0171c3c2840",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6992811198192244,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 86,
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "content_score": 2.691493157485216,
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.691493157485216,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 87,
        "address": "tests/agents/conversation/message/test_message.py",
        "content_identity": "018edd9fec6141cd06971551c60343ee4502df935dd5133ed64396386043c941",
        "content_score": 2.677861463653575,
        "document_identity": "ab89d2dc88f6dc9e1e6bf3e81bc12957376dabae7a73b86478af84b5f21fb541",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.677861463653575,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 88,
        "address": "tests/agents/conversation/test_session.py",
        "content_identity": "65cef479981456b043a3bbbb834a69aa1084381c39a405316f2507e487bf9959",
        "content_score": 2.674409296838273,
        "document_identity": "8b0ff4fa17c0b7be966ab06f563f6f391b4416dd67839dd5363353069f0ab9b7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.674409296838273,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 89,
        "address": "src/devtools/agents/conversation/docs/conversation.md",
        "content_identity": "4e3efd18c04125aa129a58ef15fa0b42935c646788bfa1c5dd3fe9f8724afdc6",
        "content_score": 2.6447151999892196,
        "document_identity": "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.6447151999892196,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 90,
        "address": "tests/core/identity/__init__.py",
        "content_identity": "318fe561871bac625099c7ec765f72d50cde7864749d33f99f94b088425fdb12",
        "content_score": 2.540045978620427,
        "document_identity": "682aca9f60d689c6df8c1d65a492f4c70b67542903096c7e900d20acf0ce72e9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.540045978620427,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 91,
        "address": "src/devtools/resources/filesystem/models/json/object.py",
        "content_identity": "6a5b17b886fdb64baf279da53a8e07a78be8bdc38a590fce40f20979ede87891",
        "content_score": 2.5394678066141645,
        "document_identity": "d00a448e59c6eb64782761170cd202dd96681c014b0eae97ccc71dd66c2e4b14",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5394678066141645,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 92,
        "address": "src/devtools/models/serving/huggingface.py",
        "content_identity": "69f8095b6883dc2d8cdf556d73f9913d89b49e2c0689d6e12f1e496c48415d1c",
        "content_score": 2.51745068439214,
        "document_identity": "4ea5572de8f23b99bc7d8358b0ea8d55741df9fbc2dbcdc324e15401f5b113ea",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.51745068439214,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 93,
        "address": "docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md",
        "content_identity": "6de96cf6eb92c336b7284b291a91b9220ab3147e971b1e7dd6ca9f17a41c68f2",
        "content_score": 2.461510393194421,
        "document_identity": "242b7e1c2fb6bd3dfc4e748f07647de260c6c5942b6f00d335a5fac4d8692cbb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.461510393194421,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 94,
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "content_score": 2.437268018744042,
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.437268018744042,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 95,
        "address": "src/devtools/models/serving/__init__.py",
        "content_identity": "cab99be95d3cf56856b7746cfd8403fd309109fc166d537f2d43934e4138e53a",
        "content_score": 2.423363339132524,
        "document_identity": "a17f72522cdf37b67ba6f2c1b7d19517c9a4b62c4d9b275446c74f21f6604f43",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.423363339132524,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 96,
        "address": "src/devtools/context/python/function/disclosure.py",
        "content_identity": "1e552d51a60cfc13211b111b624e81c9c164fe4da97efbc880719f2919c76a53",
        "content_score": 2.3792252962768643,
        "document_identity": "d43320ad88b11a63a4b24edc28b7770179baaeeb6db1e5a9aa3cf5b82b9be758",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3792252962768643,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 97,
        "address": "tests/context/python/function/test_disclosure.py",
        "content_identity": "800ae8fb61b7af70b2c3dd0e48eb9147e0a3e93beef98a9e1d269b212e469151",
        "content_score": 2.359181823318294,
        "document_identity": "9258890145639d5d6c171f6571178340198186d7bd4069cd27dbd732aef127b2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.359181823318294,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 98,
        "address": "src/devtools/persistence/docs/json.md",
        "content_identity": "85a248d3aba710365dbda906dcf1bd318352c67a726961760e8dd7f14399ccab",
        "content_score": 2.3268196848150176,
        "document_identity": "5cd072b815db6f4b680a2fc2048a1a2aa5f8c08317a14bde9da283d7572ca3ce",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.3268196848150176,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 99,
        "address": "tests/execution/test_interaction_attempt.py",
        "content_identity": "332d1f723e5435ab3c90c1b8ddc9b46391d7c86af571efd512da2a40c8b67aa9",
        "content_score": 2.326162485398452,
        "document_identity": "b1e26cbf79371992c4ff47826e66d9fa6aacda4ba7c49d25bea314f49df3933e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.326162485398452,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 100,
        "address": "docs/backlog/items/B-0032-investigate-execution-retry-mechanics.md",
        "content_identity": "1a118ed2bc983be285228f4e344b05319c9a30c557cd566185335f031df1ad21",
        "content_score": 2.2499882984533075,
        "document_identity": "65fe1c815d135b233b0140e3f642d11becb13015d009fa9676f9f19abf6b5a50",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2499882984533075,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 101,
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "907c737ace884fa0b840921ed3610d712d31693bd82a5e4931641012bcdc3987",
        "content_score": 2.237673666373125,
        "document_identity": "8986afd525a3d67583c80d8f07e5e1883310b3ebc9d6013eed34e30d2640ad46",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.237673666373125,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 102,
        "address": "tests/models/serving/test_llama_cpp.py",
        "content_identity": "2de258ff8b06e27cb3a0642c77839aef7a6511a39b5809a3dad19029b32c13df",
        "content_score": 2.218836764210472,
        "document_identity": "a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.218836764210472,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 103,
        "address": "docs/backlog/items/B-0031-investigate-generic-execution-lifecycle-promotion.md",
        "content_identity": "19766960271a3b2abc942f2819c6f18d9f711f787cf8bc1b9292f41b95f91b57",
        "content_score": 2.1494412790716457,
        "document_identity": "2ac385af72b2a19c39c43d5a5b41ccd319e02ab69b7ce2b948374ddcf1fb22d4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.1494412790716457,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 104,
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "content_score": 2.058586964801617,
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.058586964801617,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 105,
        "address": "src/devtools/execution/docs/overview.md",
        "content_identity": "d635c383c9bb86d0c3781b19256d884dbabe818d37c875c9d104a6e8629e9927",
        "content_score": 2.021883378213573,
        "document_identity": "fc21966cfaddc2a00561ad025f9726a866bf1ef432b49ce8fd565036978bf65a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.021883378213573,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 106,
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "content_score": 1.8576817472828775,
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8576817472828775,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 107,
        "address": "src/devtools/observability/evidence/inspection.py",
        "content_identity": "f41a7ea923b1ae87c804cee8a3863d92b755b3170f39446f72ed3748aa3b1f51",
        "content_score": 1.8419750092695364,
        "document_identity": "3c78bf6a87e7208882daf204034030ffb09654b9463d19be0568776fd5150e4e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8419750092695364,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 108,
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "content_score": 1.8419750092695364,
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8419750092695364,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 109,
        "address": "docs/backlog/items/B-0023-investigate-observability-architecture.md",
        "content_identity": "cc3d2b86e4fc0d8ee3a53740296881d64c171c378d516dccbceddcea2da68568",
        "content_score": 1.7531179719869443,
        "document_identity": "ac12dd4e8719bf1b45652d0b37d43ef1ba41723d3f63fe5aeaeeb93c208504c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.7531179719869443,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 110,
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "content_score": 1.690559515398568,
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.690559515398568,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 111,
        "address": "tests/persistence/test_sqlite.py",
        "content_identity": "1d86b79eeb94ebefca84c2b5ab0453290d211c2d6f1b614548dad6de1ccacbaf",
        "content_score": 1.5884659023654,
        "document_identity": "af689a96779a06c00e60ef58867af10314f90cd641ffd53ab0020e5504c1c5d5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5884659023654,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 112,
        "address": "tests/context/python/function/test_retrieval.py",
        "content_identity": "9f34ccca57fce7274073fe508ea8ce5d98ac799e316097a9cb6501fae8802b35",
        "content_score": 1.4950788502019445,
        "document_identity": "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4950788502019445,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 113,
        "address": "docs/backlog/metadata.md",
        "content_identity": "e6d3384a4dba6ba54e4c2525ea36eb692b6c8f16fc9a33a458203d68bbe14aeb",
        "content_score": 1.459063592864508,
        "document_identity": "51a580f32bea1a3d7e5190136f82dcedf721dd3c7ced7ffcf4ab9e39750d7abc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.459063592864508,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 114,
        "address": "src/devtools/models/interaction/docs/overview.md",
        "content_identity": "0e21114ed3c5afcbd745202deb7cbacc21440d36bb6baf96b21139e5a827b1e7",
        "content_score": 1.3756067645639796,
        "document_identity": "5d92535e7d4cfb0d283a7c6e912005c1363f04d7bc0284519ed82ae36b817fa1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3756067645639796,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 115,
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "82979c703980afb5f5508789155c45bb06adc7a5a7d6a973c74c251b602cde1e",
        "content_score": 1.302216774287795,
        "document_identity": "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.302216774287795,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 116,
        "address": "tests/observability/evidence/test_model_interaction.py",
        "content_identity": "b736d5348b8c5a9aa918cc53c46405399c1506092b79acf8a2102cdc5862a812",
        "content_score": 1.2693477061164897,
        "document_identity": "e6aee6e5d7ba7e7e722752348dbf953bba15033c5a065ef8a9615b28fa40c4f4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2693477061164897,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 117,
        "address": "src/devtools/agents/integrations/codex/docs/cli.md",
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "content_score": 1.2409515214717917,
        "document_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2409515214717917,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 118,
        "address": "tests/models/serving/test_huggingface.py",
        "content_identity": "9b7b273b3c1fa39ba2eef3158a8c248e1f8546815441314ffe39c9b9c404acc2",
        "content_score": 1.1550563956776667,
        "document_identity": "27a4f51ffab31c0935030839ae052c762bf0df7b6aec2acd04e0a06ae9a83860",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1550563956776667,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 119,
        "address": "src/devtools/models/serving/llama_cpp.py",
        "content_identity": "c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e",
        "content_score": 1.1040222213764952,
        "document_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1040222213764952,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 120,
        "address": "src/devtools/observability/evidence/model_interaction.py",
        "content_identity": "6791cab34092a26f1742c01d9ec807f488282fd41ef874538a02dc89a4b65e20",
        "content_score": 1.024131582560143,
        "document_identity": "e6fb5cf02c977455f40daa7b914352529b582d8dc5dbae5e20cff39510707f65",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.024131582560143,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 121,
        "address": "tests/models/interaction/test_models.py",
        "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
        "content_score": 0.9834824979733754,
        "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9834824979733754,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 122,
        "address": "src/devtools/models/serving/vllm.py",
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "content_score": 0.9687146783127355,
        "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9687146783127355,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 123,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "2a5ade1094032b7b54c428459a461dcac86a507bd031ac15a2694a53115fe3cf",
        "content_score": 0.8072567424924979,
        "document_identity": "1bf8fedf436a5ce8b8bd046305c8a601e1d91b51927835fcf4ab241570163ee6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.8072567424924979,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 124,
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "content_score": 0.5750575390626622,
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.5750575390626622,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 5,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 5,
            "address": "src/devtools/context/repository/document.py",
            "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
            "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "490c22003de02742d52376e99f3eb4536e017826fbd07b7db46918ca2da94e6e",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "91a7675828aa9f14b563a7ed214787b137d728b0187d2c332bb1c993a48a45c2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/context/repository/document.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 26,
                  "start_column_utf8": 8,
                  "start_line": 26
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/context/repository/resource.py",
                "target_content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
                "target_declaration_identity": "fce372e7691bd6934c0d5233f2cd2b0691fccc07277c78d6426d13435941ebe2",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "1835e9e39e8e0e484922c1f434e8b13accafce73c350cde72880d88bc0fb1706"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 8,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "best_supporting_source_rank": 23,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 23,
            "address": "src/devtools/resources/filesystem/models/json/list.py",
            "content_identity": "b855a01565970c7c0cf19e77c796713ed08ddf8905fa1beb37d3cabe85811424",
            "document_identity": "feb4be49ba273ee1b7a7cd5209d7bcfd330ea20b6195d04e7d045305df955d4f",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "3f00b614885493f1d3f0724157c2a063bf63f26b85cf4172665902dfe8613590",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "94e3d868467d683466e3eaf13f2b70c928138aadc644700a01fe4297e107eaac",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/resources/filesystem/models/json/list.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 107,
                  "start_column_utf8": 15,
                  "start_line": 107
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/conversion/conversion.py",
                "target_content_identity": "0af4ad387dbf34e649b2da8f2245e5272ae7a72592021f3cbb4f85f197e74abf",
                "target_declaration_identity": "80b259b3e899604a5f91f3f57ff2b1b1ec345f4dc47b32ba309f07b346173271",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "5cf3ac4b5c7eae0fd3318beb2c4440382172c68914cd6db7278151ff20f5da46"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 46,
          "address": "src/devtools/core/conversion/conversion.py",
          "content_identity": "0af4ad387dbf34e649b2da8f2245e5272ae7a72592021f3cbb4f85f197e74abf",
          "document_identity": "b52a38ef3044cfc50d27b17064062c0fe839d9eb170d1c722df6e982c483ca96"
        }
      },
      {
        "best_supporting_source_rank": 42,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 1,
        "sources": [
          {
            "a_rank": 42,
            "address": "src/devtools/persistence/json.py",
            "content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
            "document_identity": "054b8b3f80d046b70e54bee873d2bbda22f5c0098c05ce6e19300a789f03c017",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "3108e0746ab132d07fc8d805f2f34dde4a2efdae1c108c95af94de603269ad44",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "53450be62fd2c7efeeb60b6db7f431efc959e1ef6901ff30ae487d867bf0f171",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/persistence/json.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 140,
                  "start_column_utf8": 13,
                  "start_line": 140
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/agents/conversation/message.py",
                "target_content_identity": "48bce3f036e3f1aaeb4e340ac78f57cb12f37ee8e90399abcd410ac39e9a4922",
                "target_declaration_identity": "ca61b2a124b5df84c2ba517ec215d1cef615096b36688a798b27374af4d8c089",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "8a4dc754f8f9cbf9f9079313d32c907b513e812a529d67e0c93f83d4d0a684a7"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 68,
          "address": "src/devtools/agents/conversation/message.py",
          "content_identity": "48bce3f036e3f1aaeb4e340ac78f57cb12f37ee8e90399abcd410ac39e9a4922",
          "document_identity": "ef792f5457abada1b9d08a53397101b077842dd0cfadd074c72e3007ba6b5286"
        }
      },
      {
        "best_supporting_source_rank": 80,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 12,
        "sources": [
          {
            "a_rank": 80,
            "address": "tests/models/serving/test_vllm.py",
            "content_identity": "66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8",
            "document_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "00b03e987b9e95422f1f4c0db1862656d15647d7e0caa0fcdc2e3426ee6cc54b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 942,
                  "start_column_utf8": 12,
                  "start_line": 942
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "1ad4d4ee48b03e49fd5625e05b1a917e9501b41c2ab061a39d208d56e0507876",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 376,
                  "start_column_utf8": 24,
                  "start_line": 376
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "37abd057db4bee040c252daebef9e0fb1a26c4c9dcdfeee31301ccff92e888d4",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 910,
                  "start_column_utf8": 13,
                  "start_line": 910
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "7c1b47653b9e56274e5f8ce5e672a015665933a0b77ff4344113e539356729ca",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 400,
                  "start_column_utf8": 24,
                  "start_line": 400
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "96b1d70d96e1a512c89eb5f5517b2df443f308432f412300059710c051e313b6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 1141,
                  "start_column_utf8": 13,
                  "start_line": 1141
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": false,
                "fact_identity": "9d1fc8d7537b2c5dcd36f1f435c375a8ab0b03d8954eadac98555167cbddcb2f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 680,
                  "start_column_utf8": 24,
                  "start_line": 680
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c678e1437ab7f4b8aa5e18a14394708ab219d49aa30501c655b2e793dd32a4dd",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 1041,
                  "start_column_utf8": 13,
                  "start_line": 1041
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ca9255faa358de468ec7276f4ef52845f404287197263485907cb54f649a4ff1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 949,
                  "start_column_utf8": 13,
                  "start_line": 949
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cfabb9f6927a1ac1fe26210b1c6161c873225431127292c59a383aaf7c9d9f94",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 594,
                  "start_column_utf8": 13,
                  "start_line": 594
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d83d4993efeb85605512769162bca6b6d9fd5b9655180ed8c45edcc63796ed9b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 128,
                  "start_column_utf8": 13,
                  "start_line": 128
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ea105fd0697d3683f2390a0bcfb66cee4e200d574af884f6ae7a48d1771aa8f9",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 1196,
                  "start_column_utf8": 13,
                  "start_line": 1196
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              },
              {
                "derivation_identity": "9032ca2c8c325ef7ab86ee57047fd4e50f52e58fe13736b838f5ac09494b5ab3",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "f5140cedc42ff29ab5478234c0f79dbf9454ca0b73a7a6c23afd31afc6d33746",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/models/serving/test_vllm.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 997,
                  "start_column_utf8": 13,
                  "start_line": 997
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/serving/vllm.py",
                "target_content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
                "target_declaration_identity": "6c2017050b0510867633c69e77dc88ec5750bdce59710e549ae108a15dfb8084",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "294d5fb2c09be41b9a1073d0bc492aca3da61306cf7fd92a351a7064b9da2ebd"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 122,
          "address": "src/devtools/models/serving/vllm.py",
          "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
          "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
        }
      },
      {
        "best_supporting_source_rank": 116,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 2,
        "sources": [
          {
            "a_rank": 116,
            "address": "tests/observability/evidence/test_model_interaction.py",
            "content_identity": "b736d5348b8c5a9aa918cc53c46405399c1506092b79acf8a2102cdc5862a812",
            "document_identity": "e6aee6e5d7ba7e7e722752348dbf953bba15033c5a065ef8a9615b28fa40c4f4",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "4cc50bf47c027f457fa1392761eddabe4904787a61f0463e6c42b94b002e1cb6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "168cb71a812f53f464f4c2904598e0a2901b1db130325696c7253f3ecd489eeb",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/observability/evidence/test_model_interaction.py",
                "source_range_utf8": {
                  "end_column_utf8": 37,
                  "end_line": 415,
                  "start_column_utf8": 18,
                  "start_line": 415
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/interaction/providers/llama_cpp.py",
                "target_content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
                "target_declaration_identity": "e335d88de35973133f7c9716cfd883eff682b79b9dc3a3ea7dc27aebcc1e8bcf",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "a698b91360dba0a63e30f70f8804e8bd3ad7618ac4328eccfff16dfb6b44229e"
              },
              {
                "derivation_identity": "4cc50bf47c027f457fa1392761eddabe4904787a61f0463e6c42b94b002e1cb6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "5d5a60e9d60c13c7d7ef636da242d8582d8772c3a92a81b4add4ff69bd08b861",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/observability/evidence/test_model_interaction.py",
                "source_range_utf8": {
                  "end_column_utf8": 37,
                  "end_line": 257,
                  "start_column_utf8": 18,
                  "start_line": 257
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/models/interaction/providers/llama_cpp.py",
                "target_content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
                "target_declaration_identity": "e335d88de35973133f7c9716cfd883eff682b79b9dc3a3ea7dc27aebcc1e8bcf",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "a698b91360dba0a63e30f70f8804e8bd3ad7618ac4328eccfff16dfb6b44229e"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 124,
          "address": "src/devtools/models/interaction/providers/llama_cpp.py",
          "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
          "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
        }
      }
    ],
    "counts": {
      "local_pairs": 5,
      "qualifying_occurrences": 17,
      "status": "PASS",
      "support_source_target_pairs": 5,
      "supported_targets": 5
    },
    "frame": {
      "corpus_id": "32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49"
    },
    "information_need": "How should normalized terms index the exact retained documents and their frequency evidence while preserving native repository provenance?",
    "local_pairs": [
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 7,
          "address": "src/devtools/context/repository/discovery.py",
          "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
          "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89"
        },
        "query": "Q2",
        "target": {
          "a_rank": 8,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 45,
          "address": "src/devtools/context/python/function/candidates.py",
          "content_identity": "7011e4bec1b143a6ce891a7df1eaf7dde774d299039c98da26ccf09938626350",
          "document_identity": "b228f50535b7bdf088462cc743375b0b792512fda105b7eb299ebdab936d6022"
        },
        "query": "Q2",
        "target": {
          "a_rank": 46,
          "address": "src/devtools/core/conversion/conversion.py",
          "content_identity": "0af4ad387dbf34e649b2da8f2245e5272ae7a72592021f3cbb4f85f197e74abf",
          "document_identity": "b52a38ef3044cfc50d27b17064062c0fe839d9eb170d1c722df6e982c483ca96"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 67,
          "address": "src/devtools/core/identity/models.py",
          "content_identity": "e8a65769606ff11f98848952253e5ca7ab542829b992d437636c7aed785868e1",
          "document_identity": "a22d87bd3dd2f56dab30b757d6ebb0c0add5cc1baf223c95d70c0b3e88a3c09f"
        },
        "query": "Q2",
        "target": {
          "a_rank": 68,
          "address": "src/devtools/agents/conversation/message.py",
          "content_identity": "48bce3f036e3f1aaeb4e340ac78f57cb12f37ee8e90399abcd410ac39e9a4922",
          "document_identity": "ef792f5457abada1b9d08a53397101b077842dd0cfadd074c72e3007ba6b5286"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 121,
          "address": "tests/models/interaction/test_models.py",
          "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
          "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a"
        },
        "query": "Q2",
        "target": {
          "a_rank": 122,
          "address": "src/devtools/models/serving/vllm.py",
          "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
          "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
        }
      },
      {
        "obligation": "O2",
        "predecessor": {
          "a_rank": 123,
          "address": "tests/scripts/test_vllm_benchmark_driver.py",
          "content_identity": "2a5ade1094032b7b54c428459a461dcac86a507bd031ac15a2694a53115fe3cf",
          "document_identity": "1bf8fedf436a5ce8b8bd046305c8a601e1d91b51927835fcf4ab241570163ee6"
        },
        "query": "Q2",
        "target": {
          "a_rank": 124,
          "address": "src/devtools/models/interaction/providers/llama_cpp.py",
          "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
          "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
        }
      }
    ],
    "obligation": "O2",
    "query": "lexical inverted index term postings document occurrences resource identity",
    "query_identity": {
      "task": "case-0017:historical-development-001",
      "value": "Q2"
    },
    "task_identity": "case-0017:historical-development-001",
    "timings": {
      "annotation_construction_ns": 1430000,
      "canonical_a_ns": 21624100,
      "complete_online_equivalent_ns": 106710900,
      "predecessor_pairs_ns": 46000,
      "support_projection_ns": 83610800
    }
  },
  {
    "A": [
      {
        "a_rank": 1,
        "address": "src/devtools/context/retrieval/lexical.py",
        "content_identity": "6e0c2c3149119cd12e96474a48ae49e450b819fc259cd6edded2f19254759e48",
        "content_score": 37.627700339413366,
        "document_identity": "92ce6dc605cafcd14eb19f0d56ed33e4600478612f9c3006aafee4fa528a38aa",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 39.2868997176297,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 2,
        "address": "tests/context/retrieval/test_lexical.py",
        "content_identity": "06f9ac5dd16d7b3b08ab5d85d92c13c0d64955affdd54fd1ffb8a16212f100f3",
        "content_score": 25.31313930051842,
        "document_identity": "ebf7ec0c51d025e8f21418b03f1b878e55d0f704549db0076098c4c793108557",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 25.31313930051842,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 3,
        "address": "docs/architecture.md",
        "content_identity": "378a43102e1bb9872b36a605e6b302c257203d5cf4ad6ace767881594f8e7f8f",
        "content_score": 18.00781868040966,
        "document_identity": "b31200033d6232997f8fb19b7348d0a70855d00f2e52c39afbbf8837055a3ab5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 18.00781868040966,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 4,
        "address": "docs/backlog/epics/B-0002-coding-context-substrate.md",
        "content_identity": "ac12ffe3463b9ae5fd2ba564d46a776459bccb368b2ae90c371fc282d413647c",
        "content_score": 16.02000150263157,
        "document_identity": "4da6e615f76b9ca55f81240bb8081bec4312dfc35bec512f1d0e055b5be74a7d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 16.02000150263157,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 5,
        "address": "docs/documentation_map.md",
        "content_identity": "e178697304c56f75541858dd0f309dc52f5ad93aff0a6c32fe3d0eb1760a6413",
        "content_score": 15.25528769080765,
        "document_identity": "ec041deebfbfa4ea1866753994b9a262dfe7b7e505416a5701857efa6da7a424",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 15.25528769080765,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 6,
        "address": "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
        "content_identity": "ed1952604a29a25ec99b4e0715a81b84a2fb3c3372d0ad261098ad33d56331a1",
        "content_score": 13.320454248096368,
        "document_identity": "2624a81a9e4c740f9bb8f966719f1f010e258937e64b8ef6a7c5773fd8082ccc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 13.320454248096368,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 7,
        "address": "src/devtools/context/repository/corpus.py",
        "content_identity": "3424ce325df02cd6fdca1e7a3344cb5ddfa6d48c8692777bf17dcff3f4eb0477",
        "content_score": 8.891026603777068,
        "document_identity": "eb0c8651d77d8d754a458293960a87b3df80dc51b64495fbb40268a3b3018d91",
        "filename_score": 6.636797512865336,
        "filename_weight": 0.25,
        "score": 10.550225981993401,
        "weighted_filename_score": 1.659199378216334
      },
      {
        "a_rank": 8,
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "content_score": 10.512652041248513,
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.512652041248513,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 9,
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "content_score": 10.399602047870935,
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.399602047870935,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 10,
        "address": "src/devtools/context/repository/document.py",
        "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
        "content_score": 10.324309687197985,
        "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 10.324309687197985,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 11,
        "address": "src/devtools/context/python/function/candidates.py",
        "content_identity": "7011e4bec1b143a6ce891a7df1eaf7dde774d299039c98da26ccf09938626350",
        "content_score": 9.671647311280756,
        "document_identity": "b228f50535b7bdf088462cc743375b0b792512fda105b7eb299ebdab936d6022",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.671647311280756,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 12,
        "address": "tests/context/python/function/test_retrieval.py",
        "content_identity": "9f34ccca57fce7274073fe508ea8ce5d98ac799e316097a9cb6501fae8802b35",
        "content_score": 9.41659699251592,
        "document_identity": "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 9.41659699251592,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 13,
        "address": "tests/agents/conversation/history/test_history.py",
        "content_identity": "724c331ef5d9d8098a5138ea8721668f3af7977ca44569970e58220409e96075",
        "content_score": 8.421116864157382,
        "document_identity": "41dd3252be6e0d494afd2975e627749a27efbe11a76931078126369cc964d9b6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.421116864157382,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 14,
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "content_score": 8.216036033217017,
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.216036033217017,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 15,
        "address": "tests/core/time/test_parsing.py",
        "content_identity": "de9b7a2ba6d7c57112f2c0f82fb58165ee5b774ef6020051d927d9200a88cf63",
        "content_score": 8.099185104321114,
        "document_identity": "a3f3c90ae6548f028f6f50e5cdc1c3465b0fca7ca52c20064252a5a9027f48b7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 8.099185104321114,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 16,
        "address": "src/devtools/context/python/function/declarations.py",
        "content_identity": "2521087e439f635cd05993cfcbb282fcbaef4f2ddfd569e6c6fee277f1e25a66",
        "content_score": 7.9987110267170465,
        "document_identity": "038c1f33e0939a8fd7e1aeb0def4d3a390ef1fac1abea96bf001e0f4b2786baa",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.9987110267170465,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 17,
        "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
        "content_identity": "2ef7cb2c2d78413857d8d28bb905eb8454b11492e42432b5b9f049ee43171a25",
        "content_score": 7.950365408127455,
        "document_identity": "1444645c3ae583dbd0f72abaa45a994f411cf090479accaaa9163fd2b621837a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.950365408127455,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 18,
        "address": "tests/resources/filesystem/models/markdown/test_section.py",
        "content_identity": "4aabb3f8affeefe4cc1cc66e2a363d8a7f6aa356ecc0babc88702742717dcd97",
        "content_score": 7.725234907345661,
        "document_identity": "3c0b47ef625369f4e8f0c26af7c723ed43a05ba5f0a9c6f980a7a4b862ba284e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.725234907345661,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 19,
        "address": "tests/persistence/test_json.py",
        "content_identity": "e4aac80c8b2fbb70694dbb3cd678ecc9d2a996bcd71836c557d6745539b72d7f",
        "content_score": 7.677835645239717,
        "document_identity": "5b391d5c240d0a95ac12883e5a31bea0ed5fdeac3b6d49f5d1b944b6cc5065fc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.677835645239717,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 20,
        "address": "docs/architecture/taxonomy.md",
        "content_identity": "34f64ed49727becc5e0e1fa2132727a632daa84ca4b9ddfebfc8810cd1efcf95",
        "content_score": 7.558850827596463,
        "document_identity": "2ccee8ac4dd6a7b891a1f6c852419f952ddea45bc3ffa2ec1df4383ae85c8c57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.558850827596463,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 21,
        "address": "docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md",
        "content_identity": "21fdf484e58679f9731bacd6cf22f4f2635eb70d137fb0f4eeca8d1e61e4d449",
        "content_score": 7.479132907794856,
        "document_identity": "e19934b8db1cdb0943f6d0d5bfff78e198f27c542775cf03799e9a5e1178aa15",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.479132907794856,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 22,
        "address": "tests/context/python/function/test_candidates.py",
        "content_identity": "71203dab41b8c017cd280d1bfd1097ca3abe63f7be2215c8e8749bf5a5225f0d",
        "content_score": 7.368219845507463,
        "document_identity": "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.368219845507463,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 23,
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "content_score": 7.178626073305818,
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 7.178626073305818,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 24,
        "address": "src/devtools/core/conversion/docs/overview.md",
        "content_identity": "7068d7046cc793f13cf7e3ca039b2e5a1cfe7f2cac16e8441776a3b2d54a1c60",
        "content_score": 6.98383212951733,
        "document_identity": "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.98383212951733,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 25,
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "content_score": 6.758931924497233,
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.758931924497233,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 26,
        "address": "src/devtools/agents/integrations/codex/docs/cli.md",
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "content_score": 6.533568690517957,
        "document_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.533568690517957,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 27,
        "address": "src/devtools/resources/filesystem/models/markdown/file.py",
        "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
        "content_score": 6.515160428653999,
        "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.515160428653999,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 28,
        "address": "tests/context/python/function/test_disclosure.py",
        "content_identity": "800ae8fb61b7af70b2c3dd0e48eb9147e0a3e93beef98a9e1d269b212e469151",
        "content_score": 6.506595565755294,
        "document_identity": "9258890145639d5d6c171f6571178340198186d7bd4069cd27dbd732aef127b2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.506595565755294,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 29,
        "address": "src/devtools/models/serving/huggingface.py",
        "content_identity": "69f8095b6883dc2d8cdf556d73f9913d89b49e2c0689d6e12f1e496c48415d1c",
        "content_score": 6.40908127991404,
        "document_identity": "4ea5572de8f23b99bc7d8358b0ea8d55741df9fbc2dbcdc324e15401f5b113ea",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.40908127991404,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 30,
        "address": "tests/resources/filesystem/models/csv/test_file.py",
        "content_identity": "85401a1769cd653c8cefa839ab916e069a591a511849264f853bfd4d753db298",
        "content_score": 6.3320086875550885,
        "document_identity": "cedd9f7206edb06702108f33e291fc51299e9d2f3fc794639412b889fc5127c9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.3320086875550885,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 31,
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "content_score": 6.1798208259624685,
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.1798208259624685,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 32,
        "address": "src/devtools/resources/commands/models/command.py",
        "content_identity": "b35fc0c06f23ba27f318af7f62f9dd0f84ed6d0d3a77a97a6eadb9c338579473",
        "content_score": 6.1301788485530935,
        "document_identity": "1452b630a0c46e5efbb2cbd52d062d3ec9e3e71ad0aed65e32611e513168f629",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.1301788485530935,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 33,
        "address": "src/devtools/models/serving/llama_cpp.py",
        "content_identity": "c2da6456aebb93647f46b839f6fcc25cbe1b07696f9a4d0a2c44da96f70d620e",
        "content_score": 6.00565919759913,
        "document_identity": "cdaa18fe818efcf1753214239699267eab03af999d01301c29678b49158bbd1c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 6.00565919759913,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 34,
        "address": "src/devtools/context/retrieval/__init__.py",
        "content_identity": "8a8125b76e455ad20ac9e62d1318ec334e37db4e35f5bb8eb1e75b4bbb0b0880",
        "content_score": 5.454663857965735,
        "document_identity": "c09ed2a4f750106f5ae2275378e2d27a4a08de30f59aedcf71e21afad864ac91",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.454663857965735,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 35,
        "address": "tests/observability/evidence/test_inspection.py",
        "content_identity": "0defcec8dd2a18f934899e1ffe4d4789bb7ddb0f0f3d7d24f87c4ebb0ef5939a",
        "content_score": 5.410771122978666,
        "document_identity": "e66ecd41aa7eb66dfdc669c848fdd1f2c02d14f1df2a5f61ca0f4b81cbd6f66d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.410771122978666,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 36,
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "82979c703980afb5f5508789155c45bb06adc7a5a7d6a973c74c251b602cde1e",
        "content_score": 5.3878700626881395,
        "document_identity": "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.3878700626881395,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 37,
        "address": "src/devtools/context/python/function/retrieval.py",
        "content_identity": "edbb1905df9fcf9c03fa045772200a719855b3cec38dfd8ecfb486935e91a33a",
        "content_score": 5.366491587915003,
        "document_identity": "caf0f8ce539ececd78345c22cbb4e4cc809cb0e0e3b5948301717a0140d4c945",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.366491587915003,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 38,
        "address": "src/devtools/context/repository/__init__.py",
        "content_identity": "cc738de755c71f67cd21ebd290d1865996dd078387a38004d4e6a5106ae18c4b",
        "content_score": 5.322702207717357,
        "document_identity": "505c86754027c5d95f1284e158f3df600544ce793d789b042c30077b50fc2d3b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.322702207717357,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 39,
        "address": "tests/persistence/test_sqlite.py",
        "content_identity": "1d86b79eeb94ebefca84c2b5ab0453290d211c2d6f1b614548dad6de1ccacbaf",
        "content_score": 5.2855303935157965,
        "document_identity": "af689a96779a06c00e60ef58867af10314f90cd641ffd53ab0020e5504c1c5d5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.2855303935157965,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 40,
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "content_score": 5.246009577745148,
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.246009577745148,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 41,
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "content_score": 5.005239998529367,
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 5.005239998529367,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 42,
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "content_score": 4.96792579341059,
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.96792579341059,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 43,
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "content_score": 4.939197822748796,
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.939197822748796,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 44,
        "address": "docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md",
        "content_identity": "6f1b241a03cf8d8f3870ecbdce3e4295ec7702b51241d9af58e3d260e46cd6fc",
        "content_score": 4.828522981000128,
        "document_identity": "c9f47259ec704fe0351f8a21fc3d7dfdebf9bbb81e1ec7d2452d28e987df06df",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.828522981000128,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 45,
        "address": "tests/execution/test_interaction_attempt.py",
        "content_identity": "332d1f723e5435ab3c90c1b8ddc9b46391d7c86af571efd512da2a40c8b67aa9",
        "content_score": 4.695019075007923,
        "document_identity": "b1e26cbf79371992c4ff47826e66d9fa6aacda4ba7c49d25bea314f49df3933e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.695019075007923,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 46,
        "address": "docs/roadmap.md",
        "content_identity": "7724e040cf1726b008c84b28c95eb43348d237d757a58a915c1c2d537dfa3126",
        "content_score": 4.654589231066936,
        "document_identity": "3f041421977df777605700709dc99d3a6a0043133e8c62e0d58141e1043c111e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.654589231066936,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 47,
        "address": "tests/core/regex/test_models.py",
        "content_identity": "78ba9f42850dea03e85d0d70567cae40a4fdadd6af0c59d3aee9332f61111a8f",
        "content_score": 4.612996630241846,
        "document_identity": "70b367728db04a541a76e6fb70113654248a7aeb20f2e96d024b1f65df138747",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.612996630241846,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 48,
        "address": "src/devtools/resources/filesystem/docs/csv.md",
        "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
        "content_score": 4.438037681673386,
        "document_identity": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.438037681673386,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 49,
        "address": "src/devtools/models/serving/vllm.py",
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "content_score": 4.424374613435503,
        "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.424374613435503,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 50,
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "content_score": 4.412136998875833,
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.412136998875833,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 51,
        "address": "docs/backlog/items/B-0023-investigate-observability-architecture.md",
        "content_identity": "cc3d2b86e4fc0d8ee3a53740296881d64c171c378d516dccbceddcea2da68568",
        "content_score": 4.3331405185274035,
        "document_identity": "ac12dd4e8719bf1b45652d0b37d43ef1ba41723d3f63fe5aeaeeb93c208504c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.3331405185274035,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 52,
        "address": "src/devtools/context/python/function/materialization.py",
        "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
        "content_score": 4.274889387109837,
        "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.274889387109837,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 53,
        "address": "src/devtools/context/repository/discovery.py",
        "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
        "content_score": 4.254307742119706,
        "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.254307742119706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 54,
        "address": "tests/resources/commands/test_handle.py",
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "content_score": 4.174531167965468,
        "document_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.174531167965468,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 55,
        "address": "tests/context/python/function/test_cross_resource_pipeline.py",
        "content_identity": "3e1385c11ca543d63d7871103573a38d54df4bce21a197c9d4acb429407e9f86",
        "content_score": 4.101909249854129,
        "document_identity": "9aad8ade9c30a6bd48667c55317b1143acf7d6d172bf530207e49e8ff9000422",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.101909249854129,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 56,
        "address": "docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md",
        "content_identity": "6de96cf6eb92c336b7284b291a91b9220ab3147e971b1e7dd6ca9f17a41c68f2",
        "content_score": 4.070760157364726,
        "document_identity": "242b7e1c2fb6bd3dfc4e748f07647de260c6c5942b6f00d335a5fac4d8692cbb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.070760157364726,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 57,
        "address": "tests/resources/filesystem/models/csv/test_dialect.py",
        "content_identity": "b11253de0b821b7840e1164edcaa3e7055385e418694cbb5671ef6578d8cc5a7",
        "content_score": 4.068924218139802,
        "document_identity": "4238e58b6fd3e76842d6a46cbf656c76fc624a80d908d2ccc1ff67b1a1aba90d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.068924218139802,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 58,
        "address": "tests/models/benchmarks/test_runner.py",
        "content_identity": "14ee7d72d179a7b5ce3dfdc722944833986a2f16abb549d48dc92906f3e2ceb8",
        "content_score": 4.023756614436428,
        "document_identity": "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.023756614436428,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 59,
        "address": "tests/core/paths/test_resolution.py",
        "content_identity": "5f34ec0ac3a2580a7a75533d98c503e65084bf00f49f9d736b8c11f0b3ecbeb2",
        "content_score": 4.011643230654025,
        "document_identity": "3339ce5906f32477be6a3261caf7eb2c73fa7186b78ed2be80d23a9dde3fd90f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 4.011643230654025,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 60,
        "address": "tests/resources/commands/test_models.py",
        "content_identity": "c12ab32a475a94769120d17d1fedf7b497d8f961e080b29b5274dacf01808f28",
        "content_score": 3.9625860079107853,
        "document_identity": "914f8cb6fb367a70eb3a344e2032277d253f3d5d173cccd1a7c87bc3df82a3d4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.9625860079107853,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 61,
        "address": "src/devtools/agents/conversation/docs/history.md",
        "content_identity": "8f13b37857d1ba351e1cb5ab859bf7b879cbfac9060f73759da6808a41fce21a",
        "content_score": 3.858799317441106,
        "document_identity": "1c62e70a6431d31f514967ab480cdc5a591a3ed8e73d3877864ffedb19631513",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.858799317441106,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 62,
        "address": "tests/tools/test_command.py",
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "content_score": 3.8568647922637793,
        "document_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.8568647922637793,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 63,
        "address": "src/devtools/persistence/docs/json.md",
        "content_identity": "85a248d3aba710365dbda906dcf1bd318352c67a726961760e8dd7f14399ccab",
        "content_score": 3.7764441943460154,
        "document_identity": "5cd072b815db6f4b680a2fc2048a1a2aa5f8c08317a14bde9da283d7572ca3ce",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.7764441943460154,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 64,
        "address": "tests/resources/commands/test_execution.py",
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "content_score": 3.697384148052306,
        "document_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.697384148052306,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 65,
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "907c737ace884fa0b840921ed3610d712d31693bd82a5e4931641012bcdc3987",
        "content_score": 3.631759599320891,
        "document_identity": "8986afd525a3d67583c80d8f07e5e1883310b3ebc9d6013eed34e30d2640ad46",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.631759599320891,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 66,
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "content_score": 3.6239020386485974,
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.6239020386485974,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 67,
        "address": "tests/agents/integrations/codex/test_agent.py",
        "content_identity": "4c3636ded84b2b1feeebc2b27132308a34c2827098bde9be25d13450a647d607",
        "content_score": 3.610658403743851,
        "document_identity": "37524b1f8eb0f2d9faa0ab850fdf52deae56ea57ed9665ba581ccf38cd143d2e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.610658403743851,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 68,
        "address": "src/devtools/persistence/sqlite.py",
        "content_identity": "1c7948a64811c6f37f9d7070f612e60f02fc19ac2c2346c0ec66bd37082886d2",
        "content_score": 3.6078881831352625,
        "document_identity": "fb9d0eb1271935abc86461bbf5df219f6b9a046df6bd988c4a784499f8908e87",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.6078881831352625,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 69,
        "address": "src/devtools/core/paths/resolution.py",
        "content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
        "content_score": 3.5782046056289927,
        "document_identity": "ea605b7fac3963f6879f92d633cae685fcd3dd0c4b9393ed77b4f29ff9b4bd88",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.5782046056289927,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 70,
        "address": "src/devtools/agents/conversation/docs/conversation.md",
        "content_identity": "4e3efd18c04125aa129a58ef15fa0b42935c646788bfa1c5dd3fe9f8724afdc6",
        "content_score": 3.5539536278201154,
        "document_identity": "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.5539536278201154,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 71,
        "address": "src/devtools/resources/commands/docs/events.md",
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "content_score": 3.531477013415565,
        "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.531477013415565,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 72,
        "address": "src/devtools/agents/conversation/docs/overview.md",
        "content_identity": "b83cbdb84ae5d216481d0544256cbc8b4bc520b73e071a5d02bbba13fde39ee9",
        "content_score": 3.5116353701932,
        "document_identity": "22f492bc9ceb8595d4e3081786a24f3803e97aaf6150528e79ed32809b78b394",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.5116353701932,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 73,
        "address": "tests/scripts/qwen/test_python_function_context_acceptance.py",
        "content_identity": "3514b02dc85d278a0800cca66340247d63cfc5bf00630909cbffb61423553ade",
        "content_score": 3.424778720269672,
        "document_identity": "45c847b8ecfc3c1204f0ca0f496e089c64608ee0b7d600150296d1968faa3d18",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.424778720269672,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 74,
        "address": "README.md",
        "content_identity": "f7080e9cb6b51bc1795dbd54719c69e230fd737e47a2bcd0d608d5ba57db92f9",
        "content_score": 3.4059099321614434,
        "document_identity": "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.4059099321614434,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 75,
        "address": "src/devtools/agents/conversation/history.py",
        "content_identity": "25db610d54eeb1bed527bff6839a977374ef218d84e5729743fe063a09a3d1aa",
        "content_score": 3.3393305112680376,
        "document_identity": "a8c7c06f5ed02b92e7e6951196b0950141eb053837515ceeb48ab5f37419a7f9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.3393305112680376,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 76,
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "content_score": 3.2500509898266974,
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.2500509898266974,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 77,
        "address": "tests/core/time/test_models.py",
        "content_identity": "0738320772b65625e0085212c949e34b4185fcf58ebe093ed4d45a8d358b6660",
        "content_score": 3.2470294197530642,
        "document_identity": "d72f337252161b196dcd8aebdec5da0dcd2a063ff3b4882530b54dbf87d5fbb6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.2470294197530642,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 78,
        "address": "src/devtools/observability/evidence/docs/overview.md",
        "content_identity": "98431aec7bfdfc9c7a4396d6921a5f4174312ccb791b93741b03f8eb0b27c4e7",
        "content_score": 3.23837269963663,
        "document_identity": "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.23837269963663,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 79,
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "content_score": 3.1692636729343957,
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1692636729343957,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 80,
        "address": "tests/resources/filesystem/models/markdown/test_file.py",
        "content_identity": "4baafbfb0b8ed4829bb5ae9d6243ccf0a739f4560187bc3ed64938d4ceb3d5d0",
        "content_score": 3.121166439589457,
        "document_identity": "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.121166439589457,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 81,
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "content_score": 3.1119221202552536,
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.1119221202552536,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 82,
        "address": "tests/agents/conversation/test_session.py",
        "content_identity": "65cef479981456b043a3bbbb834a69aa1084381c39a405316f2507e487bf9959",
        "content_score": 3.0992537065235872,
        "document_identity": "8b0ff4fa17c0b7be966ab06f563f6f391b4416dd67839dd5363353069f0ab9b7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.0992537065235872,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 83,
        "address": "tests/agents/conversation/message/test_message.py",
        "content_identity": "018edd9fec6141cd06971551c60343ee4502df935dd5133ed64396386043c941",
        "content_score": 3.020599675116748,
        "document_identity": "ab89d2dc88f6dc9e1e6bf3e81bc12957376dabae7a73b86478af84b5f21fb541",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.020599675116748,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 84,
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "content_score": 3.020001097948008,
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 3.020001097948008,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 85,
        "address": "tests/tools/test_execution.py",
        "content_identity": "ca795dd35424539b29e091e66f20e67a66c99f9b2902729a49d1f8264555c5c2",
        "content_score": 2.9359667824588453,
        "document_identity": "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.9359667824588453,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 86,
        "address": "src/devtools/context/repository/resource.py",
        "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
        "content_score": 2.931381785915333,
        "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.931381785915333,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 87,
        "address": "src/devtools/core/identity/docs/overview.md",
        "content_identity": "49232ef5c3a6fca94691bd6dfe84468497d1e17958a349d56dfcd731730cd3b4",
        "content_score": 2.8918230066172708,
        "document_identity": "fe91279815b097915f61055c22b9cb826efac26880e6a831bb43e6ba7fd0f38d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.8918230066172708,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 88,
        "address": "tests/scripts/qwen/test_patch_proposal_worker_acceptance.py",
        "content_identity": "39d7968ad73e318294da9a5e479e28c23736f2eb3857bcbf761109a9385be5ba",
        "content_score": 2.7616743241873767,
        "document_identity": "c045e0ebdd7720591b1f4f9397c76c941cedbb9b0fce5b8d7528abf27130afb5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7616743241873767,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 89,
        "address": "src/devtools/models/benchmarks/models.py",
        "content_identity": "856e9cb0a4355718d4bd7599c1a9ba038f44eacdcfeceda48958facb56b670f5",
        "content_score": 2.7178724075050082,
        "document_identity": "5dc6c417b7eeeb78afe9888232f2cac5198575bded9ab6d985b24af847c65ed3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.7178724075050082,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 90,
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "content_score": 2.55902985388092,
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.55902985388092,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 91,
        "address": "docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md",
        "content_identity": "519c04b8ac5bb3ffddb591a7429d464b2805f84ca82787d93c05638c1a60a34f",
        "content_score": 2.5180607956763397,
        "document_identity": "e8c18d38d7dc924942a169b6607a67f9392725b4324060809b797aedd565f716",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.5180607956763397,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 92,
        "address": "AGENTS.md",
        "content_identity": "53d82c12ad707fee6bdab62b533c0a2f3c6f574667d7a60ef414e39b364a132b",
        "content_score": 2.433911197829358,
        "document_identity": "0efaaf039ed9cbf9354a3ae3092989c8cd0fccf574808ffc0775c2f431220d05",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.433911197829358,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 93,
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "content_score": 2.4067487647678116,
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.4067487647678116,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 94,
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "content_score": 2.375044355546897,
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.375044355546897,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 95,
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
        "content_score": 2.340462817692208,
        "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.340462817692208,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 96,
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "content_score": 2.260968178703606,
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.260968178703606,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 97,
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "content_score": 2.2352500492745007,
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2352500492745007,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 98,
        "address": "src/devtools/models/interaction/docs/overview.md",
        "content_identity": "0e21114ed3c5afcbd745202deb7cbacc21440d36bb6baf96b21139e5a827b1e7",
        "content_score": 2.2326191469167247,
        "document_identity": "5d92535e7d4cfb0d283a7c6e912005c1363f04d7bc0284519ed82ae36b817fa1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.2326191469167247,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 99,
        "address": "tests/observability/evidence/test_model_interaction.py",
        "content_identity": "b736d5348b8c5a9aa918cc53c46405399c1506092b79acf8a2102cdc5862a812",
        "content_score": 2.1815861505415683,
        "document_identity": "e6aee6e5d7ba7e7e722752348dbf953bba15033c5a065ef8a9615b28fa40c4f4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.1815861505415683,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 100,
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "content_score": 2.161327383326502,
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.161327383326502,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 101,
        "address": "src/devtools/core/time/parsing.py",
        "content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
        "content_score": 2.1457915836396455,
        "document_identity": "cccca326a977e6beb684aad1b0dfd37a5eac06522e26fc35816e18782ed773d9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 2.1457915836396455,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 102,
        "address": "src/devtools/core/time/docs/timestamps.md",
        "content_identity": "91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941",
        "content_score": 1.9828975144208387,
        "document_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9828975144208387,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 103,
        "address": "src/devtools/core/paths/docs/resolution.md",
        "content_identity": "fa40ca033450a10898e69600e81e7e4246280aa9a9eff6ea68da740d6cd932a5",
        "content_score": 1.9679580997375812,
        "document_identity": "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.9679580997375812,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 104,
        "address": "src/devtools/agents/conversation/conversation.py",
        "content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
        "content_score": 1.8300776086889359,
        "document_identity": "6f120fa0ff94cba2753771027282694420452f884fbccb1c9f1c7b8d1cd64422",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8300776086889359,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 105,
        "address": "pyproject.toml",
        "content_identity": "275a92369ed49b4d8add7193bf2365a36a4e1b2e1989e0078d4a13bce3a3a618",
        "content_score": 1.8104716886536973,
        "document_identity": "2b4b7c3f4b36cbdb3f013f86355fabc1bdbce1a06b80b174929ab973be578209",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.8104716886536973,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 106,
        "address": "docs/backlog/overview.md",
        "content_identity": "cf65c04505519020b18c3b67c4f3e3ce1ce867e0d9e0a3d59348cbbb8afd50a0",
        "content_score": 1.7525678525890604,
        "document_identity": "d37d55c3023bec275107bc846340172dfa999440b5c9688c2cbb0ccef6f1bcbf",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.7525678525890604,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 107,
        "address": "tests/scripts/qwen/test_llama_cpp_service.py",
        "content_identity": "d91be75d45780bd76e9606526e6d391c07e7dcc729c73fc4e62d0b6a5181b848",
        "content_score": 1.7363390057321895,
        "document_identity": "e6e99c0bd3305061c8522f31cf1b7ddca3a9f1a5ae3acc40f5dd56026fdbc1f7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.7363390057321895,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 108,
        "address": "tests/context/python/function/test_declarations.py",
        "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
        "content_score": 1.6793854056479556,
        "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6793854056479556,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 109,
        "address": "tests/agents/conversation/__init__.py",
        "content_identity": "e9c90fef7a2be899ab41d3d384bc2f24da729af15655ad1269467fac307391fd",
        "content_score": 1.6563411354065691,
        "document_identity": "d1e153e2a1f735f75da9161230da521b8c8f741b609cb971bfa05bba82d61e4a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6563411354065691,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 110,
        "address": "tests/observability/evidence/__init__.py",
        "content_identity": "3da89ca2ca4351ec7917dfe8968829b6eec8b7c99a4b5d0fbec90191a90f9591",
        "content_score": 1.6563411354065691,
        "document_identity": "2f28363c4be5501df96c33cf4be4179701c00272a1a754d1df2264486bb7a0d7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6563411354065691,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 111,
        "address": "tests/persistence/__init__.py",
        "content_identity": "edb967950ec1437b730ec9317b1ddf71b553e84dcc71fff66825f0afa8f6ee5e",
        "content_score": 1.6563411354065691,
        "document_identity": "19c8ab310844f246f4889dfbb4b029952f3172a3576b86e161c4f1d732494dcb",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6563411354065691,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 112,
        "address": "tests/agents/__init__.py",
        "content_identity": "95cb59fa30a936329c46138d6d327cb5ece9753d4c3419617e61529f519add89",
        "content_score": 1.653764512439655,
        "document_identity": "752c56dd736f6067dcc19988e2e3e0e4bd1520851b0a0bab0082f41d18ed3e55",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 113,
        "address": "tests/agents/integrations/__init__.py",
        "content_identity": "f795f63f0889aac4105ffce4a230a03af26eb8d872be78707b3a9d31ec7ec8de",
        "content_score": 1.653764512439655,
        "document_identity": "de2b54be71af9346263bc1922908c3cd4a6ca1b3d63be34339b66aaadbe2afe7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 114,
        "address": "tests/agents/integrations/codex/__init__.py",
        "content_identity": "d07cee53ec0bacf855455f5cf90cdd5139befbb2c127902bcea94fb2bf821c06",
        "content_score": 1.653764512439655,
        "document_identity": "141c494f388c8b96897e49714bde6b2d9f105209fd0f2ec3dc2f29f3eadcbec4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 115,
        "address": "tests/context/repository/__init__.py",
        "content_identity": "a4ddb695661c9f434550d390ce57e64c963c257b60c158db9fe481753701b0af",
        "content_score": 1.653764512439655,
        "document_identity": "d31c50ed94c13ec697ed34cc0ab10c5b15dd3c229acf94c6480ff3c43d95b476",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 116,
        "address": "tests/core/__init__.py",
        "content_identity": "83ab60e0b4499fac83e4e651ca33d984aa52ec0e33a06a751073108ba8100728",
        "content_score": 1.653764512439655,
        "document_identity": "93b4950e8bf19821d277fb7a6fffa03320ef6d1e14af944f4aebab5602fbe651",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 117,
        "address": "tests/execution/__init__.py",
        "content_identity": "d7e4439ed88f2edf74503d5f95e355dc6f8b9a17a104acc159d0489ae3aab26c",
        "content_score": 1.653764512439655,
        "document_identity": "c1aae5ab7c6070ef5d1d21657316331c763e8342030d8d1831587db82fdfdb9d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 118,
        "address": "tests/models/__init__.py",
        "content_identity": "5d07456e2c21e78ac7e77cb193c9fa55e2ed2f429f7c2fe7e07c752bb35f2d0e",
        "content_score": 1.653764512439655,
        "document_identity": "81d8d416a44e2156f82b9b0eb11fea3294c352e6f4fed5209827aca801b5ddc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 119,
        "address": "tests/models/benchmarks/__init__.py",
        "content_identity": "15e003260ce96077c0604a88d1b238e972c2a5a22e0d729b756c6084a9a445ff",
        "content_score": 1.653764512439655,
        "document_identity": "4b8d4353ada69fcd1f5d2be29a84a92d4e23fdf0d5c3c4b1296366b71eb13f84",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 120,
        "address": "tests/models/interaction/__init__.py",
        "content_identity": "03845fa419576eb82b4c37f6351c5c716c77590c473eb26de51c7348d3f7e86b",
        "content_score": 1.653764512439655,
        "document_identity": "25883feb876b248d957d9ae44db193ae5e55c896998878c4b03d1fe0a0774c81",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 121,
        "address": "tests/models/serving/__init__.py",
        "content_identity": "356dbed695c9205f3c2d84b1a5531529d2df170690310700f0364e851456cdeb",
        "content_score": 1.653764512439655,
        "document_identity": "b81fa5506b162929a5a882b86026d6bde5e44369cf7bd62fa23384380b649a55",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 122,
        "address": "tests/observability/__init__.py",
        "content_identity": "6be82c27ba3ce25dc49ea89660304b9c0771f03e6bcadb4c70010390d7024c27",
        "content_score": 1.653764512439655,
        "document_identity": "ecd1241594c51447b247a203ed472fd8825449e5a232b7fa3284b36aa59b2f90",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 123,
        "address": "tests/resources/__init__.py",
        "content_identity": "4d1ff59b18a129f0df9a8ded62185ecb13330f11dde0f1c08620bad2c5eba50e",
        "content_score": 1.653764512439655,
        "document_identity": "63c10870a4738a4da222cc60eba9c7f5e05033631f9af20b5e99972790bc2789",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.653764512439655,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 124,
        "address": "tests/context/python/__init__.py",
        "content_identity": "2e25d9a33df0dd911114ef812a22f7a16a3a4418014d70b982c75def2b9177fd",
        "content_score": 1.6511958934691782,
        "document_identity": "f270e3b71c08967f8b9ee77b242e5af36ab0373c8619f9b21d3df16fca47d7b1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 125,
        "address": "tests/context/python/function/__init__.py",
        "content_identity": "e8a87f81600afd1533894bf2dbee71582d94365ac2a7143caba44516e0d33b08",
        "content_score": 1.6511958934691782,
        "document_identity": "5d9f449f4110ab1e965daa4fc2cd83393b17e9303de42d9832fa8f0cf9798ab3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 126,
        "address": "tests/context/retrieval/__init__.py",
        "content_identity": "8d3f6a78566b854569d2feb7e41a240158556b0c2e8143e1a88a128102e7b16d",
        "content_score": 1.6511958934691782,
        "document_identity": "266d278806888f38a236f7577a694240f50122e14495e173b87e0c5a188591e3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 127,
        "address": "tests/core/identity/__init__.py",
        "content_identity": "318fe561871bac625099c7ec765f72d50cde7864749d33f99f94b088425fdb12",
        "content_score": 1.6511958934691782,
        "document_identity": "682aca9f60d689c6df8c1d65a492f4c70b67542903096c7e900d20acf0ce72e9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 128,
        "address": "tests/core/paths/__init__.py",
        "content_identity": "112b94984c3496a1b7b06dd0cbb40e3a542c54d32e54ef132770bf73844a4f22",
        "content_score": 1.6511958934691782,
        "document_identity": "744ee7b6cbb7b34f900baffb9ccbc76f0d865a5580bb925d59b284146900e393",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 129,
        "address": "tests/core/system/__init__.py",
        "content_identity": "879a8d83b877842bb5884828375b7858051aef530e6956484ad4506ac1d157f2",
        "content_score": 1.6511958934691782,
        "document_identity": "6df0f0e665340d4787f1ee92bd5c50627d6b1486c5547efda49fa23b135a2079",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 130,
        "address": "tests/core/time/__init__.py",
        "content_identity": "ab3d3080eb977f91154f659e95d5f6b4af74df4a692c5154c10ac24ac7f7a017",
        "content_score": 1.6511958934691782,
        "document_identity": "6a89be312e625ba08d9938b1dc34715c7773904dcc4e8c51b29611ff38db6674",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 131,
        "address": "tests/models/interaction/providers/__init__.py",
        "content_identity": "0e89c5fb746cafd96b282d84be2c2e77ea9d57b038615de658be94c75ae4e37b",
        "content_score": 1.6511958934691782,
        "document_identity": "2c626808f980084dea359ea3e67d224c52931d7515b1085acc173be29e1e4467",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6511958934691782,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 132,
        "address": "tests/core/regex/__init__.py",
        "content_identity": "42b00e65be97c2eab3e15b11883b4d62713d53628284936c1e267ad57917156a",
        "content_score": 1.6486352412576706,
        "document_identity": "3a25288adf09d5aca3872a2eecb05e5b6c44e5ffef644836464807c13bb31de8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 133,
        "address": "tests/resources/commands/__init__.py",
        "content_identity": "512f63ddf73c412067cb1c8eff784d005d70202fdae5200bd08ee33309fe67d3",
        "content_score": 1.6486352412576706,
        "document_identity": "f9dafa2b13f67569a56b60f9b1af60d2383a4e89c6c9465c8cd71f3f5f6904ad",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 134,
        "address": "tests/resources/filesystem/__init__.py",
        "content_identity": "4240eddd87df34f3412dede0acb7700e2cae0d0c227a48387a218f58cc5273af",
        "content_score": 1.6486352412576706,
        "document_identity": "65694273596e475ce8387480df883f9227b5bf3dd0dbbbce65159614cf5e6e0e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 135,
        "address": "tests/resources/filesystem/codecs/__init__.py",
        "content_identity": "70a9ca92be20c4c09ee6bfe45d22e53fe190f7941f433c41120500ac890b7933",
        "content_score": 1.6486352412576706,
        "document_identity": "b76d63f7aebf4f36fd7f9707e22c7f88d7e19fb7b07b4c3b7937fda49199b222",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 136,
        "address": "tests/resources/filesystem/models/__init__.py",
        "content_identity": "76b2736bb28edb7484c63fb8bed213e99b1cb9e50fc3db45c965238bb6e54063",
        "content_score": 1.6486352412576706,
        "document_identity": "6f7111640c0731dd98e48cf36eacdcd7ba52e604795bad960e0e7cfa313a2814",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 137,
        "address": "tests/resources/filesystem/models/markdown/__init__.py",
        "content_identity": "6b9f9de506cce6e898f7615d1a9e281049b49a5e38dc9d972448026723e131d0",
        "content_score": 1.6486352412576706,
        "document_identity": "d99bf27d4a02a09694af6ee0671baa4e6ec35d330a6b2ac9ed56d6c5a0561bc8",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 138,
        "address": "tests/tools/__init__.py",
        "content_identity": "726ac7b7eaccd4faa8c34c92b0aabf4908155cb121acca9d9f6e1b5a7af37a86",
        "content_score": 1.6486352412576706,
        "document_identity": "924b469a2755d8ee3880e4ce308979ba04cc4def8e1d3e432acc5278f56956e1",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6486352412576706,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 139,
        "address": "tests/context/__init__.py",
        "content_identity": "3572c092e02fdfe637dd358503b0f6d6f987a86cdc480a31e0a24757c4a6b3b7",
        "content_score": 1.6460825187982966,
        "document_identity": "98b79a5da04d34f985f93b0c0a348fdf72891358de0ab46ab780c4fe837a0ea2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6460825187982966,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 140,
        "address": "tests/core/conversion/__init__.py",
        "content_identity": "dd56c70d043fa64eb4f375989b1c5536b234c0b37fdf7009a44955cda33def1b",
        "content_score": 1.6460825187982966,
        "document_identity": "4049d025bc1766918eca24a74050562dd8fc5c3e53a915415ea25ef6533f5d20",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6460825187982966,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 141,
        "address": "tests/resources/filesystem/models/csv/__init__.py",
        "content_identity": "35f61202fe77fed04ffe0db8d2b53a6be7d7bbdff668c95fc9f355d5b04a3a43",
        "content_score": 1.6460825187982966,
        "document_identity": "76f757fab128fdb944c4e01146850906b4d882fcdcb1338e31a84b69cb13d983",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6460825187982966,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 142,
        "address": "tests/agents/conversation/history/__init__.py",
        "content_identity": "5669d0bd69cf02e91c6cc32ea2626b873d9849ef1e588e7e4f14138bfb4a39be",
        "content_score": 1.6435376893130693,
        "document_identity": "64e70aa293269bb55d279228dabc268e6abda8bc6078de1957deae53eb25c3b4",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6435376893130693,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 143,
        "address": "tests/agents/conversation/message/__init__.py",
        "content_identity": "3b2f62df3dc1d659a4cbc8d341c15e4e7c2f44dbe0cf385e2908ef3b598f7461",
        "content_score": 1.6435376893130693,
        "document_identity": "a8029b66600a011ecaddf55e8107428c3154f07b33e79359fd0481fca42adc9f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.6435376893130693,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 144,
        "address": "src/devtools/persistence/json.py",
        "content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
        "content_score": 1.5877604987767489,
        "document_identity": "054b8b3f80d046b70e54bee873d2bbda22f5c0098c05ce6e19300a789f03c017",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5877604987767489,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 145,
        "address": "tests/core/paths/test_errors.py",
        "content_identity": "965280ee5e8b8f4477e99820f7c0f434ac72b0c2f10edaa8f80d2841ad5e790c",
        "content_score": 1.5660619037373846,
        "document_identity": "daa5c7cf7d73b458a4a7cbcafa7ec5afd2cab4ef5d28fd3584eb7b0df35486af",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5660619037373846,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 146,
        "address": "tests/resources/commands/test_errors.py",
        "content_identity": "16db7e62541ee215137cacf568e3631473a1ae31de96f0c998ddb73bb7cdf3ac",
        "content_score": 1.5660619037373846,
        "document_identity": "4e64b11d8ff810a7d11f1039ca5416a121d2c413fc6240963585716e353a12b5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5660619037373846,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 147,
        "address": "tests/scripts/qwen/test_two_read_acceptance.py",
        "content_identity": "06bc002a1bc83452150e618d4392cf624baa9f71a02cc9e95422ffe0e7500883",
        "content_score": 1.5642602524421803,
        "document_identity": "fe68fde589c53a9ccde159d09e7316958e61c714e517722fc2674315c0415ee2",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5642602524421803,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 148,
        "address": "tests/observability/evidence/test_protocols.py",
        "content_identity": "e0f5600f06a37bceed0f1ee3ccb7c1120e485458a11c8c456800b1530d8470d1",
        "content_score": 1.5125848668678532,
        "document_identity": "e6ba8f2e83102c88dd17ca558559b5cca545ba298b792b51f8f390ddb2349217",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.5125848668678532,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 149,
        "address": "tests/core/system/test_detection.py",
        "content_identity": "3ae8419b24fb1a1e9564690664a354148a78ba51ae0658c602f455a6c412d3ae",
        "content_score": 1.501900266885603,
        "document_identity": "f89b9abcd3de9f4465eb5ce63965619921d85ce971f04744933b27ae7c935b50",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.501900266885603,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 150,
        "address": "tests/observability/evidence/test_terminal.py",
        "content_identity": "3b68af25c442cc55cd15f703b733984f7801695d34fe4720b8de0f04c5a92167",
        "content_score": 1.4586258027650276,
        "document_identity": "69c278fb0d0981b7816ed6ac0b899a4cc3dba17da1c75764ea894c72215021b3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4586258027650276,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 151,
        "address": "tests/resources/commands/test_events.py",
        "content_identity": "229c76e8ba2d20feec3734c5a62f02b1c08941aa09daa90702d41cdafc6669ee",
        "content_score": 1.4388835388357544,
        "document_identity": "e61b06439584a3672c4e51e326a45fdbed99653d7ff72828e9595580529c4295",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4388835388357544,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 152,
        "address": "tests/core/system/test_models.py",
        "content_identity": "eb127a1712e6a79e7678f774793354c74db08513b081e76a8f83a049323d99ab",
        "content_score": 1.4121254931546925,
        "document_identity": "a1e7065b1148474ee9b2b6010a32fa01671908a9941792e2d844fd2e05536382",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.4121254931546925,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 153,
        "address": "tests/resources/filesystem/models/markdown/test_heading.py",
        "content_identity": "bb40d08eb579f1f0227b8eb5700da64b870455748d0497ebbfa11fb00c997b85",
        "content_score": 1.3791504878972287,
        "document_identity": "f535129087774a07134900fd77e2da712e3ca5d8f6dc76ee1d0d7995feaa6d4e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3791504878972287,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 154,
        "address": "tests/models/interaction/test_protocols.py",
        "content_identity": "0c92cb6200c3c86604983272429298aa0c03cf16f8fa8e10fb8759970fc2d5a3",
        "content_score": 1.3111143523440287,
        "document_identity": "7e2e03225568ed44bd97fa05146654616413c5b06de5ccb01afce84127a02fc9",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3111143523440287,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 155,
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "content_score": 1.3078883205278942,
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.3078883205278942,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 156,
        "address": "tests/scripts/qwen/test_llama_cpp_profile.py",
        "content_identity": "f05049563bff24f129a9c1afb629b31bf5f02c2d100cf05a32a8ebbe9d441db8",
        "content_score": 1.2810948914040121,
        "document_identity": "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2810948914040121,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 157,
        "address": "tests/core/time/test_timing.py",
        "content_identity": "71f916d9862a9ef526637f8c1540f30367ddde7bf8dc7895b99c572ff196446f",
        "content_score": 1.2718986056298605,
        "document_identity": "9c3094b125637b3199b68bb621cb8a1156f1f401c6a63354cc1c8c510545a5ec",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2718986056298605,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 158,
        "address": "tests/agents/conversation/test_session_id.py",
        "content_identity": "a84c2db17af8824845875aa28311978a30c75aa83bb488c6586e371b95194860",
        "content_score": 1.2703787122743326,
        "document_identity": "452c09b6282e8b1e51a4fc20b6891801f094caf0f9e96ce83d3653f8afe22446",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2703787122743326,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 159,
        "address": "tests/core/identity/test_models.py",
        "content_identity": "0cf0d9523fbbf65faf921bf427eab8c7e824ede3c89b4e50a3eaddbb73d9b66a",
        "content_score": 1.2688624470674674,
        "document_identity": "cc10c70082af72eb73a9eeb4ff5bb12db25198b1ffc6c47e79f1e3ed55f034c5",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2688624470674674,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 160,
        "address": "tests/core/regex/test_search.py",
        "content_identity": "1843c27fc42cd38efa94309884e7e84b26f864d578dc1e215e2e85e0a4e8d0d6",
        "content_score": 1.2082916848237977,
        "document_identity": "2de00f4eeafe6020b4a015bce5930a4052c85118c5274a674c74e5f406120da6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.2082916848237977,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 161,
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "content_score": 1.200107590290226,
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.200107590290226,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 162,
        "address": "tests/resources/filesystem/models/csv/test_row.py",
        "content_identity": "8d63f6babe5f23ccda12074cb4945e18975502f6f4b930ca8182314e16b8e99b",
        "content_score": 1.198754341046841,
        "document_identity": "b6325384827842a4e7782e7ef2acb6673877764a6d41499d6202d107a9a1d10b",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.198754341046841,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 163,
        "address": "tests/core/paths/test_resolved_path.py",
        "content_identity": "73a33d57bf507dd3c4406a1c4b537fb7322222ff13f5c9366c74743403f9e767",
        "content_score": 1.1801243174255582,
        "document_identity": "4ade5bffcde8661003b193aafe8b6f7663f719f7c43ff9fe64f49e00a96c3501",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1801243174255582,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 164,
        "address": "src/devtools/resources/filesystem/models/csv.py",
        "content_identity": "0cade3699fe596ba492a6509405496cba9b3e2b616d8c0de6f19b47ca0ba9d40",
        "content_score": 1.115766221581824,
        "document_identity": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.115766221581824,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 165,
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
        "content_score": 1.1064305775762147,
        "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.1064305775762147,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 166,
        "address": "tests/models/interaction/test_tools.py",
        "content_identity": "6e3ab9f9b1779c387b72e6230b41ee76fed695f40eb55610240c9eecea85f596",
        "content_score": 1.0905406657393526,
        "document_identity": "7e8ca45cec1b4dfaa4fb2e2488824467b0bceba8c0abafaa885da0137c0d84d3",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0905406657393526,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 167,
        "address": "tests/agents/integrations/codex/test_parsing.py",
        "content_identity": "439b45154cc05f2121215643bef2b65528ac21882205864c96bfa03c8e0387b1",
        "content_score": 1.0860841775438004,
        "document_identity": "3e63c843d294c6ce3e6a3cfe0a39abc751c5afd430b21dd9dbafcbb053ddd833",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0860841775438004,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 168,
        "address": "tests/core/conversion/test_conversion.py",
        "content_identity": "2ec54b402be934e923753e7e92554fcc974ea330d3172e74b9aa08f3cd97cd98",
        "content_score": 1.0233551528264608,
        "document_identity": "f1a56231ca6a3df1207eb40dd21fc24a4728b5feabb6aab7ec6834ea73d32aec",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 1.0233551528264608,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 169,
        "address": "tests/resources/filesystem/test_json_conversion.py",
        "content_identity": "9757259e385ae2a84440d34809686a6dbb7854b2f475bded7f409f81c87278ce",
        "content_score": 0.9900004381941567,
        "document_identity": "24c1c20e2050fede03130cb6549cda56dac3e7b786f39434e1c450e4cd81f782",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9900004381941567,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 170,
        "address": "tests/models/benchmarks/test_models.py",
        "content_identity": "582423270354ce5925f1c493a10062f906204462e976712730d51cde04f9a1df",
        "content_score": 0.9459547721954094,
        "document_identity": "76b599267e9da2809aeb635279dbc7ecae6f6267a7ce611993e7d9c3ed0a5be0",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.9459547721954094,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 171,
        "address": "tests/resources/filesystem/test_json_models.py",
        "content_identity": "7c29e52ea97ad5929477d5e835913bb6fa1852f7f5ed9d1b2fe12085257c598f",
        "content_score": 0.8235730923507666,
        "document_identity": "7bda444036f7fd3bc32bb0de25b31fb30c3418cf1a5579ced9aabd2b1afd033e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.8235730923507666,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 172,
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "content_score": 0.7682252027761287,
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7682252027761287,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 173,
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "content_score": 0.7676704610952013,
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7676704610952013,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 174,
        "address": "tests/models/serving/test_huggingface.py",
        "content_identity": "9b7b273b3c1fa39ba2eef3158a8c248e1f8546815441314ffe39c9b9c404acc2",
        "content_score": 0.7508621471112671,
        "document_identity": "27a4f51ffab31c0935030839ae052c762bf0df7b6aec2acd04e0a06ae9a83860",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7508621471112671,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 175,
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "content_score": 0.745596021542408,
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.745596021542408,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 176,
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "content_score": 0.7357912112203705,
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.7357912112203705,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 177,
        "address": "tests/scripts/qwen/test_two_action_read_only_acceptance.py",
        "content_identity": "10fc867f673b0db841d41f18acb33e810fb6c53eb6347d2a428714d9c545ef3d",
        "content_score": 0.6550862058995028,
        "document_identity": "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6550862058995028,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 178,
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "content_score": 0.6416431394832384,
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6416431394832384,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 179,
        "address": "tests/models/interaction/test_models.py",
        "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
        "content_score": 0.6393279002116514,
        "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6393279002116514,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 180,
        "address": "tests/models/benchmarks/test_storage.py",
        "content_identity": "a9fcf22fcb76814c755cbcba819c0e8947c082f772b5a7cc9bd0c6c6f6ef8a66",
        "content_score": 0.6228468447762929,
        "document_identity": "b79f92c5457d7e56bba959136c47edf1ca116bab0410b960053a0925f2e4b729",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.6228468447762929,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 181,
        "address": "tests/scripts/test_vllm_benchmark_driver.py",
        "content_identity": "2a5ade1094032b7b54c428459a461dcac86a507bd031ac15a2694a53115fe3cf",
        "content_score": 0.5247696417302163,
        "document_identity": "1bf8fedf436a5ce8b8bd046305c8a601e1d91b51927835fcf4ab241570163ee6",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.5247696417302163,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 182,
        "address": "tests/execution/test_runtime.py",
        "content_identity": "8f4bdbf3044c5a84a7c85bf4780e54f10ca8da669b2fed8ac2f5815669a3d42c",
        "content_score": 0.5036379860943258,
        "document_identity": "5b023dfbb5c27d99b835d209f97a4be2bb8944d4b44cccebe3fa76c90d9f04a7",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.5036379860943258,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 183,
        "address": "tests/models/serving/test_llama_cpp.py",
        "content_identity": "2de258ff8b06e27cb3a0642c77839aef7a6511a39b5809a3dad19029b32c13df",
        "content_score": 0.34562860100551795,
        "document_identity": "a089f2e125cde19a5710349d147e12d4e6e0691929511ccc75f37b9ee7da2402",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.34562860100551795,
        "weighted_filename_score": 0.0
      },
      {
        "a_rank": 184,
        "address": "tests/models/serving/test_vllm.py",
        "content_identity": "66510589d97c1ec89bc405e4aed376407e606215c2bb8fecf89cf36b1ea0beb8",
        "content_score": 0.20531678265063702,
        "document_identity": "27026b44bdb5d69c4be214080f44e2ffda60d025ed1959e6fe0a0fbde1a31684",
        "filename_score": 0,
        "filename_weight": 0.25,
        "score": 0.20531678265063702,
        "weighted_filename_score": 0.0
      }
    ],
    "annotations": [
      {
        "best_supporting_source_rank": 53,
        "distinct_supporting_source_count": 2,
        "native_occurrence_count": 21,
        "sources": [
          {
            "a_rank": 53,
            "address": "src/devtools/context/repository/discovery.py",
            "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
            "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "f778f97e31d2c6a1ffcb553202cbc6ff28b72e055486fe5a963cf939351d8ca7",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "01b4456e5ee0952aa6109932f9dd2192d236aae5d059004b22a4efcd9a5a5041",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/context/repository/discovery.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 157,
                  "start_column_utf8": 24,
                  "start_line": 157
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              },
              {
                "derivation_identity": "f778f97e31d2c6a1ffcb553202cbc6ff28b72e055486fe5a963cf939351d8ca7",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "561e4ac658e55bf60ad4a5542df335f388692a6d5ef58bf5b78183d4778b826b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "src/devtools/context/repository/discovery.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 109,
                  "start_column_utf8": 22,
                  "start_line": 109
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              }
            ]
          },
          {
            "a_rank": 59,
            "address": "tests/core/paths/test_resolution.py",
            "content_identity": "5f34ec0ac3a2580a7a75533d98c503e65084bf00f49f9d736b8c11f0b3ecbeb2",
            "document_identity": "3339ce5906f32477be6a3261caf7eb2c73fa7186b78ed2be80d23a9dde3fd90f",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "07f46efe53d6d9b196dd19a302e4a220837116448302fb5ec6c140ed16f05626",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 21,
                  "end_line": 29,
                  "start_column_utf8": 11,
                  "start_line": 29
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "0941e1c6de19e98b22feb06ff5b0964f40785d1ce37111b8ac2a6dbdab3effcf",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "a2b1319686e223982ffdd15a29d062efd90c8b5ab904cc06b09f7f22b0db5632"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0bbcfacbcd003201a69cb0898262bbb91c10f17006268d5ac2d8170550009861",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 149,
                  "start_column_utf8": 11,
                  "start_line": 149
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "878a380431ce3af367b3075935b53df08975127583f68d35f6e3a355ebd4973a",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "f57bf9d899ce760054bd75455058c9a8a866394e106d0ec81980cbe8ab71da9c"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "17ed24de1ac213cb7f979c581e47c61adfeb9fd2b501ca56fdd5e4f675fdf5d7",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 36,
                  "end_line": 116,
                  "start_column_utf8": 20,
                  "start_line": 116
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "43d212bd8859b306bd058411ab6044a7987b3bfc9390afdbe0dfca994daeb494",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "cfc0b44d61e2981611824d48ee85bee3fd869a2cf9aeab9f595ea78c06256ca0"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "30d7029821e2142f8c0c92ffa3bbbc9d956f171f0391d19a9fa2df8b58cffd77",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 87,
                  "start_column_utf8": 20,
                  "start_line": 87
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "33f35dfb8fdb256eb4dff639e2511e70aa41c28efde3ba3f77ebea85b1e30178",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 128,
                  "start_column_utf8": 8,
                  "start_line": 128
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "43d212bd8859b306bd058411ab6044a7987b3bfc9390afdbe0dfca994daeb494",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "cfc0b44d61e2981611824d48ee85bee3fd869a2cf9aeab9f595ea78c06256ca0"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "399a5856c27b9c0e39a0b5c2c2c43cfeeb41c0cd09c4b839f787d94706ced869",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 20,
                  "end_line": 105,
                  "start_column_utf8": 8,
                  "start_line": 105
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "404a14d0007ace5e93f24af62caf84ba8e0f0fa6393d948e0f6e38012d3a5b7b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 18,
                  "end_line": 35,
                  "start_column_utf8": 8,
                  "start_line": 35
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "0941e1c6de19e98b22feb06ff5b0964f40785d1ce37111b8ac2a6dbdab3effcf",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "a2b1319686e223982ffdd15a29d062efd90c8b5ab904cc06b09f7f22b0db5632"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "6a9aa1a3802d81c006a21b4b478813b70bd951bbe815ae22a0c208a56efbe9b2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 25,
                  "end_line": 46,
                  "start_column_utf8": 11,
                  "start_line": 46
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "71c97709759e7e8ba78f4af2ebb8e3dfe4a641f5843cba6302411170b7b8b2e9",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 25,
                  "end_line": 52,
                  "start_column_utf8": 11,
                  "start_line": 52
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "75998e18b6130f23b43393de86933ee689bbaf7b2baa5923c500a4fe859a4278",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 76,
                  "start_column_utf8": 8,
                  "start_line": 76
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a2e0536fc0fdf3f73be15b94ed78fc4e68fc36c73a821948f794753058192906",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 148,
                  "start_column_utf8": 11,
                  "start_line": 148
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3dd498ded66184c846df73dd35997edfc15381d750ccc53dd9ddddf23e7206b0",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "4cae11e67c6301198f044350ee789ee2a8adf103a84ea1a345ea3988e61bab5c"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a39adfb7d91d161f3a600f30cfcaa8fca6b4fb29c81418d7916875c1d4f26502",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 70,
                  "start_column_utf8": 8,
                  "start_line": 70
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a4f38c3e220cf0f724c6438c4ef16171b16fc8e9f57abc8fc015a680952964b8",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 28,
                  "end_line": 150,
                  "start_column_utf8": 11,
                  "start_line": 150
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "51e94d68aad7a503d723fa01097ad815d412905331cdb4facfdc2ef90cf0c7e3",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "badab7eb89634e838a3283df54dfe0387ab2e3b913456a9ba2fd42205c7c553a"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c2b4c094761ab2445f9a4290191dd57516e2092d449edb983086af8787ce22e2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 20,
                  "end_line": 111,
                  "start_column_utf8": 8,
                  "start_line": 111
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c91af43b2ad003f70e6a6e5b6f128a109285f131b36e3cab97c64c474f0276eb",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 94,
                  "start_column_utf8": 20,
                  "start_line": 94
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "3a47af1d1f44882242c9ff31d52e3fd3de2e19685f67186f9d69cd8e16b1aa41",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "0899f39e0e8483307c79c78bb7cddead3081292b6c8c5fd71a71f703c6fe7bda"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ccc2df3c59bd561d04eeb63659f48c35a5cad0f4db0f2fea9ff4302bc94fa8a6",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 131,
                  "start_column_utf8": 8,
                  "start_line": 131
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "43d212bd8859b306bd058411ab6044a7987b3bfc9390afdbe0dfca994daeb494",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "cfc0b44d61e2981611824d48ee85bee3fd869a2cf9aeab9f595ea78c06256ca0"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "e41189e96382cb90a10b58a58f53422e4260daf2c7129de8f16c85df6c5ce852",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 25,
                  "end_line": 40,
                  "start_column_utf8": 11,
                  "start_line": 40
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ea8ae581ed9c0c2c971e7c358512294c0b637831e6e0789b98c7dbf548fe07fc",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 21,
                  "end_line": 28,
                  "start_column_utf8": 11,
                  "start_line": 28
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "0941e1c6de19e98b22feb06ff5b0964f40785d1ce37111b8ac2a6dbdab3effcf",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "a2b1319686e223982ffdd15a29d062efd90c8b5ab904cc06b09f7f22b0db5632"
              },
              {
                "derivation_identity": "2b99ab22ed58432eeb2ca1014b7f0b87c38310104e7aca660996db621356a759",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "f0a015d36c64a1c46912497656fe424ca879b38bff705a069786252259f715d5",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/paths/test_resolution.py",
                "source_range_utf8": {
                  "end_column_utf8": 22,
                  "end_line": 64,
                  "start_column_utf8": 8,
                  "start_line": 64
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/paths/resolution.py",
                "target_content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
                "target_declaration_identity": "a8fdc7586f77d2d185a9ff2bdcc827b712ac4ba17e514e9d9febe194fff0afff",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3ea2f5e2cda596e45a7bb5a420e1ef4c15518136988d5cd03a3f35f3db85a925"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 69,
          "address": "src/devtools/core/paths/resolution.py",
          "content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
          "document_identity": "ea605b7fac3963f6879f92d633cae685fcd3dd0c4b9393ed77b4f29ff9b4bd88"
        }
      },
      {
        "best_supporting_source_rank": 7,
        "distinct_supporting_source_count": 2,
        "native_occurrence_count": 2,
        "sources": [
          {
            "a_rank": 7,
            "address": "src/devtools/context/repository/corpus.py",
            "content_identity": "3424ce325df02cd6fdca1e7a3344cb5ddfa6d48c8692777bf17dcff3f4eb0477",
            "document_identity": "eb0c8651d77d8d754a458293960a87b3df80dc51b64495fbb40268a3b3018d91",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "99364ae9c49b0fe03ff3a6f7c2e0171e967abc03135835ad98907768c6b5a5f9",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cd77eb64226096a8ed054e880239bd01e3d1e16fb3beef88b0f7d1bd33b29142",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/context/repository/corpus.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 31,
                  "start_column_utf8": 8,
                  "start_line": 31
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/context/repository/resource.py",
                "target_content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
                "target_declaration_identity": "fce372e7691bd6934c0d5233f2cd2b0691fccc07277c78d6426d13435941ebe2",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "1835e9e39e8e0e484922c1f434e8b13accafce73c350cde72880d88bc0fb1706"
              }
            ]
          },
          {
            "a_rank": 10,
            "address": "src/devtools/context/repository/document.py",
            "content_identity": "7282f290f5b5b78c3d2014097aac5cc1cc6012ef6d4489ea83d2411deb980daf",
            "document_identity": "ba623a37cd1339842a7eef88b7f294ac14a1b139d86cbc414710c4bf45fad2cd",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "490c22003de02742d52376e99f3eb4536e017826fbd07b7db46918ca2da94e6e",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "91a7675828aa9f14b563a7ed214787b137d728b0187d2c332bb1c993a48a45c2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "src/devtools/context/repository/document.py",
                "source_range_utf8": {
                  "end_column_utf8": 24,
                  "end_line": 26,
                  "start_column_utf8": 8,
                  "start_line": 26
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/context/repository/resource.py",
                "target_content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
                "target_declaration_identity": "fce372e7691bd6934c0d5233f2cd2b0691fccc07277c78d6426d13435941ebe2",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "1835e9e39e8e0e484922c1f434e8b13accafce73c350cde72880d88bc0fb1706"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 86,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "best_supporting_source_rank": 79,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 22,
        "sources": [
          {
            "a_rank": 79,
            "address": "tests/tools/test_filesystem.py",
            "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
            "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "014a0ec72286ca02b18416578b63a6d4ab38c5fc971e4559697a8a362d7bc151",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 167,
                  "start_column_utf8": 16,
                  "start_line": 167
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0455ff27ea4874e1f60541c31b544f69cc488e80e5e5daf513cad517aa359fd0",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 437,
                  "start_column_utf8": 12,
                  "start_line": 437
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0bef06f1a65c2ace9d7d18bf365bc83c85c7fb16159f44fd4db695e98a88ee75",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 243,
                  "start_column_utf8": 16,
                  "start_line": 243
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "0e19694a0b0c8c61e9d032fde3ac671e4ac48a5cddab34cf5eb61df5f377dd2a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 184,
                  "start_column_utf8": 16,
                  "start_line": 184
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "242c5f063995056516a918829ca3b844efd194e83fd5d240d8f91ef992923088",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 262,
                  "start_column_utf8": 16,
                  "start_line": 262
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "28c24050362f6042631c0ec1d7a5e008cd52260f8f506b6f45617306f4e3a661",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 42,
                  "end_line": 411,
                  "start_column_utf8": 15,
                  "start_line": 411
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3adc6e3fbcfbe8c8d7d160dc985c45893f912e059573b21e22e672d6efabfb02",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 79,
                  "start_column_utf8": 16,
                  "start_line": 79
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "50abf4f13abf1233eb49f6f5ee9179ea89803b5c9024b9486e577de3ded17ec0",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 37,
                  "end_line": 280,
                  "start_column_utf8": 15,
                  "start_line": 280
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "5785691e29b6c3a95b31959217009a8d12a2db975f094b67299d4e9bd14cd986",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 332,
                  "start_column_utf8": 12,
                  "start_line": 332
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "5928711b44e115930e82d068be665c435c8aec74cfcac3295307ff67a2d3f41f",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 221,
                  "start_column_utf8": 12,
                  "start_line": 221
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "5f0c3fb2bcead8ddbca916ea5d801705ef8afd3c246856a00aff47f9795c5407",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 375,
                  "start_column_utf8": 12,
                  "start_line": 375
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "65e84d18f4dd22cff6b5a4a0f643ea7fa339205cf3e954833a2f76f0bac24589",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 35,
                  "end_line": 451,
                  "start_column_utf8": 8,
                  "start_line": 451
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "724743409be7d6b743d03cbf75b2a1fb165ed9786767476e1b6a037821b1058a",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 202,
                  "start_column_utf8": 12,
                  "start_line": 202
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8cda70684a1164c9680a46b2efdff961586005342f2cf32c8ee916d88ef910f0",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 458,
                  "start_column_utf8": 11,
                  "start_line": 458
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "9f490cdc51d499f67522b92cf056666f5a96fa2dc7550404acc5cae1cd1d5715",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 132,
                  "start_column_utf8": 16,
                  "start_line": 132
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a6300c20a34543452d7019b80c66fe89428bdbfa6e73fdb72b96d8ccbcb26bb1",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 43,
                  "end_line": 394,
                  "start_column_utf8": 16,
                  "start_line": 394
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "ab24d4d8586aeeadbb62a0a749afe3f123b463946a25d4741b1192d46f607f94",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 305,
                  "start_column_utf8": 12,
                  "start_line": 305
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "af6323d0c0e240b2b30838711b48fce6229e7be7e39140c4d539d4c983e83601",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 37,
                  "end_line": 50,
                  "start_column_utf8": 15,
                  "start_line": 50
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "c6afe1436089b9d0d9be28773db6407648910f87eb575ab550c7392f04fd10e2",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 38,
                  "end_line": 149,
                  "start_column_utf8": 16,
                  "start_line": 149
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "cd8d7d5b89388daef262a11277997c942e5618fe87912809b98d755f8bfc1667",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 43,
                  "end_line": 484,
                  "start_column_utf8": 16,
                  "start_line": 484
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d69c1b0aa70b13d4933abb06775722331a65de6ea6a235419ae7d3e10938eb3d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 353,
                  "start_column_utf8": 12,
                  "start_line": 353
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "5f3eee77f2f03a40f995f98cc154bf1baa425e489ff07fd99283e839a2720bd7",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "651bead03315576042dab3c790de5f675b396ceab7b78cac2027a14b4647fc87"
              },
              {
                "derivation_identity": "d58c3adeb7db876920758da38985aecefb16ab33a42f6b3c30012140d8a62da6",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "f4a1f67d5f2120ecadd8249b1cb5b0e6939c85563ffa423d7051ae7f35d9b727",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/tools/test_filesystem.py",
                "source_range_utf8": {
                  "end_column_utf8": 34,
                  "end_line": 112,
                  "start_column_utf8": 12,
                  "start_line": 112
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/tools/filesystem.py",
                "target_content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
                "target_declaration_identity": "03b506559c8bbcf69bcc6ea9e85cd6541cb43024c1be7fe2586af66e5f5c1483",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "66900ffdbb09f3de7a70ddb4d5daa4c84a6762cb28dd5f334c8b7c90e0e15634"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 90,
          "address": "src/devtools/tools/filesystem.py",
          "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
          "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e"
        }
      },
      {
        "best_supporting_source_rank": 15,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 7,
        "sources": [
          {
            "a_rank": 15,
            "address": "tests/core/time/test_parsing.py",
            "content_identity": "de9b7a2ba6d7c57112f2c0f82fb58165ee5b774ef6020051d927d9200a88cf63",
            "document_identity": "a3f3c90ae6548f028f6f50e5cdc1c3465b0fca7ca52c20064252a5a9027f48b7",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "10b98eb876a890e954fa33112bf9cf9e2860004e257e0431595a7c0a192c2a2d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 31,
                  "end_line": 71,
                  "start_column_utf8": 16,
                  "start_line": 71
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "29564ae7871d39356070df13c9d39e098479a37860bc4d200f5b664f04a7c878",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 66,
                  "start_column_utf8": 11,
                  "start_line": 66
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "3e681dee8e5db8adc791c2701a833ed714d0a7bbf1e422dc6c29ae11679e7e65",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 29,
                  "start_column_utf8": 11,
                  "start_line": 29
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "9cdd868fbafb17cba00b056073514bf3fdd018ce071d408d5c3ca20157e3470d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 37,
                  "start_column_utf8": 11,
                  "start_line": 37
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "b8413f002bed8871995a6b1f9d5c172c478b6be7cc25a2376dfd70391332cddf",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 80,
                  "start_column_utf8": 8,
                  "start_line": 80
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "d8a5552e06320f2452aa4871e3355fad304f1843a26826e5b03b45880edc0970",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 22,
                  "start_column_utf8": 11,
                  "start_line": 22
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              },
              {
                "derivation_identity": "308c8e1a266f0d7c81a8636c81f99b6c8168c88c03c6483855a2d8fb3b908905",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "db082c6756bcf38d40693da996ec933fa800be0e5489ad5408cff19bb62b792b",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/core/time/test_parsing.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 44,
                  "start_column_utf8": 11,
                  "start_line": 44
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/core/time/parsing.py",
                "target_content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
                "target_declaration_identity": "1970ccfb4017ebc1404973a51789f402686c830e892da6a82076d8f188d6149f",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "3a6cfe22202ed07f5bf1d039d12e9dbee2567f4e960c29eee39b06cd81f106fc"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 101,
          "address": "src/devtools/core/time/parsing.py",
          "content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
          "document_identity": "cccca326a977e6beb684aad1b0dfd37a5eac06522e26fc35816e18782ed773d9"
        }
      },
      {
        "best_supporting_source_rank": 82,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 2,
        "sources": [
          {
            "a_rank": 82,
            "address": "tests/agents/conversation/test_session.py",
            "content_identity": "65cef479981456b043a3bbbb834a69aa1084381c39a405316f2507e487bf9959",
            "document_identity": "8b0ff4fa17c0b7be966ab06f563f6f391b4416dd67839dd5363353069f0ab9b7",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "33133a244662f179ec727e67c757c9949274547c2c5e7e95afdb61825efbc52a",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "7e1dc521ad89ea6656dfabd8130a38ecd7847e098de5da21570f4fd9e5514ba4",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/agents/conversation/test_session.py",
                "source_range_utf8": {
                  "end_column_utf8": 26,
                  "end_line": 75,
                  "start_column_utf8": 14,
                  "start_line": 75
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/agents/conversation/conversation.py",
                "target_content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
                "target_declaration_identity": "6e76a5dcb6e974f4377cc29f0e682f0cf1c532854ce4d2362ad0cbf14f090f50",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "d767a48af0d1215d688fc11aa29a4a43727491592ac7d515c73f02f4df5353ca"
              },
              {
                "derivation_identity": "33133a244662f179ec727e67c757c9949274547c2c5e7e95afdb61825efbc52a",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "8c159e90c59ffdfe5a305681aa613f750f78ba77c830f16a322e5fc740f25596",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "imported-member",
                "source_address": "tests/agents/conversation/test_session.py",
                "source_range_utf8": {
                  "end_column_utf8": 23,
                  "end_line": 50,
                  "start_column_utf8": 11,
                  "start_line": 50
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/agents/conversation/conversation.py",
                "target_content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
                "target_declaration_identity": "6e76a5dcb6e974f4377cc29f0e682f0cf1c532854ce4d2362ad0cbf14f090f50",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "d767a48af0d1215d688fc11aa29a4a43727491592ac7d515c73f02f4df5353ca"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 104,
          "address": "src/devtools/agents/conversation/conversation.py",
          "content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
          "document_identity": "6f120fa0ff94cba2753771027282694420452f884fbccb1c9f1c7b8d1cd64422"
        }
      },
      {
        "best_supporting_source_rank": 19,
        "distinct_supporting_source_count": 1,
        "native_occurrence_count": 10,
        "sources": [
          {
            "a_rank": 19,
            "address": "tests/persistence/test_json.py",
            "content_identity": "e4aac80c8b2fbb70694dbb3cd678ecc9d2a996bcd71836c557d6745539b72d7f",
            "document_identity": "5b391d5c240d0a95ac12883e5a31bea0ed5fdeac3b6d49f5d1b944b6cc5065fc",
            "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
            "supports": [
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "051d93bac148548eb60a47d2cdb4e0a19c73599216a396035613d5f5dcd37350",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 64,
                  "end_line": 114,
                  "start_column_utf8": 40,
                  "start_line": 114
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "2fb3294930ceb6701100d07722cc795340ba7c82db66f69c7f69455f8adbf0b0",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "632c18d721e1f7fb8f72c21cf0ea0e39a6ad26aa9fb0507754cc50a410b65cdf"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "1f96c4257497ccbc8ddf9b43f2c74bf6bc341a0b3ef37bb47833540b031f5298",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 43,
                  "end_line": 95,
                  "start_column_utf8": 19,
                  "start_line": 95
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "2fb3294930ceb6701100d07722cc795340ba7c82db66f69c7f69455f8adbf0b0",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "632c18d721e1f7fb8f72c21cf0ea0e39a6ad26aa9fb0507754cc50a410b65cdf"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "62dda567672c5b8aa266565cd90e16132c3a6eeb43a6b1c828c400642109d934",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 47,
                  "end_line": 78,
                  "start_column_utf8": 23,
                  "start_line": 78
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "2fb3294930ceb6701100d07722cc795340ba7c82db66f69c7f69455f8adbf0b0",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "632c18d721e1f7fb8f72c21cf0ea0e39a6ad26aa9fb0507754cc50a410b65cdf"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "6632ceabf01559d7bd4fc29ec7dceef404e167fb22ee41406337af9fa4f0a8fc",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 184,
                  "start_column_utf8": 8,
                  "start_line": 184
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "6a3f617856c9bcf67aadb6a9659b5393a6359f01f64a38c2f7a2b1363b3a2301",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 114,
                  "start_column_utf8": 15,
                  "start_line": 114
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "70adb08e53a07eeee4cde296b5b4daf5fbe0834748590b9b57868baab4437f68",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 195,
                  "start_column_utf8": 8,
                  "start_line": 195
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "a2f3d5b7e2c0386ddd28591aa104883d97458b7d58caeabf7d39d96e7b3d8e58",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 39,
                  "end_line": 87,
                  "start_column_utf8": 15,
                  "start_line": 87
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "b0520346c693d4dc5c2eb50afcd7af877c6e54e52672f865693e51818100616d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 208,
                  "start_column_utf8": 8,
                  "start_line": 208
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "bfee50326ac121044ede164c2cbcc8014a09f7b81e7111e2c960f46ab0ad4c1c",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 35,
                  "end_line": 86,
                  "start_column_utf8": 11,
                  "start_line": 86
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "2fb3294930ceb6701100d07722cc795340ba7c82db66f69c7f69455f8adbf0b0",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "632c18d721e1f7fb8f72c21cf0ea0e39a6ad26aa9fb0507754cc50a410b65cdf"
              },
              {
                "derivation_identity": "8928524d87714c0c729dda7d650ecaa3c5be558dd1258d9bfcb643a7e71b10ef",
                "direct_call_tag_diagnostic_only": true,
                "fact_identity": "fd1741a12fa26f920917127949e1ee93756c3df1da4adeabdc92f6455371e27d",
                "full_native_evidence": "ri_native.json.gz; native journal source-return archive; exact fact identity lookup",
                "native_route": "one-facade-imported-member",
                "source_address": "tests/persistence/test_json.py",
                "source_range_utf8": {
                  "end_column_utf8": 32,
                  "end_line": 169,
                  "start_column_utf8": 8,
                  "start_line": 169
                },
                "source_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_address": "src/devtools/persistence/json.py",
                "target_content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
                "target_declaration_identity": "9b74776a35497e08bd6b7c1d838bf577cc97adaa832719b2513337331d04f755",
                "target_snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49",
                "target_subject_identity": "dfca3b5c875f2ad5c4ffcafb9d66d9e9a90da8535ab86c0a9ae26df5f4037f8d"
              }
            ]
          }
        ],
        "target": {
          "a_rank": 144,
          "address": "src/devtools/persistence/json.py",
          "content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
          "document_identity": "054b8b3f80d046b70e54bee873d2bbda22f5c0098c05ce6e19300a789f03c017"
        }
      }
    ],
    "counts": {
      "local_pairs": 6,
      "qualifying_occurrences": 64,
      "status": "PASS",
      "support_source_target_pairs": 8,
      "supported_targets": 6
    },
    "frame": {
      "corpus_id": "32d70eb6fef4210e2ef4ccb48486bab51357e4f84e277c3e2b84f17bd89ddf91",
      "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
      "snapshot_id": "0d49c0c3279ef4704a708a06a8ca05ac5c8eb89021802f24e695fb88b36e2d49"
    },
    "information_need": "What compatibility and validation contracts must the new statistics/index preserve at the existing lexical-analysis and repository-document boundaries?",
    "local_pairs": [
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 68,
          "address": "src/devtools/persistence/sqlite.py",
          "content_identity": "1c7948a64811c6f37f9d7070f612e60f02fc19ac2c2346c0ec66bd37082886d2",
          "document_identity": "fb9d0eb1271935abc86461bbf5df219f6b9a046df6bd988c4a784499f8908e87"
        },
        "query": "Q3",
        "target": {
          "a_rank": 69,
          "address": "src/devtools/core/paths/resolution.py",
          "content_identity": "8a6984e55364f45dff03267778fe2ac92ffbec06117ac9da6bf8c0b5cfbc757b",
          "document_identity": "ea605b7fac3963f6879f92d633cae685fcd3dd0c4b9393ed77b4f29ff9b4bd88"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 85,
          "address": "tests/tools/test_execution.py",
          "content_identity": "ca795dd35424539b29e091e66f20e67a66c99f9b2902729a49d1f8264555c5c2",
          "document_identity": "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3"
        },
        "query": "Q3",
        "target": {
          "a_rank": 86,
          "address": "src/devtools/context/repository/resource.py",
          "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
          "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 89,
          "address": "src/devtools/models/benchmarks/models.py",
          "content_identity": "856e9cb0a4355718d4bd7599c1a9ba038f44eacdcfeceda48958facb56b670f5",
          "document_identity": "5dc6c417b7eeeb78afe9888232f2cac5198575bded9ab6d985b24af847c65ed3"
        },
        "query": "Q3",
        "target": {
          "a_rank": 90,
          "address": "src/devtools/tools/filesystem.py",
          "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
          "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 100,
          "address": "src/devtools/resources/filesystem/models/text.py",
          "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
          "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48"
        },
        "query": "Q3",
        "target": {
          "a_rank": 101,
          "address": "src/devtools/core/time/parsing.py",
          "content_identity": "457df61541f03242a6b29008d6fa4db77b6774b14c3646a83d7f1c2aa2de2d9c",
          "document_identity": "cccca326a977e6beb684aad1b0dfd37a5eac06522e26fc35816e18782ed773d9"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 103,
          "address": "src/devtools/core/paths/docs/resolution.md",
          "content_identity": "fa40ca033450a10898e69600e81e7e4246280aa9a9eff6ea68da740d6cd932a5",
          "document_identity": "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524"
        },
        "query": "Q3",
        "target": {
          "a_rank": 104,
          "address": "src/devtools/agents/conversation/conversation.py",
          "content_identity": "cf5d3a46b219f33a3ea7f2f7808e4b8a3c3c09341d5a66f1b6e107e050f1c8a7",
          "document_identity": "6f120fa0ff94cba2753771027282694420452f884fbccb1c9f1c7b8d1cd64422"
        }
      },
      {
        "obligation": "O3",
        "predecessor": {
          "a_rank": 143,
          "address": "tests/agents/conversation/message/__init__.py",
          "content_identity": "3b2f62df3dc1d659a4cbc8d341c15e4e7c2f44dbe0cf385e2908ef3b598f7461",
          "document_identity": "a8029b66600a011ecaddf55e8107428c3154f07b33e79359fd0481fca42adc9f"
        },
        "query": "Q3",
        "target": {
          "a_rank": 144,
          "address": "src/devtools/persistence/json.py",
          "content_identity": "cf5624d0f4d6c2fea576105cecaa0df5753cf088e2c4f2063167ca2d0f171264",
          "document_identity": "054b8b3f80d046b70e54bee873d2bbda22f5c0098c05ce6e19300a789f03c017"
        }
      }
    ],
    "obligation": "O3",
    "query": "lexical analysis unicode word casefold ordered observations empty corpus deterministic tests exports",
    "query_identity": {
      "task": "case-0017:historical-development-001",
      "value": "Q3"
    },
    "task_identity": "case-0017:historical-development-001",
    "timings": {
      "annotation_construction_ns": 1498100,
      "canonical_a_ns": 18243000,
      "complete_online_equivalent_ns": 112298900,
      "predecessor_pairs_ns": 46600,
      "support_projection_ns": 92511200
    }
  }
]
```

Complete positive native Reference identities are in references.json.gz; all positive and negative native RI state is in ri_native.json.gz and the immutable journal.
