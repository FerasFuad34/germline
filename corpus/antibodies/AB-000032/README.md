# AB-000032 — imagemagick: Heap-buffer-overflow READ 1 in ping_jps_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 1` |
| Severity | Medium |
| Fixed in | [9177b7b3c278](https://github.com/imagemagick/imagemagick/commit/9177b7b3c2789c6196e7272e97893d9f7d3991f2) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472424 |
| Dataset | ARVO localId `42472424` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 1** in `imagemagick`
(fuzz target: `ping_jps_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42472424-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472424-fix arvo
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
