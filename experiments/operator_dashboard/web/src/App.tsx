import { useEffect, useState } from "react";
import { ConsoleLayout } from "./ConsoleLayout";
import { AssetSplitLayout } from "./upstream/AssetSplitLayout";
import { AssetPageHeader } from "./upstream/AssetPageHeader";
import { StatusTag } from "./upstream/StatusTag";

type Reference = { path: string; sha256: string };
type Proposal = {
  id: string;
  title: string;
  state: string;
  parent: string | null;
  evidence: string[];
  reference: Reference;
};
type Item = { id: string; title: string; status: string; reference: Reference };
type Work = {
  item: string;
  disposition: string;
  grant_record_present: boolean;
  branch: string | null;
  reference: Reference;
};
type Worker = {
  id: string;
  evidence_class?: string;
  disposition: string;
  accepted: boolean | null;
  started_at: string | null;
  elapsed_seconds: number | null;
  model_calls: number | null;
  repair_cycles: number | null;
  usage: Record<string, number | null>;
  validation: Record<string, number | null>;
  reference: Reference;
  coverage: string;
};
export type Snapshot = {
  schema: string;
  observed_at: string;
  source: string;
  source_head?: string;
  source_dirty?: boolean;
  proposals: Proposal[];
  backlog: Item[];
  work: Work[];
  workers: Worker[];
  errors: { path: string; error: string }[];
  limitations: string[];
};
const known = (value: unknown) =>
  value === null || value === undefined ? "UNKNOWN" : String(value);
