# AB-000077 — libarchive: Heap-buffer-overflow WRITE 1 in libarchive_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libarchive` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow WRITE 1` |
| Severity | High |
| Fixed in | [b52dd6c9e4ef](https://github.com/libarchive/libarchive/commit/b52dd6c9e4ef7cf95c2a6ae5ab7ccac7f6d462a1) |
| Upstream report | https://issues.oss-fuzz.com/issues/42471116 |
| Dataset | ARVO localId `42471116` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow WRITE 1** in `libarchive`
(fuzz target: `libarchive_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42471116-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42471116-fix arvo
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
