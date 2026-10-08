# Case 0011 final reviewed C.5

Treatment-blind deterministic materialization of immutable bounded reconciliation-v2 decisions. No pair was adjudicated anew. Strict frozen-rule coverage and secondary granularity-aware coverage remain separate.

## Exact final counts

pair_labels: `{"AMBIGUOUS": 0, "DIRECTLY_COVERS": 15, "DOES_NOT_COVER": 506, "PARTIALLY_COVERS": 55}`

strict_units: `{"AMBIGUOUS_ONLY": 0, "COVERED": 15, "PARTIAL_ONLY": 15, "UNCOVERED": 2}`

needs: `{"AMBIGUOUS": 0, "MISFORMULATED": 0, "NECESSARY": 10, "PARTIAL_ONLY": 8, "UNNECESSARY": 0, "USEFUL_REDUNDANT": 0}`

strict_alternatives: `{"AMBIGUOUS": 0, "FULLY_DIRECTLY_COVERED": 0, "INCOMPLETE": 12}`

granularity: `{"AMBIGUOUS_GRANULARITY": 0, "ATOMIC_FOR_NEED_MAPPING": 26, "COLLECTIVELY_COVERABLE": 6, "OVERCOMPOUND_FOR_PAIRWISE_MAPPING": 0}`

collective_sets: `{"AMBIGUOUS": 0, "INSUFFICIENT": 4, "VALID_BUT_NOT_MINIMAL": 0, "VALID_MINIMAL_COLLECTIVE_SET": 3}`

granularity_aware_units: `{"GRANULARITY_AWARE_AMBIGUOUS": 0, "GRANULARITY_AWARE_COVERED": 18, "GRANULARITY_AWARE_PARTIAL": 12, "GRANULARITY_AWARE_UNCOVERED": 2}`

granularity_aware_alternatives: `{"AMBIGUOUS": 0, "FULLY_COVERED_ONLY_COLLECTIVELY": 0, "FULLY_DIRECTLY_COVERED": 0, "INCOMPLETE": 12}`

## COVERED units

### U01

The planning public package explicitly imports and lists its common renderer, rendered value and assembler in __all__.

Direct needs: ['N11']; partial needs: []; diagnostic: GRANULARITY_AWARE_COVERED.

### U05

The common assembly test checks unchanged original task, Prompt role, shared settings/conversation/provider values, task-before-Context placement and replace(assembled, prompt=task.prompt) == task.

Direct needs: ['N14']; partial needs: ['N07', 'N08', 'N12']; diagnostic: GRANULARITY_AWARE_COVERED.

N07 partial components:

source_mapping_1 covered: preservation of original task, role and other request values; missing: the test-specific shared-value assertions, task-before-Context check and inverse-replacement equality assertion

source_mapping_2 covered: preservation of original task, role and unrelated request fields; missing: the specific test's task-before-Context assertion and replacement-back equality assertion

N08 partial components:

source_mapping_1 covered: original task and Prompt role preservation and task-before-Context placement; missing: shared settings/conversation/provider values and the inverse-replacement equality assertion in the test

source_mapping_2 covered: unchanged original task and Prompt role during appending; missing: the test's shared settings/conversation/provider checks, placement assertion and replacement-back equality

N12 partial components:

source_mapping_1 covered: exact original task text and its placement relative to Context; missing: role, shared non-prompt values and inverse-replacement equality assertion

source_mapping_2 covered: the test's unchanged task text and task-before-Context placement; missing: Prompt role, shared non-text request values and replacement-back equality

### U06

Common planning tests build retained snapshots by writing exact UTF-8 bytes and observing explicitly addressed resources.

Direct needs: ['N12']; partial needs: []; diagnostic: GRANULARITY_AWARE_COVERED.

### U08

Qualified-reference materialization checks the source dependency repository/snapshot, source occurrence snapshot/address, resource presence and equality with retained source content.

Direct needs: ['N09']; partial needs: ['N13']; diagnostic: GRANULARITY_AWARE_COVERED.

N13 partial components:

Covered: Source frame/content mismatch and missing-resource rejection.

Missing: Complete source dependency repository/snapshot and occurrence snapshot/address checks and equality with retained source content.

### U09

The governing architecture document is the canonical current cross-package architecture overview and contains the current common planning/materialization/rendering/assembly description to extend with the bounded byte feature.

Direct needs: ['N15']; partial needs: []; diagnostic: GRANULARITY_AWARE_COVERED.

### U11

The existing request-side optional integer validator accepts None, explicitly rejects bool and non-int, and raises a descriptive ValueError; its positive token domain must not override the task's nonnegative byte domain.

Direct needs: ['N05']; partial needs: ['N14']; diagnostic: GRANULARITY_AWARE_COVERED.

N14 partial components:

source_mapping_1 covered: numeric request admission and descriptive invalid-value errors evidenced by tests; missing: the complete request-side validator implementation convention and its positive-token/nonnegative-byte domain distinction

source_mapping_2 covered: observable optional integer invalid-type/error conventions used by request tests; missing: the existing request validator as the implementation precedent and the explicit positive-token versus nonnegative-byte domain distinction

### U13

ModelRequest is a frozen dataclass with prompt, settings, conversation, provider_settings and tools.

Direct needs: ['N07']; partial needs: ['N06', 'N14']; diagnostic: GRANULARITY_AWARE_COVERED.

N06 partial components:

Covered: Request immutability supporting failure without mutation.

Missing: Complete declared prompt, settings, conversation, provider_settings and tools inventory.

N14 partial components:

Covered: Retention of tested settings, conversation and provider values.

Missing: Frozen dataclass declaration and complete prompt/settings/conversation/provider_settings/tools inventory.

### U18

Project configuration enforces strict pytest configuration/markers and production devtools branch coverage at a 100 percent threshold.

Direct needs: ['N18']; partial needs: []; diagnostic: GRANULARITY_AWARE_COVERED.

### U21

Common assembly returns dataclasses.replace(task_request, prompt=Prompt(prompt_content, role=task_request.prompt.role)), replacing only Prompt and retaining its role.

Direct needs: ['N07']; partial needs: ['N06', 'N08', 'N14']; diagnostic: GRANULARITY_AWARE_COVERED.

N06 partial components:

source_mapping_1 covered: creation of a replacement request rather than mutation of the caller request; missing: replacement of only Prompt with explicit preservation of its role

source_mapping_2 covered: final replacement of a copied request, permitting earlier rejection; missing: the Prompt constructor and explicit preservation of the original Prompt role

N08 partial components:

Covered: Constructing appended prompt content with the original Prompt role.

Missing: dataclasses.replace replacing only prompt and consequently retaining all other request fields.

N14 partial components:

Covered: Prompt-role and non-prompt-field preservation exercised by tests.

Missing: Actual dataclasses.replace call replacing only Prompt with the role-preserving constructor.

### U22

Qualified-reference materialization checks target support/subject snapshots, target resource presence, subject resource-dependency identity and equality with retained target support.

Direct needs: ['N09']; partial needs: ['N13']; diagnostic: GRANULARITY_AWARE_COVERED.

N13 partial components:

Covered: Target frame/content mismatch and missing-resource rejection.

Missing: Complete target support/subject snapshot checks, subject resource-dependency identity and equality with retained target support.

### U23

Common planning tests distinguish changed snapshot from changed retained content under the same snapshot identity and exercise missing-resource rejection with replace and pytest.raises.

Direct needs: ['N13']; partial needs: ['N09']; diagnostic: GRANULARITY_AWARE_COVERED.

N09 partial components:

source_mapping_1 covered: changed snapshots, changed retained content and missing-resource rejection behavior; missing: the existence and construction of those regression tests with replace and pytest.raises

source_mapping_2 covered: snapshot/content/presence rejection distinctions; missing: their embodiment in common planning tests with replace and pytest.raises

### U26

Existing request numeric tests use pytest parametrization and descriptive ValueError matching for bool, string, float and out-of-domain integers, test None separately, and test valid integers; the new byte tests must accept zero as the task directs.

