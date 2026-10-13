# Stage C import / Stage D completion validation

All checks passed. This operational test receipt supplements the immutable scientific result seals.

```json
{
  "adversarial_scope": [
    "case/frame/obligation/target/predecessor/source identity",
    "A rank and source<target",
    "self edge",
    "Reference provenance",
    "gold label and primary hash",
    "duplicate/missing gold cell/pair",
    "predecessor rank",
    "classification/category arithmetic",
    "cohort aggregation",
    "Stage B completion proof",
    "output integrity",
    "overwrite refusal"
  ],
  "cached_diff_check": "PASS; checked again at checkpoint staging",
  "combined_test_command": "uv run pytest --no-cov experiments/structural_discrimination/stage_d/test_analysis.py experiments/structural_discrimination/stage_b/test_capture.py experiments/structural_discrimination/stage_c/test_import.py experiments/structural_discrimination/stage_c/test_packet.py experiments/structural_discrimination/test_protocol.py experiments/codex_dogfood/verification/test_proof.py -q",
  "combined_tests_passed": 121,
  "diff_check": "PASS",
  "documentation_impact": "Experiment-owned import/analyzer/status surfaces, documentation map and roadmap updated; no package API/architecture/backlog promotion or prior-result rewrite; ledger remains historical",
  "excluded": [
    "unrelated Graph-3 full fixtures",
    "historical Case 0016 deep replay",
    "historical child implementations/paths/diffs",
    "confirmation/reserve",
    "another adjudication",
    "live model/Docker"
  ],
  "formatter": "PASS same scope",
  "latest_stage_d_tests_passed": 42,
  "mypy": "PASS strict same scope",
  "prepublication_formatting_correction": "Extra blank line at trace EOF rejected by staged diff check; renderer corrected, unpublished build retained only under ignored .local, rebuilt outputs verified; no scientific input/label/treatment/category changed",
  "production_branch_coverage_percent": 100,
  "protected_command": "uv run python scripts/validate_development.py",
  "protected_passed": 1588,
  "protected_skipped": 2,
  "repeated_reconstruction": "PASS; fresh calculate twice, exact artifact equality; acquisition functions forbidden by test",
  "ruff": "PASS scoped Stage D and Stage C import tooling; untouched primary artifacts excluded",
  "scope": "Authorized development diagnostic; no live services or semantic reviewer",
  "separate_process_verification": "PASS; uv run python -m experiments.structural_discrimination.stage_d.analyze verify",
  "source_implementation_sha256": {
    "experiments/structural_discrimination/decision.py": "7af8ad9fff1a951039e265e6f5453223184f0500606ca6766728aaf26f34951e",
    "experiments/structural_discrimination/stage_c/import_gold.py": "a125166f5227852d5a7ce7424cd66794aa7a4e6ffca4edf7c26a8d0465386e5e",
    "experiments/structural_discrimination/stage_d/.gitattributes": "a79691a93b46e49ce460c26ef22afcc03d6eca1e63bf2edbc20e96159510f6c9",
    "experiments/structural_discrimination/stage_d/README.md": "7ac03630e337ed6d57fe679d2c3b83995d1b630986d1fff87f4e5f078f7f29b4",
    "experiments/structural_discrimination/stage_d/__init__.py": "89506211fff4a9011eaf87d6ed425b25a46cdca8051e62059df897c5fca5e497",
    "experiments/structural_discrimination/stage_d/analyze.py": "0f10e677c6e137a93460f4a2757f10f94082a27dc3fb201ecf89247b574977d0",
    "experiments/structural_discrimination/stage_d/join.py": "9c918010c0ce52d966281684bba7e9fb0250717112f73aec7571392ff7a625da",
    "experiments/structural_discrimination/stage_d/reporting.py": "583edf1fe53f8a6c1d46737f2e2dd281a52e7e765354ea92599878eeabaa01d8",
    "experiments/structural_discrimination/stage_d/test_analysis.py": "febb3b41a8c44853a6ff1b6dfb488ca8ec834737a6e0d6d5fbfd56d72809b9ea"
  },
  "stage_b_normal_sealed_verification": "PASS all three; 0 native archive decodes, 0 deep correspondence executions",
  "stage_c_import_tests_passed": 13,
  "status": "PASS"
}
```
