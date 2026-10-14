# AB-000065 — wireshark: UNKNOWN READ in fuzzshark_ip

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `wireshark` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `ubsan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [d9231144b652](https://github.com/wireshark/wireshark/commit/d9231144b652362eaf62f8595df7d4886dbaf44d) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470973 |
| Dataset | ARVO localId `42470973` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `wireshark`
(fuzz target: `fuzzshark_ip`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   UndefinedBehaviorSanitizer:DEADLYSIGNAL
docker run --rm n132/arvo:42470973-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470973-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`UndefinedBehaviorSanitizer:DEADLYSIGNAL` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
