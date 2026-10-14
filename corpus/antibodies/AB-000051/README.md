# AB-000051 — curl: Null-dereference READ in curl_fuzzer_http

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `curl` |
| Class / CWE | `memory-safety` / CWE-476 |
| Sanitizer | `ubsan` |
| Crash type | `Null-dereference READ` |
| Severity | Medium |
| Fixed in | [78d5302b5c05](https://github.com/curl/curl/commit/78d5302b5c05a49ecfa2ee8b8f1a21a2902357d3) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470017 |
| Dataset | ARVO localId `42470017` |

## What this antibody guards

This is the historical vulnerability **Null-dereference READ** in `curl`
(fuzz target: `curl_fuzzer_http`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   UndefinedBehaviorSanitizer:DEADLYSIGNAL
docker run --rm n132/arvo:42470017-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470017-fix arvo
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
