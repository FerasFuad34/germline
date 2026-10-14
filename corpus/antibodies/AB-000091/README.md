# AB-000091 — freetype2: Heap-buffer-overflow WRITE 8 in ftfuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `freetype2` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow WRITE 8` |
| Severity | High |
| Fixed in | [edf401485450](https://github.com/freetype/freetype2/commit/edf40148545038d07a394082caa1b9155941f88f) |
| Upstream report | https://issues.oss-fuzz.com/issues/42490980 |
| Dataset | ARVO localId `42490980` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow WRITE 8** in `freetype2`
(fuzz target: `ftfuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42490980-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42490980-fix arvo
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
