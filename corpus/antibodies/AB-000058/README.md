# AB-000058 — curl: Heap-use-after-free READ 6 in curl_fuzzer_http

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `curl` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 6` |
| Severity | High |
| Fixed in | [02c6b984cb7a](https://github.com/curl/curl/commit/02c6b984cb7a2e01f290544a53a24d30fc7ab32e) |
| Upstream report | https://issues.oss-fuzz.com/issues/42478820 |
| Dataset | ARVO localId `42478820` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 6** in `curl`
(fuzz target: `curl_fuzzer_http`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42478820-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42478820-fix arvo
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
