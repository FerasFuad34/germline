# AB-000097 — libwebp: UNKNOWN READ in jpegsave_file_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libwebp` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `asan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [e542fc7a8a26](https://chromium.googlesource.com/webm/libwebp/+/e542fc7a8a264562ec678970f64d6ad12a7b554a%5E%21/) |
| Upstream report | https://issues.oss-fuzz.com/issues/42500241 |
| Dataset | ARVO localId `42500241` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `libwebp`
(fuzz target: `jpegsave_file_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42500241-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42500241-fix arvo
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