Direct needs: ['N14']; partial needs: ['N05']; diagnostic: GRANULARITY_AWARE_COVERED.

N05 partial components:

source_mapping_1 covered: numeric admissibility, None, invalid types, descriptive errors and the task-directed zero boundary; missing: the existing tests use parametrization, separate None/valid cases and ValueError matching

source_mapping_2 covered: None, invalid bool/string/float/integer and valid-integer admission conventions, including zero for bytes; missing: the existing tests' parametrization, descriptive ValueError matching and separate None test structure

### U27

Canonical common rendering joins the disclosure header, purpose, plan/snapshot identities, item count, ordered item headings and option identities with each unchanged item.text, using only its explicit LF separators and no newline normalization.

Direct needs: ['N03']; partial needs: ['N04', 'N10', 'N12']; diagnostic: GRANULARITY_AWARE_COVERED.

N04 partial components:

source_mapping_1 covered: unchanged item text, explicit LF insertion and absence of newline normalization; missing: the complete ordered inventory of headers, purpose, identities, item count and headings

source_mapping_2 covered: unchanged text with explicit LF separators and no normalization; missing: the full header, purpose, plan/snapshot identity, item-count and ordered option-heading layout

N10 partial components:

source_mapping_1 covered: ordered items and unchanged item.text; missing: the complete header/identity/heading inventory and exact LF separator/no-normalization rendering contract

source_mapping_2 covered: unchanged item text and item order in rendering; missing: the complete metadata headings/identities and explicit LF-only separator construction

N12 partial components:

Covered: Exact item-text and explicit LF/no-normalization behavior established by text tests.

Missing: Complete disclosure header, purpose, plan/snapshot identities, count, ordered item headings and option-identity layout.

### U29

Project configuration selects Python 3.12, Ruff ALL with documented exceptions and 88-column formatting, and strict mypy over source, test and experiment trees with explicit package bases and src import base.

Direct needs: ['N18']; partial needs: []; diagnostic: GRANULARITY_AWARE_COVERED.

### U31

Immutable ModelUsage optional integer admission accepts None, rejects bool and non-int with descriptive TypeError, and rejects negative counts with descriptive ValueError.

Direct needs: ['N05']; partial needs: ['N14']; diagnostic: GRANULARITY_AWARE_COVERED.

N14 partial components:

Covered: Optional integer, invalid boolean/type and negative-count admission behavior relevant to tests.

Missing: Complete immutable ModelUsage contract, including descriptive TypeError for bool/non-int and descriptive ValueError for negative counts.

## PARTIAL_ONLY units

### U03

The protected command is the documented protected development entry point; it excludes the experiment test tree before collection, retains project pytest configuration and branch coverage with the 100 percent gate, returns pytest's exit code, and does not authorize excluded confirmation validation.

Direct needs: []; partial needs: ['N18', 'N17']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N18 partial components:

source_mapping_1 covered: preserved project pytest configuration and branch coverage threshold; missing: the protected command identity, before-collection experiment exclusion, exit-code propagation and authorization boundary

source_mapping_2 covered: retained pytest configuration and branch coverage with the 100 percent gate; missing: the documented entry-point identity, pre-collection exclusion, exit-code propagation and authorization boundary

N17 partial components:

source_mapping_1 covered: identification of the documented protected development entry point; missing: its complete before-collection exclusion, preserved pytest/coverage configuration and threshold, exit-code propagation and authorization boundary

source_mapping_2 covered: the documented protected entry point and its development-only scope; missing: pre-collection exclusion mechanics, retained pytest/coverage settings and propagation of the pytest exit code

### U04

The planning overview describes exact materialization, native provenance, appended copied-request Context and both supported choices, and distinguishes future token budgets/universal costs from current behavior.

Direct needs: []; partial needs: ['N16']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N16 partial components:

source_mapping_1 covered: documented rendered Context and copied-request assembly contracts; missing: the complete exact materialization/native provenance/both-choice description and future-token-budget/universal-cost distinction

source_mapping_2 covered: documentation of exact materialization, native provenance, supported disclosure choices and appended copied-request Context; missing: the overview's explicit distinction of future token budgets/universal costs from current behavior

### U07

The qualified-reference plan adapter delegates to its validated materializer and renderer and retains both source/target addresses and content identities, the rendered text and native materialized value in the common item.

Direct needs: []; partial needs: ['N09', 'N10']; diagnostic: GRANULARITY_AWARE_COVERED.

N09 partial components:

source_mapping_1 covered: retained source/target addresses and content identities supporting frame binding; missing: delegation to validated materialization/rendering and retention of rendered text and native value

source_mapping_2 covered: delegation to validated materialization and retention of source/target addresses and content identities; missing: the renderer-to-item text handoff and retention of the native materialized value

N10 partial components:

source_mapping_1 covered: retained rendered text, native materialized value and provenance-bearing addresses/content identities; missing: qualified adapter delegation to both its validated materializer and renderer

source_mapping_2 covered: renderer-to-item exact text and native materialized-value retention; missing: delegation through frame-validated materialization and both source/target address/content identity bindings

### U10

Common materialization rejects a mismatched repository or snapshot, realizes each selected option in order, verifies its returned identity/representation, and publishes a ContextDisclosure only after all items succeed.

Direct needs: []; partial needs: ['N09', 'N10', 'N13']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N09 partial components:

source_mapping_1 covered: repository/snapshot mismatch rejection; missing: ordered realization, returned identity/representation checks and publication only after every item succeeds

source_mapping_2 covered: repository/snapshot rejection, returned identity/representation verification and withholding a disclosure until all items validate; missing: ordered realization of the selected choices

N10 partial components:

source_mapping_1 covered: ordered realization and returned item identity/representation checking; missing: repository/snapshot mismatch rejection and publication only after all realizations succeed

source_mapping_2 covered: realization of each selected option in order; missing: repository/snapshot rejection, returned identity/representation verification and all-success publication

N13 partial components:

Covered: Common repository/snapshot mismatch rejection.

Missing: Selected-option realization order, returned identity/representation verification and publication only after every item succeeds.

### U12

The protected command runs tests only; the validation guide separately specifies uv Ruff lint/format, mypy and diff whitespace checks, including staged diff checking where applicable.

Direct needs: []; partial needs: ['N18', 'N17']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N18 partial components:

source_mapping_1 covered: test versus Ruff/mypy validation responsibilities; missing: the separately prescribed guide commands and diff whitespace/staged diff checks

source_mapping_2 covered: the separate lint/format/type and working/staged whitespace-check validation requirements; missing: the protected command's tests-only scope

N17 partial components:

source_mapping_1 covered: the protected test entry point; missing: the separate guide commands for lint, format, typing and unstaged/staged whitespace checks

source_mapping_2 covered: the protected entry point running tests only; missing: separate uv Ruff lint/format, mypy and working/staged diff checks prescribed by the guide

### U14

Immutable DisclosurePlan carries purpose, repository/snapshot identities and ordered choices, rejecting blank purpose, empty choices, mixed purposes or frames and duplicate choices.

Direct needs: []; partial needs: ['N09', 'N10', 'N13']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N09 partial components:

source_mapping_1 covered: repository/snapshot identities and mixed-frame rejection; missing: immutability, purpose and ordered-choice contracts, blank/empty/mixed-purpose/duplicate rejection

source_mapping_2 covered: plan repository/snapshot identities and rejection of mixed frames; missing: blank/heterogeneous purposes, empty or duplicate choices, ordered-choice retention and immutable plan shape

N10 partial components:

source_mapping_1 covered: immutable ordered choices; missing: purpose/frame identities and blank-purpose, empty-choice, mixed-purpose/frame and duplicate-choice rejection

source_mapping_2 covered: retention of the ordered choices; missing: plan immutability, repository/snapshot identities and blank-purpose, empty-choice, mixed-purpose/frame and duplicate-choice admission

N13 partial components:

