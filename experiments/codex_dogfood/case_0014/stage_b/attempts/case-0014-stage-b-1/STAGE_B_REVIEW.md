# Case 0014 Stage B mechanical review

GOLD = ABSENT

EFFECTIVENESS = UNKNOWN

R1.7 OUTCOME = NOT_SELECTED

RANK MOVEMENT IS NOT EFFECTIVENESS EVIDENCE WITHOUT GOLD

SEARCH_POLICY_FAILURE = NOT_ASSESSED

## Exact task

Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.

O1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.

O2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.

O3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.

O4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.

O5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.

O6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.

## Complete frozen obligations, queries, classifications and multipliers

See unchanged [Stage A](../../../STAGE_A_REVIEW.md) and trace.json's stage_a_protocol.

## Exactly-once summary

```json
{
  "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
  "arm_construction_records": 18,
  "candidate_counts": {
    "Q1": 216,
    "Q2": 208,
    "Q3": 180,
    "Q4": 343,
    "Q5": 492,
    "Q6": 460
  },
  "candidate_identity": "A=B=C; PASS",
  "effectiveness": "UNKNOWN",
  "execution": "case-0014-stage-b-1",
  "gold": "ABSENT",
  "index_builds": 1,
  "journal_pairs": 27,
  "native_statistics": "UNCHANGED",
  "obligation_query_executions": {
    "Q1": 1,
    "Q2": 1,
    "Q3": 1,
    "Q4": 1,
    "Q5": 1,
    "Q6": 1
  },
  "outcome": "NOT_SELECTED",
  "reference_candidate_count": 515,
  "reference_query_executions": 1,
  "role_attribution": "PASS",
  "stage_b": "CAPTURED",
  "total_candidate_occurrences": 1899
}
```

## Candidate counts and top-K pair inversions

| Query | Candidates | B-A K10/20/50 | C-A K10/20/50 | C-B K10/20/50 |
|---|---:|---|---|---|
| Q1 | 216 | 1/10/162 | 1/10/172 | 0/0/11 |
| Q2 | 208 | 14/68/130 | 14/68/154 | 0/0/23 |
| Q3 | 180 | 9/44/101 | 9/48/125 | 0/2/24 |
| Q4 | 343 | 12/33/105 | 12/33/142 | 0/0/34 |
| Q5 | 492 | 22/166/694 | 26/176/738 | 3/6/46 |
| Q6 | 460 | 53/113/371 | 53/113/385 | 0/0/26 |

Pair inversions count order reversals inside the union of both top-K sets; entered/exited crossings are separately retained. Every full arm ranking/contribution is in the compressed arm artifacts; trace.json retains every movement, inversion set, role/channel aggregate and per-document attribution. Native contributions, IDF/statistics and reference are captured separately. Binary-rational attribution discloses frozen floating summation residuals without changing scores.

## Captured cost accounting

```json
{
  "accounting": "All top-level native times single-run; no child, wall, publication or durability double counting; no timing reruns",
  "arms": {
    "A": {
      "charged_ns": 12226659800,
      "construction_ns": 1747263700,
      "queries": {
        "Q1": 198542100,
        "Q2": 197955900,
        "Q3": 174323500,
        "Q4": 298690600,
        "Q5": 450464500,
        "Q6": 427287100
      }
    },
    "B": {
      "charged_ns": 12229738600,
      "construction_ns": 1750342500,
      "queries": {
        "Q1": 199135700,
        "Q2": 197941100,
        "Q3": 170870400,
        "Q4": 305373000,
        "Q5": 445495900,
        "Q6": 431526400
      }
    },
    "C": {
      "charged_ns": 12185305200,
      "construction_ns": 1705909100,
      "queries": {
        "Q1": 197315400,
        "Q2": 189955000,
        "Q3": 173854900,
        "Q4": 304517300,
        "Q5": 424292600,
        "Q6": 415973900
      }
    }
  },
  "classification": "Frozen in Stage A; restoration verification separately reported, not mechanism charged",
  "publication_durability": {
    "accounting": "Non-mechanism publication/durability and descriptive wall only; no double counting",
    "capture_wall_ns": 131452368200,
    "classification_restoration_verification_ns": 24848500,
    "journal_publication_durability_ns": 115373859000
  },
  "reference": "Separate unchanged lane; not mechanism charged",
  "shared": {
    "canonical_index_ns": 2281626000,
    "frame_preparation_ns": 8101636000,
    "obligation_native_acquisition_ns": 96134100,
    "reference_native_acquisition_ns": 88977300
  },
  "shared_charged_equally_ns": 10479396100
}
```

No gold-dependent analysis, witness calculation, decision-rule evaluation or outcome selection has occurred.
