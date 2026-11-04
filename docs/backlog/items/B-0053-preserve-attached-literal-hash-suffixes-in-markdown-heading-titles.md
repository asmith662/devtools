# B-0053 — Preserve attached literal hash suffixes in Markdown heading titles

- type: STORY
- status: CLOSED
- decision_maturity: DISCOVERED
- primary_domain: resources
- supporting_domains: unknown
- evidence_basis: REPOSITORY
- hard_dependencies: unknown
- pressure_dependencies: unknown
- operational_dependencies: unknown
- validation_level: NONE
- execution_authorization: NONE
- proposal: ../proposals/4d56c38c-e8b2-49ba-bdaf-255f71ef238e/proposal.json
- intake_review: ../proposals/4d56c38c-e8b2-49ba-bdaf-255f71ef238e/review-0001.json

## Problem / value

On authenticated main a4274bd190bf7ee16c4f8077410617dd37461157, exported MarkdownFile parses "# C#" as title "C". find_heading("C#") and find_section("C#") consequently return None. Its optional closing-hash pattern consumes attached title characters without the space/tab boundary of a closing marker. Repair only the existing structural Markdown owner; preserve literal hashes and strip only a separated terminal hash run.

## Proposed benefit

Keep programming-language and other hash-suffixed titles intact so existing heading/section lookups find the intended source. Preserve existing levels, whitespace trimming, empty headings, fence handling, section boundaries, original content and model APIs. One-file repair, frozen public tests and independent private acceptance.

## Uncertainty / unresolved semantics

Authored in-memory reproduction, no observed production document loss. Markdown remains a narrow helper; no inline escape decoding, Setext, new indentation grammar, source-slice fidelity or full CommonMark parser. Existing fence-closer repair is delivered and separate; B-0049/50/51 and B-0052 remain unchanged.

## Discovery / parent

{'kind': 'agent', 'reference': '.local/productive-native/frozen.json; independently reproduced public API; https://spec.commonmark.org/0.31.2/#atx-headings'}
None

## Evidence

src/devtools/resources/filesystem/docs/markdown.md
tests/resources/filesystem/models/markdown/test_file.py

## Affected resources

src/devtools/resources/filesystem/models/markdown/file.py
src/devtools/resources/filesystem/models/markdown/heading.py
src/devtools/resources/filesystem/models/markdown/section.py
src/devtools/resources/filesystem/models/text.py
tests/resources/filesystem/models/markdown/test_file.py
tests/resources/filesystem/models/markdown/test_heading.py
tests/resources/filesystem/models/markdown/test_section.py
tests/resources/filesystem/codecs/test_markdown.py

## Possible dependencies

Existing filesystem Markdown model and codec; standing Intake and exact native grants; independent review; separate integration authority.

## Consumers / invariants / risks

unknown; preserve existing behavior and authority boundaries

## Promotion / validation expectations

Backlog inclusion only. Scope, priority, dependencies and acceptance require deliberate review before implementation.


## Verified direct implementation completion 6fec0a1e2038e36911b13f9fcd63a5398799151b4c6f54b401126ea6e3e5acc3

- Implementation: Codex direct maintenance @ 7be3b5221f5d12241da16d92483bf405ea5b4985
- Verified destination: origin/main@667c1aa34eae18fe5b4f4e83427f6df2ed6e5290
- Protected validation receipt: 4fc701e6418cf754aa6653f7c2481f315944ec408deceaddf4f78e308a65f01c (executed commit 667c1aa34eae18fe5b4f4e83427f6df2ed6e5290; passed; 100% configured coverage)
- Codex completion review: Codex review of B-0053 implementation 7be3b5221f5d12241da16d92483bf405ea5b4985 — Verified the complete Markdown heading obligation against the production diff, regression tests, docs, and the exact protected validation receipt; native Qwen episode remains historically BLOCKED.
- Authorization: User +approve: authorize the direct completion pathway and B-0053 reconciliation
- Engineering obligations: Preserve attached literal hashes in Markdown ATX heading titles and section lookup while stripping only valid separated closing hash sequences.; Preserve empty headings including # ##, heading levels, whitespace trimming, and section lookup.; Preserve fenced-code boundaries, CRLF handling, original content, and source behavior.
- Evidence: src/devtools/resources/filesystem/models/markdown/file.py; src/devtools/resources/filesystem/docs/markdown.md; tests/resources/filesystem/models/markdown/test_file.py
