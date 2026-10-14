# AB-000068 — ghostpdl: Segv on unknown address in gstoraster_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ghostpdl` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `asan` |
| Crash type | `Segv on unknown address` |
| Severity | Medium |
| Fixed in | [d703f355af52](https://cgit.ghostscript.com/ghostpdl.gitd703f355af5292e61dcd641332e249873ab5fb8a) |
| Upstream report | https://issues.oss-fuzz.com/issues/42482668 |
| Dataset | ARVO localId `42482668` |

## What this antibody guards

This is the historical vulnerability **Segv on unknown address** in `ghostpdl`
(fuzz target: `gstoraster_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42482668-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42482668-fix arvo
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