function Evidence({ reference }: { reference: Reference }) {
  return (
    <div className="evidence">
      <strong>Local evidence reference</strong>
      <code>{reference.path}</code>
      <code>SHA-256 {reference.sha256}</code>
    </div>
  );
}
function Empty({ children }: { children: string }) {
  return <p className="empty">{children}</p>;
}
function Portfolio({ data }: { data: Snapshot }) {
  return (
    <>
      <AssetPageHeader
        title="Work Portfolio"
        scope="Snapshot / no mutation controls"
        subtitle="Backlog review, implementation authority and protected integration remain separate."
      />
      <section className="panel">
        <h3>Proposal queue</h3>
        {data.proposals.length === 0 && (
          <Empty>No proposal records found.</Empty>
        )}
        {data.proposals.map((p) => (
          <details key={p.id}>
            <summary>
              <StatusTag label={p.state} /> {p.title}
            </summary>
            <p>Parent: {known(p.parent)}</p>
            <ul>
              {p.evidence.map((e) => (
                <li key={e}>{e}</li>
              ))}
            </ul>
            <Evidence reference={p.reference} />
          </details>
        ))}
      </section>
      <section className="panel">
        <h3>Approved intake proposals</h3>
        {data.proposals.filter((p) => p.state === "APPROVED").length === 0 && (
          <Empty>
            No approved intake proposals found. Legacy backlog entries are not
            inferred approval.
          </Empty>
        )}
        {data.proposals
          .filter((p) => p.state === "APPROVED")
          .map((p) => (
            <p key={p.id}>
              {p.title} · {p.id}
            </p>
          ))}
      </section>
      <section className="panel">
        <h3>Assignments and review outcomes</h3>
        {data.work.length === 0 && (
          <Empty>No prepared assignments or work results found.</Empty>
        )}
        {data.work.map((w) => (
          <details key={w.item}>
            <summary>
              {w.item} <StatusTag label={w.disposition} />
            </summary>
            <p>
              Branch: {known(w.branch)} · Stored grant:{" "}
              {w.grant_record_present
                ? "present, current authority not assessed"
                : "absent"}
            </p>
            <Evidence reference={w.reference} />
          </details>
        ))}
      </section>
      <section className="panel">
        <h3>Canonical backlog inventory</h3>
        <p>Recorded lifecycle status, not an implementation grant.</p>
        {data.backlog.length === 0 && (
          <Empty>No canonical backlog records found.</Empty>
        )}
        {data.backlog.map((b) => (
          <details key={b.id}>
            <summary>
              {b.title} <StatusTag label={b.status} />
            </summary>
            <Evidence reference={b.reference} />
          </details>
        ))}
      </section>
    </>
  );
}
function Activity({ data }: { data: Snapshot }) {
  const [selected, setSelected] = useState<string | null>(null);
  const worker = data.workers.find((w) => w.id === selected) ?? data.workers[0];
  return (
    <>
      <AssetPageHeader
        title="Worker Activity"
        scope={`${data.workers.length} local result records`}
        subtitle="Historical receipts. Unknown measurements remain unknown; accepted evaluation does not imply protected integration."
      />
      {!worker ? (
        <Empty>
          No worker result receipts found. Missing records do not establish zero
          model consumption.
        </Empty>
      ) : (
        <AssetSplitLayout
          sidebar={
            <div className="run-list">
              {data.workers.map((w) => (
                <button
                  type="button"
                  key={w.id}
                  aria-pressed={worker.id === w.id}
                  onClick={() => setSelected(w.id)}
                >
                  <strong>{w.id}</strong>
                  <small>{w.evidence_class ?? "UNCLASSIFIED"}</small>
                  <StatusTag label={w.disposition} />
                </button>
              ))}
            </div>
          }
          detail={
            <article className="panel">
              <h3>{worker.id}</h3>
              <p>
                <strong>
                  {worker.evidence_class ??
                    "UNCLASSIFIED — not proof of live inference"}
                </strong>
              </p>
              {worker.evidence_class === "SCRIPTED_HOST_TEST_ONLY" && (
                <p>
                  Scripted host validation: calls and tokens below are
                  synthetic, not Qwen consumption.
                </p>
              )}
              <StatusTag
                label={worker.disposition}
                theme={worker.accepted === true ? "success" : "warning"}
              />
              <dl>
                {Object.entries({
                  "Started UTC": worker.started_at,
                  "Elapsed seconds": worker.elapsed_seconds,
                  "Model calls attempted": worker.model_calls,
                  "Repair cycles": worker.repair_cycles,
                  "Input tokens": worker.usage.input_tokens,
                  "Output tokens": worker.usage.output_tokens,
                  "Cached input (subset)": worker.usage.cached_input_tokens,
                  "Reasoning output (subset)": worker.usage.reasoning_tokens,
                  "Tests exit code": worker.validation.tests,
                  "Independent oracle exit code": worker.validation.oracle,
                }).map(([k, v]) => (
                  <div key={k}>
                    <dt>{k}</dt>
                    <dd>{known(v)}</dd>
                  </div>
                ))}
              </dl>
              <p>{worker.coverage}</p>
              <p>
                Cached input and reasoning output are subsets; no category
                totals are added here.
              </p>
              <Evidence reference={worker.reference} />
            </article>
          }
        />
      )}
    </>
  );
}
export function Dashboard({ data }: { data: Snapshot }) {
  const [page, setPage] = useState("portfolio");
  return (
    <ConsoleLayout page={page} onPage={setPage}>
      <aside className="snapshot">
        Observed {data.observed_at} · Source {data.source}
        <code>
          {data.source_head ?? "Revision UNKNOWN"}
          {data.source_dirty ? " · uncommitted source records present" : ""}
        </code>
      </aside>
      {data.errors.length > 0 && (
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
  const [data, setData] = useState<Snapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    fetch("/data.json", { cache: "no-store" })
      .then(async (response) => {
        if (!response.ok)
          throw new Error(
            `Snapshot unavailable (HTTP ${response.status}). Run the projection after building.`,
          );
        const value: Snapshot = await response.json();
        if (
          value.schema !== "devtools-operator-snapshot-v1" ||
          ![
            "proposals",
            "backlog",
            "work",
            "workers",
            "errors",
            "limitations",
          ].every((k) => Array.isArray(value[k as keyof Snapshot]))
        )
          throw new Error(
            "Invalid snapshot schema. Regenerate the projection.",
          );
        setData(value);
      })
      .catch((e) => setError(String(e)));
  }, []);
  if (error)
    return (
      <main role="alert">
        <h1>Snapshot unavailable</h1>
        <p>{error}</p>
      </main>
    );
  return data ? (
    <Dashboard data={data} />
  ) : (
    <main>Loading local snapshot…</main>
  );
}
