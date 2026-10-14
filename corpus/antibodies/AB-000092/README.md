# AB-000092 — freetype2: Heap-buffer-overflow READ 8 in ftfuzzer

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `freetype2` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 8` |
| Severity | Medium |
| Fixed in | [e9a154e70015](https://github.com/freetype/freetype2/commit/e9a154e70015e602d695d65a588ecb38f5bb38cc) |
| Upstream report | https://issues.oss-fuzz.com/issues/42499092 |
| Dataset | ARVO localId `42499092` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 8** in `freetype2`
(fuzz target: `ftfuzzer`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42499092-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42499092-fix arvo
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
