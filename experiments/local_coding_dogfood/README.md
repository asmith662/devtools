# Real local coding-agent dogfood

This collection retains one explicitly authorized fresh local-model task. It is
separate from the historical Qwen and Codex scientific collections and reopens
none of their evaluations. The selected model is configuration outside reusable
framework code.

See [the terminal summary](SUMMARY.md), [the case report](case_0001/REPORT.md),
[frozen task and oracle identities](case_0001/freeze.json), and the collection
manifest. The model-generated candidate and actual normalized requests/responses
are retained under `case_0001/evidence/`; all source is independently authored
synthetic task data. Raw personal logs, environment variables and credentials are
not inputs.

Read-only provenance verification, without a model or service:

```text
uv run python experiments/local_coding_dogfood/case_0001/verify.py
uv run python experiments/local_coding_dogfood/case_0001/verify.py --grade
```

The second command reruns only the immutable focused and held-out oracles on the
archived candidate through managed Commands. It is not another model attempt.

The original entry commands were `host.py prepare`, then the ignored managed
launcher calling `host.py run` under a 900-second timeout. The host rejects a
changed freeze or repeated entry. Historical temporary paths are provenance,
not restored execution authority. Do not delete entry markers or overwrite this
case to repeat inference. Another model evaluation needs a separately authorized
linked case with a fresh explicit output namespace and freeze. Retain this
protocol, source, oracles, output and limitations unchanged.

The core coding lifecycle is `devtools.agents.coding.run_coding_agent`; this
experiment owns task composition, model selection, exact scope, archives and
grading. It adds no production provider, executor, generic agent loop or store.
