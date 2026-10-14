# AB-000081 — libarchive: Heap-buffer-overflow READ {*} in libarchive_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libarchive` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ {*}` |
| Severity | Medium |
| Fixed in | [39736c43bd73](https://github.com/libarchive/libarchive/commit/39736c43bd7374beedb372aa300ecf36c9fc4733) |
| Upstream report | https://issues.oss-fuzz.com/issues/42473801 |
| Dataset | ARVO localId `42473801` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ {*}** in `libarchive`
(fuzz target: `libarchive_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42473801-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42473801-fix arvo
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
