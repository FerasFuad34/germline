#!/usr/bin/env python3
"""
Export a fully static mirror of the GERMLINE web demo.

Runs the FastAPI app in-process (TestClient), captures every public endpoint,
and writes it into site/ as static files:

    site/index.html          — single-page mirror (fetches the JSON below)
    site/api/summary.json    — /api/summary
    site/api/corpus.json     — /api/corpus
    site/api/gate-g0..g2.json— /api/gate?generation=gN
    site/passport.json       — /passport.json
    site/healthz.json        — /healthz
    site/security.txt        — /.well-known/security.txt

The mirror updates on every push via .github/workflows/pages.yml, completely
independent of any hosting provider's build system.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"

sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402

CAPTURES: list[tuple[str, str]] = [
    ("/healthz", "api/healthz.json"),
    ("/api/summary", "api/summary.json"),
    ("/api/corpus", "api/corpus.json"),
    ("/api/gate?generation=g0", "api/gate-g0.json"),
    ("/api/gate?generation=g1", "api/gate-g1.json"),
    ("/api/gate?generation=g2", "api/gate-g2.json"),
    ("/passport.json", "api/passport.json"),
    ("/.well-known/security.txt", "api/security.txt"),
]


def main() -> int:
    SITE.mkdir(parents=True, exist_ok=True)
    (SITE / "api").mkdir(exist_ok=True)
    client = TestClient(app)

    ok = 0
    for path, out in CAPTURES:
        r = client.get(path)
        target = SITE / out
        if r.status_code != 200:
            print(f"✗ {path} -> {r.status_code}")
            continue
        target.write_bytes(r.content)
        ok += 1
        print(f"  ✓ {out} ({len(r.content)} bytes)")

    index = SITE / "index.html"
    if not index.exists():
        print("✗ site/index.html missing (must be committed)")
        return 2

    print(f"✅ static mirror refreshed: {ok}/{len(CAPTURES)} endpoints -> {SITE}")
    return 0 if ok == len(CAPTURES) else 1


if __name__ == "__main__":
    sys.exit(main())
