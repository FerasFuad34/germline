# AB-000057 — curl: Heap-buffer-overflow READ 1 in curl_fuzzer_smb

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `curl` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 1` |
| Severity | Medium |
| Fixed in | [65fda739ee35](https://github.com/curl/curl/commit/65fda739ee35c090b2e6d91229287de734f0fbae) |
| Upstream report | https://issues.oss-fuzz.com/issues/42477466 |
| Dataset | ARVO localId `42477466` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 1** in `curl`
(fuzz target: `curl_fuzzer_smb`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42477466-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42477466-fix arvo
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
