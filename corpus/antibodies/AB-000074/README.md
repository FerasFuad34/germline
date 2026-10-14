# AB-000074 — php-src: Use-of-uninitialized-value in php-fuzz-mbstring

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `php-src` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [b5e004379647](https://github.com/php/php-src/commit/24ccbb00573445b0df5e940a77e7363ace3c31f3) |
| Upstream report | https://issues.oss-fuzz.com/issues/42480756 |
| Dataset | ARVO localId `42480756` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `php-src`
(fuzz target: `php-fuzz-mbstring`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42480756-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42480756-fix arvo
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
