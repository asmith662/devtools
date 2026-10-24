# Copyright (c) 2026
# ruff: noqa: EM101, TRY003, COM812, T201, N815 -- stdlib HTTP method aliases
"""Same-origin, loopback-only static UI and read-only domain/evidence API."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from contextlib import suppress
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from apps.operator_dashboard.details import (
    backlog_detail,
    confined,
    proposal_detail,
    run_detail,
)
from apps.operator_dashboard.project import _text, project
from devtools.core.paths import resolve_path
from devtools.core.time import Duration
from devtools.resources.commands import Command, CommandExecutor
from devtools.resources.filesystem import FilesystemError
from scripts.backlog.coordinator import git, locate

MAX_RESPONSE = 2 << 20
DIST = Path(__file__).parent / "web/dist"


class DashboardServer(HTTPServer):
    """One configured read-only source; clients cannot change roots or disclosure."""

    def __init__(
        self,
        root: Path,
        worker_roots: tuple[Path, ...],
        *,
        raw: bool = False,
        port: int = 4174,
    ) -> None:
        """Bind only to IPv4 loopback, including isolated test port zero."""
        self.root = resolve_path(root).value
        self.worker_roots = tuple(resolve_path(p).value for p in worker_roots)
        self.raw = raw
        super().__init__(("127.0.0.1", port), Handler)

    def overview(self) -> dict[str, Any]:
        """Read current state on every request, never an exported/cache authority."""
        result = project(self.root, worker_roots=self.worker_roots)
        try:
            result["source_head"] = asyncio.run(git(self.root, "rev-parse", "HEAD"))
        except ValueError as error:
            result["source_head"] = "UNAVAILABLE"
            result["errors"].append({"path": str(self.root), "error": str(error)})
        result["raw_disclosure"] = self.raw
        result["limitations"][1] = (
            "Only configured worker roots are inventoried; missing is not zero usage."
        )
        return result

    def detail(self, kind: str, identity: str) -> dict[str, Any]:
        """Resolve closed identifiers through current records, never client paths."""
        if kind == "proposals":
            return proposal_detail(self.root, identity)
        if kind == "backlog":
            return backlog_detail(self.root, identity)
        if kind != "runs" or not re.fullmatch(r"[a-f0-9]{64}", identity):
            raise ValueError("Invalid evidence identifier")
        index = project(self.root, worker_roots=self.worker_roots)
        matches = [r for r in index["workers"] if r["key"] == identity]
        if len(matches) != 1:
            raise ValueError("Run is missing or ambiguous")
        path = Path(matches[0]["reference"]["path"])
        base = next(p for p in self.worker_roots if path.is_relative_to(p))
        return run_detail(confined(base, path), raw=self.raw)


class Handler(BaseHTTPRequestHandler):
    """No CORS, writes, arbitrary reads or dispatch capabilities."""

    server: DashboardServer

    def log_message(self, format: str, *args: object) -> None:  # noqa: A002
        """Avoid printing request paths or raw operational content."""

    def _allowed(self) -> bool:
        host = f"127.0.0.1:{self.server.server_port}"
        origins = self.headers.get_all("Origin", [])
        if self.headers.get_all("Host") != [host] or origins not in (
            [],
            ["http://" + host],
        ):
            self._send(HTTPStatus.FORBIDDEN, b"Untrusted Host/Origin", "text/plain")
            return False
        if self.headers.get("Sec-Fetch-Site") == "cross-site":
            self._send(
                HTTPStatus.FORBIDDEN, b"Cross-site request refused", "text/plain"
            )
            return False
        return True

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        if len(body) > MAX_RESPONSE:
            status, body, content_type = (
                HTTPStatus.SERVICE_UNAVAILABLE,
                b"Response exceeds bounded size",
                "text/plain",
            )
        # A view change can abort an observation fetch. Do not retry sending a
        # second error response to a disconnected peer, or infer worker state.
        with suppress(ConnectionError):
            self.send_response(status)
            self.send_header("Content-Type", content_type + "; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header(
                "Content-Security-Policy",
                "default-src 'self'; style-src 'self' 'unsafe-inline'; "
                "img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'",
            )
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

    def do_POST(self) -> None:
        """Reject all consequential methods, including preflight requests."""
        self._send(
            HTTPStatus.METHOD_NOT_ALLOWED, b"Read-only: GET and HEAD only", "text/plain"
        )

    do_PUT = do_POST
    do_DELETE = do_POST
    do_PATCH = do_POST
    do_OPTIONS = do_POST

    def do_HEAD(self) -> None:
        """Provide the same read-only route without a response body."""
        self.do_GET()

    def do_GET(self) -> None:
        """Serve a bounded current projection or an explicitly bundled asset."""
        if not self._allowed():
            return
        parts = urlsplit(self.path)
        path = parts.path
        if (
            parts.query
            or parts.scheme
            or parts.netloc
            or any(token in path for token in ("..", "%", "\\"))
        ):
            self._send(HTTPStatus.BAD_REQUEST, b"Invalid route", "text/plain")
            return
        try:
            if path == "/api/overview":
                value = self.server.overview()
            elif re.fullmatch(r"/api/(proposals|backlog|runs)/[A-Za-z0-9-]+", path):
                _, _, kind, identity = path.split("/")
                value = self.server.detail(kind, identity)
            else:
                self._static(path)
                return
            body = json.dumps(value, ensure_ascii=True).encode("utf-8")
            self._send(HTTPStatus.OK, body, "application/json")
        except (ValueError, KeyError, TypeError, OSError, FilesystemError):
            self._send(
                HTTPStatus.NOT_FOUND,
                b"Record unavailable, invalid or outside configured evidence scope",
                "text/plain",
            )

    def _static(self, path: str) -> None:
        if path == "/":
            name, content_type = "index.html", "text/html"
        elif path == "/UPSTREAM-LICENSE.txt":
            name, content_type = path[1:], "text/plain"
        elif re.fullmatch(r"/assets/[\w.-]+\.(js|css)", path):
            name = path[1:]
            content_type = "text/javascript" if name.endswith(".js") else "text/css"
        else:
            self._send(HTTPStatus.NOT_FOUND, b"Not found", "text/plain")
            return
        # The closed bundle list is UTF-8 text; reuse canonical bounded decoding.
        file = confined(DIST, DIST / name)
        self._send(HTTPStatus.OK, _text(file).encode("utf-8"), content_type)


async def _startup(args: argparse.Namespace) -> DashboardServer:
    checkout = resolve_path(Path(__file__)).value.parents[2]
    root = await locate(checkout)
    if args.build:
        result = await CommandExecutor().execute(
            Command("npm.cmd")
            .args("run", "build")
            .cwd(resolve_path(DIST.parent))
            .with_timeout(Duration.seconds(120))
        )
        print("Frontend build: " + ("FAIL" if result.failed else "PASS"))
        if result.failed:
            raise ValueError(
                "Frontend build failed: "
                + result.stderr.decode("utf-8", errors="replace")
            )
    if not (DIST / "index.html").is_file():
        raise ValueError("Frontend unavailable; start with --build after npm ci")
    roots = tuple(
        resolve_path(p, base_directory=Path.cwd()).value for p in args.worker_root
    )
    if any(not p.is_dir() for p in roots):
        raise ValueError("Configured worker root is missing")
    return DashboardServer(root, roots, raw=args.raw_details, port=args.port)


def main() -> None:
    """One local startup command; configuration is supplied by the trusted host."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--worker-root", action="append", required=True, type=Path)
    parser.add_argument("--raw-details", action="store_true")
    parser.add_argument("--build", action="store_true")
    parser.add_argument("--port", type=int, default=4174)
    args = parser.parse_args()
    server = asyncio.run(_startup(args))
    print(
        f"Read-only dashboard http://127.0.0.1:{server.server_port}/; "
        f"raw disclosure={server.raw}; Ctrl+C to stop"
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
