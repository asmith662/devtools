# Case 0015 Stage B mechanical human review

ATTEMPT 1 = FAILED_AUDIT_ONLY

ATTEMPT 2 = AUTHORITATIVE STAGE B CAPTURE

GOLD = ABSENT

EFFECTIVENESS = UNKNOWN

R2 OUTCOME = NOT_SELECTED

RANK MOVEMENT IS NOT EFFECTIVENESS EVIDENCE WITHOUT GOLD.

SEARCH_POLICY_FAILURE = NOT_ASSESSED.

## Exact task

Implement strict bounded acquisition for the existing codec-backed filesystem read API.

O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.

O2. Define the finite acquisition bound precisely: retain at most `max_bytes` payload bytes and acquire at most one additional byte to distinguish exact-boundary EOF from oversized input; bound individual read requests and release the stream on success and every failure. Raise `FileTooLargeError` on excess instead of returning a truncated model. Do not claim a bound on decoded model memory, a stable file snapshot, race-free pathname checks, containment, authorization or locking.

O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.

O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.

O5. Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits, growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures, multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types. Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.

O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.

## Frozen requirement_matrix

```json
[
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O1"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q1"
    },
    "requirement": "O1",
    "satisfaction": "Identify current signature, default, limit semantics and allocation-before-rejection behavior; locate the owning implementation.",
    "task_clause": "O1. In `src/devtools/resources/filesystem/reading.py`, replace the complete `read_bytes()` acquisition used by `read()` with bounded chunk acquisition when `max_bytes` is finite. Preserve the public `ResolvedPath`, `file_format`, `max_bytes` and `DEFAULT_MAX_READ_BYTES` contract, including the 16 MiB default, `None` as explicitly unbounded, negative-limit rejection, zero-limit behavior and acceptance at the exact byte boundary. A preliminary stat check may remain, but a growing file must not cause an unbounded read before rejection.\n\n",
    "task_span": {
      "end": 629,
      "start": 89
    },
    "title": "Compatible bounded read contract"
  },
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O2"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q2"
    },
    "requirement": "O2",
    "satisfaction": "Establish precise max_bytes plus one sentinel acquisition, bounded requests, closure and distinction from model memory/security/snapshot guarantees.",
    "task_clause": "O2. Define the finite acquisition bound precisely: retain at most `max_bytes` payload bytes and acquire at most one additional byte to distinguish exact-boundary EOF from oversized input; bound individual read requests and release the stream on success and every failure. Raise `FileTooLargeError` on excess instead of returning a truncated model. Do not claim a bound on decoded model memory, a stable file snapshot, race-free pathname checks, containment, authorization or locking.\n\n",
    "task_span": {
      "end": 1114,
      "start": 629
    },
    "title": "Acquisition bound and lifecycle"
  },
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O3"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q3"
    },
    "requirement": "O3",
    "satisfaction": "Identify complete-byte codec contracts, format override/inference, concrete models, metadata and strict decoding behavior.",
    "task_clause": "O3. Preserve `resolve_file_format` and `resolve_codec` behavior, explicit format override and suffix inference. Pass complete accepted bytes to the existing codecs without rewriting content. Preserve the concrete `TextFile`, `MarkdownFile`, `CsvFile`, `JsonObjectFile`, `JsonListFile` and `JsonScalarFile` results, UTF-8 decoding, original line endings, encoding and byte-size metadata. Split multibyte input across acquisition chunks without introducing replacement decoding; codec decoding failures remain `TextDecodingError` or the existing format-domain error.\n\n",
    "task_span": {
      "end": 1680,
      "start": 1114
    },
    "title": "Codec and rich-model fidelity"
  },
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O4"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q4"
    },
    "requirement": "O4",
    "satisfaction": "Establish existing error normalization, causal exceptions and package/atomic-write/path/authorization boundaries.",
    "task_clause": "O4. Preserve existing filesystem error boundaries for a missing path, non-regular file, permission denial, unsupported format and oversized input. Normalize permission failures during stream opening and chunk reads to `FilesystemPermissionError` with causal exceptions. Do not change atomic `write()` behavior, format resolution ownership, core path resolution or any Tool authorization boundary; use the existing filesystem package rather than adding a generic streaming framework.\n\n",
    "task_span": {
      "end": 2164,
      "start": 1680
    },
    "title": "Error and ownership boundaries"
  },
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O5"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q5"
    },
    "requirement": "O5",
    "satisfaction": "Find current read/codec/model test patterns and evidence needed for deterministic instrumented-stream tests of bounds and compatibility.",
    "task_clause": "O5. Add controlled tests in `tests/resources/filesystem/test_reading.py` and relevant codec/model tests for empty input, zero/exact/over-limit bytes, negative and unbounded limits, growth after stat, short chunk reads, EOF, stream closure on exceptions, opening/read permission failures, multibyte UTF-8 split across chunks, invalid UTF-8, explicit format overrides and all currently supported rich result types. Demonstrate the finite request/retention bound with deterministic instrumented streams rather than unreliable process-memory measurements or live filesystem races.\n\n",
    "task_span": {
      "end": 2742,
      "start": 2164
    },
    "title": "Controlled regression tests"
  },
  {
    "applicability": "APPLICABLE",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O6"
    },
    "mandatory": true,
    "query_identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q6"
    },
    "requirement": "O6",
    "satisfaction": "Identify authoritative behavior documentation, deferred scope and protected validation policy/configuration without changing exclusions or coverage.",
    "task_clause": "O6. Update `src/devtools/resources/filesystem/docs/io.md`, the filesystem overview and roadmap, and public API documentation where needed to describe the acquisition bound and remaining limitations accurately. Preserve existing callers and the protected development validation profile in `docs/development/validation.md`, `scripts/validate_development.py` and `pyproject.toml`; run the protected profile, Ruff, formatting, mypy and diff checks. Do not add binary codecs, new file formats, streaming format parsers, secure filesystem policy or production retrieval changes.\n",
    "task_span": {
      "end": 3315,
      "start": 2742
    },
    "title": "Documentation and protected validation"
  }
]
```

## Frozen queries

```json
[
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 7,
          "normalized_term": "reading",
          "observed_text": "reading",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 10,
          "normalized_term": "py",
          "observed_text": "py",
          "start": 8
        },
        {
          "encounter_ordinal": 2,
          "end": 15,
          "normalized_term": "read",
          "observed_text": "read",
          "start": 11
        },
        {
          "encounter_ordinal": 3,
          "end": 26,
          "normalized_term": "read_bytes",
          "observed_text": "read_bytes",
          "start": 16
        },
        {
          "encounter_ordinal": 4,
          "end": 39,
          "normalized_term": "resolvedpath",
          "observed_text": "ResolvedPath",
          "start": 27
        },
        {
          "encounter_ordinal": 5,
          "end": 51,
          "normalized_term": "file_format",
          "observed_text": "file_format",
          "start": 40
        },
        {
          "encounter_ordinal": 6,
          "end": 61,
          "normalized_term": "max_bytes",
          "observed_text": "max_bytes",
          "start": 52
        },
        {
          "encounter_ordinal": 7,
          "end": 84,
          "normalized_term": "default_max_read_bytes",
          "observed_text": "DEFAULT_MAX_READ_BYTES",
          "start": 62
        },
        {
          "encounter_ordinal": 8,
          "end": 91,
          "normalized_term": "finite",
          "observed_text": "finite",
          "start": 85
        },
        {
          "encounter_ordinal": 9,
          "end": 101,
          "normalized_term": "unbounded",
          "observed_text": "unbounded",
          "start": 92
        },
        {
          "encounter_ordinal": 10,
          "end": 110,
          "normalized_term": "negative",
          "observed_text": "negative",
          "start": 102
        },
        {
          "encounter_ordinal": 11,
          "end": 115,
          "normalized_term": "zero",
          "observed_text": "zero",
          "start": 111
        },
        {
          "encounter_ordinal": 12,
          "end": 121,
          "normalized_term": "exact",
          "observed_text": "exact",
          "start": 116
        },
        {
          "encounter_ordinal": 13,
          "end": 126,
          "normalized_term": "byte",
          "observed_text": "byte",
          "start": 122
        },
        {
          "encounter_ordinal": 14,
          "end": 135,
          "normalized_term": "boundary",
          "observed_text": "boundary",
          "start": 127
        },
        {
          "encounter_ordinal": 15,
          "end": 143,
          "normalized_term": "growing",
          "observed_text": "growing",
          "start": 136
        },
        {
          "encounter_ordinal": 16,
          "end": 148,
          "normalized_term": "file",
          "observed_text": "file",
          "start": 144
        }
      ],
      "text": "reading.py read read_bytes ResolvedPath file_format max_bytes DEFAULT_MAX_READ_BYTES finite unbounded negative zero exact byte boundary growing file"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q1"
    },
    "normalized_terms": [
      "reading",
      "py",
      "read",
      "read_bytes",
      "resolvedpath",
      "file_format",
      "max_bytes",
      "default_max_read_bytes",
      "finite",
      "unbounded",
      "negative",
      "zero",
      "exact",
      "byte",
      "boundary",
      "growing",
      "file"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O1"
    },
    "text": "reading.py read read_bytes ResolvedPath file_format max_bytes DEFAULT_MAX_READ_BYTES finite unbounded negative zero exact byte boundary growing file"
  },
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 10,
          "normalized_term": "filesystem",
          "observed_text": "filesystem",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 18,
          "normalized_term": "bounded",
          "observed_text": "bounded",
          "start": 11
        },
        {
          "encounter_ordinal": 2,
          "end": 24,
          "normalized_term": "chunk",
          "observed_text": "chunk",
          "start": 19
        },
        {
          "encounter_ordinal": 3,
          "end": 36,
          "normalized_term": "acquisition",
          "observed_text": "acquisition",
          "start": 25
        },
        {
          "encounter_ordinal": 4,
          "end": 44,
          "normalized_term": "payload",
          "observed_text": "payload",
          "start": 37
        },
        {
          "encounter_ordinal": 5,
          "end": 50,
          "normalized_term": "bytes",
          "observed_text": "bytes",
          "start": 45
        },
        {
          "encounter_ordinal": 6,
          "end": 54,
          "normalized_term": "eof",
          "observed_text": "EOF",
          "start": 51
        },
        {
          "encounter_ordinal": 7,
          "end": 72,
          "normalized_term": "filetoolargeerror",
          "observed_text": "FileTooLargeError",
          "start": 55
        },
        {
          "encounter_ordinal": 8,
          "end": 79,
          "normalized_term": "stream",
          "observed_text": "stream",
          "start": 73
        },
        {
          "encounter_ordinal": 9,
          "end": 87,
          "normalized_term": "closure",
          "observed_text": "closure",
          "start": 80
        },
        {
          "encounter_ordinal": 10,
          "end": 94,
          "normalized_term": "memory",
          "observed_text": "memory",
          "start": 88
        },
        {
          "encounter_ordinal": 11,
          "end": 99,
          "normalized_term": "stat",
          "observed_text": "stat",
          "start": 95
        },
        {
          "encounter_ordinal": 12,
          "end": 108,
          "normalized_term": "snapshot",
          "observed_text": "snapshot",
          "start": 100
        },
        {
          "encounter_ordinal": 13,
          "end": 120,
          "normalized_term": "containment",
          "observed_text": "containment",
          "start": 109
        },
        {
          "encounter_ordinal": 14,
          "end": 134,
          "normalized_term": "authorization",
          "observed_text": "authorization",
          "start": 121
        },
        {
          "encounter_ordinal": 15,
          "end": 142,
          "normalized_term": "locking",
          "observed_text": "locking",
          "start": 135
        }
      ],
      "text": "filesystem bounded chunk acquisition payload bytes EOF FileTooLargeError stream closure memory stat snapshot containment authorization locking"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q2"
    },
    "normalized_terms": [
      "filesystem",
      "bounded",
      "chunk",
      "acquisition",
      "payload",
      "bytes",
      "eof",
      "filetoolargeerror",
      "stream",
      "closure",
      "memory",
      "stat",
      "snapshot",
      "containment",
      "authorization",
      "locking"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O2"
    },
    "text": "filesystem bounded chunk acquisition payload bytes EOF FileTooLargeError stream closure memory stat snapshot containment authorization locking"
  },
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 19,
          "normalized_term": "resolve_file_format",
          "observed_text": "resolve_file_format",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 33,
          "normalized_term": "resolve_codec",
          "observed_text": "resolve_codec",
          "start": 20
        },
        {
          "encounter_ordinal": 2,
          "end": 42,
          "normalized_term": "textfile",
          "observed_text": "TextFile",
          "start": 34
        },
        {
          "encounter_ordinal": 3,
          "end": 55,
          "normalized_term": "markdownfile",
          "observed_text": "MarkdownFile",
          "start": 43
        },
        {
          "encounter_ordinal": 4,
          "end": 63,
          "normalized_term": "csvfile",
          "observed_text": "CsvFile",
          "start": 56
        },
        {
          "encounter_ordinal": 5,
          "end": 78,
          "normalized_term": "jsonobjectfile",
          "observed_text": "JsonObjectFile",
          "start": 64
        },
        {
          "encounter_ordinal": 6,
          "end": 91,
          "normalized_term": "jsonlistfile",
          "observed_text": "JsonListFile",
          "start": 79
        },
        {
          "encounter_ordinal": 7,
          "end": 106,
          "normalized_term": "jsonscalarfile",
          "observed_text": "JsonScalarFile",
          "start": 92
        },
        {
          "encounter_ordinal": 8,
          "end": 110,
          "normalized_term": "utf",
          "observed_text": "UTF",
          "start": 107
        },
        {
          "encounter_ordinal": 9,
          "end": 112,
          "normalized_term": "8",
          "observed_text": "8",
          "start": 111
        },
        {
          "encounter_ordinal": 10,
          "end": 121,
          "normalized_term": "decoding",
          "observed_text": "decoding",
          "start": 113
        },
        {
          "encounter_ordinal": 11,
          "end": 130,
          "normalized_term": "encoding",
          "observed_text": "encoding",
          "start": 122
        },
        {
          "encounter_ordinal": 12,
          "end": 140,
          "normalized_term": "byte_size",
          "observed_text": "byte_size",
          "start": 131
        },
        {
          "encounter_ordinal": 13,
          "end": 145,
          "normalized_term": "line",
          "observed_text": "line",
          "start": 141
        },
        {
          "encounter_ordinal": 14,
          "end": 153,
          "normalized_term": "endings",
          "observed_text": "endings",
          "start": 146
        },
        {
          "encounter_ordinal": 15,
          "end": 171,
          "normalized_term": "textdecodingerror",
          "observed_text": "TextDecodingError",
          "start": 154
        }
      ],
      "text": "resolve_file_format resolve_codec TextFile MarkdownFile CsvFile JsonObjectFile JsonListFile JsonScalarFile UTF-8 decoding encoding byte_size line endings TextDecodingError"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q3"
    },
    "normalized_terms": [
      "resolve_file_format",
      "resolve_codec",
      "textfile",
      "markdownfile",
      "csvfile",
      "jsonobjectfile",
      "jsonlistfile",
      "jsonscalarfile",
      "utf",
      "8",
      "decoding",
      "encoding",
      "byte_size",
      "line",
      "endings",
      "textdecodingerror"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O3"
    },
    "text": "resolve_file_format resolve_codec TextFile MarkdownFile CsvFile JsonObjectFile JsonListFile JsonScalarFile UTF-8 decoding encoding byte_size line endings TextDecodingError"
  },
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 10,
          "normalized_term": "filesystem",
          "observed_text": "filesystem",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 18,
          "normalized_term": "reading",
          "observed_text": "reading",
          "start": 11
        },
        {
          "encounter_ordinal": 2,
          "end": 42,
          "normalized_term": "filesystemnotfounderror",
          "observed_text": "FilesystemNotFoundError",
          "start": 19
        },
        {
          "encounter_ordinal": 3,
          "end": 56,
          "normalized_term": "notafileerror",
          "observed_text": "NotAFileError",
          "start": 43
        },
        {
          "encounter_ordinal": 4,
          "end": 82,
          "normalized_term": "filesystempermissionerror",
          "observed_text": "FilesystemPermissionError",
          "start": 57
        },
        {
          "encounter_ordinal": 5,
          "end": 100,
          "normalized_term": "filetoolargeerror",
          "observed_text": "FileTooLargeError",
          "start": 83
        },
        {
          "encounter_ordinal": 6,
          "end": 116,
          "normalized_term": "fileformaterror",
          "observed_text": "FileFormatError",
          "start": 101
        },
        {
          "encounter_ordinal": 7,
          "end": 127,
          "normalized_term": "permission",
          "observed_text": "permission",
          "start": 117
        },
        {
          "encounter_ordinal": 8,
          "end": 134,
          "normalized_term": "stream",
          "observed_text": "stream",
          "start": 128
        },
        {
          "encounter_ordinal": 9,
          "end": 142,
          "normalized_term": "opening",
          "observed_text": "opening",
          "start": 135
        },
        {
          "encounter_ordinal": 10,
          "end": 148,
          "normalized_term": "chunk",
          "observed_text": "chunk",
          "start": 143
        },
        {
          "encounter_ordinal": 11,
          "end": 153,
          "normalized_term": "read",
          "observed_text": "read",
          "start": 149
        },
        {
          "encounter_ordinal": 12,
          "end": 159,
          "normalized_term": "write",
          "observed_text": "write",
          "start": 154
        },
        {
          "encounter_ordinal": 13,
          "end": 166,
          "normalized_term": "atomic",
          "observed_text": "atomic",
          "start": 160
        },
        {
          "encounter_ordinal": 14,
          "end": 172,
          "normalized_term": "paths",
          "observed_text": "paths",
          "start": 167
        },
        {
          "encounter_ordinal": 15,
          "end": 177,
          "normalized_term": "tool",
          "observed_text": "Tool",
          "start": 173
        },
        {
          "encounter_ordinal": 16,
          "end": 191,
          "normalized_term": "authorization",
          "observed_text": "authorization",
          "start": 178
        }
      ],
      "text": "filesystem reading FilesystemNotFoundError NotAFileError FilesystemPermissionError FileTooLargeError FileFormatError permission stream opening chunk read write atomic paths Tool authorization"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q4"
    },
    "normalized_terms": [
      "filesystem",
      "reading",
      "filesystemnotfounderror",
      "notafileerror",
      "filesystempermissionerror",
      "filetoolargeerror",
      "fileformaterror",
      "permission",
      "stream",
      "opening",
      "chunk",
      "read",
      "write",
      "atomic",
      "paths",
      "tool",
      "authorization"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O4"
    },
    "text": "filesystem reading FilesystemNotFoundError NotAFileError FilesystemPermissionError FileTooLargeError FileFormatError permission stream opening chunk read write atomic paths Tool authorization"
  },
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 5,
          "normalized_term": "tests",
          "observed_text": "tests",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 15,
          "normalized_term": "resources",
          "observed_text": "resources",
          "start": 6
        },
        {
          "encounter_ordinal": 2,
          "end": 26,
          "normalized_term": "filesystem",
          "observed_text": "filesystem",
          "start": 16
        },
        {
          "encounter_ordinal": 3,
          "end": 39,
          "normalized_term": "test_reading",
          "observed_text": "test_reading",
          "start": 27
        },
        {
          "encounter_ordinal": 4,
          "end": 42,
          "normalized_term": "py",
          "observed_text": "py",
          "start": 40
        },
        {
          "encounter_ordinal": 5,
          "end": 49,
          "normalized_term": "codecs",
          "observed_text": "codecs",
          "start": 43
        },
        {
          "encounter_ordinal": 6,
          "end": 56,
          "normalized_term": "models",
          "observed_text": "models",
          "start": 50
        },
        {
          "encounter_ordinal": 7,
          "end": 62,
          "normalized_term": "empty",
          "observed_text": "empty",
          "start": 57
        },
        {
          "encounter_ordinal": 8,
          "end": 67,
          "normalized_term": "zero",
          "observed_text": "zero",
          "start": 63
        },
        {
          "encounter_ordinal": 9,
          "end": 73,
          "normalized_term": "exact",
          "observed_text": "exact",
          "start": 68
        },
        {
          "encounter_ordinal": 10,
          "end": 78,
          "normalized_term": "over",
          "observed_text": "over",
          "start": 74
        },
        {
          "encounter_ordinal": 11,
          "end": 84,
          "normalized_term": "limit",
          "observed_text": "limit",
          "start": 79
        },
        {
          "encounter_ordinal": 12,
          "end": 93,
          "normalized_term": "negative",
          "observed_text": "negative",
          "start": 85
        },
        {
          "encounter_ordinal": 13,
          "end": 103,
          "normalized_term": "unbounded",
          "observed_text": "unbounded",
          "start": 94
        },
        {
          "encounter_ordinal": 14,
          "end": 110,
          "normalized_term": "growth",
          "observed_text": "growth",
          "start": 104
        },
        {
          "encounter_ordinal": 15,
          "end": 115,
          "normalized_term": "stat",
          "observed_text": "stat",
          "start": 111
        },
        {
          "encounter_ordinal": 16,
          "end": 121,
          "normalized_term": "short",
          "observed_text": "short",
          "start": 116
        },
        {
          "encounter_ordinal": 17,
          "end": 127,
          "normalized_term": "reads",
          "observed_text": "reads",
          "start": 122
        },
        {
          "encounter_ordinal": 18,
          "end": 131,
          "normalized_term": "eof",
          "observed_text": "EOF",
          "start": 128
        },
        {
          "encounter_ordinal": 19,
          "end": 139,
          "normalized_term": "closure",
          "observed_text": "closure",
          "start": 132
        },
        {
          "encounter_ordinal": 20,
          "end": 150,
          "normalized_term": "permission",
          "observed_text": "permission",
          "start": 140
        },
        {
          "encounter_ordinal": 21,
          "end": 160,
          "normalized_term": "multibyte",
          "observed_text": "multibyte",
          "start": 151
        },
        {
          "encounter_ordinal": 22,
          "end": 164,
          "normalized_term": "utf",
          "observed_text": "UTF",
          "start": 161
        },
        {
          "encounter_ordinal": 23,
          "end": 166,
          "normalized_term": "8",
          "observed_text": "8",
          "start": 165
        },
        {
          "encounter_ordinal": 24,
          "end": 174,
          "normalized_term": "invalid",
          "observed_text": "invalid",
          "start": 167
        },
        {
          "encounter_ordinal": 25,
          "end": 181,
          "normalized_term": "format",
          "observed_text": "format",
          "start": 175
        },
        {
          "encounter_ordinal": 26,
          "end": 190,
          "normalized_term": "override",
          "observed_text": "override",
          "start": 182
        }
      ],
      "text": "tests/resources/filesystem/test_reading.py codecs models empty zero exact over-limit negative unbounded growth stat short reads EOF closure permission multibyte UTF-8 invalid format override"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q5"
    },
    "normalized_terms": [
      "tests",
      "resources",
      "filesystem",
      "test_reading",
      "py",
      "codecs",
      "models",
      "empty",
      "zero",
      "exact",
      "over",
      "limit",
      "negative",
      "unbounded",
      "growth",
      "stat",
      "short",
      "reads",
      "eof",
      "closure",
      "permission",
      "multibyte",
      "utf",
      "8",
      "invalid",
      "format",
      "override"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O5"
    },
    "text": "tests/resources/filesystem/test_reading.py codecs models empty zero exact over-limit negative unbounded growth stat short reads EOF closure permission multibyte UTF-8 invalid format override"
  },
  {
    "all_term_multipliers": {
      "float_hex": "0x1.0000000000000p+0"
    },
    "analysis": {
      "observations": [
        {
          "encounter_ordinal": 0,
          "end": 3,
          "normalized_term": "src",
          "observed_text": "src",
          "start": 0
        },
        {
          "encounter_ordinal": 1,
          "end": 12,
          "normalized_term": "devtools",
          "observed_text": "devtools",
          "start": 4
        },
        {
          "encounter_ordinal": 2,
          "end": 22,
          "normalized_term": "resources",
          "observed_text": "resources",
          "start": 13
        },
        {
          "encounter_ordinal": 3,
          "end": 33,
          "normalized_term": "filesystem",
          "observed_text": "filesystem",
          "start": 23
        },
        {
          "encounter_ordinal": 4,
          "end": 38,
          "normalized_term": "docs",
          "observed_text": "docs",
          "start": 34
        },
        {
          "encounter_ordinal": 5,
          "end": 41,
          "normalized_term": "io",
          "observed_text": "io",
          "start": 39
        },
        {
          "encounter_ordinal": 6,
          "end": 44,
          "normalized_term": "md",
          "observed_text": "md",
          "start": 42
        },
        {
          "encounter_ordinal": 7,
          "end": 53,
          "normalized_term": "overview",
          "observed_text": "overview",
          "start": 45
        },
        {
          "encounter_ordinal": 8,
          "end": 61,
          "normalized_term": "roadmap",
          "observed_text": "roadmap",
          "start": 54
        },
        {
          "encounter_ordinal": 9,
          "end": 68,
          "normalized_term": "public",
          "observed_text": "public",
          "start": 62
        },
        {
          "encounter_ordinal": 10,
          "end": 72,
          "normalized_term": "api",
          "observed_text": "API",
          "start": 69
        },
        {
          "encounter_ordinal": 11,
          "end": 77,
          "normalized_term": "docs",
          "observed_text": "docs",
          "start": 73
        },
        {
          "encounter_ordinal": 12,
          "end": 89,
          "normalized_term": "development",
          "observed_text": "development",
          "start": 78
        },
        {
          "encounter_ordinal": 13,
          "end": 100,
          "normalized_term": "validation",
          "observed_text": "validation",
          "start": 90
        },
        {
          "encounter_ordinal": 14,
          "end": 103,
          "normalized_term": "md",
          "observed_text": "md",
          "start": 101
        },
        {
          "encounter_ordinal": 15,
          "end": 111,
          "normalized_term": "scripts",
          "observed_text": "scripts",
          "start": 104
        },
        {
          "encounter_ordinal": 16,
          "end": 132,
          "normalized_term": "validate_development",
          "observed_text": "validate_development",
          "start": 112
        },
        {
          "encounter_ordinal": 17,
          "end": 135,
          "normalized_term": "py",
          "observed_text": "py",
          "start": 133
        },
        {
          "encounter_ordinal": 18,
          "end": 145,
          "normalized_term": "pyproject",
          "observed_text": "pyproject",
          "start": 136
        },
        {
          "encounter_ordinal": 19,
          "end": 150,
          "normalized_term": "toml",
          "observed_text": "toml",
          "start": 146
        },
        {
          "encounter_ordinal": 20,
          "end": 160,
          "normalized_term": "protected",
          "observed_text": "protected",
          "start": 151
        },
        {
          "encounter_ordinal": 21,
          "end": 171,
          "normalized_term": "validation",
          "observed_text": "validation",
          "start": 161
        },
        {
          "encounter_ordinal": 22,
          "end": 176,
          "normalized_term": "ruff",
          "observed_text": "Ruff",
          "start": 172
        },
        {
          "encounter_ordinal": 23,
          "end": 187,
          "normalized_term": "formatting",
          "observed_text": "formatting",
          "start": 177
        },
        {
          "encounter_ordinal": 24,
          "end": 192,
          "normalized_term": "mypy",
          "observed_text": "mypy",
          "start": 188
        },
        {
          "encounter_ordinal": 25,
          "end": 199,
          "normalized_term": "binary",
          "observed_text": "binary",
          "start": 193
        },
        {
          "encounter_ordinal": 26,
          "end": 207,
          "normalized_term": "formats",
          "observed_text": "formats",
          "start": 200
        },
        {
          "encounter_ordinal": 27,
          "end": 217,
          "normalized_term": "streaming",
          "observed_text": "streaming",
          "start": 208
        },
        {
          "encounter_ordinal": 28,
          "end": 226,
          "normalized_term": "security",
          "observed_text": "security",
          "start": 218
        }
      ],
      "text": "src/devtools/resources/filesystem/docs/io.md overview roadmap public API docs/development/validation.md scripts/validate_development.py pyproject.toml protected validation Ruff formatting mypy binary formats streaming security"
    },
    "authoring": "One query authored from this task clause before any prospective document statistics/rank; identical for both arms; no reformulation.",
    "identity": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "Q6"
    },
    "normalized_terms": [
      "src",
      "devtools",
      "resources",
      "filesystem",
      "docs",
      "io",
      "md",
      "overview",
      "roadmap",
      "public",
      "api",
      "development",
      "validation",
      "scripts",
      "validate_development",
      "py",
      "pyproject",
      "toml",
      "protected",
      "ruff",
      "formatting",
      "mypy",
      "binary",
      "formats",
      "streaming",
      "security"
    ],
    "obligation": {
      "task": {
        "value": "case-0015-strict-bounded-filesystem-read-v1"
      },
      "value": "O6"
    },
    "text": "src/devtools/resources/filesystem/docs/io.md overview roadmap public API docs/development/validation.md scripts/validate_development.py pyproject.toml protected validation Ruff formatting mypy binary formats streaming security"
  }
]
```

## Frozen scorer_semantics

```json
{
  "CONTENT": "RepositoryTextDocument.text: exact decoded whole-resource UTF-8 text, not a window or AST view.",
  "FILENAME": "PurePosixPath(resource.address.value).stem: final basename without final suffix; no directories, extension field or full path. Canonical iter_lexical_spans on that stem.",
  "analysis": "Query and both fields: canonical Unicode regex \\w+ spans, casefold. Underscores remain inside words; no identifier splitting, stemming or stopwords. Query duplicates retained as observations; distinct terms score once in first encounter order.",
  "b_content": {
    "float_hex": "0x1.8000000000000p-1"
  },
  "b_filename": {
    "float_hex": "0x1.8000000000000p-1"
  },
  "candidate": "Positive native content OR filename term matches; full maximum_results >= N. With positive IDF/settings these are exactly positive-score resources.",
  "canonical_sources": [
    "src/devtools/context/retrieval/lexical/analysis.py",
    "src/devtools/context/retrieval/lexical/bm25.py",
    "src/devtools/context/retrieval/lexical/filename.py",
    "src/devtools/context/retrieval/lexical/scoring.py",
    "src/devtools/context/retrieval/lexical/statistics.py",
    "src/devtools/context/retrieval/lexical/index.py"
  ],
  "df": "Independent field df counts documents with at least one field occurrence; N is all eligible resource documents in both fields.",
  "filename_coefficient": {
    "float_hex": "0x1.0000000000000p-2"
  },
  "idf": "Each field independently: ln(1 + (N - df_field + 0.5)/(df_field + 0.5)).",
  "k1": {
    "float_hex": "0x1.3333333333333p+0"
  },
  "length": "Each field length is its own observation count. Each average is total field length divided by N including zero-length field documents; empty corpus average 0.",
  "not_bm25f": "Independent field IDFs and independent saturations precede additive channel combination. True BM25F requires combined normalized tf before one saturation and one union IDF.",
  "provenance": "Native result retains query observations, content statistics/index, independent filename index, both channel scores and every contributing term tf, df, idf, length, average and score.",
  "score": "sum(content term contributions in distinct query encounter order) + 0.25 * sum(filename term contributions in distinct query encounter order)",
  "term": "idf_field * tf_field * (k1+1) / (tf_field + k1*(1-b+b*length_field/average_field_length))",
  "ties": "Descending score, then original native document collection position; full candidate enumeration before result bound."
}
```

## Frozen bm25f_formula

```json
{
  "arithmetic": "Python float, fixed grouping and field/query order; every floating input/intermediate/output serialized as float.hex; do not regroup native A channels.",
  "combined_tf": "sum(field_weight_f * normalized_tf_f) in CONTENT then FILENAME order",
  "df_union": "Count each eligible resource document once if t occurs in CONTENT OR FILENAME; never twice.",
  "document_score": "sum term_score in distinct canonical query encounter order; every query multiplier = 1.0",
  "empty_field": "If tf=0 normalized tf=0. If average=0 all field lengths/tfs must be zero: disclosed denominator=1 convention with zero contribution. No division by zero. Zero-length document in nonempty field may have denominator=0 when synthetic b=1, but tf=0 still contributes zero.",
  "idf_union": "ln(1 + (N - df_union + 0.5)/(df_union + 0.5)) using canonical calculate_bm25_inverse_document_frequency",
  "invariants": [
    "ONE aggregated tf",
    "ONE union IDF",
    "ONE saturation per term/document",
    "Only CONTENT and FILENAME",
    "Exact native tokens",
    "Identical A/B positive candidates",
    "Canonical collection-order ties"
  ],
  "normalized_tf": "tf_f / (1 - b_f + b_f * field_length_f / average_field_length_f)",
  "term_score": "idf_union * ((k1+1)*combined_tf) / (k1+combined_tf)"
}
```

## Frozen parameters

```json
{
  "b_content": {
    "float_hex": "0x1.8000000000000p-1"
  },
  "b_filename": {
    "float_hex": "0x1.8000000000000p-1"
  },
  "content_weight": {
    "float_hex": "0x1.0000000000000p+0"
  },
  "filename_weight": {
    "float_hex": "0x1.0000000000000p-2"
  },
  "k1": {
    "float_hex": "0x1.3333333333333p+0"
  }
}
```

## Execution, journal, statistics and mechanical checks

```json
{
  "SEARCH_POLICY_FAILURE": "NOT_ASSESSED",
  "attempt_1": "FAILED_AUDIT_ONLY; no treatment executed",
  "attempt_2": "AUTHORITATIVE STAGE B CAPTURE",
  "bm25f_union_statistics_preparations": 1,
  "candidate_counts": {
    "Q1": 290,
    "Q2": 307,
    "Q3": 156,
    "Q4": 221,
    "Q5": 425,
    "Q6": 408
  },
  "candidate_identity": "PASS",
  "case": "0015",
  "decomposition_reconstruction": "PASS",
  "diagnostic_aggregates": {
    "Q1": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 18014398509481984,
          "numerator": -50814154605246513
        },
        "float_display": {
          "float_hex": "-0x1.690e68a59d706p+1"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 2251799813685248,
          "numerator": 2597204250323703
        },
        "float_display": {
          "float_hex": "0x1.27449797fd5eep+0"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 36028797018963968,
          "numerator": -76116457520411753
        },
        "float_display": {
          "float_hex": "-0x1.0e6b83cc10b47p+1"
        }
      }
    },
    "Q2": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 2251799813685248,
          "numerator": -9491938640040207
        },
        "float_display": {
          "float_hex": "-0x1.0dc6f176f4888p+2"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 2251799813685248,
          "numerator": 4125828183457719
        },
        "float_display": {
          "float_hex": "0x1.d50d6768eff6ep+0"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 18014398509481984,
          "numerator": -74201940588152911
        },
        "float_display": {
          "float_hex": "-0x1.079e459666c85p+2"
        }
      }
    },
    "Q3": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 18014398509481984,
          "numerator": -17
        },
        "float_display": {
          "float_hex": "-0x1.1000000000000p-50"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 1,
          "numerator": 0
        },
        "float_display": {
          "float_hex": "0x0.0p+0"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 18014398509481984,
          "numerator": -581
        },
        "float_display": {
          "float_hex": "-0x1.2280000000000p-45"
        }
      }
    },
    "Q4": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 36028797018963968,
          "numerator": -100643496130229603
        },
        "float_display": {
          "float_hex": "-0x1.658eb9fbcbb56p+1"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 2251799813685248,
          "numerator": 2506394462032215
        },
        "float_display": {
          "float_hex": "0x1.1cf1adf2722aep+0"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 36028797018963968,
          "numerator": -76115292749222653
        },
        "float_display": {
          "float_hex": "-0x1.0e6a749a4ad30p+1"
        }
      }
    },
    "Q5": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 2251799813685248,
          "numerator": -12452040006446369
        },
        "float_display": {
          "float_hex": "-0x1.61e883ea81690p+2"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 1125899906842624,
          "numerator": 4922916864618931
        },
        "float_display": {
          "float_hex": "0x1.17d5de6f971b3p+2"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 36028797018963968,
          "numerator": -563863082912188449
        },
        "float_display": {
          "float_hex": "-0x1.f4cf9f21bc021p+3"
        }
      }
    },
    "Q6": {
      "cross_field_single_saturation_delta": {
        "exact": {
          "denominator": 18014398509481984,
          "numerator": -186646091395663717
        },
        "float_display": {
          "float_hex": "-0x1.4b8cd0cc2d43bp+3"
        }
      },
      "pre_saturation_weight_delta": {
        "exact": {
          "denominator": 562949953421312,
          "numerator": 10036499483136047
        },
        "float_display": {
          "float_hex": "0x1.1d412513d8818p+4"
        }
      },
      "union_idf_delta": {
        "exact": {
          "denominator": 36028797018963968,
          "numerator": -954030778502829377
        },
        "float_display": {
          "float_hex": "-0x1.a7acbe072e6abp+4"
        }
      }
    }
  },
  "effectiveness": "UNKNOWN",
  "execution": "case-0015-stage-b-2",
  "failures": 0,
  "field_statistics": {
    "N": 515,
    "content_average_length": {
      "float_hex": "0x1.d8c755007f412p+8"
    },
    "distinct_union_terms": 9251,
    "filename_average_length": {
      "float_hex": "0x1.82bbe626c5d74p+0"
    }
  },
  "formula_reconstruction": "PASS",
  "frame": {
    "corpus_id": "4c54a18a6fba0aa33c248a2f4776627bbfcffba740cb8e752a6f47662b1d33fa",
    "repository_id": "5cf96d9e-d6a5-44a6-83d3-1e24f6e00009",
    "representation": "native exact decoded whole UTF-8 text; no windows/subtokens/fields changed",
    "resource_count": 515,
    "resource_order": "canonical resource address ascending",
    "snapshot_id": "9846f13fdce6c8fc896f673fb7d1f6e0a40b0aeeea24ad71b73d4527e367c494",
    "source_head": "53a1d087a24e7880f305e167e2d5f3bbb727ff61"
  },
  "gold": "ABSENT",
  "journal_events": 34,
  "journal_pairs": 17,
  "largest_movements": {
    "Q1": {
      "downward": [
        {
          "A_rank": 151,
          "A_score": {
            "float_hex": "0x1.2a25d458f5f68p+2"
          },
          "B_rank": 207,
          "B_score": {
            "float_hex": "0x1.88d5aec46ffc5p+1"
          },
          "address": "src/devtools/resources/filesystem/models/markdown/file.py",
          "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
          "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
          "score_delta": {
            "float_hex": "-0x1.96ebf3daf7e16p+0"
          },
          "upward_positions": -56
        },
        {
          "A_rank": 51,
          "A_score": {
            "float_hex": "0x1.1a601d04e79bcp+3"
          },
          "B_rank": 60,
          "B_score": {
            "float_hex": "0x1.05d8086a3f962p+3"
          },
          "address": "docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md",
          "content_identity": "270a3fddbbbc84c6e4bbbb9d109343a4027316182364f1282885b8868374fcfe",
          "document_identity": "9326dbd823befd40c56e5d011c4e5207ef1bda0e3693e9844b01f598fd73186e",
          "score_delta": {
            "float_hex": "-0x1.488149aa805a0p-1"
          },
          "upward_positions": -9
        },
        {
          "A_rank": 1,
          "A_score": {
            "float_hex": "0x1.b42ae8e1e23ebp+5"
          },
          "B_rank": 1,
          "B_score": {
            "float_hex": "0x1.a7c6d39d09080p+5"
          },
          "address": "src/devtools/resources/filesystem/reading.py",
          "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
          "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
          "score_delta": {
            "float_hex": "-0x1.8c82a89b26d60p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 2,
          "A_score": {
            "float_hex": "0x1.95c573ece577fp+5"
          },
          "B_rank": 2,
          "B_score": {
            "float_hex": "0x1.95c573ece577fp+5"
          },
          "address": "tests/resources/filesystem/test_reading.py",
          "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
          "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 3,
          "A_score": {
            "float_hex": "0x1.537c174edbc44p+5"
          },
          "B_rank": 3,
          "B_score": {
            "float_hex": "0x1.537c174edbc44p+5"
          },
          "address": "src/devtools/resources/filesystem/docs/io.md",
          "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
          "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        }
      ],
      "upward": [
        {
          "A_rank": 52,
          "A_score": {
            "float_hex": "0x1.1735be5990538p+3"
          },
          "B_rank": 51,
          "B_score": {
            "float_hex": "0x1.1735be5990538p+3"
          },
          "address": "tests/agents/conversation/test_live.py",
          "content_identity": "8d785c1dd2043953ec624b38a3f7875ed56523421666f0cdabdadf3ff468bf20",
          "document_identity": "bcf1ba96f5651167486aa790e81cc04a5fded625f7b63324a8ad6016a3cb2342",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 53,
          "A_score": {
            "float_hex": "0x1.173143e258555p+3"
          },
          "B_rank": 52,
          "B_score": {
            "float_hex": "0x1.173143e258555p+3"
          },
          "address": "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
          "content_identity": "1978bad723268d286560db009f6ef5aeff4a6186563711b1571813c71166e127",
          "document_identity": "93e43be4313117786436dcfefe158087b9dd36571d305602382f986632bd2f80",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 54,
          "A_score": {
            "float_hex": "0x1.0d92467b13e08p+3"
          },
          "B_rank": 53,
          "B_score": {
            "float_hex": "0x1.0d92467b13e08p+3"
          },
          "address": "src/devtools/resources/filesystem/codecs/markdown.py",
          "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
          "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 55,
          "A_score": {
            "float_hex": "0x1.0c620b3cfb3acp+3"
          },
          "B_rank": 54,
          "B_score": {
            "float_hex": "0x1.0c620b3cfb3acp+3"
          },
          "address": "tests/context/repository/test_corpus.py",
          "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
          "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 56,
          "A_score": {
            "float_hex": "0x1.0c530d6960ddfp+3"
          },
          "B_rank": 55,
          "B_score": {
            "float_hex": "0x1.0c530d6960de0p+3"
          },
          "address": "tests/context/retrieval/lexical/test_index.py",
          "content_identity": "50cafbcaede0c499cbffc96c26e4c61bb7a2263a5652a5d213d2730c56273e0e",
          "document_identity": "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95",
          "score_delta": {
            "float_hex": "0x1.0000000000000p-49"
          },
          "upward_positions": 1
        }
      ]
    },
    "Q2": {
      "downward": [
        {
          "A_rank": 57,
          "A_score": {
            "float_hex": "0x1.d6d7bd8add081p+2"
          },
          "B_rank": 98,
          "B_score": {
            "float_hex": "0x1.6cacbbb151a4cp+2"
          },
          "address": "src/devtools/tools/filesystem.py",
          "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
          "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
          "score_delta": {
            "float_hex": "-0x1.a8ac07662d8d4p+0"
          },
          "upward_positions": -41
        },
        {
          "A_rank": 96,
          "A_score": {
            "float_hex": "0x1.79e8efc8db8bcp+2"
          },
          "B_rank": 134,
          "B_score": {
            "float_hex": "0x1.0e7fb0032ddedp+2"
          },
          "address": "src/devtools/context/repository/snapshot.py",
          "content_identity": "492cd324fd1ebacae7f990fa534ca1251d41aeaa65f2b385155f88a56c835098",
          "document_identity": "71672ee68667154dfaa647de6e53e8680fc81f07cdb4281e8fca2a4ce41be6d7",
          "score_delta": {
            "float_hex": "-0x1.ada4ff16b6b3cp+0"
          },
          "upward_positions": -38
        },
        {
          "A_rank": 34,
          "A_score": {
            "float_hex": "0x1.1ab56afa12e41p+3"
          },
          "B_rank": 54,
          "B_score": {
            "float_hex": "0x1.e04a34f8bd96cp+2"
          },
          "address": "src/devtools/context/python/classes/containment.py",
          "content_identity": "47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f",
          "document_identity": "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
          "score_delta": {
            "float_hex": "-0x1.548283eda0c58p+0"
          },
          "upward_positions": -20
        },
        {
          "A_rank": 36,
          "A_score": {
            "float_hex": "0x1.16c68afc4a1ddp+3"
          },
          "B_rank": 55,
          "B_score": {
            "float_hex": "0x1.d9dfca07b4b9ap+2"
          },
          "address": "src/devtools/context/python/function/containment.py",
          "content_identity": "7af4524a28e61dc608e35c9ab4ff34c0bc486fb1ef54a3521f9fb0735eb25d69",
          "document_identity": "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
          "score_delta": {
            "float_hex": "-0x1.4eb52fc37e080p+0"
          },
          "upward_positions": -19
        },
        {
          "A_rank": 10,
          "A_score": {
            "float_hex": "0x1.01cace3a4b345p+4"
          },
          "B_rank": 11,
          "B_score": {
            "float_hex": "0x1.f2b5c520c7213p+3"
          },
          "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
          "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
          "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
          "score_delta": {
            "float_hex": "-0x1.0dfd753cf4770p-1"
          },
          "upward_positions": -1
        }
      ],
      "upward": [
        {
          "A_rank": 37,
          "A_score": {
            "float_hex": "0x1.0aea289688cfbp+3"
          },
          "B_rank": 35,
          "B_score": {
            "float_hex": "0x1.0aea289688cfcp+3"
          },
          "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
          "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
          "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
          "score_delta": {
            "float_hex": "0x1.0000000000000p-49"
          },
          "upward_positions": 2
        },
        {
          "A_rank": 38,
          "A_score": {
            "float_hex": "0x1.081915bece6a2p+3"
          },
          "B_rank": 36,
          "B_score": {
            "float_hex": "0x1.081915bece6a3p+3"
          },
          "address": "tests/tools/test_command.py",
          "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
          "document_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
          "score_delta": {
            "float_hex": "0x1.0000000000000p-49"
          },
          "upward_positions": 2
        },
        {
          "A_rank": 39,
          "A_score": {
            "float_hex": "0x1.02f99775feb94p+3"
          },
          "B_rank": 37,
          "B_score": {
            "float_hex": "0x1.02f99775feb94p+3"
          },
          "address": "src/devtools/resources/filesystem/codecs/text.py",
          "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
          "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 2
        },
        {
          "A_rank": 40,
          "A_score": {
            "float_hex": "0x1.008e2a248c50fp+3"
          },
          "B_rank": 38,
          "B_score": {
            "float_hex": "0x1.008e2a248c50ep+3"
          },
          "address": "src/devtools/resources/filesystem/codecs/markdown.py",
          "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
          "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-49"
          },
          "upward_positions": 2
        },
        {
          "A_rank": 41,
          "A_score": {
            "float_hex": "0x1.fbbab7a47b51cp+2"
          },
          "B_rank": 39,
          "B_score": {
            "float_hex": "0x1.fbbab7a47b51bp+2"
          },
          "address": "tests/tools/test_runtime_integration.py",
          "content_identity": "82979c703980afb5f5508789155c45bb06adc7a5a7d6a973c74c251b602cde1e",
          "document_identity": "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-50"
          },
          "upward_positions": 2
        }
      ]
    },
    "Q3": {
      "downward": [
        {
          "A_rank": 1,
          "A_score": {
            "float_hex": "0x1.9f0dbfcf305c5p+5"
          },
          "B_rank": 1,
          "B_score": {
            "float_hex": "0x1.9f0dbfcf305c5p+5"
          },
          "address": "src/devtools/resources/filesystem/__init__.py",
          "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
          "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 2,
          "A_score": {
            "float_hex": "0x1.66b78c80ef727p+5"
          },
          "B_rank": 2,
          "B_score": {
            "float_hex": "0x1.66b78c80ef727p+5"
          },
          "address": "tests/resources/filesystem/test_reading.py",
          "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
          "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 3,
          "A_score": {
            "float_hex": "0x1.513290bcf8062p+5"
          },
          "B_rank": 3,
          "B_score": {
            "float_hex": "0x1.513290bcf8062p+5"
          },
          "address": "tests/resources/filesystem/codecs/test_json.py",
          "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
          "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 4,
          "A_score": {
            "float_hex": "0x1.41976a8e4bb95p+5"
          },
          "B_rank": 4,
          "B_score": {
            "float_hex": "0x1.41976a8e4bb94p+5"
          },
          "address": "src/devtools/resources/filesystem/codecs/json.py",
          "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
          "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-47"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 5,
          "A_score": {
            "float_hex": "0x1.3839d329b8281p+5"
          },
          "B_rank": 5,
          "B_score": {
            "float_hex": "0x1.3839d329b8280p+5"
          },
          "address": "src/devtools/resources/filesystem/models/__init__.py",
          "content_identity": "e09ae5eeb0da9afd9f4921634debfd2af6e9fbcf84a98450526c62f52e5fcf5c",
          "document_identity": "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-47"
          },
          "upward_positions": 0
        }
      ],
      "upward": [
        {
          "A_rank": 1,
          "A_score": {
            "float_hex": "0x1.9f0dbfcf305c5p+5"
          },
          "B_rank": 1,
          "B_score": {
            "float_hex": "0x1.9f0dbfcf305c5p+5"
          },
          "address": "src/devtools/resources/filesystem/__init__.py",
          "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
          "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 2,
          "A_score": {
            "float_hex": "0x1.66b78c80ef727p+5"
          },
          "B_rank": 2,
          "B_score": {
            "float_hex": "0x1.66b78c80ef727p+5"
          },
          "address": "tests/resources/filesystem/test_reading.py",
          "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
          "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 3,
          "A_score": {
            "float_hex": "0x1.513290bcf8062p+5"
          },
          "B_rank": 3,
          "B_score": {
            "float_hex": "0x1.513290bcf8062p+5"
          },
          "address": "tests/resources/filesystem/codecs/test_json.py",
          "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
          "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 4,
          "A_score": {
            "float_hex": "0x1.41976a8e4bb95p+5"
          },
          "B_rank": 4,
          "B_score": {
            "float_hex": "0x1.41976a8e4bb94p+5"
          },
          "address": "src/devtools/resources/filesystem/codecs/json.py",
          "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
          "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-47"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 5,
          "A_score": {
            "float_hex": "0x1.3839d329b8281p+5"
          },
          "B_rank": 5,
          "B_score": {
            "float_hex": "0x1.3839d329b8280p+5"
          },
          "address": "src/devtools/resources/filesystem/models/__init__.py",
          "content_identity": "e09ae5eeb0da9afd9f4921634debfd2af6e9fbcf84a98450526c62f52e5fcf5c",
          "document_identity": "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
          "score_delta": {
            "float_hex": "-0x1.0000000000000p-47"
          },
          "upward_positions": 0
        }
      ]
    },
    "Q4": {
      "downward": [
        {
          "A_rank": 40,
          "A_score": {
            "float_hex": "0x1.1eccbac5a9f47p+3"
          },
          "B_rank": 46,
          "B_score": {
            "float_hex": "0x1.0c127ade9d24ep+3"
          },
          "address": "docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md",
          "content_identity": "acee48b767ae4d30136ffc2ae4044e3b5be9fd2999846dd99869b3ee44287602",
          "document_identity": "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
          "score_delta": {
            "float_hex": "-0x1.2ba3fe70ccf90p-1"
          },
          "upward_positions": -6
        },
        {
          "A_rank": 1,
          "A_score": {
            "float_hex": "0x1.a5d8cbc4525f4p+5"
          },
          "B_rank": 1,
          "B_score": {
            "float_hex": "0x1.a5d8cbc4525f4p+5"
          },
          "address": "src/devtools/resources/filesystem/__init__.py",
          "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
          "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 2,
          "A_score": {
            "float_hex": "0x1.9547372ed5069p+5"
          },
          "B_rank": 2,
          "B_score": {
            "float_hex": "0x1.88e321e9fbcfep+5"
          },
          "address": "src/devtools/resources/filesystem/reading.py",
          "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
          "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
          "score_delta": {
            "float_hex": "-0x1.8c82a89b26d60p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 3,
          "A_score": {
            "float_hex": "0x1.75028cf16f161p+5"
          },
          "B_rank": 3,
          "B_score": {
            "float_hex": "0x1.75028cf16f161p+5"
          },
          "address": "src/devtools/resources/filesystem/docs/overview.md",
          "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
          "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        },
        {
          "A_rank": 4,
          "A_score": {
            "float_hex": "0x1.48599830051bap+5"
          },
          "B_rank": 4,
          "B_score": {
            "float_hex": "0x1.48599830051bap+5"
          },
          "address": "tests/resources/filesystem/test_reading.py",
          "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
          "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 0
        }
      ],
      "upward": [
        {
          "A_rank": 41,
          "A_score": {
            "float_hex": "0x1.195d7afd0b8ffp+3"
          },
          "B_rank": 40,
          "B_score": {
            "float_hex": "0x1.195d7afd0b900p+3"
          },
          "address": "src/devtools/resources/commands/docs/events.md",
          "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
          "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
          "score_delta": {
            "float_hex": "0x1.0000000000000p-49"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 42,
          "A_score": {
            "float_hex": "0x1.18bc2b763e677p+3"
          },
          "B_rank": 41,
          "B_score": {
            "float_hex": "0x1.18bc2b763e677p+3"
          },
          "address": "tests/agents/integrations/codex/test_live.py",
          "content_identity": "b705ab7d34b2b7327ec5e86563123101bb9f293b15260a627905fd8524549e64",
          "document_identity": "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 43,
          "A_score": {
            "float_hex": "0x1.113130b6ca921p+3"
          },
          "B_rank": 42,
          "B_score": {
            "float_hex": "0x1.113130b6ca921p+3"
          },
          "address": "src/devtools/observability/evidence/docs/overview.md",
          "content_identity": "98431aec7bfdfc9c7a4396d6921a5f4174312ccb791b93741b03f8eb0b27c4e7",
          "document_identity": "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 44,
          "A_score": {
            "float_hex": "0x1.0da492b205c43p+3"
          },
          "B_rank": 43,
          "B_score": {
            "float_hex": "0x1.0da492b205c43p+3"
          },
          "address": "docs/backlog/items/B-0012-investigate-governed-effect-semantics.md",
          "content_identity": "27922033df5cb70819286d39b97da02a3f22d733a83fb026eae4d1df43c7299a",
          "document_identity": "50a13c505510c08acbde149c4e774c9f0a09089b5f4ae9bf81796ba79b670990",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        },
        {
          "A_rank": 45,
          "A_score": {
            "float_hex": "0x1.0d3b5202e3ca7p+3"
          },
          "B_rank": 44,
          "B_score": {
            "float_hex": "0x1.0d3b5202e3ca7p+3"
          },
          "address": "src/devtools/resources/filesystem/docs/markdown.md",
          "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
          "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 1
        }
      ]
    },
    "Q5": {
      "downward": [
        {
          "A_rank": 306,
          "A_score": {
            "float_hex": "0x1.46f6ddc7bdf7ep+1"
          },
          "B_rank": 408,
          "B_score": {
            "float_hex": "0x1.82bc4b3337867p+0"
          },
          "address": "src/devtools/models/interaction/models.py",
          "content_identity": "6eb9d64480b0c9ab9ad6e0185f63006d0b7635e824cac8d7c111211d9926466f",
          "document_identity": "4e1cded7a20da8216abfbe52f6dc2db1ca2c04cdede2d40793162e86c4d87d17",
          "score_delta": {
            "float_hex": "-0x1.0b31705c44695p+0"
          },
          "upward_positions": -102
        },
        {
          "A_rank": 302,
          "A_score": {
            "float_hex": "0x1.5cc2182af6e48p+1"
          },
          "B_rank": 394,
          "B_score": {
            "float_hex": "0x1.a60c88c6210eap+0"
          },
          "address": "src/devtools/agents/integrations/codex/models.py",
          "content_identity": "b8ef93dea4e2d85e83c282eb31ab8908a4ada43b1e31496a399d0bc8a42b2d90",
          "document_identity": "63527658a4ba89ad41939312396e74d168f278683e3514100eeef7aebd289317",
          "score_delta": {
            "float_hex": "-0x1.1377a78fccba6p+0"
          },
          "upward_positions": -92
        },
        {
          "A_rank": 346,
          "A_score": {
            "float_hex": "0x1.b3df79c2fafe1p+0"
          },
          "B_rank": 392,
          "B_score": {
            "float_hex": "0x1.aac2ec260d29ep+0"
          },
          "address": "src/devtools/core/system/detection.py",
          "content_identity": "af034fbaecdf97680a7d6745336028ce10306daa0e3b7bce5cd8c10340e601c7",
          "document_identity": "4660ec8c908d0d8a71bc5badbc7082d62cfeb2d8c24848e513840b6e6acc05ce",
          "score_delta": {
            "float_hex": "-0x1.2391b39dba860p-5"
          },
          "upward_positions": -46
        },
        {
          "A_rank": 347,
          "A_score": {
            "float_hex": "0x1.b1843e01b625fp+0"
          },
          "B_rank": 393,
          "B_score": {
            "float_hex": "0x1.a8744c917fdd0p+0"
          },
          "address": "src/devtools/context/python/project_configuration/__init__.py",
          "content_identity": "b63c08a6a5b534fd4c41f8c1cd5b6408b3d38805e83ab4ee284d88efc7fe7470",
          "document_identity": "e7d8ec4568322dcbcd863cad67638b5765ea383b1957f0e60fbdf2616d95becc",
          "score_delta": {
            "float_hex": "-0x1.21fe2e06c91e0p-5"
          },
          "upward_positions": -46
        },
        {
          "A_rank": 300,
          "A_score": {
            "float_hex": "0x1.61b4b775ae3c7p+1"
          },
          "B_rank": 345,
          "B_score": {
            "float_hex": "0x1.ae3f232ba1596p+0"
          },
          "address": "src/devtools/core/system/models.py",
          "content_identity": "7c16b78f1616fa8b6dd89ef3a8be7db70121aa4af243a6f586ff4489e88523e9",
          "document_identity": "35afc8427151881bee7abba4e0af36c242d84551ec43524d590f3ed36ee6f9bb",
          "score_delta": {
            "float_hex": "-0x1.152a4bbfbb1f8p+0"
          },
          "upward_positions": -45
        }
      ],
      "upward": [
        {
          "A_rank": 348,
          "A_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "B_rank": 341,
          "B_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "address": "tests/agents/conversation/__init__.py",
          "content_identity": "e9c90fef7a2be899ab41d3d384bc2f24da729af15655ad1269467fac307391fd",
          "document_identity": "d1e153e2a1f735f75da9161230da521b8c8f741b609cb971bfa05bba82d61e4a",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 7
        },
        {
          "A_rank": 349,
          "A_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "B_rank": 342,
          "B_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "address": "tests/evaluation/__init__.py",
          "content_identity": "7b2ba91a1ed4b1b4e3416ef7323831b088a2ed08174d46e8727dc09ad718f69d",
          "document_identity": "a3386b3ff3e01f4b14c4647d1f0ad72cee9dc3aac8650570827b543e172882b5",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 7
        },
        {
          "A_rank": 350,
          "A_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "B_rank": 343,
          "B_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "address": "tests/observability/evidence/__init__.py",
          "content_identity": "3da89ca2ca4351ec7917dfe8968829b6eec8b7c99a4b5d0fbec90191a90f9591",
          "document_identity": "2f28363c4be5501df96c33cf4be4179701c00272a1a754d1df2264486bb7a0d7",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 7
        },
        {
          "A_rank": 351,
          "A_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "B_rank": 344,
          "B_score": {
            "float_hex": "0x1.aed213abeda2bp+0"
          },
          "address": "tests/persistence/__init__.py",
          "content_identity": "edb967950ec1437b730ec9317b1ddf71b553e84dcc71fff66825f0afa8f6ee5e",
          "document_identity": "19c8ab310844f246f4889dfbb4b029952f3172a3576b86e161c4f1d732494dcb",
          "score_delta": {
            "float_hex": "0x0.0p+0"
          },
          "upward_positions": 7
        },
        {
          "A_rank": 352,
          "A_score": {
            "float_hex": "0x1.ae31fb43bc4b7p+0"
          },
          "B_rank": 346,
          "B_score": {
            "float_hex": "0x1.ae31fb43bc4b8p+0"
          },
          "address": "tests/agents/__init__.py",
          "content_identity": "95cb59fa30a936329c46138d6d327cb5ece9753d4c3419617e61529f519add89",
          "document_identity": "752c56dd736f6067dcc19988e2e3e0e4bd1520851b0a0bab0082f41d18ed3e55",
          "score_delta": {
            "float_hex": "0x1.0000000000000p-52"
          },
          "upward_positions": 6
        }
      ]
    },
    "Q6": {
      "downward": [
        {
          "A_rank": 94,
          "A_score": {
            "float_hex": "0x1.1384fca53d68fp+3"
          },
          "B_rank": 114,
          "B_score": {
            "float_hex": "0x1.dbfe9fb2056edp+2"
          },
          "address": "src/devtools/resources/commands/docs/execution.md",
          "content_identity": "0494eb9c87561cd8bf45aa19d956edab17d7fe1b89abae5e5aa672e4949eb1f9",
          "document_identity": "562fb83e53618c6205f6efcd12f7eec0368bca5a850a79cac7e09e51dc876f7b",
          "score_delta": {
            "float_hex": "-0x1.2c2d6661d58c4p+0"
          },
          "upward_positions": -20
        },
        {
          "A_rank": 72,
          "A_score": {
            "float_hex": "0x1.547a5b0c71d59p+3"
          },
          "B_rank": 88,
          "B_score": {
            "float_hex": "0x1.1f64da1fac23ep+3"
          },
          "address": "src/devtools/tools/filesystem.py",
          "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
          "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
          "score_delta": {
            "float_hex": "-0x1.a8ac07662d8d8p+0"
          },
          "upward_positions": -16
        },
        {
          "A_rank": 124,
          "A_score": {
            "float_hex": "0x1.a6b8b4d0ea966p+2"
          },
          "B_rank": 140,
          "B_score": {
            "float_hex": "0x1.7fb91199e3881p+2"
          },
          "address": "tests/context/localization/test_kernel.py",
          "content_identity": "58d0404d46dd986aaa3c7efd943f9c34497913388912f6bfa3dc9b4c45e9dbd7",
          "document_identity": "52c66504cce0c20103cd504a32fbae74d9d907e11ac68b0c727fd3dedf78951f",
          "score_delta": {
            "float_hex": "-0x1.37fd19b838728p-1"
          },
          "upward_positions": -16
        },
        {
          "A_rank": 90,
          "A_score": {
            "float_hex": "0x1.1afac8c0ddebcp+3"
          },
          "B_rank": 105,
          "B_score": {
            "float_hex": "0x1.e8a3bd7e0e082p+2"
          },
          "address": "src/devtools/resources/commands/docs/command.md",
          "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
          "document_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
          "score_delta": {
            "float_hex": "-0x1.3547500eb73d8p+0"
          },
          "upward_positions": -15
        },
        {
          "A_rank": 89,
          "A_score": {
            "float_hex": "0x1.1c3465e78c87bp+3"
          },
          "B_rank": 103,
          "B_score": {
            "float_hex": "0x1.eab70750de22cp+2"
          },
          "address": "src/devtools/resources/commands/docs/events.md",
          "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
          "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
          "score_delta": {
            "float_hex": "-0x1.36c711f8ebb28p+0"
          },
          "upward_positions": -14
        }
      ],
      "upward": [
        {
          "A_rank": 198,
          "A_score": {
            "float_hex": "0x1.ee0552f873489p+1"
          },
          "B_rank": 181,
          "B_score": {
            "float_hex": "0x1.102f1a01820f7p+2"
          },
          "address": "src/devtools/evaluation/docs/overview.md",
          "content_identity": "f4bf6befadb975bc67b23dad16e10b41765327f1866d19d8521c0e5efbfcf7bf",
          "document_identity": "a85e192ce8cc90049355cc1274cbd99ab8ca3a47a5aa62c820c5bf5d80a2c8ff",
          "score_delta": {
            "float_hex": "0x1.92c7085486b28p-2"
          },
          "upward_positions": 17
        },
        {
          "A_rank": 199,
          "A_score": {
            "float_hex": "0x1.eae20727fcaffp+1"
          },
          "B_rank": 183,
          "B_score": {
            "float_hex": "0x1.0e9d741946c32p+2"
          },
          "address": "src/devtools/context/localization/routing/docs/overview.md",
          "content_identity": "22082bd1aff0e0e30609b53ac63c4b28c7897c442732ab58787304fe74a5ae0d",
          "document_identity": "3772b24b1207dd23238f873e96b4560efdad58ed5bc4398a5a091b2019c5c900",
          "score_delta": {
            "float_hex": "0x1.92c7085486b28p-2"
          },
          "upward_positions": 16
        },
        {
          "A_rank": 232,
          "A_score": {
            "float_hex": "0x1.7486f8c886bdep+1"
          },
          "B_rank": 216,
          "B_score": {
            "float_hex": "0x1.a6dfd9d317943p+1"
          },
          "address": "src/devtools/context/python/classes/docs/overview.md",
          "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
          "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
          "score_delta": {
            "float_hex": "0x1.92c7085486b28p-2"
          },
          "upward_positions": 16
        },
        {
          "A_rank": 113,
          "A_score": {
            "float_hex": "0x1.dd71a6b31be9cp+2"
          },
          "B_rank": 100,
          "B_score": {
            "float_hex": "0x1.f69e17386454fp+2"
          },
          "address": "src/devtools/core/identity/docs/overview.md",
          "content_identity": "49232ef5c3a6fca94691bd6dfe84468497d1e17958a349d56dfcd731730cd3b4",
          "document_identity": "fe91279815b097915f61055c22b9cb826efac26880e6a831bb43e6ba7fd0f38d",
          "score_delta": {
            "float_hex": "0x1.92c7085486b30p-2"
          },
          "upward_positions": 13
        },
        {
          "A_rank": 147,
          "A_score": {
            "float_hex": "0x1.6c69ecc103d4fp+2"
          },
          "B_rank": 135,
          "B_score": {
            "float_hex": "0x1.85965d464c401p+2"
          },
          "address": "src/devtools/models/benchmarks/docs/overview.md",
          "content_identity": "e06e6abd5f9c3422bbe5159810f443048d2b896174d4c3fcd756b21706bc6973",
          "document_identity": "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
          "score_delta": {
            "float_hex": "0x1.92c7085486b20p-2"
          },
          "upward_positions": 12
        }
      ]
    }
  },
  "native_arm_a_authenticity": "PASS",
  "native_content_index_builds": 1,
  "native_intrinsic_filename_builds": 7,
  "native_retries": 0,
  "operation_counts": {
    "fields:prepare": 1,
    "frame:prepare": 1,
    "index:native-prepare": 1,
    "query:Q1:A": 1,
    "query:Q1:B": 1,
    "query:Q2:A": 1,
    "query:Q2:B": 1,
    "query:Q3:A": 1,
    "query:Q3:B": 1,
    "query:Q4:A": 1,
    "query:Q4:B": 1,
    "query:Q5:A": 1,
    "query:Q5:B": 1,
    "query:Q6:A": 1,
    "query:Q6:B": 1,
    "query:reference": 1,
    "statistics:union-prepare": 1
  },
  "outcome": "NOT_SELECTED",
  "recovery_checkpoint": "cc9aaef40dec218e63fae7de835298ef76bd241f",
  "reference_safety": "PASS",
  "shared_field_preparations": 1,
  "stage_a": "d7e28de0e103bdf0e494a0156311fa1c14b6c9f8",
  "stage_b": "CAPTURED",
  "top_k_inversions": {
    "Q1": {
      "10": 0,
      "20": 0,
      "50": 0
    },
    "Q2": {
      "10": 1,
      "20": 1,
      "50": 34
    },
    "Q3": {
      "10": 0,
      "20": 0,
      "50": 0
    },
    "Q4": {
      "10": 0,
      "20": 0,
      "50": 6
    },
    "Q5": {
      "10": 2,
      "20": 11,
      "50": 24
    },
    "Q6": {
      "10": 2,
      "20": 4,
      "50": 45
    }
  },
  "total_candidate_occurrences": 1807
}
```

## Captured cost

```json
{
  "arm_a_native_retrieval_ns": 72046400,
  "arm_b_bm25f_scoring_ns": 27285623700,
  "capture_wall_ns": 102810183300,
  "charged_A_ns": 10614691700,
  "charged_B_ns": 37828269000,
  "counting": "Top-level scientific intervals only. Shared charged once to each arm. Native filename construction inside A/reference included in native timing. Durability, mechanical checks, wall and publication are descriptive; no double counting or outcome selection.",
  "derived_publication": {
    "derived_artifact_construction_ns": 54359943800,
    "large_surface_publication_ns": 8206600,
    "scope": "Descriptive, excluded from mechanism cost; metadata/receipt/integrity publication itself is outside these measured intervals."
  },
  "journal_publication_durability_ns": 55140891800,
  "mechanical_between_operation_validation_ns": 9541811400,
  "query_operations_ns": {
    "query:Q1:A": 7068800,
    "query:Q1:B": 13811381000,
    "query:Q2:A": 34358200,
    "query:Q2:B": 2542072900,
    "query:Q3:A": 6820100,
    "query:Q3:B": 2574438300,
    "query:Q4:A": 6685800,
    "query:Q4:B": 2823340300,
    "query:Q5:A": 8571900,
    "query:Q5:B": 2821112400,
    "query:Q6:A": 8541600,
    "query:Q6:B": 2713278800,
    "query:reference": 24904000
  },
  "reference_ns": 24904000,
  "shared_charged_equally_ns": 10542645300,
  "shared_operations_ns": {
    "fields:prepare": 223800600,
    "frame:prepare": 7658899900,
    "index:native-prepare": 2622225800,
    "statistics:union-prepare": 37719000
  }
}
```

## Complete field-length inventory

| Resource | CONTENT length | FILENAME length | Stem |
|---|---:|---:|---|
| AGENTS.md | 1629 | 1 | AGENTS |
| README.md | 281 | 1 | README |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 1686 | 6 | ADR-0001-cohesive-model-interaction-boundary |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 8240 | 7 | ADR-0002-repository-intelligence-identity-and-derivation |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 3950 | 8 | ADR-0003-information-need-retrieval-evidence-and-ranking |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 3908 | 7 | ADR-0004-context-disclosure-planning-and-assembly |
| docs/backlog/epics/B-0001-architecture-documentation-integrity.md | 106 | 5 | B-0001-architecture-documentation-integrity |
| docs/backlog/epics/B-0003-local-coding-worker-harness.md | 151 | 6 | B-0003-local-coding-worker-harness |
| docs/backlog/epics/B-0004-governed-execution-evolution.md | 97 | 5 | B-0004-governed-execution-evolution |
| docs/backlog/epics/B-0005-effect-governance.md | 110 | 4 | B-0005-effect-governance |
| docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md | 346 | 6 | B-0015-framework-acceptance-harness-validation |
| docs/backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md | 86 | 6 | B-0006-reconcile-authoritative-architecture-documentation |
| docs/backlog/items/B-0007-correct-model-serving-documentation-drift.md | 94 | 7 | B-0007-correct-model-serving-documentation-drift |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 300 | 6 | B-0008-investigate-repository-context-discovery |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 372 | 8 | B-0009-build-bounded-local-coding-worker-harness |
| docs/backlog/items/B-0010-investigate-work-execution-attempt-semantics.md | 115 | 7 | B-0010-investigate-work-execution-attempt-semantics |
| docs/backlog/items/B-0011-investigate-durable-execution-evidence.md | 104 | 6 | B-0011-investigate-durable-execution-evidence |
| docs/backlog/items/B-0012-investigate-governed-effect-semantics.md | 91 | 6 | B-0012-investigate-governed-effect-semantics |
| docs/backlog/items/B-0013-investigate-authority-grants-approval.md | 93 | 6 | B-0013-investigate-authority-grants-approval |
| docs/backlog/items/B-0014-investigate-retry-repair-reconciliation.md | 79 | 6 | B-0014-investigate-retry-repair-reconciliation |
| docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md | 127 | 7 | B-0016-define-framework-live-harness-acceptance |
| docs/backlog/items/B-0017-investigate-runtime-occurrence-observability-boundaries.md | 106 | 7 | B-0017-investigate-runtime-occurrence-observability-boundaries |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 168 | 7 | B-0018-investigate-operational-data-minimization-disclosure |
| docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md | 163 | 6 | B-0019-investigate-typed-configuration-ownership |
| docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md | 115 | 8 | B-0020-investigate-capability-operation-model-action-substrate |
| docs/backlog/items/B-0021-investigate-approval-human-governance-workflow.md | 77 | 7 | B-0021-investigate-approval-human-governance-workflow |
| docs/backlog/items/B-0022-investigate-delegation-acting-authority.md | 70 | 6 | B-0022-investigate-delegation-acting-authority |
| docs/backlog/items/B-0023-investigate-observability-architecture.md | 296 | 5 | B-0023-investigate-observability-architecture |
| docs/backlog/items/B-0024-investigate-audit-durable-accountability.md | 88 | 6 | B-0024-investigate-audit-durable-accountability |
| docs/backlog/items/B-0025-investigate-scoped-runtime-context.md | 104 | 6 | B-0025-investigate-scoped-runtime-context |
| docs/backlog/items/B-0026-investigate-runtime-control-lifecycle.md | 72 | 6 | B-0026-investigate-runtime-control-lifecycle |
| docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md | 152 | 6 | B-0027-investigate-serialization-representation-boundaries |
| docs/backlog/items/B-0028-investigate-persistence-durable-state-boundaries.md | 117 | 7 | B-0028-investigate-persistence-durable-state-boundaries |
| docs/backlog/items/B-0029-investigate-reusable-agent-definition-runtime-orchestration.md | 99 | 8 | B-0029-investigate-reusable-agent-definition-runtime-orchestration |
| docs/backlog/items/B-0030-investigate-provider-neutral-generative-model-interaction.md | 89 | 8 | B-0030-investigate-provider-neutral-generative-model-interaction |
| docs/backlog/items/B-0031-investigate-generic-execution-lifecycle-promotion.md | 124 | 7 | B-0031-investigate-generic-execution-lifecycle-promotion |
| docs/backlog/items/B-0032-investigate-execution-retry-mechanics.md | 90 | 6 | B-0032-investigate-execution-retry-mechanics |
| docs/backlog/items/B-0033-investigate-semantic-repair-replanning.md | 97 | 6 | B-0033-investigate-semantic-repair-replanning |
| docs/backlog/items/B-0034-investigate-uncertain-effect-reconciliation.md | 91 | 6 | B-0034-investigate-uncertain-effect-reconciliation |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 194 | 7 | B-0035-investigate-tool-facing-capability-exposure |
| docs/backlog/items/B-0036-investigate-action-request-semantics.md | 164 | 6 | B-0036-investigate-action-request-semantics |
| docs/backlog/items/B-0037-investigate-approval-semantics.md | 85 | 5 | B-0037-investigate-approval-semantics |
| docs/backlog/items/B-0038-investigate-approval-workflow-orchestration.md | 92 | 6 | B-0038-investigate-approval-workflow-orchestration |
| docs/backlog/items/B-0039-investigate-delegated-authority.md | 85 | 5 | B-0039-investigate-delegated-authority |
| docs/backlog/items/B-0040-investigate-delegated-agent-coordination.md | 92 | 6 | B-0040-investigate-delegated-agent-coordination |
| docs/backlog/items/B-0041-investigate-execution-local-lifecycle-control.md | 90 | 7 | B-0041-investigate-execution-local-lifecycle-control |
| docs/backlog/items/B-0042-investigate-workflow-lifecycle-control.md | 89 | 6 | B-0042-investigate-workflow-lifecycle-control |
| docs/backlog/items/B-0043-investigate-reusable-agent-semantics.md | 102 | 6 | B-0043-investigate-reusable-agent-semantics |
| docs/backlog/items/B-0044-investigate-orchestration-control-loops.md | 94 | 6 | B-0044-investigate-orchestration-control-loops |
| docs/backlog/items/B-0045-establish-minimal-model-interaction-core.md | 99 | 7 | B-0045-establish-minimal-model-interaction-core |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 1213 | 8 | B-0046-investigate-advanced-model-interaction-provider-pressure |
| docs/backlog/metadata.md | 484 | 1 | metadata |
| docs/backlog/overview.md | 1215 | 1 | overview |
| docs/experiments/qwen38_llama_cpp.md | 676 | 1 | qwen38_llama_cpp |
| pyproject.toml | 165 | 1 | pyproject |
| scripts/validate_development.py | 81 | 1 | validate_development |
| src/devtools/__init__.py | 7 | 1 | __init__ |
| src/devtools/agents/__init__.py | 10 | 1 | __init__ |
| src/devtools/agents/conversation/__init__.py | 48 | 1 | __init__ |
| src/devtools/agents/conversation/conversation.py | 505 | 1 | conversation |
| src/devtools/agents/conversation/docs/conversation.md | 110 | 1 | conversation |
| src/devtools/agents/conversation/docs/history.md | 51 | 1 | history |
| src/devtools/agents/conversation/docs/overview.md | 119 | 1 | overview |
| src/devtools/agents/conversation/history.py | 158 | 1 | history |
| src/devtools/agents/conversation/message.py | 294 | 1 | message |
| src/devtools/agents/integrations/__init__.py | 8 | 1 | __init__ |
| src/devtools/agents/integrations/codex/__init__.py | 44 | 1 | __init__ |
| src/devtools/agents/integrations/codex/agent.py | 517 | 1 | agent |
| src/devtools/agents/integrations/codex/docs/cli.md | 681 | 1 | cli |
| src/devtools/agents/integrations/codex/docs/overview.md | 120 | 1 | overview |
| src/devtools/agents/integrations/codex/errors.py | 83 | 1 | errors |
| src/devtools/agents/integrations/codex/models.py | 90 | 1 | models |
| src/devtools/agents/integrations/codex/parsing.py | 561 | 1 | parsing |
| src/devtools/context/__init__.py | 263 | 1 | __init__ |
| src/devtools/context/localization/__init__.py | 102 | 1 | __init__ |
| src/devtools/context/localization/assessment.py | 465 | 1 | assessment |
| src/devtools/context/localization/association/__init__.py | 72 | 1 | __init__ |
| src/devtools/context/localization/association/hypothesis.py | 1478 | 1 | hypothesis |
| src/devtools/context/localization/association/imports.py | 841 | 1 | imports |
| src/devtools/context/localization/association/references.py | 735 | 1 | references |
| src/devtools/context/localization/association/structural.py | 402 | 1 | structural |
| src/devtools/context/localization/generation/__init__.py | 50 | 1 | __init__ |
| src/devtools/context/localization/generation/contract.py | 1515 | 1 | contract |
| src/devtools/context/localization/generation/generate.py | 1451 | 1 | generate |
| src/devtools/context/localization/generation/imports.py | 237 | 1 | imports |
| src/devtools/context/localization/generation/references.py | 193 | 1 | references |
| src/devtools/context/localization/grounding/__init__.py | 60 | 1 | __init__ |
| src/devtools/context/localization/grounding/contract.py | 641 | 1 | contract |
| src/devtools/context/localization/grounding/resolve.py | 917 | 1 | resolve |
| src/devtools/context/localization/grounding/view.py | 532 | 1 | view |
| src/devtools/context/localization/identity.py | 348 | 1 | identity |
| src/devtools/context/localization/lexical.py | 462 | 1 | lexical |
| src/devtools/context/localization/obligation.py | 355 | 1 | obligation |
| src/devtools/context/localization/readiness.py | 1075 | 1 | readiness |
| src/devtools/context/localization/resolution/__init__.py | 49 | 1 | __init__ |
| src/devtools/context/localization/resolution/contract.py | 752 | 1 | contract |
| src/devtools/context/localization/resolution/promotion.py | 230 | 1 | promotion |
| src/devtools/context/localization/resolution/view.py | 663 | 1 | view |
| src/devtools/context/localization/roles/__init__.py | 45 | 1 | __init__ |
| src/devtools/context/localization/roles/configuration.py | 576 | 1 | configuration |
| src/devtools/context/localization/roles/derivation.py | 554 | 1 | derivation |
| src/devtools/context/localization/roles/inputs.py | 457 | 1 | inputs |
| src/devtools/context/localization/roles/models.py | 598 | 1 | models |
| src/devtools/context/localization/routing/__init__.py | 39 | 1 | __init__ |
| src/devtools/context/localization/routing/derive.py | 719 | 1 | derive |
| src/devtools/context/localization/routing/docs/overview.md | 456 | 1 | overview |
| src/devtools/context/localization/routing/models.py | 307 | 1 | models |
| src/devtools/context/localization/task.py | 248 | 1 | task |
| src/devtools/context/planning/__init__.py | 59 | 1 | __init__ |
| src/devtools/context/planning/docs/overview.md | 449 | 1 | overview |
| src/devtools/context/planning/materialization.py | 309 | 1 | materialization |
| src/devtools/context/planning/plan.py | 388 | 1 | plan |
| src/devtools/context/planning/rendering.py | 221 | 1 | rendering |
| src/devtools/context/planning/resource.py | 325 | 1 | resource |
| src/devtools/context/python/__init__.py | 39 | 1 | __init__ |
| src/devtools/context/python/classes/__init__.py | 77 | 1 | __init__ |
| src/devtools/context/python/classes/bases.py | 1378 | 1 | bases |
| src/devtools/context/python/classes/containment.py | 676 | 1 | containment |
| src/devtools/context/python/classes/declarations.py | 1365 | 1 | declarations |
| src/devtools/context/python/classes/docs/overview.md | 1010 | 1 | overview |
| src/devtools/context/python/docs/overview.md | 403 | 1 | overview |
| src/devtools/context/python/function/__init__.py | 178 | 1 | __init__ |
| src/devtools/context/python/function/candidates.py | 473 | 1 | candidates |
| src/devtools/context/python/function/containment.py | 445 | 1 | containment |
| src/devtools/context/python/function/declarations.py | 1143 | 1 | declarations |
| src/devtools/context/python/function/disclosure.py | 248 | 1 | disclosure |
| src/devtools/context/python/function/docs/overview.md | 723 | 1 | overview |
| src/devtools/context/python/function/materialization.py | 488 | 1 | materialization |
| src/devtools/context/python/function/planned_reference.py | 249 | 1 | planned_reference |
| src/devtools/context/python/function/qualified_reference.py | 1155 | 1 | qualified_reference |
| src/devtools/context/python/function/rendering.py | 316 | 1 | rendering |
| src/devtools/context/python/function/request_assembly.py | 169 | 1 | request_assembly |
| src/devtools/context/python/function/retrieval.py | 384 | 1 | retrieval |
| src/devtools/context/python/imports/__init__.py | 80 | 1 | __init__ |
| src/devtools/context/python/imports/declarations.py | 432 | 1 | declarations |
| src/devtools/context/python/imports/docs/overview.md | 357 | 1 | overview |
| src/devtools/context/python/imports/members.py | 1346 | 1 | members |
| src/devtools/context/python/imports/relations.py | 363 | 1 | relations |
| src/devtools/context/python/imports/resolution.py | 558 | 1 | resolution |
| src/devtools/context/python/mirrored_paths.py | 601 | 1 | mirrored_paths |
| src/devtools/context/python/modules/__init__.py | 65 | 1 | __init__ |
| src/devtools/context/python/modules/declarations.py | 603 | 1 | declarations |
| src/devtools/context/python/modules/docs/overview.md | 722 | 1 | overview |
| src/devtools/context/python/modules/interpretation.py | 722 | 1 | interpretation |
| src/devtools/context/python/modules/lookup.py | 59 | 1 | lookup |
| src/devtools/context/python/modules/membership.py | 849 | 1 | membership |
| src/devtools/context/python/modules/selection.py | 305 | 1 | selection |
| src/devtools/context/python/project_configuration/__init__.py | 57 | 1 | __init__ |
| src/devtools/context/python/project_configuration/declarations.py | 362 | 1 | declarations |
| src/devtools/context/python/project_configuration/models.py | 588 | 1 | models |
| src/devtools/context/python/project_configuration/resolution.py | 831 | 1 | resolution |
| src/devtools/context/python/project_configuration/settings.py | 514 | 1 | settings |
| src/devtools/context/python/references/__init__.py | 38 | 1 | __init__ |
| src/devtools/context/python/references/declarations/__init__.py | 46 | 1 | __init__ |
| src/devtools/context/python/references/declarations/analysis.py | 501 | 1 | analysis |
| src/devtools/context/python/references/declarations/bindings.py | 819 | 1 | bindings |
| src/devtools/context/python/references/declarations/model.py | 514 | 1 | model |
| src/devtools/context/python/references/declarations/resolution.py | 939 | 1 | resolution |
| src/devtools/context/python/references/docs/overview.md | 602 | 1 | overview |
| src/devtools/context/python/source_candidacy.py | 221 | 1 | source_candidacy |
| src/devtools/context/repository/__init__.py | 98 | 1 | __init__ |
| src/devtools/context/repository/corpus.py | 553 | 1 | corpus |
| src/devtools/context/repository/discovery.py | 573 | 1 | discovery |
| src/devtools/context/repository/document.py | 273 | 1 | document |
| src/devtools/context/repository/identity.py | 123 | 1 | identity |
| src/devtools/context/repository/observation.py | 525 | 1 | observation |
| src/devtools/context/repository/resource.py | 299 | 1 | resource |
| src/devtools/context/repository/snapshot.py | 196 | 1 | snapshot |
| src/devtools/context/retrieval/__init__.py | 148 | 1 | __init__ |
| src/devtools/context/retrieval/composition.py | 600 | 1 | composition |
| src/devtools/context/retrieval/docs/overview.md | 1008 | 1 | overview |
| src/devtools/context/retrieval/fusion.py | 641 | 1 | fusion |
| src/devtools/context/retrieval/graph/__init__.py | 58 | 1 | __init__ |
| src/devtools/context/retrieval/graph/pagerank.py | 952 | 1 | pagerank |
| src/devtools/context/retrieval/graph/view.py | 1497 | 1 | view |
| src/devtools/context/retrieval/graph/walk.py | 176 | 1 | walk |
| src/devtools/context/retrieval/lexical/__init__.py | 133 | 1 | __init__ |
| src/devtools/context/retrieval/lexical/analysis.py | 241 | 1 | analysis |
| src/devtools/context/retrieval/lexical/bm25.py | 853 | 1 | bm25 |
| src/devtools/context/retrieval/lexical/evaluation.py | 517 | 1 | evaluation |
| src/devtools/context/retrieval/lexical/filename.py | 627 | 1 | filename |
| src/devtools/context/retrieval/lexical/index.py | 191 | 1 | index |
| src/devtools/context/retrieval/lexical/scoring.py | 100 | 1 | scoring |
| src/devtools/context/retrieval/lexical/statistics.py | 300 | 1 | statistics |
| src/devtools/context/retrieval/repository_map/__init__.py | 52 | 1 | __init__ |
| src/devtools/context/retrieval/repository_map/importance.py | 297 | 1 | importance |
| src/devtools/context/retrieval/repository_map/ranking.py | 536 | 1 | ranking |
| src/devtools/context/retrieval/repository_map/relevance.py | 288 | 1 | relevance |
| src/devtools/context/retrieval/repository_map/view.py | 482 | 1 | view |
| src/devtools/context/retrieval/structural.py | 651 | 1 | structural |
| src/devtools/core/__init__.py | 6 | 1 | __init__ |
| src/devtools/core/conversion/__init__.py | 29 | 1 | __init__ |
| src/devtools/core/conversion/conversion.py | 180 | 1 | conversion |
| src/devtools/core/conversion/docs/overview.md | 693 | 1 | overview |
| src/devtools/core/conversion/errors.py | 107 | 1 | errors |
| src/devtools/core/identity/__init__.py | 17 | 1 | __init__ |
| src/devtools/core/identity/docs/overview.md | 281 | 1 | overview |
| src/devtools/core/identity/models.py | 112 | 1 | models |
| src/devtools/core/paths/__init__.py | 49 | 1 | __init__ |
| src/devtools/core/paths/docs/overview.md | 384 | 1 | overview |
| src/devtools/core/paths/docs/resolution.md | 425 | 1 | resolution |
| src/devtools/core/paths/errors.py | 45 | 1 | errors |
| src/devtools/core/paths/models.py | 309 | 1 | models |
| src/devtools/core/paths/resolution.py | 606 | 1 | resolution |
| src/devtools/core/regex/__init__.py | 36 | 1 | __init__ |
| src/devtools/core/regex/docs/overview.md | 668 | 1 | overview |
| src/devtools/core/regex/models.py | 252 | 1 | models |
| src/devtools/core/regex/search.py | 380 | 1 | search |
| src/devtools/core/system/__init__.py | 25 | 1 | __init__ |
| src/devtools/core/system/detection.py | 53 | 1 | detection |
| src/devtools/core/system/docs/overview.md | 300 | 1 | overview |
| src/devtools/core/system/models.py | 72 | 1 | models |
| src/devtools/core/time/__init__.py | 39 | 1 | __init__ |
| src/devtools/core/time/docs/overview.md | 241 | 1 | overview |
| src/devtools/core/time/docs/timestamps.md | 417 | 1 | timestamps |
| src/devtools/core/time/docs/timing.md | 146 | 1 | timing |
| src/devtools/core/time/errors.py | 31 | 1 | errors |
| src/devtools/core/time/models/__init__.py | 36 | 1 | __init__ |
| src/devtools/core/time/models/duration.py | 431 | 1 | duration |
| src/devtools/core/time/models/stopwatch.py | 296 | 1 | stopwatch |
| src/devtools/core/time/models/timestamp.py | 371 | 1 | timestamp |
| src/devtools/core/time/parsing.py | 337 | 1 | parsing |
| src/devtools/evaluation/__init__.py | 19 | 1 | __init__ |
| src/devtools/evaluation/coverage.py | 254 | 1 | coverage |
| src/devtools/evaluation/docs/overview.md | 159 | 1 | overview |
| src/devtools/execution/__init__.py | 45 | 1 | __init__ |
| src/devtools/execution/docs/overview.md | 172 | 1 | overview |
| src/devtools/execution/interaction_attempt.py | 535 | 1 | interaction_attempt |
| src/devtools/execution/protocols.py | 56 | 1 | protocols |
| src/devtools/execution/runtime.py | 427 | 1 | runtime |
| src/devtools/governance/__init__.py | 10 | 1 | __init__ |
| src/devtools/models/__init__.py | 9 | 1 | __init__ |
| src/devtools/models/benchmarks/__init__.py | 13 | 1 | __init__ |
| src/devtools/models/benchmarks/docs/overview.md | 353 | 1 | overview |
| src/devtools/models/benchmarks/models.py | 411 | 1 | models |
| src/devtools/models/benchmarks/runner.py | 1188 | 1 | runner |
| src/devtools/models/benchmarks/storage.py | 879 | 1 | storage |
| src/devtools/models/interaction/__init__.py | 92 | 1 | __init__ |
| src/devtools/models/interaction/docs/overview.md | 552 | 1 | overview |
| src/devtools/models/interaction/models.py | 519 | 1 | models |
| src/devtools/models/interaction/observation.py | 246 | 1 | observation |
| src/devtools/models/interaction/prompt.py | 33 | 1 | prompt |
| src/devtools/models/interaction/protocols.py | 80 | 1 | protocols |
| src/devtools/models/interaction/providers/__init__.py | 41 | 1 | __init__ |
| src/devtools/models/interaction/providers/llama_cpp.py | 2207 | 1 | llama_cpp |
| src/devtools/models/interaction/providers/llama_cpp_errors.py | 108 | 1 | llama_cpp_errors |
| src/devtools/models/interaction/providers/llama_cpp_request_settings.py | 69 | 1 | llama_cpp_request_settings |
| src/devtools/models/interaction/response.py | 150 | 1 | response |
| src/devtools/models/interaction/termination.py | 33 | 1 | termination |
| src/devtools/models/interaction/tools.py | 298 | 1 | tools |
| src/devtools/models/interaction/usage.py | 118 | 1 | usage |
| src/devtools/models/serving/__init__.py | 38 | 1 | __init__ |
| src/devtools/models/serving/docs/overview.md | 808 | 1 | overview |
| src/devtools/models/serving/errors.py | 250 | 1 | errors |
| src/devtools/models/serving/huggingface.py | 492 | 1 | huggingface |
| src/devtools/models/serving/identity.py | 206 | 1 | identity |
| src/devtools/models/serving/llama_cpp.py | 1647 | 1 | llama_cpp |
| src/devtools/models/serving/vllm.py | 1966 | 1 | vllm |
| src/devtools/observability/__init__.py | 9 | 1 | __init__ |
| src/devtools/observability/evidence/__init__.py | 66 | 1 | __init__ |
| src/devtools/observability/evidence/docs/overview.md | 315 | 1 | overview |
| src/devtools/observability/evidence/inspection.py | 251 | 1 | inspection |
| src/devtools/observability/evidence/model_interaction.py | 960 | 1 | model_interaction |
| src/devtools/observability/evidence/protocols.py | 37 | 1 | protocols |
| src/devtools/observability/evidence/terminal.py | 164 | 1 | terminal |
| src/devtools/orchestration/__init__.py | 11 | 1 | __init__ |
| src/devtools/persistence/__init__.py | 38 | 1 | __init__ |
| src/devtools/persistence/_snapshot.py | 389 | 1 | _snapshot |
| src/devtools/persistence/docs/json.md | 66 | 1 | json |
| src/devtools/persistence/docs/overview.md | 94 | 1 | overview |
| src/devtools/persistence/docs/sqlite.md | 74 | 1 | sqlite |
| src/devtools/persistence/errors.py | 49 | 1 | errors |
| src/devtools/persistence/json.py | 720 | 1 | json |
| src/devtools/persistence/sqlite.py | 989 | 1 | sqlite |
| src/devtools/resources/__init__.py | 8 | 1 | __init__ |
| src/devtools/resources/commands/__init__.py | 66 | 1 | __init__ |
| src/devtools/resources/commands/docs/command.md | 243 | 1 | command |
| src/devtools/resources/commands/docs/events.md | 236 | 1 | events |
| src/devtools/resources/commands/docs/execution.md | 287 | 1 | execution |
| src/devtools/resources/commands/docs/overview.md | 237 | 1 | overview |
| src/devtools/resources/commands/errors.py | 41 | 1 | errors |
| src/devtools/resources/commands/events.py | 133 | 1 | events |
| src/devtools/resources/commands/execution.py | 809 | 1 | execution |
| src/devtools/resources/commands/handle.py | 400 | 1 | handle |
| src/devtools/resources/commands/models/__init__.py | 40 | 1 | __init__ |
| src/devtools/resources/commands/models/command.py | 421 | 1 | command |
| src/devtools/resources/commands/models/output.py | 151 | 1 | output |
| src/devtools/resources/commands/models/result.py | 204 | 1 | result |
| src/devtools/resources/filesystem/__init__.py | 113 | 1 | __init__ |
| src/devtools/resources/filesystem/codecs/__init__.py | 43 | 1 | __init__ |
| src/devtools/resources/filesystem/codecs/csv.py | 563 | 1 | csv |
| src/devtools/resources/filesystem/codecs/json.py | 697 | 1 | json |
| src/devtools/resources/filesystem/codecs/markdown.py | 251 | 1 | markdown |
| src/devtools/resources/filesystem/codecs/text.py | 224 | 1 | text |
| src/devtools/resources/filesystem/docs/codecs.md | 176 | 1 | codecs |
| src/devtools/resources/filesystem/docs/csv.md | 289 | 1 | csv |
| src/devtools/resources/filesystem/docs/io.md | 333 | 1 | io |
| src/devtools/resources/filesystem/docs/json.md | 291 | 1 | json |
| src/devtools/resources/filesystem/docs/markdown.md | 256 | 1 | markdown |
| src/devtools/resources/filesystem/docs/models.md | 243 | 1 | models |
| src/devtools/resources/filesystem/docs/overview.md | 383 | 1 | overview |
| src/devtools/resources/filesystem/docs/roadmap.md | 173 | 1 | roadmap |
| src/devtools/resources/filesystem/errors.py | 108 | 1 | errors |
| src/devtools/resources/filesystem/models/__init__.py | 86 | 1 | __init__ |
| src/devtools/resources/filesystem/models/base.py | 84 | 1 | base |
| src/devtools/resources/filesystem/models/binary.py | 98 | 1 | binary |
| src/devtools/resources/filesystem/models/csv.py | 1236 | 1 | csv |
| src/devtools/resources/filesystem/models/json/__init__.py | 63 | 1 | __init__ |
| src/devtools/resources/filesystem/models/json/base.py | 135 | 1 | base |
| src/devtools/resources/filesystem/models/json/conversion.py | 147 | 1 | conversion |
| src/devtools/resources/filesystem/models/json/list.py | 558 | 1 | list |
| src/devtools/resources/filesystem/models/json/object.py | 519 | 1 | object |
| src/devtools/resources/filesystem/models/json/scalar.py | 109 | 1 | scalar |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 37 | 1 | __init__ |
| src/devtools/resources/filesystem/models/markdown/file.py | 546 | 1 | file |
| src/devtools/resources/filesystem/models/markdown/heading.py | 189 | 1 | heading |
| src/devtools/resources/filesystem/models/markdown/section.py | 351 | 1 | section |
| src/devtools/resources/filesystem/models/text.py | 330 | 1 | text |
| src/devtools/resources/filesystem/reading.py | 383 | 1 | reading |
| src/devtools/resources/filesystem/resolution.py | 222 | 1 | resolution |
| src/devtools/resources/filesystem/writing.py | 433 | 1 | writing |
| src/devtools/tools/__init__.py | 40 | 1 | __init__ |
| src/devtools/tools/command.py | 126 | 1 | command |
| src/devtools/tools/disclosure.py | 192 | 1 | disclosure |
| src/devtools/tools/docs/overview.md | 226 | 1 | overview |
| src/devtools/tools/errors.py | 21 | 1 | errors |
| src/devtools/tools/execution.py | 67 | 1 | execution |
| src/devtools/tools/filesystem.py | 557 | 1 | filesystem |
| src/devtools/tools/protocols.py | 88 | 1 | protocols |
| tests/__init__.py | 8 | 1 | __init__ |
| tests/agents/__init__.py | 6 | 1 | __init__ |
| tests/agents/conversation/__init__.py | 5 | 1 | __init__ |
| tests/agents/conversation/history/__init__.py | 10 | 1 | __init__ |
| tests/agents/conversation/history/test_history.py | 734 | 1 | test_history |
| tests/agents/conversation/message/__init__.py | 10 | 1 | __init__ |
| tests/agents/conversation/message/test_message.py | 578 | 1 | test_message |
| tests/agents/conversation/test_live.py | 420 | 1 | test_live |
| tests/agents/conversation/test_session.py | 1280 | 1 | test_session |
| tests/agents/conversation/test_session_id.py | 200 | 1 | test_session_id |
| tests/agents/integrations/__init__.py | 6 | 1 | __init__ |
| tests/agents/integrations/codex/__init__.py | 6 | 1 | __init__ |
| tests/agents/integrations/codex/test_agent.py | 833 | 1 | test_agent |
| tests/agents/integrations/codex/test_live.py | 309 | 1 | test_live |
| tests/agents/integrations/codex/test_parsing.py | 342 | 1 | test_parsing |
| tests/context/__init__.py | 9 | 1 | __init__ |
| tests/context/localization/__init__.py | 10 | 1 | __init__ |
| tests/context/localization/association/__init__.py | 7 | 1 | __init__ |
| tests/context/localization/association/test_hypothesis.py | 1432 | 1 | test_hypothesis |
| tests/context/localization/generation/__init__.py | 8 | 1 | __init__ |
| tests/context/localization/generation/test_branching.py | 2346 | 1 | test_branching |
| tests/context/localization/generation/test_generation.py | 1990 | 1 | test_generation |
| tests/context/localization/generation/test_imports.py | 1850 | 1 | test_imports |
| tests/context/localization/generation/test_references.py | 2442 | 1 | test_references |
| tests/context/localization/grounding/__init__.py | 8 | 1 | __init__ |
| tests/context/localization/grounding/test_grounding.py | 1941 | 1 | test_grounding |
| tests/context/localization/resolution/__init__.py | 9 | 1 | __init__ |
| tests/context/localization/resolution/test_resolution.py | 1723 | 1 | test_resolution |
| tests/context/localization/roles/__init__.py | 8 | 1 | __init__ |
| tests/context/localization/roles/helpers.py | 198 | 1 | helpers |
| tests/context/localization/roles/test_configuration.py | 742 | 1 | test_configuration |
| tests/context/localization/roles/test_evidence.py | 605 | 1 | test_evidence |
| tests/context/localization/roles/test_inputs.py | 310 | 1 | test_inputs |
| tests/context/localization/routing/__init__.py | 8 | 1 | __init__ |
| tests/context/localization/routing/test_routing.py | 1394 | 1 | test_routing |
| tests/context/localization/test_kernel.py | 1669 | 1 | test_kernel |
| tests/context/localization/test_lexical.py | 1108 | 1 | test_lexical |
| tests/context/planning/__init__.py | 9 | 1 | __init__ |
| tests/context/planning/test_plan.py | 996 | 1 | test_plan |
| tests/context/python/__init__.py | 7 | 1 | __init__ |
| tests/context/python/classes/__init__.py | 10 | 1 | __init__ |
| tests/context/python/classes/test_bases.py | 1527 | 1 | test_bases |
| tests/context/python/classes/test_declarations.py | 1340 | 1 | test_declarations |
| tests/context/python/function/__init__.py | 7 | 1 | __init__ |
| tests/context/python/function/test_candidates.py | 934 | 1 | test_candidates |
| tests/context/python/function/test_containment.py | 805 | 1 | test_containment |
| tests/context/python/function/test_cross_resource_pipeline.py | 753 | 1 | test_cross_resource_pipeline |
| tests/context/python/function/test_declaration_aggregation.py | 659 | 1 | test_declaration_aggregation |
| tests/context/python/function/test_declarations.py | 1279 | 1 | test_declarations |
| tests/context/python/function/test_disclosure.py | 463 | 1 | test_disclosure |
| tests/context/python/function/test_materialization.py | 845 | 1 | test_materialization |
| tests/context/python/function/test_qualified_reference.py | 1638 | 1 | test_qualified_reference |
| tests/context/python/function/test_rendering.py | 622 | 1 | test_rendering |
| tests/context/python/function/test_request_assembly.py | 613 | 1 | test_request_assembly |
| tests/context/python/function/test_resource_selection.py | 747 | 1 | test_resource_selection |
| tests/context/python/function/test_retrieval.py | 457 | 1 | test_retrieval |
| tests/context/python/imports/__init__.py | 9 | 1 | __init__ |
| tests/context/python/imports/test_declarations.py | 382 | 1 | test_declarations |
| tests/context/python/imports/test_members.py | 1679 | 1 | test_members |
| tests/context/python/imports/test_relations.py | 1343 | 1 | test_relations |
| tests/context/python/imports/test_resolution.py | 1112 | 1 | test_resolution |
| tests/context/python/modules/__init__.py | 10 | 1 | __init__ |
| tests/context/python/modules/test_interpretation.py | 600 | 1 | test_interpretation |
| tests/context/python/modules/test_membership.py | 811 | 1 | test_membership |
| tests/context/python/modules/test_selection.py | 502 | 1 | test_selection |
| tests/context/python/project_configuration/__init__.py | 8 | 1 | __init__ |
| tests/context/python/project_configuration/test_configuration.py | 1506 | 1 | test_configuration |
| tests/context/python/project_configuration/test_settings.py | 1181 | 1 | test_settings |
| tests/context/python/references/__init__.py | 8 | 1 | __init__ |
| tests/context/python/references/declarations/__init__.py | 8 | 1 | __init__ |
| tests/context/python/references/declarations/test_analysis.py | 1904 | 1 | test_analysis |
| tests/context/python/references/declarations/test_bindings.py | 396 | 1 | test_bindings |
| tests/context/python/test_mirrored_paths.py | 680 | 1 | test_mirrored_paths |
| tests/context/python/test_source_candidacy.py | 700 | 1 | test_source_candidacy |
| tests/context/repository/__init__.py | 6 | 1 | __init__ |
| tests/context/repository/test_corpus.py | 1320 | 1 | test_corpus |
| tests/context/repository/test_discovery.py | 1286 | 1 | test_discovery |
| tests/context/repository/test_document.py | 739 | 1 | test_document |
| tests/context/repository/test_intrinsic_paths.py | 139 | 1 | test_intrinsic_paths |
| tests/context/repository/test_observation.py | 1636 | 1 | test_observation |
| tests/context/retrieval/__init__.py | 7 | 1 | __init__ |
| tests/context/retrieval/graph/__init__.py | 6 | 1 | __init__ |
| tests/context/retrieval/graph/test_ranking.py | 1234 | 1 | test_ranking |
| tests/context/retrieval/graph/test_typed.py | 1405 | 1 | test_typed |
| tests/context/retrieval/lexical/__init__.py | 11 | 1 | __init__ |
| tests/context/retrieval/lexical/_helpers.py | 221 | 1 | _helpers |
| tests/context/retrieval/lexical/test_analysis.py | 497 | 1 | test_analysis |
| tests/context/retrieval/lexical/test_bm25.py | 919 | 1 | test_bm25 |
| tests/context/retrieval/lexical/test_evaluation.py | 1019 | 1 | test_evaluation |
| tests/context/retrieval/lexical/test_filename.py | 552 | 1 | test_filename |
| tests/context/retrieval/lexical/test_index.py | 486 | 1 | test_index |
| tests/context/retrieval/lexical/test_statistics.py | 312 | 1 | test_statistics |
| tests/context/retrieval/repository_map/__init__.py | 7 | 1 | __init__ |
| tests/context/retrieval/repository_map/test_ranking.py | 1251 | 1 | test_ranking |
| tests/context/retrieval/test_composition.py | 994 | 1 | test_composition |
| tests/context/retrieval/test_structural.py | 775 | 1 | test_structural |
| tests/core/__init__.py | 6 | 1 | __init__ |
| tests/core/conversion/__init__.py | 9 | 1 | __init__ |
| tests/core/conversion/test_conversion.py | 402 | 1 | test_conversion |
| tests/core/identity/__init__.py | 7 | 1 | __init__ |
| tests/core/identity/test_models.py | 201 | 1 | test_models |
| tests/core/paths/__init__.py | 7 | 1 | __init__ |
| tests/core/paths/test_errors.py | 42 | 1 | test_errors |
| tests/core/paths/test_resolution.py | 450 | 1 | test_resolution |
| tests/core/paths/test_resolved_path.py | 264 | 1 | test_resolved_path |
| tests/core/regex/__init__.py | 8 | 1 | __init__ |
| tests/core/regex/test_models.py | 169 | 1 | test_models |
| tests/core/regex/test_search.py | 243 | 1 | test_search |
| tests/core/system/__init__.py | 7 | 1 | __init__ |
| tests/core/system/test_detection.py | 71 | 1 | test_detection |
| tests/core/system/test_models.py | 116 | 1 | test_models |
| tests/core/time/__init__.py | 7 | 1 | __init__ |
| tests/core/time/test_models.py | 508 | 1 | test_models |
| tests/core/time/test_parsing.py | 413 | 1 | test_parsing |
| tests/core/time/test_timing.py | 199 | 1 | test_timing |
| tests/evaluation/__init__.py | 5 | 1 | __init__ |
| tests/evaluation/test_coverage.py | 296 | 1 | test_coverage |
| tests/execution/__init__.py | 6 | 1 | __init__ |
| tests/execution/test_interaction_attempt.py | 1132 | 1 | test_interaction_attempt |
| tests/execution/test_runtime.py | 1474 | 1 | test_runtime |
| tests/models/__init__.py | 6 | 1 | __init__ |
| tests/models/benchmarks/__init__.py | 6 | 1 | __init__ |
| tests/models/benchmarks/test_models.py | 487 | 1 | test_models |
| tests/models/benchmarks/test_runner.py | 2189 | 1 | test_runner |
| tests/models/benchmarks/test_storage.py | 1070 | 1 | test_storage |
| tests/models/interaction/__init__.py | 6 | 1 | __init__ |
| tests/models/interaction/providers/__init__.py | 7 | 1 | __init__ |
| tests/models/interaction/providers/test_llama_cpp.py | 3542 | 1 | test_llama_cpp |
| tests/models/interaction/test_models.py | 1026 | 1 | test_models |
| tests/models/interaction/test_protocols.py | 174 | 1 | test_protocols |
| tests/models/interaction/test_tools.py | 338 | 1 | test_tools |
| tests/models/serving/__init__.py | 6 | 1 | __init__ |
| tests/models/serving/test_huggingface.py | 779 | 1 | test_huggingface |
| tests/models/serving/test_llama_cpp.py | 2439 | 1 | test_llama_cpp |
| tests/models/serving/test_vllm.py | 4541 | 1 | test_vllm |
| tests/observability/__init__.py | 6 | 1 | __init__ |
| tests/observability/evidence/__init__.py | 5 | 1 | __init__ |
| tests/observability/evidence/test_inspection.py | 344 | 1 | test_inspection |
| tests/observability/evidence/test_model_interaction.py | 1450 | 1 | test_model_interaction |
| tests/observability/evidence/test_protocols.py | 66 | 1 | test_protocols |
| tests/observability/evidence/test_terminal.py | 92 | 1 | test_terminal |
| tests/persistence/__init__.py | 5 | 1 | __init__ |
| tests/persistence/test_json.py | 587 | 1 | test_json |
| tests/persistence/test_sqlite.py | 1411 | 1 | test_sqlite |
| tests/resources/__init__.py | 6 | 1 | __init__ |
| tests/resources/commands/__init__.py | 8 | 1 | __init__ |
| tests/resources/commands/test_errors.py | 42 | 1 | test_errors |
| tests/resources/commands/test_events.py | 102 | 1 | test_events |
| tests/resources/commands/test_execution.py | 1128 | 1 | test_execution |
| tests/resources/commands/test_handle.py | 1168 | 1 | test_handle |
| tests/resources/commands/test_models.py | 471 | 1 | test_models |
| tests/resources/filesystem/__init__.py | 8 | 1 | __init__ |
| tests/resources/filesystem/codecs/__init__.py | 8 | 1 | __init__ |
| tests/resources/filesystem/codecs/test_csv.py | 566 | 1 | test_csv |
| tests/resources/filesystem/codecs/test_json.py | 748 | 1 | test_json |
| tests/resources/filesystem/codecs/test_markdown.py | 249 | 1 | test_markdown |
| tests/resources/filesystem/codecs/test_text.py | 324 | 1 | test_text |
| tests/resources/filesystem/models/__init__.py | 8 | 1 | __init__ |
| tests/resources/filesystem/models/csv/__init__.py | 9 | 1 | __init__ |
| tests/resources/filesystem/models/csv/test_dialect.py | 138 | 1 | test_dialect |
| tests/resources/filesystem/models/csv/test_file.py | 449 | 1 | test_file |
| tests/resources/filesystem/models/csv/test_row.py | 250 | 1 | test_row |
| tests/resources/filesystem/models/markdown/__init__.py | 8 | 1 | __init__ |
| tests/resources/filesystem/models/markdown/test_file.py | 510 | 1 | test_file |
| tests/resources/filesystem/models/markdown/test_heading.py | 134 | 1 | test_heading |
| tests/resources/filesystem/models/markdown/test_section.py | 183 | 1 | test_section |
| tests/resources/filesystem/test_json_conversion.py | 437 | 1 | test_json_conversion |
| tests/resources/filesystem/test_json_models.py | 654 | 1 | test_json_models |
| tests/resources/filesystem/test_models.py | 251 | 1 | test_models |
| tests/resources/filesystem/test_reading.py | 789 | 1 | test_reading |
| tests/resources/filesystem/test_resolution.py | 176 | 1 | test_resolution |
| tests/resources/filesystem/test_writing.py | 1020 | 1 | test_writing |
| tests/scripts/qwen/test_llama_cpp_profile.py | 193 | 1 | test_llama_cpp_profile |
| tests/scripts/qwen/test_llama_cpp_service.py | 2006 | 1 | test_llama_cpp_service |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 1282 | 1 | test_patch_proposal_worker_acceptance |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 568 | 1 | test_python_function_context_acceptance |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 986 | 1 | test_two_action_read_only_acceptance |
| tests/scripts/qwen/test_two_read_acceptance.py | 1420 | 1 | test_two_read_acceptance |
| tests/scripts/test_retrieval_bm25_baseline.py | 575 | 1 | test_retrieval_bm25_baseline |
| tests/scripts/test_validate_development.py | 197 | 1 | test_validate_development |
| tests/scripts/test_vllm_benchmark_driver.py | 1389 | 1 | test_vllm_benchmark_driver |
| tests/tools/__init__.py | 8 | 1 | __init__ |
| tests/tools/test_command.py | 438 | 1 | test_command |
| tests/tools/test_execution.py | 437 | 1 | test_execution |
| tests/tools/test_filesystem.py | 1460 | 1 | test_filesystem |
| tests/tools/test_runtime_integration.py | 619 | 1 | test_runtime_integration |

## Q1: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/reading.py | 1 | 1 | 0x1.b42ae8e1e23ebp+5 | 0x1.a7c6d39d09080p+5 | 0 |
| tests/resources/filesystem/test_reading.py | 2 | 2 | 0x1.95c573ece577fp+5 | 0x1.95c573ece577fp+5 | 0 |
| src/devtools/resources/filesystem/docs/io.md | 3 | 3 | 0x1.537c174edbc44p+5 | 0x1.537c174edbc44p+5 | 0 |
| src/devtools/context/repository/observation.py | 4 | 4 | 0x1.d59b1b617bdb6p+4 | 0x1.d59b1b617bdb5p+4 | 0 |
| src/devtools/resources/filesystem/__init__.py | 5 | 5 | 0x1.4b90935687c3cp+4 | 0x1.4b90935687c3cp+4 | 0 |
| tests/context/repository/test_observation.py | 6 | 6 | 0x1.31d9d5c7deb46p+4 | 0x1.31d9d5c7deb46p+4 | 0 |
| tests/context/repository/test_discovery.py | 7 | 7 | 0x1.2893fc155fd80p+4 | 0x1.2893fc155fd80p+4 | 0 |
| src/devtools/resources/filesystem/docs/overview.md | 8 | 8 | 0x1.2503f99b862f6p+4 | 0x1.2503f99b862f6p+4 | 0 |
| tests/resources/filesystem/test_writing.py | 9 | 9 | 0x1.d95b91ccde2b0p+3 | 0x1.d95b91ccde2b0p+3 | 0 |
| src/devtools/resources/commands/docs/command.md | 10 | 10 | 0x1.d92c6cbc9d9cdp+3 | 0x1.d92c6cbc9d9ccp+3 | 0 |
| src/devtools/resources/filesystem/resolution.py | 11 | 11 | 0x1.c79f3e5be8bc8p+3 | 0x1.c79f3e5be8bc8p+3 | 0 |
| src/devtools/tools/filesystem.py | 12 | 12 | 0x1.c66a6818384b8p+3 | 0x1.c66a6818384b8p+3 | 0 |
| tests/resources/filesystem/test_models.py | 13 | 13 | 0x1.b899e1e539978p+3 | 0x1.b899e1e539978p+3 | 0 |
| tests/context/python/function/test_rendering.py | 14 | 14 | 0x1.b5e56a2aa7cfcp+3 | 0x1.b5e56a2aa7cfcp+3 | 0 |
| tests/context/python/function/test_resource_selection.py | 15 | 15 | 0x1.b3bbb5e0d9688p+3 | 0x1.b3bbb5e0d9689p+3 | 0 |
| tests/context/python/function/test_request_assembly.py | 16 | 16 | 0x1.ab2bb6f97980ep+3 | 0x1.ab2bb6f97980ep+3 | 0 |
| src/devtools/resources/filesystem/models/binary.py | 17 | 17 | 0x1.aa461c08e88c2p+3 | 0x1.aa461c08e88c0p+3 | 0 |
| tests/context/python/function/test_materialization.py | 18 | 18 | 0x1.a8724bf8c4f4fp+3 | 0x1.a8724bf8c4f4ep+3 | 0 |
| tests/resources/filesystem/test_resolution.py | 19 | 19 | 0x1.a5b8a799ffa9ap+3 | 0x1.a5b8a799ffa9bp+3 | 0 |
| tests/context/python/test_source_candidacy.py | 20 | 20 | 0x1.9dd392e9a43e4p+3 | 0x1.9dd392e9a43e5p+3 | 0 |
| src/devtools/context/python/function/docs/overview.md | 21 | 21 | 0x1.959244d77c9bep+3 | 0x1.959244d77c9bfp+3 | 0 |
| src/devtools/resources/filesystem/models/text.py | 22 | 22 | 0x1.92647a792f8fdp+3 | 0x1.92647a792f8fcp+3 | 0 |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 23 | 23 | 0x1.8bbc665b0e4f8p+3 | 0x1.8bbc665b0e4f8p+3 | 0 |
| tests/tools/test_filesystem.py | 24 | 24 | 0x1.80dd60ec74849p+3 | 0x1.80dd60ec74848p+3 | 0 |
| tests/context/python/function/test_declaration_aggregation.py | 25 | 25 | 0x1.7aac609247453p+3 | 0x1.7aac609247453p+3 | 0 |
| tests/context/python/function/test_disclosure.py | 26 | 26 | 0x1.751b67f400762p+3 | 0x1.751b67f400762p+3 | 0 |
| tests/resources/filesystem/codecs/test_csv.py | 27 | 27 | 0x1.70e8ac576ddc4p+3 | 0x1.70e8ac576ddc4p+3 | 0 |
| src/devtools/models/serving/docs/overview.md | 28 | 28 | 0x1.6a39abb0010b6p+3 | 0x1.6a39abb0010b6p+3 | 0 |
| src/devtools/context/repository/discovery.py | 29 | 29 | 0x1.6933b400ab28ap+3 | 0x1.6933b400ab289p+3 | 0 |
| tests/context/python/function/test_candidates.py | 30 | 30 | 0x1.60df63c6f5da0p+3 | 0x1.60df63c6f5da0p+3 | 0 |
| tests/context/python/function/test_cross_resource_pipeline.py | 31 | 31 | 0x1.5bd8e046a6a10p+3 | 0x1.5bd8e046a6a10p+3 | 0 |
| src/devtools/resources/filesystem/codecs/json.py | 32 | 32 | 0x1.564a87e95d899p+3 | 0x1.564a87e95d898p+3 | 0 |
| src/devtools/context/python/function/rendering.py | 33 | 33 | 0x1.51992d1bfa95ep+3 | 0x1.51992d1bfa95ep+3 | 0 |
| src/devtools/models/benchmarks/storage.py | 34 | 34 | 0x1.50209df044ebep+3 | 0x1.50209df044ebdp+3 | 0 |
| tests/resources/filesystem/codecs/test_json.py | 35 | 35 | 0x1.4c86ecf8bcfd0p+3 | 0x1.4c86ecf8bcfd0p+3 | 0 |
| src/devtools/core/paths/docs/overview.md | 36 | 36 | 0x1.4c0e7840870a0p+3 | 0x1.4c0e7840870a1p+3 | 0 |
| tests/context/python/function/test_declarations.py | 37 | 37 | 0x1.4af5c55bb5861p+3 | 0x1.4af5c55bb5861p+3 | 0 |
| AGENTS.md | 38 | 38 | 0x1.413dea27b5b56p+3 | 0x1.413dea27b5b56p+3 | 0 |
| src/devtools/models/benchmarks/models.py | 39 | 39 | 0x1.3aad2074ea070p+3 | 0x1.3aad2074ea070p+3 | 0 |
| tests/tools/test_execution.py | 40 | 40 | 0x1.3275f26e0748ap+3 | 0x1.3275f26e0748bp+3 | 0 |
| src/devtools/resources/filesystem/docs/models.md | 41 | 41 | 0x1.312c5da40bf2fp+3 | 0x1.312c5da40bf2fp+3 | 0 |
| tests/agents/integrations/codex/test_live.py | 42 | 42 | 0x1.2f029b26b141ep+3 | 0x1.2f029b26b141ep+3 | 0 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 43 | 43 | 0x1.27751e3c32b2cp+3 | 0x1.27751e3c32b2cp+3 | 0 |
| src/devtools/agents/integrations/codex/docs/cli.md | 44 | 44 | 0x1.26bc6683ca73bp+3 | 0x1.26bc6683ca73bp+3 | 0 |
| tests/context/python/function/test_retrieval.py | 45 | 45 | 0x1.2331945272b09p+3 | 0x1.2331945272b08p+3 | 0 |
| tests/models/interaction/providers/test_llama_cpp.py | 46 | 46 | 0x1.22037443cf050p+3 | 0x1.22037443cf050p+3 | 0 |
| tests/context/python/function/test_qualified_reference.py | 47 | 47 | 0x1.20b43db765db4p+3 | 0x1.20b43db765db4p+3 | 0 |
| tests/models/interaction/test_tools.py | 48 | 48 | 0x1.202392ef05dedp+3 | 0x1.202392ef05dedp+3 | 0 |
| src/devtools/context/retrieval/lexical/bm25.py | 49 | 49 | 0x1.1f532b9d7c55dp+3 | 0x1.1f532b9d7c55dp+3 | 0 |
| tests/context/retrieval/lexical/test_bm25.py | 50 | 50 | 0x1.1c79685685fe4p+3 | 0x1.1c79685685fe4p+3 | 0 |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 51 | 60 | 0x1.1a601d04e79bcp+3 | 0x1.05d8086a3f962p+3 | -9 |
| tests/agents/conversation/test_live.py | 52 | 51 | 0x1.1735be5990538p+3 | 0x1.1735be5990538p+3 | 1 |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 53 | 52 | 0x1.173143e258555p+3 | 0x1.173143e258555p+3 | 1 |
| src/devtools/resources/filesystem/codecs/markdown.py | 54 | 53 | 0x1.0d92467b13e08p+3 | 0x1.0d92467b13e08p+3 | 1 |
| tests/context/repository/test_corpus.py | 55 | 54 | 0x1.0c620b3cfb3acp+3 | 0x1.0c620b3cfb3acp+3 | 1 |
| tests/context/retrieval/lexical/test_index.py | 56 | 55 | 0x1.0c530d6960ddfp+3 | 0x1.0c530d6960de0p+3 | 1 |
| docs/experiments/qwen38_llama_cpp.md | 57 | 56 | 0x1.0c09a8ba9193ap+3 | 0x1.0c09a8ba9193ap+3 | 1 |
| tests/models/interaction/test_models.py | 58 | 57 | 0x1.0906d68fa7d31p+3 | 0x1.0906d68fa7d30p+3 | 1 |
| src/devtools/context/retrieval/graph/pagerank.py | 59 | 58 | 0x1.076152c5287b1p+3 | 0x1.076152c5287b1p+3 | 1 |
| src/devtools/evaluation/docs/overview.md | 60 | 59 | 0x1.073158d0abafbp+3 | 0x1.073158d0abafbp+3 | 1 |
| tests/context/python/project_configuration/test_configuration.py | 61 | 61 | 0x1.053531c6c426fp+3 | 0x1.053531c6c426ep+3 | 0 |
| tests/scripts/qwen/test_two_read_acceptance.py | 62 | 62 | 0x1.fab146d3aa4ccp+2 | 0x1.fab146d3aa4cbp+2 | 0 |
| src/devtools/models/serving/huggingface.py | 63 | 63 | 0x1.f7c3e32aaa590p+2 | 0x1.f7c3e32aaa58fp+2 | 0 |
| src/devtools/resources/filesystem/docs/csv.md | 64 | 64 | 0x1.f6ae12c27f712p+2 | 0x1.f6ae12c27f712p+2 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 65 | 65 | 0x1.f5ea945481b00p+2 | 0x1.f5ea945481b01p+2 | 0 |
| tests/resources/commands/test_execution.py | 66 | 66 | 0x1.ef1c7844c6b76p+2 | 0x1.ef1c7844c6b75p+2 | 0 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 67 | 67 | 0x1.e58c593ef6ea1p+2 | 0x1.e58c593ef6ea0p+2 | 0 |
| tests/context/retrieval/lexical/test_analysis.py | 68 | 68 | 0x1.e30f8fd1689eap+2 | 0x1.e30f8fd1689e9p+2 | 0 |
| src/devtools/context/python/function/qualified_reference.py | 69 | 69 | 0x1.e2664ed08f0fap+2 | 0x1.e2664ed08f0fap+2 | 0 |
| src/devtools/models/serving/vllm.py | 70 | 70 | 0x1.da9a7dfb9b298p+2 | 0x1.da9a7dfb9b297p+2 | 0 |
| src/devtools/context/python/classes/docs/overview.md | 71 | 71 | 0x1.d77aa62787767p+2 | 0x1.d77aa62787767p+2 | 0 |
| tests/resources/filesystem/models/markdown/test_file.py | 72 | 72 | 0x1.d5251ab4751d9p+2 | 0x1.d5251ab4751d9p+2 | 0 |
| tests/resources/filesystem/codecs/test_text.py | 73 | 73 | 0x1.d4fb932c9e8acp+2 | 0x1.d4fb932c9e8acp+2 | 0 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 74 | 74 | 0x1.d461e07c4d6b2p+2 | 0x1.d461e07c4d6b2p+2 | 0 |
| tests/resources/filesystem/test_json_models.py | 75 | 75 | 0x1.d3643b11e3556p+2 | 0x1.d3643b11e3556p+2 | 0 |
| src/devtools/context/python/mirrored_paths.py | 76 | 76 | 0x1.d2e2424245c6bp+2 | 0x1.d2e2424245c6ap+2 | 0 |
| tests/context/retrieval/graph/test_typed.py | 77 | 77 | 0x1.d1ac806a22be7p+2 | 0x1.d1ac806a22be8p+2 | 0 |
| tests/resources/filesystem/codecs/test_markdown.py | 78 | 78 | 0x1.cef2cc3c22906p+2 | 0x1.cef2cc3c22905p+2 | 0 |
| tests/context/retrieval/lexical/test_evaluation.py | 79 | 79 | 0x1.cebbc2de7a9fcp+2 | 0x1.cebbc2de7a9fdp+2 | 0 |
| tests/context/retrieval/test_structural.py | 80 | 80 | 0x1.cd11d9f35df6dp+2 | 0x1.cd11d9f35df6cp+2 | 0 |
| tests/context/retrieval/graph/test_ranking.py | 81 | 81 | 0x1.cad95bf3c55cap+2 | 0x1.cad95bf3c55c9p+2 | 0 |
| src/devtools/context/python/function/materialization.py | 82 | 82 | 0x1.c9304d0fb9786p+2 | 0x1.c9304d0fb9786p+2 | 0 |
| tests/resources/filesystem/test_json_conversion.py | 83 | 83 | 0x1.c878e4a55a24dp+2 | 0x1.c878e4a55a24dp+2 | 0 |
| tests/context/python/test_mirrored_paths.py | 84 | 84 | 0x1.bfb30b182a39ep+2 | 0x1.bfb30b182a39ep+2 | 0 |
| src/devtools/context/planning/resource.py | 85 | 85 | 0x1.be9fe0327fcacp+2 | 0x1.be9fe0327fcabp+2 | 0 |
| src/devtools/core/time/docs/timestamps.md | 86 | 86 | 0x1.ba8edd0a13b70p+2 | 0x1.ba8edd0a13b70p+2 | 0 |
| src/devtools/models/benchmarks/runner.py | 87 | 87 | 0x1.ba3620cfad4a4p+2 | 0x1.ba3620cfad4a4p+2 | 0 |
| src/devtools/resources/filesystem/models/base.py | 88 | 88 | 0x1.b9a3da483300ep+2 | 0x1.b9a3da4833010p+2 | 0 |
| tests/resources/filesystem/models/csv/test_file.py | 89 | 89 | 0x1.b67fe30800d72p+2 | 0x1.b67fe30800d73p+2 | 0 |
| src/devtools/resources/filesystem/codecs/text.py | 90 | 90 | 0x1.b44cce26714f6p+2 | 0x1.b44cce26714f6p+2 | 0 |
| src/devtools/agents/integrations/codex/agent.py | 91 | 91 | 0x1.b2a6cc953e92cp+2 | 0x1.b2a6cc953e92cp+2 | 0 |
| tests/context/repository/test_document.py | 92 | 92 | 0x1.acd43b0cfc208p+2 | 0x1.acd43b0cfc207p+2 | 0 |
| docs/backlog/items/B-0007-correct-model-serving-documentation-drift.md | 93 | 93 | 0x1.ac07d6259ab84p+2 | 0x1.ac07d6259ab86p+2 | 0 |
| src/devtools/context/planning/rendering.py | 94 | 94 | 0x1.aa0c3e3a934dfp+2 | 0x1.aa0c3e3a934dfp+2 | 0 |
| src/devtools/resources/filesystem/errors.py | 95 | 95 | 0x1.a7579791a341cp+2 | 0x1.a7579791a341cp+2 | 0 |
| tests/context/python/imports/test_relations.py | 96 | 96 | 0x1.a31793a3ad89ap+2 | 0x1.a31793a3ad89ap+2 | 0 |
| docs/backlog/epics/B-0005-effect-governance.md | 97 | 97 | 0x1.a1fb38a2aa94cp+2 | 0x1.a1fb38a2aa94bp+2 | 0 |
| src/devtools/resources/filesystem/codecs/csv.py | 98 | 98 | 0x1.a1c4b1794601ap+2 | 0x1.a1c4b1794601ap+2 | 0 |
| tests/models/serving/test_huggingface.py | 99 | 99 | 0x1.a19660131a32ep+2 | 0x1.a19660131a32fp+2 | 0 |
| tests/context/retrieval/repository_map/test_ranking.py | 100 | 100 | 0x1.98bbebe53e052p+2 | 0x1.98bbebe53e053p+2 | 0 |
| tests/core/paths/test_resolution.py | 101 | 101 | 0x1.962554e63ebf6p+2 | 0x1.962554e63ebf4p+2 | 0 |
| src/devtools/core/regex/models.py | 102 | 102 | 0x1.950ea83f69266p+2 | 0x1.950ea83f69266p+2 | 0 |
| tests/context/python/imports/test_declarations.py | 103 | 103 | 0x1.92031b1e8bc86p+2 | 0x1.92031b1e8bc86p+2 | 0 |
| docs/backlog/epics/B-0003-local-coding-worker-harness.md | 104 | 104 | 0x1.8dd6169d6af9ep+2 | 0x1.8dd6169d6af9cp+2 | 0 |
| src/devtools/models/serving/llama_cpp.py | 105 | 105 | 0x1.8bf965f3aa1b7p+2 | 0x1.8bf965f3aa1b7p+2 | 0 |
| src/devtools/context/python/function/retrieval.py | 106 | 106 | 0x1.886a09e709874p+2 | 0x1.886a09e709874p+2 | 0 |
| src/devtools/context/python/modules/docs/overview.md | 107 | 107 | 0x1.82e2f2f23e5d7p+2 | 0x1.82e2f2f23e5d7p+2 | 0 |
| docs/backlog/items/B-0044-investigate-orchestration-control-loops.md | 108 | 108 | 0x1.817b5b5748badp+2 | 0x1.817b5b5748baep+2 | 0 |
| src/devtools/core/paths/docs/resolution.md | 109 | 109 | 0x1.812d0503e959fp+2 | 0x1.812d0503e959ep+2 | 0 |
| src/devtools/core/conversion/docs/overview.md | 110 | 110 | 0x1.7c1b2f0e36d42p+2 | 0x1.7c1b2f0e36d42p+2 | 0 |
| tests/context/python/references/declarations/test_analysis.py | 111 | 111 | 0x1.7b945ee172c90p+2 | 0x1.7b945ee172c90p+2 | 0 |
| tests/context/python/modules/test_interpretation.py | 112 | 112 | 0x1.77bbeeeb04935p+2 | 0x1.77bbeeeb04936p+2 | 0 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 113 | 113 | 0x1.768e7eb3d87bfp+2 | 0x1.768e7eb3d87c0p+2 | 0 |
| tests/observability/evidence/test_model_interaction.py | 114 | 114 | 0x1.768482813987ap+2 | 0x1.768482813987bp+2 | 0 |
| tests/context/python/classes/test_declarations.py | 115 | 115 | 0x1.76511af8009f4p+2 | 0x1.76511af8009f3p+2 | 0 |
| src/devtools/context/python/source_candidacy.py | 116 | 116 | 0x1.7545cc69a145cp+2 | 0x1.7545cc69a145cp+2 | 0 |
| src/devtools/resources/filesystem/docs/json.md | 117 | 117 | 0x1.71382a41ad2b3p+2 | 0x1.71382a41ad2b4p+2 | 0 |
| src/devtools/core/regex/docs/overview.md | 118 | 118 | 0x1.70227970fb290p+2 | 0x1.70227970fb290p+2 | 0 |
| tests/scripts/test_validate_development.py | 119 | 119 | 0x1.6eced465e53a0p+2 | 0x1.6eced465e53a0p+2 | 0 |
| src/devtools/resources/commands/execution.py | 120 | 120 | 0x1.6c6b4650059eap+2 | 0x1.6c6b4650059e9p+2 | 0 |
| tests/core/regex/test_search.py | 121 | 121 | 0x1.687767f0ff312p+2 | 0x1.687767f0ff312p+2 | 0 |
| src/devtools/context/retrieval/docs/overview.md | 122 | 122 | 0x1.6603c0395236cp+2 | 0x1.6603c0395236cp+2 | 0 |
| tests/context/python/modules/test_membership.py | 123 | 123 | 0x1.65f05f67abcc1p+2 | 0x1.65f05f67abcc1p+2 | 0 |
| tests/context/python/function/test_containment.py | 124 | 124 | 0x1.64cb28429f5eep+2 | 0x1.64cb28429f5eep+2 | 0 |
| src/devtools/core/paths/models.py | 125 | 125 | 0x1.648d4663fac08p+2 | 0x1.648d4663fac08p+2 | 0 |
| tests/context/retrieval/test_composition.py | 126 | 126 | 0x1.646169b0fc87cp+2 | 0x1.646169b0fc87cp+2 | 0 |
| tests/context/python/imports/test_resolution.py | 127 | 127 | 0x1.5df6d3a3cdddap+2 | 0x1.5df6d3a3cdddap+2 | 0 |
| src/devtools/context/python/docs/overview.md | 128 | 128 | 0x1.5cc6848a912c4p+2 | 0x1.5cc6848a912c4p+2 | 0 |
| tests/scripts/test_retrieval_bm25_baseline.py | 129 | 129 | 0x1.59bd083de0156p+2 | 0x1.59bd083de0154p+2 | 0 |
| tests/context/localization/roles/test_evidence.py | 130 | 130 | 0x1.5995085a55e08p+2 | 0x1.5995085a55e08p+2 | 0 |
| tests/context/planning/test_plan.py | 131 | 131 | 0x1.5746bcc479d7ep+2 | 0x1.5746bcc479d7ep+2 | 0 |
| docs/backlog/items/B-0023-investigate-observability-architecture.md | 132 | 132 | 0x1.56239b339d029p+2 | 0x1.56239b339d029p+2 | 0 |
| src/devtools/context/localization/roles/models.py | 133 | 133 | 0x1.4eafabf47bd0ep+2 | 0x1.4eafabf47bd0ep+2 | 0 |
| tests/evaluation/test_coverage.py | 134 | 134 | 0x1.4c332a989b49ep+2 | 0x1.4c332a989b49ep+2 | 0 |
| src/devtools/context/localization/association/references.py | 135 | 135 | 0x1.48682a00a60c5p+2 | 0x1.48682a00a60c4p+2 | 0 |
| tests/context/python/imports/test_members.py | 136 | 136 | 0x1.47ebecb876e86p+2 | 0x1.47ebecb876e86p+2 | 0 |
| tests/tools/test_runtime_integration.py | 137 | 137 | 0x1.47cd4ab43cf7bp+2 | 0x1.47cd4ab43cf7bp+2 | 0 |
| src/devtools/context/python/function/request_assembly.py | 138 | 138 | 0x1.4753a22be56fcp+2 | 0x1.4753a22be56fcp+2 | 0 |
| src/devtools/resources/filesystem/models/json/object.py | 139 | 139 | 0x1.45d60d7024096p+2 | 0x1.45d60d7024096p+2 | 0 |
| pyproject.toml | 140 | 140 | 0x1.45ca33473edd0p+2 | 0x1.45ca33473edd0p+2 | 0 |
| tests/context/python/classes/test_bases.py | 141 | 141 | 0x1.459a4618e5351p+2 | 0x1.459a4618e5352p+2 | 0 |
| src/devtools/resources/filesystem/docs/roadmap.md | 142 | 142 | 0x1.42ad64a9340c6p+2 | 0x1.42ad64a9340c6p+2 | 0 |
| tests/core/time/test_models.py | 143 | 143 | 0x1.3de5152de4844p+2 | 0x1.3de5152de4843p+2 | 0 |
| tests/agents/integrations/codex/test_agent.py | 144 | 144 | 0x1.39ed6d6c8c202p+2 | 0x1.39ed6d6c8c201p+2 | 0 |
| tests/context/retrieval/lexical/test_statistics.py | 145 | 145 | 0x1.361ba7a1c3c28p+2 | 0x1.361ba7a1c3c28p+2 | 0 |
| tests/context/localization/generation/test_references.py | 146 | 146 | 0x1.343d2c95e13f4p+2 | 0x1.343d2c95e13f4p+2 | 0 |
| tests/context/retrieval/lexical/test_filename.py | 147 | 147 | 0x1.30f0343e48260p+2 | 0x1.30f0343e48261p+2 | 0 |
| tests/models/benchmarks/test_storage.py | 148 | 148 | 0x1.3082ef232a7d9p+2 | 0x1.3082ef232a7d8p+2 | 0 |
| tests/scripts/qwen/test_llama_cpp_service.py | 149 | 149 | 0x1.2f6f9a12a9ac2p+2 | 0x1.2f6f9a12a9ac1p+2 | 0 |
| src/devtools/core/time/models/duration.py | 150 | 150 | 0x1.2cc63364d10d3p+2 | 0x1.2cc63364d10d3p+2 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 151 | 207 | 0x1.2a25d458f5f68p+2 | 0x1.88d5aec46ffc5p+1 | -56 |
| src/devtools/resources/commands/models/output.py | 152 | 151 | 0x1.299c51d579cafp+2 | 0x1.299c51d579caep+2 | 1 |
| tests/core/regex/test_models.py | 153 | 152 | 0x1.25b88c1ab7d4dp+2 | 0x1.25b88c1ab7d4dp+2 | 1 |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 154 | 153 | 0x1.23542efdda246p+2 | 0x1.23542efdda247p+2 | 1 |
| src/devtools/models/interaction/docs/overview.md | 155 | 154 | 0x1.1f7c19f794174p+2 | 0x1.1f7c19f794174p+2 | 1 |
| tests/context/retrieval/lexical/_helpers.py | 156 | 155 | 0x1.1f6d907200034p+2 | 0x1.1f6d907200035p+2 | 1 |
| tests/context/localization/resolution/test_resolution.py | 157 | 156 | 0x1.1f08a550a098cp+2 | 0x1.1f08a550a098dp+2 | 1 |
| tests/models/serving/test_llama_cpp.py | 158 | 157 | 0x1.1cf0bfaced7e0p+2 | 0x1.1cf0bfaced7dfp+2 | 1 |
| tests/resources/commands/test_handle.py | 159 | 158 | 0x1.1b995f537cf6ep+2 | 0x1.1b995f537cf6ep+2 | 1 |
| src/devtools/core/time/docs/overview.md | 160 | 159 | 0x1.1720d183e7696p+2 | 0x1.1720d183e7696p+2 | 1 |
| src/devtools/context/python/function/declarations.py | 161 | 160 | 0x1.12d6ce0718fd6p+2 | 0x1.12d6ce0718fd6p+2 | 1 |
| tests/context/localization/generation/test_imports.py | 162 | 161 | 0x1.10d21e22622d4p+2 | 0x1.10d21e22622d4p+2 | 1 |
| tests/observability/evidence/test_protocols.py | 163 | 162 | 0x1.0e129071ad165p+2 | 0x1.0e129071ad165p+2 | 1 |
| src/devtools/core/conversion/errors.py | 164 | 163 | 0x1.0c4afdc821544p+2 | 0x1.0c4afdc821543p+2 | 1 |
| src/devtools/models/interaction/providers/llama_cpp.py | 165 | 164 | 0x1.0ad6075e71c9ep+2 | 0x1.0ad6075e71c9ep+2 | 1 |
| tests/scripts/test_vllm_benchmark_driver.py | 166 | 165 | 0x1.08cd57b201d66p+2 | 0x1.08cd57b201d67p+2 | 1 |
| src/devtools/context/python/references/docs/overview.md | 167 | 166 | 0x1.064294e773ee8p+2 | 0x1.064294e773ee8p+2 | 1 |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 168 | 167 | 0x1.0530dae1774ccp+2 | 0x1.0530dae1774cdp+2 | 1 |
| src/devtools/resources/filesystem/writing.py | 169 | 168 | 0x1.031087c9b3300p+2 | 0x1.031087c9b32ffp+2 | 1 |
| tests/models/benchmarks/test_runner.py | 170 | 169 | 0x1.fca4f4699793cp+1 | 0x1.fca4f4699793cp+1 | 1 |
| src/devtools/models/interaction/usage.py | 171 | 170 | 0x1.f9133e3abc16dp+1 | 0x1.f9133e3abc16dp+1 | 1 |
| tests/context/localization/grounding/test_grounding.py | 172 | 171 | 0x1.f2c3f853eb848p+1 | 0x1.f2c3f853eb847p+1 | 1 |
| tests/context/python/project_configuration/test_settings.py | 173 | 172 | 0x1.e8bb81f6df928p+1 | 0x1.e8bb81f6df92ap+1 | 1 |
| docs/backlog/items/B-0012-investigate-governed-effect-semantics.md | 174 | 173 | 0x1.e45f676ffef1dp+1 | 0x1.e45f676ffef1dp+1 | 1 |
| tests/context/localization/roles/test_configuration.py | 175 | 174 | 0x1.e24787338ff38p+1 | 0x1.e24787338ff39p+1 | 1 |
| docs/backlog/items/B-0045-establish-minimal-model-interaction-core.md | 176 | 175 | 0x1.e1688a70de4e0p+1 | 0x1.e1688a70de4e0p+1 | 1 |
| src/devtools/context/repository/corpus.py | 177 | 176 | 0x1.d22ab12fe943dp+1 | 0x1.d22ab12fe943fp+1 | 1 |
| docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md | 178 | 177 | 0x1.cea688834f562p+1 | 0x1.cea688834f562p+1 | 1 |
| tests/context/repository/test_intrinsic_paths.py | 179 | 178 | 0x1.cbabe5151f87cp+1 | 0x1.cbabe5151f87dp+1 | 1 |
| docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md | 180 | 179 | 0x1.caf068542a7ddp+1 | 0x1.caf068542a7dep+1 | 1 |
| docs/backlog/metadata.md | 181 | 180 | 0x1.cadef7fb0dc68p+1 | 0x1.cadef7fb0dc68p+1 | 1 |
| docs/backlog/items/B-0036-investigate-action-request-semantics.md | 182 | 181 | 0x1.ca9ac9ae842e5p+1 | 0x1.ca9ac9ae842e5p+1 | 1 |
| src/devtools/context/retrieval/structural.py | 183 | 182 | 0x1.c531386f0c4b0p+1 | 0x1.c531386f0c4aep+1 | 1 |
| tests/core/paths/test_resolved_path.py | 184 | 183 | 0x1.c50b782e4d7d8p+1 | 0x1.c50b782e4d7d8p+1 | 1 |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 185 | 184 | 0x1.c0cafb8b4499fp+1 | 0x1.c0cafb8b4499fp+1 | 1 |
| src/devtools/resources/filesystem/models/__init__.py | 186 | 185 | 0x1.bd7f2cb701337p+1 | 0x1.bd7f2cb701337p+1 | 1 |
| src/devtools/tools/docs/overview.md | 187 | 186 | 0x1.b6c78bd3f6dccp+1 | 0x1.b6c78bd3f6dccp+1 | 1 |
| tests/context/localization/roles/test_inputs.py | 188 | 187 | 0x1.b5f453e461235p+1 | 0x1.b5f453e461236p+1 | 1 |
| tests/context/localization/generation/test_branching.py | 189 | 188 | 0x1.b1fb87a8d8087p+1 | 0x1.b1fb87a8d8088p+1 | 1 |
| tests/context/localization/generation/test_generation.py | 190 | 189 | 0x1.adb9db1b5102dp+1 | 0x1.adb9db1b5102dp+1 | 1 |
| src/devtools/resources/filesystem/models/json/base.py | 191 | 190 | 0x1.ad3ec4067e4e9p+1 | 0x1.ad3ec4067e4ebp+1 | 1 |
| tests/context/localization/test_lexical.py | 192 | 191 | 0x1.a927a41e531fep+1 | 0x1.a927a41e531fep+1 | 1 |
| src/devtools/context/localization/generation/contract.py | 193 | 192 | 0x1.a63c9a8d5252cp+1 | 0x1.a63c9a8d5252cp+1 | 1 |
| src/devtools/core/paths/resolution.py | 194 | 193 | 0x1.a3f792b35a253p+1 | 0x1.a3f792b35a252p+1 | 1 |
| src/devtools/tools/execution.py | 195 | 194 | 0x1.a396fb8adbc7ep+1 | 0x1.a396fb8adbc7ep+1 | 1 |
| src/devtools/execution/interaction_attempt.py | 196 | 195 | 0x1.a01c1fd608992p+1 | 0x1.a01c1fd608993p+1 | 1 |
| src/devtools/context/python/modules/interpretation.py | 197 | 196 | 0x1.a01a1345ecb78p+1 | 0x1.a01a1345ecb78p+1 | 1 |
| tests/resources/commands/test_models.py | 198 | 197 | 0x1.9aca851a35ec6p+1 | 0x1.9aca851a35ec6p+1 | 1 |
| src/devtools/resources/filesystem/models/json/list.py | 199 | 198 | 0x1.995f7bb1c4158p+1 | 0x1.995f7bb1c4159p+1 | 1 |
| docs/backlog/items/B-0030-investigate-provider-neutral-generative-model-interaction.md | 200 | 199 | 0x1.97a18c117042dp+1 | 0x1.97a18c117042dp+1 | 1 |
| docs/backlog/items/B-0042-investigate-workflow-lifecycle-control.md | 201 | 200 | 0x1.97a18c117042dp+1 | 0x1.97a18c117042dp+1 | 1 |
| docs/backlog/items/B-0032-investigate-execution-retry-mechanics.md | 202 | 201 | 0x1.971a88305675ep+1 | 0x1.971a88305675dp+1 | 1 |
| src/devtools/core/paths/__init__.py | 203 | 202 | 0x1.91f8772f432edp+1 | 0x1.91f8772f432edp+1 | 1 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 204 | 203 | 0x1.9072bd715abfep+1 | 0x1.9072bd715abfep+1 | 1 |
| src/devtools/resources/commands/models/result.py | 205 | 204 | 0x1.8ddbe5988260fp+1 | 0x1.8ddbe59882610p+1 | 1 |
| src/devtools/models/interaction/providers/llama_cpp_errors.py | 206 | 205 | 0x1.8dd6a4626d44cp+1 | 0x1.8dd6a4626d44cp+1 | 1 |
| src/devtools/resources/commands/docs/events.md | 207 | 206 | 0x1.89b9f5cdd0bbap+1 | 0x1.89b9f5cdd0bbap+1 | 1 |
| tests/tools/test_command.py | 208 | 208 | 0x1.88c86e268c20fp+1 | 0x1.88c86e268c211p+1 | 0 |
| src/devtools/agents/conversation/docs/overview.md | 209 | 209 | 0x1.886192bb38c3cp+1 | 0x1.886192bb38c3cp+1 | 0 |
| tests/context/python/modules/test_selection.py | 210 | 210 | 0x1.87c11dd83d716p+1 | 0x1.87c11dd83d716p+1 | 0 |
| src/devtools/persistence/docs/json.md | 211 | 211 | 0x1.80f10711fab0bp+1 | 0x1.80f10711fab0dp+1 | 0 |
| src/devtools/core/time/models/timestamp.py | 212 | 212 | 0x1.7fd3a558c14e6p+1 | 0x1.7fd3a558c14e7p+1 | 0 |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 213 | 213 | 0x1.71c917a3edaedp+1 | 0x1.71c917a3edaebp+1 | 0 |
| src/devtools/execution/docs/overview.md | 214 | 214 | 0x1.700e2a091309ap+1 | 0x1.700e2a0913099p+1 | 0 |
| tests/context/localization/routing/test_routing.py | 215 | 215 | 0x1.6f4fe18421ddbp+1 | 0x1.6f4fe18421ddbp+1 | 0 |
| tests/context/localization/roles/helpers.py | 216 | 216 | 0x1.6760df2a8fc09p+1 | 0x1.6760df2a8fc08p+1 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 217 | 217 | 0x1.668c97ff44da1p+1 | 0x1.668c97ff44da1p+1 | 0 |
| src/devtools/resources/commands/models/command.py | 218 | 218 | 0x1.5fd69efee43a8p+1 | 0x1.5fd69efee43a7p+1 | 0 |
| src/devtools/models/benchmarks/docs/overview.md | 219 | 219 | 0x1.54a1ef29e5bb2p+1 | 0x1.54a1ef29e5bb2p+1 | 0 |
| src/devtools/models/interaction/observation.py | 220 | 220 | 0x1.52bc0efdf86c3p+1 | 0x1.52bc0efdf86c3p+1 | 0 |
| src/devtools/core/regex/search.py | 221 | 221 | 0x1.4bfad17beb477p+1 | 0x1.4bfad17beb477p+1 | 0 |
| src/devtools/resources/filesystem/docs/codecs.md | 222 | 222 | 0x1.4b049e5a251e2p+1 | 0x1.4b049e5a251e2p+1 | 0 |
| tests/context/python/references/declarations/test_bindings.py | 223 | 223 | 0x1.495f961069baep+1 | 0x1.495f961069badp+1 | 0 |
| tests/persistence/test_sqlite.py | 224 | 224 | 0x1.412c9666a6399p+1 | 0x1.412c9666a6398p+1 | 0 |
| src/devtools/context/python/project_configuration/resolution.py | 225 | 225 | 0x1.406c65b693f74p+1 | 0x1.406c65b693f74p+1 | 0 |
| src/devtools/context/python/imports/declarations.py | 226 | 226 | 0x1.3c7ef5f764c25p+1 | 0x1.3c7ef5f764c25p+1 | 0 |
| src/devtools/context/python/modules/lookup.py | 227 | 227 | 0x1.3ba6a32cd6eccp+1 | 0x1.3ba6a32cd6ecbp+1 | 0 |
| src/devtools/context/python/modules/selection.py | 228 | 228 | 0x1.3807c93b64609p+1 | 0x1.3807c93b64608p+1 | 0 |
| src/devtools/context/python/function/candidates.py | 229 | 229 | 0x1.3303e2604d3b4p+1 | 0x1.3303e2604d3b4p+1 | 0 |
| src/devtools/context/python/imports/docs/overview.md | 230 | 230 | 0x1.31d3dbf1b92d6p+1 | 0x1.31d3dbf1b92d5p+1 | 0 |
| src/devtools/context/localization/resolution/contract.py | 231 | 231 | 0x1.31394aec7f128p+1 | 0x1.31394aec7f127p+1 | 0 |
| tests/agents/conversation/test_session.py | 232 | 232 | 0x1.31244e2814abap+1 | 0x1.31244e2814abbp+1 | 0 |
| src/devtools/context/localization/grounding/contract.py | 233 | 233 | 0x1.2fc2a2b8812efp+1 | 0x1.2fc2a2b8812eep+1 | 0 |
| src/devtools/context/localization/grounding/resolve.py | 234 | 234 | 0x1.2f3230375bd22p+1 | 0x1.2f3230375bd21p+1 | 0 |
| src/devtools/context/python/function/disclosure.py | 235 | 235 | 0x1.2ecb89ece5823p+1 | 0x1.2ecb89ece5822p+1 | 0 |
| tests/scripts/qwen/test_llama_cpp_profile.py | 236 | 236 | 0x1.2d9f806a90a67p+1 | 0x1.2d9f806a90a67p+1 | 0 |
| src/devtools/context/localization/roles/derivation.py | 237 | 237 | 0x1.2bd77d2ea7364p+1 | 0x1.2bd77d2ea7365p+1 | 0 |
| tests/models/benchmarks/test_models.py | 238 | 238 | 0x1.2a1c8cc469463p+1 | 0x1.2a1c8cc469463p+1 | 0 |
| tests/models/serving/test_vllm.py | 239 | 239 | 0x1.272ebdcb4d825p+1 | 0x1.272ebdcb4d824p+1 | 0 |
| README.md | 240 | 240 | 0x1.26f5a35c0abdcp+1 | 0x1.26f5a35c0abdcp+1 | 0 |
| src/devtools/context/retrieval/graph/view.py | 241 | 241 | 0x1.181b8c2229a57p+1 | 0x1.181b8c2229a58p+1 | 0 |
| src/devtools/context/retrieval/lexical/analysis.py | 242 | 242 | 0x1.14027f2ca9b8cp+1 | 0x1.14027f2ca9b8cp+1 | 0 |
| src/devtools/context/python/function/planned_reference.py | 243 | 243 | 0x1.127e961154191p+1 | 0x1.127e961154191p+1 | 0 |
| src/devtools/context/repository/document.py | 244 | 244 | 0x1.0e0bfee37f43ap+1 | 0x1.0e0bfee37f43ap+1 | 0 |
| src/devtools/context/retrieval/fusion.py | 245 | 245 | 0x1.0a8823f45d5aap+1 | 0x1.0a8823f45d5abp+1 | 0 |
| src/devtools/core/system/docs/overview.md | 246 | 246 | 0x1.0936652f62b35p+1 | 0x1.0936652f62b36p+1 | 0 |
| src/devtools/models/interaction/models.py | 247 | 247 | 0x1.05cb61e2e89cdp+1 | 0x1.05cb61e2e89cdp+1 | 0 |
| src/devtools/context/localization/association/imports.py | 248 | 248 | 0x1.02138fc8563a3p+1 | 0x1.02138fc8563a3p+1 | 0 |
| src/devtools/context/retrieval/lexical/filename.py | 249 | 249 | 0x1.fc5ba3cd3b7e8p+0 | 0x1.fc5ba3cd3b7e9p+0 | 0 |
| src/devtools/context/localization/association/structural.py | 250 | 250 | 0x1.f0d327ce301e7p+0 | 0x1.f0d327ce301e9p+0 | 0 |
| src/devtools/context/planning/docs/overview.md | 251 | 251 | 0x1.e2bc03ea8c4a8p+0 | 0x1.e2bc03ea8c4a7p+0 | 0 |
| src/devtools/context/localization/routing/docs/overview.md | 252 | 252 | 0x1.e0b436b4ba530p+0 | 0x1.e0b436b4ba531p+0 | 0 |
| src/devtools/agents/conversation/conversation.py | 253 | 253 | 0x1.deadec703c520p+0 | 0x1.deadec703c520p+0 | 0 |
| src/devtools/context/python/references/declarations/analysis.py | 254 | 254 | 0x1.d40c4b4dfd6d4p+0 | 0x1.d40c4b4dfd6d3p+0 | 0 |
| src/devtools/context/python/modules/membership.py | 255 | 255 | 0x1.d0a8831764e4ap+0 | 0x1.d0a8831764e49p+0 | 0 |
| src/devtools/context/python/references/declarations/model.py | 256 | 256 | 0x1.d083d6c0419d0p+0 | 0x1.d083d6c0419d0p+0 | 0 |
| src/devtools/persistence/sqlite.py | 257 | 257 | 0x1.cc00cf6486c1ap+0 | 0x1.cc00cf6486c1ap+0 | 0 |
| src/devtools/context/localization/grounding/view.py | 258 | 258 | 0x1.cbb5d32f6d529p+0 | 0x1.cbb5d32f6d528p+0 | 0 |
| src/devtools/context/retrieval/lexical/index.py | 259 | 259 | 0x1.c9b691da961f9p+0 | 0x1.c9b691da961f7p+0 | 0 |
| src/devtools/context/localization/generation/references.py | 260 | 260 | 0x1.c8ab04a2be2f8p+0 | 0x1.c8ab04a2be2f8p+0 | 0 |
| src/devtools/context/repository/snapshot.py | 261 | 261 | 0x1.c71bf94956601p+0 | 0x1.c71bf94956601p+0 | 0 |
| src/devtools/context/python/project_configuration/models.py | 262 | 262 | 0x1.bd60c45a6ff7fp+0 | 0x1.bd60c45a6ff7fp+0 | 0 |
| src/devtools/context/localization/generation/imports.py | 263 | 263 | 0x1.b2d3385d1a1dcp+0 | 0x1.b2d3385d1a1dcp+0 | 0 |
| src/devtools/context/localization/resolution/view.py | 264 | 264 | 0x1.ab86dd35cb467p+0 | 0x1.ab86dd35cb466p+0 | 0 |
| src/devtools/resources/filesystem/docs/markdown.md | 265 | 265 | 0x1.aa069a012ed40p+0 | 0x1.aa069a012ed40p+0 | 0 |
| src/devtools/context/localization/roles/configuration.py | 266 | 266 | 0x1.a3b7f4d701b1ap+0 | 0x1.a3b7f4d701b19p+0 | 0 |
| src/devtools/context/retrieval/repository_map/importance.py | 267 | 267 | 0x1.98335309a2b66p+0 | 0x1.98335309a2b66p+0 | 0 |
| src/devtools/context/retrieval/lexical/statistics.py | 268 | 268 | 0x1.96f45f84a4292p+0 | 0x1.96f45f84a4292p+0 | 0 |
| src/devtools/context/planning/materialization.py | 269 | 269 | 0x1.93431869313e9p+0 | 0x1.93431869313e8p+0 | 0 |
| src/devtools/observability/evidence/docs/overview.md | 270 | 270 | 0x1.90d66200eec2cp+0 | 0x1.90d66200eec2dp+0 | 0 |
| tests/context/localization/association/test_hypothesis.py | 271 | 271 | 0x1.9042638b3b4eep+0 | 0x1.9042638b3b4edp+0 | 0 |
| docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md | 272 | 272 | 0x1.84c2b1c5d271dp+0 | 0x1.84c2b1c5d271dp+0 | 0 |
| src/devtools/observability/evidence/model_interaction.py | 273 | 273 | 0x1.7f0b174bec702p+0 | 0x1.7f0b174bec702p+0 | 0 |
| src/devtools/context/python/project_configuration/declarations.py | 274 | 274 | 0x1.7ecec27fb9a03p+0 | 0x1.7ecec27fb9a03p+0 | 0 |
| src/devtools/context/python/imports/relations.py | 275 | 275 | 0x1.7e710fdcd01e9p+0 | 0x1.7e710fdcd01e9p+0 | 0 |
| src/devtools/context/localization/generation/generate.py | 276 | 276 | 0x1.78d1cd98c6258p+0 | 0x1.78d1cd98c6257p+0 | 0 |
| src/devtools/context/planning/plan.py | 277 | 277 | 0x1.75837cfea0ec8p+0 | 0x1.75837cfea0ec7p+0 | 0 |
| src/devtools/context/python/function/containment.py | 278 | 278 | 0x1.62a33c1259df6p+0 | 0x1.62a33c1259df5p+0 | 0 |
| src/devtools/context/localization/roles/inputs.py | 279 | 279 | 0x1.5ee77f6f9e2fap+0 | 0x1.5ee77f6f9e2f8p+0 | 0 |
| src/devtools/context/localization/readiness.py | 280 | 280 | 0x1.5e617266d472bp+0 | 0x1.5e617266d472bp+0 | 0 |
| src/devtools/context/localization/lexical.py | 281 | 281 | 0x1.5d5f2fe5dbbffp+0 | 0x1.5d5f2fe5dbbffp+0 | 0 |
| src/devtools/context/localization/assessment.py | 282 | 282 | 0x1.5c7570eef9569p+0 | 0x1.5c7570eef9567p+0 | 0 |
| src/devtools/context/retrieval/repository_map/view.py | 283 | 283 | 0x1.575f9f33304d3p+0 | 0x1.575f9f33304d3p+0 | 0 |
| src/devtools/context/python/modules/declarations.py | 284 | 284 | 0x1.37102005750dfp+0 | 0x1.37102005750dep+0 | 0 |
| src/devtools/context/python/classes/declarations.py | 285 | 285 | 0x1.36e4945c4bd1bp+0 | 0x1.36e4945c4bd1ap+0 | 0 |
| docs/backlog/overview.md | 286 | 286 | 0x1.2fcab6d376cd2p+0 | 0x1.2fcab6d376cd3p+0 | 0 |
| src/devtools/persistence/json.py | 287 | 287 | 0x1.1d1eec553267dp+0 | 0x1.1d1eec553267dp+0 | 0 |
| src/devtools/context/python/classes/bases.py | 288 | 288 | 0x1.842d1cd774e92p-1 | 0x1.842d1cd774e91p-1 | 0 |
| tests/execution/test_runtime.py | 289 | 289 | 0x1.72e62fef07453p-1 | 0x1.72e62fef07453p-1 | 0 |
| src/devtools/context/localization/association/hypothesis.py | 290 | 290 | 0x1.72366d4fa0e07p-1 | 0x1.72366d4fa0e07p-1 | 0 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| reading | 10 | 1 | 10 | 0x1.f2868fe376a59p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.f2868fe376a59p+1 |
| py | 86 | 0 | 86 | 0x1.c934d423c47f9p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.c934d423c47f9p+0 |
| read | 75 | 0 | 75 | 0x1.ec067ec6e30c8p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.ec067ec6e30c8p+0 |
| read_bytes | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| resolvedpath | 93 | 0 | 93 | 0x1.b5490325ac488p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.b5490325ac488p+0 |
| file_format | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| max_bytes | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| default_max_read_bytes | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| finite | 14 | 0 | 14 | 0x1.c935ec6d91aebp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.c935ec6d91aebp+1 |
| unbounded | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| negative | 33 | 0 | 33 | 0x1.5e061b056f6afp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.5e061b056f6afp+1 |
| zero | 47 | 0 | 47 | 0x1.3154090ab9f44p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.3154090ab9f44p+1 |
| exact | 133 | 0 | 133 | 0x1.5a1d04be70330p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.5a1d04be70330p+0 |
| byte | 24 | 0 | 24 | 0x1.86124e474beb2p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.86124e474beb2p+1 |
| boundary | 61 | 1 | 61 | 0x1.1043d0fc1eb37p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.1043d0fc1eb37p+1 |
| growing | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| file | 73 | 1 | 73 | 0x1.f2e5f4e3c7a5ap+0 | 0x1.75cd12aa84bc2p+2 | 0x1.f2e5f4e3c7a5ap+0 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.b42ae8e1e23ebp+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a7c6d39d09080p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.d59b1b617bdb6p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.d59b1b617bdb5p+4"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.d92c6cbc9d9cdp+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.d92c6cbc9d9ccp+3"
        },
        "address": "src/devtools/resources/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "document_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.b42ae8e1e23ebp+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a7c6d39d09080p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.d59b1b617bdb6p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.d59b1b617bdb5p+4"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.d92c6cbc9d9cdp+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.d92c6cbc9d9ccp+3"
        },
        "address": "src/devtools/resources/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "document_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.c79f3e5be8bc8p+3"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.c79f3e5be8bc8p+3"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.c66a6818384b8p+3"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.c66a6818384b8p+3"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.b899e1e539978p+3"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.b899e1e539978p+3"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.b5e56a2aa7cfcp+3"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.b5e56a2aa7cfcp+3"
        },
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.b3bbb5e0d9688p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.b3bbb5e0d9689p+3"
        },
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.ab2bb6f97980ep+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.ab2bb6f97980ep+3"
        },
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.aa461c08e88c2p+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.aa461c08e88c0p+3"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.a8724bf8c4f4fp+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.a8724bf8c4f4ep+3"
        },
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.a5b8a799ffa9ap+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.a5b8a799ffa9bp+3"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.9dd392e9a43e4p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.9dd392e9a43e5p+3"
        },
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
      "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
      "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.b42ae8e1e23ebp+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a7c6d39d09080p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.95c573ece577fp+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.537c174edbc44p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.d59b1b617bdb6p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.d59b1b617bdb5p+4"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.4b90935687c3cp+4"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.31d9d5c7deb46p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.2893fc155fd80p+4"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.2503f99b862f6p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.d95b91ccde2b0p+3"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.d92c6cbc9d9cdp+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.d92c6cbc9d9ccp+3"
        },
        "address": "src/devtools/resources/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "document_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.c79f3e5be8bc8p+3"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.c79f3e5be8bc8p+3"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.c66a6818384b8p+3"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.c66a6818384b8p+3"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.b899e1e539978p+3"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.b899e1e539978p+3"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.b5e56a2aa7cfcp+3"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.b5e56a2aa7cfcp+3"
        },
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.b3bbb5e0d9688p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.b3bbb5e0d9689p+3"
        },
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.ab2bb6f97980ep+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.ab2bb6f97980ep+3"
        },
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.aa461c08e88c2p+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.aa461c08e88c0p+3"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.a8724bf8c4f4fp+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.a8724bf8c4f4ep+3"
        },
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.a5b8a799ffa9ap+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.a5b8a799ffa9bp+3"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.9dd392e9a43e4p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.9dd392e9a43e5p+3"
        },
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.959244d77c9bep+3"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.959244d77c9bfp+3"
        },
        "address": "src/devtools/context/python/function/docs/overview.md",
        "content_identity": "6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d",
        "document_identity": "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.92647a792f8fdp+3"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.92647a792f8fcp+3"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.8bbc665b0e4f8p+3"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.8bbc665b0e4f8p+3"
        },
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.80dd60ec74849p+3"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.80dd60ec74848p+3"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.7aac609247453p+3"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.7aac609247453p+3"
        },
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.751b67f400762p+3"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.751b67f400762p+3"
        },
        "address": "tests/context/python/function/test_disclosure.py",
        "content_identity": "800ae8fb61b7af70b2c3dd0e48eb9147e0a3e93beef98a9e1d269b212e469151",
        "document_identity": "9258890145639d5d6c171f6571178340198186d7bd4069cd27dbd732aef127b2",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.70e8ac576ddc4p+3"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.70e8ac576ddc4p+3"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.6a39abb0010b6p+3"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.6a39abb0010b6p+3"
        },
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.6933b400ab28ap+3"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.6933b400ab289p+3"
        },
        "address": "src/devtools/context/repository/discovery.py",
        "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
        "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.60df63c6f5da0p+3"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.60df63c6f5da0p+3"
        },
        "address": "tests/context/python/function/test_candidates.py",
        "content_identity": "71203dab41b8c017cd280d1bfd1097ca3abe63f7be2215c8e8749bf5a5225f0d",
        "document_identity": "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.5bd8e046a6a10p+3"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.5bd8e046a6a10p+3"
        },
        "address": "tests/context/python/function/test_cross_resource_pipeline.py",
        "content_identity": "3e1385c11ca543d63d7871103573a38d54df4bce21a197c9d4acb429407e9f86",
        "document_identity": "9aad8ade9c30a6bd48667c55317b1143acf7d6d172bf530207e49e8ff9000422",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.564a87e95d899p+3"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.564a87e95d898p+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
        "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.51992d1bfa95ep+3"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.51992d1bfa95ep+3"
        },
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.50209df044ebep+3"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.50209df044ebdp+3"
        },
        "address": "src/devtools/models/benchmarks/storage.py",
        "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
        "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.4c86ecf8bcfd0p+3"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.4c86ecf8bcfd0p+3"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.4c0e7840870a0p+3"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.4c0e7840870a1p+3"
        },
        "address": "src/devtools/core/paths/docs/overview.md",
        "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
        "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.4af5c55bb5861p+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.4af5c55bb5861p+3"
        },
        "address": "tests/context/python/function/test_declarations.py",
        "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
        "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.413dea27b5b56p+3"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.413dea27b5b56p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.3aad2074ea070p+3"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.3aad2074ea070p+3"
        },
        "address": "src/devtools/models/benchmarks/models.py",
        "content_identity": "856e9cb0a4355718d4bd7599c1a9ba038f44eacdcfeceda48958facb56b670f5",
        "document_identity": "5dc6c417b7eeeb78afe9888232f2cac5198575bded9ab6d985b24af847c65ed3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.3275f26e0748ap+3"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.3275f26e0748bp+3"
        },
        "address": "tests/tools/test_execution.py",
        "content_identity": "ca795dd35424539b29e091e66f20e67a66c99f9b2902729a49d1f8264555c5c2",
        "document_identity": "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.312c5da40bf2fp+3"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.312c5da40bf2fp+3"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.2f029b26b141ep+3"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.2f029b26b141ep+3"
        },
        "address": "tests/agents/integrations/codex/test_live.py",
        "content_identity": "b705ab7d34b2b7327ec5e86563123101bb9f293b15260a627905fd8524549e64",
        "document_identity": "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.27751e3c32b2cp+3"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.27751e3c32b2cp+3"
        },
        "address": "tests/scripts/qwen/test_two_action_read_only_acceptance.py",
        "content_identity": "10fc867f673b0db841d41f18acb33e810fb6c53eb6347d2a428714d9c545ef3d",
        "document_identity": "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.26bc6683ca73bp+3"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.26bc6683ca73bp+3"
        },
        "address": "src/devtools/agents/integrations/codex/docs/cli.md",
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "document_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.2331945272b09p+3"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.2331945272b08p+3"
        },
        "address": "tests/context/python/function/test_retrieval.py",
        "content_identity": "9f34ccca57fce7274073fe508ea8ce5d98ac799e316097a9cb6501fae8802b35",
        "document_identity": "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.22037443cf050p+3"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.22037443cf050p+3"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.20b43db765db4p+3"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.20b43db765db4p+3"
        },
        "address": "tests/context/python/function/test_qualified_reference.py",
        "content_identity": "d8ede2921942e6f4acabc9e4176190781eae10fba4c7e0d894aedbb831b2dafb",
        "document_identity": "9c7dfe605bbc376cbb99024b56ae468cdaefab9766bcbe2612175b46106e3c2d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.202392ef05dedp+3"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.202392ef05dedp+3"
        },
        "address": "tests/models/interaction/test_tools.py",
        "content_identity": "6e3ab9f9b1779c387b72e6230b41ee76fed695f40eb55610240c9eecea85f596",
        "document_identity": "7e8ca45cec1b4dfaa4fb2e2488824467b0bceba8c0abafaa885da0137c0d84d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.1f532b9d7c55dp+3"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.1f532b9d7c55dp+3"
        },
        "address": "src/devtools/context/retrieval/lexical/bm25.py",
        "content_identity": "65a1127673d01d713e165266ef211d0f714d5388f0fe243b29f2c1f8aadcf96b",
        "document_identity": "926ee8f3bd2ead1759e4235417e249571bd4503746f467395750ffdd859d449d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.1c79685685fe4p+3"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.1c79685685fe4p+3"
        },
        "address": "tests/context/retrieval/lexical/test_bm25.py",
        "content_identity": "3aa8e9bee063327e0f87500fc824ba13515e41a8b47117849ff55abd4282f97f",
        "document_identity": "b3a957401ac34b38a5d3816ec770fe8213ec011383535e7795f583f42d48ae08",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
      "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
      "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
      "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
      "9258890145639d5d6c171f6571178340198186d7bd4069cd27dbd732aef127b2",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
      "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
      "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
      "9aad8ade9c30a6bd48667c55317b1143acf7d6d172bf530207e49e8ff9000422",
      "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
      "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "5dc6c417b7eeeb78afe9888232f2cac5198575bded9ab6d985b24af847c65ed3",
      "458b276457730495897549ac3b572f140691cfea5945d423dc232e0f4c7fa3a3",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
      "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
      "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
      "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "9c7dfe605bbc376cbb99024b56ae468cdaefab9766bcbe2612175b46106e3c2d",
      "7e8ca45cec1b4dfaa4fb2e2488824467b0bceba8c0abafaa885da0137c0d84d3",
      "926ee8f3bd2ead1759e4235417e249571bd4503746f467395750ffdd859d449d",
      "b3a957401ac34b38a5d3816ec770fe8213ec011383535e7795f583f42d48ae08"
    ]
  }
}
```


## Q2: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/docs/roadmap.md | 1 | 1 | 0x1.a3414ae801e7dp+4 | 0x1.a3414ae801e7dp+4 | 0 |
| src/devtools/resources/filesystem/docs/io.md | 2 | 2 | 0x1.85cf9d036b049p+4 | 0x1.85cf9d036b049p+4 | 0 |
| src/devtools/resources/filesystem/docs/overview.md | 3 | 3 | 0x1.706f8803b69dap+4 | 0x1.706f8803b69dap+4 | 0 |
| src/devtools/resources/filesystem/reading.py | 4 | 4 | 0x1.40de9a7044ca4p+4 | 0x1.40de9a7044ca4p+4 | 0 |
| tests/models/interaction/providers/test_llama_cpp.py | 5 | 5 | 0x1.2750dc3157994p+4 | 0x1.2750dc3157994p+4 | 0 |
| src/devtools/models/benchmarks/runner.py | 6 | 6 | 0x1.26394f1368b9bp+4 | 0x1.26394f1368b9bp+4 | 0 |
| tests/models/benchmarks/test_runner.py | 7 | 7 | 0x1.25cf5f7c72348p+4 | 0x1.25cf5f7c72349p+4 | 0 |
| src/devtools/resources/commands/execution.py | 8 | 8 | 0x1.1bd2f90895fb0p+4 | 0x1.1bd2f90895fb0p+4 | 0 |
| tests/resources/filesystem/test_reading.py | 9 | 9 | 0x1.159ff27307869p+4 | 0x1.159ff27307869p+4 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 10 | 11 | 0x1.01cace3a4b345p+4 | 0x1.f2b5c520c7213p+3 | -1 |
| src/devtools/models/interaction/providers/llama_cpp.py | 11 | 10 | 0x1.fcf7ac341c48ap+3 | 0x1.fcf7ac341c48bp+3 | 1 |
| tests/resources/commands/test_execution.py | 12 | 12 | 0x1.d16d4617e67bcp+3 | 0x1.d16d4617e67bbp+3 | 0 |
| tests/context/repository/test_observation.py | 13 | 13 | 0x1.b1a1312c4dcb2p+3 | 0x1.b1a1312c4dcb1p+3 | 0 |
| src/devtools/resources/filesystem/errors.py | 14 | 14 | 0x1.afcfde9f2bdd2p+3 | 0x1.afcfde9f2bdd2p+3 | 0 |
| AGENTS.md | 15 | 15 | 0x1.acd6492cf7e41p+3 | 0x1.acd6492cf7e41p+3 | 0 |
| src/devtools/resources/commands/docs/events.md | 16 | 16 | 0x1.9f490f09500ffp+3 | 0x1.9f490f09500ffp+3 | 0 |
| src/devtools/resources/filesystem/models/binary.py | 17 | 17 | 0x1.9dfe83f4619fap+3 | 0x1.9dfe83f4619fap+3 | 0 |
| src/devtools/models/serving/docs/overview.md | 18 | 18 | 0x1.85ffd5d8b8326p+3 | 0x1.85ffd5d8b8325p+3 | 0 |
| src/devtools/agents/conversation/docs/conversation.md | 19 | 19 | 0x1.7dbf174480970p+3 | 0x1.7dbf17448096fp+3 | 0 |
| src/devtools/models/benchmarks/docs/overview.md | 20 | 20 | 0x1.7134525419db0p+3 | 0x1.7134525419db0p+3 | 0 |
| src/devtools/resources/filesystem/__init__.py | 21 | 21 | 0x1.6b01a46fba981p+3 | 0x1.6b01a46fba981p+3 | 0 |
| src/devtools/context/repository/observation.py | 22 | 22 | 0x1.669bdafcca938p+3 | 0x1.669bdafcca938p+3 | 0 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 23 | 23 | 0x1.621a54d7f5fa7p+3 | 0x1.621a54d7f5fa8p+3 | 0 |
| src/devtools/tools/docs/overview.md | 24 | 24 | 0x1.507962ea9ee84p+3 | 0x1.507962ea9ee84p+3 | 0 |
| tests/resources/commands/test_handle.py | 25 | 25 | 0x1.4ceddea4dcc38p+3 | 0x1.4ceddea4dcc38p+3 | 0 |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 26 | 26 | 0x1.4a040015902fep+3 | 0x1.4a040015902fdp+3 | 0 |
| src/devtools/observability/evidence/docs/overview.md | 27 | 27 | 0x1.3e0474cd8f5b2p+3 | 0x1.3e0474cd8f5b3p+3 | 0 |
| src/devtools/persistence/docs/overview.md | 28 | 28 | 0x1.36ed357216162p+3 | 0x1.36ed357216163p+3 | 0 |
| src/devtools/context/python/classes/docs/overview.md | 29 | 29 | 0x1.31a0566b17761p+3 | 0x1.31a0566b17762p+3 | 0 |
| src/devtools/resources/commands/models/output.py | 30 | 30 | 0x1.30812520072f0p+3 | 0x1.30812520072eep+3 | 0 |
| src/devtools/persistence/docs/sqlite.md | 31 | 31 | 0x1.284ef26dd1387p+3 | 0x1.284ef26dd1386p+3 | 0 |
| tests/context/retrieval/graph/test_ranking.py | 32 | 32 | 0x1.2126455eda4fap+3 | 0x1.2126455eda4fap+3 | 0 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 33 | 33 | 0x1.1b8ef64315735p+3 | 0x1.1b8ef64315736p+3 | 0 |
| src/devtools/context/python/classes/containment.py | 34 | 54 | 0x1.1ab56afa12e41p+3 | 0x1.e04a34f8bd96cp+2 | -20 |
| src/devtools/context/python/function/rendering.py | 35 | 34 | 0x1.18a38e62e5584p+3 | 0x1.18a38e62e5583p+3 | 1 |
| src/devtools/context/python/function/containment.py | 36 | 55 | 0x1.16c68afc4a1ddp+3 | 0x1.d9dfca07b4b9ap+2 | -19 |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 37 | 35 | 0x1.0aea289688cfbp+3 | 0x1.0aea289688cfcp+3 | 2 |
| tests/tools/test_command.py | 38 | 36 | 0x1.081915bece6a2p+3 | 0x1.081915bece6a3p+3 | 2 |
| src/devtools/resources/filesystem/codecs/text.py | 39 | 37 | 0x1.02f99775feb94p+3 | 0x1.02f99775feb94p+3 | 2 |
| src/devtools/resources/filesystem/codecs/markdown.py | 40 | 38 | 0x1.008e2a248c50fp+3 | 0x1.008e2a248c50ep+3 | 2 |
| tests/tools/test_runtime_integration.py | 41 | 39 | 0x1.fbbab7a47b51cp+2 | 0x1.fbbab7a47b51bp+2 | 2 |
| src/devtools/models/serving/vllm.py | 42 | 40 | 0x1.faeac0a14b646p+2 | 0x1.faeac0a14b646p+2 | 2 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 43 | 41 | 0x1.f8a80dc45cfafp+2 | 0x1.f8a80dc45cfb0p+2 | 2 |
| tests/context/localization/routing/test_routing.py | 44 | 42 | 0x1.efb6843816ed6p+2 | 0x1.efb6843816ed6p+2 | 2 |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 45 | 43 | 0x1.edf9795f88b57p+2 | 0x1.edf9795f88b57p+2 | 2 |
| tests/scripts/test_retrieval_bm25_baseline.py | 46 | 44 | 0x1.ebf8a840f66fcp+2 | 0x1.ebf8a840f66fcp+2 | 2 |
| src/devtools/resources/commands/handle.py | 47 | 45 | 0x1.ebcedc6890810p+2 | 0x1.ebcedc6890810p+2 | 2 |
| tests/scripts/qwen/test_two_read_acceptance.py | 48 | 46 | 0x1.eba96d6b7a9eep+2 | 0x1.eba96d6b7a9eep+2 | 2 |
| src/devtools/context/retrieval/repository_map/view.py | 49 | 47 | 0x1.eaf1a360b5c78p+2 | 0x1.eaf1a360b5c7ap+2 | 2 |
| tests/context/localization/association/test_hypothesis.py | 50 | 48 | 0x1.e923182f7e138p+2 | 0x1.e923182f7e138p+2 | 2 |
| src/devtools/context/retrieval/repository_map/importance.py | 51 | 49 | 0x1.e6b9d82a25c0cp+2 | 0x1.e6b9d82a25c0bp+2 | 2 |
| src/devtools/context/planning/resource.py | 52 | 50 | 0x1.e46aad477c4f3p+2 | 0x1.e46aad477c4f2p+2 | 2 |
| src/devtools/resources/filesystem/writing.py | 53 | 51 | 0x1.e33cbcca29182p+2 | 0x1.e33cbcca29182p+2 | 2 |
| tests/context/repository/test_discovery.py | 54 | 52 | 0x1.e29362e533afap+2 | 0x1.e29362e533afap+2 | 2 |
| tests/context/python/function/test_candidates.py | 55 | 53 | 0x1.e1c3b32114cc5p+2 | 0x1.e1c3b32114cc6p+2 | 2 |
| src/devtools/context/localization/routing/derive.py | 56 | 56 | 0x1.d7ca2979d004ap+2 | 0x1.d7ca2979d004cp+2 | 0 |
| src/devtools/tools/filesystem.py | 57 | 98 | 0x1.d6d7bd8add081p+2 | 0x1.6cacbbb151a4cp+2 | -41 |
| src/devtools/context/localization/generation/generate.py | 58 | 57 | 0x1.d4a1ae6c63b81p+2 | 0x1.d4a1ae6c63b80p+2 | 1 |
| docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md | 59 | 58 | 0x1.d2988a9b8a99fp+2 | 0x1.d2988a9b8a99fp+2 | 1 |
| src/devtools/context/localization/association/hypothesis.py | 60 | 59 | 0x1.cd52cd83024a2p+2 | 0x1.cd52cd83024a2p+2 | 1 |
| src/devtools/resources/filesystem/codecs/json.py | 61 | 60 | 0x1.cc94967d2a9e7p+2 | 0x1.cc94967d2a9e6p+2 | 1 |
| src/devtools/context/retrieval/docs/overview.md | 62 | 61 | 0x1.ca948560ca198p+2 | 0x1.ca948560ca199p+2 | 1 |
| src/devtools/context/python/classes/__init__.py | 63 | 62 | 0x1.b947ee8eb7e65p+2 | 0x1.b947ee8eb7e65p+2 | 1 |
| tests/resources/filesystem/codecs/test_json.py | 64 | 63 | 0x1.b8db5a35d31ebp+2 | 0x1.b8db5a35d31ecp+2 | 1 |
| src/devtools/context/planning/docs/overview.md | 65 | 64 | 0x1.b718ea7db1d30p+2 | 0x1.b718ea7db1d2fp+2 | 1 |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 66 | 65 | 0x1.b69c89f2e89d4p+2 | 0x1.b69c89f2e89d5p+2 | 1 |
| src/devtools/core/paths/docs/overview.md | 67 | 66 | 0x1.b63647dcd99a2p+2 | 0x1.b63647dcd99a1p+2 | 1 |
| src/devtools/context/retrieval/graph/view.py | 68 | 67 | 0x1.b1e719435813ap+2 | 0x1.b1e7194358139p+2 | 1 |
| src/devtools/context/localization/association/imports.py | 69 | 68 | 0x1.ad97c15aac9e8p+2 | 0x1.ad97c15aac9e8p+2 | 1 |
| src/devtools/context/python/function/docs/overview.md | 70 | 69 | 0x1.a7d77f0700b7fp+2 | 0x1.a7d77f0700b80p+2 | 1 |
| src/devtools/resources/filesystem/docs/codecs.md | 71 | 70 | 0x1.a21dd9694e831p+2 | 0x1.a21dd9694e831p+2 | 1 |
| src/devtools/resources/filesystem/codecs/csv.py | 72 | 71 | 0x1.9b8932efc5026p+2 | 0x1.9b8932efc5026p+2 | 1 |
| src/devtools/context/repository/discovery.py | 73 | 72 | 0x1.9b47ed588f5c9p+2 | 0x1.9b47ed588f5c9p+2 | 1 |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 74 | 73 | 0x1.9b22164bc68d2p+2 | 0x1.9b22164bc68d2p+2 | 1 |
| docs/backlog/epics/B-0005-effect-governance.md | 75 | 74 | 0x1.9a2cd6e6194a4p+2 | 0x1.9a2cd6e6194a3p+2 | 1 |
| src/devtools/resources/filesystem/models/text.py | 76 | 75 | 0x1.999c3a8491a3bp+2 | 0x1.999c3a8491a3ap+2 | 1 |
| src/devtools/resources/commands/models/result.py | 77 | 76 | 0x1.9633c0e2af499p+2 | 0x1.9633c0e2af499p+2 | 1 |
| tests/context/retrieval/graph/test_typed.py | 78 | 77 | 0x1.93ff18ca16fbap+2 | 0x1.93ff18ca16fbap+2 | 1 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 79 | 78 | 0x1.8da60171613f6p+2 | 0x1.8da60171613f7p+2 | 1 |
| src/devtools/context/python/function/materialization.py | 80 | 79 | 0x1.8d4251f586c18p+2 | 0x1.8d4251f586c18p+2 | 1 |
| tests/models/serving/test_vllm.py | 81 | 80 | 0x1.8c3e7a2228fc3p+2 | 0x1.8c3e7a2228fc2p+2 | 1 |
| tests/context/python/function/test_disclosure.py | 82 | 81 | 0x1.887c52068504ap+2 | 0x1.887c52068504ap+2 | 1 |
| src/devtools/resources/commands/docs/execution.md | 83 | 82 | 0x1.88446cd4b86dcp+2 | 0x1.88446cd4b86dcp+2 | 1 |
| src/devtools/context/localization/grounding/contract.py | 84 | 83 | 0x1.86a3d7d42fc7cp+2 | 0x1.86a3d7d42fc7dp+2 | 1 |
| src/devtools/context/python/function/__init__.py | 85 | 84 | 0x1.8582acfa76067p+2 | 0x1.8582acfa76066p+2 | 1 |
| docs/backlog/items/B-0013-investigate-authority-grants-approval.md | 86 | 85 | 0x1.849a081cf4e16p+2 | 0x1.849a081cf4e18p+2 | 1 |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 87 | 86 | 0x1.83c2bd892a5c6p+2 | 0x1.83c2bd892a5c7p+2 | 1 |
| tests/tools/test_filesystem.py | 88 | 87 | 0x1.832948dcce0ecp+2 | 0x1.832948dcce0ecp+2 | 1 |
| tests/context/python/function/test_materialization.py | 89 | 88 | 0x1.7fe99f7072a82p+2 | 0x1.7fe99f7072a81p+2 | 1 |
| tests/context/python/function/test_resource_selection.py | 90 | 89 | 0x1.7f280a0febcfbp+2 | 0x1.7f280a0febcfbp+2 | 1 |
| src/devtools/resources/commands/docs/command.md | 91 | 90 | 0x1.7e27e3aa32604p+2 | 0x1.7e27e3aa32604p+2 | 1 |
| src/devtools/context/python/project_configuration/resolution.py | 92 | 91 | 0x1.7cc29132830c9p+2 | 0x1.7cc29132830c9p+2 | 1 |
| tests/models/serving/test_llama_cpp.py | 93 | 92 | 0x1.7bf0013a42451p+2 | 0x1.7bf0013a42451p+2 | 1 |
| src/devtools/resources/filesystem/docs/json.md | 94 | 93 | 0x1.7bae4d303a7f6p+2 | 0x1.7bae4d303a7f7p+2 | 1 |
| tests/context/python/function/test_declaration_aggregation.py | 95 | 94 | 0x1.7a240e3190b02p+2 | 0x1.7a240e3190b01p+2 | 1 |
| src/devtools/context/repository/snapshot.py | 96 | 134 | 0x1.79e8efc8db8bcp+2 | 0x1.0e7fb0032ddedp+2 | -38 |
| tests/resources/filesystem/codecs/test_markdown.py | 97 | 95 | 0x1.799af78134790p+2 | 0x1.799af78134790p+2 | 2 |
| src/devtools/observability/evidence/model_interaction.py | 98 | 96 | 0x1.797f246d25c8fp+2 | 0x1.797f246d25c90p+2 | 2 |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 99 | 97 | 0x1.786897e767b9bp+2 | 0x1.786897e767b99p+2 | 2 |
| tests/context/localization/resolution/test_resolution.py | 100 | 99 | 0x1.6c116ba6cf176p+2 | 0x1.6c116ba6cf176p+2 | 1 |
| src/devtools/context/python/classes/bases.py | 101 | 100 | 0x1.69115b5c6bc16p+2 | 0x1.69115b5c6bc16p+2 | 1 |
| tests/context/python/function/test_rendering.py | 102 | 101 | 0x1.65ebd1019884cp+2 | 0x1.65ebd1019884bp+2 | 1 |
| tests/scripts/test_vllm_benchmark_driver.py | 103 | 102 | 0x1.62560ca3a6ef3p+2 | 0x1.62560ca3a6ef3p+2 | 1 |
| tests/context/retrieval/repository_map/test_ranking.py | 104 | 103 | 0x1.5f81ab23ed14cp+2 | 0x1.5f81ab23ed14cp+2 | 1 |
| tests/context/localization/generation/test_generation.py | 105 | 104 | 0x1.5e127773df418p+2 | 0x1.5e127773df418p+2 | 1 |
| src/devtools/context/python/modules/interpretation.py | 106 | 105 | 0x1.5d5714dbd7d08p+2 | 0x1.5d5714dbd7d07p+2 | 1 |
| tests/models/serving/test_huggingface.py | 107 | 106 | 0x1.58594bc58029ep+2 | 0x1.58594bc58029ep+2 | 1 |
| src/devtools/resources/filesystem/docs/models.md | 108 | 107 | 0x1.543ebb4795194p+2 | 0x1.543ebb4795194p+2 | 1 |
| src/devtools/context/python/modules/docs/overview.md | 109 | 108 | 0x1.5409c301e8edap+2 | 0x1.5409c301e8edbp+2 | 1 |
| tests/models/benchmarks/test_storage.py | 110 | 109 | 0x1.5381b3f74c59cp+2 | 0x1.5381b3f74c59ap+2 | 1 |
| src/devtools/models/interaction/docs/overview.md | 111 | 110 | 0x1.51f36f03b90a4p+2 | 0x1.51f36f03b90a2p+2 | 1 |
| src/devtools/context/localization/routing/docs/overview.md | 112 | 111 | 0x1.51669148a2226p+2 | 0x1.51669148a2227p+2 | 1 |
| tests/context/python/function/test_retrieval.py | 113 | 112 | 0x1.5132b28fa6bb1p+2 | 0x1.5132b28fa6bb1p+2 | 1 |
| tests/context/localization/generation/test_branching.py | 114 | 113 | 0x1.462375a215276p+2 | 0x1.462375a215277p+2 | 1 |
| src/devtools/context/python/function/qualified_reference.py | 115 | 114 | 0x1.4208f31d09c42p+2 | 0x1.4208f31d09c42p+2 | 1 |
| src/devtools/resources/commands/events.py | 116 | 115 | 0x1.3ed997e16e2cbp+2 | 0x1.3ed997e16e2ccp+2 | 1 |
| src/devtools/context/python/modules/membership.py | 117 | 116 | 0x1.3cba7b36d2f76p+2 | 0x1.3cba7b36d2f77p+2 | 1 |
| src/devtools/context/localization/roles/derivation.py | 118 | 117 | 0x1.3b37b9e061feap+2 | 0x1.3b37b9e061feap+2 | 1 |
| tests/context/python/test_source_candidacy.py | 119 | 118 | 0x1.37dbb63daa264p+2 | 0x1.37dbb63daa264p+2 | 1 |
| src/devtools/context/localization/lexical.py | 120 | 119 | 0x1.3672e47f33c7ap+2 | 0x1.3672e47f33c7ap+2 | 1 |
| tests/context/python/function/test_cross_resource_pipeline.py | 121 | 120 | 0x1.3158ade497904p+2 | 0x1.3158ade497903p+2 | 1 |
| tests/context/localization/generation/test_imports.py | 122 | 121 | 0x1.2ddbe92552032p+2 | 0x1.2ddbe92552032p+2 | 1 |
| src/devtools/context/localization/task.py | 123 | 122 | 0x1.2d97a82deae27p+2 | 0x1.2d97a82deae26p+2 | 1 |
| docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md | 124 | 123 | 0x1.2d066dac78ae0p+2 | 0x1.2d066dac78ae0p+2 | 1 |
| src/devtools/context/localization/resolution/view.py | 125 | 124 | 0x1.2c13830d15e50p+2 | 0x1.2c13830d15e50p+2 | 1 |
| docs/backlog/items/B-0039-investigate-delegated-authority.md | 126 | 125 | 0x1.298a2388a8d91p+2 | 0x1.298a2388a8d91p+2 | 1 |
| docs/backlog/items/B-0024-investigate-audit-durable-accountability.md | 127 | 126 | 0x1.2861b82dcb4c4p+2 | 0x1.2861b82dcb4c4p+2 | 1 |
| docs/backlog/items/B-0012-investigate-governed-effect-semantics.md | 128 | 127 | 0x1.273b992420d39p+2 | 0x1.273b992420d39p+2 | 1 |
| src/devtools/context/localization/grounding/view.py | 129 | 128 | 0x1.2371a41542870p+2 | 0x1.2371a4154286ep+2 | 1 |
| src/devtools/context/python/project_configuration/declarations.py | 130 | 129 | 0x1.1e6161ca18078p+2 | 0x1.1e6161ca18077p+2 | 1 |
| docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md | 131 | 130 | 0x1.1dc2f435f9881p+2 | 0x1.1dc2f435f9881p+2 | 1 |
| src/devtools/evaluation/docs/overview.md | 132 | 131 | 0x1.1b62b4f91676bp+2 | 0x1.1b62b4f91676bp+2 | 1 |
| src/devtools/context/python/function/declarations.py | 133 | 132 | 0x1.15731cb1fcda0p+2 | 0x1.15731cb1fcda0p+2 | 1 |
| tests/context/localization/test_lexical.py | 134 | 133 | 0x1.0ffc9351e85fdp+2 | 0x1.0ffc9351e85fdp+2 | 1 |
| src/devtools/context/python/function/candidates.py | 135 | 135 | 0x1.0e413a35ac89bp+2 | 0x1.0e413a35ac89ap+2 | 0 |
| tests/context/python/function/test_declarations.py | 136 | 136 | 0x1.0af313dad296ap+2 | 0x1.0af313dad2969p+2 | 0 |
| src/devtools/context/python/modules/declarations.py | 137 | 137 | 0x1.0880526be073fp+2 | 0x1.0880526be073fp+2 | 0 |
| src/devtools/context/python/imports/members.py | 138 | 138 | 0x1.049d1f13964b4p+2 | 0x1.049d1f13964b3p+2 | 0 |
| tests/context/retrieval/lexical/test_evaluation.py | 139 | 139 | 0x1.023fb6cbb8376p+2 | 0x1.023fb6cbb8375p+2 | 0 |
| tests/context/repository/test_corpus.py | 140 | 140 | 0x1.fb0f7a31311aap+1 | 0x1.fb0f7a31311aap+1 | 0 |
| src/devtools/context/python/imports/declarations.py | 141 | 141 | 0x1.f8abdf7a27f1cp+1 | 0x1.f8abdf7a27f1ep+1 | 0 |
| src/devtools/context/python/classes/declarations.py | 142 | 142 | 0x1.f37217d72e59bp+1 | 0x1.f37217d72e59cp+1 | 0 |
| src/devtools/context/python/docs/overview.md | 143 | 143 | 0x1.e5185d760ac66p+1 | 0x1.e5185d760ac66p+1 | 0 |
| tests/context/python/function/test_request_assembly.py | 144 | 144 | 0x1.e4f920ac59594p+1 | 0x1.e4f920ac59595p+1 | 0 |
| src/devtools/context/localization/routing/models.py | 145 | 145 | 0x1.e2ef90d567dadp+1 | 0x1.e2ef90d567dabp+1 | 0 |
| src/devtools/context/python/mirrored_paths.py | 146 | 146 | 0x1.dfe71e383e672p+1 | 0x1.dfe71e383e671p+1 | 0 |
| tests/context/python/references/declarations/test_bindings.py | 147 | 147 | 0x1.da19672ea46a7p+1 | 0x1.da19672ea46a7p+1 | 0 |
| src/devtools/resources/filesystem/models/__init__.py | 148 | 148 | 0x1.d7ae3f0ee9319p+1 | 0x1.d7ae3f0ee931ap+1 | 0 |
| src/devtools/resources/filesystem/models/json/__init__.py | 149 | 149 | 0x1.d607c8f1d1a8ep+1 | 0x1.d607c8f1d1a8ep+1 | 0 |
| src/devtools/core/conversion/docs/overview.md | 150 | 150 | 0x1.d3432645f20eep+1 | 0x1.d3432645f20eep+1 | 0 |
| src/devtools/resources/filesystem/codecs/__init__.py | 151 | 151 | 0x1.d33e37ea7df21p+1 | 0x1.d33e37ea7df21p+1 | 0 |
| tests/context/python/project_configuration/test_configuration.py | 152 | 152 | 0x1.d267936a4e152p+1 | 0x1.d267936a4e153p+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 153 | 153 | 0x1.cc4c9ea327d33p+1 | 0x1.cc4c9ea327d33p+1 | 0 |
| src/devtools/core/paths/models.py | 154 | 154 | 0x1.c4ab0a962e9dep+1 | 0x1.c4ab0a962e9dfp+1 | 0 |
| src/devtools/context/localization/generation/contract.py | 155 | 155 | 0x1.c44010a5983dcp+1 | 0x1.c44010a5983dcp+1 | 0 |
| src/devtools/core/paths/resolution.py | 156 | 156 | 0x1.bc397aa121260p+1 | 0x1.bc397aa121261p+1 | 0 |
| src/devtools/resources/filesystem/resolution.py | 157 | 157 | 0x1.b76bd0e5cad67p+1 | 0x1.b76bd0e5cad68p+1 | 0 |
| src/devtools/resources/filesystem/models/base.py | 158 | 158 | 0x1.b41364c0417b5p+1 | 0x1.b41364c0417b5p+1 | 0 |
| tests/context/python/function/test_qualified_reference.py | 159 | 159 | 0x1.b405561261b83p+1 | 0x1.b405561261b83p+1 | 0 |
| src/devtools/context/python/project_configuration/models.py | 160 | 160 | 0x1.b146308496ceep+1 | 0x1.b146308496ceep+1 | 0 |
| tests/context/python/classes/test_bases.py | 161 | 161 | 0x1.afac77d31f981p+1 | 0x1.afac77d31f980p+1 | 0 |
| src/devtools/context/python/references/declarations/resolution.py | 162 | 162 | 0x1.ab659c5476e57p+1 | 0x1.ab659c5476e58p+1 | 0 |
| src/devtools/context/python/function/retrieval.py | 163 | 163 | 0x1.aa6a5bb6d669bp+1 | 0x1.aa6a5bb6d669ap+1 | 0 |
| tests/context/localization/roles/test_configuration.py | 164 | 164 | 0x1.a983f3adabbd8p+1 | 0x1.a983f3adabbdap+1 | 0 |
| src/devtools/resources/filesystem/models/json/base.py | 165 | 165 | 0x1.a82c62142eea2p+1 | 0x1.a82c62142eea2p+1 | 0 |
| tests/context/python/references/declarations/test_analysis.py | 166 | 166 | 0x1.a51332c965a0bp+1 | 0x1.a51332c965a0bp+1 | 0 |
| tests/resources/filesystem/test_writing.py | 167 | 167 | 0x1.a1c91ed2d5fe5p+1 | 0x1.a1c91ed2d5fe5p+1 | 0 |
| tests/resources/filesystem/test_resolution.py | 168 | 168 | 0x1.9f10d82bbce6fp+1 | 0x1.9f10d82bbce6fp+1 | 0 |
| tests/context/localization/generation/test_references.py | 169 | 169 | 0x1.9eebecb713330p+1 | 0x1.9eebecb713330p+1 | 0 |
| src/devtools/resources/filesystem/models/json/scalar.py | 170 | 170 | 0x1.912382cc20eafp+1 | 0x1.912382cc20eaep+1 | 0 |
| tests/context/python/project_configuration/test_settings.py | 171 | 171 | 0x1.9098a9bce23f9p+1 | 0x1.9098a9bce23fap+1 | 0 |
| docs/backlog/overview.md | 172 | 172 | 0x1.907949feb6d7fp+1 | 0x1.907949feb6d80p+1 | 0 |
| tests/core/paths/test_resolution.py | 173 | 173 | 0x1.861ebeaab803ep+1 | 0x1.861ebeaab803ep+1 | 0 |
| docs/experiments/qwen38_llama_cpp.md | 174 | 174 | 0x1.845bd41c0ed47p+1 | 0x1.845bd41c0ed48p+1 | 0 |
| src/devtools/context/repository/document.py | 175 | 175 | 0x1.7ec0e9a0aab10p+1 | 0x1.7ec0e9a0aab10p+1 | 0 |
| tests/resources/filesystem/__init__.py | 176 | 176 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/codecs/__init__.py | 177 | 177 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/__init__.py | 178 | 178 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/markdown/__init__.py | 179 | 179 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/csv/__init__.py | 180 | 180 | 0x1.7dd5af5050b5bp+1 | 0x1.7dd5af5050b5dp+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 181 | 181 | 0x1.78c480c4f3a2bp+1 | 0x1.78c480c4f3a2dp+1 | 0 |
| tests/scripts/qwen/test_llama_cpp_service.py | 182 | 182 | 0x1.6d7b165538426p+1 | 0x1.6d7b165538424p+1 | 0 |
| tests/resources/filesystem/test_models.py | 183 | 183 | 0x1.6a1a503bc7b61p+1 | 0x1.6a1a503bc7b61p+1 | 0 |
| tests/context/planning/test_plan.py | 184 | 184 | 0x1.6963813e52cfep+1 | 0x1.6963813e52cfep+1 | 0 |
| tests/context/localization/grounding/test_grounding.py | 185 | 185 | 0x1.6850a337c7999p+1 | 0x1.6850a337c7997p+1 | 0 |
| tests/agents/integrations/codex/test_agent.py | 186 | 186 | 0x1.667cf1abccb67p+1 | 0x1.667cf1abccb67p+1 | 0 |
| tests/agents/integrations/codex/test_parsing.py | 187 | 187 | 0x1.64fc3a3b2781cp+1 | 0x1.64fc3a3b2781bp+1 | 0 |
| tests/context/retrieval/test_composition.py | 188 | 188 | 0x1.63d09eb204099p+1 | 0x1.63d09eb204098p+1 | 0 |
| src/devtools/context/localization/identity.py | 189 | 189 | 0x1.62e855bc0647ap+1 | 0x1.62e855bc0647bp+1 | 0 |
| tests/context/retrieval/test_structural.py | 190 | 190 | 0x1.60d6148a41cf0p+1 | 0x1.60d6148a41cf0p+1 | 0 |
| src/devtools/persistence/docs/json.md | 191 | 191 | 0x1.60c5d25373901p+1 | 0x1.60c5d25373901p+1 | 0 |
| tests/context/python/modules/test_membership.py | 192 | 192 | 0x1.60b43ea7e4609p+1 | 0x1.60b43ea7e4609p+1 | 0 |
| tests/context/python/function/test_containment.py | 193 | 193 | 0x1.603d9c15fc621p+1 | 0x1.603d9c15fc622p+1 | 0 |
| src/devtools/resources/filesystem/models/json/object.py | 194 | 194 | 0x1.5fdcb6704b75bp+1 | 0x1.5fdcb6704b75ap+1 | 0 |
| tests/context/python/imports/test_members.py | 195 | 195 | 0x1.5f3d1a3ef0a8ap+1 | 0x1.5f3d1a3ef0a8ap+1 | 0 |
| tests/context/python/imports/test_resolution.py | 196 | 196 | 0x1.5f3116b36c462p+1 | 0x1.5f3116b36c463p+1 | 0 |
| src/devtools/context/localization/roles/inputs.py | 197 | 197 | 0x1.5ecf3366f92c0p+1 | 0x1.5ecf3366f92bfp+1 | 0 |
| src/devtools/context/retrieval/composition.py | 198 | 198 | 0x1.5e6ffddde3481p+1 | 0x1.5e6ffddde3482p+1 | 0 |
| src/devtools/context/python/references/declarations/analysis.py | 199 | 199 | 0x1.5d5bcc9fce963p+1 | 0x1.5d5bcc9fce964p+1 | 0 |
| tests/context/python/classes/test_declarations.py | 200 | 200 | 0x1.5d4175f89a26fp+1 | 0x1.5d4175f89a26fp+1 | 0 |
| src/devtools/context/retrieval/structural.py | 201 | 201 | 0x1.5c0f02430d16dp+1 | 0x1.5c0f02430d16dp+1 | 0 |
| src/devtools/context/localization/grounding/resolve.py | 202 | 202 | 0x1.5a2ecf83dfb2cp+1 | 0x1.5a2ecf83dfb2cp+1 | 0 |
| src/devtools/resources/filesystem/models/json/list.py | 203 | 203 | 0x1.59dfac7d6bdfap+1 | 0x1.59dfac7d6bdfap+1 | 0 |
| tests/context/python/modules/test_selection.py | 204 | 204 | 0x1.594fed316ed34p+1 | 0x1.594fed316ed35p+1 | 0 |
| tests/context/python/test_mirrored_paths.py | 205 | 205 | 0x1.58e9d3af4168dp+1 | 0x1.58e9d3af4168ep+1 | 0 |
| src/devtools/context/localization/association/references.py | 206 | 206 | 0x1.5449d5c6f8e1fp+1 | 0x1.5449d5c6f8e21p+1 | 0 |
| src/devtools/context/repository/corpus.py | 207 | 207 | 0x1.53992fc29e043p+1 | 0x1.53992fc29e044p+1 | 0 |
| src/devtools/context/localization/association/structural.py | 208 | 208 | 0x1.5387c47d0f9c4p+1 | 0x1.5387c47d0f9c4p+1 | 0 |
| tests/context/python/imports/test_relations.py | 209 | 209 | 0x1.4f8b946fa0fa0p+1 | 0x1.4f8b946fa0fa0p+1 | 0 |
| src/devtools/context/python/modules/selection.py | 210 | 210 | 0x1.4f7b8603ad319p+1 | 0x1.4f7b8603ad319p+1 | 0 |
| tests/context/python/modules/test_interpretation.py | 211 | 211 | 0x1.4f38f73dde909p+1 | 0x1.4f38f73dde909p+1 | 0 |
| tests/resources/filesystem/test_json_models.py | 212 | 212 | 0x1.4bf76a7e8601cp+1 | 0x1.4bf76a7e8601cp+1 | 0 |
| src/devtools/core/regex/docs/overview.md | 213 | 213 | 0x1.4a07fe56fba4fp+1 | 0x1.4a07fe56fba4ep+1 | 0 |
| tests/models/benchmarks/test_models.py | 214 | 214 | 0x1.47ba6ea961edep+1 | 0x1.47ba6ea961ee0p+1 | 0 |
| src/devtools/context/retrieval/fusion.py | 215 | 215 | 0x1.473135e7493a9p+1 | 0x1.473135e7493a8p+1 | 0 |
| src/devtools/context/planning/materialization.py | 216 | 216 | 0x1.4463afa94213ap+1 | 0x1.4463afa94213bp+1 | 0 |
| src/devtools/core/paths/docs/resolution.md | 217 | 217 | 0x1.43865f477eb7fp+1 | 0x1.43865f477eb7fp+1 | 0 |
| tests/resources/filesystem/models/markdown/test_heading.py | 218 | 218 | 0x1.4368513d64234p+1 | 0x1.4368513d64234p+1 | 0 |
| src/devtools/context/python/function/planned_reference.py | 219 | 219 | 0x1.427d4a007eb0ap+1 | 0x1.427d4a007eb0cp+1 | 0 |
| src/devtools/persistence/sqlite.py | 220 | 220 | 0x1.422e4e854bb6ep+1 | 0x1.422e4e854bb6fp+1 | 0 |
| tests/resources/filesystem/models/csv/test_dialect.py | 221 | 221 | 0x1.41d4e5792ad2fp+1 | 0x1.41d4e5792ad2ep+1 | 0 |
| docs/backlog/epics/B-0003-local-coding-worker-harness.md | 222 | 222 | 0x1.412d0e5e2b823p+1 | 0x1.412d0e5e2b822p+1 | 0 |
| tests/resources/filesystem/test_json_conversion.py | 223 | 223 | 0x1.412a46534ec47p+1 | 0x1.412a46534ec47p+1 | 0 |
| src/devtools/context/retrieval/graph/pagerank.py | 224 | 224 | 0x1.405bd2bfc8d9bp+1 | 0x1.405bd2bfc8d9ap+1 | 0 |
| src/devtools/resources/filesystem/models/json/conversion.py | 225 | 225 | 0x1.3e576af6c2bffp+1 | 0x1.3e576af6c2bfep+1 | 0 |
| src/devtools/context/planning/plan.py | 226 | 226 | 0x1.3d755e5fb1eabp+1 | 0x1.3d755e5fb1eaap+1 | 0 |
| src/devtools/persistence/_snapshot.py | 227 | 227 | 0x1.3d5f650e67d75p+1 | 0x1.3d5f650e67d75p+1 | 0 |
| tests/context/localization/roles/test_inputs.py | 228 | 228 | 0x1.3c21b2cea07cep+1 | 0x1.3c21b2cea07cep+1 | 0 |
| src/devtools/persistence/json.py | 229 | 229 | 0x1.3a1b0218b9dcdp+1 | 0x1.3a1b0218b9dcep+1 | 0 |
| src/devtools/models/serving/huggingface.py | 230 | 230 | 0x1.3768ad48a3717p+1 | 0x1.3768ad48a3716p+1 | 0 |
| tests/resources/filesystem/models/markdown/test_section.py | 231 | 231 | 0x1.311b3c6b344d3p+1 | 0x1.311b3c6b344d3p+1 | 0 |
| src/devtools/context/localization/generation/references.py | 232 | 232 | 0x1.30a3906a7a601p+1 | 0x1.30a3906a7a600p+1 | 0 |
| src/devtools/context/python/references/docs/overview.md | 233 | 233 | 0x1.2ed84b03c6248p+1 | 0x1.2ed84b03c6248p+1 | 0 |
| src/devtools/context/localization/generation/imports.py | 234 | 234 | 0x1.29d62bc99ef00p+1 | 0x1.29d62bc99ef00p+1 | 0 |
| tests/context/python/imports/test_declarations.py | 235 | 235 | 0x1.28514adef7513p+1 | 0x1.28514adef7514p+1 | 0 |
| docs/backlog/items/B-0043-investigate-reusable-agent-semantics.md | 236 | 236 | 0x1.275d486222412p+1 | 0x1.275d486222411p+1 | 0 |
| src/devtools/context/retrieval/repository_map/ranking.py | 237 | 237 | 0x1.269cdcc6203c2p+1 | 0x1.269cdcc6203c2p+1 | 0 |
| src/devtools/resources/commands/docs/overview.md | 238 | 238 | 0x1.26959c5203f5bp+1 | 0x1.26959c5203f5bp+1 | 0 |
| src/devtools/agents/integrations/codex/parsing.py | 239 | 239 | 0x1.26228631d20d9p+1 | 0x1.26228631d20dap+1 | 0 |
| tests/context/localization/test_kernel.py | 240 | 240 | 0x1.25d242d2b84b6p+1 | 0x1.25d242d2b84b6p+1 | 0 |
| src/devtools/context/python/references/declarations/model.py | 241 | 241 | 0x1.2556e8dac1debp+1 | 0x1.2556e8dac1decp+1 | 0 |
| src/devtools/context/python/function/disclosure.py | 242 | 242 | 0x1.24f2f7c5befe3p+1 | 0x1.24f2f7c5befe2p+1 | 0 |
| src/devtools/context/localization/resolution/contract.py | 243 | 243 | 0x1.2101c065bb781p+1 | 0x1.2101c065bb781p+1 | 0 |
| tests/context/localization/roles/test_evidence.py | 244 | 244 | 0x1.209d5bbda6230p+1 | 0x1.209d5bbda6230p+1 | 0 |
| src/devtools/context/localization/assessment.py | 245 | 245 | 0x1.1f49c90f82ee2p+1 | 0x1.1f49c90f82ee1p+1 | 0 |
| tests/resources/filesystem/models/csv/test_row.py | 246 | 246 | 0x1.1b31a9aa01a21p+1 | 0x1.1b31a9aa01a21p+1 | 0 |
| src/devtools/context/localization/readiness.py | 247 | 247 | 0x1.196fb6a352c28p+1 | 0x1.196fb6a352c28p+1 | 0 |
| tests/context/localization/generation/__init__.py | 248 | 248 | 0x1.180fac44938b5p+1 | 0x1.180fac44938b5p+1 | 0 |
| tests/context/python/imports/__init__.py | 249 | 249 | 0x1.17a80d465ed1ep+1 | 0x1.17a80d465ed1ep+1 | 0 |
| tests/context/python/classes/__init__.py | 250 | 250 | 0x1.1740bad9825a1p+1 | 0x1.1740bad9825a0p+1 | 0 |
| tests/models/interaction/test_models.py | 251 | 251 | 0x1.173942f116b19p+1 | 0x1.173942f116b19p+1 | 0 |
| tests/context/localization/roles/helpers.py | 252 | 252 | 0x1.163d0dad79a72p+1 | 0x1.163d0dad79a72p+1 | 0 |
| src/devtools/core/system/docs/overview.md | 253 | 253 | 0x1.0cc9b99b6f48ap+1 | 0x1.0cc9b99b6f48bp+1 | 0 |
| src/devtools/context/python/references/__init__.py | 254 | 254 | 0x1.0c6817cd0ef92p+1 | 0x1.0c6817cd0ef91p+1 | 0 |
| src/devtools/agents/integrations/codex/docs/cli.md | 255 | 255 | 0x1.0c418c050052fp+1 | 0x1.0c418c050052fp+1 | 0 |
| src/devtools/core/time/docs/overview.md | 256 | 256 | 0x1.0b08e5691ad1bp+1 | 0x1.0b08e5691ad1bp+1 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 257 | 257 | 0x1.0ae76aedc9aedp+1 | 0x1.0ae76aedc9aeep+1 | 0 |
| src/devtools/context/python/references/declarations/__init__.py | 258 | 258 | 0x1.0975f32dd14d8p+1 | 0x1.0975f32dd14d8p+1 | 0 |
| src/devtools/models/serving/errors.py | 259 | 259 | 0x1.0962fa06e105bp+1 | 0x1.0962fa06e105bp+1 | 0 |
| src/devtools/context/localization/generation/__init__.py | 260 | 260 | 0x1.08030d622a590p+1 | 0x1.08030d622a58fp+1 | 0 |
| tests/resources/filesystem/codecs/test_text.py | 261 | 261 | 0x1.06619ccb0c594p+1 | 0x1.06619ccb0c595p+1 | 0 |
| src/devtools/context/python/project_configuration/__init__.py | 262 | 262 | 0x1.0583a18b6d45ep+1 | 0x1.0583a18b6d45ep+1 | 0 |
| src/devtools/context/python/modules/lookup.py | 263 | 263 | 0x1.04cf27cd739d5p+1 | 0x1.04cf27cd739d5p+1 | 0 |
| src/devtools/context/localization/grounding/__init__.py | 264 | 264 | 0x1.04754837c0cedp+1 | 0x1.04754837c0cedp+1 | 0 |
| README.md | 265 | 265 | 0x1.03dcbbbb00515p+1 | 0x1.03dcbbbb00515p+1 | 0 |
| src/devtools/context/localization/association/__init__.py | 266 | 266 | 0x1.0325c8d8554ecp+1 | 0x1.0325c8d8554ecp+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/section.py | 267 | 267 | 0x1.ff0f00d7b4d51p+0 | 0x1.ff0f00d7b4d51p+0 | 0 |
| src/devtools/context/python/imports/__init__.py | 268 | 268 | 0x1.fb4295bbeb9fdp+0 | 0x1.fb4295bbeb9fbp+0 | 0 |
| src/devtools/context/repository/__init__.py | 269 | 269 | 0x1.f509e513d7223p+0 | 0x1.f509e513d7222p+0 | 0 |
| docs/backlog/items/B-0038-investigate-approval-workflow-orchestration.md | 270 | 270 | 0x1.f3679e47e4ad0p+0 | 0x1.f3679e47e4acep+0 | 0 |
| docs/backlog/items/B-0044-investigate-orchestration-control-loops.md | 271 | 271 | 0x1.f21e7f3375641p+0 | 0x1.f21e7f3375642p+0 | 0 |
| src/devtools/context/retrieval/lexical/bm25.py | 272 | 272 | 0x1.f17182f0355b3p+0 | 0x1.f17182f0355b3p+0 | 0 |
| docs/backlog/items/B-0033-investigate-semantic-repair-replanning.md | 273 | 273 | 0x1.f033fad3dbe53p+0 | 0x1.f033fad3dbe53p+0 | 0 |
| src/devtools/context/retrieval/lexical/scoring.py | 274 | 274 | 0x1.ee4d38d07cd86p+0 | 0x1.ee4d38d07cd85p+0 | 0 |
| src/devtools/models/interaction/providers/llama_cpp_errors.py | 275 | 275 | 0x1.e94d410938dc7p+0 | 0x1.e94d410938dc7p+0 | 0 |
| src/devtools/models/serving/llama_cpp.py | 276 | 276 | 0x1.e02a8482054c4p+0 | 0x1.e02a8482054c4p+0 | 0 |
| docs/backlog/items/B-0031-investigate-generic-execution-lifecycle-promotion.md | 277 | 277 | 0x1.df99759b1d852p+0 | 0x1.df99759b1d851p+0 | 0 |
| docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md | 278 | 278 | 0x1.ddd2ac5e4885ep+0 | 0x1.ddd2ac5e4885ep+0 | 0 |
| tests/context/repository/test_document.py | 279 | 279 | 0x1.dabb94771581ap+0 | 0x1.dabb94771581ap+0 | 0 |
| src/devtools/context/retrieval/lexical/__init__.py | 280 | 280 | 0x1.da4f22675db7fp+0 | 0x1.da4f22675db7dp+0 | 0 |
| tests/resources/filesystem/models/csv/test_file.py | 281 | 281 | 0x1.d2cfab24b0538p+0 | 0x1.d2cfab24b0539p+0 | 0 |
| src/devtools/context/python/function/request_assembly.py | 282 | 282 | 0x1.c643fdfb00d8cp+0 | 0x1.c643fdfb00d8bp+0 | 0 |
| src/devtools/context/retrieval/lexical/evaluation.py | 283 | 283 | 0x1.c0a0fea372b0ep+0 | 0x1.c0a0fea372b0dp+0 | 0 |
| tests/observability/evidence/test_model_interaction.py | 284 | 284 | 0x1.bf6efb5c08568p+0 | 0x1.bf6efb5c0856ap+0 | 0 |
| tests/resources/filesystem/models/markdown/test_file.py | 285 | 285 | 0x1.baf0c14ed141cp+0 | 0x1.baf0c14ed141bp+0 | 0 |
| src/devtools/tools/disclosure.py | 286 | 286 | 0x1.ba52d553f13a2p+0 | 0x1.ba52d553f13a2p+0 | 0 |
| src/devtools/models/serving/identity.py | 287 | 287 | 0x1.b829d3b07cac1p+0 | 0x1.b829d3b07cac2p+0 | 0 |
| tests/context/retrieval/lexical/test_bm25.py | 288 | 288 | 0x1.b5af750dd0f8bp+0 | 0x1.b5af750dd0f8bp+0 | 0 |
| src/devtools/context/localization/roles/models.py | 289 | 289 | 0x1.b13da0e694bb2p+0 | 0x1.b13da0e694bb3p+0 | 0 |
| src/devtools/context/planning/rendering.py | 290 | 290 | 0x1.b0dbe794d64fdp+0 | 0x1.b0dbe794d64fep+0 | 0 |
| src/devtools/context/python/source_candidacy.py | 291 | 291 | 0x1.ac21e87564547p+0 | 0x1.ac21e87564546p+0 | 0 |
| tests/resources/filesystem/codecs/test_csv.py | 292 | 292 | 0x1.a7144ba2752f4p+0 | 0x1.a7144ba2752f3p+0 | 0 |
| src/devtools/context/__init__.py | 293 | 293 | 0x1.991f5c162ef8ep+0 | 0x1.991f5c162ef8ep+0 | 0 |
| src/devtools/context/python/imports/docs/overview.md | 294 | 294 | 0x1.783fc218825dbp+0 | 0x1.783fc218825dbp+0 | 0 |
| docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md | 295 | 295 | 0x1.781e8471f4034p+0 | 0x1.781e8471f4034p+0 | 0 |
| src/devtools/context/python/imports/relations.py | 296 | 296 | 0x1.7617340a10d32p+0 | 0x1.7617340a10d32p+0 | 0 |
| src/devtools/context/localization/obligation.py | 297 | 297 | 0x1.74db95b09b4b6p+0 | 0x1.74db95b09b4b5p+0 | 0 |
| tests/agents/conversation/test_session.py | 298 | 298 | 0x1.74ca350ccab1fp+0 | 0x1.74ca350ccab20p+0 | 0 |
| src/devtools/core/time/docs/timestamps.md | 299 | 299 | 0x1.5fd71bfc23efep+0 | 0x1.5fd71bfc23efep+0 | 0 |
| src/devtools/models/benchmarks/storage.py | 300 | 300 | 0x1.524bad76e5c37p+0 | 0x1.524bad76e5c37p+0 | 0 |
| tests/resources/commands/test_models.py | 301 | 301 | 0x1.4f5ffcb725d87p+0 | 0x1.4f5ffcb725d87p+0 | 0 |
| tests/context/retrieval/lexical/test_analysis.py | 302 | 302 | 0x1.47fc16b6d0e9ep+0 | 0x1.47fc16b6d0e9ep+0 | 0 |
| src/devtools/context/python/project_configuration/settings.py | 303 | 303 | 0x1.435384e5c5d4dp+0 | 0x1.435384e5c5d4dp+0 | 0 |
| tests/context/retrieval/lexical/test_filename.py | 304 | 304 | 0x1.3960808599607p+0 | 0x1.3960808599606p+0 | 0 |
| src/devtools/context/python/imports/resolution.py | 305 | 305 | 0x1.37dc99ed90a96p+0 | 0x1.37dc99ed90a97p+0 | 0 |
| src/devtools/context/python/references/declarations/bindings.py | 306 | 306 | 0x1.01aaa11a1e62ep+0 | 0x1.01aaa11a1e62ep+0 | 0 |
| tests/persistence/test_sqlite.py | 307 | 307 | 0x1.75b7454af4225p-1 | 0x1.75b7454af4225p-1 | 0 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| filesystem | 86 | 1 | 86 | 0x1.c934d423c47f9p+0 | 0x1.75cd12aa84bc2p+2 | 0x1.c934d423c47f9p+0 |
| bounded | 139 | 1 | 139 | 0x1.4edbd9ed1d54ap+0 | 0x1.75cd12aa84bc2p+2 | 0x1.4edbd9ed1d54ap+0 |
| chunk | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| acquisition | 43 | 0 | 43 | 0x1.3c96989829966p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.3c96989829966p+1 |
| payload | 20 | 0 | 20 | 0x1.9ce324d186cbcp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.9ce324d186cbcp+1 |
| bytes | 43 | 0 | 43 | 0x1.3c96989829966p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.3c96989829966p+1 |
| eof | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| filetoolargeerror | 6 | 0 | 6 | 0x1.17f49b3bac65cp+2 | 0x1.bc1cbc9538c85p+2 | 0x1.17f49b3bac65cp+2 |
| stream | 14 | 0 | 14 | 0x1.c935ec6d91aebp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.c935ec6d91aebp+1 |
| closure | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| memory | 16 | 0 | 16 | 0x1.b8abe9dd16039p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.b8abe9dd16039p+1 |
| stat | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| snapshot | 137 | 1 | 137 | 0x1.528e3c674a916p+0 | 0x1.75cd12aa84bc2p+2 | 0x1.528e3c674a916p+0 |
| containment | 20 | 2 | 20 | 0x1.9ce324d186cbcp+1 | 0x1.551bb4b582938p+2 | 0x1.9ce324d186cbcp+1 |
| authorization | 23 | 0 | 23 | 0x1.8b67d63162854p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.8b67d63162854p+1 |
| locking | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
    ],
    "exited": [
      "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640"
    ],
    "inversion_count": 1,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.25cf5f7c72348p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.25cf5f7c72349p+4"
        },
        "address": "tests/models/benchmarks/test_runner.py",
        "content_identity": "14ee7d72d179a7b5ce3dfdc722944833986a2f16abb549d48dc92906f3e2ceb8",
        "document_identity": "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "address": "src/devtools/resources/commands/execution.py",
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "document_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.01cace3a4b345p+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.f2b5c520c7213p+3"
        },
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "score_delta": {
          "float_hex": "-0x1.0dfd753cf4770p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.fcf7ac341c48ap+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.fcf7ac341c48bp+3"
        },
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 1
      }
    ],
    "pair_inversions": [
      [
        "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
      "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 1,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.25cf5f7c72348p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.25cf5f7c72349p+4"
        },
        "address": "tests/models/benchmarks/test_runner.py",
        "content_identity": "14ee7d72d179a7b5ce3dfdc722944833986a2f16abb549d48dc92906f3e2ceb8",
        "document_identity": "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "address": "src/devtools/resources/commands/execution.py",
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "document_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.01cace3a4b345p+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.f2b5c520c7213p+3"
        },
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "score_delta": {
          "float_hex": "-0x1.0dfd753cf4770p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.fcf7ac341c48ap+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.fcf7ac341c48bp+3"
        },
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.d16d4617e67bcp+3"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.d16d4617e67bbp+3"
        },
        "address": "tests/resources/commands/test_execution.py",
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "document_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.b1a1312c4dcb2p+3"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.b1a1312c4dcb1p+3"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.afcfde9f2bdd2p+3"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.afcfde9f2bdd2p+3"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.acd6492cf7e41p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.acd6492cf7e41p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.9f490f09500ffp+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.9f490f09500ffp+3"
        },
        "address": "src/devtools/resources/commands/docs/events.md",
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.9dfe83f4619fap+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.9dfe83f4619fap+3"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.85ffd5d8b8326p+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.85ffd5d8b8325p+3"
        },
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.7dbf174480970p+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.7dbf17448096fp+3"
        },
        "address": "src/devtools/agents/conversation/docs/conversation.md",
        "content_identity": "4e3efd18c04125aa129a58ef15fa0b42935c646788bfa1c5dd3fe9f8724afdc6",
        "document_identity": "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.7134525419db0p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.7134525419db0p+3"
        },
        "address": "src/devtools/models/benchmarks/docs/overview.md",
        "content_identity": "e06e6abd5f9c3422bbe5159810f443048d2b896174d4c3fcd756b21706bc6973",
        "document_identity": "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [
      [
        "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
      "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
      "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
      "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
      "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "15b42d1cb120af868f279bbef77c0063f1d93c0c9a2df16b70e456d929f3aa80",
      "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5"
    ],
    "exited": [
      "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
      "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8"
    ],
    "inversion_count": 34,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a3414ae801e7dp+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.85cf9d036b049p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.706f8803b69dap+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.40de9a7044ca4p+4"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2750dc3157994p+4"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.26394f1368b9bp+4"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.25cf5f7c72348p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.25cf5f7c72349p+4"
        },
        "address": "tests/models/benchmarks/test_runner.py",
        "content_identity": "14ee7d72d179a7b5ce3dfdc722944833986a2f16abb549d48dc92906f3e2ceb8",
        "document_identity": "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.1bd2f90895fb0p+4"
        },
        "address": "src/devtools/resources/commands/execution.py",
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "document_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.159ff27307869p+4"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.01cace3a4b345p+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.f2b5c520c7213p+3"
        },
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "score_delta": {
          "float_hex": "-0x1.0dfd753cf4770p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.fcf7ac341c48ap+3"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.fcf7ac341c48bp+3"
        },
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.d16d4617e67bcp+3"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.d16d4617e67bbp+3"
        },
        "address": "tests/resources/commands/test_execution.py",
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "document_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.b1a1312c4dcb2p+3"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.b1a1312c4dcb1p+3"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.afcfde9f2bdd2p+3"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.afcfde9f2bdd2p+3"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.acd6492cf7e41p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.acd6492cf7e41p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.9f490f09500ffp+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.9f490f09500ffp+3"
        },
        "address": "src/devtools/resources/commands/docs/events.md",
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.9dfe83f4619fap+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.9dfe83f4619fap+3"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.85ffd5d8b8326p+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.85ffd5d8b8325p+3"
        },
        "address": "src/devtools/models/serving/docs/overview.md",
        "content_identity": "4910894bb88b8a4c8b1a965af1ed74e16319a2d6fad50a66b6a25fe9e931e991",
        "document_identity": "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.7dbf174480970p+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.7dbf17448096fp+3"
        },
        "address": "src/devtools/agents/conversation/docs/conversation.md",
        "content_identity": "4e3efd18c04125aa129a58ef15fa0b42935c646788bfa1c5dd3fe9f8724afdc6",
        "document_identity": "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.7134525419db0p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.7134525419db0p+3"
        },
        "address": "src/devtools/models/benchmarks/docs/overview.md",
        "content_identity": "e06e6abd5f9c3422bbe5159810f443048d2b896174d4c3fcd756b21706bc6973",
        "document_identity": "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.6b01a46fba981p+3"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.6b01a46fba981p+3"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.669bdafcca938p+3"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.669bdafcca938p+3"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.621a54d7f5fa7p+3"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.621a54d7f5fa8p+3"
        },
        "address": "docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md",
        "content_identity": "33c954239327f6dd04a9c8b690b7f34577cdf32685ced4719820dfa0b4c133f7",
        "document_identity": "70f7458544fe2922cf8ec64055c8be00556abddc44dfeb9cf45fa178f079760a",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.507962ea9ee84p+3"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.507962ea9ee84p+3"
        },
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.4ceddea4dcc38p+3"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.4ceddea4dcc38p+3"
        },
        "address": "tests/resources/commands/test_handle.py",
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "document_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.4a040015902fep+3"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.4a040015902fdp+3"
        },
        "address": "docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md",
        "content_identity": "270a3fddbbbc84c6e4bbbb9d109343a4027316182364f1282885b8868374fcfe",
        "document_identity": "9326dbd823befd40c56e5d011c4e5207ef1bda0e3693e9844b01f598fd73186e",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.3e0474cd8f5b2p+3"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.3e0474cd8f5b3p+3"
        },
        "address": "src/devtools/observability/evidence/docs/overview.md",
        "content_identity": "98431aec7bfdfc9c7a4396d6921a5f4174312ccb791b93741b03f8eb0b27c4e7",
        "document_identity": "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.36ed357216162p+3"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.36ed357216163p+3"
        },
        "address": "src/devtools/persistence/docs/overview.md",
        "content_identity": "907c737ace884fa0b840921ed3610d712d31693bd82a5e4931641012bcdc3987",
        "document_identity": "8986afd525a3d67583c80d8f07e5e1883310b3ebc9d6013eed34e30d2640ad46",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.31a0566b17761p+3"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.31a0566b17762p+3"
        },
        "address": "src/devtools/context/python/classes/docs/overview.md",
        "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
        "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.30812520072f0p+3"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.30812520072eep+3"
        },
        "address": "src/devtools/resources/commands/models/output.py",
        "content_identity": "bd7b139009ad69f8bc0f5326c26eaa5d651a60cf534eef3994d0d1d5269a5336",
        "document_identity": "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.284ef26dd1387p+3"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.284ef26dd1386p+3"
        },
        "address": "src/devtools/persistence/docs/sqlite.md",
        "content_identity": "9662f99ff8f8eea4e1a9a08e37d5d87dca99690ea2fcb9f720cb5d087d2f37de",
        "document_identity": "a18a868a1b62ed579a53e0546c54d81a452028811b9c52321ffa33b7b4b25004",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.2126455eda4fap+3"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.2126455eda4fap+3"
        },
        "address": "tests/context/retrieval/graph/test_ranking.py",
        "content_identity": "ef65342956f3850174944516e1e32c566b04543cb05b476cb6f97a10289b6fc6",
        "document_identity": "a4703f865c5432fd385b91e71e369bcbb5948c3a515fd4c2957502688ef6f9d1",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.1b8ef64315735p+3"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.1b8ef64315736p+3"
        },
        "address": "tests/scripts/qwen/test_two_action_read_only_acceptance.py",
        "content_identity": "10fc867f673b0db841d41f18acb33e810fb6c53eb6347d2a428714d9c545ef3d",
        "document_identity": "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.1ab56afa12e41p+3"
        },
        "B_rank": 54,
        "B_score": {
          "float_hex": "0x1.e04a34f8bd96cp+2"
        },
        "address": "src/devtools/context/python/classes/containment.py",
        "content_identity": "47a4bec4b1e0d9ba2449efbe3bf5aa9e381660ca22eb3c904006e796d3316c4f",
        "document_identity": "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "score_delta": {
          "float_hex": "-0x1.548283eda0c58p+0"
        },
        "upward_positions": -20
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.18a38e62e5584p+3"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.18a38e62e5583p+3"
        },
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.16c68afc4a1ddp+3"
        },
        "B_rank": 55,
        "B_score": {
          "float_hex": "0x1.d9dfca07b4b9ap+2"
        },
        "address": "src/devtools/context/python/function/containment.py",
        "content_identity": "7af4524a28e61dc608e35c9ab4ff34c0bc486fb1ef54a3521f9fb0735eb25d69",
        "document_identity": "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "score_delta": {
          "float_hex": "-0x1.4eb52fc37e080p+0"
        },
        "upward_positions": -19
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.0aea289688cfbp+3"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.0aea289688cfcp+3"
        },
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.081915bece6a2p+3"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.081915bece6a3p+3"
        },
        "address": "tests/tools/test_command.py",
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "document_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.02f99775feb94p+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.02f99775feb94p+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
        "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.008e2a248c50fp+3"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.008e2a248c50ep+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
        "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.fbbab7a47b51cp+2"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.fbbab7a47b51bp+2"
        },
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "82979c703980afb5f5508789155c45bb06adc7a5a7d6a973c74c251b602cde1e",
        "document_identity": "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-50"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.faeac0a14b646p+2"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.faeac0a14b646p+2"
        },
        "address": "src/devtools/models/serving/vllm.py",
        "content_identity": "bb7f8c016464fd19407031de00636dd0578982324ef9f62cb51b8844339fbc43",
        "document_identity": "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.f8a80dc45cfafp+2"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.f8a80dc45cfb0p+2"
        },
        "address": "tests/scripts/qwen/test_python_function_context_acceptance.py",
        "content_identity": "3514b02dc85d278a0800cca66340247d63cfc5bf00630909cbffb61423553ade",
        "document_identity": "45c847b8ecfc3c1204f0ca0f496e089c64608ee0b7d600150296d1968faa3d18",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-50"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.efb6843816ed6p+2"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.efb6843816ed6p+2"
        },
        "address": "tests/context/localization/routing/test_routing.py",
        "content_identity": "eb5cd6ca53f81182cacf39d8f349bbc1a5845eee0f83153728d65f2cbf107a63",
        "document_identity": "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.edf9795f88b57p+2"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.edf9795f88b57p+2"
        },
        "address": "docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md",
        "content_identity": "1978bad723268d286560db009f6ef5aeff4a6186563711b1571813c71166e127",
        "document_identity": "93e43be4313117786436dcfefe158087b9dd36571d305602382f986632bd2f80",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.ebf8a840f66fcp+2"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.ebf8a840f66fcp+2"
        },
        "address": "tests/scripts/test_retrieval_bm25_baseline.py",
        "content_identity": "bad05da26cee696ee573abe7dd832d15c0d6b44c81b05d1dba64e5fbcd0ec3b1",
        "document_identity": "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.ebcedc6890810p+2"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.ebcedc6890810p+2"
        },
        "address": "src/devtools/resources/commands/handle.py",
        "content_identity": "c9825687577803f98911494be5c86ddd84af006d627acdbacbc2b28d9c82b06c",
        "document_identity": "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.eba96d6b7a9eep+2"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.eba96d6b7a9eep+2"
        },
        "address": "tests/scripts/qwen/test_two_read_acceptance.py",
        "content_identity": "06bc002a1bc83452150e618d4392cf624baa9f71a02cc9e95422ffe0e7500883",
        "document_identity": "fe68fde589c53a9ccde159d09e7316958e61c714e517722fc2674315c0415ee2",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.eaf1a360b5c78p+2"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.eaf1a360b5c7ap+2"
        },
        "address": "src/devtools/context/retrieval/repository_map/view.py",
        "content_identity": "e25814030b6badf5e943402afb2c19ac2dd6eee4d4ec410609716be3bf720bf7",
        "document_identity": "9834e34c522641b6926a9489c1e76096189adfdf4781e76cedf0d1a3af380bee",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.e923182f7e138p+2"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.e923182f7e138p+2"
        },
        "address": "tests/context/localization/association/test_hypothesis.py",
        "content_identity": "c6dfaacdab3157a9e64dd6156cff697c460e22b41e579354d2d38c78be77cba6",
        "document_identity": "d3eeca3ae0435312835809236e532c02683a1c85bb52c305d53c909dd8913251",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 51,
        "A_score": {
          "float_hex": "0x1.e6b9d82a25c0cp+2"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.e6b9d82a25c0bp+2"
        },
        "address": "src/devtools/context/retrieval/repository_map/importance.py",
        "content_identity": "d0f4f26b6c287f28d59ea8bc36e79cf3ea40560b40901ced5a14fc72744b8f7c",
        "document_identity": "15b42d1cb120af868f279bbef77c0063f1d93c0c9a2df16b70e456d929f3aa80",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-50"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 52,
        "A_score": {
          "float_hex": "0x1.e46aad477c4f3p+2"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.e46aad477c4f2p+2"
        },
        "address": "src/devtools/context/planning/resource.py",
        "content_identity": "f05d554cc5e81d1584c463f37c9d05801293c4a6cf74c839c5ea650a26c6123b",
        "document_identity": "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-50"
        },
        "upward_positions": 2
      }
    ],
    "pair_inversions": [
      [
        "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "45c847b8ecfc3c1204f0ca0f496e089c64608ee0b7d600150296d1968faa3d18"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "93e43be4313117786436dcfefe158087b9dd36571d305602382f986632bd2f80"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "fe68fde589c53a9ccde159d09e7316958e61c714e517722fc2674315c0415ee2"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "9834e34c522641b6926a9489c1e76096189adfdf4781e76cedf0d1a3af380bee"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "d3eeca3ae0435312835809236e532c02683a1c85bb52c305d53c909dd8913251"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "15b42d1cb120af868f279bbef77c0063f1d93c0c9a2df16b70e456d929f3aa80"
      ],
      [
        "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
        "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "45c847b8ecfc3c1204f0ca0f496e089c64608ee0b7d600150296d1968faa3d18"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "93e43be4313117786436dcfefe158087b9dd36571d305602382f986632bd2f80"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "fe68fde589c53a9ccde159d09e7316958e61c714e517722fc2674315c0415ee2"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "9834e34c522641b6926a9489c1e76096189adfdf4781e76cedf0d1a3af380bee"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "d3eeca3ae0435312835809236e532c02683a1c85bb52c305d53c909dd8913251"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "15b42d1cb120af868f279bbef77c0063f1d93c0c9a2df16b70e456d929f3aa80"
      ],
      [
        "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
        "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
      "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
      "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "c21bc65f62568fefdf37163925861c0b05351b350af6e4ff59a7cb83dbb45f71",
      "f2fc1af0ab3f1ffd2c48bb08d611011cf2d9c87beeeed602d12a7f01d67d518b",
      "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "70f7458544fe2922cf8ec64055c8be00556abddc44dfeb9cf45fa178f079760a",
      "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
      "9326dbd823befd40c56e5d011c4e5207ef1bda0e3693e9844b01f598fd73186e",
      "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
      "8986afd525a3d67583c80d8f07e5e1883310b3ebc9d6013eed34e30d2640ad46",
      "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
      "7f53d0ef6cc000c00f0a9ffb19fa42a886e1f332c1a611cf5a3c38b92f733d3d",
      "a18a868a1b62ed579a53e0546c54d81a452028811b9c52321ffa33b7b4b25004",
      "a4703f865c5432fd385b91e71e369bcbb5948c3a515fd4c2957502688ef6f9d1",
      "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
      "fdf5ea2c18fbae4e67ffa276e4aac88463b68753e7cd839635b0179173fe9175",
      "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
      "c58c277bd0efe01f5fc81064b7bf2f5c500c8babc9b13bf89154b59a2e6eaaa8",
      "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
      "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
      "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
      "102500de6c5fe4a11e8f5fb22d0f9c293883061b1cce284c36203f6847b3fd22",
      "45c847b8ecfc3c1204f0ca0f496e089c64608ee0b7d600150296d1968faa3d18",
      "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b",
      "93e43be4313117786436dcfefe158087b9dd36571d305602382f986632bd2f80",
      "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
      "87ff41fce978e2698fe96b4a0ec4bdfeec64a0c15d2b4a9fc3757cfcb59525d9",
      "fe68fde589c53a9ccde159d09e7316958e61c714e517722fc2674315c0415ee2",
      "9834e34c522641b6926a9489c1e76096189adfdf4781e76cedf0d1a3af380bee",
      "d3eeca3ae0435312835809236e532c02683a1c85bb52c305d53c909dd8913251",
      "15b42d1cb120af868f279bbef77c0063f1d93c0c9a2df16b70e456d929f3aa80",
      "0a23e17b83599252292e40cca317125d7cf495c6eed74c1a0b274ec12bb260e5"
    ]
  }
}
```


## Q3: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/__init__.py | 1 | 1 | 0x1.9f0dbfcf305c5p+5 | 0x1.9f0dbfcf305c5p+5 | 0 |
| tests/resources/filesystem/test_reading.py | 2 | 2 | 0x1.66b78c80ef727p+5 | 0x1.66b78c80ef727p+5 | 0 |
| tests/resources/filesystem/codecs/test_json.py | 3 | 3 | 0x1.513290bcf8062p+5 | 0x1.513290bcf8062p+5 | 0 |
| src/devtools/resources/filesystem/codecs/json.py | 4 | 4 | 0x1.41976a8e4bb95p+5 | 0x1.41976a8e4bb94p+5 | 0 |
| src/devtools/resources/filesystem/models/__init__.py | 5 | 5 | 0x1.3839d329b8281p+5 | 0x1.3839d329b8280p+5 | 0 |
| src/devtools/resources/filesystem/docs/models.md | 6 | 6 | 0x1.382b25943bc2ep+5 | 0x1.382b25943bc2dp+5 | 0 |
| tests/resources/filesystem/codecs/test_csv.py | 7 | 7 | 0x1.26a00ea29b338p+5 | 0x1.26a00ea29b337p+5 | 0 |
| tests/resources/filesystem/test_models.py | 8 | 8 | 0x1.f8c731d6102cep+4 | 0x1.f8c731d6102cep+4 | 0 |
| src/devtools/resources/filesystem/codecs/markdown.py | 9 | 9 | 0x1.de44cca0aff89p+4 | 0x1.de44cca0aff88p+4 | 0 |
| src/devtools/resources/filesystem/codecs/text.py | 10 | 10 | 0x1.db19e96ad238ap+4 | 0x1.db19e96ad238ap+4 | 0 |
| tests/resources/filesystem/codecs/test_text.py | 11 | 11 | 0x1.9bbc3e2a20257p+4 | 0x1.9bbc3e2a20258p+4 | 0 |
| tests/resources/filesystem/codecs/test_markdown.py | 12 | 12 | 0x1.93728e931e170p+4 | 0x1.93728e931e16fp+4 | 0 |
| src/devtools/resources/filesystem/codecs/csv.py | 13 | 13 | 0x1.9059c664a4841p+4 | 0x1.9059c664a4840p+4 | 0 |
| src/devtools/resources/filesystem/docs/json.md | 14 | 14 | 0x1.83f90a80d5463p+4 | 0x1.83f90a80d5464p+4 | 0 |
| src/devtools/resources/filesystem/writing.py | 15 | 15 | 0x1.6fd8ac94c1d1dp+4 | 0x1.6fd8ac94c1d1dp+4 | 0 |
| tests/tools/test_filesystem.py | 16 | 16 | 0x1.6c2cce8998f9bp+4 | 0x1.6c2cce8998f9bp+4 | 0 |
| src/devtools/resources/filesystem/models/json/__init__.py | 17 | 17 | 0x1.42754630b33f1p+4 | 0x1.42754630b33f0p+4 | 0 |
| src/devtools/resources/filesystem/models/text.py | 18 | 18 | 0x1.3fdf688cc9fc7p+4 | 0x1.3fdf688cc9fc8p+4 | 0 |
| tests/context/repository/test_observation.py | 19 | 19 | 0x1.1135c70c2a134p+4 | 0x1.1135c70c2a134p+4 | 0 |
| src/devtools/context/repository/observation.py | 20 | 20 | 0x1.102a4162344c0p+4 | 0x1.102a4162344c0p+4 | 0 |
| tests/resources/filesystem/test_json_conversion.py | 21 | 21 | 0x1.0fd3bb3d170b4p+4 | 0x1.0fd3bb3d170b4p+4 | 0 |
| tests/resources/filesystem/test_json_models.py | 22 | 22 | 0x1.0e56dcdd76780p+4 | 0x1.0e56dcdd76780p+4 | 0 |
| tests/resources/filesystem/test_resolution.py | 23 | 23 | 0x1.0b7992322e703p+4 | 0x1.0b7992322e704p+4 | 0 |
| tests/resources/filesystem/test_writing.py | 24 | 24 | 0x1.e9c2899933840p+3 | 0x1.e9c2899933841p+3 | 0 |
| src/devtools/resources/filesystem/docs/markdown.md | 25 | 25 | 0x1.a5381887ababap+3 | 0x1.a5381887ababbp+3 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 26 | 26 | 0x1.9f6c58191af66p+3 | 0x1.9f6c58191af66p+3 | 0 |
| src/devtools/resources/filesystem/reading.py | 27 | 27 | 0x1.97c563b5d1c68p+3 | 0x1.97c563b5d1c68p+3 | 0 |
| tests/resources/filesystem/models/markdown/test_file.py | 28 | 28 | 0x1.96755986f9c13p+3 | 0x1.96755986f9c12p+3 | 0 |
| tests/context/retrieval/lexical/_helpers.py | 29 | 29 | 0x1.9050af1754c88p+3 | 0x1.9050af1754c88p+3 | 0 |
| src/devtools/core/conversion/docs/overview.md | 30 | 30 | 0x1.8deb7adc36f7bp+3 | 0x1.8deb7adc36f7bp+3 | 0 |
| tests/context/repository/test_corpus.py | 31 | 31 | 0x1.8dc5d997ceaf4p+3 | 0x1.8dc5d997ceaf4p+3 | 0 |
| src/devtools/resources/filesystem/docs/csv.md | 32 | 32 | 0x1.8c8d21c0b1f5ep+3 | 0x1.8c8d21c0b1f5ep+3 | 0 |
| tests/context/python/function/test_materialization.py | 33 | 33 | 0x1.7232120585270p+3 | 0x1.7232120585270p+3 | 0 |
| src/devtools/resources/filesystem/resolution.py | 34 | 34 | 0x1.6684f8b902b35p+3 | 0x1.6684f8b902b35p+3 | 0 |
| src/devtools/context/python/function/materialization.py | 35 | 35 | 0x1.5ebbbbe42f0fap+3 | 0x1.5ebbbbe42f0f9p+3 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 36 | 36 | 0x1.43f93e3b05c29p+3 | 0x1.43f93e3b05c2ap+3 | 0 |
| src/devtools/context/repository/resource.py | 37 | 37 | 0x1.41eefa6d8c34cp+3 | 0x1.41eefa6d8c34cp+3 | 0 |
| src/devtools/models/benchmarks/storage.py | 38 | 38 | 0x1.3832a1f178221p+3 | 0x1.3832a1f178220p+3 | 0 |
| src/devtools/models/benchmarks/runner.py | 39 | 39 | 0x1.3126bfe7bc640p+3 | 0x1.3126bfe7bc640p+3 | 0 |
| tests/context/repository/test_discovery.py | 40 | 40 | 0x1.28f539c1c9731p+3 | 0x1.28f539c1c9731p+3 | 0 |
| tests/models/benchmarks/test_storage.py | 41 | 41 | 0x1.231fc032eed2ep+3 | 0x1.231fc032eed2dp+3 | 0 |
| src/devtools/resources/filesystem/errors.py | 42 | 42 | 0x1.1bdfb4cc784d5p+3 | 0x1.1bdfb4cc784d6p+3 | 0 |
| src/devtools/agents/integrations/codex/parsing.py | 43 | 43 | 0x1.1aff86bafe094p+3 | 0x1.1aff86bafe094p+3 | 0 |
| tests/context/python/test_source_candidacy.py | 44 | 44 | 0x1.17ca85fa9214bp+3 | 0x1.17ca85fa9214cp+3 | 0 |
| tests/context/python/imports/test_declarations.py | 45 | 45 | 0x1.147ad335fc343p+3 | 0x1.147ad335fc342p+3 | 0 |
| src/devtools/resources/filesystem/docs/io.md | 46 | 46 | 0x1.13306d39e318dp+3 | 0x1.13306d39e318fp+3 | 0 |
| src/devtools/resources/filesystem/docs/overview.md | 47 | 47 | 0x1.0ebba39b69b34p+3 | 0x1.0ebba39b69b34p+3 | 0 |
| src/devtools/resources/filesystem/docs/codecs.md | 48 | 48 | 0x1.08e903ef5bbc0p+3 | 0x1.08e903ef5bbc0p+3 | 0 |
| tests/context/python/imports/test_relations.py | 49 | 49 | 0x1.0794fd0e8c4fcp+3 | 0x1.0794fd0e8c4fdp+3 | 0 |
| tests/context/python/function/test_declarations.py | 50 | 50 | 0x1.050fe9af481c4p+3 | 0x1.050fe9af481c4p+3 | 0 |
| tests/models/benchmarks/test_runner.py | 51 | 51 | 0x1.fd57462f47726p+2 | 0x1.fd57462f47726p+2 | 0 |
| tests/scripts/test_retrieval_bm25_baseline.py | 52 | 52 | 0x1.fabaf71d0870ep+2 | 0x1.fabaf71d0870ep+2 | 0 |
| tests/scripts/qwen/test_two_read_acceptance.py | 53 | 53 | 0x1.eeafc6fd871f0p+2 | 0x1.eeafc6fd871f0p+2 | 0 |
| src/devtools/core/regex/docs/overview.md | 54 | 54 | 0x1.dbb37d9cebb66p+2 | 0x1.dbb37d9cebb66p+2 | 0 |
| src/devtools/models/serving/vllm.py | 55 | 55 | 0x1.d86e4f19834fcp+2 | 0x1.d86e4f19834fcp+2 | 0 |
| tests/context/localization/roles/helpers.py | 56 | 56 | 0x1.baa6bd7bf8fffp+2 | 0x1.baa6bd7bf8fffp+2 | 0 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 57 | 57 | 0x1.b9f80c1b775edp+2 | 0x1.b9f80c1b775ebp+2 | 0 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 58 | 58 | 0x1.ae25ff01e7f00p+2 | 0x1.ae25ff01e7efep+2 | 0 |
| src/devtools/resources/filesystem/models/json/list.py | 59 | 59 | 0x1.aae7c2ccbaa54p+2 | 0x1.aae7c2ccbaa54p+2 | 0 |
| src/devtools/resources/filesystem/models/json/object.py | 60 | 60 | 0x1.97ea4478ced76p+2 | 0x1.97ea4478ced76p+2 | 0 |
| tests/resources/filesystem/models/csv/test_file.py | 61 | 61 | 0x1.967be7fcc6b90p+2 | 0x1.967be7fcc6b90p+2 | 0 |
| src/devtools/context/python/function/request_assembly.py | 62 | 62 | 0x1.8509bdcaba036p+2 | 0x1.8509bdcaba036p+2 | 0 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 63 | 63 | 0x1.84d56aec19f78p+2 | 0x1.84d56aec19f77p+2 | 0 |
| src/devtools/models/serving/llama_cpp.py | 64 | 64 | 0x1.831c5afa602f3p+2 | 0x1.831c5afa602f3p+2 | 0 |
| src/devtools/context/planning/rendering.py | 65 | 65 | 0x1.7ce157eb251d2p+2 | 0x1.7ce157eb251d2p+2 | 0 |
| tests/context/python/project_configuration/test_configuration.py | 66 | 66 | 0x1.784a81c4697bbp+2 | 0x1.784a81c4697bap+2 | 0 |
| src/devtools/tools/docs/overview.md | 67 | 67 | 0x1.706b093b9abf8p+2 | 0x1.706b093b9abf8p+2 | 0 |
| pyproject.toml | 68 | 68 | 0x1.6f4d8583fecabp+2 | 0x1.6f4d8583fecaap+2 | 0 |
| src/devtools/context/python/function/rendering.py | 69 | 69 | 0x1.6ed3d2bd80eb9p+2 | 0x1.6ed3d2bd80eb8p+2 | 0 |
| src/devtools/resources/filesystem/models/json/base.py | 70 | 70 | 0x1.6e8c39c97bb11p+2 | 0x1.6e8c39c97bb12p+2 | 0 |
| src/devtools/resources/commands/docs/overview.md | 71 | 71 | 0x1.6d9d2c1b6ee5ap+2 | 0x1.6d9d2c1b6ee5ap+2 | 0 |
| tests/context/python/function/test_candidates.py | 72 | 72 | 0x1.6ce790b2667eep+2 | 0x1.6ce790b2667efp+2 | 0 |
| src/devtools/context/python/function/qualified_reference.py | 73 | 73 | 0x1.6ac80596aeb07p+2 | 0x1.6ac80596aeb06p+2 | 0 |
| src/devtools/resources/filesystem/models/markdown/section.py | 74 | 74 | 0x1.6a6acbf665c83p+2 | 0x1.6a6acbf665c83p+2 | 0 |
| src/devtools/tools/filesystem.py | 75 | 75 | 0x1.6294a5b1cc7bfp+2 | 0x1.6294a5b1cc7bfp+2 | 0 |
| tests/context/repository/test_document.py | 76 | 76 | 0x1.5eb2b4c3fbeffp+2 | 0x1.5eb2b4c3fbefep+2 | 0 |
| tests/agents/conversation/message/test_message.py | 77 | 77 | 0x1.5cb652a62c8d2p+2 | 0x1.5cb652a62c8d2p+2 | 0 |
| tests/context/python/function/test_request_assembly.py | 78 | 78 | 0x1.5b8ab31a67a44p+2 | 0x1.5b8ab31a67a45p+2 | 0 |
| src/devtools/resources/filesystem/models/json/scalar.py | 79 | 79 | 0x1.5b7b9bdcbc097p+2 | 0x1.5b7b9bdcbc095p+2 | 0 |
| docs/experiments/qwen38_llama_cpp.md | 80 | 80 | 0x1.5a2ffb24d3b16p+2 | 0x1.5a2ffb24d3b17p+2 | 0 |
| src/devtools/resources/filesystem/models/markdown/heading.py | 81 | 81 | 0x1.57267dadafb56p+2 | 0x1.57267dadafb55p+2 | 0 |
| tests/context/python/function/test_retrieval.py | 82 | 82 | 0x1.561350ab72a87p+2 | 0x1.561350ab72a86p+2 | 0 |
| tests/context/python/function/test_disclosure.py | 83 | 83 | 0x1.5448c99c040bep+2 | 0x1.5448c99c040bep+2 | 0 |
| tests/resources/filesystem/models/markdown/test_heading.py | 84 | 84 | 0x1.4e78419fe187ep+2 | 0x1.4e78419fe187fp+2 | 0 |
| src/devtools/models/interaction/providers/llama_cpp.py | 85 | 85 | 0x1.4dcf43872afb8p+2 | 0x1.4dcf43872afb8p+2 | 0 |
| tests/context/retrieval/graph/test_ranking.py | 86 | 86 | 0x1.3f53d2739fc0ap+2 | 0x1.3f53d2739fc0bp+2 | 0 |
| src/devtools/context/planning/resource.py | 87 | 87 | 0x1.340504b4bce30p+2 | 0x1.340504b4bce2fp+2 | 0 |
| tests/models/interaction/providers/test_llama_cpp.py | 88 | 88 | 0x1.32f96ef2e05b2p+2 | 0x1.32f96ef2e05b2p+2 | 0 |
| tests/agents/integrations/codex/test_parsing.py | 89 | 89 | 0x1.30a44c119b90cp+2 | 0x1.30a44c119b90cp+2 | 0 |
| tests/context/python/modules/test_interpretation.py | 90 | 90 | 0x1.2ff217692f96fp+2 | 0x1.2ff217692f970p+2 | 0 |
| tests/context/python/function/test_rendering.py | 91 | 91 | 0x1.2cbc4bcb85066p+2 | 0x1.2cbc4bcb85067p+2 | 0 |
| tests/context/python/function/test_declaration_aggregation.py | 92 | 92 | 0x1.2294fb5d9ccbep+2 | 0x1.2294fb5d9ccbep+2 | 0 |
| tests/context/localization/grounding/test_grounding.py | 93 | 93 | 0x1.1fcc7a028f771p+2 | 0x1.1fcc7a028f771p+2 | 0 |
| src/devtools/context/repository/corpus.py | 94 | 94 | 0x1.1fcb288e3bb4ep+2 | 0x1.1fcb288e3bb50p+2 | 0 |
| src/devtools/context/python/function/disclosure.py | 95 | 95 | 0x1.1ef959077b7f0p+2 | 0x1.1ef959077b7f0p+2 | 0 |
| tests/context/python/test_mirrored_paths.py | 96 | 96 | 0x1.1e1ac6535deadp+2 | 0x1.1e1ac6535deadp+2 | 0 |
| src/devtools/context/repository/document.py | 97 | 97 | 0x1.18e3214391d88p+2 | 0x1.18e3214391d89p+2 | 0 |
| tests/context/localization/roles/test_configuration.py | 98 | 98 | 0x1.11a7da7aaeff4p+2 | 0x1.11a7da7aaeff4p+2 | 0 |
| tests/context/python/function/test_resource_selection.py | 99 | 99 | 0x1.10b2e2dd82886p+2 | 0x1.10b2e2dd82887p+2 | 0 |
| tests/context/python/function/test_cross_resource_pipeline.py | 100 | 100 | 0x1.0f8f2d6ce7484p+2 | 0x1.0f8f2d6ce7484p+2 | 0 |
| tests/context/retrieval/test_structural.py | 101 | 101 | 0x1.0b761efdc7faep+2 | 0x1.0b761efdc7facp+2 | 0 |
| tests/context/python/function/test_containment.py | 102 | 102 | 0x1.061195a8000bfp+2 | 0x1.061195a8000bfp+2 | 0 |
| src/devtools/context/python/function/declarations.py | 103 | 103 | 0x1.0510ebd031ccep+2 | 0x1.0510ebd031ccdp+2 | 0 |
| src/devtools/context/python/imports/relations.py | 104 | 104 | 0x1.050ae27107146p+2 | 0x1.050ae27107146p+2 | 0 |
| tests/context/python/modules/test_membership.py | 105 | 105 | 0x1.0504218438a6cp+2 | 0x1.0504218438a6cp+2 | 0 |
| src/devtools/context/python/classes/docs/overview.md | 106 | 106 | 0x1.02344c47e1249p+2 | 0x1.02344c47e124ap+2 | 0 |
| src/devtools/context/planning/plan.py | 107 | 107 | 0x1.00099a295ff6cp+2 | 0x1.00099a295ff6bp+2 | 0 |
| src/devtools/agents/integrations/codex/docs/cli.md | 108 | 108 | 0x1.f3f42c0ae1b59p+1 | 0x1.f3f42c0ae1b5ap+1 | 0 |
| src/devtools/context/python/imports/declarations.py | 109 | 109 | 0x1.ef64907b665fcp+1 | 0x1.ef64907b665fep+1 | 0 |
| src/devtools/context/python/references/declarations/model.py | 110 | 110 | 0x1.d320d16311b65p+1 | 0x1.d320d16311b65p+1 | 0 |
| tests/context/retrieval/test_composition.py | 111 | 111 | 0x1.d110211f1e00ap+1 | 0x1.d110211f1e00cp+1 | 0 |
| src/devtools/context/python/imports/resolution.py | 112 | 112 | 0x1.c54ad17cac8dcp+1 | 0x1.c54ad17cac8dbp+1 | 0 |
| src/devtools/context/python/project_configuration/models.py | 113 | 113 | 0x1.bc5548e96fad5p+1 | 0x1.bc5548e96fad4p+1 | 0 |
| src/devtools/context/python/mirrored_paths.py | 114 | 114 | 0x1.b89029a798386p+1 | 0x1.b89029a798386p+1 | 0 |
| src/devtools/context/python/modules/declarations.py | 115 | 115 | 0x1.b7fd2d4ef5faap+1 | 0x1.b7fd2d4ef5fa8p+1 | 0 |
| tests/context/python/imports/test_resolution.py | 116 | 116 | 0x1.b27d2c4f9b92cp+1 | 0x1.b27d2c4f9b92cp+1 | 0 |
| tests/context/python/project_configuration/test_settings.py | 117 | 117 | 0x1.a2679199aa952p+1 | 0x1.a2679199aa953p+1 | 0 |
| src/devtools/context/planning/docs/overview.md | 118 | 118 | 0x1.a139e8961e7c7p+1 | 0x1.a139e8961e7c6p+1 | 0 |
| src/devtools/context/python/modules/interpretation.py | 119 | 119 | 0x1.9863b392aeca8p+1 | 0x1.9863b392aeca8p+1 | 0 |
| tests/context/retrieval/repository_map/test_ranking.py | 120 | 120 | 0x1.93428859206c8p+1 | 0x1.93428859206c8p+1 | 0 |
| tests/context/python/modules/test_selection.py | 121 | 121 | 0x1.8e905d045ca70p+1 | 0x1.8e905d045ca70p+1 | 0 |
| tests/context/python/classes/test_declarations.py | 122 | 122 | 0x1.81849b49e3b8ep+1 | 0x1.81849b49e3b8ep+1 | 0 |
| src/devtools/context/python/modules/membership.py | 123 | 123 | 0x1.7b6aeacd925cfp+1 | 0x1.7b6aeacd925d0p+1 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 124 | 124 | 0x1.7b569661457f5p+1 | 0x1.7b569661457f6p+1 | 0 |
| tests/context/retrieval/graph/test_typed.py | 125 | 125 | 0x1.758422c2d790cp+1 | 0x1.758422c2d790cp+1 | 0 |
| src/devtools/context/localization/roles/models.py | 126 | 126 | 0x1.70b153e6dd616p+1 | 0x1.70b153e6dd614p+1 | 0 |
| tests/context/python/classes/test_bases.py | 127 | 127 | 0x1.60e55341a0dc9p+1 | 0x1.60e55341a0dc9p+1 | 0 |
| tests/scripts/qwen/test_llama_cpp_profile.py | 128 | 128 | 0x1.5ace12b61e3c0p+1 | 0x1.5ace12b61e3bfp+1 | 0 |
| src/devtools/context/python/function/docs/overview.md | 129 | 129 | 0x1.4fe9726e08a2dp+1 | 0x1.4fe9726e08a2ep+1 | 0 |
| tests/context/python/function/test_qualified_reference.py | 130 | 130 | 0x1.4bd9e4feb9560p+1 | 0x1.4bd9e4feb9560p+1 | 0 |
| tests/context/python/imports/test_members.py | 131 | 131 | 0x1.4a2f6b0eab27ep+1 | 0x1.4a2f6b0eab27fp+1 | 0 |
| tests/models/interaction/test_models.py | 132 | 132 | 0x1.40b9695b6acfcp+1 | 0x1.40b9695b6acfcp+1 | 0 |
| tests/context/python/references/declarations/test_analysis.py | 133 | 133 | 0x1.2d77829ac93e4p+1 | 0x1.2d77829ac93e3p+1 | 0 |
| tests/models/benchmarks/test_models.py | 134 | 134 | 0x1.2ce335a1a31efp+1 | 0x1.2ce335a1a31efp+1 | 0 |
| tests/scripts/test_vllm_benchmark_driver.py | 135 | 135 | 0x1.2a6fe465870ccp+1 | 0x1.2a6fe465870cdp+1 | 0 |
| src/devtools/context/python/imports/members.py | 136 | 136 | 0x1.2962280d3d69cp+1 | 0x1.2962280d3d69bp+1 | 0 |
| src/devtools/context/python/classes/declarations.py | 137 | 137 | 0x1.26f464305c24ap+1 | 0x1.26f464305c24ap+1 | 0 |
| src/devtools/context/python/classes/bases.py | 138 | 138 | 0x1.2550de0c22f9ap+1 | 0x1.2550de0c22f9ap+1 | 0 |
| tests/context/planning/test_plan.py | 139 | 139 | 0x1.194a607e24922p+1 | 0x1.194a607e24922p+1 | 0 |
| tests/agents/conversation/history/test_history.py | 140 | 140 | 0x1.0ec4c08b6a9f7p+1 | 0x1.0ec4c08b6a9f7p+1 | 0 |
| src/devtools/context/python/references/declarations/bindings.py | 141 | 141 | 0x1.0a704a2d4f18ap+1 | 0x1.0a704a2d4f18bp+1 | 0 |
| tests/models/serving/test_llama_cpp.py | 142 | 142 | 0x1.02f8563fc337ep+1 | 0x1.02f8563fc337ep+1 | 0 |
| tests/resources/filesystem/models/markdown/test_section.py | 143 | 143 | 0x1.0132e625b6cfcp+1 | 0x1.0132e625b6cfbp+1 | 0 |
| src/devtools/context/python/references/declarations/resolution.py | 144 | 144 | 0x1.ed73802ea97d3p+0 | 0x1.ed73802ea97d4p+0 | 0 |
| AGENTS.md | 145 | 145 | 0x1.c91a929a08d9bp+0 | 0x1.c91a929a08d9ap+0 | 0 |
| tests/context/localization/generation/test_branching.py | 146 | 146 | 0x1.c46a29e0786dep+0 | 0x1.c46a29e0786dep+0 | 0 |
| tests/agents/conversation/test_session.py | 147 | 147 | 0x1.bb6b6b5e31002p+0 | 0x1.bb6b6b5e31002p+0 | 0 |
| tests/core/time/test_parsing.py | 148 | 148 | 0x1.96708ba9fda18p+0 | 0x1.96708ba9fda18p+0 | 0 |
| tests/core/time/test_models.py | 149 | 149 | 0x1.7604719a5b3ffp+0 | 0x1.7604719a5b3ffp+0 | 0 |
| tests/models/serving/test_vllm.py | 150 | 150 | 0x1.6badd9e07cad0p+0 | 0x1.6badd9e07cacep+0 | 0 |
| tests/context/localization/generation/test_references.py | 151 | 151 | 0x1.511532a08de09p+0 | 0x1.511532a08de0ap+0 | 0 |
| tests/observability/evidence/test_model_interaction.py | 152 | 152 | 0x1.4f204bd828b00p+0 | 0x1.4f204bd828b01p+0 | 0 |
| tests/execution/test_interaction_attempt.py | 153 | 153 | 0x1.ead8674bae3ccp-1 | 0x1.ead8674bae3cdp-1 | 0 |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 154 | 154 | 0x1.c55fd5e7dc3fdp-1 | 0x1.c55fd5e7dc3fdp-1 | 0 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 155 | 155 | 0x1.5ca8b2cedb940p-1 | 0x1.5ca8b2cedb941p-1 | 0 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 156 | 156 | 0x1.52d3f75ac7a06p-1 | 0x1.52d3f75ac7a06p-1 | 0 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| resolve_file_format | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| resolve_codec | 5 | 0 | 5 | 0x1.22a59ed93f0dfp+2 | 0x1.bc1cbc9538c85p+2 | 0x1.22a59ed93f0dfp+2 |
| textfile | 18 | 0 | 18 | 0x1.aa06ea46c514dp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.aa06ea46c514dp+1 |
| markdownfile | 12 | 0 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.dc3559ab98bd6p+1 |
| csvfile | 12 | 0 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.dc3559ab98bd6p+1 |
| jsonobjectfile | 13 | 0 | 13 | 0x1.d25b7daa3947ap+1 | 0x1.bc1cbc9538c85p+2 | 0x1.d25b7daa3947ap+1 |
| jsonlistfile | 12 | 0 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.dc3559ab98bd6p+1 |
| jsonscalarfile | 12 | 0 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.dc3559ab98bd6p+1 |
| utf | 95 | 0 | 95 | 0x1.afddf489c6f2cp+0 | 0x1.bc1cbc9538c85p+2 | 0x1.afddf489c6f2cp+0 |
| 8 | 114 | 0 | 114 | 0x1.816a8a9810f09p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.816a8a9810f09p+0 |
| decoding | 14 | 0 | 14 | 0x1.c935ec6d91aebp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.c935ec6d91aebp+1 |
| encoding | 64 | 0 | 64 | 0x1.0a2b23f3bab73p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.0a2b23f3bab73p+1 |
| byte_size | 19 | 0 | 19 | 0x1.a349e2a1f0b33p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.a349e2a1f0b33p+1 |
| line | 34 | 0 | 34 | 0x1.5a424577ee395p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.5a424577ee395p+1 |
| endings | 1 | 0 | 1 | 0x1.75cd12aa84bc2p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.75cd12aa84bc2p+2 |
| textdecodingerror | 14 | 0 | 14 | 0x1.c935ec6d91aebp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.c935ec6d91aebp+1 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.41976a8e4bb95p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.41976a8e4bb94p+5"
        },
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
        "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.3839d329b8281p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.3839d329b8280p+5"
        },
        "address": "src/devtools/resources/filesystem/models/__init__.py",
        "content_identity": "e09ae5eeb0da9afd9f4921634debfd2af6e9fbcf84a98450526c62f52e5fcf5c",
        "document_identity": "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.382b25943bc2ep+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.382b25943bc2dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.26a00ea29b338p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.26a00ea29b337p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.de44cca0aff89p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.de44cca0aff88p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
        "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
        "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.41976a8e4bb95p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.41976a8e4bb94p+5"
        },
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
        "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.3839d329b8281p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.3839d329b8280p+5"
        },
        "address": "src/devtools/resources/filesystem/models/__init__.py",
        "content_identity": "e09ae5eeb0da9afd9f4921634debfd2af6e9fbcf84a98450526c62f52e5fcf5c",
        "document_identity": "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.382b25943bc2ep+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.382b25943bc2dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.26a00ea29b338p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.26a00ea29b337p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.de44cca0aff89p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.de44cca0aff88p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
        "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
        "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.9bbc3e2a20257p+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.9bbc3e2a20258p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
        "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.93728e931e170p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.93728e931e16fp+4"
        },
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.9059c664a4841p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.9059c664a4840p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/csv.py",
        "content_identity": "d9ddfd29e02486d5f88d36ee9f7e88f466eaa068fc22b2513afb907018717a90",
        "document_identity": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.83f90a80d5463p+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.83f90a80d5464p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.6fd8ac94c1d1dp+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.6fd8ac94c1d1dp+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.6c2cce8998f9bp+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.6c2cce8998f9bp+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.42754630b33f1p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.42754630b33f0p+4"
        },
        "address": "src/devtools/resources/filesystem/models/json/__init__.py",
        "content_identity": "d8a21f64b411c028266d7a1ca352772f32418f839c548d3acf266d0bef827c47",
        "document_identity": "068a54d62c733dbf951842f4b6ee7f655dc5ba5332ae0dc9aa8bcfd124dc4f47",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.3fdf688cc9fc7p+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.3fdf688cc9fc8p+4"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.1135c70c2a134p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.1135c70c2a134p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.102a4162344c0p+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.102a4162344c0p+4"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
      "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "068a54d62c733dbf951842f4b6ee7f655dc5ba5332ae0dc9aa8bcfd124dc4f47",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.9f0dbfcf305c5p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.66b78c80ef727p+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.513290bcf8062p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.41976a8e4bb95p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.41976a8e4bb94p+5"
        },
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
        "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.3839d329b8281p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.3839d329b8280p+5"
        },
        "address": "src/devtools/resources/filesystem/models/__init__.py",
        "content_identity": "e09ae5eeb0da9afd9f4921634debfd2af6e9fbcf84a98450526c62f52e5fcf5c",
        "document_identity": "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.382b25943bc2ep+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.382b25943bc2dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.26a00ea29b338p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.26a00ea29b337p+5"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-47"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f8c731d6102cep+4"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.de44cca0aff89p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.de44cca0aff88p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
        "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.db19e96ad238ap+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
        "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.9bbc3e2a20257p+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.9bbc3e2a20258p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
        "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.93728e931e170p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.93728e931e16fp+4"
        },
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.9059c664a4841p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.9059c664a4840p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/csv.py",
        "content_identity": "d9ddfd29e02486d5f88d36ee9f7e88f466eaa068fc22b2513afb907018717a90",
        "document_identity": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.83f90a80d5463p+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.83f90a80d5464p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.6fd8ac94c1d1dp+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.6fd8ac94c1d1dp+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.6c2cce8998f9bp+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.6c2cce8998f9bp+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.42754630b33f1p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.42754630b33f0p+4"
        },
        "address": "src/devtools/resources/filesystem/models/json/__init__.py",
        "content_identity": "d8a21f64b411c028266d7a1ca352772f32418f839c548d3acf266d0bef827c47",
        "document_identity": "068a54d62c733dbf951842f4b6ee7f655dc5ba5332ae0dc9aa8bcfd124dc4f47",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.3fdf688cc9fc7p+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.3fdf688cc9fc8p+4"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.1135c70c2a134p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.1135c70c2a134p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.102a4162344c0p+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.102a4162344c0p+4"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.0fd3bb3d170b4p+4"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.0fd3bb3d170b4p+4"
        },
        "address": "tests/resources/filesystem/test_json_conversion.py",
        "content_identity": "9757259e385ae2a84440d34809686a6dbb7854b2f475bded7f409f81c87278ce",
        "document_identity": "24c1c20e2050fede03130cb6549cda56dac3e7b786f39434e1c450e4cd81f782",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.0e56dcdd76780p+4"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.0e56dcdd76780p+4"
        },
        "address": "tests/resources/filesystem/test_json_models.py",
        "content_identity": "7c29e52ea97ad5929477d5e835913bb6fa1852f7f5ed9d1b2fe12085257c598f",
        "document_identity": "7bda444036f7fd3bc32bb0de25b31fb30c3418cf1a5579ced9aabd2b1afd033e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.0b7992322e703p+4"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.0b7992322e704p+4"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.e9c2899933840p+3"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.e9c2899933841p+3"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.a5381887ababap+3"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.a5381887ababbp+3"
        },
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
        "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.9f6c58191af66p+3"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.9f6c58191af66p+3"
        },
        "address": "src/devtools/resources/filesystem/models/markdown/file.py",
        "content_identity": "3be01d5cb97e24f38004f176980c510a17abf2ef420a1c312ea8664f138fa76b",
        "document_identity": "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.97c563b5d1c68p+3"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.97c563b5d1c68p+3"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.96755986f9c13p+3"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.96755986f9c12p+3"
        },
        "address": "tests/resources/filesystem/models/markdown/test_file.py",
        "content_identity": "4baafbfb0b8ed4829bb5ae9d6243ccf0a739f4560187bc3ed64938d4ceb3d5d0",
        "document_identity": "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.9050af1754c88p+3"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.9050af1754c88p+3"
        },
        "address": "tests/context/retrieval/lexical/_helpers.py",
        "content_identity": "02036f53e34933d806415512b4e66bf886c2a6722f4c8fcd589031eda44bb3da",
        "document_identity": "291e32778314ee2c1c0212fc04b7732de2dd5b24ad64fe69116954c05082f97f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.8deb7adc36f7bp+3"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.8deb7adc36f7bp+3"
        },
        "address": "src/devtools/core/conversion/docs/overview.md",
        "content_identity": "7068d7046cc793f13cf7e3ca039b2e5a1cfe7f2cac16e8441776a3b2d54a1c60",
        "document_identity": "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.8dc5d997ceaf4p+3"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.8dc5d997ceaf4p+3"
        },
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.8c8d21c0b1f5ep+3"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.8c8d21c0b1f5ep+3"
        },
        "address": "src/devtools/resources/filesystem/docs/csv.md",
        "content_identity": "dc61f29ab6a82f2dde97fc7e965cfdbd52812327e2adcc6e4614009b59007be7",
        "document_identity": "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.7232120585270p+3"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.7232120585270p+3"
        },
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.6684f8b902b35p+3"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.6684f8b902b35p+3"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.5ebbbbe42f0fap+3"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.5ebbbbe42f0f9p+3"
        },
        "address": "src/devtools/context/python/function/materialization.py",
        "content_identity": "d914b5e736e7cf1e2d6af3762c6348c6a98882aa69b4fd96b65aca0833ba17a5",
        "document_identity": "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.43f93e3b05c29p+3"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.43f93e3b05c2ap+3"
        },
        "address": "src/devtools/resources/filesystem/models/csv.py",
        "content_identity": "0cade3699fe596ba492a6509405496cba9b3e2b616d8c0de6f19b47ca0ba9d40",
        "document_identity": "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.41eefa6d8c34cp+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.41eefa6d8c34cp+3"
        },
        "address": "src/devtools/context/repository/resource.py",
        "content_identity": "a1d3fbdcff843b2a2b672307a4b204bf4d4ea8fca96b2cf2cfc0533b28e1421c",
        "document_identity": "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.3832a1f178221p+3"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.3832a1f178220p+3"
        },
        "address": "src/devtools/models/benchmarks/storage.py",
        "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
        "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.3126bfe7bc640p+3"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.3126bfe7bc640p+3"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.28f539c1c9731p+3"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.28f539c1c9731p+3"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.231fc032eed2ep+3"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.231fc032eed2dp+3"
        },
        "address": "tests/models/benchmarks/test_storage.py",
        "content_identity": "a9fcf22fcb76814c755cbcba819c0e8947c082f772b5a7cc9bd0c6c6f6ef8a66",
        "document_identity": "b79f92c5457d7e56bba959136c47edf1ca116bab0410b960053a0925f2e4b729",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.1bdfb4cc784d5p+3"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.1bdfb4cc784d6p+3"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.1aff86bafe094p+3"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.1aff86bafe094p+3"
        },
        "address": "src/devtools/agents/integrations/codex/parsing.py",
        "content_identity": "be4f337ef1023dabca12dbd38dcb842b9cfc51cbabada50fb9584924b7a7266d",
        "document_identity": "6627e5a644caabf5fee34e83698162d31cc43acc79fa25968b54bfd7956638ff",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.17ca85fa9214bp+3"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.17ca85fa9214cp+3"
        },
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.147ad335fc343p+3"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.147ad335fc342p+3"
        },
        "address": "tests/context/python/imports/test_declarations.py",
        "content_identity": "a10f487e0b5593f434e70281175a0f9da22fbd0a2cd4129e1b1281597678d441",
        "document_identity": "7a37f0ca8303a2bd08ba9335b3a916836524ea81d6a439ce8d27a412b723ce12",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.13306d39e318dp+3"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.13306d39e318fp+3"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.0ebba39b69b34p+3"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.0ebba39b69b34p+3"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.08e903ef5bbc0p+3"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.08e903ef5bbc0p+3"
        },
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
        "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.0794fd0e8c4fcp+3"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.0794fd0e8c4fdp+3"
        },
        "address": "tests/context/python/imports/test_relations.py",
        "content_identity": "3073e4d26786060a5ff2d9376dfab54804dbea13146850f9a7e22065e330eb88",
        "document_identity": "552a6527d863b5cbfef8f7abb6cbadeb6e6113c7ae5820d65e47b80e2e6bcc43",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.050fe9af481c4p+3"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.050fe9af481c4p+3"
        },
        "address": "tests/context/python/function/test_declarations.py",
        "content_identity": "9b90a073bec97217be0312199d82de5d5aab94ccb2666b7de5cd5bda78688e50",
        "document_identity": "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "627f10061190df2438ba7c63973f307b5591e4c08e600b08f91c228530f54121",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
      "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "068a54d62c733dbf951842f4b6ee7f655dc5ba5332ae0dc9aa8bcfd124dc4f47",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "24c1c20e2050fede03130cb6549cda56dac3e7b786f39434e1c450e4cd81f782",
      "7bda444036f7fd3bc32bb0de25b31fb30c3418cf1a5579ced9aabd2b1afd033e",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
      "c176a151b370e412a92215a094b4311b90014509e96ddf661a89dc88ff5b12db",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
      "291e32778314ee2c1c0212fc04b7732de2dd5b24ad64fe69116954c05082f97f",
      "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
      "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
      "b967dfb98a18c252e516276046e97714cb57f4386796a6ddb4e5fe2e79e0b9bc",
      "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "0ee97c99b5a9a8df7d8e6d168be9145f3fe3315cb1cbdf5bd0f5cfdbaec245c5",
      "a7d7bf5592ead7b06fb8083307cb10ed98e771715a2436fbdb5f1dbcc4c51b2c",
      "216cce289f3fd9be8e9934580dac009863354bbc83a3763a85dedb5accce300f",
      "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "b79f92c5457d7e56bba959136c47edf1ca116bab0410b960053a0925f2e4b729",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "6627e5a644caabf5fee34e83698162d31cc43acc79fa25968b54bfd7956638ff",
      "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
      "7a37f0ca8303a2bd08ba9335b3a916836524ea81d6a439ce8d27a412b723ce12",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "552a6527d863b5cbfef8f7abb6cbadeb6e6113c7ae5820d65e47b80e2e6bcc43",
      "a994332cda61e4b429e5a232589925f51304e14bb461c5f01b1122e8655709e6"
    ]
  }
}
```


## Q4: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/__init__.py | 1 | 1 | 0x1.a5d8cbc4525f4p+5 | 0x1.a5d8cbc4525f4p+5 | 0 |
| src/devtools/resources/filesystem/reading.py | 2 | 2 | 0x1.9547372ed5069p+5 | 0x1.88e321e9fbcfep+5 | 0 |
| src/devtools/resources/filesystem/docs/overview.md | 3 | 3 | 0x1.75028cf16f161p+5 | 0x1.75028cf16f161p+5 | 0 |
| tests/resources/filesystem/test_reading.py | 4 | 4 | 0x1.48599830051bap+5 | 0x1.48599830051bap+5 | 0 |
| src/devtools/resources/filesystem/docs/io.md | 5 | 5 | 0x1.370c89e64880dp+5 | 0x1.370c89e64880dp+5 | 0 |
| src/devtools/resources/filesystem/errors.py | 6 | 6 | 0x1.19b08d30f40d1p+5 | 0x1.19b08d30f40d1p+5 | 0 |
| src/devtools/tools/filesystem.py | 7 | 7 | 0x1.0b1ccb7453054p+5 | 0x1.fbaed6724331bp+4 | 0 |
| src/devtools/resources/filesystem/writing.py | 8 | 8 | 0x1.f88b809109bd4p+4 | 0x1.f88b809109bd4p+4 | 0 |
| tests/resources/filesystem/test_writing.py | 9 | 9 | 0x1.e38c73e2590b9p+4 | 0x1.e38c73e2590bap+4 | 0 |
| tests/tools/test_filesystem.py | 10 | 10 | 0x1.c771a68dcf414p+4 | 0x1.c771a68dcf414p+4 | 0 |
| tests/context/repository/test_observation.py | 11 | 11 | 0x1.4f0a5958f84dbp+4 | 0x1.4f0a5958f84dap+4 | 0 |
| src/devtools/resources/filesystem/docs/roadmap.md | 12 | 12 | 0x1.459b3525b6420p+4 | 0x1.459b3525b6420p+4 | 0 |
| src/devtools/tools/docs/overview.md | 13 | 13 | 0x1.205babf0aaa99p+4 | 0x1.205babf0aaa99p+4 | 0 |
| src/devtools/models/benchmarks/runner.py | 14 | 14 | 0x1.1552a6d2cca4bp+4 | 0x1.1552a6d2cca4bp+4 | 0 |
| AGENTS.md | 15 | 15 | 0x1.efb6c18bff231p+3 | 0x1.efb6c18bff230p+3 | 0 |
| src/devtools/resources/commands/execution.py | 16 | 16 | 0x1.c447632b03bffp+3 | 0x1.c447632b03bfdp+3 | 0 |
| tests/models/interaction/providers/test_llama_cpp.py | 17 | 17 | 0x1.bc49f6f099cb3p+3 | 0x1.bc49f6f099cb2p+3 | 0 |
| src/devtools/resources/filesystem/docs/codecs.md | 18 | 18 | 0x1.b65c8a3ca2fc3p+3 | 0x1.b65c8a3ca2fc3p+3 | 0 |
| src/devtools/context/repository/observation.py | 19 | 19 | 0x1.b28d05b8e4f66p+3 | 0x1.b28d05b8e4f66p+3 | 0 |
| src/devtools/models/interaction/providers/llama_cpp.py | 20 | 20 | 0x1.af5742c878c24p+3 | 0x1.af5742c878c25p+3 | 0 |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 21 | 21 | 0x1.a35aa3e3cdaccp+3 | 0x1.a35aa3e3cdacbp+3 | 0 |
| tests/models/benchmarks/test_runner.py | 22 | 22 | 0x1.a1fdf15fcd9dbp+3 | 0x1.a1fdf15fcd9dcp+3 | 0 |
| tests/tools/test_command.py | 23 | 23 | 0x1.a0395da966a9cp+3 | 0x1.a0395da966a9ep+3 | 0 |
| tests/resources/commands/test_execution.py | 24 | 24 | 0x1.95609ee7d931dp+3 | 0x1.95609ee7d931cp+3 | 0 |
| tests/tools/test_runtime_integration.py | 25 | 25 | 0x1.8a6db7200788ap+3 | 0x1.8a6db7200788ap+3 | 0 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 26 | 26 | 0x1.857813b39eef4p+3 | 0x1.857813b39eef3p+3 | 0 |
| src/devtools/models/benchmarks/docs/overview.md | 27 | 27 | 0x1.8062eead86b34p+3 | 0x1.8062eead86b33p+3 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 28 | 28 | 0x1.7ecb0646007f9p+3 | 0x1.7ecb0646007fap+3 | 0 |
| src/devtools/resources/filesystem/resolution.py | 29 | 29 | 0x1.7e1b7c43ea791p+3 | 0x1.7e1b7c43ea792p+3 | 0 |
| tests/resources/filesystem/test_resolution.py | 30 | 30 | 0x1.6fea4a32c3b70p+3 | 0x1.6fea4a32c3b70p+3 | 0 |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 31 | 31 | 0x1.5514265d61246p+3 | 0x1.5514265d61246p+3 | 0 |
| src/devtools/resources/filesystem/codecs/csv.py | 32 | 32 | 0x1.5032d281469d5p+3 | 0x1.5032d281469d4p+3 | 0 |
| src/devtools/resources/filesystem/codecs/json.py | 33 | 33 | 0x1.4e412556358cbp+3 | 0x1.4e412556358cbp+3 | 0 |
| docs/backlog/epics/B-0005-effect-governance.md | 34 | 34 | 0x1.4db20340a726ep+3 | 0x1.4db20340a726cp+3 | 0 |
| src/devtools/core/paths/docs/overview.md | 35 | 35 | 0x1.4a18e632a2d1cp+3 | 0x1.4a18e632a2d1cp+3 | 0 |
| src/devtools/context/repository/discovery.py | 36 | 36 | 0x1.42101b7b9c0b5p+3 | 0x1.42101b7b9c0b4p+3 | 0 |
| tests/resources/commands/test_handle.py | 37 | 37 | 0x1.4011e7e37ea6cp+3 | 0x1.4011e7e37ea6cp+3 | 0 |
| docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md | 38 | 38 | 0x1.2d51b1e90bffdp+3 | 0x1.2d51b1e90bffcp+3 | 0 |
| tests/resources/filesystem/codecs/test_json.py | 39 | 39 | 0x1.251fbf02e4932p+3 | 0x1.251fbf02e4932p+3 | 0 |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 40 | 46 | 0x1.1eccbac5a9f47p+3 | 0x1.0c127ade9d24ep+3 | -6 |
| src/devtools/resources/commands/docs/events.md | 41 | 40 | 0x1.195d7afd0b8ffp+3 | 0x1.195d7afd0b900p+3 | 1 |
| tests/agents/integrations/codex/test_live.py | 42 | 41 | 0x1.18bc2b763e677p+3 | 0x1.18bc2b763e677p+3 | 1 |
| src/devtools/observability/evidence/docs/overview.md | 43 | 42 | 0x1.113130b6ca921p+3 | 0x1.113130b6ca921p+3 | 1 |
| docs/backlog/items/B-0012-investigate-governed-effect-semantics.md | 44 | 43 | 0x1.0da492b205c43p+3 | 0x1.0da492b205c43p+3 | 1 |
| src/devtools/resources/filesystem/docs/markdown.md | 45 | 44 | 0x1.0d3b5202e3ca7p+3 | 0x1.0d3b5202e3ca7p+3 | 1 |
| tests/resources/filesystem/models/markdown/test_file.py | 46 | 45 | 0x1.0d3abe43cbc69p+3 | 0x1.0d3abe43cbc69p+3 | 1 |
| tests/resources/filesystem/codecs/test_csv.py | 47 | 47 | 0x1.0699047401a1ep+3 | 0x1.0699047401a1ep+3 | 0 |
| tests/agents/conversation/test_live.py | 48 | 48 | 0x1.015ee72148199p+3 | 0x1.015ee72148198p+3 | 0 |
| src/devtools/models/benchmarks/storage.py | 49 | 49 | 0x1.0100cb1caff92p+3 | 0x1.0100cb1caff92p+3 | 0 |
| tests/models/interaction/test_tools.py | 50 | 50 | 0x1.e8ee89c1179e6p+2 | 0x1.e8ee89c1179e5p+2 | 0 |
| src/devtools/agents/integrations/codex/docs/cli.md | 51 | 51 | 0x1.d37a11b903050p+2 | 0x1.d37a11b903050p+2 | 0 |
| docs/backlog/epics/B-0003-local-coding-worker-harness.md | 52 | 52 | 0x1.ba743471f2434p+2 | 0x1.ba743471f2432p+2 | 0 |
| src/devtools/context/planning/resource.py | 53 | 53 | 0x1.a0dec64454f14p+2 | 0x1.a0dec64454f12p+2 | 0 |
| tests/core/paths/test_resolution.py | 54 | 54 | 0x1.91da01ac99bb2p+2 | 0x1.91da01ac99bb2p+2 | 0 |
| src/devtools/core/paths/resolution.py | 55 | 55 | 0x1.8fe6a4c53e618p+2 | 0x1.8fe6a4c53e618p+2 | 0 |
| src/devtools/context/python/docs/overview.md | 56 | 56 | 0x1.8cf563c8a3f1ep+2 | 0x1.8cf563c8a3f1ep+2 | 0 |
| src/devtools/resources/filesystem/docs/json.md | 57 | 57 | 0x1.88a0efb5d394ap+2 | 0x1.88a0efb5d394ap+2 | 0 |
| src/devtools/resources/commands/docs/execution.md | 58 | 58 | 0x1.88446cd4b86dcp+2 | 0x1.88446cd4b86dcp+2 | 0 |
| docs/backlog/items/B-0013-investigate-authority-grants-approval.md | 59 | 59 | 0x1.849a081cf4e16p+2 | 0x1.849a081cf4e18p+2 | 0 |
| src/devtools/models/interaction/docs/overview.md | 60 | 60 | 0x1.83fce4a7884c5p+2 | 0x1.83fce4a7884c4p+2 | 0 |
| src/devtools/resources/filesystem/models/binary.py | 61 | 61 | 0x1.804c98ca85a9bp+2 | 0x1.804c98ca85a9ap+2 | 0 |
| src/devtools/resources/filesystem/docs/csv.md | 62 | 62 | 0x1.7d5a420a42c02p+2 | 0x1.7d5a420a42c02p+2 | 0 |
| src/devtools/resources/commands/handle.py | 63 | 63 | 0x1.737dc0142448ep+2 | 0x1.737dc0142448ep+2 | 0 |
| src/devtools/resources/filesystem/models/base.py | 64 | 64 | 0x1.71528823dbc28p+2 | 0x1.71528823dbc28p+2 | 0 |
| tests/context/retrieval/graph/test_ranking.py | 65 | 65 | 0x1.6b14e68ce949bp+2 | 0x1.6b14e68ce949bp+2 | 0 |
| tests/context/python/function/test_cross_resource_pipeline.py | 66 | 66 | 0x1.6879dc179a983p+2 | 0x1.6879dc179a982p+2 | 0 |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 67 | 67 | 0x1.67dd189801bfep+2 | 0x1.67dd189801bfdp+2 | 0 |
| tests/context/python/project_configuration/test_configuration.py | 68 | 68 | 0x1.677a14e5826f3p+2 | 0x1.677a14e5826f3p+2 | 0 |
| tests/scripts/qwen/test_two_read_acceptance.py | 69 | 69 | 0x1.611b83c09a4ebp+2 | 0x1.611b83c09a4ebp+2 | 0 |
| src/devtools/core/paths/docs/resolution.md | 70 | 70 | 0x1.56872f38a9512p+2 | 0x1.56872f38a9511p+2 | 0 |
| src/devtools/resources/filesystem/codecs/text.py | 71 | 71 | 0x1.4a5fdf7aced76p+2 | 0x1.4a5fdf7aced76p+2 | 0 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 72 | 72 | 0x1.481d9f1b30804p+2 | 0x1.481d9f1b30804p+2 | 0 |
| src/devtools/resources/filesystem/codecs/markdown.py | 73 | 73 | 0x1.43ebee29ba9f2p+2 | 0x1.43ebee29ba9f1p+2 | 0 |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 74 | 74 | 0x1.42aaec4d62942p+2 | 0x1.42aaec4d62941p+2 | 0 |
| tests/context/python/function/test_resource_selection.py | 75 | 75 | 0x1.3eeeb55c53fe7p+2 | 0x1.3eeeb55c53fe8p+2 | 0 |
| tests/context/localization/roles/helpers.py | 76 | 76 | 0x1.37adcc9f42becp+2 | 0x1.37adcc9f42becp+2 | 0 |
| tests/context/retrieval/lexical/test_analysis.py | 77 | 77 | 0x1.326d3e2bd83a6p+2 | 0x1.326d3e2bd83a5p+2 | 0 |
| tests/resources/filesystem/codecs/test_markdown.py | 78 | 78 | 0x1.31cc634f7dea8p+2 | 0x1.31cc634f7dea8p+2 | 0 |
| tests/resources/filesystem/test_models.py | 79 | 79 | 0x1.3148850f234acp+2 | 0x1.3148850f234acp+2 | 0 |
| src/devtools/agents/integrations/codex/agent.py | 80 | 80 | 0x1.2d8a385019898p+2 | 0x1.2d8a385019898p+2 | 0 |
| tests/context/python/function/test_materialization.py | 81 | 81 | 0x1.2cdcbf555a4a0p+2 | 0x1.2cdcbf555a49ep+2 | 0 |
| docs/backlog/items/B-0039-investigate-delegated-authority.md | 82 | 82 | 0x1.298a2388a8d91p+2 | 0x1.298a2388a8d91p+2 | 0 |
| docs/backlog/items/B-0024-investigate-audit-durable-accountability.md | 83 | 83 | 0x1.2861b82dcb4c4p+2 | 0x1.2861b82dcb4c4p+2 | 0 |
| src/devtools/resources/filesystem/models/json/object.py | 84 | 84 | 0x1.2634fd30cfb87p+2 | 0x1.2634fd30cfb86p+2 | 0 |
| src/devtools/persistence/docs/overview.md | 85 | 85 | 0x1.2617bf9aef4d2p+2 | 0x1.2617bf9aef4d3p+2 | 0 |
| tests/tools/test_execution.py | 86 | 86 | 0x1.20350a73fd4eap+2 | 0x1.20350a73fd4eap+2 | 0 |
| src/devtools/tools/execution.py | 87 | 87 | 0x1.1e7d23fa07853p+2 | 0x1.1e7d23fa07853p+2 | 0 |
| tests/context/python/function/test_candidates.py | 88 | 88 | 0x1.1e2bbb2dd2e14p+2 | 0x1.1e2bbb2dd2e15p+2 | 0 |
| tests/models/serving/test_llama_cpp.py | 89 | 89 | 0x1.1b7e80620349dp+2 | 0x1.1b7e80620349cp+2 | 0 |
| pyproject.toml | 90 | 90 | 0x1.1a85aee852761p+2 | 0x1.1a85aee852762p+2 | 0 |
| tests/context/python/test_source_candidacy.py | 91 | 91 | 0x1.1a367958c2b83p+2 | 0x1.1a367958c2b83p+2 | 0 |
| tests/context/repository/test_discovery.py | 92 | 92 | 0x1.16d66243bf919p+2 | 0x1.16d66243bf919p+2 | 0 |
| src/devtools/tools/disclosure.py | 93 | 93 | 0x1.169f30ac9f788p+2 | 0x1.169f30ac9f789p+2 | 0 |
| src/devtools/tools/protocols.py | 94 | 94 | 0x1.13fe40380957dp+2 | 0x1.13fe40380957ep+2 | 0 |
| src/devtools/models/interaction/tools.py | 95 | 95 | 0x1.0c8789933bea9p+2 | 0x1.0c8789933beaap+2 | 0 |
| src/devtools/tools/__init__.py | 96 | 96 | 0x1.0c2ce22eff803p+2 | 0x1.0c2ce22eff802p+2 | 0 |
| tests/context/python/project_configuration/test_settings.py | 97 | 97 | 0x1.0a1c300107c2cp+2 | 0x1.0a1c300107c2cp+2 | 0 |
| tests/resources/filesystem/test_json_conversion.py | 98 | 98 | 0x1.082e691a7f295p+2 | 0x1.082e691a7f295p+2 | 0 |
| src/devtools/context/python/project_configuration/settings.py | 99 | 99 | 0x1.043709de0f8fdp+2 | 0x1.043709de0f8fcp+2 | 0 |
| src/devtools/tools/errors.py | 100 | 100 | 0x1.01f375b526279p+2 | 0x1.01f375b526279p+2 | 0 |
| tests/context/localization/roles/test_configuration.py | 101 | 101 | 0x1.fb1b9fd49da3cp+1 | 0x1.fb1b9fd49da3cp+1 | 0 |
| src/devtools/observability/evidence/model_interaction.py | 102 | 102 | 0x1.f9c71095d0d8dp+1 | 0x1.f9c71095d0d8cp+1 | 0 |
| tests/resources/filesystem/test_json_models.py | 103 | 103 | 0x1.f98855b24f388p+1 | 0x1.f98855b24f388p+1 | 0 |
| docs/backlog/overview.md | 104 | 104 | 0x1.f678cd491566cp+1 | 0x1.f678cd491566cp+1 | 0 |
| src/devtools/context/python/project_configuration/models.py | 105 | 105 | 0x1.f5d80f2064644p+1 | 0x1.f5d80f2064643p+1 | 0 |
| docs/backlog/items/B-0036-investigate-action-request-semantics.md | 106 | 106 | 0x1.f54d0e2833fe0p+1 | 0x1.f54d0e2833fe0p+1 | 0 |
| tests/resources/filesystem/codecs/test_text.py | 107 | 107 | 0x1.ecd4e0cb0d53ap+1 | 0x1.ecd4e0cb0d53cp+1 | 0 |
| src/devtools/context/python/project_configuration/resolution.py | 108 | 108 | 0x1.e57d81adbfc23p+1 | 0x1.e57d81adbfc23p+1 | 0 |
| src/devtools/models/interaction/models.py | 109 | 109 | 0x1.dff64ddc02fefp+1 | 0x1.dff64ddc02fefp+1 | 0 |
| src/devtools/context/python/mirrored_paths.py | 110 | 110 | 0x1.ddf44aab78668p+1 | 0x1.ddf44aab78668p+1 | 0 |
| src/devtools/tools/command.py | 111 | 111 | 0x1.db4d2f4df5414p+1 | 0x1.db4d2f4df5414p+1 | 0 |
| src/devtools/resources/filesystem/models/__init__.py | 112 | 112 | 0x1.d7ae3f0ee9319p+1 | 0x1.d7ae3f0ee931ap+1 | 0 |
| src/devtools/resources/filesystem/models/json/__init__.py | 113 | 113 | 0x1.d607c8f1d1a8ep+1 | 0x1.d607c8f1d1a8ep+1 | 0 |
| src/devtools/resources/filesystem/codecs/__init__.py | 114 | 114 | 0x1.d33e37ea7df21p+1 | 0x1.d33e37ea7df21p+1 | 0 |
| src/devtools/context/repository/corpus.py | 115 | 115 | 0x1.d22ab12fe943dp+1 | 0x1.d22ab12fe943fp+1 | 0 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 116 | 116 | 0x1.d0adfb519ad8ap+1 | 0x1.d0adfb519ad8ap+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 117 | 117 | 0x1.cc4c9ea327d33p+1 | 0x1.cc4c9ea327d33p+1 | 0 |
| src/devtools/__init__.py | 118 | 118 | 0x1.cb989b5db8db1p+1 | 0x1.cb989b5db8db3p+1 | 0 |
| tests/tools/__init__.py | 119 | 119 | 0x1.caee501477be7p+1 | 0x1.caee501477be8p+1 | 0 |
| tests/context/python/function/test_retrieval.py | 120 | 120 | 0x1.c4fae8851e608p+1 | 0x1.c4fae8851e606p+1 | 0 |
| src/devtools/core/paths/models.py | 121 | 121 | 0x1.c4ab0a962e9dep+1 | 0x1.c4ab0a962e9dfp+1 | 0 |
| tests/context/python/function/test_disclosure.py | 122 | 122 | 0x1.c29bb8914dedap+1 | 0x1.c29bb8914dedap+1 | 0 |
| tests/resources/filesystem/models/csv/test_file.py | 123 | 123 | 0x1.b6680b3386d52p+1 | 0x1.b6680b3386d52p+1 | 0 |
| tests/observability/evidence/test_model_interaction.py | 124 | 124 | 0x1.b0189d1b96ce0p+1 | 0x1.b0189d1b96ce2p+1 | 0 |
| tests/agents/integrations/codex/test_agent.py | 125 | 125 | 0x1.afa4a24602df4p+1 | 0x1.afa4a24602df3p+1 | 0 |
| src/devtools/resources/filesystem/models/json/base.py | 126 | 126 | 0x1.a82c62142eea2p+1 | 0x1.a82c62142eea2p+1 | 0 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 127 | 127 | 0x1.a459a04a51368p+1 | 0x1.a459a04a51369p+1 | 0 |
| tests/context/retrieval/repository_map/test_ranking.py | 128 | 128 | 0x1.a1e65df5c81ebp+1 | 0x1.a1e65df5c81ecp+1 | 0 |
| src/devtools/models/serving/llama_cpp.py | 129 | 129 | 0x1.a1bfe9439e780p+1 | 0x1.a1bfe9439e781p+1 | 0 |
| tests/context/localization/roles/test_inputs.py | 130 | 130 | 0x1.a1b27ed223ec0p+1 | 0x1.a1b27ed223ec1p+1 | 0 |
| src/devtools/context/localization/roles/configuration.py | 131 | 131 | 0x1.9bdf79bf07d54p+1 | 0x1.9bdf79bf07d54p+1 | 0 |
| docs/backlog/items/B-0041-investigate-execution-local-lifecycle-control.md | 132 | 132 | 0x1.9a3dc49854c45p+1 | 0x1.9a3dc49854c45p+1 | 0 |
| src/devtools/context/localization/roles/models.py | 133 | 133 | 0x1.97fc8f396c1a1p+1 | 0x1.97fc8f396c1a0p+1 | 0 |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 134 | 134 | 0x1.973adac16ce84p+1 | 0x1.973adac16ce84p+1 | 0 |
| src/devtools/resources/filesystem/models/json/scalar.py | 135 | 135 | 0x1.912382cc20eafp+1 | 0x1.912382cc20eaep+1 | 0 |
| tests/context/python/function/test_request_assembly.py | 136 | 136 | 0x1.8e735c12c3caap+1 | 0x1.8e735c12c3caap+1 | 0 |
| tests/context/python/function/test_rendering.py | 137 | 137 | 0x1.8bb3d5ecb44fcp+1 | 0x1.8bb3d5ecb44fcp+1 | 0 |
| src/devtools/agents/conversation/docs/overview.md | 138 | 138 | 0x1.8b67c2caceb74p+1 | 0x1.8b67c2caceb74p+1 | 0 |
| tests/context/repository/test_corpus.py | 139 | 139 | 0x1.8b2e61447d21ep+1 | 0x1.8b2e61447d21ep+1 | 0 |
| tests/scripts/test_retrieval_bm25_baseline.py | 140 | 140 | 0x1.8a7e1fff07196p+1 | 0x1.8a7e1fff07196p+1 | 0 |
| docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md | 141 | 141 | 0x1.877fe6518994bp+1 | 0x1.877fe6518994bp+1 | 0 |
| src/devtools/core/paths/__init__.py | 142 | 142 | 0x1.8686e7fb0f635p+1 | 0x1.8686e7fb0f635p+1 | 0 |
| tests/context/python/function/test_declaration_aggregation.py | 143 | 143 | 0x1.80cab7587d40ep+1 | 0x1.80cab7587d40cp+1 | 0 |
| tests/resources/filesystem/__init__.py | 144 | 144 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/codecs/__init__.py | 145 | 145 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/__init__.py | 146 | 146 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/markdown/__init__.py | 147 | 147 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | 0 |
| tests/resources/filesystem/models/csv/__init__.py | 148 | 148 | 0x1.7dd5af5050b5bp+1 | 0x1.7dd5af5050b5dp+1 | 0 |
| src/devtools/models/interaction/response.py | 149 | 149 | 0x1.7cb04a04a0710p+1 | 0x1.7cb04a04a070ep+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 150 | 150 | 0x1.78c480c4f3a2bp+1 | 0x1.78c480c4f3a2dp+1 | 0 |
| src/devtools/execution/docs/overview.md | 151 | 151 | 0x1.72e45b1aec709p+1 | 0x1.72e45b1aec708p+1 | 0 |
| src/devtools/models/serving/vllm.py | 152 | 152 | 0x1.6f70f3a46bb55p+1 | 0x1.6f70f3a46bb54p+1 | 0 |
| docs/backlog/items/B-0007-correct-model-serving-documentation-drift.md | 153 | 153 | 0x1.6df4c43935589p+1 | 0x1.6df4c4393558ap+1 | 0 |
| docs/backlog/items/B-0044-investigate-orchestration-control-loops.md | 154 | 154 | 0x1.6df4c43935589p+1 | 0x1.6df4c4393558ap+1 | 0 |
| tests/models/benchmarks/test_storage.py | 155 | 155 | 0x1.6c4e0a3388cdap+1 | 0x1.6c4e0a3388cd8p+1 | 0 |
| tests/context/repository/test_document.py | 156 | 156 | 0x1.6b2477a83f66cp+1 | 0x1.6b2477a83f66ap+1 | 0 |
| src/devtools/persistence/docs/json.md | 157 | 157 | 0x1.60c5d25373901p+1 | 0x1.60c5d25373901p+1 | 0 |
| tests/core/paths/test_resolved_path.py | 158 | 158 | 0x1.5c7e450632159p+1 | 0x1.5c7e450632157p+1 | 0 |
| src/devtools/resources/filesystem/models/json/list.py | 159 | 159 | 0x1.59dfac7d6bdfap+1 | 0x1.59dfac7d6bdfap+1 | 0 |
| src/devtools/resources/filesystem/models/text.py | 160 | 160 | 0x1.57817baa2de89p+1 | 0x1.57817baa2de89p+1 | 0 |
| src/devtools/core/regex/docs/overview.md | 161 | 161 | 0x1.4a07fe56fba4fp+1 | 0x1.4a07fe56fba4ep+1 | 0 |
| src/devtools/core/conversion/docs/overview.md | 162 | 162 | 0x1.46a1878c73203p+1 | 0x1.46a1878c73204p+1 | 0 |
| tests/resources/filesystem/models/markdown/test_heading.py | 163 | 163 | 0x1.4368513d64234p+1 | 0x1.4368513d64234p+1 | 0 |
| tests/context/retrieval/lexical/test_bm25.py | 164 | 164 | 0x1.425662c06168ap+1 | 0x1.425662c061689p+1 | 0 |
| tests/resources/filesystem/models/csv/test_dialect.py | 165 | 165 | 0x1.41d4e5792ad2fp+1 | 0x1.41d4e5792ad2ep+1 | 0 |
| tests/core/paths/test_errors.py | 166 | 166 | 0x1.40197a050333bp+1 | 0x1.40197a050333ap+1 | 0 |
| src/devtools/core/paths/errors.py | 167 | 167 | 0x1.3ec7be766b7e4p+1 | 0x1.3ec7be766b7e5p+1 | 0 |
| src/devtools/resources/filesystem/models/json/conversion.py | 168 | 168 | 0x1.3e576af6c2bffp+1 | 0x1.3e576af6c2bfep+1 | 0 |
| tests/context/localization/generation/test_branching.py | 169 | 169 | 0x1.3c282a907b776p+1 | 0x1.3c282a907b776p+1 | 0 |
| tests/resources/filesystem/models/markdown/test_section.py | 170 | 170 | 0x1.311b3c6b344d3p+1 | 0x1.311b3c6b344d3p+1 | 0 |
| docs/backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md | 171 | 171 | 0x1.2dc831b11dd16p+1 | 0x1.2dc831b11dd15p+1 | 0 |
| README.md | 172 | 172 | 0x1.26f5a35c0abdcp+1 | 0x1.26f5a35c0abdcp+1 | 0 |
| src/devtools/resources/filesystem/docs/models.md | 173 | 173 | 0x1.1d55c24b1ec3dp+1 | 0x1.1d55c24b1ec3ep+1 | 0 |
| tests/resources/filesystem/models/csv/test_row.py | 174 | 174 | 0x1.1b31a9aa01a21p+1 | 0x1.1b31a9aa01a21p+1 | 0 |
| tests/context/repository/test_intrinsic_paths.py | 175 | 175 | 0x1.1a525d422d865p+1 | 0x1.1a525d422d865p+1 | 0 |
| src/devtools/core/system/docs/overview.md | 176 | 176 | 0x1.0cc9b99b6f48ap+1 | 0x1.0cc9b99b6f48bp+1 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 177 | 177 | 0x1.0ae76aedc9aedp+1 | 0x1.0ae76aedc9aeep+1 | 0 |
| tests/context/python/function/test_declarations.py | 178 | 178 | 0x1.0730a51a77d85p+1 | 0x1.0730a51a77d84p+1 | 0 |
| tests/context/retrieval/lexical/_helpers.py | 179 | 179 | 0x1.00b5cbe906c9cp+1 | 0x1.00b5cbe906c9cp+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/section.py | 180 | 180 | 0x1.ff0f00d7b4d51p+0 | 0x1.ff0f00d7b4d51p+0 | 0 |
| src/devtools/resources/commands/docs/overview.md | 181 | 181 | 0x1.f87d83aae6be9p+0 | 0x1.f87d83aae6be9p+0 | 0 |
| tests/context/retrieval/lexical/test_index.py | 182 | 182 | 0x1.e675ca02f114dp+0 | 0x1.e675ca02f114dp+0 | 0 |
| src/devtools/agents/conversation/conversation.py | 183 | 183 | 0x1.deadec703c520p+0 | 0x1.deadec703c520p+0 | 0 |
| src/devtools/context/retrieval/repository_map/relevance.py | 184 | 184 | 0x1.ddfd7da7fc5c2p+0 | 0x1.ddfd7da7fc5c0p+0 | 0 |
| tests/context/localization/roles/test_evidence.py | 185 | 185 | 0x1.b9831424a325ap+0 | 0x1.b9831424a325ap+0 | 0 |
| tests/context/python/imports/test_declarations.py | 186 | 186 | 0x1.b3cc2ada7c1d0p+0 | 0x1.b3cc2ada7c1cep+0 | 0 |
| src/devtools/resources/commands/models/command.py | 187 | 187 | 0x1.a466b19a222bdp+0 | 0x1.a466b19a222bdp+0 | 0 |
| src/devtools/context/retrieval/docs/overview.md | 188 | 188 | 0x1.a2ce6e558a723p+0 | 0x1.a2ce6e558a723p+0 | 0 |
| docs/experiments/qwen38_llama_cpp.md | 189 | 189 | 0x1.a271a276a87b6p+0 | 0x1.a271a276a87b6p+0 | 0 |
| src/devtools/context/python/modules/docs/overview.md | 190 | 190 | 0x1.94be34bb96a75p+0 | 0x1.94be34bb96a75p+0 | 0 |
| src/devtools/context/python/function/docs/overview.md | 191 | 191 | 0x1.947481ae002edp+0 | 0x1.947481ae002edp+0 | 0 |
| tests/resources/commands/test_models.py | 192 | 192 | 0x1.922f457728562p+0 | 0x1.922f457728561p+0 | 0 |
| tests/models/benchmarks/test_models.py | 193 | 193 | 0x1.8caf29f88e163p+0 | 0x1.8caf29f88e164p+0 | 0 |
| src/devtools/models/serving/huggingface.py | 194 | 194 | 0x1.8afefed708069p+0 | 0x1.8afefed708069p+0 | 0 |
| src/devtools/models/serving/docs/overview.md | 195 | 195 | 0x1.7d6568a8ea2f6p+0 | 0x1.7d6568a8ea2f5p+0 | 0 |
| tests/models/serving/test_vllm.py | 196 | 196 | 0x1.74a3aff8acffdp+0 | 0x1.74a3aff8acffbp+0 | 0 |
| tests/context/python/modules/test_interpretation.py | 197 | 197 | 0x1.69be6213c1c6cp+0 | 0x1.69be6213c1c6cp+0 | 0 |
| tests/context/localization/generation/test_imports.py | 198 | 198 | 0x1.68d24c0439e95p+0 | 0x1.68d24c0439e96p+0 | 0 |
| tests/context/retrieval/graph/test_typed.py | 199 | 199 | 0x1.632e61876eda5p+0 | 0x1.632e61876eda6p+0 | 0 |
| src/devtools/context/python/modules/membership.py | 200 | 200 | 0x1.58ebae160978ap+0 | 0x1.58ebae160978bp+0 | 0 |
| tests/context/python/test_mirrored_paths.py | 201 | 201 | 0x1.54828cc2a5d78p+0 | 0x1.54828cc2a5d78p+0 | 0 |
| tests/context/retrieval/lexical/test_evaluation.py | 202 | 202 | 0x1.4e1c6e1da29c3p+0 | 0x1.4e1c6e1da29c2p+0 | 0 |
| tests/context/retrieval/test_structural.py | 203 | 203 | 0x1.3e52553f54765p+0 | 0x1.3e52553f54763p+0 | 0 |
| tests/models/serving/test_huggingface.py | 204 | 204 | 0x1.3d735cc375b8cp+0 | 0x1.3d735cc375b8cp+0 | 0 |
| tests/context/python/function/test_containment.py | 205 | 205 | 0x1.37e74669fb3d7p+0 | 0x1.37e74669fb3d7p+0 | 0 |
| tests/context/python/modules/test_membership.py | 206 | 206 | 0x1.36a69513df73fp+0 | 0x1.36a69513df73ep+0 | 0 |
| tests/agents/conversation/test_session.py | 207 | 207 | 0x1.21af7e80cb110p+0 | 0x1.21af7e80cb110p+0 | 0 |
| src/devtools/persistence/sqlite.py | 208 | 208 | 0x1.1593bde83995fp+0 | 0x1.1593bde83995ep+0 | 0 |
| tests/context/retrieval/test_composition.py | 209 | 209 | 0x1.14bfdd24f9d2ap+0 | 0x1.14bfdd24f9d2ap+0 | 0 |
| tests/context/planning/test_plan.py | 210 | 210 | 0x1.146b774cbaf75p+0 | 0x1.146b774cbaf75p+0 | 0 |
| tests/context/python/imports/test_resolution.py | 211 | 211 | 0x1.028e33d5ff1f0p+0 | 0x1.028e33d5ff1f0p+0 | 0 |
| tests/context/python/classes/test_declarations.py | 212 | 212 | 0x1.cad3e5aa12f86p-1 | 0x1.cad3e5aa12f86p-1 | 0 |
| tests/context/python/imports/test_relations.py | 213 | 213 | 0x1.ca25f5c169656p-1 | 0x1.ca25f5c169656p-1 | 0 |
| tests/scripts/test_vllm_benchmark_driver.py | 214 | 214 | 0x1.bff9ffa0c46ecp-1 | 0x1.bff9ffa0c46edp-1 | 0 |
| tests/persistence/test_sqlite.py | 215 | 215 | 0x1.bb4511c9461f3p-1 | 0x1.bb4511c9461f3p-1 | 0 |
| src/devtools/context/retrieval/graph/view.py | 216 | 216 | 0x1.a9c84039766c9p-1 | 0x1.a9c84039766c9p-1 | 0 |
| tests/context/python/classes/test_bases.py | 217 | 217 | 0x1.a4008b4e9e5a5p-1 | 0x1.a4008b4e9e5a6p-1 | 0 |
| tests/context/python/function/test_qualified_reference.py | 218 | 218 | 0x1.8fea3e1ce5e4dp-1 | 0x1.8fea3e1ce5e4dp-1 | 0 |
| tests/context/python/imports/test_members.py | 219 | 219 | 0x1.88f911f9313ebp-1 | 0x1.88f911f9313ecp-1 | 0 |
| tests/context/python/references/declarations/test_analysis.py | 220 | 220 | 0x1.66cb21670dc38p-1 | 0x1.66cb21670dc38p-1 | 0 |
| tests/scripts/qwen/test_llama_cpp_service.py | 221 | 221 | 0x1.592ee0c05e6d7p-1 | 0x1.592ee0c05e6d5p-1 | 0 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| filesystem | 86 | 1 | 86 | 0x1.c934d423c47f9p+0 | 0x1.75cd12aa84bc2p+2 | 0x1.c934d423c47f9p+0 |
| reading | 10 | 1 | 10 | 0x1.f2868fe376a59p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.f2868fe376a59p+1 |
| filesystemnotfounderror | 9 | 0 | 9 | 0x1.ff5618ca265ddp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.ff5618ca265ddp+1 |
| notafileerror | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| filesystempermissionerror | 11 | 0 | 11 | 0x1.e6e1994d5651ap+1 | 0x1.bc1cbc9538c85p+2 | 0x1.e6e1994d5651ap+1 |
| filetoolargeerror | 6 | 0 | 6 | 0x1.17f49b3bac65cp+2 | 0x1.bc1cbc9538c85p+2 | 0x1.17f49b3bac65cp+2 |
| fileformaterror | 17 | 0 | 17 | 0x1.b123d3f972544p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.b123d3f972544p+1 |
| permission | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| stream | 14 | 0 | 14 | 0x1.c935ec6d91aebp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.c935ec6d91aebp+1 |
| opening | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| chunk | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| read | 75 | 0 | 75 | 0x1.ec067ec6e30c8p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.ec067ec6e30c8p+0 |
| write | 23 | 0 | 23 | 0x1.8b67d63162854p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.8b67d63162854p+1 |
| atomic | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| paths | 107 | 0 | 107 | 0x1.9190d0136ccbep+0 | 0x1.bc1cbc9538c85p+2 | 0x1.9190d0136ccbep+0 |
| tool | 60 | 1 | 60 | 0x1.125d023a8aa72p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.125d023a8aa72p+1 |
| authorization | 23 | 0 | 23 | 0x1.8b67d63162854p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.8b67d63162854p+1 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.9547372ed5069p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.88e321e9fbcfep+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0b1ccb7453054p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.fbaed6724331bp+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8d0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.e38c73e2590b9p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.e38c73e2590bap+4"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 0,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.9547372ed5069p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.88e321e9fbcfep+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0b1ccb7453054p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.fbaed6724331bp+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8d0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.e38c73e2590b9p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.e38c73e2590bap+4"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.4f0a5958f84dbp+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.4f0a5958f84dap+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.459b3525b6420p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.459b3525b6420p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.205babf0aaa99p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.205babf0aaa99p+4"
        },
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.1552a6d2cca4bp+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.1552a6d2cca4bp+4"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.efb6c18bff231p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.efb6c18bff230p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.c447632b03bffp+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.c447632b03bfdp+3"
        },
        "address": "src/devtools/resources/commands/execution.py",
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "document_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.bc49f6f099cb3p+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.bc49f6f099cb2p+3"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.b65c8a3ca2fc3p+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.b65c8a3ca2fc3p+3"
        },
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
        "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.b28d05b8e4f66p+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.b28d05b8e4f66p+3"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.af5742c878c24p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.af5742c878c25p+3"
        },
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 6,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.a5d8cbc4525f4p+5"
        },
        "address": "src/devtools/resources/filesystem/__init__.py",
        "content_identity": "97cb3d29f27274b9c32be47b2e84b3ec51a8f4af978e0c6f022e32544819fa5e",
        "document_identity": "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.9547372ed5069p+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.88e321e9fbcfep+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.8c82a89b26d60p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.75028cf16f161p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.48599830051bap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.370c89e64880dp+5"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.19b08d30f40d1p+5"
        },
        "address": "src/devtools/resources/filesystem/errors.py",
        "content_identity": "bbdcbcaac0bdfec082c4f459b1cd2829b6747c95fc3226e68e5ad9aa00c61caf",
        "document_identity": "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0b1ccb7453054p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.fbaed6724331bp+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8d0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.f88b809109bd4p+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.e38c73e2590b9p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.e38c73e2590bap+4"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.c771a68dcf414p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.4f0a5958f84dbp+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.4f0a5958f84dap+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.459b3525b6420p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.459b3525b6420p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.205babf0aaa99p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.205babf0aaa99p+4"
        },
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.1552a6d2cca4bp+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.1552a6d2cca4bp+4"
        },
        "address": "src/devtools/models/benchmarks/runner.py",
        "content_identity": "f3d508c393972700e34e285252dcfba5a154d358d01fa42e12fae283d7d6a35c",
        "document_identity": "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.efb6c18bff231p+3"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.efb6c18bff230p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.c447632b03bffp+3"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.c447632b03bfdp+3"
        },
        "address": "src/devtools/resources/commands/execution.py",
        "content_identity": "5b1a3412c6fc3b4b5d0f0d3e4491d01c48d6dd89e47b4495dc714d0dede36f22",
        "document_identity": "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.bc49f6f099cb3p+3"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.bc49f6f099cb2p+3"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.b65c8a3ca2fc3p+3"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.b65c8a3ca2fc3p+3"
        },
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
        "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.b28d05b8e4f66p+3"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.b28d05b8e4f66p+3"
        },
        "address": "src/devtools/context/repository/observation.py",
        "content_identity": "84b0893b289fd613f3ecd441b4f963ef15c5269f3e6fcfe98ac1f52de4fe7b51",
        "document_identity": "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.af5742c878c24p+3"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.af5742c878c25p+3"
        },
        "address": "src/devtools/models/interaction/providers/llama_cpp.py",
        "content_identity": "565429b2a31457b4450465072539d1587dd3a191cfd13df988467f8be0901a3d",
        "document_identity": "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.a35aa3e3cdaccp+3"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.a35aa3e3cdacbp+3"
        },
        "address": "docs/backlog/items/B-0008-investigate-repository-context-discovery.md",
        "content_identity": "b6fba18919857fdcc652ba3147fdae731f1fd4a2e2e37b8ec3880baf47eefa04",
        "document_identity": "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.a1fdf15fcd9dbp+3"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.a1fdf15fcd9dcp+3"
        },
        "address": "tests/models/benchmarks/test_runner.py",
        "content_identity": "14ee7d72d179a7b5ce3dfdc722944833986a2f16abb549d48dc92906f3e2ceb8",
        "document_identity": "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.a0395da966a9cp+3"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.a0395da966a9ep+3"
        },
        "address": "tests/tools/test_command.py",
        "content_identity": "19fd42287878a7aba3c710bf3749466449119cd8fdb0a3307064b56048156bd6",
        "document_identity": "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.95609ee7d931dp+3"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.95609ee7d931cp+3"
        },
        "address": "tests/resources/commands/test_execution.py",
        "content_identity": "aee4e76977a7fbd06feaf1142e32aa6c5aaab740075f32e93613da388b10a283",
        "document_identity": "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.8a6db7200788ap+3"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.8a6db7200788ap+3"
        },
        "address": "tests/tools/test_runtime_integration.py",
        "content_identity": "82979c703980afb5f5508789155c45bb06adc7a5a7d6a973c74c251b602cde1e",
        "document_identity": "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.857813b39eef4p+3"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.857813b39eef3p+3"
        },
        "address": "tests/scripts/qwen/test_two_action_read_only_acceptance.py",
        "content_identity": "10fc867f673b0db841d41f18acb33e810fb6c53eb6347d2a428714d9c545ef3d",
        "document_identity": "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.8062eead86b34p+3"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.8062eead86b33p+3"
        },
        "address": "src/devtools/models/benchmarks/docs/overview.md",
        "content_identity": "e06e6abd5f9c3422bbe5159810f443048d2b896174d4c3fcd756b21706bc6973",
        "document_identity": "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.7ecb0646007f9p+3"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.7ecb0646007fap+3"
        },
        "address": "docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md",
        "content_identity": "99df09b180f72681a3a8c12489e6054edbd4119701b153cf94b992a74eaa8baf",
        "document_identity": "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.7e1b7c43ea791p+3"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.7e1b7c43ea792p+3"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.6fea4a32c3b70p+3"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.6fea4a32c3b70p+3"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.5514265d61246p+3"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.5514265d61246p+3"
        },
        "address": "docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md",
        "content_identity": "270a3fddbbbc84c6e4bbbb9d109343a4027316182364f1282885b8868374fcfe",
        "document_identity": "9326dbd823befd40c56e5d011c4e5207ef1bda0e3693e9844b01f598fd73186e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.5032d281469d5p+3"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.5032d281469d4p+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/csv.py",
        "content_identity": "d9ddfd29e02486d5f88d36ee9f7e88f466eaa068fc22b2513afb907018717a90",
        "document_identity": "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.4e412556358cbp+3"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.4e412556358cbp+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/json.py",
        "content_identity": "1ed913e313d22fe9e38fe68da1d2f948b6f19ef23421ebb951efabc988885e93",
        "document_identity": "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.4db20340a726ep+3"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.4db20340a726cp+3"
        },
        "address": "docs/backlog/epics/B-0005-effect-governance.md",
        "content_identity": "7a528fa22e45763986051340c0d609fe1636cf6046780514ccdbf10a06c83a5d",
        "document_identity": "77589241a9b804cf2f8d38afd12c1b84e807a4af4ad80ae0ae8d18549aace3ee",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.4a18e632a2d1cp+3"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.4a18e632a2d1cp+3"
        },
        "address": "src/devtools/core/paths/docs/overview.md",
        "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
        "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.42101b7b9c0b5p+3"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.42101b7b9c0b4p+3"
        },
        "address": "src/devtools/context/repository/discovery.py",
        "content_identity": "1e5d07bddab1549f1a0852d9ba82186721f662d61434fafdfbbda9f8c13ec198",
        "document_identity": "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.4011e7e37ea6cp+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.4011e7e37ea6cp+3"
        },
        "address": "tests/resources/commands/test_handle.py",
        "content_identity": "a7b72589aeec4bd1da1568909589e998544da2173da5aad1fa55e18be6710712",
        "document_identity": "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.2d51b1e90bffdp+3"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.2d51b1e90bffcp+3"
        },
        "address": "docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md",
        "content_identity": "eb9b4794c6612d5190cc85f508175a7a2b17fed694bb53afb53886dfa999197d",
        "document_identity": "2ff4a362ef64a4ec605617e500bc9956b489cd83e6a9eb447432273859858fd9",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.251fbf02e4932p+3"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.251fbf02e4932p+3"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.1eccbac5a9f47p+3"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.0c127ade9d24ep+3"
        },
        "address": "docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md",
        "content_identity": "acee48b767ae4d30136ffc2ae4044e3b5be9fd2999846dd99869b3ee44287602",
        "document_identity": "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "score_delta": {
          "float_hex": "-0x1.2ba3fe70ccf90p-1"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.195d7afd0b8ffp+3"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.195d7afd0b900p+3"
        },
        "address": "src/devtools/resources/commands/docs/events.md",
        "content_identity": "376647e8d3f3e9923e8c09bdfd55023c724abedd76d0d23596ebd8172162150c",
        "document_identity": "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.18bc2b763e677p+3"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.18bc2b763e677p+3"
        },
        "address": "tests/agents/integrations/codex/test_live.py",
        "content_identity": "b705ab7d34b2b7327ec5e86563123101bb9f293b15260a627905fd8524549e64",
        "document_identity": "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.113130b6ca921p+3"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.113130b6ca921p+3"
        },
        "address": "src/devtools/observability/evidence/docs/overview.md",
        "content_identity": "98431aec7bfdfc9c7a4396d6921a5f4174312ccb791b93741b03f8eb0b27c4e7",
        "document_identity": "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.0da492b205c43p+3"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.0da492b205c43p+3"
        },
        "address": "docs/backlog/items/B-0012-investigate-governed-effect-semantics.md",
        "content_identity": "27922033df5cb70819286d39b97da02a3f22d733a83fb026eae4d1df43c7299a",
        "document_identity": "50a13c505510c08acbde149c4e774c9f0a09089b5f4ae9bf81796ba79b670990",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.0d3b5202e3ca7p+3"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.0d3b5202e3ca7p+3"
        },
        "address": "src/devtools/resources/filesystem/docs/markdown.md",
        "content_identity": "9cc457eebfad885e0c469a4a9eb129be94f35c85d0f2a1b2e82e33da19598ca7",
        "document_identity": "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.0d3abe43cbc69p+3"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.0d3abe43cbc69p+3"
        },
        "address": "tests/resources/filesystem/models/markdown/test_file.py",
        "content_identity": "4baafbfb0b8ed4829bb5ae9d6243ccf0a739f4560187bc3ed64938d4ceb3d5d0",
        "document_identity": "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.0699047401a1ep+3"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.0699047401a1ep+3"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.015ee72148199p+3"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.015ee72148198p+3"
        },
        "address": "tests/agents/conversation/test_live.py",
        "content_identity": "8d785c1dd2043953ec624b38a3f7875ed56523421666f0cdabdadf3ff468bf20",
        "document_identity": "bcf1ba96f5651167486aa790e81cc04a5fded625f7b63324a8ad6016a3cb2342",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.0100cb1caff92p+3"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.0100cb1caff92p+3"
        },
        "address": "src/devtools/models/benchmarks/storage.py",
        "content_identity": "6c88cf637871971b04df0e3bf30a0fe62e1398e22053cce435ad6051a9508130",
        "document_identity": "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.e8ee89c1179e6p+2"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.e8ee89c1179e5p+2"
        },
        "address": "tests/models/interaction/test_tools.py",
        "content_identity": "6e3ab9f9b1779c387b72e6230b41ee76fed695f40eb55610240c9eecea85f596",
        "document_identity": "7e8ca45cec1b4dfaa4fb2e2488824467b0bceba8c0abafaa885da0137c0d84d3",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-50"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f"
      ],
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3"
      ],
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c"
      ],
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "50a13c505510c08acbde149c4e774c9f0a09089b5f4ae9bf81796ba79b670990"
      ],
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3"
      ],
      [
        "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
        "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2"
      ]
    ],
    "union": [
      "89c6154318932141de8a9643105bead3a09793b59e5d81f6ac26a28374dce579",
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "3436d74b9de1b2c117f539c699dfad2c360795dbfe0a716969f1e62af9596c6a",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "2868d9488eea970c46cf68e77257309aeba3bb20e7eef24e5db216dad5522e25",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "fa70b85937dc12b75eba6d25bab6c396409f81309ad2ee1f5a54a96827cfcbd3",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "3a8861e503621727519812dba904e2ba986d526e36cf885e9f9d52e7a26486da",
      "f21ac008c43a25bc8ebf99e1c3fcaf4e70e721af95a4ae49d331e45198d0627e",
      "5ba0f47cfc35c20cc91140d70b43fe04d792fc5a92f83e651693f9fe092df1f8",
      "34d0293a116ddc8235ca2d99f31ce6e03552fe5b2d6c65392c64d2babf245d9f",
      "5ab394192d3463bd0e16c2c33654d62537634b21bd543e79b9bd8aa09bda7535",
      "6c1e1251f93fc2d853c953fc47dcefc0afb8d8bb7d34eab0182d486115e04f8a",
      "3b1b3e11e9c6cd98a2bd9c633e009a64d38e00fa9dc82def527da989af422529",
      "737a1a2d0424c6daaedff8c59326bf645167d97fef603260ac8be59cda503b54",
      "bc87c4532d382ab87005c353f75c596865c277b44e3dd5538c37c46b7a470833",
      "571a3646d8b565891c80729cd67a57cf1cdfce85c2ea0c2a6eacfa16f5c63640",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "9326dbd823befd40c56e5d011c4e5207ef1bda0e3693e9844b01f598fd73186e",
      "2ab3783a16891f2dd1f0f11398e24726f00dfc0215a735c85f13b40840c5bd27",
      "12dd9da02cf96ac940eadf741f1925dc1251fef44d067c224019f8f185675890",
      "77589241a9b804cf2f8d38afd12c1b84e807a4af4ad80ae0ae8d18549aace3ee",
      "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "dfafd24ae78c7b2d67cbe0f17c6d5df5ffc733b30e1edee89624e43b60dbfe89",
      "4036b2656f4329634ba8554464caab1d0926bd7d95cb2a06908eec03d9259c43",
      "2ff4a362ef64a4ec605617e500bc9956b489cd83e6a9eb447432273859858fd9",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "c4e154142503ca4bf8b22fc8e8a550422e6d14cff3cc965351d15d4da8655dfe",
      "86d9325dbaf5fc3c9a7dad13bd1f922218d2a617afb5292335605c8a1f05c99f",
      "bc102965e1848562621739b54e6bdc9e5777dbceaf2dc08d4e8e91a4ac7a67a3",
      "4ea3a599fda31dbf6b92e5c55fa3d3416c98b97e60abbeb9119353910ee7392c",
      "50a13c505510c08acbde149c4e774c9f0a09089b5f4ae9bf81796ba79b670990",
      "a33a21b028e82df0a4adc260af2eef5dcc01c204f02826fbd83e5ac8432bb3b3",
      "e4b2f7925ff8dbc1f350406eae3102e5ce0d044f88b098d5f26381dfd283afe2",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "bcf1ba96f5651167486aa790e81cc04a5fded625f7b63324a8ad6016a3cb2342",
      "f7921099e61513b4486c1a9c35b73bd2a3c48498e1c96279d2526d153eb9f9e9",
      "7e8ca45cec1b4dfaa4fb2e2488824467b0bceba8c0abafaa885da0137c0d84d3"
    ]
  }
}
```


## Q5: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/reading.py | 1 | 1 | 0x1.18ae04301f775p+5 | 0x1.187bb0f87a299p+5 | 0 |
| tests/resources/filesystem/test_reading.py | 2 | 2 | 0x1.0fc613928606dp+5 | 0x1.1865ea6cf9e1ap+5 | 0 |
| src/devtools/resources/filesystem/docs/io.md | 3 | 3 | 0x1.db919dd148cbdp+4 | 0x1.db919dd148cbep+4 | 0 |
| src/devtools/resources/filesystem/docs/overview.md | 4 | 4 | 0x1.97d2041bb7449p+4 | 0x1.9723b002c1c13p+4 | 0 |
| src/devtools/resources/filesystem/docs/roadmap.md | 5 | 5 | 0x1.7bc8d6204dddbp+4 | 0x1.7b4b7dc436661p+4 | 0 |
| src/devtools/resources/filesystem/writing.py | 6 | 6 | 0x1.65aa932eb327ep+4 | 0x1.6527d69e0842ep+4 | 0 |
| tests/tools/test_filesystem.py | 7 | 7 | 0x1.55b3dc94f2734p+4 | 0x1.55b3dc94f2734p+4 | 0 |
| tests/resources/filesystem/codecs/test_csv.py | 8 | 8 | 0x1.532848ed241a1p+4 | 0x1.532848ed241a1p+4 | 0 |
| src/devtools/tools/filesystem.py | 9 | 15 | 0x1.44f638b669686p+4 | 0x1.2a6b7840068f8p+4 | -6 |
| src/devtools/resources/filesystem/models/text.py | 10 | 9 | 0x1.3e929813d798dp+4 | 0x1.3e071a6db795bp+4 | 1 |
| src/devtools/resources/filesystem/docs/json.md | 11 | 10 | 0x1.3d6bc1bc07ee2p+4 | 0x1.3cccc7f69dff1p+4 | 1 |
| tests/resources/filesystem/test_models.py | 12 | 11 | 0x1.3b19928c9cf8fp+4 | 0x1.3a86879f61af2p+4 | 1 |
| tests/context/repository/test_discovery.py | 13 | 12 | 0x1.3991d4475ffa1p+4 | 0x1.395b572230427p+4 | 1 |
| tests/resources/filesystem/codecs/test_json.py | 14 | 13 | 0x1.3282bd3a3859ap+4 | 0x1.3237c3645ae88p+4 | 1 |
| tests/resources/filesystem/codecs/test_markdown.py | 15 | 14 | 0x1.2f72d2368db47p+4 | 0x1.2f72d2368db47p+4 | 1 |
| tests/context/python/function/test_declaration_aggregation.py | 16 | 16 | 0x1.27f188ccc44d2p+4 | 0x1.27f188ccc44d2p+4 | 0 |
| src/devtools/resources/filesystem/models/binary.py | 17 | 17 | 0x1.25b769aebfbe1p+4 | 0x1.2513258ae4afcp+4 | 0 |
| tests/context/python/function/test_resource_selection.py | 18 | 18 | 0x1.1db3d2bdc5a2cp+4 | 0x1.1d68cb7b92ce4p+4 | 0 |
| src/devtools/resources/filesystem/docs/codecs.md | 19 | 29 | 0x1.1c7db2106fc44p+4 | 0x1.016f33cb362c5p+4 | -10 |
| src/devtools/resources/filesystem/docs/models.md | 20 | 26 | 0x1.1c4bf5402a1fbp+4 | 0x1.0a39cccc2bcd8p+4 | -6 |
| tests/context/repository/test_observation.py | 21 | 19 | 0x1.1bdd039b41e26p+4 | 0x1.1bdd039b41e26p+4 | 2 |
| src/devtools/resources/filesystem/models/json/base.py | 22 | 20 | 0x1.1994cb1aba865p+4 | 0x1.18dd08ffb669cp+4 | 2 |
| src/devtools/agents/integrations/codex/docs/cli.md | 23 | 21 | 0x1.179dfa8733eeap+4 | 0x1.179dfa8733eeap+4 | 2 |
| tests/context/python/function/test_candidates.py | 24 | 22 | 0x1.1425437babc4cp+4 | 0x1.13e2e99b26dbcp+4 | 2 |
| src/devtools/resources/filesystem/resolution.py | 25 | 23 | 0x1.107cf6d733b42p+4 | 0x1.1006680c870b9p+4 | 2 |
| src/devtools/resources/filesystem/codecs/markdown.py | 26 | 24 | 0x1.0e039784364c4p+4 | 0x1.0d708c96fb026p+4 | 2 |
| tests/context/python/test_source_candidacy.py | 27 | 25 | 0x1.0bfdd85418bfep+4 | 0x1.0bb044485a866p+4 | 2 |
| tests/resources/filesystem/test_resolution.py | 28 | 27 | 0x1.0508d8743120dp+4 | 0x1.0508d8743120dp+4 | 1 |
| tests/context/python/function/test_retrieval.py | 29 | 28 | 0x1.02e85d5b9cfb5p+4 | 0x1.02e85d5b9cfb4p+4 | 1 |
| tests/resources/filesystem/test_writing.py | 30 | 30 | 0x1.010c39c6b057fp+4 | 0x1.00cd39b855396p+4 | 0 |
| tests/core/paths/test_resolution.py | 31 | 32 | 0x1.ffabd02ef1f94p+3 | 0x1.fe555eb0b743bp+3 | -1 |
| tests/models/interaction/providers/test_llama_cpp.py | 32 | 31 | 0x1.ff6679ca9cbfcp+3 | 0x1.ff0c22d182615p+3 | 1 |
| src/devtools/tools/docs/overview.md | 33 | 33 | 0x1.ed6482bd78c53p+3 | 0x1.ec78704c8fb2fp+3 | 0 |
| src/devtools/resources/filesystem/codecs/text.py | 34 | 34 | 0x1.e65da05185354p+3 | 0x1.e5710899ccab6p+3 | 0 |
| tests/context/python/function/test_materialization.py | 35 | 35 | 0x1.e1fdba7fda032p+3 | 0x1.e1fdba7fda031p+3 | 0 |
| tests/context/python/function/test_rendering.py | 36 | 36 | 0x1.e1dae09fad36cp+3 | 0x1.e1dae09fad36cp+3 | 0 |
| tests/resources/filesystem/codecs/test_text.py | 37 | 37 | 0x1.e1bf95a2496a3p+3 | 0x1.e1bf95a2496a4p+3 | 0 |
| tests/context/python/function/test_request_assembly.py | 38 | 38 | 0x1.dff67cca6fbb0p+3 | 0x1.df50ea1a73987p+3 | 0 |
| tests/models/benchmarks/test_storage.py | 39 | 39 | 0x1.deb7803fc603ep+3 | 0x1.ddb5ac497dcddp+3 | 0 |
| src/devtools/context/python/mirrored_paths.py | 40 | 40 | 0x1.d4d7a73457320p+3 | 0x1.d4d7a73457320p+3 | 0 |
| src/devtools/context/python/function/docs/overview.md | 41 | 41 | 0x1.d4136c7b3cfaap+3 | 0x1.d4136c7b3cfabp+3 | 0 |
| tests/context/repository/test_corpus.py | 42 | 42 | 0x1.d23093764767dp+3 | 0x1.d23093764767ep+3 | 0 |
| src/devtools/resources/commands/docs/command.md | 43 | 43 | 0x1.d1238bcdfc2adp+3 | 0x1.d1238bcdfc2adp+3 | 0 |
| src/devtools/context/python/classes/docs/overview.md | 44 | 44 | 0x1.cf62ae8f941dbp+3 | 0x1.cf62ae8f941dcp+3 | 0 |
| src/devtools/context/python/function/rendering.py | 45 | 45 | 0x1.c61cb7b6520cep+3 | 0x1.c61cb7b6520cep+3 | 0 |
| src/devtools/context/python/function/retrieval.py | 46 | 46 | 0x1.c31ba4e1bf4b6p+3 | 0x1.c31ba4e1bf4b5p+3 | 0 |
| tests/models/interaction/test_models.py | 47 | 47 | 0x1.b47f843fa7fcap+3 | 0x1.b401f56376b45p+3 | 0 |
| src/devtools/resources/filesystem/codecs/__init__.py | 48 | 48 | 0x1.b19bff9b389d0p+3 | 0x1.b19bff9b389d0p+3 | 0 |
| AGENTS.md | 49 | 49 | 0x1.b12cefa9def43p+3 | 0x1.b0d0207007268p+3 | 0 |
| src/devtools/core/regex/docs/overview.md | 50 | 50 | 0x1.b0b0c812e46f7p+3 | 0x1.afa4be502412ep+3 | 0 |
| tests/context/python/project_configuration/test_configuration.py | 51 | 51 | 0x1.adc95b6df81bcp+3 | 0x1.adc95b6df81bap+3 | 0 |
| src/devtools/context/retrieval/graph/pagerank.py | 52 | 52 | 0x1.ad08f215c93cfp+3 | 0x1.ad08f215c93d0p+3 | 0 |
| src/devtools/context/localization/roles/models.py | 53 | 61 | 0x1.a9e04b947fadap+3 | 0x1.8c23c9d2ba5bfp+3 | -8 |
| src/devtools/resources/filesystem/__init__.py | 54 | 53 | 0x1.a9ce5e447cbcbp+3 | 0x1.a88990d75091bp+3 | 1 |
| src/devtools/resources/filesystem/codecs/json.py | 55 | 54 | 0x1.a2d72b63c6ec9p+3 | 0x1.a1b4ce4e654e2p+3 | 1 |
| tests/context/python/function/test_cross_resource_pipeline.py | 56 | 55 | 0x1.9e3e7bb0cdc7bp+3 | 0x1.9da90db0d1f47p+3 | 1 |
| src/devtools/resources/filesystem/codecs/csv.py | 57 | 56 | 0x1.938526f542237p+3 | 0x1.9292debff91eap+3 | 1 |
| src/devtools/resources/filesystem/docs/csv.md | 58 | 57 | 0x1.9369aec60cb60p+3 | 0x1.928ce9c5d04e9p+3 | 1 |
| tests/models/benchmarks/test_runner.py | 59 | 58 | 0x1.92da2ee7f011bp+3 | 0x1.9202753ae2e14p+3 | 1 |
| src/devtools/core/paths/docs/resolution.md | 60 | 59 | 0x1.8ede07063f267p+3 | 0x1.8d9e3c751643ap+3 | 1 |
| tests/context/python/project_configuration/test_settings.py | 61 | 60 | 0x1.8d3360aea79aap+3 | 0x1.8d3360aea79aap+3 | 1 |
| src/devtools/models/serving/docs/overview.md | 62 | 62 | 0x1.8d25a7fb23fdap+3 | 0x1.8bfafec59582ep+3 | 0 |
| tests/context/localization/generation/test_branching.py | 63 | 63 | 0x1.87f207147cb7bp+3 | 0x1.87f207147cb7cp+3 | 0 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 64 | 65 | 0x1.841b4a20fd4e5p+3 | 0x1.83b9f91201721p+3 | -1 |
| tests/context/python/modules/test_interpretation.py | 65 | 64 | 0x1.84146d765c4b4p+3 | 0x1.84146d765c4b5p+3 | 1 |
| src/devtools/models/serving/vllm.py | 66 | 66 | 0x1.81345914aaee6p+3 | 0x1.80527ec80fcbap+3 | 0 |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 67 | 67 | 0x1.7edef42f4a1b0p+3 | 0x1.7edef42f4a1b0p+3 | 0 |
| src/devtools/context/repository/observation.py | 68 | 68 | 0x1.7e0b31bea606cp+3 | 0x1.7e0b31bea606cp+3 | 0 |
| src/devtools/core/time/docs/timestamps.md | 69 | 69 | 0x1.7dffc860ac730p+3 | 0x1.7dffc860ac731p+3 | 0 |
| tests/context/retrieval/graph/test_ranking.py | 70 | 70 | 0x1.7a7b8fd2d63c9p+3 | 0x1.7a7b8fd2d63c9p+3 | 0 |
| tests/context/python/function/test_containment.py | 71 | 71 | 0x1.78a03fd34b932p+3 | 0x1.78a03fd34b932p+3 | 0 |
| src/devtools/core/paths/resolution.py | 72 | 73 | 0x1.76eea1e8b1c3ep+3 | 0x1.75db7db2f749bp+3 | -1 |
| tests/context/localization/generation/test_references.py | 73 | 72 | 0x1.7673416ca1706p+3 | 0x1.7673416ca1707p+3 | 1 |
| tests/scripts/test_retrieval_bm25_baseline.py | 74 | 74 | 0x1.7303b309373aap+3 | 0x1.7303b309373a9p+3 | 0 |
| tests/context/python/function/test_disclosure.py | 75 | 75 | 0x1.72d771dfb0190p+3 | 0x1.72d771dfb018fp+3 | 0 |
| src/devtools/models/benchmarks/runner.py | 76 | 77 | 0x1.72cca67a1de7fp+3 | 0x1.71f051f3f05a2p+3 | -1 |
| tests/context/python/test_mirrored_paths.py | 77 | 76 | 0x1.722206c08d536p+3 | 0x1.722206c08d536p+3 | 1 |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 78 | 78 | 0x1.6f1743a647148p+3 | 0x1.6e3cf7265a136p+3 | 0 |
| tests/context/python/imports/test_relations.py | 79 | 79 | 0x1.6ab9a7dcf4728p+3 | 0x1.6ab9a7dcf4728p+3 | 0 |
| tests/context/retrieval/graph/test_typed.py | 80 | 80 | 0x1.67c0696210494p+3 | 0x1.67c0696210495p+3 | 0 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 81 | 81 | 0x1.6481f1401839ap+3 | 0x1.63d669be3a562p+3 | 0 |
| tests/scripts/qwen/test_two_read_acceptance.py | 82 | 82 | 0x1.63969fdd9e406p+3 | 0x1.62f358563918dp+3 | 0 |
| src/devtools/resources/commands/models/result.py | 83 | 83 | 0x1.62218a86890a2p+3 | 0x1.612f9cfb64433p+3 | 0 |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 84 | 84 | 0x1.5edd7c7c182e7p+3 | 0x1.5e2c3f54dce54p+3 | 0 |
| tests/context/python/imports/test_resolution.py | 85 | 85 | 0x1.5d617936da758p+3 | 0x1.5d617936da758p+3 | 0 |
| tests/resources/filesystem/codecs/__init__.py | 86 | 86 | 0x1.5c5b022c0012ep+3 | 0x1.5c5b022c0012fp+3 | 0 |
| tests/context/localization/resolution/test_resolution.py | 87 | 87 | 0x1.59a165a183757p+3 | 0x1.59a165a183758p+3 | 0 |
| tests/context/python/function/test_declarations.py | 88 | 88 | 0x1.581945d418c13p+3 | 0x1.581945d418c13p+3 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 89 | 89 | 0x1.579a39abfe123p+3 | 0x1.5658112a395d6p+3 | 0 |
| src/devtools/context/python/docs/overview.md | 90 | 90 | 0x1.562bf775dc866p+3 | 0x1.562bf775dc866p+3 | 0 |
| tests/context/repository/test_document.py | 91 | 91 | 0x1.54849cd835fa8p+3 | 0x1.54849cd835fa7p+3 | 0 |
| tests/context/retrieval/lexical/_helpers.py | 92 | 92 | 0x1.4f25454561a99p+3 | 0x1.4f25454561a99p+3 | 0 |
| tests/context/localization/roles/test_evidence.py | 93 | 93 | 0x1.4f12631925996p+3 | 0x1.4f12631925997p+3 | 0 |
| tests/context/python/function/test_qualified_reference.py | 94 | 94 | 0x1.4e738e0cc7ee2p+3 | 0x1.4e171af521d61p+3 | 0 |
| tests/resources/filesystem/models/markdown/test_section.py | 95 | 95 | 0x1.49a6a39f481cap+3 | 0x1.49a6a39f481c9p+3 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 96 | 96 | 0x1.48dda45d1ae58p+3 | 0x1.4804df931d133p+3 | 0 |
| src/devtools/models/serving/llama_cpp.py | 97 | 98 | 0x1.476c68a7969c2p+3 | 0x1.4690ab50a588dp+3 | -1 |
| src/devtools/context/python/function/qualified_reference.py | 98 | 97 | 0x1.475b68f7b04dap+3 | 0x1.46e6aa2c582e4p+3 | 1 |
| src/devtools/core/regex/models.py | 99 | 107 | 0x1.43f5f163850d2p+3 | 0x1.30f3fa48873f6p+3 | -8 |
| tests/context/retrieval/test_structural.py | 100 | 99 | 0x1.427dfdbc0ff8bp+3 | 0x1.427dfdbc0ff8ap+3 | 1 |
| tests/observability/evidence/test_model_interaction.py | 101 | 100 | 0x1.40ab74482f94ap+3 | 0x1.3fc40af6c39ecp+3 | 1 |
| tests/context/retrieval/repository_map/test_ranking.py | 102 | 101 | 0x1.3b0b72fa46928p+3 | 0x1.3b0b72fa46928p+3 | 1 |
| tests/context/python/imports/test_declarations.py | 103 | 102 | 0x1.39a3969aed78dp+3 | 0x1.39a3969aed78dp+3 | 1 |
| src/devtools/resources/filesystem/models/base.py | 104 | 103 | 0x1.38e98c0735ba7p+3 | 0x1.37d1c384fc672p+3 | 1 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 105 | 104 | 0x1.36e8413af4e05p+3 | 0x1.3667aff999f3ap+3 | 1 |
| docs/experiments/qwen38_llama_cpp.md | 106 | 105 | 0x1.355e49cdcc044p+3 | 0x1.355e49cdcc044p+3 | 1 |
| src/devtools/models/benchmarks/models.py | 107 | 132 | 0x1.33394882c504ap+3 | 0x1.1410a4b331e2cp+3 | -25 |
| tests/context/retrieval/lexical/test_bm25.py | 108 | 106 | 0x1.3279aa9ea5e85p+3 | 0x1.3279aa9ea5e85p+3 | 2 |
| tests/context/localization/roles/test_configuration.py | 109 | 108 | 0x1.30df1dd63f619p+3 | 0x1.30df1dd63f619p+3 | 1 |
| tests/tools/test_execution.py | 110 | 109 | 0x1.307419d80a6c1p+3 | 0x1.307419d80a6c1p+3 | 1 |
| src/devtools/context/planning/resource.py | 111 | 110 | 0x1.2bf28b6a36398p+3 | 0x1.2bf28b6a36397p+3 | 1 |
| tests/context/localization/routing/test_routing.py | 112 | 111 | 0x1.2b809249ea398p+3 | 0x1.2b809249ea399p+3 | 1 |
| tests/context/retrieval/lexical/test_index.py | 113 | 112 | 0x1.29362c35f2a41p+3 | 0x1.29362c35f2a42p+3 | 1 |
| src/devtools/core/conversion/docs/overview.md | 114 | 113 | 0x1.28a3727567b86p+3 | 0x1.27c1bb4e79ef2p+3 | 1 |
| tests/evaluation/test_coverage.py | 115 | 114 | 0x1.2616d918b41e5p+3 | 0x1.2616d918b41e5p+3 | 1 |
| tests/context/python/classes/test_declarations.py | 116 | 115 | 0x1.2432d36adf94ep+3 | 0x1.2432d36adf94dp+3 | 1 |
| tests/context/planning/test_plan.py | 117 | 117 | 0x1.23da161f8ecebp+3 | 0x1.235a48e885407p+3 | 0 |
| tests/context/retrieval/lexical/test_statistics.py | 118 | 116 | 0x1.23b976ccddabcp+3 | 0x1.23b976ccddabcp+3 | 2 |
| src/devtools/resources/filesystem/models/json/object.py | 119 | 119 | 0x1.239371dc2c8e0p+3 | 0x1.2275ad2a6bc58p+3 | 0 |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 120 | 118 | 0x1.2389968048f2dp+3 | 0x1.231c636ad8464p+3 | 2 |
| src/devtools/context/planning/rendering.py | 121 | 120 | 0x1.221cef2821b38p+3 | 0x1.212f8e6b196a2p+3 | 1 |
| src/devtools/core/paths/docs/overview.md | 122 | 121 | 0x1.21cba9599fceep+3 | 0x1.21028cc832480p+3 | 1 |
| src/devtools/resources/filesystem/errors.py | 123 | 122 | 0x1.20eeb4fbcaf8ep+3 | 0x1.20eeb4fbcaf8ep+3 | 1 |
| src/devtools/context/localization/association/imports.py | 124 | 123 | 0x1.1ea851e3ff0d5p+3 | 0x1.1ea851e3ff0d5p+3 | 1 |
| src/devtools/resources/filesystem/models/json/list.py | 125 | 125 | 0x1.1dda6b609ec5fp+3 | 0x1.1cc183c17a31bp+3 | 0 |
| src/devtools/resources/commands/models/output.py | 126 | 124 | 0x1.1dccf34ecfe08p+3 | 0x1.1dccf34ecfe08p+3 | 2 |
| tests/resources/filesystem/test_json_conversion.py | 127 | 126 | 0x1.1d6608d5decaep+3 | 0x1.1c61327304cc5p+3 | 1 |
| src/devtools/context/python/source_candidacy.py | 128 | 127 | 0x1.1b60c5020bd46p+3 | 0x1.1b60c5020bd47p+3 | 1 |
| tests/resources/commands/test_execution.py | 129 | 128 | 0x1.1a7b775c23819p+3 | 0x1.1a7b775c23818p+3 | 1 |
| src/devtools/context/retrieval/docs/overview.md | 130 | 129 | 0x1.18aa1948006abp+3 | 0x1.18aa1948006abp+3 | 1 |
| docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md | 131 | 130 | 0x1.186975c633d34p+3 | 0x1.176bce609315ap+3 | 1 |
| src/devtools/persistence/sqlite.py | 132 | 131 | 0x1.14dfe56cf4b58p+3 | 0x1.145f8f3a88660p+3 | 1 |
| src/devtools/persistence/docs/json.md | 133 | 133 | 0x1.13725b4db9149p+3 | 0x1.13725b4db914ap+3 | 0 |
| tests/context/python/modules/test_membership.py | 134 | 134 | 0x1.135115549975fp+3 | 0x1.135115549975fp+3 | 0 |
| tests/context/python/classes/test_bases.py | 135 | 135 | 0x1.1095915220b8bp+3 | 0x1.1095915220b8bp+3 | 0 |
| src/devtools/context/repository/corpus.py | 136 | 136 | 0x1.0cb849297c63dp+3 | 0x1.0cb849297c63ep+3 | 0 |
| src/devtools/context/retrieval/lexical/bm25.py | 137 | 137 | 0x1.096cb7d3eaa52p+3 | 0x1.096cb7d3eaa52p+3 | 0 |
| tests/context/retrieval/lexical/test_filename.py | 138 | 138 | 0x1.095f50eabbfaep+3 | 0x1.095f50eabbfaep+3 | 0 |
| src/devtools/core/time/models/timestamp.py | 139 | 139 | 0x1.094c5ad14c14bp+3 | 0x1.094c5ad14c14cp+3 | 0 |
| src/devtools/context/python/function/materialization.py | 140 | 140 | 0x1.09228d3f2169cp+3 | 0x1.09228d3f2169cp+3 | 0 |
| src/devtools/resources/filesystem/models/__init__.py | 141 | 142 | 0x1.0836335179f21p+3 | 0x1.06b71ecf4b38cp+3 | -1 |
| tests/models/serving/test_llama_cpp.py | 142 | 141 | 0x1.07e26e500e37dp+3 | 0x1.06dac7053b8eep+3 | 1 |
| src/devtools/resources/filesystem/models/json/__init__.py | 143 | 144 | 0x1.0716411abc67ap+3 | 0x1.059883b3bd4a1p+3 | -1 |
| tests/context/localization/grounding/test_grounding.py | 144 | 143 | 0x1.05ef1b0f80cc9p+3 | 0x1.05ef1b0f80cc8p+3 | 1 |
| tests/scripts/qwen/test_llama_cpp_service.py | 145 | 146 | 0x1.03d49772e90bcp+3 | 0x1.034f149cf4c90p+3 | -1 |
| tests/resources/filesystem/models/csv/test_dialect.py | 146 | 145 | 0x1.03ad70a9a5496p+3 | 0x1.03ad70a9a5496p+3 | 1 |
| src/devtools/context/python/modules/interpretation.py | 147 | 147 | 0x1.01c65438affb0p+3 | 0x1.01c65438affafp+3 | 0 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 148 | 148 | 0x1.00914459e83d6p+3 | 0x1.fe36dc58c96bfp+2 | 0 |
| src/devtools/models/interaction/providers/llama_cpp.py | 149 | 149 | 0x1.ff45be098ef5cp+2 | 0x1.fdc55f4fc9807p+2 | 0 |
| tests/persistence/test_json.py | 150 | 151 | 0x1.fd582b4e5d226p+2 | 0x1.fc063e47b0c40p+2 | -1 |
| src/devtools/context/python/imports/declarations.py | 151 | 150 | 0x1.fd0bf9c370cc5p+2 | 0x1.fd0bf9c370cc6p+2 | 1 |
| src/devtools/models/benchmarks/storage.py | 152 | 153 | 0x1.f93b8dc424b1dp+2 | 0x1.f7a05a0c3bb1fp+2 | -1 |
| src/devtools/context/repository/document.py | 153 | 152 | 0x1.f85dc0ccd4bc7p+2 | 0x1.f85dc0ccd4bc8p+2 | 1 |
| src/devtools/context/python/project_configuration/models.py | 154 | 168 | 0x1.f24951f35628bp+2 | 0x1.cc4563bd5a8d1p+2 | -14 |
| tests/context/retrieval/test_composition.py | 155 | 154 | 0x1.ee5497357c118p+2 | 0x1.ee5497357c119p+2 | 1 |
| tests/context/localization/roles/helpers.py | 156 | 155 | 0x1.edee4424748a2p+2 | 0x1.edee4424748a2p+2 | 1 |
| tests/context/python/imports/test_members.py | 157 | 156 | 0x1.eb0323639da8ap+2 | 0x1.eb0323639da8bp+2 | 1 |
| tests/context/python/references/declarations/test_analysis.py | 158 | 157 | 0x1.e9f5c61a52312p+2 | 0x1.e9f5c61a52312p+2 | 1 |
| tests/resources/filesystem/models/csv/test_row.py | 159 | 158 | 0x1.e4424b4896a22p+2 | 0x1.e4424b4896a22p+2 | 1 |
| src/devtools/context/python/function/request_assembly.py | 160 | 159 | 0x1.e32b257b70d78p+2 | 0x1.e13369603fc13p+2 | 1 |
| src/devtools/agents/integrations/codex/agent.py | 161 | 161 | 0x1.dc195f3e1f388p+2 | 0x1.da27e34677289p+2 | 0 |
| tests/resources/filesystem/models/markdown/test_file.py | 162 | 160 | 0x1.dae06957e7377p+2 | 0x1.dae06957e7376p+2 | 2 |
| tests/core/time/test_models.py | 163 | 162 | 0x1.d99cf13613beep+2 | 0x1.d99cf13613bedp+2 | 1 |
| src/devtools/context/repository/discovery.py | 164 | 163 | 0x1.d99b25a82e726p+2 | 0x1.d99b25a82e726p+2 | 1 |
| tests/context/retrieval/lexical/test_evaluation.py | 165 | 164 | 0x1.d86c198389b7fp+2 | 0x1.d86c198389b80p+2 | 1 |
| src/devtools/models/interaction/docs/overview.md | 166 | 165 | 0x1.d7ff9e1c60ab4p+2 | 0x1.d618067c41456p+2 | 1 |
| src/devtools/resources/filesystem/models/markdown/section.py | 167 | 166 | 0x1.d426ae53ab7fcp+2 | 0x1.d2003b87b1116p+2 | 1 |
| src/devtools/context/localization/roles/derivation.py | 168 | 167 | 0x1.d0ec9e284dfb7p+2 | 0x1.cf059432ed4f2p+2 | 1 |
| src/devtools/context/python/project_configuration/resolution.py | 169 | 169 | 0x1.c86c63805a9e8p+2 | 0x1.c6c781f03f228p+2 | 0 |
| src/devtools/context/repository/snapshot.py | 170 | 170 | 0x1.c6a0cece18b8ap+2 | 0x1.c6a0cece18b8bp+2 | 0 |
| src/devtools/core/time/docs/overview.md | 171 | 171 | 0x1.c56a6b5ebcbfap+2 | 0x1.c56a6b5ebcbfap+2 | 0 |
| tests/agents/conversation/history/test_history.py | 172 | 173 | 0x1.c406a5f32d059p+2 | 0x1.c2d7c80375bd4p+2 | -1 |
| tests/resources/filesystem/models/csv/test_file.py | 173 | 172 | 0x1.c3316ecd1dbe6p+2 | 0x1.c3316ecd1dbe6p+2 | 1 |
| tests/context/localization/roles/test_inputs.py | 174 | 174 | 0x1.c2178cbbe4caep+2 | 0x1.c2178cbbe4cafp+2 | 0 |
| src/devtools/context/localization/generation/contract.py | 175 | 175 | 0x1.c1f799c1d85e9p+2 | 0x1.c0bc6f1352b84p+2 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 176 | 176 | 0x1.c1b64777b2d99p+2 | 0x1.c01f7b029e053p+2 | 0 |
| src/devtools/context/python/modules/membership.py | 177 | 177 | 0x1.bf4caf11659f7p+2 | 0x1.bf4caf11659f7p+2 | 0 |
| src/devtools/context/python/function/disclosure.py | 178 | 178 | 0x1.b65f1dfdee402p+2 | 0x1.b65f1dfdee400p+2 | 0 |
| tests/resources/filesystem/test_json_models.py | 179 | 179 | 0x1.b5c4bfabe2abfp+2 | 0x1.b37772dab8e64p+2 | 0 |
| src/devtools/resources/filesystem/models/json/scalar.py | 180 | 180 | 0x1.ad19d3fc11807p+2 | 0x1.aa8e402114780p+2 | 0 |
| src/devtools/context/retrieval/structural.py | 181 | 181 | 0x1.a518cb23285bep+2 | 0x1.a518cb23285bdp+2 | 0 |
| src/devtools/context/repository/resource.py | 182 | 182 | 0x1.a46a044267ec5p+2 | 0x1.a46a044267ec5p+2 | 0 |
| tests/resources/filesystem/__init__.py | 183 | 184 | 0x1.9e7f2aa32bd5ap+2 | 0x1.9c120c13cd644p+2 | -1 |
| tests/resources/filesystem/models/markdown/__init__.py | 184 | 185 | 0x1.9e7f2aa32bd5ap+2 | 0x1.9c120c13cd644p+2 | -1 |
| tests/resources/filesystem/models/csv/__init__.py | 185 | 186 | 0x1.9de5ce1b4c7abp+2 | 0x1.9b79955b74e67p+2 | -1 |
| src/devtools/context/python/function/declarations.py | 186 | 183 | 0x1.9c75b88c7f5e0p+2 | 0x1.9c75b88c7f5e0p+2 | 3 |
| tests/scripts/qwen/test_llama_cpp_profile.py | 187 | 187 | 0x1.98cd41fe582bdp+2 | 0x1.98cd41fe582bcp+2 | 0 |
| tests/context/retrieval/lexical/test_analysis.py | 188 | 188 | 0x1.96f56a865a112p+2 | 0x1.96f56a865a112p+2 | 0 |
| src/devtools/core/regex/search.py | 189 | 189 | 0x1.95f96ee67f7fep+2 | 0x1.9465b243336abp+2 | 0 |
| pyproject.toml | 190 | 190 | 0x1.94328d92e4110p+2 | 0x1.94328d92e4110p+2 | 0 |
| src/devtools/core/time/parsing.py | 191 | 191 | 0x1.93ab1e1f50479p+2 | 0x1.92065be0504f3p+2 | 0 |
| tests/context/localization/generation/test_generation.py | 192 | 192 | 0x1.8fa294be0a63dp+2 | 0x1.8fa294be0a63dp+2 | 0 |
| src/devtools/context/python/modules/docs/overview.md | 193 | 193 | 0x1.8f2a66725b755p+2 | 0x1.8f2a66725b755p+2 | 0 |
| tests/context/python/modules/test_selection.py | 194 | 194 | 0x1.8b28bd6e4d0c4p+2 | 0x1.8b28bd6e4d0c3p+2 | 0 |
| src/devtools/context/retrieval/repository_map/importance.py | 195 | 195 | 0x1.88e06b49dc568p+2 | 0x1.88e06b49dc567p+2 | 0 |
| src/devtools/context/localization/routing/docs/overview.md | 196 | 196 | 0x1.88cbe72310cb7p+2 | 0x1.88cbe72310cb7p+2 | 0 |
| tests/core/regex/test_models.py | 197 | 197 | 0x1.7cb11297368a6p+2 | 0x1.7cb11297368a6p+2 | 0 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 198 | 198 | 0x1.7cb0fc2ae6b4fp+2 | 0x1.7c093b1a99107p+2 | 0 |
| tests/agents/integrations/codex/test_parsing.py | 199 | 199 | 0x1.78eea5c1379dbp+2 | 0x1.78eea5c1379dbp+2 | 0 |
| tests/observability/evidence/test_protocols.py | 200 | 200 | 0x1.71013b688505ep+2 | 0x1.71013b688505ep+2 | 0 |
| src/devtools/tools/command.py | 201 | 201 | 0x1.6eb15825144d0p+2 | 0x1.6eb15825144d0p+2 | 0 |
| src/devtools/context/localization/routing/models.py | 202 | 236 | 0x1.6d329ca10d660p+2 | 0x1.26239b3bc481bp+2 | -34 |
| src/devtools/context/localization/readiness.py | 203 | 202 | 0x1.6b51f80e2b0b0p+2 | 0x1.6b51f80e2b0b0p+2 | 1 |
| src/devtools/resources/filesystem/models/json/conversion.py | 204 | 206 | 0x1.65ae900235b48p+2 | 0x1.63a979631951cp+2 | -2 |
| src/devtools/context/python/imports/relations.py | 205 | 203 | 0x1.64a726683b1c0p+2 | 0x1.64a726683b1c0p+2 | 2 |
| tests/context/repository/test_intrinsic_paths.py | 206 | 204 | 0x1.649123c609f0bp+2 | 0x1.649123c609f0cp+2 | 2 |
| tests/resources/filesystem/models/markdown/test_heading.py | 207 | 205 | 0x1.63e852abfd9e8p+2 | 0x1.63e852abfd9e7p+2 | 2 |
| tests/context/localization/test_lexical.py | 208 | 207 | 0x1.62f8862d517fcp+2 | 0x1.62f8862d517fcp+2 | 1 |
| tests/persistence/test_sqlite.py | 209 | 208 | 0x1.62f5d23b5da7ep+2 | 0x1.6228e08c25918p+2 | 1 |
| src/devtools/context/localization/routing/__init__.py | 210 | 209 | 0x1.61582078ad031p+2 | 0x1.5f05adfc2e00dp+2 | 1 |
| src/devtools/context/python/references/declarations/model.py | 211 | 210 | 0x1.5db15e6199426p+2 | 0x1.5db15e6199426p+2 | 1 |
| src/devtools/context/planning/plan.py | 212 | 211 | 0x1.5d6a79690831ep+2 | 0x1.5d6a79690831dp+2 | 1 |
| src/devtools/context/localization/routing/derive.py | 213 | 212 | 0x1.56edefe1101a2p+2 | 0x1.54e10228e79b5p+2 | 1 |
| src/devtools/evaluation/docs/overview.md | 214 | 213 | 0x1.538428c58ea5ap+2 | 0x1.538428c58ea5bp+2 | 1 |
| tests/scripts/test_vllm_benchmark_driver.py | 215 | 214 | 0x1.50aa7addc4a02p+2 | 0x1.4ed3eaeea3696p+2 | 1 |
| src/devtools/resources/filesystem/docs/markdown.md | 216 | 215 | 0x1.505629ae1305ap+2 | 0x1.4e8d1ad31791ep+2 | 1 |
| src/devtools/agents/integrations/codex/parsing.py | 217 | 216 | 0x1.4b6603f9ec6fdp+2 | 0x1.4a0d06bdf2df6p+2 | 1 |
| tests/models/benchmarks/test_models.py | 218 | 218 | 0x1.4a9769ec58182p+2 | 0x1.482645d4d847ap+2 | 0 |
| src/devtools/context/planning/docs/overview.md | 219 | 217 | 0x1.494bf545b250ep+2 | 0x1.494bf545b250dp+2 | 2 |
| src/devtools/context/retrieval/lexical/analysis.py | 220 | 219 | 0x1.474cc2a0b3e7ap+2 | 0x1.474cc2a0b3e7ap+2 | 1 |
| src/devtools/persistence/json.py | 221 | 220 | 0x1.45548e77d9746p+2 | 0x1.4422aacbe87a4p+2 | 1 |
| tests/resources/commands/test_models.py | 222 | 221 | 0x1.420367a0c4efdp+2 | 0x1.420367a0c4efdp+2 | 1 |
| tests/models/interaction/test_tools.py | 223 | 225 | 0x1.41fc6f7d0682ep+2 | 0x1.405816c04a7e2p+2 | -2 |
| src/devtools/context/python/references/declarations/analysis.py | 224 | 222 | 0x1.41a7f71488e0dp+2 | 0x1.41a7f71488e0cp+2 | 2 |
| tests/context/localization/generation/test_imports.py | 225 | 223 | 0x1.41463b1ad94d6p+2 | 0x1.41463b1ad94d6p+2 | 2 |
| src/devtools/context/python/classes/bases.py | 226 | 224 | 0x1.4111a94013e74p+2 | 0x1.4111a94013e74p+2 | 2 |
| tests/scripts/test_validate_development.py | 227 | 226 | 0x1.3e13792816302p+2 | 0x1.3e13792816303p+2 | 1 |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 228 | 227 | 0x1.3d64f18656362p+2 | 0x1.3b1936a9f896cp+2 | 1 |
| src/devtools/context/retrieval/lexical/index.py | 229 | 228 | 0x1.3a8dbf38c4d67p+2 | 0x1.3a8dbf38c4d66p+2 | 1 |
| src/devtools/core/time/docs/timing.md | 230 | 229 | 0x1.3332e7c74650bp+2 | 0x1.3332e7c74650cp+2 | 1 |
| src/devtools/context/localization/association/references.py | 231 | 230 | 0x1.2f38287ee5f4dp+2 | 0x1.2f38287ee5f4cp+2 | 1 |
| src/devtools/core/time/models/duration.py | 232 | 231 | 0x1.2cc63364d10d3p+2 | 0x1.2cc63364d10d3p+2 | 1 |
| tests/resources/filesystem/models/__init__.py | 233 | 232 | 0x1.2a6e60d6950cep+2 | 0x1.2a6e60d6950cfp+2 | 1 |
| tests/agents/integrations/codex/test_live.py | 234 | 234 | 0x1.29e8d0f0c954ep+2 | 0x1.28382e12f8b24p+2 | 0 |
| src/devtools/context/python/modules/declarations.py | 235 | 233 | 0x1.29c29ea8d840cp+2 | 0x1.29c29ea8d840cp+2 | 2 |
| src/devtools/core/paths/models.py | 236 | 255 | 0x1.28f61db379528p+2 | 0x1.02f22f7d7db6ep+2 | -19 |
| src/devtools/models/serving/huggingface.py | 237 | 235 | 0x1.264e55106ca5bp+2 | 0x1.264e55106ca5ap+2 | 2 |
| tests/core/time/test_parsing.py | 238 | 237 | 0x1.24f2e1db52141p+2 | 0x1.24f2e1db52142p+2 | 1 |
| tests/models/serving/test_vllm.py | 239 | 239 | 0x1.1deff761eac59p+2 | 0x1.1be3f9f486d9dp+2 | 0 |
| tests/context/localization/association/test_hypothesis.py | 240 | 238 | 0x1.1cb288ef264fap+2 | 0x1.1cb288ef264fap+2 | 2 |
| src/devtools/resources/commands/docs/execution.md | 241 | 240 | 0x1.1bb627a12a6fep+2 | 0x1.1bb627a12a6fep+2 | 1 |
| tests/observability/evidence/test_inspection.py | 242 | 241 | 0x1.1a48d92077da7p+2 | 0x1.18a6f5209d5bfp+2 | 1 |
| src/devtools/context/retrieval/lexical/statistics.py | 243 | 242 | 0x1.17abc28a12b88p+2 | 0x1.17abc28a12b88p+2 | 1 |
| src/devtools/resources/commands/models/__init__.py | 244 | 243 | 0x1.16ac964d5b091p+2 | 0x1.13d6affe836e1p+2 | 1 |
| src/devtools/resources/filesystem/models/markdown/heading.py | 245 | 244 | 0x1.14a73b4df04d6p+2 | 0x1.12bb0d3ce6ca2p+2 | 1 |
| src/devtools/context/localization/resolution/contract.py | 246 | 245 | 0x1.127eabe459262p+2 | 0x1.127eabe459261p+2 | 1 |
| tests/agents/conversation/message/test_message.py | 247 | 247 | 0x1.0f3cefd67f48fp+2 | 0x1.0de899551cbf2p+2 | 0 |
| tests/core/regex/test_search.py | 248 | 246 | 0x1.0e91fe19feb6bp+2 | 0x1.0e91fe19feb6bp+2 | 2 |
| src/devtools/context/retrieval/fusion.py | 249 | 248 | 0x1.0c86591b1d7bap+2 | 0x1.0c86591b1d7bap+2 | 1 |
| tests/core/conversion/test_conversion.py | 250 | 249 | 0x1.0c4bf6601bd6ep+2 | 0x1.0c4bf6601bd6fp+2 | 1 |
| src/devtools/core/conversion/errors.py | 251 | 250 | 0x1.0c4afdc821544p+2 | 0x1.0c4afdc821543p+2 | 1 |
| src/devtools/persistence/errors.py | 252 | 251 | 0x1.0bada0051454cp+2 | 0x1.0bada0051454dp+2 | 1 |
| src/devtools/core/system/docs/overview.md | 253 | 252 | 0x1.0b000f6568fe0p+2 | 0x1.0b000f6568fe0p+2 | 1 |
| src/devtools/context/python/classes/declarations.py | 254 | 253 | 0x1.0a7d34b9af29dp+2 | 0x1.0a7d34b9af29cp+2 | 1 |
| tests/core/identity/test_models.py | 255 | 254 | 0x1.09ff3351321d1p+2 | 0x1.09ff3351321d2p+2 | 1 |
| src/devtools/resources/commands/__init__.py | 256 | 257 | 0x1.fed2931a8748ep+1 | 0x1.fa588b0a107bbp+1 | -1 |
| src/devtools/context/python/function/candidates.py | 257 | 256 | 0x1.fc30f3405e7bap+1 | 0x1.fc30f3405e7b9p+1 | 1 |
| src/devtools/context/localization/generation/generate.py | 258 | 258 | 0x1.fa517520c86ebp+1 | 0x1.fa517520c86ebp+1 | 0 |
| src/devtools/models/interaction/usage.py | 259 | 259 | 0x1.f9133e3abc16dp+1 | 0x1.f9133e3abc16dp+1 | 0 |
| src/devtools/resources/commands/docs/events.md | 260 | 260 | 0x1.f14abcdae69b8p+1 | 0x1.f14abcdae69bap+1 | 0 |
| tests/models/serving/test_huggingface.py | 261 | 262 | 0x1.f146f4711382ap+1 | 0x1.ebdc595d21326p+1 | -1 |
| src/devtools/models/benchmarks/docs/overview.md | 262 | 261 | 0x1.ef743e1553edbp+1 | 0x1.ec37b8fc3c39ap+1 | 1 |
| tests/agents/integrations/codex/test_agent.py | 263 | 263 | 0x1.ee01ed0832462p+1 | 0x1.ebcbc04650757p+1 | 0 |
| src/devtools/context/python/function/containment.py | 264 | 264 | 0x1.e76f379148b3ep+1 | 0x1.e76f379148b3cp+1 | 0 |
| src/devtools/context/localization/lexical.py | 265 | 265 | 0x1.e03261f6b6358p+1 | 0x1.e03261f6b6358p+1 | 0 |
| src/devtools/context/localization/resolution/view.py | 266 | 266 | 0x1.d9a60d5284ce0p+1 | 0x1.d9a60d5284cdep+1 | 0 |
| src/devtools/context/retrieval/graph/__init__.py | 267 | 267 | 0x1.d819a43f092a0p+1 | 0x1.d819a43f092a0p+1 | 0 |
| tests/tools/test_runtime_integration.py | 268 | 269 | 0x1.d67bf706e82f3p+1 | 0x1.d3e8b9a83c328p+1 | -1 |
| src/devtools/context/python/imports/docs/overview.md | 269 | 268 | 0x1.d472c9f53a774p+1 | 0x1.d472c9f53a772p+1 | 1 |
| tests/context/python/references/declarations/test_bindings.py | 270 | 270 | 0x1.d2b7c4ee1e7aap+1 | 0x1.d2b7c4ee1e7aap+1 | 0 |
| src/devtools/context/python/classes/containment.py | 271 | 271 | 0x1.c8f811f6c2fa6p+1 | 0x1.c8f811f6c2fa6p+1 | 0 |
| src/devtools/context/python/imports/resolution.py | 272 | 272 | 0x1.c54ad17cac8dcp+1 | 0x1.c54ad17cac8dbp+1 | 0 |
| tests/resources/commands/test_errors.py | 273 | 273 | 0x1.b5b3a54371557p+1 | 0x1.b5b3a54371557p+1 | 0 |
| src/devtools/resources/commands/handle.py | 274 | 275 | 0x1.b53daeeee8063p+1 | 0x1.b112544c464e2p+1 | -1 |
| docs/backlog/items/B-0026-investigate-runtime-control-lifecycle.md | 275 | 276 | 0x1.b47778f540d7cp+1 | 0x1.b0068cb9507edp+1 | -1 |
| src/devtools/context/localization/roles/configuration.py | 276 | 277 | 0x1.b42890fa4cd4bp+1 | 0x1.af6d89837cf48p+1 | -1 |
| src/devtools/context/retrieval/graph/view.py | 277 | 274 | 0x1.b157ec55185f4p+1 | 0x1.b157ec55185f4p+1 | 3 |
| docs/backlog/items/B-0023-investigate-observability-architecture.md | 278 | 278 | 0x1.adc117fa06dc8p+1 | 0x1.aa54548e0c2bfp+1 | 0 |
| docs/backlog/items/B-0041-investigate-execution-local-lifecycle-control.md | 279 | 279 | 0x1.aa4d48847fe8cp+1 | 0x1.a5f6d68d30423p+1 | 0 |
| src/devtools/context/localization/generation/references.py | 280 | 280 | 0x1.a56739922e5f4p+1 | 0x1.a56739922e5f4p+1 | 0 |
| src/devtools/context/retrieval/__init__.py | 281 | 281 | 0x1.a4f6d4818d69ep+1 | 0x1.a4f6d4818d69fp+1 | 0 |
| tests/core/time/test_timing.py | 282 | 284 | 0x1.a0fe9dfb9db5cp+1 | 0x1.9bca44160da7bp+1 | -2 |
| src/devtools/context/localization/identity.py | 283 | 282 | 0x1.a021aa932573ep+1 | 0x1.a021aa932573dp+1 | 1 |
| src/devtools/agents/conversation/history.py | 284 | 283 | 0x1.9ff544beba30bp+1 | 0x1.9ff544beba30bp+1 | 1 |
| tests/resources/commands/test_events.py | 285 | 285 | 0x1.943e1fdf2092ap+1 | 0x1.943e1fdf2092ap+1 | 0 |
| src/devtools/resources/commands/events.py | 286 | 287 | 0x1.93d5b329a7221p+1 | 0x1.8fb9c71c3e2e1p+1 | -1 |
| src/devtools/context/localization/generation/imports.py | 287 | 286 | 0x1.913f3c9b430abp+1 | 0x1.913f3c9b430acp+1 | 1 |
| tests/agents/conversation/test_live.py | 288 | 288 | 0x1.8eff6f1000a87p+1 | 0x1.8eff6f1000a86p+1 | 0 |
| src/devtools/context/retrieval/graph/walk.py | 289 | 289 | 0x1.87d787f9c6a2cp+1 | 0x1.87d787f9c6a2cp+1 | 0 |
| tests/agents/conversation/test_session.py | 290 | 290 | 0x1.7ae7ff6bf6c41p+1 | 0x1.7932c1272f864p+1 | 0 |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 291 | 291 | 0x1.77be27a1baaf2p+1 | 0x1.73eb685a3a8a8p+1 | 0 |
| src/devtools/context/retrieval/repository_map/view.py | 292 | 292 | 0x1.73caa52e5f7b2p+1 | 0x1.73caa52e5f7b2p+1 | 0 |
| src/devtools/context/localization/association/hypothesis.py | 293 | 293 | 0x1.71ef4092e3e23p+1 | 0x1.6f703c8e929d4p+1 | 0 |
| tests/tools/test_command.py | 294 | 294 | 0x1.6dd3a30fde3e8p+1 | 0x1.6dd3a30fde3eap+1 | 0 |
| src/devtools/agents/conversation/conversation.py | 295 | 295 | 0x1.6b4f35a49b1c9p+1 | 0x1.687cb4497952ap+1 | 0 |
| src/devtools/observability/evidence/docs/overview.md | 296 | 298 | 0x1.6922c4e5a3ad4p+1 | 0x1.65c6b3041dea6p+1 | -2 |
| src/devtools/context/python/project_configuration/settings.py | 297 | 297 | 0x1.6893d9a94608cp+1 | 0x1.65c6c71afdcf4p+1 | 0 |
| src/devtools/context/retrieval/repository_map/relevance.py | 298 | 296 | 0x1.68434ffeb3f0ap+1 | 0x1.68434ffeb3f09p+1 | 2 |
| tests/models/interaction/test_protocols.py | 299 | 299 | 0x1.6816d1e0e9695p+1 | 0x1.642d3a93791eep+1 | 0 |
| src/devtools/core/system/models.py | 300 | 345 | 0x1.61b4b775ae3c7p+1 | 0x1.ae3f232ba1596p+0 | -45 |
| docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md | 301 | 300 | 0x1.5e414d5c6da3bp+1 | 0x1.5aff2542fc63bp+1 | 1 |
| src/devtools/agents/integrations/codex/models.py | 302 | 394 | 0x1.5cc2182af6e48p+1 | 0x1.a60c88c6210eap+0 | -92 |
| src/devtools/context/python/project_configuration/declarations.py | 303 | 301 | 0x1.58e44ee5c6a74p+1 | 0x1.55aeecad94a0ap+1 | 2 |
| src/devtools/resources/commands/execution.py | 304 | 302 | 0x1.56d2ca141be1ap+1 | 0x1.549381ae9d370p+1 | 2 |
| src/devtools/resources/commands/models/command.py | 305 | 303 | 0x1.4ceabd4339c5ep+1 | 0x1.4ceabd4339c5dp+1 | 2 |
| src/devtools/models/interaction/models.py | 306 | 408 | 0x1.46f6ddc7bdf7ep+1 | 0x1.82bc4b3337867p+0 | -102 |
| tests/resources/commands/test_handle.py | 307 | 304 | 0x1.3cae9957b1ef1p+1 | 0x1.3cae9957b1ef0p+1 | 3 |
| src/devtools/context/localization/roles/inputs.py | 308 | 306 | 0x1.3c25fc8431d56p+1 | 0x1.39350ea5c7e70p+1 | 2 |
| src/devtools/context/python/modules/lookup.py | 309 | 305 | 0x1.3ba6a32cd6eccp+1 | 0x1.3ba6a32cd6ecbp+1 | 4 |
| src/devtools/context/python/modules/selection.py | 310 | 307 | 0x1.3807c93b64609p+1 | 0x1.3807c93b64608p+1 | 3 |
| src/devtools/context/localization/grounding/contract.py | 311 | 308 | 0x1.2fc2a2b8812efp+1 | 0x1.2fc2a2b8812eep+1 | 3 |
| src/devtools/context/localization/grounding/resolve.py | 312 | 309 | 0x1.2f3230375bd22p+1 | 0x1.2f3230375bd21p+1 | 3 |
| src/devtools/context/python/imports/members.py | 313 | 310 | 0x1.2962280d3d69cp+1 | 0x1.2962280d3d69bp+1 | 3 |
| src/devtools/models/interaction/__init__.py | 314 | 311 | 0x1.21fef7f4b2353p+1 | 0x1.1bef11adf5570p+1 | 3 |
| docs/backlog/metadata.md | 315 | 313 | 0x1.1a5cdccda389dp+1 | 0x1.177d5ad0d10cbp+1 | 2 |
| src/devtools/context/python/references/docs/overview.md | 316 | 312 | 0x1.17a2fce5eb7dfp+1 | 0x1.17a2fce5eb7dfp+1 | 4 |
| docs/backlog/overview.md | 317 | 315 | 0x1.16982aad0c2c0p+1 | 0x1.12671a9bb5436p+1 | 2 |
| src/devtools/context/python/function/planned_reference.py | 318 | 314 | 0x1.127e961154191p+1 | 0x1.127e961154191p+1 | 4 |
| src/devtools/models/interaction/response.py | 319 | 316 | 0x1.114cbc5538041p+1 | 0x1.0b962f68a3aefp+1 | 3 |
| src/devtools/core/time/models/__init__.py | 320 | 317 | 0x1.0fe76aec6b25bp+1 | 0x1.0a38562b65e2bp+1 | 3 |
| src/devtools/models/interaction/providers/__init__.py | 321 | 318 | 0x1.0f23499f2c577p+1 | 0x1.09784e72d20c0p+1 | 3 |
| src/devtools/models/interaction/protocols.py | 322 | 319 | 0x1.094e96ee12f7bp+1 | 0x1.03c2cfdbc5fd1p+1 | 3 |
| src/devtools/context/retrieval/composition.py | 323 | 320 | 0x1.038a3d22bcc84p+1 | 0x1.038a3d22bcc84p+1 | 3 |
| scripts/validate_development.py | 324 | 321 | 0x1.0297e6bb51016p+1 | 0x1.0297e6bb51017p+1 | 3 |
| src/devtools/resources/commands/docs/overview.md | 325 | 322 | 0x1.01759ce8ff43bp+1 | 0x1.01759ce8ff43bp+1 | 3 |
| src/devtools/context/retrieval/lexical/filename.py | 326 | 323 | 0x1.fc5ba3cd3b7e8p+0 | 0x1.fc5ba3cd3b7e9p+0 | 3 |
| tests/context/localization/test_kernel.py | 327 | 324 | 0x1.f70938b5435c2p+0 | 0x1.f70938b5435c3p+0 | 3 |
| src/devtools/context/localization/association/structural.py | 328 | 325 | 0x1.f0d327ce301e7p+0 | 0x1.f0d327ce301e9p+0 | 3 |
| docs/backlog/items/B-0007-correct-model-serving-documentation-drift.md | 329 | 328 | 0x1.eca37d1cdc39dp+0 | 0x1.e25728211b603p+0 | 1 |
| src/devtools/resources/__init__.py | 330 | 326 | 0x1.e98874d640f88p+0 | 0x1.e98874d640f8ap+0 | 4 |
| src/devtools/context/retrieval/lexical/evaluation.py | 331 | 327 | 0x1.e760b2dce5715p+0 | 0x1.e760b2dce5716p+0 | 4 |
| src/devtools/models/interaction/observation.py | 332 | 329 | 0x1.e61e0eca42c54p+0 | 0x1.dbf49fafad93cp+0 | 3 |
| tests/execution/test_runtime.py | 333 | 330 | 0x1.d79094cf062d2p+0 | 0x1.d474bfdb954ecp+0 | 3 |
| src/devtools/resources/commands/errors.py | 334 | 331 | 0x1.d337910fe79d1p+0 | 0x1.d337910fe79d0p+0 | 3 |
| src/devtools/context/localization/grounding/view.py | 335 | 332 | 0x1.cbb5d32f6d529p+0 | 0x1.cbb5d32f6d528p+0 | 3 |
| src/devtools/core/identity/__init__.py | 336 | 333 | 0x1.ca4ada9c3aa15p+0 | 0x1.c0b652fd5fffbp+0 | 3 |
| src/devtools/core/system/__init__.py | 337 | 335 | 0x1.c51cfd4694c62p+0 | 0x1.bba42cf4b44b6p+0 | 2 |
| src/devtools/context/retrieval/repository_map/ranking.py | 338 | 334 | 0x1.bf1497f477183p+0 | 0x1.bf1497f477183p+0 | 4 |
| src/devtools/core/regex/__init__.py | 339 | 336 | 0x1.be2e1b8d335d5p+0 | 0x1.b4da656d16e26p+0 | 3 |
| src/devtools/models/serving/__init__.py | 340 | 337 | 0x1.bcf1389ff9f36p+0 | 0x1.b3a4224d5007ep+0 | 3 |
| src/devtools/core/time/__init__.py | 341 | 338 | 0x1.bc536fb8e7801p+0 | 0x1.b309a5c6eb773p+0 | 3 |
| src/devtools/agents/integrations/codex/__init__.py | 342 | 339 | 0x1.b9450643db829p+0 | 0x1.b00b975c19767p+0 | 3 |
| src/devtools/context/localization/roles/__init__.py | 343 | 340 | 0x1.b8a9d4fa7f13fp+0 | 0x1.af73a4941bb08p+0 | 3 |
| src/devtools/agents/conversation/__init__.py | 344 | 359 | 0x1.b6dacd6585910p+0 | 0x1.adae4ae09c108p+0 | -15 |
| src/devtools/core/paths/__init__.py | 345 | 370 | 0x1.b6414d79fbea6p+0 | 0x1.ad1800674d3b0p+0 | -25 |
| src/devtools/core/system/detection.py | 346 | 392 | 0x1.b3df79c2fafe1p+0 | 0x1.aac2ec260d29ep+0 | -46 |
| src/devtools/context/python/project_configuration/__init__.py | 347 | 393 | 0x1.b1843e01b625fp+0 | 0x1.a8744c917fdd0p+0 | -46 |
| tests/agents/conversation/__init__.py | 348 | 341 | 0x1.aed213abeda2bp+0 | 0x1.aed213abeda2bp+0 | 7 |
| tests/evaluation/__init__.py | 349 | 342 | 0x1.aed213abeda2bp+0 | 0x1.aed213abeda2bp+0 | 7 |
| tests/observability/evidence/__init__.py | 350 | 343 | 0x1.aed213abeda2bp+0 | 0x1.aed213abeda2bp+0 | 7 |
| tests/persistence/__init__.py | 351 | 344 | 0x1.aed213abeda2bp+0 | 0x1.aed213abeda2bp+0 | 7 |
| tests/agents/__init__.py | 352 | 346 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/agents/integrations/__init__.py | 353 | 347 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/agents/integrations/codex/__init__.py | 354 | 348 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/context/repository/__init__.py | 355 | 349 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/context/retrieval/graph/__init__.py | 356 | 350 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/core/__init__.py | 357 | 351 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/execution/__init__.py | 358 | 352 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/models/__init__.py | 359 | 353 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/models/benchmarks/__init__.py | 360 | 354 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/models/interaction/__init__.py | 361 | 355 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/models/serving/__init__.py | 362 | 356 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/observability/__init__.py | 363 | 357 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/resources/__init__.py | 364 | 358 | 0x1.ae31fb43bc4b7p+0 | 0x1.ae31fb43bc4b8p+0 | 6 |
| tests/context/localization/association/__init__.py | 365 | 360 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/context/python/__init__.py | 366 | 361 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/context/python/function/__init__.py | 367 | 362 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/context/retrieval/__init__.py | 368 | 363 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/context/retrieval/repository_map/__init__.py | 369 | 364 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/core/identity/__init__.py | 370 | 365 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/core/paths/__init__.py | 371 | 366 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/core/system/__init__.py | 372 | 367 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/core/time/__init__.py | 373 | 368 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/models/interaction/providers/__init__.py | 374 | 369 | 0x1.ad9259ab759fep+0 | 0x1.ad9259ab759ffp+0 | 5 |
| tests/context/localization/generation/__init__.py | 375 | 371 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/localization/grounding/__init__.py | 376 | 372 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/localization/roles/__init__.py | 377 | 373 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/localization/routing/__init__.py | 378 | 374 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/python/project_configuration/__init__.py | 379 | 375 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/python/references/__init__.py | 380 | 376 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/python/references/declarations/__init__.py | 381 | 377 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/core/regex/__init__.py | 382 | 378 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/resources/commands/__init__.py | 383 | 379 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/tools/__init__.py | 384 | 380 | 0x1.acf32e5f079c1p+0 | 0x1.acf32e5f079c2p+0 | 4 |
| tests/context/__init__.py | 385 | 381 | 0x1.ac5478db23b1cp+0 | 0x1.ac5478db23b1dp+0 | 4 |
| tests/context/localization/resolution/__init__.py | 386 | 382 | 0x1.ac5478db23b1cp+0 | 0x1.ac5478db23b1dp+0 | 4 |
| tests/context/planning/__init__.py | 387 | 383 | 0x1.ac5478db23b1cp+0 | 0x1.ac5478db23b1dp+0 | 4 |
| tests/context/python/imports/__init__.py | 388 | 384 | 0x1.ac5478db23b1cp+0 | 0x1.ac5478db23b1dp+0 | 4 |
| tests/core/conversion/__init__.py | 389 | 385 | 0x1.ac5478db23b1cp+0 | 0x1.ac5478db23b1dp+0 | 4 |
| tests/agents/conversation/history/__init__.py | 390 | 386 | 0x1.abb6389d3d600p+0 | 0x1.abb6389d3d600p+0 | 4 |
| tests/agents/conversation/message/__init__.py | 391 | 387 | 0x1.abb6389d3d600p+0 | 0x1.abb6389d3d600p+0 | 4 |
| tests/context/localization/__init__.py | 392 | 388 | 0x1.abb6389d3d600p+0 | 0x1.abb6389d3d600p+0 | 4 |
| tests/context/python/classes/__init__.py | 393 | 389 | 0x1.abb6389d3d600p+0 | 0x1.abb6389d3d600p+0 | 4 |
| tests/context/python/modules/__init__.py | 394 | 390 | 0x1.abb6389d3d600p+0 | 0x1.abb6389d3d600p+0 | 4 |
| tests/context/retrieval/lexical/__init__.py | 395 | 391 | 0x1.ab186d2388ccbp+0 | 0x1.ab186d2388ccbp+0 | 4 |
| src/devtools/models/interaction/providers/llama_cpp_request_settings.py | 396 | 396 | 0x1.aa990d1c69782p+0 | 0x1.a1ae221dc2f2ap+0 | 0 |
| src/devtools/agents/integrations/codex/docs/overview.md | 397 | 395 | 0x1.a53f0455cab31p+0 | 0x1.a53f0455cab33p+0 | 2 |
| docs/backlog/items/B-0030-investigate-provider-neutral-generative-model-interaction.md | 398 | 399 | 0x1.9f8b71997631fp+0 | 0x1.96dbad1cfdd57p+0 | -1 |
| docs/backlog/items/B-0029-investigate-reusable-agent-definition-runtime-orchestration.md | 399 | 401 | 0x1.9a3aec53063cep+0 | 0x1.91a798994ba47p+0 | -2 |
| docs/backlog/items/B-0045-establish-minimal-model-interaction-core.md | 400 | 402 | 0x1.9a3aec53063cep+0 | 0x1.91a798994ba47p+0 | -2 |
| tests/core/paths/test_errors.py | 401 | 397 | 0x1.98d4b8fd96a20p+0 | 0x1.98d4b8fd96a20p+0 | 4 |
| tests/execution/test_interaction_attempt.py | 402 | 398 | 0x1.98b772fe40104p+0 | 0x1.98b772fe40104p+0 | 4 |
| docs/backlog/items/B-0043-investigate-reusable-agent-semantics.md | 403 | 403 | 0x1.98a986ee5569cp+0 | 0x1.901e9741dcac6p+0 | 0 |
| src/devtools/agents/conversation/docs/conversation.md | 404 | 404 | 0x1.9489fcb68a955p+0 | 0x1.8c151db5e3f8ap+0 | 0 |
| src/devtools/context/planning/materialization.py | 405 | 400 | 0x1.93431869313e9p+0 | 0x1.93431869313e8p+0 | 5 |
| docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md | 406 | 405 | 0x1.920105f1f0c99p+0 | 0x1.8999b7d7865c4p+0 | 1 |
| src/devtools/observability/evidence/model_interaction.py | 407 | 407 | 0x1.8e9ab280e891ap+0 | 0x1.864595e869f39p+0 | 0 |
| tests/core/system/test_detection.py | 408 | 406 | 0x1.891aca1daea85p+0 | 0x1.891aca1daea85p+0 | 2 |
| docs/backlog/epics/B-0003-local-coding-worker-harness.md | 409 | 410 | 0x1.80a637076e52ep+0 | 0x1.789bc866a71ccp+0 | -1 |
| docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md | 410 | 411 | 0x1.803045d504627p+0 | 0x1.78284e5daecdcp+0 | -1 |
| tests/observability/evidence/test_terminal.py | 411 | 409 | 0x1.7e73917435055p+0 | 0x1.7e73917435054p+0 | 2 |
| docs/backlog/items/B-0036-investigate-action-request-semantics.md | 412 | 413 | 0x1.7abeb1136de02p+0 | 0x1.72d3db4abfad6p+0 | -1 |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 413 | 414 | 0x1.78f6e641bb406p+0 | 0x1.7115979f8e515p+0 | -1 |
| tests/core/system/test_models.py | 414 | 412 | 0x1.72f64e575df98p+0 | 0x1.72f64e575df9ap+0 | 2 |
| docs/backlog/items/B-0016-define-framework-live-harness-acceptance.md | 415 | 415 | 0x1.6dec7c1f22649p+0 | 0x1.6dec7c1f22649p+0 | 0 |
| src/devtools/context/localization/assessment.py | 416 | 416 | 0x1.5c7570eef9569p+0 | 0x1.5c7570eef9567p+0 | 0 |
| tests/agents/conversation/test_session_id.py | 417 | 417 | 0x1.4fab2411c53e4p+0 | 0x1.4fab2411c53e5p+0 | 0 |
| README.md | 418 | 418 | 0x1.4cc5b170a6acbp+0 | 0x1.45d0e0e313f71p+0 | 0 |
| src/devtools/agents/conversation/message.py | 419 | 419 | 0x1.48580ae7d7ba8p+0 | 0x1.417aed076b041p+0 | 0 |
| src/devtools/core/time/models/stopwatch.py | 420 | 420 | 0x1.47ac4eacf78afp+0 | 0x1.40d2c7d50229cp+0 | 0 |
| tests/core/paths/test_resolved_path.py | 421 | 421 | 0x1.38fb288e3003dp+0 | 0x1.38fb288e3003dp+0 | 0 |
| src/devtools/persistence/_snapshot.py | 422 | 422 | 0x1.2b3e5e5c6751dp+0 | 0x1.24fcfb0e9cad4p+0 | 0 |
| src/devtools/execution/runtime.py | 423 | 423 | 0x1.20ff93eb1b3a8p+0 | 0x1.1af5045a8015dp+0 | 0 |
| src/devtools/core/identity/models.py | 424 | 425 | 0x1.1a8261a1880e4p+0 | 0x1.04e55193333f5p-1 | -1 |
| src/devtools/execution/interaction_attempt.py | 425 | 424 | 0x1.075eeead2fc21p+0 | 0x1.01dd8417485f3p+0 | 1 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| tests | 189 | 0 | 189 | 0x1.007092e93e048p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.007092e93e048p+0 |
| resources | 164 | 0 | 164 | 0x1.24a8817f9f650p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.24a8817f9f650p+0 |
| filesystem | 86 | 1 | 86 | 0x1.c934d423c47f9p+0 | 0x1.75cd12aa84bc2p+2 | 0x1.c934d423c47f9p+0 |
| test_reading | 0 | 1 | 1 | 0x1.bc1cbc9538c85p+2 | 0x1.75cd12aa84bc2p+2 | 0x1.75cd12aa84bc2p+2 |
| py | 86 | 0 | 86 | 0x1.c934d423c47f9p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.c934d423c47f9p+0 |
| codecs | 12 | 1 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.dc3559ab98bd6p+1 |
| models | 174 | 11 | 178 | 0x1.158cf3ff4cc93p+0 | 0x1.e6e1994d5651ap+1 | 0x1.0fbfa7879d5bep+0 |
| empty | 82 | 0 | 82 | 0x1.d553b43b5333ep+0 | 0x1.bc1cbc9538c85p+2 | 0x1.d553b43b5333ep+0 |
| zero | 47 | 0 | 47 | 0x1.3154090ab9f44p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.3154090ab9f44p+1 |
| exact | 133 | 0 | 133 | 0x1.5a1d04be70330p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.5a1d04be70330p+0 |
| over | 48 | 0 | 48 | 0x1.2ea9580dc811ap+1 | 0x1.bc1cbc9538c85p+2 | 0x1.2ea9580dc811ap+1 |
| limit | 23 | 0 | 23 | 0x1.8b67d63162854p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.8b67d63162854p+1 |
| negative | 33 | 0 | 33 | 0x1.5e061b056f6afp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.5e061b056f6afp+1 |
| unbounded | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| growth | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| stat | 4 | 0 | 4 | 0x1.2f7d68bfd0b00p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.2f7d68bfd0b00p+2 |
| short | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| reads | 16 | 0 | 16 | 0x1.b8abe9dd16039p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.b8abe9dd16039p+1 |
| eof | 2 | 0 | 2 | 0x1.551bb4b582938p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.551bb4b582938p+2 |
| closure | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| permission | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| multibyte | 0 | 0 | 0 | 0x1.bc1cbc9538c85p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.bc1cbc9538c85p+2 |
| utf | 95 | 0 | 95 | 0x1.afddf489c6f2cp+0 | 0x1.bc1cbc9538c85p+2 | 0x1.afddf489c6f2cp+0 |
| 8 | 114 | 0 | 114 | 0x1.816a8a9810f09p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.816a8a9810f09p+0 |
| invalid | 58 | 0 | 58 | 0x1.16aa8ecc889aep+1 | 0x1.bc1cbc9538c85p+2 | 0x1.16aa8ecc889aep+1 |
| format | 36 | 0 | 36 | 0x1.530bb2c62b93dp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.530bb2c62b93dp+1 |
| override | 12 | 0 | 12 | 0x1.dc3559ab98bd6p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.dc3559ab98bd6p+1 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804"
    ],
    "exited": [
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e"
    ],
    "inversion_count": 2,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.18ae04301f775p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.187bb0f87a299p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.9299bd2a6e000p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.0fc613928606dp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.1865ea6cf9e1ap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x1.13fadb4e7b5a0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.db919dd148cbdp+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.db919dd148cbep+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.97d2041bb7449p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.9723b002c1c13p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "-0x1.5ca831eb06c00p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.7bc8d6204dddbp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.7b4b7dc436661p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.f561705dde800p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.65aa932eb327ep+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.6527d69e0842ep+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "-0x1.05792155ca000p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.44f638b669686p+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.2a6b7840068f8p+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8e0p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.3e929813d798dp+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.3e071a6db795bp+4"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "-0x1.16fb4c4006400p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.3d6bc1bc07ee2p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.3cccc7f69dff1p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "score_delta": {
          "float_hex": "-0x1.3df38ad3de200p-5"
        },
        "upward_positions": 1
      }
    ],
    "pair_inversions": [
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804"
      ]
    ],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
    ],
    "exited": [
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430"
    ],
    "inversion_count": 11,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.18ae04301f775p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.187bb0f87a299p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.9299bd2a6e000p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.0fc613928606dp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.1865ea6cf9e1ap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x1.13fadb4e7b5a0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.db919dd148cbdp+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.db919dd148cbep+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.97d2041bb7449p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.9723b002c1c13p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "-0x1.5ca831eb06c00p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.7bc8d6204dddbp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.7b4b7dc436661p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.f561705dde800p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.65aa932eb327ep+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.6527d69e0842ep+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "-0x1.05792155ca000p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.44f638b669686p+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.2a6b7840068f8p+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8e0p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.3e929813d798dp+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.3e071a6db795bp+4"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "-0x1.16fb4c4006400p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.3d6bc1bc07ee2p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.3cccc7f69dff1p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "score_delta": {
          "float_hex": "-0x1.3df38ad3de200p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.3b19928c9cf8fp+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.3a86879f61af2p+4"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "-0x1.2615da7693a00p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.3991d4475ffa1p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.395b572230427p+4"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "-0x1.b3e9297dbd000p-7"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.3282bd3a3859ap+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.3237c3645ae88p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "-0x1.2be75775c4800p-6"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.2f72d2368db47p+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.2f72d2368db47p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.27f188ccc44d2p+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.27f188ccc44d2p+4"
        },
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.25b769aebfbe1p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.2513258ae4afcp+4"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "-0x1.488847b61ca00p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.1db3d2bdc5a2cp+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.1d68cb7b92ce4p+4"
        },
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "score_delta": {
          "float_hex": "-0x1.2c1d08cb52000p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.1c7db2106fc44p+4"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.016f33cb362c5p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
        "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "score_delta": {
          "float_hex": "-0x1.b0e7e453997f0p+0"
        },
        "upward_positions": -10
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.1c4bf5402a1fbp+4"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.0a39cccc2bcd8p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.2122873fe5230p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.1bdd039b41e26p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.1bdd039b41e26p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.1994cb1aba865p+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.18dd08ffb669cp+4"
        },
        "address": "src/devtools/resources/filesystem/models/json/base.py",
        "content_identity": "89fba795bd6520450dd333141f6b9c79d77e27549026642f901f7bf07a817cc7",
        "document_identity": "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3",
        "score_delta": {
          "float_hex": "-0x1.6f84360839200p-5"
        },
        "upward_positions": 2
      }
    ],
    "pair_inversions": [
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
      ]
    ],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 24,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.18ae04301f775p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.187bb0f87a299p+5"
        },
        "address": "src/devtools/resources/filesystem/reading.py",
        "content_identity": "9ffd4595f59e0402287b4493741254b9814e7e8d27b01576a6236179c2afec01",
        "document_identity": "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
        "score_delta": {
          "float_hex": "-0x1.9299bd2a6e000p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.0fc613928606dp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.1865ea6cf9e1ap+5"
        },
        "address": "tests/resources/filesystem/test_reading.py",
        "content_identity": "e0265fd4fe72d258cce383f0b607bfda687c0ae489bf015ba9e8d906f80647d5",
        "document_identity": "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
        "score_delta": {
          "float_hex": "0x1.13fadb4e7b5a0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.db919dd148cbdp+4"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.db919dd148cbep+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-48"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.97d2041bb7449p+4"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.9723b002c1c13p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "-0x1.5ca831eb06c00p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.7bc8d6204dddbp+4"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.7b4b7dc436661p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.f561705dde800p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.65aa932eb327ep+4"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.6527d69e0842ep+4"
        },
        "address": "src/devtools/resources/filesystem/writing.py",
        "content_identity": "f9e3cc418c545297432601f5ac7072d7688e0c9be2ce07a9df81131852c2e527",
        "document_identity": "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
        "score_delta": {
          "float_hex": "-0x1.05792155ca000p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.55b3dc94f2734p+4"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.532848ed241a1p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_csv.py",
        "content_identity": "03c6c0354c2f9bd810f4c4bee2f626c7eaed64999bacd3d68ea4a054d9a2c988",
        "document_identity": "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.44f638b669686p+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.2a6b7840068f8p+4"
        },
        "address": "src/devtools/tools/filesystem.py",
        "content_identity": "c2810fc51756bf158b8061382cf09b2447121fe2c7f17e75cb2f6037b397300c",
        "document_identity": "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "score_delta": {
          "float_hex": "-0x1.a8ac07662d8e0p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.3e929813d798dp+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.3e071a6db795bp+4"
        },
        "address": "src/devtools/resources/filesystem/models/text.py",
        "content_identity": "beffe8d57eaed9c504a35747390aa3b6006ed87ac8e2cf4c2f9cecb8aa4e634b",
        "document_identity": "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
        "score_delta": {
          "float_hex": "-0x1.16fb4c4006400p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.3d6bc1bc07ee2p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.3cccc7f69dff1p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/json.md",
        "content_identity": "7e2637e483989a226f345ae02f5e04e6c766fe8cc62151082dfd71374eaaaf5b",
        "document_identity": "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
        "score_delta": {
          "float_hex": "-0x1.3df38ad3de200p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.3b19928c9cf8fp+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.3a86879f61af2p+4"
        },
        "address": "tests/resources/filesystem/test_models.py",
        "content_identity": "5a9a3f3c1611790e5141d512c75ffe72e106eeff303c9512fa9e5332288bba58",
        "document_identity": "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
        "score_delta": {
          "float_hex": "-0x1.2615da7693a00p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.3991d4475ffa1p+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.395b572230427p+4"
        },
        "address": "tests/context/repository/test_discovery.py",
        "content_identity": "504d86f0d3f8395f67d20431c527a5836663688feb0b96fa3f1a45cc10aeee68",
        "document_identity": "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
        "score_delta": {
          "float_hex": "-0x1.b3e9297dbd000p-7"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.3282bd3a3859ap+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.3237c3645ae88p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_json.py",
        "content_identity": "1b03c4f7a0c8a8da3c91f921e9a58743a0674e185b2b1b7e479a583e90ebf7e4",
        "document_identity": "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
        "score_delta": {
          "float_hex": "-0x1.2be75775c4800p-6"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.2f72d2368db47p+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.2f72d2368db47p+4"
        },
        "address": "tests/resources/filesystem/codecs/test_markdown.py",
        "content_identity": "a1a56af67b293df9d5fd6bafbf91dbc0b8d011e891b50529a629e3ebb219ac0d",
        "document_identity": "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.27f188ccc44d2p+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.27f188ccc44d2p+4"
        },
        "address": "tests/context/python/function/test_declaration_aggregation.py",
        "content_identity": "ee6ccca5470a6387d5efcfe23d8b13248fde8e0af262de2e0eb16db11c1861ab",
        "document_identity": "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.25b769aebfbe1p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.2513258ae4afcp+4"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "-0x1.488847b61ca00p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.1db3d2bdc5a2cp+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.1d68cb7b92ce4p+4"
        },
        "address": "tests/context/python/function/test_resource_selection.py",
        "content_identity": "0aff6abae3a77e9e3b186c9bcad44483c40db0bbf0e29908020044e9e319506f",
        "document_identity": "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
        "score_delta": {
          "float_hex": "-0x1.2c1d08cb52000p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.1c7db2106fc44p+4"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.016f33cb362c5p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/codecs.md",
        "content_identity": "69b1c8f5a7e4a5bd6d248285868c2c178b20f12718f06d672507a23569a29da0",
        "document_identity": "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "score_delta": {
          "float_hex": "-0x1.b0e7e453997f0p+0"
        },
        "upward_positions": -10
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.1c4bf5402a1fbp+4"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.0a39cccc2bcd8p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.2122873fe5230p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.1bdd039b41e26p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.1bdd039b41e26p+4"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.1994cb1aba865p+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.18dd08ffb669cp+4"
        },
        "address": "src/devtools/resources/filesystem/models/json/base.py",
        "content_identity": "89fba795bd6520450dd333141f6b9c79d77e27549026642f901f7bf07a817cc7",
        "document_identity": "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3",
        "score_delta": {
          "float_hex": "-0x1.6f84360839200p-5"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.179dfa8733eeap+4"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.179dfa8733eeap+4"
        },
        "address": "src/devtools/agents/integrations/codex/docs/cli.md",
        "content_identity": "30da5294ca3dd463bf205be41bc2b59f793b6ca4a833c87fc31a55b05f5a5294",
        "document_identity": "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.1425437babc4cp+4"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.13e2e99b26dbcp+4"
        },
        "address": "tests/context/python/function/test_candidates.py",
        "content_identity": "71203dab41b8c017cd280d1bfd1097ca3abe63f7be2215c8e8749bf5a5225f0d",
        "document_identity": "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
        "score_delta": {
          "float_hex": "-0x1.09678213a4000p-6"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.107cf6d733b42p+4"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.1006680c870b9p+4"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "-0x1.da3b2ab2a2400p-6"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.0e039784364c4p+4"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.0d708c96fb026p+4"
        },
        "address": "src/devtools/resources/filesystem/codecs/markdown.py",
        "content_identity": "3662893e3f5974d201e647f00d32ac4acdac70530920847e0f5b171c1515970c",
        "document_identity": "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
        "score_delta": {
          "float_hex": "-0x1.2615da7693c00p-5"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.0bfdd85418bfep+4"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.0bb044485a866p+4"
        },
        "address": "tests/context/python/test_source_candidacy.py",
        "content_identity": "5b03f561a6f3b381907c8f953b4908ca59a9b7219f3c6c1b2fbde0ad02d26a6a",
        "document_identity": "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
        "score_delta": {
          "float_hex": "-0x1.36502ef8e6000p-6"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.0508d8743120dp+4"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.0508d8743120dp+4"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.02e85d5b9cfb5p+4"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.02e85d5b9cfb4p+4"
        },
        "address": "tests/context/python/function/test_retrieval.py",
        "content_identity": "9f34ccca57fce7274073fe508ea8ce5d98ac799e316097a9cb6501fae8802b35",
        "document_identity": "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.010c39c6b057fp+4"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.00cd39b855396p+4"
        },
        "address": "tests/resources/filesystem/test_writing.py",
        "content_identity": "de8cff71e66e5e6a0830eef1bcd6471b22562e05eb5a4963841409ecb58c80c7",
        "document_identity": "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
        "score_delta": {
          "float_hex": "-0x1.f80072d8f4800p-7"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.ffabd02ef1f94p+3"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.fe555eb0b743bp+3"
        },
        "address": "tests/core/paths/test_resolution.py",
        "content_identity": "5f34ec0ac3a2580a7a75533d98c503e65084bf00f49f9d736b8c11f0b3ecbeb2",
        "document_identity": "3339ce5906f32477be6a3261caf7eb2c73fa7186b78ed2be80d23a9dde3fd90f",
        "score_delta": {
          "float_hex": "-0x1.56717e3ab5900p-5"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.ff6679ca9cbfcp+3"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.ff0c22d182615p+3"
        },
        "address": "tests/models/interaction/providers/test_llama_cpp.py",
        "content_identity": "9afd330cd214f11fe7c6d14cf125d24099b5e26d600804b5141419348885c8ce",
        "document_identity": "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
        "score_delta": {
          "float_hex": "-0x1.695be46979c00p-7"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.ed6482bd78c53p+3"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.ec78704c8fb2fp+3"
        },
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "score_delta": {
          "float_hex": "-0x1.d824e1d224800p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.e65da05185354p+3"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.e5710899ccab6p+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/text.py",
        "content_identity": "e408f6ca75508acc25debc8023d15d78e03665c509e7e0c478fddea8ce46b303",
        "document_identity": "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
        "score_delta": {
          "float_hex": "-0x1.d92f6f7113c00p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.e1fdba7fda032p+3"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.e1fdba7fda031p+3"
        },
        "address": "tests/context/python/function/test_materialization.py",
        "content_identity": "d71c206e1b8df47bbb23c1be65177148ee98a0757acd0e789e4e1ee5e2906dc7",
        "document_identity": "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.e1dae09fad36cp+3"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.e1dae09fad36cp+3"
        },
        "address": "tests/context/python/function/test_rendering.py",
        "content_identity": "473398e3a37c321aa451e97f00bef61bf7794a822d95e6f6e3916e4af43eede6",
        "document_identity": "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.e1bf95a2496a3p+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.e1bf95a2496a4p+3"
        },
        "address": "tests/resources/filesystem/codecs/test_text.py",
        "content_identity": "b8f9cc0b3d2ab072dafffca15ce6fe2f507cf6b8e3d8b94bbdf350d86395a3bc",
        "document_identity": "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.dff67cca6fbb0p+3"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.df50ea1a73987p+3"
        },
        "address": "tests/context/python/function/test_request_assembly.py",
        "content_identity": "2e630467829d7e324b7778ed17666113786a6c483b033f8e0b97c92d99bd9b2b",
        "document_identity": "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
        "score_delta": {
          "float_hex": "-0x1.4b255ff845200p-6"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.deb7803fc603ep+3"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.ddb5ac497dcddp+3"
        },
        "address": "tests/models/benchmarks/test_storage.py",
        "content_identity": "a9fcf22fcb76814c755cbcba819c0e8947c082f772b5a7cc9bd0c6c6f6ef8a66",
        "document_identity": "b79f92c5457d7e56bba959136c47edf1ca116bab0410b960053a0925f2e4b729",
        "score_delta": {
          "float_hex": "-0x1.01d3f64836100p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.d4d7a73457320p+3"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.d4d7a73457320p+3"
        },
        "address": "src/devtools/context/python/mirrored_paths.py",
        "content_identity": "bd267c18766fe86cd4cd324078625e5d216a55ec3596909d4300d6188676dcaa",
        "document_identity": "2f4bdfee885af43caa1e6b799a431e73beec183e3cba1a57e2bb0ffe6b046481",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.d4136c7b3cfaap+3"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.d4136c7b3cfabp+3"
        },
        "address": "src/devtools/context/python/function/docs/overview.md",
        "content_identity": "6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d",
        "document_identity": "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.d23093764767dp+3"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.d23093764767ep+3"
        },
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.d1238bcdfc2adp+3"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.d1238bcdfc2adp+3"
        },
        "address": "src/devtools/resources/commands/docs/command.md",
        "content_identity": "dcd243222036d0e93f9714a24354fb59fc7f90b82b063d1f9697d48b7de2c219",
        "document_identity": "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.cf62ae8f941dbp+3"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.cf62ae8f941dcp+3"
        },
        "address": "src/devtools/context/python/classes/docs/overview.md",
        "content_identity": "83660bad67230c9ac59b4b93fd4bd8702a957ff6ef2d96824a509a38c33749e9",
        "document_identity": "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.c61cb7b6520cep+3"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.c61cb7b6520cep+3"
        },
        "address": "src/devtools/context/python/function/rendering.py",
        "content_identity": "eb65b07b1992b931b19178e1b0d78ac08199a97a465d7cc06f17824fb1a62e74",
        "document_identity": "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.c31ba4e1bf4b6p+3"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.c31ba4e1bf4b5p+3"
        },
        "address": "src/devtools/context/python/function/retrieval.py",
        "content_identity": "edbb1905df9fcf9c03fa045772200a719855b3cec38dfd8ecfb486935e91a33a",
        "document_identity": "caf0f8ce539ececd78345c22cbb4e4cc809cb0e0e3b5948301717a0140d4c945",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.b47f843fa7fcap+3"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.b401f56376b45p+3"
        },
        "address": "tests/models/interaction/test_models.py",
        "content_identity": "03eb423890b8178020859d436d5cfb6e1aefdfd26b44036eccda1435206d234d",
        "document_identity": "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
        "score_delta": {
          "float_hex": "-0x1.f63b70c521400p-7"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.b19bff9b389d0p+3"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.b19bff9b389d0p+3"
        },
        "address": "src/devtools/resources/filesystem/codecs/__init__.py",
        "content_identity": "7c815bc2e91f3150ebd9e5551dd30c947ba6313c1a65b9cf310d5d468133b659",
        "document_identity": "1d45046209b8497c2bb47dac04f7e36eedeae6913fedb7092d41b2956470f07f",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.b12cefa9def43p+3"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.b0d0207007268p+3"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.733ce75f36c00p-7"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.b0b0c812e46f7p+3"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.afa4be502412ep+3"
        },
        "address": "src/devtools/core/regex/docs/overview.md",
        "content_identity": "80793fc954738ca10680ea80ae7b5031ef303b295b307fb5f342d1befe290af5",
        "document_identity": "8bb76ffc996af5e90360cfe72c9fdfb95ed8bdfd014de7be4ad895ca0c9b9c7f",
        "score_delta": {
          "float_hex": "-0x1.0c09c2c05c900p-5"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d"
      ],
      [
        "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
        "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42"
      ],
      [
        "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
        "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618"
      ],
      [
        "3339ce5906f32477be6a3261caf7eb2c73fa7186b78ed2be80d23a9dde3fd90f",
        "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25"
      ]
    ],
    "union": [
      "551835eab71031358c40234bf41d6e16d90cf10d0ad1e358d1998fb4cfd1ff40",
      "8e96628d2d763e51d053bc268521086b5fd1028fbeccffe2880daa0e1a67fc33",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "9debf7511d3bba255258ccc96cb0caa83743cc19d8304e87b834d1520af27c0d",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "0d582db704b07685726263e03518dd56002111b0ca8d45d7ccfbdd4ad1d9ec78",
      "afc0c3f533dec2574fcafbba4799bfaa6d4f211da3cbdb20157e609b865e537e",
      "c89523af5e6cd073bb4c9ce5ea6b391a8e800c038216ee6d2e8a51a090b08d48",
      "ab25feb3abd9cec19cd26502fd27d3ee3fdd4a44885998ed2eab3dd567738804",
      "ea3670535c57f1820269c735cfbe119554e2e9dc8a69b802f6e50b9bfb3d6517",
      "3dfc863ddabe8f033c04a59a3b7234a6e1d1e5bddb6bb17ee398c6e69866d4a5",
      "0b6c0e5d8d4b341f22d92fc21fc608be60849c4d1e5ad8db66a699e384517f5d",
      "7b0d6fb2bd3f02a1c40b8ac8123af7c5b005fdc5cef70b0af6abec880f3b8bc0",
      "14372e25aa7cc7180be5b8400d4e3d2898e34f813ca910a5ef6a5ba96dd4de30",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "fdfce6bc2da0a90ee68122f1d16cd6fb6b5684db0af7d4bf9ae5cba20fc3397f",
      "e427f44a84cd2b5ed20d228a06ad4d4e6c917ac21e413d8a4461d47c0c2f6652",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "ad7b71a85b3636a36077191ddde6a061626f8eb09d42b4f07eaeeffac0983cf3",
      "deba77b3708ce2341ba0d8cb68e1e6ed858e79462a01214a71f58867f403506f",
      "384e48b2061b91a481de9dafb493f5c863499819495d9e4b8432713fe40e14e7",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "7046bd2386f5056490abe59642fa0cf490a417d6522d70613d3aecf3c9ee9993",
      "1df24b0f88fe3cfc16d09c8d5a7b242b65f18c7edc8c71238a5bd8041a272618",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "8c0a6608202d979f3517e4fb3f78ed8192b949121b8d31b2c023cc1b90d65754",
      "df6158c13c5b9ae3e025ec4d8f9406c2a099eb791aa1baf723e1be7f3f0abc6e",
      "3339ce5906f32477be6a3261caf7eb2c73fa7186b78ed2be80d23a9dde3fd90f",
      "ff75c7928a33981fcaeb4504a42ec34122792479207957bbfd42c4b520e08f25",
      "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "5cc2d0c08b1afc7ed9ec1bc8c89e8d68f932edbce3cbbce3a3de6528c0c99bb7",
      "95b96313fc74a7f6a3e5caeb20352be2b7483609d2427df6e26f4a0b9db2631c",
      "62823b43ffdc9b7460635c80a1957ec2e2a8007841a292f964687975fcf7ad45",
      "c4aaebcc5cb7bdd2d76161a617aa3d653c143c32f6fdff2caac16b11d6a29e57",
      "014095b3c7bb7bd04e50b89902dded8436291ba82f840904b1d5535da726f810",
      "b79f92c5457d7e56bba959136c47edf1ca116bab0410b960053a0925f2e4b729",
      "2f4bdfee885af43caa1e6b799a431e73beec183e3cba1a57e2bb0ffe6b046481",
      "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
      "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
      "cbe233602d53b557622fbdae88922e3ec2b19fde62c58b6420b69b15dbf3803c",
      "f314cf97f061855c388b7f8d3fbbb30dc290a621feedd4371b0ae7dc1ed638cd",
      "8a2b76d243dde793ba9758a33463932f42bbb1d674065a68a885902b8e6b98e6",
      "caf0f8ce539ececd78345c22cbb4e4cc809cb0e0e3b5948301717a0140d4c945",
      "5f92a0e5f0c2781111fb65005a067d342665db46c8d991cb72b8f82065d81c9a",
      "1d45046209b8497c2bb47dac04f7e36eedeae6913fedb7092d41b2956470f07f",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "8bb76ffc996af5e90360cfe72c9fdfb95ed8bdfd014de7be4ad895ca0c9b9c7f"
    ]
  }
}
```


## Q6: every candidate, exact native A and true BM25F B

| Resource | A rank | B rank | A score hex | B score hex | Upward positions |
|---|---:|---:|---|---|---:|
| src/devtools/resources/filesystem/docs/roadmap.md | 1 | 1 | 0x1.88ef79ca05290p+5 | 0x1.72d27f80783d6p+5 | 0 |
| AGENTS.md | 2 | 3 | 0x1.43ae48ceffde1p+5 | 0x1.3fa47206c835dp+5 | -1 |
| src/devtools/resources/filesystem/docs/overview.md | 3 | 2 | 0x1.3eb5afad9ec8bp+5 | 0x1.404ca6610e6e8p+5 | 1 |
| tests/context/python/project_configuration/test_configuration.py | 4 | 4 | 0x1.3323432e59219p+5 | 0x1.323b82d5bb305p+5 | 0 |
| tests/context/localization/roles/test_evidence.py | 5 | 5 | 0x1.30b052a43d273p+5 | 0x1.2e48dbeb1c3fbp+5 | 0 |
| src/devtools/context/python/docs/overview.md | 6 | 7 | 0x1.13c8945766a65p+5 | 0x1.098b37cab6103p+5 | -1 |
| tests/scripts/test_retrieval_bm25_baseline.py | 7 | 6 | 0x1.0be4c94b4c2c5p+5 | 0x1.0b2fce4da4ff0p+5 | 1 |
| tests/scripts/test_validate_development.py | 8 | 8 | 0x1.02ffc4643be14p+5 | 0x1.005bc2bc4aaf8p+5 | 0 |
| tests/context/retrieval/lexical/test_evaluation.py | 9 | 9 | 0x1.eb8f3095b3a62p+4 | 0x1.ea3b4ae01ecbbp+4 | 0 |
| tests/context/repository/test_document.py | 10 | 10 | 0x1.b4065f830d0b5p+4 | 0x1.b2b46bb5ff99ep+4 | 0 |
| tests/context/localization/roles/test_configuration.py | 11 | 11 | 0x1.b161205042e7ap+4 | 0x1.af8c9e961bb9ap+4 | 0 |
| tests/context/python/project_configuration/test_settings.py | 12 | 12 | 0x1.a9b83ea8a117fp+4 | 0x1.a922cf675cbccp+4 | 0 |
| docs/backlog/overview.md | 13 | 14 | 0x1.a2664e109d53dp+4 | 0x1.988d6bb0dcf52p+4 | -1 |
| src/devtools/resources/filesystem/docs/io.md | 14 | 13 | 0x1.9d1ec47601a26p+4 | 0x1.a0b0c18906526p+4 | 1 |
| tests/context/repository/test_corpus.py | 15 | 15 | 0x1.8be423f3870e8p+4 | 0x1.8a90cf827517ap+4 | 0 |
| src/devtools/core/paths/docs/overview.md | 16 | 16 | 0x1.755e983bd452dp+4 | 0x1.7ba9b45d266d8p+4 | 0 |
| tests/context/localization/roles/test_inputs.py | 17 | 17 | 0x1.707b5492b67c4p+4 | 0x1.6f0c68f27f639p+4 | 0 |
| tests/context/retrieval/lexical/test_analysis.py | 18 | 18 | 0x1.6b1030caaa257p+4 | 0x1.697be93f58adcp+4 | 0 |
| pyproject.toml | 19 | 19 | 0x1.6a97fbd546d99p+4 | 0x1.6978cc2d4a623p+4 | 0 |
| src/devtools/resources/filesystem/docs/models.md | 20 | 22 | 0x1.5fafb7d8d6833p+4 | 0x1.4c5b42d7eb0f6p+4 | -2 |
| tests/context/localization/generation/test_branching.py | 21 | 23 | 0x1.5e55670e0fe3cp+4 | 0x1.4b3926bcf16e8p+4 | -2 |
| src/devtools/context/retrieval/docs/overview.md | 22 | 24 | 0x1.55f15199b1ffbp+4 | 0x1.3d3ad5ade9e68p+4 | -2 |
| tests/context/retrieval/lexical/test_statistics.py | 23 | 20 | 0x1.54fd47405e1abp+4 | 0x1.53e551d9c7430p+4 | 3 |
| tests/context/retrieval/lexical/test_index.py | 24 | 21 | 0x1.4fc70f9726e63p+4 | 0x1.4ed8c6b93cc5cp+4 | 3 |
| tests/context/localization/generation/test_generation.py | 25 | 25 | 0x1.39f0d84ffd813p+4 | 0x1.2ea3e9ffc1b1fp+4 | 0 |
| tests/resources/filesystem/test_resolution.py | 26 | 26 | 0x1.278bd91e27c06p+4 | 0x1.278bd91e27c06p+4 | 0 |
| docs/experiments/qwen38_llama_cpp.md | 27 | 27 | 0x1.243b68c656f3dp+4 | 0x1.22b7f5d32fcbbp+4 | 0 |
| src/devtools/core/paths/docs/resolution.md | 28 | 32 | 0x1.241d08363e057p+4 | 0x1.12f003f5b919ap+4 | -4 |
| tests/context/retrieval/lexical/test_bm25.py | 29 | 28 | 0x1.212e94340a704p+4 | 0x1.2080b4170e177p+4 | 1 |
| src/devtools/context/localization/roles/derivation.py | 30 | 29 | 0x1.1e8b3208c337ep+4 | 0x1.1daa02c0e2978p+4 | 1 |
| src/devtools/context/python/function/docs/overview.md | 31 | 35 | 0x1.177229c0b12a0p+4 | 0x1.00220870513ccp+4 | -4 |
| tests/context/retrieval/lexical/test_filename.py | 32 | 31 | 0x1.13a9f8566e428p+4 | 0x1.13a9f8566e428p+4 | 1 |
| scripts/validate_development.py | 33 | 30 | 0x1.0ffd11415f0c9p+4 | 0x1.194c3c4364a34p+4 | 3 |
| src/devtools/context/python/modules/docs/overview.md | 34 | 38 | 0x1.0cfd7841f03f7p+4 | 0x1.eb540bcafb476p+3 | -4 |
| src/devtools/context/python/references/docs/overview.md | 35 | 41 | 0x1.02a4be2146c8ap+4 | 0x1.e3b6c8a5b9302p+3 | -6 |
| src/devtools/resources/filesystem/models/base.py | 36 | 34 | 0x1.01501a8d6852ep+4 | 0x1.01501a8d6852ep+4 | 2 |
| tests/scripts/qwen/test_llama_cpp_profile.py | 37 | 36 | 0x1.0144b063323bbp+4 | 0x1.fdd72d4ed2eefp+3 | 1 |
| src/devtools/tools/docs/overview.md | 38 | 33 | 0x1.00e53d942244bp+4 | 0x1.073059b5745f7p+4 | 5 |
| README.md | 39 | 37 | 0x1.f287d7c93bbc4p+3 | 0x1.f287d7c93bbc5p+3 | 2 |
| tests/context/python/modules/test_interpretation.py | 40 | 39 | 0x1.e7668dfff8fdap+3 | 0x1.e7668dfff8fdbp+3 | 1 |
| tests/context/localization/grounding/test_grounding.py | 41 | 40 | 0x1.e5d6e78dac844p+3 | 0x1.e5d6e78dac844p+3 | 1 |
| tests/context/python/test_mirrored_paths.py | 42 | 42 | 0x1.d4563e041fa05p+3 | 0x1.d4563e041fa04p+3 | 0 |
| tests/context/python/references/declarations/test_analysis.py | 43 | 45 | 0x1.d2580f88f3d68p+3 | 0x1.d2580f88f3d66p+3 | -2 |
| src/devtools/core/time/docs/timestamps.md | 44 | 49 | 0x1.c84392cfa233ap+3 | 0x1.a5be4090cb2c5p+3 | -5 |
| src/devtools/resources/commands/docs/overview.md | 45 | 43 | 0x1.c69b5fb402a11p+3 | 0x1.d33197f6a6d6ap+3 | 2 |
| src/devtools/core/conversion/docs/overview.md | 46 | 44 | 0x1.c65f172719b3dp+3 | 0x1.d2f54f69bde96p+3 | 2 |
| src/devtools/resources/filesystem/models/binary.py | 47 | 52 | 0x1.c33b2423374cap+3 | 0x1.8d89263add12bp+3 | -5 |
| tests/tools/test_filesystem.py | 48 | 46 | 0x1.bc376c71f108dp+3 | 0x1.bc376c71f108dp+3 | 2 |
| src/devtools/context/python/imports/docs/overview.md | 49 | 51 | 0x1.baabce22434f3p+3 | 0x1.8fabe5590970ap+3 | -2 |
| src/devtools/resources/filesystem/resolution.py | 50 | 47 | 0x1.b5a0976721af0p+3 | 0x1.b5a0976721af0p+3 | 3 |
| tests/context/repository/test_observation.py | 51 | 48 | 0x1.a99767874ac4dp+3 | 0x1.a99767874ac4dp+3 | 3 |
| tests/context/localization/routing/test_routing.py | 52 | 50 | 0x1.997e1a1e21f11p+3 | 0x1.997e1a1e21f11p+3 | 2 |
| tests/scripts/qwen/test_python_function_context_acceptance.py | 53 | 53 | 0x1.8d75693dad124p+3 | 0x1.8d75693dad123p+3 | 0 |
| tests/scripts/qwen/test_patch_proposal_worker_acceptance.py | 54 | 54 | 0x1.895dd3be3bb09p+3 | 0x1.895dd3be3bb08p+3 | 0 |
| tests/context/python/test_source_candidacy.py | 55 | 55 | 0x1.850467dea65f0p+3 | 0x1.850467dea65f1p+3 | 0 |
| tests/context/localization/association/test_hypothesis.py | 56 | 56 | 0x1.848ca2b040cafp+3 | 0x1.848ca2b040cadp+3 | 0 |
| tests/context/python/imports/test_relations.py | 57 | 57 | 0x1.83456f62bb8abp+3 | 0x1.83456f62bb8abp+3 | 0 |
| src/devtools/resources/filesystem/models/__init__.py | 58 | 58 | 0x1.8079560ffe781p+3 | 0x1.8079560ffe781p+3 | 0 |
| src/devtools/resources/filesystem/docs/codecs.md | 59 | 59 | 0x1.800672de6dd71p+3 | 0x1.7b3c73ee77d07p+3 | 0 |
| tests/context/localization/roles/helpers.py | 60 | 63 | 0x1.77c74b2b835a9p+3 | 0x1.754eea8086e04p+3 | -3 |
| tests/context/localization/generation/test_references.py | 61 | 60 | 0x1.76bebec58b9d5p+3 | 0x1.76bebec58b9d6p+3 | 1 |
| tests/context/python/modules/test_membership.py | 62 | 61 | 0x1.7607a8197293ap+3 | 0x1.7607a8197293ap+3 | 1 |
| tests/context/localization/resolution/test_resolution.py | 63 | 62 | 0x1.75b86bf61406ap+3 | 0x1.75b86bf61406ap+3 | 1 |
| src/devtools/context/python/project_configuration/settings.py | 64 | 65 | 0x1.73341c659c3b9p+3 | 0x1.73341c659c3b8p+3 | -1 |
| tests/resources/filesystem/test_models.py | 65 | 67 | 0x1.6f61eb796bf65p+3 | 0x1.6f61eb796bf65p+3 | -2 |
| src/devtools/core/regex/docs/overview.md | 66 | 64 | 0x1.67842b701baa8p+3 | 0x1.741a63b2bfe02p+3 | 2 |
| tests/context/python/classes/test_bases.py | 67 | 69 | 0x1.6536707165fa2p+3 | 0x1.6536707165fa2p+3 | -2 |
| src/devtools/persistence/docs/overview.md | 68 | 66 | 0x1.64a1a36966defp+3 | 0x1.7137dbac0b149p+3 | 2 |
| docs/architecture/decisions/ADR-0004-context-disclosure-planning-and-assembly.md | 69 | 70 | 0x1.649c53b8aabd2p+3 | 0x1.649c53b8aabd3p+3 | -1 |
| src/devtools/core/time/docs/overview.md | 70 | 68 | 0x1.5e62ab5655bafp+3 | 0x1.6af8e398f9f08p+3 | 2 |
| src/devtools/resources/filesystem/codecs/csv.py | 71 | 71 | 0x1.557e1f605131ap+3 | 0x1.5230f17f83a3dp+3 | 0 |
| src/devtools/tools/filesystem.py | 72 | 88 | 0x1.547a5b0c71d59p+3 | 0x1.1f64da1fac23ep+3 | -16 |
| tests/context/localization/test_lexical.py | 73 | 72 | 0x1.502a1964ecccdp+3 | 0x1.502a1964eccccp+3 | 1 |
| src/devtools/context/python/project_configuration/models.py | 74 | 73 | 0x1.49f5be658585bp+3 | 0x1.49f5be658585bp+3 | 1 |
| docs/architecture/decisions/ADR-0003-information-need-retrieval-evidence-and-ranking.md | 75 | 74 | 0x1.48733579d0c44p+3 | 0x1.48733579d0c44p+3 | 1 |
| tests/core/paths/test_resolution.py | 76 | 75 | 0x1.483009b509e72p+3 | 0x1.483009b509e72p+3 | 1 |
| tests/resources/filesystem/test_writing.py | 77 | 76 | 0x1.45157468eba07p+3 | 0x1.45157468eba07p+3 | 1 |
| tests/scripts/test_vllm_benchmark_driver.py | 78 | 77 | 0x1.40ff27ec57b60p+3 | 0x1.40ff27ec57b61p+3 | 1 |
| docs/backlog/epics/B-0015-framework-acceptance-harness-validation.md | 79 | 82 | 0x1.3bbc4bc072e0ap+3 | 0x1.29629e7f707d5p+3 | -3 |
| tests/context/python/imports/test_members.py | 80 | 78 | 0x1.3aba0600cf260p+3 | 0x1.3aba0600cf260p+3 | 2 |
| tests/context/retrieval/graph/test_typed.py | 81 | 80 | 0x1.38a26b41a753fp+3 | 0x1.38a26b41a753fp+3 | 1 |
| tests/context/retrieval/graph/test_ranking.py | 82 | 81 | 0x1.387914ea85117p+3 | 0x1.387914ea85116p+3 | 1 |
| src/devtools/core/system/docs/overview.md | 83 | 79 | 0x1.2e12239ef9588p+3 | 0x1.3aa85be19d8e2p+3 | 4 |
| src/devtools/persistence/docs/json.md | 84 | 83 | 0x1.2663fd1b6b743p+3 | 0x1.2663fd1b6b743p+3 | 1 |
| tests/context/localization/generation/test_imports.py | 85 | 84 | 0x1.24fbb7fd95db2p+3 | 0x1.24fbb7fd95db2p+3 | 1 |
| src/devtools/context/python/mirrored_paths.py | 86 | 85 | 0x1.236874d145206p+3 | 0x1.236874d145206p+3 | 1 |
| src/devtools/resources/commands/execution.py | 87 | 86 | 0x1.22d34e38ff96fp+3 | 0x1.22d34e38ff96ep+3 | 1 |
| tests/context/repository/test_discovery.py | 88 | 87 | 0x1.2060398b31135p+3 | 0x1.2060398b31136p+3 | 1 |
| src/devtools/resources/commands/docs/events.md | 89 | 103 | 0x1.1c3465e78c87bp+3 | 0x1.eab70750de22cp+2 | -14 |
| src/devtools/resources/commands/docs/command.md | 90 | 105 | 0x1.1afac8c0ddebcp+3 | 0x1.e8a3bd7e0e082p+2 | -15 |
| tests/context/python/references/declarations/test_bindings.py | 91 | 89 | 0x1.1a3932e9e6746p+3 | 0x1.1a3932e9e6745p+3 | 2 |
| tests/scripts/qwen/test_two_action_read_only_acceptance.py | 92 | 90 | 0x1.1728ad59fe5b5p+3 | 0x1.1728ad59fe5b5p+3 | 2 |
| src/devtools/persistence/__init__.py | 93 | 91 | 0x1.15cffd9a0c01dp+3 | 0x1.15cffd9a0c01dp+3 | 2 |
| src/devtools/resources/commands/docs/execution.md | 94 | 114 | 0x1.1384fca53d68fp+3 | 0x1.dbfe9fb2056edp+2 | -20 |
| tests/resources/filesystem/models/csv/test_dialect.py | 95 | 93 | 0x1.129aece68ee66p+3 | 0x1.129aece68ee66p+3 | 2 |
| tests/resources/filesystem/codecs/test_markdown.py | 96 | 94 | 0x1.112ff7e4346c3p+3 | 0x1.112ff7e4346c3p+3 | 2 |
| docs/backlog/items/B-0008-investigate-repository-context-discovery.md | 97 | 95 | 0x1.10bd77ff96380p+3 | 0x1.10bd77ff96380p+3 | 2 |
| docs/architecture/decisions/ADR-0002-repository-intelligence-identity-and-derivation.md | 98 | 96 | 0x1.102a15b3ef015p+3 | 0x1.102a15b3ef016p+3 | 2 |
| tests/context/python/function/test_qualified_reference.py | 99 | 97 | 0x1.0aabbbfc05962p+3 | 0x1.0aabbbfc05962p+3 | 2 |
| tests/context/retrieval/repository_map/test_ranking.py | 100 | 98 | 0x1.08de2111eab77p+3 | 0x1.08de2111eab77p+3 | 2 |
| src/devtools/context/planning/docs/overview.md | 101 | 92 | 0x1.0627726cc02a0p+3 | 0x1.12bdaaaf645f8p+3 | 9 |
| src/devtools/context/repository/__init__.py | 102 | 99 | 0x1.03512b921468bp+3 | 0x1.03512b921468ap+3 | 3 |
| tests/context/python/imports/test_resolution.py | 103 | 101 | 0x1.f63c40c02603fp+2 | 0x1.f63c40c02603fp+2 | 2 |
| tests/resources/commands/test_handle.py | 104 | 102 | 0x1.f12e77c8ec5b8p+2 | 0x1.f12e77c8ec5b8p+2 | 2 |
| tests/context/retrieval/test_structural.py | 105 | 104 | 0x1.e91ac78f7e07fp+2 | 0x1.e91ac78f7e07dp+2 | 1 |
| tests/context/python/modules/test_selection.py | 106 | 106 | 0x1.e734a10393892p+2 | 0x1.e734a10393892p+2 | 0 |
| tests/context/python/function/test_resource_selection.py | 107 | 107 | 0x1.e5882de519eecp+2 | 0x1.e5882de519eedp+2 | 0 |
| docs/backlog/items/B-0046-investigate-advanced-model-interaction-provider-pressure.md | 108 | 108 | 0x1.e4e425693a4eap+2 | 0x1.e4e425693a4eap+2 | 0 |
| tests/context/retrieval/test_composition.py | 109 | 109 | 0x1.e3ad292a1757ep+2 | 0x1.e3ad292a1757ep+2 | 0 |
| tests/context/planning/test_plan.py | 110 | 110 | 0x1.dfefd3ebca779p+2 | 0x1.dfefd3ebca778p+2 | 0 |
| tests/resources/filesystem/codecs/test_json.py | 111 | 111 | 0x1.df6d849d31cebp+2 | 0x1.df6d849d31cecp+2 | 0 |
| tests/context/python/function/test_candidates.py | 112 | 112 | 0x1.ddf1abcd62af0p+2 | 0x1.ddf1abcd62af1p+2 | 0 |
| src/devtools/core/identity/docs/overview.md | 113 | 100 | 0x1.dd71a6b31be9cp+2 | 0x1.f69e17386454fp+2 | 13 |
| docs/backlog/epics/B-0001-architecture-documentation-integrity.md | 114 | 113 | 0x1.dc433942d1531p+2 | 0x1.dc433942d1530p+2 | 1 |
| src/devtools/context/retrieval/lexical/evaluation.py | 115 | 115 | 0x1.c4e9b4bc24cb5p+2 | 0x1.c4e9b4bc24cb6p+2 | 0 |
| tests/resources/filesystem/models/markdown/test_file.py | 116 | 116 | 0x1.c4e1581557e08p+2 | 0x1.c4e1581557e07p+2 | 0 |
| tests/context/repository/test_intrinsic_paths.py | 117 | 118 | 0x1.b8fc0401ff98ep+2 | 0x1.b8fc0401ff98fp+2 | -1 |
| tests/models/interaction/test_tools.py | 118 | 119 | 0x1.b3278b8a1ae30p+2 | 0x1.b3278b8a1ae31p+2 | -1 |
| src/devtools/context/__init__.py | 119 | 120 | 0x1.b0ad801715064p+2 | 0x1.b0ad801715063p+2 | -1 |
| src/devtools/resources/filesystem/__init__.py | 120 | 121 | 0x1.aea0fadc58eb6p+2 | 0x1.aea0fadc58eb8p+2 | -1 |
| src/devtools/resources/filesystem/models/json/__init__.py | 121 | 122 | 0x1.adba248468309p+2 | 0x1.adba24846830ap+2 | -1 |
| tests/context/python/function/test_containment.py | 122 | 123 | 0x1.aac41e3faf719p+2 | 0x1.aac41e3faf719p+2 | -1 |
| src/devtools/resources/filesystem/codecs/__init__.py | 123 | 124 | 0x1.aa4b121574744p+2 | 0x1.aa4b121574744p+2 | -1 |
| tests/context/localization/test_kernel.py | 124 | 140 | 0x1.a6b8b4d0ea966p+2 | 0x1.7fb91199e3881p+2 | -16 |
| src/devtools/models/serving/docs/overview.md | 125 | 117 | 0x1.a317515248aaap+2 | 0x1.bc43c1d79115cp+2 | 8 |
| src/devtools/resources/filesystem/models/markdown/__init__.py | 126 | 125 | 0x1.a2045ef966b75p+2 | 0x1.a2045ef966b75p+2 | 1 |
| docs/backlog/metadata.md | 127 | 127 | 0x1.9c1275013a3c1p+2 | 0x1.9c1275013a3c3p+2 | 0 |
| docs/backlog/items/B-0006-reconcile-authoritative-architecture-documentation.md | 128 | 128 | 0x1.9703e6a90b968p+2 | 0x1.9703e6a90b968p+2 | 0 |
| tests/context/python/imports/test_declarations.py | 129 | 130 | 0x1.92aa497a0f85ap+2 | 0x1.92aa497a0f85ap+2 | -1 |
| src/devtools/resources/filesystem/writing.py | 130 | 131 | 0x1.923d8f9d6bb4cp+2 | 0x1.923d8f9d6bb4dp+2 | -1 |
| src/devtools/context/python/function/candidates.py | 131 | 134 | 0x1.8f1bc7a9a9bd5p+2 | 0x1.87fdcee022b12p+2 | -3 |
| tests/context/python/function/test_cross_resource_pipeline.py | 132 | 132 | 0x1.8f09b0e271ba3p+2 | 0x1.8f09b0e271ba2p+2 | 0 |
| tests/tools/test_runtime_integration.py | 133 | 133 | 0x1.8b6011ecb8cf5p+2 | 0x1.8b6011ecb8cf5p+2 | 0 |
| tests/resources/commands/test_errors.py | 134 | 136 | 0x1.8416548629eedp+2 | 0x1.8416548629eedp+2 | -2 |
| src/devtools/agents/integrations/codex/docs/overview.md | 135 | 126 | 0x1.83b3ea575443bp+2 | 0x1.9ce05adc9caefp+2 | 9 |
| src/devtools/context/python/project_configuration/declarations.py | 136 | 137 | 0x1.8306cca877c7cp+2 | 0x1.8306cca877c7bp+2 | -1 |
| src/devtools/resources/filesystem/reading.py | 137 | 138 | 0x1.815c629cf257bp+2 | 0x1.815c629cf257bp+2 | -1 |
| tests/context/python/function/test_materialization.py | 138 | 139 | 0x1.80313768e0d03p+2 | 0x1.80313768e0d02p+2 | -1 |
| src/devtools/models/interaction/docs/overview.md | 139 | 129 | 0x1.7a17014278c88p+2 | 0x1.934371c7c133ap+2 | 10 |
| docs/backlog/items/B-0045-establish-minimal-model-interaction-core.md | 140 | 141 | 0x1.79e3193111095p+2 | 0x1.79e3193111095p+2 | -1 |
| tests/context/python/classes/test_declarations.py | 141 | 142 | 0x1.793d67531f4abp+2 | 0x1.793d67531f4aap+2 | -1 |
| src/devtools/resources/filesystem/models/json/base.py | 142 | 143 | 0x1.792cda9be2e97p+2 | 0x1.792cda9be2e98p+2 | -1 |
| src/devtools/context/repository/observation.py | 143 | 144 | 0x1.76f20430a3f77p+2 | 0x1.76f20430a3f78p+2 | -1 |
| tests/observability/evidence/test_model_interaction.py | 144 | 145 | 0x1.752ab88404bc8p+2 | 0x1.752ab88404bcap+2 | -1 |
| src/devtools/agents/conversation/message.py | 145 | 146 | 0x1.7221e232e0d15p+2 | 0x1.7221e232e0d15p+2 | -1 |
| tests/agents/integrations/codex/test_agent.py | 146 | 147 | 0x1.6f39b12f51608p+2 | 0x1.6f39b12f51608p+2 | -1 |
| src/devtools/models/benchmarks/docs/overview.md | 147 | 135 | 0x1.6c69ecc103d4fp+2 | 0x1.85965d464c401p+2 | 12 |
| src/devtools/resources/filesystem/errors.py | 148 | 148 | 0x1.6b6ed25978b24p+2 | 0x1.6b6ed25978b25p+2 | 0 |
| tests/context/python/function/test_declaration_aggregation.py | 149 | 149 | 0x1.69845ad9f5654p+2 | 0x1.69845ad9f5654p+2 | 0 |
| src/devtools/resources/filesystem/codecs/text.py | 150 | 150 | 0x1.68db231c4016bp+2 | 0x1.68db231c4016bp+2 | 0 |
| src/devtools/resources/filesystem/codecs/markdown.py | 151 | 151 | 0x1.635e3e1c30057p+2 | 0x1.635e3e1c30056p+2 | 0 |
| tests/evaluation/test_coverage.py | 152 | 152 | 0x1.60eb40a1d50a7p+2 | 0x1.60eb40a1d50a7p+2 | 0 |
| tests/scripts/qwen/test_two_read_acceptance.py | 153 | 153 | 0x1.5fa31491565e6p+2 | 0x1.5fa31491565e5p+2 | 0 |
| src/devtools/resources/filesystem/models/json/scalar.py | 154 | 154 | 0x1.5e3283d05f090p+2 | 0x1.5e3283d05f08fp+2 | 0 |
| src/devtools/resources/filesystem/codecs/json.py | 155 | 155 | 0x1.5e0d878e1dc1ep+2 | 0x1.5e0d878e1dc1dp+2 | 0 |
| src/devtools/resources/filesystem/models/markdown/file.py | 156 | 156 | 0x1.5a80c72b5e12ap+2 | 0x1.5a80c72b5e12cp+2 | 0 |
| src/devtools/resources/filesystem/docs/json.md | 157 | 157 | 0x1.52e8f134d91ddp+2 | 0x1.52e8f134d91dep+2 | 0 |
| tests/models/serving/test_llama_cpp.py | 158 | 159 | 0x1.4fce7b15fceb3p+2 | 0x1.4d2be29b28124p+2 | -1 |
| docs/architecture/decisions/ADR-0001-cohesive-model-interaction-boundary.md | 159 | 158 | 0x1.4f096693dfc7fp+2 | 0x1.4f096693dfc7fp+2 | 1 |
| src/devtools/context/localization/roles/models.py | 160 | 160 | 0x1.4dfc29ffaededp+2 | 0x1.4a965dcac2cdbp+2 | 0 |
| src/devtools/context/repository/discovery.py | 161 | 161 | 0x1.45e9aaa8f1b52p+2 | 0x1.45e9aaa8f1b52p+2 | 0 |
| tests/scripts/qwen/test_llama_cpp_service.py | 162 | 162 | 0x1.4550262a5e79bp+2 | 0x1.4550262a5e799p+2 | 0 |
| tests/context/python/function/test_request_assembly.py | 163 | 163 | 0x1.419e0613693f6p+2 | 0x1.419e0613693f6p+2 | 0 |
| src/devtools/resources/filesystem/models/csv.py | 164 | 164 | 0x1.4197543ae0462p+2 | 0x1.4197543ae0463p+2 | 0 |
| src/devtools/models/interaction/providers/llama_cpp.py | 165 | 165 | 0x1.3dbddfca7a144p+2 | 0x1.3dbddfca7a144p+2 | 0 |
| tests/resources/filesystem/test_reading.py | 166 | 166 | 0x1.3d8d50b91e36ep+2 | 0x1.3d8d50b91e36ep+2 | 0 |
| tests/resources/commands/test_execution.py | 167 | 167 | 0x1.3cd9ed0522ce2p+2 | 0x1.3cd9ed0522ce2p+2 | 0 |
| src/devtools/persistence/_snapshot.py | 168 | 168 | 0x1.3914cd66b39c5p+2 | 0x1.3914cd66b39c6p+2 | 0 |
| src/devtools/resources/filesystem/models/json/object.py | 169 | 169 | 0x1.37bd5760af9e5p+2 | 0x1.37bd5760af9e5p+2 | 0 |
| tests/resources/filesystem/test_json_models.py | 170 | 170 | 0x1.345f46ea803fcp+2 | 0x1.345f46ea803fcp+2 | 0 |
| src/devtools/resources/filesystem/models/json/list.py | 171 | 171 | 0x1.320f085c845b7p+2 | 0x1.320f085c845b7p+2 | 0 |
| tests/resources/filesystem/test_json_conversion.py | 172 | 172 | 0x1.2e6c815c50c00p+2 | 0x1.2e6c815c50c00p+2 | 0 |
| tests/resources/filesystem/models/markdown/test_heading.py | 173 | 173 | 0x1.296ddf365741ep+2 | 0x1.296ddf365741ep+2 | 0 |
| tests/agents/conversation/message/test_message.py | 174 | 174 | 0x1.25b18aec93f1dp+2 | 0x1.25b18aec93f1dp+2 | 0 |
| src/devtools/resources/filesystem/models/json/conversion.py | 175 | 175 | 0x1.24c525f3bf7c0p+2 | 0x1.24c525f3bf7bfp+2 | 0 |
| src/devtools/resources/filesystem/models/text.py | 176 | 176 | 0x1.2173a2084eec1p+2 | 0x1.2173a2084eec1p+2 | 0 |
| src/devtools/context/retrieval/fusion.py | 177 | 177 | 0x1.1e702379614e5p+2 | 0x1.1e702379614e5p+2 | 0 |
| tests/resources/filesystem/models/markdown/test_section.py | 178 | 178 | 0x1.189920dd85322p+2 | 0x1.189920dd85321p+2 | 0 |
| tests/models/interaction/providers/test_llama_cpp.py | 179 | 179 | 0x1.13a820fcbb4b5p+2 | 0x1.13a820fcbb4b5p+2 | 0 |
| src/devtools/context/python/modules/interpretation.py | 180 | 180 | 0x1.1054e02c16836p+2 | 0x1.1054e02c16836p+2 | 0 |
| tests/core/paths/test_errors.py | 181 | 182 | 0x1.0f71b023d6ecap+2 | 0x1.0f71b023d6ec9p+2 | -1 |
| src/devtools/models/benchmarks/storage.py | 182 | 184 | 0x1.0ce4e060a4ba8p+2 | 0x1.0ce4e060a4ba8p+2 | -2 |
| tests/resources/filesystem/models/csv/test_row.py | 183 | 185 | 0x1.0c54ee3200685p+2 | 0x1.0c54ee3200685p+2 | -2 |
| tests/core/system/test_detection.py | 184 | 186 | 0x1.0b3dbaf01bfd9p+2 | 0x1.0b3dbaf01bfd9p+2 | -2 |
| docs/backlog/items/B-0035-investigate-tool-facing-capability-exposure.md | 185 | 187 | 0x1.0abe34060ce4ap+2 | 0x1.0abe34060ce4ap+2 | -2 |
| src/devtools/core/paths/resolution.py | 186 | 188 | 0x1.02dc5a2b1aa96p+2 | 0x1.02dc5a2b1aa96p+2 | -2 |
| src/devtools/context/python/project_configuration/resolution.py | 187 | 189 | 0x1.010cf823a671ep+2 | 0x1.010cf823a671ep+2 | -2 |
| tests/resources/commands/test_models.py | 188 | 190 | 0x1.00cf9b09b47d0p+2 | 0x1.00cf9b09b47d1p+2 | -2 |
| src/devtools/context/python/source_candidacy.py | 189 | 191 | 0x1.009d530643cdcp+2 | 0x1.009d530643cddp+2 | -2 |
| src/devtools/context/retrieval/graph/pagerank.py | 190 | 192 | 0x1.ffc257956d5efp+1 | 0x1.ffc257956d5efp+1 | -2 |
| src/devtools/agents/integrations/codex/agent.py | 191 | 193 | 0x1.fdb774c043008p+1 | 0x1.fdb774c043008p+1 | -2 |
| src/devtools/context/retrieval/lexical/__init__.py | 192 | 194 | 0x1.fd91a30ed50dcp+1 | 0x1.fd91a30ed50dap+1 | -2 |
| tests/core/system/test_models.py | 193 | 195 | 0x1.fa371dcd2abf8p+1 | 0x1.fa371dcd2abf9p+1 | -2 |
| docs/backlog/items/B-0043-investigate-reusable-agent-semantics.md | 194 | 196 | 0x1.f8713ed22cf98p+1 | 0x1.f8713ed22cf98p+1 | -2 |
| tests/resources/filesystem/codecs/test_text.py | 195 | 197 | 0x1.f30ab13d46c56p+1 | 0x1.f30ab13d46c58p+1 | -2 |
| docs/backlog/items/B-0020-investigate-capability-operation-model-action-substrate.md | 196 | 198 | 0x1.f0393faa34408p+1 | 0x1.f0393faa34409p+1 | -2 |
| docs/backlog/items/B-0012-investigate-governed-effect-semantics.md | 197 | 199 | 0x1.f01b0b9e73183p+1 | 0x1.f01b0b9e73184p+1 | -2 |
| src/devtools/evaluation/docs/overview.md | 198 | 181 | 0x1.ee0552f873489p+1 | 0x1.102f1a01820f7p+2 | 17 |
| src/devtools/context/localization/routing/docs/overview.md | 199 | 183 | 0x1.eae20727fcaffp+1 | 0x1.0e9d741946c32p+2 | 16 |
| docs/backlog/epics/B-0005-effect-governance.md | 200 | 200 | 0x1.e437b91740a27p+1 | 0x1.e437b91740a25p+1 | 0 |
| tests/agents/conversation/test_session.py | 201 | 201 | 0x1.e384d799176abp+1 | 0x1.e384d799176acp+1 | 0 |
| tests/core/time/test_timing.py | 202 | 202 | 0x1.d8386b154d47ep+1 | 0x1.d8386b154d47fp+1 | 0 |
| tests/agents/conversation/test_session_id.py | 203 | 203 | 0x1.d7bf6ac0f2b58p+1 | 0x1.d7bf6ac0f2b59p+1 | 0 |
| src/devtools/resources/filesystem/models/markdown/section.py | 204 | 204 | 0x1.d601c30d33072p+1 | 0x1.d601c30d33072p+1 | 0 |
| tests/context/python/function/test_declarations.py | 205 | 205 | 0x1.d3efd6231fc6ep+1 | 0x1.d3efd6231fc6ep+1 | 0 |
| tests/models/benchmarks/test_storage.py | 206 | 206 | 0x1.c7837f56fbbbfp+1 | 0x1.c7837f56fbbbep+1 | 0 |
| tests/resources/filesystem/models/csv/test_file.py | 207 | 207 | 0x1.c72a08926d541p+1 | 0x1.c72a08926d541p+1 | 0 |
| src/devtools/context/localization/generation/generate.py | 208 | 208 | 0x1.c4eb9b4b893a4p+1 | 0x1.c4eb9b4b893a4p+1 | 0 |
| src/devtools/core/paths/models.py | 209 | 209 | 0x1.c4ab0a962e9dep+1 | 0x1.c4ab0a962e9dfp+1 | 0 |
| src/devtools/context/retrieval/graph/walk.py | 210 | 210 | 0x1.bf0260fd7034fp+1 | 0x1.bf0260fd70350p+1 | 0 |
| tests/context/python/function/test_disclosure.py | 211 | 211 | 0x1.b9e32b767593ep+1 | 0x1.b9e32b767593dp+1 | 0 |
| tests/core/time/test_models.py | 212 | 212 | 0x1.b979354f91916p+1 | 0x1.b979354f91916p+1 | 0 |
| src/devtools/tools/disclosure.py | 213 | 213 | 0x1.b6d5a19b275a6p+1 | 0x1.b6d5a19b275a7p+1 | 0 |
| tests/execution/test_interaction_attempt.py | 214 | 214 | 0x1.ae875f2bf1a02p+1 | 0x1.ae875f2bf1a02p+1 | 0 |
| tests/core/regex/test_search.py | 215 | 215 | 0x1.a908f81dcfc4dp+1 | 0x1.a908f81dcfc4ep+1 | 0 |
| src/devtools/models/serving/llama_cpp.py | 216 | 217 | 0x1.a5dd04275fafdp+1 | 0x1.a5dd04275fafdp+1 | -1 |
| tests/context/python/function/test_rendering.py | 217 | 218 | 0x1.a5008008552f9p+1 | 0x1.a5008008552f8p+1 | -1 |
| src/devtools/context/python/function/containment.py | 218 | 219 | 0x1.a245d75638003p+1 | 0x1.a245d75638002p+1 | -1 |
| src/devtools/context/localization/resolution/promotion.py | 219 | 220 | 0x1.9bc5fa48a030dp+1 | 0x1.9bc5fa48a030dp+1 | -1 |
| src/devtools/context/localization/assessment.py | 220 | 221 | 0x1.964c29f7e522ap+1 | 0x1.964c29f7e5228p+1 | -1 |
| tests/resources/filesystem/codecs/test_csv.py | 221 | 222 | 0x1.9648ccbfe6c36p+1 | 0x1.9648ccbfe6c35p+1 | -1 |
| tests/context/python/function/test_retrieval.py | 222 | 223 | 0x1.8ad649be45870p+1 | 0x1.8ad649be4586ep+1 | -1 |
| src/devtools/resources/commands/__init__.py | 223 | 224 | 0x1.850390e992f96p+1 | 0x1.850390e992f96p+1 | -1 |
| tests/resources/filesystem/__init__.py | 224 | 225 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | -1 |
| tests/resources/filesystem/codecs/__init__.py | 225 | 226 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | -1 |
| tests/resources/filesystem/models/__init__.py | 226 | 227 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | -1 |
| tests/resources/filesystem/models/markdown/__init__.py | 227 | 228 | 0x1.7e632a7da64bbp+1 | 0x1.7e632a7da64bdp+1 | -1 |
| tests/resources/filesystem/models/csv/__init__.py | 228 | 229 | 0x1.7dd5af5050b5bp+1 | 0x1.7dd5af5050b5dp+1 | -1 |
| src/devtools/models/benchmarks/models.py | 229 | 230 | 0x1.78a80d690aea4p+1 | 0x1.78a80d690aea6p+1 | -1 |
| src/devtools/resources/commands/models/__init__.py | 230 | 231 | 0x1.77196a52a358fp+1 | 0x1.77196a52a358fp+1 | -1 |
| src/devtools/context/localization/association/hypothesis.py | 231 | 232 | 0x1.75cbab1ccf4f1p+1 | 0x1.75cbab1ccf4f2p+1 | -1 |
| src/devtools/context/python/classes/docs/overview.md | 232 | 216 | 0x1.7486f8c886bdep+1 | 0x1.a6dfd9d317943p+1 | 16 |
| tests/execution/test_runtime.py | 233 | 233 | 0x1.72ecd055915d5p+1 | 0x1.72ecd055915d6p+1 | 0 |
| tests/observability/evidence/test_inspection.py | 234 | 234 | 0x1.72df507d80b4bp+1 | 0x1.72df507d80b4bp+1 | 0 |
| tests/models/benchmarks/test_runner.py | 235 | 235 | 0x1.7176c3754dd16p+1 | 0x1.7176c3754dd16p+1 | 0 |
| docs/backlog/items/B-0009-build-bounded-local-coding-worker-harness.md | 236 | 236 | 0x1.6bf4911c970cdp+1 | 0x1.6bf4911c970cfp+1 | 0 |
| tests/core/conversion/test_conversion.py | 237 | 237 | 0x1.6abe42275efd7p+1 | 0x1.6abe42275efdap+1 | 0 |
| src/devtools/core/time/docs/timing.md | 238 | 238 | 0x1.685cccd5f5206p+1 | 0x1.685cccd5f5206p+1 | 0 |
| tests/core/time/test_parsing.py | 239 | 239 | 0x1.671a29ec3605cp+1 | 0x1.671a29ec3605dp+1 | 0 |
| src/devtools/context/repository/snapshot.py | 240 | 240 | 0x1.66b3755ac644dp+1 | 0x1.66b3755ac644ep+1 | 0 |
| docs/backlog/items/B-0027-investigate-serialization-representation-boundaries.md | 241 | 241 | 0x1.65c5d40e10845p+1 | 0x1.65c5d40e10846p+1 | 0 |
| src/devtools/context/repository/corpus.py | 242 | 242 | 0x1.62be302dbebd2p+1 | 0x1.62be302dbebd2p+1 | 0 |
| docs/backlog/items/B-0019-investigate-typed-configuration-ownership.md | 243 | 243 | 0x1.611ece87a1ac6p+1 | 0x1.611ece87a1ac5p+1 | 0 |
| docs/backlog/items/B-0036-investigate-action-request-semantics.md | 244 | 244 | 0x1.60b410f5422d1p+1 | 0x1.60b410f5422d0p+1 | 0 |
| docs/backlog/items/B-0018-investigate-operational-data-minimization-disclosure.md | 245 | 245 | 0x1.5f0b9cf193f66p+1 | 0x1.5f0b9cf193f64p+1 | 0 |
| src/devtools/context/planning/resource.py | 246 | 246 | 0x1.5ac5ed2675cb8p+1 | 0x1.5ac5ed2675cb7p+1 | 0 |
| src/devtools/context/localization/routing/derive.py | 247 | 247 | 0x1.587c8e7ebd11fp+1 | 0x1.587c8e7ebd11fp+1 | 0 |
| src/devtools/context/python/modules/membership.py | 248 | 248 | 0x1.580035c9fcf7ep+1 | 0x1.580035c9fcf7ep+1 | 0 |
| src/devtools/context/retrieval/composition.py | 249 | 249 | 0x1.4d30f3ef2b7b3p+1 | 0x1.4d30f3ef2b7b3p+1 | 0 |
| tests/tools/test_command.py | 250 | 250 | 0x1.3de88bdf8349fp+1 | 0x1.3de88bdf834a0p+1 | 0 |
| src/devtools/context/python/function/retrieval.py | 251 | 251 | 0x1.3a29b24d520c2p+1 | 0x1.3a29b24d520c1p+1 | 0 |
| src/devtools/resources/commands/handle.py | 252 | 252 | 0x1.37ce8e98cddc4p+1 | 0x1.37ce8e98cddc4p+1 | 0 |
| src/devtools/context/retrieval/repository_map/ranking.py | 253 | 253 | 0x1.36ed14a68c82cp+1 | 0x1.36ed14a68c82cp+1 | 0 |
| src/devtools/context/retrieval/repository_map/importance.py | 254 | 254 | 0x1.361ed371cda99p+1 | 0x1.361ed371cda9ap+1 | 0 |
| src/devtools/resources/commands/errors.py | 255 | 255 | 0x1.3253038eba1ddp+1 | 0x1.3253038eba1dcp+1 | 0 |
| tests/persistence/test_json.py | 256 | 256 | 0x1.31dabc58ea47cp+1 | 0x1.31dabc58ea47bp+1 | 0 |
| docs/backlog/items/B-0023-investigate-observability-architecture.md | 257 | 257 | 0x1.3124a46b38987p+1 | 0x1.3124a46b38987p+1 | 0 |
| src/devtools/context/localization/resolution/view.py | 258 | 258 | 0x1.2a47b07188291p+1 | 0x1.2a47b07188291p+1 | 0 |
| tests/resources/commands/test_events.py | 259 | 259 | 0x1.27ce27d577fe6p+1 | 0x1.27ce27d577fe6p+1 | 0 |
| src/devtools/resources/commands/events.py | 260 | 260 | 0x1.1dc3121bb01dbp+1 | 0x1.1dc3121bb01dap+1 | 0 |
| src/devtools/context/localization/roles/configuration.py | 261 | 261 | 0x1.1c225181c4a6dp+1 | 0x1.1c225181c4a6cp+1 | 0 |
| src/devtools/context/retrieval/repository_map/view.py | 262 | 262 | 0x1.1b68184a4d283p+1 | 0x1.1b68184a4d282p+1 | 0 |
| src/devtools/context/localization/resolution/contract.py | 263 | 263 | 0x1.1af7e39fa66fep+1 | 0x1.1af7e39fa66fep+1 | 0 |
| tests/agents/conversation/history/test_history.py | 264 | 264 | 0x1.1a9f457e21d41p+1 | 0x1.1a9f457e21d40p+1 | 0 |
| src/devtools/context/localization/generation/references.py | 265 | 265 | 0x1.19798421cef64p+1 | 0x1.19798421cef64p+1 | 0 |
| src/devtools/context/python/imports/declarations.py | 266 | 266 | 0x1.1720d4a35a386p+1 | 0x1.1720d4a35a386p+1 | 0 |
| src/devtools/context/localization/generation/imports.py | 267 | 267 | 0x1.125455f01c3eap+1 | 0x1.125455f01c3ebp+1 | 0 |
| src/devtools/tools/command.py | 268 | 268 | 0x1.1222b15b43d32p+1 | 0x1.1222b15b43d32p+1 | 0 |
| src/devtools/resources/commands/models/result.py | 269 | 269 | 0x1.09391ad277c56p+1 | 0x1.09391ad277c56p+1 | 0 |
| src/devtools/models/serving/vllm.py | 270 | 270 | 0x1.08cee791465a4p+1 | 0x1.08cee791465a4p+1 | 0 |
| tests/context/retrieval/lexical/_helpers.py | 271 | 271 | 0x1.04c010ae95e28p+1 | 0x1.04c010ae95e28p+1 | 0 |
| src/devtools/context/repository/document.py | 272 | 272 | 0x1.041327c03ea36p+1 | 0x1.041327c03ea36p+1 | 0 |
| src/devtools/context/localization/generation/contract.py | 273 | 273 | 0x1.02420dd70393dp+1 | 0x1.02420dd70393dp+1 | 0 |
| tests/agents/integrations/codex/test_live.py | 274 | 274 | 0x1.01c65c28c0eb0p+1 | 0x1.01c65c28c0eafp+1 | 0 |
| tests/models/interaction/test_models.py | 275 | 275 | 0x1.fef197d888557p+0 | 0x1.fef197d888556p+0 | 0 |
| src/devtools/resources/__init__.py | 276 | 276 | 0x1.e98874d640f88p+0 | 0x1.e98874d640f8ap+0 | 0 |
| tests/agents/conversation/test_live.py | 277 | 277 | 0x1.dc09564c9884bp+0 | 0x1.dc09564c9884bp+0 | 0 |
| src/devtools/context/python/imports/members.py | 278 | 279 | 0x1.d7babbcb40012p+0 | 0x1.d7babbcb40012p+0 | -1 |
| src/devtools/agents/integrations/codex/docs/cli.md | 279 | 280 | 0x1.d09873bc67f95p+0 | 0x1.d09873bc67f95p+0 | -1 |
| docs/backlog/items/B-0026-investigate-runtime-control-lifecycle.md | 280 | 281 | 0x1.c007e4a0ad44ep+0 | 0x1.c007e4a0ad44dp+0 | -1 |
| docs/backlog/items/B-0041-investigate-execution-local-lifecycle-control.md | 281 | 283 | 0x1.b598c2549a16cp+0 | 0x1.b598c2549a16cp+0 | -2 |
| src/devtools/models/benchmarks/runner.py | 282 | 284 | 0x1.a6df44cac7e00p+0 | 0x1.a6df44cac7dffp+0 | -2 |
| src/devtools/context/retrieval/structural.py | 283 | 286 | 0x1.9d0cfeaa22956p+0 | 0x1.9d0cfeaa22956p+0 | -3 |
| src/devtools/context/retrieval/graph/view.py | 284 | 287 | 0x1.95d9a83c95f66p+0 | 0x1.95d9a83c95f66p+0 | -3 |
| src/devtools/agents/conversation/docs/overview.md | 285 | 278 | 0x1.75bfee0214ffap+0 | 0x1.da71b01736ac4p+0 | 7 |
| tests/models/serving/test_vllm.py | 286 | 288 | 0x1.6c11735f29f0ep+0 | 0x1.6c11735f29f0ep+0 | -2 |
| src/devtools/execution/docs/overview.md | 287 | 282 | 0x1.524022d0fb701p+0 | 0x1.b6f1e4e61d1ccp+0 | 5 |
| src/devtools/observability/evidence/docs/overview.md | 288 | 285 | 0x1.409a83b8afbb4p+0 | 0x1.a54c45cdd167ep+0 | 3 |
| src/devtools/context/python/classes/bases.py | 289 | 289 | 0x1.36e4153bee89ep+0 | 0x1.36e4153bee89ep+0 | 0 |
| src/devtools/context/python/classes/declarations.py | 290 | 290 | 0x1.0b15bbf5bef5ap+0 | 0x1.0b15bbf5bef5ap+0 | 0 |
| src/devtools/models/interaction/__init__.py | 291 | 291 | 0x1.7a5a39cf67eb5p-1 | 0x1.7a5a39cf67eb5p-1 | 0 |
| src/devtools/context/python/function/__init__.py | 292 | 292 | 0x1.78c12e3b3a0ebp-1 | 0x1.78c12e3b3a0ecp-1 | 0 |
| src/devtools/context/localization/__init__.py | 293 | 293 | 0x1.7252b04de6123p-1 | 0x1.7252b04de6123p-1 | 0 |
| src/devtools/tools/__init__.py | 294 | 294 | 0x1.6e5f0b34ede56p-1 | 0x1.6e5f0b34ede56p-1 | 0 |
| src/devtools/agents/conversation/__init__.py | 295 | 295 | 0x1.6d19c7b6bbe6fp-1 | 0x1.6d19c7b6bbe6ep-1 | 0 |
| src/devtools/context/planning/__init__.py | 296 | 296 | 0x1.6b5e3571e55ebp-1 | 0x1.6b5e3571e55ecp-1 | 0 |
| src/devtools/observability/evidence/__init__.py | 297 | 297 | 0x1.6a461f1fd096dp-1 | 0x1.6a461f1fd096ep-1 | 0 |
| src/devtools/context/localization/association/__init__.py | 298 | 298 | 0x1.695762c6690dbp-1 | 0x1.695762c6690dbp-1 | 0 |
| src/devtools/context/python/imports/__init__.py | 299 | 299 | 0x1.681afa1741906p-1 | 0x1.681afa1741905p-1 | 0 |
| src/devtools/context/retrieval/__init__.py | 300 | 300 | 0x1.670c891c145e5p-1 | 0x1.670c891c145e6p-1 | 0 |
| src/devtools/context/localization/association/structural.py | 301 | 301 | 0x1.6666f0876fdb7p-1 | 0x1.6666f0876fdb8p-1 | 0 |
| src/devtools/core/time/models/__init__.py | 302 | 302 | 0x1.64f8c62884628p-1 | 0x1.64f8c62884628p-1 | 0 |
| src/devtools/core/time/__init__.py | 303 | 303 | 0x1.645e1adecba2dp-1 | 0x1.645e1adecba2dp-1 | 0 |
| src/devtools/models/interaction/providers/__init__.py | 304 | 304 | 0x1.63f7486397d75p-1 | 0x1.63f7486397d76p-1 | 0 |
| src/devtools/context/localization/routing/models.py | 305 | 305 | 0x1.63dcabe270adfp-1 | 0x1.63dcabe270adfp-1 | 0 |
| src/devtools/agents/integrations/codex/__init__.py | 306 | 306 | 0x1.635d7bbb2a497p-1 | 0x1.635d7bbb2a498p-1 | 0 |
| src/devtools/execution/__init__.py | 307 | 307 | 0x1.632a550769317p-1 | 0x1.632a550769318p-1 | 0 |
| src/devtools/context/localization/resolution/__init__.py | 308 | 308 | 0x1.625e4d24c4fa1p-1 | 0x1.625e4d24c4fa2p-1 | 0 |
| src/devtools/core/paths/__init__.py | 309 | 309 | 0x1.625e4d24c4fa1p-1 | 0x1.625e4d24c4fa2p-1 | 0 |
| src/devtools/context/retrieval/repository_map/__init__.py | 310 | 310 | 0x1.61c5e0ced5c51p-1 | 0x1.61c5e0ced5c51p-1 | 0 |
| src/devtools/context/python/project_configuration/__init__.py | 311 | 311 | 0x1.60c8f97c176afp-1 | 0x1.60c8f97c176b0p-1 | 0 |
| src/devtools/context/localization/grounding/__init__.py | 312 | 312 | 0x1.6031e8c36682dp-1 | 0x1.6031e8c36682ep-1 | 0 |
| src/devtools/context/python/references/declarations/analysis.py | 313 | 313 | 0x1.5fd095de74a1dp-1 | 0x1.5fd095de74a1ep-1 | 0 |
| src/devtools/context/python/modules/__init__.py | 314 | 314 | 0x1.5f3740ed7738ep-1 | 0x1.5f3740ed7738ep-1 | 0 |
| src/devtools/models/interaction/response.py | 315 | 315 | 0x1.5da40c395ecd1p-1 | 0x1.5da40c395ecd1p-1 | 0 |
| src/devtools/context/python/classes/__init__.py | 316 | 316 | 0x1.5ce35423efd5ep-1 | 0x1.5ce35423efd5fp-1 | 0 |
| src/devtools/context/python/function/planned_reference.py | 317 | 317 | 0x1.5b17d2e39b6aap-1 | 0x1.5b17d2e39b6abp-1 | 0 |
| tests/observability/evidence/test_terminal.py | 318 | 318 | 0x1.5a05709b13b06p-1 | 0x1.5a05709b13b06p-1 | 0 |
| src/devtools/context/localization/association/imports.py | 319 | 319 | 0x1.5a02c1305d495p-1 | 0x1.5a02c1305d495p-1 | 0 |
| src/devtools/context/localization/lexical.py | 320 | 320 | 0x1.57065577e9ae6p-1 | 0x1.57065577e9ae6p-1 | 0 |
| src/devtools/context/localization/grounding/contract.py | 321 | 321 | 0x1.56e6f9b8e8787p-1 | 0x1.56e6f9b8e8787p-1 | 0 |
| src/devtools/context/retrieval/repository_map/relevance.py | 322 | 322 | 0x1.56afd2b477526p-1 | 0x1.56afd2b477527p-1 | 0 |
| src/devtools/core/system/__init__.py | 323 | 323 | 0x1.5579f77d22453p-1 | 0x1.5579f77d22454p-1 | 0 |
| src/devtools/context/python/modules/selection.py | 324 | 324 | 0x1.54cd0b3a3cfb1p-1 | 0x1.54cd0b3a3cfb1p-1 | 0 |
| src/devtools/core/conversion/__init__.py | 325 | 325 | 0x1.545f567ec01c8p-1 | 0x1.545f567ec01c8p-1 | 0 |
| src/devtools/context/python/references/declarations/model.py | 326 | 326 | 0x1.52ec4ccc8b980p-1 | 0x1.52ec4ccc8b97ep-1 | 0 |
| src/devtools/core/regex/__init__.py | 327 | 327 | 0x1.52751c2cf166fp-1 | 0x1.52751c2cf166dp-1 | 0 |
| src/devtools/context/localization/routing/__init__.py | 328 | 328 | 0x1.51a4b26c58a04p-1 | 0x1.51a4b26c58a03p-1 | 0 |
| src/devtools/context/python/__init__.py | 329 | 329 | 0x1.51a4b26c58a04p-1 | 0x1.51a4b26c58a03p-1 | 0 |
| src/devtools/context/localization/grounding/view.py | 330 | 330 | 0x1.5186a73d6ed75p-1 | 0x1.5186a73d6ed74p-1 | 0 |
| src/devtools/models/interaction/observation.py | 331 | 331 | 0x1.503d9173404b9p-1 | 0x1.503d9173404b9p-1 | 0 |
| src/devtools/context/localization/roles/__init__.py | 332 | 332 | 0x1.5006dd3e4f760p-1 | 0x1.5006dd3e4f760p-1 | 0 |
| src/devtools/context/python/references/declarations/__init__.py | 333 | 333 | 0x1.4fc246ed2c96dp-1 | 0x1.4fc246ed2c96dp-1 | 0 |
| src/devtools/context/localization/roles/inputs.py | 334 | 334 | 0x1.4f6b3b707f8bbp-1 | 0x1.4f6b3b707f8bcp-1 | 0 |
| src/devtools/context/localization/generation/__init__.py | 335 | 335 | 0x1.4eb104c218ac5p-1 | 0x1.4eb104c218ac5p-1 | 0 |
| src/devtools/observability/evidence/terminal.py | 336 | 336 | 0x1.4ce449095ef9cp-1 | 0x1.4ce449095ef9cp-1 | 0 |
| tests/models/benchmarks/test_models.py | 337 | 337 | 0x1.4cc4b2fd523e6p-1 | 0x1.4cc4b2fd523e6p-1 | 0 |
| src/devtools/context/localization/grounding/resolve.py | 338 | 338 | 0x1.4cc10b9133f1fp-1 | 0x1.4cc10b9133f1fp-1 | 0 |
| src/devtools/context/retrieval/graph/__init__.py | 339 | 339 | 0x1.4c93ae584aeedp-1 | 0x1.4c93ae584aeedp-1 | 0 |
| src/devtools/context/localization/association/references.py | 340 | 340 | 0x1.4a9aad00f458cp-1 | 0x1.4a9aad00f458cp-1 | 0 |
| tests/observability/evidence/test_protocols.py | 341 | 341 | 0x1.4a7d2414944c0p-1 | 0x1.4a7d2414944c0p-1 | 0 |
| src/devtools/context/planning/materialization.py | 342 | 342 | 0x1.47fdb69fc91abp-1 | 0x1.47fdb69fc91abp-1 | 0 |
| tests/models/serving/test_huggingface.py | 343 | 343 | 0x1.47c60ba402212p-1 | 0x1.47c60ba402211p-1 | 0 |
| src/devtools/models/interaction/protocols.py | 344 | 344 | 0x1.46e5abd67e639p-1 | 0x1.46e5abd67e639p-1 | 0 |
| src/devtools/context/python/references/declarations/resolution.py | 345 | 345 | 0x1.455ba0169075ep-1 | 0x1.455ba0169075ep-1 | 0 |
| src/devtools/agents/integrations/codex/models.py | 346 | 346 | 0x1.44610c7a9b3fep-1 | 0x1.44610c7a9b3fep-1 | 0 |
| src/devtools/persistence/json.py | 347 | 347 | 0x1.43982ceb1ce67p-1 | 0x1.43982ceb1ce66p-1 | 0 |
| src/devtools/context/python/modules/declarations.py | 348 | 348 | 0x1.42e6f1dbaf7b4p-1 | 0x1.42e6f1dbaf7b4p-1 | 0 |
| src/devtools/context/python/imports/relations.py | 349 | 349 | 0x1.413c54c3b4c9fp-1 | 0x1.413c54c3b4c9fp-1 | 0 |
| src/devtools/agents/conversation/conversation.py | 350 | 350 | 0x1.4014022b651efp-1 | 0x1.4014022b651f0p-1 | 0 |
| src/devtools/observability/evidence/inspection.py | 351 | 351 | 0x1.3e4c4a17b46eep-1 | 0x1.3e4c4a17b46edp-1 | 0 |
| src/devtools/context/localization/readiness.py | 352 | 352 | 0x1.3def21cc11254p-1 | 0x1.3def21cc11253p-1 | 0 |
| src/devtools/execution/runtime.py | 353 | 353 | 0x1.3994be010f907p-1 | 0x1.3994be010f907p-1 | 0 |
| src/devtools/context/python/function/materialization.py | 354 | 354 | 0x1.329e01013b6dbp-1 | 0x1.329e01013b6dap-1 | 0 |
| src/devtools/context/python/function/request_assembly.py | 355 | 355 | 0x1.31c5a059a026ap-1 | 0x1.31c5a059a026ap-1 | 0 |
| src/devtools/persistence/sqlite.py | 356 | 356 | 0x1.318c8a8e62ddep-1 | 0x1.318c8a8e62ddep-1 | 0 |
| src/devtools/context/python/function/qualified_reference.py | 357 | 357 | 0x1.316d52f757f3cp-1 | 0x1.316d52f757f3bp-1 | 0 |
| tests/__init__.py | 358 | 358 | 0x1.30c171f228454p-1 | 0x1.30c171f228454p-1 | 0 |
| src/devtools/context/python/classes/containment.py | 359 | 359 | 0x1.3042897fac5dbp-1 | 0x1.3042897fac5dbp-1 | 0 |
| tests/agents/conversation/history/__init__.py | 360 | 360 | 0x1.2fe0413d3f4ecp-1 | 0x1.2fe0413d3f4ecp-1 | 0 |
| tests/agents/conversation/message/__init__.py | 361 | 361 | 0x1.2fe0413d3f4ecp-1 | 0x1.2fe0413d3f4ecp-1 | 0 |
| src/devtools/context/retrieval/lexical/bm25.py | 362 | 362 | 0x1.2f8224ef16de4p-1 | 0x1.2f8224ef16de3p-1 | 0 |
| src/devtools/execution/interaction_attempt.py | 363 | 363 | 0x1.2d75844e4ce01p-1 | 0x1.2d75844e4ce01p-1 | 0 |
| src/devtools/core/identity/__init__.py | 364 | 364 | 0x1.2cd63951b20acp-1 | 0x1.2cd63951b20acp-1 | 0 |
| src/devtools/evaluation/__init__.py | 365 | 365 | 0x1.2bfac798cbfe8p-1 | 0x1.2bfac798cbfe8p-1 | 0 |
| src/devtools/context/planning/plan.py | 366 | 366 | 0x1.29be5617a23f6p-1 | 0x1.29be5617a23f7p-1 | 0 |
| src/devtools/core/time/errors.py | 367 | 367 | 0x1.26efef4f55d99p-1 | 0x1.26efef4f55d99p-1 | 0 |
| src/devtools/context/planning/rendering.py | 368 | 368 | 0x1.26a59915afed3p-1 | 0x1.26a59915afed4p-1 | 0 |
| src/devtools/observability/evidence/protocols.py | 369 | 369 | 0x1.247aa66df7bc9p-1 | 0x1.247aa66df7bc9p-1 | 0 |
| src/devtools/context/python/references/__init__.py | 370 | 370 | 0x1.2412c9a8c9df7p-1 | 0x1.2412c9a8c9df7p-1 | 0 |
| src/devtools/models/serving/__init__.py | 371 | 371 | 0x1.2412c9a8c9df7p-1 | 0x1.2412c9a8c9df7p-1 | 0 |
| src/devtools/context/retrieval/lexical/filename.py | 372 | 372 | 0x1.23d93bb07b3fbp-1 | 0x1.23d93bb07b3fcp-1 | 0 |
| src/devtools/core/paths/errors.py | 373 | 373 | 0x1.2143bdd4ed1dcp-1 | 0x1.2143bdd4ed1ddp-1 | 0 |
| src/devtools/context/localization/task.py | 374 | 374 | 0x1.212f09de993d2p-1 | 0x1.212f09de993d1p-1 | 0 |
| src/devtools/context/python/function/disclosure.py | 375 | 375 | 0x1.212f09de993d2p-1 | 0x1.212f09de993d1p-1 | 0 |
| src/devtools/core/system/detection.py | 376 | 376 | 0x1.1e1eb98187804p-1 | 0x1.1e1eb98187803p-1 | 0 |
| tests/core/paths/test_resolved_path.py | 377 | 377 | 0x1.1e0a78222c84bp-1 | 0x1.1e0a78222c84ap-1 | 0 |
| src/devtools/execution/protocols.py | 378 | 378 | 0x1.1cf5565efa49ap-1 | 0x1.1cf5565efa49ap-1 | 0 |
| src/devtools/context/python/modules/lookup.py | 379 | 379 | 0x1.1bce5aeebf366p-1 | 0x1.1bce5aeebf366p-1 | 0 |
| src/devtools/observability/evidence/model_interaction.py | 380 | 380 | 0x1.192e656269477p-1 | 0x1.192e656269477p-1 | 0 |
| src/devtools/tools/execution.py | 381 | 381 | 0x1.18c7464e96595p-1 | 0x1.18c7464e96595p-1 | 0 |
| src/devtools/models/interaction/providers/llama_cpp_request_settings.py | 382 | 382 | 0x1.180814e1110a2p-1 | 0x1.180814e1110a2p-1 | 0 |
| src/devtools/context/python/imports/resolution.py | 383 | 383 | 0x1.13a7aac461acfp-1 | 0x1.13a7aac461ad0p-1 | 0 |
| src/devtools/context/python/references/declarations/bindings.py | 384 | 384 | 0x1.11a480cb9f3a4p-1 | 0x1.11a480cb9f3a4p-1 | 0 |
| src/devtools/core/time/parsing.py | 385 | 385 | 0x1.10870d7ed9b29p-1 | 0x1.10870d7ed9b2ap-1 | 0 |
| tests/agents/integrations/codex/test_parsing.py | 386 | 386 | 0x1.0fa6074b9c56bp-1 | 0x1.0fa6074b9c56ap-1 | 0 |
| src/devtools/context/retrieval/lexical/scoring.py | 387 | 387 | 0x1.0cf180a8dcee5p-1 | 0x1.0cf180a8dcee4p-1 | 0 |
| tests/persistence/test_sqlite.py | 388 | 388 | 0x1.0ba185193afbep-1 | 0x1.0ba185193afbdp-1 | 0 |
| src/devtools/context/repository/identity.py | 389 | 389 | 0x1.054493a91cc72p-1 | 0x1.054493a91cc71p-1 | 0 |
| src/devtools/resources/commands/models/command.py | 390 | 390 | 0x1.0279f4e4c24d6p-1 | 0x1.0279f4e4c24d6p-1 | 0 |
| src/devtools/agents/conversation/history.py | 391 | 391 | 0x1.f4c96bb5881a7p-2 | 0x1.f4c96bb5881a6p-2 | 0 |
| tests/core/regex/test_models.py | 392 | 392 | 0x1.ee520c715bc7bp-2 | 0x1.ee520c715bc7ap-2 | 0 |
| tests/models/interaction/test_protocols.py | 393 | 393 | 0x1.eb6fa7ffd460fp-2 | 0x1.eb6fa7ffd460fp-2 | 0 |
| src/devtools/core/conversion/conversion.py | 394 | 394 | 0x1.e804e179908ccp-2 | 0x1.e804e179908cbp-2 | 0 |
| src/devtools/models/interaction/models.py | 395 | 395 | 0x1.e79f19d025974p-2 | 0x1.e79f19d025975p-2 | 0 |
| src/devtools/context/retrieval/lexical/index.py | 396 | 396 | 0x1.e1e052d12fd30p-2 | 0x1.e1e052d12fd2ep-2 | 0 |
| tests/core/identity/test_models.py | 397 | 397 | 0x1.dc6cb0d66d004p-2 | 0x1.dc6cb0d66d004p-2 | 0 |
| src/devtools/agents/integrations/codex/parsing.py | 398 | 398 | 0x1.dc0bb0102b3cap-2 | 0x1.dc0bb0102b3c9p-2 | 0 |
| src/devtools/context/retrieval/lexical/analysis.py | 399 | 399 | 0x1.c7cc46d80b625p-2 | 0x1.c7cc46d80b625p-2 | 0 |
| src/devtools/context/python/function/declarations.py | 400 | 400 | 0x1.b7308dba14355p-2 | 0x1.b7308dba14355p-2 | 0 |
| src/devtools/core/time/models/stopwatch.py | 401 | 401 | 0x1.ae3053c65e36ep-2 | 0x1.ae3053c65e36ep-2 | 0 |
| src/devtools/context/retrieval/lexical/statistics.py | 402 | 402 | 0x1.ac7026b7977d3p-2 | 0x1.ac7026b7977d3p-2 | 0 |
| src/devtools/context/python/function/rendering.py | 403 | 403 | 0x1.a593573737f61p-2 | 0x1.a593573737f61p-2 | 0 |
| src/devtools/context/localization/obligation.py | 404 | 404 | 0x1.95bc09576d69ep-2 | 0x1.95bc09576d69dp-2 | 0 |
| src/devtools/core/time/models/timestamp.py | 405 | 405 | 0x1.8f93256db5408p-2 | 0x1.8f93256db5409p-2 | 0 |
| src/devtools/core/regex/search.py | 406 | 406 | 0x1.8c31021465ad6p-2 | 0x1.8c31021465ad6p-2 | 0 |
| tests/tools/test_execution.py | 407 | 407 | 0x1.7806c00cc083dp-2 | 0x1.7806c00cc083dp-2 | 0 |
| src/devtools/models/serving/huggingface.py | 408 | 408 | 0x1.666c75d198ab2p-2 | 0x1.666c75d198ab2p-2 | 0 |

### Per-term df and IDF

| Term | Content df | Filename df | Union df | Content IDF hex | Filename IDF hex | Union IDF hex |
|---|---:|---:|---:|---|---|---|
| src | 46 | 0 | 46 | 0x1.340d40cbf6c2bp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.340d40cbf6c2bp+1 |
| devtools | 361 | 0 | 361 | 0x1.6c628f2e1f441p-2 | 0x1.bc1cbc9538c85p+2 | 0x1.6c628f2e1f441p-2 |
| resources | 164 | 0 | 164 | 0x1.24a8817f9f650p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.24a8817f9f650p+0 |
| filesystem | 86 | 1 | 86 | 0x1.c934d423c47f9p+0 | 0x1.75cd12aa84bc2p+2 | 0x1.c934d423c47f9p+0 |
| docs | 28 | 0 | 28 | 0x1.72b6c4f4be458p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.72b6c4f4be458p+1 |
| io | 8 | 1 | 9 | 0x1.06c95e8564cc8p+2 | 0x1.75cd12aa84bc2p+2 | 0x1.ff5618ca265ddp+1 |
| md | 68 | 0 | 68 | 0x1.027789cfc17d0p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.027789cfc17d0p+1 |
| overview | 18 | 28 | 39 | 0x1.aa06ea46c514dp+1 | 0x1.72b6c4f4be458p+1 | 0x1.48ef67f47b624p+1 |
| roadmap | 7 | 1 | 7 | 0x1.0ecc0acace875p+2 | 0x1.75cd12aa84bc2p+2 | 0x1.0ecc0acace875p+2 |
| public | 51 | 0 | 51 | 0x1.26faac7f4f132p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.26faac7f4f132p+1 |
| api | 35 | 0 | 35 | 0x1.5699faa5d6b78p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.5699faa5d6b78p+1 |
| development | 10 | 0 | 10 | 0x1.f2868fe376a59p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.f2868fe376a59p+1 |
| validation | 38 | 1 | 38 | 0x1.4c37a840eb492p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.4c37a840eb492p+1 |
| scripts | 16 | 0 | 16 | 0x1.b8abe9dd16039p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.b8abe9dd16039p+1 |
| validate_development | 3 | 1 | 4 | 0x1.3f92f1dc6f5efp+2 | 0x1.75cd12aa84bc2p+2 | 0x1.2f7d68bfd0b00p+2 |
| py | 86 | 0 | 86 | 0x1.c934d423c47f9p+0 | 0x1.bc1cbc9538c85p+2 | 0x1.c934d423c47f9p+0 |
| pyproject | 16 | 1 | 17 | 0x1.b8abe9dd16039p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.b123d3f972544p+1 |
| toml | 19 | 0 | 19 | 0x1.a349e2a1f0b33p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.a349e2a1f0b33p+1 |
| protected | 7 | 0 | 7 | 0x1.0ecc0acace875p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.0ecc0acace875p+2 |
| ruff | 70 | 0 | 70 | 0x1.fd9104b7f4d9cp+0 | 0x1.bc1cbc9538c85p+2 | 0x1.fd9104b7f4d9cp+0 |
| formatting | 6 | 0 | 6 | 0x1.17f49b3bac65cp+2 | 0x1.bc1cbc9538c85p+2 | 0x1.17f49b3bac65cp+2 |
| mypy | 8 | 0 | 8 | 0x1.06c95e8564cc8p+2 | 0x1.bc1cbc9538c85p+2 | 0x1.06c95e8564cc8p+2 |
| binary | 15 | 1 | 15 | 0x1.c0ac94a15edb0p+1 | 0x1.75cd12aa84bc2p+2 | 0x1.c0ac94a15edb0p+1 |
| formats | 10 | 0 | 10 | 0x1.f2868fe376a59p+1 | 0x1.bc1cbc9538c85p+2 | 0x1.f2868fe376a59p+1 |
| streaming | 9 | 0 | 9 | 0x1.ff5618ca265ddp+1 | 0x1.bc1cbc9538c85p+2 | 0x1.ff5618ca265ddp+1 |
| security | 3 | 0 | 3 | 0x1.3f92f1dc6f5efp+2 | 0x1.bc1cbc9538c85p+2 | 0x1.3f92f1dc6f5efp+2 |

### Complete top-K crossings and inversion identities

```json
{
  "10": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [],
    "exited": [],
    "inversion_count": 2,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.88ef79ca05290p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.72d27f80783d6p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.61cfa498ceba0p+1"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.43ae48ceffde1p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.3fa47206c835dp+5"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.0275b20dea100p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.3eb5afad9ec8bp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.404ca6610e6e8p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x1.96f6b36fa5d00p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.3323432e59219p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.323b82d5bb305p+5"
        },
        "address": "tests/context/python/project_configuration/test_configuration.py",
        "content_identity": "9f59b552d170df0e3f569fa5f91afbfeda52535115543da27a7605bc79ca4ecd",
        "document_identity": "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
        "score_delta": {
          "float_hex": "-0x1.cf80b13be2800p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.30b052a43d273p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2e48dbeb1c3fbp+5"
        },
        "address": "tests/context/localization/roles/test_evidence.py",
        "content_identity": "584ec4bbf88b4e37ab241f6793751b43fc524ce2b34810d693c1119ba1011316",
        "document_identity": "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
        "score_delta": {
          "float_hex": "-0x1.33bb5c9073c00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.13c8945766a65p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.098b37cab6103p+5"
        },
        "address": "src/devtools/context/python/docs/overview.md",
        "content_identity": "c7386d432c3c7501eb8d3bbc7c41db1a3b5199600eb1179341ac6f46202fafd3",
        "document_identity": "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "score_delta": {
          "float_hex": "-0x1.47ab919612c40p+0"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0be4c94b4c2c5p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.0b2fce4da4ff0p+5"
        },
        "address": "tests/scripts/test_retrieval_bm25_baseline.py",
        "content_identity": "bad05da26cee696ee573abe7dd832d15c0d6b44c81b05d1dba64e5fbcd0ec3b1",
        "document_identity": "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
        "score_delta": {
          "float_hex": "-0x1.69f5fb4e5aa00p-4"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.02ffc4643be14p+5"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.005bc2bc4aaf8p+5"
        },
        "address": "tests/scripts/test_validate_development.py",
        "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
        "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "score_delta": {
          "float_hex": "-0x1.5200d3f898e00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.eb8f3095b3a62p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.ea3b4ae01ecbbp+4"
        },
        "address": "tests/context/retrieval/lexical/test_evaluation.py",
        "content_identity": "277bcad2e6174f351c5b93e1ae7e09c01492ce2834e93b27acc96f0ff9be8155",
        "document_identity": "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
        "score_delta": {
          "float_hex": "-0x1.53e5b594da700p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.b4065f830d0b5p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.b2b46bb5ff99ep+4"
        },
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "score_delta": {
          "float_hex": "-0x1.51f3cd0d71700p-4"
        },
        "upward_positions": 0
      }
    ],
    "pair_inversions": [
      [
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3"
      ],
      [
        "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
      "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
      "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
      "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
      "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
      "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
      "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0"
    ]
  },
  "20": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
    ],
    "exited": [
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430"
    ],
    "inversion_count": 4,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.88ef79ca05290p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.72d27f80783d6p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.61cfa498ceba0p+1"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.43ae48ceffde1p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.3fa47206c835dp+5"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.0275b20dea100p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.3eb5afad9ec8bp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.404ca6610e6e8p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x1.96f6b36fa5d00p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.3323432e59219p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.323b82d5bb305p+5"
        },
        "address": "tests/context/python/project_configuration/test_configuration.py",
        "content_identity": "9f59b552d170df0e3f569fa5f91afbfeda52535115543da27a7605bc79ca4ecd",
        "document_identity": "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
        "score_delta": {
          "float_hex": "-0x1.cf80b13be2800p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.30b052a43d273p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2e48dbeb1c3fbp+5"
        },
        "address": "tests/context/localization/roles/test_evidence.py",
        "content_identity": "584ec4bbf88b4e37ab241f6793751b43fc524ce2b34810d693c1119ba1011316",
        "document_identity": "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
        "score_delta": {
          "float_hex": "-0x1.33bb5c9073c00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.13c8945766a65p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.098b37cab6103p+5"
        },
        "address": "src/devtools/context/python/docs/overview.md",
        "content_identity": "c7386d432c3c7501eb8d3bbc7c41db1a3b5199600eb1179341ac6f46202fafd3",
        "document_identity": "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "score_delta": {
          "float_hex": "-0x1.47ab919612c40p+0"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0be4c94b4c2c5p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.0b2fce4da4ff0p+5"
        },
        "address": "tests/scripts/test_retrieval_bm25_baseline.py",
        "content_identity": "bad05da26cee696ee573abe7dd832d15c0d6b44c81b05d1dba64e5fbcd0ec3b1",
        "document_identity": "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
        "score_delta": {
          "float_hex": "-0x1.69f5fb4e5aa00p-4"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.02ffc4643be14p+5"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.005bc2bc4aaf8p+5"
        },
        "address": "tests/scripts/test_validate_development.py",
        "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
        "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "score_delta": {
          "float_hex": "-0x1.5200d3f898e00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.eb8f3095b3a62p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.ea3b4ae01ecbbp+4"
        },
        "address": "tests/context/retrieval/lexical/test_evaluation.py",
        "content_identity": "277bcad2e6174f351c5b93e1ae7e09c01492ce2834e93b27acc96f0ff9be8155",
        "document_identity": "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
        "score_delta": {
          "float_hex": "-0x1.53e5b594da700p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.b4065f830d0b5p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.b2b46bb5ff99ep+4"
        },
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "score_delta": {
          "float_hex": "-0x1.51f3cd0d71700p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.b161205042e7ap+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.af8c9e961bb9ap+4"
        },
        "address": "tests/context/localization/roles/test_configuration.py",
        "content_identity": "f8291132ad691396296d9f74d9be3435d1e0149d4548aed39b2a4992b4395b61",
        "document_identity": "5b42597fd14c344963a8ddc19fbdf6a2f4865b10a873b40b6a746e8084be1033",
        "score_delta": {
          "float_hex": "-0x1.d481ba272e000p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.a9b83ea8a117fp+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.a922cf675cbccp+4"
        },
        "address": "tests/context/python/project_configuration/test_settings.py",
        "content_identity": "578033888e5c630b1ffd27425ba5d181abfd53b06ba68c3d5a49530c2e1551a5",
        "document_identity": "4387e53b4d1ac3929c61015fe8bb95dd8ae2543204c4642529c3f9c5a6215546",
        "score_delta": {
          "float_hex": "-0x1.2ade8288b6600p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.a2664e109d53dp+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.988d6bb0dcf52p+4"
        },
        "address": "docs/backlog/overview.md",
        "content_identity": "4be97fc28f085ca44602c2fa0a1c27148a91feb185606040c22220408dc263b4",
        "document_identity": "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
        "score_delta": {
          "float_hex": "-0x1.3b1c4bf80bd60p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.9d1ec47601a26p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.a0b0c18906526p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.c8fe898258000p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.8be423f3870e8p+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.8a90cf827517ap+4"
        },
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "score_delta": {
          "float_hex": "-0x1.53547111f6e00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.755e983bd452dp+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.7ba9b45d266d8p+4"
        },
        "address": "src/devtools/core/paths/docs/overview.md",
        "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
        "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "score_delta": {
          "float_hex": "0x1.92c7085486ac0p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.707b5492b67c4p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.6f0c68f27f639p+4"
        },
        "address": "tests/context/localization/roles/test_inputs.py",
        "content_identity": "3fd7678e0429935d0a91252980bfb5f2ae77e55b7ae95da3004522f5a0e85fce",
        "document_identity": "8e24304b76d9dec7f84d375614eda2b798e7290aa69885a1cacd63c938ab1f89",
        "score_delta": {
          "float_hex": "-0x1.6eeba03718b00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.6b1030caaa257p+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.697be93f58adcp+4"
        },
        "address": "tests/context/retrieval/lexical/test_analysis.py",
        "content_identity": "ff1953c36a25655257f5b3ab39c7f4c0b342011e26b6370824324126020b9030",
        "document_identity": "40d78459af0a0833633bc8773e69e4f2ac3462a647d3886a32b080781ba28c5d",
        "score_delta": {
          "float_hex": "-0x1.94478b5177b00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.6a97fbd546d99p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.6978cc2d4a623p+4"
        },
        "address": "pyproject.toml",
        "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
        "document_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "score_delta": {
          "float_hex": "-0x1.1f2fa7fc77600p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.5fafb7d8d6833p+4"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.4c5b42d7eb0f6p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.3547500eb73d0p+0"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.54fd47405e1abp+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.53e551d9c7430p+4"
        },
        "address": "tests/context/retrieval/lexical/test_statistics.py",
        "content_identity": "3f5953e9bc5dfb00eee460b8485e2875c3af9ea60b7b5710f72fbae7534eedd0",
        "document_identity": "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f",
        "score_delta": {
          "float_hex": "-0x1.17f56696d7b00p-4"
        },
        "upward_positions": 3
      }
    ],
    "pair_inversions": [
      [
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3"
      ],
      [
        "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34"
      ],
      [
        "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
      "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
      "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
      "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
      "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
      "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
      "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
      "5b42597fd14c344963a8ddc19fbdf6a2f4865b10a873b40b6a746e8084be1033",
      "4387e53b4d1ac3929c61015fe8bb95dd8ae2543204c4642529c3f9c5a6215546",
      "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
      "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "8e24304b76d9dec7f84d375614eda2b798e7290aa69885a1cacd63c938ab1f89",
      "40d78459af0a0833633bc8773e69e4f2ac3462a647d3886a32b080781ba28c5d",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
    ]
  },
  "50": {
    "definition": "Pair-order reversals inside the union of both top-K sets, separate from crossings",
    "entered": [
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
    ],
    "exited": [
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136"
    ],
    "inversion_count": 45,
    "movements": [
      {
        "A_rank": 1,
        "A_score": {
          "float_hex": "0x1.88ef79ca05290p+5"
        },
        "B_rank": 1,
        "B_score": {
          "float_hex": "0x1.72d27f80783d6p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/roadmap.md",
        "content_identity": "4be3018df37a3eab8f292f352e619dbbb218fe1bb1ac52abadb759a0c51b1f1e",
        "document_identity": "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
        "score_delta": {
          "float_hex": "-0x1.61cfa498ceba0p+1"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 2,
        "A_score": {
          "float_hex": "0x1.43ae48ceffde1p+5"
        },
        "B_rank": 3,
        "B_score": {
          "float_hex": "0x1.3fa47206c835dp+5"
        },
        "address": "AGENTS.md",
        "content_identity": "096fc5fe252684225386aeb3acd48781733286a51f9b27af142eb6d54797fa9a",
        "document_identity": "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "score_delta": {
          "float_hex": "-0x1.0275b20dea100p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 3,
        "A_score": {
          "float_hex": "0x1.3eb5afad9ec8bp+5"
        },
        "B_rank": 2,
        "B_score": {
          "float_hex": "0x1.404ca6610e6e8p+5"
        },
        "address": "src/devtools/resources/filesystem/docs/overview.md",
        "content_identity": "480fc3dedeb480d2b72ddc2c2c6086b9acc4452ee5166cb2fd54e7ee6943056e",
        "document_identity": "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
        "score_delta": {
          "float_hex": "0x1.96f6b36fa5d00p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 4,
        "A_score": {
          "float_hex": "0x1.3323432e59219p+5"
        },
        "B_rank": 4,
        "B_score": {
          "float_hex": "0x1.323b82d5bb305p+5"
        },
        "address": "tests/context/python/project_configuration/test_configuration.py",
        "content_identity": "9f59b552d170df0e3f569fa5f91afbfeda52535115543da27a7605bc79ca4ecd",
        "document_identity": "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
        "score_delta": {
          "float_hex": "-0x1.cf80b13be2800p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 5,
        "A_score": {
          "float_hex": "0x1.30b052a43d273p+5"
        },
        "B_rank": 5,
        "B_score": {
          "float_hex": "0x1.2e48dbeb1c3fbp+5"
        },
        "address": "tests/context/localization/roles/test_evidence.py",
        "content_identity": "584ec4bbf88b4e37ab241f6793751b43fc524ce2b34810d693c1119ba1011316",
        "document_identity": "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
        "score_delta": {
          "float_hex": "-0x1.33bb5c9073c00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 6,
        "A_score": {
          "float_hex": "0x1.13c8945766a65p+5"
        },
        "B_rank": 7,
        "B_score": {
          "float_hex": "0x1.098b37cab6103p+5"
        },
        "address": "src/devtools/context/python/docs/overview.md",
        "content_identity": "c7386d432c3c7501eb8d3bbc7c41db1a3b5199600eb1179341ac6f46202fafd3",
        "document_identity": "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "score_delta": {
          "float_hex": "-0x1.47ab919612c40p+0"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 7,
        "A_score": {
          "float_hex": "0x1.0be4c94b4c2c5p+5"
        },
        "B_rank": 6,
        "B_score": {
          "float_hex": "0x1.0b2fce4da4ff0p+5"
        },
        "address": "tests/scripts/test_retrieval_bm25_baseline.py",
        "content_identity": "bad05da26cee696ee573abe7dd832d15c0d6b44c81b05d1dba64e5fbcd0ec3b1",
        "document_identity": "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
        "score_delta": {
          "float_hex": "-0x1.69f5fb4e5aa00p-4"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 8,
        "A_score": {
          "float_hex": "0x1.02ffc4643be14p+5"
        },
        "B_rank": 8,
        "B_score": {
          "float_hex": "0x1.005bc2bc4aaf8p+5"
        },
        "address": "tests/scripts/test_validate_development.py",
        "content_identity": "861a78969a6f400c46635f938806475cb587e083eafea9e38241b6a44d802e7b",
        "document_identity": "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
        "score_delta": {
          "float_hex": "-0x1.5200d3f898e00p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 9,
        "A_score": {
          "float_hex": "0x1.eb8f3095b3a62p+4"
        },
        "B_rank": 9,
        "B_score": {
          "float_hex": "0x1.ea3b4ae01ecbbp+4"
        },
        "address": "tests/context/retrieval/lexical/test_evaluation.py",
        "content_identity": "277bcad2e6174f351c5b93e1ae7e09c01492ce2834e93b27acc96f0ff9be8155",
        "document_identity": "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
        "score_delta": {
          "float_hex": "-0x1.53e5b594da700p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 10,
        "A_score": {
          "float_hex": "0x1.b4065f830d0b5p+4"
        },
        "B_rank": 10,
        "B_score": {
          "float_hex": "0x1.b2b46bb5ff99ep+4"
        },
        "address": "tests/context/repository/test_document.py",
        "content_identity": "7e7cb4070c95a1927abe18a6f1a0dc1aa4473bf0f99273947b468263c96cf934",
        "document_identity": "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
        "score_delta": {
          "float_hex": "-0x1.51f3cd0d71700p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 11,
        "A_score": {
          "float_hex": "0x1.b161205042e7ap+4"
        },
        "B_rank": 11,
        "B_score": {
          "float_hex": "0x1.af8c9e961bb9ap+4"
        },
        "address": "tests/context/localization/roles/test_configuration.py",
        "content_identity": "f8291132ad691396296d9f74d9be3435d1e0149d4548aed39b2a4992b4395b61",
        "document_identity": "5b42597fd14c344963a8ddc19fbdf6a2f4865b10a873b40b6a746e8084be1033",
        "score_delta": {
          "float_hex": "-0x1.d481ba272e000p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 12,
        "A_score": {
          "float_hex": "0x1.a9b83ea8a117fp+4"
        },
        "B_rank": 12,
        "B_score": {
          "float_hex": "0x1.a922cf675cbccp+4"
        },
        "address": "tests/context/python/project_configuration/test_settings.py",
        "content_identity": "578033888e5c630b1ffd27425ba5d181abfd53b06ba68c3d5a49530c2e1551a5",
        "document_identity": "4387e53b4d1ac3929c61015fe8bb95dd8ae2543204c4642529c3f9c5a6215546",
        "score_delta": {
          "float_hex": "-0x1.2ade8288b6600p-5"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 13,
        "A_score": {
          "float_hex": "0x1.a2664e109d53dp+4"
        },
        "B_rank": 14,
        "B_score": {
          "float_hex": "0x1.988d6bb0dcf52p+4"
        },
        "address": "docs/backlog/overview.md",
        "content_identity": "4be97fc28f085ca44602c2fa0a1c27148a91feb185606040c22220408dc263b4",
        "document_identity": "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
        "score_delta": {
          "float_hex": "-0x1.3b1c4bf80bd60p-1"
        },
        "upward_positions": -1
      },
      {
        "A_rank": 14,
        "A_score": {
          "float_hex": "0x1.9d1ec47601a26p+4"
        },
        "B_rank": 13,
        "B_score": {
          "float_hex": "0x1.a0b0c18906526p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/io.md",
        "content_identity": "ddacd421164e1bd27440d320d6bb7b84d70d5c018d40492b05a8b23ed5da1af0",
        "document_identity": "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
        "score_delta": {
          "float_hex": "0x1.c8fe898258000p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 15,
        "A_score": {
          "float_hex": "0x1.8be423f3870e8p+4"
        },
        "B_rank": 15,
        "B_score": {
          "float_hex": "0x1.8a90cf827517ap+4"
        },
        "address": "tests/context/repository/test_corpus.py",
        "content_identity": "21c37c52abdccaf1c01ced1932de242cd21025511cc2bf63b883454d3ddb29a0",
        "document_identity": "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
        "score_delta": {
          "float_hex": "-0x1.53547111f6e00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 16,
        "A_score": {
          "float_hex": "0x1.755e983bd452dp+4"
        },
        "B_rank": 16,
        "B_score": {
          "float_hex": "0x1.7ba9b45d266d8p+4"
        },
        "address": "src/devtools/core/paths/docs/overview.md",
        "content_identity": "53d7bb1029bae9ba866dc7a72f1e9c7a35f455e2b5441f678065921eadea1112",
        "document_identity": "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
        "score_delta": {
          "float_hex": "0x1.92c7085486ac0p-2"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 17,
        "A_score": {
          "float_hex": "0x1.707b5492b67c4p+4"
        },
        "B_rank": 17,
        "B_score": {
          "float_hex": "0x1.6f0c68f27f639p+4"
        },
        "address": "tests/context/localization/roles/test_inputs.py",
        "content_identity": "3fd7678e0429935d0a91252980bfb5f2ae77e55b7ae95da3004522f5a0e85fce",
        "document_identity": "8e24304b76d9dec7f84d375614eda2b798e7290aa69885a1cacd63c938ab1f89",
        "score_delta": {
          "float_hex": "-0x1.6eeba03718b00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 18,
        "A_score": {
          "float_hex": "0x1.6b1030caaa257p+4"
        },
        "B_rank": 18,
        "B_score": {
          "float_hex": "0x1.697be93f58adcp+4"
        },
        "address": "tests/context/retrieval/lexical/test_analysis.py",
        "content_identity": "ff1953c36a25655257f5b3ab39c7f4c0b342011e26b6370824324126020b9030",
        "document_identity": "40d78459af0a0833633bc8773e69e4f2ac3462a647d3886a32b080781ba28c5d",
        "score_delta": {
          "float_hex": "-0x1.94478b5177b00p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 19,
        "A_score": {
          "float_hex": "0x1.6a97fbd546d99p+4"
        },
        "B_rank": 19,
        "B_score": {
          "float_hex": "0x1.6978cc2d4a623p+4"
        },
        "address": "pyproject.toml",
        "content_identity": "e013670bd2a7ea0dc22304788444ac0f1106f179a1e2af7d1b96ee7e1548b145",
        "document_identity": "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
        "score_delta": {
          "float_hex": "-0x1.1f2fa7fc77600p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 20,
        "A_score": {
          "float_hex": "0x1.5fafb7d8d6833p+4"
        },
        "B_rank": 22,
        "B_score": {
          "float_hex": "0x1.4c5b42d7eb0f6p+4"
        },
        "address": "src/devtools/resources/filesystem/docs/models.md",
        "content_identity": "b1e25f71b411c4bdcfddedfe4106ed50c759ec61d4816ea81a9eceeab38f820b",
        "document_identity": "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "score_delta": {
          "float_hex": "-0x1.3547500eb73d0p+0"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 21,
        "A_score": {
          "float_hex": "0x1.5e55670e0fe3cp+4"
        },
        "B_rank": 23,
        "B_score": {
          "float_hex": "0x1.4b3926bcf16e8p+4"
        },
        "address": "tests/context/localization/generation/test_branching.py",
        "content_identity": "6911948b663328da223af255ee264e381572b055b7f6ad11bfc9a1069abe5f22",
        "document_identity": "6e30be71aa573b6c7824d987e0e6f6642996ecc03732a3f18bb58c625448015e",
        "score_delta": {
          "float_hex": "-0x1.31c40511e7540p+0"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 22,
        "A_score": {
          "float_hex": "0x1.55f15199b1ffbp+4"
        },
        "B_rank": 24,
        "B_score": {
          "float_hex": "0x1.3d3ad5ade9e68p+4"
        },
        "address": "src/devtools/context/retrieval/docs/overview.md",
        "content_identity": "ec9ae2279d602e8d5a8b3361765800e2bbd9da422ff7038e85c7f6b07306bf95",
        "document_identity": "95c9b0c3d70cc47a5e78035ec036682dfa85d4be2c4603e037745eab012c33b0",
        "score_delta": {
          "float_hex": "-0x1.8b67bebc81930p+0"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 23,
        "A_score": {
          "float_hex": "0x1.54fd47405e1abp+4"
        },
        "B_rank": 20,
        "B_score": {
          "float_hex": "0x1.53e551d9c7430p+4"
        },
        "address": "tests/context/retrieval/lexical/test_statistics.py",
        "content_identity": "3f5953e9bc5dfb00eee460b8485e2875c3af9ea60b7b5710f72fbae7534eedd0",
        "document_identity": "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f",
        "score_delta": {
          "float_hex": "-0x1.17f56696d7b00p-4"
        },
        "upward_positions": 3
      },
      {
        "A_rank": 24,
        "A_score": {
          "float_hex": "0x1.4fc70f9726e63p+4"
        },
        "B_rank": 21,
        "B_score": {
          "float_hex": "0x1.4ed8c6b93cc5cp+4"
        },
        "address": "tests/context/retrieval/lexical/test_index.py",
        "content_identity": "50cafbcaede0c499cbffc96c26e4c61bb7a2263a5652a5d213d2730c56273e0e",
        "document_identity": "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95",
        "score_delta": {
          "float_hex": "-0x1.dc91bbd440e00p-5"
        },
        "upward_positions": 3
      },
      {
        "A_rank": 25,
        "A_score": {
          "float_hex": "0x1.39f0d84ffd813p+4"
        },
        "B_rank": 25,
        "B_score": {
          "float_hex": "0x1.2ea3e9ffc1b1fp+4"
        },
        "address": "tests/context/localization/generation/test_generation.py",
        "content_identity": "a2f2e5074e4134991e02e0a7b13f56737a1d6e37273d7b9850a70fdb06e92cef",
        "document_identity": "b5660447af92e755e89560eabec373b54a2a354912548243a22c8d3360b7dbc0",
        "score_delta": {
          "float_hex": "-0x1.699dca0779e80p-1"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 26,
        "A_score": {
          "float_hex": "0x1.278bd91e27c06p+4"
        },
        "B_rank": 26,
        "B_score": {
          "float_hex": "0x1.278bd91e27c06p+4"
        },
        "address": "tests/resources/filesystem/test_resolution.py",
        "content_identity": "8bb3b243a8f60360c4fc35aafcf04d6eda81d5dbc4db7600dc06f8759c7a0be8",
        "document_identity": "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 27,
        "A_score": {
          "float_hex": "0x1.243b68c656f3dp+4"
        },
        "B_rank": 27,
        "B_score": {
          "float_hex": "0x1.22b7f5d32fcbbp+4"
        },
        "address": "docs/experiments/qwen38_llama_cpp.md",
        "content_identity": "26c402d7fb85446b66cd0c9b014c30ab35574486483bf206b2b6b8b0f1bc4b98",
        "document_identity": "bcbb31820957884ed9da43118412fdedc3dc62dd7313fc728935b79610fe160b",
        "score_delta": {
          "float_hex": "-0x1.8372f32728200p-4"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 28,
        "A_score": {
          "float_hex": "0x1.241d08363e057p+4"
        },
        "B_rank": 32,
        "B_score": {
          "float_hex": "0x1.12f003f5b919ap+4"
        },
        "address": "src/devtools/core/paths/docs/resolution.md",
        "content_identity": "fa40ca033450a10898e69600e81e7e4246280aa9a9eff6ea68da740d6cd932a5",
        "document_identity": "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "score_delta": {
          "float_hex": "-0x1.12d044084ebd0p+0"
        },
        "upward_positions": -4
      },
      {
        "A_rank": 29,
        "A_score": {
          "float_hex": "0x1.212e94340a704p+4"
        },
        "B_rank": 28,
        "B_score": {
          "float_hex": "0x1.2080b4170e177p+4"
        },
        "address": "tests/context/retrieval/lexical/test_bm25.py",
        "content_identity": "3aa8e9bee063327e0f87500fc824ba13515e41a8b47117849ff55abd4282f97f",
        "document_identity": "b3a957401ac34b38a5d3816ec770fe8213ec011383535e7795f583f42d48ae08",
        "score_delta": {
          "float_hex": "-0x1.5bc039f8b1a00p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 30,
        "A_score": {
          "float_hex": "0x1.1e8b3208c337ep+4"
        },
        "B_rank": 29,
        "B_score": {
          "float_hex": "0x1.1daa02c0e2978p+4"
        },
        "address": "src/devtools/context/localization/roles/derivation.py",
        "content_identity": "981cac6da4e0c6d22fb015a268ed9c264775ebb76a3707bdbcfd1035634f7bdf",
        "document_identity": "1bf86647531a96eac3c0df8e48188690de98ac865516a1485bae54d08a549b04",
        "score_delta": {
          "float_hex": "-0x1.c25e8fc140c00p-5"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 31,
        "A_score": {
          "float_hex": "0x1.177229c0b12a0p+4"
        },
        "B_rank": 35,
        "B_score": {
          "float_hex": "0x1.00220870513ccp+4"
        },
        "address": "src/devtools/context/python/function/docs/overview.md",
        "content_identity": "6694ff79616580eaf377f6d9b9ab2472117b19879c651fa6bc8b9b45900f8a9d",
        "document_identity": "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "score_delta": {
          "float_hex": "-0x1.75021505fed40p+0"
        },
        "upward_positions": -4
      },
      {
        "A_rank": 32,
        "A_score": {
          "float_hex": "0x1.13a9f8566e428p+4"
        },
        "B_rank": 31,
        "B_score": {
          "float_hex": "0x1.13a9f8566e428p+4"
        },
        "address": "tests/context/retrieval/lexical/test_filename.py",
        "content_identity": "b4a210ed6a4d196233700d223c3793c635fbb422becd624a5941c34e94be3c6d",
        "document_identity": "ddfc760369fa7657b1d161e154a5356bd7808f94f23444b67da5591c900dcecb",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 33,
        "A_score": {
          "float_hex": "0x1.0ffd11415f0c9p+4"
        },
        "B_rank": 30,
        "B_score": {
          "float_hex": "0x1.194c3c4364a34p+4"
        },
        "address": "scripts/validate_development.py",
        "content_identity": "425a9c8f8d2b9408ed8952cc71494ef7c213ee89a64f341d0966352fd87d4bb5",
        "document_identity": "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
        "score_delta": {
          "float_hex": "0x1.29e56040b2d60p-1"
        },
        "upward_positions": 3
      },
      {
        "A_rank": 34,
        "A_score": {
          "float_hex": "0x1.0cfd7841f03f7p+4"
        },
        "B_rank": 38,
        "B_score": {
          "float_hex": "0x1.eb540bcafb476p+3"
        },
        "address": "src/devtools/context/python/modules/docs/overview.md",
        "content_identity": "fafb310cbfe8b944532ac8cfa2d930daa909b2a72bd3a54af57f8ca089cc8a08",
        "document_identity": "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
        "score_delta": {
          "float_hex": "-0x1.753725c729bc0p+0"
        },
        "upward_positions": -4
      },
      {
        "A_rank": 35,
        "A_score": {
          "float_hex": "0x1.02a4be2146c8ap+4"
        },
        "B_rank": 41,
        "B_score": {
          "float_hex": "0x1.e3b6c8a5b9302p+3"
        },
        "address": "src/devtools/context/python/references/docs/overview.md",
        "content_identity": "5ab01b1b0b6fa6a8c338119aa2cd820c9d1f292b1120b96a4211c0e9bf5c7d09",
        "document_identity": "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "score_delta": {
          "float_hex": "-0x1.0c959ce6a3090p+0"
        },
        "upward_positions": -6
      },
      {
        "A_rank": 36,
        "A_score": {
          "float_hex": "0x1.01501a8d6852ep+4"
        },
        "B_rank": 34,
        "B_score": {
          "float_hex": "0x1.01501a8d6852ep+4"
        },
        "address": "src/devtools/resources/filesystem/models/base.py",
        "content_identity": "ada2cec083ac5e9dd101a357401c7d7f18091fbb4c45ddaf8cf09d37b31caa3c",
        "document_identity": "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 37,
        "A_score": {
          "float_hex": "0x1.0144b063323bbp+4"
        },
        "B_rank": 36,
        "B_score": {
          "float_hex": "0x1.fdd72d4ed2eefp+3"
        },
        "address": "tests/scripts/qwen/test_llama_cpp_profile.py",
        "content_identity": "f05049563bff24f129a9c1afb629b31bf5f02c2d100cf05a32a8ebbe9d441db8",
        "document_identity": "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7",
        "score_delta": {
          "float_hex": "-0x1.2c8cdde4621c0p-3"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 38,
        "A_score": {
          "float_hex": "0x1.00e53d942244bp+4"
        },
        "B_rank": 33,
        "B_score": {
          "float_hex": "0x1.073059b5745f7p+4"
        },
        "address": "src/devtools/tools/docs/overview.md",
        "content_identity": "103cefbd4c6e21813ea33773d77b0e197498878bdac36acdd281429ef07e3f1a",
        "document_identity": "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
        "score_delta": {
          "float_hex": "0x1.92c7085486b00p-2"
        },
        "upward_positions": 5
      },
      {
        "A_rank": 39,
        "A_score": {
          "float_hex": "0x1.f287d7c93bbc4p+3"
        },
        "B_rank": 37,
        "B_score": {
          "float_hex": "0x1.f287d7c93bbc5p+3"
        },
        "address": "README.md",
        "content_identity": "f7080e9cb6b51bc1795dbd54719c69e230fd737e47a2bcd0d608d5ba57db92f9",
        "document_identity": "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 40,
        "A_score": {
          "float_hex": "0x1.e7668dfff8fdap+3"
        },
        "B_rank": 39,
        "B_score": {
          "float_hex": "0x1.e7668dfff8fdbp+3"
        },
        "address": "tests/context/python/modules/test_interpretation.py",
        "content_identity": "e751e2d401edd907095eadd2dd057a0e8687b9c97dd4383c25837f3b14a3ce0b",
        "document_identity": "19362b5f55870b0dc04e614b5d697da5410833c4f9475605182916f2518ad4ef",
        "score_delta": {
          "float_hex": "0x1.0000000000000p-49"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 41,
        "A_score": {
          "float_hex": "0x1.e5d6e78dac844p+3"
        },
        "B_rank": 40,
        "B_score": {
          "float_hex": "0x1.e5d6e78dac844p+3"
        },
        "address": "tests/context/localization/grounding/test_grounding.py",
        "content_identity": "7fb5165e952255d77a62d925b084363acc90a0aa25ecd0e964307ef0f353ed58",
        "document_identity": "ab2c8d4300981ce47ada88d85abab9084473b9a600e51b48b8ffa5185d655a4e",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 1
      },
      {
        "A_rank": 42,
        "A_score": {
          "float_hex": "0x1.d4563e041fa05p+3"
        },
        "B_rank": 42,
        "B_score": {
          "float_hex": "0x1.d4563e041fa04p+3"
        },
        "address": "tests/context/python/test_mirrored_paths.py",
        "content_identity": "608a3defd9ee9107ca690be9c140a4eb7da8c46bb3e9800c5cc2cdd76255d16b",
        "document_identity": "0036c88c468c650676fe4733ddd81f59a3f0fae8b7be4eacf2f45d79da41eb2d",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-49"
        },
        "upward_positions": 0
      },
      {
        "A_rank": 43,
        "A_score": {
          "float_hex": "0x1.d2580f88f3d68p+3"
        },
        "B_rank": 45,
        "B_score": {
          "float_hex": "0x1.d2580f88f3d66p+3"
        },
        "address": "tests/context/python/references/declarations/test_analysis.py",
        "content_identity": "5f56d5194589ee7e7bac29dd419401d405314a1c895a93542071efdb898c554a",
        "document_identity": "574bf96fbbd9e4d6bd13a23ef397d182c30f0f5881b165e93c28f6ed37db60bb",
        "score_delta": {
          "float_hex": "-0x1.0000000000000p-48"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 44,
        "A_score": {
          "float_hex": "0x1.c84392cfa233ap+3"
        },
        "B_rank": 49,
        "B_score": {
          "float_hex": "0x1.a5be4090cb2c5p+3"
        },
        "address": "src/devtools/core/time/docs/timestamps.md",
        "content_identity": "91c782d7d5011301e7a921d01057951d8f39ac3d2332bb60b3146b7059035941",
        "document_identity": "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "score_delta": {
          "float_hex": "-0x1.142a91f6b83a8p+0"
        },
        "upward_positions": -5
      },
      {
        "A_rank": 45,
        "A_score": {
          "float_hex": "0x1.c69b5fb402a11p+3"
        },
        "B_rank": 43,
        "B_score": {
          "float_hex": "0x1.d33197f6a6d6ap+3"
        },
        "address": "src/devtools/resources/commands/docs/overview.md",
        "content_identity": "7c4f2d93bb5f4033f94d22de5cab4da43a1838e8909b6347ecfa972d8fd71df8",
        "document_identity": "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
        "score_delta": {
          "float_hex": "0x1.92c7085486b20p-2"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 46,
        "A_score": {
          "float_hex": "0x1.c65f172719b3dp+3"
        },
        "B_rank": 44,
        "B_score": {
          "float_hex": "0x1.d2f54f69bde96p+3"
        },
        "address": "src/devtools/core/conversion/docs/overview.md",
        "content_identity": "7068d7046cc793f13cf7e3ca039b2e5a1cfe7f2cac16e8441776a3b2d54a1c60",
        "document_identity": "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
        "score_delta": {
          "float_hex": "0x1.92c7085486b20p-2"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 47,
        "A_score": {
          "float_hex": "0x1.c33b2423374cap+3"
        },
        "B_rank": 52,
        "B_score": {
          "float_hex": "0x1.8d89263add12bp+3"
        },
        "address": "src/devtools/resources/filesystem/models/binary.py",
        "content_identity": "abd051ba906097ca7e0296d86cfc7c08a4eed82d32a8d3b1cb42c212e17c9337",
        "document_identity": "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "score_delta": {
          "float_hex": "-0x1.ad8fef42d1cf8p+0"
        },
        "upward_positions": -5
      },
      {
        "A_rank": 48,
        "A_score": {
          "float_hex": "0x1.bc376c71f108dp+3"
        },
        "B_rank": 46,
        "B_score": {
          "float_hex": "0x1.bc376c71f108dp+3"
        },
        "address": "tests/tools/test_filesystem.py",
        "content_identity": "efdc0111f7a8d7f0b07cd504ddc2e08e243285143ca0afa1dab2fb333b2b1b96",
        "document_identity": "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      },
      {
        "A_rank": 49,
        "A_score": {
          "float_hex": "0x1.baabce22434f3p+3"
        },
        "B_rank": 51,
        "B_score": {
          "float_hex": "0x1.8fabe5590970ap+3"
        },
        "address": "src/devtools/context/python/imports/docs/overview.md",
        "content_identity": "bbb0ca72d49e60b691e305f06b3a8cc5bb932388fbb4a53b37cd02414f41bed3",
        "document_identity": "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136",
        "score_delta": {
          "float_hex": "-0x1.57ff4649cef48p+0"
        },
        "upward_positions": -2
      },
      {
        "A_rank": 50,
        "A_score": {
          "float_hex": "0x1.b5a0976721af0p+3"
        },
        "B_rank": 47,
        "B_score": {
          "float_hex": "0x1.b5a0976721af0p+3"
        },
        "address": "src/devtools/resources/filesystem/resolution.py",
        "content_identity": "195138aa122ce3559164610b53a7b14663433af90dc3fd29c2dd670474dce2c6",
        "document_identity": "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 3
      },
      {
        "A_rank": 51,
        "A_score": {
          "float_hex": "0x1.a99767874ac4dp+3"
        },
        "B_rank": 48,
        "B_score": {
          "float_hex": "0x1.a99767874ac4dp+3"
        },
        "address": "tests/context/repository/test_observation.py",
        "content_identity": "ba74f3a4ddf68f48057fa57da9f00208d291842545817db4b145371604c66016",
        "document_identity": "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 3
      },
      {
        "A_rank": 52,
        "A_score": {
          "float_hex": "0x1.997e1a1e21f11p+3"
        },
        "B_rank": 50,
        "B_score": {
          "float_hex": "0x1.997e1a1e21f11p+3"
        },
        "address": "tests/context/localization/routing/test_routing.py",
        "content_identity": "eb5cd6ca53f81182cacf39d8f349bbc1a5845eee0f83153728d65f2cbf107a63",
        "document_identity": "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b",
        "score_delta": {
          "float_hex": "0x0.0p+0"
        },
        "upward_positions": 2
      }
    ],
    "pair_inversions": [
      [
        "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
        "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3"
      ],
      [
        "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
        "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34"
      ],
      [
        "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
        "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
      ],
      [
        "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
        "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95"
      ],
      [
        "6e30be71aa573b6c7824d987e0e6f6642996ecc03732a3f18bb58c625448015e",
        "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
      ],
      [
        "6e30be71aa573b6c7824d987e0e6f6642996ecc03732a3f18bb58c625448015e",
        "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95"
      ],
      [
        "95c9b0c3d70cc47a5e78035ec036682dfa85d4be2c4603e037745eab012c33b0",
        "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f"
      ],
      [
        "95c9b0c3d70cc47a5e78035ec036682dfa85d4be2c4603e037745eab012c33b0",
        "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95"
      ],
      [
        "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "b3a957401ac34b38a5d3816ec770fe8213ec011383535e7795f583f42d48ae08"
      ],
      [
        "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "1bf86647531a96eac3c0df8e48188690de98ac865516a1485bae54d08a549b04"
      ],
      [
        "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "ddfc760369fa7657b1d161e154a5356bd7808f94f23444b67da5591c900dcecb"
      ],
      [
        "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
        "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a"
      ],
      [
        "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "ddfc760369fa7657b1d161e154a5356bd7808f94f23444b67da5591c900dcecb"
      ],
      [
        "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a"
      ],
      [
        "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4"
      ],
      [
        "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
        "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09"
      ],
      [
        "ddfc760369fa7657b1d161e154a5356bd7808f94f23444b67da5591c900dcecb",
        "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a"
      ],
      [
        "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
        "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4"
      ],
      [
        "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
        "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7"
      ],
      [
        "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
        "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09"
      ],
      [
        "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
        "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "19362b5f55870b0dc04e614b5d697da5410833c4f9475605182916f2518ad4ef"
      ],
      [
        "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
        "ab2c8d4300981ce47ada88d85abab9084473b9a600e51b48b8ffa5185d655a4e"
      ],
      [
        "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
        "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09"
      ],
      [
        "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7",
        "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09"
      ],
      [
        "574bf96fbbd9e4d6bd13a23ef397d182c30f0f5881b165e93c28f6ed37db60bb",
        "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961"
      ],
      [
        "574bf96fbbd9e4d6bd13a23ef397d182c30f0f5881b165e93c28f6ed37db60bb",
        "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000"
      ],
      [
        "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961"
      ],
      [
        "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000"
      ],
      [
        "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590"
      ],
      [
        "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      [
        "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590"
      ],
      [
        "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136"
      ],
      [
        "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      [
        "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
        "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
      ],
      [
        "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136",
        "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56"
      ],
      [
        "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136",
        "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced"
      ],
      [
        "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136",
        "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
      ]
    ],
    "union": [
      "892c578ac17061177c5cb795a95f6f95d40c80fcb8ad52c36c979f3eb98482df",
      "953ca78b4215df7a7981e46287fbc2bd96eee678f692a82d8f69b84b0aa5cc1d",
      "8312f21fe924d101d1087d0902480d3dca602e515f7862cab1b6f01aa506e8d3",
      "a60c241f9026b1c9c89fd442810a5f951c73a92cd2fd2a76a9d65e7107e023e6",
      "03dd792406677791ba016ed4fdd25bf3d0d5d0bcf9c8ce9f90e65f38b5ad9a84",
      "043163a1983de86c2f6b55624d32f088f9bf1a9b4e4cfbbaa164b3ef4f64ab6f",
      "5a988de9415a2fc092de81e059cebb4c4acae979fa95f48ffc11f265e2c66b34",
      "aac11402bce9cd4a221096b5322d062b22f30244cdb1eb27d2027a9457987986",
      "0ca98c228f02ad7eb66ac823b251641c68f53dee0d6167d070bd13f7f47c391e",
      "e0023d67c70a97f0263f72e4f57b6fe7f96946549814b7faef0e4cd5fa7bc6e0",
      "5b42597fd14c344963a8ddc19fbdf6a2f4865b10a873b40b6a746e8084be1033",
      "4387e53b4d1ac3929c61015fe8bb95dd8ae2543204c4642529c3f9c5a6215546",
      "e74ff954ecf6c377d717c5cc6cd585ce6441a3b338766e8e558e82379449a1c0",
      "056c45cb2a7af24772252cbf85d3123cfc157e4c9302589afc6285ddd4854300",
      "ba391e447a764f4997fdebc4f7034aa7600509cd10cebd7446347c40338c3396",
      "acf71f2ae8f83c46bbb9a62426e546d3014c46c90ea73cc794041c84eacd9776",
      "8e24304b76d9dec7f84d375614eda2b798e7290aa69885a1cacd63c938ab1f89",
      "40d78459af0a0833633bc8773e69e4f2ac3462a647d3886a32b080781ba28c5d",
      "6960fb8d154fecac3ee960eb940df3e2d78d6c5ccda4931b20f43d5089e421c0",
      "eb21f7ea8ae995b152ddea01805f9328d5de8d8b7fe3dfe5aec7a1568d81a430",
      "6e30be71aa573b6c7824d987e0e6f6642996ecc03732a3f18bb58c625448015e",
      "95c9b0c3d70cc47a5e78035ec036682dfa85d4be2c4603e037745eab012c33b0",
      "02d747605a6c988bff2bcaa0089a3843ba49f0f1d4340cdcf7acd96ee5033a0f",
      "d759a011e1623cf4ce0b3d0944d07e977e7a314af8d041338232f58ea3cfca95",
      "b5660447af92e755e89560eabec373b54a2a354912548243a22c8d3360b7dbc0",
      "87232fe9c98b5bec24c2f133821acb37b77a346d6019a20dd19e99f79a975e42",
      "bcbb31820957884ed9da43118412fdedc3dc62dd7313fc728935b79610fe160b",
      "52cfb23edebfbc8d12fa3cd1842ea0a2a0ee88bf62e23f0e056bb61295bfa524",
      "b3a957401ac34b38a5d3816ec770fe8213ec011383535e7795f583f42d48ae08",
      "1bf86647531a96eac3c0df8e48188690de98ac865516a1485bae54d08a549b04",
      "5ae4e5e2f60ab154856abc53979c28e910145b12a7bdaa9fa313437d29be3920",
      "ddfc760369fa7657b1d161e154a5356bd7808f94f23444b67da5591c900dcecb",
      "63e8a7f495ab6b1a5bfa5e4d9dbf4bd287cae47beedab229cefb85e22910ec9a",
      "8949e50f36f8be98c36798e14347fa778131b55bce5f9e066d6a0287bc02af95",
      "fdd6202b0566e87503fea599e162cb4cf293083b363e4a85c959a48ac634ee9b",
      "926cb2ba75c0077537449c5ab3a7e8df8572aa737a909b52d162e87e6d3bded4",
      "abebe04a64ea3a722eaf921674ce164e6b7cd61eb0dd18c89b36db1c039b04c7",
      "9dc71bac3745ea535fa0b3d781aee48d8a179fcae3864fb8672d36f7e0a24b09",
      "2307913ae9915ff065174ffef8c63eb3495e22686449d28e94e43bc9bd40e267",
      "19362b5f55870b0dc04e614b5d697da5410833c4f9475605182916f2518ad4ef",
      "ab2c8d4300981ce47ada88d85abab9084473b9a600e51b48b8ffa5185d655a4e",
      "0036c88c468c650676fe4733ddd81f59a3f0fae8b7be4eacf2f45d79da41eb2d",
      "574bf96fbbd9e4d6bd13a23ef397d182c30f0f5881b165e93c28f6ed37db60bb",
      "12fa002e1cb39eb2e6fd24ae0b280fa1d28812f356180f272c0c16d0b78576c2",
      "27945e145105307e18bedf5202ddd7d4fb1ba0bebf418f4673a1aa7583d9d961",
      "a46fffd8fe22b021beab2eab89bae199e45ec5b4c333a7cd998fe67622f3b000",
      "598ebc5d4909b2a402a7f82ba7771887094102364ff1df4fda78e1f85f6ad121",
      "53235d26ab70274fa227fbdfa7cb72eb0f3b74a9992d787ed15e08df2e3ae590",
      "41833103a626b68aa358c49d0e940e3af2465386166f6680820ef97a7b2cc136",
      "a97799cbf41332f4318f62dcf6670f58e5e6122c8e6b951da84383fb1bb0bf56",
      "094a3cf9792472dccb4850ba499aa176823b4f923a0ef4438e9898abd25feced",
      "1a4ad6b60b3bff1765851ddf5ce154d13e40ebd7e22ba2ed58a8946d825d2a8b"
    ]
  }
}
```

## Full provenance ownership

fields.json.gz retains every canonical observation/token and tf/length; native_statistics.json.gz and union_statistics.json.gz retain every term's membership, field df/IDF and union df/IDF. arm_a.json.gz and arm_b.json.gz retain all six exact query-bound candidate results. contributions.json.gz joins both field channels and every distinct term's normalized/weighted/combined tf, IDFs, saturation and scores. decomposition.json.gz retains the frozen diagnostic and exact rational residuals. top_k.json.gz owns full movements/inversions/crossings; reference.json.gz owns the unchanged separate canonical whole-task lane. All are pretty lossless JSON under deterministic gzip. Immutable operations/ owns complete native object graphs and recoverable pickle segments; projections never replace authoritative native A.

Frozen decomposition order is union-IDF replacement, moving filename weight inside saturation, then cross-field single saturation. Normalization inputs are unchanged; exact field denominators and native channel/grouping/subtraction residuals remain explicit. No intermediate stages are ranked and no relevance conclusion is drawn.
