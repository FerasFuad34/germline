# AB-000073 — php-src: Use-of-uninitialized-value in php-fuzz-exif

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `php-src` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [9ed82b1f7b17](https://github.com/php/php-src/commit/9ed82b1f7b17bf505fa22944185631e3e8156cf0) |
| Upstream report | https://issues.oss-fuzz.com/issues/42480628 |
| Dataset | ARVO localId `42480628` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `php-src`
(fuzz target: `php-fuzz-exif`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42480628-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42480628-fix arvo
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
