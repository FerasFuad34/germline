# AB-000075 — php-src: Heap-use-after-free READ 4 in php-fuzz-mbstring

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `php-src` |
| Class / CWE | `memory-safety` / CWE-416 |
| Sanitizer | `asan` |
| Crash type | `Heap-use-after-free READ 4` |
| Severity | High |
| Fixed in | [fd08f062ae5a](https://github.com/php/php-src/commit/8dd91f52a52f0804970fe65738fade9be4bafd54) |
| Upstream report | https://issues.oss-fuzz.com/issues/42481412 |
| Dataset | ARVO localId `42481412` |

## What this antibody guards

This is the historical vulnerability **Heap-use-after-free READ 4** in `php-src`
(fuzz target: `php-fuzz-mbstring`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42481412-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42481412-fix arvo
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
