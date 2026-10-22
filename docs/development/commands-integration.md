# Commands destination integration

This bounded production candidate is derived from main `862bda2d3d1d812893f84ab69691fc068ecce268`, using reviewed
Commands implementation from feature `9437ed1539fd4ad2a9b471ea20fc3de775f74765`. It imports no feature ancestry.
The five capabilities were implemented by Qwen and reviewed by Codex; their original
permanent regressions were independently authored by Codex. Destination selection,
this manifest and the cross-feature composition regression are Codex-authored.

## Original implementation provenance

- Binary stdin: `2490cb7b988d341d93c6c203edb51222aeb4f283`.
- Immutable environment overrides: `b81891ceeafa88d21741ef9b69155180a260e75f`.
- Successful exit codes: `73e5ee07ee490ac6aa9319892585e937fec9a876`.
- Output-limit type and bool validation: `c93e5bf0f50818a9b9648dc315625af394abdee9`.
- Decoded output: `9b667e597f9da160be8a9e08e1e2d24023d6f102`.

## Exact selected feature blobs

All four production Python files, eight selected tests and two package guides
retain their reviewed feature Git blob bytes. The execution guide alone adapts
provenance links to the pinned remote feature revision because those evaluation
artifacts are intentionally absent from main. There are no semantic source
adaptations or package-export changes. This documentation adaptation is Codex-authored.

| Path | Feature Git blob | SHA-256 of UTF-8 source |
| --- | --- | --- |
| `src/devtools/resources/commands/docs/command.md` | `3087563e76d6810248da6491f667863dfc9fb452` | `0a48617c7155bca9db4b9006f37d2e13601cd1d46cc6c611d1b25648b25e9242` |
| `src/devtools/resources/commands/docs/execution.md` | `9c082f5550506b2b02dcf5e5d864c4b0ee2b1d31` | `66676a3637102d9a18f0daf98be6da3952819848ab45ad5e6ccca2e70c6acb28` |
| `src/devtools/resources/commands/docs/overview.md` | `077a164237531e490f0e96e39e01cab0e66dac4d` | `9d6971b7e79f165906485d2d6d11ff8763297e34c076a2b3d27dcd9368f4e614` |
| `src/devtools/resources/commands/execution.py` | `2b81abce1be791e0ec17f944870d8e15d4bc01c6` | `1a76add3410aa1f6013e4fe19a01708833eef886a33ace7119bf153cc61b98c1` |
| `src/devtools/resources/commands/models/command.py` | `6fb4fd8f8e479525a6e2622ab606361fe845c1f2` | `899208f3a7d6a8dfed73dda4d42dbfd279bda8bb587a0fa80510abc49515a05f` |
| `src/devtools/resources/commands/models/output.py` | `cfc2becf7236abd5ed9f33c1b2052676ef68ddee` | `543ead05721b8d977b452f0862ced5a4493338d1ac8f80104a0fd97bd54882c8` |
| `src/devtools/resources/commands/models/result.py` | `5fcba682b24ec828637e0b98bdf94a9687d2292d` | `1ebf20c0c88591042513f5c62b6868449b846f67f329819fb28a8890b55b98ff` |
| `tests/resources/commands/test_decoded_output.py` | `306cbde6bb649703835518acda12083080c4234e` | `136c5ed5a4494ab00dbc5d3c82c75024bc681c1c3117756e4b0e69cbf2bf6779` |
| `tests/resources/commands/test_environment.py` | `91388e9f0644d56ede7cf23e3969c94d1442a45a` | `68b20e65a64e42ddb365fed56e178e71b6207447e4e6357fbc2d5dfce9c8de57` |
| `tests/resources/commands/test_execution.py` | `e7df04e4ad835d9ac80b0d845c39e6791963b441` | `2447c43cbc1769c7aef1b4f1c09b264cc6dc4fcb32789f0c90210ab88b0b1e0a` |
| `tests/resources/commands/test_handle.py` | `229cd4fe5f4d14d91ea702513d6fa93bb11450fe` | `eabeb1e9f0108ca68d9b9d61690987c34d962a3b49213622bdca39a9968f8b87` |
| `tests/resources/commands/test_models.py` | `735bbf73acb339e6db47e152a12121ed1b7e0e1d` | `48d5d74b48aba88e2066030f68b9ae7fbb33e1d6935049dbada2b05386cabb0b` |
| `tests/resources/commands/test_output_policy.py` | `8131f4e4ba9ab248f16e9534357d4cb3ff6ce618` | `567d0681303a1d16070bbed9c8b8290c1927bf3dd05fdbf514495a394cedb07c` |
| `tests/resources/commands/test_stdin.py` | `0e78b83e0132eb162b32dd3d37645fab61c79b9e` | `3768ea47fb97ecf2ee3b20ed948dd903fdb21fc554dea8f4c700f8647c03cfe3` |
| `tests/resources/commands/test_success_exit_codes.py` | `006730c970d208799ce4b11762e7042a992f70ea` | `5d3194cf4ae21c0671d47d5356ac9738c17957ff812274156f7da1d476ee8a6e` |

Additional destination-only files: `tests/resources/commands/test_composition.py`
and this manifest. The new regression exercises binary/empty stdin, inherited and
overridden environments, parent isolation, immutable value equality/hashing,
configured nonzero success, bounded output, decoding and raw process events together.

## Compatibility and dependencies

Main already supplies Commands, managed processes, core paths/time, events and
handles. Existing public exports and original positional Command fields remain
compatible. Appended fields and fluent replacements preserve frozen/slotted values.
Environment mappings are copied and read-only; integer exit-code policies reject
bool before deduplication. Output limits use TypeError for bool/noninteger values
and ValueError for invalid integer ranges. Decoding preserves retained bytes and
truncation facts. Raw exit codes remain independent of success classification.
Concurrent stdin delivery and output draining retain timeout/cancellation behavior.
Cleanup concerns the direct child; no process-group or descendant guarantee is added.
Windows behavior is tested on the destination runtime, not inferred for other hosts.

Excluded: Qwen application and evaluation artifacts, Context/RI/SnapshotDelta changes,
scientific experiments, unrelated feature ancestry and protected promotion policy.
The thirteen preexisting forensic files must remain byte-identical and uncommitted.

## Validation and adoption boundary

Before publication this exact staged tree must pass all Commands regressions,
scoped Ruff/formatting/strict mypy, maintained mypy, layout, whitespace and the
canonical protected development gate with 100% production branch coverage.
Full execution logs and tree/source identities are retained locally under
`.local/commands-integration-20261022/`; publication trailers identify the validated
tree and protected report. Feature validation alone is not destination acceptance.

This ordinary integration branch does not authorize protected-main promotion.
Existing WorkCycle requires a protected grant plus repository protected-target
configuration; the latter is not configured. Those controls are unchanged.
Destination-authorized review/promotion remains separate; do not merge the whole
Qwen feature branch. No new execution or integration machinery is introduced.

## Next Qwen increment

Improve atomic-edit refusal diagnostics narrowly: failing component index, target
path, reason and relevant size/version/match details. Preserve exact admission,
atomic rejection and source scope. This integration does not implement that change.
