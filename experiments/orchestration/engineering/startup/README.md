# Worker startup preflight and preparation-only recovery

Run `b34e9e288e30f7289e14453f8a2f9ca8acd6940dee05037486c403c803b5d2c6`
was approved at `52e697cea6b4ce066898031938e127f0c565fc3a`. All three Python
prepare workers exited 1 during imports, before treatment or gold entry. Their
direct script directory exposed local `statistics.py` as top-level `statistics`,
recursively shadowing the standard library's `variance` import. Renaming that owner
to `estimators.py` changes no estimator arithmetic. No path workaround or
conditional import is added. A sibling-name regression checks this package
against Python's standard-library names.

The separate [disposition](../../../source_grounding/invalidations/b34e9e288e30f7289e14453f8a2f9ca8acd6940dee05037486c403c803b5d2c6/invalidation.json)
classifies PRE_SCIENTIFIC_INFRASTRUCTURE_FAILURE. Its exact-byte gzip archive binds
original process/exit/trace records, prepare journals, run context and approval.
Original files remain unchanged; this is no old publication receipt or approval
of corrected bytes. No failed scientific judgment exists. Model invocations are
absent, rather than synthetic zero-token invocation rows. Usage observation stays
partial; closed process records establish this run launched no model.

`experiments.orchestration.entrypoints` owns a narrow prospective execution check,
not a plugin registry or framework runtime. Its versioned optional plan field
declares exact direct Python script bytes and a finite timeout. The inventory must
cover every unique configured Python stage/validator/semantic worker entrypoint.
The discrimination plan has one: `discrimination/entry.py`, shared by all stages.
Nested host artifact builders are deterministic serializers, not additional plan
workers or semantic operations; their existing projection/replay tests remain.

The gate executes the controller interpreter with `-B`, an absolute script path
and `--help` from an empty disposable directory outside the checkout and script
directory. It requires exit zero, genuine argparse help, bounded output, unchanged
CWD and unchanged script bytes. Imports run; no workspace, stage dispatch,
network operation, model or ENTERED claim runs. The receipt retains exact argv,
interpreter version, ephemeral CWD and output hashes. This proves import/startup,
not future scientific correctness or complete runtime compatibility.

Order is implementation/static validation, exact committed plan authentication,
real worker startup gate, PLAN_VALID, explicit maintainer approval, then prepare
and science. A bound plan cannot report validity or publish approval without a
successful gate. Missing/incomplete declarations, import failure or process failure
are PLAN_INVALID. Old durable plans remain parseable; the discrimination adapter
cannot obtain prospective validity without its gate. No old approval authorizes
changed implementation.

Manual operation uses precisely the same code as plan validation:

```text
uv run python -m experiments.orchestration.entrypoints experiments/source_grounding/plans/candidate-discrimination-startup-run-plan.json
```

The binding-only replacement copies candidate-05 universe, selections, packets,
method, cohort, economics and treatment template byte-for-byte. It rebinds the
corrected implementation and startup contract; the scientific question, labels,
seed/weights, analysis, adopted branches, models/efforts and four-call maximum do
not change. Failed prepare consumes 0/4 semantic calls. It must not be resumed.
