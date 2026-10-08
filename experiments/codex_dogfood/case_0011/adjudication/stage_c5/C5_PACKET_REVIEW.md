# C.5 packet pre-review transparency

PREPARED ONLY. No semantic mappings have been adjudicated; this is not C.5 gold.

The reviewer receives only four regular files: C5_INSTRUCTIONS.md, manifest.json, packet.json.gz and integrity.json. No queries, answer resource paths/filenames, ranks, scores or results are included. Integrity digests bind the frozen inputs without exposing answers. Location names in three unit statements are replaced by semantic descriptions; all other statements are verbatim.

## Exact instructions

# Stage C.5 semantic information-need coverage

Verify integrity.json, archive bytes and decompressed payload before reading.
Use only these four supplied regular files. Do not seek a repository checkout,
Git, source files, lexical queries, acquisition outputs, resource answer paths,
ranks, scores, costs, treatment arms, models, confirmation or Stage D outcomes.

Determine whether the frozen manual InformationNeeds semantically cover the
required information units. This is semantic review, not implementation or
acquisition evaluation. Every need must be compared to every unit. Do not prune
by shared words or owning obligation: cross-obligation coverage is allowed.
ALL units inside an alternative are complementary; ANY complete alternative
suffices for its obligation. A REQUIRED unit is necessary in at least one
acceptable witness alternative, not necessarily in every valid task solution.
Do not mix incompatible alternatives or flatten them to a simultaneous union.

For each mapping choose exactly one frozen mapping label and give a rationale.
DIRECTLY_COVERS must state (1) the fact the need seeks, (2) the fact the unit
establishes, and (3) why answering the need would establish the unit. Shared
wording alone is insufficient. Preserve partial and ambiguous outcomes.
Derive unit coverage only from semantic decisions using the frozen definitions;
AMBIGUOUS_ONLY takes precedence over UNCOVERED when ambiguous mappings remain.
U1 requires DIRECT coverage. Classify every need semantically, with rationale,
using the supplied need labels; do not infer usefulness from word overlap.
MISFORMULATED and AMBIGUOUS require explicit reviewer judgment rather than a
mechanical shortcut based only on mapping counts.

The statements describe required facts with answer-location names omitted.
Opaque unit and alternative identities carry no quality or chronological rank.
Freeze the complete mapping decisions, rationales, need classifications,
coverage derivation, identity checks and output digests before any later join.
Do not change the task, obligations, needs, units or alternatives. Do not perform
Stage D or conclude U1 effectiveness. Stop if packet integrity or blindness fails.

## Task

Add an optional caller-directed UTF-8 byte ceiling to copied ModelRequest assembly for explicitly planned repository Context.
The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.
Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.
Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.
Reject rather than truncate, omit items, change representation, or silently select a smaller plan; a zero ceiling permits only zero-byte rendered Context.
Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.
Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.
Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.
Update governing architecture and package documentation and run protected development validation with the established tooling configuration.
Do not implement automatic selection, token estimation, truncation, query changes, semantic resolution, persistence, or agent execution.

## Obligations and criteria

### ownership

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"ownership-information","statement":"Identify the existing common assembly ownership and dependency constraints that the byte ceiling must preserve."},"identity":"ownership","predicate":"Establish common Context Planning capacity ownership and allowed dependencies.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":126,"line":1,"origin":"VERBATIM_TASK","start":0,"text":"Add an optional caller-directed UTF-8 byte ceiling to copied ModelRequest assembly for explicitly planned repository Context.\n"},{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"}]}


### bytes

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"bytes-information","statement":"Identify which rendered text is appended, which headings/separators count, and how UTF-8 and newlines are preserved without counting the original task."},"identity":"bytes","predicate":"Establish exact rendered Context byte-count and newline semantics.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"}]}


