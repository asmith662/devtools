# Case 0011 construction operator access disclosure

During the reviewed-gold/C.5 construction session, the operator opened
`protocol.py` while verifying frozen InformationNeed identities. This exposed the
existence and wiring of A/B/C treatment arms. The operator therefore cannot attest
`arm identities accessed = NO` for that construction session.

The operator did not select or inspect literal lexical query values and did not
inspect retrieval results, candidate memberships, ranks, scores, score
contributions, acquisition costs, performance metrics, treatment outcomes or
confirmation data. The disclosure is operator-access evidence. It is not evidence
that deterministic reviewed gold or the treatment-free C.5 packet was contaminated.

Reviewed gold was mechanically derived from the immutable primary Stage C,
independent Stage C-R, their completed reliability comparison, the treatment-blind
reconciliation and its agreed-cell seal. The C.5 packet contains the complete
18-by-32 semantic mapping frame without lexical pruning or precomputed coverage
decisions. Its strict query, result and treatment leakage checks passed. The
prepared packet contains no treatment-arm identities, queries, results, ranks,
scores, costs or outcomes. A fresh Stage C.5 adjudicator can remain independently
blind by using only the prepared sterile workspace.

This note is outside the reviewer packet. It must not be supplied to the C.5
adjudicator. No Stage C.5 or Stage D adjudication has been performed.
