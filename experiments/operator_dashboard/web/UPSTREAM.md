# Upstream reuse

Pinned TencentCloud/TencentDB-Agent-Memory revision:
`e9a82935b52741e0c798c75326e90b7144eb4d5f` (resolved 2026-10-18).
[Source](https://github.com/TencentCloud/TencentDB-Agent-Memory/tree/e9a82935b52741e0c798c75326e90b7144eb4d5f/MemoryPanel/web).

The complete upstream copyright and MIT permission notice is preserved in
`public/UPSTREAM-LICENSE.txt`, copied into every production build. No logos,
credentials, account stores, mutation dialogs or backend code are adopted.
Only trailing spaces and line-ending formatting in the notice are normalized;
the complete copyright and permission text is retained.

Adopted from `MemoryPanel/web/src/`:

- `layouts/ConsoleLayout.tsx`: reduced to the existing Tea Layout, Body, Sider,
  Menu and Content composition. Replaced routing, auth, role/capability filtering,
  onboarding and Tencent header with two local read-only views and Devtools text.
- `components/asset/AssetSplitLayout.tsx` and its CSS: retained the resizable,
  responsive list/detail layout; replaced its sole translation dependency with
  the English accessible resizer label. No storage key is supplied, so it writes
  no localStorage state.
- `components/asset/AssetPageHeader.tsx`, its CSS and `components/StatusTag.tsx`:
  retained behavior, formatting only. No action slot is supplied.

`upstream.json` records original byte digests. Adopted files are formatted with
Prettier; they are not represented as byte-identical vendored originals.

Public-build verification: extracted only the pinned web subtree into ignored
inspection storage, ran `npm ci --ignore-scripts` and `npm run build` successfully.
The first install hit ECONNRESET; a cached retry succeeded. No bootstrap/backend
script ran. Upstream uses React 18, TypeScript, Vite and publicly available Tea,
i18n, graph and Markdown packages. No private package was required. Upstream
build took 25.07 seconds in Vite (1,385 modules), with chunk-size warnings.

Pilot subset: React/ReactDOM 18.3.1, Tea 2.8.0; TypeScript/Vite plus Vitest/jsdom,
Prettier and Playwright-core for local installed-browser verification. Dependencies
are locked by `package-lock.json`. No browser or model download is required.
Tea transitive packages declare older React peer ranges and emit a forwardRef
warning; observed interactions pass but broader component compatibility is not
established. Pilot JS is approximately 722 kB minified / 146 kB gzip and CSS
289 kB / 54 kB gzip. This is a reuse pilot, not bundle optimization or deployment.
Production dependency audit on 2026-10-18 reported zero advisories; this is a
point-in-time registry observation, not a security guarantee.
