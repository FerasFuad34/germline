# AB-000039 — imagemagick: Heap-buffer-overflow READ 1 in ping_dng_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 1` |
| Severity | Medium |
| Fixed in | [58b1d87bef2b](https://github.com/imagemagick/imagemagick/commit/58b1d87bef2b8d7dbd7391091069a3c279ec5e85) |
| Upstream report | https://issues.oss-fuzz.com/issues/42474313 |
| Dataset | ARVO localId `42474313` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 1** in `imagemagick`
(fuzz target: `ping_dng_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42474313-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42474313-fix arvo
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
