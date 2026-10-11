# Case 0014 prospective trace

R1.7 CURRENT; Stage B NOT EXECUTED; effectiveness UNKNOWN.

## Exact task

Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.

O1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.

O2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.

O3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.

O4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.

O5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.

O6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.

## Hypothesis and scientific boundary

```json
{
  "boundary": "Only query-term contribution multipliers differ. Whole exact text, canonical tokens, query text/identities, statistics, k1/b, filename behavior, candidate membership and native tie-break are invariant. No feature implementation, expansion, reranking, routing, BM25F or sequential search.",
  "hypothesis": "Deterministic task-side term importance can improve necessary-evidence ranking discrimination while query text, analyzed identities, native representation/statistics, positive candidates and fallback remain unchanged. More weighting is not presumed better."
}
```

## Selection record

# Prospective task selection

SELECTION_CRITERIA.json was written first, before task, queries or frame
observation. Selection used existing contracts and future capability pressure,
never rankings, document frequencies, prior-case gold or treatment outcomes.

Candidates considered:

| Candidate | Decision | Reason |
|---|---|---|
| Repository snapshot delta inspection | Rejected | Snapshot/change protocol pressure requires broader semantic design; too close to earlier Context tasks. |
| Advanced provider streaming (B-0046 pressure) | Rejected | Consumer/lifecycle ownership and incomplete integration requirements would dominate this small query-side experiment. |
| General coding-context continuation (B-0002) | Rejected | Canonical backlog concern is broad, with unresolved architecture; it is not a bounded implementable feature. |
| Completed command-result diagnostic renderer | Selected | Existing commands docs explicitly leave text decoding as future work; immutable completed results give a narrow pure presentation seam with nontrivial byte, retention, event-loss and failure contracts. |

No backlog item supplied a smaller direct feature without deciding unresolved
architecture. This task is a proposed future resource-commands capability, not
implementation authorization. Selection inspections: commands models/result.py,
models/output.py, errors.py, public exports, docs/{overview,command,execution,events}.md
and tests/resources/commands/test_models.py; architecture taxonomy/documentation
map and B-0002/B-0046 pressure. The feature spans six mandatory obligations and
mixes literal symbols/paths, domain facts and ordinary work verbs naturally.

The broad eligible source/test/doc/config universe is independent of the task.
Prior experiment material and whole resources carrying prior-case markers are
excluded by a frozen general leakage rule, never by relevance or term frequency.
Original retained resource text is unmodified. No prospective rankings were
available or used. The feature is not implemented by this checkpoint.

## Criteria frozen before authoring

```json
{
  "criteria": [
    "New realistic future devtools capability; inspect current contracts without implementing it",
    "At least five mandatory obligations spanning behavior, boundary safety, integration, tests and documentation",
    "Different subsystem and feature from Cases 0011, 0012 and 0013",
    "Natural mixture of explicit names or paths, domain-semantic facts and ordinary work verbs",
    "Nontrivial current contract evidence; lexical ranking can plausibly affect inspection",
    "No task selection based on retrieval, term document frequency, gold or treatment results",
    "Prefer a canonical backlog item only when it supports a bounded feature without deciding unresolved architecture",
    "Reject candidates requiring unapproved lifecycle, authority, durable schema or package ownership changes",
    "Broad query-independent committed source/test/doc/config frame with prior experiment evidence excluded"
  ],
  "excluded_selection_inputs": [
    "Case 0014 rankings or scores",
    "Case 0014 document frequencies or yields",
    "prior-case required resource labels or witnesses",
    "confirmation/reserve data"
  ],
  "schema": "case-0014-selection-criteria-v1",
  "sequence": "Written before final task authoring, query authoring or frame observation",
  "source_head": "3aafd897a6a46a201180dc51dbef5e5201669a58"
}
```

## Existing canonical scorer and weighting equation

```json
{
  "analysis": "Unicode regex \\w+ spans, casefold; distinct normalized terms in first encounter order; duplicate observations retained but query term frequency does not score",
  "arithmetic": "Python float with native channel summation order; no regrouping; retain raw native evidence and float.hex values for lossless reconstruction",
  "b": 0.75,
  "candidate_bound": "Full universe: maximum_results >= frozen document count; all positive content OR filename matches",
  "canonical_sources": [
    "src/devtools/context/retrieval/lexical/analysis.py",
    "src/devtools/context/retrieval/lexical/bm25.py",
    "src/devtools/context/retrieval/lexical/filename.py",
    "src/devtools/context/retrieval/lexical/scoring.py",
    "src/devtools/context/retrieval/lexical/statistics.py",
    "src/devtools/context/retrieval/lexical/index.py"
  ],
  "equation": "sum(native_content_term * query_multiplier) + 0.25 * sum(native_filename_term * query_multiplier)",
  "filename": "Independent native filename-stem BM25 statistics/contributions; fixed additive weight 0.25; inseparable canonical baseline contract, not BM25F",
  "idf": "ln(1 + (N - df + 0.5)/(df + 0.5))",
  "k1": 1.2,
  "term_contribution": "idf * tf * (k1+1) / (tf + k1*(1-b+b*document_length/average_document_length)); tf is document frequency of the term within one document",
  "tie_break": "Original native document collection position after descending treatment score, not previous rank"
}
```

## Complete term roles, lexicon, multipliers and arms

```json
{
  "arms": {
    "A": "CANONICAL_BM25",
    "B": "ANCHOR_EMPHASIS",
    "C": "FULL_QUERY_TERM_DISCRIMINATION"
  },
  "taxonomy": {
    "EXPLICIT_ANCHOR": "Native token from exact task-marked literal intentionally copied into query; anchor occurrence dominates duplicate neutral occurrences",
    "GENERIC_OPERATION": "Member of the small frozen repository-independent work-verb lexicon unless anchored",
    "SEMANTIC": "Intentionally authored obligation-specific fact term, neutral by default",
    "generic_lexicon": [
      "add",
      "build",
      "create",
      "implement",
      "update"
    ],
    "lexicon_rationale": "Five repository-independent work verbs; no domain nouns or test terminology."
  },
  "weight_rationale": "2 emphasizes a task-marked literal; 1 retains neutral semantic evidence; 0.5 challenges dilution by five generic work verbs. Positive binary-exact discrete values, not optimized, not based on corpus statistics. Three roles/arms isolate anchor emphasis from generic attenuation.",
  "weights": {
    "A": {
      "EXPLICIT_ANCHOR": 1,
      "GENERIC_OPERATION": 1,
      "SEMANTIC": 1
    },
    "B": {
      "EXPLICIT_ANCHOR": 2,
      "GENERIC_OPERATION": 1,
      "SEMANTIC": 1
    },
    "C": {
      "EXPLICIT_ANCHOR": 2,
      "GENERIC_OPERATION": 0.5,
      "SEMANTIC": 1
    }
  }
}
```

## Requirement matrix

| Requirement | Mandatory obligation | Query | Title |
|---|---|---|---|
| O1 | O1 | Q1 | Completed-result contract and pure rendering |
| O2 | O2 | Q2 | Byte-preserving UTF-8 diagnostic decoding |
| O3 | O3 | Q3 | Display bounds versus retention bounds |
| O4 | O4 | Q4 | Event loss and execution-failure boundary |
| O5 | O5 | Q5 | Public API and domain boundary |
| O6 | O6 | Q6 | Controlled tests, documentation and protected validation |

## Every frozen query and analyzed term

All spans are half-open character offsets. Duplicate observations remain; distinct terms score once. Each term is scoped by its enclosing query/obligation identity.

### Q1 / O1

Exact query:

```text
implement Command CommandResult exit_code duration succeeded failed structured executable arguments nonzero completed result pure operation
```

Task clause [0, 418):

Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.

O1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.


| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `implement` | [0,9)=implement | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `command` | [10,17)=Command | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `commandresult` | [18,31)=CommandResult | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `exit_code` | [32,41)=exit_code | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `duration` | [42,50)=duration | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `succeeded` | [51,60)=succeeded | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `failed` | [61,67)=failed | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `structured` | [68,78)=structured | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `executable` | [79,89)=executable | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `arguments` | [90,99)=arguments | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `nonzero` | [100,107)=nonzero | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `completed` | [108,117)=completed | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `result` | [118,124)=result | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `pure` | [125,129)=pure | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `operation` | [130,139)=operation | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 17,
    "query_start": 10,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 175,
        "start": 168
      }
    }
  },
  {
    "query_end": 31,
    "query_start": 18,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 102,
        "start": 89
      }
    }
  },
  {
    "query_end": 41,
    "query_start": 32,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 213,
        "start": 204
      }
    }
  },
  {
    "query_end": 50,
    "query_start": 42,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 225,
        "start": 217
      }
    }
  },
  {
    "query_end": 60,
    "query_start": 51,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 242,
        "start": 233
      }
    }
  },
  {
    "query_end": 67,
    "query_start": 61,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 251,
        "start": 245
      }
    }
  }
]
```

### Q2 / O2

Exact query:

```text
implement stdout stderr UTF-8 diagnostic excerpts original bytes replacement decoding invalid incomplete loss
```

Task clause [418, 703):

O2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.


| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `implement` | [0,9)=implement | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `stdout` | [10,16)=stdout | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `stderr` | [17,23)=stderr | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `utf` | [24,27)=UTF | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `8` | [28,29)=8 | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `diagnostic` | [30,40)=diagnostic | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `excerpts` | [41,49)=excerpts | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `original` | [50,58)=original | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `bytes` | [59,64)=bytes | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `replacement` | [65,76)=replacement | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `decoding` | [77,85)=decoding | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `invalid` | [86,93)=invalid | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `incomplete` | [94,104)=incomplete | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `loss` | [105,109)=loss | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 16,
    "query_start": 10,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 436,
        "start": 430
      }
    }
  },
  {
    "query_end": 23,
    "query_start": 17,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 449,
        "start": 443
      }
    }
  }
]
```

