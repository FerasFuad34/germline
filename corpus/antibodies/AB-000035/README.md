# AB-000035 — imagemagick: Index-out-of-bounds in ping_dng_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / CWE-129 |
| Sanitizer | `ubsan` |
| Crash type | `Index-out-of-bounds` |
| Severity | Medium |
| Fixed in | [df835cab0576](https://github.com/imagemagick/imagemagick/commit/df835cab05765a630227dc04fa2245a78fd2f204) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472890 |
| Dataset | ARVO localId `42472890` |

## What this antibody guards

This is the historical vulnerability **Index-out-of-bounds** in `imagemagick`
(fuzz target: `ping_dng_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   runtime error:
docker run --rm n132/arvo:42472890-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472890-fix arvo
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