Covered: Mixed repository/snapshot frame rejection.

Missing: Immutable purpose/frame/ordered-choice schema, blank-purpose and empty-choice rejection, mixed-purpose rejection and duplicate-choice rejection.

### U15

Common rendering and assembly import ModelRequest and Prompt, use common ContextDisclosure only as a type dependency, and introduce no language-specific adapter or Retrieval dependency.

Direct needs: []; partial needs: ['N02']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N02 partial components:

Covered: Absence of language-specific adapter and Retrieval dependencies.

Missing: Actual ModelRequest and Prompt imports and the type-only ContextDisclosure dependency.

### U16

The existing keyword-only common assembly entry point accepts RenderedContextDisclosure, has no limit argument, assembles the entire context.text, and creates the copied request only in its final replace call.

Direct needs: []; partial needs: ['N03', 'N06', 'N01', 'N07', 'N14']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N03 partial components:

source_mapping_1 covered: assembly of the entire context.text; missing: the keyword-only signature, rendered input type, absence of a limit argument and final replace staging

source_mapping_2 covered: assembly of the entire context.text payload; missing: keyword-only rendered input, absent limit argument and final copied-request construction timing

N06 partial components:

Covered: Entire context.text assembly with copying deferred to the final replacement.

Missing: Keyword-only signature, RenderedContextDisclosure input type and absence of an existing limit argument.

N01 partial components:

Covered: The common entry point owning copied request assembly.

Missing: Keyword-only RenderedContextDisclosure input, no existing limit argument, entire context.text handling and final replace-call construction timing.

N07 partial components:

source_mapping_1 covered: creation of the copied request by replacement; missing: the complete entry-point signature, rendered input, no-limit signature and entire-text assembly contract

source_mapping_2 covered: creation of the copied request at the final replace call; missing: keyword-only RenderedContextDisclosure input, no existing limit argument and full-context assembly

N14 partial components:

Covered: Tested copied-request preservation and assembly argument admission.

Missing: Keyword-only rendered input, absent limit, entire context.text handling and copying specifically at the final replace call.

### U17

Common assembly embeds unchanged task_text and context.text in separate outer envelopes, reports len(context.text.encode("utf-8")) independently of the task length, and preserves each embedded string and its newline bytes.

Direct needs: []; partial needs: ['N04', 'N03', 'N07', 'N08', 'N12']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N04 partial components:

source_mapping_1 covered: UTF-8 encoding and preservation of embedded newline bytes; missing: the full separate task/Context envelope contract and independently reported Context length excluding task length

source_mapping_2 covered: context-only UTF-8 length accounting and unchanged embedded strings/newline bytes; missing: the separate outer task and Context envelope structure

N03 partial components:

source_mapping_1 covered: the separate appended Context text, its envelope and preserved embedded text/separators; missing: the independently reported UTF-8 byte length and exclusion of task length from that measurement

source_mapping_2 covered: separate task/Context envelope boundaries and unchanged appended payload text; missing: the context-only UTF-8 length report and preservation of each embedded string's newline bytes

N07 partial components:

source_mapping_1 covered: unchanged original task content alongside appended Context; missing: exact envelopes, independent UTF-8 length reporting and embedded newline-byte semantics

source_mapping_2 covered: unchanged original task text in copied assembly; missing: separate envelope structure, the context-only byte report and context/newline preservation

N08 partial components:

source_mapping_1 covered: unchanged task text and separate appended Context; missing: independent Context UTF-8 length reporting and the full envelope/newline contract

source_mapping_2 covered: unchanged original task in its separate envelope alongside the Context envelope; missing: context-only UTF-8 length reporting and exact preservation of context.text and its newlines

N12 partial components:

Covered: Preservation of exact embedded strings and newline bytes, including non-ASCII text.

Missing: Separate outer task/Context envelopes and len(context.text.encode('utf-8')) reported independently of task length.

### U20

The outer Context public facade explicitly imports the common planning assembler and companion plan/materialization/rendering symbols and lists them in __all__.

Direct needs: []; partial needs: ['N11']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N11 partial components:

Covered: Public exposure of the common planning assembler.

Missing: Distinct outer Context facade's explicit plan/materialization/rendering companion imports and __all__ entries.

### U24

Qualified target resolution support and any retained declaration analysis must match target resource and repository/snapshot frame, with target declaration membership checked when analysis is retained.

Direct needs: []; partial needs: ['N09', 'N13']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N09 partial components:

Covered: Matching target resource and repository/snapshot identities for resolution support and retained analysis.

Missing: Target declaration membership when declaration analysis is retained.

N13 partial components:

Covered: Target resource and repository/snapshot consistency of retained target support or analysis.

Missing: Target declaration membership when declaration analysis is retained.

### U25

Common Context Planning owns ordered caller-directed plans and faithful realization before rendering and copied request assembly, independently of Retrieval or automatic selection.

Direct needs: []; partial needs: ['N15', 'N10', 'N01', 'N02']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N15 partial components:

source_mapping_1 covered: separation from automatic selection; missing: ownership of ordered caller-directed plans and faithful realization through rendering and copied assembly independently of Retrieval

source_mapping_2 covered: the architectural distinction between common Context capacity and automatic selection; missing: the complete ordered plan/realization/rendering/copied-assembly responsibility

N10 partial components:

source_mapping_1 covered: ordered faithful realization; missing: the complete common ownership/lifecycle boundary and independence from Retrieval and automatic selection

source_mapping_2 covered: ordered plans and faithful realization of selected items; missing: common pipeline ownership and separation from Retrieval/automatic selection

N01 partial components:

Covered: Common Context Planning ownership of copied ModelRequest assembly.

Missing: Ordered caller-directed plan ownership, faithful realization before rendering and independence of the whole pipeline from Retrieval and automatic selection.

N02 partial components:

source_mapping_1 covered: common planning independence from Retrieval; missing: ownership of ordered caller-directed plans and faithful realization through rendering and assembly

source_mapping_2 covered: independence from Retrieval and adapter-side ownership; missing: the common owner's ordered caller-directed planning and faithful realization/rendering/assembly pipeline

### U28

Whole-resource realization rejects foreign/stale snapshot frames, missing resources and unequal retained occurrences; its item includes unchanged retained content, resource/content identities and the original occurrence as native provenance.

Direct needs: []; partial needs: ['N09', 'N10', 'N13']; diagnostic: GRANULARITY_AWARE_COVERED.

N09 partial components:

source_mapping_1 covered: foreign/stale frames, missing resources and retained-occurrence equality; missing: unchanged item text, resource/content identity retention and original occurrence as native provenance

source_mapping_2 covered: foreign/stale frame, missing-resource and retained-occurrence rejection plus resource/content identity bindings; missing: unchanged item content and original-occurrence native provenance retention

N10 partial components:

source_mapping_1 covered: unchanged retained text, resource/content identities and original-occurrence native provenance; missing: foreign/stale/missing/unequal-occurrence rejection rules

source_mapping_2 covered: unchanged retained text and original-occurrence native provenance; missing: foreign/stale frame, missing-resource and unequal-occurrence rejection and resource/content identity bindings

N13 partial components:

Covered: Foreign/stale frame, missing-resource and unequal-occurrence rejection demonstrated by tests.

Missing: Unchanged retained content, resource/content identities and original-occurrence native provenance in the realized item.

### U30

Immutable MaterializedDisclosureItem retains option identity, representation, addresses, content identities, exact text and native_provenance; ContextDisclosure requires one item per ordered plan choice with matching identity and representation.

Direct needs: []; partial needs: ['N09', 'N10']; diagnostic: GRANULARITY_AWARE_COVERED.

N09 partial components:

source_mapping_1 covered: retained content identities and correspondence between disclosure and plan choices; missing: the full immutable item field inventory, exact text/native provenance and ordered identity/representation correspondence

source_mapping_2 covered: address/content/option/representation binding and one matching item per ordered plan choice; missing: the immutable item's exact text and native_provenance retention

N10 partial components:

Covered: Immutable exact text and native_provenance retention, with one item per ordered plan choice.

Missing: Full option identity, representation, address and content-identity fields and matching option-identity/representation requirements.

### U32

The common mixed-plan test uses CRLF and non-ASCII qualified/whole-resource fixtures and checks unchanged retained source, native whole-resource provenance and rendered item order.

Direct needs: []; partial needs: ['N10', 'N12']; diagnostic: GRANULARITY_AWARE_PARTIAL.

N10 partial components:

source_mapping_1 covered: unchanged retained source, native whole-resource provenance and item order; missing: the test-specific CRLF and non-ASCII mixed qualified/whole-resource fixtures and their assertions

source_mapping_2 covered: unchanged retained source, native whole-resource provenance and rendered order as preservation contracts; missing: the mixed-plan test's concrete CRLF and non-ASCII qualified/whole-resource fixtures and their test assertions

N12 partial components:

source_mapping_1 covered: CRLF/non-ASCII mixed text fixtures, unchanged retained source and rendered order as exact-text boundary evidence; missing: the native whole-resource provenance assertion

source_mapping_2 covered: CRLF/non-ASCII mixed-plan fixtures, unchanged source text and rendered item ordering; missing: the independent native whole-resource provenance assertion

## UNCOVERED units

### U02

Qualified-reference admission rejects blank purpose, derivation/coverage or analysis-membership mismatch, unsupported target type and unsupported resolution route; its materializer rechecks this admission for directly constructed immutable values.

Direct needs: []; partial needs: []; diagnostic: GRANULARITY_AWARE_UNCOVERED.

### U19

Common planning tests construct a qualified disclosure option through module interpretation and production reference analysis before choosing the retained reference.

Direct needs: []; partial needs: []; diagnostic: GRANULARITY_AWARE_UNCOVERED.

## AMBIGUOUS_ONLY units

## Final need classifications

### N01: PARTIAL_ONLY

Which common Context Planning contract owns copied ModelRequest assembly?

Direct: []; partial: ['U16', 'U25']; unique: []

The common copied-assembly ownership question is intelligible and task-grounded. It establishes assembly ownership in U25 and entry-point identity in U16, but does not require the full ordered planning/realization/selection lifecycle or complete assembly signature. The limited whole-unit match does not show misformulation.

### N02: PARTIAL_ONLY

What dependency constraints separate common Context Planning from language-specific adapters and Retrieval?

Direct: []; partial: ['U15', 'U25']; unique: []

The dependency-separation question is usable and task-required, but establishes only the prohibited adapter/Retrieval boundary in U15 and the independence component of U25. It does not seek positive common import details or complete pipeline ownership. Task importance does not itself confer NECESSARY under the direct-unit definition.

### N03: NECESSARY

What exact rendered Context text, headings and separators are appended during assembly?

Direct: ['U27']; partial: ['U16', 'U17']; unique: ['U27']

['This need directly seeks the complete facts of 1 units, including 1 uniquely directly covered units.', 'The exact rendered layout requires its full metadata and separator inventory; encoding alone does not supply it.']

### N04: PARTIAL_ONLY

What existing UTF-8 and newline handling contracts preserve exact rendered text?

Direct: []; partial: ['U17', 'U27']; unique: []

['This need seeks an identifiable component of 2 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.', 'Encoding/newline fidelity is legitimate and contributes to collective byte coverage, but each applicable unit also includes layout or envelope facts outside this need.']

### N05: NECESSARY

What existing validation and error conventions apply to optional nonnegative integer limits and invalid booleans?

Direct: ['U11', 'U31']; partial: ['U26']; unique: ['U11', 'U31']

['This need directly seeks the complete facts of 2 units, including 2 uniquely directly covered units.', 'This well-formed validation question uniquely seeks complete implementation admission precedents, including the distinction between positive tokens and nonnegative bytes.']

### N06: PARTIAL_ONLY

What assembly contract permits rejection before modifying a request, without truncating or omitting items?

Direct: []; partial: ['U13', 'U16', 'U21']; unique: []

Safe rejection before copying, with faithful whole-context handling, is an actionable question. It does not require U16's keyword-only input/type/absent-limit signature or U13's exhaustive schema. Partial coverage is a scope issue, rather than misformulation.

### N07: NECESSARY

How does copied ModelRequest assembly preserve all fields other than the appended Context?

Direct: ['U13', 'U21']; partial: ['U05', 'U16', 'U17']; unique: ['U13', 'U21']

['This need directly seeks the complete facts of 1 units, including 1 uniquely directly covered units.', 'The all-field copy question uniquely establishes the complete immutable request schema and also explains the copy operation.']

### N08: PARTIAL_ONLY

How are the original task text and Prompt role preserved when Context is appended?

Direct: []; partial: ['U05', 'U17', 'U21']; unique: []

The original-task/Prompt-role question establishes preservation components of envelope assembly and Prompt construction, but leaves independent byte-reporting and non-prompt-copy facts unknown. It does not completely establish U21, so the direct redundancy with N07 claimed in the competing position is not established. The formulation is coherent.

### N09: NECESSARY

What repository, snapshot and content frame checks bind a ContextDisclosure to its DisclosurePlan?

Direct: ['U08', 'U22']; partial: ['U07', 'U10', 'U14', 'U23', 'U24', 'U28', 'U30']; unique: ['U08', 'U22']

['This need directly seeks the complete facts of 2 units, including 2 uniquely directly covered units.', 'This frame question uniquely covers complete source/target binding checks and contributes to several broader units; it does not ask for every unrelated admission predicate.']

### N10: PARTIAL_ONLY

What contracts retain item order, exact item text and native disclosure provenance?

Direct: []; partial: ['U07', 'U10', 'U14', 'U25', 'U27', 'U28', 'U30', 'U32']; unique: []

Ordered item/text/native-provenance retention is a legitimate repository concern. The reviewed item unit U30 additionally requires its complete address/content/option/representation schema and matching checks. Other overlapping units add frame admission, renderer metadata or test-specific facts; collective usefulness does not give a direct-unit classification.

### N11: NECESSARY

What public Context Planning package exports expose copied assembly to callers?

Direct: ['U01']; partial: ['U20']; unique: ['U01']

The planning public-boundary question directly establishes U01's assembler/renderer/rendered-value imports and __all__. No other frozen need seeks that complete export inventory. Partial coverage of the distinct outer facade U20 does not remove this unique direct contribution.

### N12: NECESSARY

Which existing tests and fixtures establish exact text, non-ASCII and newline boundary behavior?

Direct: ['U06']; partial: ['U05', 'U17', 'U27', 'U32']; unique: ['U06']

['This need directly seeks the complete facts of 1 units, including 1 uniquely directly covered units.', 'The text-test/fixture question uniquely establishes retained UTF-8 fixture setup. It only partly establishes broader qualified-construction and provenance-assertion tests.']

### N13: NECESSARY

Which tests establish foreign or stale repository/snapshot/content frame rejection?

Direct: ['U23']; partial: ['U08', 'U10', 'U14', 'U22', 'U24', 'U28']; unique: ['U23']

['This need directly seeks the complete facts of 1 units, including 1 uniquely directly covered units.', 'The rejection-test question uniquely establishes the complete changed-frame versus changed-content and missing-resource test pattern.']

### N14: NECESSARY

Which tests establish copied-request preservation and invalid argument validation?

Direct: ['U05', 'U26']; partial: ['U11', 'U13', 'U16', 'U21', 'U31']; unique: ['U05', 'U26']

['This need directly seeks the complete facts of 2 units, including 2 uniquely directly covered units.', 'This actionable test question uniquely establishes copied-request assertions and numeric test conventions; its two concerns are explicitly stated and do not prevent acquisition.']

### N15: NECESSARY

What governing architecture documentation distinguishes Context capacity from automatic selection?

Direct: ['U09']; partial: ['U25']; unique: ['U09']