### ceiling

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"ceiling-information","statement":"Identify existing validation/error conventions for None, nonnegative integers, booleans, equality and pre-assembly rejection without truncation."},"identity":"ceiling","predicate":"Establish optional limit validation and rejection behavior.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":296,"line":2,"origin":"VERBATIM_TASK","start":126,"text":"The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.\n"},{"end":694,"line":4,"origin":"VERBATIM_TASK","start":511,"text":"Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.\n"},{"end":849,"line":5,"origin":"VERBATIM_TASK","start":694,"text":"Reject rather than truncate, omit items, change representation, or silently select a smaller plan; a zero ceiling permits only zero-byte rendered Context.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


### request

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"request-information","statement":"Identify copying and Prompt construction semantics that preserve original task, role and every other ModelRequest field."},"identity":"request","predicate":"Establish copied-request and original-task preservation.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":126,"line":1,"origin":"VERBATIM_TASK","start":0,"text":"Add an optional caller-directed UTF-8 byte ceiling to copied ModelRequest assembly for explicitly planned repository Context.\n"},{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


### frame

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"frame-information","statement":"Identify existing repository/snapshot/content checks, item order and exact-text/native provenance contracts that capacity checking cannot weaken."},"identity":"frame","predicate":"Establish disclosure provenance, order and frame integrity constraints.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":296,"line":2,"origin":"VERBATIM_TASK","start":126,"text":"The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


### exports

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"exports-information","statement":"Identify the public package boundary and export conventions for the optional assembly argument."},"identity":"exports","predicate":"Establish public package export conventions.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


### tests

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"tests-information","statement":"Identify existing tests/fixtures for exact text and copied assembly, invalid or stale frames, and numeric/UTF-8 boundary validation."},"identity":"tests","predicate":"Establish focused boundary, frame and preservation test conventions.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


### documentation

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"documentation-information","statement":"Identify current documentation ownership and claims about Context capacity, rendering and assembly that need an accurate bounded feature description."},"identity":"documentation","predicate":"Establish governing architecture and package documentation updates.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"}]}


### validation

