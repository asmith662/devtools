# B-0053 — Preserve attached literal hash suffixes in Markdown heading titles

- type: STORY
- status: BACKLOG
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