The governing-architecture question directly establishes U09's canonical current authority and relevant pipeline scope. The package-documentation question N16 seeks a different boundary, and no other frozen need seeks the complete governing authority fact. The question is actionable.

### N16: PARTIAL_ONLY

What package documentation describes rendered Context and copied assembly contracts?

Direct: []; partial: ['U04']; unique: []

['This need seeks an identifiable component of 4 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.', 'The package-documentation question is actionable but does not seek the additional future-token/universal-cost distinction bundled into its matching overview unit.']

### N17: PARTIAL_ONLY

What established entry point runs protected development validation?

Direct: []; partial: ['U03', 'U12']; unique: []

['This need seeks an identifiable component of 2 units but no complete reviewed unit; no statement defect warrants MISFORMULATED.', 'Protected-entry discovery is actionable and supplies workflow scope. It does not by itself require every command implementation, coverage-setting or separate-tool fact in the reviewed units.']

### N18: NECESSARY

What established tooling configuration constrains test, type and style validation?

Direct: ['U18', 'U29']; partial: ['U03', 'U12']; unique: ['U18', 'U29']

['This need directly seeks the complete facts of 2 units, including 2 uniquely directly covered units.', 'The configuration question uniquely establishes complete test and type/style configuration units and contributes separate-tool facts to collective workflow coverage.']

## Every witness alternative

### bytes / alternative-4b0024cccd671e90845c10dd0144689e9ea89c36dbb7b33a92bc15faa8450ef1

Members: ['U17', 'U27']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U17']; missing diagnostic: ['U17'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U17: Both supplied collective sets fail to establish the existing independent context-only UTF-8 length report, and each also leaves envelope facts unknown. Text/encoding/preservation components alone do not complete this member.

U27: The supplied shared-DIRECT N03/U27 answer establishes the complete canonical metadata/headings/item-text layout and explicit LF/no-normalization separators.

### ceiling / alternative-5823cd216c59ce3b109a4657e44e0050b4fbc485a58d5da984d3e7da3ebed7c5

Members: ['U11', 'U16']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U16']; missing diagnostic: ['U16'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U11: The supplied shared-DIRECT N05/U11 judgment establishes None/type/error admission and the positive-token versus nonnegative-byte domain distinction.

U16: N06 establishes whole-context behavior and a rejection seam before final copying, but leaves keyword-only signature, rendered input type and absence of an existing limit unestablished. No supplied valid collective cures that full entry-point contract.

### ceiling / alternative-f0674fbc795df23f5c153049fd2416ed7b3bff1e89bc3e4dc5376beb66fd13dc

Members: ['U16', 'U31']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U16']; missing diagnostic: ['U16'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U16: N06 establishes whole-context behavior and a rejection seam before final copying, but leaves keyword-only signature, rendered input type and absence of an existing limit unestablished. No supplied valid collective cures that full entry-point contract.

U31: The supplied shared-DIRECT N05/U31 judgment establishes immutable optional nonnegative-integer admission: None accepted, bool/non-int rejected with descriptive TypeError and negative counts with descriptive ValueError.

### ceiling / alternative-d1599c2ce73551e58d4eeb482661a9e62312f3766c7a77dd9bb95a8a7c1a3638

Members: ['U16', 'U26']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U16']; missing diagnostic: ['U16'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U16: N06 establishes whole-context behavior and a rejection seam before final copying, but leaves keyword-only signature, rendered input type and absence of an existing limit unestablished. No supplied valid collective cures that full entry-point contract.

U26: The supplied shared-DIRECT N14/U26 answer establishes the parametrized numeric case matrix, descriptive ValueError matching, separate None/valid cases and new accepted-zero distinction.

### documentation / alternative-15d7c3ffc813581557be5c4e0732549f4686d0fe3999af4783abbbbb7c9db6eb

Members: ['U04', 'U09']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U04']; missing diagnostic: ['U04'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U04: The alternative positions identify no complete direct or collective account of the package overview's exact materialization/native provenance/choices/current-versus-future claims. The governing-document need asks a different documentation boundary; this member remains incomplete.

U09: The reconciled N15/U09 direct decision establishes canonical current governing-architecture authority and the relevant planning/materialization/rendering/assembly scope.

### exports / alternative-fa2c4638c8d6ffb4c5cab8f91fcc0e562d8256c72a831797541622b2bf8531c6

Members: ['U01', 'U20']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U20']; missing diagnostic: ['U20'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U01: The planning-package public export inventory is completely established by the reconciled N11/U01 decision: assembler, renderer and rendered value are explicitly imported and listed in __all__.

U20: N11 overlaps assembler exposure but leaves the distinct outer Context facade's complete companion imports and __all__ inventory unknown. The full member lacks direct establishment.

### frame / alternative-24ffd4cd7ed50739eb1087c430d73dca722b05e41e52023b2f539e37a4d50063

Members: ['U02', 'U07', 'U08', 'U10', 'U14', 'U22', 'U24', 'U28', 'U30']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U02', 'U07', 'U10', 'U14', 'U24', 'U28', 'U30']; missing diagnostic: ['U02', 'U10', 'U14', 'U24'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U02: Qualified-reference semantic admission and defensive re-admission remain unestablished by the supplied binding proposition, which asks a different frame question. The alternative's complete admission member remains a gap.

U07: The accepted supplied N09+N10 collective set establishes validated source/target identity handoff and renderer/text/native-value handoff. This collective diagnostic does not supply a strict direct mapping.

U08: The supplied shared-DIRECT N09/U08 complete-unit counterfactual establishes all qualified source dependency/occurrence frame, address, presence and retained-content equality checks.

U10: Frame and ordering components are established by the supplied N09+N10 set, but all-success publication remains unknown. That proposed collective is insufficient, and this member is not fully established.

U14: The alternative positions supply no complete account of the immutable plan's purpose/nonempty/homogeneous/duplicate admission rules in addition to frame/order fields. Related frame tests do not cure this member's complete-unit gap.

U22: The supplied shared-DIRECT N09/U22 judgment establishes all target support/subject snapshot, resource-presence, dependency-identity and retained-support equality predicates.

U24: N09 and N13 supply frame-consistency components but leave conditional retained-analysis declaration membership unknown; the whole target-evidence member is incomplete.

U28: The accepted supplied N09+N10 collective set establishes whole-resource rejection/identity integrity and unchanged-text/original-occurrence provenance. It remains collective rather than strict direct coverage.

U30: The accepted supplied N09+N10 collective establishes the full immutable item schema and ordered matching. The reconciled individual N10 judgment remains partial.

### ownership / alternative-f8cc13a78a696e2cf395ea58f422d4eb26c24a17ba9eacbb7f3645755872877c

Members: ['U15', 'U25']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U15', 'U25']; missing diagnostic: ['U15', 'U25'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U15: N02 establishes the forbidden adapter/Retrieval dependencies, but actual ModelRequest/Prompt imports and type-only ContextDisclosure remain unknown. The complete member lacks direct establishment.

U25: N01 establishes common copied-assembly ownership but leaves ordered caller-directed plan ownership, faithful realization before rendering and the whole pipeline's Retrieval/automatic-selection boundary unestablished. The complete lifecycle responsibility member therefore lacks direct coverage.

### ownership / alternative-cf445deec2b6d543ca84fbd68a8dc1c97d0e7ce2f0ae19fc3b3e04f45231545f

Members: ['U15', 'U25']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U15', 'U25']; missing diagnostic: ['U15', 'U25'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U15: N02 establishes the forbidden adapter/Retrieval dependencies, but actual ModelRequest/Prompt imports and type-only ContextDisclosure remain unknown. The complete member lacks direct establishment.

U25: N01 establishes common copied-assembly ownership but leaves ordered caller-directed plan ownership, faithful realization before rendering and the whole pipeline's Retrieval/automatic-selection boundary unestablished. The complete lifecycle responsibility member therefore lacks direct coverage.

### request / alternative-8f5ca8e7e495bcd75c167aa465aa4dc9fba05a9e8d8b2e1694018b5cc0cb3ab1

