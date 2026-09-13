# B-0030 — Provider-neutral generative-model interaction

- type: INVESTIGATION
- status: SUPERSEDED
- decision_maturity: READY_FOR_DESIGN
- necessity: FUTURE_REQUIRED
- architectural_significance: STRUCTURAL
- urgency: DEFERRED
- evidence_basis: MULTIPLE
- scope: historical parent for established model interaction core and advanced provider pressure
- primary_domain: models
- supporting_domains: agents, tools, execution, evaluation
- split_children: B-0045, B-0046

## Split record

The minimal model invocation boundary is established by B-0045: Prompt,
ModelInteraction, ModelResponse, ConversationRef, InteractionSource, and
configurable LlamaCppInteraction. ModelServing remains separate.

Advanced interaction/provider pressure is B-0046. Codex is an external Agent,
not a model-provider consumer or a ModelInteraction implementation.
