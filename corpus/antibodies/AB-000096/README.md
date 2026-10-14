# AB-000096 — libwebp: Negative-size-param in advanced_api_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libwebp` |
| Class / CWE | `memory-safety` / CWE-119 |
| Sanitizer | `asan` |
| Crash type | `Negative-size-param` |
| Severity | Medium |
| Fixed in | [277d30749f15](https://chromium.googlesource.com/webm/libwebp/+/277d30749f15d3fd99649c9347867ddc2fe4f32e%5E%21/) |
| Upstream report | https://issues.oss-fuzz.com/issues/42498407 |
| Dataset | ARVO localId `42498407` |

## What this antibody guards

This is the historical vulnerability **Negative-size-param** in `libwebp`
(fuzz target: `advanced_api_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42498407-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42498407-fix arvo
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
