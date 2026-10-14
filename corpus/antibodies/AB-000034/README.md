# AB-000034 — imagemagick: UNKNOWN READ in encoder_ept3_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `imagemagick` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `msan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [07eebcd72f45](https://github.com/imagemagick/imagemagick/commit/07eebcd72f45c8fd7563d3f9ec5d2bed48f65f36) |
| Upstream report | https://issues.oss-fuzz.com/issues/42472880 |
| Dataset | ARVO localId `42472880` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `imagemagick`
(fuzz target: `encoder_ept3_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   MemorySanitizer:DEADLYSIGNAL
docker run --rm n132/arvo:42472880-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42472880-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`MemorySanitizer:DEADLYSIGNAL` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
