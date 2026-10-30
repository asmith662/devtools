# Recoverable native navigation arguments

`find_source.path` is optional. A supplied value must be an exact authorized
file-resource address; directories and prefixes are unsupported. Omitting it
searches the authorized resource set under existing result/scope limits. Both
ordinary and task-directed native descriptors disclose this contract.

Tools owns pure selection validation. `ScopedSourceNavigationTool.validate_selection`
checks the existing selection semantics; ordinary `validate` also checks source
currentness. ToolRunner still validates and executes once without catching failures.
Agents owns native argument parsing, candidate acquisition and correlated feedback.

The coding host catches only parsing/type errors from its effect-free navigation
selection construction. Candidate acquisition checks currentness outside its
refusal handler and catches only pure selection `ToolInputError` before native
dispatch. Refusal feedback retains the original call ID, says navigation/source
acquisition was not entered, grants no edit witness, explains the constraint and
describes valid selection. It lists no unauthorized resources and reflects no
arbitrary parser exception text. No call is silently corrected or replayed.

Each invalid attempt consumes the existing acquisition allowance and gets a known
refusal acknowledgment. Exhaustion retains the original action-budget feedback;
the model-call bound also remains. Multi-call responses retain independent ordered
results. Authorization, currentness, cancellation and post-entry failures propagate
unchanged, preserving uncertain effects and prior acknowledgments. A refusal is
Tool feedback, not source or permission. Exact read/edit authority is unchanged.

Maintained neutral tests exercise invalid selection, later valid search, exact
read, grounded edit, managed fixed check and restoration through the existing
coding process. Other cases cover malformed types, foreign paths, finite repeated
refusals, batches, admission failures and post-entry errors. Existing Qwen and
portable consumers continue using the same descriptors and process. Scripted
continuation is framework evidence, not model engineering competence.

The motivating [alternative-worker episode](../../experiments/alternative_b0035/REPORT.md)
remains closed with its original unacknowledged action. This correction does not
manufacture its missing result or resume its historical invocation.

The [fresh bounded real-worker assessment](../../experiments/navigation_recovery/REPORT.md)
received two correlated argument refusals and continued to a normal text stop.
The model did not correct its argument or submit an edit. Framework recovery
worked; useful B-0035 implementation was not established.
