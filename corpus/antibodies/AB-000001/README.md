# AB-000001 — libxml2: Use-of-uninitialized-value in libxml2_xml_read_memory_fuzzer

**Status: 🟢 VALIDATED** — double-checked on a real runner: crashes on the vulnerable build, stays clean on the fixed build (see `../../VERIFICATION.md`).

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-457 |
| Sanitizer | `msan` |
| Crash type | `Use-of-uninitialized-value` |
| Severity | Medium |
| Fixed in | [074180119fc9](https://gitlab.gnome.org/GNOME/libxml2/-/commit/074180119fc90d5fd04ef9e8a5ee1910d6f9ad8e) |
| Upstream report | https://issues.oss-fuzz.com/issues/42470114 |
| Dataset | ARVO localId `42470114` |

## What this antibody guards

This is the historical vulnerability **Use-of-uninitialized-value** in `libxml2`
(fuzz target: `libxml2_xml_read_memory_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   WARNING: MemorySanitizer
docker run --rm n132/arvo:42470114-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42470114-fix arvo
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
