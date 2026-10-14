# AB-000055 — curl: Use-of-uninitialized-value in curl_fuzzer_pop3

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `curl` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [84ced9389e1a](https://github.com/curl/curl/commit/84ced9389e1a7f576812e0675b37056331c4dbcd) |
| Upstream report | https://issues.oss-fuzz.com/issues/42477426 |
| Dataset | ARVO localId `42477426` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `curl`
(fuzz target: `curl_fuzzer_pop3`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42477426-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42477426-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`WARNING: MemorySanitizer` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
