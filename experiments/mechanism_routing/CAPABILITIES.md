# U3 mechanism inventory

Inspected at `b42dcb3fd93bd6ddb8af35f1cf8b3273f6486b4b`. This inventory is
contract inspection, not Case 0013 acquisition or target verification.

| Mechanism / owner | Accepted purpose and native input | Native output and qualification | Cost / frame and provenance | First U3 slice |
| --- | --- | --- | --- | --- |
| Canonical lexical resource BM25, context.retrieval.lexical | Conceptual or explicit evidence question; exact frozen query and whole-resource collection | All positive native rows; rank/score/contributions, native tie order; zero positive rows is a bounded miss | Full corpus analysis/index plus queries; native RepositoryId/SnapshotId/CorpusId and document/content identities | Always admitted, entire positive lane, k1=1.2/b=.75/filename=.25 |
| RESOURCE_ADDRESS, repository.snapshot.resource_at | Existing resource content; canonical relative address | One retained resource or bounded absence; no basename/glob expansion | Snapshot lookup and adapter validation; exact content identity | Admitted; new destination skipped only in C |
| PYTHON_MODULE, modules.lookup | Existing module contract; explicit dotted name and frozen explicit-root universe | All matching interpretations, duplicates ambiguous; no runtime importability/namespace inference | Address-only universe preparation shared; lookup and adapter cost; native root/resource/content identity | Admitted |
| PYTHON_DIRECT_FUNCTION / PYTHON_DIRECT_CLASS, modules.selection | Existing source declaration; explicit module/name/kind | Direct source declarations with selection analyses; repeats ambiguous, parser failure unsupported; decorators do not prove runtime binding | Per-request native parsing/selection and full provenance, no cross-arm outcome cache | Admitted as two reporting families; shared direct-declaration implementation |
| PYTHON_DIRECT_METHOD, classes.declarations/containment | Existing direct method; explicit module/class/method | Direct native class-body method after unique parent grounding; duplicate parent/method ambiguous; inherited/dynamic lookup unsupported | Parent selection plus method containment; retain both native accounts, aggregate route timer includes children | Admitted; no standalone broad containment scan |
| Exact declared-name acquisition, function.retrieval | Exact function name over explicit already established declaration knowledge | All matching evidence/supporting resources; bare names do not imply global uniqueness | Requires complete chosen analysis knowledge and its derivation/snapshot | Deferred alternate bare-name route; direct-source acquisition above is sufficient |
| Qualified Reference acquisition, function.qualified_reference / python.references | Native source Reference/Call occurrence and explicit established analyses | Bounded qualified reference/target disclosure, not task-prose symbol resolution | Native occurrence, derivation, dependencies and retained source validation; analysis/materialization cost | Deferred: task prose cannot fabricate native occurrence |
| Module binding lookup, modules.declarations | Explicit module/name over conservative binding analysis | Rebinding/decorators/dynamic syntax can block selection; runtime contract differs from source | Native source plus binding analyses | Deferred: first slice asks for source contracts |
| Import resolution/relations, python.imports | Native Import occurrence and explicit module universe | Directed relation only when uniquely established; module resolution does not prove exports | Native source/target/module/derivation dependencies, analysis cost | Deferred: no native Import occurrence in task text |
| Imported member resolution, imports.members | Native ImportFrom occurrence and one direct facade binding | Bounded one-facade direct function resolution; recursive/wildcard/class generalization unsupported | Source/facade/target support and snapshot; parse/resolution cost | Deferred |
| General bounded containment/declaration relationships | Already established native declarations/occurrences | Explicit partial native structural facts, not relevance or sufficiency | Native derivation, coverage and frame checks; chosen analysis costs | Only direct-method dependency admitted; no universal repository graph |

Evidence: existing U2 CAPABILITIES.md and routing/presentation contracts; native
repository resource/snapshot; module interpretation/lookup/selection/declarations;
class declarations/containment; function retrieval/planned_reference; imports
members/resolution/relations; references overview; grounding contract/resolve;
their existing controlled U2 tests. No production contracts were extended.
Unsupported/ambiguous/unresolved routes promote nothing, retain full fallback,
and remain qualified outcomes rather than automatic router defects.