{"applicability_condition":null,"author":"caller experiment designer; manual before source inspection","criterion":{"name":"validation-information","statement":"Identify the protected validation entry point and current test/type/style configuration required by the task."},"identity":"validation","predicate":"Establish protected development validation and tooling constraints.","provenance":"manual interpretation before source inspection","requirement":"mandatory","task_basis":[{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"}]}


## Frozen InformationNeeds

{"anchors":["ModelRequest"],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/ownership/assembly-owner","obligation":"ownership","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Place the requested capacity check in its existing owner.","statement":"Which common Context Planning contract owns copied ModelRequest assembly?","task_basis":[{"end":126,"line":1,"origin":"VERBATIM_TASK","start":0,"text":"Add an optional caller-directed UTF-8 byte ceiling to copied ModelRequest assembly for explicitly planned repository Context.\n"},{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/ownership/dependencies","obligation":"ownership","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The task explicitly forbids adding these dependencies.","statement":"What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?","task_basis":[{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/bytes/rendered-boundary","obligation":"bytes","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The ceiling counts the actual rendered payload, not only item bodies.","statement":"What exact rendered Context text, headings and separators are appended during assembly?","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/bytes/encoding","obligation":"bytes","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Non-ASCII and newline bytes must be counted faithfully.","statement":"What existing UTF-8 and newline handling contracts preserve exact rendered text?","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/ceiling/validation","obligation":"ceiling","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"New ceiling validation must follow existing conventions.","statement":"What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans?","task_basis":[{"end":296,"line":2,"origin":"VERBATIM_TASK","start":126,"text":"The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.\n"},{"end":694,"line":4,"origin":"VERBATIM_TASK","start":511,"text":"Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/ceiling/rejection","obligation":"ceiling","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Oversized Context must fail without silently changing the selected information.","statement":"What assembly contract permits rejection before modifying a request, without truncating or omitting items?","task_basis":[{"end":694,"line":4,"origin":"VERBATIM_TASK","start":511,"text":"Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.\n"},{"end":849,"line":5,"origin":"VERBATIM_TASK","start":694,"text":"Reject rather than truncate, omit items, change representation, or silently select a smaller plan; a zero ceiling permits only zero-byte rendered Context.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"}]}


{"anchors":["ModelRequest"],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/request/copy","obligation":"request","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The byte guard must not change unrelated request state.","statement":"How does copied ModelRequest assembly preserve all fields other than the appended Context?","task_basis":[{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/request/prompt","obligation":"request","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The original task is excluded from the ceiling and remains unchanged.","statement":"How are the original task text and Prompt role preserved when Context is appended?","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"}]}


{"anchors":["ContextDisclosure","DisclosurePlan"],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/frame/binding","obligation":"frame","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Foreign or stale frames must retain their existing rejection semantics.","statement":"What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?","task_basis":[{"end":296,"line":2,"origin":"VERBATIM_TASK","start":126,"text":"The caller supplies an already materialized ContextDisclosure from a DisclosurePlan and an optional maximum Context byte count; None retains existing unlimited behavior.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/frame/items","obligation":"frame","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Counting and rejection must not rewrite materialized information.","statement":"What contracts retain item order, exact item text and native disclosure provenance?","task_basis":[{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/exports/public-boundary","obligation":"exports","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The feature must be usable through established public boundaries.","statement":"What public Context Planning package exports expose copied assembly to callers?","task_basis":[{"end":1264,"line":7,"origin":"VERBATIM_TASK","start":1078,"text":"Keep capacity checking in common Context Planning without a dependency on a language-specific adapter or Retrieval, and preserve existing whole-resource and qualified-reference choices.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/tests/text-boundaries","obligation":"tests","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Extend real preservation tests rather than invent incompatible text assumptions.","statement":"Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/tests/frame-rejection","obligation":"tests","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The new ceiling must preserve existing invalid-frame handling.","statement":"Which tests establish foreign or stale repository/snapshot/content frame rejection?","task_basis":[{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/tests/request-preservation","obligation":"tests","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The requested unlimited, invalid-limit and request-immutability cases need current test conventions.","statement":"Which tests establish copied-request preservation and invalid argument validation?","task_basis":[{"end":694,"line":4,"origin":"VERBATIM_TASK","start":511,"text":"Accept a nonnegative integer ceiling, reject booleans and other invalid values, allow equality at the boundary, and reject an oversized disclosure before creating a modified request.\n"},{"end":1078,"line":6,"origin":"VERBATIM_TASK","start":849,"text":"Preserve item order, exact item text, native disclosure provenance, repository/snapshot/content frame checks, the original task, Prompt role, and every other ModelRequest field; failure must leave the caller's objects unchanged.\n"},{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/documentation/architecture","obligation":"documentation","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Document a caller guard without implying automated planning.","statement":"What governing architecture documentation distinguishes Context capacity from automatic selection?","task_basis":[{"end":849,"line":5,"origin":"VERBATIM_TASK","start":694,"text":"Reject rather than truncate, omit items, change representation, or silently select a smaller plan; a zero ceiling permits only zero-byte rendered Context.\n"},{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"},{"end":1790,"line":10,"origin":"VERBATIM_TASK","start":1653,"text":"Do not implement automatic selection, token estimation, truncation, query changes, semantic resolution, persistence, or agent execution.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/documentation/package","obligation":"documentation","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"Document the precise byte-count scope and unchanged behavior.","statement":"What package documentation describes rendered Context and copied assembly contracts?","task_basis":[{"end":511,"line":3,"origin":"VERBATIM_TASK","start":296,"text":"Count the exact rendered Context text that would be appended, including its headings and separators, encoded as UTF-8; exclude the caller's original task text from this count and preserve existing newline handling.\n"},{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/validation/protected-entry","obligation":"validation","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The future implementation must use the protected validation contract.","statement":"What established entry point runs protected development validation?","task_basis":[{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"}]}


{"anchors":[],"author":"caller experiment designer; manual before source inspection","identity":"case-0011-context-utf8-ceiling/validation/configuration","obligation":"validation","provenance":"manual from task/obligation/criterion only; before source inspection","reason":"The future tests and public argument must follow current configuration.","statement":"What established tooling configuration constrains test, type and style validation?","task_basis":[{"end":1512,"line":8,"origin":"VERBATIM_TASK","start":1264,"text":"Follow public package exports and existing validation/error conventions. Add focused tests for unlimited behavior, exact byte boundaries, non-ASCII text, newline handling, invalid ceilings, foreign or stale frames, and copied-request preservation.\n"},{"end":1653,"line":9,"origin":"VERBATIM_TASK","start":1512,"text":"Update governing architecture and package documentation and run protected development validation with the established tooling configuration.\n"}]}


## Required unit statements and membership

{"alternative_membership":["alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6"],"identity":"unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027","obligations":["exports"],"statement":"The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2","obligations":["frame"],"statement":"Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values."}


{"alternative_membership":["alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158"],"identity":"unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c","obligations":["validation"],"statement":"The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation."}


{"alternative_membership":["alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb"],"identity":"unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580","obligations":["documentation"],"statement":"The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed"],"identity":"unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394","obligations":["tests"],"statement":"The common assembly test checks unchanged original task, Prompt role, shared settings/conversation/provider values, task-before-Context placement and replace(assembled, prompt=task.prompt) == task."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed"],"identity":"unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42","obligations":["tests"],"statement":"Common planning tests build retained snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69","obligations":["frame"],"statement":"The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87","obligations":["frame"],"statement":"Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content."}


{"alternative_membership":["alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb"],"identity":"unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371","obligations":["documentation"],"statement":"The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd","obligations":["frame"],"statement":"Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed."}


{"alternative_membership":["alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5"],"identity":"unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30","obligations":["ceiling"],"statement":"The existing request-side optional integer validator accepts None, explicitly rejects bool and non-int, and raises a descriptive ValueError; its positive token domain must not override the task's nonnegative byte domain."}


{"alternative_membership":["alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158"],"identity":"unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c","obligations":["validation"],"statement":"The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable."}


{"alternative_membership":["alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1"],"identity":"unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7","obligations":["request"],"statement":"ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6","obligations":["frame"],"statement":"Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices."}


{"alternative_membership":["alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f","alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c"],"identity":"unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7","obligations":["ownership"],"statement":"Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency."}


{"alternative_membership":["alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5","alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638","alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc"],"identity":"unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605","obligations":["ceiling"],"statement":"The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call."}


{"alternative_membership":["alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1","alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1"],"identity":"unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c","obligations":["bytes","request"],"statement":"Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode(\"utf-8\")) independently of the task length, and preserves each embedded string and its newline bytes."}


{"alternative_membership":["alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158"],"identity":"unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9","obligations":["validation"],"statement":"Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed"],"identity":"unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc","obligations":["tests"],"statement":"Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference."}


{"alternative_membership":["alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6"],"identity":"unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14","obligations":["exports"],"statement":"The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__."}


{"alternative_membership":["alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1"],"identity":"unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702","obligations":["request"],"statement":"Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca","obligations":["frame"],"statement":"Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed"],"identity":"unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580","obligations":["tests"],"statement":"Common planning tests distinguish changed snapshot from changed retained content under the same snapshot identity and exercise missing-resource rejection with replace and pytest.raises."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf","obligations":["frame"],"statement":"Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained."}


{"alternative_membership":["alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f","alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c"],"identity":"unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2","obligations":["ownership"],"statement":"Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed","alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638"],"identity":"unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7","obligations":["ceiling","tests"],"statement":"Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs."}


{"alternative_membership":["alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1"],"identity":"unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08","obligations":["bytes"],"statement":"Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de","obligations":["frame"],"statement":"Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance."}


{"alternative_membership":["alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158"],"identity":"unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965","obligations":["validation"],"statement":"Project configuration selects Python 3.12, Ruff ALL with documented exceptions and 88-column formatting, and strict mypy over source, test and experiment trees with explicit package bases and src import base."}


{"alternative_membership":["alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063"],"identity":"unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3","obligations":["frame"],"statement":"Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation."}


{"alternative_membership":["alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc"],"identity":"unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50","obligations":["ceiling"],"statement":"Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError."}


{"alternative_membership":["alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed"],"identity":"unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329","obligations":["tests"],"statement":"The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order."}


## Alternative structures

[{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1","member_logic":"ALL_COMPLEMENTARY","units":["unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c","unit-e3c24d637a4dca9783a7b6b86dbe1abcda4ad0117b8933cc798af53004501e08"]}],"obligation":"bytes"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5","member_logic":"ALL_COMPLEMENTARY","units":["unit-50dcfb5fd4a867c57ed46736f5e8858a763c0a2f62aecc6e809ad822716dbb30","unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605"]},{"identity":"alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc","member_logic":"ALL_COMPLEMENTARY","units":["unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605","unit-f7ba939e852e8f0f8e89d99664675a3cd8f8c1d48ac0acdc0bc9b4ebb7d22c50"]},{"identity":"alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638","member_logic":"ALL_COMPLEMENTARY","units":["unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605","unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7"]}],"obligation":"ceiling"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb","member_logic":"ALL_COMPLEMENTARY","units":["unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580","unit-33a494497198cadf88145cc45dc05ca55e09e6405588ce5cdd12c4f2c65e8371"]}],"obligation":"documentation"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6","member_logic":"ALL_COMPLEMENTARY","units":["unit-0057f1c75647a0b3e2d678bb704888665ee7ffbfeec0e56f27c501027a03c027","unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14"]}],"obligation":"exports"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063","member_logic":"ALL_COMPLEMENTARY","units":["unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2","unit-1bb99811c2a45a9ce6d5dc32206e23d64f9fffa2d10fa642ca5f4ea6ce518c69","unit-21e7319918686d72a7f9e79f31bc68ed4922858fa7bfa299d351ea43ef3b0b87","unit-4b3c320635122396ffe052357de8b5f96f074e35017c0331a650de95844eaccd","unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6","unit-a2c6080b9a63cdbb8cb2057c41ba2c618614bc672246ada53ce1f470cf4d7fca","unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf","unit-eac315eb2a9f6a5634e094a5d4ef2960559030b62385b832a57f0f8d893b72de","unit-f2f60cee7a81549ef3634c65a08ec026019e35505a0b7457ff348af70571ace3"]}],"obligation":"frame"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c","member_logic":"ALL_COMPLEMENTARY","units":["unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7","unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2"]},{"identity":"alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f","member_logic":"ALL_COMPLEMENTARY","units":["unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7","unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2"]}],"obligation":"ownership"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1","member_logic":"ALL_COMPLEMENTARY","units":["unit-5bf714afea56a8406609fdff47f7aa1db5a9fed50ba652b39884aca7ddf7c8c7","unit-7a4fab44afff20a76dbc7edba7d33f2895f0cd322bdc37d5626f2ca74a792e0c","unit-a090f45af360240ad7ce7630ffd09098a6a1b7887839d5266196a6f645880702"]}],"obligation":"request"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed","member_logic":"ALL_COMPLEMENTARY","units":["unit-1979aa6106ebf66bce887d463ebbcb9d0745566f1875c359373e6e5afb72a394","unit-1bb673f66452efaf4d344988ed48b3011927a477ec8a2c9b4f5e77b2fd81aa42","unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc","unit-a3e3b3430e6bfb7351af007e1cfff42c912e499682a4d3e332c4ac6b7e043580","unit-d553be405368fb0607f76e8e953d24dcecf462b0308474311add157d55b57fc7","unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329"]}],"obligation":"tests"},{"alternative_logic":"ANY_COMPLETE_ALTERNATIVE","alternatives":[{"identity":"alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158","member_logic":"ALL_COMPLEMENTARY","units":["unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c","unit-5991a5afbd7d664372fc5b2357e8fbcacfa5d73d5560dcd97f853aa279e36b1c","unit-7ec311946c51700e892b24d725de3a5b89904e240505c5e5e79e4d1736e56bb9","unit-f0a8cdef8232323f591cb10fdee77345e0352146b082c5bea0fb239ac9602965"]}],"obligation":"validation"}]


## Complete mapping frame

18 needs × 32 units = 576 pairs. Includes all cross-obligation pairs; no lexical pruning.

## Labels

{"mapping_labels":{"AMBIGUOUS":"The semantic relationship cannot be defended confidently from the packet.","DIRECTLY_COVERS":"The information need explicitly seeks evidence capable of establishing the required unit.","DOES_NOT_COVER":"The need asks a materially different repository question.","PARTIALLY_COVERS":"The need seeks only part of the required unit and would not reasonably establish it completely."},"need_labels":{"AMBIGUOUS":"Cannot classify defensibly.","MISFORMULATED":"Intended task concern is recognizable, but the need's statement cannot reasonably guide acquisition of the required fact.","NECESSARY":"Directly covers at least one required unit that no other need directly covers.","PARTIAL_ONLY":"Has partial mappings but no direct mapping.","UNNECESSARY":"Has no direct or partial mapping to required units.","USEFUL_REDUNDANT":"Directly covers required units, but all are directly covered by another need."},"unit_coverage":{"AMBIGUOUS_ONLY":"No direct or partial mapping and at least one AMBIGUOUS.","COVERED":"At least one DIRECTLY_COVERS mapping.","PARTIAL_ONLY":"No direct mapping and at least one PARTIALLY_COVERS.","UNCOVERED":"No direct, partial or ambiguous mapping."}}


UNCOVERED excludes ambiguous-only units; AMBIGUOUS_ONLY takes precedence. U1 requires DIRECT coverage. Need classifications require future semantic reviewer decisions.
