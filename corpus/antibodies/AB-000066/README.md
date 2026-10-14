# AB-000066 — ghostpdl: Null-dereference READ in gstoraster_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ghostpdl` |
| Class / CWE | `memory-safety` / CWE-476 |
| Sanitizer | `asan` |
| Crash type | `Null-dereference READ` |
| Severity | Medium |
| Fixed in | [77f79475fd04](https://cgit.ghostscript.com/ghostpdl.git77f79475fd0419d16f1efe7812a44a9720fef10b) |
| Upstream report | https://issues.oss-fuzz.com/issues/42477726 |
| Dataset | ARVO localId `42477726` |

## What this antibody guards

This is the historical vulnerability **Null-dereference READ** in `ghostpdl`
(fuzz target: `gstoraster_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42477726-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42477726-fix arvo
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
