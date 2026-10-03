# Case 0006 independent blind Stage C checkpoint

Evidence universe: only `blind_manifest.json` and `blind_resources.json.gz`.
The complete frozen archive, rather than the current checkout, supplies every
source, test, documentation and configuration observation. The starting checkout
was clean `main` at `e076632a5e38d9d598c0fc109a12b52b424ecf22`.

## Frozen judgment

`judgments.json` retains exact Case/task/repository/snapshot/frame identities,
the unchanged ten obligations and anchors, selected information units with frozen
resource identities and line ranges, applicability, obligation-relative decisions,
ALL/ANY witness alternatives, necessity review, inferability, gaps and limitations.
`judgments.sha256` identifies the complete canonical JSON bytes. The internal
`payload_sha256` hashes the canonical document with that field omitted, avoiding
a self-referential file digest.
Case-local Git attributes preserve the frozen judgment and digest bytes across
checkout newline conversion.

All ten obligations are APPLICABLE. Package applicability follows affirmative
public imports and explicit `__all__` conventions, not initializer existence.

| Obligation | REQUIRED units across alternatives | HELPFUL_ONLY resources | Alternatives |
| --- | ---: | ---: | ---: |
| hypothesis-records | 4 | 1 | 1 |
| member-complementarity | 2 | 2 | 1 |
| generated-integration | 4 | 3 | 1 |
| accepted-promotion | 5 | 1 | 1 |
| assessment-readiness | 3 | 2 | 1 |
| provenance-frame | 3 | 5 | 1 |
| package-integration | 3 | 1 | 2 |
| tests | 4 | 3 | 2 |
| documentation | 4 | 4 | 1 |
| validation | 1 | 3 | 1 |

There are 22 distinct REQUIRED units, 33 obligation-relative REQUIRED unit
judgments, and 18 unique REQUIRED resource identities across all alternatives.
Every REQUIRED unit is INFERABLE_AT_START. INHERENT_DISCOVERY count is zero;
there are no later-observation prerequisites. No unresolved judgments or
applicability decisions remain. No obvious mandatory task-interpretation gap
was found. The historical implementation ledger is absent from the eligible
frame; its contents and possible historical update cannot be adjudicated here.

Package alternatives require the kernel facade plus either association or
generation facade. Test alternatives require candidate validation and readiness
contracts plus either the selected association or generation test example.
The other eight obligations each have one complementary complete alternative.
Exact members and reasons are retained in the JSON. The four combinations of
complete alternatives each contain 20 distinct units in 16 resources.

The safe default represents all 5,310 resource/obligation cells: 28 contain
REQUIRED units, 25 are HELPFUL_ONLY, and 5,257 are UNNECESSARY. A REQUIRED resource
cell means it contains selected required information in an acceptable alternative;
it does not make its entire content mandatory, or require reading every competing
alternative. Exact coverage diagnostics report expected/observed resource counts
531/531 and cell counts 5,310/5,310. Duplicate expected, duplicate observed,
missing and unexpected identities are empty for both frames.

## Method and replay

- `inspect_blind.py`: exact resource enumeration and selected frozen text reads.
- `author_judgments.py`: manually authored semantic units, necessity judgments
  and alternatives. No production imports or task-relative acquisition.
- `freeze_judgments.py`: pinned byte digests, packet/schema identities, semantic
  content and snapshot digest verification, target/range/alternative validation,
  applicability/inferability/gap validation, structured forbidden-field rejection,
  exact coverage expansion and deterministic serialization. `--freeze` refuses
  overwrite; invocation without it verifies the committed freeze in memory.
- `test_freeze.py` and `pytest.ini`: isolated integrity tests with production
  coverage disabled, no repository conftest and no current target imports.

Commands run from the repository root:

```text
python experiments/codex_dogfood/case_0006/adjudication/freeze_judgments.py
.venv\Scripts\python.exe -m pytest -c experiments/codex_dogfood/case_0006/adjudication/pytest.ini --noconftest --no-cov experiments/codex_dogfood/case_0006/adjudication/test_freeze.py -q
.venv\Scripts\ruff.exe check --isolated --select E,F,I,UP,B,SIM --ignore E501 experiments/codex_dogfood/case_0006/adjudication/inspect_blind.py experiments/codex_dogfood/case_0006/adjudication/author_judgments.py experiments/codex_dogfood/case_0006/adjudication/freeze_judgments.py experiments/codex_dogfood/case_0006/adjudication/test_freeze.py
.venv\Scripts\ruff.exe format --isolated --check experiments/codex_dogfood/case_0006/adjudication/inspect_blind.py experiments/codex_dogfood/case_0006/adjudication/author_judgments.py experiments/codex_dogfood/case_0006/adjudication/freeze_judgments.py experiments/codex_dogfood/case_0006/adjudication/test_freeze.py
git diff --check
git diff --cached --check
```

Results: deterministic replay passed; 13 focused tests passed; scoped isolated
Ruff and formatting passed. The selected lint gate permits long judgment prose
strings via E501 exclusion. These are Case-support checks; the protected
production test suite was not executed or imported during blind adjudication.

## Blindness and stop boundary

Only the two authorized preexisting Case inputs were accessed. Other Case 0006
artifacts, Retrieval results, lexical treatment, role treatment, grounding
treatment/results, generation treatment/results, recovery/capture history,
current target implementation and confirmation outcomes were not accessed.
No Stage D comparison or effectiveness analysis was performed. Production source
was not changed. Confirmation remains sealed. This checkpoint is committed before
any unblinding; no push is authorized.

Next step: Stage D joined analysis comparing global lexical, own-obligation
lexical, routed lexical and bounded generated candidate surface against
independently adjudicated REQUIRED witness resources and structures.
