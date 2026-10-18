// @vitest-environment jsdom
import { afterEach, expect, it, vi } from "vitest";
import { act } from "react";
import { createRoot, type Root } from "react-dom/client";
import { App, Dashboard, type Snapshot } from "./App";
import { PortfolioDetail, RunDetail } from "./Inspection";

const empty: Snapshot = {
  schema: "devtools-operator-snapshot-v1",
  observed_at: "fixture",
  source: "fixture",
  proposals: [],
  backlog: [],
  work: [],
  workers: [],
  errors: [],
  limitations: [],
};
let root: Root | undefined;
afterEach(async () => {
  if (root) await act(async () => root!.unmount());
  document.body.innerHTML = "";
  vi.unstubAllGlobals();
});
async function render(element: React.ReactNode) {
  vi.stubGlobal("IS_REACT_ACT_ENVIRONMENT", true);
  const container = document.createElement("div");
  document.body.append(container);
  root = createRoot(container);
  await act(async () => root!.render(element));
  return container;
}
it("renders both operator views, missing states and no mutation controls", async () => {
  const node = await render(<Dashboard data={empty} />);
  expect(node.textContent).toContain("No prepared assignments");
  expect(node.textContent).toContain("No approved intake proposals");
  const activity = [
    ...node.querySelectorAll('[role="menuitem"], .tea-menu__item'),
  ].find((x) => x.textContent?.includes("Worker Activity"));
  expect(activity).toBeTruthy();
  await act(async () => (activity as HTMLElement).click());
  expect(node.textContent).toContain("Missing records do not establish zero");
  expect(node.querySelector("form,input")).toBeNull();
});
it("shows actual receipt values and unknown categories without summation", async () => {
  const data: Snapshot = {
    ...empty,
    errors: [{ path: "broken", error: "digest mismatch" }],
    workers: [
      {
        id: "real-run",
        disposition: "ACCEPTED",
        accepted: true,
        started_at: "UTC",
        elapsed_seconds: 34.76,
        model_calls: 2,
        repair_cycles: 1,
        usage: {
          input_tokens: 8178,
          output_tokens: 525,
          cached_input_tokens: null,
          reasoning_tokens: null,
        },
        validation: { tests: 0, oracle: 0 },
        reference: { path: "local/result.json", sha256: "hash" },
        coverage: "Partial local observations",
      },
    ],
  };
  const node = await render(<Dashboard data={data} />);
  expect(node.textContent).toContain("digest mismatch");
  await act(async () =>
    (
      [...node.querySelectorAll(".tea-menu__item")].find((x) =>
        x.textContent?.includes("Worker Activity"),
      ) as HTMLElement
    ).click(),
  );
  expect(node.textContent).toContain("8178");
  expect(node.textContent).toContain("UNKNOWN");
  expect(node.textContent).toContain("local/result.json");
});
it("reports unavailable snapshot instead of fabricating data", async () => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ ok: false, status: 404 }));
  const node = await render(<App />);
  expect(node.textContent).toContain("Current data unavailable");
  expect(node.textContent).toContain("404");
});

it("refreshes current data and retains a visibly stale result on fetch failure", async () => {
  const api = vi
    .fn()
    .mockResolvedValueOnce({ ok: true, json: async () => empty })
    .mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        ...empty,
        proposals: [
          {
            id: "fixture",
            title: "Newly captured discovery",
            state: "PENDING_REVIEW",
          },
        ],
      }),
    })
    .mockRejectedValueOnce(new Error("connection lost"));
  vi.stubGlobal("fetch", api);
  const node = await render(<App />);
  const refresh = () => node.querySelector(".refresh button") as HTMLElement;
  await act(async () => refresh().click());
  expect(node.textContent).toContain("Newly captured discovery");
  await act(async () => refresh().click());
  expect(node.textContent).toContain("STALE previous successful data");
  expect(node.textContent).toContain("Newly captured discovery");
});

it("renders original backlog rationale, dependencies and source as plain text", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        metadata: { status: "SUPERSEDED", split_children: "B-0002" },
        rationale: ["Actual split reason"],
        body: { text: "# Original\n<script>untrusted</script>" },
        review_history: "NOT_RECORDED",
        reference: { path: "fixture" },
      }),
    }),
  );
  const node = await render(
    <PortfolioDetail kind="backlog" id="B-0001" refresh="one" />,
  );
  expect(node.textContent).toContain("Actual split reason");
  expect(node.textContent).toContain("B-0002");
  expect(node.textContent).toContain("<script>untrusted</script>");
  expect(node.querySelector("script")).toBeNull();
});

it("associates failed and accepted turns, native proposals and validation commands", async () => {
  const captured = {
    availability: "CAPTURED",
    text: "exact archived <script>model</script>",
    truncated: true,
    total_characters: 18000,
  };
  const turns = [1, 2].map((number) => ({
    number,
    stage: {
      disposition: number === 1 ? "TESTS_FAILED" : "ACCEPTED",
      proposal_valid: true,
      source_before: "before",
      source_after: "after",
      context: [],
    },
    tools: [
      {
        name: "propose_edit",
        provider_call_id: `call-${number}`,
        arguments: {
          ...captured,
          truncated: false,
          text: JSON.stringify({
            path: "src/example.py",
            old_text: "old\nregion",
            new_text: "new\n<script>inert</script>",
          }),
        },
      },
    ],
    request_text: captured,
    response_text: captured,
    feedback: captured,
    patch: captured,
    proposal_correlation: "MATCH",
    validation: {
      tests: {
        argv: ["python", "fixture-tests"],
        exit_code: number === 1 ? 1 : 0,
        stdout: captured,
        stderr: { availability: "NOT_CAPTURED", text: "NOT_CAPTURED" },
      },
    },
  }));
  vi.stubGlobal(
    "fetch",
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        objective: captured,
        turns,
        raw_disclosure: true,
        limitations: [],
        reference: { path: "fixture" },
      }),
    }),
  );
  const node = await render(<RunDetail id="fixture" refresh="one" />);
  expect(node.textContent).toContain("Turn 1 · TESTS_FAILED");
  expect(node.textContent).toContain("Turn 2 · ACCEPTED");
  expect(node.textContent).toContain("propose_edit");
  expect(node.textContent).toContain("Recorded edit target:");
  expect(node.textContent).toContain("src/example.py");
  expect(node.textContent).toContain("new\n<script>inert</script>");
  expect(node.textContent).toContain("NOT_CAPTURED");
  expect(node.textContent).toContain("TRUNCATED");
  expect(node.querySelector("script")).toBeNull();
});
