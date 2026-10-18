// Local installed browser only; no browser download or model invocation.
import assert from "node:assert/strict";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { performance } from "node:perf_hooks";
import { chromium } from "playwright-core";

const started = performance.now();
const source = JSON.parse(await readFile("dist/data.json", "utf8"));
const output = resolve(process.env.DASHBOARD_SMOKE_OUTPUT ?? "dist/smoke");
await mkdir(output, { recursive: true });
assert.ok(
  process.env.CHROME_PATH,
  "Set CHROME_PATH to an installed Chrome/Edge executable",
);
const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH,
  headless: true,
});
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
  });
  const failures = [];
  page.on("pageerror", (error) => failures.push(String(error)));
  await page.goto("http://127.0.0.1:4173");
  await page
    .getByRole("heading", { name: "Work Portfolio", exact: true })
    .waitFor();
  for (const proposal of source.proposals)
    assert.ok((await page.textContent("body")).includes(proposal.title));
  await page.screenshot({
    path: resolve(output, "portfolio.png"),
    fullPage: true,
  });
  await page.getByText("Worker Activity", { exact: true }).click();
  await page
    .getByRole("heading", { name: "Worker Activity", exact: true })
    .waitFor();
  for (const worker of source.workers) {
    await page
      .getByRole("button")
      .filter({ has: page.getByText(worker.id, { exact: true }) })
      .click();
    const text = await page.textContent("body");
    assert.ok(text.includes(worker.reference.path));
    assert.ok(text.includes(worker.evidence_class));
    assert.ok(text.includes(String(worker.usage.input_tokens ?? "UNKNOWN")));
    assert.ok(text.includes(String(worker.elapsed_seconds ?? "UNKNOWN")));
  }
  await page.screenshot({
    path: resolve(output, "activity.png"),
    fullPage: true,
  });
  assert.deepEqual(failures, []);
  assert.equal(
    (
      await page.request.post("http://127.0.0.1:4173/data.json", {
        data: "mutation",
      })
    ).status(),
    405,
  );
  assert.equal(
    (
      await page.request.get("http://127.0.0.1:4173/data.json", {
        headers: { Host: "untrusted.example" },
      })
    ).status(),
    403,
  );
  const served = await (
    await page.request.get("http://127.0.0.1:4173/data.json")
  ).json();
  assert.deepEqual(served, source);
  const report = {
    started_at: new Date().toISOString(),
    elapsed_seconds: (performance.now() - started) / 1000,
    workers: source.workers.length,
    proposals: source.proposals.length,
    console_errors: failures,
    result: "PASS",
  };
  await writeFile(
    resolve(output, "result.json"),
    JSON.stringify(report, null, 2),
  );
  console.log(JSON.stringify(report));
} finally {
  await browser.close();
}