Members: ['U13', 'U17', 'U21']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U17']; missing diagnostic: ['U17'].

All complementary members must be established inside this exact frozen alternative. The member rationales identify at least one complete-unit gap. Valid collective components remain diagnostic and cannot cure the other missing facts or satisfy strict direct coverage. Other alternatives are evaluated separately under ANY-complete-alternative logic; their members are not pooled.

U13: The reconciled N07/U13 complete answer establishes the immutable request declaration and full prompt/settings/conversation/provider_settings/tools shape.

U17: Both supplied collective sets fail to establish the existing independent context-only UTF-8 length report, and each also leaves envelope facts unknown. Text/encoding/preservation components alone do not complete this member.

U21: The supplied shared-DIRECT N07/U21 judgment establishes the actual dataclasses.replace operation changing only Prompt and constructing it with the original role; this directly establishes the complete copying operation. N08's narrower role question remains partial.

### tests / alternative-99eba0f9ffe3fe2a9dd8a51d83031cc7b4d65a80fe699213ba2f5171335513ed

Members: ['U05', 'U06', 'U19', 'U23', 'U26', 'U32']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U19', 'U32']; missing diagnostic: ['U19', 'U32'].

### validation / alternative-112ca6b6a76691a25e2cf528a62311634ca38c88086c4464abdc1d3588733158

Members: ['U03', 'U12', 'U18', 'U29']; strict: INCOMPLETE; diagnostic: INCOMPLETE.

Missing direct: ['U03', 'U12']; missing diagnostic: ['U03', 'U12'].

## All granularity decisions

U01: **ATOMIC_FOR_NEED_MAPPING**. Explicit imports and __all__ for related rendering/assembly symbols form one public planning-package export inventory.

U02: **ATOMIC_FOR_NEED_MAPPING**. One properly authored qualified-reference admission-contract need can ask all purpose, derivation/coverage, analysis-membership, target-type and resolution-support predicates, including where directly constructed immutable values are rechecked. Initial admission and defensive enforcement describe the same value-validity contract; distinct searchable predicates alone do not invalidate it.

U03: **ATOMIC_FOR_NEED_MAPPING**. One properly authored protected-command contract need can reasonably seek its documented authority, collection exclusion, retained configuration/coverage, exit-code propagation and authorized scope. These clauses define one command's complete operational boundary. The current narrower entry-point need's limitations do not make the target invalid.

U04: **ATOMIC_FOR_NEED_MAPPING**. The planning overview's current supported pipeline and future budget/cost distinction form one document's capability account, reasonably sought by one overview-content need.

U05: **ATOMIC_FOR_NEED_MAPPING**. The original task, role, shared values, placement and inverse-replacement equality are coordinated assertions in one copied-request preservation regression.

U06: **ATOMIC_FOR_NEED_MAPPING**. Writing exact UTF-8 bytes and observing addressed resources describe one retained-snapshot fixture construction mechanism.

U07: **COLLECTIVELY_COVERABLE**. The adapter bridge has an integrity boundary, validated materialization with source/target address/content identities, and a representation boundary, renderer text and native materialized-value retention. Distinct frame-binding and item-retention needs can jointly establish the bridge without changing the unit.

U08: **ATOMIC_FOR_NEED_MAPPING**. Dependency and occurrence frame/address/presence/content-equality predicates coordinate one source-side qualified-materialization binding.

U09: **ATOMIC_FOR_NEED_MAPPING**. Canonical governing authority and its current relevant pipeline scope are one documentation-authority fact.

U10: **COLLECTIVELY_COVERABLE**. Repository/snapshot and returned-identity integrity, selected-choice realization order and all-success publication are distinct validation, ordering and lifecycle boundaries. Multiple legitimate needs may jointly establish them; the supplied frame/order pair still needs an explicit publication fact.

U11: **ATOMIC_FOR_NEED_MAPPING**. Optional integer admission, exception convention and token-versus-byte domain applicability are one validator-precedent contract.

U12: **COLLECTIVELY_COVERABLE**. The command's tests-only scope is distinct from the guide's prescribed lint/format/type/working-and-staged-whitespace workflow. Multiple legitimate validation needs can establish both, but static tool configuration alone need not establish prescribed workflow steps.

U13: **ATOMIC_FOR_NEED_MAPPING**. Frozen status and the complete field inventory form a single immutable request schema.

U14: **ATOMIC_FOR_NEED_MAPPING**. One properly authored DisclosurePlan schema-and-admission need can reasonably seek purpose/frame/ordered-choice fields plus blank, empty, mixed-purpose/frame and duplicate rejection. These rules jointly define one immutable value's admissibility. Missing direct coverage from existing needs is not evidence of an invalid pairwise unit.

U15: **ATOMIC_FOR_NEED_MAPPING**. Actual common imports, type-only dependency and forbidden adapter/Retrieval dependencies form one rendering/assembly dependency contract.

U16: **ATOMIC_FOR_NEED_MAPPING**. Signature, rendered input, no existing limit, full-context behavior and final copying boundary define one assembly entry-point contract.

U17: **COLLECTIVELY_COVERABLE**. Outer task/Context placement, exact embedded-string/newline preservation and independent context-only UTF-8 length reporting have separate envelope, text-fidelity and accounting boundaries. Distinct complete needs can establish them; generic encoding fidelity does not guarantee the existing length report.

U18: **ATOMIC_FOR_NEED_MAPPING**. Strict pytest configuration/markers and branch-coverage enforcement form one test-configuration contract.

U19: **ATOMIC_FOR_NEED_MAPPING**. Interpretation, production analysis and retained-reference selection form one qualified fixture-construction sequence.

U20: **ATOMIC_FOR_NEED_MAPPING**. The outer facade's related explicit imports and __all__ form one public export inventory, even though the current need targets the planning-package boundary.

U21: **ATOMIC_FOR_NEED_MAPPING**. The single dataclasses.replace and role-preserving Prompt construction operation establishes the whole copying fact.

U22: **ATOMIC_FOR_NEED_MAPPING**. Support/subject snapshots, resource presence, dependency identity and retained-support equality coordinate one target-side materialization binding.

U23: **ATOMIC_FOR_NEED_MAPPING**. Changed snapshot, changed content under the same snapshot and missing-resource cases with replace/raises form one frame-rejection test pattern.

U24: **ATOMIC_FOR_NEED_MAPPING**. Target support and optional declaration analysis, including conditional declaration membership, form one target-evidence validity contract. Frame consistency and membership are different components within that coherent contract.

U25: **ATOMIC_FOR_NEED_MAPPING**. Ordered caller-directed planning through realization/rendering/copying and exclusion of automatic selection/Retrieval form one common-planning responsibility statement.

U26: **ATOMIC_FOR_NEED_MAPPING**. The numeric case matrix, descriptive matching, None/valid cases and new zero-domain applicability form one validation-test convention.

U27: **ATOMIC_FOR_NEED_MAPPING**. Metadata, ordered headings, unchanged item text and explicit LF separators define one exact rendered payload format.

U28: **COLLECTIVELY_COVERABLE**. Whole-resource frame/content admission is distinct from realized-item text, resource/content identity and native-occurrence retention. Separate binding and item-retention needs can jointly establish these integrity and representation boundaries.

U29: **ATOMIC_FOR_NEED_MAPPING**. Interpreter selection, coordinated Ruff settings and strict mypy scope/import/package configuration form one established type/style tooling configuration.

U30: **COLLECTIVELY_COVERABLE**. Immutable exact-text/native-provenance retention and ordered plan-to-item cardinality/identity/representation binding are distinct representation and identity boundaries. The frame and item needs jointly cover them; neither alone requires the full unit.

U31: **ATOMIC_FOR_NEED_MAPPING**. None admission, bool/non-int TypeError and negative ValueError define one optional nonnegative-integer admission contract.

U32: **ATOMIC_FOR_NEED_MAPPING**. CRLF/non-ASCII mixed-plan fixtures and associated retained-text/provenance/order assertions are one coherent regression scenario. A text-boundary need omitting provenance does not make that scenario overcompound.

