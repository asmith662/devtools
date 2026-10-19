import { useEffect, useState } from "react";
import { ConsoleLayout } from "./ConsoleLayout";
import { AssetSplitLayout } from "./upstream/AssetSplitLayout";
import { AssetPageHeader } from "./upstream/AssetPageHeader";
import { StatusTag } from "./upstream/StatusTag";
import {
  Evidence,
  Fields,
  LocalTime,
  PortfolioDetail,
  RunDetail,
  useRecord,
  type RecordData,
} from "./Inspection";

export type Snapshot = {
  schema: string;
  observed_at: string;
  source: string;
  source_head?: string;
  proposals: RecordData[];
  backlog: RecordData[];
  work: RecordData[];
  workers: RecordData[];
  errors: RecordData[];
  limitations: string[];
};
const taskTitle = (worker: RecordData) =>
  String(worker.task_name ?? "Task NOT_RECORDED")
    .replaceAll("-", " ")
    .replace(/^./, (s) => s.toUpperCase());
function Portfolio({ data }: { data: Snapshot }) {
  const [selected, setSelected] = useState<{ kind: string; id: string } | null>(
    null,
  );
  const [status, setStatus] = useState("ALL");
  return (
    <>
      <AssetPageHeader
        title="Work Portfolio"
        scope="Current read-only records"
        subtitle="Review, implementation authority and protected integration remain separate."
      />
      <label>
        Lifecycle filter{" "}
        <select
          aria-label="Lifecycle filter"
          value={status}
          onChange={(e) => setStatus(e.target.value)}
        >
          {[
            "ALL",
            ...new Set([
              ...data.proposals.map((p) => p.state),
              ...data.backlog.map((b) => b.status),
            ]),
          ].map((s) => (
            <option key={s}>{s}</option>
          ))}
        </select>
      </label>
      <AssetSplitLayout
        sidebar={
          <div className="run-list">
            <h3>Proposal queue</h3>
            {data.proposals
              .filter((p) => status === "ALL" || p.state === status)
              .map((p) => (
                <button
                  key={p.id}
                  onClick={() => setSelected({ kind: "proposals", id: p.id })}
                >
                  <strong>{p.title}</strong>
                  <StatusTag label={p.state} />
                </button>
              ))}
            {!data.proposals.length && <p>No proposal records found.</p>}
            {!data.proposals.some((p) => p.state === "APPROVED") && (
              <p>No approved intake proposals found.</p>
            )}
            <h3>Canonical backlog</h3>
            {data.backlog
              .filter((b) => status === "ALL" || b.status === status)
              .map((b) => (
                <button
                  key={b.id}
                  onClick={() => setSelected({ kind: "backlog", id: b.id })}
                >
                  <strong>{b.title}</strong>
                  <StatusTag label={b.status} />
                </button>
              ))}
          </div>
        }
        detail={
          selected ? (
            <PortfolioDetail
              key={selected.kind + selected.id}
              {...selected}
              refresh={data.observed_at}
            />
          ) : (
            <section className="panel">
              <h3>Select work to inspect</h3>
              <p>
                Objective, evidence, dependencies and original source are
                available through each record. Missing information is
                NOT_RECORDED.
              </p>
            </section>
          )
        }
      />
      <section className="panel">
        <h3>Assignments and review outcomes</h3>
        {!data.work.length && (
          <p>No prepared assignments or work results found.</p>
        )}
        {data.work.map((w) => (
          <details key={w.item}>
            <summary>
              {w.item} · {w.disposition}
            </summary>
            <Fields value={w} />
            <p>Recorded grant presence is not current authority.</p>
          </details>
        ))}
      </section>
    </>
  );
}
function Activity({ data }: { data: Snapshot }) {
  const [filter, setFilter] = useState("ALL");
  const [selected, setSelected] = useState<string | null>(null);
  const workers = data.workers.filter(
    (w) => filter === "ALL" || w.evidence_class === filter,
  );
  const worker =
    workers.find((w) => (w.key ?? w.id) === selected) ?? workers[0];
  const groups = workers.reduce<Record<string, RecordData[]>>((acc, w) => {
    const key = w.task_key ?? w.task_name ?? "Task NOT_RECORDED";
    (acc[key] ??= []).push(w);
    return acc;
  }, {});
  return (
    <>
      <AssetPageHeader
        title="Worker Activity"
        scope={`${data.workers.length} archived run records`}
        subtitle="Task → actual run → captured turns. Historical receipts are not current liveness or authority."
      />
      <label>
        Evidence type{" "}
        <select
          aria-label="Evidence type"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        >
          <option value="ALL">All evidence</option>
          <option value="LOCAL_MODEL_RECEIPT">Real local-model receipts</option>
          <option value="SCRIPTED_HOST_TEST_ONLY">Scripted host tests</option>
        </select>
      </label>
      {!worker ? (
        <p>Missing records do not establish zero model consumption.</p>
      ) : (
        <AssetSplitLayout
          sidebar={
            <div className="run-list">
              {Object.entries(groups).map(([task, runs]) => (
                <section key={task}>
                  <h3>
                    {runs?.[0] ? taskTitle(runs[0]) : "Task NOT_RECORDED"}
                  </h3>
                  {runs?.map((w) => (
                    <button
                      key={w.key ?? w.id}
                      aria-pressed={worker === w}
                      onClick={() => setSelected(w.key ?? w.id)}
                    >
                      <strong>{w.id}</strong>
                      <small>{w.evidence_class ?? "UNCLASSIFIED"}</small>
                      <StatusTag label={w.disposition} />
                    </button>
                  ))}
                </section>
              ))}
            </div>
          }
          detail={
            <article className="panel">
              <h3>
                {taskTitle(worker)} · {worker.id}
              </h3>
              <StatusTag
                label={worker.disposition}
                theme={worker.accepted ? "success" : "warning"}
              />
              {worker.evidence_class === "SCRIPTED_HOST_TEST_ONLY" && (
                <p>
                  <strong>
                    SCRIPTED HOST TEST — reported calls/tokens are synthetic,
                    not Qwen consumption.
                  </strong>
                </p>
              )}
              <p>
                Started: <LocalTime value={worker.started_at} />
              </p>
              <p>
                Ended: <LocalTime value={worker.finished_at} />
              </p>
              <Fields
                value={{
                  elapsed_seconds: worker.elapsed_seconds,
                  model_calls_attempted: worker.model_calls,
                  repair_cycles: worker.repair_cycles,
                  usage: worker.usage,
                  validation_exit_codes: worker.validation,
                }}
              />
              <p>
                Unknown usage remains UNKNOWN / NOT_RECORDED. Cache and
                reasoning are subsets, never added twice.
              </p>
              {worker.key ? (
                <RunDetail
                  key={worker.key}
                  id={worker.key}
                  refresh={data.observed_at}
                />
              ) : (
                <p>Detailed record identity NOT_CAPTURED.</p>
              )}
              <Evidence value={worker.reference} />
            </article>
          }
        />
      )}
    </>
  );
}
export function Dashboard({
  data,
  onRefresh,
  loading = false,
  error = null,
}: {
  data: Snapshot;
  onRefresh?: () => void;
  loading?: boolean;
  error?: string | null;
}) {
  const [page, setPage] = useState("portfolio");
  return (
    <ConsoleLayout
      page={page}
      onPage={(p) => {
        setPage(p);
        onRefresh?.();
      }}
    >
      <div className="refresh">
        <button onClick={onRefresh} disabled={loading}>
          Refresh
        </button>
        <span>
          {loading ? "Refreshing…" : "Last successful refresh: "}
          <LocalTime value={data.observed_at} />
        </span>
      </div>
      {error && (
        <p role="alert">
          {error} · STALE previous successful data; not current readiness.
        </p>
      )}
      <Evidence value={{ source: data.source, head: data.source_head }} />
      {!!data.errors.length && (
        <section role="alert" className="panel">
          <h3>Incomplete or invalid records</h3>
          {data.errors.map((e, i) => (
            <p key={i}>
              {e.path}: {e.error}
            </p>
          ))}
        </section>
      )}
      {page === "portfolio" ? (
        <Portfolio data={data} />
      ) : (
        <Activity data={data} />
      )}
      <aside className="limitations">
        {data.limitations.map((l) => (
          <p key={l}>{l}</p>
        ))}
      </aside>
    </ConsoleLayout>
  );
}
export function App() {
  const [revision, setRevision] = useState(0);
  const { data, error, loading } = useRecord("/api/overview", revision);
  const refresh = () => setRevision((v) => v + 1);
  useEffect(() => {
    const timer = setInterval(() => {
      if (document.visibilityState === "visible") refresh();
    }, 60000);
    return () => clearInterval(timer);
  }, []);
  if (!data)
    return (
      <main>
        <h1>{error ? "Current data unavailable" : "Loading current data…"}</h1>
        {error && <p role="alert">{error}</p>}
        <button onClick={refresh}>Refresh</button>
      </main>
    );
  if (data.schema !== "devtools-operator-snapshot-v1")
    return <main role="alert">Invalid API schema</main>;
  return (
    <Dashboard
      data={data as Snapshot}
      onRefresh={refresh}
      loading={loading}
      error={error}
    />
  );
}
