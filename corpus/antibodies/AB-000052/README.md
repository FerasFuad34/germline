# AB-000052 — curl: UNKNOWN READ in curl_fuzzer_ftp

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `curl` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `asan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [f3ce38739fa4](https://github.com/curl/curl/commit/f3ce38739fa49008e36959aa8189c01ab1bad5b5) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472402 |
| Dataset | ARVO localId `42472402` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `curl`
(fuzz target: `curl_fuzzer_ftp`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42472402-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472402-fix arvo
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
