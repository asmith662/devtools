# Case 0014 Stage D trace

[Full replayable trace](trace.json) retains exact input checkpoints, all joins, cell/witness arithmetic, captured contributions, gates and precedence. [Human review](STAGE_D_REVIEW.md) explains every gate. No scientific native execution occurred.


## Authentication

```json
{
  "ancestry": "PASS",
  "blind_packet": "15417485eba52eb07631c54dcb141ff8d3294606",
  "primary_sha256": {
    "STAGE_C_REVIEW.md": "628f2f1b86627c33f76807dd3875c7fd49b7dc7fb307f85a808e873de1dd4a4f",
    "stage_c_builder.py": "5f0e25a082118ee37651adc64d0d57228eaf0e7d7496d53f9798997c6762ddeb",
    "stage_c_hashes.json": "910ca60da636f3d888708a4709b95c2ca68969fb16f14a1c3f361d0249865a16",
    "stage_c_method.md": "e2a76a8feef89f0f5207333d4d3feaa67bb67c5b427f84b7844edb37703a713b",
    "stage_c_review.json": "cee15c825f70eee62162cf772f66597dfbfa6f51ef6567780ea161b08a7b59ea",
    "stage_c_statistics.json": "cb42c54dfde3cf88e492c3e40e3fe1f946b0eedeee5e172799d56ae4ffbbcefa",
    "stage_c_validation.json": "019cc61f46284e898615e911c64bd0e2c20c1356ad942c5e87d892163c7e920a"
  },
  "reviewed_gold": "466e0a7a473d5baf7ff0fd75ec9ae3031760649a",
  "reviewed_hashes_sha256": "eccbf9fc7b53907e17e3ef71b64a676c4f8b7649623b5e78857ed85eb825348b",
  "stage_a": "6d26f3c9cce5bc059226a0fe4023dc3ec75832ce",
  "stage_a_readme_restoration": "c43d46607e55d7999ac0277cd196ca9d9e07b9b5",
  "stage_b": "06e816693fed9165467c3afde42298e6dcefe615",
  "stage_b_integrity_sha256": "089bd2fb9be9449dc66966e097d734410030069cbd2a12aefb57610f17fe3ba0"
}
```


## Native/journal status

```json
{
  "journal": {
    "canonical_return_sha256": {
      "construct:A:Q1": "218e2bdccc298695fac73bb5f7673c161e02c37f2f6730fc358180dbe518674e",
      "construct:A:Q2": "8816492105420f02a3739e3d4ea9a0255de732a4a0b4b5d03152267ae42a8e06",
      "construct:A:Q3": "cb23c7555c8a7e4503d9acdb6687bff4bdb0b9dc8ac562a6af2693d636670a8a",
      "construct:A:Q4": "aaa1efe7ca350372b334e9ca8689a349b91f8471b3c19b1b43388f679f52a9ee",
      "construct:A:Q5": "cef05b72d43bd5854566aaa4cdfb52b9e34f749b776df85de5cfff7f911542a8",
      "construct:A:Q6": "1a4a0182b70d3f1c3ab6840f921926b7640aeebc7904808c060793833bbe05a0",
      "construct:B:Q1": "4231214f825479763a60383d5deb9622591031a04bff392cb283500902b368f8",
      "construct:B:Q2": "ed2031c5570ee3375b508d3fc4b31036bb9dc07322805d2a3f3e97cb9f4a5a3b",
      "construct:B:Q3": "2e8f15667afa66fa9d4b165e7edd1b8b771209839750f1781c981fae9489dca9",
      "construct:B:Q4": "f25c1cf478ac7a3a89cf7a210c701e50e82fe374cb6c62762daa17ee2f13c2d1",
      "construct:B:Q5": "e42abfc9c09cedd4936a62b9c4f33c27a7f6aff20c41256c202737742d1f0a19",
      "construct:B:Q6": "47b84c1f4213e244f69581cdb137aa7541acce6ddd0fedb78b02329cd365d7d7",
      "construct:C:Q1": "0d4546dc6023066ac1031aba82643ea8ba93c5f2a662cf404924954d09034272",
      "construct:C:Q2": "4e669b3b434f92ae62ce1ecf048a5ed974f831ca675ca1b08fb3ae31ed3c2b40",
      "construct:C:Q3": "2a0703a81fbc4d3c60d236fcdafe3eb638cfff314d5d494dfb6c8539b46abf38",
      "construct:C:Q4": "0f4377cc4f705c0047ea3cd351b2e1b7557c2d1cf25a0e58e683f0acf1d43020",
      "construct:C:Q5": "86b6d2a55a0d0d897195d36129269b9d8d4d315176cb425ded9540ecc5dea881",
      "construct:C:Q6": "79d713a2040515d3958f2031bc5224d0d87c63ae3d6dad69680d0413b6ee4873",
      "frame:prepare": "4eca825f9d920db9c6e2d19e76ac2a2a9c391cdd737534993e7f6e736afecefb",
      "index-build": "e26b3db74d45e105838fb7cee28ba64dbee1dd6a4d61ec6e43a54672be188ce5",
      "query:Q1": "91d6eea3d42fb6a45dd0b33dc88444fd1b615f6178478f278054e9f3c1311f11",
      "query:Q2": "f8da5a7d796f764ed52a9fdaf450db0b8001a5aa03791291b540f66976a5a346",
      "query:Q3": "e08e3bced2ebf81981a85bf1303601d53a8366413306b8a2e7a3abc888561d3b",
      "query:Q4": "69c6f9176ff66ffe04b8a1665917491a8c41bd56ab89a9cf7d0ff45901bfa1c7",
      "query:Q5": "a78c5bfd1a3f5e2889b58630a803c46f9945e1109f2525a544547e46b17cb149",
      "query:Q6": "7ff0310aab14553bab89cd3d2d8603379038303897065d7e61e7c5d19519cae1",
      "query:reference": "9907d378d4c451e23469a525b9e25ed1f36edb6951ee989149373ec018bcd4cb"
    },
    "chain_sha256": "188bcfedfa95441c9896f4578bdd1f0ab899cb95e27a8d3b009fb63007c839ee",
    "native_retries": 0,
    "pairs": 27,
    "status": "PASS"
  },
  "native": {
    "candidate_counts": {
      "Q1": 216,
      "Q2": 208,
      "Q3": 180,
      "Q4": 343,
      "Q5": 492,
      "Q6": 460
    },
    "classification_application": "PASS",
    "failures": 0,
    "index_builds": 1,
    "native_retries": 0,
    "positive_occurrences": 1899,
    "queries": 6,
    "reference": "UNCHANGED",
    "reference_query_executions": 1,
    "status": "PASS"
  }
}
```


## Final rule result

```json
{
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
}
```
