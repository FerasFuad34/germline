# AB-000062 — wireshark: Index-out-of-bounds in fuzzshark_ip_proto-udp

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `wireshark` |
| Class / CWE | `memory-safety` / CWE-129 |
| Sanitizer | `ubsan` |
| Crash type | `Index-out-of-bounds` |
| Severity | Medium |
| Fixed in | [895ad30b5a18](https://github.com/wireshark/wireshark/commit/9f472ea1501f8deb0109ea61feda6b8a5eec4f6a) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470900 |
| Dataset | ARVO localId `42470900` |

## What this antibody guards

This is the historical vulnerability **Index-out-of-bounds** in `wireshark`
(fuzz target: `fuzzshark_ip_proto-udp`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   runtime error:
docker run --rm n132/arvo:42470900-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470900-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`runtime error:` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
