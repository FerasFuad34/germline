# AB-000007 — libxml2: Index-out-of-bounds in libxml2_xml_read_memory_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `libxml2` |
| Class / CWE | `memory-safety` / CWE-129 |
| Sanitizer | `ubsan` |
| Crash type | `Index-out-of-bounds` |
| Severity | Medium |
| Fixed in | [474967241cdc](https://gitlab.gnome.org/GNOME/libxml2/-/commit/474967241cdcce6d3a2fd356079571eee794ec12) |
| Upstream report | https://issues.oss-fuzz.com/issues/42475106 |
| Dataset | ARVO localId `42475106` |

## What this antibody guards

This is the historical vulnerability **Index-out-of-bounds** in `libxml2`
(fuzz target: `libxml2_xml_read_memory_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   runtime error:
docker run --rm n132/arvo:42475106-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42475106-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`runtime error:` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
