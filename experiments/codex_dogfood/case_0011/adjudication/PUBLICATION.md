# Case 0011 primary blind gold publication

## Status

- Stage C primary gold: **COMPLETE**.
- Gold reliability review: **PENDING**.
- Reviewed/reconciled gold: **NOT AVAILABLE**.
- Stage C.5: **NOT BUILT**.
- Stage D: **NOT PERFORMED**.
- U1 effectiveness: **UNKNOWN**.

This is the primary gold, pending independent full reliability review and reconciliation. It is not final architecture-grade truth.

## Provenance and import

The primary gold was created in the sterile blind workspace at `C:\Users\RECOVE~1\AppData\Local\Temp\case_0011_stage_c_sterile_9b8f0f6_hst8rjgq`. The eight independently produced Stage C outputs below were imported byte-for-byte. Source, expected, and destination SHA-256 values matched for every file:

| Artifact | SHA-256 |
| --- | --- |
| `judgments.json` | `71da4b04a8507cc341303129dc70d4cdf4ab0ff4e0a7b700422b287e2793d4a6` |
| `gold_statistics.json` | `811afd089ab1ca8f5cefca81dc588570a53c05410bb9ae1bac8a92a9d87d37fc` |
| `judgments.sha256` | `379bb194e184a19a50d1139d5d458b8420f5fa9a86986d733ffe73a7fd18c604` |
| `METHOD.md` | `23a4a9915fcfa05a20b5c8ed75663abc33472a543a359678184336b183ab48a9` |
| `build_judgments.py` | `eeab3542ba7f5a78ba79f4b554709a87164043bdd5c7f802aef1fdab81945468` |
| `stage_c.py` | `d870c274610d0c65f1b4afcd80323fb3fbc7ddc82ed35cca62c3fa6b5c511068` |
| `test_stage_c.py` | `f1eba0a9bd6e6f8e6e3dfd1ecbdb05b9f90ac05445d8902c0a189fa6f2baa748` |
| `stage_c_pytest.ini` | `dc78dacaaf9d66ff5774b895c4ff3699e9f9f3e07015e43ef06cfb1f8fc53188` |

## Validation and recovery

An isolated temporary validation directory contained exactly the six blind packet inputs and these eight clean outputs (14 files total), with no repository source or Git metadata. Running only `test_stage_c.py` with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` and `--noconftest` passed **20 tests**. Deterministic replay reproduced both gold outputs and their expected hashes; overwrite refusal was verified by the isolated test suite. The standalone Stage C validator passed.

The sterile method records that adjudication first stopped after an unsupported compact-JSON serialization assertion failed. All declared packet integrity checks had passed; no gold existed and no excluded data had been accessed. The assertion was withdrawn, and adjudication resumed in the same blind session. This correction was procedural recovery and did not contaminate the blind gold.

## Review boundary

Stage C-R and reconciliation remain required before architectural promotion. No treatment results were accessed for this publication.
## Mechanically derived necessity views

The frozen artifacts support additional exact set calculations; the gold files were not modified to add them. The 26-address required-resource union collects resources marked REQUIRED somewhere in the matrix. A REQUIRED resource/cell is necessary within at least one acceptable witness alternative for that obligation. It does **not** mean the resource appears in every acceptable alternative or every complete task solution.

A resource is obligation-indispensable here when it is required in every acceptable alternative for that obligation. Counts by obligation: ownership 2; request 3; documentation 5; tests 3; ceiling 1; validation 3; exports 2; frame 7; bytes 1. Task-indispensable resources are the intersection of all 144 sufficient resource unions: 22 addresses. Complete sufficient unions range from 23 to 25 resources.