# AB-000029 — imagemagick: Use-of-uninitialized-value in encoder_label_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [cfd2824f02b6](https://github.com/imagemagick/imagemagick/commit/cfd2824f02b6cee4ed6e105d50035c74142d9bf0) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470067 |
| Dataset | ARVO localId `42470067` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `imagemagick`
(fuzz target: `encoder_label_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42470067-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470067-fix arvo
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
