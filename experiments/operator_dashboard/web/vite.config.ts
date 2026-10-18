import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

// Preview only: no mutation routes, repository serving, proxy or external host.
function readOnlyLoopback(): Plugin {
  return {
    name: "read-only-loopback",
    configurePreviewServer(server) {
      server.middlewares.use((request, response, next) => {
        if (!/^127\.0\.0\.1(?::\d+)?$/.test(request.headers.host ?? "")) {
          response.writeHead(403).end();
          return;
        }
        if (!["GET", "HEAD"].includes(request.method ?? "")) {
          response.writeHead(405, { Allow: "GET, HEAD" }).end();
          return;
        }
        response.setHeader("Cache-Control", "no-store");
        response.setHeader("X-Content-Type-Options", "nosniff");
        response.setHeader(
          "Content-Security-Policy",
          "default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'",
        );
        next();
      });
    },
  };
}
export default defineConfig({
  plugins: [react(), readOnlyLoopback()],
  preview: { host: "127.0.0.1", cors: false },
});
