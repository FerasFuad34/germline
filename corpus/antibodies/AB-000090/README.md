# AB-000090 — freetype2: Use-of-uninitialized-value in pdf_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `freetype2` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [94ebc248653e](https://github.com/freetype/freetype2/commit/94ebc248653ede802b2bfbf6219e17f487fab3ff) |
| Upstream report | https://issues.oss-fuzz.com/issues/42475209 |
| Dataset | ARVO localId `42475209` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `freetype2`
(fuzz target: `pdf_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42475209-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42475209-fix arvo
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
