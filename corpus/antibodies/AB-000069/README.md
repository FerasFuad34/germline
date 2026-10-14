# AB-000069 — ghostpdl: UNKNOWN READ in gstoraster_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ghostpdl` |
| Class / CWE | `memory-safety` / — |
| Sanitizer | `asan` |
| Crash type | `UNKNOWN READ` |
| Severity | Medium |
| Fixed in | [748edd2fd75c](https://cgit.ghostscript.com/ghostpdl.git748edd2fd75c684d63486eded71ad20254de6f4c) |
| Upstream report | https://issues.oss-fuzz.com/issues/42483325 |
| Dataset | ARVO localId `42483325` |

## What this antibody guards

This is the historical vulnerability **UNKNOWN READ** in `ghostpdl`
(fuzz target: `gstoraster_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42483325-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42483325-fix arvo
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
