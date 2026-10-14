# AB-000100 — libtiff: Use-of-uninitialized-value in tiff_read_rgba_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libtiff` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [0f013e5b5a55](https://gitlab.com/libtiff/libtiff/-/commit/0f013e5b5a550606298fb50c3bb90920a7da76fc) |
| Upstream report | https://issues.oss-fuzz.com/issues/42489909 |
| Dataset | ARVO localId `42489909` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `libtiff`
(fuzz target: `tiff_read_rgba_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42489909-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42489909-fix arvo
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
