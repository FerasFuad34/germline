# AB-000072 — php-src: Heap-buffer-overflow READ 1 in php-fuzz-mbstring

**Status: 🟡 DRAFT** — generated from ARVO metadata; not yet double-checked on a Docker host.

| | |
|---|---|
| Project | `php-src` |
| Class / CWE | `memory-safety` / CWE-122 |
| Sanitizer | `asan` |
| Crash type | `Heap-buffer-overflow READ 1` |
| Severity | Medium |
| Fixed in | [1806ce9cb019](https://github.com/php/php-src/commit/1cde9e852879afe123945fe42e831a6715abb866) |
| Upstream report | https://issues.oss-fuzz.com/issues/42478840 |
| Dataset | ARVO localId `42478840` |

## What this antibody guards

This is the historical vulnerability **Heap-buffer-overflow READ 1** in `php-src`
(fuzz target: `php-fuzz-mbstring`). A descendant generation that reintroduces
this class of bug will be caught by replaying this antibody.

## Reproduce (requires Docker)

```bash
# Vulnerable build — expected to CRASH with:
#   ERROR: AddressSanitizer
docker run --rm n132/arvo:42478840-vul arvo

# Fixed build — expected to run clean:
docker run --rm n132/arvo:42478840-fix arvo
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
