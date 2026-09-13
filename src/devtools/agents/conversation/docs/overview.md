# `devtools.agents.conversation`

This package owns durable conversational continuity. `Conversation` retains an
identity, creation timestamp, ordered `History` of immutable
`ConversationMessage` values, and source-keyed provider `ConversationRef`
values. It can exist while no Runtime invocation is active.

`ConversationMessage` is durable semantic communication. It records an ID,
local creation timestamp, content, conversational role, and source. It is not
a model `Prompt` or `ModelResponse`; Runtime performs the explicit boundary
materialization between conversation and model invocation.

Conversation does not own Run lifecycle, tool execution, orchestration,
provider configuration, or persistence. Persistence stores and restores its
representation without owning conversation semantics.

```python
from devtools.agents.conversation import (
    Conversation,
    ConversationMessage,
    ConversationMessageRole,
    History,
)
```

`ConversationTurn` is an architectural term but has no reusable implementation
in this package yet.
