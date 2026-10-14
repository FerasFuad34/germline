# AB-000098 — zlib: Use-of-uninitialized-value in example_dict_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `zlib` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [981ee7570ad9](https://github.com/madler/zlib/commit/981ee7570ad98a3cf1ae74d737e2ee619ed79171) |
| Upstream report | https://issues.oss-fuzz.com/issues/42514310 |
| Dataset | ARVO localId `42514310` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `zlib`
(fuzz target: `example_dict_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42514310-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42514310-fix arvo
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
