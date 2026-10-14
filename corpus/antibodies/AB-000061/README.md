# AB-000061 — wireshark: Global-buffer-overflow READ 4 in fuzzshark_ip_proto-udp

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `wireshark` |
| Class / CWE | `memory-safety` / CWE-119 |
| Sanitizer | `asan` |
| Crash type | `Global-buffer-overflow READ 4` |
| Severity | Medium |
| Fixed in | [895ad30b5a18](https://github.com/wireshark/wireshark/commit/9f472ea1501f8deb0109ea61feda6b8a5eec4f6a) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470895 |
| Dataset | ARVO localId `42470895` |

## What this antibody guards

This is the historical vulnerability **Global-buffer-overflow READ 4** in `wireshark`
(fuzz target: `fuzzshark_ip_proto-udp`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42470895-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470895-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`ERROR: AddressSanitizer` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
