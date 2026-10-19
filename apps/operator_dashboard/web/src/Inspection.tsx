import { useEffect, useState } from "react";

// Response objects are intentionally displayed as archived JSON/plain text,
// not promoted into a second work/run domain model.
export type RecordData = Record<string, any>; // eslint-disable-line @typescript-eslint/no-explicit-any
export function useRecord(url: string, refresh: string | number = 0) {
  const [data, setData] = useState<RecordData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    fetch(url, { cache: "no-store", signal: controller.signal })
      .then(async (r) => {
        if (!r.ok) throw new Error(`HTTP ${r.status}: record unavailable`);
        const value = await r.json();
        if (!controller.signal.aborted) {
          setData(value);
          setError(null);
        }
      })
      .catch((e) => {
        if (!controller.signal.aborted) setError(String(e));
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [url, refresh]);
  return { data, error, loading };
}
export const known = (v: unknown) =>
  v === null || v === undefined
    ? "NOT_RECORDED"
    : typeof v === "object"
      ? JSON.stringify(v, null, 2)
      : String(v);
export function Fields({ value }: { value: RecordData }) {
  return (
    <dl>
      {Object.entries(value).map(([key, v]) => (
        <div key={key}>
          <dt>{key.replaceAll("_", " ")}</dt>
          <dd>
            <pre>{known(v)}</pre>
          </dd>
        </div>
      ))}
    </dl>
  );
}
export function Evidence({ value }: { value: unknown }) {
  return (
    <details>
      <summary>Provenance / source reference</summary>
      <pre>{known(value)}</pre>
    </details>
  );
}
export function Archived({
  title,
  value,
}: {
  title: string;
  value: RecordData | undefined;
}) {
  return (
    <details className="archive">
      <summary>
        {title} · {value?.availability ?? "NOT_CAPTURED"}
        {value?.truncated ? " · TRUNCATED" : ""}
      </summary>
      <pre>{value?.text ?? "NOT_CAPTURED"}</pre>
      {value?.truncated && (
        <p>
          Display truncated at 16,000 characters; original length{" "}
          {value.total_characters}. The archived source remains unchanged.
        </p>
      )}
      {value?.reference && <Evidence value={value.reference} />}
    </details>
  );
}
function EditArguments({ value }: { value: RecordData }) {
  let fields: RecordData | null = null;
  if (value.availability === "CAPTURED" && !value.truncated) {
    try {
      const parsed: unknown = JSON.parse(value.text);
      if (parsed && typeof parsed === "object" && !Array.isArray(parsed))
        fields = parsed as RecordData;
    } catch {
      /* Preserve unparseable archived JSON below. */
    }
  }
  return (
    <>
      {fields && (
        <>
          <p>
            Recorded edit target: <code>{known(fields.path)}</code>
          </p>
          {["old_text", "new_text"].map((key) => (
            <details key={key}>
              <summary>Decoded {key}</summary>
              <pre>{known(fields![key])}</pre>
            </details>
          ))}
        </>
      )}
      <Archived
        title="Native arguments (path, old_text, new_text)"
        value={value}
      />
    </>
  );
}
export function LocalTime({ value }: { value: string | null | undefined }) {
  const date = value ? new Date(value) : null;
  return (
    <span title={value ?? "NOT_RECORDED"}>
      {date && !isNaN(date.valueOf()) ? date.toLocaleString() : known(value)}
      {value && <small> · UTC source: {value}</small>}
    </span>
  );
}
export function PortfolioDetail({
  kind,
  id,
  refresh,
}: {
  kind: string;
  id: string;
  refresh: string;
}) {
  const { data, error, loading } = useRecord(`/api/${kind}/${id}`, refresh);
  return (
    <section className="panel" aria-label="Selected work detail">
      <h3>Selected work: {id}</h3>
      {loading && <p>Loading current record…</p>}
      {error && (
        <p role="alert">
          {error}
          {data ? " · STALE previous detail" : ""}
        </p>
      )}
      {data &&
        (kind === "proposals" ? (
          <>
            <h3>{data.proposal.payload.title}</h3>
            <Fields
              value={{
                disposition: data.state,
                ...data.proposal.payload,
                implementation_authority: data.implementation_authority,
              }}
            />
            <h4>Possible duplicates</h4>
            <pre>
              {data.duplicates.length
                ? known(data.duplicates)
                : "None reported by existing detector"}
            </pre>
            <h4>Review history</h4>
            <pre>
              {data.history.length
                ? known(data.history)
                : "NOT_RECORDED — no review decision"}
            </pre>
            <Evidence value={data.reference} />
          </>
        ) : (
          <>
            <Fields value={data.metadata} />
            <h4>Recorded disposition rationale</h4>
            <pre>{known(data.rationale)}</pre>
            <p>
              Unspecified rationale, acceptance, priority and decision fields
              are NOT_RECORDED; none is inferred from lifecycle status.
            </p>
            <h4>Original canonical Markdown</h4>
            <pre className="document">{data.body.text}</pre>
            {data.body.truncated && <p>TRUNCATED source display</p>}
            <h4>Linked review history</h4>
            <pre>{known(data.review_history)}</pre>
            <Evidence value={data.reference} />
          </>
        ))}
    </section>
  );
}
export function RunDetail({ id, refresh }: { id: string; refresh: string }) {
  const { data, error, loading } = useRecord(`/api/runs/${id}`, refresh);
  return (
    <section aria-label="Run inspection">
      {loading && <p>Loading archived run…</p>}
      {error && <p role="alert">{error}</p>}
      {data && (
        <>
          <h3>Task objective</h3>
          <pre className="document">{data.objective.text}</pre>
          <Fields
            value={{
              task_identity: data.task_identity,
              model: data.model,
              profile: data.profile,
              limits: data.limits,
              validation_seconds: data.validation_seconds,
            }}
          />
          <p>
            Raw disclosure:{" "}
            {data.raw_disclosure
              ? "enabled for this trusted local server"
              : "disabled; restart with --raw-details to inspect archived text"}
          </p>
          <h3>Turn / event history</h3>
          {data.turns_truncated && (
            <p>
              TRUNCATED timeline: showing 10 of {data.recorded_turn_count}{" "}
              recorded turns.
            </p>
          )}
          {data.turns.length === 0 && (
            <p>NOT_CAPTURED — no model-turn records</p>
          )}
          {data.turns.map((turn: RecordData) => (
            <details className="turn" key={turn.number}>
              <summary>
                Turn {turn.number} · {turn.stage.disposition ?? "UNKNOWN"} ·{" "}
                {turn.stage.elapsed_seconds ?? "UNKNOWN"} seconds
              </summary>
              <p>
                <LocalTime value={turn.stage.started_at} />
              </p>
              <p>
                Ended: <LocalTime value={turn.stage.finished_at} />
              </p>
              <Fields
                value={{
                  phase: turn.stage.phase,
                  termination: turn.stage.termination,
                  model_seconds: turn.stage.model_seconds,
                  usage: turn.stage.usage,
                  proposal_id: turn.stage.proposal_id,
                  proposal_admitted: turn.stage.proposal_valid,
                  proposal_response_correlation: turn.proposal_correlation,
                  source_before: turn.stage.source_before,
                  source_after: turn.stage.source_after,
                  settings: turn.settings,
                  recorded_request_role: turn.request_role,
                  recorded_response_source: turn.response_source,
                }}
              />
              <details>
                <summary>
                  Host Context acquisition ·{" "}
                  {turn.stage.context_bytes ?? "UNKNOWN"} bytes
                </summary>
                <pre>{known(turn.stage.context)}</pre>
                <p>
                  Recorded utilization: {known(turn.stage.context_utilization)}.
                  These source acquisitions were host-selected, not model Tool
                  calls.
                </p>
              </details>
              <Archived
                title="Exact recorded request prompt"
                value={turn.request_text}
              />
              <Archived
                title="Exact recorded model response"
                value={turn.response_text}
              />
              <Archived
                title="Recorded reasoning"
                value={turn.reasoning_text}
              />
              <Archived
                title="Conversation continuation identity"
                value={turn.conversation}
              />
              <Archived
                title="Exact host feedback in this request"
                value={turn.feedback}
              />
              <Archived
                title="Recorded host Tool results"
                value={turn.tool_results}
              />
              <h4>Model-requested native Tool calls</h4>
              {!turn.tools.length && <p>NOT_CAPTURED</p>}
              {turn.tools.map((tool: RecordData, i: number) => (
                <div key={i}>
                  <strong>{tool.name}</strong>
                  <p>
                    {tool.name === "propose_edit"
                      ? `Edit proposal; host admission: ${known(turn.stage.proposal_valid)}`
                      : "Read-only Context request; inspect its recorded host result."}
                  </p>
                  <code>{known(tool.provider_call_id)}</code>
                  {tool.name === "propose_edit" ? (
                    <EditArguments value={tool.arguments} />
                  ) : (
                    <Archived
                      title="Native Context arguments"
                      value={tool.arguments}
                    />
                  )}
                </div>
              ))}
              <Archived
                title="Host-generated proposal diff"
                value={turn.patch}
              />
              <h4>Host-executed validation commands</h4>
              {Object.entries(turn.validation).map(([name, raw]) => {
                const command = raw as RecordData;
                return (
                  <section key={name}>
                    <h4>
                      {name} · exit {known(command.exit_code)}
                    </h4>
                    <pre>{known(command.argv)}</pre>
                    <p>{known(command.elapsed_seconds)} seconds</p>
                    <Archived title={`${name} stdout`} value={command.stdout} />
                    <Archived title={`${name} stderr`} value={command.stderr} />
                  </section>
                );
              })}
              <Evidence
                value={{
                  request: turn.request_reference,
                  response: turn.response_reference,
                }}
              />
            </details>
          ))}
          <Evidence value={data.reference} />
          {data.limitations.map((l: string) => (
            <p key={l}>{l}</p>
          ))}
        </>
      )}
    </section>
  );
}
