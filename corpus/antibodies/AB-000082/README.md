# AB-000082 — gpac: Segv on unknown address in fuzz_parse

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `gpac` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `asan` |
| Crash type | `Segv on unknown address` |
| Severity | Medium |
| Fixed in | [b03c9f252526](https://github.com/gpac/gpac/commit/b03c9f252526bb42fbd1b87b9f5e339c3cf2390a) |
| Upstream report | https://issues.oss-fuzz.com/issues/42494317 |
| Dataset | ARVO localId `42494317` |

## What this antibody guards

This is the historical vulnerability **Segv on unknown address** in `gpac`
(fuzz target: `fuzz_parse`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42494317-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42494317-fix arvo
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