## Every supplied collective set

Exact supplied semantic decisions; membership, partial contributions, removal evidence and supplied-set antichain checked mechanically. No new sets or independent semantic sufficiency proof.

### U07 ← ['N09', 'N10']: VALID_MINIMAL_COLLECTIVE_SET

The complete frame-binding answer supplies validated source/target address and content-identity handoff, and the complete item-retention answer supplies the renderer-to-item text and native materialized-value handoff. Together these establish the entire qualified adapter bridge.

Both members are necessary within this supplied set: the frame-binding singleton leaves text/native-value retention unknown, while the item-retention singleton leaves the complete validated source/target binding unknown. Thus neither member can be removed; no claim is made about unproposed sets.

N09: Delegation through validated qualified materialization and retention of source/target addresses and content identities. Removal: Removing N09 leaves validated materialization and complete source/target identity handoff unestablished; N10's text/native-value contract does not require those bindings.

N10: Renderer-to-item rendered text and native materialized-value retention. Removal: Removing N10 leaves renderer text handoff and native materialized-value retention unestablished; N09's frame-binding answer does not require them.

### U17 ← ['N03', 'N04']: INSUFFICIENT

N03 establishes the exact appended rendered payload and its headings/separators; N04 establishes UTF-8/newline fidelity. Their complete answers do not require the existing independent len(context.text.encode('utf-8')) report or the complete original-task outer envelope. Knowing what should be counted is not knowing what the assembler reports.

The set is not sufficient, so no valid minimality claim follows. Removing N03 loses exact appended-payload boundaries; removing N04 loses encoding/newline-fidelity rules. Even retaining both leaves independent reporting and complete task-envelope facts unknown.

N04: UTF-8 and newline handling that preserve exact rendered strings. Removal: Removing N04 loses encoding/newline-fidelity rules; N03 can give a textual layout without those handling rules. Neither member requires the existing context-only length report.

N03: Exact appended Context text and its heading/separator boundaries. Removal: Removing N03 loses exact appended payload/boundary knowledge; N04's encoding fidelity need does not supply the complete layout.

### U17 ← ['N04', 'N08']: INSUFFICIENT

N08 supplies original-task/Prompt-role preservation and N04 supplies rendered-text UTF-8/newline fidelity. The pair still does not require the independent context-only byte-length report; task/role preservation also need not inventory the full separate Context envelope.

Both members contribute distinct facts, but sufficiency fails before minimality can be certified. Removing N04 loses encoding/newline handling; removing N08 loses original-task/role preservation. Retaining both leaves the existing length-reporting expression and complete envelope structure unestablished.

N04: Rendered-text UTF-8 and exact newline preservation contracts. Removal: Removing N04 leaves Context encoding/newline handling unknown; original-task/role preservation does not establish it.

N08: Unchanged original-task embedding and original Prompt-role preservation. Removal: Removing N08 leaves original-task/role preservation unknown. N04's rendered-text handling does not establish those prompt facts or the complete task envelope.

### U12 ← ['N17', 'N18']: INSUFFICIENT

N17 identifies the established protected validation entry point and its tests scope. N18 establishes tooling configuration. These answers need not establish the guide's separately prescribed uv lint/format/type and working/staged diff-whitespace workflow. Configuration facts do not necessarily establish required command sequences.

The complete prescribed workflow, particularly separate working/staged whitespace checks, remains missing with both members. Removing N17 loses the protected entry-point scope; removing N18 loses configuration constraints. Distinct usefulness cannot establish a valid minimal collective set when the workflow clause remains unknown.

N18: Established test/type/style tooling constraints. Removal: Removing N18 loses configuration constraints. Its presence still does not require the guide's separate commands or applicable staged diff checking.

N17: The established protected development entry point and its tests scope. Removal: Removing N17 loses which protected entry point runs tests; tooling configuration alone does not identify it.

### U28 ← ['N09', 'N10']: VALID_MINIMAL_COLLECTIVE_SET

The frame-binding answer establishes foreign/stale frame, missing-resource and unequal retained-occurrence rejection plus resource/content bindings. The item-retention answer establishes unchanged content and original-occurrence native provenance. The combined answers establish every admission and representation clause of whole-resource realization.

Removing the frame need leaves rejection and complete resource/content binding unknown. Removing the item need leaves unchanged text and original-occurrence provenance unknown. Both distinct necessary components are present, and either singleton leaves the unit incomplete.

N09: Foreign/stale snapshot-frame, missing-resource and unequal-occurrence rejection, with resource/content identity bindings. Removal: Removing N09 leaves the whole-resource rejection and identity-binding contract unknown; unchanged text/native provenance alone does not establish admission checks.

N10: Unchanged retained item content and original-occurrence native provenance. Removal: Removing N10 leaves exact content retention and native original-occurrence provenance unknown; frame/content checks alone do not establish the item's representation.

### U10 ← ['N09', 'N10']: INSUFFICIENT

N09 establishes repository/snapshot binding and returned identity/representation consistency; N10 establishes selected-choice order. Neither complete answer must establish that publication occurs only after every item succeeds. A binding/order answer can leave that publication-timing contract unknown.

Removing N09 loses integrity predicates and removing N10 loses ordered realization, but keeping both leaves all-success publication unestablished. The set therefore cannot be sufficient or certified minimal.

N09: Repository/snapshot binding and returned option-identity/representation consistency. Removal: Removing N09 leaves mismatch rejection and returned-item integrity unknown. Binding checks alone do not require all-success publication timing.

N10: Realization of each selected choice in order. Removal: Removing N10 leaves ordered realization unknown; N09's frame checks do not require ordering. Ordered retention does not establish when publication occurs.

### U30 ← ['N09', 'N10']: VALID_MINIMAL_COLLECTIVE_SET

N09 establishes complete retained address/content/option/representation identities and one matching item per plan choice. N10 establishes immutable exact text, native provenance and ordered retention. Together these answers establish the full retained item schema and ordered correspondence.

Removing N09 leaves the full identity schema and matching requirements unknown. Removing N10 leaves immutable exact text and native-provenance retention unknown. Overlap in ordered correspondence does not remove either distinct necessary component.

N09: Address/content/option/representation identity bindings and one matching item per plan choice. Removal: Removing N09 leaves complete address/content/option/representation identity retention and matching requirements unknown; N10 need not inventory them.

N10: Immutable exact-text/native-provenance retention and ordered plan-choice correspondence. Removal: Removing N10 leaves exact text and native-provenance retention unknown; N09's identity-binding checks do not require these representation facts.

## Failure-cause synthesis

### INFORMATION_NEED_COVERAGE_FAILURE: ESTABLISHED

The final semantic mapping fails the frozen every-required-unit direct rule. This establishes a coverage failure before retrieval, without selecting treatment effectiveness.

Metrics: `{"missing_direct": 17, "required_units": 32, "strict_complete_alternatives": 0, "strict_covered": 15}`

### UNDER_SPECIFIED_INFORMATION_NEEDS: POSSIBLE

Usable narrow questions leave complete-unit components unrequested. No need is adjudicated misformulated or ambiguous; a formulation defect is not established by partial coverage alone.

Metrics: `{"ambiguous": 0, "misformulated": 0, "partial_only_needs": 8}`

### UNDER_DECOMPOSED_NEED_SET: SUPPORTED

Reconciled atomic targets remain incomplete after the supplied complete collective sets. Missing focused acquisition questions are supported; no repaired need set or causal treatment attribution is tested.

