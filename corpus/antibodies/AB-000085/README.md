# AB-000085 — gpac: Stack-use-after-return WRITE 4 in fuzz_parse

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `gpac` |
| Class / CWE | `memory-safety` / CWE-562 |
| Sanitizer | `asan` |
| Crash type | `Stack-use-after-return WRITE 4` |
| Severity | Medium |
| Fixed in | [82396cfa523b](https://github.com/gpac/gpac/commit/82396cfa523b4b7ef16e720d6c353fc85d91841d) |
| Upstream report | https://issues.oss-fuzz.com/issues/42494354 |
| Dataset | ARVO localId `42494354` |

## What this antibody guards

This is the historical vulnerability **Stack-use-after-return WRITE 4** in `gpac`
(fuzz target: `fuzz_parse`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42494354-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42494354-fix arvo
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
