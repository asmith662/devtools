# Productive native Markdown maintenance

B-0053 addresses an independently reproduced public MarkdownFile defect: `# C#`
loses its attached hash, and lookup by the source title fails. This is a distinct
literal-title obligation. B-0049/B-0050/B-0051 and the qualified, uninstalled
B-0052 candidate retain their original histories and consumed slots.

The active operator standing policy supplied the exact Intake decision through
the existing owner. The [approved decision](code-audit/productive-native-markdown-20261103/intake-result.json)
and [frozen inputs](code-audit/productive-native-markdown-20261103/frozen.json)
precede any coding inference. Public baseline: one failure and 35 passes;
independently authored private inputs also reproduce attached-title corruption.
No reference implementation or repaired control is supplied to Qwen.

Scope is the existing Markdown model only. The closing-marker boundary follows
the [ATX rule](https://spec.commonmark.org/0.31.2/#atx-headings), while the current
narrow raw-text helper, opening grammar and inline escape representation remain.
This does not introduce a full Markdown parser. Exact source, public/private
acceptance identities and provider fingerprint are frozen in the linked packet.
Private implementation was excluded from the coding source scope. It is now
archived after terminal failure; no independent review was eligible or entered.

The healthy persistent Qwen service is unchanged: one idle 65,536-token slot,
same container, image, command and read-only model mount. All 1,077 declared
production/configuration input hashes match the successful protected receipt
for `4fe7ac6c90c50e60cf7470ae1dcfa011a6956e21`: 4,269 passes, two optional skips,
100% configured line/branch coverage. This is authenticated receipt reuse, not a
new comprehensive pass or a claim of complete external environment equivalence.
The temporary public test is an additional frozen candidate check, not a new
installed production input. Existing forensic files and Inspector are preserved.

Preparation authorizes no installation, publication of candidate source or
backlog closure. The subsequent operator-authorized evidence closeout publishes
the failed candidate as immutable research data, without installing it.

## Authentic terminal coding result

Preparation was published at `3d9de0a5446c30093d4d3f4a258f737746ff60f0`.
The existing native owner issued one exact assignment and standing-policy grant,
then consumed one dispatch on branch `feat/native-markdown-b0053-20261103`.
The [native result](code-audit/productive-native-markdown-20261103/native/result.json)
is **BLOCKED**, identity
`b5a503c914fecb8f8c148a9ed83a34a17261cbbd1b0c66e99353ed98d4b5137a`.
Its internal `coding_disposition: validated` and `coding_accepted: true` describe
the public coding phase; private acceptance failed, so these fields establish
neither successful native completion nor review eligibility.

There were four genuine Qwen calls, six source acquisitions, one admitted
replacement and one public-check execution. The acquired files were the Markdown
owner, its file tests, codec tests, frozen public diagnostic, heading model and
section model. The returned edit then produced a current candidate disclosure;
that host disclosure is not a seventh worker source acquisition. The 28 sealed
native observations retain exact normalized requests, responses, Tool arguments,
disclosures, checks and Context observations. Supporting adapter records retain
provider response identities. These are normalized ModelInteraction captures,
not a claim of archived HTTP wire bodies.

The [public result](code-audit/productive-native-markdown-20261103/native/worker/observation-0023.json)
was 36 passes in 0.12 seconds, exit 0. The separately frozen
[private result](code-audit/productive-native-markdown-20261103/native/worker/observation-0025.json)
was exit 1 at `AssertionError: ('# ##', '', '##')`. It stopped at that assertion;
later private cases and hierarchy assertions are not claimed as executed passes.
No transport error, output-limit termination, source-read refusal or missing
return explains this result. Total reported usage was 24,332 input and 566 output
tokens, 24,898 total; repeated prompts contribute to input usage. Native execution
was 80.393113 seconds, wrapper wall time 80.884058 seconds, summed adapter time
44.411118 seconds. Nonstreaming first-token latency was not captured.

## Semantic failure and diagnostic limits

The exact [candidate patch](code-audit/productive-native-markdown-20261103/native/candidate.patch)
changes only `_ATX_HEADING_PATTERN` in the existing Markdown owner:

```python
r"^(?P<marker>#{1,6})[ \t]+(?P<text>.*?)(?:(?<=\S)[ \t]+#*|[ \t]*)[ \t]*$"
```

The model preserved attached literal suffixes such as `C#`, `F##` and
`alpha#beta###`, and removed separated terminal hashes after nonempty titles.
However, its closing-marker branch requires a preceding non-whitespace
character. When the title is empty, opening whitespace consumes the separator
and the terminal hashes enter the title capture. Thus `# ##` becomes title `##`
instead of the baseline empty title. This violates the explicit preservation
requirement. Public checks lacked this empty-title closing-marker case.

The original [frozen identities](code-audit/productive-native-markdown-20261103/frozen.json)
precede inference. Private oracle SHA256 is
`c83f668f576121e4f7663440347b5d4919fd951b39b4a9752208656718a662ec`.
The [post-hoc host assessment](code-audit/productive-native-markdown-20261103/host-assessment.json)
was produced after terminal failure. Its `frozen_case_completion` field is an
offline completion of selected case observations, not an expansion of the
original private execution. Its additional 27-case matrix combines opening
levels 1/2/6, space/tab/double-space separators and 1/2/7 closing hashes. Baseline
is correct on 27/27; the archived candidate is correct on 0/27. These are
**additional host-only diagnostic cases**, not original frozen private acceptance
and not independent model review. Closeout deterministically reauthenticated
these recorded observations against the unchanged archived candidate, without
model inference, source mutation or rerunning the coding episode.

## Restoration, authority and interrupted closeout

Candidate file SHA256 is
`ea9619b09ebaca244b358179fecc7c952be37e07edac66ba5171f19b3af3b119`.
The [archived candidate](code-audit/productive-native-markdown-20261103/native/worker/final-source.py)
is preserved byte for byte. Restored production
`src/devtools/resources/filesystem/models/markdown/file.py` matches the frozen
baseline and assignment baseline bytes, SHA256
`a5510a1b30945060c3d1438f0832cc8ffe5d9ee6248d5e24bd66feea6c5fb645`.
Git baseline blob is `3f40cce10b4cf600932cfcd93a075b8fad12fa22`;
candidate blob is `1f31f4a275d11de780c8f5bef741e040bd2a1b1a`.
The [Checkout release](code-audit/productive-native-markdown-20261103/checkout-release.json)
authenticates return to main at the preparation commit. No active Checkout
owner remains. The consumed dispatch identity is
`9e06efd49b8bf8bbe2bd99634ff21a8c564bbe2b99521053d15b0a358d2d5f17`;
the slot is not reset or made reusable. No reviewer subject, review dispatch,
integration plan or candidate installation was created.

At interruption recovery, local main and remote main still matched preparation
`3d9de0a5`, with no staged or tracked changes. The prior cleanup receipt existed
and its temporary file was absent, but the terminal outcome archive and closeout
commit were missing. A reported successful script exit did not establish
publication. Recovery appended the missing authentic evidence and completed
documentary publication; it makes no unsupported claim about why the earlier
script stopped producing records.

The [cleanup receipt](code-audit/productive-native-markdown-20261103/temporary-test-cleanup.json)
records removal of only the run-owned public diagnostic at 17:27:48 UTC after
restoration, preserving exact public bytes in the preparation archive. Recovery
authenticated its absence and hash correspondence and performed no further
cleanup. All 216 guarded files, 630 historical files, 192 historical native files
and thirteen forensic files retained their recorded identities. All 903 RI ledger
rows remain unchanged: 606 experimental, 94 fixture and 203 history. Historical
branch refs and active standing policy
`f712a8e21f0c07485fa46f904ea6f63a984e1fb6ae69637a5242b045fe2defcf`
remain intact. Unrelated untracked source-grounding journals were preserved and
excluded from publication.

The [integrity receipt](code-audit/productive-native-markdown-20261103/integrity-resumed.json)
records the same running, healthy persistent provider container, image, command
and mounts, with one idle 65,536-token slot. Closeout changed no service state.
Inspector was observed clean on `feat/agent-inspector` at
`4ee14926618c4e062291eeff8fe508cd364ce606`; its independent worktree was untouched
and may subsequently advance.

## Validation, disposition and next engineering action

All 1,077 declared physical production/configuration hashes and corresponding Git
blobs match the established [protected receipt](code-audit/structured-acceptance-review-20261103/protected-authorized.json)
for `4fe7ac6c90c50e60cf7470ae1dcfa011a6956e21`: 4,269 passes, two optional skips,
100% configured production line/branch coverage. Python, interpreter, platform
and installed package comparisons match. The inherited environment fingerprint
differs; complete ignored/external environment equivalence is not claimed.
This is reused historical evidence for unchanged executable inputs in an
explicitly evidence-only closeout, not a new protected pass or fresh-only
acceptance. No full protected suite was run for this closeout.

The [packet index](code-audit/productive-native-markdown-20261103/README.md)
and immutable manifest retain the genuine outcome, original patch/source,
private oracle, provider observations, standing decisions and host diagnostics.
Bounded checks authenticate sealed records, raw archive and Git object bytes,
document links, Intake consistency, root layout, supported-source Ruff/formatting,
history/RI identities and whitespace. Package docs, taxonomy, architecture,
backlog status and historical ledger require no changes: no production behavior
or architecture was delivered. B-0053 remains BACKLOG; its native coding result
remains BLOCKED and its execution slot remains consumed.

The smallest productive next engineering action is a separately authorized
bounded Markdown closing-marker boundary repair that preserves both attached
literal suffixes and empty headings, using the archived failure as regression
evidence. It belongs in the existing Markdown owner; no framework or review
transport redesign is indicated by this episode. This closeout creates no new
coding assignment, backlog item, continuation or review dispatch.
