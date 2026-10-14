# AB-000071 — ghostpdl: Stack-use-after-return WRITE 8 in gstoraster_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ghostpdl` |
| Class / CWE | `memory-safety` / CWE-562 |
| Sanitizer | `asan` |
| Crash type | `Stack-use-after-return WRITE 8` |
| Severity | Medium |
| Fixed in | [20610dc28ee3](https://cgit.ghostscript.com/ghostpdl.git20610dc28ee3cf7e64ad46f11e9b96fb3befba00) |
| Upstream report | https://issues.oss-fuzz.com/issues/42496125 |
| Dataset | ARVO localId `42496125` |

## What this antibody guards

This is the historical vulnerability **Stack-use-after-return WRITE 8** in `ghostpdl`
(fuzz target: `gstoraster_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42496125-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42496125-fix arvo
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
