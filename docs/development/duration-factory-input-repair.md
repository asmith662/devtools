# Duration factory-input repair

## Delivered scope

Normal [PR #25](https://github.com/asmith662/devtools/pull/25) first integrated the
exact twelve-path Core Identity/Time audit at `510be32bc72c1b7646af04e4cea59a8e7c6dbad8`, tree
`78d29ae1306e8dc1bd989f1957642d59a44e83aa`. This was documentation/Intake only: selected identities, JSON,
563 links, 56 Intake chains, layout, whitespace and all thirteen forensics were
reauthenticated before merge. No independent review was fabricated.

The separately authorized factory correction is **implemented and merged** through
[PR #26](https://github.com/asmith662/devtools/pull/26): production
`171699ac6de9ddb15f51b4cee440b8ee412646be`, accepted main `7bc03e9d22c919314103375934f4bf74cac5e27d`, validated/accepted tree
`bf710e4bff7af1e1c6a53f55938206fa2ea16ee4`. Remote ref, parents, four Git blobs and 930 physical validation
inputs were independently checked, and local main fast-forwarded safely.
The [complete receipt](../research/code-audit/duration-factory-repair-20261026.json)
retains commands, timestamps, durations, exits, hashes, coverage and outcomes.

## Original evidence and correction

Existing proposal [ea7c18ff](../backlog/proposals/ea7c18ff-8ca5-46b8-a230-1bfdf92c7f74/proposal.json) is the
single owner. Before source changes, its six permanent regressions failed with
the intended DID NOT RAISE assertions and 87 compatibility controls passed.
`nanoseconds(-1)`, `nanoseconds(-499)`, `seconds(-1e-12)`,
`milliseconds(-1e-9)`, `minutes(-1e-12)` and `hours(-1e-14)` all previously
returned zero. The original source blob was
`2ad7166e890795ddbdef968fb3f0b75d80de4ab5`.

Each of the five public factories now calls one private Duration-owned sign
admission helper before timedelta conversion. Negative finite numeric input
raises ValueError before rounding. No signature, return type, dependency,
generic numeric validator, clock/deadline abstraction or other domain changes.
The existing stored-value validation remains independently necessary.

Zero and negative floating zero, positive microsecond/half-even rounding,
NaN ValueError, both infinities' OverflowError, nonnegative range overflow and
unsupported-value TypeError retain their behavior. Negative finite input is
refused before any range conversion. Decimal/string/None/object controls protect
the native unsupported-input path. Literal expected timedeltas are not computed
through the factory under test. Actual Commands timeout consumption has an
additional independently expected 1500ns-to-2us regression.

The exact final six assertions were also executed against the original Git-object
Duration class in an isolated process: six intended failures, no import or
collection failure, no physical source copy or production modification. The old
Qwen task, result and restored candidate remain historical evidence; that
candidate was not reused as the implementation.

## Arithmetic compatibility

`__mul__`, `__rmul__` and `__truediv__` are unchanged; their method hashes match
the baseline. Arithmetic continues to validate the represented timedelta result.
Tiny negative products/quotients can round to zero, and zero scaled negatively
remains zero. Ordinary represented-negative results still refuse.
Permanent literal assertions retain those cases. A future raw-factor/divisor
policy would require an explicit compatibility decision; it is not an unfinished
acceptance criterion for this delivered factory repair.

## Validation and integration

- Final committed gate: **3,035 passed, two opt-in live skips, 100% configured production
  branch coverage**, exit 0; 1109.86s pytest /1111.979878s managed elapsed.
- Coverage: 12013/12013 statements and 3010/3010 branches, zero missing;
  unchanged 589 excluded lines. No threshold or exclusion changed.
- 415 focused Core/Commands/Tools/Runtime/usage tests pass on the committed source;
  415 selected post-main tests pass on the accepted tree.
- Maintained Ruff over src/tests/apps/scripts, supported formatter scope and
  configured strict mypy pass; mypy reports 520 files. The formatter's COM812
  advisory remains a warning, not a failure or reason to change configuration.
- Gate commit `171699ac6de9ddb15f51b4cee440b8ee412646be` and tree `bf710e4bff7af1e1c6a53f55938206fa2ea16ee4` are authenticated, with input
  aggregate `e94a6e84d196694a702ec25f8635225c363c9d90bfd4732260c0802514af055e` and log SHA-256
  `fa174c0489cdb04d037360b0a62b43c2ffe42799adb77018ea981074ebb94cd9`. All 930 explicitly recorded inputs remained unchanged.
  These are bounded file identities, not universal transitive environment closure.

Normal GitHub merges used the actual repository permissions/rules. At inspection
main had no server protection/rulesets or required checks/reviews; existing host
validation remained mandatory. No approvals, CI statuses or WorkCycle authority
were invented. No force-push, protection change or branch deletion occurred.
Known own text files rematerialized by Git's line-ending filters were reconciled
to their exact gate bytes only after checking committed Git identity and hashes;
unknown bytes were never overwritten. All thirteen forensics remain unchanged.
Documentation-only closeout changes no executable inputs and does not reuse old
gate evidence for a changed source/test/configuration tree.

## Canonical disposition and next work

An append-only ADVISORY records IMPLEMENTED_AND_MERGED against the existing
proposal, retaining its administrative PENDING_REVIEW state. The factory scope
must not be scheduled again. No B-number, approval, grant, parent closure or
duplicate proposal was created. Original audit/version pins and scientific
records are preserved; maintenance overlays identify the authored source/test
delta instead of transferring review credit silently.

Next bounded domain review: remaining filesystem codecs/structured models,
including the existing CSV spelling proposal and B-0048 Python-version
compatibility, then ModelInteraction/serving. This assignment starts none of
those reviews. Other Core/platform/lifecycle/Evidence responsibilities remain
separate. RI 93/93 original fixtures and 606/606 experimental paths keep their
defined review depth; 188 historical versions remain outstanding. A+C remains
unapproved, and no successor-session dossier is prepared.