### Q3 / O3

Exact query:

```text
add CommandOutputPolicy stdout_truncated stderr_truncated nonnegative per-stream character display limit leading prefix byte retention zero omitted output
```

Task clause [703, 1081):

O3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.


| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `add` | [0,3)=add | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `commandoutputpolicy` | [4,23)=CommandOutputPolicy | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `stdout_truncated` | [24,40)=stdout_truncated | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `stderr_truncated` | [41,57)=stderr_truncated | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `nonnegative` | [58,69)=nonnegative | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `per` | [70,73)=per | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `stream` | [74,80)=stream | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `character` | [81,90)=character | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `display` | [91,98)=display | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `limit` | [99,104)=limit | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `leading` | [105,112)=leading | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `prefix` | [113,119)=prefix | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `byte` | [120,124)=byte | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `retention` | [125,134)=retention | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `zero` | [135,139)=zero | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `omitted` | [140,147)=omitted | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `output` | [148,154)=output | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 23,
    "query_start": 4,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 948,
        "start": 929
      }
    }
  },
  {
    "query_end": 40,
    "query_start": 24,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 991,
        "start": 975
      }
    }
  },
  {
    "query_end": 57,
    "query_start": 41,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1010,
        "start": 994
      }
    }
  }
]
```

### Q4 / O4

Exact query:

```text
implement events_dropped CommandResult output truncation event interleaving timeout cancellation executable-not-found completed result
```

Task clause [1081, 1377):

O4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.


| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `implement` | [0,9)=implement | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `events_dropped` | [10,24)=events_dropped | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `commandresult` | [25,38)=CommandResult | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `output` | [39,45)=output | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `truncation` | [46,56)=truncation | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `event` | [57,62)=event | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `interleaving` | [63,75)=interleaving | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `timeout` | [76,83)=timeout | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `cancellation` | [84,96)=cancellation | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `executable` | [97,107)=executable | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `not` | [108,111)=not | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `found` | [112,117)=found | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `completed` | [118,127)=completed | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `result` | [128,134)=result | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 24,
    "query_start": 10,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1121,
        "start": 1107
      }
    }
  },
  {
    "query_end": 38,
    "query_start": 25,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1256,
        "start": 1243
      }
    }
  }
]
```

### Q5 / O5

Exact query:

```text
create src/devtools/resources/commands/__init__.py public API deterministic immutable presentation decoding display policy logging Evidence Trace subprocess persistence secret redaction
```

Task clause [1377, 1716):

O5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.


| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `create` | [0,6)=create | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `src` | [7,10)=src | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `devtools` | [11,19)=devtools | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `resources` | [20,29)=resources | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `commands` | [30,38)=commands | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `__init__` | [39,47)=__init__ | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `py` | [48,50)=py | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `public` | [51,57)=public | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `api` | [58,61)=API | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `deterministic` | [62,75)=deterministic | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `immutable` | [76,85)=immutable | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `presentation` | [86,98)=presentation | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `decoding` | [99,107)=decoding | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `display` | [108,115)=display | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `policy` | [116,122)=policy | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `logging` | [123,130)=logging | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `evidence` | [131,139)=Evidence | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `trace` | [140,145)=Trace | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `subprocess` | [146,156)=subprocess | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `persistence` | [157,168)=persistence | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `secret` | [169,175)=secret | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `redaction` | [176,185)=redaction | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 50,
    "query_start": 7,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1469,
        "start": 1426
      }
    }
  }
]
```

### Q6 / O6

Exact query:

```text
update tests/resources/commands/ src/devtools/resources/commands/docs/ docs/development/validation.md controlled tests success nonzero UTF-8 invalid incomplete zero default custom bounds flags event loss immutability protected validation
```

Task clause [1716, 2155):

O6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.

| Analyzed term | Exact query spans | Role | A | B | C | Classification provenance |
|---|---|---|---:|---:|---:|---|
| `update` | [0,6)=update | GENERIC_OPERATION | 1.0 | 1.0 | 0.5 | Frozen repository-independent five-verb lexicon |
| `tests` | [7,12)=tests, [113,118)=tests | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `resources` | [13,22)=resources, [46,55)=resources | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `commands` | [23,31)=commands, [56,64)=commands | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `src` | [33,36)=src | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `devtools` | [37,45)=devtools | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `docs` | [65,69)=docs, [71,75)=docs | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `development` | [76,87)=development | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `validation` | [88,98)=validation, [227,237)=validation | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `md` | [99,101)=md | EXPLICIT_ANCHOR | 1.0 | 2.0 | 2.0 | Exact task-marked literal copied into query; anchor precedence across repeated observations |
| `controlled` | [102,112)=controlled | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `success` | [119,126)=success | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `nonzero` | [127,134)=nonzero | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `utf` | [135,138)=UTF | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `8` | [139,140)=8 | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `invalid` | [141,148)=invalid | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `incomplete` | [149,159)=incomplete | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `zero` | [160,164)=zero | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `default` | [165,172)=default | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `custom` | [173,179)=custom | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `bounds` | [180,186)=bounds | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `flags` | [187,192)=flags | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `event` | [193,198)=event | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `loss` | [199,203)=loss | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `immutability` | [204,216)=immutability | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |
| `protected` | [217,226)=protected | SEMANTIC | 1.0 | 1.0 | 1.0 | Intentionally authored obligation fact term from the cited task clause; no corpus evidence |

Literal copy provenance:

```json
[
  {
    "query_end": 32,
    "query_start": 7,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1773,
        "start": 1748
      }
    }
  },
  {
    "query_end": 70,
    "query_start": 33,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 1856,
        "start": 1819
      }
    }
  },
  {
    "query_end": 101,
    "query_start": 71,
    "task_provenance": {
      "explanation": "Verbatim task-marked literal",
      "source_identity": {
        "value": "case-0014-command-result-diagnostics-v1"
      },
      "span": {
        "end": 2152,
        "start": 2122
      }
    }
  }
]
```

## Whole-task canonical safety/reference lane

```json
{
  "analysis": {
    "observations": [
      {
        "encounter_ordinal": 0,
        "end": 3,
        "normalized_term": "add",
        "observed_text": "Add",
        "start": 0
      },
      {
        "encounter_ordinal": 1,
        "end": 6,
        "normalized_term": "an",
        "observed_text": "an",
        "start": 4
      },
      {
        "encounter_ordinal": 2,
        "end": 10,
        "normalized_term": "opt",
        "observed_text": "opt",
        "start": 7
      },
      {
        "encounter_ordinal": 3,
        "end": 13,
        "normalized_term": "in",
        "observed_text": "in",
        "start": 11
      },
      {
        "encounter_ordinal": 4,
        "end": 27,
        "normalized_term": "deterministic",
        "observed_text": "deterministic",
        "start": 14
      },
      {
        "encounter_ordinal": 5,
        "end": 33,
        "normalized_term": "human",
        "observed_text": "human",
        "start": 28
      },
      {
        "encounter_ordinal": 6,
        "end": 42,
        "normalized_term": "readable",
        "observed_text": "readable",
        "start": 34
      },
      {
        "encounter_ordinal": 7,
        "end": 53,
        "normalized_term": "diagnostic",
        "observed_text": "diagnostic",
        "start": 43
      },
      {
        "encounter_ordinal": 8,
        "end": 62,
        "normalized_term": "renderer",
        "observed_text": "renderer",
        "start": 54
      },
      {
        "encounter_ordinal": 9,
        "end": 66,
        "normalized_term": "for",
        "observed_text": "for",
        "start": 63
      },
      {
        "encounter_ordinal": 10,
        "end": 69,
        "normalized_term": "an",
        "observed_text": "an",
        "start": 67
      },
      {
        "encounter_ordinal": 11,
        "end": 77,
        "normalized_term": "already",
        "observed_text": "already",
        "start": 70
      },
      {
        "encounter_ordinal": 12,
        "end": 87,
        "normalized_term": "completed",
        "observed_text": "completed",
        "start": 78
      },
      {
        "encounter_ordinal": 13,
        "end": 102,
        "normalized_term": "commandresult",
        "observed_text": "CommandResult",
        "start": 89
      },
      {
        "encounter_ordinal": 14,
        "end": 106,
        "normalized_term": "in",
        "observed_text": "in",
        "start": 104
      },
      {
        "encounter_ordinal": 15,
        "end": 116,
        "normalized_term": "devtools",
        "observed_text": "devtools",
        "start": 108
      },
      {
        "encounter_ordinal": 16,
        "end": 126,
        "normalized_term": "resources",
        "observed_text": "resources",
        "start": 117
      },
      {
        "encounter_ordinal": 17,
        "end": 135,
        "normalized_term": "commands",
        "observed_text": "commands",
        "start": 127
      },
      {
        "encounter_ordinal": 18,
        "end": 141,
        "normalized_term": "o1",
        "observed_text": "O1",
        "start": 139
      },
      {
        "encounter_ordinal": 19,
        "end": 151,
        "normalized_term": "preserve",
        "observed_text": "Preserve",
        "start": 143
      },
      {
        "encounter_ordinal": 20,
        "end": 155,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 152
      },
      {
        "encounter_ordinal": 21,
        "end": 166,
        "normalized_term": "structured",
        "observed_text": "structured",
        "start": 156
      },
      {
        "encounter_ordinal": 22,
        "end": 175,
        "normalized_term": "command",
        "observed_text": "Command",
        "start": 168
      },
      {
        "encounter_ordinal": 23,
        "end": 187,
        "normalized_term": "executable",
        "observed_text": "executable",
        "start": 177
      },
      {
        "encounter_ordinal": 24,
        "end": 191,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 188
      },
      {
        "encounter_ordinal": 25,
        "end": 201,
        "normalized_term": "arguments",
        "observed_text": "arguments",
        "start": 192
      },
      {
        "encounter_ordinal": 26,
        "end": 213,
        "normalized_term": "exit_code",
        "observed_text": "exit_code",
        "start": 204
      },
      {
        "encounter_ordinal": 27,
        "end": 225,
        "normalized_term": "duration",
        "observed_text": "duration",
        "start": 217
      },
      {
        "encounter_ordinal": 28,
        "end": 231,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 228
      },
      {
        "encounter_ordinal": 29,
        "end": 242,
        "normalized_term": "succeeded",
        "observed_text": "succeeded",
        "start": 233
      },
      {
        "encounter_ordinal": 30,
        "end": 251,
        "normalized_term": "failed",
        "observed_text": "failed",
        "start": 245
      },
      {
        "encounter_ordinal": 31,
        "end": 260,
        "normalized_term": "meaning",
        "observed_text": "meaning",
        "start": 253
      },
      {
        "encounter_ordinal": 32,
        "end": 263,
        "normalized_term": "a",
        "observed_text": "A",
        "start": 262
      },
      {
        "encounter_ordinal": 33,
        "end": 271,
        "normalized_term": "nonzero",
        "observed_text": "nonzero",
        "start": 264
      },
      {
        "encounter_ordinal": 34,
        "end": 276,
        "normalized_term": "exit",
        "observed_text": "exit",
        "start": 272
      },
      {
        "encounter_ordinal": 35,
        "end": 279,
        "normalized_term": "is",
        "observed_text": "is",
        "start": 277
      },
      {
        "encounter_ordinal": 36,
        "end": 282,
        "normalized_term": "an",
        "observed_text": "an",
        "start": 280
      },
      {
        "encounter_ordinal": 37,
        "end": 291,
        "normalized_term": "ordinary",
        "observed_text": "ordinary",
        "start": 283
      },
      {
        "encounter_ordinal": 38,
        "end": 301,
        "normalized_term": "completed",
        "observed_text": "completed",
        "start": 292
      },
      {
        "encounter_ordinal": 39,
        "end": 308,
        "normalized_term": "result",
        "observed_text": "result",
        "start": 302
      },
      {
        "encounter_ordinal": 40,
        "end": 319,
        "normalized_term": "rendering",
        "observed_text": "Rendering",
        "start": 310
      },
      {
        "encounter_ordinal": 41,
        "end": 324,
        "normalized_term": "must",
        "observed_text": "must",
        "start": 320
      },
      {
        "encounter_ordinal": 42,
        "end": 327,
        "normalized_term": "be",
        "observed_text": "be",
        "start": 325
      },
      {
        "encounter_ordinal": 43,
        "end": 329,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 328
      },
      {
        "encounter_ordinal": 44,
        "end": 334,
        "normalized_term": "pure",
        "observed_text": "pure",
        "start": 330
      },
      {
        "encounter_ordinal": 45,
        "end": 344,
        "normalized_term": "operation",
        "observed_text": "operation",
        "start": 335
      },
      {
        "encounter_ordinal": 46,
        "end": 348,
        "normalized_term": "do",
        "observed_text": "do",
        "start": 346
      },
      {
        "encounter_ordinal": 47,
        "end": 352,
        "normalized_term": "not",
        "observed_text": "not",
        "start": 349
      },
      {
        "encounter_ordinal": 48,
        "end": 360,
        "normalized_term": "execute",
        "observed_text": "execute",
        "start": 353
      },
      {
        "encounter_ordinal": 49,
        "end": 362,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 361
      },
      {
        "encounter_ordinal": 50,
        "end": 370,
        "normalized_term": "command",
        "observed_text": "command",
        "start": 363
      },
      {
        "encounter_ordinal": 51,
        "end": 378,
        "normalized_term": "invoke",
        "observed_text": "invoke",
        "start": 372
      },
      {
        "encounter_ordinal": 52,
        "end": 380,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 379
      },
      {
        "encounter_ordinal": 53,
        "end": 386,
        "normalized_term": "shell",
        "observed_text": "shell",
        "start": 381
      },
      {
        "encounter_ordinal": 54,
        "end": 393,
        "normalized_term": "retry",
        "observed_text": "retry",
        "start": 388
      },
      {
        "encounter_ordinal": 55,
        "end": 397,
        "normalized_term": "or",
        "observed_text": "or",
        "start": 395
      },
      {
        "encounter_ordinal": 56,
        "end": 404,
        "normalized_term": "mutate",
        "observed_text": "mutate",
        "start": 398
      },
      {
        "encounter_ordinal": 57,
        "end": 408,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 405
      },
      {
        "encounter_ordinal": 58,
        "end": 415,
        "normalized_term": "result",
        "observed_text": "result",
        "start": 409
      },
      {
        "encounter_ordinal": 59,
        "end": 420,
        "normalized_term": "o2",
        "observed_text": "O2",
        "start": 418
      },
      {
        "encounter_ordinal": 60,
        "end": 428,
        "normalized_term": "render",
        "observed_text": "Render",
        "start": 422
      },
      {
        "encounter_ordinal": 61,
        "end": 436,
        "normalized_term": "stdout",
        "observed_text": "stdout",
        "start": 430
      },
      {
        "encounter_ordinal": 62,
        "end": 441,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 438
      },
      {
        "encounter_ordinal": 63,
        "end": 449,
        "normalized_term": "stderr",
        "observed_text": "stderr",
        "start": 443
      },
      {
        "encounter_ordinal": 64,
        "end": 453,
        "normalized_term": "as",
        "observed_text": "as",
        "start": 451
      },
      {
        "encounter_ordinal": 65,
        "end": 464,
        "normalized_term": "separately",
        "observed_text": "separately",
        "start": 454
      },
      {
        "encounter_ordinal": 66,
        "end": 472,
        "normalized_term": "labeled",
        "observed_text": "labeled",
        "start": 465
      },
      {
        "encounter_ordinal": 67,
        "end": 476,
        "normalized_term": "utf",
        "observed_text": "UTF",
        "start": 473
      },
      {
        "encounter_ordinal": 68,
        "end": 478,
        "normalized_term": "8",
        "observed_text": "8",
        "start": 477
      },
      {
        "encounter_ordinal": 69,
        "end": 489,
        "normalized_term": "diagnostic",
        "observed_text": "diagnostic",
        "start": 479
      },
      {
        "encounter_ordinal": 70,
        "end": 498,
        "normalized_term": "excerpts",
        "observed_text": "excerpts",
        "start": 490
      },
      {
        "encounter_ordinal": 71,
        "end": 506,
        "normalized_term": "retain",
        "observed_text": "Retain",
        "start": 500
      },
      {
        "encounter_ordinal": 72,
        "end": 510,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 507
      },
      {
        "encounter_ordinal": 73,
        "end": 519,
        "normalized_term": "original",
        "observed_text": "original",
        "start": 511
      },
      {
        "encounter_ordinal": 74,
        "end": 525,
        "normalized_term": "bytes",
        "observed_text": "bytes",
        "start": 520
      },
      {
        "encounter_ordinal": 75,
        "end": 535,
        "normalized_term": "unchanged",
        "observed_text": "unchanged",
        "start": 526
      },
      {
        "encounter_ordinal": 76,
        "end": 540,
        "normalized_term": "use",
        "observed_text": "Use",
        "start": 537
      },
      {
        "encounter_ordinal": 77,
        "end": 549,
        "normalized_term": "explicit",
        "observed_text": "explicit",
        "start": 541
      },
      {
        "encounter_ordinal": 78,
        "end": 561,
        "normalized_term": "replacement",
        "observed_text": "replacement",
        "start": 550
      },
      {
        "encounter_ordinal": 79,
        "end": 570,
        "normalized_term": "decoding",
        "observed_text": "decoding",
        "start": 562
      },
      {
        "encounter_ordinal": 80,
        "end": 574,
        "normalized_term": "for",
        "observed_text": "for",
        "start": 571
      },
      {
        "encounter_ordinal": 81,
        "end": 582,
        "normalized_term": "invalid",
        "observed_text": "invalid",
        "start": 575
      },
      {
        "encounter_ordinal": 82,
        "end": 585,
        "normalized_term": "or",
        "observed_text": "or",
        "start": 583
      },
      {
        "encounter_ordinal": 83,
        "end": 596,
        "normalized_term": "incomplete",
        "observed_text": "incomplete",
        "start": 586
      },
      {
        "encounter_ordinal": 84,
        "end": 600,
        "normalized_term": "utf",
        "observed_text": "UTF",
        "start": 597
      },
      {
        "encounter_ordinal": 85,
        "end": 602,
        "normalized_term": "8",
        "observed_text": "8",
        "start": 601
      },
      {
        "encounter_ordinal": 86,
        "end": 612,
        "normalized_term": "disclose",
        "observed_text": "disclose",
        "start": 604
      },
      {
        "encounter_ordinal": 87,
        "end": 621,
        "normalized_term": "decoding",
        "observed_text": "decoding",
        "start": 613
      },
      {
        "encounter_ordinal": 88,
        "end": 626,
        "normalized_term": "loss",
        "observed_text": "loss",
        "start": 622
      },
      {
        "encounter_ordinal": 89,
        "end": 637,
        "normalized_term": "separately",
        "observed_text": "separately",
        "start": 627
      },
      {
        "encounter_ordinal": 90,
        "end": 642,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 639
      },
      {
        "encounter_ordinal": 91,
        "end": 648,
        "normalized_term": "never",
        "observed_text": "never",
        "start": 643
      },
      {
        "encounter_ordinal": 92,
        "end": 654,
        "normalized_term": "imply",
        "observed_text": "imply",
        "start": 649
      },
      {
        "encounter_ordinal": 93,
        "end": 659,
        "normalized_term": "that",
        "observed_text": "that",
        "start": 655
      },
      {
        "encounter_ordinal": 94,
        "end": 667,
        "normalized_term": "decoded",
        "observed_text": "decoded",
        "start": 660
      },
      {
        "encounter_ordinal": 95,
        "end": 672,
        "normalized_term": "text",
        "observed_text": "text",
        "start": 668
      },
      {
        "encounter_ordinal": 96,
        "end": 675,
        "normalized_term": "is",
        "observed_text": "is",
        "start": 673
      },
      {
        "encounter_ordinal": 97,
        "end": 679,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 676
      },
      {
        "encounter_ordinal": 98,
        "end": 688,
        "normalized_term": "original",
        "observed_text": "original",
        "start": 680
      },
      {
        "encounter_ordinal": 99,
        "end": 693,
        "normalized_term": "byte",
        "observed_text": "byte",
        "start": 689
      },
      {
        "encounter_ordinal": 100,
        "end": 700,
        "normalized_term": "stream",
        "observed_text": "stream",
        "start": 694
      },
      {
        "encounter_ordinal": 101,
        "end": 705,
        "normalized_term": "o3",
        "observed_text": "O3",
        "start": 703
      },
      {
        "encounter_ordinal": 102,
        "end": 710,
        "normalized_term": "add",
        "observed_text": "Add",
        "start": 707
      },
      {
        "encounter_ordinal": 103,
        "end": 712,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 711
      },
      {
        "encounter_ordinal": 104,
        "end": 719,
        "normalized_term": "caller",
        "observed_text": "caller",
        "start": 713
      },
      {
        "encounter_ordinal": 105,
        "end": 732,
        "normalized_term": "configurable",
        "observed_text": "configurable",
        "start": 720
      },
      {
        "encounter_ordinal": 106,
        "end": 744,
        "normalized_term": "nonnegative",
        "observed_text": "nonnegative",
        "start": 733
      },
      {
        "encounter_ordinal": 107,
        "end": 748,
        "normalized_term": "per",
        "observed_text": "per",
        "start": 745
      },
      {
        "encounter_ordinal": 108,
        "end": 755,
        "normalized_term": "stream",
        "observed_text": "stream",
        "start": 749
      },
      {
        "encounter_ordinal": 109,
        "end": 765,
        "normalized_term": "character",
        "observed_text": "character",
        "start": 756
      },
      {
        "encounter_ordinal": 110,
        "end": 773,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 766
      },
      {
        "encounter_ordinal": 111,
        "end": 779,
        "normalized_term": "limit",
        "observed_text": "limit",
        "start": 774
      },
      {
        "encounter_ordinal": 112,
        "end": 785,
        "normalized_term": "with",
        "observed_text": "with",
        "start": 781
      },
      {
        "encounter_ordinal": 113,
        "end": 787,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 786
      },
      {
        "encounter_ordinal": 114,
        "end": 795,
        "normalized_term": "default",
        "observed_text": "default",
        "start": 788
      },
      {
        "encounter_ordinal": 115,
        "end": 798,
        "normalized_term": "of",
        "observed_text": "of",
        "start": 796
      },
      {
        "encounter_ordinal": 116,
        "end": 803,
        "normalized_term": "2048",
        "observed_text": "2048",
        "start": 799
      },
      {
        "encounter_ordinal": 117,
        "end": 814,
        "normalized_term": "characters",
        "observed_text": "characters",
        "start": 804
      },
      {
        "encounter_ordinal": 118,
        "end": 820,
        "normalized_term": "show",
        "observed_text": "Show",
        "start": 816
      },
      {
        "encounter_ordinal": 119,
        "end": 825,
        "normalized_term": "only",
        "observed_text": "only",
        "start": 821
      },
      {
        "encounter_ordinal": 120,
        "end": 827,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 826
      },
      {
        "encounter_ordinal": 121,
        "end": 835,
        "normalized_term": "leading",
        "observed_text": "leading",
        "start": 828
      },
      {
        "encounter_ordinal": 122,
        "end": 843,
        "normalized_term": "decoded",
        "observed_text": "decoded",
        "start": 836
      },
      {
        "encounter_ordinal": 123,
        "end": 850,
        "normalized_term": "prefix",
        "observed_text": "prefix",
        "start": 844
      },
      {
        "encounter_ordinal": 124,
        "end": 854,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 851
      },
      {
        "encounter_ordinal": 125,
        "end": 863,
        "normalized_term": "disclose",
        "observed_text": "disclose",
        "start": 855
      },
      {
        "encounter_ordinal": 126,
        "end": 871,
        "normalized_term": "omitted",
        "observed_text": "omitted",
        "start": 864
      },
      {
        "encounter_ordinal": 127,
        "end": 879,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 872
      },
      {
        "encounter_ordinal": 128,
        "end": 890,
        "normalized_term": "characters",
        "observed_text": "characters",
        "start": 880
      },
      {
        "encounter_ordinal": 129,
        "end": 903,
        "normalized_term": "distinguish",
        "observed_text": "Distinguish",
        "start": 892
      },
      {
        "encounter_ordinal": 130,
        "end": 908,
        "normalized_term": "this",
        "observed_text": "this",
        "start": 904
      },
      {
        "encounter_ordinal": 131,
        "end": 916,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 909
      },
      {
        "encounter_ordinal": 132,
        "end": 922,
        "normalized_term": "limit",
        "observed_text": "limit",
        "start": 917
      },
      {
        "encounter_ordinal": 133,
        "end": 927,
        "normalized_term": "from",
        "observed_text": "from",
        "start": 923
      },
      {
        "encounter_ordinal": 134,
        "end": 948,
        "normalized_term": "commandoutputpolicy",
        "observed_text": "CommandOutputPolicy",
        "start": 929
      },
      {
        "encounter_ordinal": 135,
        "end": 954,
        "normalized_term": "byte",
        "observed_text": "byte",
        "start": 950
      },
      {
        "encounter_ordinal": 136,
        "end": 964,
        "normalized_term": "retention",
        "observed_text": "retention",
        "start": 955
      },
      {
        "encounter_ordinal": 137,
        "end": 968,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 965
      },
      {
        "encounter_ordinal": 138,
        "end": 973,
        "normalized_term": "from",
        "observed_text": "from",
        "start": 969
      },
      {
        "encounter_ordinal": 139,
        "end": 991,
        "normalized_term": "stdout_truncated",
        "observed_text": "stdout_truncated",
        "start": 975
      },
      {
        "encounter_ordinal": 140,
        "end": 1010,
        "normalized_term": "stderr_truncated",
        "observed_text": "stderr_truncated",
        "start": 994
      },
      {
        "encounter_ordinal": 141,
        "end": 1014,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 1013
      },
      {
        "encounter_ordinal": 142,
        "end": 1019,
        "normalized_term": "zero",
        "observed_text": "zero",
        "start": 1015
      },
      {
        "encounter_ordinal": 143,
        "end": 1027,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 1020
      },
      {
        "encounter_ordinal": 144,
        "end": 1033,
        "normalized_term": "limit",
        "observed_text": "limit",
        "start": 1028
      },
      {
        "encounter_ordinal": 145,
        "end": 1038,
        "normalized_term": "must",
        "observed_text": "must",
        "start": 1034
      },
      {
        "encounter_ordinal": 146,
        "end": 1045,
        "normalized_term": "remain",
        "observed_text": "remain",
        "start": 1039
      },
      {
        "encounter_ordinal": 147,
        "end": 1057,
        "normalized_term": "informative",
        "observed_text": "informative",
        "start": 1046
      },
      {
        "encounter_ordinal": 148,
        "end": 1063,
        "normalized_term": "about",
        "observed_text": "about",
        "start": 1058
      },
      {
        "encounter_ordinal": 149,
        "end": 1071,
        "normalized_term": "omitted",
        "observed_text": "omitted",
        "start": 1064
      },
      {
        "encounter_ordinal": 150,
        "end": 1078,
        "normalized_term": "output",
        "observed_text": "output",
        "start": 1072
      },
      {
        "encounter_ordinal": 151,
        "end": 1083,
        "normalized_term": "o4",
        "observed_text": "O4",
        "start": 1081
      },
      {
        "encounter_ordinal": 152,
        "end": 1093,
        "normalized_term": "preserve",
        "observed_text": "Preserve",
        "start": 1085
      },
      {
        "encounter_ordinal": 153,
        "end": 1097,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 1094
      },
      {
        "encounter_ordinal": 154,
        "end": 1105,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 1098
      },
      {
        "encounter_ordinal": 155,
        "end": 1121,
        "normalized_term": "events_dropped",
        "observed_text": "events_dropped",
        "start": 1107
      },
      {
        "encounter_ordinal": 156,
        "end": 1136,
        "normalized_term": "independently",
        "observed_text": "independently",
        "start": 1123
      },
      {
        "encounter_ordinal": 157,
        "end": 1139,
        "normalized_term": "of",
        "observed_text": "of",
        "start": 1137
      },
      {
        "encounter_ordinal": 158,
        "end": 1146,
        "normalized_term": "output",
        "observed_text": "output",
        "start": 1140
      },
      {
        "encounter_ordinal": 159,
        "end": 1157,
        "normalized_term": "truncation",
        "observed_text": "truncation",
        "start": 1147
      },
      {
        "encounter_ordinal": 160,
        "end": 1161,
        "normalized_term": "do",
        "observed_text": "Do",
        "start": 1159
      },
      {
        "encounter_ordinal": 161,
        "end": 1165,
        "normalized_term": "not",
        "observed_text": "not",
        "start": 1162
      },
      {
        "encounter_ordinal": 162,
        "end": 1177,
        "normalized_term": "reconstruct",
        "observed_text": "reconstruct",
        "start": 1166
      },
      {
        "encounter_ordinal": 163,
        "end": 1183,
        "normalized_term": "event",
        "observed_text": "event",
        "start": 1178
      },
      {
        "encounter_ordinal": 164,
        "end": 1196,
        "normalized_term": "interleaving",
        "observed_text": "interleaving",
        "start": 1184
      },
      {
        "encounter_ordinal": 165,
        "end": 1199,
        "normalized_term": "or",
        "observed_text": "or",
        "start": 1197
      },
      {
        "encounter_ordinal": 166,
        "end": 1209,
        "normalized_term": "fabricate",
        "observed_text": "fabricate",
        "start": 1200
      },
      {
        "encounter_ordinal": 167,
        "end": 1217,
        "normalized_term": "missing",
        "observed_text": "missing",
        "start": 1210
      },
      {
        "encounter_ordinal": 168,
        "end": 1224,
        "normalized_term": "events",
        "observed_text": "events",
        "start": 1218
      },
      {
        "encounter_ordinal": 169,
        "end": 1228,
        "normalized_term": "do",
        "observed_text": "Do",
        "start": 1226
      },
      {
        "encounter_ordinal": 170,
        "end": 1232,
        "normalized_term": "not",
        "observed_text": "not",
        "start": 1229
      },
      {
        "encounter_ordinal": 171,
        "end": 1239,
        "normalized_term": "create",
        "observed_text": "create",
        "start": 1233
      },
      {
        "encounter_ordinal": 172,
        "end": 1241,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 1240
      },
      {
        "encounter_ordinal": 173,
        "end": 1256,
        "normalized_term": "commandresult",
        "observed_text": "CommandResult",
        "start": 1243
      },
      {
        "encounter_ordinal": 174,
        "end": 1261,
        "normalized_term": "for",
        "observed_text": "for",
        "start": 1258
      },
      {
        "encounter_ordinal": 175,
        "end": 1269,
        "normalized_term": "timeout",
        "observed_text": "timeout",
        "start": 1262
      },
      {
        "encounter_ordinal": 176,
        "end": 1283,
        "normalized_term": "cancellation",
        "observed_text": "cancellation",
        "start": 1271
      },
      {
        "encounter_ordinal": 177,
        "end": 1287,
        "normalized_term": "or",
        "observed_text": "or",
        "start": 1285
      },
      {
        "encounter_ordinal": 178,
        "end": 1298,
        "normalized_term": "executable",
        "observed_text": "executable",
        "start": 1288
      },
      {
        "encounter_ordinal": 179,
        "end": 1302,
        "normalized_term": "not",
        "observed_text": "not",
        "start": 1299
      },
      {
        "encounter_ordinal": 180,
        "end": 1308,
        "normalized_term": "found",
        "observed_text": "found",
        "start": 1303
      },
      {
        "encounter_ordinal": 181,
        "end": 1317,
        "normalized_term": "failures",
        "observed_text": "failures",
        "start": 1309
      },
      {
        "encounter_ordinal": 182,
        "end": 1323,
        "normalized_term": "this",
        "observed_text": "this",
        "start": 1319
      },
      {
        "encounter_ordinal": 183,
        "end": 1332,
        "normalized_term": "renderer",
        "observed_text": "renderer",
        "start": 1324
      },
      {
        "encounter_ordinal": 184,
        "end": 1340,
        "normalized_term": "accepts",
        "observed_text": "accepts",
        "start": 1333
      },
      {
        "encounter_ordinal": 185,
        "end": 1345,
        "normalized_term": "only",
        "observed_text": "only",
        "start": 1341
      },
      {
        "encounter_ordinal": 186,
        "end": 1348,
        "normalized_term": "an",
        "observed_text": "an",
        "start": 1346
      },
      {
        "encounter_ordinal": 187,
        "end": 1357,
        "normalized_term": "existing",
        "observed_text": "existing",
        "start": 1349
      },
      {
        "encounter_ordinal": 188,
        "end": 1367,
        "normalized_term": "completed",
        "observed_text": "completed",
        "start": 1358
      },
      {
        "encounter_ordinal": 189,
        "end": 1374,
        "normalized_term": "result",
        "observed_text": "result",
        "start": 1368
      },
      {
        "encounter_ordinal": 190,
        "end": 1379,
        "normalized_term": "o5",
        "observed_text": "O5",
        "start": 1377
      },
      {
        "encounter_ordinal": 191,
        "end": 1388,
        "normalized_term": "provide",
        "observed_text": "Provide",
        "start": 1381
      },
      {
        "encounter_ordinal": 192,
        "end": 1390,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 1389
      },
      {
        "encounter_ordinal": 193,
        "end": 1396,
        "normalized_term": "small",
        "observed_text": "small",
        "start": 1391
      },
      {
        "encounter_ordinal": 194,
        "end": 1405,
        "normalized_term": "explicit",
        "observed_text": "explicit",
        "start": 1397
      },
      {
        "encounter_ordinal": 195,
        "end": 1412,
        "normalized_term": "public",
        "observed_text": "public",
        "start": 1406
      },
      {
        "encounter_ordinal": 196,
        "end": 1416,
        "normalized_term": "api",
        "observed_text": "API",
        "start": 1413
      },
      {
        "encounter_ordinal": 197,
        "end": 1424,
        "normalized_term": "through",
        "observed_text": "through",
        "start": 1417
      },
      {
        "encounter_ordinal": 198,
        "end": 1429,
        "normalized_term": "src",
        "observed_text": "src",
        "start": 1426
      },
      {
        "encounter_ordinal": 199,
        "end": 1438,
        "normalized_term": "devtools",
        "observed_text": "devtools",
        "start": 1430
      },
      {
        "encounter_ordinal": 200,
        "end": 1448,
        "normalized_term": "resources",
        "observed_text": "resources",
        "start": 1439
      },
      {
        "encounter_ordinal": 201,
        "end": 1457,
        "normalized_term": "commands",
        "observed_text": "commands",
        "start": 1449
      },
      {
        "encounter_ordinal": 202,
        "end": 1466,
        "normalized_term": "__init__",
        "observed_text": "__init__",
        "start": 1458
      },
      {
        "encounter_ordinal": 203,
        "end": 1469,
        "normalized_term": "py",
        "observed_text": "py",
        "start": 1467
      },
      {
        "encounter_ordinal": 204,
        "end": 1475,
        "normalized_term": "with",
        "observed_text": "with",
        "start": 1471
      },
      {
        "encounter_ordinal": 205,
        "end": 1489,
        "normalized_term": "deterministic",
        "observed_text": "deterministic",
        "start": 1476
      },
      {
        "encounter_ordinal": 206,
        "end": 1496,
        "normalized_term": "output",
        "observed_text": "output",
        "start": 1490
      },
      {
        "encounter_ordinal": 207,
        "end": 1507,
        "normalized_term": "immutable",
        "observed_text": "immutable",
        "start": 1498
      },
      {
        "encounter_ordinal": 208,
        "end": 1514,
        "normalized_term": "inputs",
        "observed_text": "inputs",
        "start": 1508
      },
      {
        "encounter_ordinal": 209,
        "end": 1518,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 1515
      },
      {
        "encounter_ordinal": 210,
        "end": 1529,
        "normalized_term": "documented",
        "observed_text": "documented",
        "start": 1519
      },
      {
        "encounter_ordinal": 211,
        "end": 1538,
        "normalized_term": "decoding",
        "observed_text": "decoding",
        "start": 1530
      },
      {
        "encounter_ordinal": 212,
        "end": 1546,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 1539
      },
      {
        "encounter_ordinal": 213,
        "end": 1553,
        "normalized_term": "policy",
        "observed_text": "policy",
        "start": 1547
      },
      {
        "encounter_ordinal": 214,
        "end": 1559,
        "normalized_term": "keep",
        "observed_text": "Keep",
        "start": 1555
      },
      {
        "encounter_ordinal": 215,
        "end": 1572,
        "normalized_term": "presentation",
        "observed_text": "presentation",
        "start": 1560
      },
      {
        "encounter_ordinal": 216,
        "end": 1575,
        "normalized_term": "in",
        "observed_text": "in",
        "start": 1573
      },
      {
        "encounter_ordinal": 217,
        "end": 1579,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 1576
      },
      {
        "encounter_ordinal": 218,
        "end": 1588,
        "normalized_term": "commands",
        "observed_text": "commands",
        "start": 1580
      },
      {
        "encounter_ordinal": 219,
        "end": 1595,
        "normalized_term": "domain",
        "observed_text": "domain",
        "start": 1589
      },
      {
        "encounter_ordinal": 220,
        "end": 1599,
        "normalized_term": "do",
        "observed_text": "do",
        "start": 1597
      },
      {
        "encounter_ordinal": 221,
        "end": 1603,
        "normalized_term": "not",
        "observed_text": "not",
        "start": 1600
      },
      {
        "encounter_ordinal": 222,
        "end": 1607,
        "normalized_term": "add",
        "observed_text": "add",
        "start": 1604
      },
      {
        "encounter_ordinal": 223,
        "end": 1615,
        "normalized_term": "logging",
        "observed_text": "logging",
        "start": 1608
      },
      {
        "encounter_ordinal": 224,
        "end": 1625,
        "normalized_term": "evidence",
        "observed_text": "Evidence",
        "start": 1617
      },
      {
        "encounter_ordinal": 225,
        "end": 1631,
        "normalized_term": "trace",
        "observed_text": "Trace",
        "start": 1626
      },
      {
        "encounter_ordinal": 226,
        "end": 1646,
        "normalized_term": "infrastructure",
        "observed_text": "infrastructure",
        "start": 1632
      },
      {
        "encounter_ordinal": 227,
        "end": 1658,
        "normalized_term": "subprocess",
        "observed_text": "subprocess",
        "start": 1648
      },
      {
        "encounter_ordinal": 228,
        "end": 1668,
        "normalized_term": "ownership",
        "observed_text": "ownership",
        "start": 1659
      },
      {
        "encounter_ordinal": 229,
        "end": 1681,
        "normalized_term": "persistence",
        "observed_text": "persistence",
        "start": 1670
      },
      {
        "encounter_ordinal": 230,
        "end": 1685,
        "normalized_term": "or",
        "observed_text": "or",
        "start": 1683
      },
      {
        "encounter_ordinal": 231,
        "end": 1687,
        "normalized_term": "a",
        "observed_text": "a",
        "start": 1686
      },
      {
        "encounter_ordinal": 232,
        "end": 1693,
        "normalized_term": "claim",
        "observed_text": "claim",
        "start": 1688
      },
      {
        "encounter_ordinal": 233,
        "end": 1696,
        "normalized_term": "of",
        "observed_text": "of",
        "start": 1694
      },
      {
        "encounter_ordinal": 234,
        "end": 1703,
        "normalized_term": "secret",
        "observed_text": "secret",
        "start": 1697
      },
      {
        "encounter_ordinal": 235,
        "end": 1713,
        "normalized_term": "redaction",
        "observed_text": "redaction",
        "start": 1704
      },
      {
        "encounter_ordinal": 236,
        "end": 1718,
        "normalized_term": "o6",
        "observed_text": "O6",
        "start": 1716
      },
      {
        "encounter_ordinal": 237,
        "end": 1723,
        "normalized_term": "add",
        "observed_text": "Add",
        "start": 1720
      },
      {
        "encounter_ordinal": 238,
        "end": 1734,
        "normalized_term": "controlled",
        "observed_text": "controlled",
        "start": 1724
      },
      {
        "encounter_ordinal": 239,
        "end": 1740,
        "normalized_term": "tests",
        "observed_text": "tests",
        "start": 1735
      },
      {
        "encounter_ordinal": 240,
        "end": 1746,
        "normalized_term": "under",
        "observed_text": "under",
        "start": 1741
      },
      {
        "encounter_ordinal": 241,
        "end": 1753,
        "normalized_term": "tests",
        "observed_text": "tests",
        "start": 1748
      },
      {
        "encounter_ordinal": 242,
        "end": 1763,
        "normalized_term": "resources",
        "observed_text": "resources",
        "start": 1754
      },
      {
        "encounter_ordinal": 243,
        "end": 1772,
        "normalized_term": "commands",
        "observed_text": "commands",
        "start": 1764
      },
      {
        "encounter_ordinal": 244,
        "end": 1778,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 1775
      },
      {
        "encounter_ordinal": 245,
        "end": 1785,
        "normalized_term": "update",
        "observed_text": "update",
        "start": 1779
      },
      {
        "encounter_ordinal": 246,
        "end": 1789,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 1786
      },
      {
        "encounter_ordinal": 247,
        "end": 1797,
        "normalized_term": "package",
        "observed_text": "package",
        "start": 1790
      },
      {
        "encounter_ordinal": 248,
        "end": 1811,
        "normalized_term": "documentation",
        "observed_text": "documentation",
        "start": 1798
      },
      {
        "encounter_ordinal": 249,
        "end": 1817,
        "normalized_term": "under",
        "observed_text": "under",
        "start": 1812
      },
      {
        "encounter_ordinal": 250,
        "end": 1822,
        "normalized_term": "src",
        "observed_text": "src",
        "start": 1819
      },
      {
        "encounter_ordinal": 251,
        "end": 1831,
        "normalized_term": "devtools",
        "observed_text": "devtools",
        "start": 1823
      },
      {
        "encounter_ordinal": 252,
        "end": 1841,
        "normalized_term": "resources",
        "observed_text": "resources",
        "start": 1832
      },
      {
        "encounter_ordinal": 253,
        "end": 1850,
        "normalized_term": "commands",
        "observed_text": "commands",
        "start": 1842
      },
      {
        "encounter_ordinal": 254,
        "end": 1855,
        "normalized_term": "docs",
        "observed_text": "docs",
        "start": 1851
      },
      {
        "encounter_ordinal": 255,
        "end": 1861,
        "normalized_term": "for",
        "observed_text": "for",
        "start": 1858
      },
      {
        "encounter_ordinal": 256,
        "end": 1869,
        "normalized_term": "success",
        "observed_text": "success",
        "start": 1862
      },
      {
        "encounter_ordinal": 257,
        "end": 1877,
        "normalized_term": "nonzero",
        "observed_text": "nonzero",
        "start": 1870
      },
      {
        "encounter_ordinal": 258,
        "end": 1882,
        "normalized_term": "exit",
        "observed_text": "exit",
        "start": 1878
      },
      {
        "encounter_ordinal": 259,
        "end": 1889,
        "normalized_term": "empty",
        "observed_text": "empty",
        "start": 1884
      },
      {
        "encounter_ordinal": 260,
        "end": 1896,
        "normalized_term": "output",
        "observed_text": "output",
        "start": 1890
      },
      {
        "encounter_ordinal": 261,
        "end": 1903,
        "normalized_term": "valid",
        "observed_text": "valid",
        "start": 1898
      },
      {
        "encounter_ordinal": 262,
        "end": 1911,
        "normalized_term": "invalid",
        "observed_text": "invalid",
        "start": 1904
      },
      {
        "encounter_ordinal": 263,
        "end": 1922,
        "normalized_term": "incomplete",
        "observed_text": "incomplete",
        "start": 1912
      },
      {
        "encounter_ordinal": 264,
        "end": 1926,
        "normalized_term": "utf",
        "observed_text": "UTF",
        "start": 1923
      },
      {
        "encounter_ordinal": 265,
        "end": 1928,
        "normalized_term": "8",
        "observed_text": "8",
        "start": 1927
      },
      {
        "encounter_ordinal": 266,
        "end": 1934,
        "normalized_term": "zero",
        "observed_text": "zero",
        "start": 1930
      },
      {
        "encounter_ordinal": 267,
        "end": 1942,
        "normalized_term": "default",
        "observed_text": "default",
        "start": 1935
      },
      {
        "encounter_ordinal": 268,
        "end": 1949,
        "normalized_term": "custom",
        "observed_text": "custom",
        "start": 1943
      },
      {
        "encounter_ordinal": 269,
        "end": 1957,
        "normalized_term": "display",
        "observed_text": "display",
        "start": 1950
      },
      {
        "encounter_ordinal": 270,
        "end": 1964,
        "normalized_term": "bounds",
        "observed_text": "bounds",
        "start": 1958
      },
      {
        "encounter_ordinal": 271,
        "end": 1977,
        "normalized_term": "independent",
        "observed_text": "independent",
        "start": 1966
      },
      {
        "encounter_ordinal": 272,
        "end": 1987,
        "normalized_term": "retention",
        "observed_text": "retention",
        "start": 1978
      },
      {
        "encounter_ordinal": 273,
        "end": 1993,
        "normalized_term": "flags",
        "observed_text": "flags",
        "start": 1988
      },
      {
        "encounter_ordinal": 274,
        "end": 2000,
        "normalized_term": "event",
        "observed_text": "event",
        "start": 1995
      },
      {
        "encounter_ordinal": 275,
        "end": 2005,
        "normalized_term": "loss",
        "observed_text": "loss",
        "start": 2001
      },
      {
        "encounter_ordinal": 276,
        "end": 2020,
        "normalized_term": "deterministic",
        "observed_text": "deterministic",
        "start": 2007
      },
      {
        "encounter_ordinal": 277,
        "end": 2027,
        "normalized_term": "output",
        "observed_text": "output",
        "start": 2021
      },
      {
        "encounter_ordinal": 278,
        "end": 2032,
        "normalized_term": "and",
        "observed_text": "and",
        "start": 2029
      },
      {
        "encounter_ordinal": 279,
        "end": 2038,
        "normalized_term": "input",
        "observed_text": "input",
        "start": 2033
      },
      {
        "encounter_ordinal": 280,
        "end": 2051,
        "normalized_term": "immutability",
        "observed_text": "immutability",
        "start": 2039
      },
      {
        "encounter_ordinal": 281,
        "end": 2061,
        "normalized_term": "preserve",
        "observed_text": "Preserve",
        "start": 2053
      },
      {
        "encounter_ordinal": 282,
        "end": 2065,
        "normalized_term": "the",
        "observed_text": "the",
        "start": 2062
      },
      {
        "encounter_ordinal": 283,
        "end": 2075,
        "normalized_term": "protected",
        "observed_text": "protected",
        "start": 2066
      },
      {
        "encounter_ordinal": 284,
        "end": 2087,
        "normalized_term": "development",
        "observed_text": "development",
        "start": 2076
      },
      {
        "encounter_ordinal": 285,
        "end": 2098,
        "normalized_term": "validation",
        "observed_text": "validation",
        "start": 2088
      },
      {
        "encounter_ordinal": 286,
        "end": 2106,
        "normalized_term": "profile",
        "observed_text": "profile",
        "start": 2099
      },
      {
        "encounter_ordinal": 287,
        "end": 2117,
        "normalized_term": "documented",
        "observed_text": "documented",
        "start": 2107
      },
      {
        "encounter_ordinal": 288,
        "end": 2120,
        "normalized_term": "in",
        "observed_text": "in",
        "start": 2118
      },
      {
        "encounter_ordinal": 289,
        "end": 2126,
        "normalized_term": "docs",
        "observed_text": "docs",
        "start": 2122
      },
      {
        "encounter_ordinal": 290,
        "end": 2138,
        "normalized_term": "development",
        "observed_text": "development",
        "start": 2127
      },
      {
        "encounter_ordinal": 291,
        "end": 2149,
        "normalized_term": "validation",
        "observed_text": "validation",
        "start": 2139
      },
      {
        "encounter_ordinal": 292,
        "end": 2152,
        "normalized_term": "md",
        "observed_text": "md",
        "start": 2150
      }
    ],
    "text": "Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.\n\nO1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.\n\nO2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.\n\nO3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.\n\nO4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.\n\nO5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.\n\nO6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.\n"
  },
  "semantics": "Whole-task canonical BM25 only; identical unchanged safety/reference lane; no treatment and no post-result rescue",
  "text": "Add an opt-in deterministic human-readable diagnostic renderer for an already completed `CommandResult` in `devtools.resources.commands`.\n\nO1. Preserve the structured `Command` executable and arguments, `exit_code`, `duration`, and `succeeded`/`failed` meaning. A nonzero exit is an ordinary completed result. Rendering must be a pure operation: do not execute a command, invoke a shell, retry, or mutate the result.\n\nO2. Render `stdout` and `stderr` as separately labeled UTF-8 diagnostic excerpts. Retain the original bytes unchanged. Use explicit replacement decoding for invalid or incomplete UTF-8, disclose decoding loss separately, and never imply that decoded text is the original byte stream.\n\nO3. Add a caller-configurable nonnegative per-stream character display limit, with a default of 2048 characters. Show only a leading decoded prefix and disclose omitted display characters. Distinguish this display limit from `CommandOutputPolicy` byte retention and from `stdout_truncated`/`stderr_truncated`; a zero display limit must remain informative about omitted output.\n\nO4. Preserve and display `events_dropped` independently of output truncation. Do not reconstruct event interleaving or fabricate missing events. Do not create a `CommandResult` for timeout, cancellation, or executable-not-found failures: this renderer accepts only an existing completed result.\n\nO5. Provide a small explicit public API through `src/devtools/resources/commands/__init__.py` with deterministic output, immutable inputs and documented decoding/display policy. Keep presentation in the commands domain; do not add logging, Evidence/Trace infrastructure, subprocess ownership, persistence, or a claim of secret redaction.\n\nO6. Add controlled tests under `tests/resources/commands/` and update the package documentation under `src/devtools/resources/commands/docs/` for success/nonzero exit, empty output, valid/invalid/incomplete UTF-8, zero/default/custom display bounds, independent retention flags, event loss, deterministic output, and input immutability. Preserve the protected development validation profile documented in `docs/development/validation.md`.\n"
}
```

## Ranking/candidate safety, metrics and witness burden accounting

```json
{
  "burden_accounting": "Compute every reviewed complete alternative independently; choose minimum depth then stable witness identity; never mix alternatives. Union chosen mandatory prefixes for unique resource/byte burden; occurrences stay repeated; labels stay owning-obligation relative; no fictional global ranking.",
  "candidate_invariants": [
    "Same exact query analysis and all terms",
    "Same native index/statistics and full positive content OR filename set",
    "No added/dropped resource",
    "Every positive contribution reconstructs native * frozen multiplier",
    "Same collection-order ties and unchanged reference lane",
    "Any violation is an experimental contract defect"
  ],
  "metrics": [
    "REQUIRED resource reach",
    "REQUIRED cell reach",
    "required semantic-unit reach",
    "every reviewed witness completion depth",
    "selected minimum complete witness depth per mandatory obligation, then stable reviewed witness identity",
    "unique completion-prefix resources",
    "total prefix occurrences",
    "duplicate occurrences",
    "owning-obligation REQUIRED occurrences",
    "owning-obligation HELPFUL_ONLY occurrences",
    "owning-obligation UNNECESSARY occurrences",
    "distinct UTF-8 whole-resource bytes",
    "REQUIRED resource rank changes",
    "REQUIRED cell rank changes",
    "obligation-indispensable resource rank changes",
    "task-indispensable resource rank changes",
    "improved/regressed REQUIRED target counts and maximum regression",
    "term-role contribution totals and per-role score shares",
    "captured treatment execution cost",
    "top-K rank inversions at K=10,20,50",
    "per-term native versus weighted contributions"
  ]
}
```

## Single-run cost accounting

```json
"Future single-run capture: frame/index and native full contribution acquisition shared once; charge shared acquisition equally to each arm plus its explicit multiplier/sort/trace construction top-level interval. Capture shared filename construction within native query cost. Reference lane separately, identical. Classification/publication/durability separate, excluded from mechanism cost; no child/composite double counting. No cost threshold selects ranking outcome."
```

## Exact frozen decision rule and precedence

```json
{
  "application_checks": [
    "Every role reconstructs from task/query spans and frozen lexicon",
    "Every term/channel contribution equals unchanged native contribution times frozen positive multiplier",
    "Native tie semantics preserved",
    "No REQUIRED resource/cell/semantic-unit reach loss"
  ],
  "burden": "Positive baseline AND 10*T <= 9*A for chosen unique resources OR repeated occurrences; resources, occurrences and bytes each <= baseline for strong support",
  "complementary_bounds": "Every baseline-complete obligation stays complete; each selected-depth regression <=20% AND <=5 positions; each REQUIRED-cell rank regression <=20% AND <=10 positions: 5*T <= 6*A; equality alone is not value",
  "contract_checks": [
    "Exact committed ancestry and frame/query identities",
    "Unchanged task and complete mandatory obligation coverage",
    "Full canonical contribution capture with unchanged settings/representation/statistics",
    "Identical candidate set, native contribution recoverability and unchanged reference lane",
    "Task/query-only pre-execution classifications and frozen multipliers",
    "Exactly-once capture and cost disclosure",
    "Valid complete treatment-blind primary gold, no unresolved required interpretation and exact content/frame joins"
  ],
  "implementation": "experiments/query_term_weighting/gates.py",
  "meaningful_required_rank": "At least two positions improvement AND 5*T_rank <= 4*A_rank",
  "meaningful_witness": "A incomplete and treatment complete OR A_depth > 0 AND 5*T_depth <= 4*A_depth",
  "precedence": [
    "contract defect => EXPERIMENTAL_CONTRACT_DEFECT",
    "classification/application or REQUIRED reach defect => QUERY_TERM_WEIGHTING_DEFECT",
    "meaningful witness gain AND no selected-depth or REQUIRED-cell rank regression AND >=10% unique-resource OR occurrence reduction AND neither resources, occurrences nor bytes increase => QUERY_TERM_WEIGHTING_SUPPORTED",
    "meaningful witness gain OR meaningful REQUIRED-cell rank gain, with bounded regressions => COMPLEMENTARY_QUERY_WEIGHTING_VALUE",
    "unbounded regression or completion loss => QUERY_TERM_WEIGHTING_HARMFUL",
    "otherwise => NO_MATERIAL_VALUE"
  ],
  "primary": "C versus A only; B versus A evaluated separately for attribution, C versus B diagnostic; never pick the better arm after results",
  "strong_no_regression": "No regression at all in any baseline-complete mandatory selected witness depth or any baseline-reached REQUIRED cell rank",
  "unreached": "No REQUIRED reach loss. Unreached baseline ranks are not fabricated; rescue only if future validated completion/reach records establish it"
}
```

## Failure attribution and exclusions

```json
{
  "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
  "execution_policy": "No Stage B entry point exists at this checkpoint. Future maintainer authorization required; exactly one prospective execution, no tuning or query changes. Controlled fixtures are synthetic and separate.",
  "failure_definitions": {
    "EXPERIMENTAL_CONTRACT_DEFECT": "Broken frame/query/candidate/statistics/blindness/execution/gold/cost contract; no effectiveness inference",
    "EXPLICIT_ANCHOR_OVERWEIGHT": "B/C anchor contributions promote reviewed HELPFUL_ONLY or UNNECESSARY evidence ahead of necessary semantic evidence",
    "GENERIC_TERM_ATTENUATION_HARM": "C-versus-B attenuation reduces useful discrimination and worsens required ranking/completion",
    "LEXICAL_REPRESENTATION_LIMIT": "Necessary evidence has no discriminative native analyzed terms under unchanged whole-text representation",
    "QUERY_AUTHORING_LIMIT": "Frozen query does not express the necessary fact; multipliers cannot repair missing terms",
    "QUERY_DILUTION_NOT_REDUCED": "Generic attenuation does not change the contribution/overtaker pattern blocking reviewed completion",
    "QUERY_TERM_CLASSIFICATION_DEFECT": "Role or literal provenance cannot be reconstructed from frozen task/query-only evidence",
    "QUERY_WEIGHT_APPLICATION_DEFECT": "Contribution multiplier, channel grouping, score or tie cannot be reconstructed",
    "REQUIRED_RANKING_REGRESSION": "Positive candidate retained but necessary target/selected witness worsens; report exact rank/depth and frozen materiality bounds"
  },
  "failure_taxonomy": [
    "QUERY_TERM_CLASSIFICATION_DEFECT",
    "QUERY_WEIGHT_APPLICATION_DEFECT",
    "REQUIRED_RANKING_REGRESSION",
    "QUERY_DILUTION_NOT_REDUCED",
    "EXPLICIT_ANCHOR_OVERWEIGHT",
    "GENERIC_TERM_ATTENUATION_HARM",
    "LEXICAL_REPRESENTATION_LIMIT",
    "QUERY_AUTHORING_LIMIT",
    "EXPERIMENTAL_CONTRACT_DEFECT"
  ],
  "gold_policy": {
    "MODEL": "GPT-6 Astra",
    "REASONING": "High",
    "allowed": [
      "case",
      "task_identity",
      "task_text",
      "obligations",
      "eligible_resources"
    ],
    "automatic_second_review": false,
    "excluded": [
      "queries",
      "analyzed terms",
      "term roles",
      "term weights",
      "arms",
      "scores",
      "ranks",
      "results",
      "metrics",
      "decision rule",
      "prior case outcomes",
      "confirmation/reserve",
      "web",
      "repository/history access",
      "prior-session content"
    ],
    "resource_policy": "Natural original task/resource identifiers intact; complete eligible resource content; no semantic rewriting",
    "treatment_blind": true
  }
}
```

## Frozen native frame and resource eligibility

```json
{
  "binding": {
    "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 515,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494",
    "source_head": "3aafd897a6a46a201180dc51dbef5e5201669a58"
  },
  "complete_identity_inventory": "frame.json; every resource binds repository/snapshot/corpus/document/address/content identity and source blob SHA-256; resources.json.gz retains exact whole content",
  "policy": {
    "excluded_prior_case_resources": [
      "docs/architecture.md",
      "docs/architecture/decisions/ADR-0005-obligation-driven-repository-localization.md",
      "docs/architecture/localization.md",
      "docs/architecture/retrieval.md",
      "docs/architecture/taxonomy.md",
      "docs/backlog/epics/B-0002-coding-context-substrate.md",
      "docs/backlog/items/B-0047-protected-development-validation-profile.md",
      "docs/development/validation.md",
      "docs/documentation_map.md",
      "docs/roadmap.md",
      "src/devtools/context/localization/docs/overview.md",
      "src/devtools/context/localization/roles/docs/overview.md",
      "src/devtools/context/python/project_configuration/docs/overview.md",
      "src/devtools/context/python/references/analysis.py",
      "src/devtools/context/retrieval/graph/docs/overview.md",
      "src/devtools/context/retrieval/repository_map/docs/overview.md"
    ],
    "path_eligibility": "Broad source/test/doc/config selection; no experiments, research/reports/ledger, held-out paths or operational files",
    "prior_case_leakage": "Exclude entire original resource if case[_ -]?00\\d\\d marker occurs, case-insensitive; never strip or rewrite text",
    "task_query_independent": true
  }
}
```

## No prospective execution

```json
{
  "gold": "ABSENT",
  "prospective_index_builds": 0,
  "prospective_obligation_query_executions": 0,
  "treatment_scorings": 0,
  "weighted_rankings": 0
}
```

Maintainer reviews Stage A. Only after authorization execute the prospective lexical treatments once.
