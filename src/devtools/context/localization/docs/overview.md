# Repository Localization semantic kernel

The `devtools.context.localization` package owns caller-authored task information
obligations and a deterministic assessment of the supplied obligation frame. It
does not retrieve repository information, infer task obligations, choose Context
representations, or execute agent work.

```text
task interpretation (snapshot independent)
  shared anchors + task/source provenance
                 |
                 v
         information obligations
         mandatory/helpful + conditional applicability
                 |
                 v
       alternative witness sets
       (all members in one set)
                 |
                 v
       snapshot-qualified assessments
                 |
                 v
       frame readiness + diagnostics
```

`LocalizationTaskIdentity`, `LocalizationAnchorIdentity`, and
`LocalizationObligationIdentity` use caller-named stable keys. Anchors retain
task-local text and optional task-source provenance; they do not assert that a
repository entity exists. An obligation states a desired-information predicate,
its shared anchors and provenance, mandatory/helpful status, optional conditional
applicability, a named satisfaction criterion, and one or more alternative
witness sets. Every target in one witness set is conjunctive; any complete set is
an acceptable alternative. Targets remain native or caller-owned hashable
identities rather than being wrapped in a new universal information-unit type.

Assessment evidence references and obligation assessments bind to a repository
and retained snapshot identity. The package stores no repository content. The
task interpretation itself may precede snapshot selection; only assessments
derived from repository evidence are snapshot-bound. Frame assessment rejects
missing, duplicate, unexpected, stale, cross-repository, or internally
inconsistent dispositions. It reuses the generic identity-coverage primitive
from Evaluation for frame accounting; Localization retains obligation meaning.

`READY` means every applicable mandatory obligation in the supplied frame has a
supported resolved or non-applicable disposition. `CONDITIONAL` permits handoff
only when a caller explicitly accepts a named deferred observation; it is not
full readiness. Open, abstained, or unaccepted deferred mandatory obligations
block handoff. Unresolved helpful obligations remain diagnostic and do not block
mandatory readiness. The result makes no claim that the frame lists every real
task obligation or that a coding agent will succeed.

Localization is not Retrieval ranking, Context representation choice, agent
execution, or Evaluation outcome ownership. Retrieval adapters may later attach
native evidence to witness targets. Context Planning may later use obligation
provenance when selecting representations. Neither integration is part of this
package's current contract.
