# AB-000067 — ghostpdl: Heap-use-after-free READ 8 in gstoraster_fuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `ghostpdl` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 8` |
| Severity | High |
| Fixed in | [6fc5cbc5bc57](https://cgit.ghostscript.com/ghostpdl.gitf5b7acb59c4f2e88591aab9f355813e0b7b68db5) |
| Upstream report | https://issues.oss-fuzz.com/issues/42481819 |
| Dataset | ARVO localId `42481819` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 8** in `ghostpdl`
(fuzz target: `gstoraster_fuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   Heap-use-after-free READ 8
docker run --rm n132/arvo:42481819-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42481819-fix arvo
```

## Double-check (canonical validation)

```bash
./double-check.sh          # verdict: verified / mismatch / environment-error
./double-check.sh --json   # machine-readable verdict
```

The antibody is only **validated** when vulnerable crashes with marker
`Heap-use-after-free READ 8` and the fixed build stays clean.

---
*Corpus policy: fixed & publicly disclosed vulnerabilities only. Upstream data: OSS-Fuzz, curated by ARVO (CC-BY-4.0).*
