# Evaluation

Evaluation provides expected-versus-observed identity coverage accounting
through [`coverage.py`](../coverage.py). The caller supplies identities and
the expected frame; `IdentityCoverage` reports duplicate identities on each
side, missing expected identities, and unexpected observed identities. Exact
coverage requires no duplicates and no missing or unexpected identities.

This capability accounts for identity presence only. A recorded observation
whose payload means `UNJUDGED` is still observed. An identity intentionally
left unsampled is missing if it remains in the expected frame and no
observation for it is supplied. Missingness is relative to that frame; it does
not mean false, irrelevant, not useful, or failed.

Evaluation owns comparison and assessment validity at this boundary. Consumer
domains own identity semantics, outcome semantics, relevance/usefulness,
rationale requirements, sampling policy, metrics, artifact freezing, and
experiment protocols. This neutral primitive can support future assessment
domains without knowing what their outcomes mean. It does not define an
assessment framework or prescribe whether a non-exact report is fatal.
