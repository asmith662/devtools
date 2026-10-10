# PRIMARY BLIND STAGE C — Case 0012

Case: `case-0012`. Task: `case-0012-direct-source-disclosure`.
PRIMARY Stage C = COMPLETE; independent Stage C-R = COMPLETE;
reliability comparison = COMPLETE; outcome = SEVERE_ARCHITECTURE_RELEVANT_DISAGREEMENT;
reviewed/reconciled gold = NOT AVAILABLE;
Stage D = BLOCKED; U2 effectiveness = UNKNOWN; final U2 outcome = NOT_SELECTED.
This publication is not architecture-grade reviewed gold.

## Source authentication and immutable import

Source: `C:\Users\recoveryadmin\CodexSterile\case_0012_stage_c_2cbc95afb120`.
The seven scientific outputs reside unchanged in [primary/](primary/).
[IMPORT.json](IMPORT.json) records original packet physical hashes, the four
sealed packet scopes, native source provenance and every imported SHA-256.
The frame identity and other exact case/task/frame bindings remain in the sealed
review; they have not been renamed or reinterpreted.

The completed source was authenticated by known-file physical hashes and
`python -B stage_c_builder.py --verify`, which passed exact deterministic byte
reconstruction and original-file preservation. The initial five-file validator
was not run in the completed PRIMARY directory: its exact whitelist applies to
an initial packet, not a completed adjudication directory.
Source, destination, staged Git blob content and committed Git blob content must
all have the same SHA-256 recorded in IMPORT.json. Git object IDs are not these
physical hashes. No formatter, regeneration or newline normalization applies to
the immutable import. The source operational `.local/` is excluded.

## Published blindness attestation

The sealed `stage_c_review.json` explicitly attests NO access to repository
checkout, Git history, parent/sibling workspace files, retrieval queries,
rankings, scores, hint/routing artifacts, experiment arms, treatment results,
acquisition costs, prior gold, confirmation data, reserve data and external web
information. Its exact attestation and scope note remain in the imported review;
IMPORT.json also retains the attestation fields. Blindness is based on that
published assertion, not independently inferred from absence of files.

This repository import session is not the blind reviewer. Its repository access
does not retroactively alter the sealed PRIMARY adjudication. No Stage B result
or confirmation/reserve artifact was accessed for this publication. No treatment
join or effectiveness analysis was performed.

## Sealed statistics

| Measure | PRIMARY value |
| --- | --- |
| Resources / applicable obligations / cells | 531 / 9 / 4,779 |
| REQUIRED / HELPFUL_ONLY / UNNECESSARY / UNRESOLVED | 28 / 49 / 4,702 / 0 |
| Required units / required-resource union | 52 / 20 |
| Alternatives / complete task combinations | 14 / 16 |
| Distinct sufficient resource unions / unit unions | 12 / 1 |
| Sufficient resource range / unit range | 17–20 / 52–52 |
| Task-indispensable resources / units | 16 / 52 |
| Task gap / repository-information gap | NONE / NONE |
| Interpretation limitations | 4 |
| Unresolved resource judgments | 0 |
| Preserved API/cardinality ambiguity | 1 |

These values report the sealed PRIMARY publication without reinterpretation.

## Preserved semantic tensions

The following are PRIMARY propositions for later independent comparison, not
import-time errors or disagreement judgments. The future reviewer must not
receive this list.

```text
tests:
    0 REQUIRED resource cells
    10 required units
    resource-empty task-backed alternative

validation:
    scripts/validate_development.py named by task
    but absent from PRIMARY required-resource union

source:
    4 alternatives

integrity:
    2 alternatives

materialization:
    2 alternatives

decorators:
    native declaration ranges exclude preceding decorators;
    additional faithful range/provenance work required

API/cardinality:
    option names and single-declaration versus caller-approved grouped-match
    shape remain ambiguous
```

## Independent-review boundary

[CR_PREPARATION.json](CR_PREPARATION.json) authenticates the new five-file sterile
workspace. [C_R_OPERATOR.md](C_R_OPERATOR.md) contains operator instructions and
the independent prompt outside that workspace. The pre-comparison criteria are
frozen in [reliability/PROTOCOL.md](reliability/PROTOCOL.md) and its deterministic
JSON source. The completed independent source is now imported unchanged in
[independent/](independent/); [INDEPENDENT_IMPORT.json](INDEPENDENT_IMPORT.json)
authenticates its seven outputs and complete blindness attestation.
[RELIABILITY_REVIEW.md](reliability/RELIABILITY_REVIEW.md) reports the executed
unchanged protocol, all 106 label differences and 19 REQUIRED-membership
differences. Neither source establishes truth. The severe gate requires
treatment-blind reconciliation; [PREPARATION.json](reliability/reconciliation/PREPARATION.json)
records the neutral packet and stable sterile workspace. No reviewer was started
and no reconciliation occurred. Stage D remains blocked. U2 effectiveness UNKNOWN;
final U2 outcome NOT_SELECTED; U3 FUTURE; R1.7 RETAINED; R2 true BM25F MANDATORY.