Metrics: `{"atomic_not_directly_covered": 11, "atomic_remaining_units": ["unit-08b960311265498f39d05f67308e78088d73f0324966eb42952517809e530aa2", "unit-1466ea6b2b7b8cdc077c41ad15c6baf8087b6e7a230723f83b9911815a09a10c", "unit-183296beacda118e38a058b6d2588e582fd74639627706768ea3eb9396cc4580", "unit-5e58e7852d6acb8027c97bf0d6ccc3deede219f1c229e52225d0b31b7ed29af6", "unit-60afd810dde9fbb0e5702b55bb3429a416665eddb2af840cc0eff247b801e7c7", "unit-722d29ab3964ccc9a263e022b8048cf7f868ecc1a00128f96a56b05b56274605", "unit-87f78f68bcbaca8cbda3d9fc4b8f1daee88e66a1ed350ec6441d5861cbb400fc", "unit-8ad51eaf88aadfa2dd3d6fff7c23390b4bec7f204bc74d276ba759e0e6b3aa14", "unit-ab36d70f1deecd237ce4358ffb3258f71b19a55589c1815c3a99545581e8cbdf", "unit-b92a7483c7e27b953e8533887d3a5a4dc664b57dd6859cb12fc7c742ae6eeca2", "unit-fddd6c59fb1d485b6e4a6a749f66062c76ddd58df987a692ae75827e2f9b8329"], "diagnostic_missing": 14}`

### NEED_TO_UNIT_GRANULARITY_MISMATCH: SUPPORTED

Three validated N09/N10 collective sets establish full units without a direct pair. Four proposed sets are insufficient. This diagnostic does not replace frozen direct coverage.

Metrics: `{"accepted_minimal_sets": 3, "collectively_coverable_units": 6, "diagnostic_covered": 18, "rejected_sets": 4, "strict_covered": 15}`

### C5_SEMANTIC_ADJUDICATION_INSTABILITY: ESTABLISHED

Historical source disagreement materially affected direct facts and classifications. Exact bounded reconciliation resolves this checkpoint with zero unresolved decisions; it does not erase the observed instability or establish general reliability.

Metrics: `{"need_disagreements": 7, "pair_disagreements": 32, "shared_direct_pairs": 12, "unit_disagreements": 11, "unresolved_decisions": 0}`

## primary to reviewed changes

Source pair counts: {'DIRECTLY_COVERS': 13, 'PARTIALLY_COVERS': 59, 'DOES_NOT_COVER': 504, 'AMBIGUOUS': 0}

pair_changes: 10

- N06 / U13: DOES_NOT_COVER → PARTIALLY_COVERS
- N15 / U04: PARTIALLY_COVERS → DOES_NOT_COVER
- N15 / U09: PARTIALLY_COVERS → DIRECTLY_COVERS
- N16 / U09: PARTIALLY_COVERS → DOES_NOT_COVER
- N16 / U17: PARTIALLY_COVERS → DOES_NOT_COVER
- N16 / U27: PARTIALLY_COVERS → DOES_NOT_COVER
- N11 / U01: PARTIALLY_COVERS → DIRECTLY_COVERS
- N10 / U30: DIRECTLY_COVERS → PARTIALLY_COVERS
- N01 / U16: DOES_NOT_COVER → PARTIALLY_COVERS
- N07 / U13: PARTIALLY_COVERS → DIRECTLY_COVERS

unit_changes: 4

- U01: PARTIAL_ONLY → COVERED
- U09: PARTIAL_ONLY → COVERED
- U13: PARTIAL_ONLY → COVERED
- U30: COVERED → PARTIAL_ONLY

need_changes: 3

- N10: NECESSARY → PARTIAL_ONLY
- N11: PARTIAL_ONLY → NECESSARY
- N15: PARTIAL_ONLY → NECESSARY

## independent to reviewed changes

Source pair counts: {'DIRECTLY_COVERS': 21, 'PARTIALLY_COVERS': 41, 'DOES_NOT_COVER': 514, 'AMBIGUOUS': 0}

pair_changes: 22

- N06 / U16: DIRECTLY_COVERS → PARTIALLY_COVERS
- N11 / U20: DIRECTLY_COVERS → PARTIALLY_COVERS
- N09 / U02: PARTIALLY_COVERS → DOES_NOT_COVER
- N09 / U24: DIRECTLY_COVERS → PARTIALLY_COVERS
- N01 / U25: DIRECTLY_COVERS → PARTIALLY_COVERS
- N02 / U15: DIRECTLY_COVERS → PARTIALLY_COVERS
- N08 / U13: PARTIALLY_COVERS → DOES_NOT_COVER
- N08 / U21: DIRECTLY_COVERS → PARTIALLY_COVERS
- N13 / U08: DOES_NOT_COVER → PARTIALLY_COVERS
- N13 / U10: DOES_NOT_COVER → PARTIALLY_COVERS
- N13 / U14: DOES_NOT_COVER → PARTIALLY_COVERS
- N13 / U22: DOES_NOT_COVER → PARTIALLY_COVERS
- N13 / U24: DOES_NOT_COVER → PARTIALLY_COVERS
- N13 / U28: DOES_NOT_COVER → PARTIALLY_COVERS
- N14 / U13: DOES_NOT_COVER → PARTIALLY_COVERS
- N14 / U16: DOES_NOT_COVER → PARTIALLY_COVERS
- N14 / U21: DOES_NOT_COVER → PARTIALLY_COVERS
- N14 / U31: DOES_NOT_COVER → PARTIALLY_COVERS
- N12 / U17: DOES_NOT_COVER → PARTIALLY_COVERS
- N12 / U19: PARTIALLY_COVERS → DOES_NOT_COVER
- N12 / U27: DOES_NOT_COVER → PARTIALLY_COVERS
- N17 / U18: PARTIALLY_COVERS → DOES_NOT_COVER

unit_changes: 7

- U02: PARTIAL_ONLY → UNCOVERED
- U15: COVERED → PARTIAL_ONLY
- U16: COVERED → PARTIAL_ONLY
- U19: PARTIAL_ONLY → UNCOVERED
- U20: COVERED → PARTIAL_ONLY
- U24: COVERED → PARTIAL_ONLY
- U25: COVERED → PARTIAL_ONLY

need_changes: 4

- N01: NECESSARY → PARTIAL_ONLY
- N02: NECESSARY → PARTIAL_ONLY
- N06: NECESSARY → PARTIAL_ONLY
- N08: USEFUL_REDUNDANT → PARTIAL_ONLY

## Provenance and limits

Packet identity: `c1ecca8aec6bb9cbfb09668a79054262d91e22cfad4adda686bdf97016476b9f`. Exact bindings: `{"frozen_needs_sha256": "8e951bc42ee08db656717ffb494880de26007c087d31f38657b421b8793c54aa", "reliability_comparison_sha256": "75c56552e97e3d86cc3a719fbb0214cbd76b86ca229e8abe5f5bc0b1b2573e2a", "reviewed_gold_sha256": "0d6f54a4ab1eed68b2deb4f4557ef767ff9f2a7771eebde534527c425ae34430"}`.

544 agreed labels are inherited; 32 disputed labels and 12 shared-direct rationales use exact decisions. Individual JSON rows retain source evidence, decision identity and origin. Statistics and diagnostics are deterministic derivations. Reviewed-gold statements and alternative memberships are unchanged. No model identity is included in reviewed mappings.

Primary Stage C.5 = COMPLETE; Independent Stage C.5-R = COMPLETE; C.5 reliability comparison = COMPLETE; Reconciliation v1 = CONTRACT DEFECT / NO DECISIONS; Reconciliation v2 = COMPLETE; Final reviewed C.5 mapping = COMPLETE; Stage D = READY BUT NOT PERFORMED; U1 effectiveness = UNKNOWN.

No treatment or confirmation data was accessed. Retrieval behavior, whole-task/obligation/need retrieval comparisons, strict frozen-rule treatment results, diagnostic treatment results and U1 effectiveness remain untested until Stage D. Semantic coverage failure alone does not select the final treatment outcome.

Next step: Perform Case 0011 Stage D. Intentionally lift treatment blindness and compare whole-task retrieval, obligation-level retrieval and information-need retrieval against the final reviewed task gold and final reviewed C.5 semantic mapping. Report strict frozen-rule results and granularity-aware diagnostics separately.
