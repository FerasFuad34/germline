# AB-000086 — binutils-gdb: Global-buffer-overflow READ 8 in fuzz_disassemble

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `binutils-gdb` |
| Class / CWE | `memory-safety` / CWE-119 |
| Sanitizer | `asan` |
| Crash type | `Global-buffer-overflow READ 8` |
| Severity | Medium |
| Fixed in | [66a66a17f489](https://github.com/bminor/binutils-gdb/commit/66a66a17f489a4ffc614a31855e8d6f516e24640) |
| Upstream report | https://issues.oss-fuzz.com/issues/42479120 |
| Dataset | ARVO localId `42479120` |

## What this antibody guards

This is the historical vulnerability **Global-buffer-overflow READ 8** in `binutils-gdb`
(fuzz target: `fuzz_disassemble`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42479120-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42479120-fix arvo
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
