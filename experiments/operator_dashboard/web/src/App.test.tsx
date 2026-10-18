// @vitest-environment jsdom
import { afterEach, expect, it, vi } from "vitest";
import { act } from "react";
import { createRoot, type Root } from "react-dom/client";
import { App, Dashboard, type Snapshot } from "./App";

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
  expect(node.textContent).toContain("Snapshot unavailable");
  expect(node.textContent).toContain("404");
});
