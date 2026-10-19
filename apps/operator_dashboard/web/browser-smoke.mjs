// Verifies the actual local API and captured evidence, without model invocation.
import assert from "node:assert/strict";
import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { performance } from "node:perf_hooks";
import { chromium } from "playwright-core";
const started = performance.now();
const startedAt = new Date().toISOString();
const base = process.env.DASHBOARD_URL ?? "http://127.0.0.1:4174";
const snapshot = await (await fetch(base + "/api/overview")).json();
const output = resolve(process.env.DASHBOARD_SMOKE_OUTPUT ?? "dist/smoke");
await mkdir(output, { recursive: true });
assert.ok(process.env.CHROME_PATH, "Set CHROME_PATH to installed Chrome/Edge");
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH,
  headless: true,
});
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1100 },
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(String(e)));
  await page.goto(base);
  await page
    .getByRole("heading", { name: "Work Portfolio", exact: true })
    .waitFor();
  const proposal = snapshot.proposals[0];
  await page.getByRole("button", { name: new RegExp(proposal.title) }).click();
  await page
    .getByRole("heading", { name: proposal.title, exact: true })
    .waitFor();
  assert.ok(
    (await page.textContent("body")).includes("Proposed") ||
      (await page.textContent("body")).includes("benefit"),
  );
  await page.getByRole("button", { name: /B-0021/ }).click();
  await page
    .getByRole("heading", { name: "Selected work: B-0021", exact: true })
    .waitFor();
  await page
    .getByText("Original canonical Markdown", { exact: true })
    .waitFor();
  assert.ok((await page.textContent("body")).includes("B-0037"));
  await page.screenshot({
    path: resolve(output, "portfolio.png"),
    fullPage: true,
  });
  await page.getByText("Worker Activity", { exact: true }).click();
  await page
    .getByRole("heading", { name: "Worker Activity", exact: true })
    .waitFor();
  await page.getByLabel("Evidence type").selectOption("LOCAL_MODEL_RECEIPT");
  const live = snapshot.workers.filter(
    (w) => w.evidence_class === "LOCAL_MODEL_RECEIPT",
  );
  assert.equal(await page.locator(".run-list button").count(), live.length);
  const inspected = [];
  for (const worker of live) {
    await page
      .getByRole("button")
      .filter({ has: page.getByText(worker.id, { exact: true }) })
      .click();
    await page
      .getByRole("heading", { name: "Turn / event history", exact: true })
      .waitFor();
    const detail = await (await fetch(base + "/api/runs/" + worker.key)).json();
    assert.equal(await page.locator(".turn").count(), detail.turns.length);
    for (let i = 0; i < detail.turns.length; i++) {
      const turn = page.locator(".turn").nth(i);
      assert.ok(
        (await turn.locator(":scope > summary").textContent()).includes(
          detail.turns[i].stage.disposition,
        ),
      );
    }
    const first = page.locator(".turn").first();
    await first.locator(":scope > summary").click();
    await first
      .getByText("Native arguments (path, old_text, new_text)", {
        exact: false,
      })
      .click();
    await first
      .getByText("Host-generated proposal diff", { exact: false })
      .click();
    assert.ok((await first.textContent()).includes("propose_edit"));
    assert.ok((await first.textContent()).includes("old_text"));
    assert.ok((await first.textContent()).includes("MATCH"));
    inspected.push({
      run: worker.id,
      turns: detail.turns.length,
      outcomes: detail.turns.map((t) => t.stage.disposition),
    });
  }
  await page.screenshot({
    path: resolve(output, "activity.png"),
    fullPage: true,
  });
  await page
    .getByLabel("Evidence type")
    .selectOption("SCRIPTED_HOST_TEST_ONLY");
  assert.equal(
    await page.locator(".run-list button").count(),
    snapshot.workers.filter(
      (w) => w.evidence_class === "SCRIPTED_HOST_TEST_ONLY",
    ).length,
  );
  await page.getByRole("button", { name: "Refresh", exact: true }).click();
  await page.waitForFunction(
    () => !document.querySelector(".refresh button").disabled,
  );
  assert.deepEqual(errors, []);
  assert.equal((await page.request.post(base + "/api/overview")).status(), 405);
  assert.equal(
    (
      await page.request.get(base + "/api/overview", {
        headers: { Origin: "https://untrusted.example" },
      })
    ).status(),
    403,
  );
  assert.equal(
    (
      await page.request.get(base + "/api/overview", {
        headers: { Host: "untrusted.example" },
      })
    ).status(),
    403,
  );
  const result = {
    started_at: startedAt,
    elapsed_seconds: (performance.now() - started) / 1000,
    source_head: snapshot.source_head,
    proposals: snapshot.proposals.length,
    inspected,
    console_errors: errors,
    result: "PASS",
  };
  await writeFile(
    resolve(output, "result.json"),
    JSON.stringify(result, null, 2),
  );
  console.log(JSON.stringify(result));
} finally {
  await browser.close();
}
