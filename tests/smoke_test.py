#!/usr/bin/env python3
"""Smoke tests for the GERMLINE web service (run in CI and locally)."""
import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient

APP = Path(__file__).parent.parent / "app" / "main.py"
spec = importlib.util.spec_from_file_location("germline_app", APP)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

c = TestClient(mod.app)

# health & pages
assert c.get("/healthz").json()["ok"] is True
assert c.get("/").status_code == 200, "landing page"
assert c.get("/demo").status_code == 200, "demo page"
assert c.get("/passport.json").status_code == 200, "passport.json"
assert c.get("/.well-known/security.txt").status_code == 200, "security.txt"

# immune gate semantics
g2 = c.get("/api/gate", params={"generation": "g2"}).json()
assert g2["immunity"]["immune_parity"] is True, "g2 must inherit full immunity"
assert g2["immunity"]["inherited_coverage_pct"] == 100.0

g1 = c.get("/api/gate", params={"generation": "g1"}).json()
assert g1["immunity"]["immune_parity"] is False, "g1 must show immune amnesia"
assert g1["immunity"]["failed"] >= 1

g0 = c.get("/api/gate", params={"generation": "g0"}).json()
assert g0["immunity"]["role"] == "reference", "g0 is the reference generation"

# every passport is signed
for p in c.get("/api/passports").json()["passports"]:
    assert p["attestation"]["signature"].startswith("sha256:")

print("smoke tests: ALL PASS ✅")
